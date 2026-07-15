# Review Record: Bash-Command Analyzer

## Summary

Reviewed the implementation record, plan, changed source/config/tests/docs, and
the exact legacy sources. The 16 `bash-safety.sh` fixed strings and 11
`protect-files.py` Bash regexes are represented exactly in the parity metadata
and replay fixture. Adversarial execution found three in-scope parser/policy
issues; all High and Medium findings were fixed with regression coverage. The
single runtime flow still emits one deny-over-ask decision and keeps command
bodies out of reasons and audit fields.

## Verdict
<!-- Approved | Approved with Reservations | Changes Requested -->

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/lib/bash_analyzer.py:161`; `tests/hooks/test_bash_command_analyzer.py:94` | Automated direct/indirect coverage now includes protected JSON and production-config names ending in `n`. |
| AC2 | Verified | `.github/hooks/lib/bash_analyzer.py:172`; `tests/hooks/test_bash_command_analyzer.py:133` | Short, long, combined-option creation and real symlink traversal execute as deny-tier tests. |
| AC3 | Verified | `tests/hooks/fixtures/bash/commands.json`; `docs/hooks/bash-command-limitations.md:7`; `tests/hooks/test_bash_command_analyzer.py:182` | Every named evasion class is covered or tied to an explicit reproducible limitation. |
| AC4 | Verified | `.github/hooks/config/file-access-rules.json:15`; `tests/hooks/test_bash_command_analyzer.py:212` | Env dumps and variable echo ask; assignment/export controls allow. |
| AC5 | Verified | `.github/hooks/lib/bash_analyzer.py:230`; `tests/hooks/test_bash_command_analyzer.py:230` | Spaced, equals, and attached short upload forms deny protected paths; literal curl data is not misclassified as a file upload. Reasons remain command-free. |
| AC6 | Verified | `.github/hooks/config/file-access-rules.json:34`; `tests/hooks/test_bash_command_analyzer.py:274` | Exact legacy forms plus split/long recursive-force options and compact device redirects ask. Approved roots remain narrow and cannot override protected-path denies or symlink escapes. |
| AC7 | Verified | `.github/hooks/config/file-access-rules.json:94`; `tests/hooks/fixtures/bash/legacy-parity.json`; `tests/hooks/test_bash_command_analyzer.py:361` | Manual source comparison and replay confirm 16 fixed strings plus 11 regex behaviors with explicit retier rationale. |
| AC8 | Verified | `.github/hooks/scripts/file-access-guard.py:77`; `.github/hooks/scripts/file-access-guard.py:127`; `tests/hooks/test_bash_command_analyzer.py:397` | Behavioral tests verify one strongest decision, malformed fail-closed output, redacted recording, bypass ask preservation, shared path imports, and no command execution. Live runner behavior remains delegated to Feature 04. |
| AC9 | Verified | `docs/hooks/bash-command-limitations.md:28`; `docs/hooks/hook-verification.md:52`; `tests/hooks/test_bash_command_analyzer.py:523` | Recursive parent scans and dynamic interpretation boundaries document risk, boundary, and safer alternatives. Runner-constrained rows honestly remain `NOT RUN`. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | `rstrip("\\n")` removed any trailing `n` or backslash from operands, allowing protected JSON/config filenames to evade matching. | High | `.github/hooks/lib/bash_analyzer.py:167` | AC1 | Fixed (applied during this review) |
| 2 | Combined symlink flags and attached curl short data options were not recognized; curl literal data was also treated as a path. | High | `.github/hooks/lib/bash_analyzer.py:172`; `.github/hooks/lib/bash_analyzer.py:248` | AC2, AC5 | Fixed (applied during this review) |
| 3 | Split/long recursive-force `rm` options and compact `/dev` redirects bypassed the configured ask tier. | Medium | `.github/hooks/config/file-access-rules.json:40`; `.github/hooks/config/file-access-rules.json:70` | AC6 | Fixed (applied during this review) |
| 4 | Bash rule `priority` is validated and stored, but same-action selection uses configuration order; e.g. overlapping `git clean -f`/`-fd` matches may record the less-specific rule. Security action precedence is unaffected. | Low | `.github/hooks/lib/bash_analyzer.py:61`; `.github/hooks/scripts/file-access-guard.py:127` | AC8 | Open (not addressed) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/hooks/lib/bash_analyzer.py` | Exact suffix removal, configured combined-short-option recognition, attached curl short upload handling, and file-reference-only curl evaluation. | 1, 2 |
| `.github/hooks/config/file-access-rules.json` | Added data-driven ask rules for equivalent recursive-force deletion and compact device redirection forms. | 3 |
| `tests/hooks/test_bash_command_analyzer.py` | Added 13 collected regressions for protected suffixes, option forms, literal curl data, destructive variants, and approved-root containment. | 1, 2, 3 |

## Remaining Concerns

- Issue #4: same-tier Bash priority affects audit specificity only; defer until the public match/selection contract intentionally carries priority.
- Live Bash deny/ask behavior in the actual runner remains `NOT RUN` by design and must be executed through Feature 04's disposable consuming-project integration.
- Optional Ruff execution was unavailable because Ruff is not installed by `requirements-dev.txt`; the repository defines no Ruff lint configuration, so this was not treated as a required gate.

## Test Coverage Assessment
- Covered: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9; 79 focused tests pass, 221 full pytest tests pass, 219 hook coverage tests pass at 89.70% combined coverage (90% analyzer), 2 legacy unittest tests pass, Python compilation and JSON parsing pass.
- Missing: runner-constrained live Bash deny, bypass-permissions ask, and live redaction observation; these are explicitly assigned to Feature 04 and are not inferred from payload-level tests.

## Risk Summary
<!-- 2-5 bullets -->
- `.github/hooks/lib/bash_analyzer.py:161-269` remains a deliberately bounded tokenizer, not a full shell interpreter; unsupported expansion/interpreter classes are documented and fixture-locked.
- `.github/hooks/scripts/file-access-guard.py:127` correctly enforces deny over ask, but same-tier rule attribution remains configuration-order dependent.
- Live harness semantics are unverified until Feature 04 runs the recorded disposable-runner checklist.
