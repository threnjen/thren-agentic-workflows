# Agent Porting Guide: From GitHub to Claude & OpenCode

**Location:** `.github/agents/` → `claude/agents/` and `opencode/agents/`

This guide is for agents and developers porting agent definitions from the GitHub Copilot format (master source) to Claude Code and OpenCode formats. **Read this before porting or updating agents on other platforms.**

---

## Golden Rule: Claude Requires Inlined Instructions

**This is the most important thing you need to know.**

```
GitHub Copilot:  Instructions LOADED AUTOMATICALLY via applyTo patterns
        ↓
Claude Code:     Instructions MUST BE INLINED into agent body
        ↓
OpenCode:        Instructions encoded in permission/config objects
```

### What This Means

When you port an agent from `.github/agents/` to `claude/agents/`:

1. **Read the instructions** that apply to that agent (check `.github/instructions/`)
2. **Copy the relevant instruction content** into the Claude agent's body
3. **Do NOT expect** Claude to automatically load `.github/instructions/` files

**Why?** Claude platform does not have a native instruction-file system like GitHub Copilot does. Inlining is the only way to ensure the agent has the constraints it needs.

### How to Find Which Instructions Apply

Look at the instruction files in `.github/instructions/`:

```bash
grep "applyTo:" .github/instructions/*.md | grep "your-agent-name"
```

**Example:** For `audit-code-or-infra.agent.md`:

```bash
grep -l "audit-code-or-infra" .github/instructions/*.md
# Output:
# - challenge-assumptions.instructions.md (applyTo pattern)
# - read-only-agent.instructions.md (not applicable)
# - proactive-research.instructions.md (applyTo pattern)
```

Then read those instruction files and embed their content into the Claude agent.

---

## Platform Differences Checklist

### Frontmatter Format

| Aspect | GitHub Copilot | Claude Code | OpenCode |
|--------|---|---|---|
| **File Extension** | `.agent.md` | `.md` | `.md` |
| **name** | Display name, e.g., "01 Project - Planner" | Kebab-case, e.g., "01-project-planner" | Kebab-case, e.g., "01-project-planner" |
| **Tools Format** | Array: `[read, search, edit]` | List: `Read, Grep, Edit` | Object: `permission: { read: allow, grep: allow }` |
| **Tool Names** | Lowercase | PascalCase | snake_case |
| **Instructions** | Load via applyTo patterns | **Inline in body** ✅ | Inline in body |
| **Model** | (implicit) | (implicit) | Explicit: `model: anthropic/claude-...` |
| **agents Field** | Lists subagents | Remove field | (N/A) |

### Tool Name Mapping

When converting tools, map across platforms:

| GitHub | Claude | OpenCode | Purpose |
|---|---|---|---|
| `read` | `Read` | `read` | File reading |
| `search` | `Grep`, `Glob` | `grep`, `glob` | File searching |
| `edit` | `Edit`, `Write` | `edit` | File writing |
| `fetch` | `WebFetch` | `web_fetch` | Web fetching |
| `execute` | `Bash` | `bash` | Shell execution |
| `agent` | `Agent` | (implicit) | Subagent invocation |
| `todo` | (N/A) | (N/A) | NOT SUPPORTED on Claude/OpenCode |

**⚠️ Important:** `todo` tool is GitHub-only. Remove it when porting to Claude/OpenCode.

---

## Porting Workflow

### Step 1: Start with the GitHub Source

```bash
cat .github/agents/YOUR-AGENT-NAME.agent.md
```

**Master source.** All truth lives here.

### Step 2: Check Applicable Instructions

```bash
grep -l "YOUR-AGENT-NAME" .github/instructions/*.md
```

Example: `grep -l "project-planner" .github/instructions/*.md`

### Step 3: Read Instructions

```bash
cat .github/instructions/INSTRUCTION-NAME.instructions.md
```

Extract the content **below** the frontmatter. This will be inlined into Claude/OpenCode agents.

### Step 4: Convert Frontmatter

Use the checklist above to convert:
- GitHub: `tools: [read, search, edit, execute, agent]`
- Claude: `tools: Read, Grep, Glob, Edit, Write, Bash, Agent`
- OpenCode: `permission: { read: allow, grep: allow, edit: allow, bash: allow }`

### Step 5: Inline Instructions

For Claude and OpenCode, add a section after the description:

