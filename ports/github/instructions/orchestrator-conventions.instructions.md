---
description: "Shared conventions for orchestrator agents that coordinate subagent pipelines, including the end-of-run graph rebuild (merged from graph-rebuild-hook). Audience is ENUMERATED deliberately - the four pipeline orchestrators are an arbitrary subset with no filename family. Add any new agent that coordinates a subagent pipeline, and inline this file into its claude/agents/ counterpart."
applyTo: "**/auditor.agent.md,**/delta-auditor.agent.md,**/04-phase-execute.agent.md,**/test-orchestrator.agent.md"
---

# Orchestrator Conventions

Orchestrators coordinate subagents. They do not do the work themselves. These conventions apply to every orchestrator agent.

## Constraints

- Do not write source code, test files, or configuration.
- Do not write plan documents, review records, or QA plans. Delegate them to subagents.
- Always ask the user before you start the fix or remediation phase.

## Working Branch

Create a dedicated git branch for the run before you modify any file, so the changes stay off the default branch.

- Prefix by type: `phase/<name>`, `audit/<type>-<name>`, `test/<operation>-<name>`.
- Use kebab-case, derived from the task, phase, or audit name.
- Run `git checkout -b <branch-name>`.
- **If the branch already exists, resume it with `git checkout <branch-name>`.** An existing branch means an upstream agent opened it for this work — the Phase Refiner commits planning docs onto `phase/<slug>` before handing off. Never create a variant name such as `-2`. That splits planning documents and implementation commits across two branches.
- If the checkout fails for any other reason, such as uncommitted changes, report the error to the user and **stop**. Do not run the pipeline until the user resolves it.

## Progress Tracking

Track progress with the todo tool. Create an entry per task or feature before you start it, mark it in-progress when you start, and mark it complete as soon as it finishes.

## Subagent Output Verification

Verify that a subagent's output exists on disk before you move to the next step. When the file is missing, re-spawn the subagent once with an explicit reminder of the expected output path. If it is still missing, report the failure to the user and stop.

## Pipeline Discipline

- Do not skip or reorder steps. The sequence matters.
- Do not move past a subagent failure without attempting remediation.
- Finish every step for one task or feature before you start the next.

## Review Reject Loop

This is the complete rule. Other documents reference it rather than restate it.

On a "Changes Requested" verdict, re-spawn the Implementer with the review findings, then re-spawn the Reviewer. **Retry once.** If the second review is also "Changes Requested":

1. Log both review summaries.
2. Continue to the next pipeline step. The final review, where one exists, will surface what is unresolved.
3. Note the unresolved review in the final report to the user.

## Pipeline Completion Report

Present results in this structure after the final review subagent returns. Adapt the field labels to your domain (Phase/Audit/Operation, Features/Tasks).

**If GO or GO WITH CONDITIONS:**

> **[Pipeline type] complete.**
>
> **[Scope label]:** [name]
> **[Items label] completed:** [count]
> **Final verdict:** [GO / GO WITH CONDITIONS]
>
> | [Item] | Impl | Review |
> |--------|------|--------|
> | [item-1] | Done | Approved |
>
> **Graph rebuild:** [OK, or the non-zero exit and its error]
>
> **Next step:** Push the branch and open a PR for review.
>
> [If GO WITH CONDITIONS: list the conditions]

**If NO-GO:** report the blocking items from the Final Review and recommend specific remediation. Do not retry automatically. The user reviews the NO-GO findings and decides.

## Graph Rebuild Hook

Run this once through the `execute` tool, without asking for confirmation, immediately after you print the user-facing completion report — including an aborted, partial, or NO-GO run:

```
code-review-graph build
```

Exactly once per run, after the report. Never before it, never a second time.

**On a non-zero exit,** record it in the report's `Graph rebuild` field and continue. Do not fail the pipeline and do not re-run any step. The rebuild is a best-effort index update.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: orchestrator-conventions."* Then proceed normally. Also state *"Graph rebuild queued."* when you queue a graph rebuild.
