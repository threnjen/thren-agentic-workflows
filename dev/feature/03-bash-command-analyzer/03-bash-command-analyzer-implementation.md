# Implementation Record: Bash-Command Analyzer

## Summary

Implemented a standard-library, non-executing Bash analyzer that extracts
literal path operands, delegates normalization and tier evaluation to Feature
02, applies data-driven environment/destructive rules from the shared config,
and returns one redacted decision through Feature 01's security framework. The
fixture corpus covers Phase-listed command forms and a 27-entry legacy parity
matrix; unsupported expansion classes are documented explicitly.

## Sibling Features

- `01-hook-framework` supplies normalized payloads, layered configuration,
  security failure handling, structured decisions, and redacted recording.
- `02-file-access-guard` supplies the shared guard entrypoint and authoritative
  `normalize_path`, `load_rules`, and `evaluate_path` contract consumed here.
- `04-hook-distribution-integration` owns generated wiring, legacy retirement,
  double-fire checks, and runner-constrained live verification. Generated
  `.claude/`, `.codex/`, and `.opencode/` outputs were not edited by this feature.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Indirect protected-path access | `test_ac1_indirect_protected_paths_are_denied`; `test_phase_fixture_corpus_replays_covered_and_limited_vectors` | Direct readers, copy/move, redirects, heredoc, xargs, substitution, subshell, base64, and xxd | Complete | `.github/hooks/lib/bash_analyzer.py`; `.github/hooks/scripts/file-access-guard.py` | `tests/hooks/test_bash_command_analyzer.py`; `tests/hooks/fixtures/bash/commands.json` | PENDING | PENDING |
