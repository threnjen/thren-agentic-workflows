# Cross-Phase Decisions

Decisions, constraints, risks, and deferred capabilities that affect a phase other than the one
that discovered them. Append only.

## Phase 01 — two runtime checks outstanding (Must-do before Phase 01 is Complete)

- **Phase 01 is implemented but NO-GO, and the two open items can only be closed by the maintainer
  at a machine with Unity.** `docs/phases/PHASE_01/PHASE_01_QA.md` checks 4 and 5 are recorded as
  `not-executed`. Check 4 is the main-Editor-open concurrency proof — whether Unity Personal permits
  a second concurrent Unity process while the maintainer's Editor stays open and usable. Check 5 is
  the controlled missing-`.meta` import on a clean checkout, blocked because the reference checkout
  at `/Users/jennywadkins/github_repos/the-movies` is not clean. No agent can produce this evidence.
- **Phase 02 was planned and written while Phase 01 was still open.** This was a deliberate call, not
  an oversight — Phase 02 is corpus authoring and shares no file, module, or contract with Phase 01.
  The signal that this is safe is the roadmap's dependency column: Phase 02 depends on None.
- **`actionlint` is unavailable, which is a Feature 04 reservation and not a pass.** Phase 01's
  GameCI workflow template has structural coverage only. Semantic validation and full-commit-SHA
  action pinning are still required before that workflow is ever activated anywhere.

## Phase 02 — deferred: the same final check at Project - Planner

- **Offering the cold-start final check at the end of Project - Planner's phase-summary write was
  considered and deferred, not rejected.** Phase 02 scopes the offer to Phase - Refiner only. The
  reason to defer: the refiner substantially rewrites the planner's document afterward, so a
  planner-stage review examines an artifact that will not be the one handed to Feature - Decomposer.
  Revisit once the refiner-stage check has been exercised on a real session and its findings are
  known to be worth the extra pass.

## Phase 02 — the blindness rule is the phase, and it erodes quietly

- **A cold-start reviewer's entire value is destroyed by a helpful spawn prompt, and nothing warns
  you.** The natural instinct of a spawning agent is to summarize the session, flag what it thinks
  matters, and say which areas are already settled. Any of those reintroduces exactly the shared
  blind spot the reviewer exists to escape. The rule therefore lives in the spawn contract where the
  spawning agent reads it, not only in the phase document.
- **A structural test can prove the prohibition text is present; it cannot prove it is obeyed at
  runtime.** Treat the guard as necessary and insufficient, and exercise the path manually at least
  once before calling the phase complete.
