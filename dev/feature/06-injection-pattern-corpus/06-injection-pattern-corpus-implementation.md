# Implementation Record: Injection Pattern Corpus

## Summary

Implemented an original clean-room production corpus with seven validated rules across all five Phase 02 categories, bidirectionally complete synthetic positive fixtures, realistic negative fixtures, markdown-native smuggling coverage, a cwd-independent deterministic benchmark over Feature 05's `load_injection_rules` and `scan_output` APIs, redacted benchmark documentation, tier-response checks, and representative performance coverage.

## Sibling Features

- `05-injection-scanner` supplies the finalized immutable rule schema, normalization, bounded decoding, deterministic strongest-match selection, `load_injection_rules`, `scan_output`, and the PostToolUse response boundary. No upstream scanner file was modified.
- `05-webfetch-exfiltration-guard` is file-disjoint and owns URL exfiltration policy; no URL signatures were added to this corpus.
- `07-multi-harness-integration` consumes the production config and benchmark evidence, propagates them to other harnesses, and owns disposable live block/warn evidence.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Original clean-room corpus | Clean-room provenance and production validation | Phase taxonomy provenance, original patterns, no surveyed source use | Complete | `.github/hooks/config/injection-patterns.json`, `docs/hooks/injection-benchmark.md` | `tests/hooks/test_injection_corpus.py::test_ac1_ac3_production_corpus_is_valid_complete_and_original`, `docs/hooks/injection-benchmark.md` | PENDING | PENDING |
| AC2 | Required categories | Category and markdown channel inventory | Five non-empty categories plus link title, image alt, reference definition, comments, and HTML attribute replay | Complete | `.github/hooks/config/injection-patterns.json`, `tests/hooks/fixtures/injection/markdown-smuggling.json` | `tests/hooks/test_injection_corpus.py::test_ac2_markdown_smuggling_covers_every_required_channel`, positive replay tests | PENDING | PENDING |
| AC3 | Complete rule schema | Production load and invalid mutation cases | Unique IDs, complete fields, enum validation, unsafe regex rejection, redacted failures | Complete | `.github/hooks/config/injection-patterns.json` | `tests/hooks/test_injection_corpus.py::test_ac1_ac3_production_corpus_is_valid_complete_and_original`, `test_ac3_invalid_schema_fails_redacted` | PENDING | PENDING |
| AC4 | Per-rule positive evidence | Bidirectional inventory and positive replay | Every rule evidenced; every fixture references a configured rule and exact result metadata | Complete | `tests/hooks/fixtures/injection/positive.json`, `tests/hooks/fixtures/injection/markdown-smuggling.json` | `tests/hooks/test_injection_corpus.py::test_ac4_rule_fixture_inventory_is_bidirectionally_complete`, `test_ac2_ac4_ac8_positive_replay_uses_production_scanner` | PENDING | PENDING |
| AC5 | Realistic negative evidence | Named negative content classes | Security/hook docs, code, markdown, authority/persona prose, encoded data; no allowlist path | Complete | `tests/hooks/fixtures/injection/negative.json` | `tests/hooks/test_injection_corpus.py::test_ac5_negative_corpus_is_realistic_and_has_no_matches` | PENDING | PENDING |
| AC6 | Measurable benchmark | Determinism, broken expectation, cwd independence | Total/category/tier counts, redacted output, non-zero failure, direct production API calls | Complete | `tests/hooks/injection_benchmark.py`, `docs/hooks/injection-benchmark.md` | `tests/hooks/test_injection_corpus.py::test_ac6_benchmark_reports_deterministic_redacted_counts`, `test_ac6_benchmark_returns_nonzero_for_broken_expectation`, `test_ac6_benchmark_invocation_is_cwd_independent` | PENDING | PENDING |
| AC7 | High-tier false-positive gate | Tier response replay and negative benchmark | Zero high false positives; every block proves no-retry suppression; every warn tier preserves output | Complete | `.github/hooks/config/injection-patterns.json`, benchmark and fixtures | `tests/hooks/test_injection_corpus.py::test_ac7_each_rule_obeys_configured_response_contract`, benchmark recorded result | PENDING | PENDING |
| AC8 | Obfuscation equivalence and performance | Variant replay and representative workload | NFKC, homoglyph, zero-width, base64, hex, leetspeak, markdown channels; median under 50 ms | Complete | `tests/hooks/fixtures/injection/positive.json`, `tests/hooks/fixtures/injection/markdown-smuggling.json` | `tests/hooks/test_injection_corpus.py::test_ac2_ac4_ac8_positive_replay_uses_production_scanner`, `test_ac8_representative_large_output_stays_within_latency_budget` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Original clean-room corpus | Complete | Production config and benchmark doc | Authored only from Phase 02 taxonomy/context; surveyed pattern source was not opened or copied. |
| AC2 | Required categories | Complete | Production config and markdown fixtures | Seven rules cover all five categories; six markdown-native channels are replayed. |
| AC3 | Complete rule schema | Complete | Production config | Final Feature 05 schema is authoritative; rules load immutably through its validator. |
| AC4 | Per-rule positive evidence | Complete | Positive and markdown fixtures | Exact bidirectional inventory is enforced. |
| AC5 | Realistic negative evidence | Complete | Negative fixtures | Seven required legitimate content classes scan without allowlisting and produce no matches. |
| AC6 | Measurable benchmark | Complete | Benchmark harness and documentation | Recorded 19 true positives, 0 misses, 0 false positives, and 0 skipped fixtures. |
| AC7 | High-tier false-positive gate | Complete | Config, fixtures, benchmark, response tests | Zero high-tier false positives; high rules block/no-retry and warn rules preserve raw output. |
| AC8 | Obfuscation equivalence and performance | Complete | Variant fixtures and corpus tests | All required variants resolve to intended rules; representative workload stays below the 50 ms median gate. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/config/injection-patterns.json` | Created | Added clean-room provenance, scan limits, and seven complete production rules | Supply data-driven policy to the Feature 05 scanner |
| `tests/hooks/injection_benchmark.py` | Created | Added cwd-independent deterministic replay and redacted human/JSON count output | Provide the measurable corpus gate without duplicating scanner logic |
| `docs/hooks/injection-benchmark.md` | Created | Documented provenance, invocation, recorded counts, evidence classes, redaction, and limits | Make benchmark use and review decisions reproducible |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_injection_corpus.py` | Created | Added schema, inventory, replay, response, benchmark, failure, cwd, and timing tests | AC1-AC8 |
| `tests/hooks/fixtures/injection/positive.json` | Created | Added per-rule positives plus normalization, encoding, leetspeak, and multi-match variants | AC2, AC4, AC8 |
| `tests/hooks/fixtures/injection/negative.json` | Created | Added seven realistic legitimate content classes | AC5, AC6, AC7 |
| `tests/hooks/fixtures/injection/markdown-smuggling.json` | Created | Added link-title, image-alt, reference-definition, HTML/code-comment, and HTML-attribute cases | AC2, AC4, AC8 |

