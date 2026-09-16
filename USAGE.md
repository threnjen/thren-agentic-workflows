# Agents

Specialized agents for structured software development workflows. The core workflow uses an **orchestrator + subagent** pattern — you interact with a few agents, and the orchestrator drives the rest automatically. A **manual implementation path** is also available for users who prefer to write their own code.

---

## How to Use an Agent

These agents deploy to Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot. How you reach one depends on the harness:

| Harness | How to invoke |
|---------|---------------|
| Claude Code | `/agent-name` slash command, or ask for the agent by name |
| Cursor | `/agent-name` slash command (needs Cursor 2.4 or later) |
| GitHub Copilot | Agent picker dropdown at the top of the Copilot Chat panel in VS Code |
| Codex | Name the agent explicitly in the prompt: `as phase-execute, ...'` |
| OpenCode | Name the agent in the prompt |

Only the 16 user-facing agents are reachable this way. The rest are spawned by orchestrators.

Be specific in your request. Each agent produces structured output — plan documents, implementation summaries, review tables, audit reports.

---

## The Project Pipeline (4 user steps)

The core development workflow. **You drive steps 1–2, step 3 runs to a verdict, and step 4 checks the finished local range.**

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU                                                            │
│                                                                 │
│  Step 1: 01 Project - Planner     → Phase documents             │
│  Step 2: 02 Phase - Refiner       → Refined phase document      │
│  Step 3: 03 Phase - Execute       → Plan, build, QA ────────┐    │
│                                                            │    │
│  Step 4: 04 Phase - Final Checks → Local readiness check       │    │
│          (after the automated run reports back)            │    │
└────────────────────────────────────────────────────────────│────┘
                                                             │
┌────────────────────────────────────────────────────────────│────┐
│  AUTOMATED (subagents)                                     │    │
│                                                            ▼    │
│  Feature - Plan Author  → Plans + deltas + graph + manifest      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  FOR EACH FEATURE (in manifest execution order):         │    │
│  │  A. Plan Author             → Selection delta            │    │
│  │  B. Feature - Implementer   → Code + tests (TDD)         │    │
│  │  C. 03c Plan Conformance    → One review + repair pass   │    │
│  │  D. Integration test gate   → Union of affected suites   │    │
│  │  E. Complete                → Manifest revalidated       │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  Optional QA Writer + Runner → Only when selected                 │
│  Prod Code Review       → GO / NO-GO verdict                     │
│  Docs Writer            → Only after a positive verdict          │
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

Interactive — you iterate to probe edge cases and dependencies before execution.

### Step 3: Execute the Phase

| Agent | Prompt | Output |
|-------|--------|--------|
| **03 Phase - Execute** | "Execute this phase" + attach refined phase doc | Feature plans, implementation, review, QA, and final verdict |

The orchestrator asks once for model overrides, optional QA, and any applicable dirty-run choice. It then:

1. Reads `dev/feature/[phase-name]-execution-manifest.md`, or spawns **Feature - Plan
   Author** to decompose the phase and write it. The manifest is the living schedule and
   the single source of truth once it exists.
2. Runs the authoritative suite before planning or child-agent work.
3. For each feature in manifest execution order, runs five stages:
   - **A. Select** → Plan Author verifies the selected scope and writes one `-delta.md`
   - **B. Implement** → implements every acceptance criterion with Red-Green-Refactor TDD
   - **C. Review** → Plan Conformance reviews and repairs once
   - **D. Integration gate** → runs the union of affected suites to catch breakage of
     earlier features
   - **E. Complete** → records the result in the manifest, then has the Plan Author
     revalidate affected manifest entries against what just landed
4. Runs consolidated QA only when you selected it
5. Runs **Prod Code Review**
6. Runs **Docs Writer** only after `GO` or `GO WITH CONDITIONS`
7. Reports the verdict and points you to `phase-final-checks` for the local range review

### Step 4: Self-Review Before Opening the PR

