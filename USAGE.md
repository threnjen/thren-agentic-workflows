# Agents

Specialized agents for structured software development workflows. The core workflow uses an **orchestrator + subagent** pattern — you interact with a few agents, and the orchestrator drives the rest automatically. A **manual implementation path** is also available for users who prefer to write their own code.

---

## How to Use an Agent

These agents deploy to Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot. How you reach one depends on the harness:

| Harness | How to invoke |
|---------|---------------|
| Claude Code | `/agent-name` slash command, or ask for the agent by name |
| Cursor | `/agent-name` slash command |
| GitHub Copilot | Agent picker dropdown at the top of the Copilot Chat panel in VS Code |
| Codex | Name the agent in the prompt: `as feature-decomposer, ...'` |
| OpenCode | Name the agent in the prompt |

Only the 15 user-facing agents are reachable this way. The rest are spawned by orchestrators.

Be specific in your request. Each agent produces structured output — plan documents, implementation summaries, review tables, audit reports.

---

## The Project Pipeline (5 user steps)

The core development workflow. **You drive steps 1–4, step 4 runs hands-free to a verdict, and step 5 is your own pre-PR self-review.**

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU                                                            │
│                                                                 │
│  Step 1: 01 Project - Planner     → Phase documents             │
│  Step 2: 02 Phase - Refiner       → Refined phase document      │
│  Step 3: 03 Feature - Decomposer  → Plan bundles + manifest     │
│  Step 4: 04 Phase - Execute       → Hands-free from here ──┐    │
│                                                            │    │
│  Step 5: 05 PR - Review           → Self-review before PR  │    │
│          (after the automated run reports back)            │    │
└────────────────────────────────────────────────────────────│────┘
                                                             │
┌────────────────────────────────────────────────────────────│────┐
│  AUTOMATED (subagents)                                     │    │
│                                                            ▼    │
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

### Step 3: Decompose the Phase

| Agent | Prompt | Output |
|-------|--------|--------|
| **03 Feature - Decomposer** | "Decompose this phase" + attach refined phase doc | Feature bundles in `dev/feature/[0N-task-name]/` + execution manifest |

Required before Step 4 — `04 Phase - Execute` fails immediately if these artifacts are missing rather than generating them itself. It asks for approval before writing.

### Step 4: Execute the Phase

| Agent | Prompt | Output |
|-------|--------|--------|
| **04 Phase - Execute** | "Execute this phase" + attach refined phase doc | All features implemented, reviewed, QA'd |

**Hands-free from here.** Reading the bundles Step 3 produced, the orchestrator automatically:

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

### Step 5: Self-Review Before Opening the PR

| Agent | Prompt | Output |
|-------|--------|--------|
| **05 PR - Review** | "Review my change before I open the PR" | Readiness report on the diff between a confirmed base and head commit |

Asks its three questions once — model tier, the base commit, and whether to post the
report to an already-open draft PR — then runs its evaluator roster over that diff and
hands back a plain-language readiness report. Advisory only: it changes no code and
records no verdict in any document. Distinct from the automated **Prod Code Review**
gate inside Step 4, which validates the phase's pipeline records; this reviews the diff
you are about to publish.

### Manual Implementation Path

Prefer to write your own code? Use the planning agents, then implement yourself:

```
Step 1: 01 Project - Planner       → Phase documents
Step 2: 02 Phase - Refiner          → Refined phase document
Step 3: 03 Feature - Decomposer     → Feature bundles + execution manifest (optional here)
Step 4: (you write the code from the plans)
Step 5: 05 PR - Review              → Readiness report on what you wrote
```

The refined Phase document from Step 2 contains detailed scope, requirements, and acceptance criteria — enough to implement directly. When you're ready for validation, run **05 PR - Review** to get a readiness verdict on your diff.

**Tip:** Decomposition is optional on this path — the refined Phase document alone is often enough. Run **03 Feature - Decomposer** anyway if you want the work broken into numbered bundles to work through by hand.

---

## Available Agents

### User-Facing (directly invocable)

