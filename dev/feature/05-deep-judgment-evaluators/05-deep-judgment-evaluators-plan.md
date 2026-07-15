# Feature Plan: 05-deep-judgment-evaluators

## Execution Metadata

- **Wave:** 5
- **Parallel safe:** no
- **Depends on:** 01-review-foundation, 02-final-review-orchestrator
- **Key files modified:** `.github/agents/05b-change-narrator.agent.md` (new), `.github/agents/05e-ac-regression.agent.md` (new), `.github/agents/05f-seam-analyzer.agent.md` (new), `.github/agents/README.md` (agent inventory update), propagated outputs (generated), `scripts/propagate_master_assets.py` (verify — no change expected)
- **Sequential reason:** shares propagated output files with all sibling features; contract dependency on features 01 and 02

## A. Requirements & Traceability

Source: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`, Deliverable 5 and the In Scope roster entries for 05b, 05e, 05f.

Acceptance criteria:

- **AC1**: `05b-change-narrator.agent.md` exists: produces the whole-phase change narrative baseline→HEAD with per-subphase attribution and multi-subphase churn hotspots; chunks diffs internally and may spawn per-directory readers to stay within context discipline. Top-tier model declaration.
- **AC2**: `05e-ac-regression.agent.md` exists: re-verifies EVERY subphase's acceptance criteria against the FINAL codebase, spawning one hidden verifier per subphase; output is the AC-regression matrix from `phase-final-review-report` covering every AC with a pass/fail/not-verifiable status.
- **AC3**: `05f-seam-analyzer.agent.md` exists: analyzes integration seams between subphases — interface mismatches, duplicated logic, orphaned scaffolding — built on code-review-graph tools (`get_impact_radius`, `get_bridge_nodes`), degrading to a not-run record with reason when the graph is unavailable.
- **AC4**: All three load `phase-final-review-conventions`, use the baseline worktree from `05a-baseline-worktree` where a baseline view is needed (05b), honor report locations and the ≤10-line return contract, and follow partial-failure semantics.
- **AC5**: Each dry-runs via the orchestrator against the development fixture; 05e's matrix covers every AC from both pseudo-subphases' summaries with no AC silently omitted.
- **AC6**: Propagation picks up all three agents; `tests/test_propagate_master_assets.py` passes.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1–AC4 | the three agent files in `.github/agents/` | Code-review evidence only |
| AC5 | fixture dry-run outputs under `dev/phase-final-review/` | Manual QA: dry-run with AC-coverage completeness count |
| AC6 | propagation outputs | Existing automated test: `tests/test_propagate_master_assets.py` |

Non-goals:

- No fixing of regressions or seams found — reporting only.
- No re-running of automated test suites by 05e (it verifies ACs by inspection and existing evidence; live test execution belongs to the target repo's own pipeline and to 05h's delegate).
- No graph-server changes.

## B. Correctness & Edge Cases

- 05b on a very large phase diff: must chunk by directory/subphase and never load the full diff into one context; per-directory reader spawning is the pressure valve.
- 05e AC wording that is untestable-by-inspection (e.g., manual-QA-only criteria): mark not-verifiable with reason — never silently pass; the count of not-verifiable ACs must surface in the matrix summary.
- 05e later-subphase-broke-earlier-AC case: the matrix must attribute the regression to the breaking subphase when the narrative/commit evidence supports it, else mark attribution unknown.
- 05f on subphases with no shared surface: report "no seams detected" as a completed check.
- Baseline worktree unavailable: 05b reports not-run; 05e and 05f can proceed (they evaluate the final tree) and must say the baseline comparison was skipped.

## C. Consistency & Architecture Fit

- Lettered-subagent house style per `04a`–`04d`; hidden-verifier spawning phrased like existing orchestrator delegation patterns.
- Consume: conventions + report skills and fixture (feature 01), `05a-baseline-worktree` and `worktree-baseline` skill (feature 01), orchestrator invocation shape (feature 02).
- Graph tool names `get_impact_radius` and `get_bridge_nodes` copied exactly from the Phase document and verified against this workspace's code-review-graph server.

## D. Clean Design & Maintainability

- Simplest design: three agents, each a judgment procedure + template reference; chunking/verifier-spawning rules stated as constraints, not elaborate protocols.
- Complexity risk: 05e is the most intricate (per-subphase verifiers + roll-up). Keep the verifier contract identical to the evaluator contract: report to disk, ≤10-line return.
- Keep-it-clean: attribution vocabulary (regressed-by, unknown) defined in the report skill's matrix template, not per-agent.

## E. Completeness: Observability, Security, Operability

- Observability: reports on disk; no logging. Correct decision.
- Security: read-only; worktree etiquette per `worktree-baseline`.
- Runbook: deploy = propagation; verify = fixture dry-runs; rollback = git revert.

## F. Test Plan

- Must-have automated tests: propagation suite (existing).
- Manual QA checks:
  1. Given the fixture and a confirmed baseline, when 05b runs, then the narrative attributes changes to each pseudo-subphase and lists any file touched by both as a churn hotspot, with the run visibly chunked (no single full-diff read).
  2. Given the fixture summaries' ACs (count them first), when 05e runs, then the matrix row count equals the total AC count and every row has a status; manual-QA-only ACs are marked not-verifiable.
  3. Given the fixture, when 05f runs with the graph available, then a seam report exists; when the graph is stopped, then a not-run record with reason is produced instead.
  4. Given all three return, then each return summary is ≤10 lines with detail on disk.

## Stage 0: Test Prerequisites

Not required — markdown assets; propagation suite exists.

## Stage 1: 05b Change Narrator

**Goal**: AC1.
**Success Criteria**: Manual QA check 1 passes.
**Status**: Not Started

## Stage 2: 05e AC Regression

**Goal**: AC2.
**Success Criteria**: Manual QA check 2 passes — full AC coverage, no omissions.
**Status**: Not Started

## Stage 3: 05f Seam Analyzer

**Goal**: AC3.
**Success Criteria**: Manual QA check 3 passes in both graph states.
**Status**: Not Started

## Stage 4: Propagation

**Goal**: AC6.
**Success Criteria**: Propagation suite passes; agents in all harness outputs.
**Status**: Not Started

## Relationships to Sibling Plans

- Depends on 01 (contracts, fixture, worktree baseline) and 02 (orchestrator).
- 05e's matrix and 05f's seam report are primary inputs to feature 06's synthesis; 05b's narrative gives 06 its attribution backbone.

## Unverified Assumptions

- The fixture's pseudo-subphase summaries contain enumerable ACs (Phase 01/02 summaries use checkbox success criteria — verified); if any fixture AC is phase-meta rather than code-verifiable, 05e marks it not-verifiable rather than the fixture being altered.
