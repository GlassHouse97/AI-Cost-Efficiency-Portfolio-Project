# MRU AI value Portfolio Project

**Intermediate · About 12 to 16 hours for core analysis and dashboard · Excel, Power Query, SQL, BI, or code**

<!-- ONLINE_DOWNLOADS_START -->
## Download the Data

[Download the complete Portfolio Project ZIP](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/mru-portfolio-project.zip) for the workbook, four CSVs, and all instructions. Extract the entire ZIP, then open **START_HERE.html** from the extracted folder. Keep the extracted files together so the guide can open the data offline.

For individual files, download the [Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/mru-portfolio-project.xlsx), or download all four CSVs below. The workbook and CSVs contain the same raw records. Choose one format.

| CSV | Contents |
| --- | --- |
| [work_log.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/work_log.csv) | Completed tasks and staff hours |
| [ai_usage.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/ai_usage.csv) | Prompt records and token usage |
| [model_pricing.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/model_pricing.csv) | Input and output token prices |
| [campaigns.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/campaigns.csv) | Campaign revenue and other spending |

Your browser may display CSV text. Save the page as a CSV file or use the complete ZIP. [Browse the source files on GitHub](https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/tree/main/DATA/TRACKS/portfolio-project).
<!-- ONLINE_DOWNLOADS_END -->

Marketing-R-Us (MRU) is a fictional marketing company using the fictional ChatABC AI platform. Evaluate whether the estimated value of staff time saved justifies AI spending, then explain how prompt volume, model prices, rework, and campaign economics relate. All people, clients, prices, and results are synthetic. This dataset is an analytical exercise, not evidence about a real provider or a causal experiment.

This standalone package contains `mru-portfolio-project.xlsx` with four raw data sheets, all four matching CSVs, a learner brief, column guide, metric formulas, and a deliverable checklist. Use the workbook **or** the CSV files: their source records are identical, so importing both versions of a table would double-count the data. Neither format contains completed answers. Open `START_HERE.html` for the complete offline guide. You can finish this exercise without visiting a hosted dashboard or any author files. The completed portfolio demo and public generator, if viewed separately, contain spoilers.

Campaign 1 and Campaign 2 are the focal comparison. Campaign 3 and Campaign 4 provide additional context. There are 240 unique completed tasks, 60 per campaign, and the same eight fictional employees across Content, Creative, Marketing Operations, and Analytics. CampaignChat supports planning, CopyStudio writing, DataFlow data work, and InsightDesk summaries. Every task uses one product and one model. Every prompt belongs to its task's campaign.

Value all staff time at **$50 per hour**. Actual hours include preparation, prompting, task setup, checking, and corrections. Rework is already inside actual hours. Baseline and actual hours cover the same completed task at acceptable quality. Net AI value estimates staff capacity value after AI fees; it is not payroll cash savings.

## Start with the row meanings

The workbook sheets are named `work_log`, `ai_usage`, `model_pricing`, and `campaigns`, matching the CSV filenames below. Work from a saved copy and preserve all supplied raw inputs.

| File | One row represents | Unique key after cleaning |
| --- | --- | --- |
| `work_log.csv` | One completed task | `work_item_id` |
| `ai_usage.csv` | One employee prompt | `usage_id` |
| `model_pricing.csv` | One model and its fixed prices | `model` |
| `campaigns.csv` | One campaign and its revenue and other spending | `campaign_id` |

The raw exports include repeated records and department labels that need trimming or capitalization changes. Check the relevant unique keys rather than assuming every file needs a row deleted. Do not remove legitimate separate prompts because they share a task or token count. There are no missing prices, missing baselines, or broken campaign links to repair.

## Prepare the data in this order

