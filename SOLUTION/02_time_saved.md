# Question 2: Human Effort

**How many hours did each campaign save or lose against its no AI estimate?**

## Direct Answer

Campaign 1 saves **100 hours** against its 240-hour baseline. Campaign 2 takes **70 more hours** than its 200-hour baseline. Together, the focal campaigns save 30 hours, worth an estimated $1,500 before their $1,900 AI bill.

| Scope | Baseline hours | Actual hours | Hours saved / lost | Time value at $50/hour |
| --- | ---: | ---: | ---: | ---: |
| Campaign 1 | 240 | 140 | +100 | +$5,000 |
| Campaign 2 | 200 | 270 | −70 | −$3,500 |
| **Focal Campaigns 1+2** | **440** | **410** | **+30** | **+$1,500** |
| Campaign 3 — deeper track | 220 | 172 | +48 | +$2,400 |
| Campaign 4 — deeper track | 260 | 218 | +42 | +$2,100 |
| **All four campaigns** | **920** | **800** | **+120** | **+$6,000** |

![Focal campaign overview comparing estimated and actual human effort](visualizations/03_department_analysis.jpg)

*Dashboard evidence: Campaigns 1 and 2, all departments, products, and models; original baseline. The Human Effort chart shows Campaign 1 falling from 240 estimated to 140 actual hours and Campaign 2 rising from 200 estimated to 270 actual hours.*

Actual hours already include preparation, prompting, setup, checking, and corrections. Rework is a subset and must not be added again. The 170-hour difference in savings between Campaigns 1 and 2 is worth $8,500, explaining most of their $9,400 net-AI-value gap.

## Deeper Analysis: Baseline Sensitivity

Only the estimated no-AI baseline changes. Actual effort and token charges remain fixed.

| Campaign | Net value: baseline −20% | Original net value | Net value: baseline +20% |
| --- | ---: | ---: | ---: |
| Campaign 1 | +$2,100 | +$4,500 | +$6,900 |
| Campaign 2 | −$6,900 | −$4,900 | −$2,900 |
| Campaign 3 | −$340 | +$1,860 | +$4,060 |
| Campaign 4 | −$1,240 | +$1,360 | +$3,960 |

Campaign 1 remains positive and Campaign 2 remains negative at both endpoints. Campaigns 3 and 4 change sign when estimated baseline hours are 20% lower. Their initial positive result therefore warrants more scrutiny of the no-AI benchmark.

![Dashboard baseline sensitivity with a negative twenty percent scenario](visualizations/05_sensitivity.jpg)

*Dashboard evidence: Campaign comparison, all four campaigns, all departments, products, and models; baseline scenario −20%. Original and +20% endpoint columns are also visible. This control changes only the sensitivity table.*

Whole-campaign financial results use actual costs and do not change with the estimated baseline. This sensitivity range is an assumption test, not a probability interval or evidence of causal savings.

## Calculation and Validation

`Hours saved = baseline hours − actual hours`. `Scenario net AI value = (baseline hours × scenario factor − actual hours) × $50 − AI cost`, where the factors are 0.8, 1.0, and 1.2.

The [campaign evidence](outputs/campaign_summary.csv), [scope totals](outputs/scope_summary.csv), and [sensitivity table](outputs/sensitivity_summary.csv) are reproducible with `python scripts/analyze_case_study.py`. Each of the 240 unique task records contributes its hours once after prompt aggregation. The raw repeated task exports do not contribute again.

**Business implication:** verify no-AI estimates against comparable completed work before treating measured time value as a dependable benefit. Preserve successful tasks while testing workflow changes where actual effort is higher.

[Next: Net value and campaign results](03_value_and_campaign_results.md) · [Solution index](README.md)
