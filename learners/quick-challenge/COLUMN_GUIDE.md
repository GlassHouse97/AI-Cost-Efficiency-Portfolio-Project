# Quick Challenge column guide

The raw CSV has one row per task, plus repeated export records for you to remove. Prompt counts and tokens are already task totals. There are no missing required numbers, ambiguous date formats, or missing model prices. Department labels may contain extra spaces or inconsistent capitalization.

| Column | Plain meaning |
| --- | --- |
| `work_item_id` | Unique task identifier. Use this to remove repeated export rows. |
| `completion_date` | Task completion date in YYYY-MM-DD format. |
| `campaign` | Campaign 1 or Campaign 2. |
| `department` | Content, Creative, Marketing Operations, or Analytics after cleaning. |
| `employee` | A fictional employee; eight employees across the four departments. |
| `product` | CampaignChat, CopyStudio, DataFlow, or InsightDesk. |
| `model` | Lite or Pro. A task uses one model. |
| `task_type` | A short description, such as Write ad copy or Clean audience data. |
| `prompt_count` | Number of employee prompts for the task, including followups. |
| `input_tokens` | Integer count of tokens sent to AI across the task's prompts, including context. |
| `output_tokens` | Integer count of tokens returned across the task's prompts. |
| `input_rate_usd_per_million` | Model's fictional USD price for one million input tokens. |
| `output_rate_usd_per_million` | Model's fictional USD price for one million output tokens. |
| `baseline_hours` | Estimated human hours to complete the same work without AI. |
| `actual_hours` | Human time with AI, including preparation, prompting, review, and rework. |
| `rework_hours` | Portion of actual hours spent correcting or redoing work. |
| `issue_tag` | Primary recorded issue: None, Unclear prompt, Brief changed, or Data problem. |

## Glossary

| Term | Meaning in this exercise |
| --- | --- |
| Baseline | Estimate of how long the same completed work would take without AI. |
| Token | A unit of processed text; it does not measure time or equal one word in every case. |
| Input and output | Input is sent to AI; output is returned by AI. Their prices differ. |
| Per million | Per 1,000,000 tokens. Divide the token-price multiplication by 1,000,000. |
| Grain | What one row represents: one task in the quick CSV. |
| Duplicate | A repeated record for the same task, not a second task to count. |
| PivotTable | A spreadsheet summary that groups rows and totals fields. |
| AI cost | Token usage multiplied by the fictional model's applicable prices. |
| Time value | Hours saved multiplied by $50; an estimate of staff capacity value. |
| Net AI value | Time value after subtracting AI fees. |
| ROI | Net AI value relative to AI fees, expressed as a percentage. |
| Rework share | Rework hours as a proportion of actual hours. Rework is already included in actual hours. |
| Aggregate ratio | A ratio of summed values, not an average of individual row ratios. |
