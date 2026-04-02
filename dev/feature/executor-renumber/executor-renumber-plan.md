# Feature Plan: executor-renumber

**Phase**: Phase 01 — Split Feature Decomposer from Phase Execute
**Feature**: Rename `phase-execute.agent.md` to `04 Phase - Execute` and update its pipeline
**Implementation order**: 3 of 3 (depends on both `decomposer-promote` and `plan-expander-create`)

---

## A. Requirements & Traceability

### Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC1 | `phase-execute.agent.md` frontmatter `name` changed from `03 Phase - Execute` to `04 Phase - Execute` |
| AC2 | `phase-execute.agent.md` frontmatter `agents` list includes `Feature - Plan Expander` alongside existing subagents |
| AC3 | Pipeline Step 1 updated: check for existing `-plan.md` files first; if present, skip decomposition; if missing, invoke `03 Feature - Decomposer` as subagent |
| AC4 | New pipeline step added between decomposition and implementation: invoke `Feature - Plan Expander` to generate `-context.md` and `-tasks.md` from existing plans |
| AC5 | `orchestrator-conventions.instructions.md` `applyTo` updated to reference the correct executor filename (still `phase-execute.agent.md` since file is not renamed) |
| AC6 | `project-planner.agent.md` references updated from `@03 Phase - Execute` to `@04 Phase - Execute` |
| AC7 | `phase-refiner.agent.md` references updated from `@03 Phase - Execute` to `@04 Phase - Execute` |
| AC8 | Pipeline diagram in `project-planner.agent.md` updated to show `03 Feature - Decomposer` and `04 Phase - Execute` as separate steps |

### Non-Goals

- Do NOT rename the file `phase-execute.agent.md` on disk (only the frontmatter `name` changes)
- Do NOT change the implementation pipeline loop (Implement → Review → Commit cycle is untouched)
- Do NOT modify audit or test orchestrator pipelines
- Do NOT update README.md or CODEBASE_CONTEXT.md

### Traceability Matrix

| Acceptance Criteria | Files to Modify | Verification |
|---------------------|----------------|--------------|
| AC1 | `.github/agents/phase-execute.agent.md` (frontmatter) | Inspect `name:` field |
| AC2 | `.github/agents/phase-execute.agent.md` (frontmatter) | Inspect `agents:` list |
| AC3 | `.github/agents/phase-execute.agent.md` (Step 1) | Review Step 1 — plan check + conditional decomposition |
| AC4 | `.github/agents/phase-execute.agent.md` (new step) | New step invokes Plan Expander before implementation loop |
| AC5 | `.github/instructions/orchestrator-conventions.instructions.md` | Inspect `applyTo` — `phase-execute.agent.md` still present |
| AC6 | `.github/agents/project-planner.agent.md` | Grep for `@03 Phase - Execute` — should be `@04 Phase - Execute` |
| AC7 | `.github/agents/phase-refiner.agent.md` | Grep for `@03 Phase - Execute` — should be `@04 Phase - Execute` |
| AC8 | `.github/agents/project-planner.agent.md` | Pipeline diagram shows both agents |

## B. Correctness & Edge Cases

### Key Workflows

1. **No existing plans** — Executor invokes `03 Feature - Decomposer` as subagent → receives plan files → invokes Plan Expander → proceeds to implementation loop
2. **Existing plans found** — Executor skips decomposition → invokes Plan Expander to generate/regenerate context + tasks → proceeds to implementation loop
3. **Existing plans AND context/tasks found** — Executor skips decomposition → invokes Plan Expander (which should handle existing files gracefully) → proceeds to implementation loop

### Failure Modes

- If the Decomposer subagent invocation still references old `Feature - Decomposer` name instead of `03 Feature - Decomposer`, it may fail to resolve. **Note**: Agent invocation uses the `name` field, which is now `03 Feature - Decomposer`; the `agents:` frontmatter list must match.
- If the Plan Expander is not listed in `agents:` frontmatter, the executor cannot invoke it
- If upstream agents still reference `@03 Phase - Execute`, users will be directed to the wrong agent

### Error Handling Strategy

- If plan check finds no plans AND Decomposer invocation fails, report to user and stop (existing orchestrator convention)
- If Plan Expander fails, report to user and stop (cannot proceed to implementation without context + tasks)

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- **Orchestrator convention**: Orchestrators coordinate, never write directly (enforced by `orchestrator-conventions.instructions.md`)
- **Subagent invocation**: `[SUBAGENT-MODE]` prefix prompt pattern
- **Pipeline discipline**: Sequential steps, verify output between steps
- **Agent numbering**: `NN Name` format, sequential
- **Subagent list in frontmatter**: All invoked subagents must be in the `agents:` field

### Deviations

