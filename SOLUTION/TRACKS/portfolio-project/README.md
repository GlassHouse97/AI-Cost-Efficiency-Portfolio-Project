# Portfolio Project Solution

This is the completed analysis of Marketing R Us (MRU), a fictional marketing company evaluating the cost and value of AI. It covers all four campaigns, 240 completed tasks, and 3,360 prompts. **This folder and its Excel workbook contain the answers to the Portfolio Project.**

## Open the Solution

| View | What it provides |
| --- | --- |
| **[Open the dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app)** | Explore campaign results, spending, and workflow patterns using interactive filters. |
| **[Download the completed Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/SOLUTION/TRACKS/portfolio-project/mru-portfolio-project-solution.xlsx)** | Present the findings or inspect every cleaned task, priced prompt, calculation, and source record. |

For a short written account, read the [executive summary](EXECUTIVE_SUMMARY.md).

## Read the Workbook

1. Open **Solution** for the six answers, key figures, charts, and recommendations.
2. Open **Tasks** for the complete prepared dataset. Each of its 240 rows represents one completed task, with its hours, prompt totals, AI cost, and estimated net value.
3. Trace a task through **Prompt Totals** and **Priced Usage** to see its aggregated usage and individual prompt charges. The original inputs are retained in **Raw Work Log**, **Raw AI Usage**, **Model Pricing**, and **Campaign Inputs**.
4. Use **Preparation** to review the cleaning steps and reconciliation checks. **Data Dictionary** defines the source and calculated columns.

**Campaigns**, **Mix**, **Workflow**, and **Daily Usage** provide the supporting summary tables. The workbook includes all underlying records and formulas, so it can be used independently of the dashboard.

The default workbook results match the dashboard with all four campaigns selected and the stated baseline. Estimated net AI value is **$2,820** for the full company and **negative $400** for the focal Campaigns 1 and 2. These are different populations. The **$12,820 campaign result for the whole company** also includes revenue and other campaign spending, so it answers a different business question from net AI value.

## Detailed Answers

The table follows the six questions in the Portfolio Project brief. The written articles also contain the original focal campaign analysis, so their page numbers do not always match the question numbers below.

| Portfolio Project question | Workbook evidence | Written explanation |
| --- | --- | --- |
| 1. What are each campaign's tokens, input and output costs, prompts, cost per prompt, hours saved, net AI value, and ROI? | **Solution**, **Campaigns**, and **Tasks** | [Usage and costs](01_usage_and_costs.md), [human effort](02_time_saved.md), and [net AI value](03_value_and_campaign_results.md) |
| 2. How do C001 and C002 differ in product and model mix, and what is associated with their spending? | **Mix**, **Prompt Totals**, and **Priced Usage** | [Cost and model comparisons](01_usage_and_costs.md) |
| 3. Within similar task types, what patterns appear in rework, correction prompts, changed briefs, and template use? | **Workflow** and **Tasks** | [Workflow investigation](05_workflow_investigation.md) |
| 4. What is each campaign's result after other spending, human labor value, and AI fees? | **Campaigns** and **Campaign Inputs** | [Complete campaign results](03_value_and_campaign_results.md) |
| 5. How does net AI value change when baseline hours are 20% lower or higher? | **Campaigns** sensitivity columns and **Solution** | [Baseline sensitivity](02_time_saved.md) |
| 6. Which practical actions follow from the evidence, and what limitations apply? | **Solution**, supported by **Mix** and **Workflow** | [Recommendations](06_strategic_recommendations.md) |

## How the Data Was Prepared

The **Preparation** worksheet records completion of the ten steps in the learner's START_HERE document.

| Step | Completed work |
| --- | --- |
| 1. Preserve and inspect the sources | Retained the supplied records and checked row counts, dates, numeric types, and categorical values. |
| 2. Clean records and departments | Removed the exact repeated W0018 and W0087 task records, reducing the work log from 242 rows to 240 tasks. Standardized ten department labels in the unique task records. |
| 3. Validate relationships | Checked unique keys, task and campaign links, one product and model per task, and one price row per model. |
| 4. Price prompts | Matched each of the 3,360 prompts to its model prices and calculated separate input and output costs in **Priced Usage**. |
| 5. Aggregate prompts | Built one row per task in **Prompt Totals** before attaching task hours. |
| 6. Prepare task results | Combined the cleaned work log with prompt totals in **Tasks**, then calculated hours saved, time value, and net AI value once per task. |
| 7. Summarize operating results | Grouped the tasks by campaign, department, product, model, and workflow observations. Calculated ratios from summed numerators and denominators. |
| 8. Calculate campaign results | Combined each complete campaign's labor and AI costs with one revenue and other spending record in **Campaigns**. |
| 9. Retain the usage timeline | Summarized prompt spending by **usage_date** in **Daily Usage**, separately from task completion dates. |
| 10. Reconcile and test assumptions | Compared the prepared results with the dashboard data and evaluated baseline hours at 80%, 100%, and 120% of the stated estimate. |

Prompt charges retain their calculation precision. Currency formatting rounds only what is displayed. Rework remains part of actual hours and is not added to labor a second time. Revenue and other campaign spending are counted once per campaign.

## Editing the Completed Workbook

The workbook uses Excel Tables and formulas, including SUMIFS and COUNTIFS. It does not require external data connections or code to view the completed analysis.

The hourly value starts at **$50 in Solution cell C5**. Changing that value, existing task hours in **Tasks**, token counts in **Priced Usage**, prices in **Model Pricing**, or financial inputs in **Campaign Inputs** recalculates the related formulas and charts.

The raw records and prepared categories are a saved snapshot. Changing source files, adding records, or changing identifiers and grouping categories requires rebuilding the workbook. Editing the raw tabs alone does not repeat the cleaning and preparation process. Written findings and recommendations describe the supplied case and should be reviewed after input changes.

The [workbook tools guide](../../../TECHNICAL/workbook-tools/README.md) documents how the workbook is generated. Keep the supplied raw learner workbook separate if you want to attempt the exercise from its original inputs.

## Supporting Evidence

The [result tables](outputs/) contain the reproducible summaries and exact validation controls. [Dashboard images](visualizations/) support the written findings, with captions identifying their filter scope. [Analysis notes](ANALYSIS.md) explain calculation grain and interpretation, while [calibration notes](CALIBRATION.md) describe the synthetic scenario.

All organizations, employees, prices, and outcomes are fictional. Estimated time value represents staff capacity rather than payroll cash savings. Workflow patterns are observations, not evidence that a particular model, template, or brief change caused an outcome.
