# Feature Tasks: 03-mechanical-evaluators

## Stage 0: Test Prerequisites

- [x] Confirm no new automated tests are required (markdown assets; propagation suite exists) — verify `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` passes as a pre-change baseline
- [x] Verify feature 01 contracts have landed: `.github/skills/phase-final-review-conventions/SKILL.md`, `.github/skills/phase-final-review-report/SKILL.md`, and the `dev/phase-final-review/fixtures/` fixture exist; stop and report to the orchestrator if missing
- [x] Verify feature 02 has landed: `.github/agents/05-phase-final-review.agent.md` exists and defines the evaluator invocation shape and not-run record format; stop and report if missing

## Stage 1: 05g Artifact Sweeper

- [x] Create `.github/agents/05g-artifact-sweeper.agent.md` following the `04a`–`04d` lettered-subagent house style (frontmatter: `name`, `description`, `tools`, `user-invocable: false`) (AC1)
- [x] Scope the sweep to artifacts introduced since baseline: debug statements, TODOs/FIXMEs, temporary feature flags, commented-out/dead code (AC1)
- [x] Instruct use of code-review-graph `refactor_tool` (`mode="dead_code"`) for dead-code detection, with explicit filtering of results to phase-touched files (baseline→HEAD diff list), since tool-level diff scoping is unverified — record this filtering approach in the agent instructions per the plan's Unverified Assumption (AC1)
- [x] Declare cheap-tier model assignment, aligned with the tier-declaration convention feature 02 established (mechanism is `[PROPOSED - name TBD]`; instructions-body declaration is the fallback) (AC1)
- [x] Load `phase-final-review-conventions`; write the sweep report to the conventions-defined path using the applicable `phase-final-review-report` template; return a ≤10-line summary (AC4)
- [x] Implement degradation rules: graph server unavailable → not-run record with stated reason (never silent pass); baseline worktree missing → not-run; empty phase diff → completed "nothing introduced since baseline" check (AC4)
- [ ] Manual QA check 1: dry-run 05g via the `05-phase-final-review` orchestrator against the fixture; verify the sweep report exists at the conventions-defined path and the return summary is ≤10 lines (AC5)
- [ ] Manual QA check 2: with the graph server stopped, verify 05g records not-run with reason and the orchestrator's verdict ceiling drops below GO (AC4, AC5)

## Stage 2: 05j Consistency Auditor

- [x] Create `.github/agents/05j-consistency-auditor.agent.md` in house style, detecting convention drift across subphases (naming, error handling, patterns) and recommending canonical forms (AC2)
- [x] Load `phase-final-review-conventions`; reference `auditor-conventions` severity norms via the conventions skill — never restate the taxonomy; use `phase-final-review-report` structures for the report; return a ≤10-line summary (AC4)
- [x] Implement degradation rules: baseline worktree missing → not-run with reason; empty phase diff → completed "nothing introduced since baseline" check (AC4)
- [ ] Manual QA check 3: dry-run 05j via the orchestrator against the fixture; verify its report names at least the known Phase 01-vs-02 stylistic differences (AC5)

## Stage 3: 05k Dependency Auditor

- [x] Create `.github/agents/05k-dependency-auditor.agent.md` in house style, inventorying new dependencies introduced across the phase and reporting licenses, vulnerabilities, and competing/duplicate libraries — read-only, never fetching or installing anything (AC3)
- [x] Declare cheap-tier model assignment consistent with 05g's mechanism (AC3)
- [x] Load `phase-final-review-conventions`; write the report to the conventions-defined path using `phase-final-review-report` structures; return a ≤10-line summary (AC4)
- [x] Implement degradation rules: baseline worktree missing → not-run with reason; no dependency manifest changes → completed "no new dependencies" check (AC4)
- [ ] Manual QA check 4: dry-run 05k via the orchestrator against the fixture (which has no dependency changes); verify it reports a completed "no new dependencies" check (AC5)

## Stage 4: Propagation

- [x] Run `scripts/propagate_master_assets.py` and confirm all three agents appear in Claude, OpenCode, and Codex outputs (Codex copies will carry the `z-` prefix for non-user-invocable agents) with no diff noise in unrelated assets (AC6)
- [x] Confirm no changes to `scripts/propagate_master_assets.py` were needed (verify-only; auto-discovery expected to work) (AC6)
- [x] Run `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` and confirm it passes (AC6)
