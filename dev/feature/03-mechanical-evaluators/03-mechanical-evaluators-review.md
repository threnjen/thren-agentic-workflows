# Review Record: 03-mechanical-evaluators

## Summary

Reviewed the three source-of-truth evaluator definitions and nine generated
Claude, OpenCode, and Codex mirrors against the implementation record and plan.
Two contract issues were found and fixed: dead-code results lacked a safe
added-line attribution fallback, and vulnerability audit commands were not
explicitly constrained to offline/local evidence. The propagation suite passed.
The orchestrator fixture dry-runs remain unverified.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Unverified (static contract present) | .github/agents/05g-artifact-sweeper.agent.md:8-69; generated mirrors in claude/agents/z-artifact-sweeper.md, opencode/agents/05g-artifact-sweeper.md, codex/agents/z-artifact-sweeper.toml | Static scope, cheap-tier, baseline, failure, and report rules are present; the dead-code attribution guard was fixed at .github/agents/05g-artifact-sweeper.agent.md:43-52. A live evaluator run is still required. |
| AC2 | Unverified (static contract present) | .github/agents/05j-consistency-auditor.agent.md:8-62; generated mirrors in claude/agents/z-consistency-auditor.md, opencode/agents/05j-consistency-auditor.md, codex/agents/z-consistency-auditor.toml | Naming, error-handling, repeated-pattern drift, canonical recommendations, fixture scope, and degradation instructions are present. Fixture execution was not observed. |
| AC3 | Unverified (static contract present) | .github/agents/05k-dependency-auditor.agent.md:8-67; generated mirrors in claude/agents/z-dependency-auditor.md, opencode/agents/05k-dependency-auditor.md, codex/agents/z-dependency-auditor.toml | Dependency, license, vulnerability, duplicate-library, no-manifest-change, and no-network rules are present; the offline evidence guard was fixed at .github/agents/05k-dependency-auditor.agent.md:33-38. A fixture run is still required. |
| AC4 | Unverified (static contract present) | All three source agents, especially shared-contract blocks at .github/agents/05g-artifact-sweeper.agent.md:13-22, .github/agents/05j-consistency-auditor.agent.md:13-22, .github/agents/05k-dependency-auditor.agent.md:13-22 | Canonical report paths, shared contracts, concise return summaries, baseline/empty-diff semantics, and NOT RUN handling are documented. Runtime failure-path behavior was not observed. |
| AC5 | Unverified | 03-mechanical-evaluators-implementation.md:34,45; plan 03-mechanical-evaluators-plan.md:21,67-70 | No live dry-run through 05-phase-final-review was available. Requires each evaluator against the fixture with a confirmed baseline, including the graph-unavailable path, and report-file evidence. |
| AC6 | Verified | tests/test_propagate_master_assets.py; scripts/propagate_master_assets.py | Targeted propagation suite passed: 20 tests and 7 subtests. Codex mirrors also parse as valid TOML. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Repo-wide dead-code results could be attributed to the phase by touched file alone when line data was absent, allowing pre-existing dead code into findings. | High | .github/agents/05g-artifact-sweeper.agent.md:43-52 and corresponding generated mirror blocks | AC1 | Fixed (applied during this review) |
| 2 | The dependency auditor allowed an “already available” vulnerability command without requiring known offline/local-data behavior, leaving a network-capable command ambiguous. | Medium | .github/agents/05k-dependency-auditor.agent.md:33-38 and corresponding generated mirror blocks | AC3, AC4 | Fixed (applied during this review) |
| 3 | Required orchestrator/fixture dry-run evidence is absent; static reading does not verify report creation or failure-path behavior. | Medium | 03-mechanical-evaluators-implementation.md:34,45; 03-mechanical-evaluators-plan.md:21,67-70 | AC5 | Open |
| 4 | The plan lists an .github/agents/README.md inventory update, but the implementation record and implementation commit contain no README change. | Low | 03-mechanical-evaluators-plan.md:8; 03-mechanical-evaluators-implementation.md:48-66 | — | Open |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| .github/agents/05g-artifact-sweeper.agent.md | Require verified path and added-line attribution; record NOT RUN when attribution is unavailable. | 1 |
| claude/agents/z-artifact-sweeper.md | Propagated the dead-code attribution guard. | 1 |
| opencode/agents/05g-artifact-sweeper.md | Propagated the dead-code attribution guard. | 1 |
| codex/agents/z-artifact-sweeper.toml | Propagated the dead-code attribution guard. | 1 |
| .github/agents/05k-dependency-auditor.agent.md | Require explicitly offline/local vulnerability evidence and reject network-capable commands. | 2 |
| claude/agents/z-dependency-auditor.md | Propagated the offline vulnerability-audit guard. | 2 |
| opencode/agents/05k-dependency-auditor.md | Propagated the offline vulnerability-audit guard. | 2 |
| codex/agents/z-dependency-auditor.toml | Propagated the offline vulnerability-audit guard. | 2 |

## Remaining Concerns

- Issue #3: AC5 remains unverified until the orchestrator can run with a confirmed baseline and fixture, including graph-server-unavailable behavior.
- Issue #4: Reconcile the planned agent inventory update or remove it from the plan in a future documentation pass.
- The full suite completed with 387 passed, 2 failed, and 7 subtests; both failures are the same pre-existing hook-integration failures recorded by the implementation and are outside this feature.

## Test Coverage Assessment

- Covered: AC6 propagation test (20 passed, 7 subtests); static contract review for AC1–AC4.
- Missing: Runtime/manual evaluator QA for AC1–AC4 and all four AC5 orchestrator fixture checks, including report creation, summary length, known fixture drift, no-new-dependency handling, and graph-unavailable degradation.
- Full-suite status after fixes: 387 passed, 2 pre-existing failures, 7 subtests.

## Risk Summary

- AC5 has no runtime report evidence, so end-to-end evaluator wiring and degradation remain unverified.
- .github/agents/05g-artifact-sweeper.agent.md:43-52 now fails closed when graph results cannot be attributed to added lines.
- .github/agents/05k-dependency-auditor.agent.md:33-38 now requires local/offline vulnerability evidence and prevents ambiguous network use.
- Generated mirrors passed propagation validation; the source/consumer identity transforms remain intentional.