| Agent | Prompt | Output |
|-------|--------|--------|
| **04 Phase - Final Checks** | "Review my change before I open the PR" | Readiness report on the diff between a confirmed base and head commit |

Confirms the base and optional context, then runs the applicable evaluators over that
fixed range. It writes a plain-language readiness report before offering one bounded
repair pass. It never posts, pushes, commits, or requires an open merge request.
**Prod Code Review** remains the separate pipeline gate inside Step 3.

### Manual Implementation Path

Prefer to write your own code? Use the planning agents, then implement yourself:

```
Step 1: 01 Project - Planner   → Phase documents
Step 2: 02 Phase - Refiner      → Refined phase document
Step 3: (you write the code from the phase plan)
Step 4: 04 Phase - Final Checks          → Readiness report on what you wrote
```

The refined Phase document from Step 2 contains detailed scope, requirements, and acceptance criteria — enough to implement directly. When you're ready for validation, run **04 Phase - Final Checks** to get a readiness verdict on your diff.

**Tip:** The refined Phase document contains the scope and acceptance criteria. Use **03 Phase - Execute** when you want the agent to create the feature schedule and run the implementation pipeline.

---

## Available Agents

### User-Facing (directly invocable)

| Agent | Purpose |
|-------|---------|
| **01 Project - Planner** | Create a project roadmap broken into phases |
| **02 Phase - Refiner** | Refine and deepen an individual Phase document |
| **03 Phase - Execute** | Orchestrate full phase execution from a prepared manifest and feature bundles |
| **04 Phase - Final Checks** | Review a confirmed local range, write an advisory readiness report, and optionally apply one bounded repair pass |
| **Client Deliverable** | Produce the client deliverable package for a modernization engagement — audits each before/after repository pair and compares the two sides |
| **Audit - Code, Infra, Refactor, Security** | Audit code quality, infrastructure, architecture, or security in one repository, with optional fix research and automated fix pipeline |
| **Audit - Delta** | Audit two revisions or checkouts of the same product and reconcile them into a delta of what changed, with optional fix research and automated fix pipeline |
| **Instructions Manager** | Create a scoped AI coding instruction set, or blind A/B-test whether a change to one is an improvement |
| **Single Feature - Agent** | Handle small, focused changes with a proposal + explicit permission gate before implementation |
| **Debugger** | Diagnose and fix frontend or backend application errors |
| **PR Author** | Write a pull request body from the real diff, the verified evidence, and the known limitations |
| **Docs Writer** | Create or update repo documentation; also spawned automatically by orchestrators after pipeline completion |
| **QA - Bootstrapper** | Bootstrap a repository's QA package — generate QA_AUTOMATED and QA_USER from available starter inputs, run the automated runbook, and stamp pass/fail results |
| **Test - Orchestrator** | Orchestrate test analysis, writing, or fixing with optional remediation pipeline |
| **Web Researcher** | Research a topic and produce a structured findings report and executive summary saved to `dev/research/[topic-name]/` |
| **Creative - Developmental Editor** | Developmental editing for fiction against an Obsidian vault — interrogates, diagnoses, and pressure-tests your material under a mode gate. Isolated from the engineering corpus; see `docs/CREATIVE_TOOLKIT.md` |

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
| **02a Phase - Final-Check Reviewer** | Phase - Refiner | Cold-start, response-only review of a completed Phase document |
| **Feature - Plan Author** | Phase - Execute | Decompose the phase into lightweight plans, build the prerequisite graph, and own the living execution manifest |
| **Feature - Implementer** | Phase - Execute, Audit orchestrator, Test orchestrator | Implement a feature plan using Red-Green-Refactor TDD |
| **03c Reviewer - Plan Conformance** | Phase - Execute, Audit orchestrator, Test orchestrator | Review plan conformance, block on unrun tests, and produce a review record |
| **Feature - QA Writer** | Phase - Execute, Audit orchestrator | Write the automated QA document and the manual QA plan, sorting every check between them |
| **Feature - QA Runner** | Phase - Execute, Audit orchestrator | Execute the automated QA document and record per-check results into it |
| **QA - Doc Generator** | QA - Bootstrapper | Generate the QA_AUTOMATED runbook and QA_USER checklist from repository, manual QA, and acceptance inputs |
| **QA - Runner** | QA - Bootstrapper | Execute the QA_AUTOMATED runbook and all test suites, then record binary pass/fail results into the runbook |
| **Baseline Worktree** | 04 Phase - Final Checks | Create or reuse a clean detached worktree at a caller-specified baseline commit and return its path |
| **04b Change Narrator** | 04 Phase - Final Checks | Build the base-to-head narrative for the diff under review and identify churn hotspots |
| **04d Consistency Auditor** | 04 Phase - Final Checks | Compare the branch diff against established repository conventions and recommend canonical forms |
| **04e Dependency Auditor** | 04 Phase - Final Checks, Client Deliverable | Inventory dependencies added by the branch and report supply-chain and duplication risks, offline |
| **03e Diff Security Scan** | 04 Phase - Final Checks | Perform a diff-scoped security scan of only the files changed by an execution and write a compact security report |
| **Unity Reviewer** | Phase - Final Checks, Single Feature - Agent | Review Unity C# code for architecture, performance, style, and Unity-specific pitfalls |
| **Prod Code Review** | Phase - Execute, Audit orchestrator | Final pre-production readiness gate — cross-validate every pipeline document in a phase and produce a GO / NO-GO verdict |
| **04f Test Health** | 04 Phase - Final Checks | Check changed tests for authentic failure power and report supplied coverage evidence |
| **04h Cleanliness Auditor** | 04 Phase - Final Checks | Check branch-added artifacts, duplication, dead code, mixed concerns, and module growth |
| **04g Readiness Synthesizer** | 04 Phase - Final Checks | Synthesize evaluator reports and optional context into readiness and repair candidates |
| **04i Local Review Fixer** | 04 Phase - Final Checks | Apply one plan-independent repair pass to eligible local findings and record test evidence |
| **Client Deliverable - Prepare** | Client Deliverable | Prepare a client engagement for comparison analysis — validate the engagement config, then ensure an analysis branch, a code graph, and a baseline snapshot per side |
| **Client Deliverable - Delta Synthesizer** | Client Deliverable | Produce the client-facing findings report, the SOW-exclusions partition, and the internal remediation recommendations for a pair |
| **Client Deliverable - Security Narrative** | Client Deliverable | Write the four-section client-facing security narrative and the internal engineer-facing security-delta report from the pair's reports and exclusions partition |
| **Client Deliverable - Pricing Researcher** | Client Deliverable | Turn scan/dependency change evidence into cited cloud/cost claims via live pricing research, plus an internal cost-basis report (sole web-granted engagement agent) |
| **Client Deliverable - Narrative Writer** | Client Deliverable | Write the business design document, intended-behavior specification, and before/after workflow narratives for a pair, plus the internal narrative-basis report |
| **Client Deliverable - Compliance Writer** | Client Deliverable | Walk SOW acceptance criteria against retained artifacts; write the compliance walkthrough, verification summary, and internal compliance-basis report |
| **Client Deliverable - Manifest Assembler** | Client Deliverable | Assemble the package manifest per its schema, evaluating every row's present/missing status from disk, plus the internal manifest-basis report |
| **Client Deliverable - Gap Reviewer** | Client Deliverable | Review the deliverable set from the client's perspective against the manifest; always emit the internal gap-review report |
| **Creative - Scribe** | Creative - Developmental Editor | Write caller-supplied text verbatim into the vault's editor notes and scene summaries — the family's only write bit |
| **Creative - Compliance Check** | Creative - Developmental Editor | Scan a draft response against the active mode's rules and return violations with repair instructions |
| **Creative - Vault Sync** | Creative - Developmental Editor | Report what changed in the vault since the commit recorded in `context/index.md` |
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

