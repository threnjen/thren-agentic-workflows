# Agents

Specialized agents for structured software development workflows. The core workflow uses an **orchestrator + subagent** pattern — you interact with a few agents, and the orchestrator drives the rest automatically. A **manual implementation path** is also available for users who prefer to write their own code.

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
│  Prod Code Review   → GO / NO-GO verdict                     │
│  Docs Writer        → Update stale documentation              │
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
3. Runs the **Prod Code Review** across all features
4. Reports the verdict back to you
5. Runs the **Docs Writer** to update any stale documentation

**After completion:** Push the branch and open a PR for final human review.

### Manual Implementation Path

Prefer to write your own code? Use the planning agents, then implement yourself:

```
Step 1: 01 Project - Planner    → Phase documents
Step 2: 02 Phase - Refiner       → Refined phase document
Step 3: (you write the code from the refined phase doc)
Step 4: Prod Code Review     → Validates your code against the plans
```

The refined Phase document from Step 2 contains detailed scope, requirements, and acceptance criteria — enough to implement directly. When you're ready for validation, run **Prod Code Review** to check your work against the plan.

**Tip:** If you want structured feature decomposition before implementing, launch **03 Phase - Execute** with your refined phase doc — it will create detailed feature plans in `dev/feature/[task-name]/` via the Feature - Decomposer subagent. You can then implement from those plans at your own pace.

---

## Available Agents

### User-Facing (in agent picker)

| Agent | Model | Purpose |
|-------|-------|---------|
| **01 Project - Planner** | Opus | Create a project roadmap broken into phases |
| **02 Phase - Refiner** | Opus | Refine and deepen an individual Phase document |
| **03 Phase - Execute** | Opus | Orchestrate full phase execution — decompose, implement, review, QA |
| **Audit - Code, Infra, Refactor** | Opus | Orchestrate code, infrastructure, or structural audits with optional automated fix pipeline |
| **Debugger** | Opus | Diagnose and fix frontend or backend application errors |
| **Docs Writer** | — | Create or update repo documentation; also invoked automatically by orchestrators after pipeline completion |
| **Prod Code Review** | Opus | Final pre-production readiness gate (also usable standalone) |
| **Test - Orchestrator** | Opus | Orchestrate test analysis, writing, or fixing with optional remediation pipeline |
| **Web Researcher** | Opus | Research solutions across GitHub issues, forums, and documentation |

### Hidden Subagents

These agents are not visible in the picker. They run automatically as part of orchestrator pipelines with `user-invocable: false`.

| Agent | Invoked By | Purpose |
|-------|------------|---------|
| **Auditor - Code** | Audit orchestrator | Comprehensive code quality, security, and health audit |
| **Auditor - Infra** | Audit orchestrator | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **Auditor - Refactor** | Audit orchestrator | Audit codebase structure, module organization, and architecture |
| **Feature - Decomposer** | Phase - Execute | Decompose a phase into features with structured plans |
| **Feature - Implementer** | Phase - Execute, Audit orchestrator, Test orchestrator | Implement a feature plan using Red-Green-Refactor TDD |
| **Feature - Reviewer** | Phase - Execute, Audit orchestrator, Test orchestrator | Review implementation, apply fixes, produce review record |
| **Feature - QA Writer** | Phase - Execute, Audit orchestrator | Write manual QA plan for non-automatable test cases |
| **Test - Analyst** | Test orchestrator | Evaluate test suite for redundancy, coverage gaps, and consolidation |
| **Test - Fixer** | Test orchestrator | Diagnose and fix broken tests without modifying source code |
| **Test - Writer** | Test orchestrator | Bootstrap a test suite from scratch for untested code |

---

## What Each Agent Does

### User-Facing Agents

**01 Project - Planner** (document-only — does not write code)
> Give it a project scope or high-level goal. It iterates with you to produce a phased roadmap (`docs/phases/PHASES_OVERVIEW.md` and individual `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` files). Each phase document is self-contained and designed to be handed to the Phase - Refiner. It will not create any files until you explicitly approve.

**02 Phase - Refiner** (document-only — does not write code)
> Give it a single Phase document from the 01 Project - Planner (or describe a standalone feature). It iterates with you to refine scope, probe edge cases, surface hidden dependencies, stress-test decomposition readiness, and walk through user flows — deepening the Phase document until it's fully ready for automated execution. It updates the Phase document in place and will not write changes until you explicitly approve.

**03 Phase - Execute** (orchestrator — delegates to subagents)
> Give it a refined Phase document. It decomposes the phase into features, then runs the implement → review → QA cycle for each feature automatically. After all features complete, it runs the Prod Code Review, reports GO / NO-GO back to you, and updates documentation via the Docs Writer. No user interaction required after launch.

