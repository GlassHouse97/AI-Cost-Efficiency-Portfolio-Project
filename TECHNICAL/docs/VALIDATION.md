# Validation record

Initial release: October 22, 2026. Reader-focused restructuring: October 23, 2026.

## Aligned tracks and Quick Challenge Excel solution — October 23

- `DATA/TRACKS/`, `QUESTIONS/TRACKS/`, and `SOLUTION/TRACKS/` now use the same `quick-challenge` and `portfolio-project` subfolders. Each data track keeps its raw Excel workbook, CSV files, and complete learner ZIP together. Root navigation distinguishes the completed quick workbook from the deeper dashboard case study.
- The completed quick workbook has four sheets: **Solution**, **Summaries**, **Clean**, and **Raw**. Raw retains all 122 original records. Clean contains 120 unique tasks after removing the exact repeated exports for `W0018` and `W0087` and normalizing department labels. Formula columns derive costs, hours saved, time value, and net AI value.
- The Solution sheet answers all six Quick Challenge questions and contains two native editable charts. Campaign, department, and issue summaries use transparent `SUMIFS` and `COUNTIFS` formulas. The quick scope reconciles to $1,900 AI cost, 30 hours saved, and −$400 estimated net AI value; the deeper four-campaign scope remains +$2,820.
- Authoring-engine recalculation checks changed the hourly value to $60 and verified Campaign 1 / Campaign 2 net values of $5,500 / −$5,600 and the updated rate label. Adding one actual hour to the final cleaned task changed Campaign 2 to −$4,950. Zeroing token rates returned N/A ROI. Every changed input was restored, then the saved $50/hour case and ratios were rechecked. The final error scan found no spreadsheet calculation errors.
- Missing native-chart display caches in the authoring export were filled from the same workbook's saved worksheet values. The compatibility helper leaves formulas, source inputs, and all non-chart ZIP parts unchanged. Independent checks verify both charts' live cell references and all 12 cached points; only the two chart XML parts differ after the compatibility step, and all other ZIP parts are byte-identical. The charts remain editable.
- All **27 regression tests** pass: 17 Python and 10 JavaScript. Five solution-workbook tests independently reconcile source and cleaned records, task formulas, campaign totals and ROI, department/issue results, and native chart references/caches. The workbook has no error cells, macros, external workbook links, or external data connections. Source validation, evidence-table regeneration, learner-package freshness, and static build also pass.
- Eight rendered worksheet regions were inspected for layout and traceability. Validation uses the spreadsheet authoring engine and independent OOXML checks; a native Microsoft Excel application was not available for an application-level opening test.
- Navigation checks passed for 293 Markdown links, 32 repository HTML links, 19 anchors, four canonical GitHub targets, and 17 local targets in the standalone ZIP guides. Local paths were checked against actual directory entries for exact case. The solved-workbook links point to SOLUTION; input-workbook links point to DATA.
- Completed workbook: 56,978 bytes; SHA-256 `0a1977c1135006eca30354aab47aeebe1a9a1a582ca676d2efaa6161f10f072f`. The four-sheet structure, three frozen identifier columns, and six frozen header rows on Raw and Clean survive export.
- The answer-free learner ZIP contents remain unchanged. They contain the raw input workbooks and guides, while the completed Excel answer is available only from the separate solution track.

## Calculation hints and reader guidance — October 23

- Added short calculation explanations to all six headline metrics, whole-campaign result, full AI ROI, and workflow rework share. Headline examples use the active selection; spending and ratio examples disclose display rounding.
- Browser checks covered all six headline explanations, keyboard focus, Escape, repeated-click dismissal, filter/view changes, Campaign 2's negative value, an empty cohort's N/A ROI, and DataFlow's rounded cost components. At a 390-pixel phone viewport, the metric and table popups fit the screen without adding page overflow. No browser errors were observed.
- All **22 regression tests** pass. Source validation, unchanged evidence-table regeneration, learner-package freshness, and static build also pass. The metric calculations and learner data are unchanged.
- The root README now gives separate portfolio-review and learner routes. The technical overview explains HTML/CSS/JavaScript, the Node.js server, and the manual Cloud Build → Artifact Registry → Cloud Run deployment; Git pushes run validation only.
- Cloud Run revision `ai-cost-efficiency-00005-8bv` is ready with 100% of traffic. Image digest: `sha256:63229de5f21231cb7662610cfb5d617f4c604b61bb49392fc93faa5ddb88f98c`.
- The live health endpoint returned HTTP 200. All dashboard source assets, the dataset, and both learner ZIPs match the local release bytes. A live-browser check confirmed the new net-value explanation and no console errors.

## Reader-focused release checks — October 23