**03 Phase - Execute** (orchestrator — delegates to subagents)
> Give it a refined Phase document. It writes lightweight plans and the living execution manifest, creates one selection delta per feature, implements sequentially, runs optional QA, and closes with Prod Code Review.

**04 Phase - Final Checks** (orchestrator — delegates to evaluators)
> Confirm a base and optional context for any local change. The command fixes one `base..HEAD` range, runs only the applicable checks, and writes an advisory report. It then offers one repair pass for confirmed security, outward-impact, and changed-test findings. `pr-review` invokes this same workflow as an alias.

**Client Deliverable** (orchestrator — delegates to the engagement subagents)
> Give it an engagement configuration file path. It produces the client-facing deliverable package — findings report, security narrative, cloud/cost analysis, business and workflow narratives, the SOW compliance walkthrough and verification summary, and the package manifest — by auditing each before/after repository pair and comparing the two sides, closing with a client-perspective gap review. Mechanically: it spawns Client Deliverable - Prepare unchanged, then drives each pair's analysis stages through subagents, holding only statuses and artifact pointers. It maintains `engagement-state.md` as its run record and resumes from it on restart.

**Audit - Code, Infra, Refactor, Security** (orchestrator — delegates to subagents)
> Asks which audit type to run (CODE, INFRA, REFACTOR, or SECURITY — multi-select), delegates to the appropriate auditor subagents, and presents findings for **one** repository. Optionally queues the open findings by severity threshold and researches fixes for them (Auditor - Remediation Research → Auditor - Remediation Reconciler), then drives automated remediation by converting findings into task plans and running them through the Feature - Implementer → 03c Reviewer - Plan Conformance → Feature - QA Writer pipeline. After remediation, updates documentation via the Docs Writer. Two checkouts or two branches belong to **Audit - Delta** instead.

