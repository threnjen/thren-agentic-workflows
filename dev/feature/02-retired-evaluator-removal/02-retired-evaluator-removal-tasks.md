# 02 Retired Evaluator Removal — Tasks

**Prerequisite:** `01-propagator-orphan-pruning` must be complete and merged. AC2 is unachievable without it.

**Retired agents (the canonical five):** `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`, `05f-seam-analyzer`, `05i-learnings-harvester`.

## Stage 0: Test Prerequisites

**Status: Not required.** Baseline 416 passed / 15 subtests across 4 consecutive full runs (2026-07-16); affected modules are directly covered.

- [x] Confirm baseline is still green before starting: `.venv/bin/python -m pytest tests/ -q` → expect 416 passed, 15 subtests

## Stage 1: Confirm the Security Delegation Path

- [x] Verify `.github/agents/04e-diff-security-scan.agent.md` exists (Plan Expander verified 2026-07-16 — confirm it has not changed)
- [x] Verify `04e` is diff-shaped and holds no `execute` (verified: `tools: [read, search, edit]`, `user-invocable: false`)
- [x] Verify `.github/agents/security-scan.agent.md` still exists and is not slated for deletion
- [x] Record the finding in the implementation record: retiring `05d` is a shape change (per-subphase rollup has no PR analogue), not a security-coverage regression, because the diff-scoped check is delegated to `04e`
- [x] **Gate:** if `04e` is missing or unsuitable, STOP and escalate — do not delete `05d`

## Stage 2: Delete Sources and Propagate

- [x] Delete `.github/agents/05c-qa-consolidator.agent.md` (AC1)
- [x] Delete `.github/agents/05d-security-rollup.agent.md` (AC1)
- [x] Delete `.github/agents/05e-ac-regression.agent.md` (AC1)
- [x] Delete `.github/agents/05f-seam-analyzer.agent.md` (AC1)
- [x] Delete `.github/agents/05i-learnings-harvester.agent.md` (AC1)
- [x] Remove the five retired agents from `.github/agents/05-phase-final-review.agent.md:5` `agents:` frontmatter list — **Discovery Delta D1: this file is not in the plan's Execution Metadata but is a required change.** Preserve `Baseline Worktree` verbatim; do not normalize it to `05a Baseline Worktree` (D10)
- [x] Reconcile the 3 remaining retired-agent mentions in the `05-phase-final-review.agent.md` body (`grep -c "05c\|05d\|05e\|05f\|05i"` → 3 at plan time)
- [x] Run propagation; confirm all three generated roots self-clean via feature `01` (AC2)
- [x] Verify absent from `claude/agents/`: `z-qa-consolidator.md`, `z-security-rollup.md`, `z-ac-regression.md`, `z-seam-analyzer.md`, `z-learnings-harvester.md` (AC2)
- [x] Verify absent from `opencode/agents/`: `05c-qa-consolidator.md`, `05d-security-rollup.md`, `05e-ac-regression.md`, `05f-seam-analyzer.md`, `05i-learnings-harvester.md` (AC2)
- [x] Verify absent from `codex/agents/`: the corresponding `z-*.toml` files (AC2)
- [x] **Zero generated files hand-deleted.** If any retired output survives propagation, that is a bug in `01` — escalate; do not `git rm` the output (AC2)

## Stage 3: Reconcile Tests

