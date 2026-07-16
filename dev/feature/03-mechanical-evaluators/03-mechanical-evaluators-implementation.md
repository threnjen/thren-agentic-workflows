# Implementation Record: 03-mechanical-evaluators

## Summary

Added the three read-only, cheap-tier mechanical Phase Final Review evaluator
definitions: artifact sweeping, cross-subphase consistency auditing, and
dependency auditing. Each source agent consumes the landed Phase Final Review
conventions/report contracts, writes to the canonical evaluator report path,
handles missing inputs explicitly, and limits its return summary to 10 lines.
Propagation produced the Claude, OpenCode, and Codex copies without changing
the propagation script. No new automated tests were added because the plan
defines the markdown assets and existing propagation suite as the test surface.

## Sibling Features

- `01-review-foundation` supplies `phase-final-review-conventions`,
  `phase-final-review-report`, and the `PHASE_05` development fixture.
- `02-final-review-orchestrator` supplies the evaluator invocation shape,
  cheap-tier assignment, and partial-failure contract.
- `04-delegating-evaluators`, `05-deep-judgment-evaluators`, and
  `06-readiness-synthesis` consume the shared report outputs; no sibling files
  were modified for this feature.
- Sibling awareness covered the numbered Wave 1–6 feature directories; this
  implementation changed only the Wave 3 feature scope and generated mirrors.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | `AC1-artifact-sweeper-contract` | Static source contract check; manual evaluator QA | Implemented; runtime QA pending | `.github/agents/05g-artifact-sweeper.agent.md` and generated mirrors | `.github/agents/05g-artifact-sweeper.agent.md:24-48`; `claude/agents/z-artifact-sweeper.md`; `opencode/agents/05g-artifact-sweeper.md`; `codex/agents/z-artifact-sweeper.toml` | PENDING | PENDING |
| AC2 | AC2 | `AC2-consistency-auditor-contract` | Static source contract check; manual evaluator QA | Implemented; runtime QA pending | `.github/agents/05j-consistency-auditor.agent.md` and generated mirrors | `.github/agents/05j-consistency-auditor.agent.md:24-54`; `claude/agents/z-consistency-auditor.md`; `opencode/agents/05j-consistency-auditor.md`; `codex/agents/z-consistency-auditor.toml` | PENDING | PENDING |
| AC3 | AC3 | `AC3-dependency-auditor-contract` | Static source contract check; manual evaluator QA | Implemented; runtime QA pending | `.github/agents/05k-dependency-auditor.agent.md` and generated mirrors | `.github/agents/05k-dependency-auditor.agent.md:24-55`; `claude/agents/z-dependency-auditor.md`; `opencode/agents/05k-dependency-auditor.md`; `codex/agents/z-dependency-auditor.toml` | PENDING | PENDING |
| AC4 | AC4 | `AC4-report-and-degradation-contract` | Static contract inspection; manual failure-path QA | Implemented in instructions; runtime failure paths pending | All three source agents and generated mirrors | `.github/agents/05g-artifact-sweeper.agent.md:13-22,50-69`; `.github/agents/05j-consistency-auditor.agent.md:13-22,41-62`; `.github/agents/05k-dependency-auditor.agent.md:13-22,43-63`; `.github/skills/phase-final-review-conventions/SKILL.md`; `.github/skills/phase-final-review-report/SKILL.md` | PENDING | PENDING |
| AC5 | AC5 | `AC5-orchestrator-fixture-dry-run` | Manual QA through `05-phase-final-review` against `dev/phase-final-review/fixtures/` | Unverified — not run in this implementation session | Three source agents; orchestrator already references all three | `.github/agents/05-phase-final-review.agent.md:5,37-48`; `dev/phase-final-review/fixtures/README.md`; `dev/phase-final-review/fixtures/PHASE_05/` | PENDING | PENDING |
| AC6 | AC6 | `tests/test_propagate_master_assets.py` | Automated propagation suite | Complete | Source agents and generated Claude/OpenCode/Codex mirrors; no script change | `tests/test_propagate_master_assets.py`; `scripts/propagate_master_assets.py`; propagation output: 20 passed, 7 subtests | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Artifact sweeper covers debug statements, TODOs/FIXMEs, temporary flags, and introduced commented/dead code; uses graph dead-code detection scoped to phase-touched files. | Implemented; runtime QA pending | `05g-artifact-sweeper` source and mirrors | Cheap tier and graph-unavailable `NOT RUN` behavior are explicit. |
| AC2 | Consistency auditor detects naming, error-handling, and repeated-pattern drift and recommends canonical forms. | Implemented; runtime QA pending | `05j-consistency-auditor` source and mirrors | Fixture-specific Phase 01-vs-02 comparison is explicit. |
| AC3 | Dependency auditor inventories new dependencies, licenses, vulnerabilities, and competing/duplicate libraries without fetching or installing. | Implemented; runtime QA pending | `05k-dependency-auditor` source and mirrors | No-manifest-change behavior is an explicit completed check. |
| AC4 | All evaluators load shared conventions/report contracts, use canonical report paths, return concise summaries, and record incomplete/not-run conditions. | Implemented in instructions; runtime QA pending | All three source agents and mirrors | Baseline, empty-diff, missing-evidence, and dependency-failure semantics are documented. |
| AC5 | Each evaluator dry-runs through the final-review orchestrator against the development fixture and produces its report. | Unverified | Orchestrator plus all three source agents | No live delegated-agent execution was available in this implementation session; no report evidence is claimed. |
| AC6 | Propagation includes all three agents and the propagation test passes. | Complete | Source agents and generated mirrors | Script was idempotent with zero changes; source script was unchanged. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|--------------|--------------|-----|
| `.github/agents/05g-artifact-sweeper.agent.md` | Create | Added cheap-tier artifact sweep scope, graph `refactor_tool` dead-code invocation/filtering, report contract, and failure semantics. | Implements AC1 and part of AC4. |
| `.github/agents/05j-consistency-auditor.agent.md` | Create | Added cross-subphase naming, error-handling, and repeated-pattern drift checks with canonical recommendations. | Implements AC2 and part of AC4. |
| `.github/agents/05k-dependency-auditor.agent.md` | Create | Added phase-diff dependency, license, vulnerability, and duplicate-library inventory rules with read-only boundaries. | Implements AC3 and part of AC4. |
| `claude/agents/z-artifact-sweeper.md` | Generated | Propagated 05g to Claude's non-user-invocable agent output. | Implements AC6. |
| `claude/agents/z-consistency-auditor.md` | Generated | Propagated 05j to Claude's non-user-invocable agent output. | Implements AC6. |
| `claude/agents/z-dependency-auditor.md` | Generated | Propagated 05k to Claude's non-user-invocable agent output. | Implements AC6. |
| `opencode/agents/05g-artifact-sweeper.md` | Generated | Propagated 05g to OpenCode. | Implements AC6. |
| `opencode/agents/05j-consistency-auditor.md` | Generated | Propagated 05j to OpenCode. | Implements AC6. |
| `opencode/agents/05k-dependency-auditor.md` | Generated | Propagated 05k to OpenCode. | Implements AC6. |
| `codex/agents/z-artifact-sweeper.toml` | Generated | Propagated 05g to Codex with the non-user-invocable `z-` identifier. | Implements AC6. |
| `codex/agents/z-consistency-auditor.toml` | Generated | Propagated 05j to Codex with the non-user-invocable `z-` identifier. | Implements AC6. |
| `codex/agents/z-dependency-auditor.toml` | Generated | Propagated 05k to Codex with the non-user-invocable `z-` identifier. | Implements AC6. |
| `dev/feature/03-mechanical-evaluators/03-mechanical-evaluators-tasks.md` | Modify | Checked off completed implementation, prerequisite, and propagation tasks; left manual QA tasks unchecked. | Preserves task traceability and records AC5 gap. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | None | No new tests added; the plan explicitly identifies markdown assets and the existing propagation suite as the test surface. | Existing `tests/test_propagate_master_assets.py` covers propagation. |

