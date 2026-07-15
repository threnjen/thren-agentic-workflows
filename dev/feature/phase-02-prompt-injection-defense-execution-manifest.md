# Phase 02 Prompt-Injection Defense Execution Manifest

- **Phase document:** `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`
- **Discovery context:** `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md`
- **Branch decomposed:** `phase/prompt-injection-defense`
- **Prepared:** 2026-07-14

**Ordering note:** The Phase document lists the pattern corpus before the WebFetch exfiltration guard. Execution schedules `05-webfetch-exfiltration-guard` in Wave 1 with `05-injection-scanner`, ahead of Wave 2 `06-injection-pattern-corpus`, because WebFetch depends only on the Phase 01 guard and its conservative file scope is disjoint from the scanner. The corpus has a runtime dependency on the scanner's validated rule-loading and output-scanning APIs. No requirement moved between feature owners.

## Ordered Feature Task Names

1. `05-injection-scanner`
2. `05-webfetch-exfiltration-guard`
3. `06-injection-pattern-corpus`
4. `07-multi-harness-integration`

## Feature Execution Metadata

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---:|---|---|---|---|
| `05-injection-scanner` | 1 | yes | none | `.github/hooks/lib/framework.py`, `.github/hooks/lib/__init__.py`, `.github/hooks/lib/injection_scanner.py` `[PROPOSED - name TBD]`, `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]`, `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]`, `.github/hooks/config/injection-allowlist.json` `[PROPOSED - name TBD]`, `tests/hooks/test_hook_framework.py`, `tests/hooks/test_injection_scanner.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/post-tool-use-payloads.json` `[PROPOSED - name TBD]` | n/a |
| `05-webfetch-exfiltration-guard` | 1 | yes | none | `.github/hooks/lib/url_exfiltration.py` `[PROPOSED - name TBD]`, `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/config/file-access-rules.json`, `.github/hooks/file-access-guard.json`, `tests/hooks/test_bash_command_analyzer.py`, `tests/hooks/test_file_access_guard.py`, `tests/hooks/fixtures/bash/commands.json`, `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` `[PROPOSED - name TBD]`, `docs/hooks/bash-command-limitations.md` | n/a |
| `06-injection-pattern-corpus` | 2 | yes | `05-injection-scanner` | `.github/hooks/config/injection-patterns.json` `[PROPOSED - name TBD]`, `tests/hooks/test_injection_corpus.py` `[PROPOSED - name TBD]`, `tests/hooks/injection_benchmark.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/positive.json` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/negative.json` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/markdown-smuggling.json` `[PROPOSED - name TBD]`, `docs/hooks/injection-benchmark.md` `[PROPOSED - name TBD]` | n/a |
| `07-multi-harness-integration` | 3 | no | `05-injection-scanner`, `05-webfetch-exfiltration-guard`, `06-injection-pattern-corpus` | `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, `tests/hooks/test_hook_distribution_integration.py`, `tests/hooks/README.md` `(verify)`, `.github/hooks/.distribution-version`, `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]` `(verify)`, `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]` `(verify)`, `.github/hooks/config/file-access-rules.json` `(verify)`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/injection-scanner.js` `[PROPOSED - name TBD]`, `.opencode/plugins/file-access-guard.js` `(verify)`, harness adapter files `[PROPOSED - name TBD]`, `docs/hooks/installation.md`, `docs/hooks/manual-qa.md`, `docs/hooks/hook-verification.md`, `docs/hooks/prompt-injection-defense.md` `[PROPOSED - name TBD]` | shares `.github/hooks/injection-scanner.json` and `.github/hooks/scripts/injection-scanner.py` with upstream `05-injection-scanner`, and may share `.github/hooks/config/file-access-rules.json` with upstream `05-webfetch-exfiltration-guard` |

## Dependency Graph

