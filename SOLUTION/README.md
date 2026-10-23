# Complete Case Study Solution

This folder collects the finished business analysis: the executive summary, six question-level answers, exact result tables, methodology, and screenshots captured from the working dashboard. **It contains learner answers.**

## Start Here

- **Explore:** [Live AI Cost Efficiency dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app).
- **Read:** [Executive summary](EXECUTIVE_SUMMARY.md) for the business problem, findings, and recommendations.
- **Review the scope:** [Case-study questions and guidelines](../QUESTIONS/README.md).
- **Try it yourself first:** [Quick Challenge](../QUESTIONS/tracks/quick-challenge/README.md) or [Portfolio Project](../QUESTIONS/tracks/portfolio-project/README.md).

## Detailed Answers

| Question | Main answer | Deeper extension |
| --- | --- | --- |
| 1. What tokens, costs, and prompts did each campaign use? | [Usage and costs](01_usage_and_costs.md) | Fixed-price model mix, product mix, cost per prompt |
| 2. How many hours did each campaign save or lose? | [Human effort](02_time_saved.md) | ±20% baseline sensitivity across all four campaigns |
| 3. Was net AI value positive or negative? | [Net AI value](03_value_and_campaign_results.md) | ROI and whole-campaign financial results |
| 4. Which department spent most and created most value? | [Department analysis](04_department_analysis.md) | Focal versus all-company comparison |
| 5. Which campaign had more rework and which issues were most common? | [Workflow investigation](05_workflow_investigation.md) | Corrections, changed briefs, templates, and comparable task types |
| 6. What should MRU keep, change, or reduce? | [Strategic recommendations](06_strategic_recommendations.md) | Two actions, measurement plan, and limitations |

The main six questions use Campaigns 1 and 2, matching the 120-task Quick Challenge. Clearly labeled deeper sections extend the analysis to all four campaigns and 240 tasks. The [scope summary](outputs/scope_summary.csv) reconciles the focal −$400 net AI value with the all-company +$2,820; those are different populations.

## Supporting Evidence

- [outputs/](outputs/) contains eight reproducible CSV tables, plus [exact validation controls](outputs/check_totals.json).
- [visualizations/](visualizations/) contains actual dashboard screenshots; each written caption states the filter scope.
- [ANALYSIS.md](ANALYSIS.md) describes calculation grain, filter behavior, and the complete methodology.
- [CALIBRATION.md](CALIBRATION.md) discloses the synthetic scenario design and exact control totals.
- [../TECHNICAL/scripts/analyze_case_study.py](../TECHNICAL/scripts/analyze_case_study.py) independently prices and summarizes the published CSVs with decimal arithmetic.
- [../TECHNICAL/dashboard/metrics.mjs](../TECHNICAL/dashboard/metrics.mjs) implements the dashboard calculations using integer microdollar charges.

## Regenerate the Evidence

From the repository root, with Python 3.10+:

```sh
python TECHNICAL/scripts/validate_data.py --write-checks
python TECHNICAL/scripts/analyze_case_study.py
```

The analysis command writes `scope_summary.csv`, `campaign_summary.csv`, `department_summary.csv`, `issue_summary.csv`, `model_summary.csv`, `product_summary.csv`, `workflow_summary.csv`, and `sensitivity_summary.csv`. Monetary values retain six decimal places in these tables; written analysis rounds only presentation values. Screenshots are captured from the running dashboard and are not generated charts or mockups.

All data are fictional, all prices are supplied teaching assumptions, and staff time value does not imply cash savings. The finished deliverable is the interactive dashboard and this documented case study.
