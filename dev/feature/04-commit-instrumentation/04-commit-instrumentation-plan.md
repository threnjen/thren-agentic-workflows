# 04 Commit Instrumentation

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** yes
- **Depends on:** 03-branch-lifecycle-migration
- **Key files modified:** `.github/agents/01-project-planner.agent.md`, `.github/agents/02-phase-refiner.agent.md`, `.github/agents/03-feature-decomposer.agent.md`, `.github/agents/04-phase-execute.agent.md`, and all six copies in `opencode/agents/` and `claude/agents/`
- **Sequential reason:** n/a (parallel-safe with 04-ledger-annotation; disjoint file sets)

> **Sibling plan note**: `04-ledger-annotation` runs in the same wave. File sets are fully disjoint — this feature touches 01, 02, 03, 04 agents; ledger-annotation touches 04b, 04c, and debugger. Safe to run in parallel.

---

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1**: `01 Project - Planner` includes a commit checkpoint after the user affirms plan documents are complete, using message: `eval: affirm plan`
- **AC2**: `02 Phase - Refiner` includes a commit checkpoint after the user affirms phase refinement is done (and the branch has been opened by Feature 3), using message: `eval: affirm phase <slug>`
- **AC3**: `03 Feature - Decomposer` includes a commit checkpoint after all feature plan files are written, using message: `eval: decompose <slug>`
- **AC4**: `04 Phase - Execute` adds per-feature commit checkpoints after implementation (`eval: implement <task>`) and review (`eval: review <task>`), then emits the consolidated phase-level QA checkpoint (`eval: qa <phase-name>`) and the single phase-level final-review checkpoint (`eval: final-review`) in Steps 4 and 5
- **AC5**: `04 Phase - Execute` keeps feature-local staging for the per-feature implementation/review checkpoints and uses phase-level staging only for the consolidated QA and final-review outputs
- **AC6**: Commit message convention is defined in each agent's instructions — not left implicit
- **AC7**: All changes propagated to all six copy files across `opencode/agents/` and `claude/agents/`

### Non-Goals