- `06-injection-pattern-corpus` depends_on `05-injection-scanner` because the corpus and benchmark must call the scanner's validated rule-loading and output-scanning APIs rather than duplicate normalization or matching.
- `07-multi-harness-integration` depends_on `05-injection-scanner` because propagation and harness adapters require the finalized PostToolUse entrypoint, response contract, allowlist, and reusable scanner APIs; it also has a conservative shared-file dependency on scanner wiring/entrypoint files.
- `07-multi-harness-integration` depends_on `05-webfetch-exfiltration-guard` because the propagated smoke must exercise finalized WebFetch and Bash URL deny/ask/allow behavior; it may share the existing rule configuration after integration discovery.
- `07-multi-harness-integration` depends_on `06-injection-pattern-corpus` because propagation and smoke verification require the finalized production corpus, benchmark evidence, and selected harmless high/warn fixtures.
- `05-injection-scanner` and `05-webfetch-exfiltration-guard` have no runtime or shared-file dependency after the WebFetch analyzer was explicitly kept module-local; their Wave 1 file scopes are disjoint.

## Wave-by-Wave Execution Schedule

### Wave 1 — parallel

Run concurrently:

1. `05-injection-scanner`
2. `05-webfetch-exfiltration-guard`

Both features are `parallel_safe: yes`, have no dependencies, and have disjoint conservative source/test/documentation scopes.

### Wave 2 — parallel

Run after all Wave 1 prerequisites complete:

1. `06-injection-pattern-corpus`

This feature is `parallel_safe: yes` because it consumes the scanner through a finalized public API and shares no file with its upstream feature. Its standalone benchmark invocation/import strategy must be resolved before the harness filename is finalized.

### Wave 3 — sequential

Run after Waves 1–2 complete:

1. `07-multi-harness-integration`

This feature is `parallel_safe: no` because conservative integration discovery may modify scanner wiring/entrypoint files and the shared file-access rule configuration. It is the required final integration/bootstrap task and must not begin adapter/propagation work until upstream implementation records finalize all proposed paths and APIs.

## Expected Bundle Files

| Feature Directory | Plan | Context | Tasks |
|---|---|---|---|
| `dev/feature/05-injection-scanner/` | `05-injection-scanner-plan.md` | `05-injection-scanner-context.md` | `05-injection-scanner-tasks.md` |
| `dev/feature/05-webfetch-exfiltration-guard/` | `05-webfetch-exfiltration-guard-plan.md` | `05-webfetch-exfiltration-guard-context.md` | `05-webfetch-exfiltration-guard-tasks.md` |
| `dev/feature/06-injection-pattern-corpus/` | `06-injection-pattern-corpus-plan.md` | `06-injection-pattern-corpus-context.md` | `06-injection-pattern-corpus-tasks.md` |
| `dev/feature/07-multi-harness-integration/` | `07-multi-harness-integration-plan.md` | `07-multi-harness-integration-context.md` | `07-multi-harness-integration-tasks.md` |

## Execution Preconditions and Evidence Boundaries

