# DRY Audit Report: Agent Definitions, Skills, and Instructions

**Date:** 2026-03-30
**Scope:** All 20 agent files in `.github/agents/`, 4 skill files in `.github/skills/`, 4 instruction files in `.github/instructions/`
**Focus:** Duplicated patterns, repeated text, and shared conventions that could be extracted into new Skills or Instructions

## 1. Executive Summary

- **Files audited:** 28 (20 agents, 4 skills, 4 instructions)
- **Findings:** 13 (4 High, 7 Medium, 2 Low)
- **Proposed new Skills:** 1 (`auditor-shared-conventions`)
- **Proposed new Instructions:** 3 (`documentation-freshness-check`, `no-code-blocks-planning`, `test-only-modification`)
- **Existing extractions needing wiring:** 1 (`implementation-pipeline-loop` — skill exists but no orchestrator references it)
- **Existing Skills to extend:** 1 (`implementation-pipeline-loop` — add Docs Writer step, report template, QA/Prod invocation templates)

### Estimated line savings

| Extraction | Lines duplicated | Lines after extraction | Net savings |
|-----------|-----------------|----------------------|-------------|
| Auditor shared conventions (new skill) | ~120 (40 × 3) | ~30 (3 refs) | ~90 |
| Orchestrators reference pipeline-loop skill | ~180 (60 × 3) | ~15 (3 refs) | ~165 |
| Documentation freshness check (new instruction) | ~60 (15 × 4) | ~15 (instruction file) | ~45 |
| Docs Writer step → pipeline-loop skill | ~30 (10 × 3) | ~10 (in skill) | ~20 |
| No-code-blocks planning (new instruction) | ~9 (3 × 3) | ~6 (instruction file) | ~3 |
| Test-only modification (new instruction) | ~12 (6 × 2) | ~8 (instruction file) | ~4 |
| **Total** | **~411** | **~84** | **~327** |

---

## 2. Findings by Category

### Category A: Auditor Shared Patterns (3 agents)

