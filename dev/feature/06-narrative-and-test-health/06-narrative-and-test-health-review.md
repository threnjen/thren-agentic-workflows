# Review Record: 06 Narrative and Test Health

## Summary

Reviewed the rename `05h-test-health` → `05f-test-health` and the rescope of both
judgment-shaped evaluators (`05b-change-narrator`, `05f-test-health`) from a
whole-phase framing to the branch diff `<merge-base>..HEAD`, at commit `8d2063e`
against feature 05's review at `f835b04`.

The implementation is sound and the agent prose is clean. All four adjudications
this review was asked to make resolve in the implementer's favour, each verified
by execution rather than by reading. **The one thing that did not hold is the
implementation record's claim of "50/50 mutations killed; zero inert."** An
independent 55-mutation sweep found **4 inert guards** — all four sharing the
exact root cause the record says was eliminated. All four are fixed; the sweep now
kills 55/55.

Nothing here required rearchitecting. No agent prose was changed by this review;
only test assertions were strengthened.

## Verdict

**Approved with Reservations**

The reservations are not defects in the shipped agents — they are (a) an
inaccurate verification claim in the record, now corrected by execution, and (b)
AC5b/AC3 remaining genuinely unverified pending manual QA, which the record itself
states plainly and correctly.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Met | `.github/agents/05f-test-health.agent.md:2` | `git mv` preserved history. `name: 05f Test Health` matches feature 04's forward reference at `05-pr-review.agent.md:5` exactly. Verified no `05h` identifier survives in either agent. |
| AC1b | Met | `05b:3`, `05f:3` | `description:` rescoped on both. Subphase attribution gone from frontmatter. Guard is whole-file via `_prose()`, so it genuinely covers frontmatter — verified by mutating the `description:` line specifically (killed). |
| AC2 | Met | `05b:3,35,69` | `"subphase"` occurs nowhere in either file. Mutation-verified in both body and description. |
| AC3 | **Met (contract) / Unverified (quality)** | `05b:9-11,71-72` | The contract that an intent account is required, and that unsupported intent must not be invented, is pinned and mutation-verified. **Whether a real narrative is actually about what the branch is *for* is not verified and cannot be from static review — requires a dry-run against the pinned fixture and human judgment.** Correctly declared as manual QA. |
| AC4 | Met | `05b:46-62` | Chunking is structural, not advisory: bounded chunks, never-load-full-diff, per-directory readers, stated serial fallback. All mutation-verified. |
| AC5 | **Met (declaration only)** | `05f:5,36-53` | Declaration pinned. `agents: [Test - Analyst]` exact; delegate's `name:` verified live at `test-analyst.agent.md:2`. **Runtime delegation is NOT verified — see AC5b.** The bare-token weakness in this guard is Issue #1, now fixed. |
| AC5b | **Unverified — requires runtime transcript** | `05f:47-53`, `05b:53-57` | Declaration is present and mutation-verified. **Verification requires a Codex runtime transcript showing the child spawn; not performed.** Adjudicated below — the implementer's deferral is correct, not evasive. |
| AC6 | Met (with recorded degradation) | `05f:26-34,55-74` | Coverage delta / redundancy / flake sections present with evidence-source naming. Degradation to not-measurable is sound — adjudicated below. |
| AC7 | Met | both bodies | Both defer the report path to `pr-review-conventions` rather than restating it; both declare the ≤10-line return and detail-on-disk. Retired root absent from both. |
| AC8 | Met | `tests/test_propagate_master_assets.py:45`, generated roots | Verified by execution: propagator at a genuine fixed point (pass 1 all-zero counters, tree clean). `opencode/agents/05h-test-health.md` absent; `05f-test-health.md` present. Claude/Codex stems stable at `z-test-health` as predicted. |
| AC9 | Met | `tests/test_propagate_master_assets.py:45` | Verified by mutation both directions: adding `execute` to `05f` fails the exact-equality grant assertion; removing `05f` from the roster fails the enumeration assertion. |

### Verified by execution vs. inferred

Verified by running: AC1, AC1b, AC2, AC4, AC6, AC7, AC8, AC9, AC5's declaration,
the ledger reconciliation, the propagation fixed point, and every guard's
liveness (55 mutations).

**Not verified, requiring runtime/manual confirmation:** AC5b (needs a Codex
transcript proving the depth-2 spawn occurred) and AC3's narrative quality (needs
a dry run plus human judgment). Neither is claimed as met.

## Adjudications

### 1. The report-root ledger was shrunk — legitimate, verified by execution

