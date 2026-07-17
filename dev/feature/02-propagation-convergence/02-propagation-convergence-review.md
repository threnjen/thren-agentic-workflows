# Review Record: Propagation Convergence

## Summary

Reviewed implementation commit `04a7340` against AC1–AC8, with focused
attention to mutation-counter classification, bounded fixed-point behavior,
the convergence-to-preflight gate, active-home containment, per-harness
failure isolation, CLI gating, and watcher guidance. One preflight defect was
found and fixed: a destination whose parent chain contained an existing
regular file could pass full-set preflight and allow an earlier harness to
mutate before the invalid harness failed during copy.

## Verdict

Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `scripts/propagate_master_assets.py:1793`; `tests/test_propagate_master_assets.py:1051` | Bounded propagation requires a subsequent zero-mutation pass and aggregates changed-pass counters. |
| AC2 | Verified | `scripts/propagate_master_assets.py:1793` | `propagate_until_converged` is the reusable public convergence boundary. |
| AC3 | Verified | `scripts/propagate_master_assets.py:1894`; `tests/test_propagate_master_assets.py:1172` | Convergence failure returns before preflight or callbacks; the deployment-capable CLI returns before global generation. |
| AC4 | Verified | `scripts/propagate_master_assets.py:1727`; `scripts/propagate_master_assets.py:2034` | `propagate_once` remains the one-pass primitive while CLI mutation paths use convergence. |
| AC5 | Verified after fix | `scripts/propagate_master_assets.py:1843`; `tests/test_propagate_master_assets.py:1143` | Full-set preflight rejects containment escapes, symlinked parents, non-directory parent components, disallowed missing parents, unavailable ownership evidence, and unresolved collisions before any callback. |
| AC6 | Verified | `scripts/propagate_master_assets.py:1918`; `tests/test_propagate_master_assets.py:1166` | Copy failures are isolated, skip reconciliation for the failed harness, and preserve earlier verified results. |
| AC7 | Verified | `scripts/propagate_master_assets.py:1974`; `tests/test_propagate_master_assets.py:1194` | Watcher startup explicitly instructs operators to restart after propagator changes before migration or release verification. |
| AC8 | Verified | `scripts/propagate_master_assets.py:2023`; focused result assertions | Results separate pass counts, mutation totals, preflight failures, copy/reconciliation counts, and redacted failure categories. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Full-set preflight did not reject an existing non-directory component in a destination parent chain when parent creation was allowed. A valid earlier harness could therefore mutate before the invalid later harness failed during copy. | High | `scripts/propagate_master_assets.py:1870` | AC3, AC5 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `scripts/propagate_master_assets.py` | Rejects an existing non-directory parent-chain component with the structured `parent_not_directory` preflight category. | 1 |
| `tests/test_propagate_master_assets.py` | Added a two-harness regression proving the invalid parent blocks every copy callback. | 1 |

## Remaining Concerns

None within this feature's scope. Platform-specific destination selection and
concrete managed-copy/reconciliation behavior remain intentionally delegated
to Features 3 and 4.

## Test Coverage Assessment

- Focused post-fix result: 76 passed, 49 subtests passed.
- `git diff --check`: passed.
- Graph analysis: the propagator has a high two-hop blast radius (23 impacted
  files), but the changed convergence and deployment boundaries have direct
  behavior coverage for their planned success and failure paths.

## Risk Summary

- Counter classification fails closed: unknown nonzero integer counters are
  mutations, and malformed or negative counters block convergence.
- Convergence and full-set preflight complete before the first deployment
  callback.
- Per-harness callback exceptions are reduced to non-sensitive structured
  categories; successful earlier harnesses are not rolled back.
