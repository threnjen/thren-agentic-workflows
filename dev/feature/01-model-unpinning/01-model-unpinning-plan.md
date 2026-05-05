# 01 Model Unpinning

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `.github/agents/*.agent.md` (18 files), `.github/agents/prod-code-review.md`, `opencode/agents/` (4 files with model:), `claude/agents/z-feature-qa-writer.md`, `claude/agents/z-feature-plan-expander.md`
- **Sequential reason:** n/a

---

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1**: No `model:` field appears in any agent definition file in `.github/agents/`
- **AC2**: No `model:` field appears in any agent definition file in `opencode/agents/`
- **AC3**: No `model:` field appears in any agent definition file in `claude/agents/`
- **AC4**: All other frontmatter fields and agent body content remain byte-for-byte unchanged
- **AC5**: Files that had no `model:` line are not modified

### Non-Goals

- Do not modify `.github/instructions/` or `.github/skills/` files
- Do not change any field other than the `model:` line
- Do not reformat or reorder any frontmatter
- Do not add or remove any other frontmatter fields

### Traceability

| AC | Files Affected | Verification |
|----|----------------|--------------|
| AC1 | 18 files in `.github/agents/` | `grep -r "^model:" .github/agents/` returns no results |
| AC2 | 4 files in `opencode/agents/` | `grep -r "^model:" opencode/agents/` returns no results |
| AC3 | 2 files in `claude/agents/` | `grep -r "^model:" claude/agents/` returns no results |
| AC4 | All modified files | Diff shows only `model:` line removal, no other changes |
| AC5 | All unmodified files | File hashes unchanged for files without `model:` |

---

## B. Correctness & Edge Cases

### Files with `model:` in `.github/agents/` (18 total)

| File | Current Model Value |
|------|---------------------|
| `01-project-planner.agent.md` | `Claude Sonnet 4.6 (copilot)` |
| `02-phase-refiner.agent.md` | `Claude Sonnet 4.6 (copilot)` |
| `03-feature-decomposer.agent.md` | `Claude Sonnet 4.6 (copilot)` |
| `04-phase-execute.agent.md` | `GPT-5.4 (copilot)` |
| `04a-feature-plan-expander.agent.md` | `GPT-5.4 (copilot)` |
| `04b-feature-implementer.agent.md` | `GPT-5.3-Codex (copilot)` |
| `04c-feature-reviewer.agent.md` | `GPT-5.3-Codex (copilot)` |
| `04d-feature-qa-writer.agent.md` | `Auto` |
| `audit-code-or-infra.agent.md` | `Claude Sonnet 4.6 (copilot)` |
| `auditor-code.agent.md` | `GPT-5.3-Codex (copilot)` |
| `auditor-infra.agent.md` | `GPT-5.4 (copilot)` |
| `auditor-refactor.agent.md` | `Claude Sonnet 4.6 (copilot)` |
| `prod-code-review.md` | `Claude Sonnet 4.6 (copilot)` |
| `test-analyst.agent.md` | `GPT-5.4 (copilot)` |
| `test-fixer.agent.md` | `GPT-5.3-Codex (copilot)` |
| `test-writer.agent.md` | `GPT-5.3-Codex (copilot)` |
| `unity-reviewer.agent.md` | `GPT-5.3-Codex (copilot)` |
| `agent-test-runner.agent.md` | `Claude Haiku 4.5 (copilot)` |

### Files with `model:` in `opencode/agents/` (4 total)

| File | Current Model Value |
|------|---------------------|
| `web-researcher.md` | `deepseek/deepseek-v4-flash` |
| `03-feature-decomposer.md` | `anthropic/claude-sonnet-4-6` |
| `agent-testing-agent.md` | `deepseek/deepseek-v4-flash` |
| `agent-test-runner.md` | `deepseek/deepseek-v4-flash` |

### Files with `model:` in `claude/agents/` (2 total)

