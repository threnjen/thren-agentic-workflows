# Review Record: Injection Pattern Corpus

## Summary

Reviewed commit `72e19b0` against the feature plan, context, tasks, implementation record, production corpus, fixtures, benchmark, tests, documentation, and the upstream Feature 05 scanner/entrypoint contract. The corpus remains clean-room and data-driven, its two regexes are bounded and accepted by Feature 05's safety validator, every rule has bidirectional positive evidence, and the benchmark delegates normalization, decoding, matching, and strongest-match selection to the production scanner. One response-tier regression gap was found and fixed: the gates now reject any configuration that maps a high rule to warning or a medium/low rule to blocking even when fixture expectations drift with it.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/hooks/config/injection-patterns.json`; `docs/hooks/injection-benchmark.md` | Provenance is explicitly recorded as Phase 02 clean-room taxonomy. The surveyed pattern source was not opened or copied during review. |
| AC2 | Verified | `.github/hooks/config/injection-patterns.json`; `tests/hooks/fixtures/injection/markdown-smuggling.json` | All five required categories are non-empty; link title, image alt, reference definition, HTML/code comments, and HTML attribute channels replay successfully. |
| AC3 | Verified | `.github/hooks/config/injection-patterns.json`; `.github/hooks/lib/injection_scanner.py` | All seven rules load through the upstream immutable schema with unique identifiers, explicit metadata, safe matchers, and deterministic priority. |
| AC4 | Verified | `tests/hooks/fixtures/injection/positive.json`; `tests/hooks/fixtures/injection/markdown-smuggling.json`; `tests/hooks/test_injection_corpus.py` | Exact bidirectional rule-to-fixture coverage passes, including strongest-match metadata. |
| AC5 | Verified with reservation | `tests/hooks/fixtures/injection/negative.json`; `tests/hooks/test_injection_corpus.py` | Seven required legitimate content classes run directly through `scan_output` without allowlisting and have no matches. The evidence is intentionally small and synthetic, so its false-positive conclusion is corpus-bounded. |
| AC6 | Verified after fix | `tests/hooks/injection_benchmark.py:133`; `tests/hooks/test_injection_corpus.py:255` | Benchmark output is deterministic, count-only, cwd-independent, redacted on invalid input, and non-zero for misses, invalid inventory, or response-tier drift. Scanner behavior is not reimplemented. |
| AC7 | Verified after fix | `tests/hooks/injection_benchmark.py:135`; `tests/hooks/test_injection_corpus.py:185` | High rules are now required to block and medium/low rules to warn at both the benchmark inventory gate and entrypoint response test. All negatives have zero high-tier false positives. |
| AC8 | Verified | `tests/hooks/fixtures/injection/positive.json`; `tests/hooks/test_injection_corpus.py` | Plain, NFKC, homoglyph, zero-width, base64, hex, leetspeak, multi-match, and markdown variants resolve as expected; the representative corpus timing gate passes. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Response tests and benchmark inventory trusted configured actions, so a high rule could drift to `warn` (or a lower tier to `block`) and still pass if fixture expectations were updated to match. | Medium | `tests/hooks/injection_benchmark.py:133`; `tests/hooks/test_injection_corpus.py:185` | AC6, AC7 | Fixed during review |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/hooks/injection_benchmark.py` | Added exact severity inventory and severity-to-response policy validation to the benchmark pass gate. | 1 |
| `tests/hooks/test_injection_corpus.py` | Asserted high-to-block and medium/low-to-warn behavior for every rule and added a regression proving synchronized config/fixture tier drift still fails the benchmark. | 1 |

## Remaining Concerns

- Disposable live high-block and warning checks across Claude, Codex, and OpenCode remain **NOT RUN**; Feature 07 owns propagation and runner-constrained evidence.
- The full repository suite still has the manifest-recorded Phase 01 propagated-guard latency failure: observed median approximately 97 ms against a 50 ms gate. This feature's focused scanner/corpus suites pass and do not modify that integration path.
- The zero-false-positive result applies to seven synthetic negative fixtures. They cover all required content-class labels and plausible neighboring prose, but they are not a broad empirical sample of real repository or third-party output.

## Test Coverage Assessment

- Corpus suite: `23 passed`.
- Combined scanner and corpus suites: `63 passed`.
- Deterministic benchmark: `19` true positives, `0` misses, `0` false positives, `0` high-tier false positives, and `0` skipped fixtures.
- Full repository suite: `362 passed, 1 failed`; the sole failure is the known propagated-guard latency prerequisite.
- Additional gate: `git diff --check` passed.

## Risk Summary

- Graph review reported 29 directly changed nodes and a high two-hop structural blast radius of 281 nodes across 19 additional files, reflecting reuse of shared scanner-loading helpers; no affected execution flow was inferred for the fixture/benchmark-only change.
- The corpus contains only fixed strings and two short regexes. Both regexes are linear-looking, contain no nested or quantified alternation, and pass Feature 05's conservative validator under the configured scan-byte cap.
- Benchmark code performs only duplicate-safe JSON loading, fixture replay, policy/count aggregation, and redacted formatting; all normalization, encoded-candidate decoding, matching, and strongest-rule selection stay in `.github/hooks/lib/injection_scanner.py`.
- Production reasons and posture text are fixed metadata. Benchmark output contains no fixture bodies, matched spans, pattern strings, or secret material.
