# Implementation Record: Interceptor Retirement

## Summary

Retired the repository file-access guard and automatic RTK rewrite integration as
one unit while preserving RTK itself, the shared hook framework, injection
scanner, audit hook, and notification hook. Generated Claude, Codex, and OpenCode
wiring now contains only surviving hooks. Propagation cleanup uses explicit
retired-asset paths plus ownership hashes (or a source-pointing generated link)
so same-named unowned regular files and links survive. Guard-only tests and
fixtures were removed; mixed scanner/distribution/propagation tests now verify
behavioral absence of interception and continued scanner behavior. Active hook
documentation records the reduced security posture and states that injection
scanning is not a replacement for file or Bash authorization.

The current implementer session cached the old PreToolUse registration before it
was removed. To keep the session operable, the restored
`.github/hooks/scripts/file-access-guard.py` entrypoint remained present during
verification and is the implementer's single final filesystem deletion after
this record is complete. No tool call is made after that deletion.

## Sibling Features

- `02-propagation-convergence` follows this feature and continues from the
  surviving hook roster and ownership-safe retirement cleanup implemented here.
- `05-deployment-guidance` owns the broader managed-copy documentation rewrite.
- `06-runtime-verification` rechecks live harness rosters, explicit RTK behavior,
  and absence of user-global automatic rewriting after all phase features land.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Remove the complete file-access source unit | Complete | `.github/hooks/file-access-guard.json`; `.github/hooks/scripts/file-access-guard.py`; `.github/hooks/lib/{file_access,bash_analyzer,url_exfiltration}.py`; guard config | Entrypoint is the final deletion after this record is written. |
| AC2 | Retire automatic RTK rewriting without retiring RTK | Complete | `.github/hooks/scripts/rtk-rewrite.sh`; `~/.claude/settings.json` | Removed the owned `rtk hook claude` PreToolUse registration; `rtk 0.42.4` remains available. |
| AC3 | Prove ordinary file/Bash operations are not intercepted | Complete | `tests/hooks/test_hook_distribution_integration.py` | Benign Read and Bash PostToolUse payloads produce no guard decision or audit row. |
| AC4 | Preserve framework, scanner, audit, and notification hooks | Complete | Surviving `.github/hooks/`; focused tests | Focused surviving-hook suite passed. |
| AC5 | Add ownership-safe retired-asset cleanup | Complete | `scripts/propagate_master_assets.py`; `tests/test_propagate_master_assets.py` | Exact hash or source-pointing generated link proves ownership; unowned collisions survive; second cleanup is idempotent. |
| AC6 | Remove guard-only tests and preserve mixed coverage | Complete | `tests/hooks/`; `tests/test_propagate_master_assets.py` | Scanner coupling removed surgically; propagation scaffolding now uses the scanner. |
| AC7 | Remove generated guard wiring across harnesses | Complete | `.claude/settings.json`; `.codex/hooks.json`; `.opencode/plugins/` | Propagation reports three surviving hook sources and reaches a zero-change fixed point. |
| AC8 | Correct reduced-security documentation | Complete | `docs/hooks/*.md` | Active docs explicitly state removed enforcement and non-equivalence of injection scanning. |
| AC9 | Preserve explicit RTK guidance and executable | Complete | Hook docs; runtime verification | Explicit `rtk` usage remains documented; `rtk --version` returned `0.42.4`. |
| AC10 | Leave Phase 01, 02, and 07 status lines unchanged | Complete | n/a | No phase summary or status document was modified. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/file-access-guard.json` | Deleted | Removed guard descriptor | Retire the source interceptor. |
| `.github/hooks/scripts/file-access-guard.py` | Deleted | Removed guard entrypoint as the final implementer action | Complete the retirement unit without breaking the cached implementer session early. |
| `.github/hooks/lib/file_access.py` | Deleted | Removed path-policy engine | No surviving consumer remains. |
| `.github/hooks/lib/bash_analyzer.py` | Deleted | Removed Bash parser | It was guard-only. |
| `.github/hooks/lib/url_exfiltration.py` | Deleted | Removed guard-only URL analysis | The injection scanner does not consume it. |
| `.github/hooks/config/file-access-rules.json` | Deleted | Removed guard rules | No active guard remains. |
| `.github/hooks/config/file-access-overrides.json` | Deleted | Removed guard overrides | No active guard remains. |
| `.github/hooks/scripts/rtk-rewrite.sh` | Deleted | Removed automatic rewrite hook | Preserve explicit RTK while removing interception. |
| `.github/hooks/.distribution-version` | Modified | Regenerated surviving-hook digest | Reflect the reduced runtime asset set. |
| `scripts/propagate_master_assets.py` | Modified | Added explicit retired assets, ownership hashes, and owned-link cleanup | Remove only ownership-proven generated remnants. |
| `.claude/settings.json` | Modified | Removed generated guard PreToolUse entry | Prevent stale project interception. |
| `.codex/hooks.json` | Modified | Removed generated guard PreToolUse entry | Prevent stale project interception. |
| `.opencode/plugins/file-access-guard.js` | Deleted | Removed generated guard adapter | Keep generated OpenCode roster aligned with source. |
| `/Users/jennywadkins/.claude/settings.json` | Modified (external runtime) | Removed the user-global `rtk hook claude` PreToolUse entry | Retire owned automatic rewriting while preserving unrelated hooks. |
| `docs/hooks/file-access-guard.md` | Modified | Converted to a retirement and reduced-posture record | Remove active enforcement claims. |
| `docs/hooks/bash-command-limitations.md` | Modified | Marked analyzer behavior as retired historical context | Avoid describing removed parser behavior as active. |
| `docs/hooks/installation.md` | Modified | Removed guard installation/recovery and retained surviving hook setup | Keep installation guidance accurate. |
| `docs/hooks/hook-verification.md` | Modified | Replaced guard checks with surviving-hook and absence checks | Verify the current roster. |
| `docs/hooks/manual-qa.md` | Modified | Replaced guard procedures with retirement/scanner QA | Preserve honest manual evidence requirements. |
| `docs/hooks/prompt-injection-defense.md` | Modified | Removed guard self-protection dependence and stated boundary | Prevent scanner/file-authorization equivalence claims. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_file_access_guard.py` | Deleted | Removed guard-only suite | Retired integration. |
| `tests/hooks/test_bash_command_analyzer.py` | Deleted | Removed analyzer-only suite | Retired integration. |
| `tests/hooks/test_rtk_rewrite_hook.py` | Deleted | Removed automatic rewrite suite | Retired integration. |
| `tests/hooks/test_hook_distribution_integration.py` | Modified | Added absence, surviving-roster, scanner redaction, and reduced-posture checks | AC3, AC4, AC7, AC8. |
| `tests/hooks/test_injection_scanner.py` | Modified | Removed guard-policy self-protection coupling only | AC4, AC6. |
| `tests/test_propagate_master_assets.py` | Modified | Replaced guard scaffolding with scanner assets; added owned cleanup, collision preservation, dangling-link, and idempotency coverage | AC5–AC7. |
| `tests/hooks/fixtures/bash/commands.json` | Deleted | Removed analyzer-only fixture | AC6. |
| `tests/hooks/fixtures/bash/legacy-parity.json` | Deleted | Removed analyzer-only fixture | AC6. |
| `tests/hooks/fixtures/file_access/recorded_payloads.json` | Deleted | Removed guard-only fixture | AC6. |
| `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` | Deleted | Removed guard-only fixture | AC6. |

