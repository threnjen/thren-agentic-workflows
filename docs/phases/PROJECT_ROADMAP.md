# Project Roadmap: Agent Pipeline Hardening

## Vision

Three independent weaknesses in the agent corpus, closed one at a time: Unity tests that run
themselves without hijacking the maintainer's machine, phase plans that get one cold-start second
look before they are handed downstream, and phase execution that can prove it did not degrade the
codebase it just changed.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Unity Headless Test Execution | In Progress — NO-GO | None | Medium | Four source-authoring features define the headless ladder, asset import, consumer alignment, and inert reference assets. Completion is blocked on main-Editor concurrency evidence, a clean controlled `.meta` import, and a green final gate. |
| 02 | Phase Document Final Check | In Progress — CONDITIONAL | None | Small | Source wiring and the 26-test focused guard suite pass. The optional cold-start reviewer reads the phase document and repository from exactly two paths, reports at most five evidence-tied findings, and lets the refiner fold in accepted findings before one-time synchronization. Manual smoke checks and maintainer propagation remain pending; the full repository gate retains baseline failures. |
| 03 | Phase Execute Audit Bookend | Planned | Phase 01, Phase 02 | Large | Phase - Execute audits at phase start and again at phase end with a byte-identical prompt, compares the two via Auditor - Delta, attributes findings against the known phase baseline commit, and auto-remediates High-or-above drift the phase caused. |

Phase 03 depends on 01 and 02 only in the soft sense that it is executed *by* the pipeline those
phases improve; it has no code-level dependency on either. Execute them in listed order.

## Constraints & Non-Goals

- **`source_of_truth/` is the only authoring surface.** Every deliverable in every phase is a file
  under `source_of_truth/{agents,skills,instructions}`, plus tests under `tests/` and docs under
  `docs/`. Nothing under `ports/` or `.github/` is ever hand-edited.
- **Agents never run propagation.** `scripts/propagate_master_assets.py` is the maintainer's manual
  step, enforced by a `PreToolUse` hook. Sync tests fail until the maintainer propagates; that is
  expected and is not a reason to run it.
- **This repository contains no Unity project.** Phase 01 changes the rules agents follow and ships
  copyable reference assets. It does not wire CI into any Unity repository — that is separate work
  in a different repository and is explicitly out of scope for this roadmap. Empirical verification
  of Phase 01's Unity invocations happens against an external reference project,
  `/Users/jennywadkins/github_repos/the-movies` (Unity `6000.3.13f1`), as a maintainer-executed
  manual QA step. Whether that machine's Unity Personal license permits a second concurrent Unity
  process is unverified and is Phase 01's primary open risk. The controlled missing-`.meta` import is
  also unverified because the reference checkout is not clean. The execution ladder degrades safely,
  but Phase 01 remains NO-GO until both evidence conditions are recorded.
- **No new runtime dependencies.** The repo is stdlib-only Python plus Markdown. Nothing in this
  roadmap changes that.
- **Delegation depth is one.** Only user-invocable root orchestrators spawn agents. Any new
  subagent introduced by these phases is a leaf.
- **Non-goal: reorganizing the agent corpus.** No renumbering, no merging of existing agents, no
  restructuring of `ports/` emitters.
- **Non-goal: GameCI adoption.** A reference workflow ships as an asset in Phase 01. Whether it is
  ever installed anywhere is a later, separate decision. Before activation, its action references
  require verified full commit SHAs and the adapted workflow requires `actionlint` validation.

## Architecture Notes

- **Corpus shape.** 55 agent definitions in `source_of_truth/agents/*.agent.md` (40 hidden
  subagents, 15 user-invocable), 44 skills, 18 instructions. Agents declare their spawnable children
  in an `agents:` frontmatter list; adding a child to an orchestrator means editing that list.
- **Two-stage pipeline.** transform (`source_of_truth/` → `ports/`) then deploy (`ports/` → real
  harness directories). Five harnesses: Claude Code, Codex, OpenCode, Cursor, GitHub Copilot.
- **Testing posture.** Corpus tests are structural only — never keyed to prose wording, because a
  wording-keyed check goes inert the moment anyone rewords the file. Any guard added by these phases
  must be provably able to fail (see the `guard-integrity` skill).
- **Authoring register.** Agent and skill files are machine-facing and read at runtime by an agent
  paying for every token: be dense but brief. Runbooks and QA docs are human-facing: TL;DR, then
  numbered steps.
- **Existing diff-scoped coverage.** Phase - Execute already runs a diff-scoped security scan
  (Step 5) and a pre-production gate (Step 6); the PR Review roster covers consistency, cleanliness,
  artifacts, and dependencies. All of it is scoped to the diff. Phase 03 exists to cover
  codebase-wide degradation *outside* the diff, which none of the above can see.