**Audit - Delta** (orchestrator — delegates to subagents)
> The comparative counterpart. Confirms the targets, snapshot labels, and which side is the baseline; materializes any git refs into read-only worktrees via Baseline Worktree; runs the full type × target matrix of auditors under identical prompts; then spawns Auditor - Delta per (type, pair) to reconcile each into a delta plus an open-items queue. All deliverables land on the newer side. Shares the same optional fix-research and remediation pipeline as the single-target orchestrator.

**Single Feature - Agent** (direct implementation path)
> Handles small-scope changes (typically up to a few files) without full pipeline artifacts. It investigates, proposes a focused plan, asks for explicit permission before implementation, executes minimal changes, and verifies results. When scope expands, it recommends switching to **03 Phase - Execute**.

**Test - Orchestrator** (orchestrator — delegates to subagents)
> Asks which test operation to run (ANALYZE, WRITE, or FIX), delegates to the appropriate test subagent, and presents results. Optionally drives remediation of findings through the Feature - Implementer → 03c Reviewer - Plan Conformance pipeline. After remediation, updates documentation via the Docs Writer.

**Debugger** (full tool access — reads and writes code)
> Give it an error message or description — frontend or backend. Triages the issue, classifies it (build-time, runtime, database, dependency, etc.), investigates, and applies minimal targeted fixes. On repos with `docs/phases/`, it also syncs the affected phase documents so they stay baseline-truth. Handles both frontend (TypeScript, React, build tools) and backend (Node.js, Python, databases, auth) errors.

**PR Author** (read-only over the repository — writes only the PR body)
> Point it at a branch you are ready to publish. It reads the real diff, the evidence that
> actually ran, and the limitations you know about, then writes a pull request body framed
> around the decision a reviewer has to make before merge. It invents no validation and
> modifies no source, tests, configuration, or pipeline document.

**QA - Bootstrapper** (orchestrator — delegates to subagents)
> Point it at a repository that has no QA package. It spawns **QA - Doc Generator** to write the `QA_AUTOMATED` technical runbook and the `QA_USER` manual acceptance checklist from the repository plus any starter inputs (existing manual QA notes, an SOW or contract, plan acceptance criteria), then spawns **QA - Runner** to execute the runbook end to end and stamp binary pass/fail results back into it.

