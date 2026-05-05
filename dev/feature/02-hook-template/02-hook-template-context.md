# 02 Hook Template Context

## Key Files

### Files to Change

| File | Role | Change Type |
|------|------|-------------|
| `eval/hooks/post-commit.sh` | New POSIX post-commit hook template that appends raw commit ledger rows for `phase/*` branches | Create |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `dev/feature/02-hook-template/02-hook-template-plan.md` | Source plan, acceptance criteria, edge cases, and stage breakdown for this feature | Read-only reference |
| `dev/feature/03-branch-lifecycle-migration/03-branch-lifecycle-migration-plan.md` | Downstream consumer of the hook template path and slug rules during branch-open setup | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Phase-level source of truth for hook location, ledger schema, wave ordering, and downstream dependencies | Read-only reference |
| `agentic-evaluator-plan.md` | Earlier evaluator design note showing the raw commit-hook intent and JSONL shape | Read-only reference |
| `.gitignore` | Current repo ignore rules; useful to confirm the hook template lives outside ignored paths and that `eval/` is not present yet | Read-only reference |
| `docs/CODEBASE_CONTEXT.md` | Confirms this repository is documentation-first and has no existing runnable application stack to integrate with | Read-only reference |

## Architectural Decisions

| Decision | Why |
|----------|-----|
| Implement the hook as pure POSIX `sh` with `#!/usr/bin/env sh` | The template must be portable across Unix-like environments without assuming Bash or external runtimes |
| Guard immediately on branch name and no-op for anything outside `phase/*` | The hook must never write ledger data on non-phase branches and must behave safely on detached HEAD |
| Append exactly one JSONL row per commit to `eval/runs/<phase-slug>/ledger-commits.jsonl` | The phase design uses the commit ledger as the raw timeline consumed by later features and the grader |
| Derive the phase slug by stripping `phase/` and replacing `/` with `-` | This matches the documented ledger directory naming used by branch lifecycle migration and grader features |
| Keep the script dependency-free and always exit 0 | The hook must never block a commit, and the plan explicitly forbids `jq`, Python, Node, Ruby, or Perl |
| Keep the script small and linear rather than introducing helper functions | The planned complexity is low, and a short single-path script is easier to verify and propagate |

## Constraints

- Create only `eval/hooks/post-commit.sh`; installation into target repos is handled later by `03-branch-lifecycle-migration`.
- The hook must write `ledger-commits.jsonl` only; `ledger-events.jsonl` remains agent-written and out of scope.
- The output row schema is fixed to exactly five fields: `sha`, `branch`, `message`, `timestamp`, and `files`.
- JSON string construction must handle quotes and backslashes without relying on non-standard tooling.
- `eval/runs/<phase-slug>/` creation must be idempotent with `mkdir -p`.
- The script must treat detached HEAD as a non-phase branch and still exit successfully.
- The repo currently has no `eval/` tree, so the hook path and parent directory structure are new.
- This repository is a static template/docs repo, so validation is manual file-and-shell verification rather than an existing automated suite.

## Relationships to Sibling Plans

- `03-branch-lifecycle-migration` depends directly on this feature and installs the template into target repos via `ln -sfn .../eval/hooks/post-commit.sh`.
- `04-commit-instrumentation` relies on this hook producing raw `ledger-commits.jsonl` rows so checkpoint commits become observable.
- `04-ledger-annotation` complements this feature by writing semantic events to the separate `ledger-events.jsonl` file.
- `05-eval-grader-agent` consumes the finalized `ledger-commits.jsonl` schema defined here alongside `ledger-events.jsonl`.

## Suggested Implementation Order

1. Create `eval/hooks/post-commit.sh` with the branch guard, slug derivation, JSON row construction, and unconditional `exit 0`.
2. Make the script executable and confirm it uses the required `#!/usr/bin/env sh` header.
3. Run the manual verification flow for non-phase no-op behavior, phase-branch write behavior, slug derivation, dependency-free implementation, and exit-code guarantees.
4. Land this feature before starting `03-branch-lifecycle-migration`, which references the hook path directly.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Documentation-first repository with Markdown assets plus a new POSIX shell hook template; no existing application runtime or package manifest detected |
| Test Runner | No tests found |
| Test Baseline | No tests found — baseline: N/A (captured 2026-05-04) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. No `.github/learnings/*.md` files exist in this repository.