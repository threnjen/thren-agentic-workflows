# Feature 06: Injection Pattern Corpus — Context

## Key Files

### Files Changed by This Feature

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/config/injection-patterns.json` `[PROPOSED - name TBD]` | Production clean-room corpus with tier, category, matcher, response, priority, reason, and posture metadata validated by Feature 05 | Create after Feature 05 finalizes its rule schema |
| `tests/hooks/test_injection_corpus.py` `[PROPOSED - name TBD]` | Schema, category inventory, exact rule/fixture relationship, replay, response, false-positive, and performance coverage | Create |
| `tests/hooks/injection_benchmark.py` `[PROPOSED - name TBD]` | Deterministic positive/negative replay and count-reporting entrypoint that calls Feature 05's public APIs | Create; finalize its invocation/import strategy in Stage 1 |
| `tests/hooks/fixtures/injection/positive.json` `[PROPOSED - name TBD]` | At least one labeled positive case for every production rule, including expected strongest match metadata | Create |
| `tests/hooks/fixtures/injection/negative.json` `[PROPOSED - name TBD]` | Realistic legitimate content classes replayed without source-path allowlisting | Create |
| `tests/hooks/fixtures/injection/markdown-smuggling.json` `[PROPOSED - name TBD]` | Paired markdown-native smuggling cases for link titles, image alt text, reference definitions, comments, and HTML attributes | Create |
| `docs/hooks/injection-benchmark.md` `[PROPOSED - name TBD]` | Clean-room provenance, reproducible benchmark command, inventory/count results, tuning decisions, and known limits | Create |

### Upstream Files to Verify Before Editing

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/lib/injection_scanner.py` `[PROPOSED - name TBD]` | Feature 05's validated rule loader, normalization, matching, and structured result contract | Read-only upstream dependency; use final path/API from Feature 05's implementation record |
| `.github/hooks/lib/__init__.py` | Verified current hook-framework export surface; Feature 05 is expected to add its minimal scanner exports here | Read-only upstream dependency |
| `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]` | Feature 05's PostToolUse response boundary used for tier-response replay | Read-only upstream dependency |
| `.github/hooks/config/injection-allowlist.json` `[PROPOSED - name TBD]` | Feature 05's source-path allowlist; benchmark negatives must not depend on it | Read-only upstream dependency |
| `tests/hooks/test_injection_scanner.py` `[PROPOSED - name TBD]` | Feature 05 engine tests and synthetic-rule examples; production corpus tests must reuse rather than duplicate their engine concerns | Read-only upstream dependency |
| `tests/hooks/fixtures/injection/post-tool-use-payloads.json` `[PROPOSED - name TBD]` | Feature 05 payload corpus for entrypoint response verification | Read-only upstream dependency |

