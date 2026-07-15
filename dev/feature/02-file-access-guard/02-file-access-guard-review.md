# Review Record: File-Access Guard

## Summary

Reviewed the complete Feature 02 implementation against AC1–AC10, including its data rules, reusable evaluator, hook adapter, source definition, fixtures, tests, and operator documentation. One High-severity Grep-scope matching gap was reproduced and fixed: exact protected credential-directory roots and overlapping wildcard scopes could evade the original matcher. The corrected implementation is green across feature, repository, coverage, legacy-unittest, and compile gates.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/lib/file_access.py:49`; `.github/hooks/config/file-access-rules.json:3`; `tests/hooks/test_file_access_guard.py:48` | Rule schema, stable identifiers, actions, reasons, priorities, and bypass escalation are data-driven; static AST evidence confirms protected-file policy is absent from Python. |
| AC2 | Verified | `.github/hooks/config/file-access-rules.json:4`; `.github/hooks/scripts/file-access-guard.py:30`; `tests/hooks/test_file_access_guard.py:118` | All five file-tool adapters deny environment variants and preserve the two exact template exceptions. |
| AC3 | Verified | `.github/hooks/config/file-access-rules.json:13`; `tests/hooks/test_file_access_guard.py:181` | Credential extensions, exact SSH names, protected directories, and the `id_generator.py` control execute as required. |
| AC4 | Verified | `.github/hooks/lib/file_access.py:252`; `.github/hooks/config/file-access-rules.json:76`; `tests/hooks/test_file_access_guard.py:202` | Lock, production, and project-override action/reason behavior is exercised through the merged framework configuration. |
| AC5 | Verified | `.github/hooks/lib/file_access.py:147`; `tests/hooks/test_file_access_guard.py:278` | Traversal, real and broken symlinks, supplied-home expansion, and controlled filesystem case behavior execute through one normalization pipeline. |
| AC6 | Verified after fix | `.github/hooks/lib/file_access.py:159`; `.github/hooks/lib/file_access.py:222`; `.github/hooks/scripts/file-access-guard.py:30`; `tests/hooks/test_file_access_guard.py:352` | Review fixes cover exact protected directory roots, independently varying wildcard overlaps, protected path-suffix globs, malformed input, ordinary searches, and Glob exclusion. |
| AC7 | Unverified | `.github/hooks/config/file-access-rules.json:94`; `tests/hooks/test_file_access_guard.py:464` | Unit behavior for source/generated paths, read-only inspection, and symlink aliases is verified. Real propagated consuming-project execution remains pending Feature 04's disposable harness. |
| AC8 | Verified | `.github/hooks/scripts/file-access-guard.py:68`; `tests/hooks/test_file_access_guard.py:514` | Executed assertions cover rule/path/reason/alternative guidance and prevent file bodies or full payloads from reaching output and audit logs. |
| AC9 | Unverified | `.github/hooks/scripts/file-access-guard.py:130`; `tests/hooks/test_file_access_guard.py:558` | Induced failures, protected-override recovery, environment-variable ineffectiveness, and unit-level bypass escalation are verified. A real `bypass-permissions` runner check remains pending Feature 04. |
| AC10 | Verified | `.github/hooks/lib/file_access.py:252`; `tests/hooks/test_file_access_guard.py:636` | The narrow public contract is exercised directly and imported in an isolated process without cwd/PYTHONPATH assumptions or runtime third-party/subprocess dependencies. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Grep scope matching allowed exact protected directory roots such as `.ssh` and missed wildcard intersections such as `prod*.*` and `config/prod*.json`, permitting scopes that can include protected files. | High | `.github/hooks/lib/file_access.py:159` | AC3, AC6 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/hooks/lib/file_access.py` | Added bounded independent wildcard sampling, protected suffix-overlap evaluation, and recursive directory-root matching with conservative fail-closed handling for excessive pattern complexity. | 1 |
| `tests/hooks/test_file_access_guard.py` | Added seven collected regressions for four credential-directory roots, two overlapping protected globs, and one ordinary-source control. | 1 |
| `docs/hooks/file-access-guard.md` | Corrected precedence documentation for concrete paths versus wildcard Grep scopes. | 1 |

## Remaining Concerns

- AC7/AC9: The real consuming-project `bypass-permissions` check is intentionally `NOT RUN`; Feature 04 must execute `.env` and generated-wiring attempts in its disposable runner harness.

## Test Coverage Assessment

- Covered: AC1–AC10 have automated unit/contract evidence; Feature 02 collected 90 passing scenarios after review fixes.
- Missing: Real propagated consuming-project and `bypass-permissions` execution evidence for AC7/AC9 remains assigned to Feature 04.
- Coverage: 73.20% combined hook runtime coverage; `.github/hooks/lib/file_access.py` 83% and `.github/hooks/scripts/file-access-guard.py` 94%.

## Risk Summary

- Wildcard intersection is intentionally conservative and fails closed when its bounded sample budget is exceeded, preferring a possible false-positive denial over a protected-scope bypass.
- New hook files are not represented as execution flows in the current graph; direct feature tests and isolated entrypoint execution supply the behavioral evidence.
- Final generated wiring and real runner behavior remain outside Feature 02 and must be closed by Feature 04 before phase completion.
