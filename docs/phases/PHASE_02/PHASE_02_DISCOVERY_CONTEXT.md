# Phase 02 Discovery Context

Context gathered during phase refinement (2026-07-14) beyond what the codebase itself records. Downstream agents (Feature - Decomposer, implementers) should consume this instead of re-researching.

## Verified Claude Code PostToolUse Platform Facts

Verified against current Claude Code hooks documentation (https://code.claude.com/docs/en/hooks.md and the Agent SDK hooks page) via research during refinement:

- **`{"decision": "block", "reason": …}` in PostToolUse suppresses the tool output from the model's context entirely.** The tool has already executed, but the model never sees the output — it receives only the hook's reason. This is what makes the phase's "hard-block on high-confidence" posture real rather than advisory.
- **`hookSpecificOutput.updatedToolOutput`** replaces the entire tool result with a hook-supplied string; **`hookSpecificOutput.additionalContext`** appends to the tool result without replacing it. Both are processed on exit code 0. These are the only output-modification mechanisms.
- **Tool coverage**: PostToolUse fires for all successful tool calls — built-ins (Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch), MCP tools (`mcp__<server>__<action>` matchers), and Task/subagent results. It does **not** fire for failed tool calls; a separate `PostToolUseFailure` event exists for those.
- **stdin payload**: `tool_name`, `tool_input`, `tool_output` (possibly truncated), a **`tool_output_truncated`** boolean, `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`; subagent-originated calls additionally carry `agent_id` and `agent_type`.
- **Permission modes**: hooks execute regardless of permission mode, including bypass permissions; `permission_mode` is informational context in the payload.
- **Subagents**: PostToolUse fires for subagent tool calls (identified via `agent_id`/`agent_type`).
- **Exit codes**: exit 0 → JSON output processed (decision, updatedToolOutput, additionalContext); non-zero → stderr shown to the model as an error and output-modification fields ignored.

Codex and OpenCode equivalents were **not** verified during refinement — that verification is deliberately the first step of the multi-harness parity deliverable.

## Inspiration Survey: Lasso Security claude-hooks

Survey summary lives at `docs/inspiration/claude-hooks.md`; a local checkout exists at `/Users/jennywadkins/github_repos/claude_skills/claude-hooks` (README + installer only in the checked-out copy). **Clean-room constraint applies: taxonomy and weaknesses below are the only things carried forward — no patterns or hook code are ever copied.**

### Category taxonomy (requirements input for our original corpus)

1. **Instruction Override** — "ignore previous instructions", "forget your training", "new system prompt:", fake system-prompt delimiters (`=== END SYSTEM PROMPT ===`).
2. **Role-Playing / persona hijack** — DAN-style jailbreaks, "pretend you are" / "act as", "bypass your restrictions", evil-twin framings.
3. **Encoding / Obfuscation** — base64-encoded instructions, hex escapes, leetspeak, homoglyphs (e.g., Cyrillic `а` for Latin `a`), zero-width/invisible Unicode.
4. **Context Manipulation** — fake Anthropic/admin/authority messages, fake `{"role": "system"}` JSON fragments, fabricated prior-conversation claims, system-prompt extraction attempts.
5. **Instruction Smuggling** — instructions hidden in HTML/code comments.

Severity model surveyed: high (definite injection) / medium (suspicious, legitimate uses possible) / low (weak signal, high FP risk). Tools it monitors: Read, WebFetch, Bash, Grep, Task, `mcp__*`.

### Weaknesses to beat (drives Phase 02 improvements)

- **Warn-only** — never blocks; our design hard-blocks `high` via output suppression.
- **Regex-only with no pre-normalization** — homoglyph/zero-width evasions defeat literal patterns; we normalize (NFKC + homoglyph folding + zero-width stripping) before matching.
- **No markdown-native smuggling coverage** — link titles, image alt text, reference-link definitions, HTML attributes in markdown; we add these.
- **No measurable test corpus** — pattern quality is anecdotal; we ship a positive/negative benchmark harness with a zero-FP bar for `high` rules.
- Very new single-vendor repo (2 commits); patterns are FP-prone.

## Refinement Decisions (user-confirmed 2026-07-14)

1. **High-confidence response = full suppression** (`decision: block`), not span redaction. Medium/low warn-and-continue via `additionalContext`.
2. **WebFetch exfiltration guarding is in scope** for Phase 02 (satisfying the must-consider item in `.github/learnings/cross-phase-decisions.md`): PreToolUse URL-payload rules plus extension of the Phase 01 bash `curl`/`wget` exfil rules.
3. **Full multi-harness parity (Codex + OpenCode) is in scope**, structured as an investigation gate: verify each harness's output-interception contract, then either implement equivalent enforcement or document an evidence-backed platform limitation with explicit user sign-off. Cursor/Copilot remain Not supported. This decision upgraded phase complexity Medium → Large.
