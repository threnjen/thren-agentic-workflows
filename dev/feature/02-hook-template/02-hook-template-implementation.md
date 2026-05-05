# Implementation Record: 02 Hook Template

## Summary
Added the planned POSIX post-commit hook template at `eval/hooks/post-commit.sh`. The hook no-ops on non-`phase/*` branches, derives the documented phase slug, creates `eval/runs/<phase-slug>/` idempotently, appends one JSONL row with the required five fields for `phase/*` commits, and exits 0 in both no-op and write-path scenarios.

## Sibling Features
- `01-model-unpinning` (Wave 1): completed earlier and orthogonal to this shell hook work.
- `03-branch-lifecycle-migration` (Wave 3): directly depends on this feature's hook path and slug contract when symlinking `.git/hooks/post-commit` into target repos.
- `04-commit-instrumentation` (Wave 4): consumes the raw `ledger-commits.jsonl` timeline produced by this hook.
- `04-ledger-annotation` (Wave 4): writes semantic events to the parallel `ledger-events.jsonl` file and does not overlap with this hook's raw commit ledger responsibility.
- `05-eval-grader-agent` (Wave 5): consumes the finalized `ledger-commits.jsonl` schema established here.
- Shared module awareness: sibling features converge on `eval/runs/<phase-slug>/` and the phase-slug naming rule, so this implementation stayed narrowly aligned to the documented path and schema without adding installation or grader logic.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `eval/hooks/post-commit.sh` exists in `github-agents-source-of-truth` | Done | `eval/hooks/post-commit.sh` | Added the hook at the planned path. |
| AC2 | Script is a no-op on all branches that do not match `phase/*` | Done | `eval/hooks/post-commit.sh` | Early `case` guard exits 0 before creating any ledger path. |
| AC3 | On a `phase/*` branch, script writes one JSONL row to `eval/runs/<phase-slug>/ledger-commits.jsonl` on every commit | Done | `eval/hooks/post-commit.sh` | Append-only write path targets `ledger-commits.jsonl` under the derived slug directory. |
| AC4 | Each JSONL row contains exactly these fields: `sha`, `branch`, `message`, `timestamp`, `files` | Done | `eval/hooks/post-commit.sh` | Single `printf` emits exactly the required schema. |
| AC5 | Script uses only POSIX shell built-ins and standard git commands — zero external dependencies | Done | `eval/hooks/post-commit.sh` | Uses POSIX `sh`, standard git metadata commands, and standard shell utilities only; forbidden runtime dependencies were checked explicitly. |
| AC6 | Script is executable (`chmod +x` applied, and the file header is `#!/usr/bin/env sh`) | Done | `eval/hooks/post-commit.sh` | Shebang added and executable bit set during validation. |
| AC7 | Phase slug derived from branch name by stripping `phase/` prefix and replacing all `/` with `-` | Done | `eval/hooks/post-commit.sh` | Implemented with POSIX shell string slicing/looping; validated for `phase/06d` and `phase/01/foundation`. |
| AC8 | `eval/runs/<phase-slug>/` directory is created if it does not already exist (idempotent) | Done | `eval/hooks/post-commit.sh` | Uses `mkdir -p` before append. |
| AC9 | Script exits 0 in all cases — it must never block a commit | Done | `eval/hooks/post-commit.sh` | No-op and write-path scenarios both executed successfully with shell checks. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `eval/hooks/post-commit.sh` | Add | Added a portable post-commit hook that guards on `phase/*`, derives phase slugs, gathers commit metadata, escapes JSON strings, and appends raw ledger rows to `eval/runs/<phase-slug>/ledger-commits.jsonl` | Implements the full hook-template feature contract |
| `dev/feature/02-hook-template/02-hook-template-implementation.md` | Add | Added the implementation handoff artifact for reviewer scoping and traceability | Required deliverable for feature completion |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated test files were added for this shell/documentation slice | Validation was performed with focused executable shell checks |

## Test Results
- **Baseline**: 0 passed, 0 failed (feature context recorded no automated tests in this repository; target hook path and `eval/` tree were absent before implementation)
- **Final**: 0 passed, 0 failed (no automated suite added; focused shell validation passed)
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan
- None

## Gaps
- None

## Reviewer Focus Areas
- Confirm `eval/hooks/post-commit.sh` remains POSIX-compatible under `/usr/bin/env sh` and does not rely on Bash-only syntax.
- Confirm the JSON escaping behavior in the hook covers quote and backslash characters in commit subjects and file paths.
- Confirm the branch guard leaves non-`phase/*` branches untouched and never creates `eval/` output outside phase branches.
- Confirm the slug derivation and ledger path match downstream `03-branch-lifecycle-migration` expectations exactly.
- Confirm the hook stays limited to `ledger-commits.jsonl` and does not drift into `ledger-events.jsonl` or installation logic.