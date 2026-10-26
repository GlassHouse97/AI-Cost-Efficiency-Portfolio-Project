# Data pipeline and reproducibility

This repository contains a deterministic teaching dataset, an independent reconciliation step, a browser dashboard, and two offline learner packages, and a separate worked Quick Challenge Excel solution. The canonical raw CSVs live in [`DATA/`](../../DATA/README.md). The generated demo source contains cleaned records; the learner sources retain the small cleaning exercise.

## Flow

```mermaid
flowchart TD
    A[Fixed scenario and seed 20261022] --> B[TECHNICAL/scripts/generate_data.py]
    B --> C[Canonical CSVs in DATA/]
    B --> D[Clean TECHNICAL/dashboard/demo-data.json]
    C --> E[TECHNICAL/scripts/validate_data.py]
    D --> E
    E --> F[SOLUTION/TRACKS/portfolio-project/outputs/check_totals.json]
    C --> L[TECHNICAL/scripts/analyze_case_study.py]
    L --> M[SOLUTION/TRACKS/portfolio-project/outputs/ evidence CSVs]
    C --> G[TECHNICAL/scripts/package_learners.py]
    H[Learner Markdown and licenses] --> G
    G --> I[DATA/TRACKS/ learner ZIPs and TECHNICAL/dashboard/downloads/ copies]
    C --> N[TECHNICAL/workbook-tools/build-quick-solution.mjs]
    N --> O[SOLUTION/TRACKS/quick-challenge/ completed Excel workbook]
    D --> J[Browser metrics and dashboard]
    I --> J
    J --> K[npm --prefix TECHNICAL run build: TECHNICAL/dist/]
```

## Rebuild from the repository root

Python 3.10+ uses only its standard library. Node.js 22+ runs the dashboard tests and static build. No database, API credentials, or external data connection is needed.

```sh
python TECHNICAL/scripts/generate_data.py
python TECHNICAL/scripts/validate_data.py --write-checks
python TECHNICAL/scripts/analyze_case_study.py
python TECHNICAL/scripts/package_learners.py
python -m unittest discover -s TECHNICAL/tests -p "test_*.py" -v
npm --prefix TECHNICAL test
python TECHNICAL/scripts/package_learners.py --check
npm --prefix TECHNICAL run build
```

The Python scripts resolve files relative to their own location, so they can also be invoked using an absolute path from another directory. Run the npm commands shown here from the repository root. Generation replaces the five canonical CSVs and `TECHNICAL/dashboard/demo-data.json`; analysis replaces the eight evidence CSVs; packaging replaces generated HTML and both archive copies under `DATA/TRACKS/<track>/` and `TECHNICAL/dashboard/downloads/`. Keep exploratory analysis in separate files.

The committed raw-data Excel workbooks are alternate learner inputs for the same CSV records. If those records change, rebuild the workbooks with the optional [workbook authoring helper](../workbook-tools/README.md) before packaging. Its separate authoring runtime is not needed for the dashboard or standard-library workbook parity checks.

## 1. Generate internally consistent sources

[`generate_data.py`](../scripts/generate_data.py) creates integer tokens and hundredths of hours before serialization. It uses seed `20261022` and largest-remainder apportionment to preserve the fixed scenario totals while varying individual tasks and prompts.

The generator emits 240 clean tasks, 3,360 prompts, two model prices, and four campaigns. The raw task exports intentionally add two repeated records and department whitespace/case inconsistencies. The quick export is limited to the same 120 Campaign 1/2 tasks and aggregates their prompt tokens and counts to task grain. It also includes model rates so learners can begin without a join.

`TECHNICAL/dashboard/demo-data.json` contains only clean original-column records in four arrays: `work_log`, `ai_usage`, `model_pricing`, and `campaigns`. It has no stored ROI or net-value answer fields. The browser calculates those metrics from the records.

## 2. Independently reconcile the records

[`validate_data.py`](../scripts/validate_data.py) reads the CSVs and demo source without importing the generator or treating saved check totals as an input. It checks:

