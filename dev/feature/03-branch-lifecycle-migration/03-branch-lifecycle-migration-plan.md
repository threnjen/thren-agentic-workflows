# 03 Branch Lifecycle Migration

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** yes
- **Depends on:** 02-hook-template
- **Key files modified:** `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md`, `.github/agents/04-phase-execute.agent.md`, `opencode/agents/04-phase-execute.md`, `claude/agents/phase-execute.md`
- **Sequential reason:** n/a

---

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1**: `02 Phase - Refiner` contains a branch-open block that creates the phase branch after user affirms the phase doc is ready
- **AC2**: The branch-open block in `02 Phase - Refiner` includes: `git checkout -b phase/<slug>` (or `git switch -c`), symlink install of `eval/hooks/post-commit.sh`, `eval/runs/<phase-slug>/` directory creation in the target repo, and `.gitignore` update
- **AC3**: The symlink install command is exactly `ln -sfn <absolute-path-to-github-agents-source-of-truth>/eval/hooks/post-commit.sh <target-repo>/.git/hooks/post-commit` followed by `chmod +x <target-repo>/.git/hooks/post-commit`
- **AC4**: The `.gitignore` update appends `eval/runs/` only if the entry does not already exist (idempotent check before append)
- **AC5**: `04 Phase - Execute` Step 0 (branch creation) is removed — the step is deleted entirely and subsequent steps renumbered if needed
- **AC6**: `02 Phase - Refiner` documents the path-assumption risk: if `github-agents-source-of-truth` moves, the symlink breaks — and provides the one-command reinstall instruction
- **AC7**: All changes propagated: each of AC1–AC6 applies equally to `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md`, `opencode/agents/04-phase-execute.md`, and `claude/agents/phase-execute.md`

### Non-Goals

- Does not add the post-affirmation commit checkpoint to `02 Phase - Refiner` — that is Feature 4 (`04-commit-instrumentation`)
- Does not modify any other agent beyond `02 Phase - Refiner` and `04 Phase - Execute`
- Does not install the hook into any specific target repo — it only adds the instructions to the agent definition

### Traceability

| AC | File | Verification |
|----|------|--------------|
| AC1 | `02-phase-refiner.agent.md` | Read file: branch-open instructions present after affirmation section |
| AC2 | `02-phase-refiner.agent.md` | All four sub-actions listed in the branch-open block |
| AC3 | `02-phase-refiner.agent.md` | Exact `ln -sfn` command documented |
| AC4 | `02-phase-refiner.agent.md` | Idempotent gitignore check instruction present |
| AC5 | `04-phase-execute.agent.md` | Step 0 absent; no branch creation instructions remain |
| AC6 | `02-phase-refiner.agent.md` | Path-assumption risk note and reinstall instruction present |
| AC7 | All 4 copy files | Same sections present in all copies |

---

## B. Correctness & Edge Cases

### Branch-Open Block Placement in `02 Phase - Refiner`

`02 Phase - Refiner` currently ends with the user affirming the phase document is ready. The branch-open block must be added as the **final action** in the agent's workflow — after user confirmation, before the agent concludes.

The exact phrasing for the affirm+branch step:

```markdown
### Phase 6: Open Working Branch

After the user affirms the phase document is ready for implementation:

1. Ask the user to confirm the target repo's absolute path (or read it from context)
2. Derive the phase slug: strip `phase/` prefix from branch name, replace `/` with `-`
3. Run: `git checkout -b phase/<slug>` in the target repo
4. Install the eval hook:
   ```sh
   ln -sfn /path/to/github-agents-source-of-truth/eval/hooks/post-commit.sh \
       /path/to/target-repo/.git/hooks/post-commit
   chmod +x /path/to/target-repo/.git/hooks/post-commit
   ```
5. Create the ledger directory: `mkdir -p /path/to/target-repo/eval/runs/phase-<slug>/`
6. Update `.gitignore`: check if `eval/runs/` already present; if not, append it
7. Note for future reference: if `github-agents-source-of-truth` is moved, reinstall the hook with the same `ln -sfn` command using the updated path
```

### `04 Phase - Execute` Step 0 Removal

Current Step 0 reads:

> "Create a branch using prefix `phase/<phase-name>`. See auto-loaded orchestrator conventions for the full procedure."

This entire step must be deleted. The subsequent step numbering (Step 1, Step 2, ...) may stay the same if steps are already numbered starting at Step 1 — remove only Step 0.