**Audit - Code, Infra, Refactor** (orchestrator — delegates to subagents)
> Asks which audit type to run (CODE, INFRA, or REFACTOR), delegates to the appropriate auditor subagent, and presents findings. Optionally drives automated remediation by converting audit findings into task plans and running them through the Feature - Implementer → Feature - Reviewer → Feature - QA Writer pipeline. After remediation, updates documentation via the Docs Writer.

**Test - Orchestrator** (orchestrator — delegates to subagents)
> Asks which test operation to run (ANALYZE, WRITE, or FIX), delegates to the appropriate test subagent, and presents results. Optionally drives remediation of findings through the Feature - Implementer → Feature - Reviewer pipeline. After remediation, updates documentation via the Docs Writer.

**Debugger** (full tool access — reads and writes code)
> Give it an error message or description — frontend or backend. Triages the issue, classifies it (build-time, runtime, database, dependency, etc.), investigates, and applies minimal targeted fixes. Handles both frontend (TypeScript, React, build tools) and backend (Node.js, Python, databases, auth) errors.

**Prod Code Review** (document-only — does not modify code)
> Cross-validates all pipeline documents across all features in the phase, verifies the actual code matches the records, runs the test suite, and produces a **GO / GO WITH CONDITIONS / NO-GO** verdict with a full traceability matrix and risk register. Can be invoked standalone or automatically by the orchestrator.

**Web Researcher** (read-only — uses fetch and web search)
> Give it a problem or topic. Searches across GitHub issues, Stack Overflow, Reddit, forums, and docs. Compiles a structured findings report with sources.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. Produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING documents. Also invoked automatically at the end of orchestrator pipelines to update stale documentation after code changes.

### Hidden Subagents

**Feature - Decomposer** *(subagent of Phase - Execute)* — Scans the codebase for context and writes structured plans with numbered acceptance criteria, architecture analysis, and test strategy to `dev/feature/[task-name]/` for each independent feature.

**Feature - Implementer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads plan docs from `dev/feature/[task-name]/`, implements each acceptance criterion using Red-Green-Refactor TDD, and writes `[task-name]-implementation.md` mapping changes to acceptance criteria.

**Feature - Reviewer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads plan and implementation docs, reviews all changed code, applies fixes for High/Blocker issues directly, and writes `[task-name]-review.md` with verdict and remaining concerns.

**Feature - QA Writer** *(subagent of Phase - Execute, Audit orchestrator)* — Reads all pipeline docs from every feature in a phase, identifies what can't be verified by automated tests, and writes a single consolidated QA plan with an execution-ready checklist. The QA doc is written to `docs/phases/` (or a fallback path) rather than per-feature.

**Auditor - Code** *(subagent of Audit orchestrator)* — Audits every source file for cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report.

**Auditor - Infra** *(subagent of Audit orchestrator)* — Evaluates Dockerfiles, CI/CD pipelines, IaC templates, and config files for security, best practices, and operational risk.

**Auditor - Refactor** *(subagent of Audit orchestrator)* — Evaluates codebase-level organization: module structure, dependency graphs, component decomposition, coupling, cohesion, and separation of concerns.

**Test - Analyst** *(subagent of Test orchestrator)* — Classifies tests by value, flags redundancy and over-mocking, and writes a categorized inventory with a staged reduction plan.

**Test - Writer** *(subagent of Test orchestrator)* — Bootstraps a test suite from scratch. Scans the codebase, creates test files with meaningful coverage, and verifies the suite passes.

**Test - Fixer** *(subagent of Test orchestrator)* — Diagnoses and fixes broken tests. Updates assertions, mocks, fixtures, and configuration to get a failing suite back to green — never modifies source code.

---

## Other Pipelines

The **Audit** and **Test** orchestrators handle most multi-step workflows internally. These pipelines combine agents across different concerns.

### Code Quality Improvement

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor** | "Audit the codebase" → select CODE, accept remediation |

The audit orchestrator runs the code audit, presents findings, and offers to implement fixes automatically through the feature pipeline.

### Structural Refactoring

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor** | "Audit the codebase" → select REFACTOR, accept remediation |

The audit orchestrator runs the structural audit, presents findings, and offers to implement fixes automatically through the feature pipeline.

### Test Suite Bootstrap & Cleanup

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Test - Orchestrator** | "Work on my test suite" → select WRITE, ANALYZE, or FIX |

The test orchestrator handles analysis, writing, and fixing. It can optionally drive remediation of findings through the implementation pipeline.