- [x] Remove the five retired slugs from `expected_slugs` in `tests/test_propagate_master_assets.py:87` (8 slugs → 3: `05b-change-narrator`, `05h-test-health`, `05l-readiness-synthesizer`) (AC3)
- [x] Delete the `05d-security-rollup` conditional at `tests/test_propagate_master_assets.py:119–121` (the `NO-GO` / `NOT RUN` body assertions) rather than leaving it referencing a deleted file (AC3)
- [x] Delete `test_learnings_harvester_declares_history_mining_and_draft_only_outputs` from `tests/test_readiness_synthesis_agents.py` (AC4)
- [x] Delete `test_learnings_harvester_declares_scoped_read_only_history_fetch` (AC4)
- [x] Delete `test_learnings_harvester_history_fetch_propagates_without_shell_access` (AC4)
- [x] Narrow `test_both_agents_honor_shared_return_contract_and_readiness_tier` (:94) to the survivor: drop `learnings_body` and its `"at most 10 lines"` assertion; keep the `READINESS_AGENT` assertions. Rename to reflect single-agent scope `[PROPOSED - name TBD]` (AC4)
- [x] Remove the `LEARNINGS_AGENT` module constant at `tests/test_readiness_synthesis_agents.py:6` (AC4)
- [x] Add new test: retired agents absent from source — no retired slug present when the agent loader runs (AC1)
- [x] Add new test: retired agents absent from all three generated roots after propagation — `claude/agents/`, `opencode/agents/`, `codex/agents/`. This is the test that proves feature `01` works (AC2)
- [x] Add new test: `Security Scan` survives — `.github/agents/security-scan.agent.md` still exists and propagates (AC5)
- [x] Add new test: no orphaned parent claim — no surviving agent's `agents:` frontmatter list names a deleted agent (covers D1 regression-side)
- [x] Define the retired-name list **once** as a module constant in the sweep test; do not duplicate it across tests
- [x] Run the suite; confirm green

## Stage 4: Reconcile the Agent README and Sweep

- [x] Delete `.github/agents/README.md` rows 164–167 (`05c QA Consolidator`, `05d Security Rollup`, `05e AC Regression`, `05f Seam Analyzer`) (AC5)
- [x] Delete `.github/agents/README.md` row 171 (`05i Learnings Harvester`) (AC5)
- [x] **Decide and record** `Security Scan`'s parent: correct row 169's parent column (currently `05d Security Rollup`, a parent that will not exist). Do NOT delete the row — `Security Scan` survives. The Phase does not settle whether it becomes standalone or re-parents; make the call and record the rationale in the implementation record (AC5, plan's Unverified Assumption)
- [x] Apply the same re-parenting decision to README **prose line 243** (`**Security Scan** *(subagent of 05d Security Rollup)*`) — **Discovery Delta D5: outside AC5's enumerated rows but the same claim** (AC6)
- [x] Build the AC6 reference sweep test `[PROPOSED - name TBD]`: every tracked file, matching **both slugs and display names** (`05c QA Consolidator` etc.), because `_rewrite_agent_references` matches on display name (AC6)
- [x] Sweep exclusion list must cover: `docs/phases/**`, `.github/learnings/`, **and the propagated learnings copies** — `claude/learnings/cross-phase-decisions.md` exists and carries retired names (**Discovery Delta D3**). Verify `opencode/` and `codex/` learnings roots at implementation time
- [x] **Resolve Discovery Delta D2 before the sweep can pass:** `.github/skills/phase-final-review-conventions/SKILL.md:33–36,39` names the five retired report filenames. AC6 allows no exception for it, but the plan's non-goals defer skill work to feature `03`. Recommended: prune the retired rows here (deletion is this feature's job; the *rename* is `03`'s). Escalate to the Decomposer if the boundary is contested
- [x] **Resolve Discovery Delta D4:** AC6 names `cross-phase-decisions.md` + `docs/phases/**`; test-plan case 3 names `docs/phases/**` + `.github/learnings/`. Pick one exclusion set — recommend directory-scoped — and encode it as the single constant
- [x] Run the sweep to extinction: no retired slug or display name outside the agreed exclusions (AC6)
- [x] Run the full suite: `.venv/bin/python -m pytest tests/ -q` (AC7)
- [x] **Explain the count delta, do not merely observe it** (AC7). Predicted (**Discovery Delta D9**): `tests/test_readiness_synthesis_agents.py` 6 → 3 tests (−3); `tests/test_propagate_master_assets.py` test count unchanged but subtests 8 → 3 slugs (15 → 10 subtests). Net before new tests: **416 → 413 passed, 15 → 10 subtests**. New tests add back. State the prediction, then reconcile actual against it
- [x] Verify the keep-it-clean checklist: five source files gone; zero generated files hand-deleted; `Security Scan` exists with a corrected parent claim; retired names only in allowed historical paths; test-count delta explained
