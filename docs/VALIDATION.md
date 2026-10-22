# Validation record

Release preparation: October 22, 2026.

## Data and calculation checks

- The independent Python validator reads the learner CSVs and recalculates prices using Decimal arithmetic without importing the generator or trusting saved answer totals.
- Ten Python regression tests cover exact reconciliation, duplicate conflicts, invalid tokens, incorrect prices, broken task/campaign joins, rework bounds, repeated prompts, premature monetary rounding, and divergence between demo data and source records.
- Eight JavaScript tests cover the focal campaign results, aggregate ratios, task-hour grain, whole-campaign scope, sensitivity signs, daily cost reconciliation, empty cohorts, duplicate conflicts, and dimension totals.
- An additional independent raw-record comparison reconciled 375 combinations of campaign, department, product, and model filters for prompt costs, task hours, daily totals, and baseline sensitivity.
- The 240-task browser CSV export independently summed to $3,180 in AI costs and $2,820 in net AI value. Exported costs retain six decimals.

## Interactive browser checks

The local dashboard was inspected at desktop and 390-pixel phone widths. Checks covered all three views, campaign and model selection, sensitivity endpoints, task-type comparisons, daily date boundaries, invalid date ranges, reset behavior, and CSV export. No browser errors were observed. A phone-width token-count overflow was corrected and rechecked.

Selecting Campaign 2 and Lite changed task AI spending to $320 while whole-campaign AI spending remained $1,400 and campaign result remained -$2,400. Setting a September 10–15 prompt-date range for Campaign 1 narrowed the daily chart to $109.02 without changing its $500 full-task cost or $4,500 estimated net value.

The portfolio homepage and new case study were inspected. A narrow-screen case-study grid overflow was corrected so the result table scrolls within its container. Existing portfolio projects remain present.

## Learner packages

Archives use explicit allowlists and contain the raw CSVs, brief, column guide, formulas, submission checklist, offline HTML guide, and licenses. Generator code, exact answer totals, completed analysis, dashboard, and tests are excluded. Both hosting downloads must match the corresponding release bytes. Package checks run in CI.

See [the learner walkthrough](learner-dry-run.md) for the timed author check and its limits. There was no novice pilot or timed Excel submission. Four hours is a design target, not a measured beginner completion time.

## Release gates

Before publication, run the Python validator/tests, JavaScript tests, package freshness check, static dashboard build, and portfolio Astro build. Verify the production build status and live dashboard/download responses after the production push. This record describes local release preparation; GitHub checks and the live Cloudflare build provide the commit-specific publication evidence.
