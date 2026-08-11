# Discovery Context

Context gathered during project planning that is not derivable from the codebase alone. Read by
Phase - Refiner and Feature - Decomposer so the user does not have to re-supply it.

## Source of the Roadmap

The three phases originate from maintainer-reported friction, not from a code review. Each carries
a stated problem the maintainer experienced directly.

## Phase 01 — Reported Symptoms and Diagnosis

**Reported symptoms.** Agent-driven Unity testing behaves inconsistently: sometimes an agent opens
Unity Hub and runs tests itself, taking over the maintainer's mouse and making the machine unusable;
other times an agent refuses to run tests at all and asks the maintainer to run them by hand. The
maintainer's stated hypothesis was that Unity cannot generate `.meta` files unless the Editor is
opened by a human.

**Diagnosis reached during planning — the hypothesis is incorrect, and both symptoms are corpus
rules, not Unity limitations.**

1. **`.meta` files do not require a human-opened Editor.** A headless import
   (`Unity -batchmode -quit -projectPath <path> -logFile -`) imports the full asset database and
   writes every missing `.meta`. There is no GUI requirement.
2. **The mouse-hijack symptom is caused by `source_of_truth/skills/unity-development/SKILL.md`
   line 177**, which currently reads: *"`-batchmode` is optional. Omit it to run against the Editor
   UI; add it for headless runs."* Agents read "optional," omit it, and the Editor GUI launches.
3. **The refusal symptom is caused by the same file, line 181** — the Editor-lock rule instructs the
   agent to report `not-executed: editor lock` and ask the user whenever `Temp/UnityLockfile` exists
   or the Editor is open on the project.
4. **The correct fix for the lock is a second checkout, not closing the Editor.** Two Unity
   processes operating on two separate directories do not contend. A persistent shadow worktree with
   its own retained `Library/` cache lets the CLI run proceed while the maintainer's Editor stays
   open.

**Known cold-start constraint.** A freshly created Unity worktree has no `Library/` folder, so its
first headless run performs a full asset import — minutes, not seconds, on a real project. The
shadow worktree must therefore be **persistent and reused**, refreshed by checkout rather than
recreated per run. Any design that creates a throwaway worktree per test run reintroduces the delay
it was meant to remove.

## Decisions Made During Planning

Recorded as time-stamped intent. Verify against what shipped before relying on any of these.

| Decision | Choice | Rationale |
|---|---|---|
| Phase 01 delivery surface | Corpus rules plus copyable reference assets only | This repository contains no Unity project. Wiring CI into a real Unity repo would make the phase span two repositories and block on Unity license setup. |
| Unity test runner strategy | Local persistent shadow worktree first; CI deferred | Works today with no Unity license secret, no Docker images, and no runner maintenance. Removes the maintainer from the loop immediately. GameCI on GitHub-hosted runners remains a later, separate decision. |
| Phase 02 final-check enforcement | Advisory and opt-in. The refiner offers it; nothing blocks | **Supersedes an earlier decision in this table that made it a blocking gate on High-or-above rubric findings.** The maintainer clarified the intent: this is a scoped last look for anything the user and agent missed, not an adversarial gate. There is no rubric, no severity threshold, and no verdict. |
| Phase 02 final-check retry budget | None — one pass, no recheck | **Supersedes an earlier one-revise-and-recheck decision.** With nothing blocking, there is nothing to re-clear. Findings are reported once and the user chooses what to apply. |
| Phase 02 findings handling | Report verbatim, then offer to fold accepted findings into the document | Report-only was considered and rejected. A check that surfaces a real gap and then leaves the user to fix it by hand at the end of a long session gets skipped after a few uses — and a skipped check is worse than none, because it still appears to exist. |
| Phase 02 binding point | End of Phase - Refiner only, after the document is written and before the working branch opens | Scoped by maintainer directive. Project - Planner is deferred, not rejected — see `docs/learnings/cross-phase-decisions.md`. |
| Audit bookend scope | Touched modules plus their dependents, derived from the phase execution manifest | Two full-codebase audits per phase plus a delta was judged too slow and expensive, and most of each report would be unchanged noise the delta must reconcile. Full-codebase remains an explicit opt-in. |
| Audit bookend exclusions | Tests and documentation excluded from both audits, always | Maintainer directive, for speed and cost. |
| Audit type selection | Code audit always; infra audit only when the manifest touches CI, Docker, IaC, or build config | Stated as an assumption during planning and accepted without objection. |
| Drift remediation policy | Auto-fix High-or-above drift attributed to the phase, then re-run the end audit once; report everything else | Bounded cost. Auto-fixing every severity risks a long tail of Low findings ballooning the phase through repeated re-audits. |
| Manifest role in the audits | Read input for both the start and end audit, supplying scope **and** intent | The execution manifest exists before any feature is implemented, which makes it a clean statement of what the phase intends to change, uncontaminated by what was actually built. |

## Standing Constraint on the Manifest-as-Intent Design

The manifest is supplied to the auditors **for scope and intent only. Stated intent never excuses a
finding.** An auditor told what a phase meant to do will otherwise rationalize real findings away as
"intended." This constraint must survive into the spawn prompt itself, not live only in the phase
document.

## Context Not Gathered

- No external URLs, specifications, or design documents were supplied.
- No web research was performed. The Unity CLI behavior above is asserted from working knowledge and
  should be verified empirically during Phase 01 execution against the actual Unity version in use.
- No additional repositories or monorepo packages were referenced. All three phases are
  single-repository work inside `github-agents-source-of-truth`.
