# Implementation Record: 05 Mechanical Evaluators

## Summary

The three cheap-tier mechanical sweeps were renumbered to `05c-artifact-sweeper`,
`05d-consistency-auditor` and `05e-dependency-auditor`, rescoped from a phase to
the branch diff `<merge-base>..HEAD`, migrated to the `dev/pr-review/` report
root, and had their `execute` grants removed. The propagation-enumeration gap is
closed: the roster is now derived from disk and asserted against a per-agent tool
map, so an agent can no longer be omitted from enumeration to dodge an assertion.

`execute` was dropped from **all three**, not two. See Deviations — the plan
anticipated `05e` might justify retention, and it could not.

All 31 guards added by this feature were mutation-tested: each was verified to
fail when the exact thing it checks is broken. 31/31 killed, 0 inert.

## Sibling Features

| Sibling | Wave | Relationship |
|---|---|---|
| `01-propagator-orphan-pruning` | 1 | Its pruning removed this feature's three OpenCode orphans automatically. Verified: `opencode_orphans_removed: 3`. |
| `02-retired-evaluator-removal` | 2 | Freed the `05c`/`05d`/`05e` slugs. Confirmed landed before the rename. |
| `03-pr-review-conventions-skills` | 3 | Owns the report root. All three bodies reference the skill rather than restating the path. |
| `04-pr-review-orchestrator` | 4 | Supplies the confirmed base and dispatches `05c`/`05d`/`05e`. Its report-root ledger was reconciled by this feature (see below). |
| `06-narrative-and-test-health` | 5 | **Shares `tests/test_propagate_master_assets.py`.** Runs immediately after this feature. |
| `07-synthesis-and-pr-posting` | 6 | Will reissue the `05g` identifier to the readiness synthesizer — deliberately accommodated (see Reviewer Focus). |
| `08-retirement-reconciliation` | 7 | Owns `claude/agents/single-feature.md`. Not touched. |