### Verified Existing References

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/lib/framework.py` | Existing `HookEvent`, `parse_payload`, `load_config`, `security_guard`, and decision-emission foundation | Read-only reference; Feature 05 owns any PostToolUse extension |
| `.github/hooks/config/file-access-rules.json` | Existing data-driven rule layout and verified `self-hook-assets` protection for `**/.github/hooks/**` | Read-only reference |
| `tests/hooks/conftest.py` | Existing session fixtures for the hook framework and recorded payloads | Read-only unless the implementer proves a shared corpus fixture is simpler than a feature-local loader; if modified, update scope records |
| `tests/hooks/README.md` | Exact virtual-environment, pytest, coverage, and stdlib regression commands | Read-only reference |
| `tests/hooks/fixtures/bash/commands.json` | Existing fixture inventory convention using explicit criterion, vector, expected outcome, and status fields | Read-only reference |
| `tests/hooks/test_hook_framework.py` | Existing payload/config/failure/redaction and performance patterns | Read-only regression reference |
| `tests/hooks/test_file_access_guard.py` | Existing data-driven schema, exact inventory, redaction, and self-protection test patterns | Read-only regression reference |
| `dev/feature/05-injection-scanner/05-injection-scanner-plan.md` | Upstream AC3–AC4 rule validation and reusable scanner API commitment | Read-only prerequisite plan |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Authoritative scope, taxonomy, response tiers, benchmark requirement, and phase success criteria | Read-only source of requirements |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Approved clean-room taxonomy and weaknesses-to-beat; not a source of production regexes | Read-only source of requirements |
| `docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md` | Last recorded complete-suite and coverage evidence plus runner-constrained status | Read-only verification reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| None of the seven proposed Feature 06 files exists yet, and Feature 05's proposed scanner module, entrypoint, allowlist, tests, and public APIs also do not exist at expansion time. | The corpus cannot safely assume a final JSON container shape, loader signature, scan-result type, tie-breaker, or import path from plan text alone. | **Warning:** Stage 1 must wait for Feature 05, read its implementation record and public exports, and replace proposed paths/symbols with the finalized contract before authoring production rules. |
| The verified existing policy config stores rules as an object keyed by rule identifier with fields such as `id`, `action`, `reason`, `matcher`, `pattern`, and `priority`; Feature 05 is responsible for the additional injection fields and may choose a different validated container shape. | Copying the Phase 01 JSON layout mechanically could conflict with the finalized scanner loader. | Treat the current config only as an architecture convention for data-driven policy. Feature 05's implemented validator is authoritative for the production corpus schema. |
| `tests/hooks/` has no `__init__.py`; the proposed `tests/hooks/injection_benchmark.py` is therefore not automatically a package-importable module. | A benchmark that works only under one cwd or only when loaded by pytest would not be a reproducible standalone gate. | **Warning:** Stage 1 must select and document a cwd-independent or repository-root invocation/import strategy, then test that exact command. The filename remains `[PROPOSED - name TBD]` until selected. |
| The active Python 3.12.6 environment and repository `.venv` do not have pytest installed, so the current hook pytest/coverage baseline could not be rerun during expansion. The stdlib suite does run and currently passes 14 tests; the graph and source scan identify 101 hook test functions. | Expansion can verify the harness and historical evidence but cannot claim a fresh 101-test hook pass. | Use the setup and commands in `tests/hooks/README.md` before implementation verification. Preserve the recorded Phase 01 evidence of 252 pytest passes and coverage above 50% as historical, not fresh, evidence. |
| Existing tests already establish exact-inventory, redaction, self-protection, data-driven configuration, and median-budget patterns, but there is no injection fixture loader or benchmark summary convention. | New test scenarios must follow repository style without presenting invented method names or output fields as established facts. | Describe scenarios rather than predeclaring test method names; finalize the fixture and machine-readable summary shapes in Stage 1 and record them in the benchmark documentation. |
| No `tests/phase*` or other phase-scoped consolidated test directory exists; Phase 01 uses feature-oriented modules under `tests/hooks/`. | A new Phase 02 consolidated file would add a second organization pattern and overlap the final integration feature. | Keep corpus verification in the proposed feature-specific module. Leave cross-feature propagated/runtime smoke coverage to `07-multi-harness-integration`. |

## Architectural Decisions

- Feature 05's validated rule loader and output scanner are the only runtime interpretation path. The benchmark must call them directly and must not implement a second normalizer, regex engine, severity mapper, or result selector.
- Author the corpus from the five Phase 02 categories and documented weaknesses only. Do not inspect or copy the surveyed repository's pattern or fixture source; provenance is a reviewable deliverable.
- Keep one production rule file and the smallest fixture set that proves exact coverage. Split markdown-native cases only because they require several channel-specific paired examples and benefit from focused review.
- Make rule-to-positive-fixture coverage bidirectional: every production rule has positive evidence, and every positive fixture references an existing production rule.
- Preserve both `severity` and configured response action as explicit rule data. Tests verify the mapping, while runtime policy remains owned by configuration rather than benchmark code.
- Evaluate negative fixtures without allowlisting. Allowlisting protects legitimate repository paths in live use; it cannot be used to improve measured rule quality.
- Resolve multiple matches through Feature 05's finalized deterministic strongest-match behavior. Fixtures may identify the expected strongest rule, but the corpus must not recreate selection logic.
- Emit human and machine-readable benchmark counts without fixture bodies. Counts include overall/per-category true positives, misses, false positives, and tier totals; any exact field names remain `[PROPOSED - name TBD]` until Stage 1.
- Prefer tightening a matcher or lowering a severity over adding overlapping exceptions. High tier is reserved for patterns that maintain zero false positives across the full negative corpus.
- Add no runtime normal-path logging. The benchmark's count output exists because measurement is a Phase requirement and remains free of matched content.

## Constraints

- Feature 06 begins only after `05-injection-scanner` AC3–AC4 are implemented and green; its finalized public API and schema override every proposed name in this bundle.
- Runtime corpus processing remains Python-standard-library-only through Feature 05; pytest and coverage remain development-only dependencies.
- Every production rule requires a unique identifier, category, matcher, pattern, severity, response action, priority, redacted reason, recommended posture, and at least one positive fixture.
- All five required categories must remain non-empty: instruction override, persona/role-play hijack, encoding/obfuscation, context manipulation, and instruction smuggling.
- Positive fixtures are synthetic and harmless. They contain no real credentials, active endpoints, executable payloads, or copied third-party content.
- Negative fixtures must cover security docs, repository prompt/hook docs, code discussing prompts, markdown examples, ordinary authority/persona prose, and encoded non-imperative data without allowlist exemptions.
- Plain, homoglyph, zero-width, base64-imperative, hex-imperative, leetspeak, and markdown-smuggling variants must resolve to the intended upstream rule/category within configured scan bounds.
- The benchmark fails on schema errors, duplicate identifiers, empty required categories, missing fixture coverage, skipped fixtures, positive misses, unexpected matches, or any high-tier negative false positive.
- High-tier response evidence must prove full block/no-retry behavior; medium/low evidence must prove intact raw output plus redacted warning context.
- Regex and decoding work must remain bounded. Representative large clean and mixed outputs are required for timing and pathological-backtracking checks.
- Production reasons, warnings, benchmark output, and retained evidence must never reproduce the matched prompt-shaped text or full fixture body.

## Scope Boundaries

- Do not implement or modify scanner normalization, rule loading, matching, allowlisting, response formatting, failure posture, or hook wiring; return any missing reusable contract to Feature 05.
- Do not add WebFetch or Bash URL exfiltration policy; `05-webfetch-exfiltration-guard` owns it.
- Do not implement Codex/OpenCode adapters, propagation, installation changes, or final live multi-harness evidence; `07-multi-harness-integration` owns them.
- Do not scan direct user prompts, failed tool calls, or add semantic/LLM classification.
- Do not claim perfect detection or use the allowlist to mask benchmark failures.
- Do not modify `docs/inspiration/` or open surveyed pattern/fixture source as an implementation input.
- Do not add a phase-wide consolidated test file unless implementation discovery proves cross-feature behavior cannot be owned by Feature 07.

## Relationships to Sibling Plans

- `05-injection-scanner` is the runtime prerequisite. It must deliver the validated rule schema plus reusable loader and scanner APIs required by AC3, AC4, and AC6.
- `05-webfetch-exfiltration-guard` is file-disjoint and runtime-independent from this corpus; no exfiltration URL signatures belong in this feature.
- `07-multi-harness-integration` consumes the completed corpus and benchmark evidence, propagates the production config, and owns combined block/warn smoke checks and live harness evidence.
- This feature has no planned file overlap with Feature 05 and remains parallel-safe in Wave 2 after the upstream runtime dependency is complete. If implementation discovery requires editing an upstream scanner or shared fixture file, stop and update the dependency/scope record before proceeding.

## Suggested Implementation Order

1. Confirm Feature 05 is complete and green; record the exact loader, scan API, result metadata, schema, tie-breaker, and entrypoint response contracts.
2. Finalize the production config, fixture inventory, benchmark summary, and standalone invocation shapes; establish clean-room provenance.
3. Author the smallest complete category corpus and bidirectionally complete positive/variant fixtures.
4. Build the realistic negative corpus and deterministic benchmark, then enforce count and failure gates.
5. Tune rules against false positives and performance, run all regression gates, publish redacted results, and hand the corpus to Feature 07.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 stdlib hook runtime + JSON configuration and fixtures + pytest/pytest-cov development tooling |
| Test Runner | `.venv/bin/python -m pytest tests/` after setup documented in `tests/hooks/README.md` |
| Feature Coverage Gate | `.venv/bin/python -m pytest tests/hooks/ --cov=.github/hooks/lib --cov-report=term-missing --cov-fail-under=50` |
| Stdlib Regression | `python3 -m unittest discover -s tests -v` |
| Test Baseline | Fresh stdlib run: 14 passed, 0 failed — captured 2026-07-14. Fresh pytest run unavailable because pytest is not installed in the active environment. Last recorded Phase 01 evidence: 252 pytest passes and 64.07% combined coverage. |
| Existing Hook Tests | 101 test functions identified under `tests/hooks/`; not freshly executed during expansion |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None directly applicable. The entries in `.github/learnings/` concern evaluation identity, agent/document propagation, shell-path serialization, Terraform, hook failure boundaries, path matching, and cross-phase WebFetch ownership. The WebFetch decision is already isolated in sibling `05-webfetch-exfiltration-guard`; no learning changes this corpus feature's clean-room, measurement, or file-scope decisions.
