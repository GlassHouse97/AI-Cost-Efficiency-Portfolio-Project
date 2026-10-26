# Learner guide author walkthrough

Date: October 22, 2026.

This is the historical walkthrough of the original CSV-only packages. File paths below use their current repository locations. The later Excel workbook addition and October 26 Quick Challenge simplification are checked by the current learner-file tests. The current Quick Challenge contains a question page and raw data, with its calculation method in the separate solution. The instructions, byte counts, archive entry counts, and SHA-256 values below describe the original October 22 packages.

This was a timed **automated author walkthrough with browser inspection**, not a beginner pilot and not a timed learner submission in Excel. It checks that the written preparation and arithmetic can be followed with the supplied files. It does not establish that a beginner can complete the assignment in four hours.

## Timing and method

The recorded walkthrough window was **4:32:19 to 4:33:50 p.m. America/New_York**, about **91 seconds**, measured from the first package build through the formula, archive, and browser checks. The Python DATA/arithmetic verification inside that window took approximately **0.037 seconds**. Time spent drafting the guides before this window was not included. These author timings are deliberately not presented as learner completion times.

Using only the source CSVs and the learner guide's stated operations, the author check read the quick export, removed exact repeated work-item records, standardized department labels with trim/title case (the same transformation as Excel TRIM/PROPER), calculated the five required fields using decimal arithmetic, and grouped the results by campaign and department. It verified the rework bounds, summed measures, and ratio definitions without printing campaign answer totals into learner materials.

The independent worked example was recalculated: 20 Lite prompts, each containing 10,000 input and 5,000 output tokens, cost $5 in total. A two-hour baseline and 1.5 actual hours produce 0.5 hours saved, $25 of time value, $20 net AI value, and 400% ROI. The actual hours enter once per task.

## Checks completed

- Quick CSV: 122 raw rows and 120 unique tasks after removing two exact repeats; four standard department labels after normalization.
- Deeper task file: 242 raw rows and 240 unique tasks; the eight-employee structure was confirmed.
- Prompt file: unique usage IDs; every prompt links to the recorded task and agrees with its campaign.
- All five source-file headers match the supplied schema exactly. No calculated answer columns are included in the raw files.
- The five quick calculations and grouped arithmetic reconcile. Rework is not added to actual hours. Group ratios use summed numerators and denominators.
- Archive contents match an explicit allowlist: eight files for Quick Challenge and eleven for Portfolio Project, including both complete licenses. CRC checks pass.
- Both archives exclude author scripts, answer files, exact check totals, and the completed dashboard. The worked illustration is intentionally included in both learner guides.
- Both offline HTML guides contain all four Markdown sections, one page-level heading, unique section anchors, local CSV links, and no scripts or external assets.
- Browser inspection at a 1,265-pixel viewport confirmed readable headers, body text, formula tables, navigation, and CSV links. A bold-formatting issue around the prompt-aggregation warning was corrected and checked again; there was no horizontal page overflow.
- The hosting copies are byte-identical to the release ZIPs. Running `python TECHNICAL/scripts/package_learners.py --check` passes and recomputes the same archive bytes from source.

## Limits and follow-up

The walkthrough did not operate Excel, create a learner workbook, time manual PivotTable/chart construction, or test the recommendation-writing task with a novice. The four-hour plan remains a design target. A future beginner pilot should record time by the six stated blocks and identify where independent learners need clarification. If core work exceeds four hours, simplify it rather than adding prerequisites. Optional BI, product, and rework charts remain optional.

This author note stays outside the learner archives. Regenerate downloads with `python TECHNICAL/scripts/package_learners.py` after editing learner Markdown, CSVs, licenses, or HTML styling, then use `python TECHNICAL/scripts/package_learners.py --check` to verify the generated files are current.

## Portable archive verification

A subsequent check found that Deflate-compressed archive bytes differed between the bundled Python 3.12.14 and system Python 3.14.6 runtimes. The package builder now uses uncompressed ZIP entries, fixed timestamps and file attributes, a sorted explicit allowlist, and UTF-8 text with LF line endings. This removes the archive's dependency on zlib version and checkout line-ending conventions.

After regeneration, the packaging check (now `TECHNICAL/scripts/package_learners.py --check`) passed under both runtimes with identical SHA-256 digests. A temporary copy with every source file changed to CRLF line endings also produced byte-identical archives. Archive metadata, uncompressed entries, and LF payloads were verified. This additional packaging check is separate from the 91-second learner-guide walkthrough above; Linux CI has not been claimed as run here.

| Package | Bytes | SHA-256 |
| --- | --- | --- |
| mru-quick-challenge.zip | 68,825 | `6a7969604ddcc6c9d490f55e4a6b4ae6bea65f3fc8850475a0892c36aef779f7` |
| mru-portfolio-project.zip | 308,812 | `10d2b0febfafc17c44e479ee75f795a17c1d870143e0f5630dc516f21bfb1465` |
