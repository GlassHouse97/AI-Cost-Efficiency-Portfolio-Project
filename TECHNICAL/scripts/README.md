# Project scripts

Use Python 3.10+ and Node.js 22+. The Python scripts require only the standard library. Run Node/npm commands from the repository root. The generator and validator reveal solution details; learners can use the checked-in CSVs and guides without running them.

The dashboard runtime has no npm dependencies. Rebuilding the optional Excel workbooks uses a separate [workbook authoring helper](../workbook-tools/README.md) and the Codex artifact runtime; ordinary data validation, workbook/CSV parity tests, packaging, and hosting do not require it.

| Script | Purpose | Files written |
| --- | --- | --- |
| [generate_data.py](generate_data.py) | Recreate the fixed-seed synthetic scenario and both raw learner datasets. | Five CSVs under `DATA/`; cleaned `TECHNICAL/dashboard/demo-data.json`. |
| [validate_data.py](validate_data.py) | Independently calculate and reconcile source data, both tracks, and the dashboard. | None by default; `--write-checks` writes `SOLUTION/TRACKS/portfolio-project/outputs/check_totals.json`. |
| [analyze_case_study.py](analyze_case_study.py) | Rebuild scoped evidence tables for the completed case-study answers from the canonical CSVs. Run validation first. | Eight summary CSVs under `SOLUTION/TRACKS/portfolio-project/outputs/`. |
| [package_learners.py](package_learners.py) | Generate offline learner HTML and deterministic ZIPs from the canonical CSVs, raw-data Excel workbooks, and learner guides. | `QUESTIONS/TRACKS/*/START_HERE.html`, `DATA/TRACKS/*/*.zip`, and matching `TECHNICAL/dashboard/downloads/*.zip`. `--check` writes nothing. |
| [build.mjs](build.mjs) | Verify the demo population/download files and copy the static dashboard. | `TECHNICAL/dist/`. Run with `npm --prefix TECHNICAL run build`. |
| [serve.mjs](serve.mjs) | Serve the dashboard for local development on loopback. | None. Run with `npm --prefix TECHNICAL run dev -- --port 4327`. |
| [server.mjs](server.mjs) | Serve the production dashboard on `0.0.0.0:$PORT` (default 8080), with `/health`. | None. Run with `npm --prefix TECHNICAL start`; also used by the Cloud Run container. |
| [sync-portfolio.mjs](sync-portfolio.mjs) | Optional manual helper for copying a completed dashboard into the separate compatible portfolio checkout. | Files in the explicitly supplied portfolio destination. It is not part of build, validation, or Cloud Run deployment. |

## Reproduce and check

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

If canonical CSV content changes, rebuild the Excel files with the [workbook helper](../workbook-tools/README.md) before packaging. The learner-file tests compare every workbook row and value with its canonical CSV, so outdated workbook copies fail validation. With the unchanged fixed seed, the committed workbooks are already the matching raw-data copies.

For a read-only verification of the checked-in sources and packages, omit generation, analysis, `--write-checks`, packaging without `--check`, and the build step. Use the [data pipeline](../docs/DATA_PIPELINE.md) for grain, rounding, archive layout, and reproduction details, and the [deployment guide](../docs/DEPLOYMENT.md) for hosting.
