# Feature 06: Injection Pattern Corpus

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** `05-injection-scanner`
- **Key files modified:** `.github/hooks/config/injection-patterns.json` `[PROPOSED - name TBD]`, `tests/hooks/test_injection_corpus.py` `[PROPOSED - name TBD]`, `tests/hooks/injection_benchmark.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/positive.json` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/negative.json` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/markdown-smuggling.json` `[PROPOSED - name TBD]`, `docs/hooks/injection-benchmark.md` `[PROPOSED - name TBD]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Original clean-room corpus:** A production configuration is authored only from the Phase 02 taxonomy and discovery context, with no regex, code, pattern, or fixture copied from the surveyed repository; provenance is recorded for review.
2. **AC2 — Required categories:** The corpus covers instruction override, persona/role-play hijack, encoding/obfuscation, context manipulation, and instruction smuggling, including markdown link titles, image alt text, reference-style definitions, and HTML attributes.
3. **AC3 — Complete rule schema:** Every rule has a unique identifier, category, matcher, pattern, severity (`high`/`medium`/`low`), configured response action, priority, redacted reason, and recommended posture compatible with Feature 05's validated rule contract.
4. **AC4 — Per-rule positive evidence:** Every production rule has at least one positive fixture and every positive fixture identifies its expected rule, category, severity, response, and normalization variant where applicable.
5. **AC5 — Realistic negative evidence:** The negative corpus includes security documentation, this repository's own prompt/hook docs, code discussing prompts, markdown examples, ordinary authority/persona prose, and encoded non-imperative data without relying on the source-path allowlist to pass.
6. **AC6 — Measurable benchmark:** A deterministic benchmark calls Feature 05's rule-loading and output-scanning APIs `[PROPOSED - name TBD]`, reports total/per-category true positives, misses, false positives, and tier counts, and exits non-zero when expectations fail.
7. **AC7 — High-tier false-positive gate:** The full negative corpus produces zero `high`-tier false positives; each high rule also proves PostToolUse block/no-retry behavior, while each medium/low rule proves intact output plus warning context.
8. **AC8 — Obfuscation equivalence and performance:** Plain-text, homoglyph, zero-width, base64-imperative, hex-imperative, leetspeak, and markdown-smuggling variants resolve to the expected rule/category within the configured scan-size and Phase 01 latency-budget approach.

### Non-Goals

- No scanner/framework implementation is duplicated or modified; discovery deltas go back to Feature 05's contract.
- No semantic/LLM classifier, remote corpus service, telemetry upload, or automatic rule learning is added.
- No direct prompt injection or failed tool output is covered.
- No guarantee of perfect detection against determined attackers is claimed.
- No allowlist is used to hide a false positive in the benchmark negative corpus.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests / Evidence |
|---|---|---|
| AC1 | Production corpus config `[PROPOSED - name TBD]`; provenance section in benchmark doc | Code-review clean-room checklist and repository diff review |
| AC2 | Corpus rules and markdown-smuggling fixtures | Per-category exact inventory assertions and positive fixture replay |
| AC3 | Feature 05 rule loader `[PROPOSED - name TBD]`; production config | Schema validation, unique-id, allowed-enum, and response/severity assertions |
| AC4 | Positive fixture files `[PROPOSED - name TBD]` | Exact rule-to-fixture completeness test |
| AC5 | Negative fixture file `[PROPOSED - name TBD]` | Full negative replay without allowlist plus named content-class coverage |
| AC6 | Benchmark harness `[PROPOSED - name TBD]` | Deterministic summary/output and non-zero failure behavior tests |
| AC7 | Corpus plus Feature 05 entrypoint contract | Zero-high-FP gate and per-tier block/warn response replay |
| AC8 | Normalization and smuggling fixtures | Variant-equivalence and representative large-output timing checks |

### Phase Fidelity and Exceptions

- Key Deliverable 2 remains a separate feature but runs in Wave 2 because it requires Feature 05's scanner API.
- The Phase document's five minimum categories, clean-room constraint, per-rule fixtures, realistic negative corpus, count reporting, and zero-high-FP bar are preserved exactly.
- Response formatting remains owned by Feature 05; this feature supplies configured rule metadata and verifies the integration contract.
- No Phase requirement is deferred or renamed.

### Unverified Assumptions

- Feature 05's final public rule-loading and output-scanning symbol names are `[PROPOSED - name TBD]`; Stage 1 must resolve them before corpus implementation.
- The final number of rules is intentionally not fixed before false-positive tuning; completeness is category- and fixture-driven rather than count-driven.
- `tests/hooks/` is not currently a Python package, so Stage 1 must choose and test an exact repository-root, cwd-independent benchmark invocation/import strategy before the harness path is finalized.
- A benchmark documentation artifact is proposed for reproducible results, but the exact filename is `[PROPOSED - name TBD]`.

## B. Correctness & Edge Cases

### Key Workflows

- Validate the entire production corpus through Feature 05's loader before running any fixture.
- Replay every positive and negative fixture through the same production scan API used by the hook.
- Aggregate exact counts overall and per category/tier, fail on misses/unexpected matches, and preserve a reviewable result.
- Tune severity downward or tighten rules when legitimate negative content hits, never suppress failures via allowlisting.

### Failure Modes and Handling

- Duplicate identifiers, missing metadata, invalid regex, or unsupported actions fail the corpus load.
- One fixture matching multiple rules must declare the expected strongest rule; unexpected shadow matches are reported for tuning.
- Encoded fixtures remain bounded and synthetic; fixtures must not contain real credentials or executable payloads.
- A benchmark result cannot pass with skipped fixtures, empty categories, or an unreported high false positive.
- Legitimate discussion of prompt injection must remain readable even when it contains partial trigger language.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Keep rule policy in `.github/hooks/config/`, matching Phase 01's engine/config split and immutable config validation.
- Use JSON fixture inventories under `tests/hooks/fixtures/`, following existing Bash and recorded-payload corpora.
- Use pytest parameterization and explicit AC-oriented assertions consistent with current hook tests.

### Contracts and Decisions

- This feature calls Feature 05's reusable loader and scanner APIs `[PROPOSED - name TBD]`; it does not replicate normalization, matching, or response mapping.
- Severity and response are both explicit rule fields, allowing Phase-required mapping while keeping engine policy data-driven.
- The benchmark's machine-readable summary shape is `[PROPOSED - name TBD]`; human output must still show counts clearly.
- Negative fixtures run without source-path allowlisting so measured false positives reflect rule quality.

### Relationships to Sibling Plans

- Depends on `05-injection-scanner` AC3–AC4; Stage 1 confirms the final upstream API before authoring rules.
- Has no file overlap with its upstream feature, so it is parallel-safe within Wave 2 after the dependency completes.
- `07-multi-harness-integration` propagates the finished corpus and includes it in end-to-end block/warn smoke checks.

## D. Clean Design & Maintainability

### Simplest Design

- One production rule file, a small set of category-oriented fixture files, and one deterministic benchmark harness.
- Test exact inventory relationships so adding a rule without evidence fails immediately.
- Treat the benchmark as the tuning loop rather than adding separate ad hoc scripts.

### Complexity and Duplication Risks

- Many near-duplicate regexes can obscure intent; prefer the smallest category coverage that meets measured goals.
- Fixture labels can drift from production identifiers; validate exact bidirectional coverage.
- Benchmark-only parsing can diverge from runtime; call the public scanner APIs directly.

### Keep It Clean Checklist

- [ ] Every rule has positive evidence and reviewable metadata.
- [ ] Negative fixtures run without allowlist exemptions.
- [ ] No surveyed regex/code/fixture is copied.
- [ ] Benchmark and runtime call the same scanner APIs.
- [ ] High-tier rules remain narrow enough for zero negative-corpus false positives.

## E. Completeness: Observability, Security, Operability

### Observability Decision

The benchmark prints aggregate and per-category counts because measurement is a Phase requirement. It must not print full matched fixture bodies. The runtime gains no new normal-path logging from this feature.

### Security

- Fixtures contain only synthetic, non-secret, non-operational text.
- High responses never embed the triggering string; reasons use fixed, reviewed prose.
- Regexes are reviewed for pathological backtracking and exercised against representative large negatives.
- Corpus changes remain self-protected through the verified `self-hook-assets` rule.

### Runbook

- Run schema/inventory tests, positive replay, negative replay, benchmark, then the complete hook coverage gate.
- Record rule count, fixture count, misses, and false positives without fixture bodies.
- Roll back a problematic corpus revision as one config/fixture unit; do not disable the scanner to hide a rule regression.

## F. Test Plan

### Evidence Categories

- **Required new tests:** Corpus schema, category inventory, exact rule/fixture mapping, positive/negative replay, response mapping, and benchmark behavior.
- **Existing tests reused:** Feature 05 scanner normalization/entrypoint tests; no existing file is modified by this feature.
- **Runner-constrained tests:** Live warnings/blocks using selected harmless fixtures after propagation.
- **Code-review evidence:** Clean-room provenance, regex complexity, no real secrets, and no allowlist masking.
- **Manual QA:** Review benchmark counts and sample redacted reasons, then exercise one high and one warn fixture in a disposable session.

### Top Five High-Value Checks

1. Given the production corpus, when inventory validation runs, then all five required categories are non-empty and every rule maps to at least one positive fixture.
2. Given all positive fixtures, when scanned through the Feature 05 API, then each expected strongest rule/category/severity/response is reported with no misses.
3. Given the full realistic negative corpus without allowlisting, when benchmarked, then there are zero high-tier false positives and all other expected outcomes are reported.
4. Given obfuscated and markdown-native variants, when scanned, then each resolves to the same intended rule/category as its plain form.
5. Given an intentionally broken expectation, duplicate rule, or skipped category, when the benchmark runs, then it exits non-zero and reports counts without printing content.

### Test Data and Fixtures

- Positive synthetic cases for every rule and every required category.
- Paired plain/obfuscated cases for NFKC, homoglyph, zero-width, base64, hex, and leetspeak.
- Markdown link-title, alt-text, reference-definition, comment, and HTML-attribute cases.
- Realistic negative excerpts authored for this repository's domains without copying protected third-party text.
- Representative large clean and mixed outputs for performance measurement.

## Stage 1: Upstream Contract and Corpus Schema
**Goal**: Resolve Feature 05's final public APIs and validate the production rule schema and clean-room provenance process
**Success Criteria**: AC1 and AC3 pass schema, source-separation, and contract tests
**Status**: Not Started

## Stage 2: Category Corpus and Positive Fixtures
**Goal**: Author the original tiered rules and complete per-rule positive/variant evidence
**Success Criteria**: AC2, AC4, and the positive portions of AC7–AC8 pass exact inventory and replay tests
**Status**: Not Started

## Stage 3: Negative Corpus and Benchmark
**Goal**: Build realistic negative evidence and a deterministic count-reporting benchmark
**Success Criteria**: AC5–AC7 pass with zero high-tier false positives and non-zero failure behavior
**Status**: Not Started

## Stage 4: Tuning and Performance Verification
**Goal**: Tune rules against false positives, regex cost, and representative large outputs without weakening required coverage
**Success Criteria**: AC8 and the full corpus/hook coverage gates pass; benchmark evidence is recorded
**Status**: Not Started
