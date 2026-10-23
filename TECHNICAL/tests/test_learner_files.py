"""Independent OOXML checks: learner workbooks must preserve the raw CSV inputs."""

import csv
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import posixpath
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
TRACKS = {
    "quick-challenge": {"Raw": "mru_quick_challenge.csv"},
    "portfolio-project": {
        "campaigns": "campaigns.csv",
        "work_log": "work_log.csv",
        "ai_usage": "ai_usage.csv",
        "model_pricing": "model_pricing.csv",
    },
}
GUIDES = {"README.md", "COLUMN_GUIDE.md", "FORMULAS.md", "SUBMISSION_CHECKLIST.md", "START_HERE.html", "LICENSE", "DATA_LICENSE"}
NUMERIC_FIELDS = {
    "prompt_count", "input_tokens", "output_tokens", "input_rate_usd_per_million",
    "output_rate_usd_per_million", "baseline_hours", "actual_hours", "rework_hours",
    "campaign_revenue_usd", "other_campaign_cost_usd", "completion_date", "usage_date",
}


def column_number(address):
    value = 0
    for char in address:
        if not char.isalpha():
            break
        value = value * 26 + ord(char.upper()) - 64
    return value


def read_workbook(path):
    with ZipFile(path) as book:
        shared = []
        if "xl/sharedStrings.xml" in book.namelist():
            shared = ["".join(node.itertext()) for node in ET.fromstring(book.read("xl/sharedStrings.xml"))]
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        props = workbook.find("s:workbookPr", NS)
        epoch = datetime(1904, 1, 1) if props is not None and props.get("date1904") in ("1", "true") else datetime(1899, 12, 30)
        relationships = {
            node.get("Id"): node.get("Target")
            for node in ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        }
        sheets = {}
        for sheet in workbook.findall("s:sheets/s:sheet", NS):
            target = relationships[sheet.get(REL)]
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            xml = ET.fromstring(book.read(target))
            if xml.findall(".//s:f", NS):
                raise AssertionError("Raw learner sheets must not contain formulas or calculated answers")
            rows = {}
            for row in xml.findall("s:sheetData/s:row", NS):
                values = {}
                for cell in row.findall("s:c", NS):
                    value = cell.find("s:v", NS)
                    kind = cell.get("t", "n")
                    if kind == "e":
                        raise AssertionError(f"Workbook contains an error cell: {cell.get('r')}")
                    if kind == "inlineStr":
                        value = "".join(cell.find("s:is", NS).itertext())
                    elif value is None:
                        continue
                    elif kind == "s":
                        value = shared[int(value.text)]
                    elif kind == "n":
                        value = Decimal(value.text)
                    else:
                        value = value.text
                    values[column_number(cell.get("r"))] = value
                if values:
                    rows[int(row.get("r"))] = values
            sheets[sheet.get("name")] = rows
        return sheets, epoch


class LearnerFileTests(unittest.TestCase):
    def test_excel_workbooks_match_every_raw_source_cell(self):
        for slug, mapping in TRACKS.items():
            with self.subTest(track=slug):
                folder = ROOT / "DATA" / "TRACKS" / slug
                sheets, epoch = read_workbook(folder / f"mru-{slug}.xlsx")
                self.assertEqual(set(sheets), set(mapping))
                for sheet, filename in mapping.items():
                    with (folder / filename).open(encoding="utf-8-sig", newline="") as handle:
                        expected = list(csv.reader(handle))
                    rows = sheets[sheet]
                    self.assertEqual(set(rows), set(range(1, len(expected) + 1)))
                    for r, row in enumerate(expected, 1):
                        self.assertEqual(set(rows[r]), set(range(1, len(row) + 1)))
                        for c, text in enumerate(row, 1):
                            actual = rows[r][c]
                            field = expected[0][c - 1]
                            if r > 1 and field in NUMERIC_FIELDS:
                                self.assertIsInstance(actual, Decimal, (slug, sheet, r, field))
                            if isinstance(actual, Decimal):
                                if r > 1 and field in ("completion_date", "usage_date"):
                                    actual = (epoch + timedelta(days=float(actual))).strftime("%Y-%m-%d")
                                    self.assertEqual(actual, text, (slug, sheet, r, c))
                                else:
                                    self.assertEqual(actual, Decimal(text), (slug, sheet, r, c))
                            else:
                                self.assertEqual(actual, text, (slug, sheet, r, c))

    def test_complete_downloads_contain_exact_inputs_and_no_solutions(self):
        for slug, mapping in TRACKS.items():
            with self.subTest(track=slug):
                workbook = f"mru-{slug}.xlsx"
                source_names = set(mapping.values()) | {workbook}
                release = ROOT / "DATA" / "TRACKS" / slug / f"mru-{slug}.zip"
                self.assertEqual(release.read_bytes(), (ROOT / "TECHNICAL" / "dashboard" / "downloads" / release.name).read_bytes())
                with ZipFile(release) as archive:
                    self.assertEqual(set(archive.namelist()), source_names | GUIDES)
                    self.assertIsNone(archive.testzip())
                    for filename in source_names:
                        source = ROOT / "DATA" / "TRACKS" / slug / filename
                        expected = source.read_bytes() if filename.endswith(".xlsx") else source.read_text(encoding="utf-8-sig").encode("utf-8")
                        self.assertEqual(archive.read(filename), expected)


if __name__ == "__main__":
    unittest.main()
