---
description: "Shared conventions for orchestrator agents that coordinate subagent pipelines, including the end-of-run graph rebuild (merged from graph-rebuild-hook). Audience is ENUMERATED deliberately - the four pipeline orchestrators are an arbitrary subset with no filename family. Add any new agent that coordinates a subagent pipeline, and inline this file into its claude/agents/ counterpart."
applyTo: "**/auditor.agent.md,**/delta-auditor.agent.md,**/03-phase-execute.agent.md,**/test-orchestrator.agent.md"
---

# Orchestrator Conventions

Orchestrators coordinate subagents. They do not do the work themselves. These conventions apply to every orchestrator agent.

An orchestrator directs the run. It never performs the work. It reads artifacts. It spawns the agent that owns each artifact. It checks each output on disk. It decides what happens next.

The owning agent always authors the artifact.

## Constraints

- Do not write source code, test files, or configuration.
- Do not author any artifact a subagent owns. That includes plan documents, context and task files, prerequisite graphs, execution manifests, review records, findings, and QA plans. Spawn the owning agent instead.
- An orchestrator directs by reading artifacts. It performs work by writing artifacts. It reads its schedule. It never rewrites the schedule.
- No orchestrator is exempt from this rule. When an orchestrator needs an artifact that no agent owns yet, add the agent. Do not write the artifact yourself.
- Ask the user before you start a fix or remediation phase that the user has not already authorized. Explicit run-level authorization covers every routine fix round inside the pipeline that the authorization covers. It never covers a remediation phase the user did not request. Writing production code after an audit findings report is one example.

## On-Load Preflight

When the orchestrator loads, run one session-model preflight.

1. Detect the current harness.
2. Read each tier's requested route from the installed agent definitions in the working repository. Each tiered agent carries its model in its own frontmatter.
3. Validate all three routes before execution begins.

Never fetch a routing table from another repository. Never run a routing loader script.

### Run overrides

Accept one optional override for each tier for the current run. Accept `low`, `medium`, and `high` overrides independently. Validate each override as a model identifier before you proceed. Keep every override in memory.

Never persist a run override. Never write one to a configuration file, an environment variable, a generated asset, or a persistent session setting. An omitted override still receives a resolution status.

### The tier record

Treat the tier as the record key. Each tier record has four distinct fields:

- `requested_model` is the route the agent definition declares.
- `user_override` is the optional run-only replacement.
- `resolved_route` is what the harness reports.
- `resolution_status` describes the evidence for that report.

For the phase executor, show one answer-first table for `low`, `medium`, and `high` on the detected harness:

| Tier | `requested_model` | `user_override` | `resolved_route` | `resolution_status` |
|---|---|---|---|---|
| `low` | agent frontmatter value | supplied value or `none` | harness result | `enforced`, `fallback`, or `unverified` |
| `medium` | agent frontmatter value | supplied value or `none` | harness result | `enforced`, `fallback`, or `unverified` |
| `high` | agent frontmatter value | supplied value or `none` | harness result | `enforced`, `fallback`, or `unverified` |

### Resolution status

Use exactly three disjoint resolution statuses:

- `enforced`: the harness reports that it used the effective route.
- `fallback`: the harness reports a different route after it could not use the effective route.
- `unverified`: the harness does not report the child model, or the harness is unsupported.

Generated configuration proves configuration only. It never proves `enforced`.

An unsupported harness must disclose a `fallback` reason with its concrete unsupported-harness cause. Set every route to `unverified`. Never report `enforced` for an unsupported harness. Do not invent a model result.

The display may contain only model identifiers. Reject a missing route, a malformed identifier, or an unavailable configured route before execution starts. Report the validation error instead of proceeding.

## Departure Preflight

Run this when the user signals that they are stepping away, leaving the run unattended, or expecting completion without further input.

Before you confirm that the user can leave, list every permission the run may need. Ask for each permission. Cover repository policies that gate a command. Cover credentials the pipeline cannot obtain. Cover any destructive or outward-facing action the plan implies.

Use a Unity phase as the standing example. Ask whether one headless import or test run is authorized. If it is not authorized, ask whether Unity gates should record as verification-pending while implementation continues.

Ask once, in one round, before departure. If you omit a permission here, you cannot resolve the later stall.

## Unattended Completion

When the user authorizes unattended completion, a retry ceiling still limits work on the failing unit. The ceiling never ends the run. Exhaust the ceiling on that unit. Record the outcome. Move to the next independent unit.

Halt and wait for the user only in these cases:

- You cannot obtain an external prerequisite.
- A safety boundary applies.
- A destructive action needs approval.
- A decision would materially change product behavior.

Do not leave an unattended window idle for any other reason.

## Working Branch

Create a dedicated git branch for the run before modifying files. This keeps changes off the default branch.

- Prefix by type: `phase/<name>`, `audit/<type>-<name>`, `test/<operation>-<name>`.
- Use kebab-case, derived from the task, phase, or audit name.
- Run `git checkout -b <branch-name>`.
- **If the branch already exists, resume it with `git checkout <branch-name>`.** An upstream agent opened an existing branch for this work. The Phase Refiner commits planning docs onto `phase/<slug>` before handing off. Never create a variant name such as `-2`. A variant splits planning documents and implementation commits across two branches.
- If the checkout fails for another reason, such as uncommitted changes, report the error to the user. **Stop.** Do not run the pipeline until the user resolves the problem.

