# Feature Plan: 06-readiness-synthesis

## Execution Metadata

- **Wave:** 6
- **Parallel safe:** no
- **Depends on:** 01-review-foundation, 02-final-review-orchestrator, 03-mechanical-evaluators, 04-delegating-evaluators, 05-deep-judgment-evaluators
- **Key files modified:** `.github/agents/05l-readiness-synthesizer.agent.md` (new), `.github/agents/05i-learnings-harvester.agent.md` (new), `.github/agents/README.md` (agent inventory update), propagated outputs (generated), `scripts/propagate_master_assets.py` (verify — no change expected), dry-run output artifacts under `dev/phase-final-review/` (generated during acceptance)
- **Sequential reason:** integration feature — requires every evaluator from waves 3–5 to exist for the full-flow dry run; shares propagated output files with all sibling features

## A. Requirements & Traceability

Source: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`, Deliverable 6, the In Scope roster entries for 05i and 05l, and the phase's dry-run success criteria.

Acceptance criteria:

- **AC1**: `05l-readiness-synthesizer.agent.md` exists: reads all evaluator reports (never code), produces the go/no-go readiness report with a severity-ordered blocking list using the `phase-final-review-report` template. It extends `prod-code-review` conventions one level up (references them; does not duplicate or modify them).
- **AC2**: 05l enforces the no-GO-with-missing-checks rule: if any evaluator is recorded as not-run, the verdict ceiling is "no blockers found, coverage incomplete" — never GO — and the not-run checks are enumerated by name in the report.
- **AC3**: `05i-learnings-harvester.agent.md` exists: mines review evidence for recurring mistakes — review records when present on disk, and otherwise git history (fix/remediation commits), merged PR discussions, eval ledgers, and QA failure records (this repo's Phase 01/02 on-disk review records were deleted in commit 4dd01e9, so git-history mining is a required capability, not a fallback); drafts `.github/learnings/` entries and instruction-file update proposals feeding the existing instructions-writer/evaluator loop (proposals only — it does not edit instruction files itself).
- **AC4**: Both agents load `phase-final-review-conventions`, honor report locations and the ≤10-line return contract, and are top-tier (05l) per the model-tier policy.
- **AC5** (integration — whole-phase proof): a full dry run of the complete flow — orchestrator preflight through 05l synthesis — against the development fixture completes and produces in `dev/phase-final-review/`: a master QA doc, a security rollup with fixed/persisting/reintroduced classification, an AC-regression matrix covering every fixture AC, and a severity-ordered go/no-go readiness report.
- **AC6** (integration — failure path): a second dry run with one evaluator forced to fail completes, names the missing check in the readiness report, and returns a verdict that is not GO.
- **AC7** (integration — verdict lifecycle): on dry-run completion, the fixture phase's status line update behavior is exercised (against fixture copies of the planning docs, not the real roadmap) and works without manual editing.
- **AC8**: 05i produces at least one draft learnings entry or instruction-file update proposal from this repo's real review-record history (named phase success criterion).
- **AC9**: Propagation picks up both agents; `tests/test_propagate_master_assets.py` passes.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1–AC4 | the two agent files in `.github/agents/` | Code-review evidence only |
| AC5–AC7 | full-flow dry-run outputs under `dev/phase-final-review/` | Manual QA: scripted dry-run walkthrough (this is the phase's integration smoke test) |
| AC8 | draft learnings/instruction proposals | Manual QA: inspect drafted entry against real review-record history |
| AC9 | propagation outputs | Existing automated test: `tests/test_propagate_master_assets.py` |

Non-goals:

- 05i does not commit learnings or edit `.github/instructions/` — it drafts; the instructions-manager loop owns acceptance.
- 05l does not re-evaluate anything — synthesis only, from report files.
- No modification of `prod-code-review`.
- No remediation of dry-run findings; NO-GO output from the fixture run is expected and correct (the fixture contains Phase 02's genuine NO-GO case).

## B. Correctness & Edge Cases

- Missing report file at synthesis time (evaluator claimed success but wrote nothing): 05l treats it as a not-run check — the report's existence, not the evaluator's claim, is the evidence.
- Conflicting severities for the same underlying issue across reports (e.g., security rollup vs. seam analyzer): 05l takes the highest severity and cross-references both sources.
- Empty learnings harvest (no recurring mistakes found): valid; 05i reports "none found" with the corpus it examined — but AC8 requires the real-history run to find at least one, which Phase 01/02 history supports (both phases had remediation cycles).
- Verdict write-back target missing (fixture without a roadmap copy): record the write-back as not-performed with reason; do not touch the real roadmap during dry runs.

## C. Consistency & Architecture Fit

- Lettered-subagent house style; 05l's relationship to `prod-code-review` mirrors how the phase doc frames it: one level up, extending conventions.
- Consume: every upstream contract — conventions/report skills and fixture (01), orchestrator run semantics and not-run record format (02), all nine evaluator report formats (03–05).
- 05i feeds the existing instructions-writer/evaluator loop (`.github/agents/instructions-writer.agent.md`, `instructions-evaluator.agent.md` — verified present) and the `.github/learnings/` directory (verified present).

## D. Clean Design & Maintainability

- Simplest design: 05l is a reader + template-filler with two hard rules (severity ordering, no-GO-with-missing-checks); 05i is a miner + drafter.
- Complexity risk: synthesis sprawl — 05l must not restate report content, only rank, cross-reference, and verdict.
- Keep-it-clean: blocking-list severity vocabulary comes from the conventions skill.

## E. Completeness: Observability, Security, Operability

- Observability: the readiness report is the run's observable output; no logging. Correct decision.
- Security: 05l reads reports only; 05i reads repo history; neither writes outside `dev/phase-final-review/` and draft-proposal locations.
- Runbook: deploy = propagation; verify = the two integration dry runs (AC5, AC6); rollback = git revert.

## F. Test Plan

- Must-have automated tests: propagation suite (existing).
- Manual QA checks (these are the phase-level integration evidence):
  1. Given all evaluators exist and the fixture is intact, when the full flow runs, then all four synthesis-input artifact types exist and the readiness report's blocking list is severity-ordered (AC5).
  2. Given one evaluator forced to fail, when the flow runs, then the readiness report names the missing check and the verdict is not GO (AC6).
  3. Given the fixture's Phase 02 NO-GO security content, when 05l synthesizes, then P2-SEC-01..03 appear in the blocking list (fixture-truth check).
  4. Given this repo's real Phase 01/02 review records, when 05i runs, then at least one draft learnings entry or instruction-update proposal exists and cites its evidence (AC8).
  5. Given a completed dry run, when planning-doc write-back executes against fixture copies, then the status line updates without manual editing (AC7).

## Stage 0: Test Prerequisites

Not required — markdown assets; propagation suite exists; integration evidence is the dry-run walkthrough.

## Stage 1: 05l Readiness Synthesizer

**Goal**: AC1, AC2.
**Success Criteria**: Agent file complete; no-GO-with-missing-checks rule explicit.
**Status**: Not Started

## Stage 2: 05i Learnings Harvester

**Goal**: AC3.
**Success Criteria**: Agent file complete; draft-only boundary explicit.
**Status**: Not Started

## Stage 3: Full-Flow Integration Dry Runs

**Goal**: AC5, AC6, AC7 — the phase's integration smoke test.
**Success Criteria**: Manual QA checks 1–3 and 5 pass; outputs archived under `dev/phase-final-review/`.
**Status**: Not Started

## Stage 4: Real-History Harvest + Propagation

**Goal**: AC8, AC9.
**Success Criteria**: Manual QA check 4 passes; propagation suite passes.
**Status**: Not Started

## Relationships to Sibling Plans

- Terminal integration feature: consumes every contract published by features 01–05; its dry runs are the phase's proof that all features operate together.
- Any template mismatch discovered here is fixed in the owning upstream feature's assets, not patched locally in 05l.

## Unverified Assumptions

- Git history, PRs #19/#20, and eval ledgers contain minable recurring-mistake evidence for AC8 (both phases had remediation cycles per their summaries); on-disk review records no longer exist, so AC8 evidence comes from history mining or QA failure records.