1. Keep raw files unchanged. Record file row counts and inspect column types. Parse dates as YYYY-MM-DD, tokens as nonnegative integers, rates and hours as numeric values, and Yes/No fields as categorical observations.
2. Remove exact repeated records using each file's unique key, then assert that the remaining keys are unique. If the same key has conflicting values, investigate instead of keeping an arbitrary row. Trim and standardize department labels to Content, Creative, Marketing Operations, and Analytics.
3. Validate that every prompt links to one work item and that its `campaign_id` agrees with the task. Confirm exactly one model and one product per task, and exactly one price row per model.
4. Join `ai_usage` to `model_pricing` on `model`. Calculate separate input and output costs for each prompt. Count one row as one employee prompt. Retain precision; no precomputed costs are supplied.
5. **Aggregate prompt rows to `work_item_id` before joining task hours.** Sum input tokens, output tokens, input cost, output cost, total cost, and prompt count. You may also summarize correction and followup counts. Carry the task's single product and model through to this task-level table.
6. Join this one-row-per-task summary to the cleaned `work_log`. Validate one resulting row per task. Calculate hours saved, time value, and net AI value once per task. Never sum task hours from a prompt-level join.
7. Group the enriched task table by campaign, department, product, and model as needed. Compute ROI and cost per prompt from summed numerators and denominators. Do not average task ratios.
8. For whole-campaign results, first aggregate labor hours and AI costs to one row per campaign, then join one campaign financial row. Subtract other spending, actual hours × $50, and AI cost from revenue. Never multiply revenue by the number of tasks or prompts.
9. Separately retain prompt-level `usage_date` for daily usage and spending. Do not substitute task completion date for the billing-style usage timeline.
10. Reconcile totals, run the baseline sensitivity exercise, and build the dashboard and findings page.

You can do this in any familiar tool. In Excel, open the supplied workbook and save your own working copy, or import each CSV as a table using **Data → From Text/CSV** and save as `.xlsx`. Use only one format of each input. Use PivotTables or Power Query to aggregate prompts before connecting task hours. In SQL or code, use a grouped prompt summary as the intermediate table. No particular stack is required.

## Analytical questions

1. For each campaign, what are input and output tokens, their separate costs, total AI cost, prompt count, cost per prompt, hours saved, net AI value, and ROI?
2. How do the focal campaigns C001 and C002 differ in product and model mix? Is spending associated with token volume, model prices, repeated work, or several of these?
3. Within similar task types, what patterns appear in rework, correction prompts, changed briefs, and template use? Avoid employee rankings and do not claim causation from observed associations.
4. What is each whole campaign's result after other spending, human labor value, and AI fees? Explain why campaign profit or loss differs from net AI value.
5. How do net AI values change when baseline hours are 20% lower or 20% higher? Which conclusions are sensitive to that assumption?
6. What two or three practical actions would you recommend, and what evidence and caveats support each?

## Dashboard views and filter meaning

Build up to three views: **Company overview**, **Campaign comparison**, and **Workflow investigation**. Show input and output tokens and cost, baseline versus actual hours, net AI value, and aggregate ROI. Filters for campaign, department, product, and model are meaningful for task-level operating metrics because each task has one product and model.

Keep the financial panel explicitly labeled **Whole-campaign financial results**. Campaign selection can choose which complete campaigns to show. Department, product, model, and prompt-date filters must not change full campaign profit or whole-campaign ROI. Do not allocate revenue or other campaign spending to those filtered subsets without an explicit allocation method, which this exercise does not require. If you show a filtered task ROI, label it **Selected tasks ROI** so it is not confused with whole-campaign ROI.

Use `usage_date` for daily spending. A date-limited prompt chart includes only the prompts in that date range; it cannot inherit complete task hours or revenue as if they were earned on those prompt dates. Keep task-level baseline, actual hours, net value, and ROI based on complete tasks. Clearly state which visuals each filter changes; a date filter may affect the usage chart alone.

The company total should be derived from summed costs and hours, and the same complete campaign should agree across every view. A weighted aggregate ROI can differ from an average of campaign ROIs; use the ratio of totals.

## Suggested project plan

| Work block | Suggested time |
| --- | --- |
| Read the brief, inspect files, and document row meanings | 1 to 2 hours |
| Clean, validate keys, price prompts, and build task aggregates | 3 to 4 hours |
| Compare campaigns and workflows; calculate sensitivity | 3 to 4 hours |
| Build and check dashboard views | 3 to 4 hours |
| Write findings and recommendations; reconcile evidence | 2 hours |

Allow extra time for publishing. These are planning estimates, not a timed learner benchmark. Keep optional features out of the core analysis.

## Scope and responsible interpretation

Do not add vendor breakdowns, invoices, subscription allocation, credits conversion, cached token pricing, a training ledger, a prediction model, causal claims, or employee rankings. Fixed fictional rates are supplied so the focus remains on the analysis. Disclose any outside AI help and be able to explain your preparation, formulas, charts, and recommendations.

Code and educational text are under the included MIT license. Synthetic Excel and CSV data is dedicated under the included CC0 1.0 license.