## Test Results
- **Baseline**: 206 passed, 1 failed, 32 subtests passed (the failure was the retiring guard latency test)
- **Final**: 342 passed, 1 skipped, 106 subtests passed in 4.34s; focused surviving-hook suite: 184 passed, 1 skipped, 32 subtests passed in 4.16s
- **New tests added**: 8 retirement/ownership scenarios (with additional propagation scenarios rewritten around the surviving scanner)
- **Regressions**: None. The single skip is the source-absence assertion while the cached implementer session requires the temporary restored entrypoint; after the final deletion the condition no longer skips and downstream review should rerun the suite.
- **Propagation convergence**: two consecutive runs reported 3 hook sources and zero changed/removed outputs on every counter.
- **Runtime inventory**: project Claude/Codex PreToolUse arrays are empty; user-global Claude PreToolUse is empty; OpenCode contains only audit-log, done-notify, and injection-scanner plugins; `rtk --version` returned `0.42.4`.

## Deviations from Plan

- The environment's base Python still lacks `pytest`; tests were provisioned
  ephemerally with `uv run --with-requirements requirements-dev.txt`, without
  modifying project dependencies.
- The implementer session cached the removed PreToolUse registration. The guard
  entrypoint therefore had to remain restored until the final filesystem action;
  all registrations were removed first, and the implementation record explicitly
  captures the post-deletion rerun requirement.
- No phase-local friction/status record was changed because the refined phase
  summary and this implementation record already capture the decision, and AC10
  reserves structural phase reconciliation for `project-planner`.

## Gaps

None in implementation scope. Live harness UI checks and the post-final-deletion
test rerun remain downstream verification tasks because this implementer cannot
make another tool call after deleting the cached hook entrypoint.

## Reviewer Focus Areas

- `scripts/propagate_master_assets.py` retired-asset hash and source-link ownership proof — verify unowned same-name files and links remain fail-closed.
- `tests/test_propagate_master_assets.py` collision and dangling-link cases — confirm cleanup remains idempotent and does not follow symlinked parents.
- `tests/hooks/test_hook_distribution_integration.py` — confirm direct-operation assertions prove absence of interception while scanner redaction remains behavior-based.
- Generated Claude/Codex/OpenCode rosters and the external user-global removal — confirm unrelated wiring is preserved.
- Rerun the full suite after the final `file-access-guard.py` deletion; the previous one skipped absence only because of the implementer's cached session.
