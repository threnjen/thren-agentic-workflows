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
│  Step 3: 04 Phase - Execute      → Hands-free from here ──┐    │
│                                                             │    │
└─────────────────────────────────────────────────────────────│────┘
                                                              │
┌─────────────────────────────────────────────────────────────│────┐
│  AUTOMATED (subagents)                                      │    │
│                                                             ▼    │
│  Feature - Decomposer  → Numbered plan sets (01-, 02-, ...)      │
│                                                                   │
│  BATCH MODE (all features, one branch):                           │
│  ┌──────────────────────────────────────────────┐                │
│  │  FOR EACH FEATURE (in 0N order):             │                │
│  │  Feature - Implementer  → Code + tests       │                │
│  │  Feature - Reviewer     → Review + fixes     │                │
│  │  Loop back for next feature                  │                │
│  └──────────────────────────────────────────────┘                │
│  Feature - QA Writer    → Consolidated QA plan                │
│  04e Diff Security Scan → Diff-scoped security report         │
│  Prod Code Review       → GO / NO-GO verdict                  │
│                                                                   │
│  PER-FEATURE MODE (one feature, one branch, one PR):             │
│  ┌──────────────────────────────────────────────┐                │
│  │  Feature - Implementer  → Code + tests       │                │
│  │  Feature - Reviewer     → Review + fixes     │                │
│  │  Feature - QA Writer    → QA for this feature │                │
│  │  Prod Code Review       → GO / NO-GO verdict │                │
│  └──────────────────────────────────────────────┘                │
│  → "Merge this PR, then re-spawn for next feature"              │
│                                                                   │
│  Docs Writer        → Update stale documentation              │
│                                                                   │
│  ──► Report back to you                                          │
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
| **04 Phase - Execute** | "Execute this phase" + attach refined phase doc | All features implemented, reviewed, QA'd |

**Hands-free from here.** `04 Phase - Execute` expects `03 Feature - Decomposer` to have already prepared the feature bundles and execution manifest. Once those files exist, the orchestrator automatically:

1. Reads `dev/feature/[phase-name]-execution-manifest.md`
2. Verifies each listed feature has `-plan.md`, `-context.md`, and `-tasks.md`
3. Fails immediately if those prepared artifacts are missing, instead of invoking planning agents
4. For each feature in manifest wave order, runs the full cycle:
   - **Implement** → Red-Green-Refactor TDD, writes implementation record
   - **Review** → Finds bugs, applies fixes, writes review record
5. Runs the **QA Writer**
6. Runs the **04e Diff Security Scan** across all files changed by the phase
7. Runs the **Prod Code Review** with the security report
8. Reports the verdict back to you
9. Runs the **Docs Writer** to update any stale documentation

### Manual Implementation Path

Prefer to write your own code? Use the planning agents, then implement yourself:

```
Step 1: 01 Project - Planner       → Phase documents
Step 2: 02 Phase - Refiner          → Refined phase document
Step 3: 03 Feature - Decomposer     → Feature bundles + execution manifest (optional)
Step 4: (you write the code from the plans)
Step 5: Prod Code Review        → Validates your code against the plans
```

The refined Phase document from Step 2 contains detailed scope, requirements, and acceptance criteria — enough to implement directly. When you're ready for validation, run **Prod Code Review** to check your work against the plan.

**Tip:** For structured feature decomposition without automated execution, use **03 Feature - Decomposer** directly — it creates numbered feature bundles in `dev/feature/[0N-task-name]/` plus `dev/feature/[phase-name]-execution-manifest.md`. Or launch **04 Phase - Execute** after those artifacts exist to run the automated implementation pipeline.

---

## Available Agents

### User-Facing (in agent picker)

