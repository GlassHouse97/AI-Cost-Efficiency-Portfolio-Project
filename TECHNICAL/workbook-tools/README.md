# Rebuild the Excel files

The two `.xlsx` files under `DATA/` contain raw learner inputs and a Data Dictionary worksheet. Each source worksheet has the same headers, record order, and values as its matching CSV. Duplicate IDs and department whitespace are intentional exercise data and remain intact. The CSV files are canonical for source records. Each track's `DATA_DICTIONARY.md` is canonical for its field definitions.

`build-learner-workbooks.mjs` uses the Codex workspace's bundled `@oai/artifact-tool` package. It does not add a repository dependency. Opening the Excel files requires no authoring runtime.

To rebuild in Codex:

1. Use `load_workspace_dependencies` to locate the bundled Node and Python executables and the `node_modules` directory.
2. Create a `node_modules` junction in a writable temporary or `.qa/` runtime directory, pointing at that bundled directory. Set `WORKBOOK_ARTIFACT_RUNTIME` to the parent of this junction.
3. Follow the Spreadsheets skill's operation marker requirement, then run the builder with the bundled Node executable.
4. Run the repository's workbook-to-CSV parity and dictionary checks. Review the rendered dictionary sheets in `.qa/workbook-previews/` before committing regenerated workbooks. Use `--render-raw` when source data or source sheet formatting changes and needs visual review.

The builder writes only the two named workbooks and ignored `.qa/` inspection/preview files. It uses `Workbook.fromCSV` to read source fields and explicitly types dates and numeric columns. Dates display as `yyyy-mm-dd`; strings are not trimmed. There are no formulas, answer columns, calculated totals, charts, or solution tabs in the learner files. Table filter buttons and frozen header rows support exploration.

| Workbook | Worksheets in order |
|---|---|
| `DATA/TRACKS/quick-challenge/mru-quick-challenge.xlsx` | `Raw`, `Data Dictionary` |
| `DATA/TRACKS/portfolio-project/mru-portfolio-project.xlsx` | `campaigns`, `work_log`, `ai_usage`, `model_pricing`, `Data Dictionary` |

The `Raw` worksheet uses `mru_quick_challenge.csv`; portfolio source filenames are the worksheet names plus `.csv`. Text fields retain exact spelling, spaces, and IDs. Columns named `completion_date` or `usage_date` contain native Excel dates. Token/prompt counts, model rates, campaign dollar values, and hour measurements contain numbers. Source provenance is documented here rather than inserted into the raw worksheets.

The Data Dictionary worksheet is generated from the four-column table in the track's `DATA_DICTIONARY.md`. It lists each source field, its worksheet, type and units, and meaning. These are source definitions only. Calculation methods and worked answers remain separate from the raw workbooks. Tests compare the dictionary with both the Markdown definitions and every CSV header.

## Completed Quick Challenge Workbook

[`build-quick-solution.mjs`](build-quick-solution.mjs) creates the separate answer workbook at `SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx`. Use the same bundled Node executable and `WORKBOOK_ARTIFACT_RUNTIME` setup described above. Set `WORKBOOK_PYTHON` to the absolute path of the bundled Python executable so the builder can run its chart-export compatibility helper, then run:

```sh
node TECHNICAL/workbook-tools/build-quick-solution.mjs
```

Its sheets are **Solution**, **Summaries**, **Clean**, and **Raw**, in that order. Raw preserves the 122 original records; Clean contains 120 deduplicated tasks, normalized department labels, and Excel metric formulas. Summaries uses transparent `SUMIFS` and `COUNTIFS` calculations. Solution presents the six answers, editable charts, and recommendations. It contains no macros or external data connections.

The cleaned rows are a snapshot, not a refreshable import pipeline. Formula results update when their input cells change; adding or changing raw records requires repeating the cleaning step and extending relevant formula ranges. This completed workbook contains answers and is excluded from the learner ZIPs.

## Completed Portfolio Project Workbook

[`build-portfolio-solution.mjs`](build-portfolio-solution.mjs) creates `SOLUTION/TRACKS/portfolio-project/mru-portfolio-project-solution.xlsx` from the four canonical CSV files in `DATA/TRACKS/portfolio-project/`. Use the same bundled Node executable, `WORKBOOK_ARTIFACT_RUNTIME`, and `WORKBOOK_PYTHON` setup as the Quick Challenge builder, then run:

```sh
node --max-old-space-size=8192 TECHNICAL/workbook-tools/build-portfolio-solution.mjs
```

The authoring process needs the larger Node memory limit above because it calculates and checks thousands of linked formulas. Opening the finished workbook requires no authoring runtime.

The workbook has 14 worksheets. **Solution** presents the six Portfolio Project answers and editable charts. **Campaigns**, **Mix**, **Workflow**, and **Daily Usage** provide summaries. **Tasks**, **Prompt Totals**, and **Priced Usage** expose the prepared data and Excel formulas. **Raw Work Log**, **Raw AI Usage**, **Model Pricing**, and **Campaign Inputs** retain the source records. **Preparation** records all ten preparation steps from START_HERE, and **Data Dictionary** defines source and calculated fields.

The builder preserves 242 raw work log rows, removes the two exact duplicate task records, normalizes department names, and validates keys, types, prices, and task relationships. It prices each of 3,360 prompts before aggregating them to 240 tasks, so task hours and campaign financial inputs are counted once. Prompt costs retain six decimal places; displayed currency is rounded only for presentation. The saved default case uses $50 per hour and reconciles with the dashboard.

Existing input changes recalculate through Excel formulas. Raw imports and cleaned task membership are snapshots, so changes to source records require rebuilding. The written answers describe the saved default case and do not rewrite themselves after edits. The workbook has no macros or external data connections and is excluded from learner ZIPs.

`TECHNICAL/tests/test_portfolio_solution.py` independently reads the saved workbook and source CSVs. It checks source preservation, every priced prompt and prepared task, summary and sensitivity values, native chart caches, and parity with the dashboard calculation module.

## Native Chart Export Compatibility

[`cache_chart_values.py`](cache_chart_values.py) repairs missing chart display caches after XLSX export. It reads each chart's declared worksheet references and copies the already-calculated saved cell values into the matching native chart cache. It preserves formulas, chart references, and source inputs, rejects missing or error-valued sources, and leaves all non-chart ZIP parts unchanged. The solution builder invokes this helper after export.

This is an export compatibility step, not a spreadsheet calculation engine. Excel can still edit and recalculate the charts from their linked cells; readers need no authoring runtime, Python, macros, or external connection to open the workbook.
