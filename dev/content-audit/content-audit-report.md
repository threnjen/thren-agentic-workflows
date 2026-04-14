# Content & Language Optimization Audit Report

**Date:** 2026-04-14
**Scope:** Full repository — all Markdown files (agents, skills, instructions, templates, documentation)
**Files Audited:** 40 files across `.github/agents/`, `.github/skills/`, `.github/instructions/`, `nodejs/`, `python/`, `docs/`, and root

---

## Executive Summary

- **Total files audited:** 40
- **Findings by severity:** Critical: 0 | High: 6 | Medium: 18 | Low: 12
- **Estimated total token savings:** 15–25% across the full repository
- **Top 5 highest-priority items:**
  1. Skills/Instructions/Agent tables repeated across 4 documentation files (High — Category 3)
  2. "Challenge User Assumptions" block duplicated verbatim across 2 agents (High — Category 1)
  3. "Proactive research over asking the user" paragraph duplicated across 3 agents (High — Category 1)
  4. Communication rules repeated identically in 4 template files (High — Category 6)
  5. Agent descriptions written 3–4 times across README, agents README, ARCHITECTURE, CODEBASE_CONTEXT (High — Category 3)

---

## Category 1: Cross-File Redundancy

Content that appears in multiple files and could be consolidated or referenced from a single source.

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1.1 | `project-planner.agent.md`, `phase-refiner.agent.md` | planner:L120-131, refiner:L55-66 | High | "Challenge User Assumptions" block duplicated verbatim | The 12-line block starting "You are not a yes-agent…" with its 4 numbered steps (Identify the conflict, Quantify the cost, Propose the simpler alternative, Let the user decide) plus the closing paragraph is character-for-character identical in both files. **Primary source:** Neither — extract to a shared instruction. **Token savings:** ~200 tokens × 1 redundant copy = ~200 tokens. |
| 1.2 | `project-planner.agent.md`, `phase-refiner.agent.md`, `debugger.agent.md` | planner:L38-39, refiner:L36-37+L71-72, debugger:L56-57 | High | "Proactive research over asking the user" paragraph repeated 3–4 times | The paragraph starting "**Proactive research over asking the user** — When you encounter an unfamiliar technology…" appears verbatim in the planner (once), refiner (twice — in sections 2A and 2B), and a near-identical variant in the debugger. All convey: "research before asking the user." **Token savings:** ~150 tokens × 3 redundant copies = ~450 tokens. |
| 1.3 | `feature-implementer.agent.md`, `feature-reviewer.agent.md` | implementer:L44-49, reviewer:L31-35 | Medium | "Tech-Stack Skill Detection" section duplicated | Both files contain the same 5-line block: "Check whether the project uses a specialized tech stack… Look for indicators: `copilot-instructions.md`… If a matching skill exists (e.g., `unity-development`), **load and read it before proceeding**". Identical logic, identical examples. **Token savings:** ~120 tokens. |
| 1.4 | `feature-implementer.agent.md`, `feature-reviewer.agent.md`, `feature-decomposer.agent.md`, `debugger.agent.md` | implementer:L37-42, reviewer:L28-30, decomposer:L31-33, debugger:L51-53 | Medium | Learnings file read list repeated in 4 agents | Each agent independently lists which `.github/learnings/*.md` files to read (project-learnings, review-learnings, debugging-learnings, cross-phase-decisions). The specific files vary slightly per agent, but the pattern — "Read the following files if they exist" + list — is repeated 4 times. Could be a shared instruction. **Token savings:** ~100 tokens × 3 = ~300 tokens. |
| 1.5 | `phase-refiner.agent.md`, `feature-decomposer.agent.md` | refiner:L82-89, decomposer:L42-51 | Medium | "Cross-Phase Decision Enforcement" section near-identical | Both files contain a "Cross-Phase Decision Enforcement" subsection with the same logic: read `cross-phase-decisions.md`, check for "Must-do before Phase N" items, and handle unaddressed items. The decomposer version is more detailed (3 branches vs 2), but the refiner version is a subset. **Token savings:** ~150 tokens. |
| 1.6 | `project-planner.agent.md`, `phase-refiner.agent.md` | planner:L25-31, refiner:L30-35+L65-69 | Medium | "Track Additional Context / DISCOVERY_CONTEXT" instructions duplicated | Both agents have multi-paragraph instructions about keeping a running list of additional context (web research, user docs, additional folders) and persisting to `DISCOVERY_CONTEXT.md`. The refiner repeats this in both the 2A and 2B paths. **Token savings:** ~200 tokens. |
| 1.7 | `feature-decomposer.agent.md`, `feature-plan-set/SKILL.md`, `dev-task-folder.instructions.md` | decomposer:L18-30, skill:L12-19, instruction:L7 | Medium | Directory numbering convention explained in 3 places | The `0N-` prefix numbering rules (start at 01, parallel features share numbers, prerequisites get lower numbers) appear in the Feature - Decomposer agent, the feature-plan-set skill, and the dev-task-folder instruction. The skill is the canonical source; the agent re-explains it. **Token savings:** ~120 tokens in agent. |
| 1.8 | `auditor-code.agent.md`, `auditor-refactor.agent.md`, `auditor-infra.agent.md` | code:L10-11, refactor:L13-14, infra:L12-13 | Low | "Load the `auditor-conventions` skill…" preamble repeated 3× | All three auditor agents contain the same sentence: "Load the `auditor-conventions` skill for standard constraints, deliverables, scope determination, file-type taxonomy, process flow, and output format." This is necessary per-agent (they each load independently), but the verbose enumeration of what the skill contains could be shortened. **Token savings:** ~30 tokens each = ~60 tokens total. |
| 1.9 | `auditor-code.agent.md`, `auditor-refactor.agent.md` | code:L18-24, refactor:L19-25 | Low | "Test File Audit Policy" structural pattern duplicated | Both agents have parallel "Test files are **in scope** but audited with a **reduced lens**" blocks with different category lists. Structure is identical; contents differ appropriately. Not actionable but noted. |
| 1.10 | `feature-implementer.agent.md`, `feature-plan-expander.agent.md`, `feature-reviewer.agent.md`, `git-commit.agent.md` | various preamble lines | Low | "You operate autonomously — do not ask questions or wait for confirmation" repeated 4× | Four hidden subagents use near-identical autonomy declarations. This is partially covered by read-only-agent's "subagent exception" clause but not via an auto-loaded instruction for non-read-only subagents. **Token savings:** ~20 tokens × 3 = ~60 tokens. |

