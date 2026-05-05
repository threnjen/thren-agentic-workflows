# Codebase Context

Quick-reference for AI agents working on this repository.

## What This Repo Is

- A **template repository** of `AGENTS.md`, style guide files, and VS Code Copilot agent definitions
- Contains **no runnable code** — only Markdown documentation
- Two language variants for templates: Node.js/TypeScript and Python
- 24 agent definitions in `.github/agents/` (13 user-facing, 11 hidden subagents)
- 11 skills in `.github/skills/` (7 directory-based shared templates + 4 standalone graph-tool workflow skills)
- 11 instruction files in `.github/instructions/` (cross-cutting conventions)
- Users copy files into their own projects and customize them

## Folder Structure

```
AGENTS.md                       # Code-review-graph MCP tools for this repo
README.md                       # Repo overview, usage instructions
.github/
  agents/
    README.md                   # Agent documentation, pipelines, and usage guide
    *.agent.md                  # 24 agent definition files (13 user-facing, 11 hidden)
  skills/
    phase-document-writing/     # Phase Doc & Overview templates, quality checklist
      SKILL.md
    auditor-conventions/        # Audit constraints, deliverables, file-type taxonomy, report format
      SKILL.md
    feature-plan-set/           # Three-file plan convention, sections A–F, stage format
      SKILL.md
    implementation-pipeline-loop/ # Implement → Review → Commit → Mark Complete loop
      SKILL.md
    implementation-record/      # Implementation record artifact template
      SKILL.md
    unity-development/          # Unity C# implementation and review rules
      SKILL.md
    unity-review-knowledge/     # Unity best practices from 11 official ebooks
      SKILL.md
    debug-issue.md              # Graph-powered debug workflow skill
    explore-codebase.md         # Graph-powered codebase navigation skill
    refactor-safely.md          # Graph-powered safe refactoring skill
    review-changes.md           # Graph-powered structured code review skill
  instructions/
    codebase-context-bootstrap.instructions.md  # Reads CODEBASE_CONTEXT.md before discovery (all agents)
    dev-task-folder.instructions.md     # dev/feature/ output naming conventions (all agents)
    documentation-freshness-check.instructions.md  # Checks for README.md/CODEBASE_CONTEXT.md (planner, refiner)
    challenge-assumptions.instructions.md  # Push back on breaking patterns (planner, refiner)
    orchestrator-conventions.instructions.md  # Shared orchestrator constraints (3 orchestrators)
    proactive-research.instructions.md  # @Web Researcher for unfamiliar tech (planner, refiner, debugger)
    read-only-agent.instructions.md     # No-modification constraints (9 agents)
    learnings-bootstrap.instructions.md  # Read .github/learnings/*.md (implementer, reviewer, decomposer, debugger)
    tech-stack-detection.instructions.md # Detect and load matching skills (implementer, reviewer)
    subagent-autonomy.instructions.md   # No questions, sensible defaults (implementer, reviewer, plan-expander, git-commit)
    output-verbosity-policy.instructions.md # Soft-target concision defaults (all agents)
docs/
  AGENT_REGRESSION_BENCHMARK_SPEC.md # Benchmark design spec for agent changes
  ARCHITECTURE.md               # Structure diagram and design decisions
  CODEBASE_CONTEXT.md           # This file
  UNDERSTANDING_AGENTIC_ECOSYSTEM.md # Agentic AI terminology explainer
  benchmarks/
    B001/                       # First benchmark pack (tasks, tools, graders, runs)
opencode/
  agents/                       # Derived agent copies for OpenCode platform
  SYMLINK_SETUP.md              # Symlink setup for skills/
claude/
  agents/                       # Derived agent copies for Claude Code platform
  skills/                       # Symlinked to .github/skills/
  README.md                     # Claude-specific setup
nodejs/
  AGENTS.md                     # GitHub Copilot instructions for Node.js/TS projects
  docs/
    STYLE_GUIDE.md              # Node.js/TS coding conventions (loaded on demand)
python/
  AGENTS.md                     # GitHub Copilot instructions for Python projects
  docs/
    STYLE_GUIDE.md              # Python coding conventions (loaded on demand)
dev/
  feature/                      # Pipeline subagent output (plans, reviews, QA)
  research/                     # Web researcher output
```

