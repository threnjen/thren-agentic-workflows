# 07 Synthesis and PR Posting — Implementation Record

**AC scope this invocation:** AC1–AC12 (all plan ACs, including AC11b, AC11c).
**Status:** Done, with two items explicitly recorded open (AC6 by design; live QA
not performable in this environment).

## Test Results

| Point | Result |
|---|---|
| **Baseline** (clean tree, `c8bb730`) | `1 failed, 536 passed, 108 subtests passed` |
| **Final** | `1 failed, 560 passed, 108 subtests passed` |

**The 1 failure is PERF-01** — `tests/hooks/test_hook_distribution_integration.py::
test_ac9_propagated_guard_median_latency_is_below_50_ms`. It is pre-existing, is not
this feature's, and was confirmed by the orchestrator through direct execution as a
real deterministic latency failure predating this phase (Phase 04's open release
blocker). This feature touched no file under `tests/hooks/` or `.github/hooks/` and
did not alter the 50 ms threshold. Treating `1 failed (PERF-01 only)` as green.

**Pass-count reconciliation, against *passed* (not collected):**

```
536 (baseline passed)
 -3 (tests/test_readiness_synthesis_agents.py: old file had 3 tests, rewritten)
+27 (new file has 27 tests)
= 560  == actual final passed count
```

This is stated explicitly because an earlier implementer on this phase shipped a red
suite while claiming green, having reconciled to *collected* rather than *passed*.

## Sibling Feature Awareness

