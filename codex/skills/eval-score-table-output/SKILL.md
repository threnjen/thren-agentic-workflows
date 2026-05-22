---
name: eval-score-table-output
description: "Append Eval Grader comparison results to a persistent additive markdown score history table using normalized 1-10 scores where 10 is best."
---
<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
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
- Preserve legacy schema sections and prior rows exactly as they are.
- If the file does not exist, create it with the current schema section shown below.
- If the file already exists with only the legacy table, append a blank line, a `## Schema v2` heading, the current schema note, and the new table header exactly once, then append the new row there.
- If the current schema section already exists, append only to that section's table.

## Table Schema

The file may contain both a legacy schema table and the current schema table. New rows must go to the current schema below.

Use this exact current-schema column order:

| Timestamp | Phase | Harness/Model | Evaluated Branch | Overall Verdict | Equivalence | Clarity | Coherence | Robustness | Bug Risk | Scope Discipline | Footprint | Turns | Initial Patch Tests | Review Quality | Mean Time/Task | Report Path | Notes |
|-----------|-------|---------------|------------------|-----------------|-------------|---------|-----------|------------|----------|------------------|-----------|-------|---------------------|----------------|----------------|-------------|-------|

## Row Rules

- Use normalized `1-10` scores in every scored axis column when the grader has enough evidence.
- If an axis lacks exact evidence and the grader marked it `[NEEDS_HUMAN_REVIEW]`, write `NHR` in that score cell and explain the missing evidence in `Notes`.
- `Bug Risk` is inverted for readability: `10` means lowest risk.
- `Turns`, `Footprint`, and `Mean Time/Task` are also normalized so `10` means the best outcome.
- `Footprint` captures diff-surface risk. Do not create a separate `Diff Minimality` column; that concern is intentionally folded into `Scope Discipline` plus `Footprint`.
- `Harness/Model` is provided by the caller (already resolved from `eval/hidden_file.md` by the `Eval - Score Recorder` subagent). Do not look it up here.
- `Overall Verdict` should contain the pre-computed weighted average score on a `1-10` scale (e.g. `6.4`), or `NHR` if all metrics were NHR. The caller provides this value; do not recompute it here.
- `Report Path` should point to the timestamped detailed score report.
- `Notes` should be compact and may include raw backing values such as `turns_raw=3`, `initial_tests_raw=128`, `files_per_ac=2.1`, or `mean_time_raw=00:18:30`.

## Golden Reference Rule

- If the evaluated branch is itself the golden path branch, append a row with `10` in every scored axis.
- Otherwise, score the evaluated branch relative to the golden path reference and append only the evaluated row.

## Additive-Only Reminder

This file is a persistent comparison history that should live on the clearly specified `main` branch. Treat every append as historical recordkeeping, not as a mutable dashboard.
