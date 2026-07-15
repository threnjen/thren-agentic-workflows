# Review Record: WebFetch Exfiltration Guard

## Summary

Reviewed commit `849c019` against the feature plan, context, tasks, implementation
record, changed runtime/configuration files, fixtures, tests, and documentation.
Graph analysis rated the change medium-risk with a high 17-file blast radius. The
review found three in-scope fail-closed/parsing defects; all were fixed with five
new regression cases. Direct WebFetch and Bash URL analysis still share one
standard-library-only classifier, preserve action-first/priority-second selection,
and keep URL material out of decisions and audit records.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/scripts/file-access-guard.py:122`; `.github/hooks/file-access-guard.json`; `tests/hooks/test_file_access_guard.py:790` | Exact `WebFetch` wiring and recorded `tool_input.url` payloads cover deny, ask, allow, and fail-closed cases. |
| AC2 | Verified | `.github/hooks/lib/url_exfiltration.py:308`; `.github/hooks/lib/bash_analyzer.py:374` | Direct WebFetch and literal curl/wget operands reuse `analyze_url`; `lib.__all__` was not broadened. |
| AC3 | Verified | `.github/hooks/config/file-access-rules.json`; `tests/hooks/test_file_access_guard.py:744` | Known credential patterns and credential-named encoded shapes deny without reflecting matched material. |
| AC4 | Verified | `.github/hooks/lib/url_exfiltration.py:308`; `tests/hooks/test_bash_command_analyzer.py:598` | Ambiguous entropy asks in both consumers and escalates to deny in bypass mode. |
| AC5 | Verified | `.github/hooks/lib/url_exfiltration.py:216`; `tests/hooks/test_bash_command_analyzer.py:618` | Ordinary URL material and configured curl/wget literal request bodies pass without URL-exfiltration matches. |
| AC6 | Verified | `.github/hooks/lib/bash_analyzer.py:283`; `tests/hooks/test_bash_command_analyzer.py:579` | Direct, quoted, option-reordered, piped, and redirection-before/after-URL forms are covered; stronger actions and configured priority win deterministically. |
| AC7 | Verified | `.github/hooks/config/file-access-rules.json`; `.github/hooks/lib/url_exfiltration.py:85`; `tests/hooks/test_bash_command_analyzer.py:624` | Policy remains data-driven; missing command coverage and empty body-option configuration now fail closed. |
| AC8 | Verified | `.github/hooks/lib/url_exfiltration.py:216`; `tests/hooks/test_file_access_guard.py:845`; `docs/hooks/bash-command-limitations.md` | Missing/non-string URLs, malformed escapes in any URL component, invalid ports, unsafe configuration, and unsupported schemes fail closed; dynamic forms remain documented. |
| AC9 | Verified | `.github/hooks/scripts/file-access-guard.py:122`; `tests/hooks/test_file_access_guard.py:864` | Decisions and audit entries remain redacted; focused, full-suite, and coverage gates pass. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Malformed authority input, including nonnumeric ports and malformed escapes outside path/query segments, was accepted as an ordinary URL instead of failing closed. | High | `.github/hooks/lib/url_exfiltration.py:216` | AC8 | Fixed (applied during this review) |
| 2 | URL operand scanning stopped at shell redirections, so valid forms such as `curl > output URL` and `curl < input URL` bypassed URL classification. | High | `.github/hooks/lib/bash_analyzer.py:283` | AC6, AC8 | Fixed (applied during this review) |
| 3 | URL command configuration could omit a required curl/wget command or declare no body options without failing closed. | Medium | `.github/hooks/lib/bash_analyzer.py:283` | AC7, AC8 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/hooks/lib/url_exfiltration.py` | Reject control/whitespace characters and malformed percent escapes across the raw URL, and force validated port parsing. | 1 |
| `.github/hooks/lib/bash_analyzer.py` | Continue URL scanning across redirections while skipping their targets; require exact curl/wget coverage and nonempty option-shaped body-option configuration. | 2, 3 |
| `tests/hooks/test_file_access_guard.py` | Added fail-closed/redaction regressions for malformed authority escapes and invalid ports. | 1 |
| `tests/hooks/test_bash_command_analyzer.py` | Added redirection-before-URL deny cases and unsafe URL-command configuration regressions. | 2, 3 |

## Remaining Concerns

- An actual interactive WebFetch runner invocation remains `NOT RUN`; recorded
  PreToolUse payloads exercise the same entrypoint, but runner UI/enforcement
  behavior is reserved for the phase integration feature.
- Dynamic shell URL construction, aliases, substitutions, redirects followed by
  the remote server, DNS behavior, and request-body inspection remain intentionally
  unsupported and are documented under `LIMIT-DYNAMIC-URLS`.
- The knowledge graph did not infer direct test edges for several new helper/value
  nodes, although executed behavioral tests cover their public call paths.

## Test Coverage Assessment

- Focused hook suites: `207 passed`.
- Full repository suite: `340 passed`.
- Combined coverage gate: `340 passed`, `70.75%` total coverage
  (`--cov-fail-under=50`); `url_exfiltration.py` is 89%, `bash_analyzer.py` is
  90%, and `file-access-guard.py` is 92%.
- Additional gates: Python compilation, JSON parsing, and `git diff --check`
  passed.
- Five review regressions were added: two malformed-URL cases, two
  redirection-before-URL cases, and one unsafe-configuration test covering two
  invalid configurations.

## Risk Summary

- The malformed-authority and redirection-order bypasses are closed with direct
  regressions at the shared trust boundary.
- URL parsing remains bounded, network-free, subprocess-free, and redacted.
- Remaining risk is limited to explicitly documented dynamic/runtime shell and
  live-harness behavior, not the implemented deterministic URL paths.
