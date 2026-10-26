"""Reconcile the full worked workbook with source records using only stdlib.

Checks read saved OOXML values and formulas. They independently price and group
the original CSVs rather than trusting the workbook builder or answer exports.
"""

from collections import defaultdict
import csv
from datetime import datetime, timedelta
from decimal import Decimal
import json
from pathlib import Path
import posixpath
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "DATA/TRACKS/portfolio-project"
SOLUTION = ROOT / "SOLUTION/TRACKS/portfolio-project/mru-portfolio-project-solution.xlsx"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "c": "http://schemas.openxmlformats.org/drawingml/2006/chart"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
D = Decimal
ZERO = D(0)
RATE = D(50)
TOLERANCE = D("0.0000001")
SOURCE_SHEETS = {
    "work_log": "Raw Work Log", "ai_usage": "Raw AI Usage",
    "model_pricing": "Model Pricing", "campaigns": "Campaign Inputs",
}
SOURCE_KEYS = {
    "work_log": "work_item_id", "ai_usage": "usage_id",
    "model_pricing": "model", "campaigns": "campaign_id",
}
NUMERIC_SOURCE_FIELDS = {
    "baseline_hours", "actual_hours", "rework_hours", "input_tokens",
    "output_tokens", "input_rate_usd_per_million", "output_rate_usd_per_million",
    "campaign_revenue_usd", "other_campaign_cost_usd",
}
DATE_FIELDS = {"completion_date", "usage_date"}


def column_number(label):
    result = 0
    for character in label:
        result = result * 26 + ord(character) - ord("A") + 1
    return result


