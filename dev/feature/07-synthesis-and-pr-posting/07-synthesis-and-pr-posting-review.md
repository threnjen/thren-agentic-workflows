# Review Record: 07 Synthesis and PR Posting

## Summary

The feature is substantively correct and unusually honest. The rename, rescope, posting
path, consent contract, and propagation all land as specified. Three of the five items
this review was asked to adjudicate came back clean on execution, and two of those were
adjudications the implementer could easily have faked and did not:

- **P5-SEC-02 is genuinely recorded OPEN** with a named owner and routing, not closed by
  firming up prose. The agent's own **Trust Boundary** section names the gap and instructs
  against resolving it by tightening prose. Mutation-verified: changing the declaration to
  "closed" trips `test_p5_sec_02_is_recorded_open_in_the_synthesizer`.
- **The converted report-root ledger genuinely trips.** Regressing `05g` to the retired
  `dev/phase-final-review/PHASE_0N/` root fails
  `test_report_root_migration_cannot_split_silently`. It is a live guard, not decoration.
- **The AC5 deviation is correct and well-judged.** Deleting the orchestrator's roadmap
  prohibition trips the presence assertion. The plan's literal absence assertion would have
  been *satisfied* by that deletion. The implementer inverted it and documented why.

The one real defect is the phase's recurring one: **my independent mutation sweep found 5
inert guards** the implementer's two rounds (58 mutations, "0 inert at final state") missed
— including one on AC9, the prompt-injection boundary, on the exact path that posts. All 5
are fixed. The implementer's `_assert_once` helper works correctly and is the right
structural fix; it was simply not applied to every load-bearing claim, and their round 2
stopped at the assertions they had already suspected.

## Verdict

**Approved with Reservations**

The reservations are the two unverifiable-by-static-review items, both correctly disclosed
by the implementer and neither a shortfall of this feature: live QA (AC7/AC8 runtime) and
P5-SEC-02 (open by design). No blocker.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 — rename `05l` → `05g` | Met | `.github/agents/05g-readiness-synthesizer.agent.md:2` | `git mv`; no `05l` self-reference survives. Mutation-verified (B8: reverting the display name trips the reachability test). |
| AC2 — reads only reports; inputs pinned to `pr-review-report` | Met (guards repaired) | `05g:28-50` | Contract correct in the body. **Its guards were inert** — see Issues #1, #2. Fixed. |
| AC3 — severity-ordered report at the run root | Met | `05g:18-19`, `05g:23-24` | Mutation-verified (A6). |
| AC4 — `Checks Not Run` mandatory; GO capped | Met | `05g:52-75` | The phase's central safety property. Pinned as whole statements; all mutations caught. |
| AC5 — no status line on any path | Met | `05g:104-112`; `05-pr-review.agent.md:21-25` | Deviation judged **correct** — see Issue #6 (Wont-Fix) and C2 evidence. |
| AC6 — P5-SEC-02 closed **or recorded open** | Met — **recorded OPEN** | `05g:77-85`; `.github/learnings/cross-phase-decisions.md:88-108` | Owner: a future hook-/script-owning phase. Routing: the phase that gains code execution for the PR Review path. Not closed by prose. Mutation-verified (B4, C1, C4). |
| AC7 — posting opt-in, honors upfront choice | Met (statically); **runtime unverified** | `05-pr-review.agent.md:287-350` | Contract assertions pass. **Requires live QA** in a scratch repo to confirm `gh pr comment` resolves the PR from the branch and that *never* issues no syscall. The command guard was inert — Issue #4. Fixed. |
| AC8 — no PR / absent `gh` reported, not errors | Met (statically); **runtime unverified** | `05-pr-review.agent.md:325-338` | Mutation-verified (O1, O2). Runtime behavior requires live QA. |
| AC9 — output to the PR is one-way | Met (guard repaired) | `05-pr-review.agent.md:229-230`, `:345-347` | **The posting path's own one-way clause was unguarded** — Issue #3, the most serious finding. Fixed. |
| AC10 — no new prompt beyond the block | Met | `05-pr-review.agent.md:46-68`, `:61-65` | Single designed exception named as the only one; pinned. |
| AC11 — synthesis tests rewritten | Met | `tests/test_readiness_synthesis_agents.py` | 3 → 28 tests (27 from the implementer + 1 split out by this review). Wrap-coupling replaced with `_prose()`; retired rollups' absence asserted. |
| AC11b — `05d-security-rollup` conditional deleted, not re-keyed | Met | `tests/test_propagate_master_assets.py` | Independently confirmed absent; nothing re-keyed onto the new `05d` (a consistency auditor). |
| AC11c — delete the live counterexample to AC5 | Met | `05g` | Both clauses gone. Mutation-verified (B6: reintroducing the write-back clause trips the test). |
| AC12 — propagates to three roots; `05l` orphan pruned | Met | `opencode/agents/05g-*.md`, `claude/agents/z-*.md`, `codex/agents/z-*.toml` | Propagator re-run: all counters zero. No `05h`–`05l` slug orphan in any root. |

