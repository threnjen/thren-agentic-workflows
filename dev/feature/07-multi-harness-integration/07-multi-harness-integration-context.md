# Feature 07: Multi-Harness Integration — Context

## Key Files

### Files to Create or Modify

| File | Role | Change Type |
|------|------|-------------|
| `scripts/propagate_master_assets.py` | Verified propagation entrypoint, recursive hook-asset copying, event translation, generated-settings merge, generated-plugin rendering, source ownership, and distribution hashing | Modify |
| `tests/test_propagate_master_assets.py` | Verified `unittest` propagation suite covering temporary consumers, asset completeness, ownership cleanup, detached execution, source/output-root containment, global setup, and final-file symlink replacement | Modify |
| `tests/hooks/test_hook_distribution_integration.py` | Verified propagated-consumer smoke, self-protection, redaction, latency, and support-document assertions; extend as the Phase 02 consolidated integration asset | Modify |
| `tests/hooks/README.md` | Exact environment setup and verification commands; verify and correct the stale two-test baseline wording if it is no longer historical-only | Modify (verify) |
| `.github/hooks/.distribution-version` | Verified generated marker currently using `phase-01-sha256:`; must represent the complete finalized Phase 02 runtime bundle | Regenerate through propagation |
| `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]` | Upstream scanner source wiring consumed by propagation and harness translation | Verify final upstream path; modify only if investigation proves a narrow source-metadata correction is required |
| `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]` | Upstream scanner entrypoint invoked by supported harness wiring | Verify final upstream path; modify only for a documented integration correction |
| `.github/hooks/config/file-access-rules.json` | Verified WebFetch/Bash policy location and broad `**/.github/hooks/**` self-protection source | Verify; modify only if upstream integration metadata is incomplete |
| `.claude/settings.json` | Generated Claude wiring; preserve unrelated untagged PostToolUse and SessionStart entries while replacing source-owned entries | Regenerate through propagation |
| `.codex/hooks.json` | Generated Codex wiring; current generic event mapping is not proof of pre-context suppression | Regenerate only to the supported/evidenced contract |
| `.opencode/plugins/injection-scanner.js` `[PROPOSED - name TBD]` | Potential generated OpenCode scanner adapter if contract investigation proves equivalent or explicitly classified partial behavior | Create through propagation only when supported by evidence |
| `.opencode/plugins/file-access-guard.js` | Verified generated OpenCode PreToolUse launcher; may need a thin native result translation based on contract evidence | Verify and regenerate; exact change depends on Stage 1 |
| Harness adapter files `[PROPOSED - name TBD]` | Payload/response shape translators for capable non-Claude harnesses | Create only where current contract evidence requires them |
| `docs/hooks/installation.md` | Verified Phase 01 support matrix, installation, upgrade, recovery, rollback, and Bash-boundary guide | Modify |
| `docs/hooks/manual-qa.md` | Verified separation between automated evidence and live checks | Modify |
| `docs/hooks/hook-verification.md` | Existing verification guide for generated hooks and runner behavior | Modify |
| `docs/hooks/prompt-injection-defense.md` `[PROPOSED - name TBD]` | Phase 02 scanner behavior, support, limitations, and operations guide | Create if this remains the smallest coherent documentation structure |

### Upstream Phase 02 Assets to Verify Before Editing

| File or Contract | Owner | Integration Use |
|------------------|-------|-----------------|
| Final scanner module and public loader/scanner API `[PROPOSED - name TBD]` | `05-injection-scanner` | Harness adapters translate payload/response shapes and call shared scanning behavior; they must not reimplement policy |
| Final scanner entrypoint and PostToolUse response contract `[PROPOSED - name TBD]` | `05-injection-scanner` | Claude source wiring and supported-harness behavioral parity |
| Final injection allowlist `[PROPOSED - name TBD]` | `05-injection-scanner` | Complete propagation, self-protection, and allowlist smoke behavior |
| Final production pattern corpus and benchmark evidence `[PROPOSED - name TBD]` | `06-injection-pattern-corpus` | Complete propagation plus harmless high/warn smoke fixtures |
| Final shared URL classifier and WebFetch/Bash entrypoint contract `[PROPOSED - name TBD]` | `05-webfetch-exfiltration-guard` | Propagated deny/ask/allow behavior for WebFetch, curl, and wget |
| Final URL and Bash fixture paths `[PROPOSED - name TBD]` | `05-webfetch-exfiltration-guard` | Select synthetic integration smoke cases without duplicating policy |

