# Completed analysis — contains learner exercise answers

Marketing-R-Us is a fictional marketing company using the fictional ChatABC platform. This completed case study examines whether estimated staff time saved covers AI token spending, and whether each campaign earns a positive result after other costs. All people, observations, prices, and financial outcomes are synthetic.

The reporting period is September 2026. Staff time is valued at $50 per hour. Net AI value is an estimate of staff capacity value after AI fees, not a reduction in payroll cash spending.

## The company result

Across 240 completed tasks and 3,360 employee prompts, MRU used 113.5 million tokens and incurred $3,180 in fictional AI charges. The work took 800 actual hours against a 920-hour no-AI estimate. The resulting 120 hours saved are worth $6,000, leaving $2,820 of estimated net AI value and 88.68% AI ROI.

The combined campaign result is $12,820: $95,000 revenue less $39,000 other campaign spending, $40,000 actual staff time, and $3,180 AI charges. Revenue and other spending are counted once per campaign.

| Campaign | Prompts | Tokens | AI spending | Baseline hours | Actual hours | Hours saved | Net AI value | AI ROI | Campaign result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Campaign 1 | 600 | 27.0 M | $500 | 240 | 140 | 100 | $4,500 | 900.00% | $7,500 |
| Campaign 2 | 1,200 | 42.0 M | $1,400 | 200 | 270 | -70 | -$4,900 | -350.00% | -$2,400 |
| Campaign 3 | 720 | 22.5 M | $540 | 220 | 172 | 48 | $1,860 | 344.44% | $4,360 |
| Campaign 4 | 840 | 22.0 M | $740 | 260 | 218 | 42 | $1,360 | 183.78% | $3,360 |

The company total hides a substantial difference between Campaign 1 and Campaign 2. Campaign 1 creates estimated AI value and earns a positive campaign result. Campaign 2 both loses estimated AI value and finishes with a campaign loss. These are separate measures: the first compares time value with AI fees; the second also includes revenue and other campaign costs.

## What explains the focal difference?

Campaign 2's net AI value is $9,400 below Campaign 1's. Of that gap, $8,500 comes from less estimated time value: Campaign 1 saves 100 hours while Campaign 2 loses 70, a 170-hour difference at $50/hour. The remaining $900 comes from higher AI spending. Human effort therefore explains most of the difference between these two synthetic scenarios.

AI rates did not increase. The entire $900 spending increase comes from Pro usage. Lite usage has identical totals and costs in the two campaigns; Pro token volume is six times as high in Campaign 2.

| Model measure | Campaign 1 | Campaign 2 |
| --- | ---: | ---: |
| Lite input / output tokens | 20 M / 4 M | 20 M / 4 M |
| Lite cost | $320 | $320 |
| Pro input / output tokens | 2 M / 1 M | 12 M / 6 M |
| Pro cost | $180 | $1,080 |
| Tasks using Pro | 12 of 60 (20%) | 30 of 60 (50%) |
| Pro share of AI spending | 36.00% | 77.14% |

This is a change in volume and model mix at fixed prices. It does not establish that choosing Pro caused the campaign's problems. Both Campaign 2 model cohorts have negative net AI value: -$2,147 for Lite and -$2,753 for Pro. A cheaper model alone would not address the observed extra human effort.

The workflow observations also differ:

| Observation | Campaign 1 | Campaign 2 |
| --- | ---: | ---: |
| Correction prompts | 68 | 482 |
| Corrections as a share of all prompts | 11.33% | 40.17% |
| Rework hours | 10.74 | 87.82 |
| Rework as a share of actual hours | 7.67% | 32.53% |
| Tasks with changed briefs | 10 of 60 (16.67%) | 27 of 60 (45.00%) |
| Tasks using a prompt template | 53 of 60 (88.33%) | 19 of 60 (31.67%) |

These observations support investigating repeated corrections, brief changes, and template use. They do not isolate their effects. Campaign, task difficulty, model, employee, and template selection can all differ between groups. The dashboard's task-type selector helps compare similar kinds of work while retaining that limitation.

Campaign averages are not universal rules. Campaign 1 includes eight tasks with negative net AI value, and Campaign 2 includes ten tasks with positive net AI value. Review the task-level records before deciding which workflows to retain or change.

## How sensitive are the conclusions?

The sensitivity calculation changes only estimated baseline hours. Actual hours, prices, tokens, and AI charges remain fixed.

| Campaign | Net value with baseline -20% | Original net value | Net value with baseline +20% |
| --- | ---: | ---: | ---: |
| Campaign 1 | $2,100 | $4,500 | $6,900 |
| Campaign 2 | -$6,900 | -$4,900 | -$2,900 |
| Campaign 3 | -$340 | $1,860 | $4,060 |
| Campaign 4 | -$1,240 | $1,360 | $3,960 |

