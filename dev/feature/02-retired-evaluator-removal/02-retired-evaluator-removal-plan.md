# 02 Retired Evaluator Removal

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** no
- **Depends on:** 01-propagator-orphan-pruning
- **Key files modified:** `.github/agents/05c-qa-consolidator.agent.md` (delete), `.github/agents/05d-security-rollup.agent.md` (delete), `.github/agents/05e-ac-regression.agent.md` (delete), `.github/agents/05f-seam-analyzer.agent.md` (delete), `.github/agents/05i-learnings-harvester.agent.md` (delete), `.github/agents/05-phase-final-review.agent.md` (orchestrator `agents:` roster + body mentions), `.github/agents/README.md`, `tests/test_propagate_master_assets.py`, `tests/test_readiness_synthesis_agents.py`, generated outputs in `claude/`, `opencode/`, `codex/`
- **Sequential reason:** runtime dependency on `01-propagator-orphan-pruning` (generated outputs cannot be removed without it); shares `tests/test_propagate_master_assets.py` with upstream `01-propagator-orphan-pruning`; shares `.github/agents/05-phase-final-review.agent.md` with downstream `04-pr-review-orchestrator`

## Ordering Note

The Phase document sequences retirement **last** (Deliverable 7), reasoning that
it is "the integration point where dangling references surface." That rationale is
sound and is preserved — but it applies to *reconciliation*, not to *deletion*.
This feature performs the deletion early; `08-retirement-reconciliation` keeps the
integration role and stays last.

Deleting first is strictly cheaper. Every surviving `05x` agent body references
the `phase-final-review-conventions` and `phase-final-review-report` skills, which
`03-pr-review-conventions-skills` renames. If the five doomed agents are still
present at that point, the rename must update five files that are about to be
deleted, `tests/test_readiness_synthesis_agents.py` must keep asserting against
`05i-learnings-harvester` until the end, and every intermediate feature carries
five dead agents through its blast radius. Deleting them now removes them from the
blast radius of features `03` through `07`.

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1** — These five source agents are deleted from `.github/agents/`:
  `05c-qa-consolidator.agent.md`, `05d-security-rollup.agent.md`,
  `05e-ac-regression.agent.md`, `05f-seam-analyzer.agent.md`,
  `05i-learnings-harvester.agent.md`.
- **AC2** — Their generated outputs are absent from **all three** roots after a
  propagation run, with no manual `git rm` of generated files. Verified absent:
  `claude/agents/z-qa-consolidator.md`, `z-security-rollup.md`,
  `z-ac-regression.md`, `z-seam-analyzer.md`, `z-learnings-harvester.md`;
  `opencode/agents/05c-qa-consolidator.md`, `05d-security-rollup.md`,
  `05e-ac-regression.md`, `05f-seam-analyzer.md`, `05i-learnings-harvester.md`;
  and the corresponding `codex/agents/*.toml`.