```markdown
---
name: YOUR-AGENT-NAME
description: "..."
tools: [...]
---

# Constraints & Instructions

[Paste relevant instruction content here]

---

# Main Content

[Rest of the agent definition...]
```

### Step 6: Remove Non-Portable Elements

- ❌ Remove `agents:` field (list of subagents) — Convert to inline agent references
- ❌ Remove `todo` tool — Not supported on Claude/OpenCode
- ❌ Remove GitHub-specific tool references (e.g., `web/screenshot`)

### Step 7: Test

- GitHub: `claude /agents` → List agents, verify presence
- Claude: `claude` + `/agents` → List agents, verify format
- OpenCode: `opencode` → Verify agent loads

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting to Inline Instructions

```yaml
# ❌ WRONG: Only copied frontmatter
---
name: 01-project-planner
description: "Creates project roadmaps"
tools: Read, Grep, Edit, Agent
---

[Missing: The actual constraints from .github/instructions/]
```

### ✅ Correct: Instructions Inlined

```yaml
---
name: 01-project-planner
description: "Creates project roadmaps"
tools: Read, Grep, Edit, Agent
---

# Constraints: Codebase Read-Only Policy

- ✅ Write planning documents to `docs/` and `dev/`
- ❌ Don't modify source code files
- ❌ Don't modify test files
[... rest of instruction content ...]

---

## Main Content

You are a planning specialist...
```

### ❌ Mistake 2: Keeping GitHub Tools

```yaml
# ❌ WRONG: GitHub-only `todo` tool
tools: Read, Grep, Edit, Todo, Agent
```

### ✅ Correct: Remove Unsupported Tools

```yaml
# ✅ CORRECT: todo removed (GitHub-only)
tools: Read, Grep, Edit, Agent
```

### ❌ Mistake 3: Forgetting Tool Name Conversion

```yaml
# ❌ WRONG: GitHub tool names in Claude agent
tools: read, search, edit, execute
```

### ✅ Correct: Platform-Specific Names

```yaml
# ✅ CORRECT: Claude PascalCase tool names
tools: Read, Grep, Edit, Bash
```

---

## Validation Checklist

Before committing a ported agent, verify:

- [ ] Frontmatter format matches target platform (GitHub/Claude/OpenCode)
- [ ] Tool names are converted correctly (GitHub lowercase → Claude PascalCase → OpenCode snake_case)
- [ ] Instructions from `.github/instructions/` are inlined (for Claude/OpenCode)
- [ ] `agents:` field removed (or converted to inline references)
- [ ] No GitHub-only tools (`todo`, platform-specific web tools)
- [ ] File naming matches convention (`.agent.md` for GitHub, `.md` for Claude/OpenCode)
- [ ] Agent loads in target platform without errors
- [ ] Content is identical to GitHub source (except platform adaptations)

---

## Quick Reference: GitHub → Claude Conversion

```bash
# Start with GitHub agent
cat .github/agents/01-project-planner.agent.md

# Find applicable instructions
grep -l "project-planner" .github/instructions/*.md

# Read instructions
cat .github/instructions/read-only-agent.instructions.md

# Create Claude version with inlined instructions
# 1. Copy frontmatter, convert tools format
# 2. Inline instruction content
# 3. Keep body content identical
# 4. Save to claude/agents/project-planner.md
```

---

## When Instructions Change

**⚠️ Maintenance Burden Alert**

If `.github/instructions/` files are updated:

1. Update the master agent in `.github/agents/YOUR-AGENT-NAME.agent.md` (GitHub auto-loads)
2. **Manually update** `claude/agents/YOUR-AGENT-NAME.md` with inlined content
3. **Manually update** `opencode/agents/YOUR-AGENT-NAME.md` with inlined content

**Future Improvement:** Automate this with a script (`scripts/generate-claude-agents.py`) that:
- Reads `.github/agents/` source
- Applies relevant `.github/instructions/` by applyTo pattern
- Generates synchronized Claude/OpenCode agent files

---

## Questions?

- **Why the duplication?** GitHub has native instruction loading; Claude doesn't. We inline to ensure agents have all constraints.
- **Can we automate this?** Yes! See "When Instructions Change" section. Contributions welcome.
- **What if I add a new instruction?** Update `.github/instructions/`, then manually sync affected Claude/OpenCode agents, or build the automation script.

**Golden Rule (again):** When porting to Claude, **always inline the instructions**. This is not optional.
