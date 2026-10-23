"""Fill native chart caches omitted by the workbook export engine.

Usage: python TECHNICAL/workbook-tools/cache_chart_values.py path/to/workbook.xlsx

The artifact tool authors and recalculates the workbook. This export repair only
copies existing saved cell values into each chart's declared same-workbook
reference cache. It retains the live references, formulas, styles, and every
other ZIP part. Missing cells, error cells, external references, unsupported
ranges, and missing formula results fail before replacing the original file.
"""

import argparse
from decimal import Decimal, InvalidOperation
import io
from pathlib import Path
import posixpath
import re
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZipFile


SHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
CHART_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"s": SHEET_NS, "c": CHART_NS}
ET.register_namespace("c", CHART_NS)
ET.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")
ET.register_namespace("r", REL_NS)
REFERENCE = re.compile(r"(?:'((?:[^']|'')+)'|([A-Za-z_][A-Za-z0-9_.]*))!\$?([A-Z]+)\$?([1-9][0-9]*)(?::\$?([A-Z]+)\$?([1-9][0-9]*))?")


def parse_xml(data):
    return ET.fromstring(data, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))


def column_index(label):
    result = 0
    for character in label:
        result = result * 26 + ord(character) - ord("A") + 1
    return result


def column_label(index):
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def reference_cells(formula):
    match = REFERENCE.fullmatch(formula.strip())
    if match is None:
        raise ValueError(f"Unsupported chart reference: {formula}")
    quoted, plain, first_column, first_row, last_column, last_row = match.groups()
    sheet_name = quoted.replace("''", "'") if quoted is not None else plain
    if "[" in sheet_name or "]" in sheet_name:
        raise ValueError(f"External chart reference: {formula}")
    first_column, last_column = column_index(first_column), column_index(last_column or first_column)
    first_row, last_row = int(first_row), int(last_row or first_row)
    if not (1 <= first_column <= last_column <= 16384 and 1 <= first_row <= last_row <= 1048576):
        raise ValueError(f"Invalid chart range: {formula}")
    if first_column != last_column and first_row != last_row:
        raise ValueError(f"Chart reference must be one row or column: {formula}")
    if max(last_column - first_column, last_row - first_row) > 100_000:
        raise ValueError(f"Chart reference is unexpectedly large: {formula}")
    addresses = [
        f"{column_label(column)}{row}"
        for row in range(first_row, last_row + 1)
        for column in range(first_column, last_column + 1)
    ]
    return sheet_name, addresses


def saved_sheets(parts):
    workbook = parse_xml(parts["xl/workbook.xml"])
    relationships = {
        node.get("Id"): node.get("Target")
        for node in parse_xml(parts["xl/_rels/workbook.xml.rels"])
        if node.get("TargetMode") != "External"
    }
    shared = []
    if "xl/sharedStrings.xml" in parts:
        shared = ["".join(node.itertext()) for node in parse_xml(parts["xl/sharedStrings.xml"])]
    sheets = {}
    for sheet in workbook.findall("s:sheets/s:sheet", NS):
        target = relationships.get(sheet.get(f"{{{REL_NS}}}id"))
        if target is None:
            raise ValueError(f"Missing internal worksheet relationship: {sheet.get('name')}")
        target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        cells = {}
        for cell in parse_xml(parts[target]).findall("s:sheetData/s:row/s:c", NS):
            kind = cell.get("t", "n")
            value = cell.find("s:v", NS)
            if kind == "inlineStr":
                inline = cell.find("s:is", NS)
                text = None if inline is None else "".join(inline.itertext())
            elif value is None or value.text is None:
                text = None
            elif kind == "s":
                text = shared[int(value.text)]
            else:
                text = value.text
            cells[cell.get("r")] = (kind, text)
        sheets[sheet.get("name")] = cells
    return sheets