- **AC3** — `tests/test_propagate_master_assets.py:87`'s `expected_slugs` tuple no
  longer names any retired agent, and the `05d-security-rollup` conditional block
  (which asserts `"NO-GO"` and `"NOT RUN"` appear in that agent's body) is removed
  rather than left referencing a deleted file.
- **AC4** — `tests/test_readiness_synthesis_agents.py` no longer references
  `05i-learnings-harvester`. Three of its six tests are wholly about that agent
  (`test_learnings_harvester_declares_history_mining_and_draft_only_outputs`,
  `test_learnings_harvester_declares_scoped_read_only_history_fetch`,
  `test_learnings_harvester_history_fetch_propagates_without_shell_access`) and are
  deleted; a fourth
  (`test_both_agents_honor_shared_return_contract_and_readiness_tier`) asserts
  against both agents and must be narrowed to the survivor.
- **AC5** — `.github/agents/README.md` no longer lists any retired agent. Known
  rows: lines 164–167 (`05c`–`05f`) and 171 (`05i`), plus line 169's **Security
  Scan** row, which declares its parent as `05d Security Rollup` — a parent that
  will not exist — **and the prose at line 243, which repeats the same parent claim
  outside the tables.** `Security Scan` itself survives and must be re-parented or
  its parent column corrected, not deleted.
- **AC5b** — `.github/agents/05-phase-final-review.agent.md:5` lists **all five**
  retired agents in its `agents:` frontmatter roster, and its body mentions them in
  three further places (the model-tier assignment table and the fan-out
  instructions). The roster is trimmed to the survivors here. This is a partial
  touch of a file that `04-pr-review-orchestrator` later rescopes wholesale — the
  minimum needed so that no surviving agent declares a deleted child (AC-test 5).
- **AC6** — No file references a retired agent by slug or by display name, except
  these **exempt paths**, which are either historical records or resolved by a later
  feature:

  | Exempt path | Why |
  |---|---|
  | `docs/phases/**` | historical phase records; must retain them |
  | `.github/learnings/**` | decision history; must retain them |
  | `claude/learnings/**` | **propagated copy** of the above — generated, not authored |
  | `.github/skills/phase-final-review-{conventions,report}/` | their report rosters name retired evaluators; `03-pr-review-conventions-skills` rescopes them. Deferring is deliberate: rewriting a skill this feature does not own would collide with feature `03` |
  | `claude/skills/`, `opencode/skills/`, `codex/skills/` (same two skills) | propagated copies of the above |

  `08-retirement-reconciliation` re-runs this sweep with the skill exemptions
  removed, once feature `03` has resolved them.
- **AC7** — The full test suite passes with an **explained** count delta. Baseline
  is 416 passed / 15 subtests (4 consecutive runs, 2026-07-16). The expected
  post-deletion figure before new tests are added is **413 passed / 10 subtests**:
  three whole `05i-learnings-harvester` tests are deleted, and the `expected_slugs`
  subtest count drops from 15 to 10 as five retired slugs leave the tuple. A count
  that does not land there is a signal, not a rounding error.

### Non-Goals

- Renaming or renumbering any surviving agent — that is features `03`–`07`.
- Rescoping any surviving agent's content.
- Removing `security-scan.agent.md` / the `Security Scan` agent. It is a
  general-purpose agent that outlives its `05d` parent and is referenced elsewhere.
- Retiring `dev/phase-final-review/` — **verified 2026-07-16: this directory does
  not exist.** The Phase document instructs retiring
  `dev/phase-final-review/fixtures/PHASE_05/` and `dev/phase-final-review/PHASE_05/`;
  both are already absent. The `cross-phase-decisions.md` note that fixtures "keep
  legacy phase identifiers" describes files that are not on disk. Nothing to do.
- Updating `docs/`, `README.md`, or `docs/CODEBASE_CONTEXT.md` — deferred to
  `08-retirement-reconciliation`, which owns documentation reconciliation.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1 | `.github/agents/` (5 deletions) | Code-review evidence |
| AC2 | generated roots; `scripts/propagate_master_assets.py` prune | Must-have automated test (new) — asserts absence in all three roots |
| AC3 | `tests/test_propagate_master_assets.py:87` | Existing test to update |
| AC4 | `tests/test_readiness_synthesis_agents.py` | Existing test to update (delete 3, narrow 1) |
| AC5 | `.github/agents/README.md` | Code-review evidence |
| AC6 | repository-wide | Must-have automated test (new) — reference sweep |
| AC7 | full suite | Existing suite regression |

## B. Correctness & Edge Cases

**The `Security Scan` re-parenting is the trap.** `05d-security-rollup` declares
`agents: [Security Scan]`, and `README.md:169` documents `Security Scan` as its
subagent. Deleting `05d` orphans `Security Scan`'s parent claim. `Security Scan`
must survive — the Phase delegates security to `04e-diff-security-scan`, which is
a *different* agent. Deleting `security-scan.agent.md` by association would remove
a working, separately-referenced agent.

**`_build_agent_reference_map` rewrites by display name.** The propagator replaces
occurrences of an agent's `name` in prose with the target identifier
(`_rewrite_agent_references`, sorted longest-first). Deleting a source agent
removes its entry from that map, so any surviving text still saying
"05d Security Rollup" stops being rewritten and silently ships as literal prose in
generated output. A reference sweep (AC6) catches this; the propagator will not.

### Failure modes

| Mode | Handling |
|---|---|
| Prune from `01` misfires and deletes a live agent | The full suite plus `01`'s inert-run test are the backstop; all generated roots are committed, so `git checkout -- claude/ opencode/ codex/` restores |
| `Security Scan` deleted as collateral | AC5 explicitly retains it; the reference sweep asserts it still exists |
| A retired name survives in a surviving agent's prose | AC6 sweep; it will no longer be rewritten and becomes a dangling literal |
| `expected_slugs` updated but the `05d` conditional left in place | AC3 names the conditional specifically; it references a file that will not exist |
| Test count drops and is read as regression | AC7 requires explaining the delta, not just recording it |

## C. Consistency & Architecture Fit

Deletion follows no special pattern — the assets are Markdown files under
`.github/agents/`, and propagation regenerates the three roots. The only
architectural commitment is **not to hand-delete generated files**: if
`01-propagator-orphan-pruning` does not remove them, that is a bug in `01`, not a
cue to `git rm` the outputs. Hand-deleting would mask the defect and it would
return on the next rename.

Proposed test symbol, `[PROPOSED - name TBD]`: a repository-wide reference-sweep
test asserting no retired slug or display name appears outside the allowed
historical paths.

## D. Clean Design & Maintainability

This feature only removes. The maintainability risk is *incomplete* removal —
leaving one row in a table or one name in a prose list. The reference sweep (AC6)
is what converts "I looked" into "the suite checks."

**Duplication risk**: the retired-name list will appear in the sweep test and in
the plan. Define it once in the test as a module constant.

### Keep-it-clean checklist

- [ ] Five source files gone
- [ ] Zero generated files hand-deleted
- [ ] `Security Scan` still exists and its parent claim is corrected
- [ ] Retired names appear only in `docs/phases/**` and `cross-phase-decisions.md`
- [ ] Test-count delta explained

## E. Completeness: Observability, Security, Operability

**Observability decision** — None. No new logging. This feature deletes static
assets; `git status` and the propagation counters from `01` are the entire
observability surface, and they already exist.

**Security** — Retiring `05d-security-rollup` removes a phase-level security
rollup. This is **not** a coverage regression: the rollup aggregated *per-subphase
security reports*, a shape with no PR analogue, while the diff-scoped security
check it wrapped is delegated to the existing `04e-diff-security-scan` in
`04-pr-review-orchestrator`. The distinction matters — if `04` did not exist, this
deletion *would* be a regression. Verify `04e-diff-security-scan` still exists
before deleting `05d`, and record that check.

**Runbook** — Verify: propagation run leaves no retired asset in any root; full
suite green. Rollback: `git revert` the feature commit; all deleted assets are in
history.

## F. Test Plan

**Existing tests to update**
- `tests/test_propagate_master_assets.py` — `expected_slugs` tuple and the
  `05d-security-rollup` conditional (AC3).
- `tests/test_readiness_synthesis_agents.py` — delete 3 tests, narrow 1 (AC4).

**Must-have automated tests (new)**

Top-value cases:

1. **Retired agents absent from source.** Given the repo, when the agent loader
   runs, then no retired slug is present.
2. **Retired agents absent from all three generated roots.** Given a propagation
   run, then no retired output file exists in `claude/agents/`,
   `opencode/agents/`, or `codex/agents/`. This is the test that proves feature
   `01` works, and it is the reason `01` must land first.
3. **Reference sweep (AC6).** Given every tracked file outside the exempt paths
   enumerated in AC6, then no retired slug or display name appears. Must cover
   display names (`05c QA Consolidator`) as well as slugs, because
   `_rewrite_agent_references` matches on display name. The exempt set must be a
   module constant shared with the assertion — an exception list that drifts from
   the thing it excepts is how `claude/learnings/` (a *propagated copy* of an
   exempt file) would sneak through.
4. **`Security Scan` survives.** Given the retirement, then
   `.github/agents/security-scan.agent.md` still exists and propagates.
5. **No orphaned parent claim.** Given the surviving agent set, then no agent's
   `agents:` frontmatter list names a deleted agent.

**Test data / fixtures** — none.

## Unverified Assumptions

- That `Security Scan` has a sensible home after `05d` is deleted. It is
  referenced by `README.md:169` and `:243` as `05d`'s subagent. Whether it becomes
  standalone, re-parents to another orchestrator, or is itself a retirement
  candidate is **not** settled by the Phase document. Narrow question, deliberately
  left to the implementer with a recorded decision; do not silently delete it.

## Relationship to Sibling Plans

- **Depends on `01-propagator-orphan-pruning`** — a hard runtime dependency. AC2 is
  unachievable without it.
- **Shrinks the blast radius of `03`–`07`.** Every downstream feature that renames
  a skill or renumbers an agent touches fewer files because these five are gone.
- **`08-retirement-reconciliation`** owns the documentation half of the Phase's
  Deliverable 7 and remains the last feature.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16); the affected modules are directly covered.
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Confirm the Security Delegation Path