- Does not add ledger-events writing — that is Feature 5 (`04-ledger-annotation`)
- Does not change the hook template or how commits are recorded by the hook — hook records all commits automatically
- Does not modify `04a`, `04b`, `04c`, or `04d` subagent definitions (those are Feature 5's scope except for the orchestrator-level commit steps in `04`)

### Traceability

| AC | File | Verification |
|----|------|--------------|
| AC1 | `01-project-planner.agent.md` | Read file: commit instruction with `eval: affirm plan` message present |
| AC2 | `02-phase-refiner.agent.md` | Read file: commit instruction with `eval: affirm phase <slug>` present after branch-open section |
| AC3 | `03-feature-decomposer.agent.md` | Read file: commit instruction with `eval: decompose <slug>` present after plan-writing section |
| AC4 | `04-phase-execute.agent.md` | Read file: four commit instructions in each feature cycle |
| AC5 | `04-phase-execute.agent.md` | File-scoping note present in each commit instruction |
| AC6 | All four agent files | Commit message format documented inline |
| AC7 | 6 copy files | Same sections present in all copies |

---

## B. Correctness & Edge Cases

### Commit Checkpoint Placement

**`01 Project - Planner`**

Add after the section where the user reviews and approves plan documents. Text:

```markdown
### Commit: Plan Affirmation

After the user confirms the plan documents are final:

Commit all `docs/phases/` files created or modified in this session with message: `eval: affirm plan`
```

**`02 Phase - Refiner`**

Feature 3 (`03-branch-lifecycle-migration`) already adds the branch-open block as Phase 6. This feature adds the commit checkpoint as the final action within Phase 6, after the branch has been created and the hook installed:

```markdown
After completing the branch-open steps, commit all `docs/phases/` files modified in this session with message: `eval: affirm phase <slug>`

Replace `<slug>` with the derived phase slug (e.g., `phase-06d`).
```

> **Important**: Feature 3 writes the branch-open block first. This feature only adds the commit instruction at the end of that block. They must not overlap — add only the commit line; do not duplicate branch-creation steps.

**`03 Feature - Decomposer`**

Add after the section where plan files are written to `dev/feature/`. Text:

```markdown
### Commit: Feature Decomposition

After all plan files are written:

Commit all `dev/feature/` files created in this session with message: `eval: decompose <slug>`

Replace `<slug>` with the phase slug derived from the current branch name.
```

**`04 Phase - Execute`**

Within the feature development loop, the existing pipeline has Implement → Review → consolidated QA → consolidated final review. Add the checkpoints at these points:

```
A. After Implementer returns → commit: eval: implement <task>
B. After Reviewer returns → commit: eval: review <task>
C. After the consolidated QA Writer step returns (if QA was run) → commit: eval: qa <phase-name>
D. After the phase final review is complete → commit: eval: final-review
```

For A and B, the commit instruction must specify: "stage only files belonging to `dev/feature/[0N-task-name]/` and any source files modified by this feature — do not stage files from other feature directories."

For C and D, the commit instruction must specify phase-level staging only: shared QA outputs, the final review artifact, and any phase-level pipeline documents updated by those steps.

### Edge Cases

- **`03 Feature - Decomposer` may not know the branch slug**: The slug is derived from the current git branch. The instruction should specify: run `git rev-parse --abbrev-ref HEAD`, strip `phase/`, replace `/` with `-`. If not on a phase branch, skip the commit or use `eval: decompose unknown`.
- **`04 Phase - Execute` QA step is conditional**: If the user opted out of QA generation (asked at the start), the consolidated `eval: qa <phase-name>` commit does not fire. The instruction must note this.
- **`04 Phase - Execute` parallel wave**: For a parallel wave, implement/review checkpoints still happen per-feature once each subagent returns. QA and final-review remain consolidated phase-level steps after all waves complete.
- **Message slug in `01 Project - Planner`**: The planner operates at the project level, not a single phase — `eval: affirm plan` (no slug) is correct.

---

## C. Consistency & Architecture Fit

### Existing Commit Pattern in `04 Phase - Execute`

The current implementation-pipeline-loop skill defines a single commit per feature at step D. The sub-step commits are additions within that same cycle, not replacements. The existing end-of-feature commit (Step D) may be replaced by the `eval: final-review` commit or remain as a separate commit — the plan chooses to replace Step D with `eval: final-review` to avoid duplicate commits.

### Commit Message Convention

All eval commit messages use the `eval:` prefix, consistent with Conventional Commits style used elsewhere. This makes `ledger-commits.jsonl` rows easy to identify as pipeline checkpoints versus user commits.

---

## D. Clean Design & Maintainability

- Each agent gets exactly one new section or one new paragraph — no restructuring
- `04 Phase - Execute` gets four new in-line commit instructions in the existing loop section
- Commit message format is defined once per agent, not repeated per call site

### Keep-It-Clean Checklist

- [ ] `02 Phase - Refiner` commit instruction added at end of Feature 3's branch-open block — not before
- [ ] `04 Phase - Execute` existing Step D commit replaced by `eval: final-review` (not duplicated)
- [ ] QA-conditional note present for `eval: qa` checkpoint
- [ ] Slug-derivation instruction present for agents 02, 03, 04
- [ ] All 7 files updated (4 master + 3 copies for 01; proportionally for each agent)

---

## E. Completeness: Observability, Security, Operability

**Observability**: Each checkpoint commit fires the post-commit hook (installed by Feature 3), which appends a row to `ledger-commits.jsonl`. The commit message (`eval: implement ...`, `eval: review ...`, etc.) appears as the `message` field in that row — making it parseable by the `05 Eval - Grader`.

**Security**: No credentials involved. All commits are local until the user pushes.

**Operability**: If an agent skips a checkpoint (e.g., implementation fails before commit), the ledger gap is visible when the grader correlates events. No special recovery needed.

---

## F. Test Plan

No automated tests — Markdown agent definition changes.

### MV1 (AC1): Planner checkpoint

Read `.github/agents/01-project-planner.agent.md`. Confirm: commit instruction with `eval: affirm plan` message is present after the user-approval section.

### MV2 (AC2): Refiner checkpoint

Read `.github/agents/02-phase-refiner.agent.md`. Confirm: commit instruction with `eval: affirm phase <slug>` is present, and appears after (not replacing) the branch-open steps added by Feature 3.

### MV3 (AC3): Decomposer checkpoint

Read `.github/agents/03-feature-decomposer.agent.md`. Confirm: commit instruction with `eval: decompose <slug>` is present after the plan-writing section.

### MV4 (AC4, AC5): Execute sub-step commits

Read `.github/agents/04-phase-execute.agent.md`. Confirm: per-feature `implement` and `review` checkpoints appear within the feature development loop, while `qa` and `final-review` are defined as consolidated phase-level checkpoints in Steps 4 and 5. Confirm the staging guidance matches each scope.

### MV5 (AC7): Propagation

Read all six copy files. Confirm the same commit instruction sections are present.

---

## Stage 1: Add checkpoint to `01 Project - Planner`

**Goal**: Add the `eval: affirm plan` commit instruction to the master file.
**Success Criteria**: MV1 passes.
**Status**: Not Started

## Stage 2: Add checkpoint to `02 Phase - Refiner`

**Goal**: Add the `eval: affirm phase <slug>` commit instruction at the end of the branch-open block (which Feature 3 added). Read the file first to locate the exact insertion point.
**Success Criteria**: MV2 passes. Feature 3's branch-open content is intact.
**Status**: Not Started

## Stage 3: Add checkpoint to `03 Feature - Decomposer`

**Goal**: Add the `eval: decompose <slug>` commit instruction after the plan-writing section.
**Success Criteria**: MV3 passes.
**Status**: Not Started

## Stage 4: Add sub-step commits to `04 Phase - Execute`

**Goal**: Add four commit instructions within the feature development loop. Replace the existing Step D end-of-feature commit with `eval: final-review`.
**Success Criteria**: MV4 passes.
**Status**: Not Started

## Stage 5: Propagate to all copy files

**Goal**: Apply identical changes to all six copy files across `opencode/agents/` and `claude/agents/`.
**Success Criteria**: MV5 passes.
**Status**: Not Started
