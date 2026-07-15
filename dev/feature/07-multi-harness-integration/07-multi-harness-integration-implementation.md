# Implementation Record: Multi-Harness Integration

## Summary

Integrated the finalized Phase 02 scanner, corpus, WebFetch/Bash guard, and
generated harness wiring into detached consumers. Claude high-tier results now
use `updatedToolOutput` for actual model-visible replacement, Codex
`tool_response` payloads are normalized without overstating unsupported tool
coverage, and the generated OpenCode plugin passes real block/warn mutation
evidence under Bun. Propagation now rejects symlinked intermediate hook
directories. The user explicitly accepted the Codex coverage limitation and
proceeding with unresolved PERF-01 in the phase-execute session on 2026-07-15.
Live harness QA is still not run, and the inherited fixed 50 ms latency gate
remains red.

## Sibling Features

- `05-injection-scanner` supplies `load_injection_rules`, `scan_output`, the
  PostToolUse entrypoint, allowlist, normalization, and redacted response model.
- `05-webfetch-exfiltration-guard` supplies the shared URL analyzer and
  WebFetch/curl/wget deny/ask/allow contract.
- `06-injection-pattern-corpus` supplies the finalized clean-room corpus,
  fixtures, and deterministic benchmark. No policy was copied into adapters.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Time-boxed contract investigation | Harness version/contract evidence | Record runner, date, payload, mutation/replacement semantics | Complete | `docs/hooks/prompt-injection-defense.md`, `docs/hooks/manual-qa.md` | `docs/hooks/prompt-injection-defense.md#current-harness-contract-evidence` | PENDING | PENDING |
