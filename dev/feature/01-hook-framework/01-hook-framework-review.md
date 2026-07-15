# Review Record: Hook Framework

## Summary

Reviewed the Feature 01 implementation against AC1–AC9, including the dynamically
loaded hook tests and the executable audit wrapper. Two fail-closed/fail-open
boundary defects were found and fixed with regression coverage. Automated
evidence is green; the four runner-constrained checks in AC8 remain explicitly
unverified and are reserved for the isolated live integration pass.

## Verdict
Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/lib/framework.py:74`; `tests/hooks/test_hook_framework.py:52` | Executed alias, serialized-input, context, malformed, empty, and invalid UTF-8 cases for all seven Phase 01 tools. |
| AC2 | Verified after fix | `.github/hooks/lib/framework.py:113`; `tests/hooks/test_hook_framework.py:143` | Executed `allow`/`ask`/`deny`, exit-code-2, and invalid direct-construction cases; emission now revalidates the public value type. |
| AC3 | Verified | `.github/hooks/lib/framework.py:150`; `tests/hooks/test_hook_framework.py:158` | Executed recursive precedence, immutable snapshots, cache hits, mtime invalidation, resolved-path isolation, missing layers, and invalid configuration cases. |
| AC4 | Verified after fix | `.github/hooks/lib/framework.py:230`; `.github/hooks/lib/framework.py:266`; `.github/hooks/scripts/audit-log.py:20`; `.github/hooks/scripts/audit-log.sh:14`; `tests/hooks/test_hook_framework.py:289`; `tests/hooks/test_hook_framework.py:496` | Security failures deny or block; audit parse/config/handler/directory/serialization/open/write and wrapper-startup failures return success without output. |
| AC5 | Verified | `.github/hooks/lib/framework.py:185`; `tests/hooks/test_hook_framework.py:332` | Executed defaults, environment, protected override, invalid value, and disabled-handler paths. |
| AC6 | Verified | `.github/hooks/lib/framework.py:279`; `.github/hooks/scripts/audit-log.py:26`; `tests/hooks/test_hook_framework.py:383` | Executed sentinel checks confirm allowlisted NDJSON excludes input, command, response, nested, and configuration bodies. |
| AC7 | Verified | `.github/hooks/lib/__init__.py:1`; `.github/hooks/lib/framework.py:97`; `tests/hooks/test_hook_framework.py:529` | Public exports are narrow, runtime imports are standard-library-only, and the audit entrypoint imports under isolated Python without cwd or `PYTHONPATH`. |
| AC8 | Partial / Unverified | `tests/hooks/fixtures/recorded_payloads.json:1`; `docs/hooks/hook-verification.md:40` | Automated fixture and exception evidence passed. Live bypass-mode `deny`, `ask`, exit-code-2, and subagent hook execution remain `NOT RUN`; an isolated live runner is required. |
| AC9 | Verified | `.github/hooks/lib/framework.py:1`; `tests/hooks/test_hook_framework.py:566` | The 1,000-invocation median budget assertion and stdlib/no-subprocess import audit passed in this review. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | A directly constructed `Decision` could bypass factory validation and emit an invalid permission action with exit code 0. | High | `.github/hooks/lib/framework.py:132`; `.github/hooks/lib/framework.py:252` | AC2, AC4 | Fixed (applied during this review) |
| 2 | The audit shell wrapper propagated a non-zero interpreter/pipeline exit instead of preserving observability fail-open behavior. | High | `.github/hooks/scripts/audit-log.sh:14` | AC4 | Fixed (applied during this review) |
| 3 | Live runner premise evidence for bypass-mode and subagent behavior has not been executed. | Medium | `docs/hooks/hook-verification.md:40` | AC8 | Open (not addressed) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/hooks/lib/framework.py` | Revalidated public `Decision` values at emission and within the security failure boundary. | 1 |
| `.github/hooks/scripts/audit-log.sh` | Removed the unnecessary `cat` pipeline and made interpreter failure explicitly non-blocking. | 2 |
| `tests/hooks/test_hook_framework.py` | Added invalid-decision and failing-wrapper regression tests. | 1, 2 |

## Remaining Concerns

- Issue #3: The four AC8 live checks require an explicitly isolated runner and must not be marked complete from static or payload-level evidence.

## Test Coverage Assessment
- Covered: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9; automated portion of AC8.
- Missing: Live bypass-mode structured `deny`, structured `ask`, exit-code-2 behavior, and hook execution for a subagent tool call.
- Results: 50 hook tests passed; 52 full pytest tests passed; 2 legacy unittest tests passed; compileall and `git diff --check` passed.

## Risk Summary
- `.github/hooks/lib/framework.py:123-147` — permission emission is security-sensitive; direct-construction regression coverage now enforces the allowed action set.
- `.github/hooks/scripts/audit-log.sh:14` — the executable wrapper now contains an explicit fail-open boundary and is exercised with a failing fake interpreter.
- `docs/hooks/hook-verification.md:40-43` — live runner semantics remain unknown until the isolated integration checklist is executed.
