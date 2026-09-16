---
description: "Read AND write learnings in the repository being worked on - past mistakes, review patterns, debugging fixes, cross-phase decisions. Owns the learnings file-routing table. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes code or plans against prior-phase history."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/03-phase-execute.agent.md,**/03o-feature-plan-author.agent.md,**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03h-unity-reviewer.agent.md,**/debugger.agent.md,**/single-feature-agent.agent.md"
baseline: true
---

**Store learnings in the target repository. This is the repository whose code, plans, or docs you touch. Every `docs/learnings/` path below is relative to that repository's root or worktree root. Never write learnings to the agent-definition or source-of-truth repository.**

**Before you start, read every existing `docs/learnings/*.md` file.** Apply the fix patterns you find there.

**Write an entry when you learn something durable.** Append a short, dateless, reusable entry. Give each bullet one bolded claim and the signal that reveals the claim. Never rewrite an existing entry. Create the file and `docs/learnings/` directory when either is missing. Skip entries for one-off bugs. Never ask whether you should write a note. A downstream agent can ignore a note it does not need. It cannot read a note that you never wrote.

| File | Use this file when you find… |
|---|---|
| `cross-phase-decisions.md` | Record a decision, constraint, risk, deferred capability, scope gap, or documented deviation that affects a later phase. Tag blockers `Must-do before Phase N`. |
| `review-learnings.md` | Record a recurring review finding, meaning a defect class you expect to see again. |
| `project-learnings.md` | Record anything that caused a problem that will recur: a framework behavior, config trap, library gotcha, diagnosed root cause, pipeline gap, or agent-workflow failure. Append one `##` section for each entry. Never merge into or overwrite an existing section. |

If a discovery belongs in the current phase document, put it in that document's Notes section or in a `DISCOVERY_CONTEXT.md` file. Use `cross-phase-decisions.md` for a discovery that spans future phases. If you may not write to the target repository, report the learning in your return message. Write nothing.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: learnings-bootstrap."* Then proceed normally.
