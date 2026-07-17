# Feature Plan: Interceptor Retirement

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `.github/hooks/file-access-guard.json`, `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/scripts/rtk-rewrite.sh`, `.github/hooks/lib/file_access.py`, `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/config/file-access-rules.json`, `.github/hooks/config/file-access-overrides.json`, `scripts/propagate_master_assets.py`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/file-access-guard.js`, `tests/hooks/test_file_access_guard.py`, `tests/hooks/test_bash_command_analyzer.py`, `tests/hooks/test_rtk_rewrite_hook.py`, `tests/hooks/test_hook_distribution_integration.py`, `tests/hooks/test_injection_scanner.py`, `tests/test_propagate_master_assets.py`, `tests/hooks/fixtures/file_access/` `(verify)`, `tests/hooks/fixtures/bash/` `(verify)`, `tests/hooks/fixtures/url_exfiltration/` `(verify)`, `docs/hooks/file-access-guard.md`, `docs/hooks/installation.md`, `docs/hooks/bash-command-limitations.md` `(verify)`, `docs/hooks/hook-verification.md` `(verify)`, `docs/hooks/manual-qa.md` `(verify)`, `docs/hooks/prompt-injection-defense.md` `(verify)`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** The file-access guard descriptor, entrypoint, path-policy implementation, Bash analyzer, guard-only URL-exfiltration logic, rule configuration, and override configuration are removed from the source hook unit.
2. **AC2:** The automatic `rtk-rewrite.sh` hook and every project-generated or user-global registration owned by it are retired without uninstalling or disabling the RTK executable.
3. **AC3:** Direct file operations and Bash commands no longer pass through the retired file-access system; verification tests absence of interception rather than only absence of filenames.
4. **AC4:** The shared hook framework, injection-scanner implementation, injection configuration, audit hook, and notification hook remain active and pass their independent regression coverage.
5. **AC5:** `scripts/propagate_master_assets.py` recognizes every retired guard and RTK asset through `RETIRED_HOOK_ASSETS` or an equivalently verified existing retirement mechanism, hardens the current cleanup path so same-named unowned regular files or links are preserved, removes only ownership-proven retired generated assets, and preserves unrelated hook wiring.
6. **AC6:** Guard-only tests and RTK-rewrite tests are removed; mixed injection-scanner, hook-distribution, and propagation tests are surgically rewritten so their independent assertions remain meaningful.
7. **AC7:** Generated Claude, Codex, and OpenCode hook outputs contain no file-access-guard or automatic RTK-rewrite registration while retaining prompt-injection and shared-framework behavior.
8. **AC8:** Active hook documentation states the reduced security posture accurately and does not claim that prompt-injection defense replaces protected-file enforcement.
9. **AC9:** Repository guidance continues to permit and recommend explicitly RTK-prefixed commands where already appropriate and never claims RTK itself was retired.
10. **AC10:** Phase 01, Phase 02, and Phase 07 status lines are not changed; structural phase reconciliation remains routed to `project-planner`.

### Non-Goals

- Uninstalling RTK or removing explicit RTK usage guidance.
- Removing the shared hook framework, injection scanner, audit hook, or notification hook.
- Repairing the retired Bash grammar or retaining its parser for future command allowlists.
- Moving historical phase status lines or rewriting project roadmap ownership.
- Implementing managed-copy deployment; that begins in `02-propagation-convergence`.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---|---|---|
| AC1–AC3 | Retired files under `.github/hooks/`; `.claude/settings.json`; `.codex/hooks.json`; `.opencode/plugins/` | Absence-of-interception scenarios; generated-wiring inventory assertions |
| AC4 | `.github/hooks/lib/framework.py`; `.github/hooks/lib/injection_scanner.py`; surviving hook descriptors | Existing framework and scanner suites; focused surviving-hook smoke checks |
| AC5–AC7 | `scripts/propagate_master_assets.py`; generated hook outputs | Updated `tests/test_propagate_master_assets.py`; updated hook-distribution integration scenarios |
| AC6 | Guard-only and mixed test files under `tests/hooks/` | Review confirms guard-only deletion and retained scanner assertions remain behavior-based |
| AC8–AC10 | `docs/hooks/`; Phase 04 records; RTK instruction surfaces | Documentation regression search distinguishing operational guidance from historical/security discussion |

## B. Correctness & Edge Cases

- Remove whole retirement units, including reverse dependents and generated copies, so `url_exfiltration.py` is not left orphaned.
- Treat guard fixtures used only as propagation scaffolding as replaceable fixtures; do not weaken the propagation behavior they exercise.
- Preserve `$source`-based user wiring not owned by the retired hooks.
- Retiring a dangling generated asset must be idempotent and must not delete a same-named unowned regular file.
- Verify explicit `rtk` invocation separately from automatic rewrite absence.
- Fail the feature if scanner/framework tests require a deleted guard API after mixed-test surgery.

## C. Consistency & Architecture Fit

- Extend the verified `RETIRED_HOOK_ASSETS` cleanup pattern in `scripts/propagate_master_assets.py`, but first harden `_remove_retired_hook_assets` because its current same-name deletion behavior does not prove ownership.
- Preserve the current source-to-generated flow: `.github/hooks/` remains authoritative for surviving hooks.
- Keep deletion fail-closed with respect to ownership: only known retired source assets and generated entries with matching ownership evidence may be removed.
- Relationship: this feature precedes `02-propagation-convergence` because both modify the propagator and its tests.
- Relationship: `06-runtime-verification` rechecks the final surviving hook roster and explicit RTK behavior.

## D. Clean Design & Maintainability

- Delete guard-only code instead of leaving compatibility shims or dead feature flags.
- Replace guard-based propagation fixtures with the smallest surviving hook fixture that tests the same propagation property.
- Keep retirement lists explicit and reviewable; do not introduce broad filename-pattern deletion.
- Keep it clean checklist: no dead imports, no orphan configuration, no stale generated plugin, no RTK uninstall logic, no weakened scanner assertion.

## E. Completeness: Observability, Security, Operability

- Observability: reuse propagation result counters for retired assets; no new normal-path log line is justified.
- Security: explicitly record that protected-file and Bash-command enforcement disappear while injection-output scanning remains.
- Data handling: do not read or echo live secret content while proving absence of interception.
- Runbook: run focused hook and propagation suites, regenerate to a fixed point, inspect surviving hook rosters, and roll back by reverting this feature as one retirement unit.

## F. Test Plan

- Existing tests retained: independent framework and injection-scanner suites.
- Existing tests removed: file-access-guard, Bash analyzer, and automatic RTK-rewrite behavior suites.
- Existing tests updated: mixed hook-distribution, injection-scanner, and propagation suites.
- Runner constraint: the current environment lacks the `pytest` module; implementation must provision the declared development requirements or record runner-constrained evidence without claiming a passing baseline.

### Top 5 High-Value Test Cases

1. **Given** generated wiring containing retired and surviving hooks, **when** propagation reconciles it, **then** only retired owned entries disappear.
2. **Given** ordinary direct file and Bash tool payloads, **when** surviving hooks execute, **then** no file-access decision is emitted.
3. **Given** malicious prompt-injection output, **when** the surviving scanner executes, **then** its independent block/redaction behavior remains unchanged.
4. **Given** an explicitly prefixed RTK command, **when** it runs after retirement, **then** RTK remains available while an unprefixed command is not rewritten.
5. **Given** a second propagation pass, **when** no source changes occurred, **then** no retired asset is removed twice and no unrelated wiring changes.

## Stage 1: Retire Source Interceptors
**Goal**: Remove the complete guard and automatic rewrite source units.
**Success Criteria**: AC1–AC3 are satisfied with no orphan guard-only imports or configuration.
**Status**: Not Started

## Stage 2: Reconcile Generated Wiring and Tests
**Goal**: Remove generated registrations and preserve independent regression coverage.
**Success Criteria**: AC4–AC7 pass focused automated verification.
**Status**: Not Started

## Stage 3: Correct Security and RTK Claims
**Goal**: Make active documentation match the reduced posture without changing phase ownership.
**Success Criteria**: AC8–AC10 pass documentation review and regression searches.
**Status**: Not Started

## Unverified Assumptions

- User-global automatic RTK registration may live outside repository-controlled files; Feature 6 must inventory and verify it rather than assume repository regeneration removes it.