**Shared module hand-off to `06`:** the roster now lives in a module-level dict
`PR_REVIEW_EVALUATOR_TOOLS` in `tests/test_propagate_master_assets.py`, keyed by
source slug. Feature `06` renames `05h-test-health` → `05f-test-health` by
renaming that key and its value's tools if they change; feature `07` does the same
for `05l-readiness-synthesizer` → `05g-readiness-synthesizer`. No tuple to
re-derive, and `test_pr_review_evaluator_roster_is_fully_enumerated` will fail if
either renames the agent without renaming the key.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Rename to 05c/05d/05e | Roster completeness | Must-have automated (new) | Complete | 3 agent files, `.github/agents/README.md` | `tests/test_mechanical_evaluators.py::RenameTests` | PENDING | PENDING |
| AC2 | Rescope to `<merge-base>..HEAD`; no subphase concepts | No subphase concepts | Must-have automated (new) | Complete | 3 agent bodies | `tests/test_mechanical_evaluators.py::ScopeTests` | PENDING | PENDING |
| AC3 | `execute` dropped where not required | Per-agent tool expectation | Must-have automated (update) | Complete | 3 agent frontmatter | `tests/test_propagate_master_assets.py::PropagateMasterAssetsTests::test_pr_review_evaluator_tool_grants_match_expected_lists` | PENDING | PENDING |
| AC4 | `05e` explicitly offline read-only mode | Per-agent tool expectation | Must-have automated (update) | Complete (grant dropped) | `.github/agents/05e-dependency-auditor.agent.md` | `tests/test_mechanical_evaluators.py::OfflineDependencyAuditTests` | PENDING | PENDING |
| AC5 | Report at conventions path; ≤10-line return | Report contract | Must-have automated (new) | Complete | 3 agent bodies | `tests/test_mechanical_evaluators.py::ReportContractTests` | PENDING | PENDING |
| AC6 | Verifiable added-line attribution | Added-line attribution declared | Must-have automated (new) | Complete | 3 agent bodies | `tests/test_mechanical_evaluators.py::AttributionTests` | PENDING | PENDING |
| AC7 | Cheap tier authoritative; limitation ≠ pass | Contract assertions | Must-have automated (new) | Complete | 3 agent bodies | `tests/test_mechanical_evaluators.py::TierTests` | PENDING | PENDING |
| AC8 | `expected_slugs` re-derived; per-agent tool lists | Roster completeness | Existing test to update | Complete | `tests/test_propagate_master_assets.py` | `::test_pr_review_evaluator_roster_is_fully_enumerated` | PENDING | PENDING |
| AC8b | `05a` enters roster keeping `execute`, declared | Per-agent tool expectation | Existing test to update | Complete | `tests/test_propagate_master_assets.py` | `PR_REVIEW_EVALUATOR_TOOLS["05a-baseline-worktree"]` | PENDING | PENDING |
| AC8c | `edit` pinned on all three | Per-agent tool expectation | Existing test to update | Complete | `tests/test_propagate_master_assets.py` | `::test_pr_review_evaluator_tool_grants_match_expected_lists` | PENDING | PENDING |
| AC9 | Propagates to 3 roots; old OpenCode slugs absent | Old OpenCode slugs pruned | Must-have automated (new) | Complete | generated roots | `tests/test_propagate_master_assets.py::OrphanPruningTests::test_renumbered_mechanical_evaluators_left_no_opencode_orphans` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Renamed with `name:` and body self-references updated | Complete | `05c-artifact-sweeper.agent.md`, `05d-consistency-auditor.agent.md`, `05e-dependency-auditor.agent.md` | `git mv` preserved history. README roster rows added (they never existed — see Gaps). |
| AC2 | Rescoped to the branch diff; no subphase concepts | Complete | 3 agent bodies | `05d`'s "compare across subphases" input had no branch-diff meaning and was replaced with comparison against established repo conventions. |
| AC3 | `execute` dropped where not genuinely required | Complete | 3 agent frontmatter | Dropped from all three. No named command with no non-shell equivalent could be produced for any of them. |
| AC4 | `05e` retains explicitly offline read-only audit mode | Complete | `05e-dependency-auditor.agent.md` | The **mode** is retained and strengthened; the **grant** is gone. Offline is now a capability boundary, not a policy. See Deviations. |
| AC5 | Report to conventions path; ≤10 lines | Complete | 3 agent bodies | Bodies name `<slug>-report.md` and defer the root format to `pr-review-conventions`. Asserted they do *not* restate it. |
| AC6 | Verifiable added-line attribution required | Complete | 3 agent bodies | Each body requires added-line attribution, rejects touched-file filtering by name, and routes unattributable candidates to `Checks Not Run`. |
| AC7 | Cheap tier authoritative; limitation is an execution condition | Complete | 3 agent bodies | Includes graph-unavailable → NOT RUN + verdict ceiling drop for `05c`/`05d`. |
| AC8 | `expected_slugs` re-derived over the settled roster | Complete | `tests/test_propagate_master_assets.py` | Roster **derived from disk**, not restated. Omission now fails. |
| AC8b | `05a` admitted with `execute` declared | Complete | `tests/test_propagate_master_assets.py` | Grant visible with justification; `05a` otherwise untouched (no rename, no rescope). |
| AC8c | `edit` pinned, not stripped | Complete | `tests/test_propagate_master_assets.py` | Mutation-verified: stripping `edit` fails. |
| AC9 | All three roots propagated; old OpenCode slugs absent | Complete | `claude/`, `opencode/`, `codex/` | Claude/Codex kept `z-*` stems; 3 OpenCode orphans pruned by feature `01`. Fixed point confirmed. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05c-artifact-sweeper.agent.md` | Rename + Modify | From `05g-artifact-sweeper`. `name:` updated; `execute` dropped; rescoped to `<merge-base>..HEAD`; added-line attribution section added; report root migrated to conventions skill. | AC1, AC2, AC3, AC5, AC6, AC7 |
| `.github/agents/05d-consistency-auditor.agent.md` | Rename + Modify | From `05j-consistency-auditor`. As above, plus the subphase-comparison input replaced with comparison against established repo conventions, and a graph-backed canonical-form derivation with NOT RUN semantics. | AC1, AC2, AC3, AC5, AC6, AC7 |
| `.github/agents/05e-dependency-auditor.agent.md` | Rename + Modify | From `05k-dependency-auditor`. As above, plus the offline contract restated as a capability boundary and the audit-command evidence path removed. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 |
| `.github/agents/README.md` | Modify | Added roster rows for `05c`, `05d`, `05e`. | AC1 |
| `claude/agents/z-artifact-sweeper.md`, `z-consistency-auditor.md`, `z-dependency-auditor.md` | Regenerate | Propagated. Stems survived the renumber as predicted. | AC9 |
| `opencode/agents/05c-*.md`, `05d-*.md`, `05e-*.md` | Add (generated) | New slug-keyed outputs. | AC9 |
| `opencode/agents/05g-*.md`, `05j-*.md`, `05k-*.md` | Delete (generated) | Orphaned by the renumber; pruned by feature `01`. | AC9 |
| `codex/agents/z-artifact-sweeper.toml`, `z-consistency-auditor.toml`, `z-dependency-auditor.toml` | Regenerate | Propagated. | AC9 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_mechanical_evaluators.py` | Add | 21 body-contract tests across 8 classes: rename, scope, attribution, tier, offline audit, report contract, read-only, empty-diff. | AC1, AC2, AC4, AC5, AC6, AC7 |
| `tests/test_propagate_master_assets.py` | Modify | Added `PR_REVIEW_EVALUATOR_TOOLS` + `_discover_pr_review_evaluator_slugs()`. Replaced the hand-listed `expected_slugs` tuple and the blanket `assertNotIn("execute", ...)` with a derived roster check and a per-agent tool-grant check. Added an OpenCode orphan assertion. Updated a fixture using the retired `05g-artifact-sweeper` slug. | AC3, AC8, AC8b, AC8c, AC9 |
| `tests/test_pr_review_orchestrator.py` | Modify | Removed the three migrated agents from `EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION`. | AC2 (report-root migration) |

