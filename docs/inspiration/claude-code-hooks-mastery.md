# claude-code-hooks-mastery (IndyDevDan / disler)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/claude-code-hooks-mastery`

## Overview

Well-known demonstration/teaching repo covering the **full Claude Code hook lifecycle** (13 events with JSON payloads) plus sub-agents, output styles, status lines, and custom commands. Mature and actively iterated (41KB README, extensive `ai_docs/` and `specs/`). Architecture: **Astral UV single-file Python scripts** (inline PEP-723 dependency blocks, run via `uv run`).

## Agents

- **meta-agent** — Generates a complete new sub-agent config file from a description (opus). The flagship.
- **work-completion-summary** — Concise TTS/audio summaries when work finishes (ElevenLabs MCP).
- **llm-ai-agents-and-eng-research** — Gathers latest LLM/AI-agent news (firecrawl + WebFetch).
- **hello-world-agent** — Trivial demo greeting agent.

## Skills

None (predates the Skills mechanism).

## Hooks

All Python UV single-file scripts in `.claude/hooks/`, wired in `settings.json`. Two are security-oriented; the rest logging/observability/TTS:

- **pre_tool_use.py** (PreToolUse) — **SECURITY**: blocks dangerous `rm -rf` variants (regex) and blocks any `.env` file access (allows `.env.sample`); exit 2 to deny. No external deps.
- **permission_request.py** (PermissionRequest) — **SECURITY-capable**: logs permission dialogs; can auto-allow/deny/modify tool input per policy.
- **user_prompt_submit.py** (UserPromptSubmit) — Logs prompts, stores last prompt, names the agent/session; optional prompt validation/blocking.
- **post_tool_use.py / post_tool_use_failure.py** — JSON logging of every tool call / failure.
- **notification.py, stop.py, subagent_start.py, subagent_stop.py** — TTS announcements (ElevenLabs > OpenAI > pyttsx3); stop.py can generate an LLM completion message.
- **pre_compact.py, session_start.py, session_end.py, setup.py** — Lifecycle logging; session_start can inject context.
- Shared utils: `utils/tts/` and `utils/llm/` backends.

## Other assets

- ~15 commands (`prime`, `plan`, `plan_w_team`, `build`, `cook`, crypto-research demos, etc.).
- 9 status-line versions; 8 output styles (yaml, table, tts-summary, genui, ultra-concise…).
- ElevenLabs MCP template; rich `ai_docs/` on hooks/subagents/status-lines.
- No plugin marketplace, no install script.

## Character

**General-purpose teaching toolset / reference kit** for developers learning the Claude Code extensibility surface. The crypto commands and sample apps are illustrative demos, not the point.

## Install verdict

**Cherry-pick, don't install wholesale.** Adoption is copy-paste; the default settings.json enables all 13 hooks, which log JSON on every event and invoke TTS/LLM subprocesses (noisy, slow, needs API keys + UV), and its permissions block is broad.

- **Worth copying:** `pre_tool_use.py` (`.env`-block + `rm -rf` guard — self-contained safety hook), `meta-agent`, output-style and status-line examples.
- **Skip:** the TTS/logging hook stack unless you want audio/observability.
