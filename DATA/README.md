# Case Study Data

Download a complete exercise package to get **everything needed to begin: an Excel workbook, all matching CSV files, and the full instructions**. All organizations, people, prices, usage, and business results are fictional. The reporting month is September 2026.

Both tracks are grouped under **[TRACKS](TRACKS/README.md)**. Each track folder keeps its source workbook, CSV files, and complete ZIP together. The [worked solutions](../SOLUTION/TRACKS/README.md) are stored separately.

## Complete Downloads

| Track | Included data | Download | Instructions on GitHub |
| --- | --- | --- | --- |
| **Quick Challenge** | One Excel workbook with one raw data sheet, plus the matching task CSV | **[Quick Challenge ZIP](TRACKS/quick-challenge/mru-quick-challenge.zip?raw=true)** | [Quick brief](../QUESTIONS/TRACKS/quick-challenge/README.md) |
| **Portfolio Project** | One Excel workbook with four raw data sheets, plus all four matching CSVs | **[Portfolio Project ZIP](TRACKS/portfolio-project/mru-portfolio-project.zip?raw=true)** | [Deeper brief](../QUESTIONS/TRACKS/portfolio-project/README.md) |

Each ZIP also contains **START_HERE.html**, the README, column guide, formulas, submission checklist, and licenses. Unzip it, open **START_HERE.html**, and choose your data format. The guide works offline; no account, API key, or connection to the hosted dashboard is required.

## Choose Excel or CSV

**Use one format for your analysis.** The workbook sheets and CSVs contain the same raw records, including the intentional cleaning issues. Do not append the workbook data to the CSV data or import both versions of a table: that would double-count the same inputs.

- **Excel:** open the workbook, save a working copy, and begin with the supplied raw sheets. There are no completed cost formulas, campaign answers, PivotTables, or charts.
- **CSV:** import the files into Excel, a BI tool, SQL, or code. Keep the originals unchanged and calculate the same metrics in your chosen tool.

The Quick Challenge and Portfolio Project also overlap: the quick file summarizes the same Campaign 1 and Campaign 2 tasks found in the deeper dataset. They are alternative exercises, not additional datasets to combine.

## Individual Files

### Quick Challenge

**[Download Excel workbook](TRACKS/quick-challenge/mru-quick-challenge.xlsx?raw=true)** · **[Download CSV](TRACKS/quick-challenge/mru_quick_challenge.csv?raw=true)**

One row represents one completed task, with its prompts, tokens, and applicable model rates already attached. The raw file contains **122 rows representing 120 tasks** across Campaigns 1 and 2. No joins or programming are required.

### Portfolio Project

**[Download Excel workbook](TRACKS/portfolio-project/mru-portfolio-project.xlsx?raw=true)** — four sheets corresponding to the four CSV files below.

| CSV file / workbook sheet | One row represents | Raw rows | Purpose |
| --- | --- | ---: | --- |
| [work_log.csv](TRACKS/portfolio-project/work_log.csv) / `work_log` | One completed task | 242 | Baseline, actual, and rework hours; workflow observations; 240 unique tasks after cleaning |
| [ai_usage.csv](TRACKS/portfolio-project/ai_usage.csv) / `ai_usage` | One prompt | 3,360 | Tokens, model, product, prompt reason, and usage date |
| [model_pricing.csv](TRACKS/portfolio-project/model_pricing.csv) / `model_pricing` | One model | 2 | Fixed fictional input/output prices in USD per million tokens |
| [campaigns.csv](TRACKS/portfolio-project/campaigns.csv) / `campaigns` | One campaign | 4 | Revenue and other spending, counted once per campaign |

Read the [Quick Challenge column guide](../QUESTIONS/TRACKS/quick-challenge/COLUMN_GUIDE.md) or [Portfolio Project column guide](../QUESTIONS/TRACKS/portfolio-project/COLUMN_GUIDE.md) for field meanings. The [case-study questions](../QUESTIONS/README.md) describe the investigation.

## Preparation Rules

1. Preserve the raw Excel workbook or CSV files; work on a copy or in a separate analysis layer.
2. Remove exact repeated task exports using `work_item_id`. Investigate conflicting records instead of silently dropping them.
3. Trim department whitespace and standardize capitalization.
4. For the deeper project, price prompts using each model's input and output rates, then aggregate prompts to tasks before combining them with human hours.
5. Count each task's hours once. `rework_hours` is already part of `actual_hours`.
6. Count revenue and other campaign spending once per campaign.

Both formats intentionally retain repeated task exports and inconsistent department formatting for a bounded cleaning exercise. They contain raw source fields, not calculated answer columns. Fixed fictional prices keep the focus on analysis rather than current vendor billing.

## Reproduction and License

For dataset generation, workbook validation, and technical checks, see the [technical guide](../TECHNICAL/README.md) and [data pipeline](../TECHNICAL/docs/DATA_PIPELINE.md). Technical generation and completed solution materials contain spoilers; the learner ZIPs keep them out.

Synthetic data in both formats are released under [CC0 1.0](LICENSE). Educational text and code use the repository's [MIT license](../LICENSE).
