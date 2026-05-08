# Codebase Context

Quick-reference for AI agents working on this repository.

## What This Repo Is

- A **template repository** of `AGENTS.md`, style guide files, and VS Code Copilot agent definitions
- Contains **no runnable code** — only Markdown documentation
- Two language variants for templates: Node.js/TypeScript and Python
- Four platform surfaces are documented: `.github/` as the master source, checked-in `opencode/` and `claude/` copies, and a repository-owned `codex/` area for Codex docs and future source artifacts
- 24 agent definitions in `.github/agents/` (14 user-facing, 10 hidden subagents)
- 12 skills in `.github/skills/` (all directory-based, each with `SKILL.md`)
- 13 instruction files in `.github/instructions/` (cross-cutting conventions)
- Users copy files into their own projects and customize them

## Folder Structure

```
AGENTS.md                       # Code-review-graph MCP tools for this repo
README.md                       # Repo overview, usage instructions
.codex/
  config.toml                   # Existing runtime Codex config surface; not the repo-owned authoring area
.github/
  agents/
    README.md                   # Agent documentation, pipelines, and usage guide
    *.agent.md                  # 24 agent definition files (14 user-facing, 10 hidden)
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
    context7-mcp/               # Context7 documentation lookup workflow
      SKILL.md
    unity-development/          # Unity C# implementation and review rules
      SKILL.md
    unity-review-knowledge/     # Unity best practices from 11 official ebooks
      SKILL.md
    debug-issue/                # Graph-powered debug workflow skill
      SKILL.md
    explore-codebase/           # Graph-powered codebase navigation skill
      SKILL.md
    refactor-safely/            # Graph-powered safe refactoring skill
      SKILL.md
    review-changes/             # Graph-powered structured code review skill
      SKILL.md
  instructions/
    codebase-context-bootstrap.instructions.md  # Reads CODEBASE_CONTEXT.md before discovery (all agents)
    dev-task-folder.instructions.md     # dev/feature/ output naming conventions (all agents)
    documentation-freshness-check.instructions.md  # Checks for README.md/CODEBASE_CONTEXT.md (planner, refiner)
    challenge-assumptions.instructions.md  # Push back on breaking patterns (planner, refiner)
    graph-rebuild-hook.instructions.md  # Triggers graph rebuild at end of orchestrator pipelines (3 orchestrators)
    orchestrator-conventions.instructions.md  # Shared orchestrator constraints (3 orchestrators)
    proactive-research.instructions.md  # @Web Researcher for unfamiliar tech (planner, refiner, debugger)
    read-only-agent.instructions.md     # No-modification constraints (9 agents)
    learnings-bootstrap.instructions.md  # Read .github/learnings/*.md (implementer, reviewer, decomposer, debugger)
    tech-stack-detection.instructions.md # Detect and load matching skills (implementer, reviewer)
    subagent-autonomy.instructions.md   # No questions, sensible defaults (implementer, reviewer, plan-expander, git-commit)
    output-verbosity-policy.instructions.md # Soft-target concision defaults (all agents)
    csharp-style.instructions.md        # C# (Google) style rules — naming, formatting, idioms (unity-reviewer, auditor-code, implementer, reviewer)
docs/
  ARCHITECTURE.md               # Structure diagram and design decisions
  CODEBASE_CONTEXT.md           # This file
  UNDERSTANDING_AGENTIC_ECOSYSTEM.md # Agentic AI terminology explainer
  agentic-evaluator-plan.md     # Evaluator architecture and scoring plan
  porting/                      # Cross-platform porting docs and tool mapping
    README.md
    TOOL_MAPPING.md
codex/
  README.md                     # Repository-owned Codex layout contract and landing area for Codex docs/source artifacts
  CODEX_PLATFORM_REFERENCE.md  # Verified Codex platform model: discovery paths, agent formats, skill structure, runtime vs repo-owned separation
  CODEX_PORTING_GUIDE.md        # Strategy for porting .github/ agent content to Codex-native formats; includes conversion table and open questions
  MACOS_SETUP_AND_SYMLINKS.md   # macOS install paths, symlink setup, and verified Codex path behavior
  PILOT_SLICE_PLAN.md           # Pilot trio definition (one instruction slice, one custom agent, one skill) and exit criteria gating full Codex parity
opencode/
  agents/                       # Derived agent copies for OpenCode platform
  SYMLINK_SETUP.md              # Symlink setup for skills/
claude/
  agents/                       # Derived agent copies for Claude Code platform
  skills/                       # Symlinked to .github/skills/
  README.md                     # Claude-specific setup
eval/
  EVAL_SYSTEM_USAGE.md          # Eval runbook and grader usage
  PHASE_EVAL_RUN_CONFIG.example.yaml # Eval run configuration template
  hooks/                        # Post-commit hook template and related evaluation hooks
  rubrics/                      # Seed grader rubrics and schema-aligned example YAML files
  runs/                         # Evaluation run outputs and ledgers
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

- **3 orchestrators** (user-facing): Phase - Execute, Audit - Code/Infra/Refactor, Test - Orchestrator
- **11 standalone user-facing**: Planner, Refiner, Decomposer, Single Feature Agent, Eval Grader, Evangelize, Debugger, Docs Writer, Prod Code Review, Web Researcher, Unity Reviewer
- **10 hidden subagents** (`user-invocable: false`): Plan Expander, Implementer, Reviewer, QA Writer, 3 Auditors, Test Analyst/Writer/Fixer
- See [agents/README.md](../.github/agents/README.md) for detailed descriptions and invocation patterns.

### Skills (.github/skills/)

12 skills loaded by agents on demand (all directory-based). See [ARCHITECTURE.md](ARCHITECTURE.md#skills) for the full mapping.

### Instructions (.github/instructions/)

13 instruction files with `applyTo` glob matching. See [ARCHITECTURE.md](ARCHITECTURE.md#instructions) for the full mapping.

## File Relationships

- `nodejs/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- `python/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- No cross-references between `nodejs/` and `python/` — they are independent
- `codex/README.md` defines what belongs in the repository-owned Codex surface versus runtime `.codex/`, `~/.codex/`, and `$HOME/.agents/skills/` locations
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
- **Adding Codex documentation or source material**: Update `codex/README.md` first so the repository-owned layout stays intentional before adding new Codex files or directories
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
- Do not treat `codex/` as a runtime install location; runtime Codex config belongs under `.codex/`, `~/.codex/`, or `$HOME/.agents/skills/` depending on scope
- Do not reference specific project names or URLs in the templates — they must be generic
- Do not merge the style guide into AGENTS.md — the separation is intentional for context window efficiency
- Do not set `user-invocable: true` on subagents — they are hidden by design and invoked only by orchestrators
