# AI Cost Efficiency & Workflow Value: Case-Study Questions

This document defines the business problem, analysis rules, and evidence expected from a completed answer. The [finished dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app) and [solution index](../SOLUTION/README.md) answer the questions. Learners can use the separate [quick](tracks/quick-challenge/README.md) or [deeper](tracks/portfolio-project/README.md) brief before reading the solution.

## Choose Your Track

| Track | Scope | Start | Complete package |
| --- | --- | --- | --- |
| Quick Challenge | 120 focal tasks; about four hours; no joins required | [Brief and instructions](tracks/quick-challenge/README.md) | [Excel, CSV, and guidance ZIP](../DATA/downloads/mru-quick-challenge.zip?raw=true) |
| Portfolio Project | 240 tasks and 3,360 prompts; about 12–16 hours | [Brief and instructions](tracks/portfolio-project/README.md) | [Excel, CSVs, and guidance ZIP](../DATA/downloads/mru-portfolio-project.zip?raw=true) |

Use either the Excel workbook or its matching CSV files; both contain the same raw inputs. Open `START_HERE.html` inside either downloaded ZIP for the offline guide. The [data guide](../DATA/README.md) describes each source. Completed answers are linked below, so learners who want to work independently can stay within their track brief first.

## Business Context

Marketing-R-Us uses the fictional ChatABC platform for campaign planning, writing, data work, and summaries. Leadership needs to assess whether estimated staff time saved justifies token fees, identify work that loses value, and decide which workflows to keep or improve. The deeper project also evaluates complete campaign results after other spending, labor value, and AI fees.

Everything in this September 2026 scenario is synthetic. Campaigns 1 and 2 form the focal comparison: 120 completed tasks. The full company includes Campaigns 3 and 4: 240 tasks and 3,360 prompts. Every task belongs to one department, product, and model. Baseline hours estimate the same completed work at acceptable quality without AI.

## Reporting Rules

1. Preserve the raw files. Remove exact repeated task IDs; reject conflicting duplicates. Trim and standardize department labels.
2. Price input and output tokens using their separate model rates. Aggregate prompt records to one row per task before combining with hours.
3. Count baseline, actual, and rework hours once per task. Actual hours already include rework, preparation, prompting, review, and corrections.
4. Value staff time at **$50 per hour**. Calculate hours saved as baseline minus actual hours, then subtract AI fees from that time value.
5. Calculate ROI as summed net AI value divided by summed AI cost, multiplied by 100. Calculate cost per prompt from total cost and total prompt count. Show N/A for zero denominators.
6. Count revenue and other spending once per campaign. Whole-campaign financial results accept only the campaign filter. Do not assign complete-campaign revenue to department or model subsets.
7. Use prompt `usage_date` for daily spending. A date filter does not move completed-task hours or campaign revenue into that date range.
8. State the population and filters in every table and image. Use **Campaigns 1 and 2** for the quick answer; label any all-four-campaign extension explicitly.
9. Compare the same task types where possible. Treat template use, changed briefs, rework, and model choice as observations, without claiming causal effects or ranking employees.
10. Treat net AI value as estimated staff capacity value. It is neither payroll cash saved nor campaign profit.

## What Each Answer Includes

- The original question and a direct business answer.
- A compact result table with units and scope.
- An actual dashboard screenshot with its filter state stated in the caption.
- The calculation or reproducible source supporting the figures.
- The business implication and the limits of the evidence.

Run `python TECHNICAL/scripts/analyze_case_study.py` after source validation to regenerate the result tables in [SOLUTION/outputs/](../SOLUTION/outputs/). [Dashboard calculations](../TECHNICAL/dashboard/metrics.mjs) provide a separate implementation for comparison.

## Question 1: Usage and Cost

**How many input and output tokens did each campaign use, what did they cost, and how many prompts were made?**

Calculate input tokens, output tokens, separate input/output costs, total AI cost, prompt count, and cost per prompt. Compare volume and model mix at the fixed fictional rates. Ask whether the higher bill comes from more tokens, a more expensive mix, or both.

**Answer:** [Usage, costs, and model/product mix](../SOLUTION/01_usage_and_costs.md).

