---
name: implementation-pipeline-loop
description: "Standard feature development loop used by orchestrators. Defines the Implement → Review → Commit → Mark Complete cycle, including invocation prompts, verification steps, and error handling. Use when: orchestrating the implementation pipeline for tasks or features."
---

# Implementation Pipeline Loop

The standard development cycle used by orchestrators to process tasks through subagents. Each task runs through the full loop before the next task begins.

## Loop Steps

For **each task** (in priority order), run these steps sequentially. Complete ALL steps for one task before starting the next.

### Step A: Implement

spawn the **z-feature-implementer** subagent:

> "[SUBAGENT-MODE] Implement the plan at `[plan-path]`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `[plan-path]/[task-name]-implementation.md`. Manifest verification assets — run these affected suites if the change touches a shared contract: [verification-assets, or `not provided`]. Return a summary of what was implemented, the test-execution status with its results artifact path, and any gaps or blockers."

After the subagent returns:
- Verify `[plan-path]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers

### Step B: Review

spawn the **z-reviewer-plan-conformance** subagent:

> "[SUBAGENT-MODE] Review and repair the implementation at `[plan-path]`. Read the plan files and implementation record, review all changed code, then fix what you find. You get one round. Write the review record to `[plan-path]/[task-name]-review.md`, and write any defect you could not fix into the implementation record under `## Unfixed findings`. Manifest verification assets — run these affected suites if the change touches a shared contract: [verification-assets, or `not provided`]. Return the verdict, what you repaired, what you left unfixed, and the test-execution status with its results artifact path."

The reviewer gets one round. It repairs what it can and records what it cannot. Never spawn it a second time for the same task, and never open a fix round of your own.

After the subagent returns:
- Verify `[plan-path]/[task-name]-review.md` exists
- Run the affected suites yourself. A reviewer self-report is not evidence
- Apply the Test Execution Gate below whatever the verdict. An unfixed finding is recorded, not blocking — the phase-close review sees the same code again

### Test Execution Gate

Read the Implementer's and Reviewer's reported test-execution status. Statuses are defined in the `test-execution-evidence` instruction.

- **`executed-green`** → proceed to Step C.
- **`executed-failing`** → re-spawn the Implementer with the failing test names, then re-spawn the Reviewer. Retry once. If still failing, record it as a blocking status and proceed — the final review surfaces it.
- **`not-executed`** → do NOT treat this as green. Record `test-execution: not-executed (<reason>)` for the task and report it to the orchestrator as a blocking status. A task with unrun tests cannot be reported complete. The direct-supervisor-attestation exception in the Test Execution Evidence instruction applies only when the user-invocable root orchestrator itself receives an explicit supervisor assertion; subagents still report `not-executed` without an artifact.

Carry the per-task status forward: the orchestrator gates feature and phase completion on it.

### Step C: Commit

This step is the only commit contract in the pipeline. A caller never defines its own commit
scheme, message format, or staging rule — it runs these checkpoints. Execute every commit
directly. Never spawn a subagent for a commit.

Four checkpoints exist. Two land per unit of work, two land once per run.

| Checkpoint | When | Stages |
|---|---|---|
| Implement | After Step A returns, before review starts | The unit's source and test changes |
| Review | After the review and any fix rounds close | The source and test files the fixes touched |
| QA | Once, after the consolidated QA stage runs | The QA documents that stage wrote outside `dev/` |
| Final review | Once, after the final review stage returns | The final review artifacts written outside `dev/` |

A caller with no consolidated QA stage or no final review stage skips that checkpoint. Skipping
one is not a missing commit.

**1. Collect files to stage.** For a unit checkpoint, read the "Files Changed" table in
`[plan-path]/[task-name]-implementation.md` and collect every source and test path it lists. For a
run-level checkpoint, collect the artifacts that stage produced outside `dev/`.

**2. Stage only those files.**

```bash
git add <file1> <file2> ...
```

Do NOT use `git add -A` — staging untracked files outside the implementation record risks
including debug files or changes from adjacent tasks.

Four staging rules hold at every checkpoint:

- Never stage anything under `dev/`. Pipeline documents — plan, context, tasks, implementation,
  review, security, and every audit report — are working state, not deliverables.
- Never stage files from another unit's directory. A checkpoint commits one unit's work.
- Never stage untracked run output such as an evidence directory. Output is not a deliverable.
- Never stage an artifact another checkpoint owns. When a stage writes a report that a later
  checkpoint aggregates, that later checkpoint stages it.

**3. Generate a commit message** using conventional commit format. Derive type, scope, and summary
from the implementation record for a unit checkpoint, or from the stage's own artifacts for a
run-level one:

```
<type>(<scope>): <short summary — 50 chars or fewer, imperative mood>

<one paragraph: what changed and why, derived from implementation record summary>

Implements: <AC refs, e.g., AC1, AC2, AC3>
Reviewed-by: z-reviewer-plan-conformance
Verdict: <Approved | Approved with Reservations>
```

**Type:** `feat` (new capability) · `fix` (bug fix) · `refactor` (restructure) · `test` (tests only) · `docs` (docs only) · `chore` (config/build)

Use `test` or `chore` for a QA checkpoint and `docs` for a final review checkpoint, and drop the
`Implements:` and `Verdict:` trailers when the checkpoint commits no code.

**4. Commit.**

```bash
git commit -m "<message>"
```

**5. Verify.**

```bash
git log --oneline -1
```

Confirm the commit appears. If `git add` staged nothing, log "Nothing to commit" and proceed —
this is not an error. A checkpoint whose only outputs live under `dev/` stages nothing by design.

### Step D: Mark Complete

Update the todo list to mark this task as completed. Proceed to the next task.

> **Note:** QA placement depends on the pipeline mode. Batch mode and per-feature mode are defined in the `pipeline-artifacts` skill; load it and follow that definition.

## Path Conventions

The orchestrator supplies both tokens in its spawn prompt.

- `[plan-path]` — the directory containing the task's plan files (phase pipeline: `dev/feature/[0N-task-name]/`; audit and test pipelines supply their own)
- `[task-name]` — the kebab-case identifier for the task, matching the plan file prefix (including the `0N-` numeric prefix for feature directories)

Token bindings are owned by the `dev-task-folder` instruction.

## Working Against a Plan

- **A plan's claim about existing code is a hypothesis.** Verify it before building to match — implementing to satisfy a false claim manufactures a dependency that never existed. Reporting the plan's error is the correct move, not working around it.
- **Checkpoint-commit steps must stage every artifact they mutate**, and resumable scopes are described as created *or modified*. Keep the checkpoint contract at the same scope as the artifacts it commits.

## Post-Loop: Documentation Update

After all tasks are complete and reported to the user, spawn the **Docs Writer** subagent to update any documentation that may be stale:

> "[SUBAGENT-MODE] [Describe what was just completed — include the pipeline type (phase/audit/test), name/scope, and list of completed tasks/features]. Update any stale documentation across the repository. Return a summary of which documents were updated and what changed."

This step is best-effort. If the Docs Writer reports no changes needed, that is expected. Do not block the pipeline on this step.

**Conditional execution:** This step only runs when the implementation pipeline was actually executed (i.e., code changes were made). If the user declined remediation or implementation after the analysis/audit phase, skip this step — no code was changed, and no branch was created.
