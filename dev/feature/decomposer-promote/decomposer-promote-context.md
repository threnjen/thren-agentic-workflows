# Feature Context: decomposer-promote

## Key Files

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/feature-decomposer.agent.md` | Agent being promoted | Edit (frontmatter + body) |
| `.github/instructions/read-only-agent.instructions.md` | Instruction auto-loaded for read-only agents | Verify only (no change expected) |

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| How to make agent user-invocable | Remove `user-invocable: false` line entirely | Codebase convention: agents are user-invocable by default; only hidden subagents have `user-invocable: false`. Removing the line follows the Docs Writer precedent for dual-use agents. |
| Plan-only scope mechanism | Remove references to `-context.md` / `-tasks.md` from body text | The Plan Expander (created in sibling feature `plan-expander-create`) will own those files. Keeping the agent body clean avoids confusion about ownership. |
| Numbering | `03 Feature - Decomposer` | Follows the existing `NN Name` convention (`01 Project - Planner`, `02 Phase - Refiner`). Takes the `03` slot currently occupied by Phase - Execute, which moves to `04`. |

## Constraints

- The `-plan.md` template content (sections A–F) must NOT change — it is defined in the `feature-plan-set` skill
- The agent must remain compatible with subagent invocation by the executor (the `[SUBAGENT-MODE]` prefix pattern)
- The `read-only-agent.instructions.md` already includes `feature-decomposer.agent.md` in its `applyTo` — this must be preserved

## Relationships to Sibling Plans

- **`plan-expander-create`**: Must be implemented after this feature. The Plan Expander will own the `-context.md` and `-tasks.md` files that this feature removes from the Decomposer's scope.
- **`executor-renumber`**: Must be implemented after both `decomposer-promote` and `plan-expander-create`. The executor will reference `03 Feature - Decomposer` by its new name and invoke it as a subagent.

## Suggested Implementation Order

This feature is **first** in the sequence: `decomposer-promote` → `plan-expander-create` → `executor-renumber`

No prerequisites from sibling features. The standalone handoff message will reference `@04 Phase - Execute` which won't exist yet — that's acceptable because the executor rename happens in `executor-renumber`.
