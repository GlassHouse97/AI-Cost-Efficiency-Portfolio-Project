# Portfolio Project column guide

## work_log.csv

One completed task after removing repeated export records. There should be 240 unique tasks across four campaigns.

| Column | Plain meaning |
| --- | --- |
| `work_item_id` | Unique task key used to connect prompt aggregates. |
| `completion_date` | Date the task was completed, YYYY-MM-DD. |
| `campaign_id` | Campaign key linking to campaigns.csv. |
| `department` | Task's department; trim and standardize labels. |
| `employee` | Fictional employee responsible for this task. |
| `task_type` | Short task label for comparing similar work. |
| `baseline_hours` | Estimated human hours for the same completed work without AI. |
| `actual_hours` | Total human time with AI, including preparation, prompting, review, and rework. |
| `rework_hours` | Part of actual hours spent correcting or redoing work. |
| `issue_tag` | Primary issue: None, Unclear prompt, Brief changed, or Data problem. |
| `brief_changed` | Yes or No observation that the brief changed. |
| `prompt_template_used` | Yes or No observation that a prompt template was used. |

## ai_usage.csv

One employee prompt. Multiple prompts can belong to the same task. Followups and corrections count as prompts. The file contains no real prompt text and no automated calls.

| Column | Plain meaning |
| --- | --- |
| `usage_id` | Unique prompt record key. |
| `usage_date` | Date the prompt was used, YYYY-MM-DD; use this for daily spending. |
| `work_item_id` | Task that this prompt belongs to. |
| `campaign_id` | Must match that task's campaign key. |
| `product` | CampaignChat, CopyStudio, DataFlow, or InsightDesk. Each task uses one product. |
| `model` | Lite or Pro. Each task uses one model. |
| `input_tokens` | Nonnegative integer count of tokens sent to AI, including context. |
| `output_tokens` | Nonnegative integer count of returned tokens. |
| `prompt_reason` | First attempt, Followup, or Correction. |

## model_pricing.csv

One unique row per model, exactly two rows. Prices are fictional USD per 1,000,000 tokens, fixed for the whole exercise and shared by every product.

| Column | Plain meaning |
| --- | --- |
| `model` | Unique model key: Lite or Pro. |
| `input_rate_usd_per_million` | USD price for one million input tokens. Lite 10; Pro 40. |
| `output_rate_usd_per_million` | USD price for one million output tokens. Lite 30; Pro 100. |

## campaigns.csv

One campaign. Do not sum these financial amounts from a prompt-level or task-level join.

| Column | Plain meaning |
| --- | --- |
| `campaign_id` | Unique key C001, C002, C003, or C004. |
| `campaign_name` | Campaign 1, Campaign 2, Campaign 3, or Campaign 4. |
| `campaign_revenue_usd` | Complete campaign revenue in USD. |
| `other_campaign_cost_usd` | Complete campaign spending excluding human labor time and AI fees. |

## Glossary

| Term | Meaning in this exercise |
| --- | --- |
| Grain | What one row represents. State it before joining or summing tables. |
| Key | A field used to identify a row or connect related records. |
| Aggregate | Summarize multiple rows at a chosen grain, such as one row per task. |
| One-to-many | One task can have many prompt rows; joining hours directly repeats the hours. |
| Input and output tokens | Text units sent to and returned by AI; count each once. |
| Baseline | Estimate of effort without AI for the same completed work and acceptable quality. |
| Net AI value | Estimated value of hours saved minus AI token fees. |
| Campaign result | Revenue minus other spending, actual human time at $50/hour, and AI fees. |
| Sensitivity analysis | Recalculate an estimate after changing an assumption to see whether the conclusion changes. |
| Whole campaign | Complete campaign scope, regardless of department, product, model, or prompt-date filters. |
| Association | An observed relationship that does not, on its own, prove cause and effect. |
