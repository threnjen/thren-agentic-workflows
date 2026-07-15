# Implementation Record: Injection Scanner

## Summary

Implemented the Phase 02 PostToolUse scanner foundation with backward-compatible framework parsing/emission, bounded normalization and encoded-candidate scanning, validated data-driven rules, deterministic redacted match metadata, conservative source allowlisting, a cwd-independent entrypoint, hook registration, and fixture-driven coverage. The finalized downstream API is `load_injection_rules(config)` plus `scan_output(output, rules, limits=...)` from `lib.injection_scanner` or the lazy public `lib` package exports.

## Sibling Features

- `05-webfetch-exfiltration-guard` ran in the same parallel wave with a disjoint source/test scope; none of its URL analyzer or file-access files were modified here.
- `06-injection-pattern-corpus` consumes the finalized rule schema, `load_injection_rules`, `scan_output`, and `ScanResult`/`MatchMetadata` contracts. It owns `.github/hooks/config/injection-patterns.json` and production rule content.
- `07-multi-harness-integration` owns propagation, Claude/Codex/OpenCode wiring, and live runner evidence for the finalized entrypoint and hook definition.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | PostToolUse framework contract | Framework PostToolUse payload cases | Raw/structured output, truncation, agent metadata, invalid fields, preserved PreToolUse aliases | Complete | `.github/hooks/lib/framework.py`, `.github/hooks/lib/__init__.py` | `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC2 | Deterministic normalization | Scanner normalization variants | NFKC, homoglyph, zero-width, base64, hex, cap limits, raw preservation | Complete | `.github/hooks/lib/injection_scanner.py` | `tests/hooks/test_injection_scanner.py::test_ac2_normalization_variants_resolve_to_same_rule_without_mutation` | PENDING | PENDING |
| AC3 | Data-driven rule contract | Scanner rule-schema cases | Valid immutable rules, configured action independent of severity, invalid/unsafe/ambiguous rules | Complete | `.github/hooks/lib/injection_scanner.py` | `tests/hooks/test_injection_scanner.py::test_ac3_rule_schema_is_data_driven_and_immutable` | PENDING | PENDING |
| AC4 | Reusable scanner API | Public package contract and redacted metadata cases | Lazy public exports, narrow loader/scanner signatures, metadata excludes matched content | Complete | `.github/hooks/lib/__init__.py`, `.github/hooks/lib/injection_scanner.py` | `tests/hooks/test_hook_framework.py::test_framework_package_exposes_only_documented_public_contract`, `tests/hooks/test_injection_scanner.py::test_ac8_strongest_match_and_tie_break_are_deterministic` | PENDING | PENDING |
| AC5 | High-tier suppression | Synthetic configured block case | `decision: block`, output absent, source/category/rule reason, no-retry/manual-inspection guidance | Complete | `.github/hooks/lib/framework.py`, `.github/hooks/scripts/injection-scanner.py` | `tests/hooks/test_injection_scanner.py::test_ac5_high_block_is_redacted_and_instructs_no_retry` | PENDING | PENDING |
| AC6 | Warn-and-continue | Synthetic medium/low warning cases | Raw logical output unchanged, only redacted `additionalContext` appended | Complete | `.github/hooks/lib/framework.py`, `.github/hooks/scripts/injection-scanner.py` | `tests/hooks/test_injection_scanner.py::test_ac6_warn_preserves_output_and_emits_redacted_context` | PENDING | PENDING |
| AC7 | Protected allowlist | Repository containment and self-protection cases | Existing paths only, traversal/outside/missing/symlink rejection, approved-root validation, `self-hook-assets` denial | Complete | `.github/hooks/lib/injection_scanner.py`, `.github/hooks/config/injection-allowlist.json` | `tests/hooks/test_injection_scanner.py::test_ac7_allowlist_requires_existing_repo_owned_source`, `tests/hooks/test_injection_scanner.py::test_ac7_self_hook_assets_protect_new_scanner_configuration` | PENDING | PENDING |
| AC8 | Output boundaries | Boundary and strongest-match cases | Empty, bytes/non-UTF8, structured output, scan cap, truncation, encoded caps, deterministic multi-match | Complete | `.github/hooks/lib/injection_scanner.py`, `.github/hooks/scripts/injection-scanner.py` | `tests/hooks/test_injection_scanner.py::test_ac8_empty_binary_structured_and_scan_cap_boundaries`, `tests/hooks/fixtures/injection/post-tool-use-payloads.json` | PENDING | PENDING |
| AC9 | Security failure posture | Framework/entrypoint failure cases | Payload/config/processing/emission failure blocks redacted; project override allows recovery | Complete | `.github/hooks/lib/framework.py`, `.github/hooks/scripts/injection-scanner.py` | `tests/hooks/test_hook_framework.py::test_post_tool_security_guard_fails_closed_without_reflecting_failure`, `tests/hooks/test_injection_scanner.py::test_ac9_entrypoint_failure_and_project_override_postures` | PENDING | PENDING |
| AC10 | Tool coverage and regression | Recorded tool payload and regression suites | Built-ins, Task/subagent, MCP, structured/malformed/binary/truncated payloads; PreToolUse regression | Complete with external prerequisite reservation | `.github/hooks/injection-scanner.json`, `.github/hooks/scripts/injection-scanner.py` | `tests/hooks/test_injection_scanner.py::test_ac10_recorded_payloads_cover_supported_tools_and_entrypoint`, full pytest/unittest results below | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | PostToolUse framework contract | Complete | `.github/hooks/lib/framework.py`, `.github/hooks/lib/__init__.py` | Existing PreToolUse result shape and behavior remain green. |
| AC2 | Deterministic normalization | Complete | `.github/hooks/lib/injection_scanner.py` | Scan copies are bounded; raw strings, bytes, and structures are never rewritten. |
| AC3 | Data-driven rule contract | Complete | `.github/hooks/lib/injection_scanner.py` | Final schema uses `rules` keyed by ID with explicit severity and `response_action`. |
| AC4 | Reusable scanner API | Complete | `.github/hooks/lib/injection_scanner.py`, `.github/hooks/lib/__init__.py` | Final API names replace the plan's proposed placeholders. |
| AC5 | High-tier suppression | Complete | `.github/hooks/scripts/injection-scanner.py`, `.github/hooks/lib/framework.py` | Response action, not severity, selects suppression. |
| AC6 | Warn-and-continue | Complete | `.github/hooks/scripts/injection-scanner.py`, `.github/hooks/lib/framework.py` | Warn output contains only validated identifiers and posture text. |
| AC7 | Protected allowlist | Complete | `.github/hooks/lib/injection_scanner.py`, `.github/hooks/config/injection-allowlist.json` | Symlinked roots are rejected even when they resolve elsewhere inside the repo. |
| AC8 | Output boundaries | Complete | `.github/hooks/lib/injection_scanner.py`, `.github/hooks/scripts/injection-scanner.py` | Blank or missing rendered frames are not applicable; this phase has no UI. |
| AC9 | Security failure posture | Complete | `.github/hooks/lib/framework.py`, `.github/hooks/scripts/injection-scanner.py` | Failures emit exactly one redacted block or exit-code-2 fallback. |
| AC10 | Tool coverage and regression | Complete with external prerequisite reservation | `.github/hooks/injection-scanner.json`, tests/fixtures | Feature tests pass; full suite retains the manifest's Phase 01 propagated latency failure. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/framework.py` | Modified | Added PostToolUse fields, result validation/emission, and fail-closed guard | Extend the shared framework without changing PreToolUse decisions |
| `.github/hooks/lib/__init__.py` | Modified | Added PostToolUse exports and lazy scanner API exports | Give Feature 06 a narrow public API without increasing PreToolUse startup cost |
| `.github/hooks/lib/injection_scanner.py` | Created | Added rule validation, normalization, bounded decoding/matching, metadata, and allowlisting | Provide the reusable scanner engine free of production pattern policy |
| `.github/hooks/scripts/injection-scanner.py` | Created | Added the cwd-independent PostToolUse adapter and redacted response mapping | Wire framework events to the scanner and project-only override posture |
| `.github/hooks/injection-scanner.json` | Created | Registered successful built-in, Task, and MCP PostToolUse coverage | Define Claude hook matcher coverage without PostToolUseFailure |
| `.github/hooks/config/injection-allowlist.json` | Created | Declared approved sources and scan/decoding caps | Keep bypass and resource limits protected and configuration-driven |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_hook_framework.py` | Modified | Added PostToolUse parsing, emission, validation, failure, fallback, and public-contract tests | AC1, AC5, AC6, AC9, AC10 |
| `tests/hooks/test_injection_scanner.py` | Created | Added scanner engine, entrypoint, allowlist, boundary, redaction, performance, and registration tests | AC2–AC10 |
| `tests/hooks/fixtures/injection/post-tool-use-payloads.json` | Created | Added secret-free built-in, MCP, Task, structured, truncated, empty, binary-shaped, and malformed payloads | AC8, AC10 |

## Test Results
- **Baseline**: 50 passed, 0 failed in `tests/hooks/test_hook_framework.py` before implementation; scanner artifacts were absent and the new scanner suite produced the expected red state (32 setup errors and 3 file-contract failures).
- **Final**: 98 passed, 0 failed for framework + scanner tests; 318 passed, 1 deselected with 89.27% hook-library coverage when excluding the already-manifested Phase 01 propagated latency prerequisite; 14 passed, 0 failed in stdlib unittest discovery. The exact complete pytest command produced 332 passed, 1 failed: `test_ac9_propagated_guard_median_latency_is_below_50_ms` (observed median approximately 107–117 ms against 50 ms).
- **New tests added**: 48 collected framework/scanner test cases beyond the 50-test framework baseline.
- **Regressions**: No scanner or PreToolUse functional regression. The single complete-suite failure is the pre-recorded Phase 01 SEC-01/PERF-01 integration prerequisite assigned to Feature 07 in the execution manifest.

## Deviations from Plan

- Finalized proposed names as `.github/hooks/lib/injection_scanner.py`, `.github/hooks/scripts/injection-scanner.py`, `.github/hooks/injection-scanner.json`, `.github/hooks/config/injection-allowlist.json`, `tests/hooks/test_injection_scanner.py`, and `tests/hooks/fixtures/injection/post-tool-use-payloads.json`.
- Finalized the Feature 06 API as `load_injection_rules` and `scan_output`; rule results use immutable `ScanResult` and `MatchMetadata` values.
- Scanner exports are lazy from `lib.__init__` so existing PreToolUse consumers do not import scanner machinery on startup.
- No production `injection-patterns.json` was created because Feature 06 explicitly owns production rule content.

## Gaps

- Disposable live Claude Code block/warn/no-retry/Task/truncation checks were **NOT RUN** in this implementation environment; Feature 07 owns live multi-harness integration evidence.
- The exact complete pytest and exact coverage commands remain red only on the execution manifest's pre-existing propagated-guard latency prerequisite. Coverage was verified above threshold by deselecting that single timing assertion, with all other hook tests passing.

## Reviewer Focus Areas

- `.github/hooks/lib/injection_scanner.py` — review regex safety restrictions, one-pass encoded-candidate bounds, and deterministic action/severity/priority/ID ordering.
- `.github/hooks/lib/injection_scanner.py` — verify lexical-plus-resolved allowlist checks reject traversal and both in-repo/out-of-repo symlink broadening.
- `.github/hooks/lib/framework.py` — confirm the new `HookEvent` defaults preserve all existing three-field consumers and PostToolUse emission exactly matches the verified runner contract.
- `.github/hooks/scripts/injection-scanner.py` — verify block/warn/notice strings cannot include raw output or matched content and project-only override handling remains fail closed.
- Phase 01 propagated-guard latency failure — confirm it remains tracked for Feature 07 rather than being attributed to the scanner feature.
