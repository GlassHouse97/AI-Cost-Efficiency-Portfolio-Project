# AI Cost Efficiency and Workflow Value

A business analytics case study by Chris Delgado.

## The Business Problem

AI can reduce the time needed to prepare content and complete routine tasks. It also involves usage fees and staff time spent preparing prompts, reviewing results, and correcting mistakes. These costs need to be included when evaluating its value to a business.

MRU is a fictional marketing company that uses AI for campaign planning, content writing, data preparation, and reporting. The case study covers 240 completed tasks across four campaigns during September 2026. These tasks involve the Content, Creative, Marketing Operations, and Analytics departments.

Management needs to understand which uses of AI justify their cost and which workflows need improvement. Faster drafting may be offset by additional review or repeated corrections. Higher AI spending may be worthwhile when it saves enough staff time. The challenge is to account for both AI fees and the work required to produce an acceptable result.

The analysis compares estimated task hours without AI against actual hours with AI, including preparation, review, and rework. Campaigns 1 and 2 are the main comparison, while Campaigns 3 and 4 provide context. The findings help identify where to improve work instructions, review practices, or model selection.

Staff time is valued at $50 per hour to estimate the value of capacity gained or lost. After subtracting AI fees, this becomes **net AI value**. It does not represent a change in payroll expenses. **Overall campaign profit or loss** is calculated separately because it also includes revenue and other campaign spending.

## Start Here

| Folder | What you will find |
| --- | --- |
| **[QUESTIONS](QUESTIONS/README.md)** | The business questions, analysis guidelines, and two learner tracks |
| **[DATA](DATA/README.md)** | Complete exercise downloads, Excel workbooks, CSV files, and a data guide |
| **[SOLUTION](SOLUTION/README.md)** | A complete Excel solution for the Quick Challenge and a detailed dashboard case study for the Portfolio Project |

**To review the project**, begin with the [assignment](QUESTIONS/README.md), then examine the [dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app). Start with Company overview, followed by Campaign comparison and Workflow investigation. The [executive summary](SOLUTION/TRACKS/portfolio-project/EXECUTIVE_SUMMARY.md) and [six detailed answers](SOLUTION/TRACKS/portfolio-project/README.md#detailed-answers) explain the conclusions.

**To complete the exercise**, choose a track in [QUESTIONS](QUESTIONS/README.md), download its [data package](DATA/README.md), and open **START_HERE.html**. Complete your analysis before reviewing the solution.

## View a Completed Solution

| Track | Finished answer |
| --- | --- |
| **[Quick Challenge](SOLUTION/TRACKS/quick-challenge/README.md)** | **[Download the completed Excel workbook](SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx?raw=true)**. It contains six answers, charts, summaries, formulas, and the original data. |
| **[Portfolio Project](SOLUTION/TRACKS/portfolio-project/README.md)** | **[Open the live dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app)** and read the detailed analysis with supporting images. |

The completed Excel workbook contains answers and is separate from the learner download. Open it in Excel to view the worksheets, as GitHub does not display them. The **`DATA/TRACKS/`**, **`QUESTIONS/TRACKS/`**, and **`SOLUTION/TRACKS/`** folders each contain the same two tracks, `quick-challenge` and `portfolio-project`.

## Three Key Findings

1. **Results vary by campaign.** The four campaigns produce a combined estimated net AI value of $2,820. Campaign 1 contributes $4,500 in positive value, while Campaign 2 has negative net AI value of $4,900.
2. **Staff time explains most of the difference.** Of the $9,400 gap between Campaigns 1 and 2, $8,500 comes from estimated time value and $900 comes from AI fees.
3. **Campaign 2 requires more rework.** It records 87.82 rework hours and 482 correction prompts, compared with Campaign 1's 10.74 hours and 68 corrections. Further investigation would be needed to establish the causes.

![Campaign comparison showing AI spend, time saved, and net AI value](SOLUTION/TRACKS/portfolio-project/visualizations/02_campaign_comparison.jpg)

*The dashboard image shows Campaigns 1 and 2 across all departments, products, and models, using the original baseline estimates. These 120 tasks have a combined net AI value of negative $400. The company total of positive $2,820 also includes Campaigns 3 and 4.*

The dashboard presents AI spending, staff time, campaign results, and rework. Readers can compare results and adjust the baseline estimates to assess how the findings change.

**[Open the live dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app)**

[Read the executive summary](SOLUTION/TRACKS/portfolio-project/EXECUTIVE_SUMMARY.md)

## Try the Analysis Yourself

| Track | Scope and planning target | Complete download |
| --- | --- | --- |
| **[Quick Challenge](QUESTIONS/TRACKS/quick-challenge/README.md)** | 120 tasks. Beginner to early intermediate. About four hours using Excel or basic BI. | **[Download Quick Challenge ZIP](DATA/TRACKS/quick-challenge/mru-quick-challenge.zip?raw=true)** |
| **[Portfolio Project](QUESTIONS/TRACKS/portfolio-project/README.md)** | 240 tasks with data for individual prompts. Intermediate. About 12 to 16 hours using Excel, SQL, BI, or code. | **[Download Portfolio Project ZIP](DATA/TRACKS/portfolio-project/mru-portfolio-project.zip?raw=true)** |

Each ZIP includes an **Excel workbook, all CSV source files, and complete instructions**. Extract the files and open **START_HERE.html**. The exercises contain source data and guidance without completed answers.

Use either the Excel files or the CSV files. They contain the same records and should not be combined. The time estimates are provided for planning and will vary with experience.

## About the Data

* **Reporting month:** September 2026.
* **Full project:** four campaigns, 240 unique tasks, and 3,360 prompts.
* **Quick Challenge:** the same 120 tasks from Campaigns 1 and 2, with prompt usage summarized per task.
* **Cleaning exercise:** repeated task exports and inconsistent department formatting are retained in both Excel and CSV.

All people, companies, prices, usage, and financial results are **fictional and created for this exercise**. They do not represent a real company's results or current AI vendor prices. The [data guide](DATA/README.md) explains the files and preparation requirements.

## Technical Details

The dashboard uses **HTML, CSS, and JavaScript**. A small Node.js container serves it on **Google Cloud Run**. The **[TECHNICAL](TECHNICAL/README.md)** folder contains the source code, setup instructions, analysis scripts, tests, and deployment documentation.

Prepared with Codex assistance. Code and documentation use the [MIT license](LICENSE). Synthetic data use [CC0 1.0](DATA/LICENSE).
