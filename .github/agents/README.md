# Agents

Specialized agents for structured software development workflows. Each agent is designed for a specific role and can be composed into **pipelines** — multi-step workflows where each step runs in a fresh context, passing written artifacts forward as attachments.

---

## How to Use an Agent

### 1. Open GitHub Copilot Chat

Open the Copilot Chat panel in VS Code (`Ctrl+Shift+I` / `Cmd+Shift+I`, or click the Copilot icon in the sidebar).

### 2. Select an agent

At the top of the chat panel, click the **agent picker** (the dropdown that might say "Ask" or "Chat" or show a model name). You'll see the available agents listed by name. Select the one you want — for example, **03 Feature - Planner**.

Alternatively, in some configurations you can type `@03 Feature - Planner` directly in the chat input to invoke an agent by name.

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

## Available Agents (15)

### Planning

| Agent | Model | Purpose |
|-------|-------|--------|
| **01 Project - Planner** | Opus | Create a project roadmap broken into phases that feed into the 02 Project - Phase Refiner |
| **02 Project - Phase Refiner** | Opus | Refine and deepen an individual Phase document before 03 Feature - Planner decomposition |
| **03 Feature - Planner** | Opus | Plan a feature with testable acceptance criteria, architecture fit, and a test strategy |

### Implementation

| **04 Feature - Implementer** | Opus | Implement from an approved plan with strict traceability and TDD |
| **05 Feature - Reviewer** | Opus | Review implementation against a plan for accuracy, bugs, and completeness |

### Testing

| Agent | Model | Purpose |
|-------|-------|---------|
| **Test - Writer** | Opus | Bootstrap a test suite from scratch for untested code |
| **Test - Analyst** | Opus | Evaluate an existing test suite for redundancy, coverage gaps, and consolidation opportunities |

### QA

| Agent | Model | Purpose |
|-------|-------|---------|
| **06 QA - Writer** | Opus | Write manual QA documents — Release QA Plan (plan + implementation + review) based on available documents |
| **07 Final Code Review** | Opus | Final pre-production readiness gate — cross-validates all pipeline documents and produces a go/no-go recommendation before manual QA begins |

### Code Quality

| Agent | Model | Purpose |
|-------|-------|---------|
| **Auditor - Code** | Opus | Comprehensive code quality, security, and health audit — report only |
| **Refactor** | Opus | Reorganize file structures, extract components, fix anti-patterns |

### Debugging & Research

| Agent | Model | Purpose |
|-------|-------|---------|
| **Debugger - Frontend** | — | Diagnose and fix frontend build-time and runtime errors |
| **Web Researcher** | Sonnet | Research solutions across GitHub issues, forums, and documentation |

### Infrastructure & Documentation

| Agent | Model | Purpose |
|-------|-------|---------|
| **Auditor - Infra** | Opus | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **Docs Writer** | — | Create or update README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING docs |

---

## What Each Agent Does

**01 Project - Planner** (document-only — does not write code)
> Give it a project scope or high-level goal. It iterates with you to produce a phased roadmap (`docs/phases/PHASES_OVERVIEW.md` and individual `docs/phases/PHASE_0N_[short-name].md` files). Each phase document is self-contained and designed to be handed off to the 03 Feature - Planner for decomposition into individual features. It will not create any files until you explicitly approve.

**02 Project - Phase Refiner** (document-only — does not write code)
> Give it a single Phase document (`docs/phases/PHASE_0N_[short-name].md`) from the 01 Project - Planner. It iterates with you to refine scope, probe edge cases, surface hidden dependencies, stress-test decomposition readiness, and walk through user flows — deepening the Phase document until it's fully ready for 03 Feature - Planner decomposition. It updates the Phase document in place and will not write changes until you explicitly approve. If iteration reveals that the overall project roadmap needs changes, it flags this and recommends returning to `@01 Project - Planner`.

**03 Feature - Planner** (document-only — does not write code)
> Give it a problem statement or spec. It scans the codebase for context, asks targeted questions, then writes a structured plan with numbered acceptance criteria, architecture analysis, edge-case identification, and a test strategy to `dev/[task-name]/`. It will not create any files until you explicitly approve.

**04 Feature - Implementer** (full tool access — reads and writes code)
> Give it an approved plan. It implements each acceptance criterion incrementally using Red-Green-Refactor TDD and writes a structured implementation record (`[task-name]-implementation.md`) to `dev/[task-name]/`. This file lists every changed file with rationale, maps changes back to acceptance criteria, and highlights focus areas for the 05 Feature - Reviewer.

**05 Feature - Reviewer** (read-only — does not modify code unless approved)
> Give it a plan and implementation to review. It checks traceability, hunts for bugs and edge cases, flags inconsistencies, and produces a prioritized issue table. It has access to PR tools and can pull Copilot review comments. After the review (and any approved fixes), it writes a review record (`[task-name]-review.md`) to `dev/[task-name]/` capturing the verdict, all issues found, fixes applied, and remaining concerns.

