---
description: "Read AND write learnings in the repository being worked on - past mistakes, review patterns, debugging fixes, cross-phase decisions. Owns the learnings file-routing table. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes code or plans against prior-phase history."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/03-phase-execute.agent.md,**/03o-feature-plan-author.agent.md,**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03h-unity-reviewer.agent.md,**/debugger.agent.md,**/single-feature-agent.agent.md"
baseline: true
---

**Store learnings in the target repository. This is the repository whose code, plans, or docs you touch. Every `docs/learnings/` path below is relative to that repository's root or worktree root. Never write learnings to the agent-definition or source-of-truth repository.**

**Before you start, read the learnings files for your role.** Apply the fix patterns you find there. Skip a file that does not exist.

| Your role | Read |
|---|---|
| Planner, phase refiner, plan author, orchestrator | `cross-phase-decisions.md` |
| Implementer, single-feature agent | `project-learnings.md`, `cross-phase-decisions.md` |
| Reviewer | `review-learnings.md`, `cross-phase-decisions.md` |
| Debugger | `debugging-learnings.md`, `project-learnings.md` |

Read another learnings file only when your task touches its subject.

**Write an entry when you learn something durable.** Append a short, dateless, reusable entry. Give each bullet one bolded claim and the signal that reveals the claim.

**Learnings files describe what is true now, not what changed.** Rewrite an entry that is wrong. Never annotate it, strike it through, or append a correction beside it. Delete a `cross-phase-decisions.md` entry when the phase it binds has shipped and code or tests enforce the rule. Create the file and `docs/learnings/` directory when either is missing. Skip entries for one-off bugs. Never ask whether you should write a note. A downstream agent can ignore a note it does not need. It cannot read a note that you never wrote.

| File | Use this file when you find… |
|---|---|
| `cross-phase-decisions.md` | Record an obligation or guard that a later phase must honor: a constraint, risk, deferred capability, or scope gap. Write one bolded rule and one `Signal:` line that names the defect pattern. Use three sentences at most. Tag blockers `Must-do before Phase N`. |
| `docs/phases/project_notes/<system>_design_notes.md` | Record design rationale, a system model, or anything longer than three sentences. Add a guard in `cross-phase-decisions.md` that points at the notes file when a later phase must honor it. |
| `review-learnings.md` | Record a recurring review finding, meaning a defect class you expect to see again. |
| `project-learnings.md` | Record anything that caused a problem that will recur: a framework behavior, config trap, library gotcha, diagnosed root cause, pipeline gap, or agent-workflow failure. Append one `##` section for each entry. Never merge a new diagnosis into an existing section. |
| `debugging-learnings.md` | Record a diagnostic technique or a misleading symptom that cost time and will recur. |

If a discovery belongs in the current phase document, put it in that document's Notes section or in a `DISCOVERY_CONTEXT.md` file. Use `cross-phase-decisions.md` for a discovery that spans future phases. If you may not write to the target repository, report the learning in your return message. Write nothing.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: learnings-bootstrap."* Then proceed normally.
