# Claude Agents

Specialized agents for structured software development workflows, configured for the **Claude Code CLI**. The core workflow uses an **orchestrator + subagent** pattern — you interact with a few agents, and the orchestrator drives the rest automatically. A **manual implementation path** is also available for users who prefer to write their own code.

---

## Setup

Before using these agents, wire the repository into your local Claude config. See [SYMLINK_SETUP.md](SYMLINK_SETUP.md) for full instructions. The short version:

```bash
# 1. Create repo-level symlinks (from the repo root)
cd claude
ln -sfn ../.github/skills skills
ln -sfn ../.github/learnings learnings

# 2. Link agents into ~/.claude one file at a time
mkdir -p ~/.claude
rm -f ~/.claude/agents
mkdir -p ~/.claude/agents
for src in /path/to/github-agents-source-of-truth/claude/agents/*; do
   ln -sfn "$src" "$HOME/.claude/agents/$(basename "$src")"
done

# 3. Link shared directories into ~/.claude
ln -sfn /path/to/github-agents-source-of-truth/claude/skills ~/.claude/skills
ln -sfn /path/to/github-agents-source-of-truth/claude/learnings ~/.claude/learnings
```

---

## How to Use an Agent

### 1. Start Claude Code

```bash
claude
```

### 2. spawn an agent by name

Use `@agent-name` in the conversation to route your request to a specific agent:

```
@01-project-planner Describe my project scope and goals
@02-phase-refiner Refine and deepen this Phase document [attach file]
@04-phase-execute Execute this phase [attach refined phase doc]
```

### 3. List available agents

```
/agents
```

### 4. Review the output

Each agent produces structured output — plan documents, implementation summaries, review tables, audit reports, etc.

---

## The Project Pipeline (3 user steps)

The core development workflow. **You interact with steps 1–3. Everything else is automated.**

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU                                                            │
│                                                                 │
│  Step 1: @01-project-planner    → Phase documents               │
│  Step 2: @02-phase-refiner      → Refined phase document        │
│  Step 3: @04-phase-execute      → Hands-free from here ──┐     │
│                                                             │    │
└─────────────────────────────────────────────────────────────│────┘
                                                              │
