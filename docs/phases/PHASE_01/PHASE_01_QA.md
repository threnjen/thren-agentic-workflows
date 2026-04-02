# QA Plan: Phase 01 — Split Feature Decomposer from Phase Execute

**Date:** 2026-04-02
**Last Updated:** 2026-04-02
**Mode:** Release QA Plan
**Scope:** All 3 features in Phase 01 — promoting the Decomposer to user-facing, creating the Plan Expander subagent, and renumbering the executor to `04`. All changes are Markdown-only (no runnable code).
**Environment:** Local workspace — open the repository in VS Code with the GitHub Copilot Chat extension
**Prerequisites:**
- Check out the `phase/split-feature-decomposer` branch (or whichever branch contains the Phase 01 changes)
- Ensure VS Code is running with the GitHub Copilot Chat extension installed (to verify agent picker visibility)

## Features Covered

| Feature | Plan | Implementation Record | Review Record |
|---------|------|-----------------------|---------------|
| decomposer-promote | `dev/feature/decomposer-promote/decomposer-promote-plan.md` | `dev/feature/decomposer-promote/decomposer-promote-implementation.md` | `dev/feature/decomposer-promote/decomposer-promote-review.md` |
| plan-expander-create | `dev/feature/plan-expander-create/plan-expander-create-plan.md` | `dev/feature/plan-expander-create/plan-expander-create-implementation.md` | `dev/feature/plan-expander-create/plan-expander-create-review.md` |
| executor-renumber | `dev/feature/executor-renumber/executor-renumber-plan.md` | `dev/feature/executor-renumber/executor-renumber-implementation.md` | `dev/feature/executor-renumber/executor-renumber-review.md` |

## Coverage Map

- Coverage Map: `docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md`

---

## Summary of Changes

Phase 01 restructured the agent pipeline to split decomposition from execution:

1. **decomposer-promote** — Promoted `Feature - Decomposer` from a hidden subagent to user-facing `03 Feature - Decomposer`. Scoped its output to `-plan.md` only (removed `-context.md` and `-tasks.md` generation). Updated standalone handoff to reference `@04 Phase - Execute`.

2. **plan-expander-create** — Created a new hidden subagent `Feature - Plan Expander` that reads `-plan.md` files and generates companion `-context.md` and `-tasks.md`. Updated the `feature-plan-set` skill and `dev-task-folder` instruction to reflect split ownership.

3. **executor-renumber** — Renamed `03 Phase - Execute` to `04 Phase - Execute` (frontmatter only; filename unchanged). Updated the pipeline to check for existing plans before invoking the Decomposer, added a Plan Expander step, and updated all upstream agent references (`project-planner`, `phase-refiner`, `README.md`).

## Automated Test Coverage

**None.** This repository contains only Markdown files — no runnable code and no automated test suite. All 23 acceptance criteria across the 3 features were verified through manual document inspection during the per-feature review phase.

---

## Manual QA Checklist

### 1. Agent Name and Number Consistency

**Features:** decomposer-promote, plan-expander-create, executor-renumber
**Covers ACs:** decomposer-promote/AC1, plan-expander-create/AC2, executor-renumber/AC1, executor-renumber/AC2
**Why manual:** Names must match exactly across frontmatter `name:` fields, `agents:` lists, prose `@agent` references, and instruction `applyTo` globs — individual feature reviews only checked their own scope.

#### Happy Path

- [ ] **Verify Decomposer name consistency** — Open `.github/agents/feature-decomposer.agent.md` and confirm `name: 03 Feature - Decomposer`. Then open `.github/agents/phase-execute.agent.md` and confirm the `agents:` list contains `03 Feature - Decomposer` (exact match). **Expected:** Both files use the identical string `03 Feature - Decomposer`.

- [ ] **Verify Plan Expander name consistency** — Open `.github/agents/feature-plan-expander.agent.md` and confirm `name: Feature - Plan Expander`. Then open `.github/agents/phase-execute.agent.md` and confirm the `agents:` list contains `Feature - Plan Expander` (exact match). **Expected:** Both files use the identical string `Feature - Plan Expander`.

- [ ] **Verify Executor name in upstream agents** — Grep all files in `.github/agents/` for `03 Phase - Execute`. **Expected:** Zero matches. All references should now say `04 Phase - Execute`.

- [ ] **Verify no `user-invocable: false` on Decomposer** — Open `.github/agents/feature-decomposer.agent.md` and confirm there is no `user-invocable` line in the YAML frontmatter. **Expected:** The field is absent (agent is user-invocable by default).

