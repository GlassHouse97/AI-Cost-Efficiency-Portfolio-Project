# Quick Challenge Excel Solution

**[Download the completed Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx)**

This is the completed analysis for Marketing R Us (MRU), a fictional marketing company evaluating AI use across two client campaigns. The workbook contains the original data, calculations, answers to all six questions, and two charts. Everything needed to read the solution is in one Excel file.

Open the **Solution** sheet first. To investigate a result, find its grouped calculation in **Summaries**, inspect the task formulas in **Clean**, and compare the original records in **Raw**.

## Answers to the Questions

### 1. What tokens, costs, and prompts did each campaign use?

| Measure | Campaign 1 | Campaign 2 | Total |
| --- | ---: | ---: | ---: |
| Input tokens | 22,000,000 | 32,000,000 | 54,000,000 |
| Output tokens | 5,000,000 | 10,000,000 | 15,000,000 |
| Prompts | 600 | 1,200 | 1,800 |
| Input cost | $280.00 | $680.00 | $960.00 |
| Output cost | $220.00 | $720.00 | $940.00 |
| Total AI cost | $500.00 | $1,400.00 | $1,900.00 |

Campaign 2 generated twice as many prompts and cost 2.8 times as much as Campaign 1. Spending depends on the input and output token volumes and the model rates attached to each task. Prompt count alone does not determine cost.

### 2. How many hours did each campaign save or lose?

| Measure | Campaign 1 | Campaign 2 | Total |
| --- | ---: | ---: | ---: |
| Estimated hours without AI | 240 | 200 | 440 |
| Actual hours with AI | 140 | 270 | 410 |
| Result | 100 hours saved | 70 additional hours | 30 hours saved |

Campaign 1 required less human time than its estimate. Campaign 2 required more. The combined result still shows a time saving, but that alone does not establish whether AI paid for itself.

### 3. Was estimated net AI value positive or negative?

| Measure | Campaign 1 | Campaign 2 | Total |
| --- | ---: | ---: | ---: |
| Estimated time value at $50 per hour | $5,000.00 | ($3,500.00) | $1,500.00 |
| AI cost | $500.00 | $1,400.00 | $1,900.00 |
| Estimated net AI value | $4,500.00 | ($4,900.00) | ($400.00) |

Parentheses indicate negative values. Campaign 1's estimated benefit did not fully offset Campaign 2's loss. Across both campaigns, the $1,500 estimated value of staff time saved fell $400 short of AI fees.

### 4. Which department had the highest spending and net value?

| Department | AI cost | Estimated net AI value |
| --- | ---: | ---: |
| Analytics | $460.54 | ($432.04) |
| Content | $448.13 | ($148.13) |
| Creative | $498.37 | $381.63 |
| Marketing Operations | $492.96 | ($201.46) |

Creative had both the highest AI spending and the highest net AI value. It saved 17.60 hours across the two campaigns. Its result illustrates why the largest bill is not necessarily the weakest investment.

### 5. Which campaign had more rework, and which issues were most common?

Campaign 2 recorded **87.82 hours of rework**, compared with **10.74 hours** in Campaign 1. Rework accounted for 32.5% and 7.7% of actual hours, respectively.

| Primary recorded issue | Campaign 1 | Campaign 2 | Total tasks |
| --- | ---: | ---: | ---: |
| Brief changed | 10 | 27 | 37 |
| Data problem | 9 | 13 | 22 |
| Unclear prompt | 9 | 10 | 19 |
| None | 32 | 10 | 42 |

Changed briefs were the most common recorded problem. Each task has one primary issue tag. The 42 records marked None have no recorded issue and are not a problem category. These counts identify areas to investigate; they do not establish that a particular issue caused every hour of rework.

### 6. What should MRU do next?

1. **Continue the approach used in Campaign 1, with regular review.** It saved 100 hours and generated $4,500 in estimated net value after AI fees. Compare future work against the same time and quality measures before expanding the approach.
2. **Review Campaign 2 before extending its AI use.** It required 70 additional hours and produced a $4,900 estimated loss. Start with brief approval and change control: changed briefs affected 27 of its 60 tasks. A smaller followup trial should track rework, total human effort, and AI cost to determine whether those changes improve the result.

## How the Workbook Was Built

### Prepare the source records

