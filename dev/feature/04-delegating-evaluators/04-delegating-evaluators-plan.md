# Feature Plan: 04-delegating-evaluators

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** no
- **Depends on:** 01-review-foundation, 02-final-review-orchestrator
- **Key files modified:** `.github/agents/05c-qa-consolidator.agent.md` (new), `.github/agents/05d-security-rollup.agent.md` (new), `.github/agents/05h-test-health.agent.md` (new), `.github/agents/README.md` (agent inventory update), propagated outputs (generated), `scripts/propagate_master_assets.py` (verify — no change expected)
- **Sequential reason:** shares propagated output files with all sibling features; contract dependency on features 01 and 02

## A. Requirements & Traceability

Source: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`, Deliverable 4 and the In Scope roster entries for 05c, 05d, 05h.

Acceptance criteria:

- **AC1**: `05c-qa-consolidator.agent.md` exists: merges all subphase QA docs into one master QA doc — dedupes, drops superseded checks, re-orders into a single efficient walkthrough. Reads QA docs only (never code). Uses the master-QA template from `phase-final-review-report`.
- **AC2**: `05d-security-rollup.agent.md` exists: unions and dedupes all subphase security findings, delegates a live re-scan of final code to the existing `security-scan` agent (`.github/agents/security-scan.agent.md`) against the full finding list, and classifies each finding fixed / persisting / reintroduced using the rollup template.
- **AC3**: `05h-test-health.agent.md` exists: reports coverage delta baseline→now, cross-subphase test redundancy, and flake candidates; delegates analysis to the existing `test-analyst` agent (`.github/agents/test-analyst.agent.md`).
- **AC4**: All three load `phase-final-review-conventions`, honor report locations and the ≤10-line return contract, and degrade per partial-failure semantics (e.g., delegate agent unavailable → not-run with reason).
- **AC5**: 05d and 05h demonstrably delegate rather than reimplement — their instructions contain no scanning/analysis procedure of their own, only delegation, merge, and classification rules (this is a named phase success criterion).
- **AC6**: Each evaluator dry-runs via the orchestrator against the development fixture; 05d correctly classifies the fixture's Phase 02 NO-GO findings (P2-SEC-01..03) in its rollup.
- **AC7**: Propagation picks up all three agents; `tests/test_propagate_master_assets.py` passes.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1–AC5 | the three agent files in `.github/agents/` | Code-review evidence only |
| AC6 | fixture dry-run outputs under `dev/phase-final-review/` | Manual QA: dry-run with NO-GO classification spot-check |
| AC7 | propagation outputs | Existing automated test: `tests/test_propagate_master_assets.py` |

Non-goals:

- No changes to `security-scan` or `test-analyst` agents — they are consumed as-is; if their return shapes don't fit, adaptation happens in the 05x wrapper, not upstream.
- No fixing of security findings or tests; classification and reporting only.
- No new QA authoring — 05c consolidates existing QA docs; net-new QA for uncovered seams belongs to feature 05's seam analyzer findings and feature 06's synthesis.

## B. Correctness & Edge Cases

- Subphase with a missing QA doc: preflight (feature 02) should have caught it; if 05c encounters one anyway, it reports the gap in the master doc rather than failing the run.
- Conflicting QA steps between subphases (same check, different expected results): 05c must keep the later subphase's version and flag the conflict, not silently pick one.
- 05d finding-matching ambiguity (re-scan finding vs. historical finding worded differently): classify conservatively as persisting-unconfirmed and flag for synthesis; never mark fixed on a fuzzy match.
- 05h with no coverage tooling configured in the target repo: report coverage delta as not-measurable, still deliver redundancy/flake analysis via `test-analyst`.
- Delegate agent returns nothing/errors: not-run record with reason, per partial-failure semantics.

## C. Consistency & Architecture Fit

- Lettered-subagent house style per `04a`–`04d`.
- Delegation phrasing consistent with how orchestrators in this repo invoke subagents (see `implementation-pipeline-loop` skill and `04-phase-execute.agent.md`).
- Consume: conventions + report skills (feature 01), orchestrator invocation shape (feature 02), fixture (feature 01), existing `security-scan` and `test-analyst` agents (verified present in `.github/agents/`).

## D. Clean Design & Maintainability

- Simplest design: three thin merge-and-delegate agents; all evaluation intelligence lives in the delegates and the templates.
- Duplication risk: 05d re-describing security-scan's methodology — prohibited by AC5.
- Keep-it-clean: classification vocabularies (fixed/persisting/reintroduced) defined once in the report skill.

## E. Completeness: Observability, Security, Operability

- Observability: reports on disk; no logging. Correct decision.
- Security: 05d handles finding data already committed in phase docs; the live re-scan delegate operates read-only.
- Runbook: deploy = propagation; verify = fixture dry-runs; rollback = git revert.

## F. Test Plan

- Must-have automated tests: propagation suite (existing).
- Manual QA checks:
  1. Given the fixture's two pseudo-subphase QA docs, when 05c runs, then the master QA doc contains each unique check exactly once, ordered as one walkthrough, with superseded checks dropped and conflicts flagged.
  2. Given the fixture's Phase 02 security scan (P2-SEC-01..03), when 05d runs, then each finding appears in the rollup with a fixed/persisting/reintroduced classification and the live re-scan delegation is visible in the run record.
  3. Given the fixture, when 05h runs, then its report contains a coverage-delta section (or an explicit not-measurable statement) plus redundancy/flake sections sourced from `test-analyst`.
  4. Given `test-analyst` is made unavailable, when 05h runs, then it records not-run with reason and the verdict ceiling drops below GO.

## Stage 0: Test Prerequisites

Not required — markdown assets; propagation suite exists.

## Stage 1: 05c QA Consolidator

**Goal**: AC1.
**Success Criteria**: Manual QA check 1 passes.
**Status**: Not Started

## Stage 2: 05d Security Rollup

**Goal**: AC2, AC5 for security.
**Success Criteria**: Manual QA check 2 passes; no scan methodology in the agent file.
**Status**: Not Started

## Stage 3: 05h Test Health

**Goal**: AC3, AC5 for tests.
**Success Criteria**: Manual QA checks 3–4 pass.
**Status**: Not Started

## Stage 4: Propagation

**Goal**: AC7.
**Success Criteria**: Propagation suite passes; agents in all harness outputs.
**Status**: Not Started

## Relationships to Sibling Plans

- Depends on 01 (contracts, fixture — including the NO-GO case this feature's QA hinges on) and 02 (orchestrator).
- 05d's classification output is a primary input to feature 06's go/no-go synthesis.

## Unverified Assumptions

- `security-scan` and `test-analyst` can be invoked with a scoped finding-list/phase-diff context; if either assumes whole-repo defaults, the 05x wrapper narrows the scope in its delegation prompt and this is recorded in implementation notes.
