---
name: eval-score-table-output
description: "Append Eval Grader comparison results to a persistent additive markdown score history table using normalized 1-10 scores where 10 is best."
---

# Eval Score Table Output

Use this skill after the Eval Grader finishes writing its detailed score report.

## Target File

Write to this persistent markdown file in the repository root:

- `eval/EVAL_GRADER_SCORE_HISTORY.md`

## Contract

- Scores in the table are normalized to `1-10`, where `10` is best.
- The golden path is the reference implementation and is treated as scoring `10` on every axis.
- Append exactly one new row per completed grading run.
- Never delete, rewrite, reorder, sort, or deduplicate existing rows.
- If the file does not exist, create it with the header and table shown below.
- If the file already exists, preserve the header and all prior rows exactly as they are.

## Table Schema

Use this exact column order:

| Timestamp | Phase | Clean Base | Golden Path | Evaluated Branch | Equivalence | Maintainability | Bug Risk | Edge Cases | Turns | Initial Patch Tests | Review Quality | Footprint | Mean Time/Task | Overall Verdict | Report Path | Notes |
|-----------|-------|------------|-------------|------------------|-------------|-----------------|----------|------------|-------|---------------------|----------------|-----------|----------------|-----------------|-------------|-------|

## Row Rules

- Use normalized `1-10` scores in every scored axis column when the grader has enough evidence.
- If an axis lacks exact evidence and the grader marked it `[NEEDS_HUMAN_REVIEW]`, write `NHR` in that score cell and explain the missing evidence in `Notes`.
- `Bug Risk` is inverted for readability: `10` means lowest risk.
- `Turns`, `Footprint`, and `Mean Time/Task` are also normalized so `10` means the best outcome.
- `Overall Verdict` should use the grader's final `PASS`, `FAIL`, or `PARTIAL` verdict.
- `Report Path` should point to the timestamped detailed score report.
- `Notes` should be compact and may include raw backing values such as `turns_raw=3`, `initial_tests_raw=128`, `files_per_ac=2.1`, or `mean_time_raw=00:18:30`.

## Golden Reference Rule

- If the evaluated branch is itself the golden path branch, append a row with `10` in every scored axis.
- Otherwise, score the evaluated branch relative to the golden path reference and append only the evaluated row.

## Additive-Only Reminder

This file is a persistent comparison history that should live on the clearly specified `main` branch. Treat every append as historical recordkeeping, not as a mutable dashboard.
