# Agents

Specialized agents for structured software development workflows. Each agent is designed for a specific role and can be composed into **pipelines** — multi-step workflows where each step runs in a fresh context, passing written artifacts forward as attachments.

---

## How to Use an Agent

### 1. Open GitHub Copilot Chat

Open the Copilot Chat panel in VS Code (`Ctrl+Shift+I` / `Cmd+Shift+I`, or click the Copilot icon in the sidebar).

### 2. Select an agent

At the top of the chat panel, click the **agent picker** (the dropdown that might say "Ask" or "Chat" or show a model name). You'll see the available agents listed by name. Select the one you want — for example, **Planner**.

Alternatively, in some configurations you can type `@Planner` directly in the chat input to invoke an agent by name.

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

Each agent produces structured output — plan documents, implementation summaries, review tables, audit reports, etc. Review what the agent produces before moving to the next step.

---

## Available Agents (11)

### Planning & Implementation

| Agent | Model | Purpose |
|-------|-------|---------|
| **Planner** | Opus | Plan a feature with testable acceptance criteria, architecture fit, and a test strategy |
| **Implementer** | Opus | Implement from an approved plan with strict traceability and TDD |
| **Reviewer** | Opus | Review implementation against a plan for accuracy, bugs, and completeness |

### Testing

| Agent | Model | Purpose |
|-------|-------|---------|
| **Test Writer** | Opus | Bootstrap a test suite from scratch for untested code |
| **Test Analyst** | Opus | Evaluate an existing test suite for redundancy, coverage gaps, and consolidation opportunities |

### Code Quality

| Agent | Model | Purpose |
|-------|-------|---------|
| **Code Auditor** | Opus | Comprehensive code quality, security, and health audit — report only |
| **Refactor** | Opus | Reorganize file structures, extract components, fix anti-patterns |

### Debugging & Research

| Agent | Model | Purpose |
|-------|-------|---------|
| **Frontend Debugger** | — | Diagnose and fix frontend build-time and runtime errors |
| **Web Researcher** | Sonnet | Research solutions across GitHub issues, forums, and documentation |

### Infrastructure & Documentation

| Agent | Model | Purpose |
|-------|-------|---------|
| **Infrastructure Auditor** | Opus | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **Docs Writer** | — | Create or update README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING docs |

---

## What Each Agent Does

**Planner** (document-only — does not write code)
> Give it a problem statement or spec. It scans the codebase for context, asks targeted questions, then writes a structured plan with numbered acceptance criteria, architecture analysis, edge-case identification, and a test strategy to `dev/active/[task-name]/`. It will not create any files until you explicitly approve.

**Implementer** (full tool access — reads and writes code)
> Give it an approved plan. It implements each acceptance criterion incrementally using Red-Green-Refactor TDD, and produces a traceable implementation summary showing what was done and where.

**Reviewer** (read-only — does not modify code)
> Give it a plan and implementation to review. It checks traceability, hunts for bugs and edge cases, flags inconsistencies, and produces a prioritized issue table. It has access to PR tools and can pull Copilot review comments. It will NOT fix anything — only report.

**Test Writer** (writes test code only — does not modify source)
> Give it a module or directory to cover. It scans the codebase, proposes a test plan, and after your approval writes working test files and configuration. It verifies the suite passes before finishing.

**Test Analyst** (document-only — does not modify tests)
> Give it a test directory to analyze. It classifies tests by value, flags redundancy and over-mocking, and writes a categorized inventory with a staged reduction plan to `dev/active/[task-name]/`. It will not create any files until you explicitly approve.

**Code Auditor** (document-only — does not modify code)
> Give it a codebase or specific files. It audits every file against categories including cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report with file:line references.

**Refactor** (full tool access — reads and writes code)
> Give it a codebase area to reorganize. It maps all dependencies, plans the new structure, executes file moves and component extractions, and updates all imports. Verifies no breakage after each step.

**Frontend Debugger** (full tool access — reads and writes code)
> Give it an error message or description. It classifies the error (build-time, runtime, network), investigates via stack traces and browser tools, and applies minimal targeted fixes.

**Web Researcher** (read-only — uses fetch)
> Give it a problem or topic. It generates multiple search query variations, searches across GitHub issues, Stack Overflow, Reddit, forums, and docs, and compiles a structured findings report with sources.

**Infrastructure Auditor** (document-only — does not modify files)
> Give it infrastructure files to audit. It evaluates Dockerfiles, CI/CD pipelines, IaC templates, build scripts, and config files for security, best practices, consistency, and operational risk. Produces a structured report.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. It explores the codebase structure, then produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING documents.

---

## Pipelines

Pipelines are multi-step workflows composed from individual agents. **Each step runs in a new chat context.** The outputs from one step (plan documents, audit reports, etc.) are passed as attachments to the next step, so prompts can be brief.

### Pipeline 1: Feature Creation

