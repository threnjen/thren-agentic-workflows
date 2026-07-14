# Phase 1: Hook Foundation + File-Access Guard

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/inspiration/README.md`

## What's New

After this phase, every project that consumes this repo's assets gets a safety layer that cannot be bypassed: agents can no longer read or edit `.env` files and other secret-bearing files, cannot touch explicitly protected files (lock files, production configs, the hook system itself), and cannot sneak around those rules through shell commands — even when the session runs with bypass permissions. When something is blocked, the agent is told exactly why and what to do instead, so work continues smoothly rather than failing mysteriously. This phase also builds the shared plumbing (config, testing, propagation) that every later hook phase reuses.

## Objective

Establish the Python-stdlib hook framework under `.github/hooks/` (with propagation to platform outputs) and ship its first consumer: a hard-blocking PreToolUse file-access guard covering secrets, protected files, and indirect access via bash — closing the highest-stakes safety gap (goals 2 and 5).

## Scope

### In Scope

- **Hook framework** (`.github/hooks/lib/` or equivalent): stdin JSON payload parsing, decision JSON emission (allow/deny with reason), layered config loading (repo defaults → project overrides), structured logging, and pytest fixtures of real hook payloads for every supported event.
- **File-access guard hook** (PreToolUse, matcher `Read|Edit|Write|MultiEdit|Bash`):
  - Secrets rules: block `.env` and variants (`.env.local`, `.env.production`, …) while allowing templates (`.env.sample`, `.env.example`); common credential files (`*.pem`, `id_rsa*`, `credentials*`, cloud config dirs).
  - Protected-file rules: glob-based config with a per-rule `reason` field (lock files, production configs, `.github/hooks/` itself, user-specified paths).
  - Bash-command analysis: parse Bash tool input to catch indirect access — `cat`/`less`/`head` on protected files, redirections, `cp`/`mv`, heredocs, `xargs`, subshells/command substitution, base64/`xxd` pipes, and symlink traversal into protected paths.
  - Structured deny messages: why it was blocked, which rule fired, and a suggested alternative (e.g., "read `.env.sample` instead").
- **Dangerous-command rules**: recursive-delete and similar destructive patterns, absorbing the current `bash-safety.sh` responsibilities.
- **Consolidation**: fold existing `bash-safety.sh` and `protect-files.sh` behavior into the new guard; retire or thin the bash scripts so there is one source of truth.
- **Optional pre-edit file backup**: snapshot protected-adjacent files before Edit/Write (config-gated, off by default).
- **Propagation**: extend `scripts/propagate_master_assets.py` to emit hook wiring (`.claude/settings.json` entries from `.github/hooks/*.json` definitions; Codex `hooks.json` where supported) and propagate hook scripts/config like other assets.

### Out of Scope

- Prompt-injection scanning of tool outputs (Phase 2).
- Formatting, lint, and Stop-time completion gates (Phase 3).
- Skill enforcement / auto-activation (Phase 4).
- Any copying of code or pattern files from `docs/inspiration/` repos (clean-room constraint — see DISCOVERY_CONTEXT.md).
- Windows support (existing setup is macOS/zsh; keep POSIX-portable but do not test Windows).
- pip-dependency-based hook logic (stdlib only).

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Hook framework | Shared Python lib: payload parsing, decision output, config layering, logging, pytest harness | framework lib; test fixtures/harness |
| 2 | File-access guard | PreToolUse hook: secrets + protected-file rules with per-rule reasons and structured deny messages | rule engine; Read/Edit/Write path guard |
| 3 | Bash-command analyzer | Command parsing to catch indirect access and destructive commands; absorbs bash-safety.sh | bash parser; dangerous-command rules |
| 4 | Propagation integration | propagate_master_assets.py emits hook wiring + scripts to platform outputs; legacy bash hooks consolidated | propagation stage; migration/cleanup |

## Technical Context

- Existing hook definitions: `.github/hooks/{bash-safety,protect-files,audit-log,done-notify}.json` with scripts in `.github/hooks/scripts/*.sh`; wired into `.claude/settings.json` with `$source` tags. The new system should keep the `$source`-tagged generation pattern.
- Propagation: `scripts/propagate_master_assets.py` currently regenerates Claude/OpenCode/Codex agent/skill outputs from `.github/`; recent commits show active work here (`28719a9 improve asset propogation script`).
- Repo conventions: Python tooling exists (`python/` template set, pytest patterns in `tests/`); hooks must be runnable via `python3` with no venv/pip step.
- Hook payload/decision contract: PreToolUse hooks receive JSON on stdin (tool name + tool_input) and can deny via exit code 2 (stderr shown to Claude) or structured JSON output with a decision + reason. The framework should support both, preferring structured JSON.
- Critical behavior to verify early: PreToolUse hooks fire and can block in bypass-permissions mode — this is the premise of the phase (spike/test this first).
- Design references (requirements only, not code): `docs/inspiration/claudekit.md` (file-guard concept, bash parsing), `docs/inspiration/claude-workflow-v2.md` (protect-files/security-check), `docs/inspiration/claude-code-hooks-mastery.md` (.env block), `docs/inspiration/buildwithclaude.md` (file-backup).

## Dependencies & Risks

- **Dependency**: none upstream — this is the foundation phase. Downstream phases 2–4 depend on the framework delivered here.
- **Risk**: bash-command parsing is inherently incomplete (shell grammar is undecidable in general). *Mitigation*: layered approach — exact-match fast paths, conservative pattern rules, and a default-deny option for commands that reference protected paths in any token; document known bypass classes; add fixtures for each discovered bypass.
- **Risk**: false positives blocking legitimate work (e.g., editing `uv.lock` intentionally). *Mitigation*: per-rule reasons + project-level override config; a documented escape hatch (user edits the override file, not the agent); tune rules during a soak period on this repo before propagating.
- **Risk**: hook latency on every tool call. *Mitigation*: stdlib-only, no subprocess spawning in the hot path, budget <50ms per invocation, measured in tests.
- **Risk**: consolidation regressions when retiring `bash-safety.sh`/`protect-files.sh`. *Mitigation*: port their existing rules into the new config first, with tests reproducing their current blocks, before removing the bash scripts.
- **Risk**: propagation wiring differs per harness (Claude settings.json vs Codex hooks.json semantics). *Mitigation*: treat Claude as the primary target; Codex propagation is best-effort and clearly marked.

## Success Criteria

- [ ] A Read/Edit/Write of `.env` in a consuming project is denied with a structured reason; `.env.sample` is allowed.
- [ ] `cat .env`, `cp .env /tmp/x`, `base64 .env`, output redirection onto a protected file, and command-substitution variants are each denied by the bash analyzer (fixture tests per vector).
- [ ] Blocking behavior is verified to hold in bypass-permissions mode (manual verification documented, plus automated payload-level tests).
- [ ] A destructive command matching the dangerous-command rules (e.g., recursive delete of a non-temp path) is denied; the same command against the scratchpad/temp dirs is allowed.
- [ ] All rules live in config files with a `reason` per rule; no rule logic is hardcoded in Python beyond the engine.
- [ ] Every existing block behavior of `bash-safety.sh` and `protect-files.sh` is reproduced by the new system (regression fixtures), and the legacy scripts are retired from settings wiring.
- [ ] `propagate_master_assets.py` emits the hook wiring and scripts into the Claude output set; a fresh consuming project gets working hooks with no manual steps beyond the documented setup.
- [ ] Hook unit tests pass via pytest with recorded payload fixtures; median hook latency <50ms in the benchmark test.

## QA Considerations

- No frontend/UI changes; no manual QA docs required for UI.
- Manual QA needed for the bypass-permissions verification (cannot be fully automated: requires a live Claude Code session in bypass mode attempting protected operations) — a short manual checklist should be produced.
- Integration behavior changes: existing bash hooks are replaced; any developer relying on their exact stderr messages will see new (better) messages. Note in changelog.
- Test impact: new pytest suite under `tests/` for the hook framework and guard; existing tests should be unaffected.

## Notes for Feature - Decomposer

Suggested feature boundaries (4 features, ordered):

1. **Hook framework + payload fixtures** — the shared lib, config layering, decision output, pytest harness, and a spike test confirming block-in-bypass-mode. Everything else depends on this; keep it free of any rule content.
2. **File-access guard (path-based)** — the rule engine + secrets/protected-file rules for Read/Edit/Write/MultiEdit, structured deny messages, project-override mechanism. Depends on 1.
3. **Bash-command analyzer** — command parsing, indirect-access vectors, dangerous-command rules, absorbing bash-safety.sh rules. Depends on 2 (reuses the rule engine); largest and riskiest feature — give it the deepest test plan (one fixture per bypass vector).
4. **Propagation + consolidation** — propagate_master_assets.py hooks stage, settings wiring generation, porting legacy rules, retiring bash scripts, optional file-backup layer, docs. Depends on 1–3.

Careful separation: rule *content* (config files) vs rule *engine* (Python) — features 2 and 3 should both extend config, not fork engine logic. Integration point to watch: the guard and analyzer share the protected-path rule set; define it once.

Clean-room reminder for all implementers: `docs/inspiration/` files describe *what* to cover and *what weaknesses to beat* — never open the inspiration repos' source files to copy code or patterns.
