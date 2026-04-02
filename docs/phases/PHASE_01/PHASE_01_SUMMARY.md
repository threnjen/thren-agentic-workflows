# Phase 1: Split Feature Decomposer from Phase Execute

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: None

## Objective

Extract the feature decomposition stage from the current `03 Phase - Execute` orchestrator into a standalone, user-facing `03 Feature - Decomposer` agent that writes only `-plan.md` files. Renumber the current executor to `04 Phase - Execute`, which checks for existing plans (invoking `03` as a subagent if missing) and delegates `-context.md` / `-tasks.md` generation to a new hidden subagent before running the implementation loop.

## Scope

### In Scope
- Promote `Feature - Decomposer` from hidden subagent to dual-use agent (user-invocable AND subagent of `04 Execute`)
- Scope `03 Feature - Decomposer` output to `-plan.md` only (no `-context.md`, no `-tasks.md`)
- Create a new hidden subagent (`Feature - Plan Expander`) that reads `-plan.md` files and generates `-context.md` and `-tasks.md`
- Renumber `03 Phase - Execute` → `04 Phase - Execute`
- Update `04 Phase - Execute` pipeline: check for existing `-plan.md` files; if missing, invoke `03 Feature - Decomposer` as subagent; then invoke `Feature - Plan Expander` to generate context+tasks before the implementation loop
- Update `02 Phase - Refiner` references to point to both `03 Feature - Decomposer` and `04 Phase - Execute`
- Update `01 Project - Planner` references for the new numbering
- Update the `feature-plan-set` skill to reflect split ownership (plan by Decomposer, context+tasks by Plan Expander)
- Update `dev-task-folder.instructions.md` producer columns
- Update `read-only-agent.instructions.md` applyTo patterns (Decomposer is now user-invocable but still read-only)
- Update `orchestrator-conventions.instructions.md` applyTo to reference the renamed executor file

### Out of Scope
- Changing the `-plan.md` template content (sections A–F stay the same)
- Changing the implementation pipeline loop (Implement → Review → Commit cycle is untouched)
- Modifying audit or test orchestrator pipelines
- README.md and CODEBASE_CONTEXT.md updates (user will run Docs Writer separately)
- Changing the `-context.md` or `-tasks.md` content templates (just moving who produces them)

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Updated `feature-decomposer.agent.md` | Promoted to user-facing `03 Feature - Decomposer`, plan-only output, dual-use (standalone + subagent) | Agent definition |
| 2 | Renamed `phase-execute.agent.md` | Becomes `04 Phase - Execute` with updated pipeline flow | Agent definition |
| 3 | New `feature-plan-expander.agent.md` | Hidden subagent that generates `-context.md` and `-tasks.md` from existing `-plan.md` files | Agent definition |
| 4 | Updated `feature-plan-set/SKILL.md` | Reflects split ownership — plan by Decomposer, context+tasks by Plan Expander | Skill update |
| 5 | Updated instruction files | `dev-task-folder`, `read-only-agent`, `orchestrator-conventions` — updated references and applyTo patterns | Instruction updates |
| 6 | Updated upstream agent references | `project-planner.agent.md` and `phase-refiner.agent.md` — updated pipeline numbering and handoff instructions | Agent updates |

## Technical Context

This repository contains only Markdown files — no runnable code. All changes are edits to `.agent.md`, `SKILL.md`, and `.instructions.md` files in `.github/agents/`, `.github/skills/`, and `.github/instructions/`.

Key files affected:
- `.github/agents/feature-decomposer.agent.md` — currently hidden subagent, writes 3 files
- `.github/agents/phase-execute.agent.md` — currently `03 Phase - Execute` orchestrator
- `.github/agents/phase-refiner.agent.md` — references `03 Phase - Execute` in handoff
- `.github/agents/project-planner.agent.md` — references `03 Phase - Execute` in pipeline diagram
- `.github/skills/feature-plan-set/SKILL.md` — defines the three-file convention
- `.github/instructions/dev-task-folder.instructions.md` — producer attribution table
- `.github/instructions/read-only-agent.instructions.md` — applyTo includes `feature-decomposer.agent.md`
- `.github/instructions/orchestrator-conventions.instructions.md` — applyTo includes `phase-execute.agent.md`

Existing patterns:
- Dual-use agent precedent: `Docs Writer` is both user-invocable and a subagent
- Hidden subagent convention: `user-invocable: false` in YAML frontmatter
- Subagent invocation uses `[SUBAGENT-MODE]` prefix prompts
- Orchestrators list subagents in `agents:` frontmatter field

## Dependencies & Risks

- **Dependency**: The `feature-plan-set` skill is consumed by both the Decomposer and the Plan Expander — changes must be coordinated so both agents reference the correct sections
- **Risk**: Agents referencing `03 Phase - Execute` by number (in prose, not just filenames) will break if not updated. **Mitigation**: Grep for all references to `03 Phase`, `@03`, and `Phase - Execute` across all `.md` files
- **Risk**: The new `Feature - Plan Expander` subagent duplicates logic that was previously inline in the Decomposer. **Mitigation**: Keep the Plan Expander minimal — it reads plans and generates two files, nothing more

## Success Criteria

- [ ] `03 Feature - Decomposer` is visible in the VS Code agent picker and produces only `-plan.md` files per feature
- [ ] `04 Phase - Execute` correctly detects existing `-plan.md` files and skips decomposition when they're present
- [ ] `04 Phase - Execute` invokes `03 Feature - Decomposer` as a subagent when no plans exist
- [ ] `04 Phase - Execute` invokes `Feature - Plan Expander` to generate `-context.md` and `-tasks.md` before the implementation loop
- [ ] `Feature - Plan Expander` is hidden (`user-invocable: false`) and correctly generates both files from existing plans
- [ ] All upstream agents (`01 Project - Planner`, `02 Phase - Refiner`) reference the updated numbering
- [ ] All instruction files have correct `applyTo` patterns for renamed/new agent files
- [ ] The `feature-plan-set` skill accurately reflects which agent produces which file

## QA Considerations

- This repo contains no runnable code — QA is document review, not automated testing
- Verify all cross-references between agent files are consistent (agent names in `agents:` frontmatter, `@agent` references in prose, instruction `applyTo` globs)
- Verify the pipeline diagrams in README.md are updated (user will run Docs Writer)

## Notes for Feature - Decomposer

Suggested decomposition into 3 features:

1. **`decomposer-promote`** — Promote `feature-decomposer.agent.md` to user-facing `03 Feature - Decomposer` (plan-only). Update its frontmatter, workflow, output format, and standalone mode messaging. Update `read-only-agent.instructions.md` applyTo.

2. **`plan-expander-create`** — Create the new `feature-plan-expander.agent.md` hidden subagent. Update `feature-plan-set/SKILL.md` to reflect split ownership. Update `dev-task-folder.instructions.md` producer table.

3. **`executor-renumber`** — Rename `phase-execute.agent.md` to `04 Phase - Execute`. Update its pipeline to check for existing plans, invoke Decomposer if missing, invoke Plan Expander for context+tasks. Update `orchestrator-conventions.instructions.md` applyTo. Update references in `project-planner.agent.md` and `phase-refiner.agent.md`.

**Implementation order**: `decomposer-promote` → `plan-expander-create` → `executor-renumber` (the executor depends on both new agents existing).
