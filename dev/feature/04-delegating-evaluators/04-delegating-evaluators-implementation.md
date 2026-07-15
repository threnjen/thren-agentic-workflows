# Implementation Record: 04-delegating-evaluators

## Summary

Implemented the three Wave 4 Phase Final Review evaluator assets and propagated
them to Claude, OpenCode, and Codex. `05c` is a QA-only merge agent using the
canonical master-QA template; `05d` is a thin finding merge/delegation wrapper
around the existing full-repository `Security Scan`; and `05h` delegates test
health analysis to `Test - Analyst` and adapts its native reduction-plan output
into a health report. The inventory and feature tasks were updated, and the
propagation script remained unchanged.

AC1–AC5 and AC7 are complete by source-contract, propagation, and targeted test
evidence. AC6 was attempted through the real orchestrator CLI against the
fixture; the collaboration runtime returned `no thread with id` for all three
evaluator launches. The run correctly recorded all three checks as `not-run`
and returned `NO-GO (incomplete coverage)`, so no live-success report or
unverified P2-SEC classification is claimed.

## Sibling Features

Read the first five lines of sibling plans before implementation:
`01-review-foundation` (Wave 1), `02-final-review-orchestrator` (Wave 2),
`03-mechanical-evaluators` (Wave 3), `05-deep-judgment-evaluators` (Wave 5), and
`06-readiness-synthesis` (Wave 6). This feature consumes the conventions,
report templates, fixture, and orchestrator contracts from 01/02; it shares
propagated outputs with the other Wave 4/5/6 features and feeds 05d's security
classifications into feature 06. No sibling implementation files were changed.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | AC1-MANUAL-QA-1 | Static agent contract plus fixture manual consolidation | Complete (static; live run not available) | `.github/agents/05c-qa-consolidator.agent.md` | `.github/agents/05c-qa-consolidator.agent.md`; `.github/skills/phase-final-review-report/SKILL.md` | PENDING | PENDING |
| AC2 | AC2 | AC2-MANUAL-QA-2 | Static delegation/classification contract plus fixture manual rollup | Complete (static; live run not available) | `.github/agents/05d-security-rollup.agent.md` | `.github/agents/05d-security-rollup.agent.md`; `.github/agents/security-scan.agent.md`; `.github/skills/phase-final-review-report/SKILL.md` | PENDING | PENDING |
| AC3 | AC3 | AC3-MANUAL-QA-3 | Static delegation/adaptation contract plus fixture manual health report | Complete (static; live run not available) | `.github/agents/05h-test-health.agent.md` | `.github/agents/05h-test-health.agent.md`; `.github/agents/test-analyst.agent.md`; `.github/skills/phase-final-review-conventions/SKILL.md` | PENDING | PENDING |
| AC4 | AC4 | AC4-CONTRACT-STATIC | Shared report-root, return-limit, and partial-failure contract checks | Complete | `.github/agents/05c-qa-consolidator.agent.md`; `.github/agents/05d-security-rollup.agent.md`; `.github/agents/05h-test-health.agent.md` | `.github/agents/05c-qa-consolidator.agent.md`; `.github/agents/05d-security-rollup.agent.md`; `.github/agents/05h-test-health.agent.md`; `.github/skills/phase-final-review-conventions/SKILL.md` | PENDING | PENDING |
| AC5 | AC5 | AC5-STATIC-DELEGATION | Static absence of local scan/test-analysis methodology | Complete | `.github/agents/05d-security-rollup.agent.md`; `.github/agents/05h-test-health.agent.md` | `.github/agents/05d-security-rollup.agent.md`; `.github/agents/05h-test-health.agent.md` | PENDING | PENDING |
| AC6 | AC6 | AC6-FIXTURE-DRY-RUN | Orchestrator fixture dry-run with delegation and P2-SEC-01..03 spot-check | Incomplete — not-run | `.github/agents/05-phase-final-review.agent.md`; `.github/agents/05c-qa-consolidator.agent.md`; `.github/agents/05d-security-rollup.agent.md`; `.github/agents/05h-test-health.agent.md`; `dev/phase-final-review/PHASE_05/evaluator-status.jsonl` | `dev/phase-final-review/fixtures/README.md`; `dev/phase-final-review/fixtures/PHASE_05/PHASE_05b/PHASE_05b-security-scan.md:53-55`; `dev/phase-final-review/PHASE_05/evaluator-status.jsonl` | PENDING | PENDING |
| AC7 | AC7 | AC7-PROPAGATION | Explicit propagation run, output-name/delegation checks, and targeted pytest suite | Complete | Generated Claude/OpenCode/Codex agents; `.github/agents/README.md`; `scripts/propagate_master_assets.py` (verified unchanged) | `claude/agents/z-qa-consolidator.md`; `claude/agents/z-security-rollup.md`; `claude/agents/z-test-health.md`; `opencode/agents/05c-qa-consolidator.md`; `opencode/agents/05d-security-rollup.md`; `opencode/agents/05h-test-health.md`; `codex/agents/z-qa-consolidator.toml`; `codex/agents/z-security-rollup.toml`; `codex/agents/z-test-health.toml`; `tests/test_propagate_master_assets.py` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|---|-------------|--------|--------------------|-------|
| AC1 | `05c-qa-consolidator.agent.md` merges QA documents only, dedupes, drops superseded checks, orders a walkthrough, and flags missing/conflicting inputs. | Complete | `.github/agents/05c-qa-consolidator.agent.md` | Uses `master-qa.md` and the phase-final-review report template; live fixture success path remains unverified. |
| AC2 | `05d-security-rollup.agent.md` unions/dedupes findings, delegates the final scan, and classifies findings. | Complete | `.github/agents/05d-security-rollup.agent.md` | Accepts the delegate's required whole-repository scope and passes the full historical finding list. |
| AC3 | `05h-test-health.agent.md` delegates coverage delta, redundancy, and flake analysis and adapts the delegate output. | Complete | `.github/agents/05h-test-health.agent.md` | Explicitly handles the native reduction-plan shape and not-measurable coverage. |
| AC4 | All three load phase-final-review conventions and honor report, return-summary, and partial-failure contracts. | Complete | The three source agent files | Static contract checks passed; each has the phase report root, 10-line limit, and failure handling. |
| AC5 | 05d and 05h delegate rather than reimplement scanning or test analysis. | Complete | `.github/agents/05d-security-rollup.agent.md`; `.github/agents/05h-test-health.agent.md` | Both explicitly prohibit a local scan/test-analysis procedure; child agents are declared in frontmatter. |
| AC6 | All three evaluators dry-run through the orchestrator; 05d classifies P2-SEC-01..03. | Incomplete — external runtime blocked | `dev/phase-final-review/PHASE_05/evaluator-status.jsonl` | Orchestrator preflight passed, but every nested launch returned `no thread with id`; all three were correctly recorded `not-run`, with NO-GO coverage ceiling. |
| AC7 | Propagation discovers all three agents and the propagation suite remains green. | Complete | Generated outputs; `.github/agents/README.md` | Explicit propagator run returned zero changes; targeted suite passed 20/20 with 7 subtests. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05c-qa-consolidator.agent.md` | Create | Added the QA-only master-QA consolidator, source boundaries, merge/supersession/conflict rules, and partial-failure contract. | AC1 and AC4. |
| `.github/agents/05d-security-rollup.agent.md` | Create | Added historical finding merge, whole-repository Security Scan delegation, conservative classification, and not-run handling. | AC2, AC4, and AC5. |
| `.github/agents/05h-test-health.agent.md` | Create | Added Test Analyst delegation, reduction-plan adaptation, coverage not-measurable handling, and below-GO failure ceiling. | AC3, AC4, and AC5. |
| `.github/agents/README.md` | Modify | Added the three hidden evaluator inventory rows. | AC7 inventory-surface consistency. |
| `dev/feature/04-delegating-evaluators/04-delegating-evaluators-tasks.md` | Modify | Checked off completed prerequisite, source-contract, partial-failure, propagation, and inventory tasks; preserved unverified live-success checks. | Required pipeline handoff state. |
| `claude/agents/z-qa-consolidator.md` | Generated | Propagated 05c with Claude's hidden-agent naming. | AC7. |
| `claude/agents/z-security-rollup.md` | Generated | Propagated 05d and resolved its Security Scan child reference. | AC7. |
| `claude/agents/z-test-health.md` | Generated | Propagated 05h and resolved its Test Analyst child reference. | AC7. |
| `opencode/agents/05c-qa-consolidator.md` | Generated | Propagated 05c to OpenCode. | AC7. |
| `opencode/agents/05d-security-rollup.md` | Generated | Propagated 05d to OpenCode. | AC7. |
| `opencode/agents/05h-test-health.md` | Generated | Propagated 05h to OpenCode. | AC7. |
| `codex/agents/z-qa-consolidator.toml` | Generated | Propagated 05c to Codex. | AC7. |
| `codex/agents/z-security-rollup.toml` | Generated | Propagated 05d with the Codex security-scan reference. | AC7. |
| `codex/agents/z-test-health.toml` | Generated | Propagated 05h with the Codex z-test-analyst reference. | AC7. |
| `scripts/propagate_master_assets.py` | Verify-only | Confirmed the propagator required no source change. | AC7 plan expectation. |
| `dev/phase-final-review/PHASE_05/evaluator-status.jsonl` | Dry-run artifact | Recorded the three evaluator launch failures and the concrete collaboration-runtime reason. | AC6 partial-failure evidence. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Read-only verification | Existing targeted propagation suite executed; no test source changed. | AC7 output generation and propagation safety. |
| None added | Not applicable | The plan is markdown-only and identifies the existing propagation suite as the must-have automated test. Transient shell contract checks were run before/after each document change and were not retained as repository tests. | AC1–AC5 static contract evidence. |

## Test Results

- **Baseline**: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` — 20 passed, 0 failed, 7 subtests (before implementation).
- **Final**: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` — 20 passed, 0 failed, 7 subtests (after implementation).
- **New tests added**: 0
- **Regressions**: None in the targeted propagation suite. The AC6 dry-run was an external collaboration-runtime not-run, not a source/test regression.

## Deviations from Plan

- The global `rtk` wrapper failed its hook-integrity check. Commands were run through the documented `rtk proxy` passthrough; the external hook was not repaired or modified.
- The `Security Scan` delegate's confirmed whole-repository contract was retained. 05d passes the complete historical finding list for matching instead of narrowing the scan to phase-changed files.
- `Test - Analyst` remains unchanged. 05h explicitly treats its native `dev/feature/` reduction-plan files as intermediate evidence and adapts them into the required phase health report.
- No new automated test file was added because the plan identifies markdown assets and the existing propagation suite as the required automated coverage; static Red–Green contract checks were transient.

## Gaps

- AC6 live-success verification is incomplete. The orchestrator's fixture preflight passed, but the collaboration runtime returned `no thread with id` for 05c, 05d, and 05h. The evidence is preserved at `dev/phase-final-review/PHASE_05/evaluator-status.jsonl`.
- Because the nested evaluators did not launch, no canonical `master-qa.md`, `security-rollup.md`, or `05h-test-health-report.md` was produced by the dry-run, and P2-SEC-01..03 remain unclassified. Re-run the fixture once the collaboration runtime can create evaluator threads.

## Reviewer Focus Areas

- 05d's whole-repository delegation and `persisting-unconfirmed` handling — confirm it never marks a fuzzy or missing-evidence finding Fixed.
- 05h's adaptation boundary — confirm the Test Analyst reduction-plan output becomes a phase health report without modifying the upstream agent.
- 05c's later-subphase conflict/supersession rule and QA-only input boundary.
- Generated child-agent name resolution across Claude, OpenCode, and Codex, especially `z-test-analyst` in Codex.
- AC6 rerun evidence and the preserved NO-GO/not-run status before accepting the feature as fully verified.
