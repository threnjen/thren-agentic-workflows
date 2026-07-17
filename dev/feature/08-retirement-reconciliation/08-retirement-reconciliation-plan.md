# 08 Retirement Reconciliation

## Execution Metadata

- **Wave:** 7
- **Parallel safe:** no
- **Depends on:** 07-synthesis-and-pr-posting
- **Key files modified:** `.github/agents/README.md`, `docs/CODEBASE_CONTEXT.md`, `README.md`, `.gitignore`, `tests/test_propagate_master_assets.py`, `tests/test_readiness_synthesis_agents.py`, `.github/learnings/cross-phase-decisions.md`, `dev/feature/phase-03-phase-final-review-execution-manifest.md` (delete — superseded)
- **Sequential reason:** runtime dependency on every prior feature — this is the integration point, and it cannot verify an assembly that does not exist yet

## This Is the Integration Feature

The Phase document's Deliverable 7 is split across two features. `02-retired-evaluator-removal`
performed the **deletion** early, so the five doomed agents did not have to be
dragged through every rename in between. This feature keeps the role the Phase
document actually described for Deliverable 7: **"the integration point where
dangling references surface."**

It is also the phase's integration/bootstrap feature in the decomposition sense.
Features `01`–`07` each ship an agent, a skill, or a propagator capability that
passes review in isolation. Nothing before this point runs the seven agents
together, through the real orchestrator, against a real base/branch pair, and
checks that a readiness report comes out the other end. That end-to-end run is this
feature's core acceptance criterion, and without it the phase can ship eight green
features and a family that has never once worked.

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1** — **End-to-end dry run.** The `05-pr-review` orchestrator runs against the
  pinned base/branch fixture and produces: a change narrative, artifact/consistency/
  dependency findings, a test-health report, a diff-scoped security report from
  `04e-diff-security-scan`, and a severity-ordered readiness report — all under one
  `dev/pr-review/<base-sha-short>-<timestamp>/` directory.
- **AC2** — **The single-interaction contract holds end to end.** The complete run
  asks exactly one block of questions and then reaches a written report with no
  further prompt. This is verified on the assembled system, not asserted per feature.
- **AC3** — **Forced-failure run.** With one evaluator forced to fail, the run
  completes, the readiness report names the missing check and its reason in
  `Checks Not Run`, and the verdict is not `GO`.
- **AC4** — **Return discipline holds.** Every subagent return in the dry run is
  ≤10 lines, with full detail on disk.
- **AC5** — **The roster is exactly seven plus the delegated security scan.**
  `05a`–`05g` exist in `.github/agents/`, propagate to all three roots, and no
  `05h`–`05l` slug survives anywhere.
- **AC6** — **No dangling references anywhere.** `.github/agents/README.md`,
  `docs/CODEBASE_CONTEXT.md`, and root `README.md` carry no retired agent, no old
  slug, and no `phase-final-review` skill or command name.

  **Exempt paths** (must match feature `02`'s shared constant, minus the skill
  exemptions that feature `03` has by now resolved): `docs/phases/**`,
  `.github/learnings/**`, `claude/learnings/**` (a tracked, *propagated copy* of an
  exempt source), and `dev/**` (these feature plans and the superseded
  `phase-03-phase-final-review-execution-manifest.md` all legitimately name retired
  agents).

  **The sweep must match three forms, not one.** Slugs (`05c-qa-consolidator`),
  display names (`05c QA Consolidator`), **and the unhyphenated prose form
  "Phase Final Review"** — which is what both `docs/CODEBASE_CONTEXT.md` and root
  `README.md` actually contain. It is neither a slug nor a `name:` value, so a
  sweep built from the agent registry misses it entirely, which is precisely how it
  survived this long.
- **AC6b** — **Stale counts are corrected.** `.github/agents/README.md` states agent
  and subagent totals (43 agents / 24 subagents) that no name-based sweep can see
  and that this phase changes: five agents are deleted and one is renamed. A count
  is a claim; verify it rather than leaving a number that quietly becomes false.
- **AC6c** — **`.gitignore` is reconciled.** It still carries
  `dev/phase-final-review/` fixture rules (`:6–9`) for a directory that does not
  exist. Feature `04` adds the `dev/pr-review/` rules; this feature removes the dead
  ones.
- **AC7** — **`claude/commands/phase-final-review.md` is absent** and
  `claude/commands/pr-review.md` (or the propagator-derived equivalent) exists. A
  surviving stale command is the sharpest dangling reference in the repo: it stays
  user-invocable and points at a deleted agent.
- **AC8** — **Propagation is clean and idempotent.** A propagation run produces no
  diff noise in unrelated assets, and a second consecutive run changes nothing.
