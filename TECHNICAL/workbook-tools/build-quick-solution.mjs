import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Optional authoring tool only. Excel needs no runtime, macros, or connections.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const runtime = process.env.WORKBOOK_ARTIFACT_RUNTIME;
if (!runtime) throw new Error('Set WORKBOOK_ARTIFACT_RUNTIME to the directory containing the bundled node_modules junction.');
const python = process.env.WORKBOOK_PYTHON;
if (!python) throw new Error('Set WORKBOOK_PYTHON to the bundled Python executable for native chart-cache export.');
const require = createRequire(path.join(path.resolve(runtime), 'package.json'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const outputDir = path.join(root, 'outputs/01a16549-fb89-7931-89c2-47b56643a454');
const previewDir = path.join(root, '.qa/quick-solution-previews');
const destination = path.join(root, 'SOLUTION/TRACKS/quick-challenge/mru-quick-challenge-solution.xlsx');
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const source = path.join(root, 'DATA/TRACKS/quick-challenge/mru_quick_challenge.csv');
const imported = await Workbook.fromCSV(await fs.readFile(source, 'utf8'), { sheetName: 'Source' });
const input = imported.worksheets.getItemAt(0).getUsedRange().values;
const headers = input[0];
const numeric = new Set(headers.slice(8, 16));
const rawRows = input.slice(1).map(row => row.map((value, index) => {
  if (index === 1) return (Date.parse(`${value}T00:00:00Z`) - Date.UTC(1899, 11, 30)) / 86400000;
  return numeric.has(headers[index]) ? Number(value) : value;
}));
const unique = new Map(), duplicateIds = [];
for (const row of rawRows) {
  if (unique.has(row[0])) {
    assert.deepEqual(row, unique.get(row[0]), `Conflicting duplicate ${row[0]}`);
    duplicateIds.push(row[0]);
  } else unique.set(row[0], row);
}
const cleanRows = [...unique.values()].map(row => row.map((value, index) => index === 3
  ? value.trim().toLowerCase().replace(/\b\w/g, character => character.toUpperCase()) : value));
assert.equal(rawRows.length, 122);
assert.equal(cleanRows.length, 120);

const workbook = Workbook.create();
const solution = workbook.worksheets.add('Solution');
const summaries = workbook.worksheets.add('Summaries');
const clean = workbook.worksheets.add('Clean');
const raw = workbook.worksheets.add('Raw');
const palette = { navy: '#16324F', blue: '#245A81', ink: '#202E3B', muted: '#596B7B', line: '#CCD6DF', light: '#EEF3F7', good: '#23784D', bad: '#AC3232' };
const usd = '"$"#,##0.00;[Red]("$"#,##0.00);"$"0.00';
const decimal = '#,##0.00;[Red](#,##0.00);0.00';
const pct = '0.0%;[Red](0.0%);0.0%';
const letter = index => {
  let result = '';
  for (let n = index + 1; n > 0; n = Math.floor((n - 1) / 26)) result = String.fromCharCode(65 + (n - 1) % 26) + result;
  return result;
};
function base(sheet, range) {
  sheet.showGridLines = false;
  const area = sheet.getRange(range);
  area.format.font = { name: 'Arial', size: 11, color: palette.ink };
  area.format.rowHeight = 23;
  area.format.verticalAlignment = 'center';
  area.format.wrapText = false;
}
function title(sheet, cell, text) {
  sheet.getRange(cell).values = [[text]];
  sheet.getRange(cell).format.font = { name: 'Arial', size: 16, bold: true, color: palette.navy };
  sheet.getRange(cell).format.rowHeight = 29;
}
function heading(sheet, address) {
  const range = sheet.getRange(address);
  range.format.fill = palette.navy;
  range.format.font = { name: 'Arial', size: 11, bold: true, color: '#FFFFFF' };
  range.format.horizontalAlignment = 'center';
  range.format.wrapText = true;
  range.format.rowHeight = 35;
  range.format.borders = { insideVertical: { style: 'thin', color: '#FFFFFF' } };
}
function emphasis(sheet, address) {
  const range = sheet.getRange(address);
  range.format.fill = palette.light;
  range.format.font.bold = true;
  range.format.borders = { top: { style: 'thin', color: palette.line } };
}
function signedColor(sheet, address) {
  const range = sheet.getRange(address);
  range.conditionalFormats.add('cellIs', { operator: 'lessThan', formula: 0, format: { font: { color: palette.bad } } });
  range.conditionalFormats.add('cellIs', { operator: 'greaterThan', formula: 0, format: { font: { color: palette.good } } });
}
function section(sheet, cell, text) {
  sheet.getRange(cell).values = [[text]];
  sheet.getRange(cell).format.font = { name: 'Arial', size: 11, bold: true, color: palette.navy };
  sheet.getRange(cell).format.rowHeight = 28;
}

for (const [sheet, rows, columns, tableName] of [[raw, rawRows, headers, 'RawTasks'], [clean, cleanRows, [...headers, 'total_tokens', 'input_cost_usd', 'output_cost_usd', 'ai_cost_usd', 'hours_saved', 'time_value_usd', 'net_ai_value_usd'], 'Tasks']]) {
  const last = rows.length + 6, lastColumn = letter(columns.length - 1);
  base(sheet, `A1:${lastColumn}${last}`);
  sheet.getRangeByIndexes(5, 0, 1, columns.length).values = [columns];
  sheet.getRangeByIndexes(6, 0, rows.length, 17).values = rows;
  const table = sheet.tables.add(`A6:${lastColumn}${last}`, true, tableName);
  table.style = 'TableStyleMedium2';
  table.showFilterButton = true;
  table.showTotals = false;
  heading(sheet, `A6:${lastColumn}6`);
  sheet.getRange(`A6:${lastColumn}6`).format.rowHeight = 43;
  for (let col = 0; col < columns.length; col++) {
    const name = columns[col];
    sheet.getRange(`${letter(col)}1:${letter(col)}${last}`).format.columnWidth = col === 3 ? 24 : col === 7 ? 26 : col === 4 ? 21 : col === 16 ? 20 : 18;
    if (col >= 8 && col !== 16) sheet.getRange(`${letter(col)}7:${letter(col)}${last}`).setNumberFormat(name.includes('hours') || name === 'hours_saved' ? decimal : name.endsWith('_usd') ? usd : '#,##0');
  }
  sheet.getRange(`B7:B${last}`).setNumberFormat('mm/dd/yy');
  sheet.getRange(`I7:P${last}`).format.horizontalAlignment = 'right';
  sheet.freezePanes.freezeRows(6);
  sheet.freezePanes.freezeColumns(3);
}
title(raw, 'A2', 'Original Quick Challenge records');
raw.getRange('A3').values = [['Source: https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/blob/main/DATA/TRACKS/quick-challenge/mru_quick_challenge.csv']];
raw.getRange('A4').values = [['122 original records, including two exact duplicate tasks. Original labels and whitespace are preserved.']];
raw.getRange('A5').values = [['Hourly value source: https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/blob/main/QUESTIONS/TRACKS/quick-challenge/README.md']];
raw.getRange('A3:A5').format.font.color = palette.muted;
title(clean, 'A2', 'Clean tasks and calculations');
clean.getRange('A3:B3').values = [['USD / staff hour', 50]];
clean.getRange('B3').setNumberFormat(usd);
clean.getRange('B3').format.fill = '#FFF1C9';
clean.getRange('B3').format.font.color = '#2154A0';
clean.getRange('D3').values = [['The supplied assumption is $50/hour. Revisit the written recommendation if you change inputs.']];
clean.getRange('A4').values = [[`Cleaning: 122 raw rows, 120 unique tasks. Removed repeated IDs ${duplicateIds.join(' and ')}. Trimmed and standardized department labels.`]];
clean.getRange('A5').values = [['Source fields A–Q are the cleaned snapshot. Formula columns R–X show each calculation. Rework is already part of actual hours.']];
clean.getRange('A4:A5').format.font.color = palette.muted;
clean.getRange('A7:Q126').format.font.color = '#2154A0';
for (const [column, formula] of Object.entries({ R: '=J7+K7', S: '=J7*L7/1000000', T: '=K7*M7/1000000', U: '=SUM(S7:T7)', V: '=N7-O7', W: '=V7*$B$3', X: '=W7-U7' })) {
  clean.getRange(`${column}7`).formulas = [[formula]];
  clean.getRange(`${column}7:${column}126`).fillDown();
}
clean.getRange('R7:X126').format.horizontalAlignment = 'right';
signedColor(clean, 'V7:X126');
clean.tabColor = '#5C7F9D';

base(summaries, 'A1:R34');
summaries.getRange('A1:A34').format.columnWidth = 3;
summaries.getRange('B1:B34').format.columnWidth = 25;
summaries.getRange('C1:R34').format.columnWidth = 17;
summaries.getRange('C8:R30').format.horizontalAlignment = 'right';
title(summaries, 'B2', 'Grouped calculations');
summaries.getRange('B3').values = [['SUMIFS and COUNTIFS group the same task table used in learner PivotTables. These formulas recalculate without a refresh.']];
summaries.getRange('B4').values = [['Scope: Campaigns 1 and 2 only. Read each formula in the Excel formula bar. Totals retain full precision.']];
section(summaries, 'B6', 'Campaign totals');
summaries.getRange('B7:R7').values = [['Campaign', 'Tasks', 'Input tokens', 'Output tokens', 'Total tokens', 'Prompts', 'Input cost', 'Output cost', 'AI cost', 'No-AI hours', 'Actual hours', 'Hours saved', 'Time value', 'Net AI value', 'AI ROI', 'Rework hours', 'Rework share']];
summaries.getRange('B8:B10').values = [['Campaign 1'], ['Campaign 2'], ['Total']];
for (const row of [8, 9]) {
  summaries.getRange(`C${row}`).formulas = [[`=COUNTIFS('Clean'!$C$7:$C$126,$B${row})`]];
  for (const [destinationColumn, sourceColumn] of Object.entries({ D: 'J', E: 'K', F: 'R', G: 'I', H: 'S', I: 'T', J: 'U', K: 'N', L: 'O', M: 'V', N: 'W', O: 'X', Q: 'P' })) {
    summaries.getRange(`${destinationColumn}${row}`).formulas = [[`=SUMIFS('Clean'!$${sourceColumn}$7:$${sourceColumn}$126,'Clean'!$C$7:$C$126,$B${row})`]];
  }
}
for (let col = 2; col <= 16; col++) {
  const name = letter(col);
  if (!['P', 'R'].includes(name)) summaries.getRange(`${name}10`).formulas = [[`=SUM(${name}8:${name}9)`]];
}
for (const row of [8, 9, 10]) {
  summaries.getRange(`P${row}`).formulas = [[`=IF(J${row}=0,"N/A",O${row}/J${row})`]];
  summaries.getRange(`R${row}`).formulas = [[`=IF(L${row}=0,"N/A",Q${row}/L${row})`]];
}
heading(summaries, 'B7:R7');
summaries.getRange('B7:R7').format.rowHeight = 43;
summaries.getRange('C8:G10').setNumberFormat('#,##0');
for (const range of ['H8:J10', 'N8:O10']) summaries.getRange(range).setNumberFormat(usd);
for (const range of ['K8:M10', 'Q8:Q10']) summaries.getRange(range).setNumberFormat(decimal);
for (const range of ['P8:P10', 'R8:R10']) summaries.getRange(range).setNumberFormat(pct);
emphasis(summaries, 'B10:R10');
signedColor(summaries, 'M8:P10');

section(summaries, 'B14', 'Department comparison');
summaries.getRange('B15:E15').values = [['Department', 'AI cost (USD)', 'Net AI value (USD)', 'Hours saved']];
summaries.getRange('B16:B20').values = [['Analytics'], ['Content'], ['Creative'], ['Marketing Operations'], ['Total']];
for (let row = 16; row <= 19; row++) {
  for (const [dest, src] of [['C', 'U'], ['D', 'X'], ['E', 'V']]) summaries.getRange(`${dest}${row}`).formulas = [[`=SUMIFS('Clean'!$${src}$7:$${src}$126,'Clean'!$D$7:$D$126,$B${row})`]];
}
for (const col of ['C', 'D', 'E']) summaries.getRange(`${col}20`).formulas = [[`=SUM(${col}16:${col}19)`]];
heading(summaries, 'B15:E15');
summaries.getRange('C16:D20').setNumberFormat(usd);
summaries.getRange('E16:E20').setNumberFormat(decimal);
emphasis(summaries, 'B20:E20');
signedColor(summaries, 'D16:E20');

section(summaries, 'B24', 'Recorded issues by task');
summaries.getRange('B25:E25').values = [['Issue', 'Campaign 1', 'Campaign 2', 'Total tasks']];
summaries.getRange('B26:B30').values = [['Brief changed'], ['Data problem'], ['Unclear prompt'], ['None'], ['Total']];
for (let row = 26; row <= 29; row++) {
  for (const col of ['C', 'D']) summaries.getRange(`${col}${row}`).formulas = [[`=COUNTIFS('Clean'!$Q$7:$Q$126,$B${row},'Clean'!$C$7:$C$126,${col}$25)`]];
  summaries.getRange(`E${row}`).formulas = [[`=SUM(C${row}:D${row})`]];
}
for (const col of ['C', 'D', 'E']) summaries.getRange(`${col}30`).formulas = [[`=SUM(${col}26:${col}29)`]];
heading(summaries, 'B25:E25');
summaries.getRange('C26:E30').setNumberFormat('#,##0');
emphasis(summaries, 'B30:E30');
summaries.getRange('B32').values = [['One primary issue per task. None means no recorded issue; it is not a problem category.']];
summaries.getRange('B33').values = [['Rework is a subset of actual hours. Revenue and whole-campaign profit are not supplied in the quick track.']];
summaries.tabColor = palette.blue;

base(solution, 'A1:L78');
solution.getRange('A1:A78').format.columnWidth = 3;
solution.getRange('B1:B78').format.columnWidth = 32;
solution.getRange('C1:E78').format.columnWidth = 17;
solution.getRange('F1:F78').format.columnWidth = 3;
solution.getRange('G1:L78').format.columnWidth = 12;
solution.getRange('C7:E49').format.horizontalAlignment = 'right';
title(solution, 'B2', 'Quick Challenge worked solution');
solution.getRange('B3').values = [['MRU, September 2026. Campaigns 1 and 2. Fictional teaching data.']];
solution.getRange('B4:L4').format.borders = { bottom: { style: 'thin', color: palette.line } };
const campaignHeader = row => {
  solution.getRange(`B${row}:E${row}`).values = [['Metric', 'Campaign 1', 'Campaign 2', 'Combined']];
  heading(solution, `B${row}:E${row}`);
};
function linkMetric(row, label, sourceColumn, format) {
  solution.getRange(`B${row}`).values = [[label]];
  solution.getRange(`C${row}:E${row}`).formulas = [[8, 9, 10].map(sourceRow => `='Summaries'!${sourceColumn}${sourceRow}`)];
  solution.getRange(`C${row}:E${row}`).setNumberFormat(format);
}
section(solution, 'B5', 'Q1. What tokens, costs and prompts did each campaign use?');
campaignHeader(6);
linkMetric(7, 'Input tokens', 'D', '#,##0');
linkMetric(8, 'Output tokens', 'E', '#,##0');
linkMetric(9, 'Total tokens', 'F', '#,##0');
linkMetric(10, 'Employee prompts', 'G', '#,##0');
linkMetric(11, 'Input cost (USD)', 'H', usd);
linkMetric(12, 'Output cost (USD)', 'I', usd);
linkMetric(13, 'Total AI cost (USD)', 'J', usd);
emphasis(solution, 'B13:E13');
section(solution, 'B16', 'Q2. How many hours did each campaign save or lose?');
campaignHeader(17);
linkMetric(18, 'No-AI estimated hours', 'K', decimal);
linkMetric(19, 'Actual hours with AI', 'L', decimal);
linkMetric(20, 'Net hours saved', 'M', decimal);
emphasis(solution, 'B20:E20');
signedColor(solution, 'C20:E20');
section(solution, 'B22', 'Q3. After AI fees, was estimated net value positive or negative?');
campaignHeader(23);
linkMetric(24, 'Time value at $50/hour', 'N', usd);
solution.getRange('B24').formulas = [['="Time value at "&TEXT(\'Clean\'!$B$3,"$0")&"/hour"']];
linkMetric(25, 'AI cost (USD)', 'J', usd);
linkMetric(26, 'Net AI value (USD)', 'O', usd);
linkMetric(27, 'AI ROI', 'P', pct);
emphasis(solution, 'B26:E26');
signedColor(solution, 'C26:E27');
solution.getRange('B28').values = [['ROI uses totals. Time value is not payroll cash saved.']];
solution.getRange('B28').format.font = { name: 'Arial', size: 11, color: palette.muted, italic: true };

section(solution, 'B30', 'Q4. Which department led AI spending and net AI value?');
solution.getRange('B31:E31').values = [['Department', 'AI cost (USD)', 'Net AI value (USD)', 'Hours saved']];
heading(solution, 'B31:E31');
for (let row = 32; row <= 35; row++) solution.getRange(`B${row}:E${row}`).formulas = [['B', 'C', 'D', 'E'].map(col => `='Summaries'!${col}${row - 16}`)];
solution.getRange('C32:D35').setNumberFormat(usd);
solution.getRange('E32:E35').setNumberFormat(decimal);
signedColor(solution, 'D32:E35');
solution.getRange('B37').formulas = [['="Highest spending: "&INDEX(B32:B35,MATCH(MAX(C32:C35),C32:C35,0))&" ("&TEXT(MAX(C32:C35),"$#,##0.00")&")."']];
solution.getRange('B38').formulas = [['="Highest net AI value: "&INDEX(B32:B35,MATCH(MAX(D32:D35),D32:D35,0))&" ("&TEXT(MAX(D32:D35),"$#,##0.00")&")."']];

section(solution, 'B40', 'Q5. Which campaign had more rework, and which issues appeared most?');
solution.getRange('B41:D41').values = [['Campaign', 'Rework hours', 'Share of actual hours']];
heading(solution, 'B41:D41');
for (let row = 42; row <= 43; row++) solution.getRange(`B${row}:D${row}`).formulas = [[`='Summaries'!B${row - 34}`, `='Summaries'!Q${row - 34}`, `='Summaries'!R${row - 34}`]];
solution.getRange('C42:C43').setNumberFormat(decimal);
solution.getRange('D42:D43').setNumberFormat(pct);
solution.getRange('B45:E45').values = [['Recorded issue', 'Campaign 1 tasks', 'Campaign 2 tasks', 'Combined tasks']];
heading(solution, 'B45:E45');
for (let row = 46; row <= 49; row++) solution.getRange(`B${row}:E${row}`).formulas = [['B', 'C', 'D', 'E'].map(col => `='Summaries'!${col}${row - 20}`)];
solution.getRange('C46:E49').setNumberFormat('#,##0');
solution.getRange('B51').formulas = [['=INDEX(B42:B43,MATCH(MAX(C42:C43),C42:C43,0))&" had the most rework: "&TEXT(MAX(C42:C43),"0.00")&" hours."']];
solution.getRange('B52').formulas = [['="Most common problem: "&INDEX(B46:B48,MATCH(MAX(E46:E48),E46:E48,0))&" ("&TEXT(MAX(E46:E48),"0")&" tasks). None means no recorded issue."']];

section(solution, 'B54', 'Q6. Should MRU keep, change or reduce its AI use?');
const recommendation = [
  'Keep the disciplined AI workflow used in Campaign 1. Its 100 hours saved were worth $5,000 at the supplied',
  '$50 hourly rate, exceeding its $500 AI bill and leaving $4,500 of estimated net value. Action 1: document',
  'its task selection, prompt preparation and review process, then repeat that process on comparable work.',
  'Record actual hours and rework so the team can confirm that the benefit continues at acceptable quality.',
  '',
  'Change and temporarily narrow AI use in Campaign 2. It used twice as many prompts as Campaign 1, yet',
  'required 70 more hours than its no-AI estimate and produced a $4,900 net loss after $1,400 of AI fees.',
  'Action 2: stabilize briefs before prompting and set a review checkpoint for rework-heavy tasks. Brief',
  'changes affected 27 Campaign 2 tasks, and its 87.82 rework hours warrant investigation before expanding use.',
  '',
  'Compare future results using summed net value and rework hours, not prompt volume alone. The combined',
  'result is a $400 net loss, so a positive campaign should not hide a weak one. These are observations from',
  'fictional data, not proof of causation or cash payroll savings. Baseline hours are estimates and campaign',
  'profit cannot be calculated because this quick-track file supplies no revenue or other campaign costs.',
];
solution.getRange(`B55:B${54 + recommendation.length}`).values = recommendation.map(line => [line]);
solution.getRange('B70').values = [['How to trace an answer: Solution links to Summaries; Summaries groups Clean; Clean retains visible task formulas.']];
solution.getRange('B71').values = [['Raw preserves the original export. Clean removes two duplicate IDs and standardizes department labels.']];
solution.getRange('B72').values = [['Use the supplied data for the reference answer. Editing Clean updates formulas and charts; review the written recommendation after changes.']];
solution.getRange('B73').values = [['No external data connection or macro is required. All calculations and source rows are inside this workbook.']];
solution.getRange('B70:B73').format.font.color = palette.muted;
solution.tabColor = palette.navy;

const valueChart = solution.charts.add('bar', [summaries.getRange('B7:B9'), summaries.getRange('O7:O9')]);
valueChart.title = 'Net AI value after fees (USD)';
valueChart.setPosition('G7', 'L20');
valueChart.hasLegend = false;
valueChart.series.items[0].fill = palette.blue;
const hourChart = solution.charts.add('bar', [summaries.getRange('B7:B9'), summaries.getRange('K7:K9'), summaries.getRange('L7:L9')]);
hourChart.title = 'Estimated and actual hours';
hourChart.setPosition('G23', 'L36');
hourChart.legend = { position: 'top', textStyle: { typeface: 'Arial', fontSize: 14 } };
hourChart.series.items[0].fill = '#A8BAC9';
hourChart.series.items[1].fill = palette.blue;
for (const chart of [valueChart, hourChart]) {
  chart.titleTextStyle.fontSize = 14;
  chart.titleTextStyle.typeface = 'Arial';
  chart.xAxis = { axisType: 'textAxis', tickLabelPosition: 'low', majorGridlines: null, textStyle: { typeface: 'Arial', fontSize: 14 } };
  chart.yAxis = { numberFormatCode: chart === valueChart ? '$#,##0;($#,##0)' : '0', numberFormatSourceLinked: false, textStyle: { typeface: 'Arial', fontSize: 14 } };
}

// Test actual recalculation, restore every input, then verify the saved case.
const approx = (actual, expected, label) => assert.ok(Math.abs(actual - expected) < 0.000001, `${label}: ${actual} != ${expected}`);
const numberAt = (sheet, address) => sheet.getRange(address).values[0][0];
clean.getRange('B3').values = [[60]];
workbook.recalculate();
approx(numberAt(solution, 'C26'), 5500, 'Changed hourly value reaches Campaign 1 answer');
approx(numberAt(solution, 'D26'), -5600, 'Changed hourly value reaches Campaign 2 answer');
assert.equal(numberAt(solution, 'B24'), 'Time value at $60/hour', 'Rate label follows the editable assumption');
clean.getRange('B3').values = [[50]];
const originalActual = numberAt(clean, 'O126');
clean.getRange('O126').values = [[originalActual + 1]];
workbook.recalculate();
approx(numberAt(solution, 'D26'), -4950, 'Last task edit reaches Campaign 2 answer');
clean.getRange('O126').values = [[originalActual]];
const originalRates = clean.getRange('L7:M126').values;
clean.getRange('L7:M126').values = originalRates.map(() => [0, 0]);
workbook.recalculate();
assert.equal(numberAt(solution, 'E27'), 'N/A', 'Zero spending has undefined ROI');
clean.getRange('L7:M126').values = originalRates;
workbook.recalculate();
for (const [cell, expected] of [['C26', 4500], ['D26', -4900], ['E26', -400], ['C27', 9], ['D27', -3.5], ['E27', -400 / 1900]]) approx(numberAt(solution, cell), expected, cell);
const checks = await workbook.inspect({ kind: 'table', range: 'Solution!B23:E27', include: 'values,formulas', tableMaxRows: 5, tableMaxCols: 4, maxChars: 3000 });
console.log(checks.ndjson);
const errors = await workbook.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 30 }, summary: 'Final formula error scan', maxChars: 2500 });
console.log(errors.ndjson);
for (const sheet of [solution, summaries, clean, raw]) {
  for (const row of sheet.getUsedRange().values) for (const value of row) {
    if (typeof value === 'string' && /^#(?:REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(value)) throw new Error(`${sheet.name}: ${value}`);
  }
}
for (const [name, range, filename] of [
  ['Solution', 'A1:L38', 'solution-top'], ['Solution', 'A40:L73', 'solution-answers'],
  ['Summaries', 'B6:J10', 'summary-usage'], ['Summaries', 'K6:R10', 'summary-value'], ['Summaries', 'B14:F33', 'summary-groups'],
  ['Clean', 'A1:H10', 'clean-inputs'], ['Clean', 'R6:X10', 'clean-formulas'], ['Raw', 'A1:H10', 'raw'],
]) {
  const preview = await workbook.render({ sheetName: name, range, scale: 1.5, format: 'png' });
  await fs.writeFile(path.join(previewDir, `${filename}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const outputPath = path.join(outputDir, path.basename(destination));
await (await SpreadsheetFile.exportXlsx(workbook)).save(outputPath);
// This runtime exports empty native chart caches. Hydrate them from saved
// source-cell results so preview readers also see the charts before a refresh.
console.log(execFileSync(python, [path.join(root, 'TECHNICAL/workbook-tools/cache_chart_values.py'), outputPath], { encoding: 'utf8' }));
await fs.mkdir(path.dirname(destination), { recursive: true });
await fs.copyFile(outputPath, destination);
console.log(JSON.stringify({ output: destination, rawRecords: rawRows.length, cleanTasks: cleanRows.length, duplicateIds, charts: 2, recalculationChecks: 'passed' }));