**Goal**: Verify `04e-diff-security-scan` exists, is diff-shaped, and holds no
`execute`, so that deleting `05d-security-rollup` is a shape change rather than a
coverage loss. Record the finding.
**Success Criteria**: Written confirmation in the implementation record; if `04e`
is missing or unsuitable, stop and escalate rather than deleting `05d`.
**Note**: this gate is already satisfied on inspection —
`.github/agents/04e-diff-security-scan.agent.md` exists with
`tools: [read, search, edit]` and no `execute`. Confirm it still holds and record
it; do not skip the check on the strength of this note.
**Status**: Not Started

## Stage 1b: Trim the Orchestrator Roster

**Goal**: Remove the five retired agents from
`.github/agents/05-phase-final-review.agent.md:5`'s `agents:` frontmatter and from
its three body mentions, so no surviving agent declares a deleted child.
**Success Criteria**: AC5b; the orphaned-parent-claim test passes. Touch only the
roster and those mentions — `04-pr-review-orchestrator` rescopes this file
wholesale later, and a broader edit here would collide with it.
**Status**: Not Started

## Stage 2: Delete Sources and Propagate

**Goal**: Remove the five source agents; run propagation; confirm all three roots
self-clean via feature `01`.
**Success Criteria**: AC1, AC2. Zero generated files hand-deleted.
**Status**: Not Started

## Stage 3: Reconcile Tests

**Goal**: Update `expected_slugs` and remove the `05d` conditional; delete the
three `05i` tests and narrow the shared one; add the absence and reference-sweep
tests.
**Success Criteria**: AC3, AC4; suite green with an explained count delta.
**Status**: Not Started

## Stage 4: Reconcile the Agent README and Sweep

**Goal**: Remove retired rows from `.github/agents/README.md`, correct the
`Security Scan` parent claim, and run the reference sweep to extinction.
**Success Criteria**: AC5, AC6, AC7.
**Status**: Not Started
