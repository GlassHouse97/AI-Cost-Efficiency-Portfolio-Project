# Project scripts

Use Python 3.10+ and Node.js 22+. The Python scripts require only the standard library. Run Node/npm commands from the repository root. The generator and validator reveal solution details; learners can use the checked-in CSVs and guides without running them.

| Script | Purpose | Files written |
| --- | --- | --- |
| [generate_data.py](generate_data.py) | Recreate the fixed-seed synthetic scenario and both raw learner datasets. | Five CSVs under `data/`; cleaned `dashboard/demo-data.json`. |
| [validate_data.py](validate_data.py) | Independently calculate and reconcile source data, both tracks, and the dashboard. | None by default; `--write-checks` writes `SOLUTION/outputs/check_totals.json`. |
| [analyze_case_study.py](analyze_case_study.py) | Rebuild scoped evidence tables for the completed case-study answers from the canonical CSVs. Run validation first. | Eight summary CSVs under `SOLUTION/outputs/`. |
| [package_learners.py](package_learners.py) | Generate offline learner HTML and deterministic ZIPs from the canonical CSVs and learner guides. | `learners/*/START_HERE.html`, `release/*.zip`, and matching `dashboard/downloads/*.zip`. `--check` writes nothing. |
| [build.mjs](build.mjs) | Verify the demo population/download files and copy the static dashboard. | `dist/`. Run with `npm run build`. |
| [serve.mjs](serve.mjs) | Serve the dashboard for local development on loopback. | None. Run with `npm run dev -- --port 4327`. |
| [server.mjs](server.mjs) | Serve the production dashboard on `0.0.0.0:$PORT` (default 8080), with `/health`. | None. Run with `npm start`; also used by the Cloud Run container. |
| [sync-portfolio.mjs](sync-portfolio.mjs) | Optional manual helper for copying a completed dashboard into the separate compatible portfolio checkout. | Files in the explicitly supplied portfolio destination. It is not part of build, validation, or Cloud Run deployment. |

## Reproduce and check

```sh
python scripts/generate_data.py
python scripts/validate_data.py --write-checks
python scripts/analyze_case_study.py
python scripts/package_learners.py
python -m unittest discover -s tests -p "test_data.py" -v
npm test
python scripts/package_learners.py --check
npm run build
```

For a read-only verification of the checked-in sources and packages, omit generation, analysis, `--write-checks`, packaging without `--check`, and the build step. Use the [data pipeline](../docs/DATA_PIPELINE.md) for grain, rounding, archive layout, and reproduction details, and the [deployment guide](../docs/DEPLOYMENT.md) for hosting.