**Instructions Manager** (router — delegates to subagents)
> Give it a request to create or assess AI coding instruction files (`.github/instructions/`, `copilot-instructions.md`, `.cursorrules`, `CLAUDE.md`, or equivalent). It routes to the **Instructions - Writer** to draft new scoped instruction sets, or to the **Instructions - Evaluator** to A/B-test whether proposed instruction changes are improvements or regressions.

**Web Researcher** (read-only — uses fetch and web search)
> Give it a problem or topic. Searches across GitHub issues, Stack Overflow, Reddit, forums, and docs. Produces two deliverable documents saved to `dev/research/[topic-name]/`: a full structured findings report (`[topic-name]-report.md`) with inline numbered citations and a References table, and an executive summary (`[topic-name]-summary.md`) with priority recommendations and key reference links. Every factual claim traces back to a numbered citation. Sources older than 2 years are flagged with ⚠️.

**Docs Writer** (reads codebase, writes documentation)
> Give it a repo to document. Produces or updates the README, ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT, and TROUBLESHOOTING documents. Also spawned automatically at the end of orchestrator pipelines to update stale documentation after code changes.


### Hidden Subagents

**Unity Reviewer** *(subagent of PR - Review and Single Feature - Agent)* — Spawned on repositories with a Unity layout. Runs the repository's compile gate, adds a batch asset-import gate when the change touches serialized assets, then reviews against the Unity reference categories. It reports what each check proves and never edits source.

**Feature - Implementer** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads the explicit pipeline contract, implements each acceptance criterion using Red-Green-Refactor TDD, and writes `[task-name]-implementation.md`. Phase uses plan, delta, and manifest. Audit and Test use plan, context, and tasks.

**03c Reviewer - Plan Conformance** *(subagent of Phase - Execute, Audit orchestrator, Test orchestrator)* — Reads the explicit pipeline contract, reviews and repairs plan conformance once, requires authoritative test evidence, and writes `[task-name]-review.md`.

**Feature - QA Writer** *(subagent of Phase - Execute, Audit orchestrator)* — Reads the pipeline docs and sorts every check three ways. A command with a deterministic expected result goes to the automated QA document. A human-only check goes to the manual QA plan. A hybrid check is split: the command goes to the automated document, the judgment to the manual one. Batch mode writes one set covering the whole phase; per-feature mode writes into the feature's own directory.

**Feature - QA Runner** *(subagent of Phase - Execute, Audit orchestrator)* — Executes the automated QA document, compares each check's actual output to its stated expected result, and records per-check status plus a Run results section back into that document. Never fixes what a check exposes. Not to be confused with `QA - Runner`, which executes the repository-wide `docs/QA_AUTOMATED.md` runbook.

**Feature - Plan Author** *(subagent of Phase - Execute)* — Owns `initial`, `select`, and `revalidate` modes. It writes lightweight plans and the manifest, writes one delta for the selected feature, and updates only affected manifest fields after completion.

**02a Phase - Final-Check Reviewer** *(subagent of Phase - Refiner)* — A stateless cold-start read of a completed Phase document. It has no memory of the refinement conversation, which is the point: it reports only what the document itself says, so anything the refiner and the user settled verbally but never wrote down shows up as a gap.

**03e Diff Security Scan** *(subagent of 04 Phase - Final Checks)* — Performs a diff-scoped security review of changed files plus immediate security context. It writes a compact report and does not replace the full-codebase Auditor - Security scan.

**Prod Code Review** *(subagent of Phase - Execute and the Audit orchestrator)* — Cross-validates all pipeline documents across all features in the phase, verifies the actual code matches the records, runs the test suite, and produces a **GO / GO WITH CONDITIONS / NO-GO** verdict with a full traceability matrix and risk register. Pipeline-internal only (`user-invocable: false`): orchestrators spawn it as the automated gate at the end of a phase. For an on-demand readiness check of your own, use **04 Phase - Final Checks** instead.