| Agent | Purpose |
|-------|---------|
| **01 Project - Planner** | Create a project roadmap broken into phases |
| **02 Phase - Refiner** | Refine and deepen an individual Phase document |
| **03 Feature - Decomposer** | Break a phase into features, prepare execution-ready bundles, and write the execution manifest |
| **04 Phase - Execute** | Orchestrate full phase execution from a prepared manifest and feature bundles |
| **05 PR - Review** | Self-review a change before opening the PR — readiness report on the diff between a base commit and a head commit |
| **Client Deliverable** | Produce the client deliverable package for a modernization engagement — audits each before/after repository pair and compares the two sides |
| **Audit - Code, Infra, Refactor, Security** | Audit code quality, infrastructure, architecture, or security in one repository, with optional fix research and automated fix pipeline |
| **Audit - Delta** | Audit two revisions or checkouts of the same product and reconcile them into a delta of what changed, with optional fix research and automated fix pipeline |
| **Instructions Manager** | Create a scoped AI coding instruction set, or blind A/B-test whether a change to one is an improvement |
| **Single Feature - Agent** | Handle small, focused changes with a proposal + explicit permission gate before implementation |
| **Debugger** | Diagnose and fix frontend or backend application errors |
| **Docs Writer** | Create or update repo documentation; also spawned automatically by orchestrators after pipeline completion |
| **QA - Bootstrapper** | Bootstrap a repository's QA package — generate QA_AUTOMATED and QA_USER from available starter inputs, run the automated runbook, and stamp pass/fail results |
| **Test - Orchestrator** | Orchestrate test analysis, writing, or fixing with optional remediation pipeline |
| **Web Researcher** | Research a topic and produce a structured findings report and executive summary saved to `dev/research/[topic-name]/` |

### Hidden Subagents

Not directly invocable in any harness. They carry `user-invocable: false` and run only when an orchestrator spawns them; Claude and Codex prefix their generated files `z-`.

| Agent | Spawned By | Purpose |
|-------|------------|---------|
| **Auditor - Code** | Audit orchestrator, Client Deliverable | Comprehensive code quality, security, and health audit |
| **Auditor - Infra** | Audit orchestrator, Client Deliverable | Audit Dockerfiles, CI/CD pipelines, IaC templates, and config files |
| **Auditor - Refactor** | Audit orchestrator | Audit codebase structure, module organization, and architecture |
| **Auditor - Security** | Audit orchestrator, Client Deliverable | Full-codebase security audit across secrets, dependencies, attack surface, auth, data protection, runtime safety, infra/CI-CD, and observability |
| **Auditor - Delta** | Audit - Delta orchestrator | Compare two audit reports of the same product and produce a reconciled delta document plus an open-items queue |
| **Auditor - Attribution** | Audit - Delta orchestrator | Probe both source trees to settle whether each provisional delta finding is a regression or pre-existing |
| **Auditor - Remediation Research** | Audit orchestrator | Research exactly one assigned open-items subsystem and write its exclusive fix-research report |
| **Auditor - Remediation Reconciler** | Audit orchestrator | Validate researcher corrections and reconcile the current report, summary, full delta, and queue |
| **Instructions - Writer** | Instructions Manager | Draft scoped `.instructions.md` files for a repository |
| **Instructions - Evaluator** | Instructions Manager | A/B evaluate whether instruction-file changes improve or regress |
| **Feature - Plan Expander** | Feature - Decomposer | Generate context and tasks files from existing plan files |
| **Feature - Implementer** | Phase - Execute, Audit orchestrator, Test orchestrator | Implement a feature plan using Red-Green-Refactor TDD |
| **Feature - Reviewer** | Phase - Execute, Audit orchestrator, Test orchestrator | Review implementation, apply fixes, produce review record |
| **Feature - QA Writer** | Phase - Execute, Audit orchestrator | Write manual QA plan for non-automatable test cases |
| **QA - Doc Generator** | QA - Bootstrapper | Generate the QA_AUTOMATED runbook and QA_USER checklist from repository, manual QA, and acceptance inputs |
| **QA - Runner** | QA - Bootstrapper | Execute the QA_AUTOMATED runbook and all test suites, then record binary pass/fail results into the runbook |
| **Baseline Worktree** | 05 PR - Review | Create or reuse a clean detached worktree at a caller-specified baseline commit and return its path |
| **05b Change Narrator** | 05 PR - Review | Build the base-to-head narrative for the diff under review and identify churn hotspots |
| **05c Artifact Sweeper** | 05 PR - Review | Sweep the branch diff for debug artifacts, TODO/FIXME markers, and dead code added by the branch |
| **05d Consistency Auditor** | 05 PR - Review | Compare the branch diff against established repository conventions and recommend canonical forms |
| **05e Dependency Auditor** | 05 PR - Review, Client Deliverable | Inventory dependencies added by the branch and report supply-chain and duplication risks, offline |
| **04e Diff Security Scan** | Phase - Execute, 05 PR - Review | Perform a diff-scoped security scan of only the files changed by an execution and write a compact security report |
| **Unity Reviewer** | Phase - Execute, PR - Review, Single Feature - Agent | Review Unity C# code for architecture, performance, style, and Unity-specific pitfalls |
| **Visual Verifier** | Phase - Execute | Produce deterministic runtime screenshots and assess them against a phase's visual acceptance criteria (does it actually render?) |
| **Prod Code Review** | Phase - Execute, Audit orchestrator | Final pre-production readiness gate — cross-validate every pipeline document in a phase and produce a GO / NO-GO verdict |
| **05f Test Health** | 05 PR - Review | Adapt root-supplied Test Analyst evidence into a test health report |
| **05h Cleanliness Auditor** | 05 PR - Review | Evaluate the cleanliness of branch-added code and recommend specific cleanup categories when non-passing |
| **05g Readiness Synthesizer** | 05 PR - Review | Synthesize evaluator reports into a severity-ordered readiness verdict |
| **Client Deliverable - Prepare** | Client Deliverable | Prepare a client engagement for comparison analysis — validate the engagement config, then ensure an analysis branch, a code graph, and a baseline snapshot per side |
| **Client Deliverable - Delta Synthesizer** | Client Deliverable | Produce the client-facing findings report, the SOW-exclusions partition, and the internal remediation recommendations for a pair |
| **Client Deliverable - Security Narrative** | Client Deliverable | Write the four-section client-facing security narrative and the internal engineer-facing security-delta report from the pair's reports and exclusions partition |
| **Client Deliverable - Pricing Researcher** | Client Deliverable | Turn scan/dependency change evidence into cited cloud/cost claims via live pricing research, plus an internal cost-basis report (sole web-granted engagement agent) |
| **Client Deliverable - Narrative Writer** | Client Deliverable | Write the business design document, intended-behavior specification, and before/after workflow narratives for a pair, plus the internal narrative-basis report |
| **Client Deliverable - Compliance Writer** | Client Deliverable | Walk SOW acceptance criteria against retained artifacts; write the compliance walkthrough, verification summary, and internal compliance-basis report |
| **Client Deliverable - Manifest Assembler** | Client Deliverable | Assemble the package manifest per its schema, evaluating every row's present/missing status from disk, plus the internal manifest-basis report |
| **Client Deliverable - Gap Reviewer** | Client Deliverable | Review the deliverable set from the client's perspective against the manifest; always emit the internal gap-review report |
| **Test - Analyst** | Test orchestrator, 05 PR - Review | Evaluate test suite for redundancy, coverage gaps, and consolidation |
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
> Give it a refined Phase document after 03 has already prepared the feature bundles. It reads `dev/feature/[phase-name]-execution-manifest.md`, verifies each listed feature has `-plan.md`, `-context.md`, and `-tasks.md`, and fails immediately if those prepared artifacts are missing. When the bundle set is complete, it implements features by manifest wave order, then runs consolidated QA, the diff security scan, and Prod Code Review.

