# 02 Hook Template

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `eval/hooks/post-commit.sh` (new)
- **Sequential reason:** n/a

---

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1**: `eval/hooks/post-commit.sh` exists in `github-agents-source-of-truth`
- **AC2**: Script is a no-op on all branches that do not match `phase/*`
- **AC3**: On a `phase/*` branch, script writes one JSONL row to `eval/runs/<phase-slug>/ledger-commits.jsonl` on every commit
- **AC4**: Each JSONL row contains exactly these fields: `sha`, `branch`, `message`, `timestamp`, `files` (array of changed file paths)
- **AC5**: Script uses only POSIX shell built-ins and standard git commands — zero external dependencies (no `jq`, `python`, `node`, etc.)
- **AC6**: Script is executable (`chmod +x` applied, and the file header is `#!/usr/bin/env sh`)
- **AC7**: Phase slug derived from branch name by stripping `phase/` prefix and replacing all `/` with `-`. Example: `phase/06d` → `phase-06d`, `phase/01/foundation` → `phase-01-foundation`
- **AC8**: `eval/runs/<phase-slug>/` directory is created if it does not already exist (idempotent)
- **AC9**: Script exits 0 in all cases — it must never block a commit

### Non-Goals

- Does not install itself — installation is handled by `03-branch-lifecycle-migration`
- Does not write `ledger-events.jsonl` — that file is agent-written only
- Does not parse or validate the rubric
- Does not run on non-phase branches (any branch not matching `phase/*`)

### Traceability

| AC | Code Area | Verification |
|----|-----------|--------------|
| AC1 | `eval/hooks/post-commit.sh` | File exists at path |
| AC2 | Branch guard in script | Test: run script with `GIT_BRANCH=main` — ledger file not created |
| AC3 | Main write path | Test: run script on `phase/test` — row appears in ledger |
| AC4 | JSON construction | Read output row and verify all 5 fields present |
| AC5 | No external tool calls | `grep -v "jq\|python\|node\|ruby\|perl"` on script body |
| AC6 | File permissions | `ls -la eval/hooks/post-commit.sh` shows `x` bit |
| AC7 | Slug derivation logic | Test with multi-segment branch name |
| AC8 | mkdir -p call | Run twice on same branch — no error, same directory |
| AC9 | Exit code | Script always `exit 0` at end |

---

## B. Correctness & Edge Cases

### JSONL Row Schema

```json
{"sha": "abc1234", "branch": "phase/06d", "message": "feat: implement foo", "timestamp": "2026-05-04T14:30:00Z", "files": ["path/to/file.md", "other/file.md"]}
```

- `sha`: full 40-char SHA from `git rev-parse HEAD`
- `branch`: raw branch name from `git rev-parse --abbrev-ref HEAD`
- `message`: first line of commit message from `git log -1 --pretty=%s`
- `timestamp`: ISO 8601 UTC from `date -u +%Y-%m-%dT%H:%M:%SZ`
- `files`: array of paths from `git diff-tree --no-commit-id -r --name-only HEAD`

### JSON Construction Without `jq`

Use printf with careful quoting. The files array requires iterating changed files and building a quoted, comma-separated list. Strategy:

```sh
files=""
while IFS= read -r f; do
    files="${files:+$files,}\"$(printf '%s' "$f" | sed 's/\\/\\\\/g; s/"/\\"/g')\""
done << (git diff-tree --no-commit-id -r --name-only HEAD)
printf '{"sha":"%s","branch":"%s","message":"%s","timestamp":"%s","files":[%s]}\n' \
    "$sha" "$branch" "$msg" "$ts" "$files" >> "$ledger_file"
```

### Edge Cases

- **Empty file list**: Initial commits or merge commits may have no changed files — `files` array should be `[]`
- **Commit message with quotes or backslashes**: Must escape before embedding in JSON string
- **Detached HEAD**: `git rev-parse --abbrev-ref HEAD` returns `HEAD` — treat as non-phase branch (no-op)
- **First commit on branch**: `eval/runs/<slug>/` may not exist yet — `mkdir -p` handles this
- **Concurrent commits**: Shell append (`>>`) is atomic at the OS level for small writes — acceptable for this use case
- **macOS vs Linux `date`**: Use `date -u +%Y-%m-%dT%H:%M:%SZ` — compatible on both (GNU date and BSD date both support this)

