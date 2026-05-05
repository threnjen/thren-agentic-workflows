# Implementation Record: 04 Commit Instrumentation

## Summary

Added explicit `eval:` checkpoint commit instructions to the planner, refiner, decomposer, and phase-execute agent definitions in the master `.github/agents/` directory and propagated the same behavior to the OpenCode and Claude copies. The execute orchestrator now documents feature-local implement and review checkpoints plus consolidated phase-level QA and final-review checkpoints, while the planner/refiner/decomposer define their checkpoint message formats inline.

## Sibling Features

- `01-model-unpinning` is an earlier phase-foundation feature in the same pipeline but does not share files with this task.
- `02-hook-template` is upstream infrastructure for the eval hook and remains disjoint from this markdown-only checkpoint work.
- `03-branch-lifecycle-migration` is the direct dependency and shares `02-phase-refiner`; this implementation appended the commit checkpoint after that branch-open block rather than rewriting it.
- `04-ledger-annotation` runs in the same wave and remains disjoint because it targets `04b`, `04c`, and debugger definitions instead of the orchestrator/planner files touched here.
- `05-eval-grader-agent` is downstream and will consume the explicit `eval:` commit message convention introduced by this feature.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `01 Project - Planner` includes the `eval: affirm plan` checkpoint after plan affirmation. | Done | `.github/agents/01-project-planner.agent.md`, `opencode/agents/01-project-planner.md`, `claude/agents/project-planner.md` | Added a `Plan Affirmation` section scoped to `docs/phases/` files from the current session. |
| AC2 | `02 Phase - Refiner` includes the `eval: affirm phase <slug>` checkpoint after the branch-open block. | Done | `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` | Appended Step 7 after the branch-open/gitignore steps, reusing the existing slug derivation. |
| AC3 | `03 Feature - Decomposer` includes the `eval: decompose <slug>` checkpoint after plan writing. | Done | `.github/agents/03-feature-decomposer.agent.md`, `opencode/agents/03-feature-decomposer.md`, `claude/agents/feature-decomposer.md` | Added explicit branch-name derivation with `unknown` fallback when not on a `phase/*` branch. |
| AC4 | `04 Phase - Execute` documents `implement`, `review`, `qa`, and `final-review` checkpoints. | Done | `.github/agents/04-phase-execute.agent.md`, `opencode/agents/04-phase-execute.md`, `claude/agents/phase-execute.md` | Implement/review remain per-feature within the loop, while QA/final-review are now documented as consolidated phase-level checkpoints in Steps 4 and 5. |
| AC5 | `04 Phase - Execute` scopes checkpoint staging to the correct level for each checkpoint. | Done | `.github/agents/04-phase-execute.agent.md`, `opencode/agents/04-phase-execute.md`, `claude/agents/phase-execute.md` | Implement/review checkpoints remain limited to the active feature; the consolidated QA checkpoint is now limited to shared QA outputs and phase-level pipeline documents. |
| AC6 | Commit message conventions are defined inline in each agent. | Done | All files above | Each touched agent now spells out the exact `eval:` checkpoint message format instead of leaving it implicit. |
| AC7 | All master changes are propagated to the live copy inventory. | Done | `opencode/agents/*.md`, `claude/agents/*.md` files listed above | Propagated to all eight live derived files, matching the context-file inventory instead of the stale “six copies” wording in the plan. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/01-project-planner.agent.md` | Modify | Added `Plan Affirmation` checkpoint with `eval: affirm plan`. | Satisfies AC1 and defines the planner commit convention. |
| `.github/agents/02-phase-refiner.agent.md` | Modify | Added Step 7 checkpoint with `eval: affirm phase <slug>` after branch-open setup. | Satisfies AC2 without duplicating Feature 3's branch lifecycle steps. |
| `.github/agents/03-feature-decomposer.agent.md` | Modify | Added `Feature Decomposition` checkpoint plus branch-derived slug fallback. | Satisfies AC3 and the decomposer edge-case requirement. |
| `.github/agents/04-phase-execute.agent.md` | Modify | Replaced the single generic feature commit step with explicit implement/review checkpoints plus consolidated QA/final-review checkpoint guidance and staging rules. | Satisfies AC4, AC5, and AC6 in the master orchestrator. |
| `opencode/agents/01-project-planner.md` | Modify | Mirrored the planner checkpoint section. | Keeps OpenCode behavior aligned with the master file. |
| `opencode/agents/02-phase-refiner.md` | Modify | Mirrored the refiner checkpoint step. | Keeps OpenCode behavior aligned with the master file. |
| `opencode/agents/03-feature-decomposer.md` | Modify | Mirrored the decomposer checkpoint section. | Keeps OpenCode behavior aligned with the master file. |
| `opencode/agents/04-phase-execute.md` | Modify | Mirrored the orchestrator checkpoint and staging guidance. | Keeps OpenCode behavior aligned with the master file. |
| `claude/agents/project-planner.md` | Modify | Mirrored the planner checkpoint section. | Keeps Claude behavior aligned with the master file. |
| `claude/agents/phase-refiner.md` | Modify | Mirrored the refiner checkpoint step. | Keeps Claude behavior aligned with the master file. |
| `claude/agents/feature-decomposer.md` | Modify | Mirrored the decomposer checkpoint section. | Keeps Claude behavior aligned with the master file. |
| `claude/agents/phase-execute.md` | Modify | Mirrored the orchestrator checkpoint and staging guidance. | Keeps Claude behavior aligned with the master file. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated tests exist for this markdown-only slice. | Validation was targeted search/readback. |

## Test Results
- **Baseline**: N/A (no test runner configured; docs-only baseline recorded in `-context.md`)
- **Final**: N/A (validated via targeted grep/readback instead of automated tests)
- **New tests added**: 0
- **Regressions**: None observed in readback validation

## Deviations from Plan

- Adjusted the execute QA checkpoint from the plan's per-feature `eval: qa <task>` wording to a consolidated phase-level `eval: qa <phase-name>` checkpoint so the instructions match the orchestrator's single shared QA pass and shared QA artifacts.

## Gaps

- No automated test, lint, or format runner exists for this repository slice, so validation is limited to targeted searches and spot readback of the edited markdown files.

## Reviewer Focus Areas

- Verify the `04-phase-execute` QA checkpoint wording now matches the single consolidated QA writer flow and uses phase-level staging only for the shared QA artifacts.
- Confirm the `02-phase-refiner` checkpoint remains clearly appended after the branch-open block from `03-branch-lifecycle-migration` in all three variants.
- Check that the explicit `eval:` messages remain identical across `.github/agents/`, `opencode/agents/`, and `claude/agents/`.