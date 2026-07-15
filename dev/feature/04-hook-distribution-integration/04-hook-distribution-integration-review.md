# Review Record: Hook Distribution Integration

## Summary

Feature 04 now satisfies its automated and static acceptance gates. The review found and fixed two root-boundary defects, made command-token validation cover normalized and nested runtime references, expanded the global installer regression across all three emitted harness outputs, and corrected the Codex support description against current official documentation. Claude Code live-runner checks, native OpenCode blocking, and Codex live trust/decision behavior remain explicitly unrun.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `scripts/propagate_master_assets.py:851-1010`; `tests/test_propagate_master_assets.py:85-224` | Complete runtime copying, deterministic marker, referenced-asset validation, source-root containment, and target-root containment pass in a temporary consumer. |
| AC2 | Verified (automated) | `tests/test_propagate_master_assets.py:226-257` | The emitted relative command executes from a detached temporary consumer with the copied stdlib-only runtime. No live Claude Code process was used. |
| AC3 | Verified (automated) | `scripts/propagate_master_assets.py:1087-1098`; `scripts/setup-hook-symlinks.sh:1-55`; `tests/test_propagate_master_assets.py:259-358` | Absolute-path global wiring, one-time backups, two-run idempotence, regular-file installation, and Claude/Codex/OpenCode ownership behavior pass under a temporary HOME. |
| AC4 | Verified | `tests/hooks/test_hook_distribution_integration.py:66-75`; legacy deletion in commit `8d5b1d8` | Legacy source/plugins are absent, the retained parity inventory has 27 entries, Feature 03 precedes Feature 04 in history, and the current full suite is green. |
| AC5 | Verified | `.claude/settings.json`; `.codex/hooks.json`; `.opencode/plugins/file-access-guard.js`; `tests/test_propagate_master_assets.py:359-437` | Consolidated generated entries preserve untagged settings and user plugins while deleting only generated stale outputs and explicitly known retired assets. |
| AC6 | Partial — live reservation | `tests/hooks/test_hook_distribution_integration.py:147-167`; `docs/hooks/installation.md:85-94` | Relative and absolute invocations return identical allow/ask/deny decisions with one redacted line per invocation. A live runner with both layers active was not exercised, so UI-level message merging remains unverified. |
| AC7 | Verified (static/current docs) | `docs/hooks/installation.md:8-23`; `tests/hooks/test_hook_distribution_integration.py:186-209` | The five-harness classifications were checked against current official Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot documentation. Codex/OpenCode remain Partial and Cursor/Copilot remain Not supported by this distribution. |
| AC8 | Verified (temporary consumer) | `docs/hooks/manual-qa.md:5-24`; `tests/test_propagate_master_assets.py:226-257` | The plan-permitted temporary consuming-project path records an observed deny. Live Claude UI checks are clearly marked Not run. |
| AC9 | Verified (automated) | `tests/hooks/test_hook_distribution_integration.py:76-184` | Real subprocess tests cover allow/ask/deny, eight protected outputs, redaction, dual command forms, and median latency below 50 ms. Live harness semantics are not inferred. |
| AC10 | Verified (documentation) | `docs/hooks/installation.md:96-146`; `docs/hooks/manual-qa.md:52-65` | Policy changes, Bash limits, upgrades, human-only recovery, generated-global behavior, and rollback are documented. The live recovery/rollback walkthrough was not executed in this review. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Symlinked source assets or destination directories could resolve outside the declared source/consumer root. | High | `scripts/propagate_master_assets.py:851`; `scripts/propagate_master_assets.py:948` | AC1, AC2 | Fixed (applied during this review) |
| 2 | Command validation accepted normalized runtime-root escapes and missed dot-prefixed or nested missing-asset tokens. | High | `scripts/propagate_master_assets.py:912` | AC1 | Fixed (applied during this review) |
| 3 | The Codex Partial support note omitted the current documented fact that `permissionDecision: "ask"` is unsupported and continues the call, plus the `apply_patch` input mismatch. | Medium | `docs/hooks/installation.md:14`; `docs/hooks/manual-qa.md:49` | AC7, AC10 | Fixed (applied during this review) |
| 4 | Global installer tests covered Claude only, leaving Codex/OpenCode backup, regular-file, idempotence, and cleanup ownership behavior unproved. | Medium | `tests/test_propagate_master_assets.py:274` | AC3, AC5 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `scripts/propagate_master_assets.py` | Enforced resolved source/output roots and hardened normalized/nested command-token validation. | 1, 2 |
| `tests/test_propagate_master_assets.py` | Added source/output escape regressions, token validation cases, and three-harness installer backup/idempotence/ownership assertions. | 1, 2, 4 |
| `docs/hooks/installation.md` | Documented Codex ask/apply-patch/root-launch limitations without overstating live enforcement. | 3 |
| `docs/hooks/manual-qa.md` | Distinguished current documented Codex limitations from unrun live evidence. | 3 |
| `tests/hooks/test_hook_distribution_integration.py` | Added durable assertions for the Codex limitation disclosures. | 3 |
| `.github/learnings/review-learnings.md` | Recorded the reusable resolved-root validation rule for propagators. | 1, 2 |

## Remaining Concerns

- Live Claude Code checks for `bypassPermissions`, ask behavior, subagent calls, and global-plus-project message presentation remain Not run.
- Codex trust review and live decisions remain Not run; current official docs also make ask-tier and `apply_patch` coverage incomplete by design.
- The OpenCode plugin launches the guard but does not translate its structured decision into native throw/permission behavior; live blocking remains Not run.

## Test Coverage Assessment

- Covered: AC1-AC5 and AC7-AC10 through executed automated/static evidence; AC6 through deterministic dual-command subprocess evidence.
- Missing: live runner evidence for Claude double-fire/message presentation, Codex trust/decision handling, and OpenCode native blocking.
- Focused: `33 passed`.
- Stdlib compatibility: `14 passed`.
- Full suite: `252 passed`.
- Combined coverage gate: `252 passed`, `63.86%` across hook libraries plus the propagation module (`--cov-fail-under=50`).
- Additional gates: Python compile, Claude/Codex JSON parsing, and `git diff --check` passed.

## Risk Summary

- Root-boundary escapes are closed with direct regressions for source symlinks, destination-directory symlinks, normalized `..`, dot-prefixed, and nested command tokens.
- The propagation module is broad and measures 46% in isolation, although the required combined phase gate is 63.86%; the changed distribution paths have direct tests.
- Harness support statements distinguish executed evidence from static contracts and unrun live semantics; no live UI behavior is claimed as verified.