| Agent | Purpose |
|-------|---------|
| **01 Project - Planner** | Create a project roadmap broken into phases |
| **02 Phase - Refiner** | Refine and deepen an individual Phase document |
| **03 Feature - Decomposer** | Break a phase into features, prepare execution-ready bundles, and write the execution manifest |
| **04 Phase - Execute** | Orchestrate full phase execution from a prepared manifest and feature bundles |
| **05 PR - Review** | Orchestrate a readiness review of the diff between a base commit and a head commit |
| **05 Eval - Grader** | Score a completed phase run from ledger files plus a rubric YAML and write a structured report |
| **06 Engagement - Prepare** | Prepare a client engagement for comparison analysis — validate the engagement config, then ensure an analysis branch, a code graph, and a baseline snapshot per side |
| **Engagement - Orchestrator** | Run a client engagement end to end from its configuration — preparation, then per-pair analysis stages through compliance, manifest, and gap review, all via subagents |
| **Eval - Feature Decomposition** | Score a feature-decomposition run against a golden-path branch across structural, naming, dependency, AC, context, and manifest dimensions |
| **Audit - Code, Infra, Refactor** | Orchestrate code, infrastructure, or structural audits with optional automated fix pipeline |
| **Instructions Manager** | Create or evaluate AI coding instruction files — routes to Instructions - Writer or Instructions - Evaluator |
| **Single Feature - Agent** | Handle small, focused changes with a proposal + explicit permission gate before implementation |
| **Debugger** | Diagnose and fix frontend or backend application errors |
| **Docs Writer** | Create or update repo documentation; also spawned automatically by orchestrators after pipeline completion |
| **Security Scan** | Full-codebase security assessment writing a phase-level report (secrets, dependencies, infra, CI/CD, config) |
| **Prod Code Review** | Final pre-production readiness gate (also usable standalone) |
| **Test - Orchestrator** | Orchestrate test analysis, writing, or fixing with optional remediation pipeline |
| **Unity Reviewer** | Review Unity C# code for architecture, performance, style, and Unity-specific pitfalls |
| **Visual Verifier** | Produce deterministic runtime screenshots and assess them against a phase's visual acceptance criteria (does it actually render?) |
| **Web Researcher** | Research a topic and produce a structured findings report and executive summary saved to `dev/research/[topic-name]/` |

### Hidden Subagents

These agents are not visible in the picker. They run automatically as part of orchestrator pipelines with `user-invocable: false`.

| Agent | spawned By | Purpose |
|-------|------------|---------|
| **Auditor - Code** | Audit orchestrator | Comprehensive code quality, security, and health audit |
| **Auditor - Infra** | Audit orchestrator | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **Auditor - Refactor** | Audit orchestrator | Audit codebase structure, module organization, and architecture |
| **Eval - Metric Grader** | Eval - Grader | Score one comparative metric from prepared diff and ledger evidence |
| **Eval - Score Recorder** | Eval - Grader | Resolve harness/model identity, compute the weighted score, and append one row to the score history |
| **Instructions - Writer** | Instructions Manager | Draft scoped `.instructions.md` files for a repository |
| **Instructions - Evaluator** | Instructions Manager | A/B evaluate whether instruction-file changes improve or regress |
| **Feature - Plan Expander** | Feature - Decomposer | Generate context and tasks files from existing plan files |
| **Feature - Implementer** | Phase - Execute, Audit orchestrator, Test orchestrator | Implement a feature plan using Red-Green-Refactor TDD |
| **Feature - Reviewer** | Phase - Execute, Audit orchestrator, Test orchestrator | Review implementation, apply fixes, produce review record |
| **Feature - QA Writer** | Phase - Execute, Audit orchestrator | Write manual QA plan for non-automatable test cases |
| **Baseline Worktree** | 05 PR - Review | Create or reuse a clean detached worktree at a caller-specified baseline commit and return its path |
| **05b Change Narrator** | 05 PR - Review | Build the base-to-head narrative for the diff under review and identify churn hotspots |
| **05c Artifact Sweeper** | 05 PR - Review | Sweep the branch diff for debug artifacts, TODO/FIXME markers, and dead code added by the branch |
| **05d Consistency Auditor** | 05 PR - Review | Compare the branch diff against established repository conventions and recommend canonical forms |
| **05e Dependency Auditor** | 05 PR - Review | Inventory dependencies added by the branch and report supply-chain and duplication risks, offline |
| **04e Diff Security Scan** | Phase - Execute | Perform a diff-scoped security scan of only the files changed by an execution and write a compact security report |
| **05f Test Health** | 05 PR - Review | Delegate coverage, redundancy, and flake analysis into a test health report |
| **05h Cleanliness Auditor** | 05 PR - Review | Evaluate the cleanliness of branch-added code and recommend specific cleanup categories when non-passing |
| **05g Readiness Synthesizer** | 05 PR - Review | Synthesize evaluator reports into a severity-ordered readiness verdict |
| **Engagement - Delta Synthesizer** | Engagement - Orchestrator | Produce the client-facing delta report, the SOW-exclusions partition, the audit-trail proof, and the internal remediation recommendations for a pair |
| **Engagement - Security Narrative** | Engagement - Orchestrator | Write the four-section client-facing security narrative and the internal engineer-facing security-delta report from the pair's reports and exclusions partition |
| **Engagement - Pricing Researcher** | Engagement - Orchestrator | Turn scan/dependency change evidence into cited cloud/cost claims via live pricing research, plus an internal cost-basis report (sole web-granted engagement agent) |
| **Engagement - Narrative Writer** | Engagement - Orchestrator | Write the business design document, intended-behavior specification, and before/after workflow narratives for a pair, plus the internal narrative-basis report |
| **Engagement - Compliance Writer** | Engagement - Orchestrator | Walk SOW acceptance criteria against retained artifacts; write the compliance walkthrough, verification summary, and package manifest |
| **Engagement - Gap Reviewer** | Engagement - Orchestrator | Review the deliverable set from the client's perspective against the manifest; always emit the internal gap-review report |
| **Test - Analyst** | Test orchestrator | Evaluate test suite for redundancy, coverage gaps, and consolidation |
| **Test - Fixer** | Test orchestrator | Diagnose and fix broken tests without modifying source code |
| **Test - Writer** | Test orchestrator | Bootstrap a test suite from scratch for untested code |