---

## Category 2: Verbose Phrasing

Sentences or paragraphs that could be shortened significantly while preserving full intent.

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 2.1 | `read-only-agent.instructions.md` | L8-12 | Medium | 5 near-identical "You do NOT" lines | Current: "You do NOT create, modify, or delete source code files / You do NOT create, modify, or delete test files / You do NOT create, modify, or delete configuration files / You only produce planning documents…" — the first three lines are the same sentence with different file types. **Proposed:** "You do NOT create, modify, or delete source code, test, or configuration files. You only produce planning documents, analysis reports, or other deliverable documents." **Token savings:** ~40% of this section (~30 tokens). |
| 2.2 | `phase-refiner.agent.md` | L1-5 | Medium | Wordy opening paragraph | Current (52 words): "You are a **Phase Iteration Specialist** who either takes an existing Phase document from the `@01 Project - Planner` or creates one from scratch for a standalone feature, then works with the user to refine, deepen, and stress-test it before it's handed off to `@04 Phase - Execute` for automated feature decomposition and implementation." **Proposed** (30 words): "You are a **Phase Iteration Specialist**. You take an existing Phase document or create one from scratch, then iteratively refine and stress-test it before handoff to `@04 Phase - Execute`." **Token savings:** ~40%. |
| 2.3 | `feature-qa-writer.agent.md` | L28-59 | Medium | "What Requires Manual QA" over-explained | Each of the 8 bullet points has a bolded category, an italicized explanation, and a parenthetical explaining what automated tests already cover. The parentheticals are informative but verbose. E.g.: "(Mock-based API tests cover request/response shapes—manual QA covers real-network behavior.)" — The QA Writer already knows the automated/manual distinction. **Proposed:** Remove parenthetical explanations; the italicized distinction is sufficient. **Token savings:** ~200 tokens (~35% of this section). |
| 2.4 | `feature-qa-writer.agent.md` | L61-75 | Low | "What Does NOT Require Manual QA" belabors the obvious | 7 bullet points listing things like "Pure business logic — Calculations, transformations, conditional branching, state machines" and "Anything expressible as `assert X == Y`". An LLM QA agent knows these are unit-testable. **Proposed:** Consolidate to: "Exclude anything verifiable by automated tests: pure logic, validation rules, return values, error content, state transitions, permission checks, and anything expressible as `assert X == Y`." **Token savings:** ~60% of the section (~120 tokens). |
| 2.5 | `project-planner.agent.md` | L75-84 | Low | "Principles for Good Phase Boundaries" list wordy | Each of the 7 bullet points has a bolded headline followed by a verbose explanation. E.g.: "**Each phase should be independently deployable or testable** — avoid phases that only 'work' when combined with the next one." The em-dash clause repeats the bolded headline's meaning. **Token savings:** ~30% if em-dash clauses are trimmed. |
| 2.6 | `phase-execute.agent.md` | L60-85 | Low | Batch/Per-feature mode instructions duplicated in per-step conditionals | Steps 3, 4, 5, 6, and 7 all have separate "Batch mode:" and "Per-feature mode:" blocks. Some share nearly identical phrasing modulo scope words. Could use a brief up-front "differences table" and reduce inline branching. **Token savings:** ~200 tokens. |
| 2.7 | `documentation-architect.agent.md` | L30-65 | Low | Document definitions include "Must include" and "Must NOT include" lists | While appropriate for a docs writer, some of the "Must include" lists (e.g., for CODEBASE_CONTEXT.md) overlap with what the file itself demonstrates. **Token savings:** ~50 tokens. |
| 2.8 | `bootstrap-learnings-system.md` | L1-170 | Low | Entire file is a setup guide for content already wired into agents | The file explains how to create learnings files and then says "Agent Wiring (already done)." The file is useful as a user guide but ~30% of its content re-explains agent behaviors documented in the agents themselves. **Token savings:** ~150 tokens if trimmed to just the setup instructions. |

