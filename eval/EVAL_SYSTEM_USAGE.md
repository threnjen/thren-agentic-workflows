# Evaluation System Usage Guide

This guide explains how to run the phase evaluation system end-to-end once your pipeline and ledgers are in place.

## What This System Scores

The `05 Eval - Grader` agent scores a completed phase run by combining:

- a clean base branch
- a source-of-truth golden path branch
- a branch to evaluate
- diff(clean base -> golden path)
- diff(clean base -> branch to evaluate)
- `eval/runs/<phase-slug>/ledger-commits.jsonl` (commit timeline, written by git hook)
- `eval/runs/<phase-slug>/ledger-events.jsonl` (semantic failures, written by agents)
- A rubric YAML you provide

It writes a timestamped score report to:

- `eval/runs/<phase-slug>/score-report-<timestamp>.md`

It also appends one additive-only comparison row to:

- `eval/EVAL_GRADER_SCORE_HISTORY.md`

## 1) Prepare the Evaluation Set

### 1. Start from the correct baseline commit

Use the exact commit you want as the run baseline (usually the phase doc that has been refined and affirmed). If needed:

```bash
git checkout <baseline-sha>
```

Then create or resume a phase branch.

### 2. Branch naming convention (required)

Evaluation capture is active only on branches that start with `phase/`.

- Valid: `phase/01`, `phase/06d`, `phase/feature-eval-infra`
- Invalid for eval capture: `main`, `feature/x`, `bugfix/y`

The hook and agents normalize the branch into a run directory slug:

- Branch `phase/06d` -> run dir `eval/runs/phase-06d/`
- Branch `phase/feature/eval-infra` -> run dir `eval/runs/phase-feature-eval-infra/`

### 3. Install/verify hook and run directory

From the target repo:

```bash
ln -sfn "$HOME/github_repos/thren-agentic-workflows/eval/hooks/post-commit.sh" .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

Create run directory:

```bash
mkdir -p eval/runs/phase-06e
```

Do not write harness/model into ledger rows, score history, or other retained grading artifacts. If you want to track which harness/model produced each branch, keep that in your own comparison notes outside the retained eval artifacts.

Recommended explicit evidence for deterministic AC-level scoring:

- rubric fields such as `expected_commit_prefix`, `expected_commit_contains`, and `require_commit_evidence`
- explicit local notes when one-commit-per-ac or other cadence expectations matter

Recommended comparison metadata for branch-based grading:

- `comparison.clean_base_branch`
- `comparison.golden_path_branch`
- `comparison.evaluated_branch`
- `comparison.golden_diff_artifact_path`
- `comparison.evaluated_diff_artifact_path`

Recommended manual inputs when exact local evidence cannot be inferred from ledgers:

- `manual_inputs.initial_patch_passing_tests`
- `manual_inputs.initial_patch_test_source`

### 4. Commit naming conventions the evaluator expects

The canonical checkpoint commit messages are:

- `eval: plan-affirmed`
- `eval: phase-affirmed`
- `eval: features-decomposed`
- `eval: implement <feature-slug>` or `eval: implement <feature-slug> <criterion-id>`
- `eval: review <feature-slug>` or `eval: review <feature-slug> <criterion-id>`
- `eval: qa`
- `eval: final-review`

For AC-level runs, there should be one `eval: implement` checkpoint and one `eval: review` checkpoint per acceptance criterion, using the exact rubric or criterion ID token when available, for example `I03A7`. Raw plan-local labels such as `AC1` are only safe when paired with the feature slug. These messages make the timeline deterministic and easy to score.

## 2) Prepare the Rubric (After Gold Truth Is Established)

Once you have your "gold truth" expectations, encode them as explicit rubric criteria.

### Which file should I use?

Start from the seed file:

- `eval/rubrics/phase-eval-infrastructure-foundation.example.yaml`

Create a run-specific copy, for example:

- `eval/rubrics/phase-06d-planning-and-implementation.yaml`

### Rubric structure

Minimum shape:

```yaml
phase: phase-06d
criteria:
  - id: P01
    description: Planning phase doc contains objective, scope, dependencies, and measurable success criteria
    automatable: true
    check: Confirm required sections exist in docs/phases/PHASE_06D/PHASE_06D_SUMMARY.md.

  - id: I01
    description: Implementation artifacts exist for each feature and include AC traceability
    automatable: true
    check: Confirm each dev/feature/<task>/ has plan/context/tasks/implementation/review and implementation maps files to ACs.

  - id: H01
    description: Human reviewer confirms implementation quality meets team bar
    automatable: false
    requires_human: true
```

Recommended richer shape for AC-level runs:

```yaml
phase: phase-06e
criteria:
  - id: I03A7
    description: Dormant Purpose remains 50 across repeated rare ticks for every tier
    automatable: true
    feature_slug: 03-ambition-purpose-runtime
    ac_ref: I03A7
    planned_test_id: test_ac7_dormant_purpose_stays_50
    planned_test_pattern: DormantPurpose_StaysAt50_AllTiers
    expected_commit_prefix: "eval: implement 03-ambition-purpose-runtime"
    expected_commit_contains: "I03A7"
    require_commit_evidence: true
    require_test_evidence: true
    check: Confirm the runtime implementation, implementation record, and planned test evidence all support I03A7.
