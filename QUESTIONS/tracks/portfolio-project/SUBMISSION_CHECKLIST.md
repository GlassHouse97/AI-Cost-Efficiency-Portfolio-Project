# Portfolio Project deliverable checklist

## Deliver your work

- An interactive dashboard with up to three views: Company overview, Campaign comparison, and Workflow investigation.
- Preparation steps in a reproducible query, script, workbook, or clear tool instructions, including duplicate handling and department standardization.
- A short findings page explaining the focal campaigns, costs, effort, workflow patterns, full campaign results, and baseline sensitivity.
- Two or three supported recommendations, each tied to evidence and accompanied by a relevant caveat.
- Definitions and assumptions visible to the reviewer, including the $50 hourly rate, fictional fixed prices, row meanings, and filter behavior.
- A brief disclosure of any outside AI help and your own role in the work.

## Validate the source and transformations

- Check unique IDs in every cleaned table and document raw versus cleaned record counts.
- Confirm 240 unique tasks, 60 per campaign, and eight employees across four standardized departments.
- Confirm every prompt matches exactly one task and its campaign.
- Confirm each task uses one product and model, and every model maps to one unique price row.
- Confirm tokens are nonnegative integers and required hours and prices are populated.
- Confirm actual and rework hours are nonnegative, with rework no greater than actual hours.
- Derive prompt charges from token counts and rates, with six decimal places if stored and rounding only for display.
- Aggregate prompts before joining hours; prove task row counts and total hours are unchanged by that join.
- Aggregate task financial measures to one campaign row before adding revenue and other spending.
- Reconcile AI costs and token totals between prompt, task, campaign, and company summaries.

## Validate the dashboard and interpretation

- Show input and output tokens and their separate costs, prompt count, cost per prompt, baseline and actual hours, net AI value, and aggregate ROI.
- Use ratios of totals and show N/A for zero denominators.
- Provide meaningful campaign, department, product, and model filters for task-level operating measures.
- Label the full campaign financial panel and keep department, product, model, and prompt-date filters from changing whole-campaign profit or whole-campaign ROI.
- Use usage_date for daily spending and explain that its date filter applies to prompt measures only.
- Show the same whole-campaign totals consistently across views.
- Distinguish net AI value from overall campaign result and estimated staff capacity from payroll cash savings.
- Compare similar tasks when discussing rework, corrections, brief changes, and templates; report sample counts and avoid causal claims or employee rankings.
- Recalculate net AI value with baselines 20% lower and higher, then explain whether the conclusions change.
- Make USD, token, hour, and percentage units clear and preserve negative values.
- If you publish your completed solution, label it clearly as a completed demo containing spoilers and keep raw learner downloads separate.

## Evidence for your findings page

State the decision MRU faces, briefly explain how you priced prompts and protected task hours from duplication, summarize the results you calculated, and give two or three concrete actions. Include the sensitivity result and the limits of an observational synthetic dataset. Support claims with your own numbers; this learner package does not supply campaign conclusions.