### Verified Existing References

| File or Symbol | Role |
|----------------|------|
| `scripts/propagate_master_assets.py::propagate_hooks_once` | Verified target/source-root propagation seam returning changed-artifact counts |
| `scripts/propagate_master_assets.py::_update_nested_settings_file` | Verified source-owned generated-entry replacement with untagged-entry preservation |
| `scripts/propagate_master_assets.py::_render_opencode_plugin` | Verified generated OpenCode launcher renderer |
| `scripts/propagate_master_assets.py::HOOK_EVENT_MAP` | Verified generic `PostToolUse` mapping for Claude/Codex and `tool.execute.after` for OpenCode; event names alone do not establish output interception semantics |
| `.github/hooks/file-access-guard.json` | Verified current PreToolUse source definition and matcher contract |
| `.github/hooks/config/file-access-rules.json` | Verified current data-driven policy and self-protection coverage for `.github/hooks/**` |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Authoritative integration, propagation, parity-or-limitation, smoke, and live-QA requirements |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Verified Claude PostToolUse facts and explicit Codex/OpenCode investigation boundary |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Authoritative Phase 01 dependency status; currently records SEC-01 and PERF-01 as release blockers |
| `docs/phases/PHASE_01/PHASE_01-qa-analysis.md` | Reproduction and remediation requirements for SEC-01/PERF-01 |
| `docs/phases/PHASE_01/PHASE_01-security-scan.md` | Security finding and release-blocking containment evidence |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| The scanner source definition, scanner entrypoint, corpus, allowlist, proposed scanner adapter, and any harness-specific adapter files do not exist at expansion time. The three upstream Phase 02 features are planning bundles, not implemented dependencies. | Feature 07 cannot safely lock filenames, imports, result types, or adapter call signatures now. | **Warning:** Begin implementation only after all three upstream features are implemented/reviewed. Read their implementation records and replace proposed paths/contracts with the finalized artifacts before touching propagation. |
| The generic propagation map already names Codex `PostToolUse` and OpenCode `tool.execute.after`, and `.codex/hooks.json` currently resembles Claude wiring. No checked-in evidence proves either event runs before model ingestion or honors suppression/rewrite results. | Treating generated event presence as parity would violate AC1–AC3 and could create a false security claim. | Preserve Stage 1 as a hard investigation gate. Record runner version, date, primary documentation, safe experiment, timing, response semantics, and one of the exact Phase-approved outcomes for each harness before adapter implementation. |
| The current OpenCode plugin renderer only awaits the scanner/guard command and does not translate a structured hook decision into a native blocking or output-replacement result. The existing installation guide already classifies OpenCode as Partial for Phase 01. | A generated OpenCode plugin can look operational while providing no equivalent enforcement. | **Warning:** If current OpenCode APIs cannot suppress/replace/annotate pre-context output, publish an evidence-backed limitation and obtain explicit user sign-off; do not simulate parity with a launcher-only adapter. |
| Phase 01 evidence is internally inconsistent: `PHASE_01_QA.md` reports containment and latency as passing, while the later Phase 01 summary, QA analysis, and security scan mark SEC-01 nested-destination containment and PERF-01 latency stability as release-blocking. Current propagation tests cover an output-root symlink and a final-file symlink, but not symlinked intermediate runtime/generated directories. | Feature 07 must not build a release-safe propagation claim on stale positive evidence. | **Warning:** AC10 is an implementation prerequisite. Reproduce or review the Phase 01 remediation status before propagation changes. Resolve it in the Phase 01 owning scope or record explicit prerequisite risk acceptance; do not silently fix or waive it inside Phase 02. |
| The active Python 3.12.6 environment and repository `.venv` cannot import pytest. A fresh stdlib regression run passes 14 tests; the last retained Phase 01 evidence reports 252 pytest passes and 64.07% combined coverage. | Current pytest/coverage health cannot be claimed from this expansion session, although historical coverage exceeds the 50% prerequisite threshold. | Install only the documented development dependencies before implementation verification. Record fresh focused, full-suite, and coverage results; keep historical and fresh evidence clearly separated. No Stage 0 bootstrap is required. |
| `.claude/settings.json` and `.codex/hooks.json` contain unrelated untagged PostToolUse/SessionStart entries, while existing generated entries use `$source`; OpenCode ownership uses a generated-file header. | Phase 02 regeneration could delete user or tooling configuration if cleanup broadens. | Extend the existing ownership mechanisms and add preservation/stale-cleanup/idempotence tests before regenerating checked-in outputs. |
| The repository has no `tests/phase*` convention. Existing cross-feature hook coverage is consolidated in `tests/hooks/test_hook_distribution_integration.py`. | Creating a separate Phase 02 test directory would duplicate the established integration harness. | Extend the verified distribution integration module for AC6–AC8, while keeping feature-local engine/corpus/URL tests in their upstream modules. |
| `tests/hooks/README.md` still describes a two-test stdlib baseline, but a fresh run collects and passes 14 tests. | Implementers may misread the historical sentence as the current count. | Treat the command as authoritative and record the fresh count in implementation evidence. Update the README only if documentation review confirms the stale count is in this feature's approved documentation scope. |

