# Implementation Record: 06 Narrative and Test Health

## Summary

Renamed `05h-test-health` → `05f-test-health` (the slug freed by feature 02's
retirement of the seam analyzer) and rescoped both judgment-shaped evaluators
from a whole-phase framing to the branch diff `<merge-base>..HEAD`:

- **`05f-test-health`** — a thin delegating adapter. Reframed around the coverage
  delta base→HEAD, branch-scoped test redundancy, and flake candidates. All of
  the existing delegation, NOT RUN / below-GO-ceiling, and not-measurable language
  was preserved rather than rewritten, per the context's Discovery Delta.
- **`05b-change-narrator`** — the family's deep-judgment agent. Subphase
  attribution deleted outright from body *and* `description:`; churn hotspots kept
  and re-anchored on directories; the "what the branch is trying to do" account
  added as the narrative spine; chunking kept structural.

Both migrated off the retired `dev/phase-final-review/PHASE_0N/` report root and
now defer the path to feature 03's `pr-review-conventions` skill. That tripped
feature 04's asserted migration ledger, which was reconciled by shrinking the set
(not weakening the assertion) — only `05l-readiness-synthesizer` remains, and
feature 07 owns it.

23 new tests, all mutation-verified. **50/50 mutations killed their guard; zero
inert.** The first mutation pass found **5 inert guards + 1 invalid mutation**;
all six were fixed and re-verified (see Reviewer Focus Areas).

## Sibling Features

Scanned all eight feature directories (title + one-line overview only).

| Sibling | Relationship to this feature |
|---|---|
| `01-propagator-orphan-pruning` | **Consumed.** Its pruning removed `opencode/agents/05h-test-health.md` automatically on propagation (`opencode_orphans_removed: 1`). No manual `git rm`. |
| `02-retired-evaluator-removal` | **Undeclared dependency, confirmed landed.** Its deletion of `05f-seam-analyzer` freed the `05f` slug. Verified absent before the rename. |
| `03-pr-review-conventions-skills` | **Consumed.** Owns the report root and the ≤10-line return; both agents now defer to it rather than restating the path. |
| `04-pr-review-orchestrator` | **Cross-feature contract resolved.** Its roster at `05-pr-review.agent.md:5` forward-references `05f Test Health`; this feature creates that exact display name. Its migration ledger in `tests/test_pr_review_orchestrator.py` was reconciled. |
| `05-mechanical-evaluators` | **Shared module, sequential.** Both edit the roster in `tests/test_propagate_master_assets.py`. Feature 05 landed first and left it extensible; this feature reconciled by renaming one key. |
| `07-synthesis-and-pr-posting` | **Feeds, via report files only.** Owns `05l`→`05g` and the last entry in the migration ledger. Both agents name `05g` as the verdict owner. |
| `08-retirement-reconciliation` | Owns the `README.md` catalogue sweep (L163/L170) and `claude/agents/single-feature.md`. Left untouched. |

