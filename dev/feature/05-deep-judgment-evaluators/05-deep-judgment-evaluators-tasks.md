# Feature Tasks: 05-deep-judgment-evaluators

## Stage 0: Prerequisite Verification

- [ ] Verify feature 01 deliverables exist on disk: `.github/skills/phase-final-review-conventions/SKILL.md`, `.github/skills/phase-final-review-report/SKILL.md`, `.github/skills/worktree-baseline/SKILL.md`, `.github/agents/05a-baseline-worktree.agent.md`; report missing prerequisites instead of proceeding
- [ ] Verify feature 02 deliverable exists: `.github/agents/05-phase-final-review.agent.md`; read its evaluator invocation prompt shape and not-run record format
- [ ] Resolve the actual fixture path from feature 01's implementation record (proposed: `dev/phase-final-review/fixtures/`) and confirm both pseudo-subphase directories are present
- [ ] Read the AC-regression matrix template and attribution vocabulary (`regressed-by`, `unknown`) from `phase-final-review-report` — do not restate them per-agent

## Stage 1: 05b Change Narrator (AC1, AC4)

- [ ] Author `.github/agents/05b-change-narrator.agent.md` in the `04a`–`04d` lettered-subagent house style (frontmatter: `name`, `description`, `tools`, `user-invocable`)
- [ ] Declare top-tier model requirement per the phase model-tier policy
- [ ] Load `phase-final-review-conventions`; write the report to the conventions-defined location under `dev/phase-final-review/PHASE_0N/`; honor the ≤10-line return contract
- [ ] Specify the baseline→HEAD narrative procedure: per-subphase attribution and multi-subphase churn hotspot identification
- [ ] State diff-chunking constraints: chunk by directory/subphase, never load the full phase diff into one context, spawn per-directory readers as the pressure valve
- [ ] Consume the baseline worktree from `05a-baseline-worktree`; define the baseline-unavailable path: report not-run with reason per partial-failure semantics
- [ ] Manual QA check 1: dry-run 05b via the orchestrator against the fixture — narrative attributes changes to each pseudo-subphase, lists files touched by both as churn hotspots, and the run is visibly chunked (no single full-diff read)

## Stage 2: 05e AC Regression (AC2, AC4)

- [ ] Author `.github/agents/05e-ac-regression.agent.md` in house style, top-tier model, loading `phase-final-review-conventions`
- [ ] Define hidden-verifier spawning: one verifier per subphase, phrased like existing orchestrator delegation patterns; verifier contract identical to the evaluator contract (report to disk, ≤10-line return)
- [ ] Require the verifier to enumerate EVERY AC from its subphase summary before verification, so the roll-up can prove no AC was silently omitted
- [ ] Output the AC-regression matrix per the `phase-final-review-report` template: one row per AC with pass/fail/not-verifiable status
- [ ] Handle untestable-by-inspection ACs (e.g., manual-QA-only): mark not-verifiable with reason; surface the not-verifiable count in the matrix summary
- [ ] Handle later-subphase-broke-earlier-AC: attribute the regression to the breaking subphase when narrative/commit evidence supports it, else mark attribution `unknown` (vocabulary from the report skill)
- [ ] State the no-baseline case: 05e proceeds against the final tree and records that baseline comparison was skipped
- [ ] Explicitly exclude re-running automated test suites (non-goal — verification by inspection and existing evidence only)
- [ ] Manual QA check 2: count all ACs in both fixture pseudo-subphase summaries first, then dry-run 05e via the orchestrator — matrix row count equals total AC count, every row has a status, manual-QA-only ACs are marked not-verifiable

## Stage 3: 05f Seam Analyzer (AC3, AC4)

- [ ] Author `.github/agents/05f-seam-analyzer.agent.md` in house style, top-tier model, loading `phase-final-review-conventions`
- [ ] Define the seam analysis procedure: interface mismatches, duplicated logic, and orphaned scaffolding between subphases, built on `get_impact_radius` and `get_bridge_nodes` (names copied exactly from the Phase document)
- [ ] Verify `get_bridge_nodes` against the live code-review-graph server; if the name differs, report the mismatch upward rather than renaming
- [ ] Define graceful degradation: when the graph server is unavailable, produce a not-run record with reason (per partial-failure semantics) instead of failing
- [ ] Define the no-shared-surface case: report "no seams detected" as a completed check, not a not-run
- [ ] State the no-baseline case: 05f proceeds against the final tree and records that baseline comparison was skipped
- [ ] Manual QA check 3: dry-run 05f via the orchestrator with the graph available (seam report exists) and with the graph stopped (not-run record with reason produced)

## Stage 4: Propagation and Verification (AC5 remainder, AC6)

- [ ] Run `scripts/propagate_master_assets.py`; confirm all three agents appear in every harness output (Claude, Codex, OpenCode)
- [ ] Run `uv run pytest tests/test_propagate_master_assets.py -q`; confirm it passes (full-suite baseline: 382 passed, 2 pre-existing unrelated failures)
- [ ] Manual QA check 4: confirm each evaluator's dry-run return summary is ≤10 lines with full detail on disk under `dev/phase-final-review/`
- [ ] Check agent inventory surfaces (`.github/agents/README.md`, `docs/CODEBASE_CONTEXT.md`, top-level README) for 05x listings established by features 01–04; update the same surfaces for 05b/05e/05f if a pattern exists (per review-learnings)
