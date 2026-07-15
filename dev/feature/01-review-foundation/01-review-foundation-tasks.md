# Feature Tasks: 01-review-foundation

## Stage 0: Test Prerequisites

- [ ] Confirm baseline: `.venv/bin/pytest tests/test_propagate_master_assets.py -q` passes before any changes (baseline: 19 passed, 2 subtests; no new automated tests required — deliverables are markdown assets)

## Stage 1: Skills

- [ ] Create `.github/skills/phase-final-review-conventions/SKILL.md` mirroring `auditor-conventions` structure, with `name` + `description` ("Use when:" clause) frontmatter (AC1)
- [ ] In the conventions skill, define report locations/naming under `dev/phase-final-review/PHASE_0N/`, severity levels, and the ≤10-line return-summary contract (AC1)
- [ ] In the conventions skill, define read-only worktree etiquette, model-tier notes, and partial-failure semantics: run completes when an evaluator fails; readiness report enumerates not-run checks; verdict may not be GO while any check is missing (AC1)
- [ ] In the conventions skill, define "missing artifact" precisely enough for feature 02's preflight to fail loudly on it (AC1, Section B)
- [ ] Reference `auditor-conventions` for shared audit norms rather than restating them; keep only phase-final-review-specific rules (Section D)
- [ ] Create `.github/skills/phase-final-review-report/SKILL.md` mirroring `implementation-record`-style template skills, with templates for: master QA doc, security rollup (fixed/persisting/reintroduced classification), AC-regression matrix, and go/no-go readiness report with severity-ordered blocking list (AC2)
- [ ] Include an explicit "checks not run" section in the readiness report template (AC2, Section B)
- [ ] Create `.github/skills/worktree-baseline/SKILL.md` defining the "check out commit X in a git worktree, return the path" procedure, reusable outside Phase Final Review (e.g., by `eval-grader`) (AC3)
- [ ] In the worktree skill, document cleanup expectations, read-only etiquette, handling of a baseline commit not present locally (clear failure message), and deterministic reuse-or-recreate for a pre-existing worktree at the target path (AC3, Section B)
- [ ] Verify all three skills contain no change-tracking language and use placeholder tokens consistent with existing template skills (Section D)

## Stage 2: Baseline Agent

- [ ] Create `.github/agents/05a-baseline-worktree.agent.md` following the frontmatter/house style of `04a-feature-plan-expander.agent.md` and `.github/agents/README.md`, including `name` and `description` frontmatter so propagation discovers it (AC4)
- [ ] Ensure the agent loads the `worktree-baseline` skill and returns only the worktree path plus a ≤10-line summary (AC4)
- [ ] Manual QA: follow the documented worktree procedure once against this repo with a known SHA; verify a read-only worktree exists at the returned path and can be removed cleanly (AC3/AC4 manual checks 2 and 4)

## Stage 3: Development Fixture

- [ ] Create the fixture tree under `dev/phase-final-review/fixtures/` `[PROPOSED - exact layout TBD]` with two pseudo-subphase directories (per phase doc: `PHASE_0Xa/`, `PHASE_0Xb/`) under one synthetic phase (AC5)
- [ ] Copy Phase 01 artifacts (SUMMARY, QA, QA_COVERAGE_MAP, qa-analysis, security-scan) from `docs/phases/PHASE_01/` into the first pseudo-subphase, without modifying the live directory (AC5)
- [ ] Copy Phase 02 artifacts from `docs/phases/PHASE_02/` into the second pseudo-subphase, including the genuine NO-GO security scan; decide whether to include `PHASE_02_DISCOVERY_CONTEXT.md` and record the decision (AC5, Discovery Delta)
- [ ] Write a fixture README documenting provenance (copied from Phase 01/02, safe to regenerate) and noting that implementation records do not exist in the source phases (AC5, Discovery Delta)
- [ ] Resolve the gitignore block: `dev/*` ignores the fixture path — add a negation rule (e.g., `!dev/phase-final-review/`) or `git add -f`, verify `git status` shows the fixture files as trackable, and record the choice in implementation notes (Discovery Delta warning)
- [ ] Manual QA: compare fixture inventory against `docs/phases/PHASE_01/` and `PHASE_02/` — every source artifact type present in pseudo-subphase layout, NO-GO verdict content included (manual check 3)

## Stage 4: Propagation

- [ ] Run `scripts/propagate_master_assets.py`; verify no script changes were needed (auto-discovery) (AC6)
- [ ] Verify all three skills and the 05a agent appear in `.claude/skills/`, `.claude/agents/`, and Codex/OpenCode outputs with `$source` tags and no diffs in unrelated assets (AC6, manual check 1)
- [ ] Verify propagated files landed only inside declared destination roots (per review-learnings propagator pattern)
- [ ] Run `.venv/bin/pytest tests/test_propagate_master_assets.py -q` and confirm it passes (AC6)
- [ ] Run the full suite `.venv/bin/pytest tests/ -q` and confirm no regressions beyond the 2 pre-existing hook-distribution failures (baseline: 382 passed, 2 failed)