┌─────────────────────────────────────────────────────────────│────┐
│  AUTOMATED (subagents)                                      │    │
│                                                             ▼    │
│  @03-feature-decomposer → Numbered plan sets (01-, 02-, ...)     │
│                                                                   │
│  BATCH MODE (all features, one branch):                           │
│  ┌──────────────────────────────────────────────┐                │
│  │  FOR EACH FEATURE (in 0N order):             │                │
│  │  @z-feature-implementer → Code + tests       │                │
│  │  @z-feature-reviewer    → Review + fixes     │                │
│  │  Loop back for next feature                  │                │
│  └──────────────────────────────────────────────┘                │
│  @z-feature-qa-writer   → Consolidated QA plan               │
│  @prod-code-review      → GO / NO-GO verdict                  │
│                                                                   │
│  PER-FEATURE MODE (one feature, one branch, one PR):             │
│  ┌──────────────────────────────────────────────┐                │
│  │  @z-feature-implementer → Code + tests       │                │
│  │  @z-feature-reviewer    → Review + fixes     │                │
│  │  @z-feature-qa-writer   → QA for this feature │               │
│  │  @prod-code-review      → GO / NO-GO verdict │                │
│  └──────────────────────────────────────────────┘                │
│  → "Merge this PR, then re-spawn for next feature"              │
│                                                                   │
│  @docs-writer  → Update stale documentation                   │
│                                                                   │
│  ──► Report back to you                                          │
└───────────────────────────────────────────────────────────────────┘
```

### Step 1: Plan the Project

| Agent | Invocation | Output |
|-------|-----------|--------|
| **01-project-planner** | `@01-project-planner` + describe your project scope and goals | Phase documents in `docs/phases/` |

Interactive — you iterate with the planner to define phases and milestones.

### Step 2: Refine a Phase

| Agent | Invocation | Output |
|-------|-----------|--------|
| **02-phase-refiner** | `@02-phase-refiner` + "Refine and deepen this Phase document" + attach phase doc | Updated phase document |

Interactive — you iterate to probe edge cases, dependencies, and decomposition readiness.

### Step 3: Execute the Phase

| Agent | Invocation | Output |
|-------|-----------|--------|
| **04-phase-execute** | `@04-phase-execute` + "Execute this phase" + attach refined phase doc | All features implemented, reviewed, QA'd |

**Hands-free from here.** The orchestrator asks whether you want **batch mode** (all features on one branch) or **per-feature mode** (one branch per feature), then automatically:

1. Decomposes the phase into numbered features (via `@03-feature-decomposer`)
2. Expands plans with context and tasks (via `@z-feature-plan-expander`)
3. For each feature (or the next unimplemented feature in per-feature mode), runs the full cycle:
   - **Implement** → Red-Green-Refactor TDD, writes implementation record
   - **Review** → Finds bugs, applies fixes, writes review record
4. Runs `@z-feature-qa-writer` (consolidated in batch mode, per-feature in per-feature mode)
5. Runs `@prod-code-review` across all features (batch) or the single feature (per-feature)
6. Reports the verdict back to you
7. Runs `@docs-writer` to update any stale documentation

**Batch mode:** After completion, push the branch and open a PR for final human review.

**Per-feature mode:** After each feature, push the feature branch and open a PR. Once merged, re-spawn `@04-phase-execute` with the same phase document — it detects completed features and picks up the next one.

### Manual Implementation Path

Prefer to write your own code? Use the planning agents, then implement yourself:

```
Step 1: @01-project-planner    → Phase documents
Step 2: @02-phase-refiner      → Refined phase document
Step 3: @03-feature-decomposer → Feature plans (optional)
Step 4: (you write the code from the plans)
Step 5: @prod-code-review      → Validates your code against the plans
```

**Tip:** For structured feature decomposition without automated execution, use `@03-feature-decomposer` directly — it creates numbered plan files in `dev/feature/[0N-task-name]/` that you can implement at your own pace.

---

## Available Agents

### User-Facing

| Agent name | Invocation | Purpose |
|-----------|-----------|---------|
| **01-project-planner** | `@01-project-planner` | Create a project roadmap broken into phases |
| **02-phase-refiner** | `@02-phase-refiner` | Refine and deepen an individual Phase document |
| **03-feature-decomposer** | `@03-feature-decomposer` | Break a phase into features with structured plan files |
| **04-phase-execute** | `@04-phase-execute` | Orchestrate full phase execution — decompose, implement, review, QA |
| **eval-grader** | `@eval-grader` | Score a completed phase run from ledger files plus a rubric YAML and write a structured report |
| **audit-code-infra-refactor** | `@audit-code-infra-refactor` | Orchestrate code, infrastructure, or structural audits with optional automated fix pipeline |
| **debugger** | `@debugger` | Diagnose and fix frontend or backend application errors |
| **docs-writer** | `@docs-writer` | Create or update repo documentation; also spawnd automatically by orchestrators |
| **prod-code-review** | `@prod-code-review` | Final pre-production readiness gate (also usable standalone) |
| **test-orchestrator** | `@test-orchestrator` | Orchestrate test analysis, writing, or fixing with optional remediation pipeline |
| **unity-reviewer** | `@unity-reviewer` | Review Unity C# code for architecture, performance, style, and Unity-specific pitfalls |
| **web-researcher** | `@web-researcher` | Research a topic and produce a structured findings report saved to `dev/research/[topic-name]/` |

### Subagents (`z-` prefix)

These agents run automatically as part of orchestrator pipelines. They are prefixed with `z-` to sort them to the bottom of the `/agents` list and signal they should not be spawnd directly.

| Agent name | spawnd By | Purpose |
|-----------|-----------|---------|
| **z-auditor-code** | `@audit-code-infra-refactor` | Comprehensive code quality, security, and health audit |
| **z-auditor-infra** | `@audit-code-infra-refactor` | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **z-auditor-refactor** | `@audit-code-infra-refactor` | Audit codebase structure, module organization, and architecture |
| **z-feature-plan-expander** | `@04-phase-execute` | Generate context and tasks files from existing plan files |
| **z-feature-implementer** | `@04-phase-execute`, audit, test orchestrators | Implement a feature plan using Red-Green-Refactor TDD |
| **z-feature-reviewer** | `@04-phase-execute`, audit, test orchestrators | Review implementation, apply fixes, produce review record |
| **z-feature-qa-writer** | `@04-phase-execute`, `@audit-code-infra-refactor` | Write manual QA plan for non-automatable test cases |
| **z-test-analyst** | `@test-orchestrator` | Evaluate test suite for redundancy, coverage gaps, and consolidation |
| **z-test-fixer** | `@test-orchestrator` | Diagnose and fix broken tests without modifying source code |
| **z-test-writer** | `@test-orchestrator` | Bootstrap a test suite from scratch for untested code |
| **z-git-commit** | `@04-phase-execute`, audit, test orchestrators | Create an atomic Git commit with a conventional commit message |

---

## What Each Agent Does

### User-Facing Agents

**`@01-project-planner`** (document-only — does not write code)
> Give it a project scope or high-level goal. It iterates with you to produce a phased roadmap (`docs/phases/PROJECT_ROADMAP.md` and individual `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` files). It will not create any files until you explicitly approve.

**`@02-phase-refiner`** (document-only — does not write code)
> Give it a single Phase document. It iterates with you to refine scope, probe edge cases, surface hidden dependencies, stress-test decomposition readiness, and walk through user flows. It will not write changes until you explicitly approve.

**`@03-feature-decomposer`** (document-only — does not write code)
> Give it a refined Phase document or describe a feature. It scans the codebase, decomposes the work into independent features, and writes a structured `-plan.md` file for each to `dev/feature/[0N-task-name]/`. Also spawnd automatically by `@04-phase-execute` when plans are missing.

**`@04-phase-execute`** (orchestrator — delegates to subagents)
> Give it a refined Phase document. It checks for existing plans (invoking `@03-feature-decomposer` if missing), expands plans, then asks whether to run in **batch mode** or **per-feature mode**. Delegates all implementation, review, QA, and documentation to subagents. No user interaction required after initial mode selection.

**`@eval-grader`** (user-facing — standalone scorer)
> Give it a rubric YAML path plus a target phase run. The rubric should follow the grader schema documented in the agent, with `eval/rubrics/phase-eval-infrastructure-foundation.example.yaml` as the seed example. The grader reads `eval/runs/<phase-slug>/ledger-commits.jsonl` and `eval/runs/<phase-slug>/ledger-events.jsonl`, correlates semantic events onto the commit timeline by SHA association, scores every automatable rubric criterion, flags manual checks as `[NEEDS_HUMAN_REVIEW]`, and writes `score-report-<timestamp>.md` into the same run directory without pausing for user confirmation.

**`@audit-code-infra-refactor`** (orchestrator — delegates to subagents)
> Asks which audit type to run (CODE, INFRA, or REFACTOR), delegates to the appropriate `@z-auditor-*` subagent, and presents findings. Optionally drives automated remediation through the feature pipeline.

**`@test-orchestrator`** (orchestrator — delegates to subagents)
> Asks which test operation to run (ANALYZE, WRITE, or FIX), delegates to the appropriate `@z-test-*` subagent, and presents results. Optionally drives remediation through the implementation pipeline.

**`@debugger`** (full tool access — reads and writes code)
> Give it an error message or description — frontend or backend. Triages the issue, classifies it (build-time, runtime, database, dependency, etc.), investigates, and applies minimal targeted fixes.

**`@prod-code-review`** (document-only — does not modify code)
> Cross-validates all pipeline documents across all features in the phase, verifies the actual code matches the records, runs the test suite, and produces a **GO / GO WITH CONDITIONS / NO-GO** verdict with a full traceability matrix and risk register.

**`@web-researcher`** (read-only — uses web fetch and search)
> Give it a problem or topic. Searches across GitHub issues, Stack Overflow, Reddit, forums, and docs. Produces two deliverable documents saved to `dev/research/[topic-name]/`: a full structured findings report and an executive summary. Every factual claim traces back to a numbered citation.

**`@docs-writer`** (reads codebase, writes documentation)
> Give it a repo to document. Produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT, and TROUBLESHOOTING documents. Also spawnd automatically at the end of orchestrator pipelines.

**`@unity-reviewer`** (read-only — does not modify code)
> Give it Unity C# source files or a directory to review. Loads Unity-specific skills (MonoBehaviour lifecycle, UI Toolkit pitfalls, performance rules, design patterns, style guide compliance) and produces structured review findings.

---

## Other Pipelines

### Code Quality Improvement

```
@audit-code-infra-refactor → select CODE → accept remediation
```

### Structural Refactoring

```
@audit-code-infra-refactor → select REFACTOR → accept remediation
```

### Test Suite Bootstrap & Cleanup

```
@test-orchestrator → select WRITE, ANALYZE, or FIX
```

### Bug Investigation and Fix

```
@web-researcher    "Describe the error or behavior"
@debugger          "Investigate and fix the error"
```

### Infrastructure Audit

```
@audit-code-infra-refactor → select INFRA → accept remediation
```

---

## Standalone Usage

These agents work well without a full pipeline:

- `@audit-code-infra-refactor` — Run anytime for a code, infrastructure, or structural health check
- `@test-orchestrator` — Analyze, write, or fix tests on demand
- `@prod-code-review` — Point at any `dev/feature/[0N-task-name]/` folder for an independent readiness check
- `@debugger` — Fix a specific error without a full pipeline
- `@unity-reviewer` — Review Unity C# code for architecture, performance, and pitfalls
- `@web-researcher` — Research a technical question or debug a tricky issue
- `@docs-writer` — Update documentation after any significant change

---

## Task Documentation Pattern

Pipeline subagents produce output in `dev/feature/[0N-task-name]/`:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md              # Plan with stages (@03-feature-decomposer)
├── [0N-task-name]-context.md           # Key files, decisions, constraints (@z-feature-plan-expander)
├── [0N-task-name]-tasks.md             # Checklist of work items (@z-feature-plan-expander)
├── [0N-task-name]-implementation.md    # Files changed, AC traceability (@z-feature-implementer)
└── [0N-task-name]-review.md            # Verdict, issues, fixes applied (@z-feature-reviewer)
```

