# Implementation Record: 04 PR Review Orchestrator

## Summary

`05 Phase - Final Review` is now `05 PR - Review`: an orchestrator for the diff
between a confirmed base commit and a head commit.

    .github/agents/05-phase-final-review.agent.md -> .github/agents/05-pr-review.agent.md

The deletions are the point of the feature. Gone, in no form: ledger reading
(`eval/runs/*/ledger-commits.jsonl`), multi-run disambiguation, the `eval:`
commit-message fallback, subphase discovery and its refusal message, the
artifact-inventory gate, archive-before-overwrite, and the entire verdict
write-back — the two-file transactional edit of `PROJECT_ROADMAP.md` +
`PHASE_0N_SUMMARY.md` with its unique-match ambiguity detection and
restore-on-second-write-failure. Preflight went from four steps to two. The
agent now writes no status line anywhere; the verdict is the user's.

Four things a reviewer should know up front:

1. **The file grew, 249 -> 284 lines, and the plan predicted subtraction.** The
   deletions were real (~150 lines of machinery), but AC2-AC6 are all *new*
   contract, and base derivation alone is 76 lines because it is the phase's
   central risk. The net is honest, not a failure to delete. See Deviations §1.
2. **The report-root split was live and unpinned, and is now pinned.** The
   orchestrator and both skills are on `dev/pr-review/<sha>-<ts>/`; six
   surviving evaluators still declare `dev/phase-final-review/PHASE_0N/`. That
   is features 05-07's to migrate, so it is recorded as an asserted ledger
   rather than silently left to whoever notices. See Decisions §3.
3. **Two of my own guards were inert and mutation testing caught them**, not
   review. One was the AC3 ordering test. See Reviewer Focus.
4. **Feature 01's pruner removed all four stale generated outputs.** Zero
   hand-deletion. `claude/commands/phase-final-review.md` — the live slash
   command pointing at a deleted agent — is gone via pruning (AC14).

## Sibling Features

Read the first 5 lines of each sibling plan. This is feature `04`, wave 4,
`parallel_safe: no`.

| Sibling | Relationship |
|---|---|
| `01-propagator-orphan-pruning` (wave 1) | **Hard prerequisite; verified working.** AC14 is unachievable without it. Its `claude/commands/` pruning — added specifically for this feature — removed the orphaned command file on the first run. |
| `02-retired-evaluator-removal` (wave 2) | **Prerequisite.** Already trimmed this file's `agents:` roster to the seven survivors. Its `RETIRED_AGENTS` constant is the canonical retired list; my tests needed no retired slugs, so nothing is re-listed. |
| `03-pr-review-conventions-skills` (wave 3) | **Hard prerequisite.** This agent is authored against its report roster, report root, and return contract. `test_orchestrator_report_root_matches_the_canonical_skill_contract` reads the root **out of** its skill rather than restating it. |
| `05-mechanical-evaluators` (wave 5) | Renumbers `05g`->`05c`, `05j`->`05d`, `05k`->`05e`. My `agents:` roster is a **forward reference** to those names. Owns three of the six evaluators in the report-root ledger. |
| `06-narrative-and-test-health` (wave 5) | Renumbers `05h`->`05f`. Owns `05b`/`05h` in the ledger. |
| `07-synthesis-and-pr-posting` (wave 6) | Renumbers `05l`->`05g`, and **edits this same file again** to add the `gh` posting path. AC2c captures the *choice* only; I implemented no posting. Owns `05l` in the ledger. |
| `08-retirement-reconciliation` (wave 7) | Verifies the forward-referenced roster resolves. Owns `claude/agents/single-feature.md` (untouched) and the dead `!dev/phase-final-review/` un-ignore rules (untouched — the old fixture is still tracked). |