```

### Planning Doc rubric criteria patterns

Use IDs like `P01`, `P02`, `P03` and encode objective checks such as:

- required section presence
- explicit in-scope / out-of-scope boundaries
- dependency and risk sections present
- success criteria are testable
- wave ordering and feature decomposition guidance present

### Implementation rubric criteria patterns

Use IDs like `I01`, `I02`, `I03` for feature-level checks and IDs like `I03A7` for AC-level checks. Encode checks such as:

- each feature folder has required artifacts
- each AC row carries `feature_slug`, `ac_ref`, and planned test identifiers when available
- review verdicts are acceptable per policy
- checkpoint commits exist and follow canonical names
- implement and review commits can be associated to the exact AC when the run uses AC-level commit cadence
- ledger events include required schema fields
- final review and QA outputs exist (or skipped with explicit rationale)

### AC-level evidence contract (recommended)

For AC-granular runs, prefer the following rubric fields whenever the information exists:

- `feature_slug`
- `ac_ref`
- `planned_test_id`
- `planned_test_pattern`
- `expected_commit_prefix`
- `expected_commit_contains`
- `require_commit_evidence`
- `require_test_evidence`

These fields reduce heuristic matching and make grading deterministic even when ledger event rows are sparse.

### Human-review criteria

For any criterion not safely automatable, set:

```yaml
automatable: false
requires_human: true
```

The grader will place it under `[NEEDS_HUMAN_REVIEW]` instead of guessing.

### Rubric quality anchors (recommended)

When writing nuanced criteria, define what good looks like using a 0-5 quality anchor scale:

- `0`: missing or incorrect
- `1`: major gaps, low utility
- `2`: partial with serious omissions
- `3`: acceptable baseline, minor omissions
- `4`: strong and mostly complete
- `5`: complete, precise, decision-useful

Even if the Phase 01 grader outputs `PASS`/`FAIL`/`PARTIAL`, these anchors improve consistency when humans author and review rubric criteria.

## 3) Expected Files and Standards

### Required run files

Inside `eval/runs/<phase-slug>/`:

- `ledger-commits.jsonl`
- `ledger-events.jsonl` (may be absent if no failures were recorded)

### Ledger standards

- `ledger-commits.jsonl` rows come from the hook and include:
  - `sha`, `branch`, `message`, `timestamp`, `files`
- `ledger-events.jsonl` rows come from agents and include:
  - `task_slug`, `stage`, `detected_by`, `severity`, `evidence`, `first_seen_attempt`, `resolved_attempt`, `resolved_by`, `human_intervention_required`, `regression`, `propagated_from_stage`

Recommended enrichment for AC-level runs when event writers can provide it:

- `criterion_id` or `ac_ref`
- `planned_test_id`
- `planned_test_pattern`
- `related_commit_sha`

These fields are not mandatory for the grader to operate, but they substantially improve criterion-to-event association quality.

### Implementation record coverage contract

Implementation records should carry an AC coverage matrix so the grader has a deterministic fallback when commit or event evidence is incomplete. Recommended columns:

- `AC`
- `Criterion ID`
- `Planned Test ID`
- `Planned Test Pattern`
- `Implementing Files`
- `Evidence Paths`
- `Implement Commit SHA`
- `Review Commit SHA`

If a commit SHA is not yet known when the implementation record is first written, use `PENDING` and update it later in the pipeline.

### Branch gating standard

No `phase/*` branch means no commit ledger capture by the hook.

### Identity-separation standard

Do not store `harness`, `model`, or other runtime identity fields in ledgers, score history, or other retained grading artifacts. Track comparison identity outside those artifacts.

## 4) Run the Eval Grader

Use `05 Eval - Grader` with:

- rubric path
- clean base branch
- source-of-truth golden path branch
- branch to evaluate
- phase identifier (or include `phase` in rubric)
- target repository root (optional if current workspace is target)

Expected grader behavior:

1. Resolve `phase-slug` and locate the evaluated branch run dir
2. Materialize clean-base->golden and clean-base->evaluated diffs, optionally writing temporary diff artifacts
3. Load rubric + ledgers + any explicit local evidence artifacts
4. Build a comparative patch model and a unified timeline by commit SHA
5. Score automatable rubric criteria as `PASS` or `FAIL`
6. Produce a comparative scorecard across patch equivalence and execution-quality metrics
7. Emit manual checks as `[NEEDS_HUMAN_REVIEW]`
8. Write `score-report-<timestamp>.md` into the run dir

### Comparative scorecard dimensions

The grader now produces a branch-comparison scorecard in addition to the rubric verdict. The persistent history table stores these axes on a normalized `1-10` scale where `10` is best, with the golden path treated as the `10` baseline. It scores or reports:

- Parallel metric subagents score:
  - equivalence: how closely the evaluated patch matches the golden-path patch
  - clarity: human readability
  - coherence: internal consistency and style-fit with the repository
  - robustness: edge cases, boundary conditions, and failure-path coverage
  - bug risk
  - scope discipline: does only what is needed for the rubric and golden-path intent
  - footprint risk, including files touched per patch or per AC, lower is better
- The parent grader computes directly:
  - turns from ledger commits and activities, lower is better
  - initial patch passing tests, higher is better, usually supplied from Unity Test Runner
  - mean time per task from ledger timestamps, lower is better
  - overall review quality evaluation

`diff minimality` is not a separate axis. It is intentionally absorbed by `scope discipline` plus `footprint risk` to avoid double-counting change size.

### Persistent additive score history

After each grading run, append exactly one new row to:

- `eval/EVAL_GRADER_SCORE_HISTORY.md`

This file is intentionally simple Markdown. It is a persistent historical record, not a mutable dashboard.

Rules:

- append only
- never delete or rewrite prior rows
- never reorder rows
- use normalized `1-10` scores where `10` is best
- use `NHR` for score cells that remained `[NEEDS_HUMAN_REVIEW]`
- assume the golden path scores `10` on every axis
- preserve legacy schema rows and append new runs to the current schema section when the metric columns evolve

### Adopted report contract fields

For consistency across runs, ensure each score report clearly exposes these comparison-friendly fields:

- verdict
- phase slug
- rubric path
- automatable pass count and fail count
- human-review required count
- regression flag count
- AC commit coverage counts when the rubric is AC-granular
- unmatched or ambiguous AC evidence counts when present

These align with B001's decision-first reporting style while staying within Phase 01 scope.

### Optional comparison delta fields (recommended)

When you run explicit A/B comparisons, include these fields in the score report:

- `pass_rate_delta`
- `quality_delta`
- `compliance_violation_delta`
- `cost_per_pass_delta`
- `p50_latency_delta`
- `p90_latency_delta`
- `regressions_by_family`

## 4.1) Optional comparison notes

No retained run metadata artifact is required.

If you want rerun notes or comparison bookkeeping, keep them outside committed eval artifacts. Useful items to track include:

- clean base, golden path, and evaluated branch names
- diff artifact paths, when you materialize them ahead of grading
- expected commit cadence notes for AC-level runs
- `initial_patch_passing_tests` and its source when Unity Test Runner is authoritative
- any personal mapping from branch names to harness/model combinations

### Recommended promotion gates (adopted defaults)

Use these defaults unless your project explicitly overrides them:

- hard fail if hard-pass rate drops by more than `2.0%`
- non-inferiority quality floor: `quality_delta >= -0.10`
- non-inferiority hard-pass floor: `pass_rate_delta >= -1.0%`
- efficiency target: `cost_per_pass_delta >= 15%` improvement for optimization variants

## 5) Practical Checklist

Before scoring:

- Branch name starts with `phase/`
- Hook is installed and executable
- Clean base, golden path, and evaluated branches are all available locally
- Rubric file exists and points at the same phase slug
- Any explicit commit cadence expectation needed for AC-level scoring is available in the rubric or another local note
- Checkpoint commit messages follow canonical names
- Implementation records include AC coverage rows with planned test identifiers and evidence paths
- Initial patch passing test count is recorded when Unity Test Runner is the source of truth for that metric

After scoring:

- Read `Overall Verdict`
- Review `Failure Breakdown`
- Triage `[NEEDS_HUMAN_REVIEW]` items
- Decide `PASS`, `FAIL`, or `PARTIAL` promotion outcome

## 6) Common Mistakes to Avoid

- Running on non-`phase/*` branches and expecting ledgers
- Writing runtime identity into retained eval artifacts
- Writing fuzzy rubric checks with no local evidence path
- Treating human-review criteria as automatable
- Using AC-level commits without the exact criterion ID in implement/review commit messages
- Omitting planned test identifiers or AC coverage rows from implementation artifacts during AC-level runs
- Comparing branches without a clean base reference or without materializing both the golden and evaluated diffs
- Assuming the Unity Test Runner initial-pass count can be reconstructed from ledgers when no local artifact or manual input was recorded
- Reusing one rubric across unrelated phase slugs without edits

## 7) Suggested Naming Conventions

- Branch: `phase/<phase-id>`
- Run directory: `eval/runs/phase-<phase-id>/`
- Rubric file: `eval/rubrics/phase-<phase-id>-planning-and-implementation.yaml`
- Score report: `eval/runs/phase-<phase-id>/score-report-<timestamp>.md`

Additional deterministic conventions adopted from B001 style:

- Run ID: `PHASE-EVAL-<phase-id>-<YYYYMMDD-HHMMSS>`
- Optional run contract: `eval/runs/<phase-slug>/run-contract.json`

## 8) Cleanup And Retention Contract

After scoring, clean temporary scratch outputs but retain these artifacts:

- `eval/runs/<phase-slug>/ledger-commits.jsonl`
- `eval/runs/<phase-slug>/ledger-events.jsonl` (if present)
- `eval/runs/<phase-slug>/score-report-<timestamp>.md`
- `eval/runs/<phase-slug>/run-contract.json` (if used)

Never delete score reports during cleanup.
