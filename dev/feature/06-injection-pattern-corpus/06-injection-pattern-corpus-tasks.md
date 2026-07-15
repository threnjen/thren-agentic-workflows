# Feature 06: Injection Pattern Corpus — Tasks

## Stage 1: Upstream Contract and Corpus Schema

- [ ] Confirm `05-injection-scanner` is implemented, reviewed, and green before corpus implementation begins; read its implementation record and record the finalized public rule-loader, output-scanner, structured-result, response-emission, and tie-breaker contracts. (AC3, AC6, AC7)
- [ ] Replace every plan-time proposed upstream path or symbol with Feature 05's authoritative implementation name; if Feature 05 did not expose a reusable loader/scanner API, return that missing contract upstream instead of duplicating runtime logic. (AC3, AC6)
- [ ] Finalize the production corpus container and rule schema against Feature 05's validator, including unique identifier, category, matcher, pattern, severity, configured response action, priority, redacted reason, and recommended posture. (AC3)
- [ ] Choose and document the exact production config, corpus-test, fixture, benchmark, and benchmark-document paths; retain `[PROPOSED - name TBD]` markers until the implementation makes each choice. (AC1, AC3, AC6)
- [ ] Define clean-room provenance using only the taxonomy and weaknesses in the Phase 02 summary/discovery context; explicitly prohibit copying regexes, code, or fixtures from the surveyed repository. (AC1)
- [ ] Define positive and negative fixture schemas that carry stable labels and expected metadata without real credentials, executable payloads, full matched-body output, or external network dependencies. (AC4, AC5)
- [ ] Define the benchmark's human-readable counts and machine-readable summary shape `[PROPOSED - name TBD]` for overall/per-category true positives, misses, false positives, and tier totals. (AC6)
- [ ] Select a reproducible benchmark invocation/import strategy that works from the repository checkout even though `tests/hooks/` is not currently a Python package; test and document the exact command. (AC6)
- [ ] Add schema/inventory failure scenarios for malformed JSON, duplicate identifiers, invalid matchers or regexes, unsupported severity/action/posture values, missing metadata, empty required categories, and an empty corpus. (AC2, AC3, AC6)
- [ ] Verify corpus loading fails before fixture replay on any invalid rule and that error evidence is redacted rather than reflecting pattern or fixture content. (AC3, AC6)

## Stage 2: Category Corpus and Positive Fixtures

- [ ] Create the production corpus with the smallest reviewable set of original rules that keeps all five required categories non-empty: instruction override, persona/role-play hijack, encoding/obfuscation, context manipulation, and instruction smuggling. (AC1, AC2)
- [ ] Give every rule a stable unique identifier and complete validated metadata, with severity and response action both explicit in configuration rather than inferred by benchmark or engine code. (AC3)
- [ ] Cover fake system delimiters and attempts to replace, ignore, or discard governing instructions without turning ordinary security discussion into a high-tier match. (AC2, AC5)
- [ ] Cover persona/restriction-bypass and fabricated authority/prior-conversation forms with severities narrow enough for realistic legitimate prose. (AC2, AC5)
- [ ] Cover fake system-role fragments and system-prompt extraction/context-manipulation forms using original matchers and fixed redacted reasons. (AC2, AC3)
- [ ] Cover instruction smuggling through HTML/code comments plus markdown link titles, image alt text, reference-style link definitions, and HTML attributes. (AC2)
- [ ] Create at least one synthetic positive fixture for every production rule; each fixture must identify the expected strongest rule, category, severity, response, and normalization variant where applicable. (AC4)
- [ ] Create paired plain/obfuscated evidence for NFKC, homoglyph, zero-width, base64-imperative, hex-imperative, and leetspeak handling, with bounded synthetic encoded values. (AC4, AC8)
- [ ] Create focused markdown-smuggling fixtures for every required markdown-native channel and verify each resolves to the intended rule/category through Feature 05's scanner API. (AC2, AC4, AC8)
- [ ] Add exact bidirectional inventory assertions so a production rule without a positive fixture and a fixture naming a missing production rule both fail. (AC4)
- [ ] Replay all positives through Feature 05's public loader and scanner rather than benchmark-local matching or normalization. (AC3, AC4, AC6)
- [ ] Add response-integration scenarios proving each high rule produces suppression plus a structured no-retry/manual-inspection reason and each medium/low rule preserves raw logical output plus redacted warning context. (AC7)
- [ ] Add multi-match fixtures that declare the expected strongest rule and report unexpected shadow matches while relying on Feature 05's finalized deterministic selection contract. (AC3, AC4, AC7)