**05 PR - Review** (orchestrator — delegates to evaluators)
> Point it at a change you are about to open a PR for — this is an author self-review, not a reviewer critiquing someone else's open PR. In a single upfront interaction it warns on a below-par model tier, confirms the base commit (suggest-and-confirm — git cannot derive a branch's base), and asks whether the report should be posted to a draft PR if one already exists (posting is opt-in; the default recommendation keeps you between the finding and the audience). It then fans out the PR Review evaluators over that diff and returns a readiness verdict without reading code or diffs itself. Advisory only: it changes no code and records no verdict in any document.

**Client Deliverable** (orchestrator — delegates to the engagement subagents)
> Give it an engagement configuration file path. It produces the client-facing deliverable package — findings report, security narrative, cloud/cost analysis, business and workflow narratives, the SOW compliance walkthrough and verification summary, and the package manifest — by auditing each before/after repository pair and comparing the two sides, closing with a client-perspective gap review. Mechanically: it spawns Client Deliverable - Prepare unchanged, then drives each pair's analysis stages through subagents, holding only statuses and artifact pointers. It maintains `engagement-state.md` as its run record and resumes from it on restart.

**Audit - Code, Infra, Refactor, Security** (orchestrator — delegates to subagents)
> Asks which audit type to run (CODE, INFRA, REFACTOR, or SECURITY — multi-select), delegates to the appropriate auditor subagents, and presents findings for **one** repository. Optionally queues the open findings by severity threshold and researches fixes for them (Auditor - Remediation Research → Auditor - Remediation Reconciler), then drives automated remediation by converting findings into task plans and running them through the Feature - Implementer → Feature - Reviewer → Feature - QA Writer pipeline. After remediation, updates documentation via the Docs Writer. Two checkouts or two branches belong to **Audit - Delta** instead.