## Question 2: Human Effort

**How many hours did each campaign save or lose against its no AI estimate?**

Compare baseline and actual task hours, preserve negative savings, and value the difference at $50 per hour. Test baseline estimates at −20% and +20%. Ask which conclusions retain their sign and which depend on the baseline assumption.

**Answer:** [Time saved and baseline sensitivity](../SOLUTION/02_time_saved.md).

## Question 3: Net Value

**After paying for AI, was estimated net value positive or negative for each campaign?**

Calculate net AI value and aggregate AI ROI. For the deeper track, calculate campaign results after revenue, other spending, actual labor value, and AI fees. Explain why these measures answer different questions.

**Answer:** [Net AI value and whole-campaign results](../SOLUTION/03_value_and_campaign_results.md).

## Question 4: Department Comparison

**Which department had the highest AI spending, and which had the highest net AI value?**

Compare departments across the same population. Start with the focal campaigns, then show the all-company extension separately. Ask whether spending leadership also implies value leadership, and whether close rankings matter operationally.

**Answer:** [Department spending and value](../SOLUTION/04_department_analysis.md).

## Question 5: Rework and Issues

**Which campaign had more rework, and which recorded issues appeared most often?**

Compare rework hours and their share of actual hours, correction prompts, primary issue counts, changed briefs, and template use. Distinguish `None` from a reported problem. In the deeper track, compare similar task types and disclose small groups and selection differences.

**Answer:** [Workflow investigation](../SOLUTION/05_workflow_investigation.md).

## Question 6: Strategic Recommendation

**Should MRU keep, change, or reduce how it uses AI? Give two actions supported by the numbers.**

Combine costs, human effort, rework, and uncertainty into two practical actions. For each action state the evidence, expected benefit, and measure that would establish whether it helped. Keep campaign-level averages from becoming blanket rules for every task.

**Answer:** [Strategic recommendations](../SOLUTION/06_strategic_recommendations.md).

## Deeper Project Questions

The deeper brief's original questions are retained below, with their answer locations. These extend the same case; they do not create a second, inconsistent set of results.

| Original deeper question | Completed answer |
| --- | --- |
| 1. For each campaign, what are input and output tokens, their separate costs, total AI cost, prompt count, cost per prompt, hours saved, net AI value, and ROI? | [Usage and cost](../SOLUTION/01_usage_and_costs.md), [human effort](../SOLUTION/02_time_saved.md), and [value](../SOLUTION/03_value_and_campaign_results.md) |
| 2. How do the focal campaigns C001 and C002 differ in product and model mix? Is spending associated with token volume, model prices, repeated work, or several of these? | [Model and product mix](../SOLUTION/01_usage_and_costs.md#deeper-analysis-model-and-product-mix) |
| 3. Within similar task types, what patterns appear in rework, correction prompts, changed briefs, and template use? Avoid employee rankings and do not claim causation from observed associations. | [Similar-task comparison](../SOLUTION/05_workflow_investigation.md#deeper-analysis-compare-similar-work) |
| 4. What is each whole campaign's result after other spending, human labor value, and AI fees? Explain why campaign profit or loss differs from net AI value. | [Whole-campaign results](../SOLUTION/03_value_and_campaign_results.md#deeper-analysis-whole-campaign-financial-results) |
| 5. How do net AI values change when baseline hours are 20% lower or 20% higher? Which conclusions are sensitive to that assumption? | [Baseline sensitivity](../SOLUTION/02_time_saved.md#deeper-analysis-baseline-sensitivity) |
| 6. What two or three practical actions would you recommend, and what evidence and caveats support each? | [Strategic recommendations](../SOLUTION/06_strategic_recommendations.md) |

## Outside the Current Scope

No real vendor comparison, subscription allocation, billing credits, cached-token pricing, prediction model, employee scoring, causal experiment, or realized payroll saving is implied. The supplied fictional rates keep the focus on analytical method. The learner packages supply raw Excel and CSV inputs with guidance. The completed dashboard and written answers are separate deliverables in SOLUTION; the learner workbooks do not contain a solved analysis.
