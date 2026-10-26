# Quick Challenge — Excel Solution

**[Download the completed Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx)**

This is the worked answer to the six Quick Challenge questions. It covers **Campaigns 1 and 2 only: 120 unique tasks from September 2026**. The entire solution is in one Excel file, including the source data; no dashboard, macros, code, or external data connection is required.

Download the file and open it in Excel. GitHub does not display workbook sheets in the repository view. Start with **Solution**, then follow a number through **Summaries → Clean → Raw** to see where it came from.

## Inside the Workbook

| Worksheet | What to read |
| --- | --- |
| **Solution** | Direct answers to all six questions, compact editable charts, recommendations, and scope notes |
| **Summaries** | Campaign, department, and issue totals calculated with `SUMIFS` and `COUNTIFS`; these show the same groupings learners can create with PivotTables |
| **Clean** | The 120 unique tasks, standardized department labels, and visible formulas for token costs, hours saved, time value, and net AI value |
| **Raw** | All 122 original source records, including the two exact repeated task exports and inconsistent department formatting |

Formula summaries recalculate when the cleaned task values change. The **Clean** sheet is a documented cleaned snapshot: editing or adding a raw record does not automatically rerun deduplication. Preserve the supplied workbook and save a separate copy for experiments.

## What the Answer Establishes

| Measure | Campaign 1 | Campaign 2 | Combined quick scope |
| --- | ---: | ---: | ---: |
| AI spend | $500 | $1,400 | $1,900 |
| Hours saved / lost | +100 | −70 | +30 |
| Estimated net AI value | +$4,500 | −$4,900 | −$400 |

Net AI value is **(baseline hours − actual hours) × $50 − AI costs**. Actual hours already include rework. Campaign 2's larger bill and higher human effort outweigh Campaign 1's gains in this two-campaign exercise. The workbook also compares departments, counts reported issues, and gives two actions supported by those results.

All data, prices, and results are fictional teaching inputs. Time value estimates useful staff capacity, not realized payroll savings. The Quick Challenge has no revenue or other-spend inputs, so this workbook does not calculate campaign profit.

## Try It Before Viewing the Answer

The solved workbook is intentionally **separate from the answer-free learner ZIP**. To attempt the exercise first, use the [Quick Challenge brief](../../../QUESTIONS/TRACKS/quick-challenge/README.md) and [complete learner package](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru-quick-challenge.zip). The input workbook and this solved workbook are different files.

For the broader four-campaign investigation, open the [Portfolio Project solution](../portfolio-project/README.md). Its +$2,820 company total includes Campaigns 3 and 4 and should not be compared directly with the quick scope's −$400.

[All solutions](../../README.md) · [Project overview](../../../README.md)
