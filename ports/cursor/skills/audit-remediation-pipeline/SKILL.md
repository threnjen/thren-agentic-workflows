---
name: audit-remediation-pipeline
description:
  "Contract for driving confirmed audit findings through implementation, review,
  consolidated QA, and a pre-production gate. Use when an audit orchestrator has
  presented findings and the user has approved automated remediation."
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Audit Remediation Pipeline

Runs only after an audit's findings are presented and the user approves
remediation. The root orchestrator spawns every agent below; none spawns
another. If the user declines, the audit deliverables are complete — stop.

`[audit-name]` and its output directory are supplied by the caller.

Load `auditor-conventions` first. Implementation is not a second chance to
validate weak findings: admit work only after the audit finding truth gate has
proved a reachable production path, material consequence, contract, identity,
scope, and bounded verification.

## 1. Offer

> **Would you like me to implement the fixes?**
>
> I'll create task files from the audit findings and run each through the
> implementation, review, and QA pipeline.

## 2. Working branch

Create a branch using prefix `audit/<audit-type>-<audit-name>`. See auto-loaded
orchestrator conventions for the full procedure.

## 3. Task files

Convert findings into actionable task file sets, grouping related findings into
independently implementable tasks (all type-hint findings in one, all secrets
findings in another). Per task, write a three-file plan set in
`dev/[audit-name]/[task-name]/`:

- `[task-name]-plan.md` — what to fix, acceptance criteria derived from findings
- `[task-name]-context.md` — affected files and findings with `file:line` refs
- `[task-name]-tasks.md` — ordered implementation steps

**Source precedence.** Use the best available input, in order: a FINAL
fix-research index's suggested remediation order — its work items are already
grouped by root cause and linked to subsystem reports; then a delta's Residual
Risk section, which distinguishes findings already closed from those still open;
then the raw audit report.

Before creating tasks, verify the selected source names the examined revision,
its counts reconcile, and every included finding passes the audit finding truth
gate. Do not implement omitted, `Open`, out-of-scope, unreachable, immaterial,
or purely stylistic items. A `Partial` item becomes a task only for its supported
in-scope portion, with the residual risk kept explicit. If the best source lacks
this evidence, return it to remediation research; do not infer a fix from the
finding's title or severity.

## 4. Implementation loop

For each task in priority order, load the `implementation-pipeline-loop` skill
and execute Steps A through D with `dev/[audit-name]/[task-name]/` as
`[plan-path]` and `[task-name]` as the task identifier. Test failures are
handled by that skill's Test Failure Handling section.

## 4a. Per-task diff security scan

Run this after each task's review closes and before its commit checkpoint. The
implementation loop defines no security step, so this pipeline owns it.

Spawn **03e Diff Security Scan**:

> "[SUBAGENT-MODE] Perform a diff-scoped security scan for the task at
> `dev/[audit-name]/[task-name]/`. Scan ONLY these changed files, taken from the
> 'Files Changed' table in
> `dev/[audit-name]/[task-name]/[task-name]-implementation.md`: [list of changed
> file paths]. Write the report to
> `dev/[audit-name]/[task-name]/[task-name]-security.md`. Do not modify source
> code or reveal secret values. Return the report path, verdict, severity
> totals, and any Critical/High findings."

After the subagent returns, verify the report exists and record the verdict. On a
**BLOCKED** verdict, log it and proceed — the pre-production gate surfaces it as a
blocker. Do NOT auto-remediate security findings here.

Do not stage the report. It lives under `dev/`, which no checkpoint stages.

## 5. Consolidated QA

After every task is implemented and reviewed, spawn **Feature - QA Writer**:

> "Write the consolidated release QA documents covering ALL tasks in this audit
> remediation. Read all documents (plan, context, tasks, implementation record,
> review record) and source code from the following task folders: [list all
> `dev/[audit-name]/[task-name]/` paths]. Write the manual QA plan to
> `dev/[audit-name]/[audit-name]-qa.md`, the automated QA document to
> `dev/[audit-name]/[audit-name]-qa-automated.md`, and the coverage map to
> `dev/[audit-name]/[audit-name]-coverage-map-qa.md`. Sort every check: a command
> with a deterministic expected result belongs in the automated document, not on
> a human's checklist. If a QA file already exists, merge new coverage into it.
> Return both document paths, the automated/hybrid/manual counts, and a summary
> of what manual QA remains."

Verify the manual QA plan and the coverage map exist.

Then, **only when the automated QA document exists**, spawn **Feature - QA Runner**:

> "[SUBAGENT-MODE] Execute the automated QA document at
> `dev/[audit-name]/[audit-name]-qa-automated.md`. Repository root: [absolute
> repository path]. Evidence directory: [an untracked directory outside the
> source tree]. Run every check, compare actual output to each stated expected
> result, and record per-check status plus the Run results section back into that
> document. Modify nothing else, and do not fix any defect a check exposes.
> Return the verdict, per-status counts, the evidence directory, and the decisive
> reason."

Record the verdict and carry a `FAIL` into the final review as a blocker. Do not
remediate here. When no automated document was written, record
`automated-qa-run: N/A (no automated checks)` and continue.

Never hand the user a command this step could have run.

## 6. Final review

Spawn **Prod Code Review**:

> "Perform the final pre-production readiness analysis for the audit
> remediation. The following task folders contain all pipeline documents: [list
> all `dev/[audit-name]/[task-name]/` paths]. The manual QA plan is at
> `dev/[audit-name]/[audit-name]-qa.md`. The automated QA document, with its run
> results, is at `dev/[audit-name]/[audit-name]-qa-automated.md`, or none was
> written. Cross-validate all documents, verify
> implementations, run tests, and evaluate QA plan completeness. Write the
> analysis to `dev/[audit-name]/[audit-name]-qa-analysis.md`. Return the verdict
> (GO / GO WITH CONDITIONS / NO-GO) and a summary of findings."

## 7. Report

Use the Pipeline Completion Report format from the auto-loaded orchestrator
conventions, with scope label **Audit**, items label **Tasks completed**, and
the QA document path `dev/[audit-name]/[audit-name]-qa.md`.

## 8. Documentation

Follow the Post-Loop: Documentation Update section of
`implementation-pipeline-loop`:

> "[SUBAGENT-MODE] The following audit remediation has just been completed:
> [audit-name] ([CODE / INFRA / REFACTOR / SECURITY]). Tasks completed: [list
> task names]. Update any stale documentation across the repository. Return a
> summary of which documents were updated and what changed."