Agents affected: `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md`

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | Constraints sections | High | **Identical constraints block across all 3 auditors** | All 3 auditors share 5 near-identical constraint bullets: "Complete the FULL audit before producing any deliverables", "DO NOT suggest fixes inline", "DO NOT skip any audit category", "DO NOT give vague feedback", "DO NOT edit source code". Only minor wording variations (e.g., "every file" vs "across the codebase"). Should be extracted into a shared skill. |
| 2 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | Deliverables sections | High | **Identical deliverables section across all 3 auditors** | All 3 share the exact same text: "Your output is a report document saved to `dev/[audit-name]/`: `[audit-name]-report.md`, `[audit-name]-summary.md`. Present your findings in chat first, then write the deliverables." This is ~5 lines duplicated 3 times. |
| 3 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | Audit Scope sections | High | **Identical scope determination block** | All 3 auditors have an "Audit Scope" section with the same 3 options (Full codebase / Specific files / Single file) and "Default to full codebase if unspecified." Minor wording variation ("Single file" vs "Single module/subsystem"). |
| 4 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | Process sections | Medium | **Identical process summary line** | All 3 have: "Discover all in-scope files → Read each thoroughly → Evaluate against all N categories → Cross-reference → Classify severity → Report." Only the category count differs. |
| 5 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | Output Format sections | Medium | **Identical output format reference** | All 3 have: "Load the `audit-report-format` skill and follow its report structure (Executive Summary, Findings by Category table, Cross-Cutting Observations, Recommended Priority Order). Use the severity meanings defined above." |
| 6 | `auditor-code.agent.md`, `auditor-refactor.agent.md` | In-Scope File Types sections | Medium | **Identical in-scope file types list** | Both code and refactor auditors list the exact same 5-language file type mapping (Python `.py`, Node.js `.js/.mjs/.cjs`, TypeScript `.ts/.tsx/.jsx`, Java `.java`, Kotlin `.kt/.kts`). Code auditor adds dependency manifests. |
| 7 | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` | Exclusions sections | Medium | **Overlapping generated/cached exclusion list** | All 3 list `__pycache__/`, `.venv/`, `node_modules/`, `target/`, `build/`, `dist/` as generated/cached exclusions. The remaining exclusions are complementary (each auditor excludes what the others audit). |
| 8 | `auditor-code.agent.md`, `auditor-refactor.agent.md` | Test File Audit Policy sections | Low | **Shared test file glob pattern list** | Both list `tests/`, `test_*.py`, `*.test.js`, `*.test.ts`, `*.spec.js`, `*.spec.ts` as test file patterns, though the audited categories differ per auditor. |

**Proposed extraction:** New **Skill** `auditor-shared-conventions` containing:
- Standard constraints block (with placeholder for domain-specific additions)
- Standard deliverables section
- Standard scope determination section
- In-scope file type detection (language list)
- Generated/cached exclusion list
- Test file glob patterns
- Process summary template
- Output format reference

Each auditor would then load this skill and add only their domain-specific content (categories, exclusions complement, severity meanings, domain-specific extensions).

---

### Category B: Orchestrator Shared Patterns (3 agents)

Agents affected: `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md`

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 9 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | Steps 2A-2D / 7A-7D | High | **Implementation Pipeline Loop inlined despite skill existing** | The `implementation-pipeline-loop` skill defines the canonical Implement → Review → Commit → Mark Complete cycle. However, **none of the 3 orchestrators reference this skill**. All 3 inline the full loop (~60 lines each) with only path convention differences. This is the single largest DRY violation: ~180 lines of near-identical text that already has an extracted skill nobody uses. |
| 10 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | Docs Writer steps | High | **Docs Writer invocation step duplicated across all 3 orchestrators** | All 3 orchestrators end with a near-identical Docs Writer invocation: `[SUBAGENT-MODE]` prompt + "This step is best-effort" caveat + conditional execution note. The 3 versions differ only in what completed (phase/audit/test) but the structure, caveat, and conditional note are identical (~10 lines × 3). |
| 11 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md` | QA Writer invocation | Medium | **QA Writer invocation prompt duplicated** | phase-execute Step 3 and audit-code-or-infra Phase 8 have near-identical QA Writer invocation prompts. They differ only in "features in this phase" vs "tasks in this audit remediation" and in path patterns. The test-orchestrator intentionally omits this step. |
| 12 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md` | Prod Code Review invocation | Medium | **Prod Code Review invocation prompt duplicated** | phase-execute Step 4 and audit-code-or-infra Phase 9 have near-identical Prod Code Review invocation prompts. The test-orchestrator intentionally omits this step. |
| 13 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` | Report sections | Medium | **Report-to-user template duplicated** | All 3 orchestrators have a similar "Report to User" section with the same table format (Task/Feature | Impl | Review), GO/NO-GO handling, and "Next step: Push the branch and open a PR" guidance. Differs only in labeling (Phase/Audit/Test). |
| 14 | `phase-execute.agent.md`, `audit-code-or-infra.agent.md` | Error Handling sections | Medium | **Identical error handling section** | Both have identical "Error Handling → Test Failures" sections: "If the Implementer reports test failures: 1. The Reviewer subagent will catch this and request fixes. 2. If tests still fail after the review cycle, the Final Review will flag it as a blocker." Word-for-word identical. |

**Proposed extraction:** Extend the existing **`implementation-pipeline-loop`** Skill to include:
- Post-loop steps: Docs Writer invocation template + best-effort caveat
- Consolidated QA invocation template (for orchestrators that use it)
- Prod Code Review invocation template (for orchestrators that use it)
- Report-to-user template
- Error handling: test failure escalation pattern

Then update all 3 orchestrators to load the skill instead of inlining the loop. Each orchestrator would supply its own path convention and any pipeline-specific variations (test-orchestrator omits QA and Prod Code Review).

---

### Category C: Planning Agent Shared Patterns (3 agents)

Agents affected: `project-planner.agent.md`, `phase-refiner.agent.md`, `feature-decomposer.agent.md`

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 15 | `project-planner.agent.md`, `phase-refiner.agent.md` | Discovery / Phase 2A / Phase 2B | High | **Documentation Freshness Check duplicated 4 times** | The ~15-line block that checks for `README.md` and `docs/CODEBASE_CONTEXT.md` and recommends `@Docs Writer` appears: 1× in project-planner (Phase 1), 3× in phase-refiner (Phase 2A and twice in Phase 2B). All 4 instances are nearly identical — only "project planning" vs "phase refinement" differs. This is the most egregious single-file duplication in the repo (3 copies in one file). |
| 16 | `project-planner.agent.md`, `phase-refiner.agent.md`, `feature-decomposer.agent.md` | Various | Medium | **"No code blocks — link to files and reference symbols" convention** | Three planning agents share this rule: "You do NOT write code blocks — link to files and reference `symbols` instead." project-planner states it in "What You Do and Don't Do", feature-decomposer states it identically, and phase-refiner states "You do NOT write code blocks" in its constraints. This is a cross-cutting planning convention that isn't captured in any existing instruction. |

