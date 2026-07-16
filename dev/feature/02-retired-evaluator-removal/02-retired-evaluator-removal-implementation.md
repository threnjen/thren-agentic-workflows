# Implementation Record: 02 Retired Evaluator Removal

## Summary

The five phase-shaped evaluators (`05c-qa-consolidator`, `05d-security-rollup`,
`05e-ac-regression`, `05f-seam-analyzer`, `05i-learnings-harvester`) are deleted from
source. All 15 of their generated outputs (5 × `claude/agents`, `opencode/agents`,
`codex/agents`) were removed **by the propagator**, not by hand — feature `01`'s pruner
fired exactly as designed on its first real consumer. Seven survivors remain: `05a`,
`05b`, `05g`, `05h`, `05j`, `05k`, `05l`.

Two decisions the plan left open, both resolved and recorded below:

1. **`Security Scan`'s parent → standalone (user-invocable), not re-parented.** The
   propagator independently corroborated this from the source of truth.
2. **Discovery Delta D2 → skills exempted, not pruned.** The plan's own AC6 exempt table
   supersedes the tasks file's recommendation; the tasks file predates that table.

**The load-bearing discovery is a cascade the plan did not anticipate.** `Security Scan`
was **dual-use** — user-invocable *and* declared as a child by `05d-security-rollup`, the
only agent that ever declared it. Deleting `05d` dropped it from
`_referenced_agent_names`, which correctly removed its spawnable subagent file and then
**renamed its Claude slash command** `z-security-scan` → `security-scan`. This is a
correction, not a regression, and it is detailed in full below. It also means
**propagation needed three runs to reach a fixed point**.

The AC7 count delta was predicted before running and **matched exactly**: 428 → 431
passed, 22 → 17 subtests.

## Sibling Features

Read the first 5 lines of each sibling plan. This is feature `02`, wave 2.

| Sibling | Relationship |
|---|---|
| `01-propagator-orphan-pruning` (wave 1) | **Hard prerequisite; verified working.** AC2 is unachievable without it. Its pruner removed all 15 generated outputs on the first run. Its review predicted "02 will prune cleanly" — confirmed. |
| `03-pr-review-conventions-skills` (wave 3) | Owns the `phase-final-review-{conventions,report}` skill renames. AC6 exempts those two skills; I did **not** touch them (see Decisions §2). `test_time_boxed_skill_exemption_is_still_load_bearing` will fail once `03` lands, by design. |
| `04-pr-review-orchestrator` (wave 4) | **Shares `.github/agents/05-phase-final-review.agent.md`**, which it rescopes wholesale. I made the minimum touch only: roster trim + two model-tier table rows. |
| `05`, `06`, `07` (waves 5–6) | Blast radius shrunk — the five are gone before their renumbering work begins, which is the whole point of deleting early. |
| `08-retirement-reconciliation` (wave 7) | Owns documentation reconciliation, the `single-feature.md` orphan, and re-running this sweep with the skill exemptions removed. Three items handed to it under Gaps. |

