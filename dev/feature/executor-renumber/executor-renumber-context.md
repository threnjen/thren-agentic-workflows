# Feature Context: executor-renumber

## Key Files

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/phase-execute.agent.md` | Executor orchestrator being renumbered | Edit (frontmatter + pipeline body) |
| `.github/agents/project-planner.agent.md` | Upstream agent referencing executor | Edit (references + pipeline diagram) |
| `.github/agents/phase-refiner.agent.md` | Upstream agent referencing executor | Edit (references + handoff message) |
| `.github/instructions/orchestrator-conventions.instructions.md` | Orchestrator instruction with applyTo | Verify only (file not renamed on disk) |

### Reference Files (read-only, for pattern following)

| File | Why |
|------|-----|
| `.github/agents/feature-decomposer.agent.md` | Now `03 Feature - Decomposer` — the subagent the executor will invoke |
| `.github/agents/feature-plan-expander.agent.md` | New subagent the executor will invoke |
| `.github/skills/implementation-pipeline-loop/SKILL.md` | Implementation loop skill referenced by executor (unchanged) |

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| File not renamed on disk | Keep filename as `phase-execute.agent.md` | Only the frontmatter `name` changes to `04 Phase - Execute`. Renaming the file would break all `applyTo` globs in instruction files. The `name` field controls what users see in the VS Code picker. |
| Plan check mechanism | Simple existence check — scan `dev/feature/*/` for `-plan.md` files | Keeps the conditional logic minimal. No content validation. If plans exist, skip decomposition. |
| Plan Expander always runs | Invoke Plan Expander even if context/tasks files already exist | The Plan Expander should handle existing files gracefully (overwrite or skip). This keeps the pipeline simple — always invoke, let the subagent decide. |
| Decomposer invocation uses new name | Invoke `03 Feature - Decomposer` (by name) | The `agents:` frontmatter field must list the agent by its new `name` field value. The subagent invocation prompt should also use the new name. |

## Constraints

- The implementation pipeline loop (Steps 2+) must remain unchanged — only pre-loop steps change
- The `orchestrator-conventions.instructions.md` `applyTo` uses filename globs, not agent names — since the file isn't renamed, no change is needed
- The `phase-execute.agent.md` filename must NOT change (all instruction applyTo globs reference it)
- All references in upstream agents must be updated consistently — both prose mentions and `@agent` invocation references

## Cross-Reference Audit

All locations where `03 Phase - Execute` or `@03 Phase - Execute` currently appears (must be updated to `04`):

| File | Location | Current Reference |
|------|----------|-------------------|
| `phase-execute.agent.md` | Frontmatter `name:` | `03 Phase - Execute` |
| `project-planner.agent.md` | Opening paragraph | `@03 Phase - Execute` |
| `project-planner.agent.md` | Pipeline diagram (ASCII art) | `Phase - Execute (orchestrator)` |
| `project-planner.agent.md` | Phase 4 instructions | `@03 Phase - Execute` (if present) |
| `project-planner.agent.md` | Pipeline Next Step section | `@03 Phase - Execute` (if present) |
| `phase-refiner.agent.md` | "Where You Sit in the Pipeline" | `03 Phase - Execute` |
| `phase-refiner.agent.md` | Pipeline Next Step section | `@03 Phase - Execute` |
| `phase-refiner.agent.md` | Various prose mentions | `Phase - Execute` |

## Relationships to Sibling Plans

- **`decomposer-promote`** (prerequisite): Must complete first. The executor's updated Step 1 references `03 Feature - Decomposer` by its new name.
- **`plan-expander-create`** (prerequisite): Must complete first. The executor invokes `Feature - Plan Expander` as a new pipeline step, and it must be listed in the `agents:` frontmatter.

## Suggested Implementation Order

This feature is **third and final** in the sequence: `decomposer-promote` → `plan-expander-create` → `executor-renumber`

Both prerequisite features must be fully implemented before this one. The executor cannot reference agents that don't exist yet.
