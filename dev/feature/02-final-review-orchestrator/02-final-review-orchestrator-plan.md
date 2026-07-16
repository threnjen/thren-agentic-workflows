# Feature Plan: 02-final-review-orchestrator

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** no
- **Depends on:** 01-review-foundation
- **Key files modified:** `.github/agents/05-phase-final-review.agent.md` (new), `.github/agents/README.md` (agent inventory update), propagated outputs under `.claude/agents/` and Codex/OpenCode equivalents (generated), `scripts/propagate_master_assets.py` (verify — no change expected)
- **Sequential reason:** shares propagated output files with all sibling features; contract dependency on 01-review-foundation skills

## A. Requirements & Traceability

Source: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`, Deliverable 2 plus the In Scope bullets for preflight, partial-failure semantics, and verdict lifecycle.

Acceptance criteria:

- **AC1**: `05-phase-final-review.agent.md` exists in `.github/agents/`, follows the numbered-orchestrator house style of `04-phase-execute.agent.md`, and loads `phase-final-review-conventions`.
- **AC2**: Context discipline is explicit: the orchestrator never reads code, diffs, or full subphase docs — only structured reports under `dev/phase-final-review/PHASE_0N/`; it enforces the ≤10-line return-summary contract on every subagent it spawns.
- **AC3**: Preflight auto-suggests the pre-phase baseline commit (last commit before subphase a's first feature commit), requires user confirmation, and derives the suggestion from ledger files (`ledger-commits.jsonl`/`ledger-events.jsonl` under `eval/runs/`) when present, falling back to commit-message conventions (the `eval:`-prefixed checkpoint commits) when ledgers are absent. The fallback path is documented as a first-class path, not an error path.
- **AC4**: Preflight discovers subphases from `docs/phases/PHASE_0N*/` directory patterns, inventories required pipeline artifacts per subphase (implementation records, QA docs, security reports, per the conventions skill's missing-artifact definition), and refuses to proceed with a clear itemized message when any required artifact is missing.
- **AC5**: The orchestrator warns at startup when not running on a state-of-the-art model, and declares the model-tier assignment: deep-judgment evaluators (05b, 05e, 05f, 05l) on top tier; mechanical sweeps (05g, 05j, 05k) on a cheap tier.
- **AC6**: Partial-failure semantics are implemented as orchestration rules: an evaluator failure does not abort the run; the failure is recorded (evaluator name + reason) and passed to synthesis; the orchestrator never reports GO while any check is missing.
- **AC7**: Verdict lifecycle: on completion the orchestrator updates the phase's status line in `docs/phases/PROJECT_ROADMAP.md` and the phase summary with the go/no-go verdict, and states the full-re-run policy (after remediation, the entire review re-runs; no partial re-run).
- **AC8**: Propagation picks up the agent into all three harness outputs and `tests/test_propagate_master_assets.py` passes.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1, AC2, AC5, AC6, AC7 | `.github/agents/05-phase-final-review.agent.md` | Code-review evidence only (agent markdown) |
| AC3 | agent preflight section | Manual QA: run preflight against this repo's history with `eval/runs/` present, then with it emptied |
| AC4 | agent preflight section | Manual QA: run preflight against the 01-review-foundation fixture with one artifact removed |
| AC8 | propagation outputs | Existing automated test: `tests/test_propagate_master_assets.py` |

Non-goals:

- No evaluator subagent authoring (features 03–05) and no synthesizer (feature 06).
- No "combine sibling phases" mode; no partial re-run machinery (phase-level out-of-scope).
- No changes to the eval-grader agent or eval hooks.

## B. Correctness & Edge Cases

- Ledger present but malformed/empty: treat as ledger-absent and use the commit-message fallback; say which path was used.
- No `eval:`-prefixed commits found on the branch (fallback exhausted): present candidate commits and require the user to pick — never guess silently.
- Zero subphase directories discovered: refuse with a message pointing at `prod-code-review` as the right tool for single, un-subdivided phases (phase-level out-of-scope boundary).
- Evaluator that hangs vs. fails: orchestrator instructions must bound waiting behavior and record a not-run entry either way.
- Verdict write-back must edit only the target phase's status line — never restructure the roadmap (mirrors the phase-refiner roadmap-editing rule).
- Re-invocation after a completed run: prior reports exist under `dev/phase-final-review/PHASE_0N/`; the orchestrator must define whether it archives or overwrites, deterministically (suggested: timestamped run subdirectory `[PROPOSED - name TBD]`).

## C. Consistency & Architecture Fit

- House style: numbered orchestrator (`04-phase-execute.agent.md` as the model), delegation phrasing consistent with `implementation-pipeline-loop` skill conventions.
- Consumes contracts published by 01-review-foundation: report locations/naming, missing-artifact definition, ≤10-line contract, worktree-baseline procedure (delegated to `05a-baseline-worktree`).
- Publishes contracts consumed downstream: the evaluator invocation prompt shape and the not-run record format (consumed by features 03–06). These belong in this agent's instructions and must align with `phase-final-review-conventions`.

## D. Clean Design & Maintainability

- Simplest design: one agent file; all shared rules live in the conventions skill, referenced not restated.
- Complexity risk: preflight is the densest part — keep it a linear checklist (baseline → subphases → artifact inventory → model check) with one loud failure mode per step.
- Keep-it-clean: no duplicated report templates (they live in `phase-final-review-report`); no evaluator-specific logic in the orchestrator.

## E. Completeness: Observability, Security, Operability

- Observability: the orchestrator's run record is its report directory; no logging machinery. Correct decision — agent markdown has no runtime logging surface.
- Security: read-only against code; write access limited to `dev/phase-final-review/` and the two planning-doc status lines (AC7).
- Runbook: deploy = propagation; verify = manual preflight QA runs; rollback = git revert.

## F. Test Plan

- Must-have automated tests: propagation suite (existing).
- Manual QA checks (top value):
  1. Given ledgers exist for a phase run, when preflight runs, then the suggested baseline matches the last commit before the phase's first feature commit and the user is asked to confirm.
  2. Given `eval/runs/` is empty, when preflight runs, then a baseline is still suggested from `eval:` commit-message conventions and the fallback is named in output.
  3. Given the fixture with one required artifact deleted, when preflight runs, then the run refuses with an itemized missing-artifact message.
  4. Given a wrong-model session, when the orchestrator starts, then a model-tier warning is emitted before any work.
  5. Given a simulated evaluator failure record, when the run completes, then the not-run check is named and the verdict is not GO.
- Fixtures: the 01-review-foundation fixture; this repo's own `eval/runs/` history.

## Stage 0: Test Prerequisites

Not required — markdown asset; propagation suite exists.

## Stage 1: Orchestrator Skeleton

**Goal**: Agent file with role, context discipline, model-tier policy (AC1, AC2, AC5).
**Success Criteria**: File exists, house-style compliant, conventions skill loaded.
**Status**: Not Started

## Stage 2: Preflight

**Goal**: Baseline suggestion with ledger fallback, subphase discovery, artifact inventory (AC3, AC4).
**Success Criteria**: Manual QA checks 1–3 pass.
**Status**: Not Started

## Stage 3: Run Semantics and Verdict Lifecycle

**Goal**: Partial-failure rules, verdict write-back, full-re-run policy (AC6, AC7).
**Success Criteria**: Manual QA check 5 passes; write-back edits only the status lines.
**Status**: Not Started

## Stage 4: Propagation

**Goal**: Propagate and verify (AC8).
**Success Criteria**: Propagation suite passes; agent present in all harness outputs.
**Status**: Not Started

## Relationships to Sibling Plans

- Depends on 01-review-foundation (conventions/report/worktree contracts, fixture).
- Features 03–05 dry-run their evaluators through this orchestrator; feature 06's full dry run exercises every rule here end-to-end.

## Unverified Assumptions

- The `eval:` commit-message convention (`eval: phase-affirmed`, `eval: features-decomposed`, per-feature checkpoints) is stable enough to anchor the ledger-absent fallback; verified for Phases 01/02 history, assumed for future runs.