## Test Results

- **Baseline**: 387 passed, 2 failed, 7 subtests (full suite; before implementation)
- **Final**: 387 passed, 2 failed, 7 subtests (full suite; after implementation)
- **Propagation baseline/final**: 20 passed, 7 subtests / 20 passed, 7 subtests
- **New tests added**: 0
- **Regressions**: None introduced. The same two pre-existing failures remain in `tests/hooks/test_hook_distribution_integration.py` (latency threshold and harness-classification text).

## Deviations from Plan

- AC5's four manual orchestrator dry-runs were not executed: no user-confirmed
  baseline was supplied, and the orchestrator's preflight requires explicit
  baseline confirmation before delegated execution. No runtime report is
  claimed.
- The required `rtk` command wrapper failed its global hook-integrity check, so
  equivalent read-only shell commands were used; the global hook was not changed.
- A repository-wide `git diff --check` is blocked by unrelated pre-existing
  CRLF/trailing-whitespace changes in `deepswe_20260709.csv`; feature files were
  separately checked and contain no trailing whitespace.

## Gaps

- AC5 remains unverified until the `05-phase-final-review` orchestrator can be
  run with user-confirmed baseline input and the fixture, including the
  graph-server unavailable path. The four corresponding manual QA tasks remain
  unchecked.

## Reviewer Focus Areas

- `.github/agents/05g-artifact-sweeper.agent.md:36-48` — verify graph results are filtered to introduced phase-diff code and unrelated dead code cannot leak into findings.
- `.github/agents/05j-consistency-auditor.agent.md:35-54` — verify canonical recommendations and the known fixture drift are evidenced during a real run.
- `.github/agents/05k-dependency-auditor.agent.md:30-55` — verify local license/vulnerability evidence is never represented as a clean result when unavailable.
- Generated Claude/OpenCode/Codex files — verify propagation parity with the source definitions.
