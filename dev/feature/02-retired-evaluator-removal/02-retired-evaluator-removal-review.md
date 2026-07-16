# Review Record: 02 Retired Evaluator Removal

## Summary

The deletion is complete and correct. All five retired evaluators are gone from source
and from all three generated roots, zero generated files were hand-deleted, and no
dangling reference survives outside the exempt paths. The implementation record is
unusually honest: it predicted the AC7 delta before running, recorded the deviations it
took, and surfaced the dual-use cascade rather than hiding it.

I adjudicated the four items raised, verifying by execution rather than by reading:

1. **The `/z-security-scan` → `/security-scan` rename is correct.** Judgement upheld on
   evidence the implementer did not cite: `z-security-scan.md` was the **only** `z-`
   prefixed file among the 19 files in `claude/commands/`. The `z-` prefix is an
   *agents-only* convention marking `user-invocable: false`; it has never been a command
   convention. The old name was an anomaly produced by dual-use stem resolution, and the
   rename converges Claude with OpenCode/Codex. **No dangling reference survives** —
   every repo-wide `z-security-scan` hit is either a historical *report filename*
   (`z-security-scan-final.md`, an unrelated artifact) or documentation of this change.
   The propagator correctly re-pointed the one live prose reference in
   `claude/agents/z-diff-security-scan.md`. Not hand-reverting was the right call.
2. **Non-idempotence is a real latent defect, correctly diagnosed and correctly not
   fixed here — but it was recorded in the wrong place.** The tree **is** genuinely at a
   fixed point: I ran the propagator three separate times; every counter reported zero
   and `git status` showed no drift. The mechanism is confirmed structural
   (`_claude_filename_for:540` resolves against on-disk stems, while pruning deliberately
   runs *after* emission at `:1566-1568`). It was documented only in the implementation
   record — a per-feature artifact no future implementer reads. Now recorded durably.
3. **The D2 time-boxing is sound; its hand-off was mis-addressed.** Plan-over-tasks is
   the right call and is independently corroborated: feature `03`'s own context file
   states it drops the retired-evaluator templates, so pruning here would collide exactly
   as the plan predicts. The tripwire test is good design. But it was addressed to feature
   `08` (wave 7) when it in fact trips at feature `03` (wave 3) — see Issue #1.
4. **Deletion completeness verified.** Complete, with no survivors.

Three issues fixed. Two out-of-scope findings recorded durably rather than patched.

## Verdict

**Approved with Reservations**

