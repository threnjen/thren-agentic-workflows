# Agents

Specialized agents for structured software development workflows.

---

## How to Use an Agent

### 1. Open GitHub Copilot Chat

Open the Copilot Chat panel in VS Code (`Ctrl+Shift+I` / `Cmd+Shift+I`, or click the Copilot icon in the sidebar).

### 2. Select an agent

At the top of the chat panel, click the **agent picker** (the dropdown that might say "Ask" or "Chat" or show a model name). You'll see the available agents listed by name. Select the one you want — for example, **feature-planner**.

Alternatively, in some configurations you can type `@feature-planner` directly in the chat input to invoke an agent by name.

### 3. Give it context and a prompt

Write your request in the chat input. Be specific about what you want:

```
Plan a new user notification service. Here are the requirements:
- Send email and SMS notifications
- Support scheduling for future delivery
- Integrate with our existing auth service
```

The agent will ask clarifying questions if it needs more context before proceeding.

### 4. Review the output

Each agent produces structured output — plan documents, implementation summaries, review tables, etc. Review what the agent produces before moving to the next step.

---

## Available Agents (4)

| Agent | Model | Purpose |
|-------|-------|---------|
| **feature-planner** | opus | Plan a feature with testable acceptance criteria, architecture fit, and a test strategy |
| **implementation-executor** | sonnet | Implement from an approved plan with strict traceability and incremental checkpoints |
| **code-reviewer** | opus | Review an implementation against the plan for accuracy, bugs, and completeness |
| **test-suite-evaluator** | sonnet | Evaluate an existing test suite for redundancy, coverage gaps, and consolidation opportunities |

### What each agent does

**feature-planner** (document-only — does not write code)
> Give it a problem statement or spec. It first scans the codebase for context, then asks targeted questions. Once you confirm the plan outline, it writes a structured plan with numbered acceptance criteria, architecture analysis, edge-case identification, and a test strategy to `dev/active/[task-name]/`. It will not create any files until you explicitly approve.

**implementation-executor** (full tool access — reads and writes code)
> Give it an approved plan. It implements each acceptance criterion incrementally, writes tests as it goes, and produces a traceable implementation summary showing what was done and where.

**code-reviewer** (read-only — does not modify code)
> Give it a plan and the implementation to review. It checks traceability, hunts for bugs and edge cases, flags inconsistencies, and produces a prioritized issue table. It will NOT fix anything — only report.

**test-suite-evaluator** (document-only — does not modify tests)
> Give it a test directory to analyze. It scans the tests and asks targeted questions about scope and pain points. Once you confirm the findings summary, it writes a categorized inventory, risk assessment, and staged reduction plan to `dev/active/[task-name]/`. It will not create any files until you explicitly approve.

---

## Recommended Workflow

These agents form a development pipeline. Use them in sequence for maximum rigor:

```
1. feature-planner        → Produces plan, context, and task documents
2. implementation-executor → Implements the plan with AC traceability
3. code-reviewer           → Reviews implementation against the plan
4. test-suite-evaluator    → Evaluates the resulting test suite quality
```

### Step-by-step example

1. **Plan**: Switch to `feature-planner`. Describe what you want to build. Review and approve the plan it produces.
2. **Implement**: Switch to `implementation-executor`. Point it at the plan files. It implements incrementally, one acceptance criterion at a time.
3. **Review**: Switch to `code-reviewer`. Point it at both the plan and the implementation. Fix any issues it surfaces.
4. **Evaluate tests**: Switch to `test-suite-evaluator`. Point it at the test files. Use its analysis to improve test quality.

### When to use each step

- **Always start with `feature-planner`** for any non-trivial feature. It produces the plan documents that downstream agents depend on.
- **Use `implementation-executor`** when you have an approved plan and want disciplined, incremental implementation with clear deliverables.
- **Use `code-reviewer`** after implementation is complete. Attach both the plan documents and the implementation for a thorough review.
- **Use `test-suite-evaluator`** periodically to audit test health — after a feature lands, during maintenance windows, or when test suites grow unwieldy.

### Skipping steps

- For small bug fixes, you can skip `feature-planner` and go straight to `implementation-executor` with a brief description of the fix.
- `code-reviewer` and `test-suite-evaluator` can each be used independently at any time — they don't require the other agents to have run first.

---

## Task Documentation Pattern

The `feature-planner` and `implementation-executor` agents produce output in the **three-file pattern**:

```
dev/active/[task-name]/
├── [task-name]-plan.md      # Accepted plan with stages
├── [task-name]-context.md   # Key files, decisions, constraints
└── [task-name]-tasks.md     # Checklist of work items
```

The `code-reviewer` appends its review to the same task directory. The `test-suite-evaluator` writes its analysis there as well.

---

## Adding Agents to Another Project

Each agent file is standalone. To use these agents in a different repository:

1. Create a `.github/agents/` directory in the target repo.
2. Copy the agent `.md` files you want into that directory.
3. That's it — VS Code will discover them automatically.

---

## Integration Notes

- **Language-agnostic**: These agents are generic. They read your workspace's `AGENTS.md` at runtime for language-specific conventions (naming, testing tools, formatting, etc.).
- **Self-contained**: Each agent file works standalone — just copy the `.md` file into any project's `.github/agents/` directory.
- **Read-only agents**: `code-reviewer` is restricted to read-only tools. It analyzes and reports but does not modify code.
- **Document-writing agents**: `feature-planner` and `test-suite-evaluator` have read/search/edit access, but will **never write a file without your explicit confirmation**. They always present a summary outline or findings summary and ask for your approval before creating any documents. Only `implementation-executor` has full tool access to write implementation files.
