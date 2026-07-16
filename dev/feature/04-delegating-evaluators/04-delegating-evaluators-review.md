# Review Record: 04-delegating-evaluators

## Summary

The permission-boundary remediation and Claude/OpenCode/Codex renderer-parity coverage are verified. Canonical 05c and 05h report artifacts are present and internally consistent. The single retry still did not produce a 05d security rollup: the canonical CLI could not find `05 Phase - Final Review`, the ephemeral retry waited on the delegated Security Scan thread, and it was stopped with SIGINT exit 130. The status artifact now records `not-run`, `report: null`, the exact runtime reason, and `NO-GO (incomplete coverage)`. No P2-SEC-01..03 classification is claimed.

## Verdict
<!-- Approved | Approved with Reservations | Changes Requested -->
Changes Requested

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Unverified — canonical artifact present | `.github/agents/05c-qa-consolidator.agent.md:8-59`; `dev/phase-final-review/PHASE_05/master-qa.md:21-82`; `dev/phase-final-review/PHASE_05/05c-qa-consolidator-report.md:3-11` | Static QA-only boundary and merge rules are present. The canonical artifact contains 31 retained checks, three supersessions, both conflicts, and preserved NOT RUN states. Artifact inspection verifies content, but does not independently observe the evaluator thread executing. |
| AC2 | Incomplete — 05d not-run | `.github/agents/05d-security-rollup.agent.md:9-74`; `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1` | Delegation, whole-repository scope, conservative matching, and failure rules are present. No canonical `security-rollup.md` or `05d-security-rollup-report.md` exists, so no final-state classification is available. |
| AC3 | Unverified — canonical artifact present | `.github/agents/05h-test-health.agent.md:9-58`; `dev/phase-final-review/PHASE_05/05h-test-health-report.md:1-67` | Static delegation/adaptation rules are present. The artifact contains not-measurable coverage, redundancy, and flake sections and preserves delegate evidence paths; the evaluator/delegate execution itself is not independently observed. |
| AC4 | Partial / unverified | `.github/agents/05c-qa-consolidator.agent.md:11-21`; `.github/agents/05d-security-rollup.agent.md:13-23,65-74`; `.github/agents/05h-test-health.agent.md:13-24,44-58`; `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1` | Shared report/return/partial-failure contracts are statically present, and the 05d failure artifact now explicitly carries NO-GO. The 05h unavailable-delegate failure path has no retained runtime report or status evidence. |
| AC5 | Complete (static) | `.github/agents/05d-security-rollup.agent.md:39-49`; `.github/agents/05h-test-health.agent.md:26-36` | Both wrappers delegate analysis and explicitly prohibit local scan/test-analysis procedures. |
| AC6 | Incomplete — NO-GO; 05d not-run | `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1`; `dev/phase-final-review/PHASE_05/runs/20260715T222902Z-1/evaluator-status.jsonl:1-3`; `dev/feature/04-delegating-evaluators/04-delegating-evaluators-implementation.md:103,107-108` | Retry evidence: canonical CLI reported `--agent 05 Phase - Final Review not found`; the ephemeral retry waited on the 05d/delegated Security Scan thread, produced no report/status, and exited via SIGINT 130. The prior exact `no thread with id: 019f679b-75ed-7690-9238-c0e36a118875` record is archived. 05c/05h artifacts exist, but 05d has `report: null`; P2-SEC-01..03 remain unclassified and are not claimed here. |
| AC7 | Complete (test verified) | `tests/test_propagate_master_assets.py:86-139`; `claude/agents/z-qa-consolidator.md:1-74`; `claude/agents/z-security-rollup.md:1-78`; `claude/agents/z-test-health.md:1-61`; `opencode/agents/05c-qa-consolidator.md:1-64`; `opencode/agents/05d-security-rollup.md:1-84`; `opencode/agents/05h-test-health.md:1-66`; `codex/agents/z-qa-consolidator.toml:1-57`; `codex/agents/z-security-rollup.toml:1-73`; `codex/agents/z-test-health.toml:1-55` | Source discovery, no-`execute` boundary, 05d NO-GO contract, and exact Claude/OpenCode/Codex renderer parity pass. Targeted suite: 21 passed, 10 subtests. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Evaluator permissions exceeded the read-only/delegation boundary by granting execute access and emitting Bash permissions. | Medium | `.github/agents/05c-qa-consolidator.agent.md:4`; `.github/agents/05d-security-rollup.agent.md:4`; `.github/agents/05h-test-health.agent.md:4` | AC1-AC4 | Fixed during prior review; retained and reverified |
| 2 | Propagation coverage did not assert discovery and renderer parity for all three new evaluators across all three harnesses. | Medium | `tests/test_propagate_master_assets.py:86-139` | AC7 | Fixed during prior review; retained and reverified |
| 3 | AC6 still lacks a canonical 05d security rollup, delegated final-scan evidence, and P2-SEC-01..03 classifications after the single retry. | High | `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1` | AC2, AC6 | Open — requires collaboration-runtime recovery and a full fixture rerun |
| 4 | 05d’s delegate-failure contract did not explicitly set a NO-GO/incomplete-coverage ceiling, and the status artifact exposed only `not-run` with no visible verdict. | Medium | `.github/agents/05d-security-rollup.agent.md:67-74`; `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1` | AC4, AC6 | Fixed during this review |
| 5 | The implementation record incorrectly said the propagation test was read-only and that zero tests were added. | Medium | `dev/feature/04-delegating-evaluators/04-delegating-evaluators-implementation.md:82-94` | AC7 | Fixed during this review |
| 6 | The task checklist marks the 05h unavailable-delegate manual check complete without retained runtime evidence for that failure path. | Medium | `dev/feature/04-delegating-evaluators/04-delegating-evaluators-tasks.md:35-36`; `dev/feature/04-delegating-evaluators/04-delegating-evaluators-implementation.md:50,94` | AC4 | Open — rerun 05h with `Test - Analyst` unavailable and retain the NOT RUN/below-GO evidence |

