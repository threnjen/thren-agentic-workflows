# Implementation Record: 08 Retirement Reconciliation

**AC scope this invocation:** AC5–AC11 (all statically verifiable ACs).
**AC1–AC4 are NOT done** and are recorded open with routing — see Gaps §1. They
require an agent fan-out this context cannot perform.

## Summary

The integration feature. Features `01`–`07` each passed review in isolation; this
one checks they compose. It does, on every surface a test can reach. **What it
does not do is prove the family runs**, and that gap is the honest headline of
this record rather than a footnote.

Three claims routed to this feature by name turned out to be **false**, and each
was refuted by direct evidence rather than argued about:

1. **`dev/phase-final-review/fixtures/` is not live wiring.** It was left alone by
   four successive features on the recorded grounds that "seven surviving agents
   name the fixture root". Those agents named the **report** root
   (`dev/phase-final-review/PHASE_0N/`) — the output — never the **fixture** root
   — the input. `git grep` returns zero `.github/agents/` hits for the fixture
   path at every commit in this phase. Retired (13 files deleted).
2. **The working tree was clean.** The brief described 12 uncommitted deletions of
   those fixtures "excluded from every commit so far". `git status` was empty and
   the files were tracked in `HEAD`. Nothing was in flight; the deletion in this
   feature is the first one that exists.
