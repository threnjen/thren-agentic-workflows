# Codebase Context

Quick-reference for AI agents working on this repository.

## What This Repo Is

- A **template repository** of `AGENTS.md`, style guide files, and VS Code Copilot agent definitions
- Contains **no runnable code** — only Markdown documentation
- Two language variants for templates: Node.js/TypeScript and Python
- 19 agent definitions in `.github/agents/` (9 user-facing, 10 hidden subagents)
- 4 skills in `.github/skills/` (shared templates and patterns extracted from agents)
- 5 instruction files in `.github/instructions/` (cross-cutting conventions)
- Users copy files into their own projects and customize them

## Folder Structure

```
README.md                       # Repo overview, usage instructions
.github/
  agents/
    README.md                   # Agent documentation, pipelines, and usage guide
    *.agent.md                  # 19 agent definition files
  skills/
    phase-document-writing/     # Phase Doc & Overview templates, quality checklist
      SKILL.md
    auditor-conventions/        # Merged auditor skill: constraints, deliverables, file-type taxonomy, report format, severity levels
      SKILL.md
    feature-plan-set/           # Three-file plan convention, sections A–F, stage format
      SKILL.md
    implementation-pipeline-loop/ # Standard Implement → Review → Commit → Mark Complete loop + post-loop Docs Writer step
      SKILL.md
  instructions/
    codebase-context-bootstrap.instructions.md  # Reads CODEBASE_CONTEXT.md before discovery (applies to all agents)
    dev-task-folder.instructions.md     # dev/feature/[task-name]/ naming convention (applies to all agents)
    documentation-freshness-check.instructions.md  # Checks for README.md and CODEBASE_CONTEXT.md, recommends @Docs Writer (applies to planner, refiner)
    orchestrator-conventions.instructions.md  # Shared orchestrator constraints, branch creation, reporting (applies to 3 orchestrators)
    read-only-agent.instructions.md     # No-modification, no code blocks, no code-level details, approval constraints (applies to 8 agents)
docs/
  ARCHITECTURE.md               # Structure diagram and design decisions
  CODEBASE_CONTEXT.md           # This file
nodejs/
  AGENTS.md                     # GitHub Copilot instructions for Node.js/TS projects
  docs/
    STYLE_GUIDE.md              # Node.js/TS coding conventions (loaded on demand)
python/
  AGENTS.md                     # GitHub Copilot instructions for Python projects
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
- Docs Writer is dual-use: standalone user-facing agent AND invoked as a subagent by all three orchestrators at the end of the pipeline to update stale documentation
- 01 Project - Planner and 02 Phase - Refiner check for missing critical docs (`README.md`, `docs/CODEBASE_CONTEXT.md`) during discovery and recommend running the Docs Writer before proceeding
- All agents use `model: "Claude Opus 4 (Copilot)"` except Docs Writer (no model specified)
- Orchestrators list their subagents in the `agents:` frontmatter field

### Skills (.github/skills/)

- Each skill is a `SKILL.md` file in its own named subdirectory
- Skills have YAML frontmatter with `name` and `description`
- Agents load skills by name at runtime — skills are not auto-loaded
- Skills contain templates and formats that would otherwise be duplicated across agents
- `phase-document-writing` — Phase Document Template + Phases Overview Template + quality checklist (used by Planner, Refiner)
- `auditor-conventions` — Merged auditor skill: standard constraints, deliverables, file-type taxonomy, scope determination, process flow, report format, severity levels (used by all 3 Auditors)
- `feature-plan-set` — Three-file plan convention, sections A–F, stage format, decomposition rules (used by Decomposer)
- `implementation-pipeline-loop` — Standard development cycle (Implement → Review → Commit → Mark Complete) with prompt templates, error handling, and post-loop Docs Writer step (referenced by all 3 orchestrators)

### Instructions (.github/instructions/)

- Instruction files use `.instructions.md` extension with YAML frontmatter
- The `applyTo` field is a glob pattern — matching agents receive the instruction automatically
- `codebase-context-bootstrap.instructions.md` — Reads `docs/CODEBASE_CONTEXT.md` before discovery to reduce redundant scanning; applies to `.github/agents/**`
- `dev-task-folder.instructions.md` — Standardizes `dev/feature/[task-name]/` naming; applies to `.github/agents/**`
- `documentation-freshness-check.instructions.md` — Checks for `README.md` and `docs/CODEBASE_CONTEXT.md`, recommends `@Docs Writer` if missing; applies to project-planner, phase-refiner
- `orchestrator-conventions.instructions.md` — Common constraints, branch creation, progress tracking, output verification, pipeline discipline, review reject loop, reporting template; applies to 3 orchestrators
- `read-only-agent.instructions.md` — No codebase modification, no code blocks, no code-level details, approval-before-writing; applies to 8 read-only agents (with subagent exception)

## File Relationships

- `nodejs/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- `python/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- No cross-references between `nodejs/` and `python/` — they are independent
- `.github/agents/README.md` documents all agents — keep it in sync when adding/removing agents
- Orchestrator agent files reference their subagents by name in YAML `agents:` field
- Agents reference skills by name in their instructions (e.g., "Load the `phase-document-writing` skill")
- Skills are single-source-of-truth — agents do NOT duplicate skill content inline
- `codebase-context-bootstrap.instructions.md` auto-loads into all agents and directs them to read `docs/CODEBASE_CONTEXT.md` (if it exists) before starting discovery
- Instruction files auto-load into agents matching their `applyTo` glob pattern

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
- **Changing a shared template or format**: Edit the corresponding skill in `.github/skills/` — do NOT re-inline the content in agent files
- **Adding a new skill**: Create `.github/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`). Update agent files to reference it. Update ARCHITECTURE.md and this file.
- **Adding a new instruction**: Create `.github/instructions/<name>.instructions.md` with `applyTo` glob. Update ARCHITECTURE.md and this file.
- **Updating README.md**: Keep the structure tree, usage instructions, and comparison table current

## Do Not

- Do not add runnable code, build scripts, or CI/CD configuration — this is a docs-only repo
- Do not create a shared base file and use includes/inheritance — each AGENTS.md must be independently copyable
- Do not add deployment or infrastructure documentation
- Do not reference specific project names or URLs in the templates — they must be generic
- Do not merge the style guide into AGENTS.md — the separation is intentional for context window efficiency
- Do not set `user-invocable: true` on subagents — they are hidden by design and invoked only by orchestrators