def column_label(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result


def read_workbook(path):
    with ZipFile(path) as archive:
        names = archive.namelist()
        if any(name.startswith("xl/externalLinks/") or name.lower().endswith("vbaproject.bin") for name in names):
            raise AssertionError("Solution must not require external workbooks or macros")
        if "xl/connections.xml" in names:
            raise AssertionError("Solution must not require a data connection")
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        props = workbook.find("s:workbookPr", NS)
        epoch = datetime(1904, 1, 1) if props is not None and props.get("date1904") in ("1", "true") else datetime(1899, 12, 30)
        shared = []
        if "xl/sharedStrings.xml" in names:
            shared = ["".join(node.itertext()) for node in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        relationships = {
            node.get("Id"): node.get("Target")
            for node in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        }
        sheets = {}
        for sheet in workbook.findall("s:sheets/s:sheet", NS):
            target = relationships[sheet.get(REL)]
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            cells = {}
            for cell in ET.fromstring(archive.read(target)).findall("s:sheetData/s:row/s:c", NS):
                kind = cell.get("t", "n")
                node = cell.find("s:v", NS)
                formula = cell.find("s:f", NS)
                if kind == "e":
                    raise AssertionError(f"Error in {sheet.get('name')}!{cell.get('r')}: {node.text}")
                if kind == "inlineStr":
                    value = "".join(cell.find("s:is", NS).itertext())
                elif node is None or node.text is None:
                    value = None
                elif kind == "s":
                    value = shared[int(node.text)]
                elif kind == "n":
                    value = D(node.text)
                else:
                    value = node.text
                if isinstance(value, D) and not value.is_finite():
                    raise AssertionError(f"Nonfinite value in {sheet.get('name')}!{cell.get('r')}")
                if formula is not None and value is None:
                    raise AssertionError(f"Missing saved formula value in {sheet.get('name')}!{cell.get('r')}")
                cells[cell.get("r")] = {"value": value, "formula": None if formula is None else formula.text}
            sheets[sheet.get("name")] = cells
        return sheets, epoch


def table(sheets, name, required_headers, key, row_count=None):
    """Locate a table by column meanings, independent of its presentation row."""
    by_row = defaultdict(dict)
    for address, cell in sheets[name].items():
        match = re.fullmatch(r"([A-Z]+)(\d+)", address)
        by_row[int(match[2])][column_number(match[1])] = cell
    candidates = [
        row for row, cells in by_row.items()
        if set(required_headers).issubset({cell["value"] for cell in cells.values() if isinstance(cell["value"], str)})
    ]
    if len(candidates) != 1:
        raise AssertionError(f"Expected one {name} table with {required_headers}, found {candidates}")
    header_row = candidates[0]
    columns = {cell["value"]: column for column, cell in by_row[header_row].items() if isinstance(cell["value"], str)}
    rows = []
    row_number = header_row + 1
    while by_row.get(row_number, {}).get(columns[key], {}).get("value") is not None and (row_count is None or len(rows) < row_count):
        rows.append({field: by_row[row_number].get(column, {"value": None, "formula": None}) for field, column in columns.items()})
        row_number += 1
    return rows


def unique(rows, key):
    result = {}
    for row in rows:
        if row[key] in result and row != result[row[key]]:
            raise AssertionError(f"Conflicting source duplicate {key}: {row[key]}")
        result.setdefault(row[key], row)
    return list(result.values())


def sum_field(rows, field):
    return sum((D(row[field]) for row in rows), ZERO)


def expected_model(source):
    """Price each prompt first, then attach one prompt aggregate per task."""
    prices = {row["model"]: row for row in unique(source["model_pricing"], "model")}
    work = unique(source["work_log"], "work_item_id")
    tasks = {row["work_item_id"]: row for row in work}
    usage = []
    grouped = defaultdict(list)
    for original in unique(source["ai_usage"], "usage_id"):
        row = dict(original)
        price = prices[row["model"]]
        task = tasks[row["work_item_id"]]
        if row["campaign_id"] != task["campaign_id"] or row["usage_date"] > task["completion_date"]:
            raise AssertionError("Source prompt links disagree")
        for side in ("input", "output"):
            row[f"{side}_rate_usd_per_million"] = D(price[f"{side}_rate_usd_per_million"])
            row[f"{side}_cost_usd"] = D(row[f"{side}_tokens"]) * row[f"{side}_rate_usd_per_million"] / D(1_000_000)
        row["total_tokens"] = D(row["input_tokens"]) + D(row["output_tokens"])
        row["ai_cost_usd"] = row["input_cost_usd"] + row["output_cost_usd"]
        usage.append(row)
        grouped[row["work_item_id"]].append(row)
    clean = []
    prompt_totals = []
    for original in work:
        prompts = grouped[original["work_item_id"]]
        if len({row["product"] for row in prompts}) != 1 or len({row["model"] for row in prompts}) != 1:
            raise AssertionError("Source task has multiple products or models")
        summary = {field: prompts[0][field] for field in ("work_item_id", "campaign_id", "product", "model")}
        summary.update({field: sum_field(prompts, field) for field in (
            "input_tokens", "output_tokens", "total_tokens", "input_cost_usd", "output_cost_usd", "ai_cost_usd",
        )})
        summary["prompt_count"] = D(len(prompts))
        summary["first_attempt_prompts"] = D(sum(row["prompt_reason"] == "First attempt" for row in prompts))
        summary["correction_prompts"] = D(sum(row["prompt_reason"] == "Correction" for row in prompts))
        summary["followup_prompts"] = D(sum(row["prompt_reason"] == "Followup" for row in prompts))
        prompt_totals.append(summary)
        row = dict(original, department=original["department"].strip().title(), **{key: value for key, value in summary.items() if key not in original})
        row["hours_saved"] = D(row["baseline_hours"]) - D(row["actual_hours"])
        row["time_value_usd"] = row["hours_saved"] * RATE
        row["net_ai_value_usd"] = row["time_value_usd"] - row["ai_cost_usd"]
        clean.append(row)
    return clean, usage, prompt_totals


def totals(rows):
    result = {field: sum_field(rows, field) for field in (
        "input_tokens", "output_tokens", "total_tokens", "input_cost_usd", "output_cost_usd",
        "ai_cost_usd", "prompt_count", "correction_prompts", "followup_prompts", "baseline_hours",
        "actual_hours", "rework_hours", "hours_saved", "time_value_usd", "net_ai_value_usd",
    )}
    result["tasks"] = D(len(rows))
    result["ai_roi"] = result["net_ai_value_usd"] / result["ai_cost_usd"] if result["ai_cost_usd"] else None
    result["cost_per_prompt_usd"] = result["ai_cost_usd"] / result["prompt_count"] if result["prompt_count"] else None
    result["rework_share"] = result["rework_hours"] / result["actual_hours"] if result["actual_hours"] else None
    result["correction_share"] = result["correction_prompts"] / result["prompt_count"] if result["prompt_count"] else None
    result["template_tasks"] = D(sum(row["prompt_template_used"] == "Yes" for row in rows))
    result["changed_brief_tasks"] = D(sum(row["brief_changed"] == "Yes" for row in rows))
    result["positive_net_value_tasks"] = D(sum(row["net_ai_value_usd"] > 0 for row in rows))
    result["negative_net_value_tasks"] = D(sum(row["net_ai_value_usd"] < 0 for row in rows))
    result["net_ai_value_lower20_usd"] = (result["baseline_hours"] * D("0.8") - result["actual_hours"]) * RATE - result["ai_cost_usd"]
    result["net_ai_value_higher20_usd"] = (result["baseline_hours"] * D("1.2") - result["actual_hours"]) * RATE - result["ai_cost_usd"]
    for output, field in [("corrections_per_task", "correction_prompts"), ("ai_cost_per_task_usd", "ai_cost_usd"), ("hours_saved_per_task", "hours_saved")]:
        result[output] = result[field] / len(rows) if rows else None
    return result


class PortfolioSolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = {}
        cls.headers = {}
        for name in SOURCE_SHEETS:
            with (SOURCE / f"{name}.csv").open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                cls.headers[name] = reader.fieldnames
                cls.source[name] = list(reader)
        cls.clean, cls.usage, cls.prompt_totals = expected_model(cls.source)
        cls.sheets, cls.epoch = read_workbook(SOLUTION)

    def rows(self, sheet, headers, key, row_count=None):
        return table(self.sheets, sheet, headers, key, row_count)

    def assert_numeric(self, cell, expected, context, formula=False):
        self.assertIsInstance(cell["value"], D, context)
        self.assertTrue(cell["value"].is_finite(), context)
        self.assertLessEqual(abs(cell["value"] - D(expected)), TOLERANCE, (context, cell["value"], expected))
        if formula:
            self.assertTrue(cell["formula"], (context, "Expected a formula rather than a stored answer"))

    def assert_source_rows(self, sheet, source_name, expected):
        rows = self.rows(sheet, self.headers[source_name], SOURCE_KEYS[source_name])
        self.assertEqual(len(rows), len(expected), sheet)
        for actual, source in zip(rows, expected):
            for field in self.headers[source_name]:
                cell = actual[field]
                context = (sheet, source[SOURCE_KEYS[source_name]], field)
                self.assertIsNone(cell["formula"], (context, "Original input must stay intact"))
                if field in DATE_FIELDS:
                    self.assertIsInstance(cell["value"], D, context)
                    date = (self.epoch + timedelta(days=float(cell["value"]))).strftime("%Y-%m-%d")
                    self.assertEqual(date, source[field], context)
                elif field in NUMERIC_SOURCE_FIELDS:
                    self.assert_numeric(cell, D(source[field]), context)
                else:
                    self.assertEqual(cell["value"], source[field], context)

    def test_preserves_all_raw_sources_and_clean_task_grain(self):
        self.assertEqual(list(self.sheets), [
            "Solution", "Campaigns", "Mix", "Workflow", "Daily Usage", "Tasks",
            "Prompt Totals", "Priced Usage", "Raw Work Log", "Raw AI Usage",
            "Model Pricing", "Campaign Inputs", "Preparation", "Data Dictionary",
        ])
        for source_name, sheet in SOURCE_SHEETS.items():
            self.assert_source_rows(sheet, source_name, self.source[source_name])
        self.assertEqual(len(self.source["work_log"]), 242)
        self.assertEqual(len(self.clean), 240)
        self.assertEqual(len(self.usage), 3360)
        self.assert_source_rows("Tasks", "work_log", self.clean)
        self.assertEqual({row["department"] for row in self.clean}, {
            "Analytics", "Content", "Creative", "Marketing Operations",
        })

    def test_every_priced_prompt_preserves_source_and_uses_its_model_rate(self):
        self.assert_source_rows("Priced Usage", "ai_usage", self.usage)
        calculated = (
            "input_rate_usd_per_million", "output_rate_usd_per_million", "total_tokens",
            "input_cost_usd", "output_cost_usd", "ai_cost_usd",
        )
        actual = self.rows("Priced Usage", ["usage_id", *calculated], "usage_id")
        for row, expected in zip(actual, self.usage):
            for field in calculated:
                self.assert_numeric(row[field], expected[field], ("Priced Usage", expected["usage_id"], field), formula=True)
        self.assertEqual(len({row["usage_id"]["value"] for row in actual}), 3360)

    def test_prompt_totals_join_once_per_task_and_task_formulas_match_source(self):
        fields = (
            "input_tokens", "output_tokens", "total_tokens", "prompt_count",
            "input_cost_usd", "output_cost_usd", "ai_cost_usd", "first_attempt_prompts",
            "followup_prompts", "correction_prompts",
        )
        actual = self.rows("Prompt Totals", ["work_item_id", *fields], "work_item_id")
        self.assertEqual(len(actual), 240)
        self.assertEqual(len({row["work_item_id"]["value"] for row in actual}), 240)
        by_task = {row["work_item_id"]["value"]: row for row in actual}
        for expected in self.prompt_totals:
            row = by_task[expected["work_item_id"]]
            for field in ("campaign_id", "product", "model"):
                self.assertEqual(row[field]["value"], expected[field])
            for field in fields:
                self.assert_numeric(row[field], expected[field], ("Prompt Totals", expected["work_item_id"], field), formula=True)
        calculated = (*fields, "hours_saved", "time_value_usd", "net_ai_value_usd")
        actual = self.rows("Tasks", ["work_item_id", *calculated], "work_item_id")
        for row, expected in zip(actual, self.clean):
            for field in ("product", "model"):
                self.assertEqual(row[field]["value"], expected[field])
            for field in calculated:
                self.assert_numeric(row[field], expected[field], ("Tasks", expected["work_item_id"], field), formula=True)
        self.assertEqual(sum((row["actual_hours"]["value"] for row in actual), ZERO), D(800))
        self.assertEqual(sum((row["baseline_hours"]["value"] for row in actual), ZERO), D(920))
        self.assertEqual(sum((row["prompt_count"]["value"] for row in actual), ZERO), D(3360))

    def test_dashboard_source_records_match_the_workbook_source(self):
        with (ROOT / "TECHNICAL/dashboard/demo-data.json").open(encoding="utf-8") as handle:
            demo = json.load(handle, parse_float=D, parse_int=D)
        for name, rows in self.source.items():
            if name == "work_log":
                rows = [{field: row[field] for field in self.headers[name]} for row in self.clean]
            self.assertEqual(len(demo[name]), len(rows), name)
            key = SOURCE_KEYS[name]
            displayed_rows = {row[key]: row for row in demo[name]}
            self.assertEqual(set(displayed_rows), {row[key] for row in rows}, name)
            for source in rows:
                displayed = displayed_rows[source[key]]
                self.assertEqual(set(displayed), set(source), name)
                for field, value in source.items():
                    expected = D(value) if field in NUMERIC_SOURCE_FIELDS else value
                    self.assertEqual(displayed[field], expected, (name, source[SOURCE_KEYS[name]], field))

    def test_excel_answers_match_the_actual_dashboard_calculations(self):
        script = """
            import fs from 'node:fs';
            import {prepare, summarize, selectTasks, wholeCampaigns, dailyUsage}
                from './TECHNICAL/dashboard/metrics.mjs';
            const model = prepare(JSON.parse(fs.readFileSync('./TECHNICAL/dashboard/demo-data.json', 'utf8')));
            const selections = {ALL: model.tasks, FOCAL: selectTasks(model.tasks, {campaign_id: ['C001', 'C002']})};
            for (const c of model.campaigns) selections[c.campaign_id] = selectTasks(model.tasks, {campaign_id: c.campaign_id});
            const summaries = Object.fromEntries(Object.entries(selections).map(([key, tasks]) => [key, {
                ...summarize(tasks), lower: summarize(tasks, -20).value, higher: summarize(tasks, 20).value,
            }]));
            const daily = model.campaigns.flatMap(c => dailyUsage(model, selections[c.campaign_id])
                .map(row => ({...row, campaign_id: c.campaign_id})));
            process.stdout.write(JSON.stringify({summaries, financial: wholeCampaigns(model), daily}));
        """
        process = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT,
                                 capture_output=True, text=True, check=True, timeout=30)
        dashboard = json.loads(process.stdout, parse_float=D, parse_int=D)
        fields = {
            "tasks": "tasks", "inputTokens": "input_tokens", "outputTokens": "output_tokens",
            "inputCost": "input_cost_usd", "outputCost": "output_cost_usd", "cost": "ai_cost_usd",
            "baseline": "baseline_hours", "actual": "actual_hours", "rework": "rework_hours",
            "saved": "hours_saved", "value": "net_ai_value_usd", "prompts": "prompt_count",
            "costPerPrompt": "cost_per_prompt_usd", "corrections": "correction_prompts",
            "lower": "net_ai_value_lower20_usd", "higher": "net_ai_value_higher20_usd",
        }
        campaigns = self.rows("Campaigns", ["campaign_id", "net_ai_value_usd", "campaign_result_usd"], "campaign_id")
        by_campaign = {row["campaign_id"]["value"]: row for row in campaigns}
        for key, totals in dashboard["summaries"].items():
            row = by_campaign[key]
            for dashboard_field, excel_field in fields.items():
                self.assert_numeric(row[excel_field], totals[dashboard_field], ("Dashboard", key, excel_field))
            self.assert_numeric(row["ai_roi"], totals["roi"] / 100, ("Dashboard", key, "ai_roi"))
            self.assert_numeric(row["rework_share"], totals["reworkShare"] / 100, ("Dashboard", key, "rework_share"))
        for financial in dashboard["financial"]:
            key = financial["campaign_id"]
            self.assert_numeric(by_campaign[key]["campaign_result_usd"], financial["result"], ("Dashboard", key, "campaign_result_usd"))
        daily = self.rows("Daily Usage", ["usage_date", "campaign_id", "ai_cost_usd"], "usage_date")
        by_day = {
            ((self.epoch + timedelta(days=float(row["usage_date"]["value"]))).strftime("%Y-%m-%d"), row["campaign_id"]["value"]): row
            for row in daily
        }
        self.assertEqual(len(by_day), len(dashboard["daily"]))
        for expected in dashboard["daily"]:
            key = (expected["date"], expected["campaign_id"])
            row = by_day[key]
            for dashboard_field, excel_field in [("inputCost", "input_cost_usd"), ("outputCost", "output_cost_usd"), ("cost", "ai_cost_usd"), ("prompts", "prompt_count")]:
                self.assert_numeric(row[excel_field], expected[dashboard_field], ("Dashboard", *key, excel_field))

    def assert_summary(self, actual, rows, context):
        expected = totals(rows)
        fields = (
            "tasks", "input_tokens", "output_tokens", "total_tokens", "input_cost_usd", "output_cost_usd",
            "ai_cost_usd", "prompt_count", "cost_per_prompt_usd", "baseline_hours", "actual_hours", "hours_saved",
            "time_value_usd", "net_ai_value_usd", "ai_roi", "rework_hours", "rework_share", "correction_prompts",
            "correction_share", "template_tasks", "changed_brief_tasks", "positive_net_value_tasks", "negative_net_value_tasks",
        )
        self.assertTrue(set(fields).issubset(actual), (context, set(fields) - set(actual)))
        for field in fields:
            self.assert_numeric(actual[field], expected[field], (*context, field), formula=True)
        return expected

    def test_campaign_answers_company_totals_profit_and_sensitivity_reconcile(self):
        actual = self.rows("Campaigns", ["campaign_id", "net_ai_value_usd", "campaign_result_usd"], "campaign_id")
        self.assertEqual([row["campaign_id"]["value"] for row in actual], ["C001", "C002", "C003", "C004", "ALL", "FOCAL"])
        # Totals stay outside the sortable Excel table so a normal sort cannot
        # move them into the four campaign rows used by readers.
        native_tables = []
        with ZipFile(SOLUTION) as archive:
            for name in archive.namelist():
                if not name.endswith(".xml"):
                    continue
                root = ET.fromstring(archive.read(name))
                if root.tag != f"{{{NS['s']}}}table":
                    continue
                fields = [column.get("name") for column in root.findall("s:tableColumns/s:tableColumn", NS)]
                if {"campaign_id", "campaign_name", "campaign_result_usd"}.issubset(fields):
                    native_tables.append((root, fields))
        self.assertEqual(len(native_tables), 1)
        native_table, fields = native_tables[0]
        match = re.fullmatch(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", native_table.get("ref"))
        self.assertIsNotNone(match)
        first_column, first_row, _, last_row = match.groups()
        key_column = column_label(column_number(first_column) + fields.index("campaign_id"))
        ids_in_sortable_table = [self.sheets["Campaigns"][f"{key_column}{row}"]["value"]
                                 for row in range(int(first_row) + 1, int(last_row) + 1)]
        self.assertEqual(ids_in_sortable_table, ["C001", "C002", "C003", "C004"])
        for row in actual:
            key = row["campaign_id"]["value"]
            ids = {"C001", "C002", "C003", "C004"} if key == "ALL" else {"C001", "C002"} if key == "FOCAL" else {key}
            tasks = [task for task in self.clean if task["campaign_id"] in ids]
            expected = self.assert_summary(row, tasks, ("Campaigns", key))
            financial = [campaign for campaign in self.source["campaigns"] if campaign["campaign_id"] in ids]
            expected["campaign_revenue_usd"] = sum_field(financial, "campaign_revenue_usd")
            expected["other_campaign_cost_usd"] = sum_field(financial, "other_campaign_cost_usd")
            expected["actual_staff_cost_usd"] = expected["actual_hours"] * RATE
            expected["campaign_result_usd"] = expected["campaign_revenue_usd"] - expected["other_campaign_cost_usd"] - expected["actual_staff_cost_usd"] - expected["ai_cost_usd"]
            for field in (
                "campaign_revenue_usd", "other_campaign_cost_usd", "actual_staff_cost_usd", "campaign_result_usd",
                "net_ai_value_lower20_usd", "net_ai_value_higher20_usd",
            ):
                self.assert_numeric(row[field], expected[field], ("Campaigns", key, field), formula=True)

    def test_front_sheet_answers_match_the_underlying_complete_groups(self):
        self.assert_numeric(self.sheets["Solution"]["C5"], RATE, ("Solution", "Hourly assumption"))
        overview = self.rows("Solution", ["Metric", "All campaigns", "C001 and C002"], "Metric")
        labels = {"AI spending": "ai_cost_usd", "Hours saved": "hours_saved", "Net AI value": "net_ai_value_usd", "AI ROI": "ai_roi"}
        self.assertEqual({row["Metric"]["value"] for row in overview}, {*labels, "Campaign result"})
        for column, ids in [("All campaigns", {"C001", "C002", "C003", "C004"}), ("C001 and C002", {"C001", "C002"})]:
            expected = totals([task for task in self.clean if task["campaign_id"] in ids])
            finances = [row for row in self.source["campaigns"] if row["campaign_id"] in ids]
            expected["campaign_result_usd"] = sum_field(finances, "campaign_revenue_usd") - sum_field(finances, "other_campaign_cost_usd") - expected["actual_hours"] * RATE - expected["ai_cost_usd"]
            for row in overview:
                label = row["Metric"]["value"]
                self.assert_numeric(row[column], expected[labels.get(label, "campaign_result_usd")], ("Solution", column, label), formula=True)
        answer_tables = [
            {"AI cost": "ai_cost_usd", "Hours saved": "hours_saved", "Net AI value": "net_ai_value_usd", "AI ROI": "ai_roi"},
            {"Revenue": "campaign_revenue_usd", "Other spending": "other_campaign_cost_usd", "Labor value": "actual_staff_cost_usd", "Profit or loss": "campaign_result_usd"},
            {"Baseline 20% lower": "net_ai_value_lower20_usd", "Stated baseline": "net_ai_value_usd", "Baseline 20% higher": "net_ai_value_higher20_usd"},
        ]
        campaigns = {row["campaign_name"]: row for row in self.source["campaigns"]}
        for labels in answer_tables:
            # These presentation blocks have four campaigns and may be followed
            # immediately by a prose note in the campaign-name column.
            rows = self.rows("Solution", ["Campaign", *labels], "Campaign", row_count=len(campaigns))
            self.assertEqual({row["Campaign"]["value"] for row in rows}, set(campaigns))
            for row in rows:
                campaign = campaigns[row["Campaign"]["value"]]
                expected = totals([task for task in self.clean if task["campaign_id"] == campaign["campaign_id"]])
                expected.update({field: D(campaign[field]) for field in ("campaign_revenue_usd", "other_campaign_cost_usd")})
                expected["actual_staff_cost_usd"] = expected["actual_hours"] * RATE
                expected["campaign_result_usd"] = expected["campaign_revenue_usd"] - expected["other_campaign_cost_usd"] - expected["actual_staff_cost_usd"] - expected["ai_cost_usd"]
                for label, field in labels.items():
                    self.assert_numeric(row[label], expected[field], ("Solution", campaign["campaign_id"], label), formula=True)
        mix = self.rows("Solution", ["Metric", "Campaign 1", "Campaign 2"], "Metric")
        mix_labels = {
            "Pro model tasks": ("Pro", "tasks"), "Pro model tokens": ("Pro", "total_tokens"),
            "Pro model spending": ("Pro", "ai_cost_usd"), "Lite model spending": ("Lite", "ai_cost_usd"),
        }
        self.assertEqual({row["Metric"]["value"] for row in mix}, set(mix_labels))
        for row in mix:
            model, field = mix_labels[row["Metric"]["value"]]
            for name, campaign in [("Campaign 1", "C001"), ("Campaign 2", "C002")]:
                expected = totals([task for task in self.clean if task["campaign_id"] == campaign and task["model"] == model])
                self.assert_numeric(row[name], expected[field], ("Solution", name, row["Metric"]["value"]), formula=True)
        workflow = self.rows("Solution", ["Observation", "Tasks", "Rework share", "Corrections per task"], "Observation")
        observations = {
            "Template used": ("prompt_template_used", "Yes"), "No template": ("prompt_template_used", "No"),
            "Brief changed": ("brief_changed", "Yes"), "Brief unchanged": ("brief_changed", "No"),
        }
        self.assertEqual({row["Observation"]["value"] for row in workflow}, set(observations))
        for row in workflow:
            dimension, flag = observations[row["Observation"]["value"]]
            expected = totals([task for task in self.clean if task["campaign_id"] == "C002" and task["task_type"] == "Draft email sequence" and task[dimension] == flag])
            for label, field in [("Tasks", "tasks"), ("Rework share", "rework_share"), ("Corrections per task", "corrections_per_task")]:
                self.assert_numeric(row[label], expected[field], ("Solution", row["Observation"]["value"], label), formula=True)

    def test_preparation_evidence_and_dictionary_cover_the_finished_workbook(self):
        steps = self.rows("Preparation", ["Step", "Preparation completed", "Evidence"], "Step")
        self.assertEqual([row["Step"]["value"] for row in steps], [D(number) for number in range(1, 11)])
        for row in steps:
            for field in ("Preparation completed", "Evidence"):
                self.assertTrue(row[field]["value"], (row["Step"]["value"], field))
        controls = self.rows("Preparation", ["Check", "Workbook", "Source control", "Difference"], "Check")
        self.assertGreaterEqual(len(controls), 15)
        for row in controls:
            self.assert_numeric(row["Workbook"], row["Source control"]["value"], ("Preparation", row["Check"]["value"]), formula=True)
            self.assert_numeric(row["Difference"], ZERO, ("Preparation", row["Check"]["value"], "Difference"), formula=True)
        dictionary = self.rows("Data Dictionary", ["worksheet", "column", "type_and_units", "meaning"], "worksheet")
        definitions = {(row["worksheet"]["value"], row["column"]["value"]): row for row in dictionary}
        self.assertEqual(len(definitions), len(dictionary), "Every dictionary worksheet/column pair must be unique")
        for row in dictionary:
            self.assertTrue(row["type_and_units"]["value"])
            self.assertTrue(row["meaning"]["value"])
        for name, key in [
            ("Tasks", "work_item_id"), ("Prompt Totals", "work_item_id"), ("Priced Usage", "usage_id"),
            ("Campaigns", "campaign_id"), ("Mix", "campaign_id"), ("Workflow", "campaign_id"), ("Daily Usage", "usage_date"),
            *[(sheet, SOURCE_KEYS[source]) for source, sheet in SOURCE_SHEETS.items()],
        ]:
            records = self.rows(name, [key], key)
            self.assertTrue(records, name)
            for field in records[0]:
                self.assertIn((name, field), definitions, (name, field, "Missing field definition"))

    def test_mix_groups_each_campaign_without_multiplying_hours(self):
        actual = self.rows("Mix", ["campaign_id", "dimension", "group", "ai_cost_usd"], "campaign_id")
        expected_keys = {
            (row["campaign_id"], dimension, row[dimension])
            for row in self.clean for dimension in ("department", "product", "model")
        }
        actual_keys = [(row["campaign_id"]["value"], row["dimension"]["value"], row["group"]["value"]) for row in actual]
        self.assertEqual(len(actual_keys), len(set(actual_keys)))
        self.assertEqual(set(actual_keys), expected_keys)
        for row, (campaign, dimension, group) in zip(actual, actual_keys):
            tasks = [task for task in self.clean if task["campaign_id"] == campaign and task[dimension] == group]
            self.assert_summary(row, tasks, ("Mix", campaign, dimension, group))

    def test_workflow_compares_flags_within_task_types_using_task_grain(self):
        actual = self.rows("Workflow", ["campaign_id", "task_type", "dimension", "flag", "tasks"], "campaign_id")
        expected_keys = {
            (row["campaign_id"], task_type, dimension, row[dimension])
            for row in self.clean for task_type in ("All task types", row["task_type"])
            for dimension in ("prompt_template_used", "brief_changed")
        }
        actual_keys = [tuple(row[field]["value"] for field in ("campaign_id", "task_type", "dimension", "flag")) for row in actual]
        self.assertEqual(len(actual_keys), len(set(actual_keys)))
        self.assertEqual(set(actual_keys), expected_keys)
        for row, (campaign, task_type, dimension, flag) in zip(actual, actual_keys):
            tasks = [task for task in self.clean if task["campaign_id"] == campaign and task[dimension] == flag
                     and (task_type == "All task types" or task["task_type"] == task_type)]
            expected = self.assert_summary(row, tasks, ("Workflow", campaign, task_type, dimension, flag))
            for field in ("corrections_per_task", "ai_cost_per_task_usd", "hours_saved_per_task"):
                self.assert_numeric(row[field], expected[field], ("Workflow", campaign, task_type, dimension, flag, field), formula=True)

    def test_daily_usage_uses_prompt_dates_and_does_not_allocate_labor_or_revenue(self):
        actual = self.rows("Daily Usage", ["usage_date", "campaign_id", "prompt_count", "ai_cost_usd"], "usage_date")
        expected = defaultdict(list)
        for prompt in self.usage:
            expected[(prompt["usage_date"], prompt["campaign_id"])].append(prompt)
        actual_keys = []
        for row in actual:
            self.assertIsInstance(row["usage_date"]["value"], D)
            date = (self.epoch + timedelta(days=float(row["usage_date"]["value"]))).strftime("%Y-%m-%d")
            key = (date, row["campaign_id"]["value"])
            actual_keys.append(key)
            prompts = expected[key]
            self.assertTrue(prompts, key)
            amounts = {field: sum_field(prompts, field) for field in (
                "input_tokens", "output_tokens", "total_tokens", "input_cost_usd", "output_cost_usd", "ai_cost_usd",
            )}
            amounts["prompt_count"] = D(len(prompts))
            amounts["correction_prompts"] = D(sum(prompt["prompt_reason"] == "Correction" for prompt in prompts))
            amounts["correction_share"] = amounts["correction_prompts"] / amounts["prompt_count"]
            for field, value in amounts.items():
                self.assert_numeric(row[field], value, ("Daily Usage", *key, field), formula=True)
            self.assertFalse({"baseline_hours", "actual_hours", "campaign_revenue_usd", "net_ai_value_usd"}.intersection(row))
        self.assertEqual(len(actual_keys), len(set(actual_keys)))
        self.assertEqual(set(actual_keys), set(expected))
        self.assertEqual(sum((row["prompt_count"]["value"] for row in actual), ZERO), D(3360))

    def test_native_chart_caches_match_their_live_cell_references(self):
        reference_pattern = re.compile(r"(?:'((?:[^']|'')+)'|([A-Za-z_][A-Za-z0-9_.]*))!\$?([A-Z]+)\$?(\d+)(?::\$?([A-Z]+)\$?(\d+))?")
        charts = []
        with ZipFile(SOLUTION) as archive:
            for name in archive.namelist():
                if not name.endswith(".xml"):
                    continue
                root = ET.fromstring(archive.read(name))
                if root.tag == f"{{{NS['c']}}}chartSpace":
                    charts.append(root)
        self.assertGreaterEqual(len(charts), 2, "Solution should include native charts for presentation")
        for chart in charts:
            references = chart.findall(".//c:strRef", NS) + chart.findall(".//c:numRef", NS)
            self.assertTrue(references)
            for reference in references:
                formula = reference.find("c:f", NS).text
                match = reference_pattern.fullmatch(formula)
                self.assertIsNotNone(match, formula)
                quoted, plain, first_col, first_row, last_col, last_row = match.groups()
                sheet = quoted.replace("''", "'") if quoted else plain
                first_col, last_col = column_number(first_col), column_number(last_col or first_col)
                first_row, last_row = int(first_row), int(last_row or first_row)
                self.assertTrue(first_col == last_col or first_row == last_row, formula)
                expected = [self.sheets[sheet][f"{column_label(column)}{row}"]["value"]
                            for row in range(first_row, last_row + 1)
                            for column in range(first_col, last_col + 1)]
                numeric = reference.tag.endswith("numRef")
                cache = reference.find("c:numCache" if numeric else "c:strCache", NS)
                self.assertIsNotNone(cache, formula)
                self.assertEqual(int(cache.find("c:ptCount", NS).get("val")), len(expected), formula)
                points = cache.findall("c:pt", NS)
                self.assertEqual([int(point.get("idx")) for point in points], list(range(len(expected))), formula)
                for point, value in zip(points, expected):
                    cached = point.find("c:v", NS).text
                    if numeric:
                        self.assertIsInstance(value, D, formula)
                        self.assertLessEqual(abs(D(cached) - value), TOLERANCE, formula)
                    else:
                        self.assertEqual(cached, value, formula)


if __name__ == "__main__":
    unittest.main()
