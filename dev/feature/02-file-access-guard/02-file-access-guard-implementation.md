# Implementation Record: File-Access Guard

## Summary

Implemented a standard-library, data-driven file-access guard using Feature
01's payload, configuration, decision, security, kill-switch, and redacted
recording contracts. The feature adds normalized reusable path evaluation,
tiered rules and project overrides, five file-tool adapters, explicit Grep
scope handling, hook self-protection, structured safe guidance, and a
source-of-truth hook definition without changing generated wiring.

## Sibling Features

- `01-hook-framework` supplies `.github/hooks/lib/framework.py`; this feature
  consumes it without changing its public export contract.
- `03-bash-command-analyzer` can import `normalize_path`, `load_rules`, and
  `evaluate_path` from `.github/hooks/lib/file_access.py` and extend the shared
  hook definition/configuration without duplicating tier logic.
- `04-hook-distribution-integration` owns generated Claude/Codex/OpenCode
  wiring, legacy retirement, double-fire checks, and real consuming-project
  bypass verification.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Tiered rule configuration | `test_ac1_default_rules_have_data_driven_tier_schema`; `test_ac1_invalid_rule_configuration_is_rejected` | Validate stable IDs, tiers, reasons, patterns, priority, bypass escalation, and fail-closed schema errors | Complete | `.github/hooks/lib/file_access.py`; `.github/hooks/config/file-access-rules.json` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC2 | Environment-file behavior | `test_ac2_all_file_tools_deny_environment_variants`; `test_ac2_exact_environment_templates_are_allowed` | Five file tools, three environment variants, two exact templates, and non-broadened template prefix | Complete | `.github/hooks/scripts/file-access-guard.py`; `.github/hooks/config/file-access-rules.json` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC3 | Credential behavior | `test_ac3_credential_names_patterns_and_directories_are_denied`; `test_ac3_unrelated_id_prefix_is_allowed` | Key extensions, exact SSH names, credential names, four protected directories, and `id_generator.py` | Complete | `.github/hooks/config/file-access-rules.json` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC4 | Protected project files | `test_ac4_lock_files_use_configured_ask_tier`; `test_ac4_production_configuration_is_denied`; `test_ac4_project_override_can_add_user_rule_with_its_action_and_reason` | Lock ask tier, production deny, and merged user rule action/reason | Complete | `.github/hooks/lib/file_access.py`; `.github/hooks/config/file-access-rules.json`; `.github/hooks/config/file-access-overrides.json` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC5 | Normalized matching | `test_ac5_traversal_and_symlink_are_resolved_before_matching`; `test_ac5_broken_symlink_resolves_conservatively`; `test_ac5_tilde_expands_against_supplied_home`; `test_ac5_case_folding_is_controlled_by_filesystem_mode` | Traversal, real/broken symlink, tilde, and controlled filesystem case behavior | Complete | `.github/hooks/lib/file_access.py` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC6 | Grep coverage | `test_ac6_grep_protected_path_or_glob_is_denied`; `test_ac6_malformed_guarded_grep_input_fails_closed`; `test_ac6_glob_tool_remains_outside_file_matcher` | Protected `path`/`glob`, ordinary/no scope, malformed input, and Glob exclusion | Complete | `.github/hooks/scripts/file-access-guard.py`; `.github/hooks/file-access-guard.json` | `tests/hooks/fixtures/file_access/recorded_payloads.json`; `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC7 | Hook self-protection | `test_ac7_consuming_project_hook_assets_are_self_protected`; `test_ac7_symlink_alias_to_wiring_file_is_denied` | Scripts, config, override, Claude/Codex/OpenCode wiring, normalized alias, and symlink | Complete | `.github/hooks/config/file-access-rules.json` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC8 | Structured guidance | `test_ac8_blocked_or_held_guidance_is_structured_and_actionable`; `test_ac8_decision_and_log_never_reflect_file_content_or_full_payload` | Rule/path/reason/alternative guidance and secret-sentinel output/log redaction | Complete | `.github/hooks/scripts/file-access-guard.py` | `tests/hooks/test_file_access_guard.py`; `docs/hooks/file-access-guard.md` | PENDING | PENDING |
| AC9 | Failure and recovery | `test_ac9_induced_evaluator_exception_becomes_redacted_guard_error`; `test_ac9_only_protected_override_can_disable_guard`; `test_ac9_bypass_mode_escalates_configured_ask_to_deny` | Induced exception, environment ineffectiveness, protected override kill switch, and bypass escalation | Complete | `.github/hooks/scripts/file-access-guard.py`; `.github/hooks/config/file-access-overrides.json` | `tests/hooks/test_file_access_guard.py`; `docs/hooks/file-access-guard.md` | PENDING | PENDING |
| AC10 | Reusable guard contract | `test_ac10_reusable_evaluator_contract_is_narrow_and_complete`; `test_ac10_reusable_contract_imports_without_cwd_or_pythonpath`; `test_ac10_runtime_imports_are_stdlib_only_without_subprocess` | Narrow result contract, isolated import, and runtime dependency audit | Complete | `.github/hooks/lib/file_access.py` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Keep complete tiered policy in validated data configuration. | Complete | `.github/hooks/lib/file_access.py`; `.github/hooks/config/file-access-rules.json` | Python contains no concrete protected filenames. |
| AC2 | Deny environment variants across five tools while allowing exact templates. | Complete | `.github/hooks/scripts/file-access-guard.py`; rule config | Exact allow rules have higher priority. |
| AC3 | Deny credential patterns/names/directories without `id_*` false positives. | Complete | Rule config | Private SSH names are exact rules. |
| AC4 | Apply configured lock, production, user, and override policy. | Complete | Evaluator; default/override config | Framework recursive merge supplies project precedence. |
| AC5 | Normalize home, traversal, symlinks, and filesystem case behavior. | Complete | `.github/hooks/lib/file_access.py` | Controlled case mode keeps tests portable. |
| AC6 | Guard recorded Grep scopes and fail malformed input closed; omit Glob. | Complete | Guard script; hook definition | Explicit fields are `path` and `glob`. |
| AC7 | Self-protect source and generated hook assets in consuming roots. | Complete | Rule config | Generated wiring remains unchanged until Feature 04. |
| AC8 | Provide actionable structured decisions and redacted logs. | Complete | Guard script | Only allowlisted metadata is recorded. |
| AC9 | Fail closed and restrict recovery to the protected override. | Complete | Guard script; override config | Live runner premise check remains Feature 04 evidence. |
| AC10 | Expose one reusable normalization and tier contract. | Complete | `.github/hooks/lib/file_access.py` | Does not emit framework decisions itself. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/file_access.py` | Create | Validated rules, path normalization, matching, precedence, reusable result | Shared path/tier contract for Features 02 and 03 |
| `.github/hooks/scripts/file-access-guard.py` | Create | File/Grep payload adapters, framework handler, guidance, redacted match recording | Security-hook runtime entrypoint |
| `.github/hooks/config/file-access-rules.json` | Create | Environment, credential, project, and self-protection rules | Keep concrete policy out of Python |
| `.github/hooks/config/file-access-overrides.json` | Create | Empty protected project override layer | Human-managed rules and kill switch |
| `.github/hooks/file-access-guard.json` | Create | Source PreToolUse matcher and command | Distribution source for Feature 04 |
| `docs/hooks/file-access-guard.md` | Create | Policy, contract, boundaries, verification, recovery, rollback | Operability and handoff |
| `dev/feature/02-file-access-guard/02-file-access-guard-tasks.md` | Modify | Mark completed automated implementation work | Plan execution status |
| `dev/feature/02-file-access-guard/02-file-access-guard-implementation.md` | Create | Traceability and evidence | Reviewer handoff |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_file_access_guard.py` | Create | 83 collected file guard scenarios | AC1–AC10 |
| `tests/hooks/fixtures/file_access/recorded_payloads.json` | Create | File-tool and explicit Grep scope payload corpus | AC2, AC6 |

## Test Results
- **Baseline**: 52 passed, 0 failed
- **Final**: 135 passed, 0 failed; 83 feature tests at 72.55% combined hook runtime coverage; 2 passed, 0 failed via legacy unittest
- **New tests added**: 83 collected scenarios
- **Regressions**: None

## Deviations from Plan

- Finalized the reusable engine path as `.github/hooks/lib/file_access.py` so
  Feature 03 can import evaluation independently of the hyphenated command
  entrypoint.
- Reused Feature 01's completed pytest/coverage harness through `uv` instead of
  invoking another test-writer pass.
- The live bypass-permissions check is documented as `NOT RUN`; Feature 04 owns
  the disposable consuming-project harness needed to observe it safely.

## Gaps

- Real runner evidence for deny-tier `.env` and generated-wiring access in a
  disposable `bypass-permissions` session remains `NOT RUN` pending Feature 04.

## Reviewer Focus Areas

- `.github/hooks/lib/file_access.py` priority/action ordering and filesystem
  case detection, especially narrow allow rules over broad denies.
- `.github/hooks/scripts/file-access-guard.py` Grep `path`/`glob` extraction and
  the fail-closed boundary for malformed guarded inputs.
- `.github/hooks/config/file-access-rules.json` self-protection completeness and
  avoidance of broad `id_*` behavior.
- Structured guidance/audit redaction: normalized paths are intentional, while
  content, patterns, commands, and full payloads must remain absent.
