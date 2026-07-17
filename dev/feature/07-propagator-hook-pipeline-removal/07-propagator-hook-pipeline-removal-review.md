# Review Record: 07-propagator-hook-pipeline-removal

## Summary

The hook-emission pipeline is fully removed from `scripts/propagate_master_assets.py`
and the done-notify wiring is converted to hand-owned static config. All five focus
areas verified: (1) every AC1 hook symbol is gone — a case-insensitive grep for
`hook` and all 14 named symbols returns nothing; (2) the done-notify static config
carries no `$source` tag and no generated header, with command content byte-preserved
across `.claude/settings.json`, `.codex/hooks.json`, and `.opencode/plugins/done-notify.js`;
(3) code-review-graph PostToolUse/SessionStart entries are byte-identical in the diff;
(4) the propagator no longer references the `hooks` key or `.opencode/plugins/` at all —
pruning is marker-based and scoped to agent/command/skill roots, so the header-less
done-notify plugin cannot be classed as an orphan; (5) double `--once` produces zero
`git diff` and the plugin survives. The propagation suite is green (36 passed, 34
subtests). No issues requiring fixes were found.

## Verdict
Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Met | `scripts/propagate_master_assets.py` | grep for `hook` (case-insensitive) + all named symbols returns nothing; `INVENTORY_COUNTERS = frozenset({"source_agents"})` (line 60); `shlex` import pruned; `.github/hooks` removed from `WATCH_DIRS` (lines 31-35); `.distribution-version` deleted |
| AC2 | Met | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/done-notify.js` | Diff confirms only `$source` tags removed; done-notify command strings byte-preserved; `done-notify.js` generated header removed, body unchanged; `.github/hooks/done-notify.json` deleted |
| AC3 | Met | `.claude/settings.json`, `.codex/hooks.json` | audit-log + injection-scanner entries removed; `.opencode/plugins/audit-log.js` and `injection-scanner.js` deleted; grep for `$source`/`audit-log`/`injection-scanner`/`generated` in configs returns nothing; CRG entries byte-identical |
| AC4 | Met (verified by execution) | propagator `--once` | Ran `--once` twice; `git status` empty after both; `.opencode/plugins/done-notify.js` survives |
| AC5 | Met | `tests/test_propagate_master_assets.py` | Hook-emission tests deleted; `StaticDoneNotifyNonInterferenceTests` (lines 930-1029) added; suite green (36 passed, 34 subtests) |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | `test_propagation_does_not_prune_static_done_notify_plugin` asserts survival but does not itself drive a prune over `.opencode/plugins/` (that dir is not a pruned root), so it is a defensive/tautological guard rather than an exercise of the prune path | Low | `tests/test_propagate_master_assets.py:1004` | AC5 | Open (Wont-Fix) |

## Fixes Applied

None — no Blocker/High/Medium issues found.

## Remaining Concerns

- Issue #1: the anti-prune test is defensive rather than exercising a real prune of the
  plugins directory. Low severity; the propagator provably never targets that root, so
  the test correctly encodes the intended invariant. Acceptable as-is.
- Operational (already flagged in the implementation record, not a code issue): any
  long-running `--watch` propagator must be restarted after merge or stale in-memory
  code will re-emit hook wiring.

## Test Coverage Assessment
- Covered: AC1 (symbol-absence grep + surviving suite), AC2/AC3 (config diffs + grep),
  AC4 (double `--once` executed during review), AC5 (two new non-interference tests).
- Missing: no automated test drives the full Claude/OpenCode runtime to confirm the
  Stop notification fires (manual QA per plan; out of static-review scope). The
  end-to-end runtime firing of done-notify remains **unverified by this review** and
  requires a live session check.

## Risk Summary
- `scripts/propagate_master_assets.py` — 546 lines removed; every non-hook propagation
  path is guarded by the surviving suite (36 passed) and the executed double-`--once`
  zero-diff. Low residual risk.
- Config byte-preservation confirmed structurally (diff shows only intended lines
  changed) and both JSON files parse; runtime notification firing not exercised.
- Prune safety rests on marker-based ownership (`_is_generated_output`, positional
  marker check) plus `.opencode/plugins/` not being a prune root — both verified.
