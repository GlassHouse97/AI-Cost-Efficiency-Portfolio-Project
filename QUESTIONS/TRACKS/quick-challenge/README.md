# MRU AI value Quick Challenge

**Beginner to early intermediate · Four hour target · Excel or a basic BI tool**

<!-- ONLINE_DOWNLOADS_START -->
## Download the Data

[Download the complete Quick Challenge ZIP](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru-quick-challenge.zip) for the workbook, CSV, and all instructions. Extract the entire ZIP, then open **START_HERE.html** from the extracted folder. Keep the extracted files together so the guide can open the data offline.

For individual files, download the [Excel workbook](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru-quick-challenge.xlsx) or the [CSV source](https://raw.githubusercontent.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/main/DATA/TRACKS/quick-challenge/mru_quick_challenge.csv). Both contain the same raw records. Choose one format.

Your browser may display CSV text. Save the page as a CSV file or use the complete ZIP. [Browse the source files on GitHub](https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/tree/main/DATA/TRACKS/quick-challenge).
<!-- ONLINE_DOWNLOADS_END -->

Marketing-R-Us (MRU) is a fictional marketing company that used the fictional ChatABC AI platform for Campaign 1 and Campaign 2. Your job is to determine whether the estimated value of staff time saved justifies AI fees. All employees, clients, prices, and results are synthetic. The dataset is an exercise, not evidence about any real AI provider.

Start with the raw sheet in `mru-quick-challenge.xlsx` **or** `mru_quick_challenge.csv`. These are two formats of the same source records; use one, not both. One row represents one completed task, with its prompts and tokens already summed. The two campaigns were completed during one month. Every task belongs to one employee, department, product, and model. There are eight fictional employees across Content, Creative, Marketing Operations, and Analytics.

The products are CampaignChat for planning, CopyStudio for writing, DataFlow for data work, and InsightDesk for summaries. Lite and Pro are fictional models with fixed prices shared by every product. You do not need accounts, API keys, coding, or additional data. A spreadsheet application is sufficient.

The complete Quick Challenge ZIP contains the Excel workbook, the matching CSV, and all exercise guidance, without a completed dashboard or campaign answer totals. Both formats preserve the original cleaning exercise. Open `START_HERE.html` for this entire guide in your browser without an internet connection. The same material is divided into Markdown files for reading on GitHub.

## What you will learn

Clean a small export, calculate AI fees from input and output tokens, compare estimated and actual human effort, and communicate a defensible business recommendation. Tokens measure processed text, not work hours. Value staff time at **$50 per hour** throughout this exercise.

You should already be able to open a CSV, create a spreadsheet table and PivotTable, enter arithmetic formulas, and insert a chart. The starter steps below recap these actions. Power Query, DAX, SQL, Python, and web development are optional and are never needed to finish this track.

## Your four hour plan

| Time | Activity |
| --- | --- |
| 0 to 20 minutes | Read the brief, open the workbook or CSV, and explain one row in your own words. |
| 20 to 50 minutes | Remove duplicate tasks and standardize department labels. |
| 50 to 110 minutes | Calculate tokens, AI cost, hours saved, time value, and net AI value. Summarize campaign totals and ROI. |
| 110 to 160 minutes | Use PivotTables to compare campaigns, departments, AI spending, and rework. |
| 160 to 215 minutes | Create one dashboard sheet with KPI cells and charts. |
| 215 to 240 minutes | Write your recommendation and check that totals agree. |

Four hours is a planning target, not a tested guarantee for every learner. Keep optional analysis out of your first submission.

## Six questions to answer

1. How many input and output tokens did each campaign use, what did they cost, and how many prompts were made?
2. How many hours did each campaign save or lose against its no AI estimate?
3. After paying for AI, was estimated net value positive or negative for each campaign?
4. Which department had the highest AI spending, and which had the highest net AI value?
5. Which campaign had more rework, and which recorded issues appeared most often?
6. Should MRU keep, change, or reduce how it uses AI? Give two actions supported by the numbers.

## Get started in Excel

1. Open `mru-quick-challenge.xlsx` in Excel to begin with the supplied raw sheet. Alternatively, import `mru_quick_challenge.csv` using **Data → From Text/CSV** with a comma delimiter. Choose one source format; do not combine the workbook and CSV. Check that `completion_date` is a date and the rates, tokens, prompts, and hours are numeric.
2. Use **File → Save As** to save your own working workbook (`.xlsx`). Keep the supplied workbook and CSV unchanged. If you began with CSV, saving as `.xlsx` is necessary to preserve multiple sheets, formulas, charts, and formatting.
3. Confirm the first sheet is named **Raw**, then copy it to a new sheet named **Clean**. The supplied workbook already contains a formatted Excel table, so copying its sheet also copies that table. Click a populated cell in Clean: if **Table Design** appears, rename the copied table `Tasks` there. If you imported CSV and the data is not yet a table, choose **Insert → Table** (or Ctrl+T), confirm that it has headers, then name it `Tasks` on **Table Design**.
4. Inspect `work_item_id` for repeat rows. The raw export has 122 records, including exact duplicate task records. In the Clean table, choose **Data → Remove Duplicates**, select only `work_item_id`, and confirm. Verify 120 unique completed tasks remain. Record the change in a small cleaning note; do not delete tasks just because they share a department or task type.
5. Standardize department spelling using a temporary column with `=PROPER(TRIM([@department]))`. Copy the results and **Paste Special → Values** over the original department cells, then remove the temporary column. The four final labels must be Content, Creative, Marketing Operations, and Analytics. Filter the column to check them.
6. Add the five calculated columns described in FORMULAS.md. Enter each formula in the first table row; Excel will normally fill it down. Inspect one task manually and leave all calculation columns visible.
7. Click a cell in `Tasks`, then choose **Insert → PivotTable → New Worksheet**. Put `campaign` in Rows. Put the numeric fields you need in Values. Open **Value Field Settings** and choose **Sum**, not Count or Average. Build a second PivotTable with `department` in Rows. Build another with `campaign` in Rows and `issue_tag` in Columns, counting `work_item_id`.
8. For campaign ROI, divide each campaign's summed net AI value by its summed AI cost. Calculate it next to a PivotTable or in a small summary table; do not average task ROI. Refresh PivotTables after any source change.
9. Create a **Dashboard** sheet. Link KPI cells to the overall totals and insert charts from the summaries with **Insert → Column or Bar Chart**. Use clear titles and units; a clustered column chart can compare baseline and actual hours. Keep colors consistent and use a visible zero line when values can be negative.
10. Check all dashboard totals against the Clean table. Write your 150 to 250 word recommendation and complete SUBMISSION_CHECKLIST.md.

Excel menus differ slightly by edition. If your locale uses semicolons in formulas, replace argument-separating commas with semicolons. Arithmetic operators and the supplied USD rates stay the same.

## Optional basic BI route

Import either the CSV or the workbook raw sheet, remove duplicate `work_item_id` records, trim and standardize departments, and add the same five arithmetic calculations. Use summed metrics for visuals and calculate ratios from totals. Submit your dashboard file or accessible view, the cleaned CSV, and a calculation summary. An Excel workbook remains a complete solution; BI features are optional.

## Limited outside AI assistance

Use at most **20 minutes of AI help within your four hours**, for a formula explanation, PivotTable question, or troubleshooting. Create the analysis, charts, and recommendation yourself. Briefly disclose the tool, approximate minutes, and what you asked it to explain. This is an honor-based guideline with no monitoring or enforcement software. The author may use AI to prepare this exercise without that learner limit.

## A sound interpretation

Actual hours already include preparation, prompting, setup, checking, and corrections. Rework is a subset of actual hours: do not add it again. Baseline and actual hours refer to the same completed task at acceptable quality. A negative hours-saved number means the task took longer with AI. Estimated time value is not a cash saving from payroll, and this observational exercise does not prove AI caused an outcome.

If you chart costs by `completion_date`, label the result **AI spending by task completion date**. This is not a provider billing timeline. Campaign revenue and profit are not supplied in this track.

Code and educational text are under the included MIT license. Synthetic Excel and CSV data is dedicated under the included CC0 1.0 license.
