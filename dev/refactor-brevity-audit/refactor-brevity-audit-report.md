# Refactor Brevity Audit Report

**Date:** 2026-03-30
**Scope:** All files in `.github/agents/`, `.github/skills/`, `.github/instructions/` (31 files: 20 agents + 1 README + 5 skills + 5 instructions)
**Focus:** Structural reorganization for brevity — extraction, consolidation, and decomposition opportunities that go beyond line-level prose tightening

**Relationship to Code Audit:** The companion [code-brevity-audit-report.md](../code-brevity-audit/code-brevity-audit-report.md) identified 26 findings focused on DRY violations and verbose prose within individual files. This audit evaluates whether the **file organization itself** — which content lives where, which files exist, and how they reference each other — can be restructured to achieve brevity. Where findings overlap with the code audit, this report references that finding and focuses on the structural dimension.

**Findings by severity:**
- **HIGH**: 3
- **MEDIUM**: 6
- **LOW**: 4
- **Total**: 13

---

## Dependency Graph Observations

### Loading Chains

All dependencies in this system are Markdown-level references: `applyTo` globs (instructions → agents), `agents:` frontmatter (orchestrators → subagents), and textual "Load the `<name>` skill" directives (agents → skills).

#### Instruction → Agent Loading (via `applyTo`)

| Instruction | Applies To | Agent Count |
|-------------|-----------|-------------|
| `codebase-context-bootstrap` | `.github/agents/**` (all) | 20 |
| `dev-task-folder` | `.github/agents/**` (all) | 20 |
| `read-only-agent` | 8 named agents | 8 |
| `orchestrator-conventions` | 3 orchestrators | 3 |
| `documentation-freshness-check` | project-planner, phase-refiner | 2 |

#### Skill → Agent Loading (via textual reference)

| Skill | Loaded By | Agent Count |
|-------|-----------|-------------|
| `auditor-shared-conventions` | auditor-code, auditor-infra, auditor-refactor | 3 |
| `audit-report-format` | *transitively via auditor-shared-conventions* | 3 |
| `implementation-pipeline-loop` | phase-execute, audit-code-or-infra, test-orchestrator | 3 |
| `phase-document-writing` | project-planner, phase-refiner | 2 |
| `feature-plan-set` | feature-decomposer | 1 |

#### Subagent → Orchestrator Loading (via `agents:` frontmatter)

| Subagent | Used By | Orchestrator Count |
|----------|---------|-------------------|
| Feature - Implementer | all 3 orchestrators | 3 |
| Feature - Reviewer | all 3 orchestrators | 3 |
| Git Commit | all 3 orchestrators | 3 |
| Docs Writer | all 3 orchestrators | 3 |
| Feature - QA Writer | phase-execute, audit orchestrator | 2 |
| Prod Code Review | phase-execute, audit orchestrator | 2 |
| Feature - Decomposer | phase-execute only | 1 |
| Auditor - Code/Infra/Refactor | audit orchestrator only | 1 each |
| Test - Analyst/Writer/Fixer | test orchestrator only | 1 each |

### Highest Fan-In (Most Referenced — Fragile Change Points)

1. **`auditor-shared-conventions` SKILL** — Referenced by 3 auditors + transitively loads `audit-report-format`. Changes here affect 3 agent files and require validating the transitive skill.
2. **`read-only-agent.instructions.md`** — Applies to 8 agents. Any change propagates to half the agent fleet.
3. **Feature - Implementer / Feature - Reviewer** — Referenced by all 3 orchestrators via `agents:` frontmatter.

### Highest Fan-Out (Most Dependencies)

1. **`audit-code-or-infra.agent.md`** — References 9 subagents + 1 skill + receives 3 auto-loaded instructions = 13 dependencies.
2. **`phase-execute.agent.md`** — References 7 subagents + 1 skill + receives 3 auto-loaded instructions = 11 dependencies.
3. **`test-orchestrator.agent.md`** — References 7 subagents + 1 skill + receives 3 auto-loaded instructions = 11 dependencies.