## Fixes Applied
<!-- "None" if none -->

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/agents/05d-security-rollup.agent.md` | Added an explicit NO-GO/incomplete-coverage ceiling for unavailable, error, timeout, or empty delegate results. | 4 |
| `claude/agents/z-security-rollup.md` | Propagated the 05d NO-GO failure contract without restoring Bash access. | 4 |
| `opencode/agents/05d-security-rollup.md` | Propagated the 05d NO-GO failure contract without restoring `bash: allow`. | 4 |
| `codex/agents/z-security-rollup.toml` | Propagated the 05d NO-GO failure contract. | 4 |
| `dev/phase-final-review/PHASE_05/evaluator-status.jsonl` | Recorded the explicit `NO-GO (incomplete coverage)` outcome alongside the exact 05d runtime failure and `report: null`. | 4 |
| `tests/test_propagate_master_assets.py` | Added assertions that 05d carries the NOT RUN and NO-GO contract while preserving all-harness parity checks. | 4 |
| `dev/feature/04-delegating-evaluators/04-delegating-evaluators-implementation.md` | Corrected the test-change table and reported one added test method with ten subtests. | 5 |
| `.github/learnings/review-learnings.md` | Added a reusable rule requiring explicit readiness ceilings for delegated evaluator failures. | — |

## Remaining Concerns
<!-- "None" if all clear -->

- Issue #3: AC6 remains a hard NO-GO until the collaboration runtime can launch the canonical orchestrator, complete the delegated 05d Security Scan, write the canonical rollup, and classify P2-SEC-01..03.
- Issue #6: The 05h unavailable-delegate degradation branch remains runtime-unverified.
- Full suite after fixes: 388 passed, 2 failed in unrelated existing checks at `tests/hooks/test_hook_distribution_integration.py:207` (latency threshold) and `:216` (installation-guide classification).

## Test Coverage Assessment

- Covered: static AC1-AC5 contract checks; canonical 05c/05h artifact content; AC7 source discovery and Claude/OpenCode/Codex renderer parity.
- Missing: 05d live delegated scan/rollup and P2-SEC-01..03 classification for AC2/AC6; 05h unavailable-delegate runtime evidence for AC4.
- Targeted result after fixes: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` — 21 passed, 0 failed, 10 subtests passed.
- Full result after fixes: `.venv/bin/python -m pytest -q` — 388 passed, 2 failed; failures are outside the feature’s changed files and reproduce the prior review’s known failures.
- Runtime honesty: report artifacts were inspected as evidence, but static review and artifact content do not independently prove evaluator-thread execution; AC6 remains explicitly unverified for 05d.

## Risk Summary
<!-- 2-5 bullets -->

- `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1` is now fail-closed (`not-run`, `report: null`, explicit NO-GO), but the missing 05d report prevents release readiness.
- `dev/phase-final-review/PHASE_05/master-qa.md:59-82` and `05h-test-health-report.md:62-67` preserve incomplete/not-measurable evidence rather than converting it into a pass.
- Generated evaluator outputs remain aligned with their source contracts, including the no-execute permission boundary and 05d NO-GO rule.
