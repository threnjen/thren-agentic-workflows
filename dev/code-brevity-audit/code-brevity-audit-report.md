# Code Brevity Audit Report

**Date:** 2026-03-30
**Scope:** All files in `.github/agents/`, `.github/skills/`, `.github/instructions/`
**Total files audited:** 31 (20 agent files + 5 skill files + 5 instruction files + 1 README)
**Focus:** Brevity — can files be reduced without losing context or capabilities?

**Findings by severity:**
- **HIGH**: 4
- **MEDIUM**: 10
- **LOW**: 12
- **Total**: 26

---

## Findings by Category

### 1. Duplicated Content (DRY Violations)

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | phase-execute L31–L39, audit L79–L87, test L73–L81 | HIGH | Branch creation logic triplicated | All 3 orchestrators repeat the full branch creation procedure (retry on existing name, suffix logic, error handling for uncommitted changes) already defined in the auto-loaded `orchestrator-conventions.instructions.md`. Each copy is ~10 lines. Only the prefix (`phase/`, `audit/`, `test/`) varies. **Estimated savings: ~50 words × 3 = ~150 words** if orchestrators just specify their prefix and reference the convention. |
| 2 | `project-planner.agent.md`, `phase-refiner.agent.md`, `feature-decomposer.agent.md`, `test-analyst.agent.md` | planner L20, refiner L29–L36, decomposer L20–L22, analyst L15–L17 | HIGH | Read-only constraints restated despite auto-loaded instruction | `read-only-agent.instructions.md` applies to all 4 agents via `applyTo` globs and already specifies: no creating/modifying/deleting source code, test files, or config files; approval before writing; present findings first. Each agent restates "You NEVER touch the codebase" and related constraints. The agents should only state domain-specific restrictions beyond what the instruction provides. **Estimated savings: ~40 words per file × 4 = ~160 words.** |
| 3 | `project-planner.agent.md`, `phase-refiner.agent.md`, `feature-decomposer.agent.md` | planner L21, refiner L36, decomposer L22 | MEDIUM | Identical "no code blocks" constraint in 3 files | Exact text "You do NOT write code blocks — link to files and reference `symbols` instead" appears in all 3 agents. Could be added to `read-only-agent.instructions.md` once and removed from all 3 agents. **Estimated savings: ~45 words.** |
| 4 | `phase-execute.agent.md`, `dev-task-folder.instructions.md` | phase-execute L55–L63 | MEDIUM | QA output path fallback logic duplicated | Phase - Execute Step 3 has a 3-step fallback for determining QA output path and coverage map path. This same hierarchical logic (docs/phases → dev/feature fallback) is already documented in `dev-task-folder.instructions.md` (Consolidated QA Documents table), which auto-loads for all agents. **Estimated savings: ~80 words.** |
| 5 | `audit-code-or-infra.agent.md`, `dev-task-folder.instructions.md` | audit L112–L115 | MEDIUM | QA path convention restated in audit orchestrator | The audit orchestrator specifies `dev/[audit-name]/[audit-name]-qa.md` and coverage map paths, which are already defined in the auto-loaded `dev-task-folder.instructions.md`. **Estimated savings: ~30 words.** |
| 6 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md` | phase-execute L81–L96, audit L135–L155 | MEDIUM | GO/NO-GO reporting templates are verbose and similar | Both orchestrators have ~15-line reporting templates for GO and NO-GO results. The structure is nearly identical, differing only in field labels (Features/Tasks, Phase/Audit). Could be extracted to a shared skill or condensed. **Estimated savings: ~100 words if consolidated.** |
| 7 | `auditor-code.agent.md` | L31–L58 | LOW | Exclusion lists mirror each other across auditor agents | auditor-code has a ~25-line exclusion list; auditor-infra has a ~20-line exclusion list that's the inverse. While domain-specific, some entries are obvious given the domain focus statement (e.g., `.gitignore` in IDE exclusions). **Estimated savings: ~30 words per file if obvious exclusions are dropped.** |
| 8 | `auditor-code.agent.md` | L85–L86, L114–L115 | LOW | "Bare except" referenced in both Category 2 and Category 10 | Category 2 (Errors & Defects) includes "bare `except` clauses" and Category 10 (Error Handling Patterns) includes "bare/overly broad `except` catching too many failure modes." Cross-reference rather than restate. **Estimated savings: ~15 words.** |

### 2. Verbose/Redundant Prose

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 9 | `phase-refiner.agent.md` | L10–L27 | HIGH | Oversized ASCII pipeline diagram | The "Where You Sit in the Pipeline" section uses a 15-line ASCII diagram to show two entry points (from Planner vs. standalone). The same information could be conveyed in 4 lines of prose or a compact table. **Estimated savings: ~80 words.** |
| 10 | `phase-refiner.agent.md` | L38–L68 | HIGH | "Question Triage" section is wordy | The ASK list (6 items), DON'T ASK list (5 items), and "the test" paragraph total ~25 lines. Several items are overlapping (e.g., "Business rules that determine user-visible behavior" and "User experience decisions where the answer depends on business context"). The test paragraph restates the principle. Could be compressed to ~15 lines. **Estimated savings: ~80 words.** |
| 11 | `phase-refiner.agent.md` | L70–L120 | MEDIUM | 7 Iteration Focus Areas are verbose | Each of the 7 focus areas has 4–5 bullet points, many asking rhetorical questions. E.g., "What happens when things go wrong? (Network failures, invalid data, partial failures, timeouts)" could be "Failure modes (network, invalid data, partial, timeout)." Total ~50 lines that could be ~30. **Estimated savings: ~120 words.** |
| 12 | `project-planner.agent.md` | L75–L79 | MEDIUM | "Why incremental?" explanation paragraph | "Writing all phases upfront leads to scope creep and inconsistencies as priorities shift. By writing one phase at a time, refinements to earlier phases naturally influence later ones. When the user returns after completing a phase..." This rationale could be a single sentence. **Estimated savings: ~40 words.** |
| 13 | `project-planner.agent.md` | L41–L55 | MEDIUM | Phase 2 clarification questions are verbose | 9 numbered questions, some with sub-explanations. "Project vision — What does the finished product look like? Who is it for?" and "Current state — What exists today? What works, what doesn't?" — the sub-questions are somewhat redundant with the label. **Estimated savings: ~30 words.** |
| 14 | `feature-implementer.agent.md` | L85–L90 | LOW | Implementation Record writing instructions are over-explained | "Determine the output path: Use the same dev/feature/[task-name]/ directory... If plan documents were provided as attachments, match the [task-name] from their path. If no plan directory exists, create one using a slug of the task description." — 3 sentences to say "write to the task's dev/feature/[task-name]/ directory." **Estimated savings: ~30 words.** |
| 15 | `feature-qa-writer.agent.md` | L24–L51 | LOW | "What Requires Manual QA" uses dual-format explanations | Each of the 8 categories has both regular text AND italicized text in parentheses explaining what automated tests cover. The parenthetical explanations add clarity but almost double the length of each item. Could use a two-column table instead. **Estimated savings: ~60 words.** |
| 16 | `debugger.agent.md` | L12–L24 | LOW | Core Expertise lists technologies as bullets | Frontend (5 items) and Backend (5 items) list specific frameworks. These could be comma-separated on one line each. **Estimated savings: ~20 words.** |
| 17 | `test-orchestrator.agent.md` | L116–L119 | LOW | Pipeline Asymmetry explanation is verbose | "This orchestrator omits the QA Writer and Prod Code Review steps that the Audit and Phase-Execute orchestrators include. Rationale: test remediation tasks are scoped narrowly to test code changes, which are self-validating (tests either pass or fail). A full QA plan and prod readiness gate add overhead without proportional value for test-only changes." Could be one sentence. **Estimated savings: ~25 words.** |

### 3. Unnecessary/Redundant Sections

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 18 | All 5 skill SKILL.md files | Varies | MEDIUM | "When to Use" sections repeat frontmatter description | Every skill file has a "When to Use" section (3–5 bullets) that restates information from the YAML `description` field, which is already surfaced by the VS Code skill loading mechanism. E.g., `implementation-pipeline-loop` description says "Use when: orchestrating the implementation pipeline" and the When to Use section says "Phase - Execute orchestrating feature implementation." **Estimated savings: ~15 words × 5 = ~75 words total.** |
| 19 | `phase-document-writing/SKILL.md` | L77–L92 | MEDIUM | Quality Checklist largely restates template requirements | 15 checklist items, at least 8 of which directly restate section requirements from the template above. E.g., "Every phase has a clear, distinct objective" is guaranteed by the mandatory "## Objective" section; "Scope boundaries are explicit" is guaranteed by the "### In Scope / ### Out of Scope" sections. Only items about cross-phase concerns and code-level leakage add new validation beyond what the template enforces. **Estimated savings: ~60 words.** |
| 20 | `audit-report-format/SKILL.md` | L63–L72 | LOW | "Domain-Specific Extensions" section is metadata about agents | This section says "Auditor - Refactor adds: Dependency Graph Observations, Risk Matrix, Architectural Health Score" and "Auditor - Code and Auditor - Infra use the common format as-is." This is informational metadata about which agents do what, not a format specification. Better placed in agent files themselves (where it already is). **Estimated savings: ~40 words.** |
| 21 | `project-planner.agent.md` | L24–L34 | LOW | Pipeline diagram in Project Planner | The ASCII flow diagram showing Planner → Refiner → Execute flow is already well-documented in the README and described in prose. Serves as orientation but is 10 lines for a 3-step pipeline that the preceding paragraph already explains. **Estimated savings: ~30 words.** |
| 22 | `phase-refiner.agent.md` | L195–L205 | LOW | Escalation section has verbose quoted text | The escalation guidance includes a ~30-word quoted recommendation template. The situations list (5 bullets) is useful, but the quoted text is a soft prescription that could be shorter. **Estimated savings: ~20 words.** |

### 4. Content Extractable to Shared Files

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 23 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | Varies | MEDIUM | Each orchestrator has its own "Constraints" section with overlapping items | All 3 say "DO NOT write source code, test files, or configuration directly." Phase-Execute and Audit also say "DO NOT write plan/review/QA documents directly." These are orchestrator-wide constraints that could be in `orchestrator-conventions.instructions.md` (already auto-loaded). **Estimated savings: ~30 words × 3 = ~90 words.** |
| 24 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md` | phase-execute L81–L96, audit L135–L155 | LOW | Reporting templates could be a shared skill | The GO/NO-GO reporting sections share structure (verdict, features completed, table of tasks, next step). A small shared "pipeline-report-format" skill could eliminate this duplication if the pattern appears in future orchestrators. **Estimated savings: ~80 words (if extracted).** |

