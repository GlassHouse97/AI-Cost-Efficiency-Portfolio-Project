# Case study data

These are the canonical CSV sources for the Marketing-R-Us AI cost and efficiency case study. All people, organizations, usage, prices, revenue, and results are fictional. The reporting period is September 2026. The data is released under [CC0 1.0](../DATA_LICENSE).

## Choose a dataset

| Track | Source | Grain and scope |
| --- | --- | --- |
| Quick Challenge | [mru_quick_challenge.csv](quick-challenge/mru_quick_challenge.csv) | 122 raw export rows representing 120 tasks in Campaigns 1 and 2. Prompt totals and model rates are already attached to each task. |
| Portfolio Project | [work_log.csv](portfolio-project/work_log.csv) | 242 raw export rows representing 240 tasks in four campaigns. Contains human time and workflow observations. |
| Portfolio Project | [ai_usage.csv](portfolio-project/ai_usage.csv) | 3,360 prompt records linked to tasks. |
| Portfolio Project | [model_pricing.csv](portfolio-project/model_pricing.csv) | Two fixed fictional model rate schedules in USD per million tokens. |
| Portfolio Project | [campaigns.csv](portfolio-project/campaigns.csv) | Four campaigns, with revenue and other spending recorded once per campaign. |

Read the [data dictionary](../docs/DATA_DICTIONARY.md) for keys, types, and field meanings. The [case study questions](../CASE_STUDY_QUESTIONS.md) define the investigation. Start with the [Quick Challenge brief](../learners/quick-challenge/README.md) or [Portfolio Project brief](../learners/portfolio-project/README.md) for guided exercises.

## Preparation rules

- Preserve these raw files. Work on a copy or in a separate analysis layer.
- Remove exact repeated task exports using `work_item_id`; investigate conflicting records rather than silently dropping them.
- Trim department whitespace and standardize capitalization.
- Price prompts using their model's input and output rates. Aggregate prompts to tasks before combining them with human hours.
- Count each task's hours once. `rework_hours` is already part of `actual_hours`.
- Count revenue and other campaign spending once per campaign.

The quick file is a task-level projection of the same Campaign 1 and Campaign 2 records used in the deeper track. It is not an additional population to append to the four-table dataset. The files intentionally retain duplicate exports and inconsistent department formatting for a bounded cleaning exercise; they contain no calculated answer columns.

## Reproduction and downloads

[`scripts/generate_data.py`](../scripts/generate_data.py) recreates the sources with fixed seed `20261022`. It also writes the cleaned dashboard source. The independent validator reconciles both tracks and that dashboard source. See the [data pipeline](../docs/DATA_PIPELINE.md) for the sequence and safeguards. The generator and validation output contain solution spoilers.

The [Quick Challenge ZIP](../release/mru-quick-challenge.zip?raw=true) and [Portfolio Project ZIP](../release/mru-portfolio-project.zip?raw=true) combine these exact CSVs with their learner guides and licenses. Their flat internal layout supports offline use; no second editable CSV copy is maintained under `learners/`.