---

## What Each Agent Does

### User-Facing Agents

**01 Project - Planner** (document-only — does not write code)
> Give it a project scope or high-level goal. It iterates with you to produce a phased roadmap (`docs/phases/PROJECT_ROADMAP.md` and individual `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` files). Each phase document is self-contained and designed to be handed to the Phase - Refiner. It will not create any files until you explicitly approve.

**02 Phase - Refiner** (document-only — does not write code)
> Give it a single Phase document from the 01 Project - Planner (or describe a standalone feature). It iterates with you to refine scope, probe edge cases, surface hidden dependencies, stress-test decomposition readiness, and walk through user flows — deepening the Phase document until it's fully ready for automated execution. It updates the Phase document in place and will not write changes until you explicitly approve.

**03 Feature - Decomposer** (document-only — does not write code)
> Give it a refined Phase document or describe a feature. It scans the codebase, decomposes the work into independent features, writes a structured `-plan.md` file for each to `dev/feature/[0N-task-name]/`, spawns the Plan Expander to generate companion `-context.md` and `-tasks.md` files, and writes `dev/feature/[phase-name]-execution-manifest.md` as the execution schedule. In standalone mode, it asks for approval before writing.

**04 Phase - Execute** (orchestrator — delegates to subagents)
> Give it a refined Phase document after 03 has already prepared the feature bundles. It reads `dev/feature/[phase-name]-execution-manifest.md`, verifies each listed feature has `-plan.md`, `-context.md`, and `-tasks.md`, and fails immediately if those prepared artifacts are missing. When the bundle set is complete, it implements features by manifest wave order, then runs consolidated QA and Final Review.

