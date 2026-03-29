# Codebase Context

Quick-reference for AI agents working on this repository.

## What This Repo Is

- A **template repository** of `AGENTS.md`, style guide files, and VS Code Copilot agent definitions
- Contains **no runnable code** — only Markdown documentation
- Two language variants for templates: Node.js/TypeScript and Python
- 19 agent definitions in `.github/agents/` (9 user-facing, 10 hidden subagents)
- Users copy files into their own projects and customize them

## Folder Structure

```
README.md                       # Repo overview, usage instructions
.github/
  agents/
    README.md                   # Agent documentation, pipelines, and usage guide
    *.agent.md                  # 19 agent definition files
docs/
  ARCHITECTURE.md               # Structure diagram and design decisions
  CODEBASE_CONTEXT.md           # This file
nodejs/
  AGENTS.md                     # Claude Code instructions for Node.js/TS projects
  docs/
    STYLE_GUIDE.md              # Node.js/TS coding conventions (loaded on demand)
python/
  AGENTS.md                     # Claude Code instructions for Python projects
  docs/
    STYLE_GUIDE.md              # Python coding conventions (loaded on demand)
```

## Key Facts

### Templates (nodejs/, python/)

- Each `AGENTS.md` contains an "Extended Guides" section pointing to `docs/STYLE_GUIDE.md`
- The two AGENTS.md files share ~70% identical content (principles, process, testing, quality, agent ops)
- Language-specific differences: dependency tooling, property-based testing library, data modeling, style preferences
- No shared base file — each AGENTS.md is fully self-contained by design
- Style guides are intentionally separate from AGENTS.md to save agent context window space

### Agent Definitions (.github/agents/)

- All agent files use `.agent.md` extension with YAML frontmatter
- **3 orchestrators** (user-facing): 03 Phase - Execute, Audit - Code, Infra, Refactor, Test - Orchestrator
- **6 standalone user-facing agents**: 01 Project - Planner, 02 Phase - Refiner, Debugger, Docs Writer, Prod Code Review, Web Researcher
- **10 hidden subagents** (`user-invocable: false`): Feature - Decomposer, Feature - Implementer, Feature - Reviewer, Feature - QA Writer, Auditor - Code, Auditor - Infra, Auditor - Refactor, Test - Analyst, Test - Writer, Test - Fixer
- Feature - Implementer and Feature - Reviewer are shared across all three orchestrators
- All agents use `model: "Claude Opus 4 (Copilot)"` except Docs Writer (no model specified)
- Orchestrators list their subagents in the `agents:` frontmatter field

## File Relationships

- `nodejs/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- `python/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- No cross-references between `nodejs/` and `python/` — they are independent
- `.github/agents/README.md` documents all agents — keep it in sync when adding/removing agents
- Orchestrator agent files reference their subagents by name in YAML `agents:` field

## Conventions

- All files are Markdown (`.md`)
- AGENTS.md uses H2 (`##`) for top-level sections, H3 (`###`) for subsections
- Style guides use H2 for the language header, H3 for topics
- Agent files use YAML frontmatter with `name`, `description`, `tools`, `model`, and optionally `agents` and `user-invocable`
- Checklist items use `- [ ]` syntax
- Tables use pipe-delimited Markdown format

## When Editing

- **Adding a new section to both languages**: Update both `nodejs/AGENTS.md` and `python/AGENTS.md` to keep the shared structure in sync
- **Changing language-specific content**: Only edit the relevant language folder
- **Adding a new language**: Create a new top-level folder (e.g., `go/`) with the same `AGENTS.md` + `docs/STYLE_GUIDE.md` structure
- **Adding/removing an agent**: Update the agent file in `.github/agents/` AND update `.github/agents/README.md` to keep tables, descriptions, and pipelines current
- **Adding a new orchestrator**: Add the orchestrator file, add its subagents (with `user-invocable: false`), and update the README agent tables
- **Updating README.md**: Keep the structure tree, usage instructions, and comparison table current

## Do Not

- Do not add runnable code, build scripts, or CI/CD configuration — this is a docs-only repo
- Do not create a shared base file and use includes/inheritance — each AGENTS.md must be independently copyable
- Do not add deployment or infrastructure documentation
- Do not reference specific project names or URLs in the templates — they must be generic
- Do not merge the style guide into AGENTS.md — the separation is intentional for context window efficiency
- Do not set `user-invocable: true` on subagents — they are hidden by design and invoked only by orchestrators