**Resolved in the implementer's favour.** The claim was tested, not accepted.

`EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION` at
`tests/test_pr_review_orchestrator.py:57-59` is not a hand-maintained allowlist.
The assertion at `:575` derives `still_retired` from disk by globbing
`.github/agents/05*.agent.md` and grepping for the retired root, then asserts
**exact set equality**. That is two-sided: shrinking the expected set does not
carve a hole, because any agent that regresses to the old root re-enters the
derived set and fails the test.

Verified by mutation:

- Regressing `05f-test-health` to the retired root → **fails**, reporting
  `05f-test-health.agent.md` as an extra item.
- Regressing `05b-change-narrator` to the retired root → **fails**.

The backing assertions are separate and untouched by this feature: the
orchestrator's root (`:524`) and the skill's root (`:542`) are independently
asserted, so the ledger cannot be satisfied by regressing them instead. The test's
own docstring states the design intent — an empty set means the migration is
complete and the test can be deleted — and feature 07 owns the last entry.

This is the ledger working exactly as designed. Migrating an agent is *supposed*
to trip it and be reconciled here. Shrinking the set is the required reconciliation,
not a weakening.

### 2. AC5b and the Codex delegation trap — the deferral is the right call

**The implementer's honesty is correct, and nothing stronger is achievable
statically.** I checked rather than assumed.

`.github/learnings/debugging-learnings.md:25-38` and the generated Codex artifacts
confirm `max_depth` is a **global `~/.codex/config.toml`** setting (`[agents]
max_depth = 2`), **not a per-agent TOML field**. The propagator emits no such key
and none of the three roots can carry one. A repository test cannot assert on an
operator's home-directory config, so there is no static artifact in scope that
could pin the runtime contract.

That establishes the limit: any static assertion can only confirm the body *says*
it delegates, which passes in precisely the failure case (blocked spawn → silent
inline fallback → reports success). `test_delegation_is_declared_not_inlined` and
`test_test_health_names_the_max_depth_fallback` are correctly labelled as
declaration assertions, in both their docstrings and the module docstring, and the
record does not overclaim them anywhere I could find. The AC coverage matrix marks
AC5b "Verification deferred to manual QA" rather than Done.

The strongest thing achievable statically is what was built: name the default,
name the required value, name the silent-fallback mechanism, and forbid continuing
inline. All four are now pinned as distinct single-occurrence claims.

One residual, correctly scoped away: the operator requirement `[agents] max_depth = 2`
is named in both agent bodies but not recorded in operator documentation. Feature
08's reference sweep owns that. Logged to cross-phase decisions.

### 3. Guards are not inert — 4 found, contradicting the record

**This is the one adjudication that went against the implementation record.**

I ran an independent 55-mutation sweep (harness:
`scratchpad/rev06_mutate.py`, not committed — a verification tool, not a
deliverable; restores the tree after every mutation and leaves it clean). Result
on the as-shipped tree: **51 killed, 4 INERT, 0 invalid.**

The record claims "50/50 mutations killed their guard; zero inert." That claim is
**not accurate**. All four inert guards share the *identical* root cause the record
identifies and says it eliminated — asserting a phrase exists *somewhere* when it
occurs in several places, so deleting the load-bearing occurrence stays green. The
implementer fixed five instances of this pattern and missed four more, evidently
because their mutations targeted the phrase each guard intended to pin rather than
testing whether the *imperative sentence itself* could be deleted or reversed.

| Guard | Token | Occurrences | What stayed green |
|---|---|---|---|
| `test_delegation_is_declared_not_inlined` | `"delegate"` | **13** in `05f` | Reversing the AC5 imperative to "**Perform** coverage, redundancy, and flake-candidate analysis" — i.e. the exact silent-reimplementation failure AC5 exists to catch |
| `test_test_health_preserves_the_not_run_ceiling` | `"not run"` | 2 | Deleting the rule requiring a NOT RUN entry with a concrete reason |
| `test_narrator_frames_the_comparison_as_the_branch_diff` | `"<merge-base>..head"` | 3 in `05b` | Deleting the assigned-scope statement entirely |
| `test_both_agents_defer_the_report_path_to_the_conventions_skill` | `"pr-review-conventions"` | 2 in `05b`, 1 in `05f` | Deleting `05b`'s skill-load line. Inert on `05b` only — which is why a `05f`-targeted mutation missed it |

The first is the serious one: with the token appearing 13 times, `assert "delegate"
in body` **cannot fail under any mutation**. It is unconditionally true. The
headline contract of the feature — AC5, "demonstrably delegates" — had its central
imperative unpinned.