**Shared modules touched:** `tests/test_propagate_master_assets.py` (with 05),
`tests/test_pr_review_orchestrator.py` (with 04, 07).

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Rename `05h`→`05f` | F.new.1 | Must-have automated (new) | Done | `.github/agents/05f-test-health.agent.md` | `tests/test_narrative_and_test_health_agents.py::test_test_health_is_renamed_to_the_05f_slug`, `::test_test_health_declares_the_cross_feature_display_name`, `::test_no_retired_test_health_identifier_survives_in_either_agent` | PENDING | PENDING |
| AC1b | `description:` rescoped | F.new.2 | Must-have automated (new) | Done | `.github/agents/05b-change-narrator.agent.md:3`, `.github/agents/05f-test-health.agent.md:3` | `::test_narrator_has_no_subphase_attribution_anywhere_in_the_file` (whole-file, incl. frontmatter) | PENDING | PENDING |
| AC2 | No subphase attribution; `<merge-base>..HEAD` | F.new.2 | Must-have automated (new) | Done | `.github/agents/05b-change-narrator.agent.md` | `::test_narrator_has_no_subphase_attribution_anywhere_in_the_file`, `::test_narrator_frames_the_comparison_as_the_branch_diff`, `::test_narrator_keeps_churn_hotspots` | PENDING | PENDING |
| AC3 | Account of branch intent | — | Automated contract + **manual QA** for quality | Done (contract) / Manual QA open | `.github/agents/05b-change-narrator.agent.md:9-11,58-63` | `::test_narrator_accounts_for_intent_not_only_content`, `::test_narrator_keeps_the_top_tier_requirement` | PENDING | PENDING |
| AC4 | Structural chunking; readers | F.new.3 | Must-have automated (new) | Done | `.github/agents/05b-change-narrator.agent.md:45-57` | `::test_narrator_chunking_is_structural`, `::test_narrator_chunking_degrades_when_readers_are_unavailable` | PENDING | PENDING |
| AC5 | Delegates to `test-analyst` | F.new.1 | Must-have automated (new) — **declaration only** | Done (declaration) / Runtime → manual QA | `.github/agents/05f-test-health.agent.md:5,36-53` | `::test_delegation_target_display_name_is_exact`, `::test_delegation_is_declared_not_inlined`, `::test_test_health_preserves_the_not_run_ceiling` | PENDING | PENDING |
| AC5b | `max_depth` named and handled | — | **Manual QA only** — static assertion provably cannot detect it | Declaration Done / **Verification deferred to manual QA** | `.github/agents/05f-test-health.agent.md:45-52`, `.github/agents/05b-change-narrator.agent.md:53-57` | `::test_test_health_names_the_max_depth_fallback` (names the trap; does **not** verify delegation) | PENDING | PENDING |
| AC6 | Coverage delta base→HEAD | F.new.1 | Must-have automated (new) | Done (with recorded degradation) | `.github/agents/05f-test-health.agent.md:26-34,55-72` | `::test_test_health_reports_a_branch_scoped_delta`, `::test_test_health_names_its_evidence_source`, `::test_test_health_consumes_the_baseline_worktree_rather_than_creating_one`, `::test_test_health_degrades_honestly_without_coverage_tooling`, `::test_test_health_drops_the_subphase_redundancy_framing` | PENDING | PENDING |
| AC7 | Report path + ≤10-line return | F.new.3 | Must-have automated (new) | Done | both agent bodies | `::test_both_agents_declare_the_ten_line_return`, `::test_both_agents_defer_the_report_path_to_the_conventions_skill`, `::test_neither_agent_produces_a_verdict` | PENDING | PENDING |
| AC8 | Roster + OpenCode orphan pruned | F.new.5 | Must-have automated (new) + existing to update | Done | `tests/test_propagate_master_assets.py:45`, generated roots | `::test_retired_test_health_slug_left_no_opencode_orphan`; `tests/test_propagate_master_assets.py::test_pr_review_evaluator_roster_is_fully_enumerated`, `::test_phase_review_agents_match_all_generated_harness_outputs` | PENDING | PENDING |
| AC9 | Neither gains `execute` | F.existing.4 | **Existing test to update** (not new) | Done | `tests/test_propagate_master_assets.py:45` | `tests/test_propagate_master_assets.py::test_pr_review_evaluator_tool_grants_match_expected_lists` (exact list equality per slug) | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `05h`→`05f` rename, `name:` + self-references | Done | `.github/agents/05f-test-health.agent.md` | `git mv` preserved history (`RM` in status). `name: 05f Test Health` matches feature 04's forward reference exactly. |
| AC1b | `description:` rescoped on both agents | Done | both agents, line 3 | The AC2 assertion is whole-file, so it covers frontmatter. |
| AC2 | Subphase attribution deleted outright | Done | `05b` | Deleted: subphase input, path→subphase mapping, per-subphase partition/reporting, multi-subphase hotspot definition, per-subphase report sections. `"subphase"` appears nowhere in either file. |
| AC3 | Account of what the branch is trying to do | Done (contract) | `05b:9-11,58-63` | Narrative quality is **manual QA** — no assertion covers judgment. |
| AC4 | Structural chunking | Done | `05b:45-57` | Chunk boundary re-anchored on directories now subphases are gone. Serial fallback + max_depth caveat retained. |
| AC5 | Demonstrably delegates to `test-analyst` | Done (declaration) | `05f:5,36-53` | **Declaration only.** See AC5b — the runtime contract is not verifiable statically. |
| AC5b | `max_depth` fallback named and handled | Declaration Done; verification deferred | `05f:45-52`, `05b:53-57` | **Deliberately not claimed as verified.** See Gaps. |
| AC6 | Coverage delta base→HEAD, redundancy, flakes | Done | `05f:26-34,55-72` | Unverified Assumption resolved — see Deviations. |
| AC7 | Report path + ≤10-line return | Done | both | Both defer the path to `pr-review-conventions` rather than restating it. |
| AC8 | Roster + OpenCode orphan pruned | Done | test roster; generated roots | Orphan removed by feature 01's pruning on propagation, not by hand. |
| AC9 | Neither gains `execute` | Done | test roster | Both remain `[agent, read, search, edit]`. Posture unchanged, as the plan predicted. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05h-test-health.agent.md` → `.github/agents/05f-test-health.agent.md` | Rename (`git mv`) + Modify | `name: 05f Test Health`; body rescoped to the branch delta; report path deferred to the conventions skill; `max_depth` trap named; evidence-source naming added; `cross-subphase` dropped | AC1, AC5, AC5b, AC6, AC7 |
| `.github/agents/05b-change-narrator.agent.md` | Modify | `description:` rescoped; subphase attribution deleted; reframed to `<merge-base>..HEAD`; intent account added; chunking re-anchored on directories; report path deferred to the skill | AC1b, AC2, AC3, AC4, AC7 |
| `claude/agents/z-test-health.md` | Modify (generated) | Body regenerated; **filename stable** across the rename | AC8 |
| `codex/agents/z-test-health.toml` | Modify (generated) | Body regenerated; **filename stable** | AC8 |
| `opencode/agents/05f-test-health.md` | Create (generated) | New OpenCode slug | AC8 |
| `opencode/agents/05h-test-health.md` | Delete (via propagation) | Orphaned by the rename; removed by feature 01's pruning | AC8 |
| `claude/agents/z-change-narrator.md`, `opencode/agents/05b-change-narrator.md`, `codex/agents/z-change-narrator.toml` | Modify (generated) | Bodies regenerated | AC8 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_narrative_and_test_health_agents.py` | Create | 23 new contract assertions, pytest-style per the house convention of `test_pr_review_orchestrator.py` | AC1, AC1b, AC2, AC3, AC4, AC5, AC5b, AC6, AC7, AC8 |
| `tests/test_propagate_master_assets.py` | Modify | Roster key `05h-test-health` → `05f-test-health` (one line, L45) | AC8, AC9 |
| `tests/test_pr_review_orchestrator.py` | Modify | Migration ledger shrunk to `{05l-readiness-synthesizer.agent.md}`; comment records why | AC7 |