---

## Category 3: Over-Documentation

Information about skills, instructions, or agents repeated across README.md, ARCHITECTURE.md, CODEBASE_CONTEXT.md, and the agents README — the same tables/lists appearing 3–4 times.

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 3.1 | `README.md`, `.github/agents/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Multiple | High | Skills table repeated 4 times | The table mapping skills to consuming agents and contents appears in all 4 files: README.md (L164-170), ARCHITECTURE.md (L100-106), CODEBASE_CONTEXT.md (L44-48), and agents/README.md (L316-322). Each has slightly different formatting but identical information. **Proposal:** Canonical source in ARCHITECTURE.md; other files should link to it with a one-line reference. **Token savings:** ~300 tokens (3 redundant copies × ~100 tokens each). |
| 3.2 | `README.md`, `.github/agents/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Multiple | High | Instructions table repeated 4 times | Same situation as 3.1 — the instructions table (5 rows mapping instruction → applyTo → purpose) appears in all 4 documentation files. **Token savings:** ~300 tokens. |
| 3.3 | `README.md`, `.github/agents/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Multiple | High | Agent categorization and listing repeated across all 4 docs | The categorization "3 orchestrators, 7 standalone, 11 hidden subagents" with per-agent purpose descriptions appears at different levels of detail in: README.md (compact table + descriptions), agents/README.md (tables + full paragraphs for each), ARCHITECTURE.md (Mermaid + summary), CODEBASE_CONTEXT.md (bullet-point inventory). agents/README.md should be the canonical source; others should link to it. **Token savings:** ~800 tokens across 3 redundant locations. |
| 3.4 | `README.md`, `docs/ARCHITECTURE.md` | README:L89-98, ARCH:L75-85 | Medium | "Design decisions" partially duplicated | ARCHITECTURE.md has a detailed "Design Decisions" section. README.md re-explains several of the same decisions (two files per language, orchestrator + subagent pattern). **Proposal:** README.md should link to ARCHITECTURE.md for design rationale. **Token savings:** ~150 tokens. |
| 3.5 | `README.md`, `.github/agents/README.md` | README:L85-108, agents/README:L1-120 | Medium | Pipeline description written twice | README.md has a "The Project Pipeline (3 user steps)" section. agents/README.md has a more detailed version of the same pipeline. README.md should reference agents/README.md instead of re-describing. **Token savings:** ~250 tokens. |
| 3.6 | `README.md` | L196-205 | Medium | "Further Reading" section appears twice | The "Further Reading" section with links to agents/README, ARCHITECTURE, and CODEBASE_CONTEXT is duplicated at the bottom of README.md — it appears at L196 and again at L202 with different text. **Token savings:** ~60 tokens. |
| 3.7 | `README.md`, `docs/CODEBASE_CONTEXT.md` | README:L36-62, CODEBASE:L14-28 | Low | Repository structure tree nearly identical | Both files have a directory tree showing the repo structure. The CODEBASE_CONTEXT version includes inline annotations. README.md has a cleaner version. Mild redundancy since they target different audiences (humans vs agents). |
| 3.8 | `docs/CODEBASE_CONTEXT.md` | L78-95 | Low | "When Editing" rules overlap with ARCHITECTURE.md design decisions | CODEBASE_CONTEXT.md's "When Editing" section provides procedural guidance that partially overlaps with ARCHITECTURE.md's design decisions. Both explain "don't re-inline skill content in agent files," "each AGENTS.md must be independently copyable," etc. **Token savings:** ~80 tokens. |

---

## Category 4: Template Bloat

Templates or format specifications within skills and agents that could be tightened.

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 4.1 | `feature-qa-writer.agent.md` | L95-160 | Medium | QA plan template is 65+ lines with verbose scaffolding | The template includes extensive HTML comments as placeholder guidance (`<!-- One to three sentences: overall review verdict -->`), full example table structures, and detailed section headers. Many of the section contents are self-evident from the header name. E.g., "## Summary of Changes / [Brief summary of what was implemented across all features, derived from the documents]" — the agent knows what a "Summary of Changes" is. **Proposed:** Cut HTML comments to one-word hints; remove self-evident descriptions. **Token savings:** ~250 tokens (~35% of template). |
| 4.2 | `feature-implementer.agent.md` | L90-130 | Medium | Implementation record template is 40+ lines | The template has extensive table structures with example data (`src/foo.py`, `src/bar.py`) interspersed with HTML comments. The example rows add context but consume tokens. **Proposed:** Remove example rows; keep table headers and column definitions. **Token savings:** ~150 tokens (~30%). |
| 4.3 | `feature-reviewer.agent.md` | L103-155 | Medium | Review record template is 50+ lines | Same pattern: the template's HTML comments and example rows (`src/handler.py`, `src/utils.py`) consume tokens. The agent will fill these in from the actual review. **Proposed:** Remove example rows. **Token savings:** ~150 tokens (~30%). |
| 4.4 | `web-research-specialist.agent.md` | L38-80 | Low | Two full report templates with extensive structural examples | The report template and summary template include full example structures with placeholder content. Given the agent's specificity, these are useful but could be compressed — e.g., the References table example row could be inlined as "| # | Source | URL | Retrieved |" without a sample data row. **Token savings:** ~100 tokens. |
| 4.5 | `phase-document-writing/SKILL.md` | L10-65 | Low | Phase Document Template includes verbose inline comments | Four `[bracketed guidance notes]` explain what to write in each section. The section headers are self-documenting. E.g., "## Technical Context / [Existing code, patterns, libraries, or infrastructure relevant to this phase. Reference specific files/modules so the Feature - Decomposer knows where to look.]" — the guidance repeats the header's intent. **Token savings:** ~60 tokens. |
| 4.6 | `phase-final-review.agent.md` | L25-140 | Low | Prod Code Review has extensive table scaffolding | The document inventory, traceability matrix, and verdict tables are well-structured but include enough example rows to illustrate the pattern multiple times over. One example row per table would suffice. **Token savings:** ~100 tokens. |

---

## Category 5: Redundant Inline Explanations

Agent files that re-explain conventions already covered by auto-loaded instructions or skills.

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 5.1 | `feature-decomposer.agent.md` | L18-30 | Medium | Re-explains `0N-` numbering convention already in `feature-plan-set` skill and `dev-task-folder` instruction | The agent has a 15-line "Directory Numbering Convention" section explaining `0N-` prefixes, parallel numbering, dependency ordering — all of which is already in the `feature-plan-set` skill (which the agent loads) and the `dev-task-folder` instruction (which is auto-loaded). A one-line reference would suffice. **Token savings:** ~120 tokens. |
| 5.2 | `project-planner.agent.md`, `phase-refiner.agent.md` | planner:L20, refiner:L45 | Medium | Inline "Documentation Freshness Check" instructions re-explain auto-loaded instruction | Both agents say "Run the Documentation Freshness Check (see auto-loaded instructions)." but the planner also adds "Wait for the user to acknowledge before continuing to Phase 2" — which is already stated in `documentation-freshness-check.instructions.md` ("Wait for the user to acknowledge before continuing"). The inline text is a reference + partial re-statement. **Token savings:** ~20 tokens per file. |
| 5.3 | `auditor-refactor.agent.md` | L26-41 | Medium | Severity levels table re-stated despite "Use the severity meanings defined above" reference to skill | The agent says "Follow the output format from the `auditor-conventions` skill" but also includes a full Severity Levels table. The auditor-conventions skill already defines the 4-level severity structure; the agent's table provides domain-specific meanings. This is intentional customization but could be noted more clearly as "domain overrides" rather than re-stating the full table structure that's already in the skill. Low savings potential — the domain customization is necessary. |
| 5.4 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | various | Low | Orchestrators repeat "DO NOT write code/plans directly" | All three orchestrators have inline constraints like "You do NOT perform audits, write code, write reviews, or write QA plans yourself. You coordinate subagents that do." The `orchestrator-conventions.instructions.md` already states "DO NOT write source code, test files, or configuration directly / DO NOT write plan documents, review records, or QA plans directly." The agents expand on this with pipeline-specific wording. **Token savings:** ~30 tokens per agent. |
| 5.5 | `feature-decomposer.agent.md` | L38-45 | Low | Plan template reference + partial re-explanation | The agent says "Load the `feature-plan-set` skill for the plan template (sections A–F), file structure, and stage format" then also has a "Plan Template" subsection header. The actual template content lives in the skill. The agent's inline section serves as a reminder but is redundant. **Token savings:** ~20 tokens. |

---

## Category 6: Communication/Constraint Repetition

The same constraints or communication rules repeated across multiple agent files.

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 6.1 | `nodejs/AGENTS.md`, `python/AGENTS.md`, `nodejs/docs/STYLE_GUIDE.md`, `python/docs/STYLE_GUIDE.md` | AGENTS ~bottom, STYLE_GUIDE ~bottom | High | Communication section repeated identically in 4 files | The 6-line Communication section ("No preamble/postamble unless requested / No code comments unless asked / No explanations for refusals / Use ripgrep (`rg`) not `grep`/`find` / Use Read/LS tools not `cat`/`head`/`tail`/`ls` / Never guess URLs") appears identically in all 4 template files. The style guides should not repeat AGENTS.md content — the agent already loaded AGENTS.md first. **Proposed:** Remove from both style guides. The AGENTS.md files serve as the primary source. **Token savings:** ~60 tokens × 2 removed copies = ~120 tokens. |
| 6.2 | `nodejs/AGENTS.md`, `python/AGENTS.md` | Both: Principles, Process, Quality Standards, Communication | Medium | ~70% shared content between language AGENTS.md files | The Principles (9 bullets), Process/When Stuck (4 steps), Quality Standards (Every Commit Must checklist, Always, Never, Decision Priority), and Communication sections are verbatim identical in both files. Only Package Management, Testing, TypeScript Style (nodejs), and Base Classes (python) differ. This is acknowledged as "by design" in CODEBASE_CONTEXT.md ("No shared base file — each AGENTS.md is fully self-contained by design") so the redundancy is intentional. **Noted but not actionable** — the design rationale (independent copyability) is sound. |
| 6.3 | Multiple subagent files | Various | Medium | "You operate autonomously" + "do not ask questions" pattern repeated across 4 subagents | `feature-implementer.agent.md`, `feature-reviewer.agent.md` ("Be skeptical and thorough. You operate autonomously — apply fixes directly without asking for approval."), `feature-plan-expander.agent.md` ("You operate autonomously — do not ask questions or wait for confirmation. Make sensible defaults and proceed."), `git-commit.agent.md` ("You operate autonomously — do not ask questions or wait for confirmation."). The `read-only-agent` instruction covers the "subagent exception" for approval, but these agents aren't read-only — there's no shared instruction for "subagent autonomy." **Proposed:** Add a `subagent-autonomy` instruction auto-loaded via `user-invocable: false` pattern or a glob matching hidden subagents. **Token savings:** ~30 tokens × 3 = ~90 tokens. |
| 6.4 | Multiple agent files | Various | Low | "DO NOT skip any [X] category — be comprehensive" phrasing pattern | Appears in reviewer ("DO NOT skip any review category—be comprehensive"), all 3 auditors ("DO NOT skip any audit category — be comprehensive"), and the final review agent. The wording is near-identical. Minor savings if extracted. |
| 6.5 | `feature-implementer.agent.md`, `feature-reviewer.agent.md` | implementer:L133, reviewer:L105 | Low | "Do not skip this step — downstream pipeline steps depend on this file" repeated | Both agents warn against skipping the record-writing step with the same sentence. Minor redundancy. |

---

## Cross-Cutting Observations

### Pattern: Cascade Documentation

The most impactful redundancy pattern is the **cascade documentation** problem: information originates in one file (usually a skill, instruction, or an agent's own definition) but is then summarized or re-stated in `ARCHITECTURE.md`, `CODEBASE_CONTEXT.md`, `README.md`, and `agents/README.md`. When any of the 4 tables (skills, instructions, agents) changes, it must be updated in 4 places.

**Root cause:** Each documentation file targets a different audience (README→humans, CODEBASE_CONTEXT→agents, ARCHITECTURE→developers, agents/README→users of the agents), so there's a reasonable argument for different presentations. But the content itself is identical — only the framing differs.

**Recommended pattern:** Establish one canonical table location per concern. Other files should link to it with a brief contextual sentence. Specifically:
- Agent inventory + descriptions → canonical in `.github/agents/README.md`
- Skills table → canonical in `docs/ARCHITECTURE.md`
- Instructions table → canonical in `docs/ARCHITECTURE.md`
- Design decisions → canonical in `docs/ARCHITECTURE.md`

### Pattern: Instruction-Worthy Content Inline in Agents

Several pieces of content are shared across 2–4 agents but haven't been extracted into an instruction file:
- "Challenge User Assumptions" (planner + refiner)
- Learnings file read lists (implementer + reviewer + decomposer + debugger)
- "Proactive research over asking the user" (planner + refiner + debugger)
- Tech-Stack Skill Detection (implementer + reviewer)
- Cross-Phase Decision Enforcement (refiner + decomposer)

Each could become a targeted instruction with an appropriate `applyTo` glob, eliminating 200–400 tokens of redundancy per extraction.

### Pattern: By-Design Duplication in Templates

The `nodejs/AGENTS.md` and `python/AGENTS.md` files share ~70% identical content. This is documented as intentional ("each AGENTS.md must be independently copyable"). The Communication section appearing in the style guides is NOT covered by this design rationale and should be removed from the style guides.

---

## Recommended Priority Order

### 1. Quick Wins (low effort, high impact)

1. **Remove Communication section from both style guides** (Finding 6.1) — Delete 6 lines from each style guide. Saves ~120 tokens. No cross-reference needed; AGENTS.md already loads first.
2. **Remove duplicate "Further Reading" section from README.md** (Finding 3.6) — Delete the second copy. Saves ~60 tokens.
3. **Trim read-only-agent.instructions.md constraint list** (Finding 2.1) — Consolidate 3 similar lines into 1. Saves ~30 tokens.
4. **Remove parenthetical explanations from QA Writer's "What Requires Manual QA"** (Finding 2.3) — The italicized text is sufficient. Saves ~200 tokens.

### 2. Important Consolidations (medium effort, significant savings)

5. **Establish canonical locations for Skills, Instructions, and Agent tables** (Findings 3.1, 3.2, 3.3) — Keep full tables in their primary location; replace with links + one-line summary in other docs. Saves ~1,400 tokens across 3 concerns.
6. **Extract "Challenge User Assumptions" into a shared instruction** (Finding 1.1) — Create `.github/instructions/challenge-assumptions.instructions.md` with `applyTo` to planner + refiner. Remove inline text from both agents. Saves ~200 tokens.
7. **Extract "Proactive research over asking the user" into a shared instruction** (Finding 1.2) — Create an instruction or add to an existing one. Apply to planner, refiner, debugger. Saves ~450 tokens.
8. **Trim template bloat in QA Writer, Implementer, Reviewer** (Findings 4.1–4.3) — Remove HTML comments and example rows from templates. Saves ~550 tokens.

### 3. Major Reorganizations (higher effort, completed savings)

9. **Create shared instructions for recurring cross-agent content** (Findings 1.3–1.7) — New instructions for Tech-Stack Skill Detection, Learnings File Reading, Cross-Phase Decision Enforcement, Discovery Context Tracking. Requires `applyTo` design and testing across agents. Saves ~800+ tokens.
10. **Restructure documentation hierarchy** (Pattern observation) — Establish formal canonical-source → reference pattern. Requires coordinated edits to README.md, ARCHITECTURE.md, CODEBASE_CONTEXT.md, and agents/README.md. Saves ~2,000+ tokens and prevents future drift.

---

## Token Savings Estimates

| Category | Estimated Token Savings | Files Affected |
|----------|------------------------|----------------|
| Category 1: Cross-File Redundancy | ~1,400 tokens | 10+ files |
| Category 2: Verbose Phrasing | ~800 tokens | 8 files |
| Category 3: Over-Documentation | ~1,900 tokens | 4 documentation files |
| Category 4: Template Bloat | ~800 tokens | 6 files |
| Category 5: Redundant Inline Explanations | ~250 tokens | 5 files |
| Category 6: Communication/Constraint Repetition | ~330 tokens | 8 files |
| **Total** | **~5,500 tokens** | **~25 unique files** |

This represents approximately **15–20% of the total documentation content** in the repository.
