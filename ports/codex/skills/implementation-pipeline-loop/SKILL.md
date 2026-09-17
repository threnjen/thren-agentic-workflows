---
name: implementation-pipeline-loop
description: "Standard feature development loop used by orchestrators. Defines the Implement → Review → Commit → Mark Complete cycle, including invocation prompts, verification steps, and error handling. Use when: orchestrating the implementation pipeline for tasks or features."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Implementation Pipeline Loop

Orchestrators use this standard development cycle to process tasks through subagents. Each task runs through the full loop before the next task begins.

## Loop Steps

For **each task** (in priority order), run these steps sequentially. Complete all steps for one task before starting the next.

### Step A: Implement

Spawn the **z-feature-implementer** subagent:

> "[SUBAGENT-MODE] Implement the plan at `[plan-path]`. Pipeline: `[pipeline]`. Read that pipeline's planning artifacts, implement all acceptance criteria using Red-Green-Refactor TDD, and write `[plan-path]/[task-name]-implementation.md`. Run these affected suites: [verification-assets, or `not provided`]. Return a summary, test-execution status, results artifact path, and blockers."

After the subagent returns:
- Verify `[plan-path]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers

### Step B: Review

Spawn the **z-reviewer-plan-conformance** subagent:

> "[SUBAGENT-MODE] Review and repair the implementation at `[plan-path]`. Pipeline: `[pipeline]`. Read that pipeline's planning artifacts and the implementation record, then fix what you find. You get one round. Write `[plan-path]/[task-name]-review.md`, and record unresolved defects under `## Unfixed findings`. Run these affected suites: [verification-assets, or `not provided`]. Return the verdict, repairs, unresolved findings, and test-execution status."

The reviewer gets one round. It repairs what it can and records what it cannot. Never spawn the reviewer a second time for the same task. Never open a fix round yourself.

After the subagent returns:
- Verify `[plan-path]/[task-name]-review.md` exists
- Run the affected suites yourself. A reviewer self-report is not evidence
- Apply the Test Execution Gate below, regardless of the verdict.
- Carry every unresolved finding to the caller's final decision.

### Test Execution Gate

Read the test-execution statuses reported by the Implementer and Reviewer. The `test-execution-evidence` instruction defines the statuses.

- **`executed-green`** → Proceed to Step C.
- **`executed-failing`** → Apply the matching pipeline branch.
  - **Phase** — Spawn the Implementer once in `gate-remediation` mode with the exact failure evidence. Never spawn the Reviewer again. Rerun the named failures. If they pass, rerun the full required gate. A failed rerun blocks the feature and its dependents.
  - **Audit or Test** — Spawn the Implementer and Reviewer once again with the failing test names. Record a second failure as blocking.
- **`not-executed`** → Do not treat this as green. Record `test-execution: not-executed (<reason>)` for the task. Report it to the orchestrator as a blocking status. The orchestrator cannot report a task with unrun tests as complete. The direct-supervisor-attestation exception in the Test Execution Evidence instruction applies only when the user-invocable root orchestrator itself receives an explicit supervisor assertion. Subagents still report `not-executed` without an artifact.

Carry the per-task status forward. The orchestrator gates feature and phase completion on that status.

### Step C: Commit

This step defines the pipeline's only commit contract. A caller never defines its own commit
scheme, message format, or staging rule. The caller runs these checkpoints. Execute every commit
directly. Never spawn a subagent for a commit.

The pipeline has four checkpoints. Two checkpoints apply to each unit of work. Two checkpoints
apply once per run.

| Checkpoint | When | Stages |
|---|---|---|
| Implement | After Step A returns, before review starts | The unit's source and test changes |
| Review | After the review and any fix rounds close | The source and test files the fixes touched |
| QA | Once, after the consolidated QA stage runs | The QA documents that stage wrote outside `dev/` |
| Final review | Once, after the final review stage returns | The final review artifacts written outside `dev/` |

A caller with no consolidated QA stage or no final review stage skips that checkpoint. Skipping a
checkpoint does not indicate a missing commit.