### Verified vs. inferred

**Verified by execution:** the full suite (561 passed, 1 PERF-01 failure); an independent
26-mutation sweep across four rounds — **23 caught, 0 inert** at final state, 3 skipped as
wrap-position duplicates that re-ran successfully under other labels; the propagator fixed
point (two consecutive all-zero runs); the ledger guard; the roster reachability check; and
occurrence counts for every membership assertion in the file.

The sweep deliberately included **negation**, not just deletion (e.g. flipping the
P5-SEC-02 declaration from open to closed, reverting the `05g` display name to its
pre-rename dangling state, reintroducing the retired write-back clause and comment
ingestion) — deletion-only sweeps do not model the regression that actually occurs.

**Not verified — requires runtime/live QA:** AC7 and AC8 runtime behavior. Static reading
confirms the agent *declares* the right contract; it does not confirm `gh` behaves as
described, that *never* issues no network call, or that the report is on disk before the
prompt in a real run. The implementer disclosed this correctly and recommended routing it
to QA with a scratch repo. **That recommendation stands and this review endorses it.**

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Skill-load directives unguarded: `pr-review-conventions` occurs 2x and `pr-review-report` 3x in `05g`, asserted with a bare `in prose` check. Deleting either load directive left the test green. | High | `tests/test_readiness_synthesis_agents.py:114-115` (pre-fix) | AC2 | Fixed |
| 2 | AC2's input-roster pin to the `pr-review-report` templates could be removed entirely with no test failing — an evaluator could hand the synthesizer arbitrarily-shaped text, which is the same trust gap P5-SEC-02 records. | High | `05g:32-33` guard | AC2 | Fixed |
| 3 | **The posting section's own one-way clause was unguarded.** `test_output_to_the_pull_request_is_one_way` pins feature 04's pre-existing sentence at `05-pr-review.agent.md:229-230`; the clause this feature added at `:345-347` could be deleted with the test green. AC9 is a prompt-injection boundary and it was unguarded on the exact path that posts a comment and gets a URL back. | High | `tests/test_readiness_synthesis_agents.py:500-505` (pre-fix) | AC9 | Fixed |
| 4 | The `gh pr comment --body-file` command — the mechanism AC7 rests on — could be deleted with `test_posting_path_honors_the_three_upfront_consent_settings` green. Every assertion covered the *choice*; none covered the thing the choice actuates. | High | `05-pr-review.agent.md:298` guard | AC7 | Fixed |
| 5 | `REPORT_PATH` is asserted against raw `_body()` rather than `_prose()`, re-introducing wrap-coupling in the file whose docstring exists to explain why wrap-coupling is a defect class. Currently passes (the path does not wrap); would break on a reflow. | Low | `tests/test_readiness_synthesis_agents.py:164` | AC3 | Open |
| 6 | AC5 applied as a presence assertion on the orchestrator rather than the plan's literal absence assertion. | — (deviation, judged correct) | `tests/test_readiness_synthesis_agents.py:301-319` | AC5 | Wont-Fix — the deviation is right; see below |
| 7 | `at most 10 lines`, `top available`, `state-of-the-art` use bare membership checks. Currently each occurs exactly once, so they are live today, but they are the same defect class as #1 waiting on a second occurrence. | Low | `tests/test_readiness_synthesis_agents.py:332-334` | AC11 | Open |

