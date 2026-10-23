# Technical implementation

This folder contains the dashboard application, reproducible analysis scripts, tests, deployment configuration, and developer documentation. Start at the [project overview](../README.md) for the business case, [questions](../QUESTIONS/README.md) for the assignment, [data](../DATA/README.md) for learner files, or [solution](../SOLUTION/README.md) for the answers.

## How it works

The dashboard is a plain **HTML, CSS, and JavaScript** application. JavaScript runs in the visitor's browser, calculates the metrics from a bundled synthetic dataset, and updates the charts and tables when filters change. There is no frontend framework, live database, or AI API call.

| Part | Where it lives | What it does |
| --- | --- | --- |
| Page and styling | [dashboard/index.html](dashboard/index.html), [dashboard/styles.css](dashboard/styles.css) | Define the layout and appearance. |
| Interactions and calculations | [dashboard/app.mjs](dashboard/app.mjs), [dashboard/metrics.mjs](dashboard/metrics.mjs) | Filter the data, calculate results, and render the dashboard in the browser. |
| Dashboard data | [dashboard/demo-data.json](dashboard/demo-data.json) | Provide the prepared synthetic records derived from the published CSV files. |
| Web server | [scripts/server.mjs](scripts/server.mjs) | Use Node.js to serve the dashboard files and learner ZIP downloads. |
| Container | [Dockerfile](Dockerfile) | Package the dashboard and server with Node.js 24 for Cloud Run. |

**GitHub stores the source; Google Cloud Run hosts the live dashboard.** Deployment is a separate manual step from the local repository: `gcloud run deploy --source TECHNICAL` sends the selected source files to Google Cloud Build, which builds the Dockerfile into a container image. Artifact Registry stores that image, and Cloud Run runs it to serve the public URL. See the [deployment guide](docs/DEPLOYMENT.md) for the complete command.

A Git push runs the repository's validation workflow; **it does not automatically deploy to Cloud Run**. Python scripts prepare and check the data before deployment. Python is not needed by the running dashboard. The portfolio website can link to this independent dashboard.

## Run the dashboard

Use Node.js 22 or newer. The dashboard and server have no npm dependencies to install. Run these commands from the repository root:

```sh
npm --prefix TECHNICAL run dev
```

Open [localhost:4327](http://127.0.0.1:4327/). To choose another port, use `npm --prefix TECHNICAL run dev -- --port 4328`. The server must serve the page over HTTP so the browser can load the bundled JSON data.

`npm --prefix TECHNICAL start` starts the production server on `0.0.0.0`, using the `PORT` environment variable or port 8080. Its health endpoint is `/health`.

## Validate and rebuild

The Python analysis and packaging scripts use Python 3.10+ and its standard library. The checked-in learner files are ready to use; generation is only needed when rebuilding sources.

```sh
python TECHNICAL/scripts/validate_data.py
python -m unittest discover -s TECHNICAL/tests -p "test_*.py" -v
python TECHNICAL/scripts/analyze_case_study.py
npm --prefix TECHNICAL test
python TECHNICAL/scripts/package_learners.py --check
npm --prefix TECHNICAL run build
```

The analysis command rebuilds eight evidence CSVs under `SOLUTION/outputs/`. The build writes `TECHNICAL/dist/`. CI also checks that regenerated evidence matches the committed tables. Running tests or building the dashboard does not deploy anything.

For the full source-generation sequence, workbook authoring, and package contents, see the [script guide](scripts/README.md) and [data pipeline](docs/DATA_PIPELINE.md). The Python scripts and direct Node server/build scripts locate inputs relative to their own files; `npm --prefix TECHNICAL` selects this folder's package from the repository root. Inside this folder, ordinary `npm test`, `npm run dev`, and `npm run build` also work.

## Folder guide

| Path | Purpose |
| --- | --- |
| [dashboard/](dashboard/) | Browser app, metric calculations, clean demo data, and hosted learner downloads. |
| [scripts/](scripts/README.md) | Fixed-seed generation, independent validation, evidence tables, packaging, servers, and optional portfolio copying. |
| [tests/](tests/) | Data integrity, learner-file parity, metric behavior, and HTTP-server regression tests. |
| [workbook-tools/](workbook-tools/README.md) | Optional workbook authoring with the Codex artifact runtime. The checked-in Excel files require no builder setup. |
| [docs/](docs/) | [Data dictionary](docs/DATA_DICTIONARY.md), [pipeline](docs/DATA_PIPELINE.md), [validation record](docs/VALIDATION.md), [deployment](docs/DEPLOYMENT.md), and [portfolio handoff](docs/PORTFOLIO_HANDOFF.md). |
| [Dockerfile](Dockerfile) | Small non-root Node container for the static app. |
| [package.json](package.json) | Dependency-free local development, test, build, and production commands. |

Cloud Run source deployment uses **this folder** as its build context: `--source TECHNICAL` from the repository root. Its ignore files allow only the dashboard, production server, Dockerfile, and ignore configuration into the upload. Follow the [deployment guide](docs/DEPLOYMENT.md) for the complete commands and checks.

## Why some files stay at the repository root

The four visible project areas are `QUESTIONS/`, `DATA/`, `SOLUTION/`, and `TECHNICAL/`. The root README remains GitHub's landing page. `.github/workflows/` stays at GitHub's required workflow location; `.gitignore` and `.gitattributes` apply repository-wide ignore and line-ending rules. The root `LICENSE` is the code/documentation license, while `DATA/LICENSE` covers the synthetic data. These small metadata files remain outside the technical folder so Git and GitHub can discover and apply them normally.