## Test Results

- **Baseline**: `1 failed, 489 passed, 17 subtests passed in 12.50s` (before implementation, at `f29e9ca`).
  The single failure is `test_ac9_propagated_guard_median_latency_is_below_50_ms` (PERF-01),
  which reproduced red on **3/3 baseline runs on this machine** before any change was made.
  Deselecting it reconciles the documented baseline exactly: `489 passed, 1 deselected` = 490 collected.
- **Final**: `1 failed, 513 passed, 108 subtests passed in 12.29s` (after implementation).
  Stable across 3 consecutive full runs (513 passed each; 12.64s / 12.06s / 11.96s).
- **New tests added**: 24 (21 in `test_mechanical_evaluators.py`, 3 in `test_propagate_master_assets.py`).
  489 + 24 = 513. The arithmetic reconciles to *passed*, not *collected*.
- **Regressions**: None. The one failure is PERF-01, owned by Phase 04 and load-sensitive
  (fires on slow runs; this machine ran ~12s throughout). `git status` confirms this feature
  touched neither `tests/hooks/` nor `.github/hooks/`. Its threshold was **not** altered.

### Mutation verification

Every guard added by this feature was mutation-tested: the thing it claims to check was
broken, and the named test was required to fail. **31/31 killed, 0 survived.** This covers
all 21 body contracts, the AC8 roster ledger (omitting `05c`; omitting `05a`), the AC3
widening case (`execute` re-added), the AC8c narrowing case (`edit` stripped), both
file-existence guards, and both directions of the feature-04 report-root ledger.

Notable kills:
- Omitting `05c` **or** `05a` from `PR_REVIEW_EVALUATOR_TOOLS` fails — the exact gap AC8 exists to close.
- Re-adding `execute` to `05c` fails; stripping `edit` from `05d` fails.
- Leaving a migrated agent listed as awaiting migration fails, **and** regressing `05c` back
  onto `dev/phase-final-review/` fails — the feature-04 ledger bites both ways, so the edit
  to it was forced by the migration rather than a convenience.

## Deviations from Plan

1. **`execute` was dropped from `05e-dependency-auditor`, not retained.** The plan (AC4)
   anticipated `05e` as "the most likely place" a grant survives, and the recorded learning
   called it "not a simple removal". AC3's bar is explicit and is the one that governs: the
   justification **must name a command with no non-shell equivalent, "or the grant goes."**
   No such command could be named. Verified in-environment: `pip-audit`, `osv-scanner` and
   `safety` are absent; `npm` is present but `npm audit` requires the registry and
   `--offline` makes it fail. Every candidate either contacts the network (which the body's
   own contract forbids) or needs a pre-provisioned local advisory DB that is not guaranteed.
   Retaining the grant on the strength of a command that might exist somewhere is exactly the
   "broad grant with a comment explaining why it is fine" that `cross-phase-decisions.md:86`
   prohibits. **AC4 is satisfied and strengthened**: the offline *mode* is retained — it is
   now a capability boundary rather than a policy the agent is trusted to observe. The cost is
   real and is declared in the body: vulnerability evidence now comes only from supplied
   artifacts, and its absence is a NOT RUN, never a pass. `05e`'s body was edited to remove
   the audit-command evidence path, so its frontmatter and body agree.

2. **`05d-consistency-auditor` gained a code-review-graph dependency it did not have.**
   The plan (section B) states `05c` and `05d` both build on the graph, but the verified `05j`
   body referenced it nowhere. Rather than invent an integration to match the plan, the graph
   is used for the one thing the rescope genuinely requires: the old body derived canonical
   forms by comparing subphases against each other, and with subphases gone the canonical form
   must come from the repository's established patterns. Locating that prior art is what
   `semantic_search_nodes`/`query_graph` are for, and it is what this repo's `CLAUDE.md`
   prescribes. The plan named `get_impact_radius` for `05d`; that tool answers blast-radius
   questions and is not a natural fit for convention-drift comparison, so it was not used.
   Graph-unavailable is a NOT RUN with a verdict-ceiling drop, per the plan's contract.

