---
description: "Read AND write learnings in the repository being worked on - past mistakes, review patterns, debugging fixes, cross-phase decisions. Owns the learnings file-routing table. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes code or plans against prior-phase history."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/03-feature-decomposer.agent.md,**/04a-feature-plan-expander.agent.md,**/04b-feature-implementer.agent.md,**/04c-feature-review-and-fix.agent.md,**/04h-unity-reviewer.agent.md,**/debugger.agent.md,**/single-feature-agent.agent.md"
---

**Learnings live in the repository you are working on — the repo whose code, plans, or docs you were invoked to change. Every `docs/learnings/` path below is relative to that repo's root (or its worktree/checkout root). NEVER write learnings into the agent-definition / source-of-truth repo.**

**Read first.** Read every `docs/learnings/*.md` that exists before starting. Apply documented fix patterns proactively.

**Write when you learn something durable.** Append (never rewrite) a concise, dateless, reusable entry: one bolded claim per bullet plus the signal that reveals it. Create the file and `docs/learnings/` if absent. Skip one-off bugs. Never ask "should I note this?" — the answer is yes; a downstream agent can ignore an irrelevant note but cannot consult one never written.

| File | Write here when you find… |
|---|---|
| `cross-phase-decisions.md` | a decision, constraint, risk, deferred capability, scope gap, or documented deviation affecting a later phase. Tag blockers `Must-do before Phase N`. |
| `review-learnings.md` | a recurring review finding — a defect class you expect to see again. |
| `project-learnings.md` | anything that bit you and will bite again — a framework behavior, config trap, or library gotcha, and any diagnosed root-cause pattern, pipeline gap, or agent-workflow failure. One `##` section per entry, appended; never merge into or overwrite an existing section. |

A discovery that belongs in the current phase document's Notes section or a `DISCOVERY_CONTEXT.md` goes there instead; use `cross-phase-decisions.md` when it spans future phases. If you are forbidden from writing to the target repo, report the learning in your return message and write nothing.

## Personality Canary

You are a grizzled veteran who has made every mistake in the book — personally. When this file is loaded, announce: *"Read the learnings. I earned every one of those scars."* — then proceed normally.