- **AC9** — **Test baseline reconciled and explained.** The suite is green and the
  count delta from the 416 baseline (2026-07-16) is accounted for: deletions from
  feature `02`, additions from features `01`–`07`. A number that cannot be explained
  is not a baseline.
- **AC10** — **`cross-phase-decisions.md` is reconciled.** The PR-Review Rescope
  section's claims that decomposition falsified are corrected — specifically the
  allowlist "forcing function" entry, which is already annotated with a correction
  and should be verified as consistent with what actually shipped.
- **AC11** — **Deferred capabilities are recorded with routing**, not dropped:
  per-agent command scoping (needs a PreToolUse hook; not expressible on Claude via
  frontmatter), the `NO-GO` enforcement hook (needs a hook-owning phase), and
  P5-SEC-02 if feature `07` left it open.

### Non-Goals

- Deleting the five retired evaluators — done in feature `02`.
- Rescoping any agent — done in features `03`–`07`.
- Fixing findings the dry run surfaces about *this* repository. The dry run proves
  the machinery works; the findings it produces about the branch are outputs, not
  bugs.
- Updating `docs/phases/**` status lines. Verdicts are issued by the user by hand,
  and an unverified verdict must not update roadmap or summary status lines.
- Retiring `dev/phase-final-review/` — verified absent from disk (2026-07-16).

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC2, AC3, AC4 | assembled agent family | **Manual QA / fixture dry-run** — required release evidence; static review cannot observe runtime report creation |
| AC5 | `.github/agents/`; three generated roots | Must-have automated test (new) — roster assertion |
| AC6 | `README.md`, `docs/CODEBASE_CONTEXT.md`, `.github/agents/README.md` | Must-have automated test (new) — reference sweep |
| AC7 | `claude/commands/` | Must-have automated test (new) |
| AC8 | `scripts/propagate_master_assets.py` | Must-have automated test (new) — idempotency |
| AC9 | full suite | Existing suite regression |
| AC10, AC11 | `.github/learnings/cross-phase-decisions.md` | Code-review evidence |

## B. Correctness & Edge Cases

**The dry run is required release evidence, not a nicety.** The recorded contract:
*"Fixture dry-runs remain required release evidence for agent wiring and degradation
behavior. Static contract review cannot observe runtime report creation, and a run
whose required evaluators are recorded `not-run` is artifact-level, below-GO
evidence — not a passing dry run."* A dry run in which five of seven evaluators
report not-run does not satisfy AC1. It is evidence the wiring is broken.

**This is also where the phase's own history becomes relevant.** The recorded note
says the whole-phase flow *never successfully ran against a real phase* — which is
why little working code is lost in the rescope. That is a warning, not trivia: this
agent family has never demonstrably worked end to end. AC1 is the first time it
would.

**Reference sweeps must match display names, not just slugs.** The propagator
rewrites agent references by `name:` via `_build_agent_reference_map`, longest-first.
A surviving "05 Phase - Final Review" in prose stops being rewritten once the source
agent is renamed and ships as a literal string. Slug-only greps miss this entirely.

### Failure modes

| Mode | Handling |
|---|---|
| Dry run has evaluators reporting not-run | AC1 unsatisfied — this is broken wiring, not a pass |
| A prompt fires mid-run | AC2 unsatisfied — the erosion this phase was most worried about, caught here |
| Stale command file survives | AC7 — the most dangerous orphan, since it is invokable |
| Propagation produces unrelated diff noise | AC8 — investigate before accepting; noise usually means an identifier resolution changed |
| Test count changed and nobody can say why | AC9 — an unexplained count is not a baseline. The repo has already recorded a coin-flip green run being mistaken for one |
| PERF-01 fires during the suite run | Expected; it is probabilistic and owned by Phase 04. Capture repeated runs; do **not** relax the budget to make a gate pass |

## C. Consistency & Architecture Fit

No new patterns. This feature verifies that features `01`–`07` produced a coherent
whole and updates the three documentation surfaces that describe the agent family
to the reader: `.github/agents/README.md` (the agent catalogue, including its
orchestrator/subagent tables and the "Four orchestrators" note at line 412),
`docs/CODEBASE_CONTEXT.md`, and root `README.md`.

`[PROPOSED - name TBD]`: `claude/commands/pr-review.md` — the exact generated
command filename derives from `_claude_identifier_for` and must be read from the
propagator's output, not assumed.

## D. Clean Design & Maintainability

The reference sweep should be a **test**, not a checklist. A checklist verifies once;
a test verifies forever, and this phase has established that stale references
survive propagation silently. Feature `02` introduces the sweep for retired
evaluators; this feature extends it to old slugs and skill/command names and points
it at the documentation surfaces.

