# Review Record: 04 PR Review Orchestrator

## Summary

The rescope of `05 Phase - Final Review` into `05 PR - Review` is sound, and the
deletions — the point of the feature — are genuinely gone rather than reworded.
Verified by execution, not by reading: the machinery token counts drop to zero
against the old body (`subphase` 20 -> 0, `write-back` 5 -> 0,
`ledger-commits.jsonl` 2 -> 0, `PHASE_0N_SUMMARY` 1 -> 0, `restore` 1 -> 0), and
every attempt to reintroduce each piece is caught by a test.

The implementation record is unusually honest and largely survived re-execution.
Its central self-report — "two of my guards were inert; mutation testing caught
them; 20 mutations all caught" — is true but **under-powered**. I ran an
independent 51-mutation sweep and found **five more inert guards of exactly the
same class the implementer had already identified and fixed twice**. They fixed
the two instances they found; they did not sweep the class. All five are now
fixed and re-verified by mutation.

Everything the orchestrator asked me to adjudicate held up under execution except
that one item.

## Verdict

**Approved with Reservations**

The reservations are all deferred-by-necessity rather than unaddressed: AC13's dry
run is impossible until wave 6, and the report-root split is owned by features
05-07. Neither is fixable from this feature.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Met | `.github/agents/05-pr-review.agent.md:1-6` | `git mv` preserved rename. `name: 05 PR - Review`; the ` - ` separator is load-bearing against `_rewrite_agent_references`' unanchored replace — mutation to `PR Review` is caught. |
| AC2 | Met (static) | `:31-59` | Three questions in one block; no-prompt rule names all four tempting paths. Mutations deleting the rule, dropping the PR-comment question, and licensing a prompt on evaluator failure are all caught. **Live single-interaction proof is manual QA, not run.** |
| AC3 | Met | `:69-84` | Order verified by mutation: reorder, rank swap, and dropped fallback all caught. The implementer's section-scoped rewrite of this guard is genuine. |
| AC4 | Met | `:86-107` | **Verified live.** `git merge-base HEAD repo_improvements_project` -> `ae9823a` and `git merge-base HEAD origin/repo_improvements_project` -> `ae9823a`, while `git merge-base HEAD main` -> `e3398c7`. Both self-refs return the branch tip, not a real base; embedded evidence is accurate as measured at `ae9823a`. |
| AC5 | Met (guard was inert; **fixed**) | `:109-119` | Contract text was always correct. **Both halves of its guard were inert** — see Issue #1. Fixed and re-verified. |
| AC6 | Met | `:121-135` | Override propagation + the no-merge-base stop. Mutations stopping the override at the orchestrator and fabricating a range are both caught. |
| AC7 | Met | `:137-154` | Root is SHA + UTC timestamp, no branch component. Branch-name injection into the root is caught; so is regressing to the retired root. |
| AC8 | Met | whole rewrite | Machinery gone, not reworded — token counts above. Three residual words (`ledger`, `archive`, `PROJECT_ROADMAP.md`) are the absence being *stated*, which is what stops re-invention. I read AC8's "in any form" as governing machinery, not vocabulary; the prohibition is worth more than the purity. |
| AC9 | Met (guard partly inert; **fixed**) | `:21-25` | `PROJECT_ROADMAP.md` appears once, inside the prohibition, asserted as such. The `advisory` half of the guard was inert — Issue #3. |
| AC10 | Met | `:5,185-202` | Three positions, fan-out is six incl. `04e`. Flattening, dropping `04e`, and demoting the `05a`-stops-the-run rule are all caught. |
| AC10b | Met | `.gitignore:10-16` | Fixture tracked (`git ls-files` confirms), run output ignored (`git check-ignore` confirms via `.gitignore:14`). Un-ignoring run output is caught. |
| AC11 | Met (guard partly inert; **fixed**) | `:230-273` | Bounded wait, status records, GO-never-with-missing-check all present and mutation-caught. The `evaluator-status.jsonl` append rule guard was inert — Issue #2. |
| AC12 | Met | `:16-19,204-228` | Read-only, 10-line cap, one-way output, no model identity. All four mutation-caught. |
| AC13 | **Partial — dry run unverified, and legitimately deferred** | `dev/pr-review/fixtures/pinned-diff-range.md` | Fixture is genuinely PR-shaped and pinned: 26 files / 1288 insertions / 3 commits, `git merge-base e6ff28a f5ab960` -> `f5ab960`, so it is a real base/head pair. **Dry run not executed.** See Adjudication below — this is impossible, not skipped. |
| AC14 | Met | generated roots | All four stale outputs absent; propagation at a fixed point. No stale `phase-final-review` refs survive in any agent, skill, or generated asset. |

### Adjudication: AC13 is legitimately deferred, not shipped short

