# 02 Hook Template Tasks

## Stage 1: Write the Hook Script

- [ ] Create `eval/hooks/post-commit.sh` with the `#!/usr/bin/env sh` header and POSIX-compatible shell syntax only.
- [ ] Add an early branch guard so non-`phase/*` branches, including detached HEAD, no-op and still exit 0.
- [ ] Derive the phase slug by stripping `phase/` and replacing `/` with `-`, then target `eval/runs/<phase-slug>/ledger-commits.jsonl`.
- [ ] Create the ledger directory idempotently with `mkdir -p` before any write.
- [ ] Collect the current commit SHA, raw branch name, first-line commit message, UTC timestamp, and changed file paths using standard git commands only.
- [ ] Build a valid JSONL row containing exactly `sha`, `branch`, `message`, `timestamp`, and `files`, including escaping for quotes and backslashes.
- [ ] Append one row per commit to `ledger-commits.jsonl` without overwriting existing content.
- [ ] Make the hook executable and keep the implementation free of `jq`, Python, Node, Ruby, Perl, or other external dependencies.
- [ ] Ensure the script exits 0 even if an intermediate metadata lookup or write path is unavailable.

## Stage 2: Verify and Validate

- [ ] Verify the hook does not create a ledger file when run on a non-phase branch.
- [ ] Verify the hook creates `eval/runs/<phase-slug>/` and appends a row when run on a `phase/*` branch.
- [ ] Inspect a sample JSONL row and confirm all five required fields are present with the expected schema.
- [ ] Validate slug derivation for both a single-segment branch like `phase/06d` and a multi-segment branch like `phase/01/foundation`.
- [ ] Confirm the script body contains no forbidden external dependency calls.
- [ ] Confirm the hook returns exit code 0 in both no-op and write-path scenarios.