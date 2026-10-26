"""Independent OOXML checks: learner workbooks must preserve the raw CSV inputs."""

import csv
from datetime import datetime, timedelta
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
import posixpath
import re
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
DOWNLOAD_BASE = "https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS"
SOURCE_BASE = "https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/tree/main/DATA/TRACKS"
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
GUIDES = {
    "quick-challenge": {"START_HERE.html", "LICENSE", "DATA_LICENSE"},
    "portfolio-project": {"README.md", "COLUMN_GUIDE.md", "FORMULAS.md", "SUBMISSION_CHECKLIST.md", "START_HERE.html", "LICENSE", "DATA_LICENSE"},
}
NUMERIC_FIELDS = {
    "prompt_count", "input_tokens", "output_tokens", "input_rate_usd_per_million",
    "output_rate_usd_per_million", "baseline_hours", "actual_hours", "rework_hours",
    "campaign_revenue_usd", "other_campaign_cost_usd", "completion_date", "usage_date",
}


class GuideLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src"):
                self.targets.append(value)
            elif name == "id":
                self.anchors.add(value)


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
    def test_question_briefs_and_repository_guides_link_the_track_downloads(self):
        for slug, mapping in TRACKS.items():
            with self.subTest(track=slug):
                source_names = set(mapping.values()) | {f"mru-{slug}.xlsx"}
                expected = {f"{DOWNLOAD_BASE}/{slug}/mru-{slug}.zip"}
                if slug == "portfolio-project":
                    expected.update(f"{DOWNLOAD_BASE}/{slug}/{name}" for name in source_names)
                    expected.add(f"{SOURCE_BASE}/{slug}")
                folder = ROOT / "QUESTIONS" / "TRACKS" / slug
                brief = (folder / "README.md").read_text(encoding="utf-8")
                markdown_links = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", brief))
                if slug == "quick-challenge":
                    self.assertEqual(markdown_links, expected)
                else:
                    self.assertTrue(expected <= markdown_links, expected - markdown_links)
                guide = GuideLinks()
                guide.feed((folder / "START_HERE.html").read_text(encoding="utf-8"))
                file_links = {target for target in guide.targets if not target.startswith("#")}
                self.assertEqual(file_links, expected)
                self.assertTrue(all(urlsplit(target).scheme == "https" for target in file_links))

    def test_extracted_guides_need_only_files_inside_the_learner_zip(self):
        for slug, mapping in TRACKS.items():
            with self.subTest(track=slug):
                release = ROOT / "DATA" / "TRACKS" / slug / f"mru-{slug}.zip"
                with ZipFile(release) as archive:
                    guide = GuideLinks()
                    guide.feed(archive.read("START_HERE.html").decode("utf-8"))
                    source_names = set(mapping.values()) | {f"mru-{slug}.xlsx"}
                    self.assertEqual({target for target in guide.targets if not target.startswith("#")}, source_names)
                    for target in guide.targets:
                        if target.startswith("#"):
                            self.assertIn(target[1:], guide.anchors)
                        else:
                            self.assertFalse(urlsplit(target).scheme)
                            self.assertIn(target, archive.namelist())
                    for filename in GUIDES[slug]:
                        if filename.endswith((".md", ".html")):
                            text = archive.read(filename).decode("utf-8")
                            self.assertNotIn("ONLINE_DOWNLOADS_", text)
                            self.assertNotIn(DOWNLOAD_BASE, text)

    def test_quick_question_document_excludes_the_worked_solution(self):
        folder = ROOT / "QUESTIONS" / "TRACKS" / "quick-challenge"
        brief = (folder / "README.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"^\d+\. ", brief, re.MULTILINE)), 6)
        with ZipFile(ROOT / "DATA" / "TRACKS" / "quick-challenge" / "mru-quick-challenge.zip") as archive:
            documents = (brief, archive.read("START_HERE.html").decode("utf-8"))
        for document in documents:
            for worked_step in (
                "SUMIFS(", "COUNTIFS(", "PROPER(", "TRIM(", "Remove Duplicates",
                "COLUMN_GUIDE.md", "FORMULAS.md", "SUBMISSION_CHECKLIST.md",
                "Excel walkthrough", "total_tokens", "net_ai_value_usd",
            ):
                self.assertNotIn(worked_step.casefold(), document.casefold())

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
                    self.assertEqual(set(archive.namelist()), source_names | GUIDES[slug])
                    self.assertIsNone(archive.testzip())
                    for filename in source_names:
                        source = ROOT / "DATA" / "TRACKS" / slug / filename
                        expected = source.read_bytes() if filename.endswith(".xlsx") else source.read_text(encoding="utf-8-sig").encode("utf-8")
                        self.assertEqual(archive.read(filename), expected)


if __name__ == "__main__":
    unittest.main()
