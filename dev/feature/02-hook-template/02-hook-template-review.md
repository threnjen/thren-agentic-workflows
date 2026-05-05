# Review Record: 02 Hook Template

## Summary

Reviewed the implementation against the task plan, context, tasks, and implementation record. The hook met the intended branch guard, slug derivation, ledger path, and exit-zero behavior, but the original path serialization corrupted newline-containing filenames and the JSON escaping logic did not cover tab or carriage-return control characters. Both code defects were fixed in `eval/hooks/post-commit.sh` and revalidated with focused shell checks.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Done | `eval/hooks/post-commit.sh:1-111` | Hook exists at the planned path. |
| AC2 | Done | `eval/hooks/post-commit.sh:35-43` | Non-`phase/*` branches exit 0 before any ledger path is created. |
| AC3 | Done | `eval/hooks/post-commit.sh:67-109` | Phase branches append one JSONL row to `eval/runs/<phase-slug>/ledger-commits.jsonl`. |
| AC4 | Done | `eval/hooks/post-commit.sh:72-109` | Row contains exactly `sha`, `branch`, `message`, `timestamp`, and `files`; path/message escaping defects were fixed during review. |
| AC5 | Done | `eval/hooks/post-commit.sh:35-109` | Uses `sh`, git commands, and POSIX utilities only; no forbidden runtime dependencies (`jq`, `python`, `node`, `ruby`, `perl`) were introduced. |
| AC6 | Done | `eval/hooks/post-commit.sh:1` | Shebang is correct; executable bit was confirmed during focused shell validation. |
| AC7 | Done | `eval/hooks/post-commit.sh:51-68` | Single-segment and multi-segment phase slugs were both validated. |
| AC8 | Done | `eval/hooks/post-commit.sh:67-70` | Ledger directory creation remains idempotent via `mkdir -p`. |
| AC9 | Done | `eval/hooks/post-commit.sh:37-49`, `eval/hooks/post-commit.sh:70`, `eval/hooks/post-commit.sh:109-111` | No-op and write paths both return 0. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Converting `git diff-tree -z` output to newline-delimited text split filenames that contain embedded newlines, producing incorrect `files` arrays. | High | `eval/hooks/post-commit.sh:75` | AC4 | Fixed |
| 2 | `json_escape()` only handled quotes and backslashes, so tab or carriage-return characters in commit subjects or raw path strings could emit invalid JSON. | Medium | `eval/hooks/post-commit.sh:3`, `eval/hooks/post-commit.sh:102` | AC4 | Fixed |
| 3 | The feature still has no repeatable regression test artifact for shell edge cases, so special-character path coverage depends on manual review-time validation. | Low | `dev/feature/02-hook-template/02-hook-template-implementation.md:41` | — | Open |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `eval/hooks/post-commit.sh` | Replaced newline-collapsed path capture with git quoted-path output so newline-containing filenames serialize as a single JSON string. | 1 |
| `eval/hooks/post-commit.sh` | Extended JSON escaping to cover tab and carriage-return control characters before emitting `branch`, `message`, and non-quoted paths. | 2 |

## Remaining Concerns

- Issue #3: no automated regression harness exists for special-character filename and commit-subject edge cases; future edits could reintroduce ledger corruption without an explicit shell fixture.

## Test Coverage Assessment

- Covered: AC2, AC3, AC4, AC6, AC7, AC8, AC9 via focused shell validation (`sh -n`, non-phase no-op, phase write path, quote/backslash escaping, newline-path serialization, tab-subject escaping, executable-bit and slug checks).
- Missing: A repeatable repository-local shell regression test for special-character filenames and commit subjects.

## Risk Summary

- `eval/hooks/post-commit.sh:75-95` now relies on git's quoted-path output for unusual filenames; newline, tab, quote, and backslash cases were manually verified, but there is no checked-in regression fixture.
- `eval/hooks/post-commit.sh:3-32` still performs hand-rolled JSON escaping in POSIX shell; any future expansion of serialized fields should be reviewed against control-character handling before shipping.