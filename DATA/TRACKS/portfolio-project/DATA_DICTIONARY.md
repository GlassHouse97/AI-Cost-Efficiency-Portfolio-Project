# Portfolio Project Data Dictionary

This document defines the original data supplied for the Marketing R Us (MRU) Portfolio Project. The four source worksheets in `mru-portfolio-project.xlsx` contain the same records as their corresponding CSV files. These definitions are also included in the workbook's **Data Dictionary** worksheet.

The **campaigns** table describes each complete campaign. The **work_log** records completed tasks, and **ai_usage** records individual employee prompts associated with those tasks. The **model_pricing** table supplies the prices for each model. Organizations, employees, products, models, and prices are fictional. The reporting month is September 2026, and model prices remain fixed throughout that month.

A campaign can contain several tasks, and a task can contain several prompts. Campaign identifiers connect the campaign, task, and prompt records. Task identifiers connect prompt records to their tasks, and model names connect prompt records to model prices.

| Worksheet | Column | Type and units | Meaning |
| --- | --- | --- | --- |
| campaigns | `campaign_id` | Text identifier | Identifier assigned to the campaign. The same identifier appears in work_log and ai_usage. |
| campaigns | `campaign_name` | Text | Display name of the campaign: Campaign 1, Campaign 2, Campaign 3, or Campaign 4. |
| campaigns | `campaign_revenue_usd` | Decimal, USD | Revenue for the complete campaign, rather than for an individual task, employee, or prompt. |
| campaigns | `other_campaign_cost_usd` | Decimal, USD | Spending for the complete campaign excluding human labor time and AI fees. |
| work_log | `work_item_id` | Text identifier | Identifier assigned to the completed task. The same identifier appears on its prompt records in ai_usage. |
| work_log | `completion_date` | Date, YYYY-MM-DD | Date the task was completed. It is distinct from usage_date, which records when an individual prompt occurred. |
| work_log | `campaign_id` | Text identifier | Campaign associated with the task, identified by campaign_id in the campaigns table. |
| work_log | `department` | Text | Department responsible for the task. The business departments are Content, Creative, Marketing Operations, and Analytics. |
| work_log | `employee` | Text | Fictional employee responsible for the task. |
| work_log | `task_type` | Text | Description of the work performed, such as Write ad copy or Draft email sequence. |
| work_log | `baseline_hours` | Decimal, hours | Estimated human effort to complete the same task at acceptable quality without AI. |
| work_log | `actual_hours` | Decimal, hours | Total human effort while using AI, including preparation, prompting, review, and rework. |
| work_log | `rework_hours` | Decimal, hours | Portion of actual_hours spent correcting or redoing work. These hours are already included in actual_hours. |
| work_log | `issue_tag` | Text category | Primary recorded issue: None, Unclear prompt, Brief changed, or Data problem. None means no issue was recorded. |
| work_log | `brief_changed` | Text flag, Yes or No | Recorded observation of whether the task's brief changed during the work. |
| work_log | `prompt_template_used` | Text flag, Yes or No | Recorded observation of whether the employee used a prompt template for the task. |
| ai_usage | `usage_id` | Text identifier | Unique identifier for one employee prompt. Followups and corrections are separate prompt records. |
| ai_usage | `usage_date` | Date, YYYY-MM-DD | Date the prompt occurred. It falls on or before the linked task's completion_date. |
| ai_usage | `work_item_id` | Text identifier | Task associated with the prompt, identified by work_item_id in work_log. |
| ai_usage | `campaign_id` | Text identifier | Campaign associated with the prompt. It is the same campaign assigned to the linked task and identified in campaigns. |
| ai_usage | `product` | Text | AI application used for the prompt: CampaignChat, CopyStudio, DataFlow, or InsightDesk. Each task uses one product. |
| ai_usage | `model` | Text | Fictional AI model used for the prompt: Lite or Pro. The name corresponds to model in model_pricing. Each task uses one model. |
| ai_usage | `input_tokens` | Integer, tokens | Text units sent to AI in this prompt, including instructions and supporting context. |
| ai_usage | `output_tokens` | Integer, tokens | Text units returned by AI for this prompt. |
| ai_usage | `prompt_reason` | Text category | Purpose recorded for the interaction: First attempt, Followup, or Correction. |
| model_pricing | `model` | Text identifier | Fictional model whose prices appear on this row: Lite or Pro. The same name appears in ai_usage. |
| model_pricing | `input_rate_usd_per_million` | Decimal, USD per 1,000,000 input tokens | Price for the model to process one million input tokens. The same price applies across all products. |
| model_pricing | `output_rate_usd_per_million` | Decimal, USD per 1,000,000 output tokens | Price for the model to produce one million output tokens. The same price applies across all products. |

A prompt is one employee interaction with AI. The source data contains no prompt text, personal information from real employees, or automated API calls.