### 5. Bloated Formatting

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 25 | `README.md` | L170–L260 | LOW | "What Each Agent Does" section re-describes agents already in tables | The README has agent summary tables (User-Facing and Hidden Subagents) with Purpose columns, then a separate ~100-line "What Each Agent Does" section that provides longer descriptions. Some redundancy with the tables and with each agent's own description frontmatter. However, as a user-facing reference doc, some expansion beyond table cells is expected. **Estimated savings: ~50 words if descriptions are tightened (not removed).** |
| 26 | `README.md` | L293–L310 | LOW | "Integration Notes" partially restate earlier content | "Three orchestrators" and "Shared subagents" bullets restate information from the agent tables. "Subagent autonomy" and "Read-only subagents" restate agent-level constraints. However, this summary section serves as a quick reference and adding it all to the tables would clutter them. **Estimated savings: ~40 words if trimmed.** |

---

## Cross-Cutting Observations

### Pattern 1: Read-Only Constraints Restated Despite Auto-Loading

The `read-only-agent.instructions.md` file applies to 8 agents via `applyTo` globs. Despite this, 4 agents (project-planner, phase-refiner, feature-decomposer, test-analyst) restate "You NEVER touch the codebase" with specific bullets that are already covered by the instruction. This is the single largest cross-file DRY violation.

