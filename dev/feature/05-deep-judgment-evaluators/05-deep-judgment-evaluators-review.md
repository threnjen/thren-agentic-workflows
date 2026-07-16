# Review Record: 05-deep-judgment-evaluators

## Summary

Reviewed the implementation record first, then the feature plan, all 17 files
listed in its Files Changed table, and the relevant graph/test evidence. The
three evaluator contracts and generated mirrors now align with the plan after
fixes for propagation coverage, read-only permissions, verifier artifact
naming, and contradictory test-count documentation. Static review confirms the
agent contracts and `get_bridge_nodes` is available on the live graph server.
The required orchestrator dry-runs remain unavailable in this environment.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified (static contract) | `.github/agents/05b-change-narrator.agent.md:15-72`; Claude/OpenCode/Codex mirrors | Baseline-to-HEAD procedure, bounded chunking, subphase attribution, churn hotspots, baseline failure path, top-tier requirement, report path, and return limit are present. Runtime narrative/chunk visibility is covered by the AC5 reservation. |
| AC2 | Verified (static contract) | `.github/agents/05e-ac-regression.agent.md:16-98`; generated mirrors | Complete AC enumeration, one verifier per subphase, row-count validation, status vocabulary, not-verifiable counting, regression attribution, baseline fallback, and unique verifier artifacts are specified. Live matrix generation is not observed. |
| AC3 | Verified (static contract; graph operation live-checked) | `.github/agents/05f-seam-analyzer.agent.md:15-76`; generated mirrors | Interface/duplication/orphan checks, exact `get_impact_radius`/`get_bridge_nodes` calls, degradation, and no-seams conclusion are specified. Live evaluator behavior remains part of AC5. |
| AC4 | Verified (static contract) | All three source agents and generated mirrors; source frontmatter at lines 4-5 | Shared conventions, report locations, read-only posture, partial-failure rules, baseline handling, and the ≤10-line contract are present; execute/Bash permissions were removed. |
| AC5 | Unverified | `dev/feature/05-deep-judgment-evaluators/05-deep-judgment-evaluators-tasks.md:18,30,40,46` | Requires four orchestrator/manual dry-runs: 05b chunk/narrative, 05e 26-row matrix, 05f graph available/stopped, and ≤10-line returns. No agent/orchestrator runtime is available here. |
| AC6 | Verified | `tests/test_propagate_master_assets.py:86-139`; generated agent outputs; propagation command | Propagation reports zero generated-output drift; targeted suite passes with 21 tests and 13 subtests. The test now covers 05b, 05c, 05d, 05e, 05f, and 05h. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Propagation coverage omitted the three new evaluator slugs, allowing stale 05b/05e/05f mirrors to pass the test. | High | `tests/test_propagate_master_assets.py:89-95` | AC6 | Fixed (applied during this review) |
| 2 | New evaluator source contracts and generated Claude/OpenCode permissions exposed shell execution despite the read-only contract and 05e’s no-test-execution rule. | High | `.github/agents/05b-change-narrator.agent.md:4`, `.github/agents/05e-ac-regression.agent.md:4`, `.github/agents/05f-seam-analyzer.agent.md:4`; generated frontmatter | AC4 | Fixed (applied during this review) |
| 3 | 05e gave concurrent hidden verifiers a shared directory but no required unique filename, allowing report overwrites. | Medium | `.github/agents/05e-ac-regression.agent.md:57-63`; generated mirrors | AC2 | Fixed (applied during this review) |
| 4 | The task record reported 382 full-suite passes while the implementation record and observed run report 388. | Medium | `dev/feature/05-deep-judgment-evaluators/05-deep-judgment-evaluators-tasks.md:45`; implementation record:73-75 | AC6 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/agents/05b-change-narrator.agent.md` | Removed `execute` from the source tool list. | 2 |
| `.github/agents/05e-ac-regression.agent.md` | Removed `execute` and required a subphase-derived verifier report filename. | 2, 3 |
| `.github/agents/05f-seam-analyzer.agent.md` | Removed `execute` from the source tool list. | 2 |
| `claude/agents/z-change-narrator.md` | Removed `Bash` from generated permissions. | 2 |
| `claude/agents/z-ac-regression.md` | Removed `Bash` and synchronized the verifier filename contract. | 2, 3 |
| `claude/agents/z-seam-analyzer.md` | Removed `Bash` from generated permissions. | 2 |
| `opencode/agents/05b-change-narrator.md` | Removed `bash: allow`. | 2 |
| `opencode/agents/05e-ac-regression.md` | Removed `bash: allow` and synchronized the verifier filename contract. | 2, 3 |
| `opencode/agents/05f-seam-analyzer.md` | Removed `bash: allow`. | 2 |
| `codex/agents/z-ac-regression.toml` | Synchronized the verifier filename contract. | 3 |
| `tests/test_propagate_master_assets.py` | Added 05b, 05e, and 05f to generated-harness/parity and read-only permission coverage. | 1, 2 |
| `dev/feature/05-deep-judgment-evaluators/05-deep-judgment-evaluators-tasks.md` | Corrected the full-suite pass count to 388. | 4 |
| `.github/learnings/review-learnings.md` | Added the durable rule that parallel verifiers need child-derived artifact paths. | 3 |
| `claude/learnings/review-learnings.md` | Synchronized the new review learning mirror. | 3 |

## Remaining Concerns

- AC5 remains unverified until the Phase Final Review orchestrator can run the four fixture/manual checks listed in the task record.
- The full suite still has two pre-existing failures in `tests/hooks/test_hook_distribution_integration.py` (latency threshold and installation-guide classification); the targeted propagation suite and all review fixes pass.

## Test Coverage Assessment

- Covered: AC1–AC4 by static contract review; AC6 by propagation regeneration and `uv run pytest tests/test_propagate_master_assets.py -q` (21 passed, 13 subtests).
- Missing: AC5 live/manual orchestrator evidence for 05b, 05e, 05f, and the ≤10-line return summaries. Full-suite validation after fixes: 388 passed, 2 known pre-existing failures, 13 subtests.

## Risk Summary

- Runtime report creation and degradation behavior are not observed until the Phase Final Review orchestrator dry-runs are available.
- Generated asset parity is now validated for all six delegating/deep-judgment evaluator slugs, but harness execution itself remains outside this environment.
- The repository-wide suite is not fully green because of the two documented pre-existing hook-distribution failures.