The reservations are not defects in this feature's code — they are two items that now have
no owner (Issues #4 and #5) and are recorded in `cross-phase-decisions.md` rather than
carried silently.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | **Met** | `.github/agents/` (5 deletions) | Verified: only `05`, `05a`, `05b`, `05g`, `05h`, `05j`, `05k`, `05l` remain. |
| AC2 | **Met (verified by execution)** | propagator prune (feature `01`) | Not inferred — I ran `propagate_master_assets.py --once` three times; all counters zero, no drift. Zero generated files hand-deleted. |
| AC3 | **Met** | `tests/test_propagate_master_assets.py:89-93` | `expected_slugs` = 3. `NO-GO`/`NOT RUN` conditional gone (remaining hit is in `tests/hooks/`, unrelated). |
| AC4 | **Met** | `tests/test_readiness_synthesis_agents.py` | 6 → 3 tests; `LEARNINGS_AGENT` gone; shared test narrowed and renamed. |
| AC5 | **Met** | `.github/agents/README.md:165,238` | `Security Scan` retained; parent corrected to `None — user-invocable` in both the row and the prose. |
| AC5b | **Met** | `.github/agents/05-phase-final-review.agent.md:5` | Roster = 7 survivors; `grep` for retired refs returns 0. `Baseline Worktree` preserved verbatim (D10 honored). |
| AC6 | **Met, with exemption tightened** | `tests/test_retired_evaluator_removal.py` | Sweep passes. `dev/` exemption narrowed to `dev/feature/` — see Issue #2. |
| AC7 | **Met** | whole suite | 431 passed / 17 subtests, reproduced post-fix. Delta predicted before running and matched exactly. |

**Unverified (requires runtime confirmation, not obtainable by static review):** that
`/security-scan` actually resolves as an invocable slash command in the Claude Code
harness. I verified the file exists at `claude/commands/security-scan.md`, that it carries
the generated marker, and that nothing references the old identifier — but file presence
proves wiring exists, not that the command resolves. Requires a manual invocation to
confirm. This is a pre-existing property of the harness, not a risk this feature
introduced.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Tripwire test addressed to feature `08` (wave 7) but trips at feature `03` (wave 3) — would leave the suite red across waves 4–7, failing every intermediate feature's green-baseline gate | High | `tests/test_retired_evaluator_removal.py:165-186` | AC6 | **Fixed** |
| 2 | `dev/` sweep exemption rests on a false premise ("entirely planning records with no live wiring") — `dev/phase-final-review/fixtures/` is live wiring named by seven surviving agents | Medium | `tests/test_retired_evaluator_removal.py:47` | AC6 | **Fixed** |
| 3 | Propagator non-idempotence recorded only in the implementation record — a per-feature artifact future implementers do not read | Medium | implementation record Gaps §1 | — | **Fixed** (recorded durably) |
| 4 | `dev/phase-final-review/fixtures/PHASE_05/` exists and is tracked, but the plan's Non-Goals dismissed it as "does not exist" — so no feature inherited the Phase document's retirement instruction | Medium | plan Non-Goals; `dev/phase-final-review/fixtures/` | — | **Open** (recorded; out of scope) |
| 5 | Identifier resolution reads disk state, so `propagate_once` has no fixed-point guard; `test_phase02_generated_wiring_is_complete_and_idempotent:657` covers `propagate_hooks_once` only | Medium | `scripts/propagate_master_assets.py:531-547` | — | **Open** (recorded; >50 lines, module not owned here) |
| 6 | `test_no_surviving_agent_declares_a_retired_child` parses frontmatter positionally (`[4:].split("\n---\n", 1)`) and only matches single-line `agents:` rosters; a multi-line YAML list would slip past | Low | `tests/test_retired_evaluator_removal.py:197-201` | AC5b | **Open** (accepted) |

### Issue #1 detail — the four-wave red window

This was the most consequential finding. The tripwire itself is good design: without it,
`EXEMPT_SKILL_DIRS` rots into a permanent hole in the sweep — the exact drift hazard the
plan warns about. But the ownership attribution was inherited from the plan's AC6 text
("`08-retirement-reconciliation` re-runs this sweep"), which predates the tripwire's
invention.

Feature `03` does two things that both trip it: it `git mv`s both skill directories
(`phase-final-review-*` → `pr-review-*`), which makes `EXEMPT_SKILL_DIRS` match nothing,
**and** it strips the retired templates. So the test fails the moment `03` lands, with a
message telling that implementer the cleanup belongs to a feature four waves away. The
likely outcome is either a wasted escalation or four waves of red baseline. The cleanup is
a two-symbol deletion and belongs in `03`'s own pass.

Worth noting the design holds up under the rename: because `03` strips the retired names
*and* renames the dirs, `test_no_tracked_file_references_a_retired_agent` still passes.
Exactly one test trips, with an actionable message. That is a clean hand-off once
correctly addressed.

### Issue #6 detail — why accepted

The positional frontmatter parse is brittle, but the blast radius is nil: any retired name
in `.github/agents/` is independently caught by
`test_no_tracked_file_references_a_retired_agent`, which sweeps the raw text. The roster
test is belt-and-braces over a sweep that already covers it. Fixing it means adding a YAML
dependency or a parser for a format that is currently uniform. Not worth it.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/test_retired_evaluator_removal.py` | Re-addressed the tripwire's docstring, comment, and assertion message from `08` to "whoever lands `03`", with the four-wave red-baseline reasoning recorded inline | #1 |
| `tests/test_retired_evaluator_removal.py` | Narrowed `EXEMPT_PREFIXES` `dev/` → `dev/feature/`, with a comment recording that `dev/phase-final-review/fixtures/` is live wiring and must stay swept | #2 |
| `.github/learnings/cross-phase-decisions.md` | Appended two Propagation Contracts entries (non-idempotence across reclassification; the dual-use reclassification hazard) and one Deferred Pipeline Work entry (the orphaned fixtures) | #3, #4, #5 |
| `claude/learnings/cross-phase-decisions.md` | Propagated copy — regenerated by the propagator, **not hand-edited** | #3, #4, #5 |

Narrowing the `dev/` exemption cost nothing and closed a real hole: the sweep still passes,
which independently confirms `dev/phase-final-review/` and the rest of `dev/` carry no
retired references today. It would now catch one if a future feature introduced it.

After all fixes: propagator run to a fixed point (all counters zero, no drift), full suite
**431 passed / 17 subtests**. No regression. PERF-01
(`test_ac9_propagated_guard_median_latency_is_below_50_ms`) passed; **no threshold was
touched**.

## Remaining Concerns

- **Issue #5 — `propagate_once` has no fixed-point guard.** The real defect behind item 2.
  A future feature can run propagation once, see a plausible tree, and commit a
  non-converged state; nothing in the suite catches it. The naive guard — run the real
  propagator against the real repo and assert zeros — is side-effecting and would mutate
  the working tree on failure, so I did not add it. The honest fix is to make identifier
  resolution derive from source rather than disk state. Recorded in
  `cross-phase-decisions.md`; needs an owner.
- **Issue #4 — the orphaned fixtures.** Not a defect in this feature; the plan's factual
  error created it. Notable because it is *not* a simple deletion: seven surviving agents
  name the fixture root as live wiring, and `cross-phase-decisions.md` pins the fixtures to
  recorded commit SHAs. Retiring them is a design decision with real blast radius.
- **Issue #6** — low severity, covered by the sweep, defer.
- `claude/agents/single-feature.md` — pre-existing orphan, feature `08`'s. Untouched, as
  instructed.

## Test Coverage Assessment

- **Covered**: AC1, AC2, AC3, AC4, AC5, AC5b, AC6 — all by automated tests. AC2's test is
  the one that proves feature `01` works, and it does.
- **Coverage quality is above average.** The sweep was mutation-tested rather than merely
  asserted (appending a retired name to a live agent fails it; removing it passes), and
  `RETIRED_AGENTS` is a single module constant, so the retired list cannot drift between
  tests.
- **Missing**:
  - No fixed-point guard for `propagate_once` (Issue #5). This is the highest-value test
    not present, and the reason a reviewer had to verify convergence by hand.
  - AC7 is a human-reconciled count, not an assertion — inherent to its shape, not a gap.
  - The `/security-scan` command's runtime invocability is not covered by any test and
    cannot be (see Traceability).

## Risk Summary

- **`scripts/propagate_master_assets.py:531-547`** — identifier resolution reads disk
  state, so emission-class changes converge only across multiple runs. This feature is the
  first consumer to trigger it and handled it correctly; the next one may not notice. The
  operational rule ("run until every counter is zero") is now recorded, but a rule in a
  learnings file is weaker than a gate.
- **Deleting an orchestrator can rename a user-facing command.** The `05d` → `Security
  Scan` cascade is not a one-off: any agent that is user-invocable *and* declared as some
  orchestrator's only child will reclassify when that parent dies. Features `04`–`07`
  renumber and rescope agents heavily. Recorded as a standing check.
- **`.github/agents/05-phase-final-review.agent.md`** is shared with feature `04`, which
  rescopes it wholesale. The minimum-touch discipline here (roster + two table rows) was
  correct and keeps the collision small.
- **`EXEMPT_SKILL_DIRS` is a deliberate, time-boxed hole in the AC6 sweep.** It is guarded
  by a tripwire that now names its own trigger, but it is still a hole until `03` lands.
