# Validation record

Release preparation: October 22, 2026.

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

The six dashboard evidence screenshots were inspected against their captions and filters. They are actual browser captures; the [image record](../SOLUTION/visualizations/README.md) documents their scope. All six original quick questions and six deeper questions are retained or mapped to completed answers. The repository's local documentation and image links resolve.

## Learner packages

Archives use explicit allowlists and contain the raw CSVs, brief, column guide, formulas, submission checklist, offline HTML guide, and licenses. Generator code, exact answer totals, completed analysis, dashboard, and tests are excluded. Both hosting downloads must match the corresponding release bytes. Package checks run in CI.

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
