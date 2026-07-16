# Execution Manifest: Phase 05 — Phase Final Review Agent Family

- **Phase document**: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`
- **Discovery context**: `docs/phases/DISCOVERY_CONTEXT.md` (§ Phase 05 Design Notes)
- **Working branch**: `phase/phase-final-review`
- **Ordered feature task names**: `01-review-foundation`, `02-final-review-orchestrator`, `03-mechanical-evaluators`, `04-delegating-evaluators`, `05-deep-judgment-evaluators`, `06-readiness-synthesis`

Ordering note: feature order matches the Phase document's Key Deliverables sequence exactly; no reordering was needed.

Repo-wide sequencing constraint: every feature ends by running `scripts/propagate_master_assets.py`, which regenerates shared output files (`.claude/agents/`, `.claude/skills/`, Codex and OpenCode outputs), and every feature updates `.github/agents/README.md` (agent inventory). No two features are parallel-safe; the schedule is strictly sequential, one feature per wave.

Commit note: `.gitignore` line 5 (`dev/*`) ignores this directory — stage `dev/feature/` files with force-add, as was done for the phase-01/02 manifests.

## Feature Table

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---|---|---|---|---|
| `01-review-foundation` | 1 | no | none | `.github/skills/phase-final-review-conventions/SKILL.md`, `.github/skills/phase-final-review-report/SKILL.md`, `.github/skills/worktree-baseline/SKILL.md`, `.github/agents/05a-baseline-worktree.agent.md`, `.github/agents/README.md`, `dev/phase-final-review/fixtures/` `[PROPOSED - layout TBD]`, propagated outputs (generated), `scripts/propagate_master_assets.py` (verify) | shares propagated outputs and `.github/agents/README.md` with all features |
| `02-final-review-orchestrator` | 2 | no | `01-review-foundation` | `.github/agents/05-phase-final-review.agent.md`, `.github/agents/README.md`, propagated outputs (generated) | shares propagated outputs and README with all features; contract dependency on wave 1 skills |
| `03-mechanical-evaluators` | 3 | no | `01-review-foundation`, `02-final-review-orchestrator` | `.github/agents/05g-artifact-sweeper.agent.md`, `.github/agents/05j-consistency-auditor.agent.md`, `.github/agents/05k-dependency-auditor.agent.md`, `.github/agents/README.md`, propagated outputs (generated) | shares propagated outputs and README with all features; dry-runs through wave 2 orchestrator |
| `04-delegating-evaluators` | 4 | no | `01-review-foundation`, `02-final-review-orchestrator` | `.github/agents/05c-qa-consolidator.agent.md`, `.github/agents/05d-security-rollup.agent.md`, `.github/agents/05h-test-health.agent.md`, `.github/agents/README.md`, propagated outputs (generated) | shares propagated outputs and README with all features |
| `05-deep-judgment-evaluators` | 5 | no | `01-review-foundation`, `02-final-review-orchestrator` | `.github/agents/05b-change-narrator.agent.md`, `.github/agents/05e-ac-regression.agent.md`, `.github/agents/05f-seam-analyzer.agent.md`, `.github/agents/README.md`, propagated outputs (generated) | shares propagated outputs and README with all features |
| `06-readiness-synthesis` | 6 | no | all of waves 1–5 | `.github/agents/05l-readiness-synthesizer.agent.md`, `.github/agents/05i-learnings-harvester.agent.md`, `.github/agents/README.md`, propagated outputs (generated), dry-run artifacts under `dev/phase-final-review/` | integration feature — full-flow dry run requires every evaluator from waves 3–5 |

## Wave-by-Wave Execution Schedule

- Wave 1 (sequential): `01-review-foundation`
- Wave 2 (sequential): `02-final-review-orchestrator`
- Wave 3 (sequential): `03-mechanical-evaluators`
- Wave 4 (sequential): `04-delegating-evaluators`
- Wave 5 (sequential): `05-deep-judgment-evaluators`
- Wave 6 (sequential): `06-readiness-synthesis`

## Expected Bundle Files

Each `dev/feature/[0N-task-name]/` directory contains:

- `[0N-task-name]-plan.md`
- `[0N-task-name]-context.md`
- `[0N-task-name]-tasks.md`

All 18 files verified present for the six features listed above.

## Accepted Risks and Open Verifications (from Plan Expander Discovery Delta)

- `ledger-events.jsonl` is absent from real `eval/runs/` directories (only `ledger-commits.jsonl` observed); the orchestrator's preflight treats the events ledger as optional input, consistent with plan 02 AC3's "when present" wording.
- No `model:`/tier frontmatter precedent exists in any agent file; the tier-declaration mechanism is `[PROPOSED - name TBD]` and must be chosen once in feature 02 and reused verbatim in features 03–06.
- `refactor_tool` dead-code detection is repo-wide; 05g filters results to phase-touched files (plan 03 assumption, confirmed).
- `security-scan` defaults to whole-repo scanning and `test-analyst` outputs a reduction-plan file set; the 05d/05h wrappers must adapt scope and output shape (plan 04 assumptions, confirmed mandatory).
- `get_bridge_nodes` is named in the Phase document and exists on this workspace's code-review-graph server; re-verify against the live server at implementation time (plan 05).
- Phase 01/02 on-disk review records were deleted (commit 4dd01e9); 05i mines git history, PRs #19/#20, and eval ledgers instead (plan 06, updated).
- Fixture and dry-run artifacts under `dev/` require a gitignore negation or force-add to be committed (plan 01, updated).

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| None identified | — | Phase ships agent/skill markdown and a document fixture; no new automated test files are planned. Automated coverage rides on the existing propagation suite. |

### Existing Test Files Updated By Multiple Features

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/test_propagate_master_assets.py` (verify — updates expected only if asset auto-discovery misses a naming edge case) | all features | Propagation regression coverage; baseline 19 passed, captured 2026-07-15 |

### Manual QA Checklist

- [ ] Fixture inventory matches the Phase 01/02 source artifact types, in pseudo-subphase layout, including the Phase 02 NO-GO security content (feature 01)
- [ ] Preflight suggests a correct baseline with ledgers present, and again with `eval/runs/` emptied via the commit-message fallback (feature 02)
- [ ] Preflight refuses with an itemized message when a fixture artifact is deleted (feature 02)
- [ ] Each evaluator, dry-run through the orchestrator against the fixture, writes its report to the conventions-defined path and returns ≤10 lines (features 03–05)
- [ ] 05d classifies P2-SEC-01..03 as fixed/persisting/reintroduced in the rollup (feature 04)
- [ ] 05e's AC-regression matrix row count equals the fixture's total AC count (feature 05)
- [ ] Full-flow dry run produces master QA doc, security rollup, AC matrix, and severity-ordered readiness report (feature 06)
- [ ] Forced-failure dry run names the missing check and returns a non-GO verdict (feature 06)
- [ ] Verdict write-back updates fixture planning-doc status lines without manual editing; the real roadmap is untouched by dry runs (feature 06)
- [ ] 05i drafts at least one learnings/instruction proposal from real repo history (feature 06)
- [ ] After each feature: propagation regenerates all three harness outputs with no diff noise in unrelated assets (all features)
