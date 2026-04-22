# github-agents-source-of-truth

Opinionated templates and VS Code Copilot agent definitions for standardizing how [GitHub Copilot](https://docs.github.com/en/copilot) behaves in your projects. Two things in one repo:

1. **`AGENTS.md` + style guide templates** (Node.js and Python) — copy into your project so Copilot follows your coding conventions, TDD workflow, and quality gates
2. **24 VS Code Copilot agent definitions** — a full orchestrator + subagent system for planning, implementing, reviewing, auditing, testing, and documenting entire projects hands-free

## Why This Exists

GitHub Copilot reads `AGENTS.md` files to learn coding conventions, workflow rules, and quality standards. Writing these from scratch for every repo is tedious and error-prone. This repo gives you tested starting points for both:

- **Coding standards** — Principles, TDD workflow, language-specific style conventions, property-based testing, agent operation guidelines, and quality gates
- **Development workflow agents** — A pipeline that takes a project from planning through implementation, code review, QA, and documentation with minimal manual intervention

## Repository Structure

```
.
├── README.md
├── .github/
│   ├── agents/                # VS Code Copilot agent definitions
│   │   ├── README.md          # Agent documentation, pipelines, and usage guide
│   │   └── *.agent.md         # 24 agent files (12 user-facing, 12 hidden subagents)
│   ├── skills/                # Shared templates and formats loaded by agents on demand
│   │   ├── auditor-conventions/       # Audit constraints, report format, severity levels
│   │   ├── feature-plan-set/          # Three-file plan convention, sections A–F
│   │   ├── implementation-pipeline-loop/  # Implement → Review → Commit cycle
│   │   ├── phase-document-writing/    # Phase doc templates and quality checklist
│   │   ├── unity-development/         # Unity C# implementation and review rules
│   │   └── unity-review-knowledge/    # Unity best practices from official Unity ebooks
│   ├── instructions/          # Cross-cutting conventions injected via applyTo globs
│   │   └── *.instructions.md  # 10 instruction files (see ARCHITECTURE.md for full list)
│   └── learnings/             # Persistent review and implementation learnings for agents
│       ├── project-learnings.md       # Project-specific lessons and recurring implementation notes
│       └── review-learnings.md        # Recurring review issues and patterns
│       └── cross-phase-decisions.md   # Decisions that affect downstream features/phases
├── docs/
│   ├── ARCHITECTURE.md        # Structure diagram and design decisions
│   ├── CODEBASE_CONTEXT.md    # Agent-oriented quick-reference
│   └── phases/
│       ├── PHASES_OVERVIEW.md # High-level project roadmap across phases
│       └── PHASE_01/
│           └── PHASE_01_SUMMARY.md # Current phase objective, scope, and success criteria
├── nodejs/
│   ├── AGENTS.md              # Agent guidelines for Node.js/TypeScript projects
│   └── docs/
│       └── STYLE_GUIDE.md     # Node.js/TypeScript coding conventions
└── python/
    ├── AGENTS.md              # Agent guidelines for Python projects
    └── docs/
        └── STYLE_GUIDE.md     # Python coding conventions
```

## Usage

### AGENTS.md Templates

Copy the template files for your language into your project, then customize them.

#### 1. Pick your language

```bash
# For a Node.js/TypeScript project
cp -r nodejs/AGENTS.md /path/to/your-project/AGENTS.md
cp -r nodejs/docs/STYLE_GUIDE.md /path/to/your-project/docs/STYLE_GUIDE.md

# For a Python project
cp -r python/AGENTS.md /path/to/your-project/AGENTS.md
cp -r python/docs/STYLE_GUIDE.md /path/to/your-project/docs/STYLE_GUIDE.md
```

#### 2. Customize

- **AGENTS.md** — Adjust dependency tooling, testing framework preferences, or commit conventions to match your team's workflow.
- **docs/STYLE_GUIDE.md** — Modify naming rules, import ordering, or style preferences to align with your existing codebase.

#### 3. Use with GitHub Copilot

Once the files are in your project, GitHub Copilot automatically discovers and follows them. No additional configuration is needed.

### VS Code Copilot Agents

Copy the `.github/` directory into your project to get the full agent system:

```bash
cp -r .github/agents /path/to/your-project/.github/agents
cp -r .github/skills /path/to/your-project/.github/skills
cp -r .github/instructions /path/to/your-project/.github/instructions
```

The agents appear in the VS Code Copilot Chat agent picker. See [.github/agents/README.md](.github/agents/README.md) for the full usage guide, pipeline documentation, and per-agent descriptions.

#### The Project Pipeline (3 user steps)

1. **01 Project - Planner** — Describe your project scope. Produces phase documents.
2. **02 Phase - Refiner** — Refine scope, edge cases, and dependencies.
3. **04 Phase - Execute** — Automated: decomposes, implements via TDD, reviews, QA, docs.

See [.github/agents/README.md](.github/agents/README.md#the-project-pipeline-3-user-steps) for the full pipeline documentation.

## What's in Each File

### AGENTS.md (templates)

The core instructions file that GitHub Copilot reads. Both language variants share a common structure:

| Section | Purpose |
|---|---|
| **Package/Environment Management** | Dependency tooling (`npm` / `uv`) and lockfile rules |
| **Core Engineering Principles** | Compact, high-signal defaults for implementation behavior |
| **Process** | TDD implementation flow (plan → test → implement → refactor → commit) |
| **Testing** | TDD workflow, test quality rules, property-based testing (fast-check / Hypothesis) |
| **Quality Standards** | Commit checklist, decision priority, never/always rules |
| **Communication** | Concision and tooling preferences for predictable outputs |
| **Extended Guides** | Pointer to `docs/STYLE_GUIDE.md` for detailed conventions |

Compaction note: shared guidance between `nodejs/AGENTS.md` and `python/AGENTS.md` is intentionally concise to reduce token usage while preserving safety, quality, and workflow constraints.

### docs/STYLE_GUIDE.md (templates)

Detailed, language-specific coding conventions covering:

- Logging, configuration, and error handling patterns
- Naming conventions and import ordering
- Type annotations and documentation standards
- Async patterns (Node.js) / OOP preferences (Python)
- Function size and structure guidelines

### Agent Definitions (.github/agents/)

24 agent files using an **orchestrator + subagent** pattern (4 orchestrators, 8 standalone user-facing, 12 hidden subagents). Orchestrators delegate to subagents automatically; shared subagents are reused across orchestrator pipelines. See [.github/agents/README.md](.github/agents/README.md) for detailed per-agent documentation and pipeline descriptions.

### Skills (.github/skills/)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#skills) for the full skills inventory.

### Instructions (.github/instructions/)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#instructions) for the full instructions inventory.

## Key Differences Between Languages

| Concern | Node.js | Python |
|---|---|---|
| Dependency management | `npm` + `package-lock.json` | `uv` + `pyproject.toml` |
| Property-based testing | [fast-check](https://fast-check.dev/) | [Hypothesis](https://hypothesis.readthedocs.io/) |
| Data models | TypeScript interfaces | Pydantic v2 with frozen config |
| Style preference | Functional patterns where appropriate | Object-oriented programming |
| Logging | `pino` or `winston` | Python `logging` module |

## Further Reading

- [.github/agents/README.md](.github/agents/README.md) — Full agent documentation, pipeline diagrams, and per-agent descriptions
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Mermaid diagrams of repo structure, agent architecture, and design decisions
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) — Dense structured facts for AI agent orientation
- [docs/phases/PHASES_OVERVIEW.md](docs/phases/PHASES_OVERVIEW.md) — Current phased roadmap and scope sequencing
- [docs/phases/PHASE_01/PHASE_01_SUMMARY.md](docs/phases/PHASE_01/PHASE_01_SUMMARY.md) — Detailed scope and quality gates for Phase 01
- [docs/AGENT_REGRESSION_BENCHMARK_SPEC.md](docs/AGENT_REGRESSION_BENCHMARK_SPEC.md) — Project-specific benchmark design for A/B testing model and agent changes
- [docs/benchmarks/B001/README.md](docs/benchmarks/B001/README.md) — First concrete benchmark pack with 30 core task cards and run/grader templates