## Key Facts

### Templates (nodejs/, python/)

- Each `AGENTS.md` contains an "Extended Guides" section pointing to `docs/STYLE_GUIDE.md`
- The two AGENTS.md files share ~70% identical content (principles, process, testing, quality, agent ops)
- Shared guidance is intentionally compacted into concise sections to reduce token usage while preserving critical constraints
- Language-specific differences: dependency tooling, property-based testing library, data modeling, style preferences
- No shared base file — each AGENTS.md is fully self-contained by design
- Style guides are intentionally separate from AGENTS.md to save agent context window space

### Agent Definitions (.github/agents/)

- **4 orchestrators** (user-facing): Phase - Execute, Audit - Code/Infra/Refactor, Test - Orchestrator, Agent Testing Agent
- **9 standalone user-facing**: Planner, Refiner, Decomposer, Eval Grader, Debugger, Docs Writer, Prod Code Review, Web Researcher, Unity Reviewer
- **11 hidden subagents** (`user-invocable: false`): Agent Test Runner, Plan Expander, Implementer, Reviewer, QA Writer, 3 Auditors, Test Analyst/Writer/Fixer
- See [agents/README.md](../.github/agents/README.md) for detailed descriptions and invocation patterns.

### Skills (.github/skills/)

11 skills loaded by agents on demand (7 directory-based shared templates + 4 standalone graph-tool workflow skills). See [ARCHITECTURE.md](ARCHITECTURE.md#skills) for the full mapping.

### Instructions (.github/instructions/)

11 instruction files with `applyTo` glob matching. See [ARCHITECTURE.md](ARCHITECTURE.md#instructions) for the full mapping.

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
- Agent files use YAML frontmatter with `name`, `description`, `tools`, and optionally `agents` and `user-invocable`
- Checklist items use `- [ ]` syntax
- Tables use pipe-delimited Markdown format

## When Editing

- **Adding a new section to both languages**: Update both `nodejs/AGENTS.md` and `python/AGENTS.md` to keep the shared structure in sync
- **Changing language-specific content**: Only edit the relevant language folder
- **Adding a new language**: Create a new top-level folder (e.g., `go/`) with the same `AGENTS.md` + `docs/STYLE_GUIDE.md` structure
- **Adding/removing an agent**: Update the agent file in `.github/agents/` AND update `.github/agents/README.md` to keep tables, descriptions, and pipelines current
- **Adding a new orchestrator**: Add the orchestrator file, add its subagents (with `user-invocable: false`), and update the README agent tables
- **Changing a shared template or format**: Edit the corresponding skill in `.github/skills/` — do NOT re-inline the content in agent files
- **Adding a new skill**: Create `.github/skills/<name>/SKILL.md` (or `<name>.md` for standalone skills) with YAML frontmatter (`name`, `description`). Update agent files to reference it. Update ARCHITECTURE.md and this file.
- **Adding a new instruction**: Create `.github/instructions/<name>.instructions.md` with `applyTo` glob. Update ARCHITECTURE.md and this file.
- **Updating README.md**: Keep the structure tree, usage instructions, and comparison table current

## Do Not

- Do not add runnable code, build scripts, or CI/CD configuration — this is a docs-only repo
- Do not create a shared base file and use includes/inheritance — each AGENTS.md must be independently copyable
- Do not add deployment or infrastructure documentation
- Do not reference specific project names or URLs in the templates — they must be generic
- Do not merge the style guide into AGENTS.md — the separation is intentional for context window efficiency
- Do not set `user-invocable: true` on subagents — they are hidden by design and invoked only by orchestrators