### Keep-it-clean checklist

- [ ] Dry run genuinely ran — seven reports on disk, not seven not-run records
- [ ] Sweep covers display names, not only slugs
- [ ] Sweep is a test, not a one-time grep
- [ ] Propagation idempotent across two consecutive runs
- [ ] Deferred capabilities recorded with routing, not dropped
- [ ] Test count delta explained

## E. Completeness: Observability, Security, Operability

**Observability decision** — None added. This feature's output is evidence, not
runtime behavior.

**Security** — This is where the phase's honest security accounting lands. The
phase set out to narrow every `05x` `execute` grant and **cannot**: per-agent
command scoping is not expressible in Claude subagent frontmatter, works natively
only on OpenCode, and does not exist per-profile on Codex. What the phase actually
achieved is narrower and real: `execute` **removed** from evaluators that did not
need it (feature `05`), never added to those that never had it (feature `06`), and
retained only where a named command has no non-shell equivalent. What remains open
is recorded with routing (AC11) rather than reworded into looking closed — the
recorded rule this project already relies on.

**Runbook** — Verify: the dry run itself is the verification. Rollback: `git revert`
of the feature commits; every asset is static and every generated root is committed.

## F. Test Plan

**Existing tests to update**
- `tests/test_propagate_master_assets.py` — final roster reconciliation and the
  idempotency assertion.
- `tests/test_readiness_synthesis_agents.py` — final consistency pass.

**Must-have automated tests (new)**

Top-value cases:

1. **Roster is exactly seven (AC5).** Given `.github/agents/`, then `05a`–`05g`
   exist and no `05h`–`05l` slug exists in source or any generated root.
2. **Repository-wide reference sweep (AC6).** Given every tracked file outside
   `docs/phases/**` and `.github/learnings/**`, then no retired slug, no old slug,
   and no `phase-final-review` skill or command name appears — matching **display
   names as well as slugs**.
3. **Stale command absent, new command present (AC7).**
4. **Propagation idempotency (AC8).** Given two consecutive propagation runs, then
   the second reports zero changes.
5. **No status-line write-back anywhere in the family (AC5 of feature `07`,
   re-verified on the assembled roster).**

**Manual QA checklist** — this is the phase's release evidence:

- [ ] Dry run against the pinned fixture produces all seven reports plus the `04e`
      security report under one run directory (AC1)
- [ ] Exactly one question block; report reached with no further prompt (AC2)
- [ ] Forced evaluator failure: run completes, `Checks Not Run` names it, verdict is
      not `GO` (AC3)
- [ ] Every subagent return ≤10 lines (AC4)
- [ ] **In a scratch consumer repo, never this one:** `origin/HEAD` unset; base
      correction; no PR open; `gh` unauthenticated
- [ ] Claude, OpenCode, and Codex each load the propagated family without error

## Unverified Assumptions

- That a dry run in this repository is a fair test of an agent family that ships to
  *other* repositories. It is not entirely: this repo has `pytest`, a graph MCP
  server, and pipeline artifacts. The scratch-repo QA above covers the gap
  partially. Full adoption readiness is explicitly out of scope and already
  recorded as needing its own roadmap entry.

## Relationship to Sibling Plans

- **Depends on every prior feature.** It is the assembly test.
- **Completes the Phase document's Deliverable 7**, whose deletion half landed in
  feature `02`.
- **Feeds `@project-planner`** — AC11's deferred capabilities need routing, and the
  adoption-readiness roadmap entry remains outstanding.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16), adjusted by features `01`–`07`.
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Sweep to Extinction

**Goal**: Extend the reference sweep to old slugs, skill names, and command names
across the three documentation surfaces; fix every hit.
**Success Criteria**: AC6, AC7.
**Status**: Not Started

## Stage 2: Verify Propagation

**Goal**: Confirm the roster is exactly seven in all three roots; confirm
idempotency across two consecutive runs; confirm no unrelated diff noise.
**Success Criteria**: AC5, AC8.
**Status**: Not Started

## Stage 3: End-to-End Dry Run

**Goal**: Run the assembled family against the pinned fixture. Then run it again
with one evaluator forced to fail.
**Success Criteria**: AC1, AC2, AC3, AC4. Seven reports on disk — not seven not-run
records.
**Success Criteria (negative)**: the forced-failure run must not produce `GO`.
**Status**: Not Started

## Stage 4: Reconcile the Record

**Goal**: Reconcile `cross-phase-decisions.md`; record deferred capabilities with
routing; explain the test-count delta.
**Success Criteria**: AC9, AC10, AC11.
**Status**: Not Started