| AC2 | Symlink defenses | `test_ac2_symlink_creation_to_protected_target_is_denied`; `test_ac2_existing_symlink_traversal_is_denied` | Short/long symlink creation and real normalized traversal | Complete | `.github/hooks/lib/bash_analyzer.py` | `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC3 | Evasion boundary | `test_ac3_evasion_fixtures_are_covered_or_documented` | Quote split, variable, glob, interpreter, home, traversal, and command case fixtures | Complete | `.github/hooks/lib/bash_analyzer.py`; `docs/hooks/bash-command-limitations.md` | `tests/hooks/fixtures/bash/commands.json`; `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC4 | Environment exposure tiers | `test_ac4_environment_exposure_uses_ask_tier`; `test_ac4_non_dump_environment_commands_are_allowed` | Dump/echo asks including PATH, with non-dump safe controls | Complete | `.github/hooks/config/file-access-rules.json`; `.github/hooks/lib/bash_analyzer.py` | `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC5 | Exfiltration tiers | `test_ac5_protected_file_exfiltration_is_denied_and_redacted`; `test_ac8_command_only_match_records_no_command_body` | Curl/wget option forms, encoding pipelines, normalized protected paths, redacted output/records | Complete | `.github/hooks/lib/bash_analyzer.py`; `.github/hooks/scripts/file-access-guard.py`; shared rule config | `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC6 | Destructive command tiers | `test_ac6_all_legacy_destructive_patterns_use_ask_tier`; `test_ac6_approved_scratchpad_delete_is_allowed`; `test_ac6_protected_target_inside_scratchpad_still_denies` | All 16 patterns, case variants, narrow approved roots, deny precedence | Complete | `.github/hooks/config/file-access-rules.json`; `.github/hooks/lib/bash_analyzer.py` | `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC7 | Legacy regression parity | `test_ac7_exact_legacy_inventory_has_config_and_replay_coverage` | Replay exact 16 fixed strings and 11 regex behaviors with retier rationale | Complete | `.github/hooks/config/file-access-rules.json` | `tests/hooks/fixtures/bash/legacy-parity.json`; `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC8 | One shared engine | `test_ac8_guard_entrypoint_emits_one_strongest_decision`; `test_ac8_analyzer_reuses_shared_path_contract_and_never_executes_commands`; malformed-input tests | One decision, shared imports, no execution, fail closed, redaction, bypass ask preservation | Complete | `.github/hooks/lib/bash_analyzer.py`; `.github/hooks/scripts/file-access-guard.py` | `tests/hooks/test_bash_command_analyzer.py`; `docs/hooks/hook-verification.md` | PENDING | PENDING |
| AC9 | Documented limitations | `test_ac9_recursive_parent_scan_is_explicitly_bounded`; `test_ac9_shared_live_checklist_contains_bash_evidence_rows` | Reproducible risks, boundaries, alternatives, and shared verification evidence | Complete | `docs/hooks/bash-command-limitations.md`; `docs/hooks/hook-verification.md` | `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Detect Phase-listed literal and structural protected-path access. | Complete | Analyzer; guard entrypoint | Every candidate uses Feature 02 evaluation. |
| AC2 | Deny protected symlink creation and traversal. | Complete | Analyzer | Both `-s` and `--symbolic` are configured. |
| AC3 | Cover or explicitly bound all named evasion classes. | Complete | Analyzer; limitations doc | Variable/interpreter expansion is intentionally unsupported and documented. |
| AC4 | Apply ask-tier environment exposure policy. | Complete | Shared config; analyzer | `echo $PATH` remains `ask`, including bypass mode absent explicit escalation. |
| AC5 | Deny protected-file exfiltration without command disclosure. | Complete | Analyzer; guard entrypoint | Curl/wget paths and encoding pipeline sources use the path engine. |
| AC6 | Ask for destructive commands while allowing narrow scratch paths. | Complete | Shared config; analyzer | Protected paths nested under approved roots still deny. |
| AC7 | Preserve or explicitly retier all 27 legacy behaviors. | Complete | Shared config | 16/16 fixed strings and 11/11 regex cases replay green. |
| AC8 | Reuse one framework, configuration, decision, and path engine. | Complete | Analyzer; guard entrypoint | No subprocess, shell execution, or duplicate decision JSON. |
| AC9 | Publish honest unsupported boundaries. | Complete | Limitations and verification docs | Recursive parent scans are explicitly not claimed as covered. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/bash_analyzer.py` | Create | Tokenization, operand extraction, validated Bash matchers, approved-root handling, and aggregate matches | Non-executing Bash classification using shared path contracts |
| `.github/hooks/scripts/file-access-guard.py` | Modify | Route Bash payloads through the analyzer and emit/record the strongest match | Preserve the single decision boundary |
| `.github/hooks/config/file-access-rules.json` | Modify | Add Bash analysis metadata, env/destructive rules, approved roots, exfil options, and 27-entry parity metadata | Keep policy data out of Python |
| `docs/hooks/bash-command-limitations.md` | Create | Reproductions, risks, boundaries, and safer alternatives | Honest unsupported-syntax contract |
| `docs/hooks/hook-verification.md` | Modify | Add payload-level Bash deny/redaction evidence and retain live ask as NOT RUN | Shared runner-constrained handoff |
| `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-tasks.md` | Modify | Mark completed implementation/evidence tasks and retain the live-runner item | Accurate execution state |
| `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-implementation.md` | Create | Traceability, evidence, deviations, and gaps | Reviewer handoff |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_bash_command_analyzer.py` | Create | 66 collected analyzer, integration, parity, redaction, precedence, and limitation cases | AC1–AC9 |
| `tests/hooks/fixtures/bash/commands.json` | Create | Covered/limited Phase command corpus with expected action and category | AC1–AC6, AC9 |
| `tests/hooks/fixtures/bash/legacy-parity.json` | Create | Exact 16 fixed-string and 11 regex replay cases | AC7 |

## Test Results
- **Baseline**: 142 passed, 0 failed via full pytest; 2 passed, 0 failed via legacy unittest
- **Final**: 208 passed, 0 failed via full pytest; 66 feature tests passed; 2 passed, 0 failed via legacy unittest; 90% analyzer coverage and 77.76% combined hook-library coverage
- **New tests added**: 66 collected Bash-command analyzer cases
- **Regressions**: None

## Deviations from Plan

- Reused and verified Feature 01's completed pytest/coverage harness rather than
  invoking a redundant test-writer pass.
- Finalized proposed names as `.github/hooks/lib/bash_analyzer.py`,
  `tests/hooks/fixtures/bash/`, and
  `docs/hooks/bash-command-limitations.md`.
- Scoped destructive-operation exceptions to `.agent/scratchpad` and
  `.agent/tmp`; these exceptions apply only to configured destructive rules and
  cannot weaken a protected-path denial.
- Live Claude Code execution was not launched from this implementation pass;
  the shared checklist records `NOT RUN` rather than inferring runner behavior.

## Gaps

- Representative live Bash `deny`, Bash `ask` in bypass-permissions mode, and
  live redaction inspection remain `NOT RUN` pending Feature 04's disposable
  consuming-project integration pass.

## Reviewer Focus Areas

- `.github/hooks/lib/bash_analyzer.py` operand extraction and supported-syntax
  boundary, especially redirects, xargs, symlink creation, and upload options.
- Strongest-action selection in `.github/hooks/scripts/file-access-guard.py` so
  `deny` cannot be weakened by an environment/destructive `ask`.
- Approved-root exemption logic: only `.agent/scratchpad` and `.agent/tmp`
  targets may suppress configured recursive-delete asks; path denials remain.
- The 27-entry parity mapping and fixture must remain synchronized before
  Feature 04 deletes legacy Bash hooks.