### Edge Cases

- **Branch already exists**: The branch-open block should note that if the branch already exists (resuming work), `git checkout phase/<slug>` (not `-b`) should be used instead
- **Hook already installed**: `ln -sfn` is idempotent — it replaces an existing symlink silently
- **`.gitignore` missing**: If `.gitignore` doesn't exist in the target repo, the append command should create it: `echo "eval/runs/" >> .gitignore`
- **Relative vs absolute path for symlink**: The symlink source must be an absolute path. The agent must derive or ask for the absolute path of `github-agents-source-of-truth`

---

## C. Consistency & Architecture Fit

### Existing Pattern in `02 Phase - Refiner`

The agent already has a multi-phase workflow with numbered phases. Adding "Phase 6: Open Working Branch" follows this existing pattern without restructuring.

### Removal Pattern in `04 Phase - Execute`

Step 0 currently references "auto-loaded orchestrator conventions" for the branch procedure. Remove only Step 0 from the numbered execution pipeline. Do not remove any references to branch conventions in preamble or non-numbered sections.

### Decision: Branch slug derivation in agent text (not code)

The slug derivation rule (strip `phase/`, replace `/` with `-`) is documented as natural language instructions for the agent to follow, consistent with all other procedural steps in the agent definitions.

---

## D. Clean Design & Maintainability

- Add a single self-contained section to `02 Phase - Refiner` — no restructuring of existing content
- Delete one step from `04 Phase - Execute` — no restructuring of remaining steps
- Document the path-assumption risk inline where the symlink command appears

### Keep-It-Clean Checklist

- [ ] Branch-open block is a new section, not merged into an existing section
- [ ] Step 0 completely removed from `04 Phase - Execute` — no orphaned references
- [ ] All six copy files updated (3 copies of `02`, 3 copies of `04`)
- [ ] Idempotency guard documented for `.gitignore` append
- [ ] Path risk note present with one-command reinstall

---

## E. Completeness: Observability, Security, Operability

**Risk**: The `ln -sfn` symlink uses an absolute path that embeds the user's local filesystem layout. If `github-agents-source-of-truth` is moved, the hook silently stops firing. The agent text must note this risk and provide the reinstall command.

**Security**: No credentials. The hook script path is local. No network operations.

**Operability**: The gitignore update prevents ledger data from being committed accidentally.

---

## F. Test Plan

No automated tests — Markdown agent definition changes.

### MV1 (AC1, AC2): Branch-open block in `02 Phase - Refiner`

Read `.github/agents/02-phase-refiner.agent.md`. Confirm: a section titled "Open Working Branch" (or equivalent) exists after the affirmation step. Confirm all four sub-actions are listed: branch creation, hook symlink, ledger dir creation, gitignore update.

### MV2 (AC3, AC4): Symlink command and idempotency

In the same file, confirm the exact `ln -sfn` form is documented. Confirm the gitignore append has an existence check instruction.

### MV3 (AC5): Step 0 absent in `04 Phase - Execute`

Read `.github/agents/04-phase-execute.agent.md`. Confirm: no text block beginning with "Step 0" remains. Confirm Step 1 is the first numbered step.

### MV4 (AC6): Path-assumption risk note

In `02-phase-refiner.agent.md`, confirm a note about the symlink path assumption and one-command reinstall exists near the `ln -sfn` command.

### MV5 (AC7): Propagation

Read each of the four copy files (`opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md`, `opencode/agents/04-phase-execute.md`, `claude/agents/phase-execute.md`). Confirm the same changes are present.

---

## Stage 1: Add Branch-Open Block to `02 Phase - Refiner`

**Goal**: Add the Phase 6 branch-open section to `.github/agents/02-phase-refiner.agent.md` with all four sub-actions, the symlink command, and the path-assumption risk note.
**Success Criteria**: MV1, MV2, MV4 pass on the master file.
**Status**: Not Started

## Stage 2: Remove Step 0 from `04 Phase - Execute`

**Goal**: Delete the branch creation Step 0 from `.github/agents/04-phase-execute.agent.md`.
**Success Criteria**: MV3 passes on the master file.
**Status**: Not Started

## Stage 3: Propagate to `opencode/agents/` and `claude/agents/`

**Goal**: Apply identical changes to the four copy files.
**Success Criteria**: MV5 passes — all four copies match the master files.
**Status**: Not Started
