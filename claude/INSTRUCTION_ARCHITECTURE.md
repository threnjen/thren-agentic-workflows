# Claude Platform Architectural Notes

## How Instructions Work Across Platforms

### GitHub Copilot (`.github/instructions/*.instructions.md`)

GitHub Copilot has a native **instruction loading system**:

1. Instruction files use `applyTo:` glob patterns to automatically apply to matching agents
2. Instructions are **loaded by the platform** based on filename patterns
3. Agents don't need to know about instructions — they're injected by the platform
4. When instructions are updated, all matching agents automatically use the new version

**Example:** `read-only-agent.instructions.md` has:
```yaml
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,..."
```

All agents matching this pattern automatically receive the read-only constraints.

**Status:** ✅ Native platform support

### Claude Code (`.github/instructions/` — NOT directly supported)

Claude Code does **NOT** have a native instruction-file loading system comparable to GitHub Copilot.

**Current State:**
- Claude agents **do not** automatically load `.github/instructions/` files via `applyTo:` patterns
- Instructions **must be inlined directly into agent bodies** as static text
- When `.github/instructions/` are updated, Claude agent files must be manually updated
- No dynamic instruction loading from external files

**Current Approach in This Repo:**
- Many Claude agents inline instruction content directly in their markdown body
- Example: [claude/agents/audit-code-infra-refactor.md](claude/agents/audit-code-infra-refactor.md) inlines the "challenge-assumptions" and "read-only-agent" instructions

**Maintenance Burden:**
- Instruction changes require manual updates to multiple Claude agent files
- Risk of drift: Claude agents may have stale instruction versions

**Possible Solutions (Future):**
1. **Instruction Templating:** Build a script that generates Claude agents by:
   - Reading source from `.github/agents/*.agent.md`
   - Reading relevant `.github/instructions/*.md`
   - Combining them into final Claude agent `.md` files
   - Run on each commit to keep Claude agents in sync

2. **Custom MCP Server:** Create an MCP (Model Context Protocol) server that:
   - Exposes instruction file content as a custom tool
   - Claude agents invoke this tool to dynamically load instructions
   - Eliminates inlining and keeps source-of-truth in `.github/instructions/`

3. **Anthropic API Enhancement:** Request native instruction-file support from Anthropic (comparable to GitHub's `applyTo:` system)

**Status:** ❌ Not currently supported — instructions must be inlined

### OpenCode

OpenCode does **NOT** use instruction files. Instead:

- Permission model is declarative: `permission: { read: allow, edit: allow, ... }`
- Constraints are encoded in YAML frontmatter, not external instruction files
- No `applyTo:` system
- All instructions must be written directly in agent bodies

**Status:** ❌ External instruction files not supported

---

## Why Instruction Inlining in Claude Is Necessary

The current architecture inlines instructions in Claude agents because:

1. **Platform Limitation:** Claude does not natively support instruction-file loading
2. **Completeness:** All constraints must be conveyed to the agent
3. **Discoverability:** Agents are self-contained — no external file dependencies
4. **API Compatibility:** Works with Claude API directly without custom tooling

This is **not a design choice** but a **platform requirement**.

---

## Recommendation: Instruction Templating Script

To reduce maintenance burden, create an `./scripts/generate-claude-agents.py` that:

1. Reads `.github/agents/*.agent.md` (source of truth)
2. Parses `applyTo:` patterns from `.github/instructions/*.md`
3. For each agent, determines which instructions apply
4. Embeds applicable instructions into the agent body
5. Writes the final output to `claude/agents/*.md`
6. Commit with message: "chore: sync claude agents from source-of-truth"

**Benefits:**
- Single source of truth: `.github/` is master
- Automatic sync: Keep `claude/` agents in sync on each build
- Less manual work: No hand-editing Claude agents
- Reduced drift: Instructions in Claude are always current

**When to Run:**
- On pre-commit hook (in CI/CD)
- After any changes to `.github/agents/` or `.github/instructions/`
- On-demand: `./scripts/generate-claude-agents.py`

---

## Current Status

| Platform | Instruction Support | Current Approach |
|---|---|---|
| GitHub Copilot | ✅ Native `applyTo:` loading | Centralized instructions |
| Claude Code | ❌ Not supported | Inlined instructions (manual maintenance) |
| OpenCode | ❌ Not supported | Permission objects in YAML |

The inlining approach is necessary and correct for Claude, but should be **automated** to prevent drift.