The orchestrator asked me to decide explicitly. **Shipping AC13 partial is correct
here, and the dry run must not happen now.**

The recorded contract — *a fixture dry-run is required release evidence; a run
whose required evaluators are recorded `not-run` is below-GO evidence, not a
passing run* — is what settles it, in the opposite direction from how it first
reads. I verified by execution that **five of the eight roster names do not
resolve to any agent on disk**:

```
'05c Artifact Sweeper'      -> UNRESOLVED (forward ref)
'05d Consistency Auditor'   -> UNRESOLVED (forward ref)
'05e Dependency Auditor'    -> UNRESOLVED (forward ref)
'05f Test Health'           -> UNRESOLVED (forward ref)
'05g Readiness Synthesizer' -> UNRESOLVED (forward ref)
```

A dry run executed today would record five of six fan-out evaluators as
`not-run`. By the orchestrator's own AC11 semantics that caps the verdict at
NO-GO **by construction**. It would produce below-GO evidence and prove nothing
about the thing AC13 exists to prove. Running it now would be theatre that
manufactures a passing-looking artifact from an unrunnable roster — the precise
failure the contract is written against.

One thing worth recording that the implementer did not check: the forward
reference is **safe**, not merely unresolved. `05g Readiness Synthesizer` does
not mis-bind to the existing `05g-artifact-sweeper.agent.md`, because the
propagator resolves `agents:` by display name and that file's name is `05g
Artifact Sweeper`. A slug-based resolver would have silently bound the synthesis
position to the artifact sweeper. It doesn't. Confirmed by execution.

**Routing:** the dry run is feature `08-retirement-reconciliation`'s (wave 7),
which already owns verifying the roster resolves. It is the first point at which
the run is possible.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | AC5 guard inert in **both** halves: `squash-merged base` also occurs at `:133` (the no-merge-base section), so deleting the AC5 bullet left a stray occurrence and the assert passed over a missing case; `first-class` also occurs at `:109` in the section's own heading, so demoting the rule below it passed too | High | `tests/test_pr_review_orchestrator.py:445-454` | AC5 | **Fixed** |
| 2 | AC11 guard inert: `evaluator-status.jsonl` occurs twice (`:244` append rule, `:261` collection), so deleting the rule that *writes* the records stayed green — leaving an agent that reads a file it never writes | Medium | `tests/test_pr_review_orchestrator.py:605` | AC11 | **Fixed** |
| 3 | AC9 guard inert: `advisory` occurs in frontmatter `description:` (`:3`) as well as the body rule (`:23`), so deleting the body rule stayed green | Medium | `tests/test_pr_review_orchestrator.py:343` | AC9 | **Fixed** |
| 4 | Cleanliness guard inert: both skill names occur in the invocation shape (`:223`), so deleting the orchestrator's own `Load pr-review-conventions` line (`:27`) stayed green | Medium | `tests/test_pr_review_orchestrator.py:672-673` | — | **Fixed** |
| 5 | AC13 dry run not executed | Medium | `dev/pr-review/fixtures/` | AC13 | **Open — routed to feature 08** (impossible before wave 6; see Adjudication) |
| 6 | Report-root split pinned, not closed: six evaluators still on `dev/phase-final-review/PHASE_0N/` | Low | `.github/agents/05{b,g,h,j,k,l}-*.agent.md` | — | **Open — owned by 05/06/07**, correctly pinned |

Issues #1-#4 are one defect class, not four: **a presence assertion over
whole-document normalized prose is inert wherever the literal occurs twice.** The
implementer found this class twice (AC3's `body.index()`, AC1's string literal),
fixed both instances correctly, and stopped. The fix technique they established
for AC3 — section-scoping — is exactly what #1-#4 needed; it just was not applied
beyond the two cases that happened to surface.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/test_pr_review_orchestrator.py` | `test_the_three_wrong_suggestion_cases_are_named` — scoped to the `Confirm, and make correction first-class` section; now parses the three `- **...**` bullets and asserts exactly three, and checks the first-class rule against the prose above the bullets rather than the heading | 1 |
| `tests/test_pr_review_orchestrator.py` | `test_evaluator_failure_never_aborts_and_never_passes` — asserts the append rule (`append exactly one json object to the current run's`) rather than bare filename presence | 2 |
| `tests/test_pr_review_orchestrator.py` | `test_agent_declares_it_writes_no_status_line_anywhere` — asserts `the readiness report is advisory` against the body after the frontmatter, not the whole file | 3 |
| `tests/test_pr_review_orchestrator.py` | `test_report_templates_and_severity_are_not_restated` — asserts the load instruction, not bare skill-name presence | 4 |

No source file was modified. All four fixes are test-side, and each carries a
comment recording the duplicate-occurrence site that made it inert, so the next
editor cannot re-flatten it by accident.

