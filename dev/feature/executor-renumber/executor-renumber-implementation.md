# Implementation Record: executor-renumber

## Summary

Renumbered `phase-execute.agent.md` from `03 Phase - Execute` to `04 Phase - Execute` in the YAML frontmatter (filename unchanged). Updated the executor's pipeline to check for existing plans before invoking the Decomposer, added a new Plan Expander step, and updated all upstream agent references to use the new number.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Frontmatter `name` changed to `04 Phase - Execute` | Done | `.github/agents/phase-execute.agent.md` | |
| AC2 | `agents:` list includes `Feature - Plan Expander` and `03 Feature - Decomposer` | Done | `.github/agents/phase-execute.agent.md` | Also updated `Feature - Decomposer` → `03 Feature - Decomposer` to match the renamed agent |
| AC3 | Step 1 checks for existing plans, conditionally invokes Decomposer | Done | `.github/agents/phase-execute.agent.md` | Step 1 renamed to "Obtain Feature Plans" with conditional branching |
| AC4 | New step invokes Plan Expander between decomposition and implementation loop | Done | `.github/agents/phase-execute.agent.md` | Added as Step 2: "Expand Plans" |
| AC5 | `orchestrator-conventions.instructions.md` `applyTo` still matches `phase-execute.agent.md` | Done | `.github/instructions/orchestrator-conventions.instructions.md` | Verify only — no change needed since filename unchanged |
| AC6 | `project-planner.agent.md` references updated from `@03` to `@04` | Done | `.github/agents/project-planner.agent.md` | 3 references updated |
| AC7 | `phase-refiner.agent.md` references updated from `@03` to `@04` | Done | `.github/agents/phase-refiner.agent.md` | 3 references updated (opening paragraph, Entry A/B, Pipeline Next Step) |
| AC8 | Pipeline diagram updated to show Decomposer and Execute as separate steps | Done | `.github/agents/project-planner.agent.md` | 4-column diagram: Planner → Refiner → Feature - Decomposer → Phase - Execute |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/phase-execute.agent.md` | Modified | Frontmatter: `name` 03→04, `description` updated, `agents` list updated with `03 Feature - Decomposer` and `Feature - Plan Expander`. Pipeline: Step 1 rewritten with plan-check + conditional Decomposer invocation, new Step 2 for Plan Expander, Steps 2-6 renumbered to 3-7. Decomposer invocation prompt updated to reference plan files only (not three-file set). | AC1, AC2, AC3, AC4 |
| `.github/agents/project-planner.agent.md` | Modified | All `@03 Phase - Execute` → `@04 Phase - Execute` (3 occurrences). Pipeline diagram replaced with 4-column version showing Feature - Decomposer between Refiner and Execute. | AC6, AC8 |
| `.github/agents/phase-refiner.agent.md` | Modified | All `@03 Phase - Execute` → `@04 Phase - Execute` (3 occurrences: opening paragraph, Entry A/B pipeline lines, Pipeline Next Step handoff message). | AC7 |
| `.github/instructions/orchestrator-conventions.instructions.md` | Verified | `applyTo` glob already matches `**/phase-execute.agent.md` — no change needed since the filename is unchanged. | AC5 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| N/A | — | No automated tests (docs-only repo) | — |

## Test Results
- **Baseline**: No automated tests (docs-only repository)
- **Final**: N/A
- **New tests added**: 0
- **Regressions**: None

### Manual Verification Performed

- Grep confirmed zero remaining `@03 Phase - Execute` references in `.github/agents/` files
- Grep confirmed `orchestrator-conventions.instructions.md` `applyTo` still contains `phase-execute.agent.md`
- Step numbering verified sequential: 0, 1, 2, 3, 4, 5, 6, 7
- `agents:` frontmatter list contains both new agents: `03 Feature - Decomposer`, `Feature - Plan Expander`

## Deviations from Plan

- The Decomposer invocation prompt was simplified to reference only `-plan.md` (not the "three-file plan set") since the `decomposer-promote` feature already changed the Decomposer to produce only plan files. This is consistent with the current Decomposer behavior.

## Gaps

None.

## Reviewer Focus Areas

- **Step 1 conditional logic** in `phase-execute.agent.md` (lines 25-44) — verify the plan-check + conditional Decomposer invocation is clear and handles both paths correctly
- **Step 2 Plan Expander invocation** in `phase-execute.agent.md` (lines 46-55) — verify the prompt is actionable and the verification step is sufficient
- **Pipeline diagram** in `project-planner.agent.md` — verify the 4-column format is readable and correctly shows the Decomposer as a separate pipeline step
- **Reference consistency** — all three upstream/downstream files should show `04 Phase - Execute` with no remaining `03` references
