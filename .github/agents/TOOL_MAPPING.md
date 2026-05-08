# Cross-Platform Tool Mapping

This document defines how tools are named and represented across the three agentic platforms: **GitHub Copilot**, **Claude Code**, and **OpenCode**.

## Tool Name Mapping

| GitHub Copilot | Claude Code | OpenCode | Purpose |
|---|---|---|---|
| `read` | `Read` | `permission.read` | Read files and directories |
| `search` | `Grep`, `Glob` | `permission.grep`, `permission.glob` | Search and find in files |
| `edit` | `Edit`, `Write` | `permission.edit`, `permission.write` | Modify and create files |
| `fetch` | `WebFetch` | `permission.web_fetch` | Fetch web content |
| `execute` | `Bash` | `permission.bash` | Execute shell commands |
| `agent` | `Agent` | (implicit) | Invoke subagents/other agents |
| `todo` | (N/A) | (N/A) | Manage TODO lists (GitHub Copilot only) |
| `web/*` | `WebFetch`, `WebScreenshot`, `WebSearch` | `permission.web_*` | Web-specific tools |

## Platform-Specific Details

### GitHub Copilot (`.github/agents/*.agent.md`)

**Tool List Format:** Array of lowercase strings
```yaml
tools: [read, search, edit, fetch, execute, agent, todo]
```

**Notes:**
- Lowercase names
- Array format `[tool1, tool2, ...]`
- Includes `todo` for TODO list management
- `web/fetch`, `web/screenshot`, `web/search` are available for web-specific agents
- Duplicates should be removed (they are configuration errors)

### Claude Code (`claude/agents/*.md`)

**Tool List Format:** Comma-separated PascalCase list
```yaml
tools: Read, Grep, Glob, Edit, Write, WebFetch, Bash, Agent
```

**Notes:**
- PascalCase names
- Comma-separated (not array)
- No `todo` equivalent
- Web tools: `WebFetch`, `WebScreenshot`, `WebSearch`
- Instructions are inlined in agent body (Claude does not support instruction file loading via `applyTo`)

### OpenCode (`opencode/agents/*.md`)

**Tool List Format:** Permission object structure
```yaml
permission:
  read: allow
  grep: allow
  edit: allow
  bash: allow
  web_fetch: allow
  agent: allow
```

**Notes:**
- Permission object with `permission:` prefix
- Lowercase snake_case names
- Boolean values (`allow` / not present = deny)
- No `todo` equivalent
- Web tools: `web_fetch`, `web_screenshot`, `web_search`
- Model specification required: `model: anthropic/claude-3-5-sonnet-20241022`

## Conversion Rules

### GitHub → Claude

1. Lowercase tools → PascalCase (except `agent` stays `Agent`)
   - `read` → `Read`
   - `search` → `Grep`, `Glob`
   - `edit` → `Edit`, `Write`
   - `fetch` → `WebFetch`
   - `execute` → `Bash`
2. Array format → comma-separated list
3. Remove `todo` (not supported)
4. Inline instructions from `.github/instructions/` directly into agent body
5. Remove `agents:` field (Claude references agents inline)

### GitHub → OpenCode

1. Lowercase tools → lowercase snake_case
   - `read` → `read`
   - `search` → `grep`, `glob`
   - `edit` → `edit`
   - `fetch` → `web_fetch`
   - `execute` → `bash`
2. Array format → permission object structure
3. Remove `todo` (not supported)
4. Add `model:` field with OpenCode-compatible model ID
5. Rename file to omit `.agent` suffix (keep `.md`)
6. Inline any tool-specific configuration

## Tool Capability Alignment

### Read-Only Agents

Read-only agents (planners, analyzers, auditors) should have:

```
GitHub:  [read, search, edit, fetch, agent]  (no execute)
Claude:  Read, Grep, Glob, Edit, WebFetch, Agent
OpenCode: read, grep, edit, web_fetch (no bash)
```

**Rationale:** These agents write deliverable documents and reports (`edit` allowed), but do not execute shell commands or modify source code.

### Implementation Agents

Implementation agents (implementer, reviewer, test-writer) should have:

```
GitHub:  [read, edit, search, execute, todo]  (or with agent for orchestrator roles)
Claude:  Read, Edit, Write, Bash, Grep, Glob
OpenCode: read, edit, bash, grep (no web_fetch unless needed)
```

**Rationale:** These agents write code, run tests, and execute build/test commands.

## Best Practices

1. **Avoid Duplicates:** Do not list the same tool twice in a single agent
2. **Minimal Toolset:** Only include tools the agent actually needs
3. **Document Mapping:** When converting an agent to a new platform, document the mapping in comments
4. **Test After Conversion:** Verify the agent's tool usage matches the intended capabilities
5. **Consistency:** Use this mapping as the source of truth when adding new agents

## Future Improvements

- Automated validation: Script to verify tool names are valid per platform
- Automated conversion: Tool to generate Claude/OpenCode agents from GitHub source
- Instruction templating: System to embed instructions from `.github/instructions/` into Claude agents automatically
