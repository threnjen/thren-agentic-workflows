# Review Record: 08 Retirement Reconciliation

## Summary

The integration feature. AC5–AC11 are implemented and, after the fixes below, genuinely
verified. AC1–AC4 — the fixture dry run, which this feature's own plan calls its "core
acceptance criterion" — are **not done**, honestly recorded, and correctly routed.

Two things dominate this review.

**First, the suite was red at the implementer's own commit, and their own new file caused
it.** The record reports `1 failed, 581 passed`. Measured on a clean tree at `3cd47e5`:
`2 failed, 580 passed`. The extra failure is feature `02`'s retirement sweep
(`tests/test_retired_evaluator_removal.py::test_no_tracked_file_references_a_retired_agent`),
tripped by `tests/test_retirement_reconciliation.py:194`, which spelled a retired
evaluator slug in a docstring. The sweep enumerates through `git ls-files`, so the file
was invisible while untracked and became visible the moment it was committed. The green
run was taken pre-commit and never re-measured. AC9's reconciliation — `561 + 20 = 581 ==
actual final passed count` — matched a *prediction*, not a measurement; the real
post-commit figure was 580. This is the third-order version of the phase's signature
defect, in a record that itself warns that "an earlier implementer on this phase shipped a
red suite while claiming green."

**Second, my independent mutation sweep (~65 mutations) found 3 inert guards their two
rounds missed — and 2 of them corresponded to live defects already on disk.** AC6b's count
guards were keyed to the *corrected* string via `_assert_once`, which is blind to stale
restatements by construction. Asserting `"41 source agent definitions"` appears exactly
once was satisfied while **four stale `43` claims survived** on two of the three surfaces
AC6 names. The single most-quoted principle in this feature's own record — "a count is a
claim; verify it rather than leaving a number that quietly becomes false" — was violated by
the guard written to enforce it.

Everything else held up well. The catalogue guard, roster guards, propagation fixed-point
guard, allowlist sweep, skill-directory backstop, command guards and orphan guards all
survived every mutation I could construct (14 catalogue mutations, 21 propagation-root
mutations, 5 orphan-plant mutations, 6 allowlist-reach mutations, 5 `.gitignore`
mutations, all caught).

**The three contested judgement calls all resolve in the implementer's favour**, and each
was verified by execution rather than accepted: the fixtures retirement is correct, the
AC6 allowlist is equivalent-or-stronger, and the deferral of AC1–AC4 is the right call.

## Verdict

**Approved with Reservations**

The reservation is not the code — after these fixes the feature is correct and the suite is
genuinely green. The reservation is that **this phase cannot be GO.** See Risk Summary.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | **Unverified — NOT DONE** | — | End-to-end dry run. Requires an agent fan-out; no agent-spawning tool in the implementer's context. Recorded open with owner + routing. Below-GO by the recorded contract. |
| AC2 | **Unverified — NOT DONE** | — | Single-interaction contract. Requires runtime observation of a live run. |
| AC3 | **Unverified — NOT DONE** | — | Forced-failure run. Requires execution. |
| AC4 | **Unverified — NOT DONE** | — | Return discipline. Requires observation of live subagent returns. |
| AC5 | Met | `.github/agents/` (unchanged) | Roster already correct; the *catalogue* describing it was not. Verified by derivation from disk, not restatement. 26 mutations caught. |
| AC6 | Met | `README.md`, `docs/CODEBASE_CONTEXT.md`, `.github/agents/README.md` | Three pattern classes incl. the prose form. Allowlist deviation accepted — see Issue #5. |
| AC6b | **Met after fix** | `README.md:17,130`; `docs/CODEBASE_CONTEXT.md:16,29,31,89` | **Was materially incomplete.** Four stale `43` claims survived and the guards could not see them. Fixed (Issues #2, #3). |
| AC6c | Met | `.gitignore:5-12` | Both directions asserted through real traversal. `git check-ignore` correctly rejected as an oracle — I confirmed that reasoning is sound. One redundant rule (Issue #6, Low). |
| AC7 | Met | `claude/commands/pr-review.md` | Name derived from `_claude_identifier_for`, not assumed. Both directions mutation-caught. |
| AC8 | Met | `scripts/propagate_master_assets.py` (read-only) | Fixed point verified; converged from an isolated empty consumer, which is the stronger claim. |
| AC9 | **Met after fix** | whole suite | **The reported baseline was wrong.** Real: `2 failed, 580 passed` at `3cd47e5`. Now `1 failed (PERF-01 only), 582 passed`. Reconciled below. |
| AC10 | Met | `.github/learnings/cross-phase-decisions.md` | 5 falsified claims struck with strikethrough, history preserved. Named target (allowlist "forcing function") correctly verified as needing no edit. |
| AC11 | Met | `.github/learnings/cross-phase-decisions.md:104-207` | 6 deferrals, each with owner + routing. Verified none was reworded into looking closed. |
| Plan test 5 | Met (existing) | `test_readiness_synthesis_agents.py` | Correctly not duplicated. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Suite red at `3cd47e5` (`2 failed, 580 passed`), reported as `1 failed, 581 passed`. New test file's docstring trips feature `02`'s sweep once committed; green run taken pre-commit | **High** | `tests/test_retirement_reconciliation.py:194` | AC9 | **Fixed** |
| 2 | Four stale `43` count claims survive on 2 of the 3 AC6 surfaces | **High** | `README.md:17`; `docs/CODEBASE_CONTEXT.md:16,29,31` | AC6b | **Fixed** |
| 3 | AC6b count guards inert: `_assert_once` on the corrected string is blind to stale restatements; `CODEBASE_CONTEXT`'s source-agent count untested entirely | **High** | `tests/test_retirement_reconciliation.py:399-422` (pre-fix) | AC6b | **Fixed** |
| 4 | `docs/CODEBASE_CONTEXT.md` names `prod-code-review.md` as the only plain-`.md` exception; `README.md` was corrected to add `docs-writer.md`. Surfaces disagreed | Medium | `docs/CODEBASE_CONTEXT.md:32` | AC6b/DD-4 | **Fixed** |
| 5 | Record claims `opencode/skills/` and `codex/skills/` "do not exist" and pass vacuously. Both exist and are fully populated with tracked `SKILL.md` files; the check is real for all four roots | Medium | `08-...-implementation.md` Gaps §5 | AC6 | **Open** (record-only; guard is *stronger* than claimed) |
| 6 | `.gitignore:12` `!dev/pr-review/fixtures/**` is redundant — deletable with the guard green | Low | `.gitignore:12` | AC6c | **Wont-Fix** (harmless; documents intent) |
| 7 | `.github/skills/` holds 24 dirs; both surfaces claim 16 | Medium | `README.md:18`; `docs/CODEBASE_CONTEXT.md:17,34` | — | **Open** (pre-existing; this phase did not falsify it) |
| 8 | "6 orchestrators" / "11 visible user-facing agents" disagree with disk | Medium | `docs/CODEBASE_CONTEXT.md:87-88` | — | **Open** (implementer's Gaps §4; pre-existing) |
| 9 | `04-phase-execute.agent.md:176` carries the retired prose name as a step heading | Low | `04-phase-execute.agent.md:176` | AC6 | **Open** (name collision, not a dangling ref; out of scope) |

### Issue #1 in detail — the mechanism matters

This is not a careless miss; it is a **structurally invisible** failure, and worth
recording as a pattern. The sweep enumerates candidates via `git ls-files`. An untracked
file is not swept. So a new test file that violates the sweep is green for its entire
authoring life and turns red at `git add`. Every local verification the implementer ran was
honest and every one of them was wrong.

The fix respects the constraint I was given. The offending docstring named a retired slug;
**I did not add the file to `EXEMPT_FILES`.** Both modules already state the rule that
makes the fix obvious: the retired names live exactly once, in
`test_retired_evaluator_removal.py`'s `RETIRED_AGENTS`, and
`test_retirement_reconciliation.py:51-53` explicitly says it does not re-list them — while
its own docstring did. The sweep was right and the docstring was wrong.

### Issue #3 in detail — why `_assert_once` was the wrong tool here

`_assert_once` is an excellent instrument and the implementer was right to reuse it. It was
simply pointed at the wrong class of claim. It pins **one load-bearing statement** and
fails on 0 or 2+ — perfect for "this directive must exist exactly once."

A count claim is not one statement. It is a **class** of sentence that may be restated
anywhere on the surface, and the stale members are invisible to any needle built from the
right answer: `"41 source agent definitions"` simply does not match `"43 source agent
definitions"`. The guard could only ever see the sentence someone had already remembered to
fix. Confirmed by mutation, then confirmed as live on disk.

The replacement, `_assert_every_count_claim`, matches the claim's **shape** by regex
(`(\d+) source agent definitions`) and reads the number out of it, so every restatement is
verified and a stale one fails. It also asserts at least one claim matched, so rewording
the claim out of existence fails rather than silently disarming the guard.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/test_retirement_reconciliation.py` | Reworded the `04e` docstring so it no longer spells a retired slug; documented why the exemption is refused | 1 |
| `README.md` | `:17` `43` → `41` (recounted from disk) | 2 |
| `docs/CODEBASE_CONTEXT.md` | `:16,29,31` `43` → `41`; added `docs-writer.md` to the key-paths tree as the second plain-`.md` agent | 2, 4 |
| `tests/test_retirement_reconciliation.py` | Replaced the two inert `_assert_once` count guards with `_assert_every_count_claim`; added `test_codebase_context_source_agent_count_matches_disk` | 3 |
| `eval/runs/phase-pr-review/ledger-events.jsonl` | 2 `discovered-failure` + 2 `resolution` rows (`20260716-review-08-001..004`), verified present | — |

No agent prose changed. No assertion weakened or removed. Nothing added to `EXEMPT_FILES`
or `EXEMPT_SKILL_DIRS`. No shell/Bash permission granted or restored. No file under
`tests/hooks/` or `.github/hooks/` touched; the 50 ms threshold is unchanged.

## The four adjudications

### 1. AC1–AC4 — the dry run. Deferral is honest, correctly recorded, and **below GO**.

The deferral is **correct behaviour and I would have made the same call.** The implementer
had the means to manufacture a passing-looking artifact and refused, on the grounds that
the recorded contract makes a run with `not-run` evaluators *below-GO evidence, not a
passing run*. Fabricating it would have converted a known gap into a false claim of
release evidence. Recorded with owner and routing at
`cross-phase-decisions.md:202-207`, and flagged in their own record as "the honest headline
rather than a footnote," with an explicit warning not to read the green suite as evidence
the family runs. That is exactly right, and given that this review found their green suite
was not even green, the warning is better-founded than they knew.

I verified the preconditions they claim are now met, and they are: 8/8 roster names resolve
to agents on disk; the pinned range is 3 commits / 26 files; the report-root migration is
closed; run output is gitignored (I mutation-tested that rule in both directions). **The
run is now possible for the first time in this phase's history. It has still never
happened.**

**Stated plainly, as instructed: this phase cannot be GO.**

AC1 is this feature's own core acceptance criterion, and this feature is the phase's
integration point — the only place where the seven agents are ever exercised together.
Eight features have passed review in isolation. **The assembled family has never once run.**
The recorded contract makes a fixture dry run *required release evidence*, and required
evidence that was not produced is not satisfied by eight green features; the plan's own
words are that the phase can otherwise "ship eight green features and a family that has
never once worked." Nothing in AC5–AC11 substitutes: they prove the family is *described*
correctly and *assembles* correctly, not that it *runs*. Static review cannot observe
runtime report creation — that is the contract's explicit premise, not my caution.

The correct disposition is GO **conditional on** executing AC1–AC4 in a context that can
spawn subagents, before release. Approving this feature is approving the code; it is not
approving the phase.

### 2. Independent mutation sweep — 3 inert found, 2 live

Covered above. ~65 mutations across every assertion in the module. Their claim of "40
mutations / 2 rounds / 0 inert" was, once again for this phase, **not clean** — the
prediction that every implementer's sweep would be disproven by their reviewer held for the
eighth consecutive feature. Notably, their rounds were strong exactly where they had been
burned before (they found the superstring hole in the catalogue guard themselves, and the
`git check-ignore` hole is a genuinely excellent catch) and blind in the one place they had
declared victory.

`_assert_once` verified as reused correctly at `test_retirement_reconciliation.py:136-150`;
it fails on 0 and on 2+, confirmed by mutation in both directions on all seven catalogue
rows.

### 3. The AC6 allowlist deviation — **accepted; equivalent-or-stronger**

The implementer is right, and I verified it rather than accepting the argument.

Their claim is that the plan's exclusion list ("every tracked file outside `docs/phases/**`
and `.github/learnings/**`") fires on `tests/test_pr_review_skills.py` (which *holds the
rename map*) and `tests/test_readiness_synthesis_agents.py` (which asserts the old names are
absent) — the guards for the very thing being swept — and that the only way to green is the
exemptions they were told not to add. I confirmed both files do carry the names for exactly
those reasons.

I tested the narrowing directly rather than reasoning about it. I grepped every retired
skill/command name and old slug across **every tracked path outside the allowlist**. The
only hits are (a) `tests/`, i.e. the guards themselves, and (b) `claude/learnings/`, the
propagated copy of an exempt source. **There is no live, load-bearing surface outside the
allowlist carrying a retired name.** I then mutation-tested that the allowlist actually
*reaches* all six prefixes it claims — planting a retired skill name in a real tracked file
under each — and all six fired, while the exempt `claude/learnings/` correctly did not. The
backstop (`test_retired_skill_directories_are_absent_from_every_root`) fires for all four
skill roots.

The reasoning is also sound on its own terms: a retired skill name is only harmful where
something *loads* it, and an exclusion list closes each false positive by appending an
exemption until it stops sweeping. The allowlist does not narrow coverage of the harm
class. **Not a hole.**

One residual: the allowlist does not cover `.claude/`, `.codex/`, `.opencode/`,
`AGENTS.md`, or `HARNESS_SETUP.md`. None carries a retired name today. If a future harness
config names a skill directory, the sweep would not see it. Worth widening opportunistically;
not a defect now.

### 4. Deferral reconciliation — complete; nothing silently dropped

Each item routed to this feature, verified individually:

| Routed item | Disposition | Verified |
|---|---|---|
| `claude/agents/single-feature.md` orphan | Deleted | Absent; guarded by a *derived* invariant (`test_claude_agents_root_holds_only_the_catalogue_and_generated_output`), not a name list — mutation-caught by replanting it. The upgrade from a hardcoded 2-name list is a real improvement |
| Fixture-root retirement | Retired (13 files) | Gone; mutation-caught. Reasoning independently confirmed — see below |
| Feature `04`'s AC13 dry run | **Open**, routed | `cross-phase-decisions.md:202-207`, owner + routing named. Not reworded closed |
| README-roster / `expected_slugs` correspondence | Fact confirmed; cause corrected | Their refutation holds. `execute` cannot explain the catalogue half — a README has no assertion to dodge, so the stated motive is unavailable there. "Category" (the mechanical evaluators) explains both halves, and the decomposition independently named feature `05` after exactly that set. Fixed by derivation, which is the right fix regardless of cause |
| Pre-rescope manifest | Deleted | Absent; mutation-caught |
| Propagation non-idempotence | **Open**, routed | `cross-phase-decisions.md:171`, owner = a propagator-owning feature, routing = `_claude_identifier_for`. Correctly *not* fixed here (would be rearchitecting) |
| P5-SEC-02 | **Open**, verified | Confirmed still open, correctly |

**Propagation fixed point:** verified at a genuine fixed point. `propagate_once` against the
real repo root reports zero change counters, and — the stronger test — converges from an
isolated empty consumer, which would catch a propagator that never converges from scratch.
`INVENTORY_COUNTERS` is a good design: unlisted counters fail *closed* into the assertion.
No orphans in any root: all 21 roster/root combinations mutation-caught, and orphan plants
in all five agent roots caught.

**Empty-directory residue: genuinely absent.** `find . -type d -empty` outside `.git`
returns nothing under any shipped root. (The only empty dirs anywhere are under
`eval/runs/` and `docs/inspiration/`, both pre-existing and gitignored.) I also
independently reproduced the residue class the implementer describes — my own mutation
harness created empty `opencode/skills/`-style dirs invisible to `git status` — which
confirms the hazard is real and that their `find`-plus-`git status` double check is the
right verification. Their harness cleanup is correct.

### On the fixtures retirement — the highest-value second opinion, as they asked

They were right, and the orchestrator's independent execution already settled it. I did not
re-litigate. I note only that the reusable lesson they drew is the sharpest thing in this
phase's record and generalises well beyond it: **corroboration is not evidence when every
corroborator is quoting the same source.** Four features restated one unverified claim until
it looked settled; a `grep` refuted it at any point. That is now in the learnings.

The irony is worth stating plainly rather than scoring points with: **this record contains
its own instance of the pattern.** Gaps §5 asserts `opencode/skills/` and `codex/skills/`
"do not exist" — a claim that is false, that one `ls` refutes, and that appears in the same
document that diagnoses the four-feature chain of unverified restatement (Issue #5). It is
harmless — it *understates* the guard's coverage — but it is the same failure mode, one
paragraph away from its own diagnosis. Left open as a record correction.

## Remaining Concerns

- **Issue #1 and #3 are the reason to distrust "the suite is green" as a phase-exit
  signal.** Both were reported as verified and both were false. The suite is now genuinely
  green, measured twice, but the recurring lesson is that a *reported* count is a claim of
  the same kind as a count in a README — and this phase now has an unbroken record of those
  claims being wrong until independently re-measured.
- **Issue #5** — record correction only; the guard is stronger than documented.
- **Issues #7, #8** — pre-existing wrong counts (`16` skills vs 24 on disk; orchestrator and
  visible-agent counts). Deliberately left open: AC6b scopes to counts *this phase* makes
  false, and I followed the implementer's own Gaps §4 precedent rather than widening scope
  mid-review. Both need an owner. #8 additionally needs a *definition* reconciled — two
  surfaces disagree on what "orchestrator" means.
- **Issue #9** — `04-phase-execute.agent.md:176`. A reader looking up "Phase Final Review"
  finds nothing. Correctly diagnosed as a name collision and correctly left out of scope.
- **Issue #6** — Low, declined.

## Test Coverage Assessment

- **Covered:** AC5, AC6, AC6b (after fix), AC6c, AC7, AC8 — all mutation-verified by me
  independently, not accepted from the record.
- **Missing:** AC1, AC2, AC3, AC4 — **not coverable by any automated test.** These require a
  live seven-evaluator fan-out with runtime observation. No static test can substitute, and
  the plan says so explicitly.
- **Suite:** `1 failed (PERF-01 only), 582 passed, 106 subtests` — stable across two
  consecutive runs.

**AC9 reconciliation, corrected and measured (not predicted):**

```
561  baseline passed (6bb7e23)
+20  new tests in tests/test_retirement_reconciliation.py
 -1  test_no_tracked_file_references_a_retired_agent flipped to FAILING
     (the new file's docstring, visible to the sweep only once committed)
=580 == measured passed at 3cd47e5   [record claimed 581 with 1 failed; actual was 2 failed]

580  measured at 3cd47e5
 +1  Issue #1 fix: the sweep test passes again
 +1  Issue #3 fix: test_codebase_context_source_agent_count_matches_disk added
=582 == measured passed at review HEAD, 1 failed (PERF-01)

108  baseline subtests
 -2  test_marker_guard_matches_every_real_generated_file: a 2-item subTest loop
     over ("README.md", "single-feature.md") collapses to one assert once
     single-feature.md is deleted   [VERIFIED — the record's explanation is correct]
=106 == measured
```

The −2 subtest explanation **checks out**; I verified it against
`tests/test_propagate_master_assets.py`. The passed-count reconciliation did not.

## Risk Summary

- **The phase is NOT GO.** AC1–AC4 are unexecuted. The assembled agent family has never run
  end to end — not in this feature, not in this phase, and per the record, not ever. Every
  precondition is now met for the first time, so the run is finally possible. Until it
  happens, the phase has eight green features and no evidence the thing works. This is a
  deliberate decision someone must make explicitly, not a detail to be carried by an
  approval.
- **`dev/feature/08-.../08-retirement-reconciliation-implementation.md` overstates its test
  result.** Anyone consuming that record downstream should use this one's corrected
  reconciliation. The pre-commit/post-commit sweep visibility gap is a real trap that will
  recur for any future test file naming a swept identifier.
- **AC6b's coverage was the thinnest surface in the feature and is now the best-guarded.**
  Four false claims shipped behind a guard written specifically to prevent them.
- **Two pre-existing count claims remain false** (`docs/CODEBASE_CONTEXT.md:17,87-88`;
  `README.md:18`) with no owner. They are the same defect class this feature exists to
  close, deferred only because this phase did not falsify them.
- **The propagation non-idempotence defect is real and correctly deferred.** Identifier
  resolution reads on-disk stems, so a reclassification needs multiple runs to converge —
  this tree needed three. `test_committed_tree_is_at_a_propagation_fixed_point` correctly
  asserts the *settled state* rather than trusting "I ran the propagator," which is the
  right shape for a defect that cannot be fixed here.
</content>
