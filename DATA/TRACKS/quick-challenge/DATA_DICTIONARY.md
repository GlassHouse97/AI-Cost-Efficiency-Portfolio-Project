# Quick Challenge Data Dictionary

This document defines the original data supplied for the Marketing R Us (MRU) Quick Challenge. The **Raw** worksheet in `mru-quick-challenge.xlsx` and `mru_quick_challenge.csv` contain the same source records. These definitions are also included in the workbook's **Data Dictionary** worksheet.

Each source record describes a completed task for Campaign 1 or Campaign 2, with its AI prompt and token usage already summarized for that task. Organizations, employees, products, models, and prices are fictional. The reporting month is September 2026. Model prices are fixed assumptions for this exercise.

| Worksheet | Column | Type and units | Meaning |
| --- | --- | --- | --- |
| Raw | `work_item_id` | Text identifier | Identifier assigned to the completed task. The same task has the same identifier in the Portfolio Project work log. |
| Raw | `completion_date` | Date, YYYY-MM-DD | Date the task was completed. This is the completion date rather than the date of an individual AI prompt. |
| Raw | `campaign` | Text | Campaign associated with the task: Campaign 1 or Campaign 2. |
| Raw | `department` | Text | Department responsible for the task. The business departments are Content, Creative, Marketing Operations, and Analytics. |
| Raw | `employee` | Text | Fictional employee responsible for the task. |
| Raw | `product` | Text | AI application used for the task: CampaignChat, CopyStudio, DataFlow, or InsightDesk. Each task uses one product. |
| Raw | `model` | Text | Fictional AI model used for the task: Lite or Pro. Each task uses one model. |
| Raw | `task_type` | Text | Description of the work performed, such as Write ad copy or Draft email sequence. |
| Raw | `prompt_count` | Integer, prompts | Number of employee interactions with AI for this task, including the first attempt, followups, and corrections. |
| Raw | `input_tokens` | Integer, tokens | Total text units sent to AI across the task's prompts, including instructions and supporting context. |
| Raw | `output_tokens` | Integer, tokens | Total text units returned by AI across the task's prompts. |
| Raw | `input_rate_usd_per_million` | Decimal, USD per 1,000,000 input tokens | Price for the task's model to process one million input tokens. |
| Raw | `output_rate_usd_per_million` | Decimal, USD per 1,000,000 output tokens | Price for the task's model to produce one million output tokens. |
| Raw | `baseline_hours` | Decimal, hours | Estimated human effort to complete the same task at acceptable quality without AI. |
| Raw | `actual_hours` | Decimal, hours | Total human effort while using AI, including preparation, prompting, review, and rework. |
| Raw | `rework_hours` | Decimal, hours | Portion of actual_hours spent correcting or redoing work. These hours are already included in actual_hours. |
| Raw | `issue_tag` | Text category | Primary recorded issue: None, Unclear prompt, Brief changed, or Data problem. None means no issue was recorded. |