**05 PR - Review** (orchestrator — delegates to evaluators)
> Give it a pull request. In a single upfront interaction it confirms the base commit (suggest-and-confirm — git cannot derive a branch's base), warns on a below-par model tier, and asks how the report should reach the PR. It then fans out the PR Review evaluators and returns a readiness verdict without reading code or diffs itself. Advisory only: it records no verdict in any document.

**Eval - Grader** (user-facing — standalone scorer)
> Give it a rubric YAML path plus three branch names: clean base, source-of-truth golden path, and branch to evaluate. The rubric should follow the grader schema documented in the agent, with `eval/rubrics/phase-eval-infrastructure-foundation.example.yaml` as the seed example. The grader materializes clean-base->golden and clean-base->evaluated diffs, reads `eval/runs/<phase-slug>/ledger-commits.jsonl` and `eval/runs/<phase-slug>/ledger-events.jsonl`, correlates semantic events onto the commit timeline by SHA association, preserves remediation-turn metadata such as `event_kind` and `related_event_id` when present, supports both feature-level and AC-level commit cadence, fans out one parallel `Eval - Metric Grader` subagent per comparative review metric, keeps exact ledger-derived metrics in the parent grader, produces both a rubric verdict and a comparative scorecard, and appends normalized `1-10` scores to the persistent additive markdown history file at `eval/EVAL_GRADER_SCORE_HISTORY.md`.

**06 Engagement - Prepare** (spawns no agents; never modifies engagement source)
> Give it an engagement configuration file path (schema in the `engagement-configuration` skill). After validation and a roster confirmation gate, it prepares every side of every declared comparison pair: a local, never-pushed analysis branch, an incremental code graph build, and a SHA-pinned internal baseline snapshot. Documentation is produced later by the engagement orchestrator's evidence stage. Idempotent: re-runs rebuild the graph and re-emit snapshots identically. See the `engagement-preparation-runbook` skill for the full operating procedure.

**Engagement - Orchestrator** (orchestrator — delegates to the engagement subagents)
> Give it an engagement configuration file path. It spawns Engagement - Prepare unchanged, then drives each comparison pair through comparative audit runs, delta and security synthesis, cloud/cost analysis, and narrative/specification documents, finishing the engagement with the SOW compliance walkthrough, verification summary, package manifest, and client-perspective gap review. It holds only statuses and artifact pointers, maintains `engagement-state.md` as its run record, and resumes from it on restart.

**Audit - Code, Infra, Refactor** (orchestrator — delegates to subagents)
> Asks which audit type to run (CODE, INFRA, or REFACTOR), delegates to the appropriate auditor subagent, and presents findings. Optionally drives automated remediation by converting audit findings into task plans and running them through the Feature - Implementer → Feature - Reviewer → Feature - QA Writer pipeline. After remediation, updates documentation via the Docs Writer.

**Single Feature - Agent** (direct implementation path)
> Handles small-scope changes (typically up to a few files) without full pipeline artifacts. It investigates, proposes a focused plan, asks for explicit permission before implementation, executes minimal changes, and verifies results. When scope expands, it recommends switching to **04 Phase - Execute**.

**Test - Orchestrator** (orchestrator — delegates to subagents)
> Asks which test operation to run (ANALYZE, WRITE, or FIX), delegates to the appropriate test subagent, and presents results. Optionally drives remediation of findings through the Feature - Implementer → Feature - Reviewer pipeline. After remediation, updates documentation via the Docs Writer.

**Debugger** (full tool access — reads and writes code)
> Give it an error message or description — frontend or backend. Triages the issue, classifies it (build-time, runtime, database, dependency, etc.), logs a remediation-turn ledger row on `phase/*` branches before diagnosis when you bring it a bug report or failing output, investigates, and applies minimal targeted fixes. Handles both frontend (TypeScript, React, build tools) and backend (Node.js, Python, databases, auth) errors.

**Prod Code Review** (document-only — does not modify code)
> Cross-validates all pipeline documents across all features in the phase, verifies the actual code matches the records, runs the test suite, and produces a **GO / GO WITH CONDITIONS / NO-GO** verdict with a full traceability matrix and risk register. Can be spawned standalone or automatically by the orchestrator.

**Security Scan** (document-only — does not modify code)
> Performs an evidence-based, full-codebase security assessment across all tracked, security-relevant repository artifacts. Writes a phase-level report covering secrets, dependencies, application attack surface, authentication, data protection, runtime safety, infrastructure, CI/CD, observability, and cross-cutting security patterns. It redacts sensitive values and distinguishes phase regressions from pre-existing release risks. (Distinct from the hidden **04e Diff Security Scan**, which only covers a single pass's diff.)

**Instructions Manager** (router — delegates to subagents)
> Give it a request to create or assess AI coding instruction files (`.github/instructions/`, `copilot-instructions.md`, `.cursorrules`, `CLAUDE.md`, or equivalent). It routes to the **Instructions - Writer** to draft new scoped instruction sets, or to the **Instructions - Evaluator** to A/B-test whether proposed instruction changes are improvements or regressions.

**Eval - Feature Decomposition** (document-only — does not write code)
> Give it a golden-path branch and a test branch. It scores the test branch's feature-decomposition documents against the golden path across structural, naming, dependency, AC, context, and manifest dimensions, and writes a numbered report to `eval/feature_decomp_eval_round_N.md`.

**Web Researcher** (read-only — uses fetch and web search)
> Give it a problem or topic. Searches across GitHub issues, Stack Overflow, Reddit, forums, and docs. Produces two deliverable documents saved to `dev/research/[topic-name]/`: a full structured findings report (`[topic-name]-report.md`) with inline numbered citations and a References table, and an executive summary (`[topic-name]-summary.md`) with priority recommendations and key reference links. Every factual claim traces back to a numbered citation. Sources older than 2 years are flagged with ⚠️.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. Produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING documents. Also spawned automatically at the end of orchestrator pipelines to update stale documentation after code changes.

**Unity Reviewer** (read-only — does not modify code)
> Give it Unity C# source files or a directory to review. Loads Unity-specific skills (MonoBehaviour lifecycle, UI Toolkit pitfalls, performance rules, design patterns, style guide compliance) and produces structured review findings. Does not modify code — review output only.

**Visual Verifier** (runs capture, reads frames, writes a report — does not modify source)
> Give it a phase's visual acceptance criteria and a capture config path. It runs the repository's documented deterministic screenshot capture, reads the produced frames as images, and judges each visual AC against what is actually on screen — returning Pass / Fail / Unverified with per-AC evidence. Catches the defect class that compiles, passes unit tests, and passes static review while rendering nothing usable. Honesty-bound: never certifies a visual AC without viewing the frame, and reports Unverified (not a fake pass) if it cannot ingest the images. Also spawned automatically by Phase - Execute on Unity phases that have visual ACs and a capture config.

### Hidden Subagents

**Feature - Plan Expander** *(subagent of Feature - Decomposer)* — Reads existing `-plan.md` files and generates companion `-context.md` and `-tasks.md` files in the same `dev/feature/[0N-task-name]/` directory. Does not modify plan files.

**Feature - Implementer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads plan docs from `dev/feature/[0N-task-name]/`, scans sibling feature directories for context awareness, implements each acceptance criterion using Red-Green-Refactor TDD, and writes `[0N-task-name]-implementation.md` with an AC coverage matrix mapping changes, planned test identifiers, and evidence paths back to acceptance criteria. Only implements the single feature it is given.

**Feature - Reviewer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads plan and implementation docs, reviews all changed code, applies fixes for High/Blocker issues directly, and writes `[0N-task-name]-review.md` with verdict and remaining concerns.

**Feature - QA Writer** *(subagent of Phase - Execute, Audit orchestrator)* — In batch mode: reads all pipeline docs from every feature in a phase and writes a single consolidated QA plan. In per-feature mode: reads pipeline docs from a single feature and writes QA plan and coverage map to that feature's directory.

**04e Diff Security Scan** *(subagent of Phase - Execute)* — Performs a diff-scoped security review of only the files changed by an implementation pass (from an implementation record's "Files Changed" table or a git diff range), plus their immediate security-relevant context. Writes a compact report with verdict, findings, and the categories not assessable at diff scope. It does not replace the full-codebase Security Scan.

**Auditor - Code** *(subagent of Audit orchestrator)* — Audits every source file for cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report.

**Auditor - Infra** *(subagent of Audit orchestrator)* — Evaluates Dockerfiles, CI/CD pipelines, IaC templates, and config files for security, best practices, and operational risk.

**Auditor - Refactor** *(subagent of Audit orchestrator)* — Evaluates codebase-level organization: module structure, dependency graphs, component decomposition, coupling, cohesion, and separation of concerns.

**Eval - Metric Grader** *(subagent of Eval - Grader)* — Scores one comparative metric at a time from prepared diff artifacts, rubric context, and ledger evidence. Returns a normalized `1-10` score, evidence summary, and confidence back to the parent grader.

**Eval - Score Recorder** *(subagent of Eval - Grader)* — Resolves harness/model identity from `eval/scoring/HARNESS_MODEL_MAPPINGS.md`, computes the weighted overall score with step-by-step verification, and appends a single additive-only row to the persistent score history. Spawned only after the parent grader's score report is fully written.

**Instructions - Writer** *(subagent of Instructions Manager)* — Discovers a repository's domains and non-obvious rules and drafts scoped `.instructions.md` files following the AI Instruction File Framework.

**Instructions - Evaluator** *(subagent of Instructions Manager)* — Evaluates whether changes to instruction files are improvements or regressions using blind A/B testing, rule classification, 3-run stability scoring, and rule-quality analysis. Reads the BEFORE state automatically from git history.

**Engagement - Delta Synthesizer** *(subagent of Engagement - Orchestrator)* — Consumes both sides' report sets to produce the business-framed delta report, owns the single-point SOW-exclusions partition, writes the audit-trail proof checklist, and emits the internal remediation-recommendations worklist of in-SOW-scope postures still open on the upgraded side.

**Engagement - Security Narrative** *(subagent of Engagement - Orchestrator)* — Writes the four-section client-facing security narrative (posture, repaired, out-of-scope, residual) with every original-side finding classified exactly once, consuming the exclusions partition rather than re-deriving it. Also writes the internal engineer-facing security-delta report (original / fixed / unfixed / introduced) verifying the upgrade added no new security issues.


**Engagement - Pricing Researcher** *(subagent of Engagement - Orchestrator)* — The only web-granted engagement agent; researches live pricing for evidenced infrastructure/dependency changes with strict query hygiene (no client content in queries), cites source and retrieval date per figure, and degrades to NOT RESEARCHED offline. Also writes the internal cost-basis report — per-figure sources and calculations plus the verbatim query-hygiene audit trail.

**Engagement - Narrative Writer** *(subagent of Engagement - Orchestrator)* — Writes the three per-pair narrative documents (business design, intended-behavior specification, before/after workflow narratives) from analysis-branch docs and graphs, framed by the pair's value-story mode. Also writes the internal narrative-basis report: claims traceability, a warranty risk register (verified vs. assumed spec statements), framing discrepancies, and evidence gaps.

**Engagement - Compliance Writer** *(subagent of Engagement - Orchestrator)* — Walks every SOW acceptance criterion against retained on-disk artifacts, writes the verification summary with its functional-preservation statement, and assembles the package manifest per the `engagement-package-manifest` schema.

**Engagement - Gap Reviewer** *(subagent of Engagement - Orchestrator)* — Reviews the complete deliverable set from the client's perspective using the manifest as its completeness checklist and unconditionally emits `internal/gap-review.md`, even when no gaps are found.

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
- **Single Feature - Agent** — Implement a focused change with an explicit approval gate and minimal churn
- **05 Eval - Grader** — Score a completed `phase/*` run against a rubric and preserve a Markdown score report under `eval/runs/<phase-slug>/`
- **Test - Orchestrator** — Analyze, write, or fix tests on demand
- **Prod Code Review** — Point at any `dev/feature/[0N-task-name]/` folder for an independent readiness check
- **Debugger** — Fix a specific frontend or backend error without a full pipeline
- **Unity Reviewer** — Review Unity C# code for architecture, performance, and pitfalls
- **Visual Verifier** — Screenshot a rendering phase and judge it against its visual acceptance criteria
- **Web Researcher** — Research a technical question or debug a tricky issue
- **Docs Writer** — Update documentation after any significant change

---

## Task Documentation Pattern

The pipeline subagents produce output in the `dev/feature/[0N-task-name]/` directory (numbered by execution order). After a full feature cycle, the folder contains:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md              # Plan with stages (Feature - Decomposer)
├── [0N-task-name]-context.md           # Key files, decisions, constraints (Feature - Plan Expander)
├── [0N-task-name]-tasks.md             # Checklist of work items (Feature - Plan Expander)
├── [0N-task-name]-implementation.md    # Files changed, AC traceability (Feature - Implementer)
└── [0N-task-name]-review.md            # Verdict, issues, fixes applied (Feature - Reviewer)
```

**Batch mode:** The **Feature - QA Writer** produces a single consolidated QA document covering ALL features in the phase:

```
docs/phases/[phase-name]/[phase-name]_QA.md                # Consolidated manual QA checklist
docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md   # AC coverage map (automated vs manual)
```

If `docs/phases/` does not exist, the QA doc falls back to `dev/feature/[phase-name]-qa.md`.

**Per-feature mode:** QA and review documents are written inside the feature's own directory:

```
dev/feature/[0N-task-name]/[0N-task-name]-qa.md                 # QA plan for this feature
dev/feature/[0N-task-name]/[0N-task-name]-coverage-map-qa.md    # Coverage map for this feature
dev/feature/[0N-task-name]/[0N-task-name]-qa-analysis.md        # GO/NO-GO verdict for this feature
```

The **Prod Code Review** writes its readiness analysis to:

```
dev/[phase-name]-qa-analysis.md      # GO/NO-GO verdict, traceability matrix, risk register (batch mode)
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
- The orchestrator's `agents:` frontmatter restricts which subagents it can spawn, preventing unintended delegation.

---

## Skills and Instructions

Agents reference **skills** (`.github/skills/<name>/SKILL.md`) for shared templates and formats that would otherwise be duplicated. Skills are loaded on demand when an agent's instructions say "Load the `<name>` skill."

See [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md#skills) for the full skills inventory.

**Instructions** (`.github/instructions/*.instructions.md`) inject cross-cutting conventions into agents automatically via `applyTo` glob patterns.

See [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md#instructions) for the full instructions inventory.

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
- **Four orchestrators**: **04 Phase - Execute**, **05 PR - Review**, **Audit - Code, Infra, Refactor**, and **Test - Orchestrator** all delegate to hidden subagents marked `user-invocable: false`. These appear as collapsible tool calls in the chat UI.
- **Shared subagents**: **Feature - Implementer** and **Feature - Reviewer** are used by the implementation, audit, and test orchestrators. **Feature - QA Writer** is used by Phase - Execute and the Audit orchestrator. **Docs Writer** is spawned by Phase - Execute, Audit, and Test orchestrators at the end of the pipeline to update stale documentation (it remains user-invocable for standalone use as well).
- **Dual-use agents**: **03 Feature - Decomposer** is user-facing for standalone plan creation and also spawned by **04 Phase - Execute** when plans are missing. **Docs Writer** is user-facing and also spawned by all three orchestrators.
- **Subagent autonomy**: Hidden subagents operate without user confirmation — they read inputs from `dev/feature/[0N-task-name]/`, execute their role, write outputs to the same folder, and return a summary to the orchestrator.
- **Read-only subagents**: **Auditor - Code**, **Auditor - Infra**, **Auditor - Refactor**, and **Test - Analyst** do not modify code. They analyze and report only.
- **Approval-gated agents**: **01 Project - Planner**, **02 Phase - Refiner**, and **03 Feature - Decomposer** always present findings and ask for explicit approval before creating files. They also check for missing critical documentation (`README.md`, `docs/CODEBASE_CONTEXT.md`) and recommend running the **Docs Writer** before continuing. The **Audit** and **Test** orchestrators ask before proceeding to the remediation phase.
- **Code-writing agents**: **Debugger**, **Test - Writer**, **Test - Fixer**, **Feature - Implementer**, and **Feature - Reviewer** have full tool access to create and modify files.
- **Prod Code Review** does not modify code — it analyzes and reports only, producing a GO / NO-GO verdict.