Read the first 5 lines of each sibling `-plan.md`. Waves 1–6 (features 01–06) have
landed; this is wave 6. **Feature 08 (Retirement Reconciliation, wave 7)** verifies the
whole assembly — `05a`–`05g` in all three roots, no `05h`–`05l` slug surviving — so
this feature's rename and propagation are its direct inputs. `claude/agents/
single-feature.md` is a pre-existing orphan owned by feature 08 and was left alone.
`dev/phase-final-review/fixtures/` is live wiring named by surviving agents, not a dead
planning record, and was left alone.

## Acceptance Criteria Status

| AC | Status | Evidence |
|---|---|---|
| AC1 — rename `05l` → `05g`, name + self-references | Done | `git mv`; `.github/agents/05g-readiness-synthesizer.agent.md`. `test_readiness_synthesizer_is_renamed_to_05g`, `test_readiness_synthesizer_carries_no_05l_self_reference` |
| AC2 — reads only report files; inputs pinned to `pr-review-report` | Done | `05g:29-49`. `test_readiness_synthesizer_declares_report_only_synthesis_contract`, `..._pins_metadata_only_validation`, `..._dropped_retired_evaluators_rollups` |
| AC3 — severity-ordered report at the `dev/pr-review/` run root | Done | `05g:18`. `test_readiness_report_is_written_under_the_pr_review_run_root`, `..._carries_the_three_verdict_values` |
| AC4 — `Checks Not Run` mandatory; GO capped | Done | `05g:61-72`. `test_checks_not_run_section_is_mandatory_and_names_reasons`, `test_go_is_invalid_while_any_check_is_missing`, `test_a_later_success_never_repairs_an_earlier_failure` |
| AC5 — no status line on any path | Done | `05g:104-112`; write-back clause deleted. `test_readiness_synthesizer_writes_no_status_line_anywhere`, `test_orchestrator_writes_no_status_line_anywhere` |
| AC6 — P5-SEC-02 closed **or recorded open** | **Recorded OPEN** (correct outcome) | See "P5-SEC-02" below. `05g:76-85`; `.github/learnings/cross-phase-decisions.md`. `test_p5_sec_02_is_recorded_open_in_the_synthesizer` |
| AC7 — posting opt-in, honors upfront choice | Done | `05-pr-review.agent.md` posting section. `test_posting_path_honors_the_three_upfront_consent_settings`, `test_never_setting_makes_no_network_call`, `test_ask_when_ready_writes_the_report_before_it_prompts`, `test_auto_setting_states_the_consequence_plainly` |
| AC8 — no PR / absent `gh` are reported, not errors | Done | `test_posting_failures_are_reported_conditions_not_run_failures`, `test_posting_never_retries_into_a_prompt`, `test_oversized_comment_behavior_is_decided_not_silent` |
| AC9 — output to PR is one-way | Done | `test_output_to_the_pull_request_is_one_way`, `test_no_agent_body_reads_pr_discussion_back_in` |
| AC10 — no new prompt beyond the block | Done | `test_posting_introduces_no_new_prompt_beyond_the_block` |
| AC11 — synthesis tests rewritten | Done | `tests/test_readiness_synthesis_agents.py` rewritten, 3 → 27 tests |
| AC11b — `05d-security-rollup` conditional **deleted, not re-keyed** | Done (already absent) | Verified absent from `tests/test_propagate_master_assets.py`; reconciled by an upstream feature. Nothing re-keyed. |
| AC11c — delete the live counterexample to AC5 | Done | Both clauses removed. `test_readiness_synthesizer_writes_no_status_line_anywhere` asserts `write-back` and `learnings agent` are absent |
| AC12 — propagates to three roots; `05l` orphan pruned | Done | `test_readiness_synthesizer_propagates_to_all_three_roots`, `test_orchestrator_roster_entry_resolves_to_the_synthesizer_on_disk` |

## Files Changed

### Source of truth

| File | Change |
|---|---|
| `.github/agents/05l-readiness-synthesizer.agent.md` → `.github/agents/05g-readiness-synthesizer.agent.md` | `git mv` + rescope (AC1–AC6). Report root, input roster, Trust Boundary section, `prod-code-review` reframed to a complement, write-back clause deleted, revision-naming added. `tools: [read, search, edit]` carried forward unchanged — no `execute`. |
| `.github/agents/05-pr-review.agent.md` | Added the Posting section (AC7–AC10); auto-consequence warning and the sole-designed-exception clause in the interaction block. |
| `.github/agents/README.md` | Roster row `05l` → `05g`. |
| `.github/learnings/cross-phase-decisions.md` | Recorded P5-SEC-02 **open** with owner + routing (AC6). |

### Tests

| File | Change |
|---|---|
| `tests/test_readiness_synthesis_agents.py` | Rewritten. 3 → 27 tests. `_prose()` normalization replaces the wrap-coupled assertion; `_assert_once()` added. |
| `tests/test_propagate_master_assets.py` | `PR_REVIEW_EVALUATOR_TOOLS`: `05l-readiness-synthesizer` → `05g-readiness-synthesizer`, grant unchanged. |
| `tests/test_pr_review_orchestrator.py` | `EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION` migrated to empty; the ledger test converted to a migration-complete assertion rather than deleted (see Decisions). |

### Generated (propagator output, all counters zero at convergence)

`claude/agents/z-readiness-synthesizer.md`, `claude/commands/pr-review.md`,
`claude/learnings/cross-phase-decisions.md`, `codex/agents/z-readiness-synthesizer.toml`,
`codex/agents/05-pr-review.toml`, `codex/profiles/pr-review.config.toml`,
`opencode/agents/05-pr-review.md`, **`opencode/agents/05g-readiness-synthesizer.md` (new)**,
**`opencode/agents/05l-readiness-synthesizer.md` (deleted — the slug-keyed orphan)**.

Propagator run repeatedly to convergence: all `*_changed` and `*_orphans_removed`
counters zero. OpenCode keys filenames on the source slug and orphaned as predicted;
Claude and Codex key on the stem (`z-readiness-synthesizer`) and survived the renumber
with filenames intact. Verified no slug-keyed orphan survives in `opencode/agents/`.

## P5-SEC-02 — Recorded OPEN (AC6)

**Outcome: open. Owner: a future hook- or script-owning phase. Routing: the same phase
that gains code execution for the PR Review path.**

The recorded finding says P5-SEC-02 "is closed by rebuilding the readiness path **in
code**", and anticipated the rescope *would be* that rebuild. It is not. The rescope
rebuilt the readiness path **as agent Markdown**. `05g` still reduces evaluator *claims*
into a verdict behind metadata-only validation (readable, regular, non-empty, under the
current run root). There is no strict schema and no deterministic status reducer over
structured records, because there is still no code to attach them to.

Closing it here would have required asserting the trust contract more firmly in prose —
exactly the move the Phase 03 scan already faulted, and it would make the record say
closed without closing anything. **This was the expected outcome, stated up front in the
plan (Stage 2), and it is not a shortfall.**

What was done instead of closing it: `05g` names the gap in its own **Trust Boundary**
section, states that metadata validation is *not* claim validation, and instructs
against resolving it by tightening prose — so the agent cannot present a metadata check
as claim validation. That is honest scoping, not closure.

Generalization recorded in learnings: *"the rebuild will bring the validator" is a
prediction, not a plan.* A finding routed to a rebuild must name the capability the
rebuild has to gain; otherwise the rebuild arrives, lacks it, and the finding silently
looks overdue rather than correctly deferred.

## Decisions and Deviations

1. **The report-root ledger was converted, not deleted.** `test_report_root_migration
_cannot_split_silently`'s own docstring said "an empty set means the migration is
complete and this test can go". Feature 07 migrated the last entry (`05l`), so the set
is now empty. Deleting the test would have removed the only guard on the retired root
across `05*` bodies. Instead the set is frozen empty and the assertion inverted meaning:
it no longer records drift, it denies drift exists. Mutation-verified — regressing `05g`
to `dev/phase-final-review/` still trips it. This resolves it by **migrating**, not by
weakening, and adds no exemption.

2. **AC11b needed no work.** The `05d-security-rollup` conditional was already absent
from `tests/test_propagate_master_assets.py`, reconciled upstream. Verified rather than
assumed. Nothing was re-keyed onto the new `05d` (a consistency auditor — a different
agent).

3. **Nothing was added to `EXEMPT_FILES` / `EXEMPT_SKILL_DIRS`.** The retired-name sweep
correctly caught my *own* new test-file docstrings naming retired slugs to explain their
absence. Resolved by rewording the docstrings, not by exempting the file. The sweep was
right.

4. **`execute` narrowing by removal only.** `05g` holds `[read, search, edit]` — no
`execute`, unchanged from `05l`. No shell permission was restored anywhere. `gh` runs
through the orchestrator's existing unrestricted Bash (held already for base derivation),
so it widens nothing. Per-agent command scoping is not expressible in Claude subagent
frontmatter and was not attempted. Mutation-verified: adding `execute` to `05g` trips the
tool-grant ledger.

5. **Oversized-comment decision (recorded, per plan Section B):** post a truncated report
with an explicit truncation notice and the local report path, keeping Verdict, Blocking
List, and `Checks Not Run`. Never truncate silently; never drop `Checks Not Run` to fit,
since that converts an incomplete run into one that reads as complete.

6. **AC5 on the orchestrator asserts presence, not absence.** The plan's test note says
"assert neither `05g` nor the orchestrator references `PROJECT_ROADMAP.md`". Applied
literally to the orchestrator that would be wrong and harmful: feature 04 names the
roadmap *only to prohibit writing to it*, so a bare absence assertion would be satisfied
by deleting the prohibition. `05g` gets the absence assertion; the orchestrator gets a
presence assertion on the prohibition itself. Documented as a deliberate deviation.

## Evidence: Mutation Sweep

Every guard was mutation-tested by changing the thing it claims to check and confirming
the named test fails. Two rounds, **58 mutations, 0 inert at final state**. Harness:
each mutation is applied to a real file, the named test run, the file restored; a
mutation whose test still passes is reported as INERT.

**Round 1 (38 mutations) — 0 inert.** Round 1 mutated one clause per test.

**Round 2 (20 mutations) — found 5 INERT, all now fixed.** Round 2 deliberately targeted
the assertions round 1 did *not* cover, because an untested assertion is where an inert
guard hides. It found exactly the failure mode this phase keeps hitting — asserting a
token that occurs in several places:

| Inert guard found | Why it could never fail | Fix |
|---|---|---|
| `` `GO` `` in body | substring of `` `GO WITH CONDITIONS` `` and `` `NO-GO` `` | pin the whole vocabulary sentence, `_assert_once` |
| `` `NO-GO` `` in body | recurs in several rules | pin the no-evidence sentence, `_assert_once` |
| `Critical` in body | in both the severity list and the sort rule | pin both statements separately |
| `Low` in body | same | pin both statements separately |
| `not-run` in body | recurs in the GO-cap rule | pin the classification rule whole |

Had I reported after round 1 only, I would have claimed a clean sweep that was false in
exactly the reviewer's terms. Both rounds re-run at final state: **0 inert**.

The harness verifies restoration: the working tree was checked for mutation residue
after the sweep (clean), and the propagator re-run to convergence afterward.

`_assert_once` is the structural fix for this defect class and is now the file's default
for any load-bearing claim: it fails on 0 occurrences (clause gone) *and* on 2+
(assertion no longer pins a single statement).

Additional mutation, added after the pre-handoff reachability check:
`test_orchestrator_roster_entry_resolves_to_the_synthesizer_on_disk` — reverting the
agent's display name to `05l Readiness Synthesizer` (the pre-rename dangling state)
fails the test.

## Pre-Handoff Self-Check

1. **Runtime reachability** — The orchestrator's `agents:` roster resolves by display
   name. Feature 04 wrote `05g Readiness Synthesizer` as a *forward reference* that
   resolved to nothing (recorded as safe precisely because nothing bound to it). This
   rename is what makes it bind. The existing orchestrator test only asserts the string
   is present in the roster line — which was already true while it resolved to nothing —
   so a new reachability test was added asserting **every** roster entry resolves to an
   agent's declared `name:` on disk. Mutation-verified.
2. **Per-frame callers** — N/A (not a game/render project).
3. **Event handler completeness** — N/A; the posting path's analogue is covered: each of
   the three consent settings performs its actual action (post / ask-then-post / no call),
   not merely a message.
4. **Test authenticity** — Tests read the real agent files and real generated roots from
   disk; no simplified stand-ins or fixture copies.
5. **Stack-specific rules** — No Unity/tech-stack skill applies (Markdown agents + Python
   pytest). Verified via the recorded Environment State rather than re-derived.

Additional checks:
- **Claude/Codex slug prose.** `claude/commands/pr-review.md` carries `05g-readiness-
  synthesizer` as prose while Claude's agent file is stem-keyed (`z-readiness-
  synthesizer`). Confirmed **pre-existing propagator behavior**, identical for
  `05a-baseline-worktree` and `04e-diff-security-scan`, and owned by feature 04's source
  prose style — not introduced by this rename. Not changed here.

## Keep-It-Clean Checklist (plan Section D)

- [x] `05g` reads reports only — no code, no other agents' internals
- [x] `Checks Not Run` cannot be omitted
- [x] No status-line write-back anywhere
- [x] `never` makes no network call
- [x] P5-SEC-02 explicitly recorded open (with owner + routing)
- [x] Posting stays one command with three outcomes

## Gaps / Not Done

- **Live QA is not performable from this environment** and is left unchecked in the tasks
  file (5 items): posting against a real PR, no-PR, unauthenticated `gh`, and the
  *never*-makes-no-network-call observation all require a **scratch consumer repo**, which
  the plan explicitly forbids doing against this repository. The two Unverified
  Assumptions therefore remain unverified by execution: (a) that `gh pr comment` resolves
  the PR for the current branch without a PR number — the agent documents the no-PR path
  as the failure mode; (b) that a readiness report fits in a PR comment — handled by the
  recorded truncation decision rather than by measurement. All are covered by static
  contract assertions only. **Recommend routing live QA to the QA stage with a scratch
  repo.**
- **AC6 remains open by design.** See above. It is a recorded High finding with a named
  owner, not a shortfall of this feature.
- **PERF-01** remains failing and is out of scope (Phase 04's open release blocker).
