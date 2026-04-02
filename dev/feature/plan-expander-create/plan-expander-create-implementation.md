# Implementation Record: plan-expander-create

## Summary

Created the new `Feature - Plan Expander` hidden subagent that reads existing `-plan.md` files and generates companion `-context.md` and `-tasks.md` files. Updated the `feature-plan-set` skill and `dev-task-folder` instruction to reflect split ownership between Decomposer (plan) and Plan Expander (context + tasks).

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Agent file exists | Done | `.github/agents/feature-plan-expander.agent.md` | Created |
| AC2 | Frontmatter has correct fields | Done | `.github/agents/feature-plan-expander.agent.md` | `name`, `description`, `tools`, `model`, `user-invocable: false` |
| AC3 | Agent reads plans and generates context + tasks | Done | `.github/agents/feature-plan-expander.agent.md` | Workflow steps 1-4 cover read plan → read codebase → write context → write tasks |
| AC4 | Context file generation instructions | Done | `.github/agents/feature-plan-expander.agent.md` | Step 3 details key files, decisions, constraints, sibling relationships |
| AC5 | Tasks file generation instructions | Done | `.github/agents/feature-plan-expander.agent.md` | Step 4 details stage-based ordered checklist derivation |
| AC6 | Subagent mode support | Done | `.github/agents/feature-plan-expander.agent.md` | `user-invocable: false`, autonomous operation, Return Value section for subagent mode |
| AC7 | Skill updated for split ownership | Done | `.github/skills/feature-plan-set/SKILL.md` | Opening paragraph now attributes plan to Decomposer, context+tasks to Plan Expander |
| AC8 | Instruction producer table updated | Done | `.github/instructions/dev-task-folder.instructions.md` | `-context.md` and `-tasks.md` rows now show `Feature - Plan Expander` |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/feature-plan-expander.agent.md` | Created | New hidden subagent with YAML frontmatter and full workflow body | AC1-AC6: Core deliverable of this feature |
| `.github/skills/feature-plan-set/SKILL.md` | Modified | Opening paragraph updated to reflect split ownership | AC7: Decomposer → plan, Plan Expander → context + tasks |
| `.github/instructions/dev-task-folder.instructions.md` | Modified | Producer column for `-context.md` and `-tasks.md` changed from `Feature - Decomposer` to `Feature - Plan Expander` | AC8: Accurate attribution |

### Test Files

No test files — this is a docs-only repository. All verification is manual document review per Test Plan.

## Test Results
- **Baseline**: N/A (no automated tests — docs-only repo)
- **Final**: N/A
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

None. All acceptance criteria implemented as specified.

## Gaps

None. All 8 acceptance criteria are complete.

## Reviewer Focus Areas

- Agent frontmatter in `feature-plan-expander.agent.md` — verify fields match conventions used by other hidden subagents (Feature - Implementer, Feature - Reviewer)
- Workflow Step 3 (context generation) — verify instructions are sufficient for the agent to produce a complete context file matching the `feature-plan-set` skill template
- Workflow Step 4 (tasks generation) — verify the stage-to-checklist derivation logic is clear and actionable
- Skill ownership wording in `feature-plan-set/SKILL.md` — confirm the split attribution is unambiguous
- Producer table in `dev-task-folder.instructions.md` — confirm `-plan.md` row still shows `Feature - Decomposer`