## Verification Performed

Stated plainly, because static reading proves nothing here:

- **Mutation sweep, independent, 51 mutations** (reviewer-authored harness, not
  the implementer's). Before my fixes: 41 caught, **5 genuine survivors**. After:
  **51/51 caught**, re-confirmed by re-running both rounds. The implementer's
  "20 mutations, all caught" was accurate for the 20 they ran.
- **Merge-base self-exclusion trap — executed**, results in AC4 above. Suggestion
  order `origin/HEAD` -> `origin/main` -> `origin/master` -> candidates confirmed
  by three separate ordering mutations. User correction is first-class in the
  contract text (and now actually guarded).
- **Report-root ledger — executed both directions.** Migrating `05h` to the new
  root trips it; regressing the orchestrator to the retired root is caught
  independently by two other tests, so the ledger **cannot** be satisfied by
  regression. It is structurally a pin (set equality computed from disk, fails on
  addition *and* removal), not an `EXEMPT_FILES` carve-out — that pattern lives in
  feature 02's `tests/test_retired_evaluator_removal.py:65` and is a different
  shape entirely. The implementer's judgement here is correct, and it was the call
  they flagged as most wanting a second opinion.
- **Propagation fixed point — three consecutive runs**, every orphan counter zero,
  `git status` clean each time.
- **Fixture shape — executed.** 26 files / 1288 insertions / 3 commits;
  `git merge-base e6ff28a f5ab960` -> `f5ab960`.
- **Deleted machinery — executed** against the old body at `ae9823a`; token counts
  in AC8 above.

**Not verified, and not verifiable from static review:** the single-interaction
property in a live run, base correction reaching evaluators at runtime,
`origin/HEAD` unset, no-remote fallback, and the dry run. These are the manual QA
items and remain open. The tests assert that the *contract text* says the right
thing; they cannot assert the runtime obeys it.

## Remaining Concerns

- **Issue #5: AC13 dry run** — open, routed to feature 08. Impossible before wave
  6. Adjudicated above; this is the right call, not a concession.
- **Issue #6: report-root split** — open, owned by 05/06/07, correctly pinned
  rather than silently migrated. Until it closes, a real run would route
  evaluators to a root they do not write to — which is a second, independent
  reason the dry run cannot pass yet.
- **All four manual QA items remain open**, including the live single-interaction
  proof. AC2 is the requirement the plan itself flags as most likely to erode
  silently; static guards are necessary but not sufficient for it.
- **`04e` on the top model tier** (implementer's Decisions §4) — a judgement, not a
  derivation, and the implementer flagged it as such. I agree with it: `04e`
  produces security findings rather than aggregating them, which is judgement work.
  No change.
- **PERF-01** fired on every full-suite run I made (12.6-31.5s, all loaded by my
  own ~50 mutation invocations) and even standalone at 0.88s. Known, expected,
  Phase 04's open release blocker. **Threshold untouched; `tests/hooks/` untouched.**

## Test Coverage Assessment

- **Covered**: AC1, AC2 (static), AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC10b,
  AC11, AC12, AC14 — 46 tests in `tests/test_pr_review_orchestrator.py` (42 as
  shipped, plus the strengthened guards), all mutation-verified by me.
- **Missing**: the behavioural half of AC13 and all four manual QA items. No
  automated test can cover these — they need a live run, which needs wave 6.
- **Highest-value test not present**: none that is authorable today. The gap is
  runtime, not coverage.
- **Suite**: 490 collected; 489 passed + PERF-01. Feature-04 modules in isolation:
  77 passed, 17 subtests, no regressions from my fixes.

## Risk Summary

- **`tests/test_pr_review_orchestrator.py` — the whole module is prose assertions
  over a Markdown body, and that genre has exactly one failure mode: the assertion
  that is satisfied by an occurrence other than the one it means.** Five of them
  shipped. The class is now swept, but every future addition to this module
  reintroduces the risk, and only mutation testing detects it — review does not,
  and the implementer said so first.
- **AC2's unattended-run property is guarded only in text.** The tests prove the
  agent *says* it never asks again. Whether the runtime obeys is unproven until a
  live run exists. This is the requirement the plan predicts will erode one
  reasonable question at a time, and it is the one with the weakest evidence.
- **The roster is a forward reference to five agents that do not exist.** Verified
  safe today (no display-name mis-binding), but nothing re-checks that until
  feature 08. If a wave-5 feature names an evaluator `05g Readiness Synthesizer`
  while `05g Artifact Sweeper` still exists, the display-name resolution is what
  keeps them apart.
- **`.github/agents/README.md` was updated here on contested ownership** (04 vs
  08). Correct call — the rename is what invalidated the rows — but feature 08
  should expect the rows already fixed.
