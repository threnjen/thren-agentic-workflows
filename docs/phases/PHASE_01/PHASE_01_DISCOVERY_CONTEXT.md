# Phase 01 — Discovery Context

Context gathered during phase refinement that is not derivable from this repository alone. Read by
Feature - Decomposer. Extends `docs/phases/DISCOVERY_CONTEXT.md`, which holds the project-level
diagnosis; nothing here repeats it.

## Reference Unity Project

This repository contains no Unity project. All empirical verification for this phase happens against
a single external project supplied by the maintainer.

| Fact | Value |
|---|---|
| Path | `/Users/jennywadkins/github_repos/the-movies` |
| Unity version | `6000.3.13f1` (`ProjectSettings/ProjectVersion.txt`) |
| EditMode tests | `Assets/Tests/Editor` |
| PlayMode tests | `Assets/Tests/PlayMode` |
| Shared test code | `Assets/Tests/Shared` |
| Total size on disk | 602 MB |
| `Library/` size | 309 MB |
| `Library/` tracked? | No — gitignored at `.gitignore:60` (`[Ll]ibrary/*`) |
| State when inspected | Clean working tree, on `main`, no `Temp/UnityLockfile` |

**Observed worktree accumulation.** `git worktree list` on that project reported four stale detached
worktrees under agent scratchpad directories, all marked prunable, left behind by earlier agent runs.
This is why `git worktree prune` is part of the procedure rather than an optional nicety.

**Test path discrepancy.** The `unity-development` skill's Refactor / Rewire Test Preservation Rules
section names `Assets/Tests/EditMode`. That directory does not exist in the reference project, which
uses `Assets/Tests/Editor`. Folded into this phase's scope as a correction.

## Maintainer Decisions Made During Refinement

| Decision | Choice | Rationale |
|---|---|---|
| Testing uncommitted work | Commit before every test run | A worktree can only test committed code. Rejected alternatives: mirroring the working tree with `rsync` (abandons git semantics, risks stale-file bugs) and a detached worktree with the constraint merely documented rather than automated. In practice the Feature - Implementer's existing per-feature commits cover most runs. |
| Unity license | Unity Personal | Single-seat activation. Whether it permits a second concurrent Unity process on one machine is unverified and is the phase's primary open risk. |
| Editor-lock handling | Agent may ask the user to close the Editor | The refusal rule is demoted to rung 2 of a ladder, not deleted. The agent still runs the tests itself after the Editor closes; it never hands the run back to the user. |
| Reference asset placement | Split | GameCI workflow template to `source_of_truth/skills/unity-development/references/` (propagates with the skill bundle); runbook to `docs/unity/` (human-facing, not propagated). Keeping both in the skill bundle would copy a human-facing runbook into five harness directories. |
| Worktree creation | On first need, announced | The agent creates it when a Unity test run needs it and reports the path, the ~600 MB cost, and the multi-minute first import. Rejected: silent creation (surprises the maintainer with 600 MB), and manual pre-creation (the first run after this phase ships would still interrupt the maintainer). |
| Worktree lifetime | Permanent, one per Unity project | Cold-start import costs minutes, so teardown would defeat the purpose. Teardown is a documented manual command only. |
| Test results location | Absolute path in the main checkout | The run happens in the worktree, so a relative `dev/test-results/` would write to the worktree's copy while the agent reads the main checkout's. Rejected: reading results back out of the worktree, which makes the worktree an input as well as an execution target. |
| Worktree path convention | `<project-dir>-agent-tests/`, sibling, one per project | A fixed name is what makes "already exists" detectable. The four observed stale worktrees are what an unnamed convention produces. |
| Unity binary location | Reuse `04g-unity-visual-verification`'s editor discovery | A bare `Unity` on `PATH` fails on machines with multiple Editor versions, which is the normal Unity setup. Rejected: a second discovery implementation in the skill. |
| Rung 2 with no user present | Non-response treated as a decline | An unattended agent must not hang, and must not escalate to a GUI. Reports `not-executed: editor open, user unavailable`. |

## Corpus Facts Established by Inspection

- `scripts/propagate_master_assets.py` transforms only `source_of_truth/{agents,skills,instructions,hooks}`.
  There is no general asset directory, which is why Deliverable 5's two files needed homes chosen
  from what already propagates.
- Skill directories propagate **all** bundled files, not just `SKILL.md` (`rglob` over the skill
  directory, skipping `SKILL.md` which is transformed separately). `unity-review-knowledge/references/`
  is the existing precedent.
- The defect lines cited in the phase summary were verified present as described:
  `SKILL.md` line 177 (`-batchmode` is optional) and line 181 (Editor-lock refusal).

## Context Not Gathered

- **No web research was performed.** The Unity CLI claims — headless `.meta` generation, and whether
  two Unity processes can coexist under a Personal license — remain asserted from working knowledge.
  Both must be verified against the reference project during execution before the rules are
  finalized.
- No external URLs, specifications, or design documents were supplied.
- No repositories beyond this one and the reference Unity project were referenced.