**Audit - Delta** (orchestrator — delegates to subagents)
> The comparative counterpart. Confirms the targets, snapshot labels, and which side is the baseline; materializes any git refs into read-only worktrees via Baseline Worktree; runs the full type × target matrix of auditors under identical prompts; then spawns Auditor - Delta per (type, pair) to reconcile each into a delta plus an open-items queue. All deliverables land on the newer side. Shares the same optional fix-research and remediation pipeline as the single-target orchestrator.

**Single Feature - Agent** (direct implementation path)
> Handles small-scope changes (typically up to a few files) without full pipeline artifacts. It investigates, proposes a focused plan, asks for explicit permission before implementation, executes minimal changes, and verifies results. When scope expands, it recommends switching to **04 Phase - Execute**.

**Test - Orchestrator** (orchestrator — delegates to subagents)
> Asks which test operation to run (ANALYZE, WRITE, or FIX), delegates to the appropriate test subagent, and presents results. Optionally drives remediation of findings through the Feature - Implementer → Feature - Reviewer pipeline. After remediation, updates documentation via the Docs Writer.

**Debugger** (full tool access — reads and writes code)
> Give it an error message or description — frontend or backend. Triages the issue, classifies it (build-time, runtime, database, dependency, etc.), investigates, and applies minimal targeted fixes. On repos with `docs/phases/`, it also syncs the affected phase documents so they stay baseline-truth. Handles both frontend (TypeScript, React, build tools) and backend (Node.js, Python, databases, auth) errors.

**QA - Bootstrapper** (orchestrator — delegates to subagents)
> Point it at a repository that has no QA package. It spawns **QA - Doc Generator** to write the `QA_AUTOMATED` technical runbook and the `QA_USER` manual acceptance checklist from the repository plus any starter inputs (existing manual QA notes, an SOW or contract, plan acceptance criteria), then spawns **QA - Runner** to execute the runbook end to end and stamp binary pass/fail results back into it.

**Instructions Manager** (router — delegates to subagents)
> Give it a request to create or assess AI coding instruction files (`.github/instructions/`, `copilot-instructions.md`, `.cursorrules`, `CLAUDE.md`, or equivalent). It routes to the **Instructions - Writer** to draft new scoped instruction sets, or to the **Instructions - Evaluator** to A/B-test whether proposed instruction changes are improvements or regressions.

**Web Researcher** (read-only — uses fetch and web search)
> Give it a problem or topic. Searches across GitHub issues, Stack Overflow, Reddit, forums, and docs. Produces two deliverable documents saved to `dev/research/[topic-name]/`: a full structured findings report (`[topic-name]-report.md`) with inline numbered citations and a References table, and an executive summary (`[topic-name]-summary.md`) with priority recommendations and key reference links. Every factual claim traces back to a numbered citation. Sources older than 2 years are flagged with ⚠️.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. Produces or updates README, ARCHITECTURE, CODEBASE_CONTEXT, and TROUBLESHOOTING documents. Also spawned automatically at the end of orchestrator pipelines to update stale documentation after code changes.


### Hidden Subagents

**Unity Reviewer** *(subagent of Phase - Execute, PR - Review, Single Feature - Agent)* — Spawned on repositories with a Unity layout. Runs the repository's compile gate, adds a batch asset-import gate when the change touches serialized assets, then reviews against the Unity reference categories (style, performance, architecture, lifecycle/wiring, UI Toolkit, test authenticity, 2D rendering, DOTS/ECS, serialized-asset integrity). Returns severity-ranked findings with a rule citation per finding. Read-only: it never edits source and never implements a fix. States what each check actually proves — a clean compile or import is not evidence that references resolve or that anything renders, so runtime and visual criteria come back as unverified rather than passing.

**Visual Verifier** *(subagent of Phase - Execute)* — Spawned on Unity phases that have visual acceptance criteria and a capture config. Runs the repository's documented deterministic screenshot capture, reads the produced frames as images, and judges each visual AC against what is actually on screen — returning Pass / Fail / Unverified with per-AC evidence. Catches the defect class that compiles, passes unit tests, and passes static review while rendering nothing usable. Honesty-bound: never certifies a visual AC without viewing the frame, and reports Unverified (not a fake pass) if it cannot ingest the images. Does not modify source.

