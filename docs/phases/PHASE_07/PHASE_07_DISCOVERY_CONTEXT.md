# Phase 07 Discovery Context

Context gathered during the 2026-07-17 refinement session that rescoped Phase 07 from
"Hook Release Remediation & Verification" to "Package for General Use". Downstream agents
should load this alongside `PHASE_07_SUMMARY.md`.

## Why the rescope happened

- The user established that hooks currently protect **only this repository**: hook wiring
  is generated only into this repo's `.claude/settings.json`, `.codex/hooks.json`, and
  `.opencode/plugins/`, anchored to `$CLAUDE_PROJECT_DIR`-style paths. The `--runtime-deploy`
  managed-copy flow ships agents, commands, skills, and learnings (`scripts/runtime_deployment.py`,
  `_ASSET_POLICIES`) — **not hooks**. Verifying an undistributable suite was judged the wrong
  next investment; packaging is what makes the hook work meaningful.
- Execution order changed: Phase 07 previously ran 5th (before 05/06); it now runs **last**,
  after Phases 05 and 06, so the complete hook set is packaged once. The prior Phase 07's
  verification content (Phase 02 gate re-run, REPO-SEC-06, live QA, record reconciliation,
  Phase 02/03 verdicts) was absorbed into this phase's tail, not dropped.
- The user has **macOS only**; Linux/native Windows/WSL live evidence is permanently
  `NOT RUN` for this phase by hardware constraint.
- The live PR Review run (the fixture family's first end-to-end execution, previously the
  decision log's largest open risk) was started by the user on a real external repo during
  this session; its outcome is evidence input for the Phase 03 verdict in deliverable 6.

## Web research: Codex hooks mechanism (2026-07-17)

Full report: `dev/research/codex-hooks-mechanism/codex-hooks-mechanism-report.md`
(summary alongside it). Key findings consumed by this phase:

- Codex CLI hooks are official (developers.openai.com/codex/hooks). Events:
  `SessionStart`, `SubagentStart/Stop`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`,
  `PostToolUse`, `PreCompact`, `PostCompact`, `Stop`. Config is Claude-Code-shaped JSON or
  TOML array-of-tables.
- **User-global hooks exist**: precedence (highest→lowest) `~/.codex/hooks.json`,
  `~/.codex/config.toml` `[hooks]`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`,
  plugin hooks. Merging is **additive** — all matching hooks run concurrently.
- `PreToolUse` can deny (exit code 2 with stderr reason, or JSON `permissionDecision`) and
  can rewrite tool inputs (`updatedInput`). Hooks receive stdin JSON (`session_id`, `cwd`,
  `model`, `permission_mode`, `tool_name`, `tool_input`, `tool_response`, ...).
- Caveats: per-hook **hash-based trust** (regenerated commands require re-trust via
  `/hooks` — upgrades are non-silent on Codex); only "simple" shell calls under
  `unified_exec` are intercepted; open bug — `codex exec` non-interactive mode does not
  dispatch repo-level `hooks.json` hooks (openai/codex issues #26383, #26452; user-global
  layer behavior to be verified in live QA); hooks can stop firing after rate-limit stops
  (#21160); disable via `[features] hooks = false`; Windows uses `commandWindows`.
  Version gate: full feature set at ~**v0.123 (late Apr 2026)**, inferred from merged PRs
  and release tags rather than an explicit GA changelog entry.
- Enterprise `requirements.toml` can set `allow_managed_hooks_only = true`, suppressing
  user/project/plugin hooks entirely — worth one line in the install disclosure.

## Precedent inside this repo

- The retired `rtk-rewrite` hook was registered globally in `~/.claude/settings.json` with
  an absolute path into this repo and fired in every project — proof the Claude global
  mechanism works, and the recorded absolute-path fragility is the failure mode the
  managed-copy home deployment avoids.
- The hook framework's config layering (repo defaults → project overrides) is the intended
  base for the per-repo opt-out deliverable.
- Kill-switch asymmetry (`injection-overrides.json`: absent = enabled, present = disabled,
  restore = delete) is recorded in `.github/learnings/cross-phase-decisions.md` under
  "Hook Composition".
