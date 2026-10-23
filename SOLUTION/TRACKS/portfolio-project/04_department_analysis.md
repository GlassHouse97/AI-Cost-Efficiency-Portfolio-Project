# Question 4: Department Spending and Value

**Which department had the highest AI spending, and which had the highest net AI value?**

## Direct Answer: Focal Campaigns 1 and 2

**Creative leads both measures:** $498.37 AI spending and +$381.63 estimated net AI value across the 120 focal tasks. It is the only department with positive combined net value in that population.

| Department | Tasks | AI spending | Hours saved | Net AI value | Aggregate AI ROI |
| --- | ---: | ---: | ---: | ---: | ---: |
| Creative | 32 | $498.37 | +17.60 | +$381.63 | 76.58% |
| Marketing Operations | 29 | $492.96 | +5.83 | −$201.46 | −40.87% |
| Analytics | 28 | $460.54 | +0.57 | −$432.04 | −93.81% |
| Content | 31 | $448.13 | +6.00 | −$148.13 | −33.06% |
| **Focal total** | **120** | **$1,900.00** | **+30.00** | **−$400.00** | **−21.05%** |

![Department comparison within the focal two-campaign dashboard population](visualizations/03_department_analysis.jpg)

*Dashboard evidence: Company overview, Campaigns 1 and 2 only, all departments, products, and models; original baseline. The department table sorts by AI spend and displays the same four department values shown above.*

Positive hours saved do not necessarily cover token costs. Content saves six hours, worth $300, but spends $448.13 on AI and therefore has negative net value. Creative's 17.60 hours are worth $880, enough to cover its $498.37 bill.

## Deeper Extension: All Four Campaigns

| Department | Tasks | AI spending | Hours saved | Net AI value |
| --- | ---: | ---: | ---: | ---: |
| Creative | 63 | $820.26 | +39.29 | +$1,144.24 |
| Marketing Operations | 61 | $820.12 | +30.34 | +$696.88 |
| Analytics | 57 | $788.91 | +24.38 | +$430.09 |
| Content | 59 | $750.71 | +25.99 | +$548.79 |
| **Company total** | **240** | **$3,180.00** | **+120.00** | **+$2,820.00** |

Creative also leads the all-company comparison. Its spending lead over Marketing Operations is only **$0.14 when the exact difference is rounded**, so that ranking has little operational significance. Its net-value lead is more substantial. All four departments are positive in the full-company scope, unlike the focal scope.

Department totals are not employee scores or causal measures of department effectiveness. Task type, campaign mix, volume, model use, and baseline estimates can differ. Each department has positive net value within Campaign 1 and negative net value within Campaign 2, indicating that campaign context warrants investigation before imposing broad department-level rules.

## Calculation and Validation

The [department evidence](outputs/department_summary.csv) includes rows for `focal_campaigns_1_2`, `all_four_campaigns`, and each individual campaign. Filter that scope field before summing; these are overlapping breakdowns, not additive populations.

Department labels are trimmed and standardized before grouping. Each clean task is assigned to one department; token costs are aggregated from all its prompts and task hours are counted once. Rebuild with `python TECHNICAL/scripts/analyze_case_study.py`. The four focal rows reconcile to −$400 net value, and the four company rows reconcile to +$2,820. Independently rounded rows may differ from a displayed total by one cent.

**Business implication:** compare spending with value and task context. Neither a high AI bill nor a low AI bill alone identifies the best workflow.

[Next: Workflow investigation](05_workflow_investigation.md) · [Solution index](README.md)