### Bug Investigation and Fix

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Web Researcher** | Describe the error message or behavior |
| 2 | **Debugger** | "Investigate and fix the error" |

### Documentation Overhaul

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor** | "Audit the codebase" (optional — for context gathering) |
| 2 | **Docs Writer** | "Create documentation for the repo" |

### Infrastructure Audit & Remediation

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor** | "Audit the codebase" → select INFRA, accept remediation |

---

## Standalone Usage

Not everything needs a pipeline. These agents work well on their own:

- **Audit - Code, Infra, Refactor** — Run anytime for a code, infrastructure, or structural health check
- **Test - Orchestrator** — Analyze, write, or fix tests on demand
- **Prod Code Review** — Point at any `dev/feature/[task-name]/` folder for an independent readiness check
- **Debugger** — Fix a specific frontend or backend error without a full pipeline
- **Web Researcher** — Research a technical question or debug a tricky issue
- **Docs Writer** — Update documentation after any significant change

---

## Task Documentation Pattern

The pipeline subagents produce output in the `dev/feature/[task-name]/` directory. After a full feature cycle, the folder contains:

```
dev/feature/[task-name]/
├── [task-name]-plan.md              # Plan with stages (Feature - Decomposer)
├── [task-name]-context.md           # Key files, decisions, constraints (Feature - Decomposer)
├── [task-name]-tasks.md             # Checklist of work items (Feature - Decomposer)
├── [task-name]-implementation.md    # Files changed, AC traceability (Feature - Implementer)
└── [task-name]-review.md            # Verdict, issues, fixes applied (Feature - Reviewer)
```

The **Feature - QA Writer** produces a single consolidated QA document covering ALL features in the phase:

```
docs/phases/[phase-name]/[phase-name]_QA.md                # Consolidated manual QA checklist
docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md   # AC coverage map (automated vs manual)
```

If `docs/phases/` does not exist, the QA doc falls back to `dev/feature/[phase-name]-qa.md`.

The **Prod Code Review** writes its readiness analysis to:

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

## Skills and Instructions

Agents reference **skills** (`.github/skills/<name>/SKILL.md`) for shared templates and formats that would otherwise be duplicated. Skills are loaded on demand when an agent's instructions say "Load the `<name>` skill."

| Skill | Used By | Purpose |
|-------|---------|---------|
| `phase-document-writing` | 01 Project - Planner, 02 Phase - Refiner | Phase Document Template, Phases Overview Template, quality checklist |
| `audit-report-format` | Auditor - Code, Auditor - Infra, Auditor - Refactor | Report structure, findings table format, severity levels, priority tiers |
| `feature-plan-set` | Feature - Decomposer | Three-file plan convention, plan sections A–F, stage format, decomposition rules |

**Instructions** (`.github/instructions/*.instructions.md`) inject cross-cutting conventions into agents automatically via `applyTo` glob patterns.

| Instruction | Applies To | Purpose |
|-------------|-----------|---------|
| `dev-task-folder` | `.github/agents/**` | Standardizes `dev/feature/[task-name]/` naming and file suffix conventions |

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
- **Three orchestrators**: **03 Phase - Execute**, **Audit - Code, Infra, Refactor**, and **Test - Orchestrator** all delegate to hidden subagents marked `user-invocable: false`. These appear as collapsible tool calls in the chat UI.
- **Shared subagents**: **Feature - Implementer** and **Feature - Reviewer** are used by all three orchestrators. **Feature - QA Writer** is used by Phase - Execute and the Audit orchestrator. **Docs Writer** is invoked by all three orchestrators at the end of the pipeline to update stale documentation (it remains user-invocable for standalone use as well).
- **Subagent autonomy**: Hidden subagents operate without user confirmation — they read inputs from `dev/feature/[task-name]/`, execute their role, write outputs to the same folder, and return a summary to the orchestrator.
- **Read-only subagents**: **Auditor - Code**, **Auditor - Infra**, **Auditor - Refactor**, and **Test - Analyst** do not modify code. They analyze and report only.
- **Approval-gated agents**: **01 Project - Planner** and **02 Phase - Refiner** always present findings and ask for explicit approval before creating files. They also check for missing critical documentation (`README.md`, `docs/CODEBASE_CONTEXT.md`) and recommend running the **Docs Writer** before continuing. The **Audit** and **Test** orchestrators ask before proceeding to the remediation phase.
- **Code-writing agents**: **Debugger**, **Test - Writer**, **Test - Fixer**, **Feature - Implementer**, and **Feature - Reviewer** have full tool access to create and modify files.
- **Prod Code Review** does not modify code — it analyzes and reports only, producing a GO / NO-GO verdict.
