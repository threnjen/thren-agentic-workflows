# Project Roadmap: Security & Determinism Hooks + Phase Final Review

## Vision

A propagated, source-of-truth hook system (Python stdlib, under `.github/hooks/`) that hardens every project against prompt injection and file/secret manipulation — even under bypass permissions — and converts agent-judgment steps in the existing pipeline (formatting, completion claims, skill activation) into deterministic, testable gates. All hooks are original implementations that improve on patterns surveyed in `docs/inspiration/`, never direct copies. The project also adds **Phase Final Review** — a new `05-` orchestrator agent family that evaluates an entire large phase (subphases `PHASE_0Na`–`PHASE_0NX`) end-to-end after implementation.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Hook Foundation + File-Access Guard | Planned | None | Large | Python hook framework (shared helpers, config, tests, propagation support) plus a hard-blocking PreToolUse guard for .env/secrets/protected files, including bash-command parsing for indirect access |
| 02 | Prompt-Injection Defense | Planned | Phase 01 | Medium | PostToolUse scanner over tool outputs with an original, severity-tiered pattern corpus; hard-block on high-confidence matches, warn on the rest; fixture-driven pattern test suite |
| 03 | Format-on-Save + Completion Gates | Planned | Phase 01 | Medium | Project-aware formatter dispatch on edit, plus Stop-time verification gates that block unverified "done" claims using this repo's pipeline artifacts as evidence |
| 04 | Skill Enforcement / Auto-Activation | Planned | Phase 01 (framework), informed by 01–03 tuning | Large | Rules file mapping globs/keywords → required skills; UserPromptSubmit suggestion injection + PreToolUse guard with block/suggest/warn enforcement levels, propagated multi-harness |
| 05 | Phase Final Review agent family | Planned | None (independent of hooks phases; uses existing pipeline assets) | Large | New `05-phase-final-review` orchestrator + `05a`–`05l` evaluator subagents + 3 skills: baseline worktree diffing, whole-phase change narrative, master QA/security rollups, AC regression, seam analysis, artifact/test/consistency/dependency audits, learnings harvest, and a go/no-go readiness synthesis — designed for state-of-the-art models with strict context discipline. Full design in DISCOVERY_CONTEXT.md |

## Constraints & Non-Goals

- **Clean-room constraint**: All hooks and skills are written from scratch. `docs/inspiration/` files are requirements/design references (which events to hook, which failure modes to cover) — never code to copy. No verbatim reuse of pattern files, scripts, or prompts from the surveyed repos.
- **Runtime**: Python 3 stdlib only for hook logic (no pip dependencies in the hooks themselves). Existing bash hooks are folded in or retired as phases absorb their responsibilities.
- **Enforcement posture**: Hard-block (exit 2 / deny) for file access and dangerous commands; warn-and-continue for prompt-injection matches except high-confidence patterns, which block.
- **Distribution**: Hooks live in `.github/hooks/` as source of truth and are propagated to platform outputs via `scripts/propagate_master_assets.py`, consistent with agents/skills/instructions.
- **Non-goal**: Adopting any surveyed repo wholesale (claudekit binary, gstack pipeline, workflow-v2 agents/skills — the latter duplicate this repo's existing pipeline).
- **Non-goal**: Notification/TTS/sound hooks, telemetry hooks, and duplicate agents (code-reviewer, security-auditor, docs-writer variants already exist here).
- **Non-goal**: UI/design skill packs (ui-ux-pro-max is orthogonal to this effort).

## Architecture Notes

- **Hook framework**: shared Python helpers for reading the hook JSON payload from stdin, emitting decision JSON (allow/deny/block with reason), loading layered config (repo defaults → project overrides), and structured logging. Every hook is a thin entrypoint over this framework, unit-testable with pytest fixtures of real hook payloads.
- **Why hooks, not permissions**: `permissions.deny` rules do not survive bypass-permissions mode; PreToolUse hooks fire regardless of permission mode and an exit-2 result blocks the tool call. This is the mechanism that satisfies "protect files even with bypass permissions."
- **Rule/pattern configs are data, not code**: protected-file rules, injection patterns, formatter mappings, and skill rules all live in readable config files (JSON/YAML) with per-rule reasons, so they can be reviewed, tested, and tuned without touching hook logic.
- **Propagation**: `propagate_master_assets.py` gains a hooks stage — emitting `.claude/settings.json` hook wiring (and Codex `hooks.json` where supported) from the `.github/hooks/` source.
- **Phase ordering rationale**: Phase 01 builds the framework everything reuses and closes the highest-stakes gap. Phases 02/03 are independent consumers of the framework. Phase 04 is last because it is the most invasive to the working agent pipeline and benefits from pattern-tuning experience in 01–03.

## Research Base

Nine surveyed repos are inventoried in `docs/inspiration/` (one file per repo + README comparison). Key design references per phase are cross-referenced in each phase summary and in `DISCOVERY_CONTEXT.md`.
