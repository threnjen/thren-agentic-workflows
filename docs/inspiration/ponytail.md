# ponytail (Dietrich Gebert)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/ponytail`

## Overview

A single behavioral skill — "lazy senior dev mode" — distributed to **~20 agent harnesses** from one repo. The skill forces the simplest solution that actually works via a 7-rung decision ladder (YAGNI → reuse what's in the codebase → stdlib → native platform feature → installed dependency → one line → minimum code that works), with explicit carve-outs it never cuts: trust-boundary validation, data-loss error handling, security, accessibility, and problem comprehension. Mature and popular: npm-published (`@dietrichgebert/ponytail` v4.8.4), 205 commits, MIT, trending badges, multilingual READMEs, and an unusually honest benchmark culture (it publicly corrected its own inflated early numbers after a community issue — mean −54% LOC / −20% cost / −27% time vs a fair agentic baseline, with a separate adversarial safety tier showing 100% safe).

## Agents

None.

## Skills

Six skills in `skills/` (single source of truth; per-platform copies are generated or referenced from here):

- **ponytail** — the core ruleset with intensity levels `lite`/`full`/`ultra` and worked examples per level; "Persistence: ACTIVE EVERY RESPONSE".
- **ponytail-review** — reviews the current diff for over-engineering, returns a delete-list.
- **ponytail-audit** — same, but whole-repo.
- **ponytail-debt** — harvests deferred `ponytail:` corner-cut comments into a ledger.
- **ponytail-gain** — reports the measured benchmark impact.
- **ponytail-help** — command reference.

## Hooks

Six small Node.js scripts (~655 LOC total) in `hooks/`, wired via `hooks/claude-codex-hooks.json` (shared by Claude Code and Codex plugins), plus `copilot-hooks.json` and `qoder-hooks.json` variants. Behavioral, not security:

- **ponytail-activate.js** (SessionStart, matcher `startup|resume|clear|compact`) — loads the active mode and injects the ruleset at session start.
- **ponytail-mode-tracker.js** (UserPromptSubmit) — parses `/ponytail [lite|full|ultra|off|default <mode>]` from the prompt, persists mode to a flag file (session-scoped) or config (default), and injects the mode-filtered ruleset every turn.
- **ponytail-subagent.js** (SubagentStart) — **injects the ruleset into every spawned subagent**, scoped by an optional `PONYTAIL_SUBAGENT_MATCHER` regex against `agent_type` (falls back to inject-everything on invalid regex or unreported type).
- **ponytail-instructions.js** — shared instruction builder; filters the SKILL.md body per active mode (only intensity-table rows and worked examples are mode-keyed; ordinary rules survive verbatim — a subtle bug here got its own fix + test).
- **ponytail-config.js** — config layering: `PONYTAIL_DEFAULT_MODE` env var → `~/.config/ponytail/config.json` (`%APPDATA%` on Windows) → default `full`.
- **ponytail-statusline.sh / .ps1** — optional statusline showing the active mode; setup nudge emitted at most once per user.

Every hook entry in the JSON carries a `commandWindows` PowerShell variant guarded by `Get-Command node`, a 5s timeout, and a `statusMessage`.

## Other assets

- **Distribution matrix** — the repo's real engineering feat. Plugin-tier adapters: Claude Code (`.claude-plugin/` + marketplace), Codex (`.codex-plugin/`), GitHub Copilot CLI, OpenCode (`.opencode/plugins/ponytail.mjs` + commands), Gemini CLI/Antigravity (`gemini-extension.json`), Qoder (`.qoder-plugin/`), Hermes (`plugin.yaml`), Pi (`pi-extension/`), Devin (`.devin-plugin/`), OpenClaw (generated `.openclaw/skills/`). Instruction-only fallbacks: `AGENTS.md`, `.cursor/rules/`, `.windsurf/rules/`, `.clinerules/`, `.github/copilot-instructions.md`, `.kiro/steering/`, `.qoder/rules/`, `.agents/rules/`. `docs/agent-portability.md` maps which file serves which agent, and the README states each harness's support tier honestly (plugin with mode switches vs always-on rules only).
- **Consistency enforcement** — `scripts/check-rule-copies.js` keeps all rule-file copies aligned with the source; `scripts/build-openclaw-skills.js` regenerates the OpenClaw package and the test suite **fails if it is stale**; `scripts/check-versions.js` syncs versions across manifests.
- **Tests** — 15+ `node --test` suites, one per platform adapter (hooks, hooks-windows, opencode-plugin, gemini-extension, copilot-plugin, qoder-plugin, hermes-plugin, openclaw-skills, commands, uninstall, behavior, correctness…).
- **Uninstall hygiene** — `scripts/uninstall.js` cleans state written outside the plugin dir (mode flag, config, statusline entry — only if the entry points at ponytail's own script).
- **Benchmarks** — promptfoo single-shot + a headless agentic harness (`benchmarks/agentic/`) scoring real `git diff`s on a real repo, with control arms (bare model, "caveman", a plain YAGNI prompt) and an adversarial safety tier; dated results write-ups including self-corrections.
- **ponytail-mcp** — a tiny MCP server exposing the instructions as a tool, for hosts with MCP but no skills/hooks.
- Commands as TOML (`commands/*.toml`, Gemini) and markdown (`.opencode/command/`).

## Character

**Specialized behavioral skill, generalized distribution.** The skill content (anti-over-engineering) is orthogonal to this project's security goals — but the repo is the strongest example in the whole survey of exactly what this project's propagation layer and Phase 01 install guide are trying to do: one source of truth, generated per-platform adapters, staleness-tested copies, honest per-harness support tiers, Windows parity, subagent injection, and clean uninstall.

## Install verdict

**Cherry-pick patterns; optional personal install.** As a coding-style skill it may genuinely appeal (it aligns with base-code-guidelines' anti-overcomplication rules), and installing it as a Claude Code plugin is low-risk. For the hooks project, its value is as a **design reference for distribution**, not content:

- **SubagentStart injection + `PONYTAIL_SUBAGENT_MATCHER`** — directly relevant to Phase 01's "hooks must cover subagents" premise spike; proves the event exists and shows a scoping mechanism.
- **Per-harness support-tier honesty** (plugin tier vs instruction-only tier, stated per harness in the README + `docs/agent-portability.md`) — the model for Phase 01's multi-harness install guide AC.
- **Generated adapters with staleness-failing tests** (`check-rule-copies.js`, `build-openclaw-skills.js`) — the pattern `propagate_master_assets.py` should enforce for hook propagation.
- **Config layering + flag-file mode state** and **uninstall that cleans external state** — small, clean references for the hook framework's config and lifecycle story.
- **Caveats:** hooks are Node (this project standardizes on Python stdlib); the ruleset's "ACTIVE EVERY RESPONSE" injection adds per-turn context cost; nothing here addresses security/injection defense.
