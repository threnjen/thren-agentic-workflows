# Phase 01: Hook Foundation + File-Access Guard — Execution Manifest

- **Phase document:** `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`
- **Branch planned:** `phase/hook-foundation-file-access-guard`
- **Execution contract:** Implement features in ascending wave order. A later wave starts only after every dependency in earlier waves is implemented, reviewed, and green.
- **Phase fidelity:** The Phase Key Deliverables sequence is preserved; no requirement is renamed, reordered, moved, or deferred.
- **Test prerequisite:** The current repository has two passing `unittest` tests, no installed/configured pytest runner, and less than 50% hook coverage. Every bundle therefore begins with Stage 0 test prerequisites.

## Ordered Feature Task Names

1. `01-hook-framework`
2. `02-file-access-guard`
3. `03-bash-command-analyzer`
4. `04-hook-distribution-integration`

## Feature Execution Metadata

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---:|---|---|---|---|
| `01-hook-framework` | 1 | yes | none | `.github/hooks/lib/__init__.py` `[PROPOSED - name TBD]`, `.github/hooks/lib/framework.py` `[PROPOSED - name TBD]`, `.github/hooks/scripts/audit-log.py`, `.github/hooks/scripts/audit-log.sh`, `tests/hooks/conftest.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/` `[PROPOSED - name TBD]`, `tests/hooks/test_hook_framework.py` `[PROPOSED - name TBD]`, `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]` | n/a |
| `02-file-access-guard` | 2 | yes | `01-hook-framework` | `.github/hooks/file-access-guard.json` `[PROPOSED - name TBD]`, `.github/hooks/config/file-access-rules.json` `[PROPOSED - name TBD]`, `.github/hooks/config/file-access-overrides.json` `[PROPOSED - name TBD]`, `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]`, `tests/hooks/test_file_access_guard.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/file_access/` `[PROPOSED - name TBD]`, `docs/hooks/file-access-guard.md` `[PROPOSED - name TBD]` | n/a — runtime dependency only; no upstream file is modified |
| `03-bash-command-analyzer` | 3 | no | `01-hook-framework`, `02-file-access-guard` | `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]`, `.github/hooks/config/file-access-rules.json` `[PROPOSED - name TBD]`, `.github/hooks/lib/bash_analyzer.py` `[PROPOSED - name TBD]`, `tests/hooks/conftest.py` `[PROPOSED - name TBD]` `(verify)`, `tests/hooks/test_bash_command_analyzer.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/bash/` `[PROPOSED - name TBD]`, `docs/hooks/bash-command-limitations.md` `[PROPOSED - name TBD]`, `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]` | shares the guard entrypoint and rule config with upstream `02-file-access-guard`, and may extend the shared fixture/checklist assets from `01-hook-framework` |
| `04-hook-distribution-integration` | 4 | yes | `01-hook-framework`, `02-file-access-guard`, `03-bash-command-analyzer` | `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, `scripts/setup-hook-symlinks.sh`, `.gitignore`, generated-global output path `[PROPOSED - name TBD]`, legacy hook definitions/scripts, `.claude/settings.json`, `.codex/hooks.json`, generated `.opencode/plugins/`, `tests/hooks/test_hook_distribution_integration.py` `[PROPOSED - name TBD]`, `docs/hooks/installation.md` `[PROPOSED - name TBD]`, `docs/hooks/manual-qa.md` `[PROPOSED - name TBD]` | n/a — runtime integration dependency only; no upstream source file is expected to be modified |

## Dependency Graph

- `02-file-access-guard` depends_on `01-hook-framework` because it consumes the framework payload, configuration, decision, failure-posture, kill-switch, and redacted-observability contracts.
- `03-bash-command-analyzer` depends_on `01-hook-framework` because it consumes the shared framework and may extend the shared fixture/checklist assets.
- `03-bash-command-analyzer` depends_on `02-file-access-guard` because it reuses and modifies the single guard entrypoint, shared rule configuration, normalized-path evaluator, and tier contract.
- `04-hook-distribution-integration` depends_on `01-hook-framework`, `02-file-access-guard`, and `03-bash-command-analyzer` because it propagates the completed deployable unit, gates legacy retirement on parity, and verifies combined runtime behavior.

## Wave-by-Wave Execution Schedule

### Wave 1 — parallel

- `01-hook-framework`

Exit gate: framework contracts, Stage 0 environment, redacted audit path, live-premise evidence target, and latency tests are ready.

### Wave 2 — parallel

- `02-file-access-guard`

Exit gate: finalized Feature 01 APIs are consumed; recorded Grep payload fields are verified; path, tier, self-protection, and failure tests are green.

### Wave 3 — sequential

- `03-bash-command-analyzer`

Sequential reason: this feature modifies the guard entrypoint and rule configuration created by Feature 02 and may extend shared Feature 01 verification assets. Exit only after the exact 16 `bash-safety.sh` fixed strings and 11 `protect-files.py` Bash regexes are reproduced or explicitly re-tiered with green fixtures.

### Wave 4 — parallel

- `04-hook-distribution-integration`

Exit gate: target-root propagation tests, fresh-consumer smoke tests, generated-global setup, legacy retirement, generated output regeneration, double-fire checks, and installation documentation are complete.

## Expected Feature Bundle Files

| Feature | Plan | Context | Tasks |
|---|---|---|---|
| `01-hook-framework` | `dev/feature/01-hook-framework/01-hook-framework-plan.md` | `dev/feature/01-hook-framework/01-hook-framework-context.md` | `dev/feature/01-hook-framework/01-hook-framework-tasks.md` |
| `02-file-access-guard` | `dev/feature/02-file-access-guard/02-file-access-guard-plan.md` | `dev/feature/02-file-access-guard/02-file-access-guard-context.md` | `dev/feature/02-file-access-guard/02-file-access-guard-tasks.md` |
| `03-bash-command-analyzer` | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-plan.md` | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-context.md` | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-tasks.md` |
| `04-hook-distribution-integration` | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-plan.md` | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-context.md` | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-tasks.md` |

## Discovery Delta Disposition

- Pytest and coverage are not configured: retained as mandatory Stage 0 work in every bundle; hook runtime remains stdlib-only.
- Existing payload aliases differ across hooks: Feature 01 explicitly normalizes all observed aliases and records fixtures.
- The current audit wrapper can propagate filesystem/write failures: Feature 01 now includes the shell wrapper and induced fail-open tests.
- Sibling hook-library imports are not automatically resolvable: Feature 01 requires a tested cwd/PYTHONPATH-independent entrypoint strategy.
- Native Grep scope fields are not recorded: Feature 02 must consume verified Feature 01 fixtures rather than guessing fields.
- Feature 03's upstream names are not implemented yet: Stage 0 requires resolving finalized Feature 01/02 contracts before implementation.
- Existing tests do not cover hook propagation, despite the Phase narrative: Feature 04 classifies hook assertions as new coverage in the existing test module.
- `propagate_hooks_once` is module-global-path-bound: Feature 04 adds the smallest compatible target-root/testability seam before consumer-project tests.

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/hooks/conftest.py` `[PROPOSED - name TBD]` | `01-hook-framework`, `03-bash-command-analyzer` | Shared payload, temporary-repository, and optional Bash fixture helpers |
| `tests/hooks/test_hook_framework.py` `[PROPOSED - name TBD]` | `01-hook-framework` | Payload aliases, decisions, config/cache, failure posture, redaction, and framework latency |
| `tests/hooks/test_file_access_guard.py` `[PROPOSED - name TBD]` | `02-file-access-guard` | File tools, verified Grep fields, path normalization, tier rules, credentials, self-protection, and recovery |
| `tests/hooks/test_bash_command_analyzer.py` `[PROPOSED - name TBD]` | `03-bash-command-analyzer` | Required evasion vectors, action precedence, env/exfiltration/destructive tiers, and exact legacy parity |
| `tests/hooks/test_hook_distribution_integration.py` `[PROPOSED - name TBD]` | `04-hook-distribution-integration` | Fresh consumer, double-fire, redaction, self-protection, end-to-end smoke, and combined latency |
| `tests/hooks/fixtures/` and feature subdirectories `[PROPOSED - name TBD]` | `01-hook-framework`, `02-file-access-guard`, `03-bash-command-analyzer` | Recorded hook payloads and isolated path/Bash scenario data |

