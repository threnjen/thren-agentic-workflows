# Agent Regression Benchmark Spec

Status: Draft v0.1
Last updated: 2026-04-22
Owner: Project maintainers

## 1. Purpose

Define a stable, repeatable benchmark harness that detects regressions when changing:

- Base LLM
- Custom agent instructions
- Prompt style (including token-minimized variants)
- Tool policies and orchestration flow

This benchmark is not a generic intelligence score. It is a project-specific go/no-go gate for changes that affect real workflows.

## 2. Scope

In scope:

- A/B and multi-variant comparisons
- Regression detection versus a pinned baseline
- Measurement of quality, compliance, latency, and cost
- Support for both full agent runs and direct model runs

Out of scope:

- Replacing public benchmarks
- Producing a universal one-number quality ranking
- Fully automated grading for all nuanced writing tasks

## 3. Core Principles

1. Immutability: Core benchmark tasks are never edited in place.
2. Reproducibility: Runs pin code revision, benchmark version, model, and run settings.
3. Representativeness: Task families mirror day-to-day work.
4. Anti-gaming: Hidden holdout tasks detect overfitting.
5. Decision-first reporting: Every run ends with pass/fail/review-required.

## 4. Benchmark Unit: Task Card

Each benchmark task is defined by a Task Card.

Required fields:

- `task_id`: globally unique and versioned (`B001-A03`, `B001-C07`)
- `family`: planning, decomposition, implementation, review, documentation, orchestration
- `difficulty`: S, M, L
- `prompt_package`: exact user request + context payload
- `constraints`: allowed tools, forbidden actions, policy constraints
- `expected_outcomes`: required artifacts and required decisions
- `scoring_mode`: deterministic, rubric, or hybrid
- `time_budget_s`: max runtime in seconds
- `token_budget`: max total input/output tokens
- `tags`: domain, risk class, failure mode

Optional fields:

- `fixtures`: files, branch, or synthetic inputs used during execution
- `reference_run_notes`: baseline observations

## 5. Task Families

Family A: Planning and scope refinement

- Clarify scope boundaries and non-goals
- Surface dependencies and edge cases
- Improve decomposition readiness

Family B: Decomposition and sequencing

- Split phase work into independent, testable feature slices
- Enforce dependency order and integration sequencing

Family C: Implementation quality

- Make focused code changes in realistic repo context
- Validate correctness with test/build checks
- Penalize unrelated churn

Family D: Review quality

- Identify real defects in proposed changes
- Penalize false positives and speculative issues
- Require severity and impact justification

Family E: Documentation maintenance

- Keep docs aligned with current code/repo state
- Preserve consistency across context and architecture docs

Family F: Tool-using orchestration

- Multi-step tasks requiring search, evidence gathering, and synthesis
- Score protocol compliance and completion quality

## 6. Dataset Design

Use three sets:

- Core Set (immutable): release gate tasks
- Shadow Set (mutable): candidate tasks under calibration
- Canary Set (fresh): tasks from recent failures/regressions

Versioning:

- Benchmark versions: `B001`, `B002`, ...
- Task IDs are never reused
- Published Core tasks are never edited in place
- Corrections produce a new task ID/version and deprecate the prior task

Suggested initial size:

- Core: 30 tasks
- Shadow: 20 tasks
- Canary: 10 tasks

## 7. Execution Protocol

For each experiment run:

1. Pin revisions: repo commit, benchmark version, harness version.
2. Pin runtime settings: model id, temperature, top_p, tool policy, budgets.
3. Run each task with repeats (`N=3` recommended).
4. Randomize task order per run.
5. Persist full traces, intermediate tool logs, and final outputs.

Fair A/B requirements:

- Change exactly one variable between A and B.
- Keep all other run settings identical.
- Use the same grader version.

## 8. Scoring Model

Per-task outputs:

- `hard_pass`: boolean
- `quality_score`: 0.0 to 5.0
- `compliance_score`: 0.0 to 5.0
- `latency_ms`
- `tokens_in`, `tokens_out`, `tokens_total`
- `cost_usd`

Suite aggregates:

- Hard pass rate
- Weighted quality mean
- Compliance violation count by severity
- Cost per passed task
- P50/P90 latency
- Regression counts by family