**Test - Writer** (writes test code only — does not modify source)
> Give it a module or directory to cover. It scans the codebase, proposes a test plan, and after your approval writes working test files and configuration. It verifies the suite passes before finishing.

**Test - Analyst** (document-only — does not modify tests)
> Give it a test directory to analyze. It classifies tests by value, flags redundancy and over-mocking, and writes a categorized inventory with a staged reduction plan to `dev/[task-name]/`. It will not create any files until you explicitly approve.

**Auditor - Code** (document-only — does not modify code)
> Give it a codebase or specific files. It audits every file against categories including cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report with file:line references.

**Refactor** (full tool access — reads and writes code)
> Give it a codebase area to reorganize. It maps all dependencies, plans the new structure, executes file moves and component extractions, and updates all imports. Verifies no breakage after each step.

**Debugger - Frontend** (full tool access — reads and writes code)
> Give it an error message or description. It classifies the error (build-time, runtime, network), investigates via stack traces and browser tools, and applies minimal targeted fixes.

**Web Researcher** (read-only — uses fetch)
> Give it a problem or topic. It generates multiple search query variations, searches across GitHub issues, Stack Overflow, Reddit, forums, and docs, and compiles a structured findings report with sources.

**06 QA - Writer** (document-only — does not modify code)
> Give it a task folder. With plan + implementation + review + code/tests, it produces a full **Release QA Plan** — an execution-ready checklist with concrete steps, expected results, and coverage gap analysis. Output goes to `dev/[task-name]/[task-name]-qa.md`.

**07 Final Code Review** (document-only — does not modify code or documents)
> Give it the complete `dev/[task-name]/` folder containing all pipeline documents (plan, context, tasks, implementation record, review record, and QA plan). It performs an exhaustive cross-validation of every document against every other document, verifies the actual code matches the records, runs the test suite, and evaluates the QA plan's completeness. Produces a detailed readiness analysis with a **GO / GO WITH CONDITIONS / NO-GO** verdict, a full traceability matrix, a risk register, and actionable recommendations. This is the final automated gate before manual QA execution and release. Output goes to `dev/[task-name]/[task-name]-qa-analysis.md`.

**Auditor - Infra** (document-only — does not modify files)
> Give it infrastructure files to audit. It evaluates Dockerfiles, CI/CD pipelines, IaC templates, build scripts, and config files for security, best practices, consistency, and operational risk. Produces a structured report.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. It explores the codebase structure, then produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING documents.

---

## Pipelines

Pipelines are multi-step workflows composed from individual agents. **Each step runs in a new chat context.** The outputs from one step (plan documents, audit reports, etc.) are passed as attachments to the next step, so prompts can be brief.

### Pipeline 1: Project Pipeline

The core development pipeline — plan, build, review, ship.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **01 Project - Planner** | Plan out the project scope and trajectory at a high level | Spec docs (optional) |
| 2 | **02 Project - Phase Refiner** | "Refine and deepen this Phase document" | Individual Phase document (`docs/phases/PHASE_0N_*.md`) |
| 3 | **03 Feature - Planner** | "Prepare implementation plans for individual features" | (`docs/phases/PHASE_0N_*.md`) |
| 5 | **04 Feature - Implementer** | "Implement the plan" | 03 Feature - Planner docs output (`dev/[task-name]/`) |
| 6 | **05 Feature - Reviewer** | "Review the implementation" | 03 Feature - Planner docs output, 04 Feature - Implementer record, QA skeleton (`[task-name]-qa.md`) |
| 7 | — | Push to GitHub and open PR with Copilot review | — |
| 8 | **05 Feature - Reviewer** | "Pull the PR Copilot review comments and address problems" | 03 Feature - Planner docs output, 04 Feature - Implementer record |
| 9 | **06 QA - Writer** | "Write the release QA plan for this feature" | All task docs in `dev/[task-name]/` |
| 10 | **07 Final Code Review** | "Evaluate readiness for manual QA" | All task docs in `dev/[task-name]/` |

### Pipeline 2: Test Suite Bootstrap

For projects with no tests or low coverage — create a test suite, then validate it.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Test - Writer** | "Bootstrap tests for `[directory or module]`" | None (reads codebase) |
| 2 | **Test - Analyst** | "Evaluate the test suite" | None (reads test files) |
| 3 | **04 Feature - Implementer** | "Implement the Test - Analyst's recommendations" | Test - Analyst docs output (`dev/[task-name]/`) |

### Pipeline 3: Test Suite Cleanup

For projects where tests have grown unwieldy — analyze, plan reductions, execute.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Test - Analyst** | "Analyze the test suite in `[test directory]`" | None (reads test files) |
| 2 | **03 Feature - Planner** | "Create a plan to implement the test reduction recommendations" | Test - Analyst docs output (`dev/[task-name]/`) |
| 3 | **04 Feature - Implementer** | "Implement the plan" | 03 Feature - Planner docs output |
| 4 | **05 Feature - Reviewer** | "Review the test changes" | 03 Feature - Planner docs output, Test - Analyst docs output, 04 Feature - Implementer record |