## Stage 3: Negative Corpus and Benchmark

- [ ] Create realistic negative fixtures for security documentation, this repository's prompt/hook documentation, code discussing prompts, markdown examples, ordinary authority/persona prose, and encoded non-imperative data. (AC5)
- [ ] Run every negative fixture with source-path allowlisting disabled or bypassed at the test seam, and fail if a result depends on the allowlist to appear clean. (AC5, AC7)
- [ ] Ensure the negative corpus includes legitimate partial trigger language and category-neighbor prose so false-positive tuning measures matcher quality rather than only obviously unrelated text. (AC5)
- [ ] Implement the deterministic benchmark as a thin caller of Feature 05's production rule loader and output scanner; do not duplicate normalization, regex compilation, response mapping, or strongest-match selection. (AC6)
- [ ] Report total and per-category true positives, misses, false positives, and tier counts in the finalized human/machine summary without printing fixture bodies or matched spans. (AC6)
- [ ] Make the benchmark exit non-zero for positive misses, unexpected rule/category/severity/response results, negative false positives that violate expectations, missing/skipped fixtures, empty categories, schema failures, or count mismatches. (AC6, AC7)
- [ ] Enforce zero high-tier false positives across the complete negative corpus as a hard pass/fail gate. (AC7)
- [ ] Verify medium/low negative outcomes are counted and surfaced for tuning even when the Phase's hard zero bar applies specifically to high tier. (AC6, AC7)
- [ ] Add an intentionally broken expectation scenario proving the benchmark returns non-zero and still reports redacted counts. (AC6)
- [ ] Write the benchmark documentation with clean-room provenance, exact invocation, rule/fixture/category counts, result interpretation, redaction guarantees, failure behavior, and the distinction between automated, runner-constrained, review, and manual evidence. (AC1, AC6, AC7)

## Stage 4: Tuning and Performance Verification

- [ ] Tune any legitimate hit by narrowing the matcher or lowering its severity; never suppress a benchmark false positive through the source-path allowlist. (AC5, AC7)
- [ ] Review every regex for pathological backtracking and exercise representative large clean and mixed outputs within Feature 05's configured scan-size and decode bounds. (AC8)
- [ ] Measure and record corpus scan timing using the Phase 01 latency-budget approach and Feature 05's finalized scanner workload target; keep the existing framework performance regression green. (AC8)
- [ ] Replay plain, homoglyph, zero-width, base64-imperative, hex-imperative, leetspeak, and markdown-smuggling variants after tuning and confirm each retains its intended strongest rule/category. (AC8)
- [ ] Re-run exact schema, category, bidirectional fixture inventory, positive replay, negative replay, tier-response, benchmark-failure, and large-output checks after every production corpus change. (AC1–AC8)
- [ ] Run `.venv/bin/python -m pytest tests/` and require all repository tests green after installing only the documented development dependencies. (AC1–AC8)
- [ ] Run `.venv/bin/python -m pytest tests/hooks/ --cov=.github/hooks/lib --cov-report=term-missing --cov-fail-under=50` and retain evidence that the repository's existing coverage threshold remains satisfied. (AC1–AC8)
- [ ] Run `python3 -m unittest discover -s tests -v` and preserve the current 14-test stdlib compatibility baseline. (AC1–AC8)
- [ ] Perform code-review evidence checks for clean-room authorship, smallest sufficient rule set, complete metadata/evidence, bounded regex/decoding cost, no real secrets, no copied survey content, no allowlist masking, and no fixture-body logging. (AC1–AC8)
- [ ] Hand the finalized corpus paths, exact benchmark command, redacted count evidence, and selected harmless high/warn fixtures to `07-multi-harness-integration` for propagation and end-to-end smoke verification. (AC6, AC7, AC8)
- [ ] After Feature 07 propagation is available, record or explicitly mark `NOT RUN` the runner-constrained checks for one harmless high block and one medium/low warning; do not claim live evidence from automated scanner replay. (AC7)