Recommended initial weighting:

- Correctness: 45%
- Quality: 25%
- Compliance: 20%
- Efficiency: 10%

## 9. Grading Strategy

Deterministic graders (preferred where possible):

- Schema and format checks
- Required decision/presence checks
- File and diff checks
- Build/test pass checks

Rubric graders (for nuanced tasks):

- Binary anchors per criterion
- Explicit evidence notes per score
- Optional second judge pass for tie-breaks

Human audit is required when:

- Delta is inside the gray zone
- High-severity regressions are detected
- Major prompt-style changes alter behavior profile

## 10. Regression Gates

Hard fail conditions:

- Hard pass rate drop exceeds threshold (initial recommendation: >2%)
- Increase in high-severity compliance violations
- Regression in any critical family (A, C, or D)

Non-inferiority rule for optimization changes:

- Quality delta must be >= -0.10 (0-5 scale)
- Hard pass delta must be >= -1.0%
- Cost per pass improvement must be >= 15%

If all three pass, optimization can be promoted.

## 11. Policy: Token-Minimized Prompt Style Experiments

For compressed or "caveman speak" prompt strategy changes:

1. Run on Core + Canary sets.
2. Compare success, quality, compliance, latency, and cost.
3. Reject if compliance/readability drops materially, even if cost improves.
4. Require two consecutive passing benchmark runs before promotion.

## 12. Anti-Gaming Controls

- Maintain hidden holdout tasks not exposed to prompt authors.
- Rotate holdout subset each benchmark version.
- Detect overfitting via divergence between Core and holdout performance.
- Flag suspicious gains for manual review.

## 13. Reporting Contract

Each run must produce:

- Verdict: `PASS`, `FAIL`, or `REVIEW_REQUIRED`
- Delta table versus baseline by family
- Top regressions with representative examples
- Cost/latency tradeoff summary
- Promotion recommendation

## 14. Governance

Roles:

- Benchmark Owner: curates tasks, versions, and thresholds
- Variant Author: proposes agent/model/prompt changes
- Reviewer: approves promotion or rollback
- Incident Lead: triages major regression failures

Controls:

- Threshold changes require documented rationale.
- Grader changes require replay on at least one previous benchmark version.

## 15. Rollout Plan

Phase 1 (Week 1):

- Build initial Core Set (30 tasks) from real recent work
- Capture baseline run for current production setup

Phase 2 (Weeks 2-3):

- Add deterministic graders for at least 50% of tasks
- Add repeat runs and confidence intervals

Phase 3 (Ongoing):

- Expand Core to 50-80 tasks
- Enforce benchmark gate for agent/prompt changes
- Refresh Canary tasks from new incidents

## 16. Acceptance Criteria For This Benchmark System

This spec is considered implemented when:

1. Two variants can be compared by one command/workflow.
2. Runs are reproducible and versioned.
3. Known historical regressions are detectable.
4. Output supports a clear go/no-go decision.
5. Cost-quality tradeoffs are explicit in reports.

## 17. Task Card Template

```yaml
task_id: B001-A01
family: planning
difficulty: M
prompt_package:
  user_request: |
    Refine this phase summary and identify missing edge cases.
  context_files:
    - docs/phases/PHASE_04/PHASE_04_SUMMARY.md
constraints:
  allowed_tools: [read_file, list_dir, grep_search]
  forbidden_actions: [source_code_edits]
  notes:
    - Must stay phase-level (no code-level API design)
expected_outcomes:
  required_sections:
    - strengths
    - gaps_to_explore
    - suggested_iteration_rounds
  quality_expectations:
    - identifies at least 3 meaningful scope risks
    - includes at least 2 edge/failure cases
scoring_mode: hybrid
time_budget_s: 900
token_budget: 45000
tags: [phase-refinement, scope-clarity, regression-critical]
```

## 18. Initial Seed Matrix (Example)

Use this as a starter map for `B001` composition.

- A-family (Planning): 8 tasks
- B-family (Decomposition): 5 tasks
- C-family (Implementation): 6 tasks
- D-family (Review): 5 tasks
- E-family (Documentation): 3 tasks
- F-family (Orchestration): 3 tasks

Total: 30 tasks
