# Discovery Context: Security & Determinism Hooks

Context gathered during planning (2026-07-14) beyond this repo's codebase. Downstream agents (phase-refiner, feature-decomposer, phase-execute) should load this file with each phase document.

## Binding Constraints (user-directed)

1. **Clean-room implementations only.** The user explicitly directed: write our own versions of these hooks/skills — no direct copies from the inspiration repos — and where possible improve and strengthen the existing patterns. Treat `docs/inspiration/` as a requirements/design source (events to hook, failure modes to cover, weaknesses to fix), never as code to copy. Do not lift pattern files (e.g., Lasso's `patterns.yaml`), scripts, or prompt text verbatim.
2. **Runtime**: Python 3 stdlib for all new hook logic (user-selected over bash and TypeScript).
3. **Enforcement**: hard-block for file access / dangerous commands; warn-and-continue for injection detection except high-confidence patterns.
4. **Distribution**: source of truth in `.github/hooks/`, propagated via `scripts/propagate_master_assets.py` alongside agents/skills/instructions.

## Project Goals (user's own framing)

1. Security/vulnerability hooks to stop prompt injection.
2. Protect the system and important files from manipulation **even with bypass permissions** (hence hooks, not `permissions.deny` — PreToolUse hooks fire in bypass mode).
3. Make deterministic what is currently agent-controlled in the workflows.
4. Auto-format files on save with the correct linter/formatter.
5. Block agent access to `.env` files and other common secret-bearing files.

Explicitly rejected: adopting agent/skill collections that duplicate the existing pipeline (e.g., claude-workflow-v2's orchestrator/reviewer/docs-writer agents — "almost the same as my current workflow").

## Additional Research Material

Nine repos cloned by the user into `/Users/jennywadkins/github_repos/claude_skills/` were crawled by subagents; full inventories live in `docs/inspiration/` (one file per repo, plus `README.md` with a comparison table and goal mapping). Summary of design references per phase:

- **Phase 01 (file-access guard)**: claudekit `file-guard` (ignore-file-driven patterns + bash-command parsing for indirect access; ships as compiled binary — a weakness we fix with readable config), claude-workflow-v2 `protect-files.py`/`security-check.py` (stdlib Python, naive path matching), hooks-mastery `pre_tool_use.py` (.env block + `rm -rf` guard), buildwithclaude `file-backup`. Existing repo hooks `bash-safety.sh` and `protect-files.sh` overlap and should be folded in or retired.
- **Phase 02 (prompt injection)**: Lasso Security `claude-hooks` — the only injection defense found; PostToolUse scanner on `Read|WebFetch|Bash|Grep|Task` with 5 pattern categories (instruction-override, roleplay/DAN, encoding-obfuscation, context-manipulation, instruction-smuggling) and severity tiers. Weaknesses to improve: warn-only (never blocks), regex-only, no homoglyph/markdown-smuggling coverage, no measurable test corpus. We author our own pattern corpus from the category taxonomy.
- **Phase 03 (format + gates)**: claude-workflow-v2 `format-on-edit.py` (hardcoded file-type→formatter map — improve with project-aware detection from pyproject.toml/package.json), buildwithclaude `no-vibes` Stop hook (blocks "done" claims without same-turn verification evidence — adapt evidence definition to this repo's pipeline artifacts: implementation records, review records, QA docs), claudekit Stop-gates (typecheck/lint/test-project, check-todos, check-comment-replacement).
- **Phase 04 (skill enforcement)**: claude-code-infrastructure-showcase — `skill-rules.json` (globs/keywords → required skills, enforcement levels block/suggest/warn) + UserPromptSubmit suggestion-injection hook + PreToolUse guard blocking edits until required skills are activated + PostToolUse tracker clearing pending enforcement. Node/tsx + sqlite implementation, single-project — we rebuild in Python for this repo's 16+ skills and multi-harness propagation.
- **Hook-event reference**: shanraisshan `claude-code-hooks` — the most complete public catalog of all 30 Claude Code hook events and which fire in agent contexts; consult when choosing attachment points.

## Key Technical Facts Established

- PreToolUse hooks execute regardless of permission mode; a hook exiting 2 (or emitting a deny decision) blocks the tool call even under `--dangerously-skip-permissions`. This is the only reliable enforcement layer for goal 2.
- All nine surveyed repos are MIT-licensed; the clean-room constraint is the user's preference, not a legal necessity — but it stands regardless.
- Current repo hook wiring lives in `.claude/settings.json` with `$source`-tagged entries generated from `.github/hooks/*.json` definitions; existing hooks: `bash-safety` (PreToolUse), `protect-files` (PreToolUse), `audit-log` (PostToolUse), `done-notify` (Stop/Notification), plus code-review-graph update/status hooks.
- The repo's propagation mechanism is `scripts/propagate_master_assets.py` (regenerates Claude/OpenCode/Codex outputs from `.github/` source). New hooks must join this flow.