**Proposed extractions:**

1. New **Instruction** `documentation-freshness-check.instructions.md`:
   - Content: The check for `README.md` and `docs/CODEBASE_CONTEXT.md`, the recommendation to run `@Docs Writer`, and the wait-for-acknowledgment protocol
   - `applyTo: "**/project-planner.agent.md,**/phase-refiner.agent.md"`
   - All 4 inline instances can be replaced with a single reference note (or auto-loaded)

2. New **Instruction** `no-code-blocks-planning.instructions.md`:
   - Content: "Do not write code blocks in your output. Instead, link to files and reference `symbols` inline. This keeps planning documents focused on architecture and behavior, not implementation details."
   - `applyTo: "**/project-planner.agent.md,**/phase-refiner.agent.md,**/feature-decomposer.agent.md"`

---

### Category D: Test Agent Shared Patterns (3 agents)

Agents affected: `test-fixer.agent.md`, `test-writer.agent.md`, `test-analyst.agent.md`

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 17 | `test-fixer.agent.md`, `test-writer.agent.md` | "What You Do and Don't Do" / Constraints | Medium | **"Never modify source code" constraint duplicated** | Both test-fixer and test-writer have a "You NEVER modify source code" section with overlapping bullets: "You do NOT change application logic, APIs, or business rules" (identical), plus variations on "do not refactor production code." The Constraints sections also duplicate: "DO NOT modify source code — only [fix/create] test files and test configuration." |