**Feature - Plan Expander** *(subagent of Feature - Decomposer)* — Reads existing `-plan.md` files and generates companion `-context.md` and `-tasks.md` files in the same `dev/feature/[0N-task-name]/` directory. Does not modify plan files.

**Feature - Implementer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads plan docs from `dev/feature/[0N-task-name]/`, scans sibling feature directories for context awareness, implements each acceptance criterion using Red-Green-Refactor TDD, and writes `[0N-task-name]-implementation.md` with an AC coverage matrix mapping changes, planned test identifiers, and evidence paths back to acceptance criteria. Only implements the single feature it is given.

**Feature - Reviewer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads plan and implementation docs, reviews all changed code, applies fixes for High/Blocker issues directly, and writes `[0N-task-name]-review.md` with verdict and remaining concerns.

**Feature - QA Writer** *(subagent of Phase - Execute, Audit orchestrator)* — In batch mode: reads all pipeline docs from every feature in a phase and writes a single consolidated QA plan. In per-feature mode: reads pipeline docs from a single feature and writes QA plan and coverage map to that feature's directory.

**04e Diff Security Scan** *(subagent of Phase - Execute and 05 PR - Review)* — Performs a diff-scoped security review of only the files changed by an implementation pass (from an implementation record's "Files Changed" table or a git diff range), plus their immediate security-relevant context. Writes a compact report with verdict, findings, and the categories not assessable at diff scope. It does not replace the full-codebase Auditor - Security scan.

**Prod Code Review** *(subagent of Phase - Execute and the Audit orchestrator)* — Cross-validates all pipeline documents across all features in the phase, verifies the actual code matches the records, runs the test suite, and produces a **GO / GO WITH CONDITIONS / NO-GO** verdict with a full traceability matrix and risk register. Pipeline-internal only (`user-invocable: false`): orchestrators spawn it as the automated gate at the end of a phase. For an on-demand readiness check of your own, use **05 PR - Review** instead.

**QA - Doc Generator** *(subagent of QA - Bootstrapper)* — Generates the `QA_AUTOMATED` runbook and the `QA_USER` manual acceptance checklist from the repository plus optional manual-QA, SOW/contract, and plan-acceptance inputs, per the `qa-generation` skill.

**QA - Runner** *(subagent of QA - Bootstrapper)* — Executes the `QA_AUTOMATED` runbook end to end — every runbook check plus every discovered test suite — with strict binary PASS/FAIL mapping and captured evidence, recording per-check results and the overall verdict back into the runbook's Run results section, per the `qa-run` skill.

**Auditor - Code** *(subagent of Audit orchestrator)* — Audits every source file for cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report.

**Auditor - Infra** *(subagent of Audit orchestrator)* — Evaluates Dockerfiles, CI/CD pipelines, IaC templates, and config files for security, best practices, and operational risk.

**Auditor - Refactor** *(subagent of Audit orchestrator)* — Evaluates codebase-level organization: module structure, dependency graphs, component decomposition, coupling, cohesion, and separation of concerns.

**Auditor - Security** *(subagent of Audit orchestrator and Client Deliverable)* — Audits every in-scope file against ten fixed security categories: secrets, dependencies and supply chain, attack surface and injection, authentication and authorization, data protection and cryptography, API and input boundaries, filesystem/process/runtime safety, infrastructure and CI/CD, observability, and cross-cutting security architecture. Redacts every secret value, records each category as assessed-clean or not-assessed so the two are never confused, and produces a structured report plus executive summary. (Distinct from the hidden **04e Diff Security Scan**, which only covers a single pass's diff.)

**Auditor - Delta** *(subagent of Audit - Delta orchestrator)* — Compares two completed audit reports of the same product — a baseline snapshot and a current one — and produces a delta document classifying every finding as resolved, improved, unchanged, transformed, or unverified, with the counts reconciled against both reports, plus a standalone open-items queue. Current-side findings with no baseline counterpart are marked `PROVISIONAL` and handed off; it attributes nothing itself and raises no findings of its own.

**Auditor - Attribution** *(subagent of Audit - Delta orchestrator)* — Runs after a delta closes its arithmetic. For each provisional finding it searches the baseline tree by symbol and signature and settles the item as NEW (the newer work introduced the code), PRE-EXISTING (position materially identical at baseline), or UNVERIFIED-ORIGIN (no baseline tree). It rewrites only the attribution fields of the delta and queue, and proves the unattributed total is unchanged. This split is what keeps a reporting difference between two auditors from being reported as a regression.

**Auditor - Remediation Research** *(subagent of Audit orchestrator)* — Receives one subsystem assignment and writes one exclusive detailed report after validating every assigned item as real, true, current, and actionable. Returns correction candidates compactly; it does not edit shared audit artifacts or production code.

**Auditor - Remediation Reconciler** *(subagent of Audit orchestrator)* — Validates all subsystem correction candidates against the snapshots, then is the sole child writer for the affected current report, current summary, full delta, and open-items queue. It writes no production code.

**Instructions - Writer** *(subagent of Instructions Manager)* — Discovers a repository's domains and non-obvious rules and drafts scoped `.instructions.md` files following the AI Instruction File Framework.

**Instructions - Evaluator** *(subagent of Instructions Manager)* — Evaluates whether changes to instruction files are improvements or regressions using blind A/B testing, rule classification, 3-run stability scoring, and rule-quality analysis. Reads the BEFORE state automatically from git history.

**Client Deliverable - Prepare** *(subagent of Client Deliverable; spawns no agents, never modifies engagement source)* — Given an engagement configuration file path (schema in the `engagement-configuration` skill), validates it, gates on the roster confirmation, then prepares every side of every declared comparison pair: a local, never-pushed analysis branch, an incremental code graph build, and a SHA-pinned internal baseline snapshot. Documentation is produced later by the Client Deliverable orchestrator's evidence stage. Idempotent: re-runs rebuild the graph and re-emit snapshots identically. Operating procedure lives in the `engagement-preparation-runbook` skill.

**Client Deliverable - Delta Synthesizer** *(subagent of Client Deliverable)* — Consumes both sides' report sets to produce the plain-language findings report (with the how-we-checked-our-own-work appendix), owns the single-point SOW-exclusions partition, and emits the internal remediation-recommendations worklist of in-SOW-scope postures still open on the upgraded side.

**Client Deliverable - Security Narrative** *(subagent of Client Deliverable)* — Writes the four-section client-facing security narrative (posture, repaired, out-of-scope, residual) with every original-side finding classified exactly once, consuming the exclusions partition rather than re-deriving it. Also writes the internal engineer-facing security-delta report (original / fixed / unfixed / introduced) verifying the upgrade added no new security issues.

**Client Deliverable - Pricing Researcher** *(subagent of Client Deliverable)* — The only web-granted engagement agent; researches live pricing for evidenced infrastructure/dependency changes with strict query hygiene (no client content in queries), cites source and retrieval date per figure, and degrades to NOT RESEARCHED offline. Also writes the internal cost-basis report — per-figure sources and calculations plus the verbatim query-hygiene audit trail.

**Client Deliverable - Narrative Writer** *(subagent of Client Deliverable)* — Writes the three per-pair narrative documents (business design, intended-behavior specification, before/after workflow narratives) from analysis-branch docs and graphs, framed by the pair's value-story mode. Also writes the internal narrative-basis report: claims traceability, a warranty risk register (verified vs. assumed spec statements), framing discrepancies, and evidence gaps.

**Client Deliverable - Compliance Writer** *(subagent of Client Deliverable)* — Walks every SOW acceptance criterion against retained on-disk artifacts and writes the compliance walkthrough and the verification summary with its functional-preservation statement, plus the internal compliance-basis report (per-criterion evidence map, verification standards, NOT VERIFIED reasons).

**Client Deliverable - Manifest Assembler** *(subagent of Client Deliverable)* — Assembles the package manifest per the `engagement-package-manifest` schema, evaluating every row's present/missing status from disk as an independent check on the writing agents, plus the internal manifest-basis report (per-row determination notes and the report-vs-disk discrepancy audit trail), then hands the manifest to the gap review.

**Client Deliverable - Gap Reviewer** *(subagent of Client Deliverable)* — Reviews the complete deliverable set from the client's perspective using the manifest as its completeness checklist and unconditionally emits `internal/gap-review.md`, even when no gaps are found.

**Test - Analyst** *(subagent of Test orchestrator and PR Review)* — Classifies tests by value, flags redundancy and over-mocking, and writes a categorized inventory with a staged reduction plan. PR Review spawns it directly and passes its files to 05f as sibling evidence.

**Test - Writer** *(subagent of Test orchestrator)* — Bootstraps a test suite from scratch. Scans the codebase, creates test files with meaningful coverage, and verifies the suite passes.

**Test - Fixer** *(subagent of Test orchestrator)* — Diagnoses and fixes broken tests. Updates assertions, mocks, fixtures, and configuration to get a failing suite back to green — never modifies source code.

---

## Other Pipelines

The **Audit** and **Test** orchestrators handle most multi-step workflows internally. These pipelines combine agents across different concerns.

### Code Quality Improvement

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor, Security** | "Audit the codebase" → select CODE, accept remediation |

The audit orchestrator runs the code audit, presents findings, and offers to implement fixes automatically through the feature pipeline.

### Structural Refactoring

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor, Security** | "Audit the codebase" → select REFACTOR, accept remediation |

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
| 1 | **Audit - Code, Infra, Refactor, Security** | "Audit the codebase" (optional — for context gathering) |
| 2 | **Docs Writer** | "Create documentation for the repo" |

### Infrastructure Audit & Remediation

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor, Security** | "Audit the codebase" → select INFRA, accept remediation |

### Security Audit & Remediation

| Step | Agent | Prompt |
|------|-------|--------|
| 1 | **Audit - Code, Infra, Refactor, Security** | "Audit the codebase" → select SECURITY, accept remediation |

---

## Standalone Usage

Not everything needs a pipeline. These agents work well on their own:

- **Audit - Code, Infra, Refactor, Security** — Run anytime for a code, infrastructure, structural, or security health check
- **Single Feature - Agent** — Implement a focused change with an explicit approval gate and minimal churn
- **Test - Orchestrator** — Analyze, write, or fix tests on demand
- **05 PR - Review** — Get a readiness verdict on any diff, without running a pipeline first
- **QA - Bootstrapper** — Generate a repository's QA_AUTOMATED and QA_USER package and run it
- **Debugger** — Fix a specific frontend or backend error without a full pipeline
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

Audit agents (**Auditor - Code**, **Auditor - Infra**, **Auditor - Refactor**, **Auditor - Security**) produce reports in:

```
dev/[audit-name]/
├── [audit-name]-report.md           # Full structured findings
└── [audit-name]-summary.md          # Executive summary with priority actions
```

The **Audit - Delta** orchestrator keeps each snapshot in its own labelled directory and adds a delta from **Auditor - Delta**, all under the newer side:

```
dev/[audit-name]/
├── <baseline-label>/                # e.g. orig-code/, main/
│   ├── [audit-name]-report.md
│   └── [audit-name]-summary.md
├── <current-label>/                 # e.g. 20260725/, feature-branch/
│   ├── [audit-name]-report.md
│   └── [audit-name]-summary.md
├── [audit-name]-delta-<baseline-label>-to-<current-label>.md
├── [audit-name]-delta-<baseline-label>-to-<current-label>-open-items.md
├── [audit-name]-delta-<baseline-label>-to-<current-label>-fix-research.md
└── [audit-name]-delta-<baseline-label>-to-<current-label>-fix-research-<subsystem>.md
```

After the delta, the root spawns **Auditor - Attribution** batches to settle
every provisional finding against both trees; no regression count exists until
they return. Only then does fix research become available.

The root Audit orchestrator writes the fix-research index first as an
unvalidated DRAFT, grouping the queue and dependency closure by subsystem. It
then spawns one **Auditor - Remediation Research** sibling per subsystem. After
all exclusive subsystem reports exist, **Auditor - Remediation Reconciler**
corrects the shared audit chain; the root incorporates compact returns and marks
the index FINAL.

Each selected audit type gets its own tree and its own delta; code and infra findings are never merged into one document.

---

## VS Code / Copilot Settings

Copilot-specific. Other harnesses need no equivalent configuration.

- **`chat.subagents.allowInvocationsFromSubagents`**: Leave at `false` (default) — delegation is one level; only the user-invocable root spawns agents.
- The orchestrator's `agents:` frontmatter restricts which subagents it can spawn, preventing unintended delegation.

---

## Skills, Instructions, and Learnings

Agents reference **skills** (`source_of_truth/skills/<name>/SKILL.md`) for shared templates and formats that would otherwise be duplicated. Skills are loaded on demand when an agent's instructions say "Load the `<name>` skill."

**Instructions** (`source_of_truth/instructions/*.instructions.md`) inject cross-cutting conventions into agents automatically via `applyTo` glob patterns. Agent-targeted instructions are inlined into the generated agents at propagation time, so they cost no separate lookup at runtime.

**Learnings** (`source_of_truth/learnings/*.md`) are four seed files of durable, repo-agnostic rules:

| File | Holds |
|------|-------|
| `review-learnings.md` | Recurring review findings — guards and tests, safety-critical code, delegation and documents |
| `cross-phase-decisions.md` | Conventions that must hold across phases — identifiers and scope, verification and verdicts, capability grants, git base derivation |
| `project-learnings.md` | Framework quirks, config traps, and library behavior |
| `debugging-learnings.md` | Diagnosed root causes for pipeline gaps, harness quirks, and agent workflow failures |

They ship into a working repository at `.github/learnings/` (and, for Cursor, as agent-requested rules). This is a two-way loop: agents read them for prior art, and the **Feature - Reviewer** appends new durable rules to `review-learnings.md` and new forward-looking decisions to `cross-phase-decisions.md` as it works. Entries appended in a project stay in that project — the authored seed here stays general.

All three are authored under `source_of_truth/` and propagated per harness. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the transform model.

---

## Using These Agents in Your Own Projects

The agents deploy **user-level**, not per-repository — install once and they are available in every project you open.

```bash
python3 deploy_agents.py
```

This copies the generated per-harness outputs into the real config directories each harness reads (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.cursor`) and mirrors the Copilot port into this repo's `.github/`. See [INSTALLATION.md](INSTALLATION.md).

Do not hand-copy files out of `ports/` or `.github/` — both are generated. Edit `source_of_truth/`, propagate, then deploy.

---

## Integration Notes

- **Language-agnostic**: These agents are generic. They read your workspace's `AGENTS.md` at runtime for language-specific conventions (naming, testing tools, formatting, etc.).
- **Self-contained**: Each generated agent file is complete on its own — applicable instruction content is inlined at propagation time rather than referenced.
- **Orchestrators**: **04 Phase - Execute**, **05 PR - Review**, **Audit - Code, Infra, Refactor, Security**, **Audit - Delta**, **Test - Orchestrator**, **QA - Bootstrapper**, **Instructions Manager**, and **Client Deliverable** all delegate to hidden subagents marked `user-invocable: false`. These appear as collapsible tool calls in the chat UI.
- **Shared subagents**: **Feature - Implementer** and **Feature - Reviewer** are used by the implementation, audit, and test orchestrators. **Feature - QA Writer** is used by Phase - Execute and the Audit orchestrator. **Docs Writer** is spawned at the end of the Phase - Execute, Audit, Test, and Client Deliverable pipelines to update stale documentation, and by the Planner and Refiner when critical docs are missing (it remains user-invocable for standalone use as well). **Unity Reviewer** and **Visual Verifier** are spawned on Unity repositories — Unity Reviewer by Phase - Execute, PR - Review, and Single Feature - Agent, Visual Verifier by Phase - Execute alone. Both are hidden-only.
- **Dual-use agents**: two agents are user-invocable *and* declared as children by an orchestrator, so they emit both a slash command and a spawnable subagent file — **Docs Writer** (Planner, Refiner, Phase - Execute, Audit, Test, Client Deliverable) and **Web Researcher** (Planner, Refiner, Debugger). **03 Feature - Decomposer** is not among them: Phase - Execute fails on missing bundles rather than spawning the decomposer.
- **Subagent autonomy**: Hidden subagents operate without user confirmation — they read inputs from `dev/feature/[0N-task-name]/`, execute their role, write outputs to the same folder, and return a summary to the orchestrator.
- **Read-only subagents**: **Auditor - Code**, **Auditor - Infra**, **Auditor - Refactor**, **Auditor - Security**, **Auditor - Delta**, **Auditor - Remediation Research**, **Auditor - Remediation Reconciler**, **Test - Analyst**, **Unity Reviewer**, **Visual Verifier**, **04e Diff Security Scan**, and the **05x PR Review evaluators** do not modify production code. They analyze and write only their assigned reports or audit artifacts. **Unity Reviewer** and **Baseline Worktree** are the two that hold no write tool at all.
- **Approval-gated agents**: **01 Project - Planner**, **02 Phase - Refiner**, and **03 Feature - Decomposer** always present findings and ask for explicit approval before creating files. They also check for missing critical documentation (`README.md`, `docs/CODEBASE_CONTEXT.md`) and recommend running the **Docs Writer** before continuing. The **Audit** and **Test** orchestrators ask before proceeding to the remediation phase.
- **Code-writing agents**: **Debugger**, **Test - Writer**, **Test - Fixer**, **Feature - Implementer**, and **Feature - Reviewer** have full tool access to create and modify files.
- **Prod Code Review** does not modify code — it analyzes and reports only, producing a GO / NO-GO verdict.
