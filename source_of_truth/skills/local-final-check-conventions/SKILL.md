---
name: local-final-check-conventions
description: "Shared evidence, attribution, report, and partial-failure rules for local final-check evaluators."
---

# Local Final Check Conventions

Apply these rules to a local review of one confirmed `base..HEAD` range. Apply
`auditor-conventions` for shared severity definitions. Load
`local-final-check-report` when writing a report.

## Inputs and Boundaries

The orchestrator supplies the fixed base and head, a clean baseline worktree,
`changed-files.txt`, `range.diff`, and one output path. Never derive another
base, create a worktree, or modify either tree.

Findings must map to lines the range added or behavior those lines changed. A
touched file does not make its pre-existing defects attributable to the range.
Use the supplied diff artifacts as the authoritative attribution source.

Plans, specifications, QA records, merge-request context, and approval
summaries are synthesis enrichment. Evaluators do not receive them. Coverage
evidence is direct Test Health input because it measures that evaluator's
subject.

## Reports

Write exactly one assigned report under:

```text
dev/local-final-checks/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/
```

The timestamp contains no colons. Each evaluator report uses
`<evaluator-slug>-report.md`. The synthesizer writes `readiness-report.md`.
The fixer writes `repair-report.md`.

Every report names the base, head, evidence paths, completed checks, findings,
checks not run, and conclusion. Cite concrete paths and lines. Use Critical,
High, Medium, and Low from `auditor-conventions`.

## Empty and Partial Runs

- An empty range is a completed no-change result.
- A missing baseline or diff artifact makes the dependent check `NOT RUN`.
- An independent check continues after another check fails.
- A missing or incomplete required check prevents `GO`.
- A condition that does not apply is complete evidence, not `NOT RUN`.
- Missing optional synthesis enrichment does not prevent `GO`.

Treat a report as present only when it is readable, regular, non-empty, and
under the current run root. This validates metadata, not the report's claims.

## Read-Only Evaluation

Evaluators write reports only. They never edit source, install dependencies,
run state-changing commands, commit, push, or post externally. A shell-enabled
evaluator may use read-only commands for its assigned check.

Return only the report path, status, and key outcome or failure reason. Keep the
return to ten lines.