| File | Current Model Value |
|------|---------------------|
| `z-feature-qa-writer.md` | `haiku` |
| `z-feature-plan-expander.md` | `haiku` |

### Edge Cases

- `model: Auto` in `04d-feature-qa-writer.agent.md` is still a model pin — remove it
- The `prod-code-review.md` file uses `.md` not `.agent.md` but lives in `.github/agents/` — treat identically
- Some agents (e.g., `debugger.agent.md`, `docs-writer.agent.md`) have no `model:` line — do not touch them
- Remove only the line containing `model:`. If the line is adjacent to other frontmatter, ensure the surrounding YAML remains valid (no double blank lines introduced)
- Frontmatter block is delimited by `---` markers. Removing a key-value line leaves valid YAML

---

## C. Consistency & Architecture Fit

### Pattern

All three directories share the same YAML frontmatter convention. The `model:` key is a single line within the `---` frontmatter block. Removal must be surgical (one line deleted per file).

### Decision Rationale

Removing `model:` allows the harness (VS Code / OpenCode / Claude Code) to select the active model at invocation time. This is the prerequisite for the eval framework to compare different model+harness combinations on the same task.

### Naming and Structure

No structural changes — existing agent body, other frontmatter fields (`name:`, `description:`, `tools:`, `agents:`), and all body content remain unchanged.

---

## D. Clean Design & Maintainability

- One operation: delete the `model:` line. Nothing else.
- Use `replace_string_in_file` or `multi_replace_string_in_file` — not sed — to avoid accidental collateral edits
- After editing, read the first 10 lines of each modified file to verify frontmatter integrity
- No helpers, no scripts — direct file edits only

### Keep-It-Clean Checklist

- [ ] Only `model:` lines removed — no other diffs
- [ ] Frontmatter block still opens and closes with `---`
- [ ] No blank lines introduced between remaining frontmatter keys
- [ ] All 24 files confirmed modified or intentionally skipped

---

## E. Completeness: Observability, Security, Operability

**Verification command** (run after edits):
```bash
grep -r "^model:" .github/agents/ opencode/agents/ claude/agents/
```
Expected output: nothing (empty).

**Security**: No secrets, credentials, or sensitive data involved.

**Rollback**: `git diff` shows only `model:` line removals. `git checkout -- <file>` restores any file.

---

## F. Test Plan

No automated tests apply — this is a configuration-file-only change.

### Manual Verification Steps

**MV1** (AC1, AC2, AC3): Run `grep -r "^model:" .github/agents/ opencode/agents/ claude/agents/` — must return empty.

**MV2** (AC4): Run `git diff --stat` — diff count equals number of modified files; `git diff` body shows only `- model: ...` line deletions with no other context lines changed.

**MV3** (AC5): Files with no `model:` line must not appear in `git diff` output.

**MV4** (structural): Open one modified file from each directory and confirm `---` frontmatter delimiters are intact and the file is readable.

---

## Stage 1: Remove `model:` from `.github/agents/`

**Goal**: Delete the `model:` line from all 18 files in `.github/agents/` that contain one.
**Success Criteria**: `grep -r "^model:" .github/agents/` returns no output. All other file content unchanged.
**Status**: Not Started

## Stage 2: Remove `model:` from `opencode/agents/`

**Goal**: Delete the `model:` line from the 4 files in `opencode/agents/` that contain one.
**Success Criteria**: `grep -r "^model:" opencode/agents/` returns no output.
**Status**: Not Started

## Stage 3: Remove `model:` from `claude/agents/`

**Goal**: Delete the `model:` line from the 2 files in `claude/agents/` that contain one.
**Success Criteria**: `grep -r "^model:" claude/agents/` returns no output.
**Status**: Not Started

## Stage 4: Final Verification

**Goal**: Confirm all three directories are clean and no collateral damage occurred.
**Success Criteria**: All manual verification steps MV1–MV4 pass. `git diff` shows only expected line removals.
**Status**: Not Started