- [ ] **Verify Plan Expander is hidden** — Open `.github/agents/feature-plan-expander.agent.md` and confirm `user-invocable: false` is present in the YAML frontmatter. **Expected:** `user-invocable: false` exists.

- [ ] **Verify Decomposer appears in VS Code agent picker** — Open VS Code with the Copilot Chat extension, click the agent picker dropdown. **Expected:** `03 Feature - Decomposer` is listed as a selectable agent.

#### Edge Cases

- [ ] **Verify no stale `@03 Phase` references across all `.md` files** — Run `grep -r "03 Phase" .github/` from the repo root. **Expected:** Zero matches. If any appear, they are stale references that need updating.

- [ ] **Verify no stale non-numbered `Phase - Execute` references without `04`** — Run `grep -rn "Phase - Execute" .github/ | grep -v "04 Phase - Execute"` from the repo root. **Expected:** Zero matches (all Phase - Execute references should be prefixed with `04`), OR only matches in contexts where the number prefix is intentionally omitted (e.g., filename `phase-execute.agent.md`).

---

### 2. Pipeline Flow Correctness

**Features:** executor-renumber, decomposer-promote, plan-expander-create
**Covers ACs:** executor-renumber/AC3, executor-renumber/AC4, executor-renumber/AC8
**Why manual:** The 3 features were implemented separately and the end-to-end pipeline flow was never validated as a coherent whole.

#### Happy Path

- [ ] **Walk through executor pipeline when no plans exist** — Open `.github/agents/phase-execute.agent.md`. Read Step 1. Verify: (1) it scans `dev/feature/*/` for existing `-plan.md` files, (2) when none found, it invokes `03 Feature - Decomposer` as a subagent, (3) it references the Decomposer by its correct name (`03 Feature - Decomposer`). **Expected:** Step 1 clearly describes both the check and the conditional invocation using the correct agent name.

- [ ] **Walk through executor pipeline when plans exist** — Read Step 1 again. Verify: when existing `-plan.md` files are found, decomposition is skipped entirely and pipeline proceeds to Step 2. **Expected:** Clear skip-to-Step-2 path documented.

- [ ] **Verify Plan Expander step** — Read Step 2 in the executor. Verify: (1) it invokes `Feature - Plan Expander` by its correct name, (2) it passes all `dev/feature/[task-name]/` paths, (3) it verifies `-context.md` and `-tasks.md` exist after invocation. **Expected:** Step 2 matches the Plan Expander's documented input/output contract.

- [ ] **Verify Planner → Refiner → Decomposer → Executor pipeline diagram** — Open `.github/agents/project-planner.agent.md` and find the pipeline diagram. Verify it shows 4 columns: `Project - Planner` → `Phase - Refiner` → `Feature - Decomposer` → `Phase - Execute (orchestrator)`. **Expected:** The diagram shows the Decomposer as a separate, visible step between the Refiner and Executor.

- [ ] **Verify Refiner handoff references `@04 Phase - Execute`** — Open `.github/agents/phase-refiner.agent.md`. Find the "Pipeline Next Step" section. Verify the handoff message references `@04 Phase - Execute`. **Expected:** User is told to hand off to `@04 Phase - Execute`.

- [ ] **Verify executor Step 3+ unchanged** — Open `.github/agents/phase-execute.agent.md`. Verify Steps 3–7 cover the implementation loop, QA, final review, reporting, and docs update — unchanged from the pre-Phase-01 pipeline (just renumbered). **Expected:** The implementation pipeline loop (skill reference), QA step, Prod Code Review, report, and Docs Writer steps are all present.

---

### 3. Skill and Instruction Ownership Accuracy

**Features:** plan-expander-create, decomposer-promote
**Covers ACs:** plan-expander-create/AC7, plan-expander-create/AC8, decomposer-promote/AC3, decomposer-promote/AC6
**Why manual:** Ownership changes span a skill file, an instruction file, and multiple agent files — each feature's review only verified its own slice.

#### Happy Path

- [ ] **Verify `feature-plan-set` skill ownership statement** — Open `.github/skills/feature-plan-set/SKILL.md` and read the opening paragraph. Verify it says `-plan.md` is produced by `Feature - Decomposer` and `-context.md`/`-tasks.md` are produced by `Feature - Plan Expander`. **Expected:** Clear, unambiguous split ownership statement.