**QA - Doc Generator** *(subagent of QA - Bootstrapper)* — Generates the `QA_AUTOMATED` runbook and the `QA_USER` manual acceptance checklist from the repository plus optional manual-QA, SOW/contract, and plan-acceptance inputs, per the `qa-generation` skill.

**QA - Runner** *(subagent of QA - Bootstrapper)* — Executes the `QA_AUTOMATED` runbook end to end — every runbook check plus every discovered test suite — with strict binary PASS/FAIL mapping and captured evidence, recording per-check results and the overall verdict back into the runbook's Run results section, per the `qa-run` skill.

**Auditor - Code** *(subagent of Audit orchestrator)* — Audits every source file for cleanup, bugs, security, type hints, readability, DRY, and consistency. Produces a structured report.

**Auditor - Infra** *(subagent of Audit orchestrator)* — Evaluates Dockerfiles, CI/CD pipelines, IaC templates, and config files for security, best practices, and operational risk.

**Auditor - Refactor** *(subagent of Audit orchestrator)* — Evaluates codebase-level organization: module structure, dependency graphs, component decomposition, coupling, cohesion, and separation of concerns.

**Auditor - Security** *(subagent of Audit orchestrator and Client Deliverable)* — Audits every in-scope file against ten fixed security categories: secrets, dependencies and supply chain, attack surface and injection, authentication and authorization, data protection and cryptography, API and input boundaries, filesystem/process/runtime safety, infrastructure and CI/CD, observability, and cross-cutting security architecture. Redacts every secret value, records each category as assessed-clean or not-assessed so the two are never confused, and produces a structured report plus executive summary. (Distinct from the hidden **03e Diff Security Scan**, which only covers a single pass's diff.)

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

**Creative - Scribe** *(subagent of Creative - Developmental Editor)* — Writes text it was handed, where it was told to put it, into the vault's `_editor-notes/` and `scene-summaries/`. Append-only except for the context directory. It holds the only write tool in the creative family and forms no opinion about the manuscript, which is what keeps the editor unable to write to canon or drafts.

**Creative - Compliance Check** *(subagent of Creative - Developmental Editor)* — Receives a draft response plus the mode it was written under and decides whether it complies, returning violations with repair instructions. Read-only and stateless.

**Creative - Vault Sync** *(subagent of Creative - Developmental Editor)* — Resolves the vault's current git SHA, compares it to the one recorded in `context/index.md`, and returns the file-level diff. It reports the change and does not interpret it.

**Test - Analyst** *(subagent of Test orchestrator)* — Classifies tests by value, flags redundancy and over-mocking, and writes a categorized inventory with a staged reduction plan.

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
- **04 Phase - Final Checks** — Get a readiness verdict on any diff, without running a pipeline first
- **QA - Bootstrapper** — Generate a repository's QA_AUTOMATED and QA_USER package and run it
- **Debugger** — Fix a specific frontend or backend error without a full pipeline
- **Web Researcher** — Research a technical question or debug a tricky issue
- **Docs Writer** — Update documentation after any significant change

---

## Task Documentation Pattern

The pipeline subagents produce output in the `dev/feature/[0N-task-name]/` directory (numbered by execution order). After a full feature cycle, the folder contains:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md              # Lightweight plan (Feature - Plan Author)
├── [0N-task-name]-delta.md             # Selection findings (Feature - Plan Author)
├── [0N-task-name]-implementation.md    # Files changed, AC traceability (Feature - Implementer)
└── [0N-task-name]-review.md            # Verdict and issues found (03c Reviewer - Plan Conformance)
```

Audit and Test keep their existing `-plan.md`, `-context.md`, and `-tasks.md` planning contract.

**Batch mode:** The **Feature - QA Writer** produces a single consolidated QA document covering ALL features in the phase:

```
docs/phases/[phase-name]/[phase-name]_QA.md                # Consolidated manual QA checklist
docs/phases/[phase-name]/[phase-name]_QA_AUTOMATED.md      # Automated checks, run by Feature - QA Runner
docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md   # AC coverage map (automated vs manual)
```

If `docs/phases/` does not exist, the QA doc falls back to `dev/feature/[phase-name]-qa.md`.

**Per-feature mode:** QA and review documents are written inside the feature's own directory:

```
dev/feature/[0N-task-name]/[0N-task-name]-qa.md                 # Manual QA plan for this feature
dev/feature/[0N-task-name]/[0N-task-name]-qa-automated.md       # Automated QA checks for this feature
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

**Learnings** live in the repository being worked on, under `docs/learnings/`. Nothing is authored or shipped from here; the `learnings-bootstrap` instruction owns the routing table:

| File | Holds |
|------|-------|
| `review-learnings.md` | Recurring review findings — guards and tests, safety-critical code, delegation and documents |
| `cross-phase-decisions.md` | Conventions that must hold across phases — identifiers and scope, verification and verdicts, capability grants, git base derivation |
| `project-learnings.md` | Framework quirks, config traps, library behavior, and diagnosed root causes for pipeline gaps, harness quirks, and agent workflow failures |

Agents read every existing learnings file before starting and append to them as they work — **03c Reviewer - Plan Conformance** adds recurring defect classes to `review-learnings.md` and forward-looking decisions to `cross-phase-decisions.md`, **Debugger** adds diagnosed root causes to `project-learnings.md`. Entries stay in the project that produced them.

Agents, skills, and instructions are authored under `source_of_truth/` and propagated per harness. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the transform model.

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
- **Orchestrators**: **03 Phase - Execute**, **04 Phase - Final Checks**, **Audit - Code, Infra, Refactor, Security**, **Audit - Delta**, **Test - Orchestrator**, **QA - Bootstrapper**, **Instructions Manager**, and **Client Deliverable** all delegate to hidden subagents marked `user-invocable: false`. These appear as collapsible tool calls in the chat UI.
- **Shared subagents**: **Feature - Implementer** and **03c Reviewer - Plan Conformance** serve the phase, audit, and test pipelines through explicit artifact contracts. **Feature - QA Writer** and **Feature - QA Runner** serve Phase - Execute and Audit. **Docs Writer** updates stale documentation after positive pipeline outcomes and remains user-invocable.
- **Dual-use agents**: two agents are user-invocable *and* declared as children by an orchestrator, so they emit both a slash command and a spawnable subagent file — **Docs Writer** (Planner, Refiner, Phase - Execute, Audit, Test, Client Deliverable) and **Web Researcher** (Planner, Refiner, Debugger).
- **Subagent autonomy**: Hidden subagents operate without user confirmation — they read inputs from `dev/feature/[0N-task-name]/`, execute their role, write outputs to the same folder, and return a summary to the orchestrator.
- **Read-only subagents**: **Auditor - Code**, **Auditor - Infra**, **Auditor - Refactor**, **Auditor - Security**, **Auditor - Delta**, **Auditor - Remediation Research**, **Auditor - Remediation Reconciler**, **Test - Analyst**, **Unity Reviewer**, **03e Diff Security Scan**, and the `04a` through `04h` final-check evaluators do not modify production code. **04i Local Review Fixer** may edit during its one accepted repair pass.
- **Approval-gated agents**: **01 Project - Planner** and **02 Phase - Refiner** present findings and ask for explicit approval before creating files. They also check for missing critical documentation (`README.md`, `docs/CODEBASE_CONTEXT.md`) and recommend running the **Docs Writer** before continuing. The **Audit** and **Test** orchestrators ask before proceeding to the remediation phase.
- **Code-writing agents**: **Debugger**, **Test - Writer**, **Test - Fixer**, **Feature - Implementer**, and **04i Local Review Fixer** can modify files within their contracts.
- **Prod Code Review** does not modify code — it analyzes and reports only, producing a GO / NO-GO verdict.