**Shared modules**: `tests/test_propagate_master_assets.py` (the phase-wide
sequential bottleneck — I changed one test, lines 187-202). The six surviving
`05x` agent bodies are shared with 05/06/07; **I modified none of them**, only
enumerated them in a test constant.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Rename file + `name:` + `description:` to diff scope | Plan test (new) | Renamed agent exists, old absent, frontmatter restated | Done | `.github/agents/05-pr-review.agent.md:1-5` | `tests/test_pr_review_orchestrator.py::test_orchestrator_is_renamed_and_the_old_source_is_gone`; `::test_frontmatter_declares_the_pr_review_name_and_diff_scope`; `::test_agent_name_does_not_collide_with_prose_in_any_source_asset` | PENDING | PENDING |
| AC2 | Single upfront interaction; no prompt after the block | Plan test 4 | All three questions named in block; no-prompt rule declared | Done | `05-pr-review.agent.md:31-60` | `::test_all_three_questions_are_named_inside_the_upfront_block`; `::test_no_prompt_may_occur_after_the_block` | PENDING | PENDING |
| AC3 | Base suggestion order + derivation source shown | Plan test 3 | Fallback chain in order | Done | `05-pr-review.agent.md:70-85` | `::test_suggestion_chain_appears_in_order`; `::test_derivation_source_is_shown_with_the_suggestion`; `::test_no_remote_falls_through_to_local_candidates` | PENDING | PENDING |
| AC4 | Suggester excludes current branch + its tracking ref | Plan test 2 | Self-exclusion declared | Done | `05-pr-review.agent.md:87-107` | `::test_self_exclusion_is_declared_for_branch_and_tracking_ref` | PENDING | PENDING |
| AC5 | Three wrong-suggestion cases named; correction first-class | Plan test (new) | Three cases present | Done | `05-pr-review.agent.md:109-122` | `::test_the_three_wrong_suggestion_cases_are_named` | PENDING | PENDING |
| AC6 | Override replaces suggestion and reaches every evaluator | Plan test (new) | Override propagation declared | Done | `05-pr-review.agent.md:124-131` | `::test_override_replaces_the_suggestion_and_reaches_every_evaluator`; `::test_absent_merge_base_is_a_stop_not_a_fabricated_range` | PENDING | PENDING |
| AC7 | Report root is SHA + timestamp; no branch component | Plan test 5 | Root declared, no branch name | Done | `05-pr-review.agent.md:137-155` | `::test_report_root_is_sha_and_timestamp_with_no_branch_component`; `::test_collision_policy_is_recorded`; `::test_orchestrator_report_root_matches_the_canonical_skill_contract` | PENDING | PENDING |
| AC8 | Deleted machinery survives in no form | Plan test 1 | Absence assertions | Done | `05-pr-review.agent.md` (whole rewrite) | `::test_no_ledger_machinery_survives`; `::test_no_subphase_discovery_survives`; `::test_no_artifact_inventory_gate_survives`; `::test_no_verdict_write_back_survives`; `::test_no_archive_before_overwrite_survives` | PENDING | PENDING |
| AC9 | Agent writes no status line on any path | Plan test 1 | Absence + declared rule | Done | `05-pr-review.agent.md:21-25` | `::test_agent_declares_it_writes_no_status_line_anywhere`; `::test_no_verdict_write_back_survives` (roadmap-as-target check) | PENDING | PENDING |
| AC10 | Roster in three positions; fan-out is six incl. `04e` | Plan test (new) | Roster declared | Done | `05-pr-review.agent.md:5,185-203` | `::test_roster_declares_three_positions_not_a_flat_range`; `::test_fan_out_is_six_evaluators_including_the_security_seam`; `::test_frontmatter_agents_list_names_the_full_roster_by_display_name` | PENDING | PENDING |
| AC10b | `.gitignore` tracks fixture, ignores run output | Context Discovery Delta | Fixture tracked; report root ignored | Done | `.gitignore:10-16` | `::test_fixture_is_actually_tracked_by_git`; `::test_run_output_root_stays_ignored` | PENDING | PENDING |
| AC11 | Partial-failure semantics; GO never with a missing check | Plan test (new) | Status records + bounded wait retained | Done | `05-pr-review.agent.md:230-274` | `::test_evaluator_failure_never_aborts_and_never_passes`; `::test_bounded_wait_is_retained`; `::test_verdict_can_never_be_go_while_a_check_is_missing` | PENDING | PENDING |
| AC12 | Never reads code/diffs; <=10-line returns | Plan test (new) | Read-only contract retained | Done | `05-pr-review.agent.md:16-19,204-229` | `::test_orchestrator_never_reads_code_or_diffs`; `::test_return_contract_caps_every_subagent_at_ten_lines`; `::test_output_is_one_way_and_never_ingests_pr_comments`; `::test_model_and_harness_identity_stay_out_of_retained_reports` | PENDING | PENDING |
| AC13 | Pinned base/head SHA pair sufficient for a dry run | Code-review evidence + dry-run | Fixture exists, merge-base resolves | **Partial** — fixture pinned and asserted; **dry run not executed** (behavioural, see Gaps §1) | `dev/pr-review/fixtures/pinned-diff-range.md` | `::test_fixture_pins_both_shas_of_a_real_base_head_pair`; `::test_fixture_shas_resolve_and_merge_base_is_the_pinned_base`; `::test_fixture_range_is_pr_shaped_not_a_whole_phase`; `::test_fixture_records_why_the_pair_was_chosen` | PENDING | PENDING |
| AC14 | Propagates to all three roots; stale command absent | Plan test (new) | Outputs present, orphans pruned | Done | generated roots (feature 01's pruner) | `::test_renamed_orchestrator_reaches_all_three_generated_roots`; `::test_stale_generated_outputs_are_absent_from_every_root`; `tests/test_propagate_master_assets.py::...::test_pr_review_agent_is_present_in_all_harness_outputs` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Rename + restate frontmatter | Done | `.github/agents/05-pr-review.agent.md` | `git mv`; rename preserved in history (`R` in status). `name: 05 PR - Review`. See Decisions §1. |
| AC2 | Single upfront interaction | Done | `05-pr-review.agent.md` | Three questions; the no-prompt rule names all four tempting post-block paths. **Live single-interaction proof is manual QA — not run.** |
| AC3 | Suggestion order + source | Done | `05-pr-review.agent.md` | `origin/HEAD` -> `origin/main` -> `origin/master` -> candidates. Guard was inert; fixed. See Reviewer Focus §1. |
| AC4 | Self-exclusion | Done | `05-pr-review.agent.md` | Measured evidence embedded verbatim, including the `origin/`-tracking-ref case. |
| AC5 | Three wrong cases | Done | `05-pr-review.agent.md` | Feature-branch parent, rebase, squash-merge. |
| AC6 | Override propagates | Done | `05-pr-review.agent.md` | Plus the no-merge-base stop. |
| AC7 | Report root | Done | `05-pr-review.agent.md` | Collision policy decided: accept. See Decisions §2. |
| AC8 | Deletions | Done | `05-pr-review.agent.md` | Three residual word-mentions are rationale/prohibition, not machinery — enumerated in Deviations §2. |
| AC9 | No status line | Done | `05-pr-review.agent.md` | `PROJECT_ROADMAP.md` appears exactly once, inside the prohibition; asserted as such. |
| AC10 | Roster, three positions | Done | `05-pr-review.agent.md` | Fan-out is six. `04e` reused; no new security agent. Roster is a forward reference (accepted risk). |
| AC10b | `.gitignore` | Done | `.gitignore` | Mirrors the existing four-rule pattern. |
| AC11 | Partial failure | Done | `05-pr-review.agent.md` | `evaluator-status.jsonl` contract preserved verbatim in force. |
| AC12 | Read-only + <=10 lines | Done | `05-pr-review.agent.md` | Plus the one-way-output rule. |
| AC13 | Pinned fixture | **Partial** | `dev/pr-review/fixtures/pinned-diff-range.md` | Pair pinned, tracked, asserted. **Dry run not executed** — Gaps §1. |
| AC14 | Propagation + pruning | Done | generated roots | All four stale outputs pruned; zero hand-deletion. |

## Decisions

### 1. `name:` -> `05 PR - Review`; test file -> `tests/test_pr_review_orchestrator.py`

Both were `[PROPOSED - name TBD]`. Took the plan's suggestions.

The name matters more than it looks. `_rewrite_agent_references`
(`scripts/propagate_master_assets.py:565`) does an unanchored
`text.replace(agent.name, identifier)` over every source-agent body, so a
generic `PR Review` would rewrite that common phrase throughout this phase's
prose. The ` - ` separator is what makes it collision-safe.

`test_agent_name_does_not_collide_with_prose_in_any_source_asset` enforces this,
and it is **derived, not restated**: it reads the name out of the frontmatter and
checks it against `propagator.load_source_agents()` — the propagator's own
loader — rather than a glob. That distinction is load-bearing. My first version
globbed `.github/agents/*.md`, which flagged `.github/agents/README.md` as a
collision. It is not one: the README carries no frontmatter `name`/`description`,
so `load_source_agents` skips it and it is never rewritten. Naming every agent by
display name is the roster document's whole job. A glob-based test would have
pushed a future implementer to "fix" the README.

Test file is new, pytest-style (module-level `Path` constants + plain `assert`),
per the tasks file's explicit instruction to follow
`tests/test_readiness_synthesis_agents.py` rather than the `unittest` classes of
`test_propagate_master_assets.py`.

### 2. Two runs in the same second -> **accept the collision**

Required to be decided and recorded. A collision means the same base at the same
second — a duplicate run of the same review. A sequence suffix would add a path
component (and a second thing to get wrong) to defend a case whose only outcome
is that a duplicate run overwrites a duplicate report. Recorded in the agent body
and asserted by `::test_collision_policy_is_recorded`.

### 3. The report-root split -> **pinned as an asserted ledger**

The brief is explicit that no test pins either report root and that this feature
is the first that can. The split is live right now:

| Asset | Report root | Owner |
|---|---|---|
| `05-pr-review.agent.md` | `dev/pr-review/<base-sha-short>-<UTC-...>/` | this feature |
| `pr-review-conventions`, `pr-review-report` | same | feature 03 (already landed) |
| `05b`, `05g`, `05h`, `05j`, `05k`, `05l` | `dev/phase-final-review/PHASE_0N/` | features 05, 06, 07 |

Migrating those six from here would collide with all three owning features and
violate this plan's own scope boundary ("do not rescope any evaluator's
internals"). But leaving it unpinned is how the split ships silently: each half
is internally consistent, and every feature in waves 4-6 can assume another owns
it.

So `test_report_root_migration_cannot_split_silently` asserts the **exact set**
of evaluators still on the retired root. It is green today, fails the moment any
evaluator migrates (with a message saying to update the set), and is deleted when
the set empties. Two properties make it a pin and not an exemption:

- It cannot be satisfied by regressing the orchestrator or the skills — those are
  asserted separately to be on the new root, and the orchestrator is explicitly
  excluded from the set.
- It is **not** an `EXEMPT_FILES`-style sweep hole. It carves nothing out; it
  adds an assertion where there was none. (This was the instinct feature 03's
  reviewer had to undo, and I checked mine against it deliberately.)

Mutation-verified: rewriting `05h-test-health.agent.md` to the new root trips it.

### 4. `04e` placed on the top model tier

The table had to be re-derived for the new roster. The renumbering maps cleanly
(`05g`->`05c`, `05j`->`05d`, `05k`->`05e` stay cheap; `05h`->`05f` stays
delegated; `05l`->`05g` and `05b` stay top). `04e` is **new to this table** — the
old one mapped the retired twelve and never included it. I put it on the top
tier: it is the run's only security analysis, and security reasoning over a diff
is judgement work, not a mechanical sweep. The retired `05d-security-rollup` was
"delegated", but it aggregated someone else's findings; `04e` produces them.
Flagging as a judgement call a reviewer may want to revisit.

## Fixture selection (AC13)

**Pinned: `f5ab960..e6ff28a`** — PR #17, `feat/visual-verification-package`.
3 commits, 26 files, 1288 insertions. `git merge-base e6ff28a f5ab960` ->
`f5ab960`, so the pair is genuinely base/head, not two commits that differ.

Rejected candidates, and why — the sizing correction is an explicit plan
requirement, so this is recorded rather than assumed:

| Candidate | Shape | Verdict |
|---|---|---|
| `e3398c7..ae9823a` | 5 commits, **242 files, 27,041 insertions** | Rejected. A whole-phase diff, not a PR. It appears in AC4's base-derivation evidence, where it served a different purpose; inheriting it would be borrowing a number never sized for this job. |
| PR #16 `f5ab960..983546c` | 10 commits, 41 files, +858/-95 | Rejected despite a better *drift* surface (source + all three generated roots). It has **no test delta and no dependency manifest**, so `05f` and `05e` would both return "nothing to report" — the dry run would not exercise them. |
| **PR #17 `f5ab960..e6ff28a`** | 3 commits, 26 files, +1288/-0 | **Selected.** Every roster position has real material. |

Why every evaluator finds something: a genuine debug artifact
(`Debug.Log($"VISUAL_VERIFICATION_MANIFEST={manifestPath}")`), four C# test files
including `CaptureGateTest.cs`, a `package.json` declaring
`com.unity.test-framework: 1.6.0` (the head commit's subject line **is** "declare
test-framework dependency"), ~500 lines of new C# doing filesystem writes, and
Unity `.meta`/`.asmdef` conventions. Full rationale in the fixture itself.

Recorded weakness, not hidden: the range has **zero deletions**, so it is a
weaker proxy for a removal-shaped PR. No bounded pair in this repo's history has
a dependency change *and* a test delta *and* deletions; roster coverage was
weighted above shape-completeness. The fix is a second fixture, not a resize.

One incidental find worth keeping: PR #17's branch was cut from `f5ab960` while
PR #16 landed on top independently, so the merge commit's first parent
(`7ff1974`) is **not** the base. The fixture is itself a live instance of the
AC5 "branch cut from another feature branch" case.

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05-phase-final-review.agent.md` -> `.github/agents/05-pr-review.agent.md` | **Rename + rewrite** | `git mv`. Frontmatter `name`/`description`/`agents` restated. Deleted: ledger, subphase discovery, artifact inventory, write-back, archiving. Added: single interaction block, base suggest-and-confirm, report root, roster table. Preflight 4 steps -> 2. 249 -> 284 lines. | AC1, AC2-AC12 |
| `.gitignore` | Modify | Added four un-ignore rules for `dev/pr-review/`, mirroring the existing `dev/phase-final-review/` pattern, with a comment recording that only `fixtures/` is un-ignored back in. | AC10b — without it AC13 fails invisibly (`dev/*` at `:5`) |
| `dev/pr-review/fixtures/pinned-diff-range.md` | Create | The pinned base/head pair, its derivation, why it was chosen, the two rejected candidates, per-evaluator expectations, and the recorded weakness. | AC13 |
| `.github/agents/README.md` | Modify | Six references: the orchestrator's own row (`:136`), the parent column of three surviving `05x` rows (`:163,166,167`), the prose blurb (`:190`), and the four-orchestrators line (`:407`). Each replacement asserted to match exactly once. | Context Discovery Delta — feature 02's AC5 covered retired-agent rows only, so these survived it |

### Generated Files (propagator output — zero hand-edits, zero hand-deletions)

| File | Change | Why |
|------|--------|-----|
| `claude/commands/pr-review.md` | Created | Orchestrator is `user-invocable`, so the Claude output is a **command**, not an agent. |
| `opencode/agents/05-pr-review.md`, `codex/agents/05-pr-review.toml` (`name = "pr-review"`), `codex/profiles/pr-review.config.toml` | Created | Rename propagation. |
| `claude/commands/phase-final-review.md`, `opencode/agents/05-phase-final-review.md`, `codex/agents/05-phase-final-review.toml`, `codex/profiles/phase-final-review.config.toml` | **Pruned by feature 01** | AC14. The command file is the sharpest case — it stays user-invocable, so a stale copy leaves a live slash command pointing at a deleted agent. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_pr_review_orchestrator.py` | Create | 42 tests. Absence assertions (AC8/AC9), base derivation (AC3-AC6), single interaction (AC2), report root (AC7), roster (AC10), partial failure (AC11), read-only (AC12), fixture + `.gitignore` (AC13/AC10b), rename + propagation (AC1/AC14), and the report-root migration pin. Includes `_prose()`, which normalizes whitespace so assertions are not coupled to line-wrap position. | AC1-AC14 |
| `tests/test_propagate_master_assets.py` | Modify | `test_phase_final_review_agent_is_present_in_all_harness_outputs` -> `test_pr_review_agent_is_present_in_all_harness_outputs`; all five pinned strings updated (`:187-202`). | AC1, AC14 |

`expected_slugs` (`:87`) left alone as instructed — it omits `execute` holders
including this orchestrator, which retains `execute` for base derivation.
Feature 05 closes that enumeration gap.

## Test Results

- **Baseline**: **448 passed, 17 subtests passed** — re-run and confirmed on a
  clean tree at `7555c1e` before any change. Matches the brief exactly.
- **Final**: **`490 passed, 17 subtests passed in 7.36s`** — the exact final line
  of a real full-suite run (`.venv/bin/python -m pytest tests/ -q`) on the
  working tree.
- **New tests added**: 42
- **Arithmetic**: 448 + 42 = 490. Reconciled against **passed**, not collected.
  Verified independently: `--collect-only` reports `490 tests collected`, so
  collected == passed and nothing is hiding in a skip or xfail.
- **Regressions**: None.

### PERF-01: real, load-sensitive, threshold untouched

Two runs in one batch of three showed `1 failed, 489 passed`. I did not assume
which test, and re-running clean gave 490 four times consecutively. I reproduced
it deliberately under eight busy cores to identify it rather than guess:

    FAILED tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms
    1 failed, 489 passed, 17 subtests passed in 25.39s

This is the known PERF-01 gate. It measures subprocess/interpreter startup, is
untouched by this feature (which adds no code to the hook path — the changes are
a Markdown agent, a fixture document, `.gitignore`, a README, and tests), and
feature 01's record documents the same flake. Unloaded it passes standalone
(`1 passed in 0.49s`) and in the full suite.

**The 50 ms threshold was not changed.** It was relaxed once before (50->90 in
PR #22) and reverted. Noted for visibility, per instruction, not worked around.

### Propagation convergence

Propagation is not idempotent across an agent-identifier reclassification, so it
was run repeatedly rather than once. Run 1 removed the four orphans; runs 2-4
reported every non-inventory counter at zero with no `git status` drift. Verified
again after the final edit.

## Deviations from Plan

1. **The agent grew (249 -> 284), where the plan predicted subtraction.** Plan §D
   says "the current orchestrator is ~180 lines of preflight, ledger parsing,
   artifact inventory, and write-back; the rescoped one is a base confirmation, a
   fan-out, and a report path." The deletions happened in full — but AC2-AC6 are
   entirely new contract, and "a base confirmation" is not one line: AC3's chain,
   AC4's self-exclusion with its measured evidence, AC5's three cases, and AC6's
   override propagation are 76 lines, and each is separately mandated and
   separately mutation-tested. I did not pad and did not restate the report
   templates (asserted). Recording it rather than claiming a subtraction that did
   not happen. A reviewer who wants this shorter should cut the *rationale*
   paragraphs, not the contracts — but those paragraphs are what the learnings
   file says keep getting re-litigated.

2. **Three retired words survive as rationale, not machinery.** AC8 says the
   deleted machinery must not survive "in any form", so the exact residue is
   enumerated rather than left for a reviewer's grep to find:
   - `ledger` x1 — "the ledger, artifact-refusal, and verdict-recording questions
     were removed", explaining *why* one interaction is achievable.
   - `archive` x1 — "nothing is ever archived", the rule that replaces archiving.
   - `PROJECT_ROADMAP.md` x1 — inside the prohibition, asserted to be in a
     sentence containing "never".

   All three are the absence being *stated*, which is what stops re-invention. No
   machinery token survives: `ledger-commits.jsonl`, `ledger-events.jsonl`,
   `eval/runs/`, `subphase`, `PHASE_0N`, `artifact inventory`, `write-back`,
   `existing status line`, and `PHASE_0N_SUMMARY.md` are all zero, asserted.
   I did remove the literal token `write-back` from explanatory prose so the
   absence test could ban it outright — the strongest available guard on the
   riskiest deletion.

3. **`.github/agents/README.md` updated here.** The context flags it as "owner
   unconfirmed" between `04` and `08`. Taken here: the rows name *this* agent, the
   rename is what invalidates them, and leaving a roster doc pointing at a deleted
   agent for three waves has no upside.

## Gaps

1. **The dry run (AC13) was not executed.** It is behavioural: the orchestrator
   opens with a mandatory user interaction and fans out seven subagents, which an
   implementation pass cannot perform or honestly simulate. The fixture is pinned,
   tracked, and asserted (both SHAs resolve, merge-base checks out, size is
   PR-shaped) — but "one interaction, then a report" is unproven. **AC13 is marked
   Partial for this reason.** Left unchecked in the tasks file.
2. **All four Manual QA items remain open** and are unchecked: the dry run;
   `origin/HEAD` unset in a scratch consumer repo (it **is** set here, to
   `refs/remotes/origin/main`, so this cannot be exercised locally without
   unsetting it); base correction propagating to every evaluator; no-remote
   fallback.
3. **The `agents:` roster is a forward reference.** `05c`/`05d`/`05e`/`05f`/`05g`
   do not exist until waves 5-6. Accepted risk per the plan; `08` verifies it. A
   dry run before wave 6 will not resolve five of the eight names.
4. **The report-root split is pinned, not closed** (Decisions §3). Six evaluators
   still write to `dev/phase-final-review/PHASE_0N/` while the orchestrator routes
   to `dev/pr-review/<sha>-<ts>/`. Until 05-07 land, a real run would route
   evaluators to a root they do not write to — which is exactly why the dry run
   cannot pass yet either. Owned by 05/06/07.
5. **`dev/phase-final-review/fixtures/` untouched.** It is live wiring named by
   seven surviving agents, not a dead planning record, and its retirement is
   feature 08's. The now-dead `!dev/phase-final-review/` un-ignore rules are left
   in place for the same reason — the old fixture is still tracked.

## Reviewer Focus Areas

- **Two of my guards were inert, and mutation testing — not review — caught
  them.** Both are fixed and re-verified, but they are the honest place to start.
  (a) `test_suggestion_chain_appears_in_order` used `body.index()` over the whole
  document; because `refs/remotes/origin/HEAD` occurs twice, reordering the actual
  ranked list left an earlier stray occurrence and the test passed over a broken
  contract. It now parses the numbered items of the `Suggestion order` section and
  fails on both a rank swap and a dropped fallback. (b)
  `test_agent_name_does_not_collide_with_prose` asserted `" - " in "05 PR - Review"`
  — a string literal, not the file. It would have passed with the agent named
  `PR Review`. It now reads the name from frontmatter and checks it against
  `load_source_agents()`. **Worth re-running the mutation sweep rather than
  trusting this paragraph** — 20 mutations, all caught; harness at
  `scratchpad/mutate.py`. Note one apparent failure there is a harness artifact
  (`replace(..., 1)` vs 2 occurrences of `04e-diff-security-scan`), confirmed
  separately with a full replace.
- **`test_report_root_migration_cannot_split_silently` (Decisions §3)** is the
  judgement call most worth a second opinion. It asserts a set of six filenames I
  do not own. I believe it is a pin rather than an exemption, but it is the
  closest thing here to the `EXEMPT_FILES` instinct feature 03's reviewer had to
  undo, and it deserves the scrutiny.
- **`04e` on the top model tier (Decisions §4)** — a defensible judgement, not a
  derivation. The old table never mapped `04e`.
- **The `_prose()` normalizer** in the test module. It exists so contract
  assertions are not pinned to line-wrap position (cf.
  `tests/test_readiness_synthesis_agents.py:16`, `"never read\ncode"`, which is
  coupled to its author's wrap column — feature 07's to fix, left alone). Check
  that it does not make any assertion *too* permissive: it lowercases and collapses
  whitespace, so it would not catch a case-only or spacing-only regression. I
  judged neither to be a real failure mode for a prose contract.
- **AC8 residue (Deviations §2)** — three retired words survive deliberately as
  rationale. If the reviewer reads AC8's "in any form" more strictly than I did,
  these are the three lines to cut, and no test blocks cutting them.
