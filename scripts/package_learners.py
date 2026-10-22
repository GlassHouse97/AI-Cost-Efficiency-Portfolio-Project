"""Build standalone learner downloads from an explicit, solution-free allowlist.

Usage: python scripts/package_learners.py [--check]
Only the standard library is required. Author code and completed-demo outputs
are deliberately excluded from every archive. HTML guides are generated from
the same Markdown shipped in each archive, without network dependencies.
ZIP entries are stored without compression and text uses UTF-8/LF so archive
bytes do not depend on the operating system, Git newline settings, or zlib.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
from pathlib import Path
import re
import sys
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
GUIDES = ("README.md", "COLUMN_GUIDE.md", "FORMULAS.md", "SUBMISSION_CHECKLIST.md")
COMMON_FILES = (*GUIDES, "START_HERE.html")
PACKAGES = {
    "quick-challenge": {
        "title": "MRU AI value Quick Challenge",
        "subtitle": "Beginner to early intermediate · Four hour target · Excel or basic BI",
        "files": ("mru_quick_challenge.csv", *COMMON_FILES),
    },
    "portfolio-project": {
        "title": "MRU AI value Portfolio Project",
        "subtitle": "Intermediate · 12 to 16 hour target · Your choice of analysis tools",
        "files": (
            "work_log.csv", "ai_usage.csv", "model_pricing.csv", "campaigns.csv", *COMMON_FILES
        ),
    },
}
SCHEMAS = {
    "mru_quick_challenge.csv": "work_item_id,completion_date,campaign,department,employee,product,model,task_type,prompt_count,input_tokens,output_tokens,input_rate_usd_per_million,output_rate_usd_per_million,baseline_hours,actual_hours,rework_hours,issue_tag",
    "work_log.csv": "work_item_id,completion_date,campaign_id,department,employee,task_type,baseline_hours,actual_hours,rework_hours,issue_tag,brief_changed,prompt_template_used",
    "ai_usage.csv": "usage_id,usage_date,work_item_id,campaign_id,product,model,input_tokens,output_tokens,prompt_reason",
    "model_pricing.csv": "model,input_rate_usd_per_million,output_rate_usd_per_million",
    "campaigns.csv": "campaign_id,campaign_name,campaign_revenue_usd,other_campaign_cost_usd",
}
SECTIONS = (
    ("README.md", "brief", "Brief and steps"),
    ("COLUMN_GUIDE.md", "columns", "Column guide"),
    ("FORMULAS.md", "formulas", "Formulas and example"),
    ("SUBMISSION_CHECKLIST.md", "checklist", "Submission checklist"),
)


def inline(value: str) -> str:
    """Escape all source HTML and support only our small inline Markdown set."""
    rendered: list[str] = []
    cursor = 0
    for match in re.finditer(r"`([^`]+)`|\*\*(.+?)\*\*", value):
        rendered.append(html.escape(value[cursor:match.start()]))
        if match.group(1) is not None:
            rendered.append("<code>" + html.escape(match.group(1)) + "</code>")
        else:
            rendered.append("<strong>" + inline(match.group(2)) + "</strong>")
        cursor = match.end()
    rendered.append(html.escape(value[cursor:]))
    return "".join(rendered)


def render_markdown(source: str) -> str:
    """Render the controlled headings, paragraphs, lists, and tables we author."""
    lines = source.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        heading = re.match(r"^(#{1,5}) (.+)$", line)
        if heading:
            # Each source document sits inside a section below the page's h1.
            level = len(heading.group(1)) + 1
            output.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            index += 1
            continue
        if line.startswith("|"):
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            if not rows:
                raise ValueError("Table without a header")
            output.append('<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable reference table"><table><thead><tr>')
            output.extend(f'<th scope="col">{inline(cell)}</th>' for cell in rows[0])
            output.append("</tr></thead><tbody>")
            for row in rows[1:]:
                if len(row) != len(rows[0]):
                    raise ValueError("Table row has an inconsistent column count")
                output.append("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>")
            output.append("</tbody></table></div>")
            continue
        ordered = bool(re.match(r"^\d+\. ", line))
        if line.startswith("- ") or ordered:
            tag = "ol" if ordered else "ul"
            expression = r"^\d+\. (.+)$" if ordered else r"^- (.+)$"
            output.append(f"<{tag}>")
            while index < len(lines):
                item = re.match(expression, lines[index].strip())
                if not item:
                    break
                output.append("<li>" + inline(item.group(1)) + "</li>")
                index += 1
            output.append(f"</{tag}>")
            continue
        paragraph = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            candidate = lines[index].strip()
            if candidate.startswith(("#", "|", "- ")) or re.match(r"^\d+\. ", candidate):
                break
            paragraph.append(candidate)
            index += 1
        output.append("<p>" + inline(" ".join(paragraph)) + "</p>")
    return "\n".join(output)


STYLE = """
:root{color-scheme:light;--ink:#162e36;--muted:#50646b;--paper:#fff;--edge:#d9e4e4;--brand:#006a62}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:1.5rem}body{margin:0;background:#edf3f2;color:var(--ink);font:16px/1.68 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:#00665e;text-underline-offset:.2em}a:hover{text-decoration-thickness:2px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid #bd6b13;outline-offset:4px}
.skip{position:absolute;left:1rem;top:-6rem;background:white;padding:.7rem;z-index:10}.skip:focus{top:1rem}
header{background:#102c34;color:#eef8f6;padding:3.5rem max(1.4rem,calc((100vw - 1180px)/2)) 3rem;border-bottom:6px solid #65cfb3}
.eyebrow{font-size:.76rem;text-transform:uppercase;letter-spacing:.17em;font-weight:750;color:#91ddc9;margin:0 0 .7rem}h1{font-size:clamp(2rem,4vw,3.1rem);line-height:1.13;letter-spacing:-.035em;max-width:880px;margin:0 0 1rem}.subtitle{margin:0;color:#c9dedf;max-width:800px}
.shell{max-width:1220px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:2rem;margin:auto;padding:2rem 1.3rem 5rem}aside{align-self:start;position:sticky;top:1.5rem}nav a{display:block;padding:.7rem .8rem;margin:.2rem 0;border-radius:7px;font-weight:650;text-decoration:none}nav a:hover{background:#dcebe6}aside .small{font-size:.85rem;color:var(--muted);margin:1.2rem .8rem}.files{padding:.7rem .8rem;border-top:1px solid var(--edge);margin-top:1rem}.files p{font-weight:700;font-size:.85rem;margin:.3rem 0}.files a{display:block;font-size:.78rem;margin:.6rem 0;overflow-wrap:anywhere}
main{min-width:0}section{background:var(--paper);border:1px solid var(--edge);border-radius:14px;padding:clamp(1.2rem,3.3vw,2.7rem);margin-bottom:1.6rem;box-shadow:0 5px 20px #12393204}section>h2:first-child{margin-top:0}h2{font-size:1.8rem;line-height:1.25;letter-spacing:-.025em}h3{font-size:1.18rem;margin:2rem 0 .6rem;line-height:1.35}p{margin:.85rem 0}li{margin:.55rem 0;padding-left:.15rem}ul,ol{padding-left:1.45rem}strong{font-weight:700}code{font: .85em/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;background:#edf4f2;color:#174b45;padding:.12em .28em;border-radius:4px;overflow-wrap:anywhere}
.table-wrap{max-width:100%;overflow-x:auto;margin:1.2rem 0;border:1px solid var(--edge);border-radius:8px}table{border-collapse:collapse;text-align:left;width:100%;font-size:.9rem}th,td{padding:.75rem .8rem;border-bottom:1px solid var(--edge);vertical-align:top}th{background:#e8f2ef;color:#21453f;font-weight:700}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#fafcfc}td:first-child{font-weight:550}footer{font-size:.85rem;color:var(--muted);padding:.6rem 1rem}
@media(max-width:800px){.shell{grid-template-columns:1fr;gap:1rem;padding-top:1rem}aside{position:static}nav{display:flex;flex-wrap:wrap;gap:.1rem;font-size:.88rem}nav a{padding:.45rem .6rem}.files{display:flex;gap:.8rem;flex-wrap:wrap;align-items:baseline}.files a{margin:.2rem 0}.files p{width:100%}aside .small{margin:.5rem .6rem}section{border-radius:9px}th,td{padding:.6rem}header{padding:2.4rem 1.4rem 2rem}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:#fff;font-size:10pt}header{background:white;color:#162e36;padding:0 0 1rem;border-bottom:2px solid #162e36}.eyebrow,.subtitle{color:#38515a}h1{font-size:24pt}.shell{display:block;padding:1rem 0}aside,.skip{display:none}section{border:0;padding:0;box-shadow:none;break-before:page}section:first-child{break-before:auto}.table-wrap{overflow:visible}h2,h3{break-after:avoid}tr{break-inside:avoid}a{color:inherit}}
"""


def html_guide(folder: Path, package: dict, csv_prefix: str = "") -> bytes:
    navigation = "".join(f'<a href="#{anchor}">{label}</a>' for _, anchor, label in SECTIONS)
    sections = []
    for filename, anchor, _ in SECTIONS:
        source = (folder / filename).read_text(encoding="utf-8")
        sections.append(f'<section id="{anchor}">\n{render_markdown(source)}\n</section>')
    csv_links = "".join(
        f'<a href="{csv_prefix}{filename}" download>{filename}</a>'
        for filename in package["files"] if filename.endswith(".csv")
    )
    document = f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Standalone synthetic AI cost and staff time value exercise with data, formulas, and a submission checklist.">
<title>{html.escape(package["title"])} | Learner guide</title><style>{STYLE}</style></head>
<body><a class="skip" href="#main">Skip to the learner guide</a>
<header><p class="eyebrow">Marketing-R-Us · Standalone learner guide</p><h1>{html.escape(package["title"])}</h1><p class="subtitle">{html.escape(package["subtitle"])}</p></header>
<div class="shell"><aside><nav aria-label="Guide sections">{navigation}</nav><p class="small">Works offline. No accounts, API keys, or external links are needed to complete the exercise.</p><div class="files"><p>Source data</p>{csv_links}</div></aside>
<main id="main">{"".join(sections)}<footer>Synthetic data for learning. Documentation: MIT. Data: CC0 1.0. Full licenses are included in the download.</footer></main></div>
</body></html>
'''
    return document.encode("utf-8")


def validate_raw_schema(path: Path) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    expected = SCHEMAS[path.name].split(",")
    if header != expected:
        raise ValueError(f"{path.name}: raw schema changed or a calculated answer column was added")


def canonical_text(path: Path) -> bytes:
    """All allowlisted sources are UTF-8 text; normalize platform line endings."""
    return path.read_text(encoding="utf-8-sig").encode("utf-8")


def archive_bytes(folder: Path, package: dict, guide: bytes) -> bytes:
    """Only explicitly named learner files and both licenses can enter the ZIP."""
    payloads: dict[str, bytes] = {}
    for filename in package["files"]:
        path = (ROOT / "data" / folder.name / filename) if filename.endswith(".csv") else folder / filename
        if path.suffix == ".csv":
            validate_raw_schema(path)
        payloads[filename] = guide if filename == "START_HERE.html" else canonical_text(path)
    for license_name in ("LICENSE", "DATA_LICENSE"):
        payloads[license_name] = canonical_text(ROOT / license_name)
    output = io.BytesIO()
    # Deflate output can differ across zlib versions. These source files are
    # small, so storing bytes provides portable reproducibility without a pin.
    with ZipFile(output, "w", compression=ZIP_STORED) as archive:
        for filename, payload in sorted(payloads.items()):
            info = ZipInfo(filename, date_time=(2026, 10, 22, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload, compress_type=ZIP_STORED)
    result = output.getvalue()
    with ZipFile(io.BytesIO(result)) as archive:
        if set(archive.namelist()) != set(payloads):
            raise ValueError("Archive contains an unexpected file")
        if archive.testzip() is not None:
            raise ValueError("Archive failed its CRC check")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated HTML and ZIPs are current without writing")
    args = parser.parse_args()
    stale = []
    for slug, package in PACKAGES.items():
        folder = ROOT / "learners" / slug
        guide = html_guide(folder, package)
        archive = archive_bytes(folder, package, guide)
        outputs = {
            folder / "START_HERE.html": html_guide(folder, package, csv_prefix=f"../../data/{slug}/"),
            ROOT / "release" / f"mru-{slug}.zip": archive,
            ROOT / "dashboard" / "downloads" / f"mru-{slug}.zip": archive,
        }
        for target, content in outputs.items():
            if args.check:
                if not target.exists() or target.read_bytes() != content:
                    stale.append(str(target.relative_to(ROOT)))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
        digest = hashlib.sha256(archive).hexdigest()
        print(f"mru-{slug}.zip: {len(archive):,} bytes; sha256={digest}")
    if stale:
        print("Stale or missing generated output:\n" + "\n".join(stale), file=sys.stderr)
        return 1
    print("Learner HTML and ZIPs verified." if args.check else "Learner HTML and ZIPs built; hosting copies match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
