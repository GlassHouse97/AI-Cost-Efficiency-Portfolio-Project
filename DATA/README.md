# Case Study Data

These are the original source files for the Marketing R Us (MRU) case study. All organizations, people, prices, usage, and business results are fictional. The reporting month is September 2026.

## Complete Downloads

Choose the package for your track, extract it, and open **START_HERE.html**. Each package works offline and contains both Excel and CSV versions of its source data.

| Track | Package contents | Download |
| --- | --- | --- |
| **Quick Challenge** | The questions in one HTML document, one raw Excel workbook, the matching CSV, a data dictionary, and licenses | **[Download Quick Challenge ZIP](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru-quick-challenge.zip)** |
| **Portfolio Project** | The HTML guide, question brief, column guide, formulas, checklist, one raw Excel workbook, four matching CSVs, a data dictionary, and licenses | **[Download Portfolio Project ZIP](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/mru-portfolio-project.zip)** |

Excel and CSV contain the same records. Choose whichever format suits your analysis. The Quick Challenge covers Campaigns 1 and 2 from the larger Portfolio Project dataset, so the tracks overlap.

## Individual Source Files

The files below are also included in the complete packages.

### Quick Challenge

**[Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru-quick-challenge.xlsx)** or **[CSV file](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru_quick_challenge.csv)**

Each record describes a completed task, including its department, campaign, hours, prompt usage, token usage, and model rates. The workbook has one **Raw** source worksheet and a **Data Dictionary** worksheet. The [Quick Challenge data dictionary](TRACKS/quick-challenge/DATA_DICTIONARY.md) is also available here as a document defining every source column.

### Portfolio Project

**[Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/mru-portfolio-project.xlsx)** with four source worksheets corresponding to the CSV files below and a **Data Dictionary** worksheet. The [Portfolio Project data dictionary](TRACKS/portfolio-project/DATA_DICTIONARY.md) defines every source column and explains how the tables relate to each other.

| CSV file and worksheet | Record type | Source fields |
| --- | --- | --- |
| [work_log.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/work_log.csv) / `work_log` | Completed task | Baseline, actual, and rework hours; workflow observations |
| [ai_usage.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/ai_usage.csv) / `ai_usage` | Prompt | Tokens, model, product, prompt reason, and usage date |
| [model_pricing.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/model_pricing.csv) / `model_pricing` | Model | Fictional input and output prices in USD per million tokens |
| [campaigns.csv](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/portfolio-project/campaigns.csv) / `campaigns` | Campaign | Revenue and other spending |

## License and Reproduction

Synthetic data are released under [CC0 1.0](LICENSE). Educational text and code use the repository's [MIT license](../LICENSE). Dataset generation and validation are documented in the [technical guide](../TECHNICAL/README.md).