3. **The claim-#4 correlation is real but its stated cause is wrong.** The four
   agents missing from the catalogue are exactly the four missing from
   `expected_slugs` and all four held `execute` — confirmed. But `execute` is a
   *marker*, not the cause (see AC-#4 finding below).

**The mutation sweep found two inert guards in my own tests** — both in the class
this phase keeps rediscovering. Reported here because round 1 would have let me
claim a clean sweep that was false.

## Sibling Features

Read the first 5 lines of every sibling `-plan.md`, plus every prior
`-implementation.md` and `-review.md` in full (this feature is the integration
point and inherits their deferrals). Wave 7; depends on all of `01`–`07`.

**Shared modules touched:** `tests/test_propagate_master_assets.py` (shared with
`01`, `02`, `05`, `06`, `07` — one comment-and-assertion edit, no structural
change), `.github/agents/README.md` (shared with `02`, `05`, `07`),
`.github/learnings/cross-phase-decisions.md` (shared with `03`, `04`, `07`).

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | End-to-end dry run | Manual QA | Seven reports on disk under one run dir | **NOT DONE** | — | Gaps §1; `cross-phase-decisions.md` "STILL UNEXECUTED" entry | PENDING | PENDING |
| AC2 | Single-interaction contract holds end to end | Manual QA | Exactly one question block | **NOT DONE** | — | Gaps §1 | PENDING | PENDING |
| AC3 | Forced-failure run is not `GO` | Manual QA | `Checks Not Run` names it | **NOT DONE** | — | Gaps §1 | PENDING | PENDING |
| AC4 | Every subagent return ≤10 lines | Manual QA | Observed on the run | **NOT DONE** | — | Gaps §1 | PENDING | PENDING |
| AC5 | Roster is exactly seven + delegated scan | Plan test 1 | `05a`–`05g` exist; no `05h`–`05l` anywhere | Done | `.github/agents/` (verified, unchanged) | `test_retirement_reconciliation.py::test_pr_review_roster_is_exactly_seven_contiguous_agents`, `::test_orchestrator_and_delegated_security_scan_both_exist`, `::test_no_renumbered_predecessor_slug_survives_anywhere`, `::test_roster_propagates_to_all_three_generated_roots` | PENDING | PENDING |
| AC6 | No dangling references (3 pattern classes) | Plan test 2 | Slugs + display names + **prose forms** | Done | `README.md`, `docs/CODEBASE_CONTEXT.md`, `.github/agents/README.md` | `::test_documentation_surfaces_carry_no_retired_prose_form`, `::test_documentation_surfaces_carry_no_old_slug_or_display_name`, `::test_no_shipped_asset_names_a_retired_skill_or_command`, `::test_retired_skill_directories_are_absent_from_every_root`, `::test_agents_readme_roster_covers_every_pr_review_evaluator_on_disk` | PENDING | PENDING |
| AC6b | Stale counts corrected | DD-5 | Recount from disk, never arithmetic | Done | `README.md:130`, `docs/CODEBASE_CONTEXT.md:89` | `::test_root_readme_source_agent_count_matches_disk`, `::test_codebase_context_hidden_subagent_count_matches_disk` | PENDING | PENDING |
| AC6c | `.gitignore` reconciled | DD-1 | Fixture trackable, run output ignored | Done | `.gitignore:5-12` | `::test_gitignore_carries_no_retired_fixture_rule`, `::test_gitignore_tracks_the_pr_review_fixture_and_ignores_run_output` | PENDING | PENDING |
| AC7 | Stale command absent, replacement present | Plan test 3 | Name derived from propagator output | Done | `claude/commands/` (verified) | `::test_stale_claude_command_is_absent`, `::test_replacement_claude_command_exists_and_is_derived_not_assumed` | PENDING | PENDING |
| AC8 | Propagation clean and idempotent | Plan test 4 | Second run reports zero changes | Done | `scripts/propagate_master_assets.py` (read-only) | `::test_propagation_is_idempotent`, `::test_committed_tree_is_at_a_propagation_fixed_point` | PENDING | PENDING |
| AC9 | Test baseline reconciled and explained | Existing suite | Delta accounted for | Done | whole suite | Test Results below | PENDING | PENDING |
| AC10 | `cross-phase-decisions.md` reconciled | Code review | Falsified claims corrected | Done | `.github/learnings/cross-phase-decisions.md` | AC10 section below | PENDING | PENDING |
| AC11 | Deferred capabilities recorded with routing | Code review | Not dropped, not reworded closed | Done | `.github/learnings/cross-phase-decisions.md` | AC11 section below | PENDING | PENDING |
| — | Plan test 5: no status-line write-back, re-verified | Plan test 5 | Assembled roster | Done (existing) | — | `test_readiness_synthesis_agents.py::test_readiness_synthesizer_writes_no_status_line_anywhere`, `::test_orchestrator_writes_no_status_line_anywhere` — re-run green on the assembled roster; not duplicated | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1–AC4 | Fixture dry run, single-interaction, forced-failure, return discipline | **NOT DONE — recorded open with routing** | — | No agent-spawning tool in this context. The recorded blocker (five of eight roster names unresolvable) **is gone** — all 8 now resolve. Manufacturing a partial run would produce below-GO evidence by construction. Gaps §1. |
| AC5 | Roster is exactly seven plus `04e` | Done | `.github/agents/` | Verified, not changed. Roster was already correct; the *catalogue* describing it was not (AC6). |
| AC6 | No dangling references, three pattern classes | Done | 3 doc surfaces | Prose form was the live defect on 2 of 3 surfaces. Catalogue also had a stale `05h` slug and a missing `05a` row. |
| AC6b | Stale counts | Done | `README.md`, `docs/CODEBASE_CONTEXT.md` | 43→**41**, 24→**22**. Both were *already wrong at baseline* — see below. |
| AC6c | `.gitignore` | Done | `.gitignore` | 4 dead rules removed; both directions now asserted through real traversal. |
| AC7 | Command reconciliation | Done | `claude/commands/` | Already correct; now pinned, with the name derived from `_claude_identifier_for`. |
| AC8 | Propagation | Done | — | Converged on run 1; zero generated-file diff noise. |
| AC9 | Baseline reconciled | Done | whole suite | 561→581 passed, exactly +20. |
| AC10 | Decision record | Done | `cross-phase-decisions.md` | 4 falsified claims corrected. |
| AC11 | Deferred capabilities | Done | `cross-phase-decisions.md` | 6 recorded open with owner + routing. |

## The four deferrals routed to this feature

### 1. `claude/agents/single-feature.md` — DELETED

The pruner can never remove it: it predates the generated marker, so
`_is_generated_output` fails closed — **correctly**, because that same guard is
what protects the hand-maintained `claude/agents/README.md`. To the pruner they
are indistinguishable, which is why this needed a human decision and not a pruner
change.

They are *not* indistinguishable to a reader, and that is the deciding evidence:
`README.md` is documentation. `single-feature.md` is a **loadable Claude subagent
definition with no source** — `name: single-feature`, `tools: Skill`,
`user-invocable: false`, while the real source (`single-feature-agent.agent.md`)
declares `Single Feature - Agent` and a six-tool grant. It is a stale, divergent
second copy of a live agent that Claude Code would load. Deleted.

Replaced the marker-guard test's hardcoded 2-name list with a derived invariant
(`test_claude_agents_root_holds_only_the_catalogue_and_generated_output`): every
file in `claude/agents/` is either the catalogue or carries the marker. A future
orphan now fails without anyone remembering to add it to a list.

### 2. `dev/phase-final-review/fixtures/` — RETIRED (13 files)

**The disposition the brief asked me to decide, and the claim it asked me to
honour is false.** Evidence, all direct:

| Claim | Verdict |
|---|---|
| "LIVE WIRING named by seven surviving agents" | **False.** `git grep` over `.github/agents/` returns **zero** hits for the fixture path, at every commit in this phase. |
| The real basis of that claim | A **conflation of two roots**. The seven agents declared the *report* root `dev/phase-final-review/PHASE_0N/` (output). No agent ever named the *fixture* root (input). |
| Even the true half | **Gone.** Feature `07` completed the report-root migration to `dev/pr-review/`; `test_report_root_migration_cannot_split_silently` now asserts the set is empty. |
| Its actual consumers | The five phase-shaped evaluators feature `02` deleted. Its `PHASE_05a`/`PHASE_05b` pseudo-subphase shape **is** the phase premise the rescope retired. |
| Its replacement | `dev/pr-review/fixtures/pinned-diff-range.md` (feature `04`). |
| The Phase document | Instructs retiring it. Dismissed as "moot — the directory does not exist", which was true of the report root and false of the fixtures. |
| "12 deletions sitting uncommitted, excluded from every commit" | **False.** `git status` was clean; all 13 files were tracked in `HEAD`. |

**Why it survived four features** is the reusable part, and it is recorded in the
learnings: the claim was made once by a review, then restated by features `04`,
`06`, and `07` as settled fact. Each restatement made it look better-attested
while adding no evidence. **Corroboration is not evidence when every corroborator
is quoting the same source.** A `grep` refuted it at any point.

### 3. AC13 fixture dry run — **NOT EXECUTED.** See Gaps §1.

The recorded blocker is gone and I verified that much:

| Precondition | Status |
|---|---|
| All 8 roster names resolve to an agent on disk | **Yes** — verified; was 3 of 8 when deferred |
| Report-root split | **Closed** (feature `07`) |
| Pinned range `f5ab960..e6ff28a` | **Resolves**: exactly 3 commits, 26 files, 1288 insertions — matches the fixture's recorded claims |
| Run output would pollute the tree | **No** — `.gitignore` fixed here (AC6c), which was the recorded reason to do it before the run |

The run itself was not performed: **this context has no agent-spawning tool**, and
a seven-evaluator fan-out cannot be simulated. Per the contract the plan quotes —
*a run whose required evaluators are recorded `not-run` is below-GO evidence, not
a passing run* — producing a partial artifact would be actively worse than
recording the gap.

### 4. The four missing agents — **CONFIRMED as fact; the stated cause is wrong**

The set identity is exact. At the phase baseline (`ae9823a`):

| Surface | Members | Missing |
|---|---|---|
| `expected_slugs` | 8 | `05a`, `05g`, `05j`, `05k` |
| Catalogue subagent table | 8 | `05a`, `05g`, `05j`, `05k` |

All four held `execute`. **So it is not a coincidence — but `execute` is not the
cause.** `expected_slugs` had a documented motive (omission dodged a blanket
`assertNotIn("execute", ...)`); **a README has no assertion to dodge**, so the
same motive cannot explain the catalogue.

The real shared cause is **category**: those four are the mechanical,
tool-running evaluators. The decomposition independently named its feature
`05-mechanical-evaluators` after exactly that set. `execute` is a *marker* of the
category (mechanical work needs shell), not the cause of the omission. Two
surfaces built from the same mental roster inherit the same gap.

Three pieces of evidence, none of which is the original claim:

- **It reproduced.** Feature `05` closed the `expected_slugs` half by *deriving* it
  from disk. Nothing derived the catalogue — and at `08` the catalogue still
  omitted `05a` and still listed `05f` under its retired `05h` slug, while the
  tested surface stayed correct. The defect survived on the untested surface.
- **It reproduced a third time, in the record itself.** `cross-phase-decisions.md`
  described the enumeration gap as omitting "`05g`/`05j`/`05k`" — dropping `05a`
  *while discussing `05a`'s `execute` one clause earlier*.
- **`05a` is doubly invisible**: its display name is `Baseline Worktree`, carrying
  no `05a` prefix, so any roster eyeballed by display name loses it silently.

**Not a coincidence; not caused by `execute`.** Fixed by derivation, not
vigilance: `test_agents_readme_roster_covers_every_pr_review_evaluator_on_disk`
derives the expectation from `.github/agents/`.

### 5. `phase-03-phase-final-review-execution-manifest.md` — DELETED
### 6. Propagation non-idempotence — recorded open with routing (AC11)

## AC6b — why "recount, never arithmetic" was load-bearing

DD-5 insisted on recounting from disk. It was right, and not for the reason
given: **both claims were already wrong at the baseline.**

| Claim | Stated | Actual @ baseline | Actual @ HEAD | Arithmetic would give |
|---|---|---|---|---|
| Root README source agents | 43 | **46** | **41** | 43−5 = 38 ✗ |
| CODEBASE_CONTEXT hidden subagents | 24 | **27** | **22** | 24−5 = 19 ✗ |

Subtracting this phase's five deletions from a wrong number produces a *newly*
wrong number that looks derived. Both are now asserted against disk.

Also corrected: root README claimed `prod-code-review.md` is the only non-`.agent.md`
exception. `docs-writer.md` is a second one. Found by counting rather than reading.

## AC10 — falsified claims corrected

| Claim | Correction |
|---|---|
| "Development fixtures keep legacy phase identifiers… renaming invalidates the fixture contract" | Struck. Both roots gone. Advice preserved for the *new* pinned fixture. |
| "`dev/phase-final-review/fixtures/PHASE_05/` … seven surviving agents name the fixture root as live wiring" | Refuted + closed. See deferral §2. |
| "The migration itself is still open and still owned by `05`–`07`" | Closed. Feature `07` migrated the last entry and **converted** the guard rather than deleting it as its own docstring invited. |
| "**The rescope rebuilds that path, so the validator arrives with the rebuild**" (P5-SEC-02) | Struck. The rescope rebuilt the readiness path **as agent Markdown**, not code. P5-SEC-02 still open. |
| "the propagation-enumeration gap omitting `05g`/`05j`/`05k`" | Corrected to **four** — `05a` was dropped. See deferral §4. |

**AC10's named target — the allowlist "forcing function" entry — was verified
consistent with what shipped and needed no edit.** DD-8 predicted this ("AC10 is
verification, not authoring"). Its two corrections match the as-built state:
per-agent scoping is genuinely inexpressible on Claude, and the orchestrator does
hold unrestricted `execute` regardless, so the `gh` grant widens nothing.

## AC11 — deferred capabilities recorded with routing

Six, each with owner + routing, none reworded into looking closed:

1. **Per-agent command scoping** → hook-owning phase; per-agent `PreToolUse` hook.
2. **`NO-GO` enforcement hook** → hook-owning phase. The verdict is advisory.
3. **P5-SEC-02** → verified still open (feature `07` left it open, correctly).
4. **Propagation non-idempotence across reclassification** → propagator-owning
   feature; `_claude_identifier_for` identifier resolution.
5. **The AC13 dry run** → QA stage or any context that can spawn subagents.
6. **User-local config naming retired skills** → acknowledged, unclosable.

**Security accounting, stated honestly:** the phase set out to narrow every `05x`
`execute` grant and **could not**. What it achieved is narrower and real:
`execute` *removed* where unneeded (`05`), *never added* where absent (`06`),
*retained only* where a named command has no non-shell equivalent (`05a`'s
`git worktree`; the orchestrator's `git symbolic-ref`/`merge-base`/`branch`).
Removal is the only narrowing the target formats can express. **No shell/Bash
permission was granted or restored anywhere in this feature.**

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.gitignore` | Modify | Removed 4 dead `dev/phase-final-review/` rules | AC6c / DD-1 |
| `README.md` | Modify | `43`→`41`; "Phase Final Review orchestration and evaluators"→"PR Review…"; added `docs-writer.md` as a second suffix exception | AC6, AC6b, DD-4, DD-5 |
| `docs/CODEBASE_CONTEXT.md` | Modify | `24`→`22`; "Phase Final Review evaluators"→"PR Review evaluators"; "security scan"→"diff security scan" | AC6, AC6b, DD-4, DD-5 |
| `.github/agents/README.md` | Modify | Added the missing `Baseline Worktree` row; `05h Test Health`→`05f Test Health` | AC6 / deferral §4 |
| `.github/learnings/cross-phase-decisions.md` | Modify | 4 falsified claims corrected; 6 deferrals recorded with routing | AC10, AC11 |
| `claude/agents/single-feature.md` | **Delete** | Unsourced, divergent duplicate agent | Deferral §1 |
| `dev/phase-final-review/**` (13 files) | **Delete** | Phase-shaped fixture; consumers deleted | Deferral §2 |
| `dev/feature/phase-03-phase-final-review-execution-manifest.md` | **Delete** | Pre-rescope manifest | Deferral §5 |
| `claude/learnings/cross-phase-decisions.md` | Modify | **Propagator-produced**, not hand-edited | AC8 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_retirement_reconciliation.py` | Create | 20 tests. `SHIPPED_ASSET_PREFIXES` is an **allowlist**; `_assert_once` reused from feature `07` | AC5–AC8 + deferrals |
| `tests/test_propagate_master_assets.py` | Modify | Marker-guard's hardcoded 2-name unmarked list → single `README.md` assertion (`single-feature.md` deleted); rationale inline | Deferral §1 |

## Test Results

- **Baseline**: `1 failed, 561 passed, 108 subtests passed` (clean tree, `6bb7e23`)
- **Final**: `1 failed, 581 passed, 106 subtests passed`
- **New tests added**: 20
- **Regressions**: None.

**The 1 failure is PERF-01** — pre-existing, Phase 04's open release blocker, and
not this feature's. No file under `tests/hooks/` or `.github/hooks/` was touched
and the 50 ms threshold was not altered. Treating `1 failed (PERF-01 only)` as
green, per the orchestrator's verified finding.

**AC9 reconciliation, against *passed* (not collected):**

```
561 (baseline passed)
+20 (tests/test_retirement_reconciliation.py: 20 new tests)
=581  == actual final passed count

108 (baseline subtests)
 -2 (test_marker_guard_matches_every_real_generated_file: a 2-item subTest loop
     over ("README.md", "single-feature.md") became a single assert once
     single-feature.md was deleted)
=106  == actual final subtest count
```

Both numbers are explained. Stated against *passed* deliberately: an earlier
implementer on this phase shipped a red suite while claiming green, having
reconciled to *collected*.

## Evidence: Mutation Sweep

**Two rounds, 40 mutations, 0 inert at final state.** Each mutation is applied to
a real file, the named test run, the file restored; a mutation whose test still
passes is reported INERT.

**Round 1 (19 mutations) — found 2 INERT.** Round 2 (21 mutations) deliberately
targeted assertions round 1 never covered: the opposite direction of each
one-directional check, and every *other* member of each set a guard claims to
cover (all three doc surfaces, all four generated roots, all seven roster
members, the `_assert_once` 2+ direction).

**Both inert guards were mine, and both are the class this phase keeps hitting:**

| Inert guard | Why it could never fail | Fix |
|---|---|---|
| `test_agents_readme_roster_covers_every_pr_review_evaluator_on_disk` | `name in catalogue` is satisfied by any **superstring** — renaming a row to `Baseline Worktreex` kept it green. The same substring hole as `GO` inside `GO WITH CONDITIONS`. | Match the whole bolded table cell `\| **{name}** \|` via `_assert_once` |
| `test_gitignore_tracks_the_pr_review_fixture_and_ignores_run_output` | Built on `git check-ignore -q`, which is **wrong twice**: it exits 0 when *any* rule matches **including a negation**, so an explicitly un-ignored path is indistinguishable from an ignored one; and its per-path matching disagrees with real traversal for nested paths. The guard passed while both halves of the contract were broken. | Observe real traversal via `git status` on a scratch file, both directions |

The round-1 sweep also **left residue that round 1 could not see**: an empty
`dev/phase-final-review/` directory survived, invisible to `git status` (git
tracks files, not directories) and inside a gitignored tree, so doubly invisible.
`test_retired_phase_shaped_fixture_is_gone` caught it on the next full-suite run.
The harness now records and removes created directories; final state verified
clean by `find` **and** `git status`, and propagation re-run to convergence after.

A third check worth naming: `test_gitignore_...`'s first half asserts the fixture
is tracked via `git ls-files`, which reads the **index** — `.gitignore` cannot
affect an already-tracked file, so no `.gitignore` mutation can ever break it.
That assertion is real (the fixture *is* committed) but it does not test the
un-ignore rule. A second probe on a *new* path was added to cover the rule the
first half cannot reach.

## Deviations from Plan

1. **The AC6 sweep is an allowlist (`SHIPPED_ASSET_PREFIXES`), not the plan's
   exclusion list.** Test-plan item 2 says "every tracked file outside
   `docs/phases/**` and `.github/learnings/**`". Applied literally it fires on
   `tests/test_pr_review_skills.py` (which *holds the rename map*) and
   `tests/test_readiness_synthesis_agents.py` (which asserts the old names are
   absent) — the guards for the very thing being swept. The only way to keep an
   exclusion list green is to append exemptions until it stops sweeping. An
   allowlist asks "where would this *hurt*?" — a retired skill name is only
   harmful where something loads it — and does not grow under pressure. Backed by
   `test_retired_skill_directories_are_absent_from_every_root` so the narrower
   scope is not a hole. **Nothing was added to `EXEMPT_FILES`/`EXEMPT_SKILL_DIRS`.**
2. **DD-2's "exempt `dev/**`" was not applied.** Feature `02`'s review had already
   narrowed it to `dev/feature/` and DD-2's own rationale (the manifest's filename)
   is void — that manifest is deleted here. My sweep does not touch `dev/` at all.
3. **AC6's prose-form sweep is scoped to the three named surfaces, not repo-wide.**
   Repo-wide it false-positives on `04-phase-execute.agent.md:176` ("Step 6: Phase
   Final Review"), a heading that labels a **Prod Code Review** step — a genuine
   name collision, not a reference to the retired family. AC6's own wording scopes
   this class to the three surfaces. See Gaps §3.
4. **AC5 needed no source change** — the roster was already correct. The defect was
   in the *catalogue* describing it. Verified rather than assumed.
5. **Plan test 5 was not duplicated.** Feature `07`'s two status-line tests already
   assert it on the assembled roster; re-run green. Writing a third would fork the
   assertion.
6. **Feature `07`'s roster-resolution test was not duplicated** for the same reason —
   it already asserts *every* entry resolves.

## Gaps

1. **AC1–AC4 (the dry run) are NOT DONE.** This is the phase's largest open risk and
   the feature's own core acceptance criterion. **This agent family has still never
   demonstrably worked end to end** — eight features passed review in isolation and
   nothing has run them together. Not performable here: no agent-spawning tool, so a
   seven-evaluator fan-out cannot be executed or simulated. Every precondition is now
   verified (roster resolves 8/8, fixture range checks out, report root migrated,
   run output gitignored), so the run is *possible* for the first time — it just was
   not *performed*. Recorded open with owner + routing. **Do not read this feature's
   green suite as evidence the family runs.**
2. **Live scratch-repo QA not performed** (`origin/HEAD` unset, base correction, no
   PR open, unauthenticated `gh`; Claude/OpenCode/Codex each loading the family).
   The plan forbids running it against this repository and no scratch consumer repo
   exists here. Left unchecked in the tasks file with reasons, per instruction.
3. **`04-phase-execute.agent.md:176` "### Step 6: Phase Final Review"** — a live
   agent carries the retired family's prose name as a step heading. It refers to
   **Prod Code Review**, so it is a name collision rather than a dangling reference,
   and `04-phase-execute` is outside this feature's scope (touching it re-propagates
   an unrelated orchestrator to three roots). Recorded rather than fixed; a reader
   looking up "Phase Final Review" will find nothing, so a future rename to "Step 6:
   Prod Code Review" is worth doing where that file is owned.
4. **`docs/CODEBASE_CONTEXT.md:87-88` carries two more count claims** — "6
   orchestrators" and "11 visible user-facing agents" — that disagree with disk (19
   user-invocable; the 3 auditors it counts as user-invocable are
   `user-invocable: false`), and its 6-orchestrator list omits `05 PR - Review`
   while `.github/agents/README.md:410` says "Four orchestrators" naming a different
   set. **This phase did not falsify them — they were already wrong at baseline and
   this phase changes neither number.** AC6b scopes to the counts this phase makes
   false. Recorded rather than silently widened into scope; the two definitions of
   "orchestrator" need reconciling by whoever owns that doc.
5. **`opencode/skills/` and `codex/skills/` do not exist** as roots; the retired-skill
   directory check covers them defensively and passes vacuously for those two. Not a
   defect — the check is real for `.github/skills/` and `claude/skills/`.

## Reviewer Focus Areas

- **The `dev/phase-final-review/fixtures/` retirement is the highest-value second
  opinion.** I deleted 13 tracked files against a claim, recorded in the learnings
  and restated by four features, that they were live wiring. My evidence is that no
  agent has ever named the *fixture* root (`git grep`, zero hits in `.github/agents/`)
  and that the claim conflated it with the *report* root, which feature `07` migrated.
  If that reading is wrong, this is the deletion to catch.
- **The AC6 sweep is an allowlist, deliberately** (Deviation §1). It is the broadest
  design call here. My argument is that an exclusion list with false positives dies by
  exemption, and that `tests/` cannot cause a load failure. If you disagree, the
  alternative is exempting two test modules by name — which is what I was told not to do.
- **Deferral §4's causal claim.** I confirmed the set identity and *refuted* the
  `execute` explanation, substituting "category". The falsifiable part: a README has no
  assertion to dodge, so `execute` cannot explain that half. Worth a second read.
- **`_git_sees` creates and deletes real files inside the repo** to observe traversal.
  It is the only honest oracle (`git check-ignore` demonstrably lies here), but it is a
  test with a side effect in the working tree; cleanup is in `finally`.
- **AC1–AC4 are not done.** Confirm the routing is adequate and that shipping this
  phase with an unrun family is a decision someone is making deliberately.