## Architectural Decisions

- Treat harness investigation as a behavioral contract gate, not a documentation-only task. Equivalent event naming is insufficient; evidence must prove when output enters model context and how block/warn responses are consumed.
- Use the completed scanner entrypoint/config and WebFetch guard entrypoint as the source contracts. Add a harness adapter only for payload/response shape translation and call the finalized upstream loader, normalizer, validator, scanner, and URL classifier APIs where the harness contract permits it.
- Do not duplicate injection patterns, URL signatures, severity mapping, strongest-match selection, normalization, validation, redaction, or failure policy in generated JavaScript or harness-specific wrappers.
- Keep `.github/hooks/` as the source of truth. Generate `.claude/settings.json`, `.codex/hooks.json`, and `.opencode/plugins/` through the verified propagation pipeline; do not hand-maintain separate policy in generated outputs.
- Preserve untagged settings entries and user-owned plugins. Remove only entries carrying propagation's `$source` ownership and files carrying the exact generated OpenCode header.
- Propagate the finalized Phase 02 hook tree as one self-contained standard-library runtime. Every generated command must resolve inside a detached consumer, and the marker must change when any runtime/config/adapter input changes while remaining stable for unchanged inputs.
- Reuse `tests/hooks/test_hook_distribution_integration.py` for the phase-level propagated smoke. The smoke uses selected harmless upstream fixtures and asserts behavior; it does not become a second corpus or URL-rule test suite.
- Give each harness exactly one support state: equivalent enforcement with passing evidence, or an evidence-backed limitation with explicit user sign-off. A partial launcher, inferred support, or unresolved investigation is not completion.
- Add no normal-path runtime logging. Investigation and QA evidence may retain versions, commands, timestamps, rule/category identifiers, decisions, counts, and timings only; never retain output bodies, matched text, URLs, commands, secret sentinels, or warning-shaped attacker content.

## Constraints

- This feature is Wave 3 and runs only after `05-injection-scanner`, `05-webfetch-exfiltration-guard`, and `06-injection-pattern-corpus` are implemented, reviewed, and green.
- Runtime Python remains standard-library-only, deterministic, cwd-independent, and usable in a fresh consumer without pip, the source repository, symlinks, or a virtual environment.
- Preserve the Phase document's successful-output tool coverage, strongest-match selection, high suppression, medium/low warning, truncation notice, fail-closed posture, allowlist, redaction, and no-retry behavior wherever a harness can provide equivalent interception.
- Safe harness experiments use disposable repositories, synthetic sentinels, and reserved hosts. Do not expose real credentials, user prompts, source contents, or external endpoints.
- Explicit user sign-off is a retained decision artifact; it cannot be inferred from automated tests, documentation edits, or silence.
- Cursor and GitHub Copilot remain Not supported. No adapter, extension, or plugin work for them belongs here.
- `PostToolUseFailure`, direct prompt injection, semantic/LLM detection, Phase 03 backup/edit-time behavior, and plugin packaging remain out of scope.
- Any still-open SEC-01 or PERF-01 issue remains Phase 01-owned. Feature 07 may consume a reviewed remediation or documented prerequisite risk acceptance, but must not obscure ownership.
- Manual/live evidence stays labeled `NOT RUN` until actually observed in the corresponding runner.

## Scope Boundaries

- Do not alter upstream scanner, corpus, or URL policy merely to simplify propagation. Return a missing reusable API or integration defect to the owning feature and sequence it explicitly.
- Do not treat Codex/OpenCode configuration generation as proof of enforcement.
- Do not hand-edit generated platform files as independent sources of truth.
- Do not retain full tool output, matches, URLs, command bodies, prompts, secrets, or raw runner payloads in tests, docs, warnings, or audit artifacts.
- Do not broaden installation support claims beyond the recorded behavioral evidence.
- Do not perform live recovery, global-install replacement, or limitation sign-off in the developer's active checkout/session; use disposable or human-controlled environments.