- The root now presents `QUESTIONS/`, `DATA/`, `SOLUTION/`, and `TECHNICAL/`. Source, test, dependency, container, and deployment files moved into `TECHNICAL/`; GitHub workflow and repository-wide Git metadata remain at their required scope.
- The root README is 61 lines, with a short business problem, direct navigation, three findings, one dashboard image, and the two complete learner downloads.
- Both learner ZIPs now include a native Excel workbook, every matching CSV, four Markdown guides, the offline HTML guide, and licenses. Excel and CSV are alternative representations of the same inputs.
- Independent OOXML tests compare every worksheet cell with its canonical CSV, preserve raw duplicates/whitespace, verify native numeric/date types, reject formulas/error cells, and check package contents. Seven rendered worksheet regions covering all five sheets were visually inspected.
- All **22 regression tests** pass: 12 Python and 10 JavaScript. Source validation, evidence regeneration, package freshness, static build, and whitespace checks also pass. Isolated regeneration reproduced all 14 source/demo/evidence files exactly after relocation.
- Navigation checks verified 195 Markdown/image targets and anchors, plus 34 HTML targets across the repository guides and both standalone archives. All six original quick questions remain intact.
- Cloud Run revision `ai-cost-efficiency-00004-jzz` is ready and receives 100% of traffic. Image digest: `sha256:d8abfc5c46830ed95fda7f4835f6443bc2a846a7a8913af660577c1510ce06bd`.
- The live page and `/health` returned HTTP 200. Both live downloads match the local package bytes and contain the new Excel workbooks. The live browser displays the Excel + CSV labels, loads all 240 tasks, and reports no browser errors.
- Quick ZIP SHA-256: `4c031b4f22ffa29cf8b68932bfc8b06a0eb709a3c1944ed5af292c52a7b01af7`; portfolio ZIP SHA-256: `1b327ec85b23c3117f6acc57dbfbe81ab6a0e5ab33fcc0e8cf35666883ba30c2`.

The following sections retain the initial release's calculation and browser evidence; the scenario values are unchanged.

## Data and calculation checks

- The independent Python validator reads the learner CSVs and recalculates prices using Decimal arithmetic without importing the generator or trusting saved answer totals.
- Ten Python regression tests cover exact reconciliation, duplicate conflicts, invalid tokens, incorrect prices, broken task/campaign joins, rework bounds, repeated prompts, premature monetary rounding, and divergence between demo data and source records.
- Ten JavaScript tests cover the focal campaign results and combined quick-challenge selection, aggregate ratios, task-hour grain, whole-campaign scope, sensitivity signs, daily cost reconciliation, empty cohorts, duplicate conflicts, dimension totals, and the production HTTP server's routes, methods, download bytes, and path boundaries.
- Eight case-study CSV evidence tables (262 rows) were independently reconciled against SQLite queries over the raw source files. Regeneration reproduced all eight files exactly; CI now checks that they stay current.
- An additional independent raw-record comparison reconciled 375 combinations of campaign, department, product, and model filters for prompt costs, task hours, daily totals, and baseline sensitivity.
- The 240-task browser CSV export independently summed to $3,180 in AI costs and $2,820 in net AI value. Exported costs retain six decimals.

## Interactive browser checks

The local dashboard was inspected at desktop and 390-pixel phone widths. Checks covered all three views, campaign and model selection, sensitivity endpoints, task-type comparisons, daily date boundaries, invalid date ranges, reset behavior, and CSV export. No browser errors were observed. Phone-width token-count and sensitivity-grid overflows were corrected and rechecked. All three views fit the phone viewport; wide tables scroll inside their panels. The final live campaign comparison was also rechecked at phone width.

Selecting Campaign 2 and Lite changed task AI spending to $320 while whole-campaign AI spending remained $1,400 and campaign result remained -$2,400. Setting a September 10–15 prompt-date range for Campaign 1 narrowed the daily chart to $109.02 without changing its $500 full-task cost or $4,500 estimated net value.

The six dashboard evidence screenshots were inspected against their captions and filters. They are actual browser captures; the [image record](../../SOLUTION/TRACKS/portfolio-project/visualizations/README.md) documents their scope. All six original quick questions and six deeper questions are retained or mapped to completed answers. The repository's local documentation and image links resolve.

## Learner packages

Archives use explicit allowlists and contain the raw Excel workbook and matching CSVs, brief, column guide, formulas, submission checklist, offline HTML guide, and licenses. Generator code, exact answer totals, completed analysis, dashboard, and tests are excluded. Both hosting downloads must match the corresponding release bytes. Package checks run in CI.

See [the learner walkthrough](learner-dry-run.md) for the timed author check and its limits. There was no novice pilot or timed Excel submission. Four hours is a design target, not a measured beginner completion time.

## Release gates

The Python validator, all 20 regression tests (10 Python and 10 JavaScript), package freshness check, static build, and whitespace checks passed. The GitHub workflow repeats validation, evidence-table regeneration, tests, packaging checks, and the build on each push.

## Cloud Run release

Verified October 22, 2026:

- Public dashboard: [ai-cost-efficiency-860922042669.us-east1.run.app](https://ai-cost-efficiency-860922042669.us-east1.run.app).
- Project `chris-delgados-data-portfolio`, region `us-east1`, service `ai-cost-efficiency`.
- Ready revision `ai-cost-efficiency-00003-pb7`, receiving 100% of traffic.
- Container image digest: `sha256:ae016df5fe8aef912142b6397539867022c15b2b38aa4636cd41ec792b425c26`.
- The public page, `/health`, JavaScript, styles, dataset, and both ZIP downloads returned HTTP 200. Application asset/download bytes matched the local release SHA-256 values.
- Live browser checks confirmed all-company totals ($3,180 cost / $2,820 net value), the focal 120-task cohort ($1,900 / -$400), and Campaign 2 + Lite ($320 task cost while whole-campaign cost stays $1,400 and campaign result stays -$2,400). The workflow view loaded correctly; no browser errors were observed.

The health endpoint is `/health` to avoid Google's reserved paths. See [deployment and rollback](DEPLOYMENT.md). Portfolio-site connection and Cloudflare publication belong to the owner's separate project; they are not a release gate for this independently hosted dashboard.