## Test Results
- **Baseline**: 40 passed, 0 failed in `tests/hooks/test_injection_scanner.py` before corpus implementation; the new corpus suite then failed as expected because all production corpus artifacts were absent.
- **Final**: 22 passed, 0 failed in `tests/hooks/test_injection_corpus.py`; benchmark passed with 19 true positives, 0 misses, 0 false positives, and 0 skipped; 361 passed, 1 failed in the exact complete pytest suite due only to the manifest-recorded `test_ac9_propagated_guard_median_latency_is_below_50_ms`; 347 passed, 1 deselected with 89.92% hook-library coverage; 14 passed, 0 failed in stdlib unittest discovery.
- **New tests added**: 22 pytest cases, including eight parameterized invalid-schema cases, malformed/duplicate JSON cases, empty-category rejection, and two positive replay fixture groups.
- **Regressions**: No corpus, scanner, response, or stdlib regression. The single exact-suite failure is the pre-existing propagated-guard latency prerequisite already assigned to Feature 07.

## Deviations from Plan

- Finalized all proposed paths exactly as `.github/hooks/config/injection-patterns.json`, `tests/hooks/test_injection_corpus.py`, `tests/hooks/injection_benchmark.py`, the three planned fixture paths, and `docs/hooks/injection-benchmark.md`.
- Finalized the benchmark machine summary as `passed`, `inventory_valid`, `fixtures`, `totals`, `per_category`, and `tier_counts`; default output includes human-readable counts plus a sorted `summary-json` line.
- Used seven production rules as the smallest measured set that covers all required categories, all three severity tiers, and the required response evidence.

## Gaps

- Disposable live high block and medium/low warning checks in propagated Claude, Codex, and OpenCode harnesses are `NOT RUN`; Feature 07 owns propagation and runner-constrained evidence.
- The exact full pytest and coverage commands remain red only on the execution manifest's pre-existing propagated-guard latency test. All other tests pass, and coverage was verified above threshold by deselecting that one timing assertion.

## Reviewer Focus Areas

- `.github/hooks/config/injection-patterns.json` — verify the two regex rules remain narrow, bounded by Feature 05 validation, and original to this clean-room implementation.
- `tests/hooks/injection_benchmark.py` — confirm all matching, normalization, decoding, and strongest-match behavior is delegated to `load_injection_rules` and `scan_output`.
- `tests/hooks/fixtures/injection/negative.json` — assess whether the legitimate neighbor prose is realistic enough to support the zero-high-false-positive claim without allowlisting.
- `tests/hooks/test_injection_corpus.py` — verify every production rule's configured block/warn response is exercised through the upstream PostToolUse entrypoint boundary.