**Proposed extraction:** New **Instruction** `test-only-modification.instructions.md`:
- Content: "You only create or modify test files and test configuration. You do NOT modify application source code, APIs, business logic, or production behavior. If a test failure reveals an actual bug in source code, document it — do not fix it."
- `applyTo: "**/test-fixer.agent.md,**/test-writer.agent.md"`
- Note: test-analyst is already covered by `read-only-agent.instructions.md` (doesn't modify anything). This instruction applies specifically to agents that DO write test code but must not touch source code.

---

### Category E: Structural Patterns (cross-cutting)

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 18 | `feature-decomposer.agent.md`, `project-planner.agent.md`, `phase-refiner.agent.md`, `test-analyst.agent.md`, `test-fixer.agent.md`, `test-writer.agent.md` | Top sections | Low | **"What You Do and Don't Do" section pattern used by 6 agents** | Six agents use the exact same H2 heading "What You Do and Don't Do" → "You ONLY [scope]" → "You NEVER [prohibition]" structure. This is a useful convention for agent clarity but the CONTENT varies per agent, so it's better treated as a recommended convention (documented in a style guide) rather than an extractable instruction. Not actionable for extraction, but worth noting as a deliberate convention to keep consistent. |

---

## 3. Cross-Cutting Observations

### 3.1 Existing Skill-Orchestrator Disconnect

The `implementation-pipeline-loop` skill was clearly extracted to serve as the single source of truth for the Implement → Review → Commit → Mark Complete cycle. However, none of the 3 orchestrators that should consume it actually reference it. This suggests the skill was created AFTER the orchestrators were written and the orchestrators were never updated to delegate to it. This is the highest-impact DRY win: wiring 3 existing files to 1 existing skill.

### 3.2 Auditor Triad Has Highest Duplication Density

The 3 auditor agents (code, infra, refactor) share the most duplicated text relative to their total content. Approximately 30-40% of each auditor's content is identical across all three. The `audit-report-format` skill already extracts the OUTPUT format, but the INPUT conventions (constraints, scope, exclusions, process) remain inlined.

### 3.3 Phase-Refiner Internal Duplication

`phase-refiner.agent.md` contains the Documentation Freshness Check block 3 times within the same file (once in Phase 2A, twice in Phase 2B — under steps 1 and 2). Even before extracting to an instruction, this should be consolidated to a single occurrence within the file.

### 3.4 Pattern: Complementary Exclusion Lists

The 3 auditors have complementary exclusion lists (code excludes infra files, infra excludes code files, refactor excludes both). Extracting the COMMON exclusions (generated/cached) into the shared skill while keeping domain-specific exclusions inline would reduce duplication while preserving clarity.

### 3.5 Orchestrator Post-Loop Steps are a Natural Skill Extension

The existing `implementation-pipeline-loop` skill covers Steps A-D (Implement → Review → Commit → Mark Complete). The natural extension is to also cover the post-loop steps that all orchestrators share: Docs Writer invocation, report-to-user template, and error handling. The QA Writer and Prod Code Review invocations used by 2 of 3 orchestrators could be documented as optional post-loop steps in the same skill.

---

## 4. Recommended Priority Order

### Quick wins (High impact, low effort)

1. **Wire orchestrators to `implementation-pipeline-loop` skill** — The skill already exists. Update `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, and `test-orchestrator.agent.md` to say "Load the `implementation-pipeline-loop` skill for the Implement → Review → Commit → Mark Complete cycle" and remove the inlined loop. **~165 lines saved, 0 new files created.**

2. **Consolidate Documentation Freshness Check within `phase-refiner.agent.md`** — Before extracting to an instruction, fix the internal duplication: the block appears 3 times in this one file. Reduce to a single occurrence at the top of the workflow section. **~30 lines saved, 0 new files created.**

### Important extractions (High impact, moderate effort)

3. **Create `documentation-freshness-check.instructions.md`** — Extract the shared Documentation Freshness Check block. Apply to project-planner and phase-refiner. Remove all inline instances. **~45 lines saved, 1 new file created.**

4. **Create `auditor-shared-conventions` skill** — Extract shared constraints, deliverables, scope, exclusions, process, and output format sections from all 3 auditors. Each auditor loads the skill and adds domain-specific content. **~90 lines saved, 1 new file created.**

5. **Extend `implementation-pipeline-loop` skill with post-loop steps** — Add: Docs Writer invocation template, report-to-user template, error handling, and optional QA/Prod Code Review invocations. Update all 3 orchestrators to reference these new sections. **~60 additional lines saved.**

### Lower-priority extractions (Medium impact, low effort)

6. **Create `no-code-blocks-planning.instructions.md`** — Extract the planning convention. Apply to project-planner, phase-refiner, feature-decomposer. **~3 lines saved per agent, but improves convention consistency.**

7. **Create `test-only-modification.instructions.md`** — Extract the source-code prohibition for test agents. Apply to test-fixer and test-writer. **~4 lines saved per agent, but prevents accidental drift.**

---

## 5. Proposed Extractions Reference

### New Skill: `auditor-shared-conventions`

| Property | Value |
|----------|-------|
| **Path** | `.github/skills/auditor-shared-conventions/SKILL.md` |
| **Type** | Skill (loaded on demand by auditors) |
| **Consumers** | `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md` |
| **Content** | Shared constraints, deliverables format, scope determination, in-scope file types, generated/cached exclusions, test file patterns, process summary, output format reference |
| **Relationship to `audit-report-format`** | Complementary. `audit-report-format` defines OUTPUT structure. `auditor-shared-conventions` defines INPUT conventions (constraints, scope, process). |

### New Instruction: `documentation-freshness-check.instructions.md`

| Property | Value |
|----------|-------|
| **Path** | `.github/instructions/documentation-freshness-check.instructions.md` |
| **Type** | Instruction (auto-loaded via applyTo) |
| **applyTo** | `**/project-planner.agent.md,**/phase-refiner.agent.md` |
| **Content** | Check for `README.md` and `docs/CODEBASE_CONTEXT.md`, recommend `@Docs Writer` if missing, wait for user acknowledgment |

### New Instruction: `no-code-blocks-planning.instructions.md`

| Property | Value |
|----------|-------|
| **Path** | `.github/instructions/no-code-blocks-planning.instructions.md` |
| **Type** | Instruction (auto-loaded via applyTo) |
| **applyTo** | `**/project-planner.agent.md,**/phase-refiner.agent.md,**/feature-decomposer.agent.md` |
| **Content** | Do not write code blocks. Link to files and reference `symbols` instead. Keep planning documents at the behavior/architecture level. |

### New Instruction: `test-only-modification.instructions.md`

| Property | Value |
|----------|-------|
| **Path** | `.github/instructions/test-only-modification.instructions.md` |
| **Type** | Instruction (auto-loaded via applyTo) |
| **applyTo** | `**/test-fixer.agent.md,**/test-writer.agent.md` |
| **Content** | Only modify test files and test configuration. Never modify application source code. Document source bugs rather than fixing them. |

### Existing Skill Extension: `implementation-pipeline-loop`

| Property | Value |
|----------|-------|
| **Path** | `.github/skills/implementation-pipeline-loop/SKILL.md` (existing) |
| **Change** | Add sections: Docs Writer invocation template, report-to-user template, error handling (test failures), optional QA Writer invocation, optional Prod Code Review invocation |
| **Consumers** | `phase-execute.agent.md`, `audit-code-or-infra.agent.md`, `test-orchestrator.agent.md` |

---

## 6. Detailed Duplication Evidence

### Finding #9 (Highest impact): Implementation Pipeline Loop Inlined

The following text blocks are near-identical across all 3 orchestrators. Only the path convention differs.

**phase-execute.agent.md** Step 2A:
```
Invoke the **Feature - Implementer** subagent:
> "Implement the plan at `dev/feature/[task-name]/`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `dev/feature/[task-name]/[task-name]-implementation.md`. Return a summary of what was implemented and test results."

After the subagent returns:
- Verify `dev/feature/[task-name]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers
```

**audit-code-or-infra.agent.md** Step 7A:
```
Invoke the **Feature - Implementer** subagent:
> "Implement the plan at `dev/[audit-name]/[task-name]/`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `dev/[audit-name]/[task-name]/[task-name]-implementation.md`. Return a summary of what was implemented and test results."

After the subagent returns:
- Verify `dev/[audit-name]/[task-name]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers
```

**test-orchestrator.agent.md** Step 7A:
```
Invoke the **Feature - Implementer** subagent:
> "Implement the plan at `dev/feature/[task-name]/[fix-name]/`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `dev/feature/[task-name]/[fix-name]/[fix-name]-implementation.md`. Return a summary of what was implemented and test results."

After the subagent returns:
- Verify `dev/feature/[task-name]/[fix-name]/[fix-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers
```

This pattern repeats identically for Steps B (Review), C (Commit), and D (Mark Complete).

### Finding #15: Documentation Freshness Check (4 instances)

The following block appears 4 times — once in `project-planner.agent.md` and 3 times in `phase-refiner.agent.md`:

```markdown
#### Documentation Freshness Check

After reading the codebase, check whether these critical documentation files exist:
- `README.md` (repo root)
- `docs/CODEBASE_CONTEXT.md`

If either file is missing, present a recommendation before continuing:

> **Documentation gap detected.** The following critical doc(s) are missing: [list missing files]. Well-maintained documentation helps agents orient quickly and humans onboard faster.
>
> **Recommendation:** Run `@Docs Writer` to generate the missing documentation before continuing with [phase refinement/project planning]. This ensures the [refinement/planning] process starts from an accurate, well-documented baseline.
>
> You can proceed without this step — just let me know.

Wait for the user to acknowledge before continuing...
```

The ONLY difference between instances is "project planning" vs "phase refinement" in the recommendation text.

### Finding #1-3: Auditor Shared Constraints (3 instances)

**auditor-code.agent.md:**
```markdown
## Constraints

- Complete the FULL audit before producing any deliverables
- DO NOT suggest fixes inline — only report findings with file:line references
- DO NOT skip any audit category — be comprehensive on every file
- DO NOT give vague feedback — every finding must cite a specific location
- DO NOT edit source code — you only create report documents
- Focus ONLY on application source code, dependency manifests, and test files — do NOT audit or report on infrastructure, deployment, documentation, or configuration files
```

**auditor-refactor.agent.md:**
```markdown
## Constraints

- Complete the FULL audit before producing any deliverables
- DO NOT suggest fixes inline — only report findings with file:line references
- DO NOT skip any audit category — be comprehensive across the codebase
- DO NOT give vague feedback — every finding must cite specific files and locations
- DO NOT edit source code — you only create report documents
- DO NOT report on file-level code quality (type hints, docstrings, security, readability, DRY) — that is the Code Auditor's domain
- Focus ONLY on application source code and test files — do NOT audit infrastructure, deployment, documentation, or configuration files
```

**auditor-infra.agent.md:**
```markdown
## Constraints

- Complete the FULL audit before producing any deliverables
- DO NOT suggest fixes inline — only report findings with file:line references
- DO NOT skip any audit category — be comprehensive on every file
- DO NOT give vague feedback — every finding must cite a specific location
- DO NOT edit source files — you only create report documents
- Focus ONLY on infrastructure, deployment, documentation, and configuration files — do NOT audit or report on application source code, dependency manifests, or test files
```

The first 5 bullets are identical (with trivial wording variations). Only the scope-focus bullet (#6) differs per auditor.
