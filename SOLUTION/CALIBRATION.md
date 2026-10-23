# Calibration notes — contains solution spoilers

These files support the completed demonstration and its audit trail. Keep this folder, the generator, the check totals, tests, and the completed dashboard out of both learner ZIPs.

All organizations, employees, usage records, prices, revenue, and results are fictional. This is a deliberately calibrated teaching scenario, not evidence about any real AI provider or workplace. The specification supplied by the project owner defines Campaign 1 and Campaign 2 targets and the fixed fictional prices. Campaign 3 and Campaign 4 add more mixed outcomes for investigation.

## Reproduce and verify

Use Python 3.10 or later; no third-party dependencies or API credentials are needed:

```text
python TECHNICAL/scripts/generate_data.py
python TECHNICAL/scripts/validate_data.py --write-checks
python -m unittest discover -s TECHNICAL/tests -p "test_data.py" -v
```

The seed is `20261022`. The reporting period is the completed month September 2026. Generation uses integer hundredths for task hours and integer tokens; largest-remainder apportionment preserves totals. Token allocations vary across tasks and prompts. Costs are never generated as independent campaign charges. They are calculated from integer input/output tokens and the two fixed rate pairs: Lite 10/30 and Pro 40/100 USD per million tokens.

[`TECHNICAL/scripts/validate_data.py`](../TECHNICAL/scripts/validate_data.py) does not import the generator or read saved check totals. It independently reads the canonical CSVs in `DATA/`, removes exact repeated task IDs, standardizes department labels, prices prompts with `Decimal`, aggregates to task grain, and reconciles the clean dashboard source. [`outputs/check_totals.json`](outputs/check_totals.json) is its reproducible output. Stored monetary values use six decimal places; the dashboard rounds only for display.

## Source and dashboard contract

- `DATA/quick-challenge/mru_quick_challenge.csv`: 122 raw records, 120 distinct focal tasks. Prompt counts and tokens are aggregated to task grain, with rates included for direct Excel formulas.
- `DATA/portfolio-project/work_log.csv`: 242 raw records, 240 distinct tasks, 60 per campaign. The same two repeated focal tasks occur in both learner exports.
- `DATA/portfolio-project/ai_usage.csv`: 3,360 distinct employee prompts with no repeated usage IDs. One `First attempt` per task, followed by `Followup` and `Correction` records.
- `DATA/portfolio-project/model_pricing.csv`: exactly the two fixed model prices.
- `DATA/portfolio-project/campaigns.csv`: four campaigns with one revenue and other-spending record each.
- `TECHNICAL/dashboard/demo-data.json`: arrays named `work_log`, `ai_usage`, `model_pricing`, and `campaigns`, containing clean original-column source records. Numeric fields are JSON numbers, dates are ISO strings, and observation flags are the strings `Yes` and `No`. There are no precomputed dashboard costs or ROI fields.

Every task has one fictional employee, department, product, and model. Employees remain in one department. Usage dates precede or equal task completion dates and fall on September workdays. Prompts span up to four workdays. The task completion date and prompt usage date answer different questions.

Only the intended cleaning problems are injected: exact duplicate task export rows and department labels with whitespace/capitalization changes. Duplicates are W0018 and W0087. Raw focal rows share the same cleaning defects across both tracks. No prices, time estimates, dates, or relationships are missing.

## Calibrated results

| Campaign | Prompts | Input tokens | Output tokens | AI cost | Baseline hours | Actual hours | Net AI value | AI ROI | Campaign result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C001 | 600 | 22,000,000 | 5,000,000 | $500 | 240 | 140 | $4,500 | 900% | $7,500 |
| C002 | 1,200 | 32,000,000 | 10,000,000 | $1,400 | 200 | 270 | -$4,900 | -350% | -$2,400 |
| C003 | 720 | 18,000,000 | 4,500,000 | $540 | 220 | 172 | $1,860 | 344.44% | $4,360 |
| C004 | 840 | 17,000,000 | 5,000,000 | $740 | 260 | 218 | $1,360 | 183.78% | $3,360 |

The entire company has 920 baseline hours and 800 actual hours. Its 120 hours of estimated time saved are worth $6,000 at $50/hour; $3,180 of token spending leaves $2,820 estimated net AI value. Sum underlying amounts before calculating ROI or prompt cost. These time values are not payroll cash savings.

C001 contains eight tasks with negative estimated net AI value. C002 contains ten positive tasks. The scenario therefore supports task-level investigation without implying that every task follows its campaign average. C002 has 482 correction prompts and 87.82 rework hours versus C001's 68 and 10.74. C001 uses templates on 53 tasks versus C002's 19. These are synthetic associations, not evidence of causal effects.

For C001, changing baseline hours by -20% and +20% produces net values of $2,100 and $6,900. For C002, those values are -$6,900 and -$2,900. Both focal conclusions retain their signs. C003 and C004 cross below zero under the -20% baseline case, illustrating why uncertain baselines matter.

## Analytical safeguards

Price and aggregate prompts to one row per task before combining with task hours. Never join prompt-level records and then sum repeated task hours. Rework is already included in actual hours and must not be added again. Sum campaign revenue only from one row per campaign. Full campaign results are whole-campaign measures and must remain independent of prompt-date, product, model, and department filters; label their scope clearly.

The validator checks focal token mix, full-precision costs, shared source populations, duplicate handling, per-task rates, hours, prompt relationships, clean demo parity, sensitivity signs, successful C002 tasks, and weak C001 tasks. Unit tests exercise corrupted input cases so a changed ID, rate, join, token count, hour value, or dashboard source cannot silently pass.

Generation is deterministic for the fixed Python seed and code. This audit does not constitute a timed human learner pilot; the learner dry-run record separately describes what was actually tested.