**Files affected:** `project-planner.agent.md`, `phase-refiner.agent.md`, `feature-decomposer.agent.md`, `test-analyst.agent.md`

### Pattern 2: Orchestrator Branch + Pipeline Logic Repeated

The `orchestrator-conventions.instructions.md` provides branch creation conventions, but each orchestrator re-implements the full procedure rather than using the convention and specifying only the branch prefix. Similarly, each orchestrator restates "DO NOT write source code/tests/config directly" which could be in the shared instruction file.

**Files affected:** `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md`

### Pattern 3: Skill "When to Use" Sections Are Vestigial

All 5 skills have a "When to Use" section that repeats the frontmatter `description`, which already contains "Use when:" phrasing. The VS Code skill-loading mechanism surfaces the description to agents deciding whether to load a skill. The section inside the file body adds ~15 words per skill with no new information.

**Files affected:** All 5 `SKILL.md` files

### Pattern 4: phase-refiner.agent.md is Disproportionately Long

At ~250 lines, `phase-refiner.agent.md` is the longest agent file by a significant margin. Its verbosity comes from: (1) a large ASCII diagram, (2) a lengthy Question Triage section, (3) seven detailed Iteration Focus Areas, and (4) restated read-only constraints. Individually each section has value, but the cumulative length could be reduced by ~30% without losing capabilities.

