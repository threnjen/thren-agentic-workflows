# Feature Plan: 03-mechanical-evaluators

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** no
- **Depends on:** 01-review-foundation, 02-final-review-orchestrator
- **Key files modified:** `.github/agents/05g-artifact-sweeper.agent.md` (new), `.github/agents/05j-consistency-auditor.agent.md` (new), `.github/agents/05k-dependency-auditor.agent.md` (new), `.github/agents/README.md` (agent inventory update), propagated outputs (generated), `scripts/propagate_master_assets.py` (verify — no change expected)
- **Sequential reason:** shares propagated output files with all sibling features; contract dependency on features 01 and 02

## A. Requirements & Traceability

Source: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`, Deliverable 3 and the In Scope roster entries for 05g, 05j, 05k.

Acceptance criteria:

- **AC1**: `05g-artifact-sweeper.agent.md` exists: sweeps for debug statements, TODOs/FIXMEs, temporary feature flags, and commented-out/dead code introduced since baseline, using code-review-graph `refactor_tool` dead-code detection scoped to the phase diff. Cheap-tier declaration in frontmatter/instructions.
- **AC2**: `05j-consistency-auditor.agent.md` exists: detects convention drift across subphases (naming, error handling, patterns) and recommends canonical forms.
- **AC3**: `05k-dependency-auditor.agent.md` exists: inventories new dependencies introduced across the phase and reports licenses, vulnerabilities, and competing/duplicate libraries. Cheap-tier.
- **AC4**: All three load `phase-final-review-conventions`, write reports to the conventions-defined location using `phase-final-review-report` structures where applicable, return ≤10-line summaries, and degrade per partial-failure semantics when a dependency (e.g., the graph server) is unavailable — reporting not-run with a stated reason rather than silently skipping.
- **AC5**: Each evaluator dry-runs through the `05-phase-final-review` orchestrator against the development fixture and produces a report file in the expected location.
- **AC6**: Propagation picks up all three agents; `tests/test_propagate_master_assets.py` passes.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1–AC4 | the three agent files in `.github/agents/` | Code-review evidence only |
| AC5 | `dev/phase-final-review/` fixture run outputs | Manual QA: dry-run each evaluator via the orchestrator |
| AC6 | propagation outputs | Existing automated test: `tests/test_propagate_master_assets.py` |

Non-goals:

- No remediation of anything found (findings are report content only).
- No overlap with `z-auditor-code`/`z-auditor-refactor` scope — these evaluators are phase-diff-scoped, not whole-repo audits; reference `auditor-conventions` severity norms via the conventions skill rather than duplicating.
- No graph-server setup or modification.

## B. Correctness & Edge Cases

- Graph server unavailable (05g): not-run record with reason, per AC4 — never a silent pass.
- Empty phase diff: valid; each evaluator reports "nothing introduced since baseline" as a completed check, not a failure.
- 05k with no dependency manifest changes: report "no new dependencies" as a completed check.
- Baseline worktree missing (05a failed upstream): all three must report not-run rather than evaluating against the wrong tree.

## C. Consistency & Architecture Fit

- Lettered-subagent house style per `04a`–`04d` files.
- Consume: conventions skill (report paths, severity, ≤10-line contract), report skill templates, orchestrator invocation shape from feature 02, fixture from feature 01.
- Graph tool names referenced must match the MCP server's actual tools (`refactor_tool` verified in this workspace's code-review-graph server).

## D. Clean Design & Maintainability

- Simplest design: three thin agents that are mostly "scope + tool + report template" declarations; shared rules live in the conventions skill.
- Duplication risk: severity taxonomies — reference the conventions skill, never restate.
- Keep-it-clean: no per-agent report format inventions; all formats come from `phase-final-review-report`.

## E. Completeness: Observability, Security, Operability

- Observability: reports on disk are the record; no logging. Correct decision for markdown assets.
- Security: read-only evaluators; 05k reports vulnerabilities but does not fetch or install anything.
- Runbook: deploy = propagation; verify = fixture dry-runs; rollback = git revert.

## F. Test Plan

- Must-have automated tests: propagation suite (existing).
- Manual QA checks:
  1. Given the fixture and a confirmed baseline, when 05g runs via the orchestrator, then a sweep report exists at the conventions-defined path and the return summary is ≤10 lines.
  2. Given the graph server is stopped, when 05g runs, then it records not-run with reason and the orchestrator's verdict ceiling drops below GO.
  3. Given the fixture, when 05j runs, then its report names at least the known Phase 01-vs-02 stylistic differences (real drift exists between those artifact sets).
  4. Given no dependency changes in the fixture diff, when 05k runs, then it reports a completed "no new dependencies" check.

## Stage 0: Test Prerequisites

Not required — markdown assets; propagation suite exists.

## Stage 1: 05g Artifact Sweeper

**Goal**: AC1 with graceful graph-unavailable degradation.
**Success Criteria**: Manual QA checks 1–2 pass.
**Status**: Not Started

## Stage 2: 05j Consistency Auditor

**Goal**: AC2.
**Success Criteria**: Manual QA check 3 passes.
**Status**: Not Started

## Stage 3: 05k Dependency Auditor

**Goal**: AC3.
**Success Criteria**: Manual QA check 4 passes.
**Status**: Not Started

## Stage 4: Propagation

**Goal**: AC6.
**Success Criteria**: Propagation suite passes; agents in all harness outputs.
**Status**: Not Started

## Relationships to Sibling Plans

- Depends on 01 (contracts, fixture) and 02 (orchestrator to dry-run through).
- Reports feed feature 06's synthesizer; formats must stay template-conformant.

## Unverified Assumptions

- `refactor_tool` dead-code detection can be scoped to a diff/file list; if the tool only operates repo-wide, 05g filters results to phase-touched files and this is recorded in its instructions.