**Shared modules**: `tests/test_propagate_master_assets.py` (shared with `01` — the reason
this feature is not parallel-safe) and `.github/agents/05-phase-final-review.agent.md`
(shared with `04`). Neither had its structure changed.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Five source agents deleted | Plan test 1 | No retired slug present when the agent loader runs | Done | `.github/agents/` (5 deletions) | `tests/test_retired_evaluator_removal.py::test_retired_agents_are_absent_from_source` | PENDING | PENDING |
| AC2 | Generated outputs absent from all three roots, no manual `git rm` | Plan test 2 | No retired output in `claude/`, `opencode/`, `codex/` after propagation | Done | propagator prune (feature `01`) | `::test_retired_agents_are_absent_from_every_generated_root`; propagator counters `claude/opencode/codex_orphans_removed: 5` each | PENDING | PENDING |
| AC3 | `expected_slugs` trimmed; `05d` conditional removed | Existing test update | 8 slugs → 3; `NO-GO`/`NOT RUN` block gone | Done | `tests/test_propagate_master_assets.py:87` | `::test_phase_review_agents_match_all_generated_harness_outputs` (17 subtests, was 22) | PENDING | PENDING |
| AC4 | No `05i` reference; delete 3 tests, narrow 1 | Existing test update | 6 tests → 3; `LEARNINGS_AGENT` gone | Done | `tests/test_readiness_synthesis_agents.py` | `::test_readiness_synthesizer_honors_shared_return_contract_and_top_tier` | PENDING | PENDING |
| AC5 | README lists no retired agent; `Security Scan` retained + re-parented | Plan test 4 | `security-scan.agent.md` exists and propagates | Done | `.github/agents/README.md:163-167,243` | `::test_security_scan_survives_and_still_propagates` | PENDING | PENDING |
| AC5b | Orchestrator roster trimmed to survivors | Plan test 5 | No agent's `agents:` list names a deleted agent | Done | `.github/agents/05-phase-final-review.agent.md:5,37,39` | `::test_no_surviving_agent_declares_a_retired_child` | PENDING | PENDING |
| AC6 | No file references a retired agent outside exempt paths | Plan test 3 | Repo-wide sweep on slugs **and** display names | Done | `.github/agents/README.md` (only offender) | `::test_no_tracked_file_references_a_retired_agent`; `::test_time_boxed_skill_exemption_is_still_load_bearing` | PENDING | PENDING |
| AC7 | Suite passes with an **explained** count delta | Existing suite regression | Predicted delta matches actual | Done | whole suite | 431 passed / 17 subtests across 4 consecutive runs; reconciliation below | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Delete the five source agents | Done | `.github/agents/` | Via `git rm`. Seven `05x` survivors remain. |
| AC2 | Generated outputs absent from all three roots | Done | `scripts/propagate_master_assets.py` (feature `01`) | **Zero generated files hand-deleted.** 5 orphans pruned per root, reported by the counters. |
| AC3 | `expected_slugs` + `05d` conditional | Done | `tests/test_propagate_master_assets.py` | Subtests 22 → 17. D8 confirmed: a stale slug raises `KeyError`, not a soft failure. |
| AC4 | `05i` tests deleted / narrowed | Done | `tests/test_readiness_synthesis_agents.py` | 6 → 3 tests. The `"never read\ncode"` line-wrap assertion at `:16` was **not** touched. |
| AC5 | README reconciled; `Security Scan` retained | Done | `.github/agents/README.md` | Parent corrected to standalone. See Decisions §1. |
| AC5b | Orchestrator roster trimmed | Done | `.github/agents/05-phase-final-review.agent.md` | D1 resolved. `Baseline Worktree` preserved verbatim (D10 — not normalized). |
| AC6 | Repo-wide reference sweep | Done | `tests/test_retired_evaluator_removal.py` | Exactly one non-exempt offender existed (README). Sweep mutation-tested. |
| AC7 | Explained count delta | Done | whole suite | Predicted **before** running; matched exactly. |

## Stage 1 — Security Delegation Path (gate: recorded, not skipped)

The plan required this check be evidenced rather than taken on the strength of its own
note. Re-verified at implementation time, **before** deleting `05d`:

| Check | Result |
|---|---|
| `.github/agents/04e-diff-security-scan.agent.md` exists | Yes |
| `04e` holds no `execute` | Confirmed — `tools: [read, search, edit]` |
| `04e` is diff-shaped | Confirmed — `user-invocable: false`; body: "review of ONLY the files changed by a specific implementation pass… NOT a phase-level gate" |
| `.github/agents/security-scan.agent.md` exists | Yes — retained |

**Finding, as required:** retiring `05d-security-rollup` is a **shape change, not a
security-coverage regression**. The rollup aggregated *per-subphase* security reports — a
shape with no PR analogue. The diff-scoped check it wrapped is delegated to `04e`, which
already exists, is already diff-shaped, and already holds no `execute`. Had `04` not
existed, this deletion *would* have been a regression and the gate would have stopped it.

