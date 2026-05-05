# Context: 04 Ledger Annotation

## Key Files

### Files to Modify

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/04c-feature-reviewer.agent.md` | Master reviewer definition; add ledger event writing only on the "Changes Requested" path with review-stage metadata | Modify |
| `.github/agents/04b-feature-implementer.agent.md` | Master implementer definition; add ledger event writing for blocking failures and unresolvable issues | Modify |
| `.github/agents/debugger.agent.md` | Master debugger definition; add a pre-fix user-discovered annotation step for `phase/*` branches | Modify |
| `opencode/agents/04c-feature-reviewer.md` | OpenCode reviewer copy; must stay behaviorally aligned with the master reviewer file | Modify |
| `opencode/agents/04b-feature-implementer.md` | OpenCode implementer copy; must stay behaviorally aligned with the master implementer file | Modify |
| `opencode/agents/debugger.md` | OpenCode debugger copy; must stay behaviorally aligned with the master debugger file | Modify |
| `claude/agents/z-feature-reviewer.md` | Claude reviewer copy; must stay behaviorally aligned with the master reviewer file | Modify |
| `claude/agents/z-feature-implementer.md` | Claude implementer copy; must stay behaviorally aligned with the master implementer file | Modify |
| `claude/agents/debugger.md` | Claude debugger copy; must stay behaviorally aligned with the master debugger file | Modify |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `dev/feature/04-ledger-annotation/04-ledger-annotation-plan.md` | Source plan for acceptance criteria, schema requirements, stage breakdown, and propagation scope | Read-only reference |
| `dev/feature/04-commit-instrumentation/04-commit-instrumentation-plan.md` | Sibling wave plan that confirms parallel safety and disjoint file ownership | Read-only reference |
| `docs/ARCHITECTURE.md` | Confirms `.github/` is the master source of truth and `opencode/` plus `claude/` are derived copies | Read-only reference |
| `docs/CODEBASE_CONTEXT.md` | Confirms this repository is a docs-and-agent-definition repo rather than an application codebase | Read-only reference |
| `README.md` | Confirms repository purpose and platform layout for the affected agent families | Read-only reference |

## Architectural Decisions

| Decision | Why |
|----------|-----|
| Add one small ledger-writing instruction block per agent instead of restructuring agent flows | The plan explicitly treats this as an additive behavior change, not a redesign of agent control flow |
| Place the reviewer write only in the "Changes Requested" path | AC1 and the keep-it-clean checklist prohibit ledger rows for approved outcomes |
| Place the implementer write only on blocking failures or unresolvable issues | AC2 excludes routine red-green-refactor loops from ledger annotation |
| Insert the debugger annotation before any fixes begin on `phase/*` branches | AC3 defines this as a user-discovered event that must be captured before the debugger's first commit |
| Derive the ledger location from the current git branch and silently skip non-`phase/*` branches | AC5, AC6, and AC7 require phase-scoped output without adding noise on unrelated branches |
| Treat `.github/agents/*.agent.md` as the master edit surface and propagate identical semantics to `opencode/` and `claude/` copies afterward | `docs/ARCHITECTURE.md` and the plan both define `.github/` as source of truth and the other platform folders as derived variants |
| Use append-only JSONL writes with `mkdir -p` and `>>` | The plan's edge-case guidance prefers safe append semantics and directory creation over any in-place mutation |

## Constraints

- Do not add ledger writing to `04a Feature - Plan Expander` or `04d Feature - QA Writer`.
- Do not write to `ledger-commits.jsonl`; this feature only annotates `ledger-events.jsonl`.
- Do not validate, parse, or rewrite existing ledger rows.
- Do not change the agents' core review, implementation, or debugging logic beyond adding the ledger-write steps.
- Every ledger instruction must target `eval/runs/<phase-slug>/ledger-events.jsonl` in the target repo.
- Every ledger instruction must derive `phase-slug` from the current git branch by stripping `phase/` and replacing `/` with `-`.
- Every ledger instruction must silently skip writing when the current branch is not `phase/*`.
- Every ledger instruction must populate the full schema: `task_slug`, `harness`, `model`, `stage`, `detected_by`, `severity`, `evidence`, `first_seen_attempt`, `resolved_attempt`, `resolved_by`, `human_intervention_required`, `regression`, `propagated_from_stage`.
- Propagation to all six platform-copy files is mandatory before the feature is complete.

## Relationships to Sibling Plans

- Depends on `03-branch-lifecycle-migration`; the branch naming and phase-branch workflow need to exist before branch-derived ledger paths are useful.
- Runs in the same wave as `04-commit-instrumentation`.
- `04-commit-instrumentation` and `04-ledger-annotation` are explicitly parallel-safe because their file sets are disjoint.
- This feature complements commit instrumentation: commit checkpoints capture git timeline data, while ledger events capture semantic failure annotations.

## Suggested Implementation Order

1. Update the three `.github/agents/` master files first.
2. Verify schema completeness, path rules, branch guards, and agent-specific metadata across those master files.
3. Propagate the matching instruction blocks to the three `opencode/agents/` copies.
4. Propagate the matching instruction blocks to the three `claude/agents/` copies.
5. Re-read all nine changed files to confirm parity and agent-specific placement.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent-definition repository for VS Code Copilot, OpenCode, and Claude variants; primary edit surfaces are Markdown files with YAML frontmatter, with incidental Python benchmark utilities elsewhere in the repo |
| Test Runner | No tests found |
| Test Baseline | No tests found — baseline: N/A (captured 2026-05-04) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. No `.github/learnings/` directory or learning files were present in this repository during discovery.