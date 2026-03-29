# Agents

Specialized agents for structured software development workflows. The core workflow uses an **orchestrator + subagent** pattern — you interact with 3 agents, and the orchestrator drives the rest automatically.

---

## How to Use an Agent

### 1. Open GitHub Copilot Chat

Open the Copilot Chat panel in VS Code (`Ctrl+Shift+I` / `Cmd+Shift+I`, or click the Copilot icon in the sidebar).

### 2. Select an agent

At the top of the chat panel, click the **agent picker** dropdown. Select the agent you want — for example, **01 Project - Planner**.

### 3. Give it context and a prompt

Write your request in the chat input. Be specific about what you want.

### 4. Review the output

Each agent produces structured output — plan documents, implementation summaries, review tables, audit reports, etc.

---

## The Project Pipeline (3 user steps)

The core development workflow. **You interact with steps 1–3. Everything else is automated.**

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU                                                            │
│                                                                 │
│  Step 1: 01 Project - Planner    → Phase documents              │
│  Step 2: 02 Phase - Refiner      → Refined phase document       │
│  Step 3: 03 Phase - Execute      → Hands-free from here ──┐    │
│                                                             │    │
└─────────────────────────────────────────────────────────────│────┘
                                                              │
┌─────────────────────────────────────────────────────────────│────┐
│  AUTOMATED (subagents)                                      │    │
│                                                             ▼    │
│  Feature - Decomposer  → Plan sets for each feature              │
│  ┌──────────────────────────────────────────────┐                │
│  │  FOR EACH FEATURE:                           │                │
│  │  Feature - Implementer  → Code + tests       │                │
│  │  Feature - Reviewer     → Review + fixes     │                │
│  │  Feature - QA Writer    → QA plan            │                │
│  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │                │
│  │  Loop back for next feature                  │                │
│  └──────────────────────────────────────────────┘                │
│  Phase - Final Review   → GO / NO-GO verdict                     │
│                                                                   │
│  ──► Report back to you: "Phase complete. Ready for PR."         │
└───────────────────────────────────────────────────────────────────┘
```

### Step 1: Plan the Project

| Agent | Prompt | Output |
|-------|--------|--------|
| **01 Project - Planner** | Describe your project scope and goals | Phase documents in `docs/phases/` |

Interactive — you iterate with the planner to define phases and milestones.

### Step 2: Refine a Phase

| Agent | Prompt | Output |
|-------|--------|--------|
| **02 Phase - Refiner** | "Refine and deepen this Phase document" + attach phase doc | Updated phase document |

Interactive — you iterate to probe edge cases, dependencies, and decomposition readiness.

### Step 3: Execute the Phase

| Agent | Prompt | Output |
|-------|--------|--------|
| **03 Phase - Execute** | "Execute this phase" + attach refined phase doc | All features implemented, reviewed, QA'd |

**Hands-free from here.** The orchestrator automatically:

1. Decomposes the phase into features (via Feature - Decomposer subagent)
2. For each feature, runs the full cycle:
   - **Implement** → Red-Green-Refactor TDD, writes implementation record
   - **Review** → Finds bugs, applies fixes, writes review record
   - **QA Plan** → Writes manual QA checklist for non-automatable testing
3. Runs the **Phase - Final Review** across all features
4. Reports the verdict back to you

**After completion:** Push the branch and open a PR for final human review.

---

## Available Agents

### User-Facing (in agent picker)

| Agent | Model | Purpose |
|-------|-------|---------|
| **01 Project - Planner** | Opus | Create a project roadmap broken into phases |
| **02 Phase - Refiner** | Opus | Refine and deepen an individual Phase document |
| **03 Phase - Execute** | Opus | Orchestrate full phase execution — decompose, implement, review, QA |
| **Phase - Final Review** | Opus | Final pre-production readiness gate (also usable standalone) |
| **Test - Writer** | Opus | Bootstrap a test suite from scratch for untested code |
| **Test - Analyst** | Opus | Evaluate an existing test suite for redundancy, coverage gaps, and consolidation |
| **Auditor - Code** | Opus | Comprehensive code quality, security, and health audit — report only |
| **Auditor - Infra** | Opus | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **Refactor** | Opus | Reorganize file structures, extract components, fix anti-patterns |
| **Debugger - Frontend** | Opus | Diagnose and fix frontend build-time and runtime errors |
| **Debugger - Backend** | Opus | Diagnose and fix backend server-side errors |
| **Web Researcher** | Sonnet | Research solutions across GitHub issues, forums, and documentation |
| **Docs Writer** | — | Create or update README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING docs |

### Hidden Subagents (invoked by 03 Phase - Execute)

These agents are not visible in the picker. They run automatically as part of the Phase - Execute pipeline with `user-invocable: false`.

| Agent | Purpose |
|-------|---------|
| **Feature - Decomposer** | Decompose a phase into independent features with 3-file plan sets |
| **Feature - Implementer** | Implement a feature plan using Red-Green-Refactor TDD |
| **Feature - Reviewer** | Review implementation, apply fixes, produce review record |
| **Feature - QA Writer** | Write manual QA plan for non-automatable test cases |

---

## What Each Agent Does

**01 Project - Planner** (document-only — does not write code)
> Give it a project scope or high-level goal. It iterates with you to produce a phased roadmap (`docs/phases/PHASES_OVERVIEW.md` and individual `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` files). Each phase document is self-contained and designed to be handed to the Phase - Refiner. It will not create any files until you explicitly approve.

**02 Phase - Refiner** (document-only — does not write code)
> Give it a single Phase document from the 01 Project - Planner. It iterates with you to refine scope, probe edge cases, surface hidden dependencies, stress-test decomposition readiness, and walk through user flows — deepening the Phase document until it's fully ready for automated execution. It updates the Phase document in place and will not write changes until you explicitly approve.

**03 Phase - Execute** (orchestrator — delegates to subagents)
> Give it a refined Phase document. It decomposes the phase into features, then runs the implement → review → QA cycle for each feature automatically. After all features complete, it runs the Phase - Final Review and reports GO / NO-GO back to you. No user interaction required after launch.

**Feature - Decomposer** *(hidden subagent)* — Reads a phase doc, scans the codebase for context, and writes structured plans with numbered acceptance criteria, architecture analysis, and test strategy to `dev/[task-name]/` for each independent feature.

**Feature - Implementer** *(hidden subagent)* — Reads plan docs from `dev/[task-name]/`, implements each acceptance criterion using Red-Green-Refactor TDD, and writes `[task-name]-implementation.md` mapping changes to acceptance criteria.

**Feature - Reviewer** *(hidden subagent)* — Reads plan and implementation docs, reviews all changed code, applies fixes for High/Blocker issues directly, and writes `[task-name]-review.md` with verdict and remaining concerns.

**Feature - QA Writer** *(hidden subagent)* — Reads all pipeline docs, identifies what can't be verified by automated tests, and writes `[task-name]-qa.md` — an execution-ready checklist with concrete steps and expected results.

**Phase - Final Review** (document-only — does not modify code)
> Cross-validates all pipeline documents across all features in the phase, verifies the actual code matches the records, runs the test suite, and produces a **GO / GO WITH CONDITIONS / NO-GO** verdict with a full traceability matrix and risk register. Can be invoked standalone or automatically by the orchestrator.

**Test - Writer** (writes test code only — does not modify source)
> Give it a module or directory to cover. It scans the codebase, proposes a test plan, and writes working test files and configuration. Verifies the suite passes before finishing.

**Test - Analyst** (document-only — does not modify tests)
> Give it a test directory to analyze. It classifies tests by value, flags redundancy and over-mocking, and writes a categorized inventory with a staged reduction plan.

**Auditor - Code** (document-only — does not modify code)
> Give it a codebase or specific files. Audits every file for cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report.

**Refactor** (full tool access — reads and writes code)
> Give it a codebase area to reorganize. Maps dependencies, executes file moves and extractions, updates all imports. Verifies no breakage after each step.

**Debugger - Frontend** / **Debugger - Backend** (full tool access — reads and writes code)
> Give it an error message or description. Classifies the error, investigates, and applies minimal targeted fixes.

**Web Researcher** (read-only — uses fetch)
> Give it a problem or topic. Searches across GitHub issues, Stack Overflow, Reddit, forums, and docs. Compiles a structured findings report with sources.

**Auditor - Infra** (document-only — does not modify files)
> Give it infrastructure files to audit. Evaluates Dockerfiles, CI/CD pipelines, IaC templates, and config files for security, best practices, and operational risk.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. Produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING documents.

---

## Other Pipelines

These pipelines use agents manually in sequence. Each step runs in a new chat context.

### Test Suite Bootstrap

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Test - Writer** | "Bootstrap tests for `[directory or module]`" |
| 2 | **Test - Analyst** | "Evaluate the test suite" |

### Test Suite Cleanup

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Test - Analyst** | "Analyze the test suite in `[test directory]`" |
| 2 | **03 Phase - Execute** | Use with a plan that addresses the analyst's recommendations |

### Code Quality Improvement

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Auditor - Code** | "Audit the codebase" (or specify a directory) |
| 2 | **03 Phase - Execute** | Use with a plan that addresses the audit findings |

### Refactoring

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Auditor - Code** | "Audit `[area]` for structural issues" |
| 2 | **Refactor** | "Refactor based on the audit findings" |

### Bug Investigation and Fix

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Web Researcher** | Describe the error message or behavior |
| 2 | **Debugger - Frontend** or **Debugger - Backend** | "Investigate and fix the error" |

### Documentation Overhaul

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Auditor - Code** | "Audit the codebase" |
| 2 | **Auditor - Infra** | "Audit infrastructure files" (optional) |
| 3 | **Docs Writer** | "Create documentation for the repo" |

### Infrastructure Audit & Remediation

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Auditor - Infra** | "Audit infrastructure files" |
| 2 | **03 Phase - Execute** | Use with a plan that addresses the infrastructure findings |

---

## Standalone Usage

Not everything needs a pipeline. These agents work well on their own:

- **Phase - Final Review** — Point at any `dev/[task-name]/` folder for an independent readiness check
- **Auditor - Code** or **Auditor - Infra** — Run anytime for a health check
- **Test - Analyst** — Evaluate test quality during maintenance windows
- **Web Researcher** — Research a technical question or debug a tricky issue
- **Docs Writer** — Update documentation after any significant change
- **Debugger - Frontend** or **Debugger - Backend** — Fix a specific error without a full pipeline

---

## Task Documentation Pattern

The pipeline subagents produce output in the `dev/[task-name]/` directory. After a full feature cycle, the folder contains:

```
dev/[task-name]/
├── [task-name]-plan.md              # Plan with stages (Feature - Decomposer)
├── [task-name]-context.md           # Key files, decisions, constraints (Feature - Decomposer)
├── [task-name]-tasks.md             # Checklist of work items (Feature - Decomposer)
├── [task-name]-implementation.md    # Files changed, AC traceability (Feature - Implementer)
├── [task-name]-review.md            # Verdict, issues, fixes applied (Feature - Reviewer)
└── [task-name]-qa.md                # Manual QA checklist (Feature - QA Writer)
```

The **Phase - Final Review** writes its readiness analysis to:

```
dev/[phase-name]-qa-analysis.md      # GO/NO-GO verdict, traceability matrix, risk register
```

Audit agents (**Auditor - Code**, **Auditor - Infra**) produce reports in:

```
dev/[audit-name]/
├── [audit-name]-report.md           # Full structured findings
└── [audit-name]-summary.md          # Executive summary with priority actions
```

---

## VS Code Settings

The orchestrator uses subagents. Ensure these settings are configured:

- **`chat.subagents.allowInvocationsFromSubagents`**: Leave at `false` (default) — subagents don't need to spawn further subagents.
- The orchestrator's `agents:` frontmatter restricts which subagents it can invoke, preventing unintended delegation.

---

## Adding Agents to Another Project

Each agent file is standalone. To use these agents in a different repository:

1. Create a `.github/agents/` directory in the target repo.
2. Copy the agent `.md` files you want into that directory.
3. That's it — VS Code will discover them automatically.

For the project pipeline, copy all files including the hidden subagents. For standalone use, copy only the agents you need.

---

## Integration Notes

- **Language-agnostic**: These agents are generic. They read your workspace's `AGENTS.md` at runtime for language-specific conventions (naming, testing tools, formatting, etc.).
- **Self-contained**: Each agent file works standalone — just copy the `.md` file into any project's `.github/agents/` directory.
- **Orchestrator pattern**: **03 Phase - Execute** delegates to hidden subagents with `user-invocable: false`. These appear as collapsible tool calls in the chat UI.
- **Subagent autonomy**: Hidden subagents operate without user confirmation — they read inputs from `dev/[task-name]/`, execute their role, write outputs to the same folder, and return a summary to the orchestrator.
- **Read-only agents**: **Phase - Final Review**, **Auditor - Code**, **Auditor - Infra**, and **Test - Analyst** do not modify code. They analyze and report only.
- **Approval-gated agents**: **01 Project - Planner** and **02 Phase - Refiner** always present findings and ask for explicit approval before creating files.
- **Code-writing agents**: **Refactor**, **Test - Writer**, **Debugger - Frontend**, and **Debugger - Backend** have full tool access to create and modify files.