## Test Results

- **Baseline**: `1 failed, 513 passed, 108 subtests passed` (clean tree at `f835b04`)
- **Final**: `1 failed, 536 passed, 108 subtests passed` (two consecutive runs, identical)
- **New tests added**: 23
- **Regressions**: None

The single failure is `tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms` (PERF-01) — a pre-existing deterministic latency failure on code predating this phase, and Phase 04's open release blocker. It is **not** attributable to this feature: nothing here touches `tests/hooks/` or `.github/hooks/`. The 50 ms threshold was not changed.

Arithmetic reconciles to **passed**, not collected: 513 + 23 = 536.

### Mutation verification

Every guard was mutation-tested: the thing it claims to check was broken, and the
guard was confirmed to fail. **50/50 mutations killed their guard; zero inert.**

The first pass found **5 inert guards and 1 invalid mutation**, all from one root
cause: each asserted a phrase appeared *somewhere*, but the phrase occurred in
several places, so deleting the load-bearing occurrence left the guard green.

| Guard | Why it was inert | Fix |
|---|---|---|
| `test_test_health_names_the_max_depth_fallback` | `"max_depth" in body` also matched the required-value sentence | Assert four distinct single-occurrence claims (default is 1, requirement is 2, silent inline fallback, never continue inline) |
| `test_test_health_reports_a_branch_scoped_delta` | `"coverage delta"` also appears in the not-measurable rule | Assert at the section headers with their objects attached |
| `test_test_health_names_its_evidence_source` | mutation anchor was wrong (line-wrap) — harness bug, not a guard bug | Corrected anchor; guard strengthened to three claims |
| `test_narrator_keeps_churn_hotspots` | phrase also appears in `description:` | Assert the procedure step, the empty-case rule, and the report table |
| `test_narrator_accounts_for_intent_not_only_content` | phrase appears twice; one deletion survived | Assert both positions + the honesty rule |
| `test_narrator_chunking_is_structural` | `"one bounded chunk at a time"` also matched the max_depth paragraph | Assert the full instruction with its objects |

One further guard (`test_narrator_chunking_degrades_when_readers_are_unavailable`)
was live but fragile — it passed only because `max_depth` happened to occur once
in that file. Strengthened to specific claims rather than left to luck.

Harness: `scratchpad/mutate_f06.py` (not committed — a verification tool, not a
deliverable). Re-runnable; it restores the tree and leaves propagation at a fixed
point.

### Propagation

Run to a fixed point, as required for an agent-identifier reclassification:

- Pass 1: `claude_changed: 1, opencode_changed: 1, codex_changed: 1, opencode_orphans_removed: 1`
- Pass 2: all counters `0` — fixed point proven

The context's Discovery Delta prediction was validated exactly: `_claude_filename_for`
and `_codex_identifier_for` resolved to the existing `z-test-health` stem, so those
filenames are **stable**; only `_opencode_filename_for` (which prefers `source_slug`)
orphaned, and feature 01's pruning removed it. No `05f-*` file appeared in the
Claude or Codex roots.