- [ ] **Verify `dev-task-folder` instruction producer table** — Open `.github/instructions/dev-task-folder.instructions.md` and inspect the "Standard File Naming" table. Verify: (1) `-plan.md` row shows `Feature - Decomposer` as producer, (2) `-context.md` row shows `Feature - Plan Expander`, (3) `-tasks.md` row shows `Feature - Plan Expander`. **Expected:** All three rows have correct producers.

- [ ] **Verify `read-only-agent.instructions.md` applyTo includes Decomposer** — Open `.github/instructions/read-only-agent.instructions.md` and check the `applyTo` field. Verify `**/feature-decomposer.agent.md` is present. **Expected:** Pattern matches the Decomposer file.

- [ ] **Verify `orchestrator-conventions.instructions.md` applyTo includes Executor** — Open `.github/instructions/orchestrator-conventions.instructions.md` and check the `applyTo` field. Verify `**/phase-execute.agent.md` is present. **Expected:** Pattern matches the executor file (filename unchanged on disk).

- [ ] **Verify Decomposer agent body references only `-plan.md` output** — Open `.github/agents/feature-decomposer.agent.md` and grep for `context.md` and `tasks.md`. **Expected:** Zero matches. The Decomposer should only reference producing `-plan.md` files.

- [ ] **Verify Plan Expander agent references `feature-plan-set` skill** — Open `.github/agents/feature-plan-expander.agent.md` and search for `feature-plan-set`. **Expected:** At least one reference to loading the skill for template structure.

---

### 4. Stale References in Out-of-Scope Files (Known Gaps)

**Features:** decomposer-promote, plan-expander-create, executor-renumber
**Covers ACs:** Cross-cutting — none of the 3 feature plans included these files in scope
**Why manual:** All 3 feature review records flagged stale references in files outside their scope. These were explicitly deferred but must be verified before the Phase 01 branch is merged.

#### README.md Gaps

- [ ] **README.md hidden subagents table — Decomposer misclassified** — Open `.github/agents/README.md` and find the "Hidden Subagents" table. Check whether `Feature - Decomposer` is listed as a hidden subagent. **Expected:** The Decomposer should either be moved to the "User-Facing" table as `03 Feature - Decomposer`, or annotated as dual-use. Currently, it is incorrectly listed as hidden-only.

- [ ] **README.md hidden subagents table — Plan Expander missing** — In the same table, check for a `Feature - Plan Expander` row. **Expected:** `Feature - Plan Expander` should be listed as a hidden subagent invoked by `Phase - Execute`. Currently missing.

- [ ] **README.md Task Documentation Pattern — stale producer attributions** — Find the "Task Documentation Pattern" section. Check the annotations on the file tree. **Expected:** `-context.md` and `-tasks.md` should be attributed to `Feature - Plan Expander` (not `Feature - Decomposer`). Currently stale.

- [ ] **README.md Skills table — Plan Expander not listed** — Find the "Skills and Instructions" section. Check the `feature-plan-set` row's "Used By" column. **Expected:** Should list both `Feature - Decomposer` and `Feature - Plan Expander`. Currently shows only `Feature - Decomposer`.

- [ ] **README.md Features - Decomposer description — stale** — Find the "Hidden Subagents" descriptions section. Check the `Feature - Decomposer` entry. **Expected:** Should describe plan-only output and note dual-use status. Currently describes writing "structured plans" generically.

#### phase-final-review.agent.md Gaps

- [ ] **phase-final-review per-feature documents table — stale producer attribution** — Open `.github/agents/phase-final-review.agent.md`. Find the "Per-feature documents" table (around line 29). Check whether `-context.md` and `-tasks.md` rows attribute the source to `Feature - Decomposer`. **Expected:** `-context.md` and `-tasks.md` should be attributed to `Feature - Plan Expander`. Currently stale.

- [ ] **phase-final-review document inventory template — stale producer** — Find the "Document Inventory" template table (around line 181). Check provider column for Context and Tasks rows. **Expected:** Should say `Feature - Plan Expander`. Currently says `Feature - Decomposer`.

#### phase-document-writing Skill

- [ ] **phase-document-writing skill — verify Decomposer references still valid** — Open `.github/skills/phase-document-writing/SKILL.md` and find lines referencing `Feature - Decomposer` (around lines 44 and 62). Verify these references are still correct — the Decomposer still reads the phase doc and decomposes features, so references like "so the Feature - Decomposer knows where to look" should still be valid. **Expected:** References to `Feature - Decomposer` in the context of reading phase docs and decomposing are still correct. No references should say the Decomposer writes context or tasks files.

