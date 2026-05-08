# Phase 02 Discovery Context

Additional context gathered for Phase 02 beyond the repository itself.

## External Research Summary

The phase scope and technical assumptions for Codex support were informed by current Codex documentation and upstream Codex source behavior.

### Codex Instructions Model

- Codex discovers instructions from the global Codex home directory first, using `~/.codex/AGENTS.override.md` if present, otherwise `~/.codex/AGENTS.md`
- Codex then discovers project instruction files from the project root to the current working directory, preferring `AGENTS.override.md` over `AGENTS.md` at each level
- Additional fallback filenames can be configured via `project_doc_fallback_filenames` in `~/.codex/config.toml`
- For this repository's planned Codex port, AGENTS-derived source content should target the global Codex AGENTS layer rather than either repository's checked-in `AGENTS.md`

### Codex Custom Agents Model

- Codex custom agents are standalone TOML files, not markdown manifests
- User-scoped custom agents live under `~/.codex/agents/`
- Repo-scoped custom agents live under `.codex/agents/`
- Required fields are `name`, `description`, and `developer_instructions`
- Optional fields include model selection, sandbox settings, MCP server configuration, nicknames, and skill configuration

### Codex Skills Model

- Codex skills are directory-based assets containing a required `SKILL.md`
- Skills may also include optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`
- Repo-scoped skills are discovered from `.agents/skills` between repo root and current working directory
- User-scoped skills are discovered from `$HOME/.agents/skills`
- Codex supports symlinked skill folders, which makes a macOS symlink setup guide viable

### Verified macOS-Relevant Locations

- `~/.codex/config.toml`
- `~/.codex/AGENTS.md`
- `~/.codex/AGENTS.override.md`
- `~/.codex/agents/`
- `$HOME/.agents/skills/`

## Repository-Specific Context

- The repository already has a live hidden Codex config surface at `.codex/config.toml`
- The repository-owned `codex/` directory exists but is currently empty, making it the natural destination for Codex-specific planning docs and future source artifacts
- Existing multi-platform support already distinguishes a master source of truth in `.github/` from derived platform copies in `claude/` and `opencode/`
- Existing architecture and roadmap docs currently describe a three-platform model and will need explicit Codex-aware updates

## Sources Consulted

- OpenAI Codex documentation for AGENTS.md guidance discovery
- OpenAI Codex documentation for skills authoring and discovery
- OpenAI Codex documentation for subagents and custom agent configuration
- OpenAI Codex advanced configuration documentation for config and filesystem locations
- Upstream `openai/codex` repository excerpts confirming AGENTS discovery precedence, skill root scanning, and custom agent TOML loading behavior