No shell/Bash permission was granted or restored anywhere in this feature.

## Decisions

### 1. `Security Scan`'s parent → **standalone (user-invocable)**, not re-parented

The plan's sole Unverified Assumption, explicitly left to the implementer. Resolved
against evidence rather than preference:

- **Only `05d` ever declared it.** `grep "^agents:.*Security Scan"` across all source
  agents returns exactly one hit: `05d-security-rollup.agent.md:5`. `04-phase-execute`
  declares `04e Diff Security Scan` — a *different* agent with a different exact name.
  Nothing else spawns it. Nothing is stranded by removing the parent.
- **It is user-invocable**, so losing a parent does not strand it: `security-scan.agent.md`
  has no `user-invocable` key, which the propagator defaults to `true`
  (`propagate_master_assets.py:417`). It remains directly reachable on all three platforms.
- **Re-parenting to `05 Phase - Final Review` was rejected.** It would mean *adding* a
  child to a roster this feature is scoped only to *trim*, inventing pipeline design this
  feature does not own, and colliding with `04-pr-review-orchestrator`, which rescopes that
  file wholesale. It would also contradict the architectural decision that security is
  delegated to `04e`.
- **Retiring it was rejected** — the plan forbids it, and it is separately referenced.

Applied to README row 169 (`05d Security Rollup` → `None — user-invocable`) and prose
line 243 (`*(subagent of 05d Security Rollup)*` → `*(standalone; user-invocable)*`).

**The propagator independently reached the same conclusion**, which is the strongest
evidence available that the call is right — see the cascade below.

### 2. Discovery Delta D2 → **exempt the skills; do not prune them**

D2 records a contradiction between AC6 and the plan's non-goals, and the tasks file
recommends option (a) — prune the retired report rows from
`.github/skills/phase-final-review-conventions/SKILL.md` here.

**I took option (b), because the plan has since been updated and D2's premise no longer
holds.** D2 states "AC6 allows only `cross-phase-decisions.md` and `docs/phases/**` as
exceptions", and its Action column says "Update plan". That update **was made**: the
current plan's AC6 carries a five-row exempt table that explicitly includes
`.github/skills/phase-final-review-{conventions,report}/` and their propagated copies,
with the rationale "Deferring is deliberate: rewriting a skill this feature does not own
would collide with feature `03`", and states that `08` re-runs the sweep with the
exemptions removed. The tasks file's recommendation predates that table.

The plan is the authority and it resolves the conflict in the opposite direction from the
tasks file. Pruning the skill here would collide with feature `03`, which owns those files.

To stop the exemption from silently outliving its cause — the exact drift hazard the plan
warns about — I added `test_time_boxed_skill_exemption_is_still_load_bearing`, which
**fails once feature `03` lands** and instructs `08` to delete the exemption. The exemption
cannot rot into a permanent hole in the sweep.

### 3. Discovery Deltas D3 / D4 → directory-scoped exclusions, one constant

D4 (AC6 vs. test-plan case 3 disagreeing) is likewise resolved by the plan's exempt table.
Encoded as directory-scoped prefixes in a single module constant, per D4's recommendation.
D3's trap (`claude/learnings/` is a *propagated copy* of an exempt file) is covered.
**Verified at implementation time, as D3 requires:** `opencode/learnings/` and
`codex/learnings/` **do not exist**, so only `.github/learnings/` and `claude/learnings/`
need exempting.

### 4. Sweep scope → `dev/` exempted (not in the plan's table)

The plan's exempt table omits `dev/`, but the sweep hits 14 files under `dev/feature/` —
including this feature's own plan, context, and tasks, and features `03`–`08`'s planning
documents. These name the retired agents *in order to describe retiring them*. They are
records of the work, not live harness wiring — the same category as `docs/phases/**`, which
the plan does exempt. Exempting `dev/` is required for the sweep to be writable at all.
Recorded here rather than taken silently.

## The `Security Scan` dual-use cascade (unplanned; correct)

