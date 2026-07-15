# Implementation Record: Hook Distribution Integration

## Summary

Extended the existing hook propagation stage with an isolated target-root seam,
self-contained runtime copying, command validation, deterministic versioning,
known-retired asset cleanup, and generated Claude/Codex/OpenCode outputs. The
user-global installer now generates absolute-path regular files with backups
instead of cwd-sensitive symlinks. Legacy `bash-safety` and `protect-files`
sources and generated plugins were retired after the upstream parity gate. A
temporary-consumer integration suite verifies structured decisions,
self-protection, redaction, double invocation, and the latency budget. The
installation and manual-QA guides distinguish automated evidence from unrun
live-runner checks.

## Sibling Features

- Feature 01 supplies `.github/hooks/lib/framework.py`, configuration loading,
  structured decisions, redaction, and failure posture.
- Feature 02 supplies the consolidated `file-access-guard.py`, path evaluator,
  rule/default and protected override files, and self-protection policy.
- Feature 03 supplies `bash_analyzer.py`, the 27-entry legacy parity inventory,
  and the Bash limitations contract. Its green parity suite gated legacy
  retirement here.
- Feature 04 owns only distribution, generated outputs, legacy consolidation,
  cross-feature integration evidence, and installation/operations guidance.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | F04-AC1 | F04-AC1-T1 | `test_hook_propagation_copies_runtime_unit_and_writes_stable_version`; `test_hook_propagation_rejects_missing_runtime_asset` | Complete | `scripts/propagate_master_assets.py`; `.github/hooks/.distribution-version` | `tests/test_propagate_master_assets.py`; `.claude/settings.json`; `.codex/hooks.json`; `.opencode/plugins/file-access-guard.js` | PENDING | PENDING |
