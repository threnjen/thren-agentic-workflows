---
name: phase-final-review-conventions
description: "Shared conventions for Phase Final Review evaluators. Defines report contracts, severity handling, read-only boundaries, model tiers, and incomplete-run semantics. Use when: running or authoring any 05x Phase Final Review evaluator."
---
<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
# Phase Final Review Conventions

Shared conventions for the Phase Final Review evaluator family. Load this skill
before performing work for a multi-subphase phase. Apply
`auditor-conventions` for the shared audit constraints and report norms; this
skill defines only the whole-phase review contracts.

## Standard Constraints

- Complete every assigned check or record it as not run with a concrete reason.
- Read source files, diffs, worktrees, and subphase artifacts without modifying
  them.
- Write only the assigned report artifacts under the current review's report
  root: `dev/phase-final-review/PHASE_0N/`.
- Keep findings evidence-based and cite the input artifact, file, or report that
  supports each conclusion.
- Do not treat an unavailable evaluator, dependency, or worktree as a clean
  result.

## Report Locations and Naming

For a review of phase `PHASE_0N`, use:

```text
dev/phase-final-review/PHASE_0N/
├── 05a-baseline-worktree-report.md
├── 05b-change-narrator-report.md
├── 05c-qa-consolidator-report.md
├── 05d-security-rollup-report.md
├── 05e-ac-regression-report.md
├── 05f-seam-analyzer-report.md
├── 05g-artifact-sweeper-report.md
├── 05h-test-health-report.md
├── 05i-learnings-harvester-report.md
├── 05j-consistency-auditor-report.md
├── 05k-dependency-auditor-report.md
├── 05l-readiness-synthesizer-report.md
├── master-qa.md
├── security-rollup.md
├── ac-regression-matrix.md
└── readiness-report.md
```

Evaluator-specific reports use `<evaluator-slug>-report.md`. The four named
rollups are the canonical hand-off files for downstream evaluators and must
remain at the phase report root. A report for a discovered subphase may use a
subdirectory below the same root only when the invoking agent's contract calls
for one.

## Severity Levels

Use the four levels from `auditor-conventions` consistently:

| Level | Meaning in a whole-phase review |
|---|---|
| **Critical** | A direct security, data-loss, or release-blocking failure with no safe containment. |
| **High** | A material correctness, security, or operability failure that should block readiness until resolved or explicitly accepted. |
| **Medium** | A meaningful coverage, maintainability, reliability, or documentation concern that does not independently prove release failure. |
| **Low** | A minor consistency, clarity, or cleanup issue with limited operational impact. |

Order blocking findings from Critical to Low, then preserve source order within
the same level. Do not downgrade a missing check to a finding that looks clean.

## Read-Only Worktree Etiquette

- Treat the checked-out baseline worktree and the current source tree as
  read-only inputs.
- Do not edit, format, install into, commit in, or change branches in either
  worktree while evaluating.
- Put generated reports and temporary review notes under the declared review
  report root; do not place them in the baseline worktree.
- Reuse the `worktree-baseline` procedure for baseline creation and cleanup.
  Never remove a worktree that the caller did not create or explicitly assign
  for this run.
- If a read-only operation cannot be completed, record the check as not run
  and state the failed operation and its reason.

## Model Tiers

- The orchestrator should recommend or require a state-of-the-art model and
  warn when the active model is below that tier.
- Deep-judgment work—change narration, AC regression, seam analysis, and
  readiness synthesis—uses the top available tier.
- Mechanical sweeps—artifact, consistency, and dependency checks—may use a
  lower-cost tier when their agent contract permits it.
- A model-tier limitation is an execution condition to report, not evidence
  that an unrun check passed.

## Missing Artifacts and Preflight

An artifact is **missing** when a preflight-declared required path or artifact
category has no one readable, regular, non-empty file in the expected phase or
subphase location. A directory, broken link, unreadable file, empty file, or
file that cannot be identified as the declared artifact type counts as missing.
If multiple candidates exist but none is valid, report the category and every
candidate's rejection reason. Preflight must list each missing category and its
expected location before starting evaluators; it must not silently substitute a
different phase, stale report, or evaluator output.

The expected set is established by the phase's pipeline contract. Typical
inputs include implementation records, QA plans, QA coverage maps,
qa-analysis documents, summaries, and security scans. A fixture may document a
source-phase exception, but the exception must be explicit in its provenance
README and cannot be inferred from an empty directory.

## Partial-Failure Semantics

- The review run completes when an evaluator fails, crashes, loses a required
  dependency, or cannot access its assigned worktree. Remaining evaluators may
  continue.
- The orchestrator records the evaluator name, attempted check, failure reason,
  and resulting report path (if any) as **not run** or **incomplete**.
- `readiness-report.md` must contain an explicit **Checks Not Run** section
  listing exactly those checks and their reasons.
- A readiness verdict may not be **GO** while any required check is missing or
  incomplete. With no blockers found but incomplete coverage, the highest
  permitted outcome is a clearly labelled incomplete/no-blockers result below
  GO.
- A failed evaluator is not converted into a passing result by a missing report,
  an empty report, or a later evaluator's success.

## Return Summary Contract

Each evaluator returns only:

1. Its report path (or the explicit statement that no report was written).
2. A concise status and the key outcome or failure reason.

The return payload is at most **10 lines**. Full findings belong in the report
file, not in the return message. The orchestrator should pass the report path
and status to the next stage without copying the report into the conversation.

## Process

1. Confirm the assigned phase, subphase scope, input artifacts, model tier, and
   report destination.
2. Perform the complete assigned check against read-only inputs.
3. Write the required report, including evidence and any checks not run.
4. Return only the report path and a summary of no more than 10 lines.

## Handoff Checklist

- [ ] The report is under `dev/phase-final-review/PHASE_0N/`.
- [ ] Required evidence paths and severity labels are present.
- [ ] Failed or unavailable checks are explicitly marked not run/incomplete.
- [ ] No source or baseline worktree was modified.
- [ ] The return summary is no more than 10 lines.