---

## C. Consistency & Architecture Fit

### Existing Patterns

- `eval/hooks/` is a new directory — no existing pattern to follow
- Shell scripts in this repo follow `#!/usr/bin/env sh` (POSIX, not bash-specific)
- JSONL (one JSON object per line, newline-delimited) is the established schema from the Phase 01 spec

### Interface Contract

**Input**: Git environment at post-commit time (HEAD, branch, changed files)

**Output**: One appended line to `eval/runs/<phase-slug>/ledger-commits.jsonl`

**Side effects**: Creates `eval/runs/<phase-slug>/` if absent. Exits 0 always.

### Decision: Pure POSIX sh, no bash features

The hook must work on any Unix-like system where git is installed. Using `#!/usr/bin/env sh` and avoiding bashisms (arrays, `[[`, `$()` nesting beyond one level) ensures portability.

---

## D. Clean Design & Maintainability

- Script is ~30–50 lines. No functions needed for this complexity level.
- Variables are named clearly: `branch`, `slug`, `sha`, `msg`, `ts`, `ledger_dir`, `ledger_file`
- The branch guard is the first real line after variable setup: `case "$branch" in phase/*) ;; *) exit 0 ;; esac`
- One output path — no conditionals in the write block

### Keep-It-Clean Checklist

- [ ] No `jq`, `python`, `node`, `ruby`, or `perl` dependencies
- [ ] Script exits 0 unconditionally (even if an intermediate command fails — use `|| true` guards where needed)
- [ ] Commit message escaping handles `"` and `\` characters
- [ ] `mkdir -p` used for directory creation (not `mkdir` alone)
- [ ] File output uses `>>` (append), never `>` (overwrite)

---

## E. Completeness: Observability, Security, Operability

**Observability**: The hook itself is the logging mechanism. If it fails silently (e.g., directory permissions), the ledger row is simply absent. The `03-branch-lifecycle-migration` feature ensures the `eval/runs/` directory is `.gitignore`'d, so ledger files are local-only.

**Security**: The script reads only local git metadata. It writes only to `eval/runs/` in the target repo. No network calls, no credentials.

**Portability**: POSIX sh. Tested mentally against macOS (BSD sh/dash) and Linux (dash/bash in POSIX mode).

**Reinstallation**: The hook is a symlink. If it breaks, `02 Phase - Refiner` reinstalls it with `ln -sfn`. One-command operation.

---

## F. Test Plan

No automated test suite — this is a shell script. Manual verification:

### MV1 (AC2): No-op on non-phase branch

```sh
# Temporarily: cd to any repo, switch to main, run the script
GIT_DIR=<repo>/.git sh eval/hooks/post-commit.sh
# ledger-commits.jsonl must NOT be created
```

### MV2 (AC3, AC4): Row written on phase branch

```sh
# cd to target repo on a phase/* branch, make a test commit
# Read the last line of eval/runs/<slug>/ledger-commits.jsonl
# Confirm sha, branch, message, timestamp, files fields present
```

### MV3 (AC7): Slug derivation

```sh
# Test with branch phase/06d → expect phase-06d
# Test with branch phase/01/foo → expect phase-01-foo
```

### MV4 (AC5): No external dependencies

```sh
grep -E "jq|python|node|ruby|perl" eval/hooks/post-commit.sh
# Must return no output
```

### MV5 (AC9): Always exits 0

```sh
sh eval/hooks/post-commit.sh; echo "Exit: $?"
# Must print "Exit: 0"
```

---

## Stage 1: Write the Hook Script

**Goal**: Create `eval/hooks/post-commit.sh` with correct logic, schema, and POSIX compatibility.
**Success Criteria**: Script file exists, is executable, passes MV4 (no external deps), and the JSON construction produces valid JSONL output for a sample input.
**Status**: Not Started

## Stage 2: Verify and Validate

**Goal**: Run through all manual verification steps MV1–MV5.
**Success Criteria**: All five verification steps pass. Script exits 0 on both phase and non-phase branch simulations.
**Status**: Not Started