| AC2 | F04-AC2 | F04-AC2-T1 | `test_propagated_guard_runs_from_detached_consumer_without_dependencies` | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py`; `docs/hooks/manual-qa.md` | PENDING | PENDING |
| AC3 | F04-AC3 | F04-AC3-T1 | `test_generate_global_hooks_uses_absolute_source_commands`; `test_global_setup_backs_up_user_files_and_installs_regular_outputs` | Complete | `scripts/propagate_master_assets.py`; `scripts/setup-hook-symlinks.sh`; `.gitignore` | `tests/test_propagate_master_assets.py`; `docs/hooks/installation.md` | PENDING | PENDING |
| AC4 | F04-AC4 | F04-AC4-T1 | `test_ac4_legacy_sources_are_retired_after_parity_gate`; upstream parity suite | Complete | Legacy source and generated plugin deletions; generated settings | `tests/hooks/test_hook_distribution_integration.py`; `.github/hooks/config/file-access-rules.json` | PENDING | PENDING |
| AC5 | F04-AC5 | F04-AC5-T1 | `test_hook_regeneration_preserves_user_wiring_and_cleans_owned_stale_output`; `test_hook_regeneration_removes_only_known_retired_runtime_assets` | Complete | `scripts/propagate_master_assets.py`; generated settings/plugins | `tests/test_propagate_master_assets.py`; `.claude/settings.json`; `.codex/hooks.json`; `.opencode/plugins/file-access-guard.js` | PENDING | PENDING |
| AC6 | F04-AC6 | F04-AC6-T1 | `test_ac6_project_and_global_double_invocation_is_consistent` | Complete | Generated relative and absolute command paths | `tests/hooks/test_hook_distribution_integration.py`; `docs/hooks/installation.md` | PENDING | PENDING |
| AC7 | F04-AC7 | F04-AC7-T1 | `test_ac7_installation_guide_classifies_all_five_harnesses` | Complete | `docs/hooks/installation.md` | `docs/hooks/installation.md`; official links embedded in support matrix | PENDING | PENDING |
| AC8 | F04-AC8 | F04-AC8-T1 | `test_ac8_manual_qa_separates_automated_evidence_from_unrun_live_checks`; temporary-consumer deny | Complete | Installation and manual-QA guides | `docs/hooks/manual-qa.md`; `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC9 | F04-AC9 | F04-AC9-T1 | `test_ac9_*` subprocess smoke, self-protection, redaction, and latency tests | Complete | Propagated guard unit and integration suite | `tests/hooks/test_hook_distribution_integration.py`; `docs/hooks/manual-qa.md` | PENDING | PENDING |
| AC10 | F04-AC10 | F04-AC10-T1 | Documentation topic assertions and review audit | Complete | `docs/hooks/installation.md`; `docs/hooks/manual-qa.md` | `tests/hooks/test_hook_distribution_integration.py`; `docs/hooks/installation.md` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Per-project artifact propagation | Complete | `scripts/propagate_master_assets.py`; `.github/hooks/.distribution-version` | Copies the full hook tree without pycache, validates referenced runtime assets, preserves relative wiring, and updates a SHA-256 marker only when inputs change. |
| AC2 | Fresh-clone operation | Complete | Propagator and temporary-consumer tests | The emitted command runs from an isolated consumer with Python stdlib only and no source symlink. |
| AC3 | Generated global setup | Complete | Propagator CLI, setup script, `.gitignore` | `.generated-global-hooks/` is local-only; installed files contain absolute paths, preserve one backup, and are not symlinks. |
| AC4 | Legacy consolidation | Complete | Deleted legacy source definitions/scripts and plugins | Retirement occurred only after the 219-test upstream hook/parity baseline passed. The 27-entry parity inventory remains. |
| AC5 | Harness outputs | Complete | Generated Claude/Codex/OpenCode files | Source-tag cleanup preserves untagged settings; generated-header cleanup preserves user plugins; known retired runtime assets are removed explicitly. |
| AC6 | Double-fire tolerance | Complete | Integration tests and guide | Relative and absolute invocations produce identical allow/ask/deny outcomes and one structured line each. No raw-payload duplicate cache was introduced. |
| AC7 | Installation guide | Complete | `docs/hooks/installation.md` | Claude is fully supported; Codex/OpenCode are partial; Cursor/Copilot are not supported by this distribution. Claims link to current official docs. |
| AC8 | Verified installation path | Complete | Temporary-consumer test and `docs/hooks/manual-qa.md` | The allowed plan alternative—temporary consuming project—was used. Live UI-only checks remain explicitly Not run. |
| AC9 | Integration verification | Complete | `tests/hooks/test_hook_distribution_integration.py` | Real subprocess tests cover allow/ask/deny, eight self-protection targets, redaction, and median latency below 50 ms. |
| AC10 | Change communication and rollback | Complete | Installation/manual-QA docs | Covers env-rule re-tiering, denial messages, Bash limits, versioning, global behavior, upgrade, human-only recovery, and rollback. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/propagate_master_assets.py` | Modify | Added target/source roots, runtime copying, missing-command validation, stable versioning, retired-asset cleanup, absolute command generation, global CLI output, and matcher preservation | Extend the existing propagator rather than add a parallel distribution path |
| `scripts/setup-hook-symlinks.sh` | Modify | Replaced symlinks with generated absolute wiring, one-time backups, regular-file installation, stale owned-plugin cleanup, and explicit verification failures | Make global setup cwd-independent and safe to test with a temporary HOME |
| `.gitignore` | Modify | Ignores `.generated-global-hooks/` | Prevent machine-specific absolute paths from being committed |
| `.github/hooks/.distribution-version` | Create | Stores `phase-01-sha256:<digest>` | Detect and communicate runtime-unit changes deterministically |
| `.claude/settings.json` | Regenerate | Removed legacy source-tagged entries; emitted consolidated matcher/command; preserved untagged and unrelated hooks | Claude project wiring from the single guard source |
| `.codex/hooks.json` | Regenerate | Removed legacy source-tagged entries; emitted consolidated matcher/command; preserved untagged and unrelated hooks | Codex compatibility wiring from the single guard source |
| `.opencode/plugins/file-access-guard.js` | Create/Regenerate | Generated consolidated `tool.execute.before` adapter | OpenCode compatibility output from the single guard source |
| `.github/hooks/bash-safety.json` | Delete | Retired legacy Bash source definition | Consolidated analyzer passed parity gate |
| `.github/hooks/protect-files.json` | Delete | Retired legacy file-protection definition | Consolidated guard supersedes it |
| `.github/hooks/scripts/bash-safety.sh` | Delete | Retired legacy Bash script | Consolidated Python entrypoint supersedes it |
| `.github/hooks/scripts/protect-files.sh` | Delete | Retired legacy wrapper | Consolidated Python entrypoint supersedes it |
| `.github/hooks/scripts/protect-files.py` | Delete | Retired legacy implementation | Consolidated path evaluator/entrypoint supersedes it |
| `.opencode/plugins/bash-safety.js` | Delete | Removed generated legacy plugin | Avoid legacy/consolidated double firing |
| `.opencode/plugins/protect-files.js` | Delete | Removed generated legacy plugin | Avoid legacy/consolidated double firing |
| `docs/hooks/installation.md` | Create | Five-harness support, project/global setup, double-fire, upgrade, recovery, rollback, policy, and limitations guide | AC7 and AC10 operations contract |
| `docs/hooks/manual-qa.md` | Create | Records disposable-consumer results and separates automated evidence from unrun live checks | Honest AC8 evidence disposition |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Added eight propagation/global tests while retaining the original two | AC1–AC5, idempotence, ownership preservation, safe symlink replacement |
| `tests/hooks/test_hook_distribution_integration.py` | Create | Added 19 parameterized/integration/documentation tests | AC4, AC6–AC10 |

## Test Results
- **Baseline**: 221 passed, 0 failed (219 upstream hook/parity tests plus 2 stdlib propagation tests)
- **Final**: 248 passed, 0 failed (`pytest -q`); the stdlib compatibility run separately passed 10/10
- **New tests added**: 27
- **Coverage**: 63.08% across the Phase 01 hook libraries and propagation module (`--cov-fail-under=50`)
- **Regressions**: None

## Deviations from Plan

- Stage 0's separate `@z-test-writer` invocation was not repeated because the
  upstream feature wave had already delivered `requirements-dev.txt`, pytest,
  pytest-cov, and a green 219-test hook/parity suite before this feature began.
- The selected machine-local path is `.generated-global-hooks/`; the selected
  marker format is `phase-01-sha256:<digest>`.
- The historical `setup-hook-symlinks.sh` filename remains for compatibility,
  but its behavior no longer creates symlinks.
- No persistent duplicate-message cache was added. Each invocation already
  emits one redacted decision, and storing request-derived fingerprints would
  add security/state complexity. The guide documents that two configured
  layers may produce two redacted audit rows.

## Gaps

- Live Claude Code UI checks for `bypassPermissions`, ask behavior, subagent
  tool calls, and global-plus-project message presentation were **Not run**.
- Live Codex trust/decision handling and live OpenCode blocking were **Not
  run**. They remain classified Partial and must not be treated as verified
  enforcement.
- The OpenCode adapter launches the consolidated source command but does not
  yet translate every structured decision into native OpenCode permission
  behavior; this is documented rather than overstated.

## Reviewer Focus Areas

- `scripts/propagate_master_assets.py`: verify command-token validation and the
  source/target-root boundary, including symlink replacement and explicit
  retired-path cleanup.
- `scripts/setup-hook-symlinks.sh`: verify backup idempotence and that stale
  OpenCode cleanup removes only generated-header files.
- Generated Claude/Codex settings: confirm untagged code-review-graph wiring and
  unrelated audit/notification hooks remain intact.
- Support matrix: confirm Partial/Not supported classifications remain aligned
  with current official schemas and the explicitly unrun live checks.
