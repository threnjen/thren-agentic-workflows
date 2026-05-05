# 03 Branch Lifecycle Migration Context

## Key Files

### Files to Modify

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/02-phase-refiner.agent.md` | Master source for the refiner workflow; add the new final branch-open phase here first | Modify |
| `opencode/agents/02-phase-refiner.md` | OpenCode copy of the refiner workflow; must mirror the master behavior | Modify |
| `claude/agents/phase-refiner.md` | Claude copy of the refiner workflow; must mirror the master behavior | Modify |
| `.github/agents/04-phase-execute.agent.md` | Master source for the execute orchestrator; remove the numbered Step 0 branch-creation block | Modify |
| `opencode/agents/04-phase-execute.md` | OpenCode copy of the execute orchestrator; must mirror the master behavior | Modify |
| `claude/agents/phase-execute.md` | Claude copy of the execute orchestrator; must mirror the master behavior | Modify |

### Read-only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Phase-level source for the hook-template dependency, phase-slug rule, and propagation discipline across agent directories | Read-only reference |
| `.github/agents/README.md` | Documents `.github/agents/` as the master source and `opencode/` / `claude/` as derived copies that must stay in sync | Read-only reference |
| `README.md` | Confirms this repository is a docs-and-agent-definition source of truth rather than a runnable application | Read-only reference |
| `docs/CODEBASE_CONTEXT.md` | Confirms the repo is docs-only and captures the directory layout relevant to this feature | Read-only reference |

## Architectural Decisions

- Add a new self-contained final section to `02 Phase - Refiner` instead of folding branch-open behavior into an existing phase. This matches the existing numbered workflow and keeps the migration reviewable.
- Remove only the numbered Step 0 block from `04 Phase - Execute`. The feature is a targeted responsibility move, not a broader orchestrator rewrite.
- Keep branch slug derivation as natural-language agent instructions rather than introducing helper code or new shared files. That matches the current agent-definition style.
- Treat `.github/agents/` as the authoritative edit surface, then propagate equivalent behavior to `opencode/` and `claude/` after the master files are correct.

## Constraints

- Do not modify the feature plan or create implementation/review artifacts from this task; this feature only prepares companion context and task docs.
- Do not add the post-affirmation commit checkpoint to `02 Phase - Refiner`; that belongs to sibling feature `04-commit-instrumentation`.
- Do not expand scope beyond the six agent-definition files listed above.
- The `.gitignore` update in the branch-open block must be idempotent and must account for the case where `.gitignore` does not yet exist.
- The symlink source path must be absolute, and the refiner text must explain the relocation risk plus the one-command reinstall path.
- `02-hook-template` is a prerequisite. A workspace scan did not find `eval/hooks/post-commit.sh`, so this feature should continue to treat that hook path as a dependency contract rather than implementing the hook itself.
- Preserve each platform file's existing frontmatter and naming differences while keeping the behavioral instructions equivalent.

## Relationships to Sibling Plans

- Depends on `02-hook-template`: the refiner's new branch-open instructions point at `eval/hooks/post-commit.sh`, which is expected to be delivered by that earlier feature.
- Pairs with `04-commit-instrumentation`: both features touch `02 Phase - Refiner`, so this migration should land first and keep its branch-open section isolated to reduce adjacent-edit conflicts.
- This feature does not subsume the broader eval-instrumentation work in the phase. It only relocates branch-opening responsibility and documents hook/setup behavior.

## Suggested Implementation Order

1. Update `.github/agents/02-phase-refiner.agent.md` with the new final branch-open phase and its risk/idempotency notes.
2. Update `.github/agents/04-phase-execute.agent.md` to remove Step 0 without disturbing the rest of the numbered pipeline.
3. Propagate the same behavior changes to the matching `opencode/` and `claude/` copies.
4. Verify all six files satisfy AC1-AC7 by readback comparison.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-only agent-definition repository. Primary artifacts are Copilot agent files with YAML frontmatter in `.github/agents/`, plus derived OpenCode and Claude Markdown copies. No package-managed application runtime was detected. |
| Test Runner | Not configured |
| Test Baseline | No tests found — baseline: N/A (captured 2026-05-04) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. A workspace scan did not find a `.github/learnings/` directory in this repository snapshot, so there were no repo-scoped learnings to filter for this feature.