The plan calls the `Security Scan` re-parenting "the trap" and warns that deleting `05d`
orphans its child's parent claim. The real cascade went further than the plan predicted,
and it is the most consequential finding of this feature.

`Security Scan` was **dual-use**: `user_invocable=True` **and** named as a child by `05d`
(`propagate_master_assets.py:1531`: `is_dual_use = agent.user_invocable and agent.name in
referenced_names`). Dual-use agents get **both** a slash command and a spawnable subagent
file. Deleting `05d` removed the only entry that made it dual-use, with two effects:

1. **`claude/agents/z-security-scan.md` was removed.** Correct: no agent declares
   `Security Scan` as a child any more, so a spawnable subagent file would be dead weight.
   Removed by the propagator's reclassification path (`:1515`), **not** the orphan pruner —
   which is why `claude_orphans_removed` reports `5` while six files left that root.
2. **Its Claude slash command was renamed** `z-security-scan.md` → `security-scan.md`.
   `_claude_filename_for` (`:540`) resolves identifiers against **on-disk stems**. While
   `z-security-scan.md` existed in `claude/agents/`, the command latched onto the `z-`
   stem. Once it was gone, the identifier resolved to the natural `security-scan`.

**The rename is a correction, and the old name was the anomaly.** The `z-` prefix marks
hidden subagents (`user-invocable: false`); `Security Scan` is user-invocable and never
qualified. OpenCode and Codex already named it `security-scan` — only Claude carried the
`z-`, as an artifact of the dual-use stem resolution. The rename **converges Claude with
the other two roots**.

Nothing references the old command identifier: the only `z-security-scan` hits repo-wide
are historical *report filenames* (`…/z-security-scan-final.md`) in `docs/phases/**` and
the learnings, which are unrelated to the command. The propagator also correctly re-pointed
the one live reference — `claude/agents/z-diff-security-scan.md`'s prose now reads
`` `security-scan` `` instead of `` `z-security-scan` ``. Had it not, that reference would
now dangle.

Per the plan's architectural commitment, **none of this was hand-reverted**. The generated
roots are a pure function of source plus on-disk state; fighting the propagator by hand is
exactly the masking behavior AC2 forbids.

**Consequence — propagation is not idempotent across a reclassification.** Because
identifier resolution reads on-disk stems, the tree needed **three** `--once` runs to reach
a fixed point (run 1: prune + reclassify; run 2: rename the command; run 3: settle
`codex_profiles`; run 4: all counters zero). A single run would have left the tree in a
valid-looking but non-converged state. This is a latent propagator wart, not a defect
introduced here — see Gaps §1.

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05c-qa-consolidator.agent.md` | Delete | — | AC1 |
| `.github/agents/05d-security-rollup.agent.md` | Delete | — | AC1 |
| `.github/agents/05e-ac-regression.agent.md` | Delete | — | AC1 |
| `.github/agents/05f-seam-analyzer.agent.md` | Delete | — | AC1 |
| `.github/agents/05i-learnings-harvester.agent.md` | Delete | — | AC1 |
| `.github/agents/05-phase-final-review.agent.md` | Modify | Roster `:5` trimmed 12 → 7 children; model-tier table rows `:37`/`:39` dropped the five. Nothing else. | AC5b / D1. Minimum touch — `04` rescopes this file wholesale. |
| `.github/agents/README.md` | Modify | Removed the 5 evaluator rows; corrected `Security Scan`'s parent in row 169 and prose 243. | AC5 / D5 |

### Generated Files (propagator-produced — none hand-edited)

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `claude/agents/z-{qa-consolidator,security-rollup,ac-regression,seam-analyzer,learnings-harvester}.md` | Delete (pruned) | — | AC2 — feature `01` pruner |
| `opencode/agents/05{c,d,e,f,i}-*.md` | Delete (pruned) | — | AC2 — feature `01` pruner |
| `codex/agents/z-{qa-consolidator,security-rollup,ac-regression,seam-analyzer,learnings-harvester}.toml` | Delete (pruned) | — | AC2 — feature `01` pruner |
| `claude/agents/z-security-scan.md` | Delete (reclassified) | — | Dual-use cascade — no longer declared as any agent's child |
| `claude/commands/z-security-scan.md` → `claude/commands/security-scan.md` | Rename | Identifier resolved to its natural stem | Dual-use cascade |
| `claude/agents/z-diff-security-scan.md` | Modify | `` `z-security-scan` `` → `` `security-scan` `` in prose | Reference map re-pointed at the new identifier |
| `claude/commands/phase-final-review.md`, `opencode/agents/05-phase-final-review.md`, `codex/agents/05-phase-final-review.toml`, `codex/profiles/phase-final-review.config.toml` | Modify | Regenerated from the trimmed orchestrator | AC5b |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_retired_evaluator_removal.py` | Create | New module, 6 tests. `RETIRED_AGENTS` is the single definition of the retired names; exclusions are one directory-scoped constant. | AC1, AC2, AC5, AC5b, AC6 |
| `tests/test_propagate_master_assets.py` | Modify | `expected_slugs` 8 → 3; deleted the `05d` `NO-GO`/`NOT RUN` conditional; updated `test_marker_guard_matches_every_real_generated_file` counts (33→27, 46→41, 46→41). | AC3 |
| `tests/test_readiness_synthesis_agents.py` | Modify | Deleted the 3 `05i` tests and the `LEARNINGS_AGENT` constant; narrowed + renamed the shared-contract test to `test_readiness_synthesizer_honors_shared_return_contract_and_top_tier`. | AC4 |

