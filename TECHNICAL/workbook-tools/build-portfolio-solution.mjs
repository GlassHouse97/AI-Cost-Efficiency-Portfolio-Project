import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Optional authoring tool. The finished workbook needs no macros or connections.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const runtime = process.env.WORKBOOK_ARTIFACT_RUNTIME;
const python = process.env.WORKBOOK_PYTHON;
if (!runtime || !python) throw new Error('Set WORKBOOK_ARTIFACT_RUNTIME and WORKBOOK_PYTHON to the bundled workspace runtime.');
const require = createRequire(path.join(path.resolve(runtime), 'package.json'));
const { Workbook, SpreadsheetFile, FileBlob } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const destination = path.join(root, 'SOLUTION/TRACKS/portfolio-project/mru-portfolio-project-solution.xlsx');
const outputDir = path.join(root, 'outputs/01a16549-fb89-7931-89c2-47b56643a454');
const previewDir = path.join(root, '.qa/portfolio-solution-previews');
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });
// A bounded presentation repair can reuse the verified calculation graph.
// The normal full build below includes the same formatting and chart changes.
if (process.argv.includes('--refine-presentation')) {
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(destination));
  const solution = workbook.worksheets.getItem('Solution');
  const prep = workbook.worksheets.getItem('Preparation');
  const campaigns = workbook.worksheets.getItem('Campaigns');
  solution.getRange('G55:G58').values = [['Only five tasks are represented in this example.'], ['Template use coincides with less rework and fewer corrections.'], ['Changed briefs coincide with more rework and corrections.'], ['These associations do not isolate a causal effect.']];
  solution.getRange('F55:F58').clear({ applyTo: 'contents' });
  solution.getRange('E5').values = [['Editable assumption. Reference answers use $50.']];
  solution.getRange('D5').clear({ applyTo: 'contents' });
  for (let r = 21; r <= 37; r++) prep.getRange(`E${r}`).formulas = [[`=ROUND(C${r}-D${r},6)`]];
  for (const r of [33, 34, 35]) {
    const formula = prep.getRange(`C${r}`).formulas[0][0];
    if (!formula.startsWith('=ROUND(')) prep.getRange(`C${r}`).formulas = [[`=ROUND(${formula.slice(1)},6)`]];
  }
  prep.getRange('C21:E37').setNumberFormat('#,##0.00;(#,##0.00);0.00');
  prep.getRange('C21:D24').setNumberFormat('#,##0');
  campaigns.getRange('A15:C15').values = [['Campaign', 'Estimated hours', 'Actual hours']];
  campaigns.getRange('A15:C19').format = { font: { name: 'Arial', size: 11, color: '#202E3B' }, rowHeight: 23, verticalAlignment: 'center' };
  campaigns.getRange('A15:C15').format = { fill: '#16324F', font: { name: 'Arial', size: 11, bold: true, color: '#FFFFFF' }, wrapText: true, rowHeight: 44 };
  for (let i = 0; i < 4; i++) campaigns.getRange(`A${16 + i}:C${16 + i}`).formulas = [[`=INDEX($B$7:$B$10,MATCH("C00${i + 1}",$A$7:$A$10,0))`, `=INDEX($L$7:$L$10,MATCH("C00${i + 1}",$A$7:$A$10,0))`, `=INDEX($M$7:$M$10,MATCH("C00${i + 1}",$A$7:$A$10,0))`]];
  campaigns.getRange('B16:C19').setNumberFormat('#,##0.00;(#,##0.00);0.00');
  const hours = solution.charts.items[1];
  hours.setData(campaigns.getRange('A15:C19'));
  hours.series.items[0].fill = '#A8BAC9'; hours.series.items[1].fill = '#245A81';
  const dictionary = workbook.worksheets.getItem('Data Dictionary');
  const rows = dictionary.getRange('A7:D188').values;
  rows.forEach((row, index) => {
    if (row[0] !== 'Model Pricing' && row[1] === 'model' && !row[0].startsWith('Raw')) dictionary.getRange(`D${index + 7}`).values = [['Fictional model used by the task or prompt. Lite and Pro connect to the model prices in Model Pricing.']];
  });
  workbook.recalculate();
  assert.ok(Math.abs(solution.getRange('C11').values[0][0] - 2820) < 1e-6);
  for (const value of prep.getRange('E21:E37').values) assert.equal(value[0], 0);
  for (const [name, range, filename] of [['Solution', 'A1:M42', 'solution-overview'], ['Solution', 'A43:M59', 'solution-mix-workflow'], ['Preparation', 'B19:E37', 'preparation-checks'], ['Campaigns', 'A15:C19', 'campaign-chart-inputs'], ['Data Dictionary', 'A35:D47', 'dictionary-derived']]) {
    const preview = await workbook.render({ sheetName: name, range, scale: 1.3, format: 'png' });
    await fs.writeFile(path.join(previewDir, `${filename}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
  const outputPath = path.join(outputDir, path.basename(destination));
  await (await SpreadsheetFile.exportXlsx(workbook)).save(outputPath);
  console.log(execFileSync(python, [path.join(root, 'TECHNICAL/workbook-tools/cache_chart_values.py'), outputPath], { encoding: 'utf8' }));
  await fs.copyFile(outputPath, destination);
  console.log('Presentation refinements exported.');
  process.exit(0);
}
const sourceBase = 'https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/blob/main/';
const sourceFolder = 'DATA/TRACKS/portfolio-project/';
const numeric = new Set(['campaign_revenue_usd', 'other_campaign_cost_usd', 'input_tokens', 'output_tokens', 'baseline_hours', 'actual_hours', 'rework_hours', 'input_rate_usd_per_million', 'output_rate_usd_per_million']);
const dates = new Set(['usage_date', 'completion_date']);
const sources = {};
for (const name of ['work_log', 'ai_usage', 'model_pricing', 'campaigns']) {
  const imported = await Workbook.fromCSV(await fs.readFile(path.join(root, sourceFolder, `${name}.csv`), 'utf8'), { sheetName: 'Source' });
  const [headers, ...records] = imported.worksheets.getItemAt(0).getUsedRange().values;
  const rows = records.map(row => row.map((value, index) => {
    assert.ok(value !== '' && value !== null, `Missing ${name}.${headers[index]}`);
    if (dates.has(headers[index])) {
      assert.match(value, /^\d{4}-\d{2}-\d{2}$/);
      const date = new Date(`${value}T00:00:00Z`);
      assert.equal(date.toISOString().slice(0, 10), value);
      return (date.getTime() - Date.UTC(1899, 11, 30)) / 86400000;
    }
    if (numeric.has(headers[index])) {
      assert.match(String(value), /^\d+(?:\.\d+)?$/);
      const number = Number(value);
      assert.ok(Number.isFinite(number) && number >= 0);
      if (headers[index].endsWith('_tokens')) assert.ok(Number.isInteger(number));
      return number;
    }
    return value;
  }));
  const unique = new Map(), duplicates = [];
  for (const row of rows) {
    if (unique.has(row[0])) { assert.deepEqual(row, unique.get(row[0]), `Conflicting ${name} key ${row[0]}`); duplicates.push(row[0]); }
    else unique.set(row[0], row);
  }
  sources[name] = { headers, rows, unique: [...unique.values()], duplicates };
}
const work = sources.work_log;
const cleaned = work.unique.map(row => row.map((v, i) => i === 3 ? v.trim().toLowerCase().replace(/\b\w/g, c => c.toUpperCase()) : v));
const tasksById = new Map(cleaned.map(row => [row[0], row]));
const campaignsById = new Map(sources.campaigns.unique.map(row => [row[0], row]));
const pricesByModel = new Map(sources.model_pricing.unique.map(row => [row[0], row]));
const promptGroups = new Map();
const departments = new Set(['Content', 'Creative', 'Marketing Operations', 'Analytics']);
for (const row of cleaned) {
  assert.ok(campaignsById.has(row[2])); assert.ok(departments.has(row[3]));
  assert.ok(row[8] <= row[7]);
  for (const index of [10, 11]) assert.ok(['Yes', 'No'].includes(row[index]));
}
for (const row of sources.ai_usage.unique) {
  const task = tasksById.get(row[2]); assert.ok(task, `Unmatched prompt ${row[0]}`);
  assert.equal(row[3], task[2]); assert.ok(row[1] <= task[1]); assert.ok(pricesByModel.has(row[5]));
  assert.ok(['First attempt', 'Followup', 'Correction'].includes(row[8]));
  const group = promptGroups.get(row[2]) ?? [];
  if (group.length) { assert.equal(row[4], group[0][4]); assert.equal(row[5], group[0][5]); }
  group.push(row); promptGroups.set(row[2], group);
}
for (const row of cleaned) {
  assert.ok(promptGroups.has(row[0]));
  assert.equal(promptGroups.get(row[0]).filter(prompt => prompt[8] === 'First attempt').length, 1);
}
assert.equal(cleaned.length, 240); assert.equal(sources.ai_usage.unique.length, 3360);
assert.deepEqual(work.duplicates, ['W0018', 'W0087']);
console.log('Validated four raw sources, 240 unique tasks and 3,360 prompts.');

const wb = Workbook.create();
const sheetNames = ['Solution', 'Campaigns', 'Mix', 'Workflow', 'Daily Usage', 'Tasks', 'Prompt Totals', 'Priced Usage', 'Raw Work Log', 'Raw AI Usage', 'Model Pricing', 'Campaign Inputs', 'Preparation', 'Data Dictionary'];
const sheets = Object.fromEntries(sheetNames.map(name => [name, wb.worksheets.add(name)]));
const p = { navy: '#16324F', blue: '#245A81', ink: '#202E3B', muted: '#596B7B', line: '#CCD6DF', light: '#EEF3F7', good: '#23784D', bad: '#AC3232', input: '#2154A0', link: '#23784D' };
const usd = '"$"#,##0.00;[Red]("$"#,##0.00);"$"0.00';
const costPrecision = '"$"0.000000;[Red]("$"0.000000);"$"0.000000';
const dec = '#,##0.00;[Red](#,##0.00);0.00';
const pct = '0.00%;[Red](0.00%);0.00%';
const col = i => { let s = ''; for (let n = i + 1; n > 0; n = Math.floor((n - 1) / 26)) s = String.fromCharCode(65 + (n - 1) % 26) + s; return s; };
const schemas = {};
const idx = (sheet, header) => schemas[sheet].headers.indexOf(header);
const cell = (sheet, header, row) => `${col(idx(sheet, header))}${row}`;
const rng = (sheet, header) => `'${sheet}'!$${col(idx(sheet, header))}$7:$${col(idx(sheet, header))}$${schemas[sheet].last}`;
const campaignLookup = (header, id) => `=INDEX(${rng('Campaigns', header)},MATCH("${id}",${rng('Campaigns', 'campaign_id')},0))`;
function base(sheet, range) {
  sheet.showGridLines = false;
  sheet.getRange(range).format = { font: { name: 'Arial', size: 11, color: p.ink }, rowHeight: 23, verticalAlignment: 'center', wrapText: false };
}
function title(sheet, address, text) { sheet.getRange(address).values = [[text]]; sheet.getRange(address).format.font = { name: 'Arial', size: 16, bold: true, color: p.navy }; sheet.getRange(address).format.rowHeight = 29; }
function heading(sheet, address) { sheet.getRange(address).format = { fill: p.navy, font: { name: 'Arial', size: 11, bold: true, color: '#FFFFFF' }, horizontalAlignment: 'center', verticalAlignment: 'center', wrapText: true, rowHeight: 44, borders: { insideVertical: { style: 'thin', color: '#FFFFFF' } } }; }
function emphasis(sheet, address) { sheet.getRange(address).format.fill = p.light; sheet.getRange(address).format.font.bold = true; sheet.getRange(address).format.borders = { top: { style: 'thin', color: p.line } }; }
function signed(sheet, address) { sheet.getRange(address).conditionalFormats.add('cellIs', { operator: 'lessThan', formula: 0, format: { font: { color: p.bad } } }); sheet.getRange(address).conditionalFormats.add('cellIs', { operator: 'greaterThan', formula: 0, format: { font: { color: p.good } } }); }
function section(sheet, address, text) { sheet.getRange(address).values = [[text]]; sheet.getRange(address).format.font = { name: 'Arial', size: 11, bold: true, color: p.navy }; sheet.getRange(address).format.rowHeight = 28; }
function formatMetric(header) {
  if (dates.has(header)) return 'yyyy-mm-dd';
  if (['ai_roi', 'rework_share', 'correction_share'].includes(header)) return pct;
  if (header.endsWith('_usd')) return usd;
  if (header.includes('hours') || header.includes('_per_task') || header.endsWith('_per_million')) return dec;
  return '#,##0';
}
function table(name, headers, rows, description, notes = '', tableName = name.replaceAll(' ', '')) {
  const sheet = sheets[name], last = rows.length + 6, lastCol = col(headers.length - 1);
  schemas[name] = { headers, last, rows: rows.length };
  base(sheet, `A1:${lastCol}${Math.max(last, 7)}`);
  title(sheet, 'A2', description);
  sheet.getRange('A4').values = [[notes]]; sheet.getRange('A4').format.font.color = p.muted;
  sheet.getRangeByIndexes(5, 0, 1, headers.length).values = [headers];
  if (rows.length) sheet.getRangeByIndexes(6, 0, rows.length, headers.length).values = rows.map(row => [...row, ...Array(headers.length - row.length).fill(null)]);
  // Aggregate rows stay outside the sortable campaign detail table.
  const tableLast = name === 'Campaigns' ? 10 : last;
  const tbl = sheet.tables.add(`A6:${lastCol}${tableLast}`, true, tableName); tbl.style = 'TableStyleMedium2'; tbl.showFilterButton = true; tbl.showTotals = false;
  heading(sheet, `A6:${lastCol}6`);
  for (let i = 0; i < headers.length; i++) {
    const width = ['task_type', 'dimension'].includes(headers[i]) ? 30 : ['department', 'group', 'employee', 'campaign_name'].includes(headers[i]) ? 24 : headers[i].length > 25 ? 23 : 18;
    sheet.getRange(`${col(i)}1:${col(i)}${last}`).format.columnWidth = width;
    sheet.getRange(`${col(i)}7:${col(i)}${last}`).setNumberFormat(formatMetric(headers[i]));
  }
  sheet.freezePanes.freezeRows(6); sheet.freezePanes.freezeColumns(Math.min(2, headers.length));
  return sheet;
}
function formulas(name, header, fn) {
  const sheet = sheets[name], column = col(idx(name, header)), last = schemas[name].last;
  sheet.getRange(`${column}7:${column}${last}`).formulas = Array.from({ length: last - 6 }, (_, i) => [fn(i + 7)]);
  sheet.getRange(`${column}7:${column}${last}`).format.font.color = fn(7).includes('!') ? p.link : p.ink;
}
function sourceSheet(name, sourceName, description) {
  const source = sources[sourceName];
  const sheet = table(name, source.headers, source.rows, description, 'Original source values are retained. Dates and numeric fields are typed for Excel.');
  sheet.getRange('A3').values = [[`Source: ${sourceBase}${sourceFolder}${sourceName}.csv`]];
  sheet.getRange('A3').format.font.color = p.muted;
  for (let i = 0; i < source.headers.length; i++) if (numeric.has(source.headers[i])) sheet.getRange(`${col(i)}7:${col(i)}${schemas[name].last}`).format.font.color = p.input;
}
sourceSheet('Raw Work Log', 'work_log', 'Original task records');
sourceSheet('Raw AI Usage', 'ai_usage', 'Original prompt records');
sourceSheet('Model Pricing', 'model_pricing', 'Fixed fictional model prices');
sourceSheet('Campaign Inputs', 'campaigns', 'Whole campaign financial inputs');

const solution = sheets.Solution;
base(solution, 'A1:M88'); solution.tabColor = p.navy;
solution.getRange('A1:A88').format.columnWidth = 3;
solution.getRange('B1:B88').format.columnWidth = 30;
solution.getRange('C1:F88').format.columnWidth = 16;
solution.getRange('G1:G88').format.columnWidth = 3;
solution.getRange('H1:M88').format.columnWidth = 11;
title(solution, 'B2', 'Portfolio Project worked solution');
solution.getRange('B3').values = [['Marketing R Us (MRU). September 2026. Fictional teaching data.']];
solution.getRange('B4:M4').format.borders = { bottom: { style: 'thin', color: p.line } };
solution.getRange('B5:C5').values = [['USD per staff hour', 50]]; solution.getRange('C5').setNumberFormat(usd);
solution.getRange('C5').format.fill = '#FFF1C9'; solution.getRange('C5').format.font.color = p.input;
solution.getRange('E5').values = [['Editable assumption. Reference answers use $50.']];
solution.getRange('C5').dataValidation = { rule: { type: 'decimal', operator: 'greaterThanOrEqual', formula1: 0 } };

const pricedHeaders = [...sources.ai_usage.headers, 'input_rate_usd_per_million', 'output_rate_usd_per_million', 'total_tokens', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd'];
table('Priced Usage', pricedHeaders, sources.ai_usage.unique, 'Prompt pricing', 'One row per prompt. Costs retain full precision. usage_date is the spending date.');
console.log('Created all original sources and the prepared prompt table.');
for (const [header, sourceHeader] of [['input_rate_usd_per_million', 'input_rate_usd_per_million'], ['output_rate_usd_per_million', 'output_rate_usd_per_million']]) formulas('Priced Usage', header, r => `=INDEX(${rng('Model Pricing', sourceHeader)},MATCH(F${r},${rng('Model Pricing', 'model')},0))`);
for (const [header, fn] of Object.entries({ total_tokens: r => `=G${r}+H${r}`, input_cost_usd: r => `=G${r}*J${r}/1000000`, output_cost_usd: r => `=H${r}*K${r}/1000000`, ai_cost_usd: r => `=SUM(M${r}:N${r})` })) formulas('Priced Usage', header, fn);
sheets['Priced Usage'].getRange(`M7:O${schemas['Priced Usage'].last}`).setNumberFormat(costPrecision);
console.log('Priced prompt formulas populated.');
const promptHeaders = ['work_item_id', 'campaign_id', 'product', 'model', 'input_tokens', 'output_tokens', 'total_tokens', 'prompt_count', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd', 'first_attempt_prompts', 'followup_prompts', 'correction_prompts'];
const promptRows = cleaned.map(task => { const first = promptGroups.get(task[0])[0]; return [task[0], task[2], first[4], first[5]]; });
table('Prompt Totals', promptHeaders, promptRows, 'Prompt totals by task', 'Prompt rows are aggregated here before any task hours are joined. Each task has one model and one product.');
for (const header of ['input_tokens', 'output_tokens', 'total_tokens', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd']) formulas('Prompt Totals', header, r => `=SUMIFS(${rng('Priced Usage', header)},${rng('Priced Usage', 'work_item_id')},$A${r})`);
formulas('Prompt Totals', 'prompt_count', r => `=COUNTIFS(${rng('Priced Usage', 'work_item_id')},$A${r})`);
for (const [header, reason] of [['first_attempt_prompts', 'First attempt'], ['followup_prompts', 'Followup'], ['correction_prompts', 'Correction']]) formulas('Prompt Totals', header, r => `=COUNTIFS(${rng('Priced Usage', 'work_item_id')},$A${r},${rng('Priced Usage', 'prompt_reason')},"${reason}")`);
const taskHeaders = [...work.headers, 'product', 'model', 'input_tokens', 'output_tokens', 'total_tokens', 'prompt_count', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd', 'first_attempt_prompts', 'followup_prompts', 'correction_prompts', 'hours_saved', 'time_value_usd', 'net_ai_value_usd'];
table('Tasks', taskHeaders, cleaned, 'Clean tasks and value calculations', 'One row per completed task. Rework is already included in actual hours. No campaign revenue is allocated to tasks.');
for (const header of taskHeaders.slice(12, 24)) formulas('Tasks', header, r => `=INDEX(${rng('Prompt Totals', header)},MATCH($A${r},${rng('Prompt Totals', 'work_item_id')},0))`);
formulas('Tasks', 'hours_saved', r => `=G${r}-H${r}`);
formulas('Tasks', 'time_value_usd', r => `=Y${r}*'Solution'!$C$5`);
formulas('Tasks', 'net_ai_value_usd', r => `=Z${r}-U${r}`);
sheets.Tasks.getRange('G7:I246').format.font.color = p.input;
signed(sheets.Tasks, 'Y7:AA246'); sheets.Tasks.tabColor = '#5C7F9D';
console.log('Built prompt pricing, task aggregates and cleaned task formulas.');

const summaryMetrics = ['tasks', 'input_tokens', 'output_tokens', 'total_tokens', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd', 'prompt_count', 'cost_per_prompt_usd', 'baseline_hours', 'actual_hours', 'hours_saved', 'time_value_usd', 'net_ai_value_usd', 'ai_roi', 'rework_hours', 'rework_share', 'correction_prompts', 'correction_share', 'template_tasks', 'changed_brief_tasks', 'positive_net_value_tasks', 'negative_net_value_tasks'];
function aggregateFormula(name, metric, r, criteria) {
  const args = criteria.flatMap(([header, value]) => [rng('Tasks', header), value]).join(',');
  const c = header => cell(name, header, r);
  const ratio = (num, den) => `=IF(${c(den)}=0,"N/A",${c(num)}/${c(den)})`;
  if (metric === 'tasks') return `=COUNTIFS(${args})`;
  if (metric === 'cost_per_prompt_usd') return ratio('ai_cost_usd', 'prompt_count');
  if (metric === 'ai_roi') return ratio('net_ai_value_usd', 'ai_cost_usd');
  if (metric === 'rework_share') return ratio('rework_hours', 'actual_hours');
  if (metric === 'correction_share') return ratio('correction_prompts', 'prompt_count');
  if (metric === 'template_tasks') return `=COUNTIFS(${args},${rng('Tasks', 'prompt_template_used')},"Yes")`;
  if (metric === 'changed_brief_tasks') return `=COUNTIFS(${args},${rng('Tasks', 'brief_changed')},"Yes")`;
  if (metric === 'positive_net_value_tasks' || metric === 'negative_net_value_tasks') return `=COUNTIFS(${args},${rng('Tasks', 'net_ai_value_usd')},"${metric.startsWith('positive') ? '>' : '<'}0")`;
  return `=SUMIFS(${rng('Tasks', metric)},${args})`;
}
const campaignHeaders = ['campaign_id', 'campaign_name', ...summaryMetrics, 'campaign_revenue_usd', 'other_campaign_cost_usd', 'actual_staff_cost_usd', 'campaign_result_usd', 'net_ai_value_lower20_usd', 'net_ai_value_higher20_usd'];
table('Campaigns', campaignHeaders, [...sources.campaigns.unique.map(row => row.slice(0, 2)), ['ALL', 'All four campaigns'], ['FOCAL', 'Campaigns 1 and 2']], 'Campaign performance and financial results', 'ALL includes four campaigns. FOCAL includes C001 and C002. Financial results always cover complete campaigns.');
for (let r = 7; r <= 10; r++) {
  const rowFormulas = summaryMetrics.map(metric => aggregateFormula('Campaigns', metric, r, [['campaign_id', `$A${r}`]]));
  sheets.Campaigns.getRange(`C${r}:Y${r}`).formulas = [rowFormulas];
  for (const header of ['campaign_revenue_usd', 'other_campaign_cost_usd']) sheets.Campaigns.getRange(cell('Campaigns', header, r)).formulas = [[`=INDEX(${rng('Campaign Inputs', header)},MATCH($A${r},${rng('Campaign Inputs', 'campaign_id')},0))`]];
}
for (const r of [11, 12]) for (const header of [...summaryMetrics, 'campaign_revenue_usd', 'other_campaign_cost_usd']) {
  const c = col(idx('Campaigns', header)), end = r === 11 ? 10 : 8;
  const ratioFields = { ai_roi: ['net_ai_value_usd', 'ai_cost_usd'], rework_share: ['rework_hours', 'actual_hours'], correction_share: ['correction_prompts', 'prompt_count'], cost_per_prompt_usd: ['ai_cost_usd', 'prompt_count'] };
  let formula = r === 11 ? `=SUM(${c}7:${c}${end})` : `=SUMIFS(${c}$7:${c}$10,$A$7:$A$10,"C001")+SUMIFS(${c}$7:${c}$10,$A$7:$A$10,"C002")`;
  if (ratioFields[header]) { const [num, den] = ratioFields[header].map(h => cell('Campaigns', h, r)); formula = `=IF(${den}=0,"N/A",${num}/${den})`; }
  sheets.Campaigns.getRange(`${c}${r}`).formulas = [[formula]];
}
formulas('Campaigns', 'actual_staff_cost_usd', r => `=${cell('Campaigns', 'actual_hours', r)}*'Solution'!$C$5`);
formulas('Campaigns', 'campaign_result_usd', r => `=${cell('Campaigns', 'campaign_revenue_usd', r)}-${cell('Campaigns', 'other_campaign_cost_usd', r)}-${cell('Campaigns', 'actual_staff_cost_usd', r)}-${cell('Campaigns', 'ai_cost_usd', r)}`);
for (const [header, factor] of [['net_ai_value_lower20_usd', 0.8], ['net_ai_value_higher20_usd', 1.2]]) formulas('Campaigns', header, r => `=(${cell('Campaigns', 'baseline_hours', r)}*${factor}-${cell('Campaigns', 'actual_hours', r)})*'Solution'!$C$5-${cell('Campaigns', 'ai_cost_usd', r)}`);
emphasis(sheets.Campaigns, 'A11:AE12'); sheets.Campaigns.tabColor = p.blue;
const mixRows = [];
for (const campaign of campaignsById.keys()) for (const dimension of ['product', 'model', 'department']) {
  const column = taskHeaders.indexOf(dimension);
  const groups = [...new Set(cleaned.filter(t => t[2] === campaign).map(t => dimension === 'department' ? t[3] : promptGroups.get(t[0])[0][dimension === 'product' ? 4 : 5]))].sort();
  for (const group of groups) mixRows.push([campaign, dimension, group]);
}
table('Mix', ['campaign_id', 'dimension', 'group', ...summaryMetrics], mixRows, 'Product, model and department comparisons', 'Filter campaign_id to C001 and C002 for the focal comparison. Rows from different dimensions overlap and must not be added together.');
for (let i = 0; i < mixRows.length; i++) {
  const r = i + 7, dimension = mixRows[i][1];
  sheets.Mix.getRange(`D${r}:Z${r}`).formulas = [summaryMetrics.map(metric => aggregateFormula('Mix', metric, r, [['campaign_id', `$A${r}`], [dimension, `$C${r}`]]))];
}
const workflowRows = [];
for (const campaign of campaignsById.keys()) {
  const campaignTasks = cleaned.filter(t => t[2] === campaign);
  for (const type of ['All task types', ...[...new Set(campaignTasks.map(t => t[5]))].sort()]) {
    const groupTasks = campaignTasks.filter(t => type === 'All task types' || t[5] === type);
    for (const [dimension, index] of [['prompt_template_used', 11], ['brief_changed', 10]]) for (const flag of ['No', 'Yes']) if (groupTasks.some(t => t[index] === flag)) workflowRows.push([campaign, type, dimension, flag]);
  }
}
table('Workflow', ['campaign_id', 'task_type', 'dimension', 'flag', ...summaryMetrics, 'corrections_per_task', 'ai_cost_per_task_usd', 'hours_saved_per_task'], workflowRows, 'Comparable workflow cohorts', 'Compare Yes and No within the same campaign and task type. Groups overlap. Small observed groups do not establish causation.');
for (let i = 0; i < workflowRows.length; i++) {
  const r = i + 7, [, type, dimension] = workflowRows[i];
  const criteria = [['campaign_id', `$A${r}`], [dimension, `$D${r}`]];
  if (type !== 'All task types') criteria.push(['task_type', `$B${r}`]);
  sheets.Workflow.getRange(`E${r}:AA${r}`).formulas = [summaryMetrics.map(metric => aggregateFormula('Workflow', metric, r, criteria))];
}
for (const [header, numerator] of [['corrections_per_task', 'correction_prompts'], ['ai_cost_per_task_usd', 'ai_cost_usd'], ['hours_saved_per_task', 'hours_saved']]) formulas('Workflow', header, r => `=IF(${cell('Workflow', 'tasks', r)}=0,"N/A",${cell('Workflow', numerator, r)}/${cell('Workflow', 'tasks', r)})`);
const dailyKeys = [...new Set(sources.ai_usage.unique.map(row => JSON.stringify([row[1], row[3]])))].map(JSON.parse).sort((a, b) => a[0] - b[0] || a[1].localeCompare(b[1]));
table('Daily Usage', ['usage_date', 'campaign_id', 'input_tokens', 'output_tokens', 'total_tokens', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd', 'prompt_count', 'correction_prompts', 'correction_share'], dailyKeys, 'Daily prompt usage and spending', 'Each row is one observed usage date and campaign. Task hours and campaign revenue are not assigned to prompt dates.');
for (const header of ['input_tokens', 'output_tokens', 'total_tokens', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd']) formulas('Daily Usage', header, r => `=SUMIFS(${rng('Priced Usage', header)},${rng('Priced Usage', 'usage_date')},$A${r},${rng('Priced Usage', 'campaign_id')},$B${r})`);
formulas('Daily Usage', 'prompt_count', r => `=COUNTIFS(${rng('Priced Usage', 'usage_date')},$A${r},${rng('Priced Usage', 'campaign_id')},$B${r})`);
formulas('Daily Usage', 'correction_prompts', r => `=COUNTIFS(${rng('Priced Usage', 'usage_date')},$A${r},${rng('Priced Usage', 'campaign_id')},$B${r},${rng('Priced Usage', 'prompt_reason')},"Correction")`);
formulas('Daily Usage', 'correction_share', r => `=IF(I${r}=0,"N/A",J${r}/I${r})`);
console.log(`Built campaign, mix, ${workflowRows.length} workflow and ${dailyKeys.length} daily groups.`);

section(solution, 'B7', 'Company overview and focal comparison');
solution.getRange('B8:D8').values = [['Metric', 'All campaigns', 'C001 and C002']]; heading(solution, 'B8:D8');
for (const [r, label, header, format] of [[9, 'AI spending', 'ai_cost_usd', usd], [10, 'Hours saved', 'hours_saved', dec], [11, 'Net AI value', 'net_ai_value_usd', usd], [12, 'AI ROI', 'ai_roi', pct], [13, 'Campaign result', 'campaign_result_usd', usd]]) {
  solution.getRange(`B${r}`).values = [[label]];
  solution.getRange(`C${r}:D${r}`).formulas = [['ALL', 'FOCAL'].map(id => campaignLookup(header, id))]; solution.getRange(`C${r}:D${r}`).setNumberFormat(format);
}
emphasis(solution, 'B11:D11'); signed(solution, 'C10:D13');
section(solution, 'B16', 'Q1. Campaign costs and estimated value');
solution.getRange('B17:F17').values = [['Campaign', 'AI cost', 'Hours saved', 'Net AI value', 'AI ROI']]; heading(solution, 'B17:F17');
for (let i = 0; i < 4; i++) {
  const r = 18 + i, id = sources.campaigns.unique[i][0];
  solution.getRange(`B${r}:F${r}`).formulas = [[...['campaign_name', 'ai_cost_usd', 'hours_saved', 'net_ai_value_usd', 'ai_roi'].map(h => campaignLookup(h, id))]];
}
solution.getRange('C18:C21').setNumberFormat(usd); solution.getRange('D18:D21').setNumberFormat(dec); solution.getRange('E18:E21').setNumberFormat(usd); solution.getRange('F18:F21').setNumberFormat(pct); signed(solution, 'D18:F21');
section(solution, 'B24', 'Q4. Whole campaign financial results');
solution.getRange('B25:F25').values = [['Campaign', 'Revenue', 'Other spending', 'Labor value', 'Profit or loss']]; heading(solution, 'B25:F25');
for (let i = 0; i < 4; i++) solution.getRange(`B${26 + i}:F${26 + i}`).formulas = [[...['campaign_name', 'campaign_revenue_usd', 'other_campaign_cost_usd', 'actual_staff_cost_usd', 'campaign_result_usd'].map(h => campaignLookup(h, sources.campaigns.unique[i][0]))]];
solution.getRange('C26:F29').setNumberFormat(usd); signed(solution, 'F26:F29');
solution.getRange('B30').values = [['Profit also deducts the AI fees shown above. Net AI value measures a different comparison.']];
section(solution, 'B33', 'Q5. Sensitivity to the estimated baseline');
solution.getRange('B34:E34').values = [['Campaign', 'Baseline 20% lower', 'Stated baseline', 'Baseline 20% higher']]; heading(solution, 'B34:E34');
for (let i = 0; i < 4; i++) solution.getRange(`B${35 + i}:E${35 + i}`).formulas = [[...['campaign_name', 'net_ai_value_lower20_usd', 'net_ai_value_usd', 'net_ai_value_higher20_usd'].map(h => campaignLookup(h, sources.campaigns.unique[i][0]))]];
solution.getRange('C35:E38').setNumberFormat(usd); signed(solution, 'C35:E38');
solution.getRange('B40').values = [['At the supplied $50 rate, C001 remains positive and C002 remains negative in all three cases.']];
solution.getRange('B41').values = [['C003 and C004 change sign. At the lower baseline, company net AI value falls to a $6,380 loss.']];
solution.getRange('B42').values = [['Whole campaign profit does not use baseline hours and remains unchanged by this test.']];

section(solution, 'B44', 'Q2. Why do the focal campaigns spend differently?');
solution.getRange('B45:D45').values = [['Metric', 'Campaign 1', 'Campaign 2']]; heading(solution, 'B45:D45');
for (const [r, label, dimension, group, header, format] of [[46, 'Pro model tasks', 'model', 'Pro', 'tasks', '#,##0'], [47, 'Pro model tokens', 'model', 'Pro', 'total_tokens', '#,##0'], [48, 'Pro model spending', 'model', 'Pro', 'ai_cost_usd', usd], [49, 'Lite model spending', 'model', 'Lite', 'ai_cost_usd', usd]]) {
  solution.getRange(`B${r}`).values = [[label]]; solution.getRange(`C${r}:D${r}`).formulas = [['C001', 'C002'].map(campaign => `=SUMIFS(${rng('Mix', header)},${rng('Mix', 'campaign_id')},"${campaign}",${rng('Mix', 'dimension')},"${dimension}",${rng('Mix', 'group')},"${group}")`)]; solution.getRange(`C${r}:D${r}`).setNumberFormat(format);
}
solution.getRange('F46').values = [['C002 used twice as many prompts and more Pro tokens.']];
solution.getRange('F47').values = [['Lite spending was equal. Pro spending explains the $900 gap.']];
solution.getRange('F48').values = [['All four products show negative net value in C002.']];
solution.getRange('F49').values = [['Mix provides every product, model and department result.']];

section(solution, 'B52', 'Q3. Similar task types and workflow observations');
solution.getRange('B53').values = [['C002, Draft email sequence. Template and changed brief groups overlap.']];
solution.getRange('B54:E54').values = [['Observation', 'Tasks', 'Rework share', 'Corrections per task']]; heading(solution, 'B54:E54');
for (const [i, dimension, flag, label] of [[0, 'prompt_template_used', 'Yes', 'Template used'], [1, 'prompt_template_used', 'No', 'No template'], [2, 'brief_changed', 'Yes', 'Brief changed'], [3, 'brief_changed', 'No', 'Brief unchanged']]) {
  const r = 55 + i;
  assert.ok(workflowRows.some(row => row[0] === 'C002' && row[1] === 'Draft email sequence' && row[2] === dimension && row[3] === flag));
  solution.getRange(`B${r}`).values = [[label]]; solution.getRange(`C${r}:E${r}`).formulas = [[...['tasks', 'rework_share', 'corrections_per_task'].map(header => `=SUMIFS(${rng('Workflow', header)},${rng('Workflow', 'campaign_id')},"C002",${rng('Workflow', 'task_type')},"Draft email sequence",${rng('Workflow', 'dimension')},"${dimension}",${rng('Workflow', 'flag')},"${flag}")`)]];
}
solution.getRange('C55:C58').setNumberFormat('#,##0'); solution.getRange('D55:D58').setNumberFormat(pct); solution.getRange('E55:E58').setNumberFormat(dec);
solution.getRange('G55').values = [['Only five tasks are represented in this example.']];
solution.getRange('G56').values = [['Template use coincides with less rework and fewer corrections.']];
solution.getRange('G57').values = [['Changed briefs coincide with more rework and corrections.']];
solution.getRange('G58').values = [['These associations do not isolate a causal effect.']];

section(solution, 'B61', 'Q6. Recommendations from the supplied case');
const narrative = [
  '1. Retain the successful Campaign 1 workflow and document its preparation and review process.',
  'It saves 100 estimated hours and returns $4,500 after AI fees. Recheck acceptable quality and actual',
  'effort on comparable future tasks. The no AI baseline is an estimate, not a measured counterfactual.',
  '',
  '2. Narrow Campaign 2 use while investigating changed briefs, corrections and model selection.',
  'Its 1,200 prompts cost $1,400, yet actual effort exceeds the baseline by 70 hours. Review Pro usage',
  'and establish a brief approval checkpoint. Model prices and repeat prompts both affect spending.',
  '',
  '3. Test templates within comparable task types and track rework, corrections and net value.',
  'The five task email example supports investigation, but its small overlapping groups cannot prove',
  'that templates caused the difference. Compare future cohorts before expanding the practice.',
  '',
  'Results above are reference answers for the supplied data and $50 hourly assumption. Written findings',
  'need review after inputs change. Estimated time value represents staff capacity, not payroll cash savings.',
];
solution.getRange(`B63:B${62 + narrative.length}`).values = narrative.map(text => [text]);
section(solution, 'B79', 'Reading and using the workbook');
solution.getRange('B80').values = [['Campaigns, Mix and Workflow contain full grouped answers. Daily Usage retains prompt dates.']];
solution.getRange('B81').values = [['Tasks is the complete cleaned table. Prompt Totals and Priced Usage expose the calculations behind it.']];
solution.getRange('B82').values = [['Original input records, the ten preparation steps and field definitions are retained on the remaining tabs.']];
solution.getRange('B83').values = [['Existing numeric input edits update formulas and charts. New records or changed keys require a rebuild.']];
solution.getRange('B84').values = [['Filter table rows to inspect records. Summary formulas still use their labeled complete groups.']];
solution.getRange('B80:B84').format.font.color = p.muted;
const valueChart = solution.charts.add('bar', [sheets.Campaigns.getRange('B6:B10'), sheets.Campaigns.getRange('P6:P10')]);
valueChart.title = 'Net AI value after fees (USD)'; valueChart.hasLegend = false; valueChart.setPosition('H8', 'M22'); valueChart.series.items[0].fill = p.blue;
base(sheets.Campaigns, 'A15:C19');
sheets.Campaigns.getRange('A15:C15').values = [['Campaign', 'Estimated hours', 'Actual hours']]; heading(sheets.Campaigns, 'A15:C15');
for (let i = 0; i < 4; i++) sheets.Campaigns.getRange(`A${16 + i}:C${16 + i}`).formulas = [[`=INDEX($B$7:$B$10,MATCH("C00${i + 1}",$A$7:$A$10,0))`, `=INDEX($L$7:$L$10,MATCH("C00${i + 1}",$A$7:$A$10,0))`, `=INDEX($M$7:$M$10,MATCH("C00${i + 1}",$A$7:$A$10,0))`]];
sheets.Campaigns.getRange('B16:C19').setNumberFormat(dec);
const hoursChart = solution.charts.add('bar', sheets.Campaigns.getRange('A15:C19'));
hoursChart.title = 'Estimated and actual hours'; hoursChart.setPosition('H25', 'M39'); hoursChart.legend = { position: 'top', textStyle: { typeface: 'Arial', fontSize: 13 } }; hoursChart.series.items[0].fill = '#A8BAC9'; hoursChart.series.items[1].fill = p.blue;
for (const chart of [valueChart, hoursChart]) {
  chart.titleTextStyle.typeface = 'Arial'; chart.titleTextStyle.fontSize = 14;
  chart.xAxis = { axisType: 'textAxis', tickLabelPosition: 'low', majorGridlines: null, textStyle: { typeface: 'Arial', fontSize: 13 } };
  chart.yAxis = { numberFormatCode: chart === valueChart ? '$#,##0;($#,##0)' : '0', numberFormatSourceLinked: false, textStyle: { typeface: 'Arial', fontSize: 13 } };
}

const preparation = sheets.Preparation;
base(preparation, 'A1:F57'); title(preparation, 'A2', 'Preparation and reconciliation');
preparation.getRange('A3').values = [[`Method: ${sourceBase}QUESTIONS/TRACKS/portfolio-project/README.md`]];
preparation.getRange('A4').values = [['The ten required preparation steps are completed below. These checks do not feed business calculations.']];
for (const [column, width] of [['A', 8], ['B', 41], ['C', 20], ['D', 20], ['E', 20], ['F', 50]]) preparation.getRange(`${column}1:${column}57`).format.columnWidth = width;
preparation.getRange('A6:C6').values = [['Step', 'Preparation completed', 'Evidence']]; heading(preparation, 'A6:C6');
const steps = [
  [1, 'Preserved raw data and typed fields', 'Raw Work Log has 242 rows. Raw AI Usage has 3,360. Model Pricing has 2. Campaign Inputs has 4. Dates are sortable Excel dates. Tokens are nonnegative integers. Hours and rates are numbers. Flags are Yes or No.'],
  [2, 'Removed exact repeated IDs and normalized departments', 'Removed W0018 and W0087 repeats, retaining 240 tasks. All four source keys are unique after deduplication. Ten retained task department labels were trimmed and capitalized. Conflicting duplicates fail the build.'],
  [3, 'Validated relationships and task model/product consistency', 'Every prompt has one task and an agreeing campaign. Each task has one product, one model and one First attempt. Every model has exactly one price. Prompt dates do not follow task completion.'],
  [4, 'Priced each prompt from the model table', 'Priced Usage uses exact model lookups. Separate input and output costs are calculated at full precision, without rounding prompts to cents.'],
  [5, 'Aggregated prompts before joining task hours', 'Prompt Totals has one row per task. SUMIFS and COUNTIFS calculate tokens, separate costs, prompt counts and reasons. Hours are absent from this table.'],
  [6, 'Joined the cleaned task table and calculated value', 'Tasks combines one prompt aggregate with one cleaned task. Hours saved are baseline less actual hours. Time value uses Solution C5. Net AI value deducts AI fees. Rework is already included in actual hours.'],
  [7, 'Grouped complete tasks and calculated ratios from totals', 'Campaigns and Mix group by campaign, product, model and department. Workflow groups comparable task types and observations. ROI, cost per prompt and shares divide summed components. Zero denominators display N/A.'],
  [8, 'Joined finances after aggregation to campaign', 'Campaigns includes one financial row per campaign. Profit deducts other spending, actual labor value and AI fees. Revenue is never repeated on task or prompt records.'],
  [9, 'Retained prompt usage dates for daily spending', 'Daily Usage groups Priced Usage by usage_date and campaign. No full task hours, revenue or whole campaign profit is assigned to a prompt date.'],
  [10, 'Reconciled totals and tested baseline sensitivity', 'The checks below compare workbook totals with independent source calculations. Campaigns shows baseline 20% lower and higher. Solution answers all six analytical questions and provides two editable charts.'],
];
preparation.getRange('A7:C16').values = steps;
preparation.getRange('C1:C57').format.columnWidth = 100;
preparation.getRange('A7:C16').format.wrapText = true; preparation.getRange('A7:C16').format.verticalAlignment = 'top'; preparation.getRange('A7:C16').format.rowHeight = 65;
const independentlyPriced = sources.ai_usage.unique.map(row => { const price = pricesByModel.get(row[5]); return { row, input: row[6] * price[1] / 1e6, output: row[7] * price[2] / 1e6 }; });
const sum = (rows, fn) => rows.reduce((total, row) => total + fn(row), 0);
const controls = [
  ['Unique tasks', `=COUNTA(${rng('Tasks', 'work_item_id')})`, cleaned.length],
  ['Priced prompts', `=COUNTA(${rng('Priced Usage', 'usage_id')})`, sources.ai_usage.unique.length],
  ['Input tokens', `=SUM(${rng('Priced Usage', 'input_tokens')})`, sum(independentlyPriced, x => x.row[6])],
  ['Output tokens', `=SUM(${rng('Priced Usage', 'output_tokens')})`, sum(independentlyPriced, x => x.row[7])],
  ['Input cost USD', `=SUM(${rng('Priced Usage', 'input_cost_usd')})`, sum(independentlyPriced, x => x.input)],
  ['Output cost USD', `=SUM(${rng('Priced Usage', 'output_cost_usd')})`, sum(independentlyPriced, x => x.output)],
  ['AI cost USD', `=SUM(${rng('Tasks', 'ai_cost_usd')})`, sum(independentlyPriced, x => x.input + x.output)],
  ['Baseline hours', `=SUM(${rng('Tasks', 'baseline_hours')})`, sum(cleaned, row => row[6])],
  ['Actual hours', `=SUM(${rng('Tasks', 'actual_hours')})`, sum(cleaned, row => row[7])],
  ['Hours saved', `=SUM(${rng('Tasks', 'hours_saved')})`, sum(cleaned, row => row[6] - row[7])],
  ['Net AI value USD at $50/hour', `='Campaigns'!P11`, 2820],
  ['Campaign result USD at $50/hour', `='Campaigns'!AC11`, 12820],
  ['Task / prompt AI cost difference', `=SUM(${rng('Tasks', 'ai_cost_usd')})-SUM(${rng('Priced Usage', 'ai_cost_usd')})`, 0],
  ['Daily / prompt AI cost difference', `=SUM(${rng('Daily Usage', 'ai_cost_usd')})-SUM(${rng('Priced Usage', 'ai_cost_usd')})`, 0],
  ['Campaign / task AI cost difference', `='Campaigns'!I11-SUM(${rng('Tasks', 'ai_cost_usd')})`, 0],
  ['Prompt counts / original records', `=SUM(${rng('Prompt Totals', 'prompt_count')})-COUNTA(${rng('Raw AI Usage', 'usage_id')})`, 0],
  ['First attempts / unique tasks', `=SUM(${rng('Prompt Totals', 'first_attempt_prompts')})-COUNTA(${rng('Tasks', 'work_item_id')})`, 0],
];
section(preparation, 'B19', 'Reconciliation against the supplied source case');
preparation.getRange('B20:E20').values = [['Check', 'Workbook', 'Source control', 'Difference']]; heading(preparation, 'B20:E20');
// Column C is wide for the step narrative; the check results are aligned left so each is easy to find.
for (let i = 0; i < controls.length; i++) { const r = 21 + i, [label, formula, expected] = controls[i]; preparation.getRange(`B${r}`).values = [[label]]; preparation.getRange(`C${r}`).formulas = [[r >= 33 && r <= 35 ? `=ROUND(${formula.slice(1)},6)` : formula]]; preparation.getRange(`D${r}`).values = [[expected]]; preparation.getRange(`E${r}`).formulas = [[`=ROUND(C${r}-D${r},6)`]]; }
preparation.getRange('C21:E37').setNumberFormat('#,##0.00;(#,##0.00);0.00'); preparation.getRange('C21:D24').setNumberFormat('#,##0'); preparation.getRange('C21:C37').format.horizontalAlignment = 'left';
preparation.getRange('E21:E37').conditionalFormats.add('cellIs', { operator: 'notBetween', formula: [-0.000001, 0.000001], format: { fill: '#FCE8E6', font: { color: p.bad, bold: true } } });
section(preparation, 'B40', 'Using or refreshing the prepared data');
const refresh = [
  'The source controls above describe the supplied reference case. Differences after deliberate edits are expected.',
  'Tasks contains typed, deduplicated source fields plus live formulas. Original rows remain in Raw Work Log.',
  'Priced Usage contains prepared prompt fields. Original prompt rows remain in Raw AI Usage.',
  'Editing existing task hours, prompt tokens, model rates, campaign finances or Solution C5 recalculates results.',
  'New source rows or changed keys, dates, categories and group membership require rebuilding the workbook.',
  'The builder repeats validation and reconstructs groups. Manual table filters do not change summary scope.',
  'Source: four synthetic CSVs in DATA/TRACKS/portfolio-project. MIT code/text. CC0 1.0 synthetic data.',
  'Hourly assumption source: the Portfolio Project learner brief. Prices are supplied fictional rates, not vendor quotes.',
  'Baseline sensitivity changes baseline hours only. These simple formulas reuse campaign totals and do not forecast.',
  'The written conclusions describe the original case. Review them after changing assumptions or source inputs.',
];
preparation.getRange('B42:B51').values = refresh.map(text => [text]); preparation.getRange('B42:B51').format.font.color = p.muted;
preparation.freezePanes.freezeRows(6); preparation.tabColor = '#9BA8B4';

const dictionaryText = await fs.readFile(path.join(root, sourceFolder, 'DATA_DICTIONARY.md'), 'utf8');
const originalDefinitions = dictionaryText.split(/\r?\n/).filter(line => line.startsWith('|')).slice(2).map(line => line.split('|').slice(1, -1).map(value => value.trim().replaceAll('`', '')));
const sheetMap = { campaigns: 'Campaign Inputs', work_log: 'Raw Work Log', ai_usage: 'Raw AI Usage', model_pricing: 'Model Pricing' };
const definitions = originalDefinitions.map(row => [sheetMap[row[0]], ...row.slice(1)]);
const derivedDefinitions = {
  input_rate_usd_per_million: ['USD per million input tokens', 'Exact model lookup from Model Pricing.'], output_rate_usd_per_million: ['USD per million output tokens', 'Exact model lookup from Model Pricing.'],
  total_tokens: ['Integer, tokens', 'Input tokens plus output tokens for the stated record or group.'], input_cost_usd: ['Decimal, USD', 'Input tokens multiplied by the model input price, divided by one million. Sum prompt costs before reporting.'], output_cost_usd: ['Decimal, USD', 'Output tokens multiplied by the model output price, divided by one million.'], ai_cost_usd: ['Decimal, USD', 'Input cost plus output cost. Values retain full precision before display.'],
  prompt_count: ['Integer, prompts', 'Count of distinct prepared prompt records. Followups and corrections count as separate prompts.'], first_attempt_prompts: ['Integer, prompts', 'Count of prompt records with prompt_reason First attempt.'], followup_prompts: ['Integer, prompts', 'Count of prompt records with prompt_reason Followup.'], correction_prompts: ['Integer, prompts', 'Count of prompt records with prompt_reason Correction.'],
  hours_saved: ['Decimal, hours', 'Baseline hours less actual hours. A negative result means more effort than the no AI estimate.'], time_value_usd: ['Decimal, USD', 'Hours saved multiplied by the hourly value in Solution C5.'], net_ai_value_usd: ['Decimal, USD', 'Time value less AI cost. Estimated staff capacity value rather than payroll cash savings.'], tasks: ['Integer, tasks', 'Count of complete cleaned tasks in this group.'],
  cost_per_prompt_usd: ['Decimal, USD per prompt', 'Total AI cost divided by total prompt count. N/A when no prompts exist.'], ai_roi: ['Fraction, displayed as percent', 'Total net AI value divided by total AI cost. N/A when AI cost is zero. May be below minus 100 percent.'], rework_share: ['Fraction, displayed as percent', 'Total rework hours divided by total actual hours. Rework is already included in actual hours.'], correction_share: ['Fraction, displayed as percent', 'Correction prompt count divided by total prompt count.'],
  template_tasks: ['Integer, tasks', 'Tasks with prompt_template_used Yes in the group.'], changed_brief_tasks: ['Integer, tasks', 'Tasks with brief_changed Yes in the group.'], positive_net_value_tasks: ['Integer, tasks', 'Tasks with net AI value greater than zero.'], negative_net_value_tasks: ['Integer, tasks', 'Tasks with net AI value less than zero.'], actual_staff_cost_usd: ['Decimal, USD', 'Complete campaign actual hours multiplied by Solution C5.'], campaign_result_usd: ['Decimal, USD', 'Campaign revenue less other campaign spending, actual staff value and AI fees. Revenue enters once per campaign.'],
  net_ai_value_lower20_usd: ['Decimal, USD', 'Net AI value with baseline hours multiplied by 0.8. All other inputs remain fixed.'], net_ai_value_higher20_usd: ['Decimal, USD', 'Net AI value with baseline hours multiplied by 1.2. All other inputs remain fixed.'], corrections_per_task: ['Decimal, prompts per task', 'Correction prompt count divided by task count in the same cohort.'], ai_cost_per_task_usd: ['Decimal, USD per task', 'AI spending divided by task count in the same cohort.'], hours_saved_per_task: ['Decimal, hours per task', 'Hours saved divided by task count in the same cohort.'], dimension: ['Text category', 'Field used to group observations. Different dimensions overlap and must not be added together.'], group: ['Text category', 'Selected product, model or department value within the specified dimension.'], flag: ['Text, Yes or No', 'Observed template or changed brief flag for the cohort.'],
};
const originalLookup = new Map(originalDefinitions.map(row => [row[1], row.slice(2)]));
for (const name of ['Priced Usage', 'Prompt Totals', 'Tasks', 'Campaigns', 'Mix', 'Workflow', 'Daily Usage']) for (const header of schemas[name].headers) {
  let definition = derivedDefinitions[header] ?? originalLookup.get(header);
  if (header === 'campaign_id') definition = ['Text identifier', name === 'Campaigns' ? 'Campaign being summarized. ALL includes all four campaigns. FOCAL includes Campaigns 1 and 2. Other rows represent one complete campaign.' : 'Campaign associated with the task, prompt or reported group. The identifier connects to Campaign Inputs.'];
  if (header === 'model') definition = ['Text identifier', 'Fictional model used by the task or prompt. Lite and Pro connect to the model prices in Model Pricing.'];
  if (name === 'Workflow' && header === 'task_type') definition = ['Text', 'Type of completed work in the cohort. All task types summarizes the entire campaign for this observation.'];
  assert.ok(definition, `Missing dictionary definition ${name}.${header}`);
  definitions.push([name, header, definition[0], definition[1]]);
}
table('Data Dictionary', ['worksheet', 'column', 'type_and_units', 'meaning'], definitions, 'Source and prepared field definitions', 'Original input meanings and every prepared column are documented here. Formulas remain visible in their working tables.', 'PortfolioDictionary');
const dictionary = sheets['Data Dictionary'];
for (const [column, width] of [['A', 23], ['B', 39], ['C', 35], ['D', 85]]) dictionary.getRange(`${column}1:${column}${schemas['Data Dictionary'].last}`).format.columnWidth = width;
dictionary.getRange(`A7:D${schemas['Data Dictionary'].last}`).format.wrapText = true;
dictionary.getRange(`A7:D${schemas['Data Dictionary'].last}`).format.verticalAlignment = 'top';
dictionary.getRange(`A7:D${schemas['Data Dictionary'].last}`).format.rowHeight = 46;

const at = (name, address) => sheets[name].getRange(address).values[0][0];
const near = (value, expected, label) => assert.ok(typeof value === 'number' && Math.abs(value - expected) < 0.000001, `${label}: ${value} != ${expected}`);
console.log('Testing live formula recalculation.');
solution.getRange('C5').values = [[60]]; wb.recalculate();
near(at('Campaigns', 'P11'), 4020, 'Hourly value change updates company net value');
near(at('Solution', 'C11'), 4020, 'Hourly value reaches presentation');
solution.getRange('C5').values = [[50]];
const actual = at('Tasks', 'H246'); sheets.Tasks.getRange('H246').values = [[actual + 1]]; wb.recalculate();
near(at('Campaigns', 'P11'), 2770, 'Last task hours affect company value');
near(at('Campaigns', 'AC11'), 12770, 'Last task hours affect company profit');
sheets.Tasks.getRange('H246').values = [[actual]];
const originalRate = at('Model Pricing', 'B7'); sheets['Model Pricing'].getRange('B7').values = [[originalRate + 1]]; wb.recalculate();
const liteInput = sum(sources.ai_usage.unique.filter(row => row[5] === 'Lite'), row => row[6]);
near(at('Campaigns', 'I11'), 3180 + liteInput / 1e6, 'Model price reaches totals');
sheets['Model Pricing'].getRange('B7').values = [[originalRate]];
const rates = sheets['Model Pricing'].getRange('B7:C8').values;
sheets['Model Pricing'].getRange('B7:C8').values = [[0, 0], [0, 0]]; wb.recalculate();
assert.equal(at('Campaigns', 'Q11'), 'N/A', 'Zero denominator ROI');
sheets['Model Pricing'].getRange('B7:C8').values = rates; wb.recalculate();
for (const [address, expected] of [['I11', 3180], ['N11', 120], ['P11', 2820], ['Q11', 2820 / 3180], ['AC11', 12820], ['AD11', -6380], ['AE11', 12020], ['I12', 1900], ['P12', -400]]) near(at('Campaigns', address), expected, address);
for (const name of sheetNames) for (const row of sheets[name].getUsedRange().values) for (const value of row) if (typeof value === 'string' && /^#(?:REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(value)) throw new Error(`${name}: ${value}`);
console.log((await wb.inspect({ kind: 'table', range: 'Solution!B8:D13', include: 'values,formulas', tableMaxRows: 6, tableMaxCols: 3, maxChars: 2200 })).ndjson);
console.log((await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 20 }, summary: 'Final formula error scan', maxChars: 1500 })).ndjson);
const previews = [
  ['Solution', 'A1:M42', 'solution-overview'], ['Solution', 'A43:M59', 'solution-mix-workflow'], ['Solution', 'A60:M85', 'solution-recommendations'],
  ['Campaigns', 'A6:K12', 'campaign-costs'], ['Campaigns', 'L6:U12', 'campaign-value'], ['Campaigns', 'Z6:AE12', 'campaign-finances'],
  ['Mix', 'A1:J13', 'mix'], ['Workflow', 'A1:H14', 'workflow'], ['Workflow', 'T6:AD14', 'workflow-ratios'], ['Daily Usage', 'A1:K12', 'daily-usage'],
  ['Tasks', 'A1:F12', 'tasks-identifiers'], ['Tasks', 'G6:N12', 'tasks-hours'], ['Tasks', 'O6:AA12', 'tasks-calculations'],
  ['Prompt Totals', 'A1:N12', 'prompt-totals'], ['Priced Usage', 'A1:I12', 'priced-usage-source'], ['Priced Usage', 'J6:O12', 'priced-usage-formulas'],
  ['Raw Work Log', 'A1:F11', 'raw-work-log'], ['Raw AI Usage', 'A1:I11', 'raw-ai-usage'], ['Model Pricing', 'A1:C8', 'model-pricing'], ['Campaign Inputs', 'A1:D10', 'campaign-inputs'],
  ['Preparation', 'A1:C16', 'preparation-steps'], ['Preparation', 'B19:E37', 'preparation-checks'], ['Preparation', 'B40:F52', 'preparation-refresh'],
  ['Data Dictionary', 'A1:D15', 'dictionary-source'], ['Data Dictionary', 'A35:D47', 'dictionary-derived'], ['Data Dictionary', `A${schemas['Data Dictionary'].last - 12}:D${schemas['Data Dictionary'].last}`, 'dictionary-last'],
];
for (const [name, range, filename] of previews) {
  const preview = await wb.render({ sheetName: name, range, scale: 1.3, format: 'png' });
  await fs.writeFile(path.join(previewDir, `${filename}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const outputPath = path.join(outputDir, path.basename(destination));
console.log('Exporting workbook.');
await (await SpreadsheetFile.exportXlsx(wb)).save(outputPath);
console.log(execFileSync(python, [path.join(root, 'TECHNICAL/workbook-tools/cache_chart_values.py'), outputPath], { encoding: 'utf8' }));
await fs.copyFile(outputPath, destination);
await fs.writeFile(path.join(previewDir, 'schema.json'), JSON.stringify({ sheetNames, schemas, sourceCounts: Object.fromEntries(Object.entries(sources).map(([name, source]) => [name, { raw: source.rows.length, clean: source.unique.length }])) }, null, 2));
console.log(JSON.stringify({ output: destination, tasks: cleaned.length, prompts: sources.ai_usage.unique.length, sheets: sheetNames.length, charts: 2, recalculationChecks: 'passed' }));
