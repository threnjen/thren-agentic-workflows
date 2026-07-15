# Review Record: Injection Scanner

## Summary

Feature 05 satisfies its automated scanner/framework acceptance gates after two review fixes. The review hardened regex configuration against an exponential-backtracking shape that escaped the original validator and made the source allowlist reject traversal syntax even when it resolves back into an approved directory. The scanner remains standard-library-only, redacts matched content, preserves allowed output, and fails closed. Live Claude Code suppression/warning behavior remains unrun, and the repository-wide Phase 01 propagated-guard latency prerequisite remains above budget.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/lib/framework.py`; `tests/hooks/test_hook_framework.py` | Exact PostToolUse fields are parsed without changing existing PreToolUse aliases or decision output. |
| AC2 | Verified | `.github/hooks/lib/injection_scanner.py`; `tests/hooks/test_injection_scanner.py` | NFKC, homoglyph, invisible-character, base64, and hex scan-copy paths pass without mutating raw output. |
| AC3 | Verified after fix | `.github/hooks/lib/injection_scanner.py:90`; `tests/hooks/test_injection_scanner.py:87` | Rule policy remains data-driven and immutable; unsafe nested and overlapping quantified regex shapes are rejected. |
| AC4 | Verified | `.github/hooks/lib/__init__.py`; `.github/hooks/lib/injection_scanner.py` | The lazy public loader/scanner API returns structured metadata without matched content. |
| AC5 | Verified (automated) | `.github/hooks/scripts/injection-scanner.py`; `tests/hooks/test_injection_scanner.py` | Configured block actions suppress output and emit a redacted no-retry/manual-inspection reason. Live runner behavior was not exercised. |
| AC6 | Verified (automated) | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/injection-scanner.py` | Warning responses use `additionalContext` and leave the original logical output intact. Live runner behavior was not exercised. |
| AC7 | Verified after fix | `.github/hooks/lib/injection_scanner.py:296`; `tests/hooks/test_injection_scanner.py:250` | Allowlisting requires existing repository-owned sources, rejects configured-root broadening, symlinks, missing paths, and traversal syntax, and inherits `self-hook-assets` protection. |
| AC8 | Verified | `.github/hooks/lib/injection_scanner.py`; `tests/hooks/test_injection_scanner.py` | Empty, binary, structured, capped, truncated, encoded, and deterministic strongest-match paths pass. |
| AC9 | Verified (automated) | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/injection-scanner.py` | Payload/config/processing/emission failures use the redacted fail-closed posture; project-only `guard.enabled` recovery passes. |
| AC10 | Verified with reservation | `.github/hooks/injection-scanner.json`; `tests/hooks/fixtures/injection/post-tool-use-payloads.json` | Built-in, Task, MCP, structured, malformed, binary-shaped, and truncated fixtures pass. The unrelated propagated-guard latency prerequisite remains red. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Regex validation accepted overlapping quantified alternation such as `(a|aa)+$`, permitting exponential backtracking and hook-budget exhaustion from a corpus configuration mistake. | High | `.github/hooks/lib/injection_scanner.py:98` | AC3, AC8, AC9 | Fixed during review |
| 2 | A source path containing `..` could qualify when traversal resolved back into an approved allowlist root, contrary to the feature's conservative traversal contract. | Medium | `.github/hooks/lib/injection_scanner.py:317` | AC7 | Fixed during review |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/hooks/lib/injection_scanner.py` | Rejected quantified alternation groups in configured regexes and rejected source paths containing traversal components before resolution. | 1, 2 |
| `tests/hooks/test_injection_scanner.py` | Added regressions for overlapping-alternation regex denial and an existing in-root target addressed through `..`. | 1, 2 |

## Remaining Concerns

- Disposable live Claude Code checks for real output suppression, warning attachment, Task/subagent handling, truncation behavior, and retry behavior remain **NOT RUN** and must not be inferred from unit tests.
- The repository-wide `test_ac9_propagated_guard_median_latency_is_below_50_ms` remains red at an observed median of approximately 98 ms. This is the pre-recorded Phase 01 propagation prerequisite assigned outside Feature 05, not a scanner regression.
- Regex safety uses conservative static rejection plus bounded input size; it is defense in depth rather than a proof that Python's backtracking engine has a hard execution timeout. Production corpus performance still requires Feature 06 benchmark coverage.

## Test Coverage Assessment

- Focused framework/scanner suite: `100 passed`.
- Hook coverage gate: `325 passed, 1 failed`; total hook-library coverage `89.46%`, above the required 50%. The sole failure is the known propagated-guard latency prerequisite.
- Full pytest suite: `339 passed, 1 failed`; the same known latency prerequisite is the only failure.
- Stdlib unittest discovery: `14 passed`.
- Additional gates: Python compilation and `git diff --check` passed.

## Risk Summary

- The shared framework extension retains boundary revalidation and redacted failure emission; no raw or matched output is included in scanner result metadata or response text.
- Encoded-candidate counts, decoded byte sizes, and scanned bytes remain explicitly bounded, and the newly covered quantified-alternation case cannot enter the runtime matcher.
- Allowlist decisions now reject traversal components before strict filesystem resolution, while existing repository containment and symlink checks remain intact.
- Automated evidence supports approval; live runner evidence and the inherited Phase 01 latency failure justify reservations.
