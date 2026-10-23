import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

// The authoring library is supplied by the Codex workspace runtime. It is not a
// repository dependency and is not needed to open the resulting Excel files.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const runtime = process.env.WORKBOOK_ARTIFACT_RUNTIME;
if (!runtime) throw new Error('Set WORKBOOK_ARTIFACT_RUNTIME to the directory containing the bundled node_modules junction.');
const require = createRequire(path.join(path.resolve(runtime), 'package.json'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const previewDir = path.join(root, '.qa/workbook-previews');
await fs.mkdir(previewDir, { recursive: true });

const numeric = new Set([
  'campaign_revenue_usd', 'other_campaign_cost_usd', 'prompt_count',
  'input_tokens', 'output_tokens', 'input_rate_usd_per_million',
  'output_rate_usd_per_million', 'baseline_hours', 'actual_hours', 'rework_hours',
]);
const dates = new Set(['completion_date', 'usage_date']);
const outputs = [
  { directory: 'quick-challenge', name: 'mru-quick-challenge.xlsx', sources: [
    ['Raw', 'mru_quick_challenge.csv', ['A1:H8', 'I1:Q8']],
  ] },
  { directory: 'portfolio-project', name: 'mru-portfolio-project.xlsx', sources: [
    ['campaigns', 'campaigns.csv', ['A1:D5']],
    ['work_log', 'work_log.csv', ['A1:F8', 'G1:L8']],
    ['ai_usage', 'ai_usage.csv', ['A1:I8']],
    ['model_pricing', 'model_pricing.csv', ['A1:C3']],
  ] },
];

function letters(index) {
  let result = '';
  for (let value = index + 1; value > 0; value = Math.floor((value - 1) / 26))
    result = String.fromCharCode(65 + ((value - 1) % 26)) + result;
  return result;
}

function convert(value, header) {
  if (value === null || value === '') return value;
  if (dates.has(header)) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error(`Unexpected date: ${header}=${value}`);
    const date = new Date(`${value}T00:00:00.000Z`);
    if (date.toISOString().slice(0, 10) !== value) throw new Error(`Invalid date: ${value}`);
    // Use the Excel 1900-system serial explicitly. This keeps exported cells
    // numeric and sortable even in runtimes that serialize Date as ISO text.
    return (date.getTime() - Date.UTC(1899, 11, 30)) / 86_400_000;
  }
  if (numeric.has(header)) {
    if (!/^-?\d+(?:\.\d+)?$/.test(value)) throw new Error(`Unexpected numeric input: ${header}=${value}`);
    return Number(value);
  }
  // Deliberately preserve leading/trailing spaces and duplicate IDs.
  return value;
}

for (const output of outputs) {
  const workbook = Workbook.create();
  const metadata = [];
  for (const [name, source, previewRanges] of output.sources) {
    const csvPath = path.join(root, 'DATA', 'TRACKS', output.directory, source);
    const imported = await Workbook.fromCSV(await fs.readFile(csvPath, 'utf8'), { sheetName: name });
    const rows = imported.worksheets.getItemAt(0).getUsedRange().values;
    const headers = rows[0];
    const sheet = workbook.worksheets.add(name);
    const matrix = [headers, ...rows.slice(1).map(row => row.map((value, column) => convert(value, headers[column])))];
    const range = sheet.getRangeByIndexes(0, 0, matrix.length, headers.length);
    range.values = matrix;
    const table = sheet.tables.add(`A1:${letters(headers.length - 1)}${matrix.length}`, true, `${name}_raw`);
    table.style = 'TableStyleMedium2';
    table.showFilterButton = true;
    table.showTotals = false;
    range.format.font = { name: 'Arial', size: 11, color: '#1E293B' };
    range.format.verticalAlignment = 'center';
    range.format.rowHeight = 22;
    range.format.wrapText = false;
    const headerRange = sheet.getRangeByIndexes(0, 0, 1, headers.length);
    headerRange.format.fill = '#16324F';
    headerRange.format.font = { name: 'Arial', size: 11, bold: true, color: '#FFFFFF' };
    headerRange.format.horizontalAlignment = 'center';
    headerRange.format.verticalAlignment = 'center';
    headerRange.format.rowHeight = 38;
    headerRange.format.wrapText = true;
    headerRange.format.borders = { insideVertical: { style: 'thin', color: '#FFFFFF' } };
    for (let column = 0; column < headers.length; column++) {
      const label = headers[column];
      const width = Math.max(15, Math.min(34, Math.max(label.length + 3,
        ...rows.slice(1).map(row => String(row[column] ?? '').length + 2))));
      sheet.getRangeByIndexes(0, column, matrix.length, 1).format.columnWidth = width;
      const body = sheet.getRangeByIndexes(1, column, matrix.length - 1, 1);
      body.format.horizontalAlignment = numeric.has(label) || dates.has(label) ? 'right' : 'left';
      if (dates.has(label)) body.setNumberFormat('yyyy-mm-dd');
      else if (label.endsWith('_hours')) body.setNumberFormat('0.00');
      else if (label.endsWith('_usd')) body.setNumberFormat('"$"#,##0.00');
      else if (numeric.has(label)) body.setNumberFormat('#,##0');
      else body.setNumberFormat('@');
    }
    sheet.showGridLines = false;
    sheet.freezePanes.freezeRows(1);
    if (headers.length > 4) sheet.freezePanes.freezeColumns(1);
    metadata.push({ sheet: name, source: path.relative(root, csvPath), rows: matrix.length - 1, columns: headers.length,
      headers, numericColumns: headers.filter(h => numeric.has(h)), dateColumns: headers.filter(h => dates.has(h)), previewRanges });
  }
  workbook.recalculate();
  const inspect = await workbook.inspect({ kind: 'workbook,sheet,table', maxChars: 3000, tableMaxRows: 2, tableMaxCols: 4 });
  await fs.writeFile(path.join(previewDir, `${output.directory}-inspection.ndjson`), inspect.ndjson);
  const errors = await workbook.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',
    options: { useRegex: true, maxResults: 20 }, maxChars: 1500, summary: 'Raw workbook error scan' });
  await fs.writeFile(path.join(previewDir, `${output.directory}-errors.ndjson`), errors.ndjson);
  for (const info of metadata) {
    for (let part = 0; part < info.previewRanges.length; part++) {
      const preview = await workbook.render({ sheetName: info.sheet, range: info.previewRanges[part], scale: 1.5, format: 'png' });
      await fs.writeFile(path.join(previewDir, `${output.directory}-${info.sheet}-${part + 1}.png`), new Uint8Array(await preview.arrayBuffer()));
    }
  }
  const exported = await SpreadsheetFile.exportXlsx(workbook);
  const outputPath = path.join(root, 'DATA', 'TRACKS', output.directory, output.name);
  // The runtime emits an inspection sidecar on save. Keep it in ignored QA.
  const stagingPath = path.join(previewDir, output.name);
  await exported.save(stagingPath);
  await fs.rename(stagingPath, outputPath);
  await fs.writeFile(path.join(previewDir, `${output.directory}-metadata.json`), JSON.stringify(metadata, null, 2));
  console.log(JSON.stringify({ output: path.relative(root, outputPath), sheets: metadata.map(({sheet,rows,columns}) => ({sheet,rows,columns})) }));
}
