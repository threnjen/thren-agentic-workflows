# github-agents-source-of-truth

Opinionated, ready-to-use `AGENTS.md` and style guide templates that standardize how [GitHub Copilot](https://docs.github.com/en/copilot) behaves in your Node.js and Python projects.

## Why This Exists

GitHub Copilot reads `AGENTS.md` files at the root and in subdirectories of your project to learn coding conventions, workflow rules, and quality standards. Writing these from scratch for every repo is tedious and error-prone. This template repo gives you a tested starting point covering:

- Coding principles and TDD workflow
- Language-specific style conventions (TypeScript/Node.js and Python)
- Testing strategies including property-based testing
- Agent operation guidelines (context management, self-review, subagents)
- Quality gates for every commit

## Repository Structure

```
.
├── README.md
├── .github/
│   └── agents/                # VS Code Copilot agent definitions
│       ├── README.md          # Agent documentation, pipelines, and usage guide
│   └── *.agent.md         # 21 agent files (10 user-facing, 11 hidden subagents)
├── docs/
│   ├── ARCHITECTURE.md        # Structure diagram and design decisions
│   └── CODEBASE_CONTEXT.md    # Agent-oriented quick-reference
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

### 1. Pick your language

Copy the folder matching your project's language into your repository root:

```bash
# For a Node.js/TypeScript project
cp -r nodejs/AGENTS.md /path/to/your-project/AGENTS.md
cp -r nodejs/docs/STYLE_GUIDE.md /path/to/your-project/docs/STYLE_GUIDE.md

# For a Python project
cp -r python/AGENTS.md /path/to/your-project/AGENTS.md
cp -r python/docs/STYLE_GUIDE.md /path/to/your-project/docs/STYLE_GUIDE.md
```

### 2. Customize

Edit the copied files to match your project's specifics:

- **AGENTS.md** — Adjust dependency tooling, testing framework preferences, or commit conventions to match your team's workflow.
- **docs/STYLE_GUIDE.md** — Modify naming rules, import ordering, or style preferences to align with your existing codebase.

### 3. Use with GitHub Copilot

Once the files are in your project, GitHub Copilot automatically discovers and follows them. No additional configuration is needed.

## What's in Each File

### AGENTS.md

The core instructions file that GitHub Copilot reads. Both language variants share a common structure:

| Section | Purpose |
|---|---|
| **Package/Environment Management** | Dependency tooling (`npm` / `uv`) and lockfile rules |
| **Principles** | Incremental progress, clear intent, single responsibility, fail-fast |
| **Process** | TDD implementation flow (plan → test → implement → refactor → commit) |
| **Testing** | TDD workflow, test quality rules, property-based testing (fast-check / Hypothesis) |
| **Quality Standards** | Commit checklist, decision priority, never/always rules |
| **Agent Operations** | Context clearing, subagent usage, self-review checklist |
| **Extended Guides** | Pointer to `docs/STYLE_GUIDE.md` for detailed conventions |

### docs/STYLE_GUIDE.md

Detailed, language-specific coding conventions covering:

- Logging, configuration, and error handling patterns
- Naming conventions and import ordering
- Type annotations and documentation standards
- Async patterns (Node.js) / OOP preferences (Python)
- Function size and structure guidelines

## Key Differences Between Languages

| Concern | Node.js | Python |
|---|---|---|
| Dependency management | `npm` + `package-lock.json` | `uv` + `pyproject.toml` |
| Property-based testing | [fast-check](https://fast-check.dev/) | [Hypothesis](https://hypothesis.readthedocs.io/) |
| Data models | TypeScript interfaces | Pydantic v2 with frozen config |
| Style preference | Functional patterns where appropriate | Object-oriented programming |
| Logging | `pino` or `winston` | Python `logging` module |

## Further Reading

- [.github/agents/README.md](.github/agents/README.md) — Full agent documentation: pipelines, usage, and what each agent does
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — How the template files and agents are structured and relate to each other
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) — Agent-oriented quick-reference for working on this repo