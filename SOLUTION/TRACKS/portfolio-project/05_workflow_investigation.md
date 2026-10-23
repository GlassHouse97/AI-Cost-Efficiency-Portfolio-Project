# Question 5: Rework and Recorded Issues

**Which campaign had more rework, and which recorded issues appeared most often?**

## Direct Answer

**Campaign 2 has far more rework:** 87.82 hours versus 10.74 in Campaign 1. Rework accounts for 32.53% of Campaign 2's actual hours, compared with 7.67% in Campaign 1. **Brief changed** is the most common reported problem in each focal campaign and across the focal population; `None` is a separate no-issue category.

| Observation | Campaign 1 | Campaign 2 |
| --- | ---: | ---: |
| Tasks | 60 | 60 |
| Rework hours | 10.74 | 87.82 |
| Rework / actual hours | 7.67% | 32.53% |
| Correction prompts | 68 | 482 |
| Corrections / all prompts | 11.33% | 40.17% |
| Changed-brief tasks | 10 (16.67%) | 27 (45.00%) |
| Tasks using a prompt template | 53 (88.33%) | 19 (31.67%) |

## Which Issues Appear Most Often?

| Recorded primary issue | Campaign 1 tasks | Campaign 2 tasks | Focal total | Campaign 2 rework hours |
| --- | ---: | ---: | ---: | ---: |
| Brief changed | 10 | 27 | 37 | 41.38 |
| Data problem | 9 | 13 | 22 | 23.69 |
| Unclear prompt | 9 | 10 | 19 | 16.56 |
| None | 32 | 10 | 42 | 6.19 |
| **Total** | **60** | **60** | **120** | **87.82** |

Among all focal task records, `None` is the largest category at 42 tasks. Among the 78 tasks with a recorded problem, **37 have changed briefs**. Campaign 2's changed-brief group contributes 41.38 rework hours and 218 corrections, making it a useful place to investigate requirements and handoffs. Those are observed group totals, not hours proven to be caused by brief changes.

![Campaign 2 model, product, recorded-issue, and workflow observations](visualizations/04_workflow_investigation.jpg)

*Dashboard evidence: Workflow investigation, Campaign 2 only, all departments, products, models, and task types. The issue table shows 27 changed-brief tasks and 41.38 rework hours; its four groups sum to 60 tasks, 87.82 rework hours, and 482 correction prompts.*

For context, the all-four-campaign population has 132.04 rework hours. Campaign 3 contributes 14.94 hours and Campaign 4 contributes 18.54. Across all four, reported issues are 57 changed briefs, 40 unclear prompts, and 38 data problems; 105 tasks are marked `None`.

## Deeper Analysis: Compare Similar Work

The broad template-use gap is a hypothesis to test, not proof that templates create better outcomes. Narrowing the dashboard to **Campaign 2 → Draft email sequence** holds campaign and task type constant, but only five tasks remain:

| Within Campaign 2, Draft email sequence | Tasks | Rework / actual hours | Corrections / task |
| --- | ---: | ---: | ---: |
| Template used: Yes | 3 | 25.74% | 5.67 |
| Template used: No | 2 | 30.43% | 13.00 |
| Brief changed: Yes | 3 | 31.02% | 11.00 |
| Brief changed: No | 2 | 20.90% | 5.00 |

The template-using group has fewer corrections per task and a lower rework share; the changed-brief group has more of both. The template and brief groups overlap and must be compared within their own pair, not added together. With only two or three tasks per group, different task difficulty, model choices, and selection effects can still explain the pattern. This small comparison guides a trial; it does not estimate an intervention effect.

Reproduce this specific table by filtering [workflow_summary.csv](outputs/workflow_summary.csv) to `campaign_id=C002` and `task_type=Draft email sequence`, then dividing correction prompts by tasks and rework hours by actual hours. The dashboard's task-type selector reproduces the same comparison; the screenshot above deliberately retains all task types for the overall issue finding.

## Calculation and Validation

Sources: [campaign_summary.csv](outputs/campaign_summary.csv), [issue_summary.csv](outputs/issue_summary.csv), and [workflow_summary.csv](outputs/workflow_summary.csv). Issue tags identify one primary category per task, while correction counts come from prompt reasons. A task marked `None` can still contain correction prompts and some rework; these fields measure different observations.

Actual hours include rework. Counting it again would exaggerate human cost. The issue table's tasks, rework, and prompt counts reconcile to campaign totals after duplicate task records are removed.

**Business implication:** test clearer briefs, templates, and a stop-and-review point for repeated corrections, measuring total human effort and accepted quality rather than simply reducing prompt counts.

[Next: Strategic recommendations](06_strategic_recommendations.md) · [Solution index](README.md)