## Deviations from Plan

1. **Unverified Assumption resolved — the coverage delta degrades, honestly.**
   The plan asked whether `Test - Analyst` can be pointed at a revision to produce
   the base side. Resolved by reading its contract (`.github/agents/test-analyst.agent.md:4`):
   it holds `tools: [read, search, edit, fetch]` — **no `execute`**. So:
   - It **can** be pointed at `05a`'s baseline worktree — a worktree is just
     readable files, and nothing in its contract pins it to the repo root.
   - It **cannot** *measure* coverage at any revision, because no agent in the
     chain can run a coverage tool (`05f` lacks `execute` too, per AC9).

   So `05f` reports a *measured* delta only when the orchestrator supplies coverage
   evidence for both revisions; otherwise **not-measurable** plus the structural
   suite delta the delegate derived from reading both trees. This is the plan's
   stated preferred degradation. Notably AC9's no-execute constraint is what
   *structurally* prevents `05f` growing its own coverage runner — the security
   posture and the design constraint are the same fact.

2. **Report root migrated (not listed as an AC task).** Both agents were still on
   the retired `dev/phase-final-review/PHASE_0N/` root. AC7 requires feature 03's
   contract, so the migration was in scope. Resolved properly: both now defer the
   path to the conventions skill (the `05c` house pattern) rather than restating
   it. Feature 04's ledger tripped and was reconciled by **shrinking the set** —
   the assertion was not weakened, and the orchestrator/skill root assertions that
   back it were untouched.

3. **AC9 needs no new test.** Per the context's Discovery Delta, the plan's
   traceability table mislabels AC9 "new"; `test_pr_review_evaluator_tool_grants_match_expected_lists`
   already asserts exact per-slug tool lists. Only the roster key changed. Adding a
   second `execute` assertion would duplicate existing coverage.

## Gaps

1. **AC5b is not verified, and cannot be verified statically.** `max_depth`
   defaults to 1; a blocked depth-2 spawn causes a **silent inline fallback** — the
   agent does the work itself and reports success. `05f`→`Test - Analyst` and
   `05b`→per-directory readers both sit at depth 2. `test_test_health_names_the_max_depth_fallback`
   asserts the agent *names and handles* the trap; it does **not** verify that
   delegation occurs, and it passes in exactly the failure case. Its docstring says
   so explicitly. **Verification requires a runtime transcript and belongs to
   manual QA.** No automated evidence here should be read as covering it.

2. **AC3's narrative quality is manual QA.** The assertions pin that the intent
   account is required and that unsupported intent must not be invented. Whether a
   real dry-run narrative is genuinely about what the branch is *for* is a judgment
   no assertion covers.

3. **No dry run performed.** Stage 4's dry runs against the pinned fixture
   (`dev/pr-review/fixtures/pinned-diff-range.md`) require live orchestration and a
   configured harness; they are manual QA. The tasks file records them unchecked.

4. **`[agents] max_depth = 2` is required where this family is operated**
   (`~/.codex/config.toml`). Named in both agent bodies. Recording it in operator
   documentation is feature 08's reference sweep, not this feature's file scope.

5. **PERF-01 remains failing** — pre-existing, Phase 04's blocker, untouched.

## Reviewer Focus Areas

- **`tests/test_pr_review_orchestrator.py:38-57` — the migration ledger.** Confirm
  shrinking the set to `{05l-readiness-synthesizer.agent.md}` is the correct
  reconciliation and not a weakening. The backing assertions (orchestrator + skill
  on the new root) are separate and untouched, so this cannot be satisfied by
  regressing them — verified by mutation (regressing `05f` to the retired root
  trips it).
- **AC5b honesty.** The strongest temptation in this feature is to present
  `test_test_health_names_the_max_depth_fallback` as covering AC5. It does not.
  Please check the record does not overclaim anywhere.
- **`05f` thinness (86 lines).** The plan says past a page it is absorbing
  `test-analyst`'s job. Growth came from required content (branch scope, `max_depth`,
  evidence-source naming). Confirm no analysis procedure leaked in — the delegation
  language is preserved verbatim.
- **`05b`'s max_depth paragraph (`:53-57`)** permits inline work as the *stated
  serial fallback* while forbidding whole-diff reads. That distinction is load-bearing
  and subtle; confirm the wording cannot be read as licence to skip chunking.
- **Whole-file vs body scoping.** `_prose()` reads the entire file including
  frontmatter, deliberately — `description:` is where subphase attribution hid. A
  reviewer re-scoping these to the body would silently reopen AC1b.