**One existing test the plan did not name required an update.**
`test_marker_guard_matches_every_real_generated_file` hardcodes per-root generated-file
counts. It was added by feature `01`'s **review**, after this plan was written, so the plan
could not have anticipated it. Counts updated with the arithmetic recorded inline:
claude/agents 33 → **27** (−5 retired, −1 `z-security-scan`), opencode/agents and
codex/agents 46 → **41** (−5 each); command and profile counts unchanged (the Security Scan
command was renamed, not removed). The two unmarked files it pins — `README.md` and
`single-feature.md` — are untouched and still unmatched.

## Test Results

- **Baseline**: **428 passed, 22 subtests** (verified before starting; matches the
  orchestrator's figure, **not** the plan's stale 416/15, which predates feature `01`).
- **Final**: **431 passed, 17 subtests** — stable across **4 consecutive full runs**.
- **New tests added**: 6
- **Regressions**: None.

### AC7 — the delta, predicted then reconciled

AC7 requires the delta be *explained*, not observed. It was **predicted before running**
and matched exactly:

| Step | Passed | Subtests |
|---|---|---|
| Baseline | 428 | 22 |
| −3 `05i` tests deleted from `test_readiness_synthesis_agents.py` (6 → 3) | 425 | 22 |
| −5 subtests as five retired slugs leave `expected_slugs` (8 → 3) | 425 | **17** |
| +6 new tests in `test_retired_evaluator_removal.py` | **431** | 17 |
| **Actual** | **431** ✓ | **17** ✓ |

The intermediate 425/17 figure was confirmed by direct observation mid-implementation, so
both halves of the prediction are independently evidenced rather than inferred from the
endpoint.

The plan's own AC7 prediction (416 → 413 / 15 → 10) is **stale in its absolute numbers**
but its *arithmetic* — −3 tests, −5 subtests — is exactly right and is what reconciled.

### PERF-01

`test_ac9_propagated_guard_median_latency_is_below_50_ms` **passed on all runs**. No
threshold was touched.

## Deviations from Plan

1. **Discovery Delta D2 resolved as option (b) — exempt the skills — against the tasks
   file's recommendation of option (a).** The plan's AC6 exempt table postdates D2 and
   resolves the conflict the other way. Full reasoning in Decisions §2. Mitigated by a test
   that fails when the exemption stops being load-bearing.
2. **`dev/` added to the sweep exclusions.** Not in the plan's exempt table; required for
   the sweep to be writable. Decisions §4.
