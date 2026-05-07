# Project Learnings

## Canonical Run Metadata Before Ledger Events

**Problem**
Semantic ledger rows can end up with `unknown` for `harness` and `model` when each writer tries to infer runtime identity independently.

**Root cause**
The phase setup flow created the ledger directory but did not persist one canonical run-level metadata source that later implementer, reviewer, and debugger steps could reuse.

**Fix**
Write `eval/runs/<phase-slug>/run-config.yaml` during phase branch setup, then require every ledger-event writer and the grader to read that file before appending or interpreting event rows.

**Watch for**
Any ledger schema that includes runtime identity fields without a phase-start step that captures those values once and reuses them across every later stage.