**Batch mode QA** — single consolidated document:

```
docs/phases/[phase-name]/[phase-name]_QA.md
docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md
```

**Per-feature mode QA** — written inside the feature directory:

```
dev/feature/[0N-task-name]/[0N-task-name]-qa.md
dev/feature/[0N-task-name]/[0N-task-name]-coverage-map-qa.md
dev/feature/[0N-task-name]/[0N-task-name]-qa-analysis.md
```

Audit agents produce reports in:

```
dev/[audit-name]/
├── [audit-name]-report.md
└── [audit-name]-summary.md
```

---

## Skills and Learnings

Agents load **skills** (`claude/skills/<name>/SKILL.md`) for shared templates and formats on demand. Skills are a symlink to `.github/skills/` — the source-of-truth is always in `.github/`.

**Learnings** (`claude/learnings/*.md`) are persistent notes from prior sessions loaded automatically by the implementer, reviewer, decomposer, and debugger agents. Also a symlink to `.github/learnings/`.

---

## Adding Agents to Another Project

Each agent file is standalone. To use these agents in a different repository:

1. Copy the `claude/agents/` directory into the target repo.
2. Wire symlinks for skills and learnings following [SYMLINK_SETUP.md](SYMLINK_SETUP.md).
3. Update the `~/.claude` symlinks to point at the new location.