**1. Collect files to stage.** For a unit checkpoint, read the "Files Changed" table in
`[plan-path]/[task-name]-implementation.md`. Collect every source and test path listed in that
table. For a run-level checkpoint, collect the artifacts that the stage produced outside `dev/`.

**2. Stage only those files.**

```bash
git add <file1> <file2> ...
```

Do not use `git add -A` — staging untracked files outside the implementation record risks
including debug files or changes from adjacent tasks.

Apply these four staging rules at every checkpoint:

- Never stage anything under `dev/`. Pipeline documents — plan, context, tasks, implementation,
  review, security, and every audit report — are working state, not deliverables.
- Never stage files from another unit's directory. A checkpoint commits one unit's work.
- Never stage untracked run output such as an evidence directory. Output is not a deliverable.
- Never stage an artifact another checkpoint owns. When a stage writes a report that a later
  checkpoint aggregates, that later checkpoint stages it.

**3. Generate a commit message** using conventional commit format. For a unit checkpoint, derive
the type, scope, and summary from the implementation record. For a run-level checkpoint, derive
the type, scope, and summary from the stage's own artifacts:

```
<type>(<scope>): <short summary — 50 chars or fewer, imperative mood>

<one paragraph: what changed and why, derived from implementation record summary>

Implements: <AC refs, e.g., AC1, AC2, AC3>
Reviewed-by: z-reviewer-plan-conformance
Verdict: <Approved | Approved with Reservations>
```

**Type:** `feat` (new capability) · `fix` (bug fix) · `refactor` (restructure) · `test` (tests only) · `docs` (docs only) · `chore` (config/build)

Use `test` or `chore` for a QA checkpoint. Use `docs` for a final review checkpoint. Drop the
`Implements:` and `Verdict:` trailers when the checkpoint commits no code.

**4. Commit.**

```bash
git commit -m "<message>"
```

**5. Verify.**

```bash
git log --oneline -1
```

Confirm that the commit appears. If `git add` staged nothing, log "Nothing to commit". Proceed
afterward. This is not an error. A checkpoint whose only outputs live under `dev/` stages nothing
by design.

### Step D: Mark Complete

Update the todo list to mark this task as completed. Proceed to the next task.

> **Note:** QA placement depends on the pipeline mode. The `pipeline-artifacts` skill defines batch mode and per-feature mode. Load that skill and follow its definition.

## Path Conventions

The orchestrator supplies all three tokens in its spawn prompt.

- `[plan-path]` — the directory containing the task's plan files (phase pipeline: `dev/feature/[0N-task-name]/`; audit and test pipelines supply their own)
- `[task-name]` — the kebab-case identifier for the task, matching the plan file prefix (including the `0N-` numeric prefix for feature directories)
- `[pipeline]` — `phase`, `audit`, or `test`. Shared agents never infer it from files.

Token bindings are owned by the `dev-task-folder` instruction.

## Working Against a Plan

- **A plan's claim about existing code is a hypothesis.** Verify the claim before building to match the plan. Implementing against a false claim manufactures a dependency that never existed. Report the plan's error instead of working around it.
- **Checkpoint-commit steps must stage every artifact they mutate.** Describe resumable scopes as created *or modified*. Keep the checkpoint contract at the same scope as the artifacts it commits.

## Post-Loop: Documentation Update

After the caller completes and reports all tasks to the user, spawn the **Docs Writer** subagent to update documentation that may be stale. A Phase caller applies its own production-verdict gate first.

> "[SUBAGENT-MODE] [Describe what was just completed — include the pipeline type (phase/audit/test), name/scope, and list of completed tasks/features]. Update any stale documentation across the repository. Return a summary of which documents were updated and what changed."

This step is best-effort. If the Docs Writer reports no changes needed, that is expected. Do not block the pipeline on this step.

**Conditional execution:** Run this step only when the implementation pipeline was actually executed, meaning that code changes were made. If the user declined remediation or implementation after the analysis/audit phase, skip this step because no code was changed and no branch was created.
