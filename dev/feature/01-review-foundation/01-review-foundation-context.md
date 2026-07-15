# Feature Context: 01-review-foundation

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `.github/skills/phase-final-review-conventions/SKILL.md` | Shared conventions for all Phase Final Review agents (report locations, severity, return contract, partial-failure semantics) | Create |
| `.github/skills/phase-final-review-report/SKILL.md` | Output templates: master QA doc, security rollup, AC-regression matrix, go/no-go readiness report | Create |
| `.github/skills/worktree-baseline/SKILL.md` | Reusable "check out commit X in a git worktree" procedure with cleanup and read-only etiquette | Create |
| `.github/agents/05a-baseline-worktree.agent.md` | Thin agent that loads `worktree-baseline` and returns the worktree path + ≤10-line summary | Create |
| `dev/phase-final-review/fixtures/` `[PROPOSED - exact layout TBD]` | Development fixture: Phase 01/02 artifact copies in pseudo-subphase layout, plus provenance README | Create |
| `.gitignore` | Requires a negation rule so the fixture is committable (see Discovery Delta) | Modify |
| `.claude/skills/`, `.claude/agents/`, Codex/OpenCode outputs | Propagated copies of the three skills and 05a agent | Generated (via propagation) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` | Source phase document (Deliverable 1) |
| `docs/phases/PHASE_01/` (5 artifacts) | Fixture source: SUMMARY, QA, QA_COVERAGE_MAP, qa-analysis, security-scan |
| `docs/phases/PHASE_02/` (6 artifacts) | Fixture source, including the genuine NO-GO security scan; also contains `PHASE_02_DISCOVERY_CONTEXT.md` |
| `.github/skills/auditor-conventions/SKILL.md` | House-style model for the conventions skill (frontmatter: `name` + `description` with "Use when:" clause) |
| `.github/skills/implementation-record/SKILL.md` | House-style model for template skills (AC2) |
| `.github/agents/04a-feature-plan-expander.agent.md` | House-style model for the 05a agent (frontmatter: `name`, `description`, `tools`, `user-invocable`) |
| `.github/agents/README.md` | Agent authoring conventions |
| `scripts/propagate_master_assets.py` | Propagation script — verify only, no change expected |
| `tests/test_propagate_master_assets.py` | Existing automated verification for AC6 |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| **Gitignore contradiction (WARNING):** `.gitignore` line 5 is `dev/*`, which ignores all new files under `dev/`. The plan's Section B assumption "`dev/` contents are currently tracked" is wrong — existing `dev/feature/` manifests are tracked only because they were added before/despite the ignore rule (`git check-ignore` confirms `dev/phase-final-review/fixtures/*` would be ignored). | The fixture (AC5) is not committable at the proposed path without action. PHASE_05_SUMMARY.md anticipates this: "or equivalent gitignore-reviewed path chosen during decomposition." | Add a `.gitignore` negation (e.g., `!dev/phase-final-review/`) as part of Stage 3, or `git add -f` the fixture tree. Implementer must choose one, verify `git status` shows the fixture, and record the decision in implementation notes. Flagged to Decomposer. |
| Propagation auto-discovery verified: `load_source_agents()` globs `.github/agents/*.md` and requires `name` + `description` frontmatter (~line 260); skill propagation iterates `.github/skills/*/SKILL.md` directories (~line 1204). | Plan assumption confirmed — no script change needed as long as the new agent has `name` + `description` frontmatter and each skill directory contains `SKILL.md`. | None; author assets to those requirements. |
| `tests/test_propagate_master_assets.py` currently passes (19 passed, 2 subtests). Full suite has 2 pre-existing failures in `tests/hooks/test_hook_distribution_integration.py` (AC7/AC9 hook-distribution tests), unrelated to this feature. | AC6 verification must not be blamed for the pre-existing hook failures. | Baseline recorded below; compare against it after propagation. |
| PHASE_05_SUMMARY.md (line 24) lists "implementation records" among fixture contents, but no implementation records exist under `docs/phases/PHASE_01/` or `PHASE_02/` (prior-phase `dev/feature/` bundles were not retained). Plan AC5 correctly omits them. | Fixture can only contain the artifact types that actually exist: summary, QA, coverage map, qa-analysis, security scan. | Accepted; document in fixture README. |
| `docs/phases/PHASE_02/` contains an extra artifact type not listed in AC5: `PHASE_02_DISCOVERY_CONTEXT.md`. | Ambiguity in fixture inventory ("every source artifact type"). | Include it in the fixture for completeness (it is a real pipeline artifact) or explicitly note exclusion in the fixture README; implementer decides and records. |
| No `05*`-numbered agents exist yet; `05a-baseline-worktree.agent.md` name is copied exactly from the phase document — no collision. Skill names `phase-final-review-conventions`, `phase-final-review-report`, `worktree-baseline` do not exist in `.github/skills/` — no collision. | Names are safe as-is. | None. |
| `eval-grader.agent.md` exists in `.github/agents/` — the plan's reusability target for `worktree-baseline` (AC3) is real. | Confirms AC3's "reusable outside Phase Final Review" framing. | Write the skill without Phase-Final-Review-specific assumptions. |

## Architectural Decisions

- **Skills-first contract publication**: this feature publishes the contracts (report naming, four templates, worktree procedure, fixture layout) that features 02–06 are authored against; that is why it is Wave 1 and sequential-first.
- **Reference, don't restate**: `phase-final-review-conventions` keeps only phase-final-review-specific rules and references `auditor-conventions` for shared audit norms, avoiding duplication.
- **Copied fixture, not live pointers**: Phase 01/02 are sibling top-level phases, not subphases, so the fixture copies their artifacts into the pseudo-subphase layout (`PHASE_0Xa/`, `PHASE_0Xb/` per the phase document) rather than pointing the orchestrator at live directories.
- **No code**: simplest design is three skills + one thin agent + copied files. No scripts, no automation added.
- **Partial-failure semantics live in the conventions skill**: run completes when an evaluator fails; readiness report enumerates not-run checks; verdict may not be GO while any check is missing. Features 02 and 06 consume this.

## Constraints

- Do NOT modify `scripts/propagate_master_assets.py` — auto-discovery handles new assets; only a discovery-config fix is permitted if a naming edge case surfaces.
- Agent frontmatter must include `name` and `description` or propagation silently skips it.
- Each skill must live in its own directory containing `SKILL.md`, matching `.github/skills/auditor-conventions/`.
- Skill/agent prose must contain no change-tracking language; templates use placeholder tokens consistent with existing template skills (`implementation-record`).
- The conventions skill must define "missing artifact" precisely enough for feature 02's preflight to fail loudly on it.
- Report templates must include an explicit "checks not run" section.
- The `worktree-baseline` procedure must specify behavior for: baseline commit not present locally (clear failure message), pre-existing worktree at target path (deterministic reuse-or-recreate, documented), and cleanup on completion.
- Fixture must include Phase 02's genuine NO-GO security case, unmodified in substance.

## Scope Boundaries

- No orchestrator or evaluator agents beyond `05a` (those are features 02–06).
- No "combine sibling phases" mode — the fixture is the only mechanism for Phase 01/02 material.
- No changes to `prod-code-review`, `auditor-conventions`, or any existing skill.
- No modification of live `docs/phases/PHASE_01/` / `PHASE_02/` directories — fixture files are copies.
- No new logging or observability — all deliverables are markdown assets.
- Do not touch the two pre-existing failing hook-distribution tests; they are out of scope.

## Relationships to Sibling Plans

- **All of features 02–06 depend on this feature.** They consume: report locations/naming (conventions skill), the four report templates (report skill), the worktree-checkout contract (features 02 and 05), and the fixture layout (every feature's dry-run acceptance).
- The whole phase runs strictly sequentially because every feature regenerates shared propagated output files.

## Suggested Implementation Order

1. This feature is Wave 1 and must land first; no upstream dependencies.
2. Internally, follow the plan's stages in order: skills → agent → fixture → propagation, so the agent can reference a finished `worktree-baseline` skill and propagation verifies everything at once.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 (repo tooling); primary deliverables are markdown assets |
| Test Runner | `.venv/bin/pytest tests/ -q` (pytest ≥9, configured in `pyproject.toml [tool.pytest.ini_options]`, `testpaths=["tests"]`) |
| Test Baseline | 382 passed, 2 failed (pre-existing, `tests/hooks/test_hook_distribution_integration.py` AC7/AC9), 2 subtests passed — captured 2026-07-15 |
| Targeted AC6 Suite | `.venv/bin/pytest tests/test_propagate_master_assets.py -q` — 19 passed, 2 subtests passed (baseline green) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/review-learnings.md`:

> **Pattern:** Artifact propagators must validate resolved source assets and resolved destination directories against their declared roots before reading or writing; replacing only a symlinked leaf file is not sufficient.
> **Impact:** A symlinked parent directory can redirect generated files outside the consumer root... breaks isolation and can overwrite or disclose unrelated files.

Relevance: when verifying AC6 propagation output, confirm new assets land inside the declared destination roots (`.claude/skills/`, `.claude/agents/`, Codex/OpenCode equivalents) and nothing is written elsewhere.

No other entries in `.github/learnings/` match this feature's domain (markdown skill/agent authoring, fixtures, git worktrees).
