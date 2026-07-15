# Review Record: 01-review-foundation

## Summary

Reviewed the implementation record, plan, all listed source-of-truth assets,
generated variants, fixture assets, and the listed propagation test. The fixture
copies are byte-identical to the Phase 01/02 sources, the Phase 02 NO-GO case is
present, propagation is idempotent, and the targeted suite passes. Two Medium
implementation issues were fixed during review. AC4 remains runtime-unverified
because a live agent harness is unavailable; the full suite retains two
pre-existing failures.

## Verdict

<!-- Approved | Approved with Reservations | Changes Requested -->
Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified (static) | `.github/skills/phase-final-review-conventions/SKILL.md:13-152` | Required report-root, severity, read-only, model-tier, missing-artifact, partial-failure, and return-summary contracts are present; generated skill copies match. |
| AC2 | Verified (static) | `.github/skills/phase-final-review-report/SKILL.md:13-218` | Master QA, security rollup, AC regression, readiness, and Checks Not Run templates are present with severity ordering. |
| AC3 | Verified (manual) | `.github/skills/worktree-baseline/SKILL.md:27-134` | Baseline `48d37504bf7a` was checked out detached, HEAD and clean status matched, a spaced target path worked, and owned cleanup succeeded. |
| AC4 | Unverified | `.github/agents/05a-baseline-worktree.agent.md:8-52` | Static frontmatter, skill-loading, failure, verification, and return-limit contracts pass. A live spawn and observed path-plus-summary return still require the agent harness. |
| AC5 | Verified (manual) | `dev/phase-final-review/fixtures/README.md:3-36`; fixture tree; `.gitignore:5-9` | Inventory contains the required 5/6 artifacts, all 11 copies compare byte-for-byte with the Phase 01/02 sources, the NO-GO case is present, and only the fixture subtree is trackable. |
| AC6 | Verified for repository outputs | `claude/`, `opencode/`, `codex/` generated assets; `tests/test_propagate_master_assets.py` | Propagation returned zero changes on rerun and the targeted suite passed 19 tests plus 2 subtests. The plan's `.claude`/`$source` wording is a documented repository-convention divergence. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|--------|----------|-----------|-----|--------|
| 1 | Fixture ignore exception unignored all of `dev/phase-final-review/`, not only `fixtures/`. | Medium | `.gitignore:5-9` | AC5 | Fixed |
| 2 | Worktree collision policy was stated but the procedure's create/reuse/recreate branch was implicit; literal execution could call `git worktree add` for an existing target. | Medium | `.github/skills/worktree-baseline/SKILL.md:47-74` | AC3 | Fixed |
| 3 | Live 05a agent execution was not available for verification. | Medium | `.github/agents/05a-baseline-worktree.agent.md:12-50`; implementation record:98-101 | AC4 | Open |
| 4 | Plan references `.claude` outputs and `$source` tags, while the verified propagator emits `claude/`, `opencode/`, and `codex/` assets and tags hook JSON only. | Low | plan:8,77; implementation record:82-90 | AC6 | Open |
| 5 | Full suite remains red on two documented pre-existing integration tests. | Medium | `tests/hooks/test_hook_distribution_integration.py:207,216` | — | Open |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

## Fixes Applied
<!-- "None" if none -->

| File | What Changed | Issue # |
|------|--------------|---------|
| `.gitignore` | Added a re-ignore rule for other direct children of `dev/phase-final-review/`, preserving trackability only for `fixtures/**`. | 1 |
| `.github/skills/worktree-baseline/SKILL.md` | Made create/reuse/recreate decisions explicit, quoted paths, and created only a missing parent before registration. | 2 |
| `claude/skills/worktree-baseline/SKILL.md` | Regenerated the Claude copy from the corrected source skill. | 2 |
| `opencode/skills/worktree-baseline/SKILL.md` | Regenerated the OpenCode copy from the corrected source skill. | 2 |
| `codex/skills/worktree-baseline/SKILL.md` | Regenerated the Codex copy from the corrected source skill. | 2 |

## Remaining Concerns
<!-- "None" if all clear -->

- Issue #3: run `05a-baseline-worktree` through a live agent harness with a known SHA and verify the observed return is the absolute path plus no more than 10 summary lines.
- Issue #4: reconcile future plan language with the repository's actual propagation roots and metadata behavior.
- Issue #5: the two unrelated integration failures remain outside this feature's scope.

## Test Coverage Assessment
- Covered: AC1, AC2, AC3, AC5, and AC6 targeted propagation behavior.
- Missing: AC4 live agent spawn; full-suite green status (386 passed, 2 failed); automated tests for the manual Markdown contracts, which the plan explicitly excludes.

## Risk Summary
<!-- 2-5 bullets -->
- `.github/agents/05a-baseline-worktree.agent.md:48-52` — runtime return formatting is statically correct but not observed in a live harness.
- `tests/hooks/test_hook_distribution_integration.py:207,216` — full-suite failures are pre-existing and unrelated to this feature.
- Plan/output-root metadata divergence should be reconciled before downstream features depend on the written paths.