### Pipeline 4: Code Quality Improvement

Audit the codebase, plan fixes, implement, and review.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Auditor - Code** | "Audit the codebase" (or specify a directory) | None (reads codebase) |
| 2 | **03 Feature - Planner** | "Create a plan to address the audit findings" | Auditor - Code report (`dev/[audit-name]/`) |
| 3 | **04 Feature - Implementer** | "Implement the plan" | 03 Feature - Planner docs output |
| 4 | **05 Feature - Reviewer** | "Review the implementation" | 03 Feature - Planner docs output, Auditor - Code report, 04 Feature - Implementer record |

### Pipeline 5: Refactoring

Audit for structural issues, then refactor with review.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Auditor - Code** | "Audit `[area]` for structural and organizational issues" | None (reads codebase) |
| 2 | **Refactor** | "Refactor based on the audit findings" | Auditor - Code report |
| 3 | **05 Feature - Reviewer** | "Review the refactoring" | Auditor - Code report |

### Pipeline 6: Bug Investigation and Fix

Research a tricky bug, fix it, and review — useful when the root cause is unclear.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Web Researcher** | Describe the error message or behavior | None |
| 2 | **Debugger - Frontend** or **Debugger - Backend** | "Investigate and fix the error" | Web Researcher findings (optional) |
| 3 | **05 Feature - Reviewer** | "Review the fix" | None |

### Pipeline 7: Documentation Overhaul

Audit the codebase and infrastructure, then produce comprehensive docs.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Auditor - Code** | "Audit the codebase" | None (reads codebase) |
| 2 | **Auditor - Infra** | "Audit infrastructure files" | None (reads infra files) |
| 3 | **Docs Writer** | "Create documentation for the repo" | Auditor - Code report, Auditor - Infra report (optional) |

### Pipeline 8: Infrastructure Audit & Remediation

Audit infrastructure files, plan fixes, and implement.

| Step | Agent | Prompt | Attachments |
|------|-------|--------|-------------|
| 1 | **Auditor - Infra** | "Audit infrastructure files" | None |
| 2 | **03 Feature - Planner** | "Create a plan to address the infrastructure findings" | Auditor - Infra report (`dev/[audit-name]/`) |
| 3 | **04 Feature - Implementer** | "Implement the plan" | 03 Feature - Planner docs output |
| 4 | **05 Feature - Reviewer** | "Review the implementation" | 03 Feature - Planner docs output, Auditor - Infra report, 04 Feature - Implementer record |

---

## Standalone Usage

Not everything needs a pipeline. These agents work well on their own:

- **Auditor - Code** or **Auditor - Infra** — Run anytime for a health check
- **05 Feature - Reviewer** — Point at any PR or set of changes for an independent review
- **Test - Analyst** — Evaluate test quality during maintenance windows
- **Web Researcher** — Research a technical question or debug a tricky issue
- **Docs Writer** — Update documentation after any significant change
- **Debugger - Frontend** — Fix a specific error without a full pipeline

---

## Task Documentation Pattern

Several agents produce output in the **three-file pattern**:

```
dev/[task-name]/
├── [task-name]-plan.md      # Accepted plan with stages
├── [task-name]-context.md   # Key files, decisions, constraints
└── [task-name]-tasks.md     # Checklist of work items
```

Agents that produce this pattern: **03 Feature - Planner**, **Test - Analyst**.

Audit agents (**Auditor - Code**, **Auditor - Infra**) produce reports in:

```
dev/[audit-name]/
├── [audit-name]-report.md   # Full structured findings
└── [audit-name]-summary.md  # Executive summary with priority actions
```

The **04 Feature - Implementer** writes an implementation record to the same directory:

```
dev/[task-name]/
└── [task-name]-implementation.md   # Files changed, AC traceability, reviewer focus areas
```

The **05 Feature - Reviewer** writes a review record to the same directory:

```
dev/[task-name]/
└── [task-name]-review.md   # Verdict, issues found, fixes applied, remaining concerns
```

The **07 Final Code Review** writes a readiness analysis to the same directory:

```
dev/[task-name]/
└── [task-name]-qa-analysis.md   # GO/NO-GO verdict, traceability matrix, risk register, recommendations
```

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
- **Read-only agents**: **05 Feature - Reviewer**, **Auditor - Code**, **Auditor - Infra**, **Test - Analyst**, and **07 Final Code Review** do not modify code. They analyze and report only.
- **Approval-gated agents**: **01 Project - Planner**, **02 Project - Phase Refiner**, **03 Feature - Planner**, **Test - Analyst**, **Auditor - Code**, **Auditor - Infra**, and **07 Final Code Review** always present findings and ask for explicit approval before creating any files.
- **Code-writing agents**: **04 Feature - Implementer**, **Refactor**, **Test - Writer**, and **Debugger - Frontend** have full tool access to create and modify files.
