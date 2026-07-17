# Claude Agents

Agents for Claude Code platform, converted from the `.github/agents/` master source.

---

## ⚠️ CRITICAL: Instructions Are Inlined

**Claude does NOT automatically load instruction files like GitHub Copilot does.**

When you work with these agents or create new ones:

1. **Instructions must be embedded directly in the agent body**
2. Check `.github/instructions/` for applicable constraints
3. Inline the relevant instruction content into the agent markdown

**Example:** If porting `audit-code-or-infra.agent.md` to Claude:

```yaml
---
name: audit-code-or-infra
description: "Audits code or infrastructure..."
tools: Read, Grep, Edit, WebFetch
---

# Constraints: Read-Only Agent Policy

[Paste content from .github/instructions/read-only-agent.instructions.md here]

# Constraints: Proactive Research

[Paste content from .github/instructions/proactive-research.instructions.md here]

---

## Main Content

You are an auditor...
```

**Do NOT expect** Claude to automatically load `.github/instructions/`. It won't.

---

## Porting Process

See [claude/CLAUDE_PORTING_GUIDE.md](../CLAUDE_PORTING_GUIDE.md) for complete instructions on:
- How to identify which instructions apply
- Tool name mapping across platforms
- Common mistakes to avoid
- Validation checklist

**TL;DR:** 
1. Read GitHub source at `.github/agents/YOUR-AGENT.agent.md`
2. Find applicable instructions: `grep -l "your-agent" .github/instructions/*.md`
3. Inline those instructions into the Claude version
4. Convert tool names (GitHub lowercase → Claude PascalCase)
5. Remove `todo` tool (GitHub-only)
6. Save as `claude/agents/YOUR-AGENT.md`

---

## Setup

Run repository propagation to a fixed point, resolve and review the active Claude destination inventory, then invoke `deploy_managed_copies_after_convergence`. Verify regular-copy freshness, roster coverage, collision outcomes, and discovery from a fresh Claude session.

See [../SYMLINK_SETUP.md](../SYMLINK_SETUP.md) for details; its legacy filename is retained for compatibility.

---

## Agent Naming Convention

Claude agents use `z-` prefix for subagents (e.g., `z-feature-implementer`) to distinguish them from user-invocable orchestrators (e.g., `project-planner`, `phase-refiner`).

This differs from GitHub (`04b-feature-implementer`) and OpenCode (same as GitHub). Document your agent references with platform context.

---

## Skills and Learnings

- **Skills:** Generated from `.github/skills/` (shared source across platforms)
- **Learnings:** Generated from `.github/learnings/` (shared source across platforms)

To update them, modify the source in `.github/` and rerun propagation.

---

## Platform Differences

For tool name mapping and frontmatter format differences, see:
- [docs/porting/TOOL_MAPPING.md](../../docs/porting/TOOL_MAPPING.md) — Cross-platform tool reference
- [claude/INSTRUCTION_ARCHITECTURE.md](../INSTRUCTION_ARCHITECTURE.md) — Why instructions are inlined

---

## Troubleshooting

**Q: My agent isn't loading**
- Check symlinks: `ls -la ~/.claude/agents`
- Verify agent frontmatter is valid YAML
- Ensure instructions are properly inlined (not referencing external files)

**Q: Agent can't find instructions**
- Verify they're inlined in the agent body (not in separate files)
- Check that instruction content is pasted correctly

**Q: Tool definitions are wrong**
- Use [docs/porting/TOOL_MAPPING.md](../../docs/porting/TOOL_MAPPING.md) to verify correct names
- Remember: Claude uses PascalCase (`Read`, `Bash`), not lowercase (`read`, `execute`)

---

## Contributing

When adding or updating agents:

1. Update the master source at `.github/agents/`
2. Sync changes to `claude/agents/` **with inlined instructions**
3. Sync changes to `opencode/agents/` (different format)
4. Update this README if the process changes

See [claude/CLAUDE_PORTING_GUIDE.md](../CLAUDE_PORTING_GUIDE.md) for full process.