### Transitive Dependencies

- `auditor-code/infra/refactor` → load `auditor-shared-conventions` → which tells them to load `audit-report-format`. This two-hop chain means the 3 auditors always load 2 skills.

### Orphaned Files

None. Every file is referenced by at least one other file or serves as a user-facing entry point.

### Overly Broad Loading

- `codebase-context-bootstrap.instructions.md` and `dev-task-folder.instructions.md` both use `applyTo: ".github/agents/**"` (all 20 agents), but are only relevant to the ~12 agents that perform codebase discovery or produce `dev/` output. Agents like `git-commit`, `web-research-specialist`, and `debugger` receive these instructions without using them.

---

## Findings by Category

### 1. Directory & Module Organization

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `.github/skills/auditor-shared-conventions/`, `.github/skills/audit-report-format/` | — | High | Two tightly-coupled auditor skills should be one | `auditor-shared-conventions` and `audit-report-format` are always loaded together by the exact same 3 agents. `auditor-shared-conventions` contains a directive "Load the `audit-report-format` skill and follow its report structure" — meaning every auditor performs a two-hop skill load. The report format is integral to the auditor conventions (not independently reusable). Merging them into a single `auditor-conventions` skill eliminates one directory, removes the transitive loading directive, and removes the duplicate "When to Use" section from `audit-report-format`. **Estimated structural savings: 1 skill directory + ~70 words (transitive reference + "When to Use" + "Domain-Specific Extensions" section already flagged by code audit finding #20).** |

### 2. Import Graph & Dependency Health

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 2 | `orchestrator-conventions.instructions.md`, `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | orchestrator-conventions L20–L29, phase-execute L18–L25, audit L77–L85, test L73–L81 | High | `orchestrator-conventions` instruction is structurally underutilized — agents duplicate what it should own | The instruction file defines branch creation conventions (type-prefixed, kebab-case, retry on existing name, stop on error). Yet each orchestrator restates the **full procedure** (code audit finding #1) AND adds constraints ("DO NOT write source code/tests/config directly") that are universal to all orchestrators (code audit finding #23). **Structural fix:** Move all shared orchestrator behavior into the instruction. Orchestrators should only specify: (a) their pipeline steps, (b) their subagent invocation prompts, and (c) any domain-specific constraints. The instruction should own: branch creation procedure, common constraints, and output verification rules. **Estimated structural savings: ~240 words across 3 agents (branch logic + constraints).** |
| 3 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | code L31–L58, infra L32–L68, refactor L23–L35 | High | Auditor exclusion lists are inverse mirrors — structurally redundant | auditor-code excludes infra/deployment/docs/config files (~25 lines). auditor-infra excludes source code/deps/tests/agents (~25 lines). These are the **exact complements** of each other — auditor-code's exclusions are auditor-infra's inclusions and vice versa. auditor-refactor shares code-auditor's exclusions plus docs. **Structural fix:** Define all file-type categories in `auditor-shared-conventions` (source code, infrastructure, documentation, config, test files, dependency manifests). Each auditor then declares `In-scope categories: [X, Y]` (~3 lines) instead of maintaining a full exclusion list (~20 lines). The skill already has a "Source Code File Types" section — extend it to cover all categories. **Estimated structural savings: ~50 lines across 3 auditors.** |
| 4 | `codebase-context-bootstrap.instructions.md`, `dev-task-folder.instructions.md` | — | Low | Broad `applyTo` globs load instructions into agents that don't use them | Both instructions use `applyTo: ".github/agents/**"` which loads them into all 20 agents. `codebase-context-bootstrap` is irrelevant to `git-commit`, `web-research-specialist`, and `debugger` (no discovery phase). `dev-task-folder` is irrelevant to agents that don't produce `dev/` output (same three, plus `documentation-architect`). Narrowing the glob would save ~100 tokens per non-relevant agent invocation. However, maintaining explicit agent lists in `applyTo` increases maintenance cost. **Tradeoff:** Acceptable as-is; flag for awareness, not action. |

### 3. Component & Module Decomposition

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 5 | `phase-refiner.agent.md` | L70–L120 | Medium | Iteration Focus Areas section is a candidate for skill extraction (with caveats) | The 7 Iteration Focus Areas (~50 lines) are the densest section of the longest agent file (~250 lines). Extracting to a `phase-refinement-checklist` skill would reduce the agent to ~200 lines and make the checklist independently referenceable. **However**, this content is specific to the phase-refiner role and unlikely to be reused by other agents, so extraction adds indirection without shared benefit. **Recommendation:** Consider extraction only if a second consumer emerges (e.g., a future "Feature - Refiner" agent). For now, compress inline per code audit findings #10–#11. |
| 6 | `feature-plan-set/SKILL.md`, `feature-decomposer.agent.md` | skill L96–L102, agent L51–L60 | Medium | Decomposition rules duplicated between skill and agent | The `feature-plan-set` skill has a "Decomposition Rules" section (~8 lines) defining the independence criterion and combination rules. The `feature-decomposer` agent has Phase 2 (Decomposition) that restates the same logic: "Two items are independent if they can be implemented, tested, and shipped without depending on each other" and combination rules. **Structural fix:** The skill should be the single source of truth for decomposition rules. The agent's Phase 2 should reference the skill's rules rather than restating them. **Estimated savings: ~40 words in the agent.** |

### 4. Coupling & Cohesion

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 7 | `read-only-agent.instructions.md`, `project-planner.agent.md`, `phase-refiner.agent.md`, `feature-decomposer.agent.md`, `test-analyst.agent.md` | instruction L6–L17, planner L20, refiner L29–L36, decomposer L20–L22, analyst L15–L17 | Medium | `read-only-agent` instruction is structurally under-enriched — agents compensate by restating constraints | The instruction defines 4 constraints (no create/modify/delete source, test, config files; approval before writing). But 4 agents add their own versions: "You NEVER touch the codebase," "no code blocks," "no code-level planning" (code audit findings #2, #3). **Structural fix:** Enrich the instruction once with the commonly restated constraints. Add: "You do NOT write code blocks — link to files and reference symbols instead" and "You do NOT produce code-level details (function signatures, schemas, API contracts)." Then agents only specify domain-specific restrictions beyond the instruction. **Estimated structural savings: ~160 words across 4 agents + prevents future agents from needing to restate.** |

### 5. Separation of Concerns

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 8 | `phase-execute.agent.md` L81–L96, `audit-code-or-infra.agent.md` L135–L155 | — | Medium | GO/NO-GO reporting templates are orchestrator-shared content living in individual agents | Both phase-execute and audit orchestrators have ~15-line reporting templates for GO and NO-GO verdicts. These follow the same structure (verdict, task count, status table, next step) with minor field label differences. The test orchestrator has a simpler version (Phase 8). This concern (pipeline completion reporting) is not in the `orchestrator-conventions` instruction or `implementation-pipeline-loop` skill. **Structural fix:** Add a "Pipeline Completion Report" section to `orchestrator-conventions.instructions.md` with a parameterized template. Orchestrators specify only their field labels. **Estimated savings: ~100 words across 2–3 agents.** Alternatively, add to `implementation-pipeline-loop` skill since reporting logically follows the loop. |
| 9 | `README.md` L240–L270, `dev-task-folder.instructions.md` | — | Medium | README "Task Documentation Pattern" section duplicates `dev-task-folder.instructions.md` | The README has a ~30-line "Task Documentation Pattern" section showing the file tree and naming conventions. This is the same content as `dev-task-folder.instructions.md` (which auto-loads into all agents). Users see the README; agents see the instruction. While duplication across audience boundaries is more acceptable, the README section could reference the instruction file rather than restating it, or the instruction file could be cited as the canonical source. **Risk:** If the naming convention changes, both must be updated — currently no cross-reference connects them. |

### 6. API Surface & Encapsulation

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 10 | All 5 `SKILL.md` files | Varies | Medium | "When to Use" sections are vestigial API surface that duplicates frontmatter | Every skill has a "When to Use" section (3–5 bullets) that restates the YAML `description` field. The VS Code skill-loading mechanism surfaces the description to agents deciding whether to load a skill. The body section adds no new information — it's a public-facing interface component that served a purpose during initial development but is now redundant with the frontmatter. **Structural fix:** Remove all 5 "When to Use" sections. If any skill's description is insufficient, enrich the frontmatter description instead. (Aligns with code audit finding #18.) **Estimated savings: ~75 words total.** |
| 11 | `README.md` L282–L290 | — | Low | README Skills table lists 3 of 5 skills — incomplete public interface | The README's "Skills and Instructions" section has a Skills table listing only `phase-document-writing`, `audit-report-format`, and `feature-plan-set`. Missing: `auditor-shared-conventions` and `implementation-pipeline-loop`. The Instructions table similarly lists only `dev-task-folder`. This incomplete surface makes it harder for users to understand the full skill/instruction inventory. **Fix:** Complete both tables or reference a canonical source. |

### 7. Migration & Restructuring Opportunities

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 12 | `auditor-shared-conventions/SKILL.md` + `audit-report-format/SKILL.md` → merged `auditor-conventions/SKILL.md` | — | High | Merge two auditor skills into one | (Migration plan for finding #1.) Create `.github/skills/auditor-conventions/SKILL.md` containing the merged content of both skills. Update 3 auditor agents to reference `auditor-conventions` instead of `auditor-shared-conventions`. Delete both old skill directories. **Dependencies:** 3 auditor agents + the auditor mode instructions in the system prompt. **Risk:** Low — the 3 consumers are all in the same directory and follow the same loading pattern. |
| 13 | `orchestrator-conventions.instructions.md` | — | High | Enrich orchestrator-conventions to absorb shared orchestrator content | (Migration plan for finding #2.) Add to the instruction: (a) common constraints ("DO NOT write source code, test files, configuration, plan documents, review records, or QA plans directly"), (b) the full branch creation procedure (parameterized by prefix), (c) a reporting template (parameterized by field labels). Then remove the duplicated sections from all 3 orchestrators. **Dependencies:** 3 orchestrator agents. **Risk:** Low — the instruction already auto-loads into these agents. The orchestrators become shorter and more focused on their domain-specific pipeline steps. |

---

## Cross-Cutting Observations

### Pattern 1: Shared Content Under-Extracted to Instruction/Skill Files

The system has the right architecture — shared instructions and skills exist. But the extraction is incomplete. In several cases, a shared file exists but agents still restate the content it provides:

- `orchestrator-conventions.instructions.md` owns branch creation and pipeline discipline, but orchestrators restate branch creation and add constraints the instruction should own.
- `read-only-agent.instructions.md` owns "no modification" constraints, but agents restate "no code blocks" and "no code-level planning."
- `auditor-shared-conventions` owns file-type scoping, but each auditor maintains its own full exclusion list.

**Root cause:** The shared files were likely created to avoid starting from nothing, but the agent files weren't fully trimmed after the shared files were established. The fix is to complete the extraction and trim the agents.

### Pattern 2: Two-Skill Loading Chain for Auditors

The `auditor-shared-conventions` → `audit-report-format` transitive dependency is the only multi-hop skill chain in the system. Every other skill is loaded directly by agents. This adds cognitive overhead (understanding which skill provides what) and token cost (two loading operations instead of one). Merging resolves both.

### Pattern 3: Inverse Exclusion Lists Are a Sign of Missing Abstraction

When two components maintain complementary lists (auditor-code excludes what auditor-infra includes, and vice versa), it signals a missing shared taxonomy. The `auditor-shared-conventions` skill should define the taxonomy once, and each auditor should select from it.

### Pattern 4: README as Parallel Documentation Creates Drift Risk

The README documents agent tables, pipeline descriptions, task documentation patterns, and skill/instruction tables — much of which also exists in the agent files, `dev-task-folder.instructions.md`, and skill frontmatter. Without linkage, these parallel descriptions drift. The README's Skills table is already out of date (showing 3 of 5 skills).

---

## Recommended Restructuring Priority

### 1. Quick Wins (Low risk, high benefit)

1. **Merge `auditor-shared-conventions` + `audit-report-format` into `auditor-conventions`** (Finding #1/12) — 3 files to update, clear merge path, eliminates transitive loading. Saves ~70 words + 1 skill directory.
2. **Remove "When to Use" sections from all 5 skills** (Finding #10) — 5 simple deletions. Saves ~75 words. (Shared with code audit finding #18.)
3. **Complete README Skills and Instructions tables** (Finding #11) — Add the 2 missing skills and 4 missing instructions to the tables.
4. **Remove decomposition rules duplication from feature-decomposer** (Finding #6) — Replace with a reference to the skill's rules. Saves ~40 words.

### 2. Important Restructurings (Moderate effort, significant savings)

5. **Enrich `orchestrator-conventions.instructions.md` with shared constraints and reporting** (Finding #2/8/13) — Add common constraints, parameterize branch creation, add reporting template. Then trim all 3 orchestrators. Saves ~340 words across 3 agents.
6. **Restructure auditor file-type scoping into category-based selection** (Finding #3) — Define file-type taxonomy in `auditor-conventions` (merged skill). Each auditor declares included categories instead of listing exclusions. Saves ~50 lines across 3 auditors.
7. **Enrich `read-only-agent.instructions.md` with commonly restated constraints** (Finding #7) — Add "no code blocks" and "no code-level details" to the instruction. Trim 4 agents. Saves ~160 words. (Builds on code audit findings #2, #3.)

### 3. Deferred / Conditional

8. **Extract phase-refiner Iteration Focus Areas to a skill** (Finding #5) — Only worthwhile if a second consumer emerges. For now, compress inline per code audit findings.
9. **Narrow `applyTo` globs** (Finding #4) — Saves ~100 tokens per irrelevant agent. But increases maintenance of the `applyTo` lists. Current tradeoff is acceptable.
10. **Cross-reference README to dev-task-folder instruction** (Finding #9) — Add a note in the README pointing to the instruction as the canonical source.

---

## Risk Matrix

| Move | Files Affected | References to Update | Risk |
|------|---------------|---------------------|------|
| Merge auditor-shared-conventions + audit-report-format → auditor-conventions | 2 skills → 1 | 3 auditor agents + CODEBASE_CONTEXT.md + ARCHITECTURE.md | Low |
| Enrich orchestrator-conventions.instructions.md | 1 instruction | 3 orchestrator agents (trim duplicated content) | Low |
| Restructure auditor file-type scoping | 1 skill (merged) | 3 auditor agents (replace exclusion lists with category selections) | Low-Medium |
| Enrich read-only-agent.instructions.md | 1 instruction | 4–5 agents (trim restated constraints) | Low |
| Remove "When to Use" from 5 skills | 5 skills | None | Low |
| Complete README tables | 1 README | None | Low |
| Remove decomposition rules from feature-decomposer | 1 agent | None (skill already has the rules) | Low |

---

## Estimated Total Impact

| Action Tier | Findings | Word Savings | Files Touched |
|-------------|----------|-------------|---------------|
| Quick wins (#1–4) | 4 | ~185 words | 9 files |
| Important restructurings (#5–7) | 3 | ~550 words | 10 files |
| Deferred (#8–10) | 3 | ~100 words (conditional) | 3–8 files |
| **Total** | **10 actionable** | **~735 words** | **~19 files** |

**Combined with code audit:** The code audit estimated ~1,550 words of reducible content. This refactor audit identifies ~735 additional words addressable through structural changes. Some findings overlap (e.g., both audits flag the read-only constraint restatement — the code audit counts the words, this audit proposes the structural fix). Net additional savings from structural restructuring beyond what the code audit already covers: **~400–500 words**.

**Token impact:** ~500–650 tokens saved from structural changes alone, plus cleaner loading chains and reduced maintenance surface area.