### Existing Test Files Updated By Multiple Features

None identified. `tests/test_propagate_master_assets.py` is updated only by `04-hook-distribution-integration`; it receives new hook-propagation and target-root coverage while preserving its two current tests.

### Manual QA Checklist

- [ ] In a disposable live Claude Code session, verify deny-tier protected access remains blocked in bypass-permissions mode.
- [ ] Record the observed behavior of ask-tier rules in bypass-permissions mode; do not infer it from payload-level tests.
- [ ] Verify PreToolUse protection runs for a subagent-originated tool call.
- [ ] Inspect decisions, stderr, audit output, and evidence artifacts to confirm secret sentinels and raw tool/command bodies are absent.
- [ ] With per-project and generated-global layers active, verify allow/ask/deny outcomes are consistent and blocked calls do not produce confusing duplicate messages.
- [ ] Follow the Claude Code installation guide verbatim in a clean checkout/temporary consuming project and verify a representative protected access is denied.
- [ ] Confirm Claude Code, OpenCode, Codex, Cursor, and GitHub Copilot support classifications match current primary documentation or direct observed evidence.
- [ ] Exercise the human-only override kill switch outside the guarded session, restore protection, and complete the rollback/re-propagation walkthrough.
- [ ] Review documented Bash limitations, including recursive parent-directory scans, for an honest covered/unsupported boundary.