- **New plan-check step**: The executor currently always invokes the Decomposer. The new flow adds a conditional check. This is a new pattern but follows the Phase doc's design intent.

### Interfaces

- **Input**: Same as current — a refined Phase document path
- **New subagent invocations**: `03 Feature - Decomposer` (conditional) and `Feature - Plan Expander` (always)
- **Output**: Same as current — completed features with all pipeline artifacts

## D. Clean Design & Maintainability

### Simplest Design

1. Add a plan-check step before Step 1 (or modify Step 1): scan `dev/feature/*/` for existing `-plan.md` files
2. If plans exist, skip to Plan Expander invocation
3. If no plans, invoke Decomposer, then Plan Expander
4. Rest of pipeline unchanged

### Complexity Risks

- Medium. The conditional decomposition step adds branching logic to the pipeline. Keep the branch simple: "plans exist → skip; no plans → invoke Decomposer."

### Keep It Clean Checklist

- [ ] Pipeline steps are clearly numbered and sequential
- [ ] Plan-check logic is simple (existence check only, not content validation)
- [ ] Both new subagents listed in `agents:` frontmatter
- [ ] All upstream references updated consistently

## E. Completeness: Observability, Security, Operability

- **Logging/metrics/tracing**: Not applicable (Markdown docs)
- **Security**: Not applicable
- **Runbook**: Not applicable — verify by running the executor pipeline end-to-end

## F. Test Plan

### Test Approach

All verification is manual document review and cross-reference checking.

### Test Cases

| # | Test Case | Given | When | Then |
|---|-----------|-------|------|------|
| T1 | Executor name updated | After implementation | Inspect frontmatter | `name` is `04 Phase - Execute` |
| T2 | Plan Expander in agents list | After implementation | Inspect frontmatter `agents:` | `Feature - Plan Expander` is listed |
| T3 | No existing plans flow | No `-plan.md` files exist | Executor runs Step 1 | Invokes `03 Feature - Decomposer`, then Plan Expander |
| T4 | Existing plans flow | `-plan.md` files exist in `dev/feature/` | Executor runs Step 1 | Skips Decomposer, invokes Plan Expander directly |
| T5 | Orchestrator instruction | After implementation | Inspect `orchestrator-conventions.instructions.md` applyTo | `phase-execute.agent.md` is still matched |
| T6 | Planner references | After implementation | Grep `project-planner.agent.md` for `Phase - Execute` | All references are `@04 Phase - Execute` or `04 Phase - Execute` |
| T7 | Refiner references | After implementation | Grep `phase-refiner.agent.md` for `Phase - Execute` | All references are `@04 Phase - Execute` or `04 Phase - Execute` |
| T8 | Pipeline diagram | After implementation | Inspect `project-planner.agent.md` pipeline diagram | Shows `03 Feature - Decomposer` and `04 Phase - Execute` as separate entities |

### Test Data / Fixtures

- Use any existing refined Phase document as input for manual end-to-end verification

---

## Stage 1: Update Executor Frontmatter

**Goal**: Rename to `04 Phase - Execute` and add Plan Expander to subagent list
**Success Criteria**: `name` is `04 Phase - Execute`; `agents:` includes `Feature - Plan Expander`; `description` updated to reflect new pipeline
**Status**: Not Started

## Stage 2: Update Executor Pipeline — Plan Check and Conditional Decomposition

**Goal**: Modify Step 1 to check for existing `-plan.md` files and conditionally invoke Decomposer
**Success Criteria**: Step 1 scans for existing plans; if found, skips decomposition; if not found, invokes `03 Feature - Decomposer`; Decomposer invocation prompt updated to reference `03 Feature - Decomposer`
**Status**: Not Started

## Stage 3: Add Plan Expander Invocation Step

**Goal**: Add a new step between decomposition and the implementation loop that invokes `Feature - Plan Expander`
**Success Criteria**: New step invokes Plan Expander with paths to plan files; verifies `-context.md` and `-tasks.md` exist after invocation; pipeline numbering is consistent
**Status**: Not Started

## Stage 4: Update Orchestrator Instruction applyTo

**Goal**: Verify/update `orchestrator-conventions.instructions.md` applyTo
**Success Criteria**: `applyTo` glob still matches `phase-execute.agent.md` (file is not renamed on disk, so no change expected — verify only)
**Status**: Not Started

## Stage 5: Update Upstream Agent References

**Goal**: Update `project-planner.agent.md` and `phase-refiner.agent.md` to reference `04 Phase - Execute`
**Success Criteria**: All `@03 Phase - Execute` references become `@04 Phase - Execute`; pipeline diagram in Planner shows both `03 Feature - Decomposer` and `04 Phase - Execute`
**Status**: Not Started
