# Portfolio Project metric formulas

Use **$50 per hour** for every employee. Use the two supplied fixed fictional model prices: Lite input 10 and output 30 USD per million; Pro input 40 and output 100 USD per million.

## Prompt level

After joining each prompt to exactly one model price row:

| Metric | Formula |
| --- | --- |
| `total_tokens` | input_tokens + output_tokens |
| `input_cost_usd` | input_tokens × input_rate_usd_per_million ÷ 1,000,000 |
| `output_cost_usd` | output_tokens × output_rate_usd_per_million ÷ 1,000,000 |
| `ai_cost_usd` | input_cost_usd + output_cost_usd |
| Prompt count | Count distinct usage_id after cleaning; one row is one employee prompt. |

Retain full precision during calculations. If costs are stored, retain six decimal places. Display USD to cents and do not round each prompt to cents before summing. Use integer token counts and the supplied whole-dollar rates, so the costs are traceable to their inputs.

## Task level

First aggregate input tokens, output tokens, input cost, output cost, total cost, and prompt count to one row per task, then join work_log. Carry each task's single model and product through the aggregation. Include all its prompts when comparing complete task hours.

| Metric | Formula |
| --- | --- |
| `hours_saved` | baseline_hours − actual_hours |
| `time_value_usd` | hours_saved × 50 |
| `net_ai_value_usd` | time_value_usd − ai_cost_usd |

Actual hours already include rework. Do not add it again. A task's 1.5 actual hours remain 1.5 hours even if it has 20 prompts.

## Group metrics

For each selected campaign, department, product, model, or task type, sum the appropriate task or prompt numerators and denominators first.

| Metric | Formula |
| --- | --- |
| AI ROI percentage | sum(net_ai_value_usd) ÷ sum(ai_cost_usd) × 100 |
| Average cost per prompt | sum(ai_cost_usd) ÷ sum(prompt_count) |
| Rework share percentage | sum(rework_hours) ÷ sum(actual_hours) × 100 |
| Correction share percentage | count(Correction prompts) ÷ count(all prompts) × 100 |
| Input spending share percentage | sum(input_cost_usd) ÷ sum(ai_cost_usd) × 100 |
| Output spending share percentage | sum(output_cost_usd) ÷ sum(ai_cost_usd) × 100 |

Show **N/A** if a denominator is zero. Never average row ROI or row cost per prompt. ROI can be below −100% when human effort also increases. In Excel, divide numerator by denominator and apply Percentage formatting; do not multiply the already formatted fraction by 100 a second time.

Compare template use and changed briefs within comparable task types and campaigns where possible. Report group task counts alongside averages or shares. These descriptive relationships do not isolate causal effects.

## Whole campaign financial result

Aggregate actual hours and AI cost to one row per campaign before joining campaigns.csv:

`campaign_result_usd = campaign_revenue_usd − other_campaign_cost_usd − (campaign_actual_hours × 50) − campaign_ai_cost_usd`

Revenue and other costs each enter the formula once. Other spending excludes staff time and AI fees. Net AI value compares AI-assisted effort to the estimated no-AI baseline. Campaign result compares revenue to total stated costs. They answer different questions and need separate labels.

Campaign filters may select whole campaigns. Department, product, model, and prompt-date filters do not change the whole-campaign financial panel or whole-campaign ROI. If you provide ROI for a filtered task cohort, label it **Selected tasks ROI**.

## Baseline sensitivity at minus and plus 20 percent

Change baseline hours only; keep actual hours, AI fees, the $50 hourly rate, revenue, and other costs fixed.

| Scenario | Net AI value formula |
| --- | --- |
| Baseline 20% lower | ((baseline_hours × 0.8) − actual_hours) × 50 − ai_cost_usd |
| Stated baseline | (baseline_hours − actual_hours) × 50 − ai_cost_usd |
| Baseline 20% higher | ((baseline_hours × 1.2) − actual_hours) × 50 − ai_cost_usd |

Calculate these at the task level and sum, or apply the same factors to consistently scoped sums. Show the three net-value results for each focal campaign, report whether the sign changes, and explain what that implies about reliance on the baseline estimate. Campaign result does not change in this test because it uses actual hours rather than baseline hours.

## Worked example from tokens to value

This illustration is independent of the campaign answers. A Lite task has **20 prompts**, each with **10,000 input tokens** and **5,000 output tokens**. Input cost per prompt is 10,000 × 10 ÷ 1,000,000 = **$0.10**. Output cost is 5,000 × 30 ÷ 1,000,000 = **$0.15**. Each prompt costs **$0.25**, so the task costs **$5.00**.

Aggregate first: 20 prompts contain **200,000 input** and **100,000 output tokens**. The task calculation (200,000 × 10 + 100,000 × 30) ÷ 1,000,000 also equals **$5.00**. Total tokens are **300,000**.

The no-AI estimate is **2 hours** and actual time is **1.5 hours**, including review and rework. Hours saved are **0.5**; time value is **$25**; net AI value is **$20**; ROI is **400%**. Joining all 20 prompts directly to task hours and summing would wrongly create 30 actual hours. Instead, aggregate prompts first and count the task's **1.5 hours once**.
