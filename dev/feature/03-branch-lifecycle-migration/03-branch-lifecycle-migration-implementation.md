# Implementation Record: 03 Branch Lifecycle Migration

## Summary

Moved the phase-branch opening workflow from `04 Phase - Execute` into a new final branch-open section in each `02 Phase - Refiner` copy, including the exact hook symlink command, ledger-directory initialization, idempotent `.gitignore` update, branch-resume guidance, and the path-relocation reinstall note. Removed the obsolete Step 0 branch-creation block from each `04 Phase - Execute` copy and updated the remaining QA preamble to reference Step 1.

## Sibling Features

- `01-model-unpinning` touches the same three agent directories but not the same workflow sections.
- `02-hook-template` is the direct dependency for the documented `eval/hooks/post-commit.sh` path contract used here.
- `04-commit-instrumentation` also modifies `02 Phase - Refiner`, so this change keeps the new branch-open block isolated as its own final section to reduce adjacent-edit conflict.
- `04-ledger-annotation` and `05-eval-grader-agent` rely on the same `eval/runs/` ledger path conventions documented by this feature.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `02 Phase - Refiner` contains a branch-open block after phase readiness confirmation | Done | `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` | Added as a new final workflow section |
| AC2 | Branch-open block includes branch creation, hook install, ledger dir creation, and `.gitignore` update | Done | `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` | All four sub-actions are listed in order |
| AC3 | Symlink install command matches the required `ln -sfn` form plus `chmod` | Done | `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` | Exact command string present in all three copies |
| AC4 | `.gitignore` update is idempotent and works when `.gitignore` does not yet exist | Done | `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` | Guard uses `grep -qxF ... 2>/dev/null` before append |
| AC5 | `04 Phase - Execute` Step 0 branch creation is removed | Done | `.github/agents/04-phase-execute.agent.md`, `opencode/agents/04-phase-execute.md`, `claude/agents/phase-execute.md` | Step 1 is now the first numbered execution step |
| AC6 | Refiner documents path-assumption risk and reinstall guidance | Done | `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` | Inline risk note includes one-command reinstall guidance plus `chmod` rerun |
| AC7 | All changes propagated to the OpenCode and Claude copies | Done | All six agent files above | Validated with targeted searches across all copies |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/02-phase-refiner.agent.md` | Modify | Added a final branch-open workflow section with branch creation, hook install, ledger init, `.gitignore` guard, and relocation note | Makes the master refiner own branch lifecycle setup |
| `.github/agents/04-phase-execute.agent.md` | Modify | Removed Step 0 branch creation and updated the QA preamble from Step 0 to Step 1 | Eliminates duplicated branch-opening responsibility |
| `opencode/agents/02-phase-refiner.md` | Modify | Mirrored the new final branch-open workflow section | Keeps OpenCode behavior aligned with the master source |
| `opencode/agents/04-phase-execute.md` | Modify | Mirrored the Step 0 removal and Step 1 wording update | Keeps OpenCode behavior aligned with the master source |
| `claude/agents/phase-refiner.md` | Modify | Mirrored the new final branch-open workflow section in the main workflow block | Keeps Claude behavior aligned with the master source |
| `claude/agents/phase-execute.md` | Modify | Mirrored the Step 0 removal and Step 1 wording update | Keeps Claude behavior aligned with the master source |
| `dev/feature/03-branch-lifecycle-migration/03-branch-lifecycle-migration-implementation.md` | Add | Recorded implementation scope, validation, sibling awareness, and reviewer focus areas | Required handoff artifact for the feature reviewer |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated tests added; this feature is a Markdown-only orchestration change | Validation was done with targeted searches, readback, and diff review |

## Test Results
- **Baseline**: N/A (markdown-only repository slice; no test runner configured)
- **Final**: N/A (validated with targeted searches/readback/diff instead of an automated suite)
- **New tests added**: 0
- **Regressions**: None observed in the targeted validation scope

## Deviations from Plan
- Used `### Phase 7: Open Working Branch` instead of renumbering the existing `### Phase 6: Write Document`; this preserves the current workflow structure while still making the branch-open block the final action before the agent concludes.

## Gaps
None.

## Reviewer Focus Areas
- Confirm all three refiner copies keep the exact hook-install and `.gitignore` guard text aligned.
- Confirm all three execute copies remove Step 0 entirely and do not leave behind any branch-creation wording in the numbered pipeline.
- Confirm the `Phase 7` heading choice is acceptable given the pre-existing `Phase 6: Write Document` section and does not conflict with downstream expectations.
- Confirm no out-of-scope commit-checkpoint instructions were introduced into the touched agent files.