- Raw and deduplicated row counts; exact duplicate equality and department normalization.
- Unique pricing, campaign, and usage keys; task/prompt/campaign relationships; supported categories; valid dates and nonnegative numbers.
- One product/model and one first attempt per task; all tasks having prompts.
- Rework within actual hours and task hours counted once.
- Token-based charges using `Decimal`, without rounding individual prompts to cents.
- Quick/deeper-track agreement and record-level parity between cleaned CSV sources and the dashboard source.
- Focal scenario controls, task-level exceptions, and baseline sensitivity.

`--write-checks` saves six-decimal monetary controls to [`SOLUTION/TRACKS/portfolio-project/outputs/check_totals.json`](../../SOLUTION/TRACKS/portfolio-project/outputs/check_totals.json). Normal validation prints the calculated result without changing that file. Scenario details and answer values are in [`SOLUTION/TRACKS/portfolio-project/CALIBRATION.md`](../../SOLUTION/TRACKS/portfolio-project/CALIBRATION.md).

The Python regression tests deliberately corrupt duplicate rows, prices, tokens, foreign keys, rework values, and demo records to establish that those errors are rejected. Dashboard tests separately exercise metric calculations and filter scope.

After validation, [`analyze_case_study.py`](../scripts/analyze_case_study.py) independently prices the canonical CSV records with `Decimal` and writes eight compact evidence tables under `SOLUTION/TRACKS/portfolio-project/outputs/`: scope, campaign, department, issue, model, product, workflow, and sensitivity summaries. These support the completed case-study answers and retain their scope labels. They are excluded from learner packages.

## 3. Package the learner tracks

[`package_learners.py`](../scripts/package_learners.py) reads each track's canonical CSVs from `DATA/TRACKS/` and its four Markdown guides from `QUESTIONS/TRACKS/`. An explicit filename and schema allowlist keeps completed analyses, scripts, tests, and calculated answer columns out of the archives.

Both ZIPs have a flat layout: an Excel workbook containing the raw data, CSV file(s), four Markdown guides, `START_HERE.html`, `LICENSE`, and `DATA_LICENSE`. The workbook retains the source rows and cleaning exercise without calculated answers. The packaged HTML links to the files beside itself and works offline after the complete ZIP is extracted. Repository question briefs and HTML guides use direct GitHub file links under `raw.githubusercontent.com` and provide a link to browse the source folder on GitHub. The marked online download section is omitted from the packaged Markdown and HTML. The archive's `DATA_LICENSE` is sourced from the repository's `DATA/LICENSE`.

The packager normalizes text to UTF-8/LF, fixes ZIP timestamps and permissions, sorts entries, and stores entries without compression to avoid zlib-dependent bytes. Excel files enter the archive as the exact checked-in binary snapshots; the parity test independently checks every cell against its CSV source and requires numeric/date fields to have native Excel types. Given those input snapshots, packaging is deterministic. Regenerating a workbook can change its internal metadata bytes without changing its source values. The packager verifies the entry allowlist and CRC. The release archive in `DATA/TRACKS/<track>/` and dashboard download copy are byte-identical. The completed Quick Challenge workbook lives in `SOLUTION/TRACKS/quick-challenge/` and is excluded from these archives. `--check` recomputes all outputs and fails if any are stale or missing.

## 4. Build and present the dashboard

[`TECHNICAL/dashboard/metrics.mjs`](../dashboard/metrics.mjs) prices prompts in integer microdollars and aggregates them to tasks before combining costs with human time. Totals and ratios are calculated at the selected scope and rounded for display. Rework remains part of actual hours.

Task filters retain each selected task's full prompt history. Daily spending uses prompt usage dates; that chart's date range does not allocate task hours or change task ROI. Whole-campaign financial results count revenue and other spending once and use only the campaign filter. Baseline sensitivity changes estimated no-AI hours while actual effort and AI spending remain fixed.

`npm --prefix TECHNICAL run build` validates the clean task population and the learner download presence, then copies the dashboard to `TECHNICAL/dist/`. Hosting instructions are documented separately in [DEPLOYMENT.md](DEPLOYMENT.md).

## Continuous validation and limits

The [GitHub workflow](../../.github/workflows/validate.yml) runs independent source reconciliation, Python regression tests, JavaScript tests, package freshness checks, and the static build. The checked-in data and downloads make both learning tracks usable without running a generator.

Deterministic generation and reconciliation establish internal consistency. They do not make this synthetic case a causal experiment, a real provider benchmark, a validated estimate of payroll savings, or a timed human learner pilot.