The core development pipeline — plan, build, review, ship.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Planner** | Describe the feature in detail | Spec docs (optional) |
| 2 | **Implementer** | "Implement the plan" | Planner docs output (`dev/active/[task-name]/`) |
| 3 | **Reviewer** | "Review the implementation" | Planner docs output |
| 4 | — | Push to GitHub and open PR with Copilot review | — |
| 5 | **Reviewer** | "Pull the PR Copilot review comments and address problems" | Planner docs output |

### Pipeline 2: Test Suite Bootstrap

For projects with no tests or low coverage — create a test suite, then validate it.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Test Writer** | "Bootstrap tests for `[directory or module]`" | None (reads codebase) |
| 2 | **Test Analyst** | "Evaluate the test suite" | None (reads test files) |
| 3 | **Implementer** | "Implement the test analyst's recommendations" | Test Analyst docs output (`dev/active/[task-name]/`) |

### Pipeline 3: Test Suite Cleanup

For projects where tests have grown unwieldy — analyze, plan reductions, execute.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Test Analyst** | "Analyze the test suite in `[test directory]`" | None (reads test files) |
| 2 | **Planner** | "Create a plan to implement the test reduction recommendations" | Test Analyst docs output (`dev/active/[task-name]/`) |
| 3 | **Implementer** | "Implement the plan" | Planner docs output |
| 4 | **Reviewer** | "Review the test changes" | Planner docs output, Test Analyst docs output |

### Pipeline 4: Code Quality Improvement

Audit the codebase, plan fixes, implement, and review.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Code Auditor** | "Audit the codebase" (or specify a directory) | None (reads codebase) |
| 2 | **Planner** | "Create a plan to address the audit findings" | Code Auditor report (`dev/active/[audit-name]/`) |
| 3 | **Implementer** | "Implement the plan" | Planner docs output |
| 4 | **Reviewer** | "Review the implementation" | Planner docs output, Code Auditor report |

### Pipeline 5: Refactoring

Audit for structural issues, then refactor with review.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Code Auditor** | "Audit `[area]` for structural and organizational issues" | None (reads codebase) |
| 2 | **Refactor** | "Refactor based on the audit findings" | Code Auditor report |
| 3 | **Reviewer** | "Review the refactoring" | Code Auditor report |

### Pipeline 6: Bug Investigation and Fix

Research a tricky bug, fix it, and review — useful when the root cause is unclear.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Web Researcher** | Describe the error message or behavior | None |
| 2 | **Frontend Debugger** | "Investigate and fix the error" | Web Researcher findings (optional) |
| 3 | **Reviewer** | "Review the fix" | None |

### Pipeline 7: Documentation Overhaul

Audit the codebase and infrastructure, then produce comprehensive docs.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Code Auditor** | "Audit the codebase" | None (reads codebase) |
| 2 | **Infrastructure Auditor** | "Audit infrastructure files" | None (reads infra files) |
| 3 | **Docs Writer** | "Create documentation for the repo" | Code Auditor report, Infrastructure Auditor report (optional) |

### Pipeline 8: Infrastructure Audit & Remediation

Audit infrastructure files, plan fixes, and implement.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Infrastructure Auditor** | "Audit infrastructure files" | None |
| 2 | **Planner** | "Create a plan to address the infrastructure findings" | Infrastructure Auditor report (`dev/active/[audit-name]/`) |
| 3 | **Implementer** | "Implement the plan" | Planner docs output |
| 4 | **Reviewer** | "Review the implementation" | Planner docs output, Infrastructure Auditor report |

---

## Standalone Usage

Not everything needs a pipeline. These agents work well on their own:

- **Code Auditor** or **Infrastructure Auditor** — Run anytime for a health check
- **Reviewer** — Point at any PR or set of changes for an independent review
- **Test Analyst** — Evaluate test quality during maintenance windows
- **Web Researcher** — Research a technical question or debug a tricky issue
- **Docs Writer** — Update documentation after any significant change
- **Frontend Debugger** — Fix a specific error without a full pipeline

---

## Task Documentation Pattern

Several agents produce output in the **three-file pattern**:

```
dev/active/[task-name]/
├── [task-name]-plan.md      # Accepted plan with stages
├── [task-name]-context.md   # Key files, decisions, constraints
└── [task-name]-tasks.md     # Checklist of work items
```

Agents that produce this pattern: **Planner**, **Test Analyst**.

Audit agents (**Code Auditor**, **Infrastructure Auditor**) produce reports in:

```
dev/active/[audit-name]/
├── [audit-name]-report.md   # Full structured findings
└── [audit-name]-summary.md  # Executive summary with priority actions
```

The **Reviewer** appends its review to the relevant task directory. The **Implementer** tracks its progress in the same location.

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
- **Read-only agents**: **Reviewer**, **Code Auditor**, **Infrastructure Auditor**, and **Test Analyst** do not modify code. They analyze and report only.
- **Approval-gated agents**: **Planner**, **Test Analyst**, **Code Auditor**, and **Infrastructure Auditor** always present findings and ask for explicit approval before creating any files.
- **Code-writing agents**: **Implementer**, **Refactor**, **Test Writer**, and **Frontend Debugger** have full tool access to create and modify files.
