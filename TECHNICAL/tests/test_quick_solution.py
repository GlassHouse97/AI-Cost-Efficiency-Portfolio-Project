"""Independently reconcile the worked Excel solution with the learner source.

Read-only OOXML checks use the standard library so CI needs no spreadsheet app.
They verify saved formula results; interactive recalculation is checked during
workbook authoring, not claimed by these file checks.
"""

import csv
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import posixpath
import re
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "DATA/TRACKS/quick-challenge/mru_quick_challenge.csv"
SOLUTION = ROOT / "SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
NUMERIC_FIELDS = {
    "prompt_count", "input_tokens", "output_tokens", "input_rate_usd_per_million",
    "output_rate_usd_per_million", "baseline_hours", "actual_hours", "rework_hours",
}
CALCULATED_FIELDS = (
    "total_tokens", "input_cost_usd", "output_cost_usd", "ai_cost_usd",
    "hours_saved", "time_value_usd", "net_ai_value_usd",
)
D = Decimal
ZERO = D(0)
HOURLY_RATE = D(50)
TOLERANCE = D("0.0000001")


def read_solution(path):
    with ZipFile(path) as book:
        if any(name.startswith("xl/externalLinks/") for name in book.namelist()):
            raise AssertionError("Worked solution must not depend on another workbook")
        if "xl/connections.xml" in book.namelist():
            raise AssertionError("Worked solution must not require a data connection")
        if any(name.lower().endswith("vbaproject.bin") for name in book.namelist()):
            raise AssertionError("Worked solution must not require macros")
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        props = workbook.find("s:workbookPr", NS)
        epoch = datetime(1904, 1, 1) if props is not None and props.get("date1904") in ("1", "true") else datetime(1899, 12, 30)
        shared = []
        if "xl/sharedStrings.xml" in book.namelist():
            shared = ["".join(node.itertext()) for node in ET.fromstring(book.read("xl/sharedStrings.xml"))]
        relationships = {
            node.get("Id"): node.get("Target")
            for node in ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        }
        sheets = {}
        for sheet in workbook.findall("s:sheets/s:sheet", NS):
            target = relationships[sheet.get(REL)]
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            cells = {}
            for cell in ET.fromstring(book.read(target)).findall("s:sheetData/s:row/s:c", NS):
                value_node = cell.find("s:v", NS)
                formula = cell.find("s:f", NS)
                kind = cell.get("t", "n")
                if kind == "e":
                    raise AssertionError(f"Formula error at {sheet.get('name')}!{cell.get('r')}: {value_node.text}")
                if kind == "inlineStr":
                    value = "".join(cell.find("s:is", NS).itertext())
                elif value_node is None or value_node.text is None:
                    value = None
                elif kind == "s":
                    value = shared[int(value_node.text)]
                elif kind == "n":
                    value = D(value_node.text)
                else:
                    value = value_node.text
                if formula is not None and value is None:
                    raise AssertionError(f"Missing saved formula result at {sheet.get('name')}!{cell.get('r')}")
                cells[cell.get("r")] = {"value": value, "formula": None if formula is None else formula.text}
            sheets[sheet.get("name")] = cells
        return sheets, epoch


def task_metrics(row):
    """Independent source arithmetic without the workbook builder or dashboard."""
    input_cost = D(row["input_tokens"]) * D(row["input_rate_usd_per_million"]) / D(1_000_000)
    output_cost = D(row["output_tokens"]) * D(row["output_rate_usd_per_million"]) / D(1_000_000)
    saved = D(row["baseline_hours"]) - D(row["actual_hours"])
    return {
        "total_tokens": D(row["input_tokens"]) + D(row["output_tokens"]),
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "ai_cost_usd": input_cost + output_cost,
        "hours_saved": saved,
        "time_value_usd": saved * HOURLY_RATE,
        "net_ai_value_usd": saved * HOURLY_RATE - input_cost - output_cost,
    }


