# Evaluation System Usage Guide

This guide explains how to run the phase evaluation system end-to-end once your pipeline and ledgers are in place.

## What This System Scores

The `05 Eval - Grader` agent scores a completed phase run by combining:

- `eval/runs/<phase-slug>/ledger-commits.jsonl` (commit timeline, written by git hook)
- `eval/runs/<phase-slug>/ledger-events.jsonl` (semantic failures, written by agents)
- A rubric YAML you provide

It writes a timestamped score report to:

- `eval/runs/<phase-slug>/score-report-<timestamp>.md`

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
ln -sfn <absolute-path-to-github-agents-source-of-truth>/eval/hooks/post-commit.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

Create run directory and metadata:

```bash
mkdir -p eval/runs/phase-<slug>
cat > eval/runs/phase-<slug>/run-config.yaml <<'EOF'
runtime:
  harness: copilot
  model: <exact-current-model-label>
EOF
```

Keep `runtime.harness` and `runtime.model` identical throughout one run. Do not rename or restyle them between events.

### 4. Commit naming conventions the evaluator expects

The canonical checkpoint commit messages are:

- `eval: plan-affirmed`
- `eval: phase-affirmed`
- `eval: features-decomposed`
- `eval: implement <feature-slug>`
- `eval: review <feature-slug>`
- `eval: qa`
- `eval: final-review`

These messages make the timeline deterministic and easy to score.

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
harness: copilot
model: GPT-5.3-Codex (copilot)
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

### Planning Doc rubric criteria patterns

Use IDs like `P01`, `P02`, `P03` and encode objective checks such as:

- required section presence
- explicit in-scope / out-of-scope boundaries
- dependency and risk sections present
- success criteria are testable
- wave ordering and feature decomposition guidance present

### Implementation rubric criteria patterns

Use IDs like `I01`, `I02`, `I03` and encode checks such as:

- each feature folder has required artifacts
- review verdicts are acceptable per policy
- checkpoint commits exist and follow canonical names
- ledger events include required schema fields
- final review and QA outputs exist (or skipped with explicit rationale)

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

- `run-config.yaml`
- `ledger-commits.jsonl`
- `ledger-events.jsonl` (may be absent if no failures were recorded)

### Ledger standards

- `ledger-commits.jsonl` rows come from the hook and include:
  - `sha`, `branch`, `message`, `timestamp`, `files`
- `ledger-events.jsonl` rows come from agents and include:
  - `task_slug`, `harness`, `model`, `stage`, `detected_by`, `severity`, `evidence`, `first_seen_attempt`, `resolved_attempt`, `resolved_by`, `human_intervention_required`, `regression`, `propagated_from_stage`

### Branch gating standard

No `phase/*` branch means no commit ledger capture by the hook.

### Metadata consistency standard

For one run directory, reuse the same `harness` and `model` values in all event rows.

## 4) Run the Eval Grader

Use `05 Eval - Grader` with:

- rubric path
- phase identifier (or include `phase` in rubric)
- target repository root (optional if current workspace is target)

Expected grader behavior:

1. Resolve `phase-slug` and locate run dir
2. Load rubric + ledgers + run metadata
3. Build a unified timeline by commit SHA
4. Score automatable criteria as `PASS` or `FAIL`
5. Emit manual checks as `[NEEDS_HUMAN_REVIEW]`
6. Write `score-report-<timestamp>.md` into the run dir

### Adopted report contract fields

For consistency across runs, ensure each score report clearly exposes these comparison-friendly fields:

- verdict
- phase slug
- rubric path
- harness and model (rubric + run metadata, when present)
- automatable pass count and fail count
- human-review required count
- regression flag count

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

## 4.1) Reproducibility run config (adopted standard)

Create a run config file for each evaluation run by copying:

- `eval/PHASE_EVAL_RUN_CONFIG.example.yaml`

Suggested naming:

- `eval/runs/<phase-slug>/run-config.yaml`

Use this file to pin baseline SHA, rubric path, model label, and grading inputs for reruns.

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
- `run-config.yaml` exists with stable harness/model
- Rubric file exists and points at the same phase slug
- Checkpoint commit messages follow canonical names

After scoring:

- Read `Overall Verdict`
- Review `Failure Breakdown`
- Triage `[NEEDS_HUMAN_REVIEW]` items
- Decide `PASS`, `FAIL`, or `PARTIAL` promotion outcome

## 6) Common Mistakes to Avoid

- Running on non-`phase/*` branches and expecting ledgers
- Changing model label mid-run in metadata/events
- Writing fuzzy rubric checks with no local evidence path
- Treating human-review criteria as automatable
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

- `eval/runs/<phase-slug>/run-config.yaml`
- `eval/runs/<phase-slug>/ledger-commits.jsonl`
- `eval/runs/<phase-slug>/ledger-events.jsonl` (if present)
- `eval/runs/<phase-slug>/score-report-<timestamp>.md`
- `eval/runs/<phase-slug>/run-config.yaml` (if used)
- `eval/runs/<phase-slug>/run-contract.json` (if used)

Never delete score reports during cleanup.
