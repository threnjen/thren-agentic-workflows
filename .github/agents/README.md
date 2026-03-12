# Agents

Specialized agents for structured software development workflows.

---

## Available Agents (4)

| Agent | Model | Purpose |
|-------|-------|---------|
| **feature-planner** | opus | Plan a feature with testable acceptance criteria, architecture fit, and a test strategy |
| **implementation-executor** | sonnet | Implement from an approved plan with strict traceability and incremental checkpoints |
| **code-reviewer** | opus | Review an implementation against the plan for accuracy, bugs, and completeness |
| **test-suite-evaluator** | sonnet | Evaluate an existing test suite for redundancy, coverage gaps, and consolidation opportunities |

---

## Recommended Invocation Order

These agents form a development pipeline. Use them in sequence for maximum rigor:

```
1. feature-planner        → Produces plan, context, and task documents
2. implementation-executor → Implements the plan with AC traceability
3. code-reviewer           → Reviews implementation against the plan
4. test-suite-evaluator    → Evaluates the resulting test suite quality
```

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

## Integration Notes

- **Language-agnostic**: These agents are generic. They read your workspace's `AGENTS.md` at runtime for language-specific conventions (naming, testing tools, formatting, etc.).
- **Self-contained**: Each agent file works standalone — just copy the `.md` file into any project's `.github/agents/` directory.
- **Read-only agents**: `feature-planner`, `code-reviewer`, and `test-suite-evaluator` are restricted to read-only tools. They analyze and report but do not modify code. Only `implementation-executor` has full tool access.
