---
name: pr-review-conventions
description: "Shared conventions for PR Review evaluators. Defines report contracts, severity handling, read-only boundaries, model tiers, and incomplete-run semantics for a review scoped to the diff between a base commit and a head commit. Use when: running or authoring any PR Review evaluator."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# PR Review Conventions

Shared conventions for the PR Review evaluator family. Load this skill before
performing work for a review scoped to the diff between a base commit and a
head commit. Apply `auditor-conventions` for the shared audit constraints and
report norms; this skill defines only the branch-diff review contracts.

## Standard Constraints

- Complete every assigned check or record it as not run with a concrete reason.
- Read source files, diffs, worktrees, and any available pipeline artifacts
  without modifying them.
- Write only the assigned report artifacts under the current review's report
  root: `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`.
- Keep findings evidence-based and cite the input artifact, file, or report that
  supports each conclusion.
- Do not treat an unavailable evaluator, dependency, or worktree as a clean
  result.

## Evidence Scope: the Diff Is the Subject

The reviewed change is the diff between the caller-supplied base commit and the
head commit. An evaluator's findings come from that diff and the trees on either
side of it.

**Pipeline artifacts are optional enrichment.** Implementation records, plans,
QA documents, and security reports may exist for a change, and an evaluator
should use them when they do. But a run **proceeds on the diff alone** when they
do not, and the report **names which evidence was unavailable** in its Checks
Not Run section.

This is a contract, not a preference. It is the recorded boundary that keeps PR
Review from duplicating `prod-code-review`, which is the pipeline-artifact gate.
PR Review must stay able to review any branch, including one produced without
the pipeline. An evaluator that refuses to run without artifacts has become a
second copy of `prod-code-review`; an evaluator that quietly omits the artifacts
it never found has hidden its own coverage gap instead. Optional is not the same
as ignorable — unavailable evidence is named, never assumed clean.

## Report Locations and Naming

Reports for a run go under a root keyed by the base commit and the run's start
time:

```text
dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/
├── 05a-baseline-worktree-report.md
├── 05b-change-narrator-report.md
├── 05c-artifact-sweeper-report.md
├── 05d-consistency-auditor-report.md
├── 05e-dependency-auditor-report.md
├── 05f-test-health-report.md
├── 05g-readiness-synthesizer-report.md
└── readiness-report.md
```

The root key is a short base SHA plus a UTC timestamp. No path component carries
a branch name: a run is identified by what it reviewed and when, both of which
are stable and unique, while a branch name is neither.

Evaluator-specific reports use `<evaluator-slug>-report.md`.
`readiness-report.md` is the canonical hand-off file for the orchestrator and
must remain at the report root.

## Tone: Write for the Author

This review is a self-check the author runs before opening a PR, so the reader
is the author of the change. Write findings in plain, natural language: say what
to check or fix in ordinary words, and lead with that rather than a severity
code or dense technical phrasing. Severity labels still exist for ordering and
evidence, but they support the plain-language point — they are not the headline.
Prefer a short, skimmable summary (a TL;DR) over exhaustive prose wherever the
report structure allows one.

## Severity Levels

Use the four levels from `auditor-conventions` consistently:

| Level | Meaning in a branch-diff review |
|---|---|
| **Critical** | A direct security, data-loss, or release-blocking failure with no safe containment. |
| **High** | A material correctness, security, or operability failure that should block the merge until resolved or explicitly accepted. |
| **Medium** | A meaningful coverage, maintainability, reliability, or documentation concern that does not independently prove the change unsafe. |
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
- A narrowly scoped capability is always preferred to a broad grant: read a file
  rather than shelling out to read it, and scope any command that is genuinely
  required to the specific check it serves.
- If a read-only operation cannot be completed, record the check as not run
  and state the failed operation and its reason.

## Model Tiers

- The orchestrator should recommend or require a state-of-the-art model and
  warn when the active model is below that tier.
- Deep-judgment work—change narration and readiness synthesis—uses the top
  available tier.
- Mechanical sweeps—artifact, consistency, and dependency checks—may use a
  lower-cost tier when their agent contract permits it.
- A model-tier limitation is an execution condition to report, not evidence
  that an unrun check passed.

## Missing and Unreadable Inputs

An input is **missing** when a path an evaluator's contract requires has no one
readable, regular, non-empty file at its expected location. A directory, broken
link, unreadable file, empty file, or file that cannot be identified as the
declared input type counts as missing.

A missing *optional* artifact is not a failure: it is named in the report's
Checks Not Run section and the run continues on the diff. A missing *required*
input is a check that did not run, and is reported as such. Neither is ever
silently substituted with a different revision, a stale report, or another
evaluator's output.

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

1. Confirm the assigned base and head commits, input artifacts, model tier, and
   report destination.
2. Perform the complete assigned check against read-only inputs.
3. Write the required report, including evidence and any checks not run.
4. Return only the report path and a summary of no more than 10 lines.

## Handoff Checklist

- [ ] The report is under `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`.
- [ ] Required evidence paths and severity labels are present.
- [ ] Failed or unavailable checks are explicitly marked not run/incomplete.
- [ ] Unavailable optional artifacts are named, not silently omitted.
- [ ] No source or baseline worktree was modified.
- [ ] The return summary is no more than 10 lines.