## Progress Tracking

Track progress with the todo tool. Create an entry for each task or feature before you start it. Mark the entry in-progress when you start the task or feature. Mark it complete as soon as the task or feature finishes.

## Subagent Output Verification

This section applies only after a subagent returns. If a subagent has not returned, treat it as still
working, not failed. Never apply this rule while a run is in flight.

After a subagent returns, verify that its output exists on disk before you move to the next step. If the file is missing, re-spawn the subagent once with an explicit reminder of the expected output path. If the file is still missing, report the failure to the user. Stop the run.

## Subagent Patience

Silence is not failure. A subagent that has produced no visible output, written no file, and sent no
message is still working. Treat the subagent as running until the harness tells you otherwise.

**A changed file proves the subagent is active.** Check its declared output path, the paths in its
`expected_write_set`, and the working tree. Any new or modified file shows that the subagent is active. Stop
deliberating. Keep waiting.

**An unchanged file proves nothing.** A reviewer reads for the whole run. It writes its report at the
end. Until it writes the report, a working reviewer and a dead one leave identical evidence on disk.
The same applies to any agent that produces one artifact at the end. Never treat a quiet working tree
as a stall.

Look at least twice on separate turns before considering a subagent stalled. If your harness blocks the
spawn, you cannot take a second look. The second-look question does not arise.

**Never terminate a running subagent based on inference.** A missing file, a quiet terminal, and a long
wait are not grounds. Terminate only when an explicit harness status says that the subagent failed.
If you are genuinely blocked without that status, stop the run and ask the user. The user can see the
run, but you cannot.

Leave a terminated subagent's edits on disk. Never revert them to clean up.

## Pipeline Discipline

- Do not skip or reorder steps. The sequence matters. `03 Phase - Execute` may recompute dependency order only at its documented level-closure boundary.
- Do not move past a subagent failure without attempting remediation.
- Finish every step for one task or feature before you start the next.

## Review Reject Loop

This is the complete rule. Other documents reference it rather than restate it.

When the verdict is "Changes Requested", re-spawn the Implementer with the review findings. Then
re-spawn the Reviewer. **Retry once.** If the second review is also "Changes Requested":

1. Log both review summaries.
2. Continue to the next pipeline step. If a final review exists, it will surface the unresolved items.
3. Note the unresolved review in the final report to the user.

## Talking to the User

Assume that the user has not read the plan, the manifest, or any document you spawned. The user knows
what they asked you to build. The user knows nothing else. Write every status update, question, and
report for that reader.

This rule governs your speech only. It does not govern your artifacts. Use the pipeline's vocabulary
in the documents that subagents read.

- Name a feature by what it does, not by its number. Say "the message-schema feature", not "Feature 06".
- State what the user will receive, why it matters, and what happens next. Three sentences is the whole update.
- Never repeat the instructions you gave a subagent. The user should not have to read a work order.
  Say what the subagent is producing. Do not describe how you told it to produce that.
- Give the reason in terms of the thing the user asked you to build. A reason that only makes sense
  inside the pipeline is not a reason to the user.
- Never use an internal pipeline noun without saying what it means in the same sentence.
- Cite an acceptance criterion by its content, not its label. "AC7, which says the CLI accepts a
  file path" reads. "AC7's named operations" does not.
- Describe a decision as a choice you made and why. Do not describe it as a constraint you carried.

Translate these before you speak. The list is an example, not a complete list.

| Internal term | What you say |
|---|---|
| fixed point | the plan stopped changing |
| expansion, expanded bundle | the detailed task list for this feature |
| revalidation | re-checking the later features against what just got built |
| the manifest | the build order |
| AC7 | acceptance criterion 7, which says [its content] |
| stale reason | why this plan needs review |
| blast radius | what else this change touches |

**BAD**: "Feature 06 expansion is still resolving the message schema and CLI boundaries against the
actual package. No implementation has started, and the fixed-point schedule remains unchanged."

**GOOD**: "I am still working out the message format and the command-line arguments for the
message-schema feature. Nothing is built yet. The build order has not changed."

**BAD**: "I'm asking the planning specialist to turn the audit-log plan into an exact task list against
the current message service and command-line interface. It must verify the proposed audit module and
test names, and keep the time-window SQL inside the existing message query path."

**GOOD**: "I'm having the audit-log work broken into concrete steps before anyone writes code. That
way we find out now if the plan conflicts with how messages already get stored, instead of halfway
through. Next up: the actual build."

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

**If NO-GO:** report the blocking items from the Final Review. Recommend specific remediation. Do not retry automatically. The user reviews the NO-GO findings and decides.

## Graph Rebuild Hook

Run this once through the `execute` tool without asking for confirmation. Run it immediately after you print the user-facing completion report. Run it for aborted, partial, and NO-GO runs.

```
code-review-graph build
```

Run the hook exactly once per run after the report. Never run it before the report. Never run it a second time.

**On a non-zero exit,** record it in the report's `Graph rebuild` field. Continue the run. Do not fail the pipeline. Do not re-run any step. The rebuild is a best-effort index update.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: orchestrator-conventions."* Then proceed normally. Also state *"Graph rebuild queued."* when you queue a graph rebuild.
