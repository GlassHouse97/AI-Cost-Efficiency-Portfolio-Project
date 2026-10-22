# Dashboard evidence

These images are direct captures of the working dashboard, taken on October 22, 2026. They support the findings in the [completed analysis](../ANALYSIS.md). The data, people, campaigns, clients, prices, and results are synthetic.

## Capture provenance

- Source: `dashboard/index.html`, `dashboard/app.mjs`, `dashboard/metrics.mjs`, and `dashboard/demo-data.json` in this repository.
- Local preview: `node scripts/serve.mjs --port 4331`, using the same dashboard files packaged for deployment.
- Browser: Chromium in the Codex in-app browser, tested at a desktop viewport of 1600 × 1000 pixels. The campaign comparison table fit without horizontal overflow at that viewport.
- Format: original JPEG screenshots returned by the browser. Panel crops use browser screenshot clipping; the images contain no composited panels, substituted values, or AI-generated visuals.
- Data fingerprint: SHA-256 of `dashboard/demo-data.json` was `d0f2b641b8d8634c9c81a48b029d80172ce290d0682adee4227dd2257ada5176`.
- Scope: September 2026 full task history. Department, product, and model filters are set to **All** throughout. Prompt date filters are unset. Staff time is valued at the fixed fictional assumption of **$50/hour**.

## Images and reproducible filter settings

| Image | Dashboard view and filter settings | What it supports |
|---|---|---|
| [01_company_overview.jpg](01_company_overview.jpg) | Company overview; **All campaigns**; baseline assumption unchanged. | 240 tasks, 3,360 prompts, $3,180 AI spend, 120 estimated hours saved, $2,820 net AI value, and 88.7% AI ROI. |
| [02_campaign_comparison.jpg](02_campaign_comparison.jpg) | Campaign comparison; **Campaigns 1 + 2 (quick challenge)**; baseline assumption unchanged. | Exact focal-campaign token counts, prompt counts, costs, hours saved, net value, and ROI. The filter and 120-task scope are visible. |
| [03_department_analysis.jpg](03_department_analysis.jpg) | Company overview; **Campaigns 1 + 2 (quick challenge)**; baseline assumption unchanged. | The two campaigns' value and effort charts, combined token economics, and department spend/value table. Department figures cover the same 120 focal tasks as image 02. |
| [04_workflow_investigation.jpg](04_workflow_investigation.jpg) | Workflow investigation; **Campaign 2**; **All task types**. | Campaign 2 KPIs, model/product spending, recorded issues, correction prompts, and template/brief cohorts. Scope and observational caveats remain visible. |
| [05_sensitivity.jpg](05_sensitivity.jpg) | Campaign comparison; **All campaigns**; baseline adjustment set to **−20%**. | Original net value, the selected −20% scenario, and fixed ±20% comparison columns for all four campaigns. Only baseline hours change. |
| [06_campaign_profit.jpg](06_campaign_profit.jpg) | Campaign comparison; **All campaigns**; whole-campaign financial table. | Revenue less other spending, actual staff time, and AI costs. This panel always uses original assumptions and ignores department/product/model/date/sensitivity filters. |

To reproduce, start the local preview, reset filters, choose the view and campaign settings in the table, and capture the corresponding visible panel. Image 05 changes the sensitivity slider only; image 06 remains independent of that slider. Open an image at its original size to inspect the exact values.

## Reading the evidence

- Mint marks favorable values; coral marks unfavorable values. Dollar signs and explicit plus/minus signs also communicate direction.
- Estimated net AI value is **time value less AI fees**, not payroll cash savings or proof of causal impact.
- Input/output costs and model/product breakdowns describe the same underlying tasks; do not add alternative breakdowns together.
- The workflow cohorts overlap. Compare the template pair or changed-brief pair separately, and account for task mix before treating differences as evidence for a workflow change.
- A screenshot confirms what the dashboard displayed. The underlying calculation and data validation checks provide the arithmetic evidence; see the [analysis](../ANALYSIS.md) and the repository test suite.
