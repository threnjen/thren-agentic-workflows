# 04 Commit Instrumentation Context

## Key Files

### Files to Modify

| File | Role | Change Type |
|---|---|---|
| `.github/agents/01-project-planner.agent.md` | Master planner agent; add the plan-affirmation commit checkpoint. | Modify |
| `.github/agents/02-phase-refiner.agent.md` | Master refiner agent; append the phase-affirmation checkpoint after the branch-open block. | Modify |
| `.github/agents/03-feature-decomposer.agent.md` | Master decomposer agent; add the feature-decomposition checkpoint after plan writing. | Modify |
| `.github/agents/04-phase-execute.agent.md` | Master execute orchestrator; add per-feature lifecycle checkpoints and replace the old final commit step. | Modify |
| `opencode/agents/01-project-planner.md` | OpenCode copy of the planner checkpoint change. | Modify |
| `opencode/agents/02-phase-refiner.md` | OpenCode copy of the refiner checkpoint change. | Modify |
| `opencode/agents/03-feature-decomposer.md` | OpenCode copy of the decomposer checkpoint change. | Modify |
| `opencode/agents/04-phase-execute.md` | OpenCode copy of the execute-loop checkpoint changes. | Modify |
| `claude/agents/project-planner.md` | Claude copy of the planner checkpoint change. | Modify |
| `claude/agents/phase-refiner.md` | Claude copy of the refiner checkpoint change. | Modify |
| `claude/agents/feature-decomposer.md` | Claude copy of the decomposer checkpoint change. | Modify |
| `claude/agents/phase-execute.md` | Claude copy of the execute-loop checkpoint changes. | Modify |

### Read-only Reference Files

| File | Role | Change Type |
|---|---|---|
| `dev/feature/04-commit-instrumentation/04-commit-instrumentation-plan.md` | Source plan defining acceptance criteria, stage breakdown, and edge cases. | Read-only reference |
| `dev/feature/03-branch-lifecycle-migration/03-branch-lifecycle-migration-plan.md` | Upstream dependency that owns the branch-open flow this feature extends. | Read-only reference |
| `dev/feature/04-ledger-annotation/04-ledger-annotation-plan.md` | Parallel sibling feature with intentionally disjoint scope. | Read-only reference |
| `.github/skills/implementation-pipeline-loop/SKILL.md` | Defines the existing implement-review-commit loop that Stage 4 refines. | Read-only reference |
| `docs/CODEBASE_CONTEXT.md` | Confirms the repo is docs-only and that `.github/` is the master source for derived platform copies. | Read-only reference |
| `README.md` | Documents the master/copy propagation model across GitHub Copilot, OpenCode, and Claude variants. | Read-only reference |

## Architectural Decisions

- Add checkpoint instructions as local insertions inside each agent's existing workflow rather than restructuring the documents.
- Make the commit message convention explicit in every touched agent using the `eval:` prefix so downstream ledger parsing is deterministic.
- In `04-phase-execute`, keep the current implementation pipeline shape but split the old single end-of-feature commit into lifecycle checkpoints anchored to implement, review, optional QA, and final review.
- Derive phase-specific slugs from the active git branch where needed, with an explicit fallback for decomposer flows that are not running on a phase branch.
- Treat `.github/agents/` as the master source and propagate equivalent behavior to `opencode/agents/` and `claude/agents/` after master edits are correct.

## Constraints

- Scope is limited to the four agent definitions named in the plan and their derived platform copies.
- Do not add ledger-writing logic or modify hook behavior; this feature only inserts commit checkpoint instructions.
- Do not modify `04a`, `04b`, `04c`, or `04d` subagent definitions.
- `02-phase-refiner` must append its checkpoint after the branch-open block introduced by `03-branch-lifecycle-migration`; do not duplicate the branch-open steps.
- `04-phase-execute` must stage only the active feature's files and related source edits for each checkpoint; no cross-feature staging.
- Keep changes additive and small: add one section or paragraph per agent rather than rewriting document structure.
- The plan text says "six copies," but the current repo inventory contains eight derived agent files across `opencode/agents/` and `claude/agents/`; propagation should follow the live inventory.
- This repository has no configured automated test, lint, or formatting runner, so validation for this feature is targeted file readback/manual verification.

## Relationships to Sibling Plans

- Depends on `03-branch-lifecycle-migration`: this feature assumes the branch-open instructions already exist before adding the refiner checkpoint.
- Parallel-safe with `04-ledger-annotation`: the current plan states the file sets are disjoint, so both features can run in the same wave without overlapping edits.

## Suggested Implementation Order

1. Update the master `.github/agents/` files in plan order: planner, refiner, decomposer, then execute.
2. Propagate the finalized behavior to the matching `opencode/agents/` files.
3. Propagate the finalized behavior to the matching `claude/agents/` files.
4. Read back all masters and copies to confirm message text, placement, and per-feature staging guidance.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Markdown documentation repository for GitHub Copilot/OpenCode/Claude agent definitions and skills; no runnable application code is present. |
| Test Runner | Not configured |
| Test Baseline | No tests found - baseline: N/A (captured 2026-05-04) |
| Lint | Not configured |
| Format | Not configured |

Discovery command used for the baseline scan:

```bash
find . \( -name 'package.json' -o -name 'pyproject.toml' -o -name 'pytest.ini' -o -name 'jest.config.*' -o -name 'vitest.config.*' -o -name 'ruff.toml' -o -name '.ruff.toml' -o -name '.flake8' -o -name '.eslintrc' -o -name '.eslintrc.*' -o -name '.prettierrc' -o -name '.prettierrc.*' -o -name 'prettier.config.*' -o -name '.markdownlint*' -o -name 'markdownlint.config.*' -o -name '*.test.*' -o -name '*.spec.*' -o -name '*_test.py' -o -path './tests/*' -o -path './.github/learnings/*.md' -o -path './dev/feature/*/*-context.md' -o -path './dev/feature/*/*-tasks.md' \) | sort
```

## Relevant Learnings

None applicable. The repository does not currently contain a `.github/learnings/` directory, so there were no repo-local learnings to filter for this feature.