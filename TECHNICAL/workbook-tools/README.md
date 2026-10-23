# Rebuild the learner Excel files

The two `.xlsx` files under `DATA/` are raw learner inputs. Each worksheet has the same headers, record order, and source values as its matching CSV. Duplicate IDs and department whitespace are intentional exercise data and remain intact. The CSV files are canonical.

`build-learner-workbooks.mjs` uses the Codex workspace's bundled `@oai/artifact-tool` package. It does not add a repository dependency. Opening the Excel files requires no authoring runtime.

To rebuild in Codex:

1. Use `load_workspace_dependencies` to locate the bundled Node executable and `node_modules` directory.
2. Create a `node_modules` junction in a writable temporary or `.qa/` runtime directory, pointing at that bundled directory. Set `WORKBOOK_ARTIFACT_RUNTIME` to the parent of this junction.
3. Follow the Spreadsheets skill's operation marker requirement, then run the builder with the bundled Node executable.
4. Run the repository's workbook-to-CSV parity check. Review the rendered worksheet samples in `.qa/workbook-previews/` before committing regenerated workbooks.

The builder writes only the two named workbooks and ignored `.qa/` inspection/preview files. It uses `Workbook.fromCSV` to read source fields and explicitly types dates and numeric columns. Dates display as `yyyy-mm-dd`; strings are not trimmed. There are no formulas, answer columns, calculated totals, charts, or solution tabs in the learner files. Table filter buttons and frozen header rows support exploration.

| Workbook | Worksheets in order |
|---|---|
| `DATA/quick-challenge/mru-quick-challenge.xlsx` | `Raw` |
| `DATA/portfolio-project/mru-portfolio-project.xlsx` | `campaigns`, `work_log`, `ai_usage`, `model_pricing` |

The `Raw` worksheet uses `mru_quick_challenge.csv`; portfolio source filenames are the worksheet names plus `.csv`. Text fields retain exact spelling, spaces, and IDs. Columns named `completion_date` or `usage_date` contain native Excel dates. Token/prompt counts, model rates, campaign dollar values, and hour measurements contain numbers. Source provenance is documented here rather than inserted into the raw worksheets.