The focal Campaign 1 and Campaign 2 conclusions retain their signs at both endpoints. Campaign 3 and Campaign 4 cross below zero when their baseline estimates are 20% lower. Their apparent benefit depends more on the reliability of the no-AI estimate. Whole-campaign financial results use actual costs and remain unchanged by baseline sensitivity.

## Recommended next steps

1. **Retain promising workflows and test them on comparable tasks.** Use successful Campaign 1 tasks as candidates for a controlled template trial. Compare the same task type and acceptance criteria, and measure actual effort including review and rework. The 88.33% versus 31.67% template-use difference identifies a question to test, not a proven cause.
2. **Add a brief review and a stop-and-review point for repeated corrections.** Campaign 2 records 482 corrections and 87.82 rework hours. Confirm requirements before repeated prompting and investigate tasks where corrections recur. Track whether the intervention lowers total actual hours while maintaining quality, rather than judging success only by fewer prompts.
3. **Test model routing alongside workflow changes.** Pro accounts for the full $900 extra AI spending, at unchanged prices. Trial Lite on comparable routine tasks where it meets the same quality criteria. Evaluate token cost, corrections, and human effort together; a lower token bill is not an improvement if checking and rework increase.

## Preparation and calculation grain

The raw exercise files retain two small cleaning problems. The quick export has 122 rows representing 120 tasks; the deeper work log has 242 rows representing 240 tasks. The same two focal task exports are repeated in both. Some department labels contain extra spaces or inconsistent capitalization.

1. Read `work_log.csv` at one row per completed task. Remove exact duplicate `work_item_id` records; conflicting duplicates are errors. Trim department labels and map capitalization to the four canonical department names. Preserve the original task hours and Yes/No observations.
2. Read `model_pricing.csv` at one row per model. Verify the unique Lite and Pro keys and the fixed fictional rates. Lite input/output rates are $10/$30 per million tokens; Pro rates are $40/$100.
3. Read `ai_usage.csv` at one row per employee prompt. Verify unique `usage_id` values, nonnegative integer tokens, and valid task and campaign relationships. Each task uses one product and one model. Each prompt's campaign must match its task.
4. Join the model rate to each prompt. Calculate input cost and output cost separately as tokens multiplied by the applicable rate, divided by 1,000,000. Retain precision when summing. The dashboard uses integer microdollars for prompt costs; the independent validator uses decimal arithmetic.
5. Aggregate prompts to `work_item_id` before joining to the cleaned work log. Sum input tokens, output tokens, input cost, output cost, prompt count, and correction count. Count each task's baseline, actual, and rework hours once. Rework is already part of actual hours and must not be added again.
6. Calculate hours saved as baseline minus actual hours. Multiply by $50 for estimated time value and subtract AI cost for net AI value. Calculate aggregate ROI from summed net value divided by summed AI cost, multiplied by 100. Calculate average prompt cost from summed AI cost divided by prompt count. Zero denominators display N/A.
7. Read `campaigns.csv` at one row per campaign. Calculate campaign result as revenue minus other campaign spending, actual hours multiplied by $50, and AI cost. Other campaign spending excludes staff time and AI fees.

The quick CSV aggregates the same focal prompt records to task grain and includes their applicable rates. The independent validator reconciles its tokens, prompt counts, calculated costs, and hours to the deeper files before presentation rounding.

## Dashboard scope and evidence

Campaign, department, product, and model selectors apply to the task analysis and retain each selected task's full prompt history. Daily spending uses `usage_date`; the date range changes only that chart. It does not allocate task hours to dates or alter task ROI.

The whole-campaign financial table accepts only a campaign filter. Department, product, model, prompt dates, and sensitivity settings do not change its revenue, actual costs, result, or original-baseline ROI. The workflow task-type selector narrows the investigation tables; the completed-data export clearly retains the scope of the four main task filters.

Source preparation and reconciliation are documented in the [data pipeline](../docs/DATA_PIPELINE.md) and [calibration notes](CALIBRATION.md). The generator uses seed `20261022`; [`scripts/validate_data.py`](../scripts/validate_data.py) independently recalculates the canonical sources in `data/` and checks the clean dashboard data. [`outputs/check_totals.json`](outputs/check_totals.json) records exact controls. Python and JavaScript tests cover reconciliation, duplicate handling, invalid joins and rates, filtering, sensitivity, prompt-date aggregation, and zero-denominator behavior.

This deliberately calibrated teaching case demonstrates an analytical method. It is not a causal experiment, a prediction, a real provider pricing comparison, an employee ranking, or evidence of realized payroll savings. Baseline estimates assume the same completed work at acceptable quality. Generation and automated checks establish internal consistency, not external validity.