All four fixed by re-anchoring on single-occurrence load-bearing claims, using the
same technique the implementer applied to the five they self-caught. Re-ran the
sweep: **55/55 killed, 0 inert, 0 invalid.**

### 4. The `05f` coverage-measurement resolution — sound

**Resolved in the implementer's favour, verified by execution.**

The reasoning chain checks out: `test-analyst.agent.md:4` holds
`tools: [read, search, edit, fetch]` — no `execute`. `05f` holds
`[agent, read, search, edit]` — no `execute`. So no agent in the delegation chain
can run a coverage tool. The conclusion follows: a *measured* delta exists only
when the orchestrator supplies coverage evidence for both revisions; otherwise
not-measurable plus the structural suite delta derived from reading both trees.
That is precisely the degradation the plan named as preferable
(`plan.md:202-208`), and it is honest rather than convenient — it reports less,
not more.

The distinction the implementer drew is also correct: `test-analyst` **can** be
pointed at `05a`'s baseline worktree (a worktree is just readable files, and
nothing in its contract pins it to the repo root), it simply cannot *measure*
coverage there.

**Does AC9's no-execute grant genuinely block `05f` growing a coverage runner?**
Verified by mutation, both directions:

- Adding `execute` to `05f`'s `tools:` → `test_pr_review_evaluator_tool_grants_match_expected_lists`
  **fails** on exact list equality (`tests/test_propagate_master_assets.py:166`).
- Deleting `05f` from the roster to dodge that → `test_pr_review_evaluator_roster_is_fully_enumerated`
  **fails**, because the roster is derived from disk via
  `_discover_pr_review_evaluator_slugs()`.

So the escape hatch is closed on both sides. The grant is a structural constraint,
not a promise. As the record observes, the security posture and the design
constraint here are the same fact.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | `assert "delegate" in body` cannot fail — token occurs 13× in `05f`. AC5's delegation imperative was unpinned; reversing it to "Perform coverage analysis" left the guard green | High | `tests/test_narrative_and_test_health_agents.py:149` | AC5 | **Fixed** |
| 2 | `assert "not run" in body` inert — "NOT RUN" occurs twice; deleting the NOT RUN entry requirement stayed green | Medium | `tests/test_narrative_and_test_health_agents.py:182` | AC5 | **Fixed** |
| 3 | `assert "<merge-base>..head" in body` inert — occurs 3× in `05b`; deleting the assigned-scope statement stayed green | Medium | `tests/test_narrative_and_test_health_agents.py:264` | AC2 | **Fixed** |
| 4 | `assert "pr-review-conventions" in text` inert on `05b` — occurs twice there; deleting the skill-load line stayed green | Medium | `tests/test_narrative_and_test_health_agents.py:385` | AC7 | **Fixed** |
| 5 | Implementation record states "50/50 mutations killed; zero inert" — contradicted by execution (4 inert found). The verification was less rigorous than claimed | Medium | `06-narrative-and-test-health-implementation.md:24,113` | — | **Open** (documented; record is historical) |
| 6 | `.github/agents/README.md:169` still catalogues the retired **05h Test Health** slug | Low | `.github/agents/README.md:169` | AC8 | **Wont-Fix** — verified feature 08's AC5/AC6 (`08-...-plan.md:46-48`) explicitly own this sweep. Correct scope discipline. |
| 7 | `.github/learnings/cross-phase-decisions.md:32,50` describe the old `05h`-era roster and ledger | Low | `cross-phase-decisions.md:32,50` | — | **Wont-Fix** — historical decision records; accurate as history. |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/test_narrative_and_test_health_agents.py` | `test_delegation_is_declared_not_inlined` — replaced the bare `"delegate"` token check with the full imperative and its objects/target: `delegate coverage, redundancy, and flake-candidate analysis to \`test - analyst\``. Comment records why the bare token cannot fail. | 1 |
| `tests/test_narrative_and_test_health_agents.py` | `test_test_health_preserves_the_not_run_ceiling` — anchored on the rule requiring the entry (`write a report with a not run entry and concrete reason`) plus `missing analysis is never a clean result`, instead of the twice-occurring token. | 2 |
| `tests/test_narrative_and_test_health_agents.py` | `test_narrator_frames_the_comparison_as_the_branch_diff` — pinned both positions that must hold: the assigned-scope statement and the reconciliation step that ranges the narrative. | 3 |
| `tests/test_narrative_and_test_health_agents.py` | `test_both_agents_defer_the_report_path_to_the_conventions_skill` — pinned the load instruction itself rather than the bare token. | 4 |

