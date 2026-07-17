# Review Record: Cross-Platform Destinations

## Summary

Reviewed implementation commit `f18acd8` against AC1–AC8, with focused
attention to platform classification, documented relocation variables,
path-flavor normalization, active-home containment, content-safe errors,
destination-leaf preservation, and the post-convergence handoff. One boundary
defect was found and fixed: existing native Windows junctions in a destination
parent chain were not rejected before downstream mutation.

## Verdict

Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `scripts/runtime_deployment.py:51`; `scripts/runtime_deployment.py:73`; `tests/test_phase04_runtime_deployment.py:39` | Immutable records cover the eight supported generated asset classes with explicit source, destination, active-home boundary, and status fields. |
| AC2 | Verified | `scripts/runtime_deployment.py:73`; `scripts/runtime_deployment.py:178`; override matrix tests | Claude agents, commands, skills, and learnings use the default or validated `CLAUDE_CONFIG_DIR` root; hooks remain outside this stage. |
| AC3 | Verified | `scripts/runtime_deployment.py:115`; `scripts/runtime_deployment.py:178`; `tests/test_phase04_runtime_deployment.py:101` | `CODEX_HOME` relocates Codex-owned agents only, must be an existing directory, and does not relocate shared skills. |
| AC4 | Verified | `scripts/runtime_deployment.py:73`; `tests/test_phase04_runtime_deployment.py:101` | `OPENCODE_CONFIG_DIR` relocates generated config-owned agents while skills remain at the documented user path; undocumented XDG behavior is ignored. |
| AC5 | Verified | `scripts/runtime_deployment.py:91`; `scripts/runtime_deployment.py:105`; platform matrix tests | POSIX and case-insensitive Windows path flavors normalize beneath the injected active home/profile without elevated links. |
| AC6 | Verified | `scripts/runtime_deployment.py:27`; `scripts/runtime_deployment.py:91`; `tests/test_phase04_runtime_deployment.py:183` | WSL is mutually exclusive with native Windows and rejects mounted Windows-drive overrides. |
| AC7 | Verified | `scripts/runtime_deployment.py:18`; `scripts/runtime_deployment.py:115`; `tests/test_phase04_runtime_deployment.py:199` | Relative, empty, NUL-bearing, cross-environment, and outside-home overrides fail with category-only diagnostics before mutation. |
| AC8 | Verified after fix | `scripts/runtime_deployment.py:150`; `tests/test_phase04_runtime_deployment.py:227`; `tests/test_phase04_runtime_deployment.py:263` | Parent validation now rejects both symbolic links and native Windows junctions while leaving the destination leaf unresolved for Feature 4 classification. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Existing destination-parent junctions were not detected because `_check_existing_parents` checked only `is_symlink()`. On native Windows, a junction could therefore redirect a later managed copy outside the declared active-home boundary. | High | `scripts/runtime_deployment.py:150` | AC7, AC8 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `scripts/runtime_deployment.py` | Rejects an existing parent component reported by `Path.is_junction()` with the content-safe `junction_parent` category. | 1 |
| `tests/test_phase04_runtime_deployment.py` | Added a mocked junction-parent regression that is deterministic on the macOS review runner and proves rejection happens during resolution. | 1 |

## Remaining Concerns

Live native Windows junction behavior and live WSL environment discovery remain
runner-constrained and belong to Feature 6 runtime verification. The policy and
failure branch are covered deterministically here; no unresolved feature-scope
finding remains.

## Test Coverage Assessment

- Focused post-fix result: 67 passed, 0 failed.
- Full post-fix result: 88 passed, 0 failed.
- `git diff --check`: passed.
- Graph analysis rated the implementation medium risk with a high two-hop blast
  radius (25 impacted files). The graph did not associate file-level tests with
  the new module, but direct scenario tests cover every acceptance criterion,
  including the corrected junction branch.

## Risk Summary

- Platform classification is single-valued and injectable; WSL cannot be
  classified as native Windows in the same run.
- Only documented relocation variables are read, and submitted path content is
  excluded from exception messages and normal inventory output.
- Lexical normalization and active-home containment occur before existing
  parent inspection; parent links are rejected without dereferencing the final
  destination leaf.
- `resolve_destinations_after_convergence` rejects absent, invalid, or
  unconverged results before invoking destination resolution.