The original export contains 122 rows for September 2026. Each row records one completed task, with prompts and tokens already totaled for that task. The Excel input and CSV contain the same records, so only one source format is needed.

The Raw sheet preserves the export. The Clean sheet retains one record for each `work_item_id`. Tasks **W0018** and **W0087** each appear twice with identical values, so removing the repeated copies leaves **120 unique tasks**. Matching campaign, employee, or task descriptions alone would not justify deleting a record.

Department labels contain inconsistent spaces and capitalization. Standardizing them with `=PROPER(TRIM([@department]))` produces Analytics, Content, Creative, and Marketing Operations. This prevents the same department from appearing as several groups in the summaries. The cleaned labels are stored as values in the finished workbook.

The date field records task completion, not the provider's billing date. Tokens, prompts, rates, and hours are numeric. `baseline_hours` estimates the human effort needed without AI; `actual_hours` includes preparation, prompting, review, and corrections. `rework_hours` is part of actual hours and must not be added to it again.

### Calculation method

The analysis values staff time at **$50 per hour**, stored in **Clean!B3**. Input and output rates are supplied per million tokens on each source row. These are fictional exercise prices: Lite uses $10 for input and $30 for output; Pro uses $40 and $100. They are fixed across the exercise.

The Clean sheet adds seven calculation columns. The formulas below are the actual formulas in its first task row, row 7, and are filled down through row 126.

| Column | Formula in row 7 | Purpose |
| --- | --- | --- |
| R: `total_tokens` | `=J7+K7` | Combines input and output volume for Question 1. |
| S: `input_cost_usd` | `=J7*L7/1000000` | Prices input tokens at the task's input rate for Question 1. |
| T: `output_cost_usd` | `=K7*M7/1000000` | Prices output tokens separately because their rate differs. |
| U: `ai_cost_usd` | `=SUM(S7:T7)` | Establishes the total AI fee used in Questions 1, 3, and 4. |
| V: `hours_saved` | `=N7-O7` | Compares estimated and actual effort for Question 2. A negative result means additional work. |
| W: `time_value_usd` | `=V7*$B$3` | Expresses the time difference in dollars so it can be compared with AI fees. |
| X: `net_ai_value_usd` | `=W7-U7` | Measures estimated value after AI fees for Questions 3 and 4. |

For a worked example, task **W0001** has 258,261 input tokens and 113,210 output tokens at Pro rates. Its input cost is $10.33044 and its output cost is $11.321, giving a total of $21.65144. Actual effort was 4.75 hours against a 4.57 hour baseline, so the additional 0.18 hours have an estimated cost of $9. Its net AI value is therefore negative $30.65144, displayed as ($30.65).

The source already contains task totals. Multiplying tokens or actual hours by prompt count would count the same activity again. Calculations retain full precision; currency formatting supplies the displayed rounding.

### Build and check the summaries

The Summaries sheet uses `SUMIFS` to group numeric measures by campaign or department and `COUNTIFS` to count tasks by campaign and issue. The Solution sheet links to those results. A PivotTable using sums for numeric measures and a task count for issues can reproduce the same comparisons.

Ratios use the grouped totals. Campaign AI ROI is total net AI value divided by total AI cost. Rework share is total rework hours divided by total actual hours. Average cost per prompt, if needed, is total AI cost divided by total prompts. Averaging individual task ratios would give each task equal weight regardless of its size. Use percentage formatting for ROI and rework share, and display N/A when the denominator is zero.

The campaign and department summaries both reconcile to 120 tasks, $1,900 of AI cost, 30 hours saved, and negative $400 of net AI value. Issue counts also total 120. The two charts use the same summary values as the written answers.

The Clean sheet is a saved, cleaned snapshot. Changes to its existing task inputs recalculate the formulas and summaries. Changes to Raw do not automatically repeat the cleaning process. The written recommendations should also be reviewed when inputs change.

## What the Results Mean

All records, employees, prices, and outcomes are fictional teaching inputs. The $50 hourly assumption estimates the value of staff capacity. It does not establish that payroll spending decreased. Baseline hours are estimates, and the comparison does not prove that AI caused the observed differences.

This solution covers Campaigns 1 and 2 only. Revenue and other campaign expenses are not supplied, so these results measure estimated AI value rather than campaign profit.

[Return to the Quick Challenge questions](../../../QUESTIONS/TRACKS/quick-challenge/README.md)