**File affected:** `phase-refiner.agent.md`

---

## Recommended Priority Order

### 1. Quick Wins (Low effort, high impact)

1. **Remove restated read-only constraints from 4 agents** (Finding #2) — Delete the "You NEVER touch the codebase" subsections from agents where `read-only-agent.instructions.md` auto-loads. ~160 words saved.
2. **Remove "When to Use" sections from all 5 skills** (Finding #18) — The frontmatter description already serves this purpose. ~75 words saved.
3. **Add "no code blocks" constraint to `read-only-agent.instructions.md`** (Finding #3) — Then remove from 3 agents. ~45 words saved.
4. **Remove "Domain-Specific Extensions" from `audit-report-format`** (Finding #20) — Already in agent files. ~40 words saved.

### 2. Important Fixes (Moderate effort, significant savings)

5. **Consolidate branch creation into `orchestrator-conventions.instructions.md`** (Finding #1) — Define the full creation procedure in the shared instruction; orchestrators only specify their prefix pattern. ~150 words saved.
6. **Add orchestrator constraints to `orchestrator-conventions.instructions.md`** (Finding #23) — Move "DO NOT write code/tests/config/plans directly" to the shared instruction. ~90 words saved.
7. **Remove duplicated QA path logic from `phase-execute.agent.md`** (Finding #4) — Reference `dev-task-folder.instructions.md` convention instead of restating the fallback. ~80 words saved.
8. **Tighten `phase-refiner.agent.md` prose** (Findings #9, #10, #11) — Compress ASCII diagram, Question Triage, and Iteration Focus Areas. ~280 words saved.

### 3. Improvement Pass (Higher effort, moderate savings)

9. **Trim `phase-document-writing` quality checklist** (Finding #19) — Keep only items that validate concerns NOT already enforced by the template sections. ~60 words saved.
10. **Tighten GO/NO-GO templates** (Finding #6) — Condense the reporting blocks in both orchestrators or extract to a shared skill. ~100 words saved.
11. **Condense `project-planner.agent.md` explanation prose** (Findings #12, #13) — Tighten "Why incremental?" and clarification questions. ~70 words saved.
12. **Trim README "What Each Agent Does" descriptions** (Finding #25) — Tighten descriptions that closely mirror agent table Purpose columns. ~50 words saved.

---

## Summary Statistics

| Severity | Count | Estimated Total Word Savings |
|----------|-------|------------------------------|
| HIGH | 4 | ~470 words |
| MEDIUM | 10 | ~680 words |
| LOW | 12 | ~400 words |
| **Total** | **26** | **~1,550 words** |

**Estimated total token savings:** ~2,000–2,500 tokens across all files (using ~1.3 tokens/word average for markdown).