| AC2 | Exhaustive harness outcome | Exact support matrix and sign-off state | Claude/OpenCode supported; Codex limitation has explicit session approval | Complete — limitation approved | `docs/hooks/installation.md`, `docs/hooks/manual-qa.md` | `docs/hooks/manual-qa.md#current-harness-evidence-and-sign-off` | PENDING | PENDING |
| AC3 | Equivalent enforcement where supported | Framework aliases, Claude replacement, Bun adapter smoke | Block replacement, warn preservation/context, redacted fail closed | Complete with Codex coverage limitation | `.github/hooks/lib/framework.py`, `.github/hooks/scripts/injection-scanner.py`, `scripts/propagate_master_assets.py` | `tests/hooks/test_hook_framework.py`, `tests/hooks/test_injection_scanner.py`, `tests/test_propagate_master_assets.py::PropagateMasterAssetsTests::test_phase02_opencode_adapter_replaces_blocked_output_and_appends_warning` | PENDING | PENDING |
| AC4 | Complete artifact propagation | Complete asset and stable marker test | Detached consumer contains scanner/corpus/allowlist/URL guard/wiring | Complete | `scripts/propagate_master_assets.py`, generated outputs | `tests/test_propagate_master_assets.py::PropagateMasterAssetsTests::test_phase02_generated_wiring_is_complete_and_idempotent` | PENDING | PENDING |
| AC5 | Generated wiring integrity | Preservation, cleanup, target, idempotence tests | Untagged entries survive; owned entries regenerate; second run byte-stable | Complete | `scripts/propagate_master_assets.py`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/injection-scanner.js` | `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC6 | Fresh consumer and self-protection | Detached invocation and expanded protected-path matrix | All Phase 02 policy/wiring paths deny Write; runtime needs no pip/source checkout | Complete | Propagated hook tree and wiring | `tests/hooks/test_hook_distribution_integration.py::test_ac9_every_propagated_policy_asset_is_self_protected`, `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC7 | Combined integration smoke | One propagated scanner/exfiltration flow | High block, warn, truncation, allowlist, WebFetch and curl/wget outcomes | Complete | `tests/hooks/test_hook_distribution_integration.py` | `tests/hooks/test_hook_distribution_integration.py::test_phase02_combined_propagated_scanner_and_exfiltration_smoke` | PENDING | PENDING |
| AC8 | Redaction, latency, retry evidence | Sentinel assertions, fixed latency gates, live checklist | Redaction passes; PERF-01 and live no-retry remain open | Partial — blocker retained | Runtime, integration tests, manual QA | `docs/hooks/manual-qa.md`, `tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms` | PENDING | PENDING |
| AC9 | Operations and honest support docs | Documentation assertions | Install/verify/recovery/rollback/limits/support classifications present | Complete with live reservations | `docs/hooks/installation.md`, `docs/hooks/hook-verification.md`, `docs/hooks/manual-qa.md`, `docs/hooks/prompt-injection-defense.md`, `tests/hooks/README.md` | `tests/hooks/test_hook_distribution_integration.py::test_phase02_support_and_operations_guide_is_honest_and_complete` | PENDING | PENDING |
| AC10 | Phase prerequisite gate | Nested symlink regression and fixed latency reproduction | SEC-01 passes; unresolved PERF-01 explicitly accepted without threshold change | Complete with accepted prerequisite risk | `scripts/propagate_master_assets.py`, propagation/integration tests | `tests/test_propagate_master_assets.py::PropagateMasterAssetsTests::test_hook_asset_copy_rejects_symlinked_intermediate_directory`, `docs/hooks/manual-qa.md` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Time-boxed contract investigation | Complete | Harness evidence docs | Versions: Claude 2.1.210, Codex 0.144.4, OpenCode 1.16.2, Bun 1.3.14; captured 2026-07-15. |
| AC2 | Exhaustive harness outcome | Complete — limitation approved | Support/sign-off docs | User approval in phase-execute session accepted the Codex 0.144.4 residual risk on 2026-07-15. |
| AC3 | Equivalent enforcement where supported | Complete with limitation | Framework, scanner, propagator | Claude and OpenCode automated parity pass. Codex supports Bash/apply_patch/MCP only. |
| AC4 | Complete artifact propagation | Complete | Propagator and generated files | Full runtime tree and command targets are verified detached. |
| AC5 | Generated wiring integrity | Complete | Propagator/generated wiring | Untagged ownership and byte idempotence pass. |
| AC6 | Fresh consumer and self-protection | Complete | Integration suite | New scanner/corpus/allowlist/plugin assets are protected. |
| AC7 | Combined integration smoke | Complete | Distribution integration test | All required scanner and URL guard outcomes pass in one consumer. |
| AC8 | Redaction, latency, and retry evidence | Partial | Tests/manual QA | Sentinels are absent; live retry QA is NOT RUN; fixed latency gate fails. |
| AC9 | Operations and honest support docs | Complete with reservations | Hook docs and README | Live rows remain explicitly NOT RUN; Cursor/Copilot remain Not supported. |
| AC10 | Phase prerequisite gate | Complete with accepted prerequisite risk | Propagation/integration evidence | SEC-01 passes. PERF-01 is still failed/open, and User approval in phase-execute session accepted proceeding on 2026-07-15. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/framework.py` | Modified | Added Codex output aliases/default truncation, runner-aware emission, and Claude replacement payload | Support current contracts without leaking blocked output |
| `.github/hooks/scripts/injection-scanner.py` | Modified | Builds shape-preserving redacted replacement values | Make high-tier suppression real for structured Claude outputs |
| `scripts/propagate_master_assets.py` | Modified | Generates the OpenCode translator and rejects symlinked nested destinations | Provide supported mutation and close SEC-01 propagation containment |
| `.claude/settings.json` | Regenerated/reconciled | Added source-owned scanner wiring and finalized guard matcher | Emit complete Claude configuration |
| `.codex/hooks.json` | Regenerated/reconciled | Added source-owned scanner wiring and finalized guard matcher | Emit supported Codex subset without claiming full parity |
| `.opencode/plugins/injection-scanner.js` | Generated | Forwards mutable output to shared scanner and applies block/warn result | Implement OpenCode adapter with no policy duplication |
| `.github/hooks/.distribution-version` | Regenerated | Updated full hook-tree digest | Version finalized Phase 02 assets |
| `docs/hooks/installation.md` | Modified | Phase 02 artifact and support matrix | Honest installation/support contract |
| `docs/hooks/hook-verification.md` | Modified | Added generated-target and multi-harness checks | Non-silent verification and live reservations |
| `docs/hooks/manual-qa.md` | Modified | Added evidence, versions, blockers, and sign-off template | Preserve automated/live distinction and explicit decision |
| `docs/hooks/prompt-injection-defense.md` | Created | Added enforcement, benchmark, limits, recovery, and support guide | Operational Phase 02 reference |
| `tests/hooks/README.md` | Modified | Replaced stale two-test wording | Current baseline guidance |
| `claude/learnings/cross-phase-decisions.md` | Reconciled pre-existing edit | Marks WebFetch Phase 02 ownership as addressed | Preserve authoritative upstream phase decision |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_hook_framework.py` | Modified | Codex alias, Claude replacement, native Codex emission tests | AC1, AC3, AC8 |
| `tests/hooks/test_injection_scanner.py` | Modified | Structured redacted replacement assertions | AC3, AC8 |
| `tests/test_propagate_master_assets.py` | Modified | Nested symlink, complete/idempotent output, live Bun adapter tests | AC3–AC6, AC10 |
| `tests/hooks/test_hook_distribution_integration.py` | Modified | Expanded self-protection, combined smoke, documentation assertions | AC6–AC9 |

## Test Results
- **Baseline**: 32 passed, 1 failed in 14.44s; sole failure was PERF-01 at approximately 383 ms median versus 50 ms.
- **Final**: 379 passed, 1 failed in 9.20s; sole failure remains PERF-01 (fresh median 117.16 ms; repeated runs ranged to about 383 ms). Focused functional gate: 171 passed, 1 latency test deselected. Coverage gate excluding both fixed timing assertions: 377 passed, 2 deselected, 71.34% coverage. Stdlib unittest discovery: 18 passed. Corpus benchmark: 19 true positives, 0 misses, 0 false positives, 0 high-tier false positives.
- **New tests added**: 10 test cases plus expanded matrices/assertions.
- **Regressions**: No functional regression. The inherited PERF-01 prerequisite remains red; coverage instrumentation also raised the scanner-only timing test to 59.66 ms, so timing assertions were excluded only from the passing coverage measurement and remain independently enforced.

## Deviations from Plan

- Current Claude documentation corrects the phase refinement assumption: a
  top-level PostToolUse block adds feedback but does not itself hide original
  output. `updatedToolOutput` was therefore added as the minimum integration
  correction.
- Codex now has stable hooks, but handler coverage is limited to
  Bash/apply_patch/MCP. This is a narrower and newer limitation than the plan's
  unverified-event assumption.
- OpenCode needed a real stdin/stdout translator rather than the generic
  command launcher. The generated adapter calls the shared Python entrypoint and
  contains no scanner policy.
- The legacy `phase-01-sha256:` prefix remains for compatibility; its digest
  covers the complete Phase 02 hook asset tree.

## Gaps

- Codex missing Read/Grep/WebFetch/WebSearch/Task PostToolUse coverage was
  explicitly accepted on 2026-07-15 by **User approval in phase-execute
  session**. This closes the decision requirement without changing Codex's
  Partial classification.
- Disposable live Claude block/warn/no-retry/Task/MCP/kill-switch QA is NOT RUN.
- Disposable live Codex and OpenCode behavior is NOT RUN. OpenCode has passing
  Bun adapter evidence; Codex has contract/source evidence for its subset.
- Phase 01 PERF-01 remains open: fixed 50 ms gate reproduced at 117–383 ms.
  **User approval in phase-execute session** accepted proceeding with this
  unresolved risk on 2026-07-15; the result remains failed.
- SEC-01 disposition: resolved for the planned intermediate hook destination
  case; symlinked `.github/hooks/config` is rejected before external mutation.

## Reviewer Focus Areas

- `.github/hooks/lib/framework.py` — confirm runner detection keeps Claude's
  `updatedToolOutput` out of Codex output while retaining redacted native block.
- `.github/hooks/scripts/injection-scanner.py` — review shape preservation and
  verify dynamic string values cannot survive a blocked structured output.
- `scripts/propagate_master_assets.py` — verify the Bun adapter forwards no
  policy and nested path validation precedes every copied/retired asset write.
- `docs/hooks/manual-qa.md` — verify both session approvals are recorded without
  promoting any live or latency result to pass.