**Issue #6 rationale (Wont-Fix — the implementer is correct):** the plan's test note says
"assert neither `05g` nor the orchestrator references `PROJECT_ROADMAP.md`". Feature 04
names the roadmap *only to prohibit writing to it*. A bare absence assertion would
therefore have been **satisfied by deleting the prohibition** — the test would have
rewarded removing the safety property it exists to protect. The implementer asserted the
prohibition's presence instead and documented the deviation. Verified by mutation (C2):
deleting the prohibition trips the test. This is the correct reading of intent over
letter, and it is exactly the kind of deviation that should be documented rather than
silently applied — which it was.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/test_readiness_synthesis_agents.py` | Replaced the bare `pr-review-conventions` / `pr-review-report` membership checks in `test_readiness_synthesizer_declares_report_only_synthesis_contract` with `_assert_once` pins on the two load directives as whole statements. | #1 |
| `tests/test_readiness_synthesis_agents.py` | Added `test_readiness_synthesizer_pins_its_inputs_to_the_report_templates` — splits AC2's input-roster pin into its own test, pinning the template pin, the `evaluator-status.jsonl` input, and the closed-input-set clause. | #2 |
| `tests/test_readiness_synthesis_agents.py` | Added two `_assert_once` pins to `test_output_to_the_pull_request_is_one_way` covering the posting path's own one-way clause and the no-read-back-to-confirm rule, with a comment recording why feature 04's sentence was insufficient. | #3 |
| `tests/test_readiness_synthesis_agents.py` | Added `_assert_once` pins to `test_posting_path_honors_the_three_upfront_consent_settings` for the `gh pr comment` command and the one-command-three-outcomes constraint. | #4 |

**No agent prose was changed. No assertion was weakened or removed.** Every guard now pins
strictly more than before. Test count 27 → 28.

Explicitly not done, per the orchestrator's standing constraints and my own judgement:
nothing added to `EXEMPT_FILES`/`EXEMPT_SKILL_DIRS`; the 50 ms PERF-01 threshold untouched;
no file under `tests/hooks/` or `.github/hooks/` touched; no shell/`execute` permission
restored anywhere; `claude/agents/single-feature.md` and `dev/phase-final-review/fixtures/`
left alone.

## Remaining Concerns

- **Issue #5 and #7** — Low severity, deferred. Both are latent instances of the defect
  class this file exists to prevent, not live defects. Worth a cleanup pass; not worth
  churning the file now.
- **AC7/AC8 live QA is genuinely outstanding.** The implementer's disclosure is accurate
  and the recommendation to route it to QA with a scratch repo is correct. The two
  Unverified Assumptions from the plan (that `gh pr comment` resolves the PR from the
  branch without a PR number; that a readiness report fits a comment) remain unverified by
  execution. The second is mitigated by the recorded truncation decision, which keeps
  Verdict, Blocking List, and `Checks Not Run` — a good decision, since dropping
  `Checks Not Run` to fit would convert an incomplete run into one that reads as complete.
- **P5-SEC-02 remains open by design**, with a named owner and routing. This is the correct
  outcome, not a shortfall. The generalization the implementer recorded — *"the rebuild
  will bring the validator" is a prediction, not a plan* — is the right lesson and is worth
  carrying forward.
- **PERF-01** remains failing, out of scope, Phase 04's open release blocker.

## Test Coverage Assessment

- **Covered:** AC1, AC2 (guards repaired), AC3, AC4, AC5, AC6, AC7 (contract only), AC8
  (contract only), AC9 (guard repaired), AC10, AC11, AC11b, AC11c, AC12.
- **Missing:** No runtime/integration coverage for AC7/AC8 — the posting path is asserted
  entirely through contract assertions on agent Markdown. This is inherent to shipping
  agent prose and cannot be closed in this repo; it needs a scratch consumer repo.
- **Highest-value test not present:** a live posting dry-run under each of the three consent
  settings, confirming *never* issues no syscall. That is the one property whose whole
  content is a negative, which is precisely the kind that degrades silently.

## Risk Summary

- `tests/test_readiness_synthesis_agents.py` — the inert-guard defect class has now recurred
  in **four consecutive features** (04: 5 inert; 06: 4 inert; 07: 5 inert), every time from
  the same cause, and every time found by the reviewer rather than the implementer's own
  sweep. `_assert_once` is the right fix and works; the gap is that implementers sweep the
  assertions they already suspect. **The sweep must enumerate every assertion mechanically,
  not by intuition.**
- `.github/agents/05-pr-review.agent.md:287-350` — the posting path's correctness rests
  entirely on prose contract assertions. It is well-scoped (one command, three outcomes) and
  resists accretion explicitly, but no test can prove it behaves as written until live QA.
- P5-SEC-02 open: `05g` reduces evaluator claims into a verdict behind metadata-only
  validation. The verdict is advisory and the agent says so plainly — the risk is bounded
  and disclosed, not hidden.
- The consent contract's asymmetry is real and correctly surfaced: a posted PR comment is
  not rolled back by reverting the agent. *Ask when ready* as the recommended default is the
  right call, and the body states the cost of *auto* plainly rather than as a convenience.
