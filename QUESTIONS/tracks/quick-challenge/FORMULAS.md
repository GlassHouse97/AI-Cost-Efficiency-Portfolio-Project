# Quick Challenge formulas and worked example

All monetary amounts are USD. Value staff time at **$50 per hour**. The prices below are fictional, fixed for the full exercise, and identical across all ChatABC products. Do not replace them with current vendor pricing.

| Model | Input USD per million tokens | Output USD per million tokens |
| --- | --- | --- |
| Lite | 10 | 30 |
| Pro | 40 | 100 |

## Add these five task columns

The formulas below use Excel table structured references and assume the table has the supplied column names. Type each formula into the first row of the new column.

| New column | Excel formula |
| --- | --- |
| `total_tokens` | `=[@input_tokens]+[@output_tokens]` |
| `ai_cost_usd` | `=([@input_tokens]*[@input_rate_usd_per_million]+[@output_tokens]*[@output_rate_usd_per_million])/1000000` |
| `hours_saved` | `=[@baseline_hours]-[@actual_hours]` |
| `time_value_usd` | `=[@hours_saved]*50` |
| `net_ai_value_usd` | `=[@time_value_usd]-[@ai_cost_usd]` |

Keep full calculation precision. Format money to two decimal places for display, but do not use `ROUND(...,2)` on each row before totaling. If exporting calculated costs, retain six decimal places. One prompt can cost less than one cent.

## Calculate these summary ratios from totals

| Metric | Calculation |
| --- | --- |
| AI ROI percentage | Sum of net AI value ÷ sum of AI cost × 100 |
| Average cost per prompt | Sum of AI cost ÷ sum of prompt count |
| Rework share percentage | Sum of rework hours ÷ sum of actual hours × 100 |

In Excel, you can calculate `net_value_total/ai_cost_total` and apply **Percentage** formatting. Do not also multiply this Excel result by 100; percentage formatting already does that visually. For example, the numeric value 4 displays as 400%. The formulas ending with × 100 above describe a percentage number rather than an Excel formatted fraction.

If the denominator is zero, display **N/A**, not zero. For an overall KPI in the table named `Tasks`, use `=IF(SUM(Tasks[ai_cost_usd])=0,"N/A",SUM(Tasks[net_ai_value_usd])/SUM(Tasks[ai_cost_usd]))` and percentage formatting. For a campaign summary, apply the same rule to that campaign's summed cells. Never average row ROI or row cost per prompt.

Negative hours saved means more human work with AI. A negative time value reduces net AI value further, so ROI can be below −100%. No campaign profit formula is needed for this track.

## Worked example from tokens to value

This independent illustration explains the arithmetic; it is not a campaign answer or a required row to find in the data.

A Lite task has **20 prompts**. Every prompt sends **10,000 input tokens** and returns **5,000 output tokens**.

1. Input cost per prompt = 10,000 × 10 ÷ 1,000,000 = **$0.10**.
2. Output cost per prompt = 5,000 × 30 ÷ 1,000,000 = **$0.15**.
3. Total per prompt = $0.10 + $0.15 = **$0.25**.
4. Total task cost = 20 × $0.25 = **$5.00**.

The quick row would hold **200,000 input tokens**, **100,000 output tokens**, and rates **10** and **30**. Its cost is (200,000 × 10 + 100,000 × 30) ÷ 1,000,000 = **$5.00**. Total tokens are **300,000**; count input and output once each.

Without AI the task would take **2 hours**; actual human time with AI is **1.5 hours**, including review and rework. Hours saved = 2 − 1.5 = **0.5 hours**. Time value = 0.5 × $50 = **$25.00**. Net AI value = $25 − $5 = **$20.00**. ROI = $20 ÷ $5 × 100 = **400%**. Count the 1.5 actual hours once, not once per prompt.
