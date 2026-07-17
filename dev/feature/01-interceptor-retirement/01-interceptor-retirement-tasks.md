# Feature Tasks: Interceptor Retirement

- [ ] Task 1: Capture a pre-change inventory of the source hook descriptors, Claude/Codex/OpenCode generated wiring, the user-global automatic RTK rewrite registration, installed RTK executable, and surviving framework/scanner/audit/notification assets without reading secret content.
- [ ] Task 2: Run or record the focused pre-change hook and propagation baseline; if `pytest` remains unavailable, provision `requirements-dev.txt` or mark the evidence runner-constrained without claiming a pass.
- [ ] Task 3: Confirm the complete reverse-dependency cut for `file-access-guard.py`, `file_access.py`, `bash_analyzer.py`, `url_exfiltration.py`, the two guard configuration files, and the guard descriptor before deletion.

## Stage 1: Retire Source Interceptors

- [ ] Task 4: Remove `.github/hooks/file-access-guard.json` and `.github/hooks/scripts/file-access-guard.py` as one source-hook unit.
- [ ] Task 5: Remove `.github/hooks/lib/file_access.py`, `.github/hooks/lib/bash_analyzer.py`, and `.github/hooks/lib/url_exfiltration.py`; then remove stale imports and verify no surviving runtime module consumes their APIs.
- [ ] Task 6: Remove `.github/hooks/config/file-access-rules.json` and `.github/hooks/config/file-access-overrides.json`; verify surviving scanner configuration remains intact and independently loadable.
- [ ] Task 7: Remove `.github/hooks/scripts/rtk-rewrite.sh` and the repository-owned user-global registration that points to it while preserving every unrelated user-global hook entry.
- [ ] Task 8: Verify RTK remains installed and an explicitly prefixed RTK command still works; separately verify an unprefixed command is no longer automatically rewritten.
- [ ] Task 9: Verify ordinary direct file operations and Bash payloads execute without producing a retired file-access decision, audit row, prompt, or denial.

## Stage 2: Reconcile Generated Wiring and Tests

- [ ] Task 10: Extend `RETIRED_HOOK_ASSETS` or the equivalent verified cleanup mechanism in `scripts/propagate_master_assets.py` with every copied guard or rewrite runtime asset that source discovery alone cannot remove.
- [ ] Task 11: Keep retirement cleanup fail-closed on ownership: do not delete a same-named unowned regular file, do not follow symlinked parents, and do not broaden cleanup into filename-pattern matching.
- [ ] Task 12: Regenerate repository hook outputs so `.claude/settings.json`, `.codex/hooks.json`, and `.opencode/plugins/` contain no guard registration or plugin while preserving scanner, audit, notification, and unrelated project hooks.
- [ ] Task 13: Run propagation repeatedly until a no-change pass is observed; restart any stale watcher first and record the final counters.
- [ ] Task 14: Remove `tests/hooks/test_file_access_guard.py`, `tests/hooks/test_bash_command_analyzer.py`, and `tests/hooks/test_rtk_rewrite_hook.py` with the retired integrations.
- [ ] Task 15: Check `tests/hooks/fixtures/file_access/`, `tests/hooks/fixtures/bash/`, `tests/hooks/fixtures/url_exfiltration/`, and the shared recorded-payload fixture for surviving consumers; remove only fixtures made orphaned by retirement.
- [ ] Task 16: Surgically update `tests/hooks/test_injection_scanner.py` to remove the guard self-protection dependency while retaining scanner schema, normalization, redaction, fail-closed, allowlist, performance, and entrypoint coverage.
- [ ] Task 17: Surgically update `tests/hooks/test_hook_distribution_integration.py` to remove propagated-guard and guard-latency cases while preserving independent scanner distribution, redaction, installation-classification, and honest manual-QA assertions.
- [ ] Task 18: Replace guard-based `_seed_hooks` scaffolding and `$source == "file-access-guard"` expectations in `tests/test_propagate_master_assets.py` with the smallest surviving hook fixture that proves the same propagation, path anchoring, cleanup, and idempotency properties.
- [ ] Task 19: Add or update behavior-based retirement scenarios proving owned retired entries disappear, unowned collisions survive, surviving hooks remain active, and a second pass performs no repeated retirement or unrelated mutation.
- [ ] Task 20: Run the independent shared-framework, injection-scanner, injection-corpus, hook-distribution, and propagation suites; classify evidence as existing-test pass, required-new-test pass, runner-constrained, code-review-only, or manual QA.

## Stage 3: Correct Security and RTK Claims

- [ ] Task 21: Retire or rewrite `docs/hooks/file-access-guard.md` so active documentation plainly states that protected-file and Bash-command enforcement have been removed and prompt-injection defense is not a replacement.
- [ ] Task 22: Update `docs/hooks/installation.md` to remove guard installation, double-invocation, override, and recovery instructions while preserving accurate surviving-hook setup.
- [ ] Task 23: Inspect and reconcile `docs/hooks/bash-command-limitations.md`, `docs/hooks/hook-verification.md`, `docs/hooks/manual-qa.md`, and `docs/hooks/prompt-injection-defense.md`; remove stale operational claims and counts without deleting legitimate historical or security-threat discussion.
- [ ] Task 24: Search repository RTK instruction surfaces and preserve explicit RTK-prefixed command recommendations; remove only claims or setup steps for automatic rewriting.
- [ ] Task 25: Update phase-local friction, hook-composition, and retirement records required by Phase 04 while leaving Phase 01, Phase 02, and Phase 07 status lines unchanged and routing structural reconciliation to `project-planner`.
- [ ] Task 26: Run staged-file retirement sweeps for guard and rewrite identifiers, review every remaining match as historical, explicitly supported, or stale, and remove any active source/generated/test/documentation reference that would reactivate the retired integrations.
- [ ] Task 27: Hand Feature 6 a verification note identifying the surviving hook roster, explicit RTK result, user-global registration result, runner constraints, and any machine-global location that could not be safely reconciled in this feature.

## Completion Gate

- [ ] Task 28: Confirm AC1–AC10 are each backed by automated evidence or an explicitly named manual/runtime check, all feature stages meet their success criteria, no guard-only code/config/test fixture is orphaned, and no out-of-scope phase status line or unrelated user-global hook was changed.
