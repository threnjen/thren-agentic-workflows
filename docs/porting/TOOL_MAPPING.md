# Cross-Platform Tool Mapping

This document defines how tools are represented across GitHub Copilot source manifests, Claude agents, OpenCode agents, and Codex agents.

## Mapping Table

| GitHub Copilot | Claude | OpenCode | Codex | Purpose |
|---|---|---|---|---|
| `read` | `Read` | `permission.read` | Describe in `developer_instructions` | Read files and folders |
| `search` | `Grep`, `Glob` | `permission.grep`, `permission.glob` | Describe in `developer_instructions` | Search files |
| `edit` | `Edit`, `Write` | `permission.edit` | Describe in `developer_instructions` | Modify/create files |
| `fetch` | `WebFetch` | `permission.webfetch` | Describe in `developer_instructions` | Fetch web content |
| `execute` | `Bash` | `permission.bash` | Describe in `developer_instructions` | Execute shell commands |
| `agent` | `Agent` | `permission.task` | Describe in `developer_instructions` | spawn subagents |
| `todo` | No equivalent | `permission.todowrite` | Describe in `developer_instructions` | Manage todo/progress lists |

## Platform Notes

### GitHub Copilot

- Declared in `.github/agents/*` frontmatter `tools: [ ... ]`
- Lowercase tool names
- Supports `todo`

### Claude

- Declared in `claude/agents/*` frontmatter `tools: ...`
- PascalCase names
- No dedicated `todo` tool

### OpenCode

- Declared in `opencode/agents/*` frontmatter `permission:` object
- snake_case keys with `allow`
- Includes `task` and `todowrite` in this repository's convention

### Codex

- Agent files are TOML with required fields including `developer_instructions`
- Tool semantics are represented through instructions rather than a direct tool key table in this repository's current format

## Reference Guides

- `CLAUDE_PORTING_GUIDE.md`
- `OPENCODE_PORTING_GUIDE.md`
- `CODEX_PORTING_GUIDE.md`