- Fresh expansion evidence: `python3 -m unittest discover -s tests -v` passes 14 tests. One expander also recorded 252 pytest passes and 63.56% total coverage through an isolated `uv run --with-requirements requirements-dev.txt` run.
- The repository `.venv` and active Python do not currently provide pytest. Implementers must install only `requirements-dev.txt` into the documented isolated environment and rerun the exact `.venv` pytest/coverage commands before claiming fresh implementation evidence.
- No Stage 0 bootstrap is required: 101 hook test functions exist, the fresh stdlib baseline passes, and recorded pytest coverage exceeds the 50% prerequisite threshold.
- Phase 01 SEC-01 nested-destination containment and PERF-01 latency evidence is contradictory. Feature 07 must reproduce/review intermediate-directory symlink containment and fixed latency stability, then record reviewed Phase 01 resolution or explicit prerequisite risk acceptance.
- Codex/OpenCode event-name mappings and command launchers are not evidence of pre-context output suppression. Feature 07 must complete the parity-or-evidenced-limitation gate and obtain explicit user sign-off for every limitation.

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/hooks/test_injection_scanner.py` `[PROPOSED - name TBD]` | `05-injection-scanner` | PostToolUse parsing/emission, normalization, synthetic rule schema, block/warn behavior, allowlist boundaries, truncation, failure posture, and performance |
| `tests/hooks/test_injection_corpus.py` `[PROPOSED - name TBD]` | `06-injection-pattern-corpus` | Exact category/rule/fixture inventory, positive/negative replay, tier response, zero-high-false-positive, and variant-equivalence coverage |
| `tests/hooks/injection_benchmark.py` `[PROPOSED - name TBD]` | `06-injection-pattern-corpus` | Deterministic production-API benchmark with redacted total/per-category counts and non-zero failure behavior |

### New Fixture and Benchmark Assets

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/hooks/fixtures/injection/post-tool-use-payloads.json` `[PROPOSED - name TBD]` | `05-injection-scanner` | Built-in, MCP, Task/subagent, structured, malformed, binary, and truncated PostToolUse payload evidence |
| `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` `[PROPOSED - name TBD]` | `05-webfetch-exfiltration-guard` | Fixture-verified WebFetch URL input and synthetic deny/ask/allow/malformed cases |
| `tests/hooks/fixtures/injection/positive.json`, `negative.json`, `markdown-smuggling.json` `[PROPOSED - names TBD]` | `06-injection-pattern-corpus` | Per-rule positives, realistic negatives, and required normalization/markdown-smuggling variants |
| `docs/hooks/injection-benchmark.md` `[PROPOSED - name TBD]` | `06-injection-pattern-corpus`, `07-multi-harness-integration` | Clean-room provenance, exact invocation, redacted result counts, tuning decisions, and handoff evidence |

### Existing Test Files Updated By Multiple Features

None identified. Wave 1 deliberately uses disjoint tests: scanner work updates `tests/hooks/test_hook_framework.py`, while WebFetch work updates `tests/hooks/test_bash_command_analyzer.py` and `tests/hooks/test_file_access_guard.py`. The final integration feature alone updates propagation and consolidated integration tests.

### Existing Consolidated Integration Test

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/hooks/test_hook_distribution_integration.py` | `07-multi-harness-integration` consuming all upstream features | Established phase-level hook integration asset; extend for propagated scanner/corpus/allowlist plus WebFetch/Bash combined smoke, redaction, latency, and support evidence instead of creating a new `tests/phase02/` convention |

### Manual QA Checklist

- [ ] In a disposable Claude Code session, verify a real high-tier match suppresses output and shows the redacted no-retry/manual-inspection reason.
- [ ] Verify a real medium/low match preserves output and appends one informative warning without amplifying matched content.
- [ ] Observe whether the agent avoids retrying the same blocked call; record runner version, date, command, and redacted outcome.
- [ ] Verify truncated-output notice, allowlisted repository-owned sources, and non-allowlisted/missing source behavior.
- [ ] With reserved `.invalid` URLs and synthetic sentinels, verify WebFetch known-secret deny, ambiguous-entropy ask, and ordinary URL allow outcomes.
- [ ] Verify Bash `curl`/`wget` URL behavior matches direct WebFetch classification while existing protected-file/destructive rules remain intact.
- [ ] Confirm prompt, URL, command, and secret sentinels are absent from stdout, stderr, structured decisions, warnings, audit files, generated outputs, and retained evidence.
- [ ] Exercise the human-only kill switch outside the guarded session, restore protection, and complete rollback/re-propagation.
- [ ] For Codex and OpenCode, record equivalent live enforcement where supported or evidence-backed platform limitation plus explicit user sign-off; do not infer parity from generated event names.
- [ ] Verify generated Claude/Codex/OpenCode files preserve unrelated user/tool-owned entries and remove only source-owned stale entries.
- [ ] Verify intermediate runtime/config/settings/plugin directory symlinks cannot redirect propagation outside the target root, and record the Phase 01 SEC-01/PERF-01 prerequisite disposition.