#### CODEBASE_CONTEXT.md Gaps

- [ ] **CODEBASE_CONTEXT.md agent count stale** — Open `docs/CODEBASE_CONTEXT.md` and check the line that says "20 agent definitions." **Expected:** Should say 21 (after adding `feature-plan-expander.agent.md`). Currently says 20. Note: This is expected to be fixed by a Docs Writer pass, but should be flagged if still stale at merge time.

---

### 5. Agent Frontmatter Completeness

**Features:** decomposer-promote, plan-expander-create, executor-renumber
**Covers ACs:** decomposer-promote/AC1-AC2, plan-expander-create/AC2, executor-renumber/AC1-AC2
**Why manual:** Each feature's review verified its own agent in isolation — this checks that all 3 modified/created agents form a consistent set.

#### Happy Path

- [ ] **Verify Decomposer frontmatter** — Open `.github/agents/feature-decomposer.agent.md`. Confirm frontmatter has: `name: 03 Feature - Decomposer`, `description` mentioning plan-only output, `tools` list, NO `user-invocable` field, NO `model` field (uses VS Code default). **Expected:** Clean frontmatter matching codebase conventions.

- [ ] **Verify Plan Expander frontmatter** — Open `.github/agents/feature-plan-expander.agent.md`. Confirm frontmatter has: `name: Feature - Plan Expander`, `description`, `tools: [read, search, edit, run in terminal]`, `model`, `user-invocable: false`. **Expected:** Clean frontmatter matching hidden subagent conventions (consistent with Feature - Implementer, Feature - Reviewer, etc.).

- [ ] **Verify Executor frontmatter** — Open `.github/agents/phase-execute.agent.md`. Confirm frontmatter has: `name: 04 Phase - Execute`, `description` mentioning plan check and Plan Expander, `tools` list, `agents` list containing all 8 subagents. **Expected:** All subagent names in `agents:` match their respective `name:` fields exactly.

- [ ] **Count executor `agents:` list** — Count the entries in the executor's `agents:` list. **Expected:** 8 agents: `03 Feature - Decomposer`, `Feature - Plan Expander`, `Feature - Implementer`, `Feature - Reviewer`, `Git Commit`, `Feature - QA Writer`, `Prod Code Review`, `Docs Writer`.

---

## Cross-Cutting Concerns

### Consistency

- [ ] **No orphaned agent references** — Run `grep -rn "Feature - Decomposer" .github/` and review each match. Verify that every reference to `Feature - Decomposer` is contextually correct — it should refer to the agent that produces **plans only** (not context or tasks). **Expected:** All references are consistent with the new plan-only scope.

- [ ] **No orphaned `@03` references** — Run `grep -rn "@03" .github/` from the repo root. **Expected:** Only references to `@03 Feature - Decomposer` (not `@03 Phase - Execute`).

- [ ] **Naming pattern consistency** — User-facing agents use `NN Name` pattern. Verify: `01 Project - Planner`, `02 Phase - Refiner`, `03 Feature - Decomposer`, `04 Phase - Execute` all follow this pattern. Hidden subagents should NOT have number prefixes. **Expected:** `Feature - Plan Expander` has no number prefix; all user-facing agents have sequential numbers.

---

## Notes

- **README.md and CODEBASE_CONTEXT.md updates were explicitly out of scope** for all 3 feature plans. The plan stated these would be handled by a Docs Writer pass. The QA checklist (Section 4) flags the known stale references so they can be tracked to resolution before the branch is merged.
- **phase-final-review.agent.md** was flagged by the decomposer-promote review (Issue #3) and plan-expander-create review (implicitly) as having stale producer attributions. This was not in scope for any of the 3 features. It should be updated before or alongside the Docs Writer pass.
- **model: field removal** from `feature-decomposer.agent.md` was an undocumented change flagged by the decomposer-promote reviewer as "Wont-Fix" — it aligns with codebase convention (no other agents have `model:` in frontmatter). The Plan Expander was created WITH a `model:` field, creating a minor inconsistency to verify.
- **Review record Issue #2 (executor-renumber)**: The implementation record's manual verification claimed "zero remaining `@03 Phase - Execute`" but only checked for the `@` prefix — the reviewer caught 6 non-`@` references in README.md and fixed them. Traceability is slightly misleading but the gap was resolved.
