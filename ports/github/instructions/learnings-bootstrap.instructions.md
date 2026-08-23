---
description: "Read AND write learnings in the repository being worked on - past mistakes, review patterns, debugging fixes, cross-phase decisions. Owns the learnings file-routing table. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes code or plans against prior-phase history."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/03-phase-execute.agent.md,**/03a-feature-plan-expander.agent.md,**/03b-feature-implementer.agent.md,**/03c-feature-review-and-fix.agent.md,**/03h-unity-reviewer.agent.md,**/debugger.agent.md,**/single-feature-agent.agent.md"
baseline: true
---

**Learnings live in the repository you were invoked to change — the repo whose code, plans, or docs you are touching. Every `docs/learnings/` path below is relative to that repo's root or worktree root. Never write learnings into the agent-definition or source-of-truth repo.**

**Read first.** Read every `docs/learnings/*.md` that exists before you start. Apply the fix patterns you find there.

**Write when you learn something durable.** Append a short, dateless, reusable entry — one bolded claim per bullet plus the signal that reveals it. Never rewrite an existing entry. Create the file and `docs/learnings/` when they are missing. Skip one-off bugs. Never ask whether to write a note. A downstream agent can ignore a note it does not need, but cannot read one you never wrote.

| File | Write here when you find… |
|---|---|
| `cross-phase-decisions.md` | a decision, constraint, risk, deferred capability, scope gap, or documented deviation that affects a later phase. Tag blockers `Must-do before Phase N`. |
| `review-learnings.md` | a recurring review finding — a defect class you expect to see again. |
| `project-learnings.md` | anything that bit you and will bite again: a framework behavior, config trap, library gotcha, diagnosed root cause, pipeline gap, or agent-workflow failure. One `##` section per entry, appended. Never merge into or overwrite an existing section. |

Put a discovery in the current phase document's Notes section or in a `DISCOVERY_CONTEXT.md` when it belongs there instead. Use `cross-phase-decisions.md` when it spans future phases. If you may not write to the target repo, report the learning in your return message and write nothing.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: learnings-bootstrap."* Then proceed normally.