def hydrate_chart(xml, sheets):
    chart = parse_xml(xml)
    if chart.tag != f"{{{CHART_NS}}}chartSpace":
        return None, 0
    point_count = 0
    references = chart.findall(".//c:strRef", NS) + chart.findall(".//c:numRef", NS)
    if not references:
        raise ValueError("Native chart has no supported cell references")
    for reference in references:
        numeric = reference.tag == f"{{{CHART_NS}}}numRef"
        formula = reference.find("c:f", NS)
        if formula is None or formula.text is None:
            raise ValueError("Chart reference has no formula")
        sheet_name, addresses = reference_cells(formula.text)
        if sheet_name not in sheets:
            raise ValueError(f"Unknown chart source sheet: {sheet_name}")
        values = []
        for address in addresses:
            kind, value = sheets[sheet_name].get(address, (None, None))
            if kind == "e" or value is None or value == "":
                raise ValueError(f"Missing or invalid chart source value: {sheet_name}!{address}")
            if numeric:
                try:
                    valid = kind == "n" and Decimal(value).is_finite()
                except InvalidOperation:
                    valid = False
                if not valid:
                    raise ValueError(f"Chart numeric reference is not a saved number: {sheet_name}!{address}")
            values.append(value)
        cache_tag = f"{{{CHART_NS}}}{'numCache' if numeric else 'strCache'}"
        cache = reference.find(cache_tag)
        if cache is None:
            cache = ET.SubElement(reference, cache_tag)
        for node in list(cache):
            if node.tag in (f"{{{CHART_NS}}}ptCount", f"{{{CHART_NS}}}pt"):
                cache.remove(node)
        insert_at = 1 if cache.find(f"{{{CHART_NS}}}formatCode") is not None else 0
        cache.insert(insert_at, ET.Element(f"{{{CHART_NS}}}ptCount", {"val": str(len(values))}))
        for index, value in enumerate(values):
            point = ET.Element(f"{{{CHART_NS}}}pt", {"idx": str(index)})
            ET.SubElement(point, f"{{{CHART_NS}}}v").text = value
            cache.insert(insert_at + index + 1, point)
        point_count += len(values)
    return ET.tostring(chart, encoding="utf-8", xml_declaration=True), point_count


def hydrate_workbook(path):
    path = Path(path).resolve(strict=True)
    if path.suffix.lower() != ".xlsx":
        raise ValueError("Expected an .xlsx workbook")
    with ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) != len({entry.filename for entry in entries}):
            raise ValueError("Workbook archive has duplicate entries")
        parts = {entry.filename: archive.read(entry) for entry in entries}
        archive_comment = archive.comment
    sheets = saved_sheets(parts)
    replacements = {}
    points = 0
    for name, content in parts.items():
        if not name.endswith(".xml"):
            continue
        # Identify the document by its XML root, not an assumed chart directory.
        if parse_xml(content).tag != f"{{{CHART_NS}}}chartSpace":
            continue
        replacements[name], count = hydrate_chart(content, sheets)
        points += count
    if not replacements:
        raise ValueError("Workbook has no native charts to cache")
    output = io.BytesIO()
    with ZipFile(output, "w") as archive:
        archive.comment = archive_comment
        for entry in entries:
            archive.writestr(entry, replacements.get(entry.filename, parts[entry.filename]))
    with ZipFile(io.BytesIO(output.getvalue())) as verified:
        if verified.testzip() is not None or verified.namelist() != [entry.filename for entry in entries]:
            raise ValueError("Repaired archive failed integrity checks")
        for name, original in parts.items():
            if name not in replacements and verified.read(name) != original:
                raise ValueError(f"Unrelated workbook part changed: {name}")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.stem}-", suffix=".xlsx", delete=False) as temporary:
        temporary.write(output.getvalue())
        temporary_path = Path(temporary.name)
    try:
        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return len(replacements), points


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path, help="Saved .xlsx to repair in place")
    arguments = parser.parse_args()
    charts, points = hydrate_workbook(arguments.workbook)
    print(f"Filled {points} cached category/value points across {charts} native charts; all other workbook parts preserved.")
