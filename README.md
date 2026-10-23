# AI Cost Efficiency & Workflow Value

**Does the value of staff time saved justify the AI bill?** A business analytics case study by Chris Delgado.

## Explore the Dashboard

**[Open the live dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app)** · [Read the executive summary](SOLUTION/TRACKS/portfolio-project/EXECUTIVE_SUMMARY.md)

Explore AI spending, human effort, campaign results, and rework. Filter the analysis, test baseline assumptions, and inspect the evidence behind each finding.

## The Business Problem

Marketing-R-Us, a fictional marketing company, uses AI to support campaign work. Leadership needs to know whether the time saved covers token fees after preparation, review, and corrections—and which workflows deserve improvement.

The analysis separates estimated **net AI value** from **whole-campaign profit or loss**. Staff time is valued at $50 per hour; this estimates useful capacity, not payroll cash savings.

## Start Here

| Folder | What you will find |
| --- | --- |
| **[QUESTIONS](QUESTIONS/README.md)** | The business questions, analysis guidelines, and two learner tracks |
| **[DATA](DATA/README.md)** | Complete exercise downloads, Excel workbooks, CSV files, and a data guide |
| **[SOLUTION](SOLUTION/README.md)** | Two completed tracks: a self-contained Excel answer and the deeper dashboard case study |

- **Portfolio review:** Read this overview → [QUESTIONS](QUESTIONS/README.md) for the assignment → [live dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app) for the evidence → [executive summary](SOLUTION/TRACKS/portfolio-project/EXECUTIVE_SUMMARY.md) and [six detailed answers](SOLUTION/TRACKS/portfolio-project/README.md#detailed-answers) for the conclusions. In the dashboard, follow **Company overview → Campaign comparison → Workflow investigation**.
- **Learner route:** Choose a track in [QUESTIONS](QUESTIONS/README.md), download its complete [DATA package](DATA/README.md), and open **START_HERE.html**. Complete your analysis before opening **SOLUTION**.

## View a Completed Solution

| Track | Finished answer |
| --- | --- |
| **[Quick Challenge](SOLUTION/TRACKS/quick-challenge/README.md)** | **[Download the solved Excel workbook](SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx?raw=true)** — six answers, compact charts, grouped summaries, formulas, and original data in one file |
| **[Portfolio Project](SOLUTION/TRACKS/portfolio-project/README.md)** | **[Explore the live dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app)** and read the deeper analysis with supporting images |

The solved Excel file contains answers and is separate from the answer-free learner download. Download it and open it in Excel; GitHub does not display its worksheets. All three reader areas use the same layout: **`DATA/TRACKS/` → `QUESTIONS/TRACKS/` → `SOLUTION/TRACKS/`**, with `quick-challenge` and `portfolio-project` inside each.

## Three Key Findings

- **The company total hides opposite outcomes.** All four campaigns create $2,820 of estimated net AI value; Campaign 1 contributes +$4,500 while Campaign 2 loses $4,900.
- **Human effort explains most of the focal gap.** Of the $9,400 difference between Campaigns 1 and 2, $8,500 comes from estimated time value and $900 from higher AI fees.
- **Campaign 2 has substantially more rework.** It records 87.82 rework hours and 482 correction prompts, compared with Campaign 1's 10.74 hours and 68 corrections. These patterns identify questions to investigate, not proven causes.

![Campaign comparison showing AI spend, time saved, and net AI value](SOLUTION/TRACKS/portfolio-project/visualizations/02_campaign_comparison.jpg)

*Actual dashboard view: Campaigns 1 and 2, all departments, products, and models; original baseline estimates. These 120 tasks have combined net AI value of −$400. The all-company +$2,820 includes Campaigns 3 and 4.*

## Try the Analysis Yourself

| Track | Scope and planning target | Complete download |
| --- | --- | --- |
| **[Quick Challenge](QUESTIONS/TRACKS/quick-challenge/README.md)** | 120 tasks; beginner / early intermediate; about four hours; Excel or basic BI | **[Download Quick Challenge ZIP](DATA/TRACKS/quick-challenge/mru-quick-challenge.zip?raw=true)** |
| **[Portfolio Project](QUESTIONS/TRACKS/portfolio-project/README.md)** | 240 tasks and prompt-level data; intermediate; about 12–16 hours; Excel, SQL, BI, or code | **[Download Portfolio Project ZIP](DATA/TRACKS/portfolio-project/mru-portfolio-project.zip?raw=true)** |

Each ZIP includes its **Excel workbook, all CSV source files, and complete instructions**. Unzip it and open **START_HERE.html**. The exercises contain raw inputs and guidance, without completed answers.

Use **Excel or CSV**: they contain the same source records, so do not combine both copies. The four-hour and 12–16-hour estimates are planning targets, not completion guarantees.

## About the Data

- **Reporting month:** September 2026.
- **Full project:** four campaigns, 240 unique tasks, and 3,360 prompts.
- **Quick Challenge:** the same 120 tasks from Campaigns 1 and 2, with prompt usage summarized per task.
- **Cleaning exercise:** repeated task exports and inconsistent department formatting are retained in both Excel and CSV.

All people, companies, prices, usage, and financial results are **synthetic and deliberately calibrated for teaching**. They do not represent a real company's results or current AI vendor prices. See the [data guide](DATA/README.md) for file descriptions and preparation rules.

## Technical Details

The dashboard uses **HTML, CSS, and JavaScript**, served by a small Node.js container on **Google Cloud Run**. Source code, local setup, reproduction steps, tests, and deployment documentation are collected in **[TECHNICAL](TECHNICAL/README.md)**. You can review the business case without opening that folder.

Prepared with Codex assistance. Code and documentation use the [MIT license](LICENSE); synthetic data use [CC0 1.0](DATA/LICENSE).
