# Review Record: Interceptor Retirement

## Summary

Reviewed commit `65c2c75` against AC1–AC10, including the retired source cut,
generated harness rosters, ownership-safe propagation cleanup, mixed-test
surgery, reduced-posture documentation, and live RTK/user-global registration
state. The deferred post-deletion assertion now executes normally. Two defects
were found and fixed: legacy retired assets were missing ownership hashes, and
the committed distribution digest still represented the temporary restored
entrypoint rather than the final surviving hook tree.

## Verdict

Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/`; `tests/hooks/test_hook_distribution_integration.py:77` | The descriptor, entrypoint, policy modules, analyzer, URL logic, and configurations are absent; the absence test ran without skipping. |
| AC2 | Verified | `.github/hooks/scripts/`; `~/.claude/settings.json`; runtime `rtk --version` | The rewrite hook and its user-global registration are absent; RTK 0.42.4 remains installed. |
| AC3 | Verified | `tests/hooks/test_hook_distribution_integration.py:109` | Direct Read and Bash payload scenarios execute against surviving hooks without a retired decision or audit row. |
| AC4 | Verified | `.github/hooks/lib/framework.py`; `.github/hooks/lib/injection_scanner.py`; focused hook suites | Framework, scanner, audit, and notification assets remain; focused regressions pass. |
| AC5 | Verified after fix | `scripts/propagate_master_assets.py:61`; `scripts/propagate_master_assets.py:81`; `tests/test_propagate_master_assets.py:739` | Cleanup is exact-path and ownership-hash/source-link gated. All retired regular assets now have explicit last-shipped hashes; collision, symlink, and idempotency tests pass. |
| AC6 | Verified | `tests/hooks/`; `tests/test_propagate_master_assets.py` | Guard-only suites and fixtures are removed; mixed scanner, distribution, and propagation coverage remains behavior-based. |
| AC7 | Verified | `.claude/settings.json`; `.codex/hooks.json`; `.opencode/plugins/`; `tests/hooks/test_hook_distribution_integration.py:85` | Generated rosters contain audit, notification, and scanner hooks only; no retired registration or plugin remains. |
| AC8 | Verified | `docs/hooks/file-access-guard.md`; `docs/hooks/installation.md`; `docs/hooks/prompt-injection-defense.md` | Active documentation states the reduced posture and does not present injection scanning as file/Bash authorization. |
| AC9 | Verified | Hook documentation; runtime `rtk --version` | Explicit RTK use remains supported and documented; only automatic rewriting was retired. |
| AC10 | Verified | Commit `65c2c75` file inventory | No Phase 01, Phase 02, or Phase 07 status document changed. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Ownership hardening omitted hashes for five previously retired `bash-safety`/`protect-files` assets, so stale owned regular copies would no longer be removed. | High | `scripts/propagate_master_assets.py:81` | AC5 | Fixed (applied during this review) |
| 2 | The distribution marker was committed before the final guard-entrypoint deletion and no longer matched the surviving hook asset tree. | Medium | `.github/hooks/.distribution-version:1` | AC1, AC7 | Fixed (regenerated and digest-verified during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `scripts/propagate_master_assets.py` | Added verified last-shipped SHA-256 ownership evidence for all five earlier retired hook assets. | 1 |
| `tests/test_propagate_master_assets.py` | Added completeness and hash-shape coverage for every explicit retired regular asset. | 1 |
| `.github/hooks/.distribution-version` | Updated the marker to the digest of the final post-deletion surviving hook tree. | 2 |

## Remaining Concerns

None.

## Test Coverage Assessment

- Covered: AC1–AC10.
- Focused post-fix result: 187 passed, 45 subtests passed.
- Full post-fix result: 345 passed, 119 subtests passed.
- Missing: none in feature scope. The prior source-absence skip is gone.

## Risk Summary

- Retired regular-file cleanup depends on an explicit last-shipped hash ledger; the new completeness test prevents silent omission when the retired path list changes.
- Symlink cleanup remains narrow: only a generated link resolving to the exact retired source path is removed, and symlinked parent directories are rejected.
- Runtime inventory confirms project and user-global PreToolUse wiring contains no retired interceptor while the surviving scanner/audit/notification roster remains present.