**One file edited. No agent prose was modified by this review.** Every fix
strengthens an assertion; none weakens, removes, or exempts anything. Each guard
now pins strictly more than it did before.

Explicitly **not** done, per scope constraints: the 50 ms PERF-01 threshold was not
touched, `tests/hooks/` and `.github/hooks/` were not touched, nothing was added to
`EXEMPT_FILES`/`EXEMPT_SKILL_DIRS`, no tool grants were widened, and
`claude/agents/single-feature.md`, `tests/test_readiness_synthesis_agents.py:16`
and `dev/phase-final-review/fixtures/` were left alone.

## Remaining Concerns

- **Issue #5: the record's "zero inert" claim is inaccurate.** Now corrected by
  execution and logged to the ledger. The pattern worth carrying forward: a
  mutation sweep that only mutates the phrase each guard *intends* to pin will
  systematically miss guards whose assertion is satisfied by an incidental
  occurrence elsewhere. The sweep must also try to delete or reverse the
  load-bearing sentence itself.
- **AC5b remains unverified and will stay that way until a Codex dry run.** The
  static surface is exhausted; this is a genuine limitation, not an omission.
  Manual QA must inspect a transcript for the child invocation. A green suite here
  means nothing about AC5b, and the record says so.
- **AC3's narrative quality is unverified.** Requires a dry run against
  `dev/pr-review/fixtures/pinned-diff-range.md` plus human judgment.
- **No dry run was performed** in this feature (record Gap #3), so Stage 4's
  runbook check ("two reports produced") is outstanding.
- **`[agents] max_depth = 2` is an operator prerequisite** named in both agent
  bodies but not yet in operator docs — feature 08's sweep.

## Test Coverage Assessment

- **Covered (automated, all mutation-verified live):** AC1, AC1b, AC2, AC4, AC6,
  AC7, AC8, AC9, and AC5's *declaration*.
- **Not covered, by necessity:** AC5b's runtime delegation — provably not
  statically detectable, since `max_depth` lives in operator config outside the
  repo. AC3's narrative quality — judgment, not assertion.
- **Highest-value test not present:** a runtime transcript assertion for the
  depth-2 spawn. It cannot be built from repository artifacts; it belongs to
  manual QA or to a future harness that captures Codex transcripts.
- **Suite after fixes:** `1 failed, 536 passed, 108 subtests passed in 12.14s`.
  The single failure is PERF-01
  (`tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms`),
  a pre-existing deterministic latency failure on code predating this phase and
  Phase 04's open release blocker. Not attributable to this feature; untouched.
  Treated as green per the orchestrator's verified baseline.
- **Propagation:** verified at a genuine fixed point by execution — all `*_changed`
  and `*_orphans_removed` counters zero on a fresh run, tree clean afterward. No
  orphans survive in any of the three generated roots. The `Test - Analyst`
  delegation reference resolves live in all three (`z-test-analyst` in Claude and
  Codex, `test-analyst` in OpenCode), confirming it ships as a reference rather
  than literal prose.

## Risk Summary

- **`tests/test_narrative_and_test_health_agents.py` — the inert-guard pattern is
  systemic across this phase, not a one-off.** Five were self-caught here, four
  more found at review, and prior features had five found only at review. Every
  guard in this family asserts on prose, and prose repeats itself; short-phrase
  membership checks are the default failure. Captured as a durable learning.
- **AC5b is a real, live runtime risk that no green suite will ever reveal.** A
  blocked depth-2 spawn produces a plausible, confident, wrong test-health report
  and reports success. The mitigation is entirely operator configuration
  (`[agents] max_depth = 2`), which nothing in the repo can enforce.
- **`05f` is 86 lines and thin.** Checked for leaked analysis procedure: none. The
  body explicitly states no local scan or test-analysis procedure is defined and
  that analysis belongs to the delegate. Growth is attributable to required
  content (branch scope, `max_depth` trap, evidence-source naming).
- **`05b:53-62`'s max_depth paragraph permits inline work as the stated serial
  fallback while forbidding whole-diff reads.** Reviewed the wording specifically
  as flagged. The distinction holds: the inline path is admissible *only* as "the
  stated serial fallback above, one bounded chunk at a time" and is explicitly
  "never a licence to read the whole diff at once." Both clauses are now
  mutation-pinned. It cannot be read as licence to skip chunking.
- **Coverage delta will be not-measurable in the common case.** Correct and
  honest, but consumers should expect a structural delta rather than a numeric one
  unless the orchestrator supplies coverage evidence for both revisions.