def totals(rows):
    calculated = [task_metrics(row) for row in rows]
    total = {key: sum((row[key] for row in calculated), ZERO) for key in CALCULATED_FIELDS}
    for field in NUMERIC_FIELDS:
        total[field] = sum((D(row[field]) for row in rows), ZERO)
    total["tasks"] = D(len(rows))
    total["roi"] = total["net_ai_value_usd"] / total["ai_cost_usd"]
    total["rework_share"] = total["rework_hours"] / total["actual_hours"]
    return total


class QuickSolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            cls.headers = reader.fieldnames
            cls.raw = list(reader)
        deduplicated = {}
        for row in cls.raw:
            key = row["work_item_id"]
            if key in deduplicated and deduplicated[key] != row:
                raise AssertionError(f"Conflicting source duplicate: {key}")
            deduplicated.setdefault(key, row)
        cls.clean = [dict(row, department=row["department"].strip().title()) for row in deduplicated.values()]
        cls.sheets, cls.epoch = read_solution(SOLUTION)

    def cell(self, sheet, address):
        return self.sheets[sheet].get(address, {"value": None, "formula": None})

    def assert_number(self, sheet, address, expected, formula=False):
        cell = self.cell(sheet, address)
        self.assertIsInstance(cell["value"], D, (sheet, address))
        self.assertLessEqual(abs(cell["value"] - D(expected)), TOLERANCE, (sheet, address, expected, cell["value"]))
        if formula:
            self.assertTrue(cell["formula"], (sheet, address, "Expected a formula, not a hardcoded answer"))

    def assert_source_table(self, sheet, rows):
        for column, field in zip("ABCDEFGHIJKLMNOPQ", self.headers):
            self.assertEqual(self.cell(sheet, f"{column}6")["value"], field)
        for row_number, row in enumerate(rows, 7):
            for column, field in zip("ABCDEFGHIJKLMNOPQ", self.headers):
                cell = self.cell(sheet, f"{column}{row_number}")
                actual = cell["value"]
                self.assertIsNone(cell["formula"], (sheet, row_number, field, "Source inputs must remain intact"))
                if field == "completion_date":
                    self.assertIsInstance(actual, D)
                    actual = (self.epoch + timedelta(days=float(actual))).strftime("%Y-%m-%d")
                    self.assertEqual(actual, row[field], (sheet, row_number, field))
                elif field in NUMERIC_FIELDS:
                    self.assertIsInstance(actual, D)
                    self.assertEqual(actual, D(row[field]), (sheet, row_number, field))
                else:
                    self.assertEqual(actual, row[field], (sheet, row_number, field))
        self.assertIsNone(self.cell(sheet, f"A{len(rows) + 7}")["value"], "Unexpected extra source record")

    def test_preserves_raw_inputs_and_cleaned_task_population(self):
        self.assertEqual(list(self.sheets), ["Solution", "Summaries", "Clean", "Raw"])
        self.assertEqual(len(self.raw), 122)
        self.assertEqual(len(self.clean), 120)
        self.assert_source_table("Raw", self.raw)
        self.assert_source_table("Clean", self.clean)
        self.assertEqual({row["department"] for row in self.clean}, {"Analytics", "Content", "Creative", "Marketing Operations"})

    def test_each_task_formula_result_reconciles_to_source(self):
        self.assert_number("Clean", "B3", HOURLY_RATE)
        for column, field in zip("RSTUVWX", CALCULATED_FIELDS):
            self.assertEqual(self.cell("Clean", f"{column}6")["value"], field)
        for row_number, row in enumerate(self.clean, 7):
            expected = task_metrics(row)
            for column, field in zip("RSTUVWX", CALCULATED_FIELDS):
                self.assert_number("Clean", f"{column}{row_number}", expected[field], formula=True)

    def test_campaign_answers_and_ratios_reconcile_to_summed_tasks(self):
        fields = (
            "tasks", "input_tokens", "output_tokens", "total_tokens", "prompt_count",
            "input_cost_usd", "output_cost_usd", "ai_cost_usd", "baseline_hours",
            "actual_hours", "hours_saved", "time_value_usd", "net_ai_value_usd", "roi",
            "rework_hours", "rework_share",
        )
        for row_number, campaign in [(8, "Campaign 1"), (9, "Campaign 2"), (10, None)]:
            expected = totals([row for row in self.clean if campaign is None or row["campaign"] == campaign])
            for column, field in zip("CDEFGHIJKLMNOPQR", fields):
                self.assert_number("Summaries", f"{column}{row_number}", expected[field], formula=True)
        for column, campaign in [("C", "Campaign 1"), ("D", "Campaign 2"), ("E", None)]:
            expected = totals([row for row in self.clean if campaign is None or row["campaign"] == campaign])
            self.assert_number("Solution", f"{column}26", expected["net_ai_value_usd"], formula=True)
            self.assert_number("Solution", f"{column}27", expected["roi"], formula=True)

    def test_department_and_issue_answers_cover_the_same_clean_population(self):
        for row_number, department in [(16, "Analytics"), (17, "Content"), (18, "Creative"), (19, "Marketing Operations"), (20, None)]:
            rows = [row for row in self.clean if department is None or row["department"] == department]
            expected = totals(rows)
            for column, field in [("C", "ai_cost_usd"), ("D", "net_ai_value_usd"), ("E", "hours_saved")]:
                self.assert_number("Summaries", f"{column}{row_number}", expected[field], formula=True)
        for row_number, issue in [(26, "Brief changed"), (27, "Data problem"), (28, "Unclear prompt"), (29, "None"), (30, None)]:
            for column, campaign in [("C", "Campaign 1"), ("D", "Campaign 2"), ("E", None)]:
                count = sum(1 for row in self.clean if (issue is None or row["issue_tag"] == issue) and (campaign is None or row["campaign"] == campaign))
                self.assert_number("Summaries", f"{column}{row_number}", count, formula=True)

    def test_native_charts_cache_their_declared_source_values(self):
        chart_ns = {"c": "http://schemas.openxmlformats.org/drawingml/2006/chart"}
        with ZipFile(SOLUTION) as workbook:
            charts = []
            for name in workbook.namelist():
                if name.endswith(".xml"):
                    root = ET.fromstring(workbook.read(name))
                    if root.tag == f"{{{chart_ns['c']}}}chartSpace":
                        charts.append(root)
            self.assertEqual(len(charts), 2)
            for chart in charts:
                references = chart.findall(".//c:strRef", chart_ns) + chart.findall(".//c:numRef", chart_ns)
                self.assertTrue(references)
                for reference in references:
                    formula = reference.find("c:f", chart_ns).text
                    match = re.fullmatch(r"'([^']+)'!\$([A-Z]+)\$(\d+):\$([A-Z]+)\$(\d+)", formula)
                    self.assertIsNotNone(match, formula)
                    sheet, first_column, first_row, last_column, last_row = match.groups()
                    self.assertEqual(first_column, last_column)
                    expected = [self.cell(sheet, f"{first_column}{row}")["value"] for row in range(int(first_row), int(last_row) + 1)]
                    numeric = reference.tag.endswith("numRef")
                    cache = reference.find("c:numCache" if numeric else "c:strCache", chart_ns)
                    self.assertIsNotNone(cache, formula)
                    self.assertEqual(int(cache.find("c:ptCount", chart_ns).get("val")), len(expected))
                    points = cache.findall("c:pt", chart_ns)
                    self.assertEqual(len(points), len(expected))
                    self.assertEqual([int(point.get("idx")) for point in points], list(range(len(expected))))
                    for point, value in zip(points, expected):
                        cached = point.find("c:v", chart_ns).text
                        if numeric:
                            self.assertIsInstance(value, D)
                            self.assertLessEqual(abs(D(cached) - value), TOLERANCE, formula)
                        else:
                            self.assertEqual(cached, value, formula)


if __name__ == "__main__":
    unittest.main()