3. **One unplanned existing test updated** — `test_marker_guard_matches_every_real_generated_file`
   (added by feature `01`'s review, after this plan). See Test Files.
4. **`.github/agents/README.md` rows are removed, not just the enumerated line numbers.**
   The plan names rows 164–167 and 171; those line numbers shifted as I edited. Verified by
   the sweep rather than by line number.
5. **The `05-phase-final-review` body edit touched 2 lines, not "3 mentions".** The tasks
   file predicts `grep -c` → 3; the three *locations* are the roster (`:5`) and two
   model-tier table rows (`:37`, `:39`). Post-edit `grep` for retired refs returns zero.

## Gaps

1. **Propagation is not idempotent across a reclassification** (Propagator wart, `01`'s
   module). `_claude_filename_for` resolves identifiers from on-disk stems, so removing a
   subagent file changes the identifier computed on the *next* run. This tree needed three
   `--once` runs to converge. Feature `01`'s review flagged the mechanism ("any reordering
   silently renames survivors"); this feature is the first to trigger it. **A single
   propagation run is not sufficient to prove convergence** — run until all counters are
   zero. Not fixed here: fixing it means changing identifier resolution in a module this
   feature does not own, and the plan's non-goals forbid it. Recommend `08` or a dedicated
   feature.
2. **`claude/agents/single-feature.md`** — the pre-existing unmarked orphan from feature
   `01`'s Gap 1. Untouched, exactly as instructed. Still feature `08`'s.
3. **The two `phase-final-review-*` skills still name the retired report filenames** —
   deliberately, per Decisions §2. `08` must remove `EXEMPT_SKILL_DIRS` from
   `tests/test_retired_evaluator_removal.py` once `03` lands;
   `test_time_boxed_skill_exemption_is_still_load_bearing` will fail and say so.
4. **`Security Scan` sits in README's "Hidden Subagents" table** whose preamble says those
   agents run "with `user-invocable: false`". It does not, and never did — this misfiling
   is **pre-existing** (it was dual-use before, and is standalone now), not caused by this
   feature. I corrected its parent column, which is what AC5 sanctions; moving it to the
   User-Facing table is documentation reconciliation and belongs to `08`.
5. **The sweep reads `git ls-files`, so untracked files are not swept.** This matches the
   plan's "every tracked file" wording. Both files this feature leaves untracked
   (`claude/commands/security-scan.md`, `tests/test_retired_evaluator_removal.py`) were
   manually verified clean, and both become swept once committed.

## Reviewer Focus Areas

- **The `Security Scan` dual-use cascade is the thing to check.** Deleting `05d` removed a
  file (`claude/agents/z-security-scan.md`) and **renamed a user-facing slash command**
  (`/z-security-scan` → `/security-scan`) that the plan never mentions. My judgement is
  that both are correct and the rename converges Claude with OpenCode/Codex, and that
  hand-reverting either would violate AC2's no-hand-editing commitment. This is the
  highest-value second opinion in the feature.
- **Decisions §2 (D2) is where I departed from the tasks file.** I read the plan's AC6
  exempt table as superseding it. If that reading is wrong, the skill rows should be pruned
  here instead — worth confirming.
- **`test_time_boxed_skill_exemption_is_still_load_bearing` is an inverted assertion**
  (`assert still_offending`) and is *designed to fail* when feature `03` lands. Confirm
  that is a desirable hand-off signal rather than a future false alarm.
- **The sweep is mutation-tested, not merely asserted.** Appending "05d Security Rollup" to
  a live agent makes `test_no_tracked_file_references_a_retired_agent` fail; removing it
  makes it pass. `test_security_scan_survives_and_still_propagates` was likewise verified
  by hiding the source agent. Both trees were restored and re-verified.
- **`dev/` in `EXEMPT_PREFIXES` is the broadest exclusion** and the one most able to hide a
  real reference. My rationale is that `dev/` is entirely planning records with no live
  wiring. If a reviewer disagrees, narrowing it to `dev/feature/` is a one-line change.