3. **Body-contract tests live in a new `tests/test_mechanical_evaluators.py`**, not in
   `test_propagate_master_assets.py`. The plan marked these `[PROPOSED - name TBD]`. Roster
   and tool-grant assertions stayed in `test_propagate_master_assets.py` where AC8 places
   them; body contracts are a separate concern and a separate file reduces the merge surface
   this feature shares with feature `06`.

4. **`expected_slugs` is derived, not re-listed.** The plan says "re-derive `expected_slugs`
   over the settled seven". A hand-written tuple of seven cannot satisfy AC8's own requirement
   that "omitting an agent **fails**" — omission from a literal list is silent by construction,
   which is how the original gap arose. The roster is therefore read from disk and asserted
   against the tool map. The literal that remains is the tool map, where omission fails loudly.

## Gaps

1. **`.github/agents/README.md` never listed `05a`, `05g`, `05j` or `05k`** — verified via
   `git log -S`; there were no rows to rename. Rows were added for the three agents this
   feature owns. **`05a-baseline-worktree` remains unlisted**, left alone because the plan
   scopes it out ("no rescope, no rename"). Worth noting for feature `08`: the four agents
   missing from the README are precisely the four that were missing from `expected_slugs` —
   the same four `execute` holders. That correlation is pre-existing and is probably not a
   coincidence, but confirming it is outside this feature's scope.

2. **The orchestrator's roster still names two agents that do not exist.** `05-pr-review`
   dispatches `05f` and `05g-readiness-synthesizer`; the agents on disk are `05h-test-health`
   and `05l-readiness-synthesizer` until features `06` and `07` rename them. This feature made
   `05c`/`05d`/`05e` resolve; the remaining two are owned by later waves. Nothing currently
   asserts that the orchestrator's roster resolves to real agents — a genuine gap, but it
   belongs to feature `08`'s reconciliation, and adding it now would fail on other features' work.

3. **`.github/learnings/cross-phase-decisions.md` still describes the grants as open.**
   Lines 56–58 name `05g`/`05j`/`05k` and the enumeration gap as outstanding. That file is a
   historical decision ledger, and rewriting it to reflect this feature's outcome is the
   learnings-harvester's job, not the implementer's. Left untouched deliberately.

4. **Manual QA (dry run against the pinned fixture) not performed.** The tasks call for a
   dry run producing three findings reports and a graph-unavailable degradation check. These
   agents are prompts; executing them requires an agent-harness run against
   `f5ab960..e6ff28a`, which is outside a test-suite pass. The contracts those runs would
   verify are pinned statically and mutation-tested instead. **Static contract assertions are
   not a substitute for observing the agents actually run** — this remains open for QA.

## Reviewer Focus Areas

- **The AC4 grant decision (`05e` lost `execute`) is the judgment call of this feature.**
  It reverses the plan's expectation. The reasoning is in Deviations #1 and rests on AC3's
  "name a command, or the grant goes" being the governing rule. If you disagree, the
  disagreement is about which of AC3/AC4 governs — not about whether a command was found.
  Note the body and frontmatter were changed together; a reviewer who restores the grant must
  also restore the body's evidence path, and must name the command AC3 demands.

- **`05d`'s new graph dependency (Deviations #2)** is the one place this feature added
  capability rather than removing it. Confirm it is justified by the rescope rather than by
  the plan's assertion, and that `get_impact_radius` being unused is acceptable.

- **`tests/test_mechanical_evaluators.py` asserts on prose via regex.** Whitespace is
  normalized (`_prose`) so reflowing a paragraph cannot silently drop an assertion — that was
  a real failure mode caught during implementation, where 9 guards were passing/failing on
  line-break position rather than content. All 21 are mutation-verified, but regex-on-prose
  is inherently brittle to rewording; the mutation harness is the evidence that they currently
  bite.

- **`test_no_body_retains_an_old_self_reference` deliberately bans the retired *identifiers*,
  not the bare substring `05g`.** Feature `07` reissues `05g` to the readiness synthesizer in
  the next wave; a substring ban would pass today and misfire then — the same trap the plan
  flagged for the OpenCode `05g-*` glob. Verified both ways: old identifiers kill it, and a
  reference to `05g-readiness-synthesizer` does not.

- **Hand-off to feature `06`:** `PR_REVIEW_EVALUATOR_TOOLS` is the shared surface. Feature `06`
  renames the `05h-test-health` key; the derived roster check fails if it renames the agent
  without the key. This is intended.