## Relationships to Sibling Plans

- `05-injection-scanner` supplies the finalized PostToolUse entrypoint, response contract, protected allowlist, and reusable scanning/validation API. Feature 07 propagates and translates that behavior but does not own scanner policy.
- `05-webfetch-exfiltration-guard` supplies the shared URL classifier plus WebFetch and Bash curl/wget deny/ask/allow behavior. Feature 07 propagates it and verifies cross-feature smoke behavior.
- `06-injection-pattern-corpus` supplies the finalized production corpus, benchmark command/evidence, and selected harmless high/warn fixtures for smoke use.
- Feature 07 owns harness investigation, thin supported adapters, generated wiring, complete propagation, detached-consumer/self-protection checks, combined smoke evidence, support documentation, live QA records, and explicit limitation sign-off.
- This feature may share scanner source/config or file-access rule files with upstream features after contract discovery, so it is sequential and `parallel_safe: no` even though implementation begins in a later wave.

## Suggested Implementation Order

1. Confirm all upstream Phase 02 features are implemented/reviewed; resolve their actual files, public APIs, selected smoke fixtures, and benchmark evidence.
2. Audit SEC-01/PERF-01 status and record the Phase 01 prerequisite disposition before changing propagation or claiming release safety.
3. Time-box Codex/OpenCode contract research and safe experiments; assign each harness its exact supported or limitation-plus-sign-off path.
4. Add only the necessary payload/response translators and source metadata for capable harnesses, with no duplicated policy.
5. Extend propagation and generated-output tests for complete assets, command resolution, ownership preservation, cleanup, idempotence, versioning, and detached consumers.
6. Extend the propagated integration suite for scanner/corpus/WebFetch/Bash behavior, self-protection, redaction, timing, and no-retry evidence.
7. Regenerate checked-in outputs, perform disposable live checks, update operations/support documentation, capture explicit limitation sign-off, and verify rollback.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 standard-library hook runtime and propagation tooling; JSON source/settings/config; generated JavaScript OpenCode plugins; POSIX shell setup/verification |
| Test Runner | After setup: `.venv/bin/python -m pytest tests/`; focused integration: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py tests/hooks/test_hook_distribution_integration.py`; stdlib regression: `python3 -m unittest discover -s tests -v` |
| Coverage | `.venv/bin/python -m pytest tests/ --cov=.github/hooks/lib --cov=.github/hooks/scripts --cov=scripts --cov-report=term-missing --cov-fail-under=50` |
| Test Baseline | Fresh pytest/coverage NOT RUN: both active Python and `.venv` lack pytest. Fresh stdlib regression: 14 passed, 0 failed in 0.424s. Last retained Phase 01 evidence: 252 pytest passes and 64.07% combined coverage. Captured 2026-07-14. |
| Lint | Not configured |
| Format | Not configured |
| Branch | `phase/prompt-injection-defense` at expansion revision `53b74bd` |

## Relevant Learnings

- `.github/learnings/review-learnings.md`: propagators must validate resolved source assets and every resolved destination directory against declared roots; replacing a symlinked leaf is insufficient because an intermediate parent can redirect writes. This directly governs AC4, AC6, and the SEC-01 prerequisite gate.
- `.github/learnings/review-learnings.md`: externally emitted public decision values must be revalidated at security-sensitive boundaries. Thin adapters must validate translated upstream results before returning them to a harness.
- `.github/learnings/review-learnings.md`: documentation verification blocks for future-facing paths must emit useful readiness/failure output rather than using silent bare existence tests. Apply this to installation and verification guidance for proposed adapters/assets.
- `.github/learnings/cross-phase-decisions.md`: WebFetch exfiltration was explicitly moved into Phase 02 and is satisfied by the upstream guard plus this feature's propagated smoke; plugin packaging remains deferred and must not be pulled into installation work.
- `.github/learnings/debugging-learnings.md`: mismatched or stale generated harness files/symlinks can fail silently. Generated wiring verification must check both the expected filename/ownership marker and the command target after propagation.
- `.github/learnings/project-learnings.md` concerns retained evaluation runtime identity and does not change this feature's integration contract.
