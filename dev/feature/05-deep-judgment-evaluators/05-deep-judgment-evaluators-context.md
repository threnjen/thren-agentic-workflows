# Feature Context: 05-deep-judgment-evaluators

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/05b-change-narrator.agent.md` | Whole-phase change narrative (baseline→HEAD), per-subphase attribution, churn hotspots | Create |
| `.github/agents/05e-ac-regression.agent.md` | Re-verifies every subphase AC against final codebase via hidden per-subphase verifiers; emits AC-regression matrix | Create |
| `.github/agents/05f-seam-analyzer.agent.md` | Integration-seam analysis between subphases via code-review-graph tools | Create |
| Propagated outputs (`claude/`, Codex/OpenCode equivalents) | Generated mirrors of the three agents | Generated (via propagation script) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `scripts/propagate_master_assets.py` | Propagation script; auto-discovers `.github/agents/*.md` via glob (line 260) — verified, no change expected |
| `tests/test_propagate_master_assets.py` | Existing propagation test suite (AC6 evidence) |
| `.github/agents/04a-feature-plan-expander.agent.md` (and `04b`–`04d`) | Lettered-subagent house style models (YAML frontmatter: `name`, `description`, `tools`, `user-invocable`) |
| `.github/skills/phase-final-review-conventions/SKILL.md` | Shared evaluator constraints (report locations, ≤10-line return contract, partial-failure semantics) — delivered by feature 01, **does not exist yet** |
| `.github/skills/phase-final-review-report/SKILL.md` | Output templates incl. AC-regression matrix and attribution vocabulary — delivered by feature 01, **does not exist yet** |
| `.github/skills/worktree-baseline/SKILL.md` | Baseline worktree procedure — delivered by feature 01, **does not exist yet** |
| `.github/agents/05a-baseline-worktree.agent.md` | Baseline worktree provider consumed by 05b — delivered by feature 01, **does not exist yet** |
| `.github/agents/05-phase-final-review.agent.md` | Orchestrator whose invocation shape and not-run record format the evaluators must honor — delivered by feature 02, **does not exist yet** |
| `dev/phase-final-review/fixtures/` `[PROPOSED - exact path TBD in feature 01]` | Development fixture (Phase 01/02 artifact copies in pseudo-subphase layout) used for dry-runs (AC5) |
| `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` | Source phase document (Deliverable 5; roster entries 05b, 05e, 05f) |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| None of the upstream artifacts exist yet: `phase-final-review-conventions`, `phase-final-review-report`, `worktree-baseline` skills, `05a-baseline-worktree.agent.md`, `05-phase-final-review.agent.md`, and the fixture directory (`dev/phase-final-review/` does not exist) | Expected — this is a wave-5 feature depending on features 01 and 02, which are not yet implemented | Implementer must verify all upstream artifacts exist before starting; read the actual contracts from disk, not from this plan's summary of them |
| Fixture root is `[PROPOSED - exact path TBD]` in feature 01's plan; this plan's AC5 references fixture dry-runs by role only | Final fixture path must be read from feature 01's implementation record | Add task: resolve fixture path from feature 01 outputs |
| `get_impact_radius` verified as a documented code-review-graph MCP tool (project CLAUDE.md tool table); `get_bridge_nodes` appears only in the Phase document and is copied exactly from it — it is not in the project CLAUDE.md tool table | If the tool name differs on the live server, 05f's graceful-degradation path must still produce a not-run record rather than error | Implementer verifies `get_bridge_nodes` against the live MCP server during Stage 3; degradation behavior covers the miss case |
| Propagation script auto-discovery confirmed: `GITHUB_AGENTS_DIR.glob("*.md")` at `scripts/propagate_master_assets.py:260` | Validates plan's "no change expected" claim for AC6 | None |
| Test baseline has 2 pre-existing failures in `tests/hooks/test_hook_distribution_integration.py` (unrelated to this feature); `tests/test_propagate_master_assets.py` passes | AC6 success must be measured against the propagation suite, not the full-suite green | Recorded in Environment State; do not attempt to fix the hook-latency failures in this feature |
| Learnings warn that adding new agents requires updating inventory surfaces (agent counts, README tables, Mermaid diagrams, CODEBASE_CONTEXT summaries); the plan does not list any doc-inventory tasks | Sibling 04x lettered subagents appear in `.github/agents/README.md` diagrams/tables; three new agent files may leave those surfaces stale | Warning for Decomposer/Implementer: check whether `.github/agents/README.md` or `docs/CODEBASE_CONTEXT.md` enumerate 05x agents by the time this feature lands; if features 01/02 established an inventory pattern, follow it |

## Architectural Decisions

- **Three agents, judgment procedure + template reference each**: chunking and hidden-verifier-spawning rules are stated as constraints inside the agent instructions, not elaborate protocols (plan Section D).
- **Verifier contract = evaluator contract**: 05e's hidden per-subphase verifiers report to disk and return ≤10 lines, identical to top-level evaluators — no second contract to maintain.
- **Attribution vocabulary lives in the report skill**: terms like `regressed-by` and `unknown` are defined once in `phase-final-review-report`'s AC-regression matrix template, not per-agent.
- **05b chunks by directory/subphase**: never loads the full phase diff into one context; per-directory reader spawning is the pressure valve for large diffs.
- **05f degrades, never blocks**: when the code-review-graph server is unavailable, 05f produces a not-run record with reason (partial-failure semantics), and the run continues.
- **Model tier**: all three are deep-judgment evaluators and declare the top model tier (per the phase's model-tier policy and the orchestrator's AC5).
- **No new logging**: reports on disk are the observability surface; agent markdown has no runtime logging surface (plan Section E — correct decision).

## Constraints

- ≤10-line return-summary contract for every agent and every hidden verifier; full detail on disk under `dev/phase-final-review/PHASE_0N/`.
- Report locations, naming, severity levels, and partial-failure semantics come from `phase-final-review-conventions` — the agents load that skill rather than restating its rules.
- Lettered-subagent house style per `04a`–`04d`: YAML frontmatter (`name`, `description`, `tools`, `user-invocable`), constraints section, workflow steps, return-value contract.
- 05e must cover EVERY AC from every subphase summary — no silent omissions; untestable-by-inspection ACs are marked not-verifiable with reason, and the not-verifiable count surfaces in the matrix summary.
- 05b uses the baseline worktree from `05a-baseline-worktree`; if the baseline is unavailable, 05b reports not-run while 05e/05f proceed (final-tree evaluation) and state that baseline comparison was skipped.
- Graph tool names `get_impact_radius` and `get_bridge_nodes` are copied exactly from the Phase document — do not rename.
- Read-only posture: worktree etiquette per `worktree-baseline`; no repo mutation by any evaluator.

## Scope Boundaries

- Reporting only — no fixing of regressions or seams found.
- 05e does not re-run automated test suites; it verifies ACs by inspection and existing evidence (live test execution belongs to the target repo's pipeline and 05h's delegate).
- No changes to the code-review-graph server.
- No changes to `scripts/propagate_master_assets.py` (auto-discovery covers new agents).
- Do not modify the fixture: if a fixture AC is phase-meta rather than code-verifiable, 05e marks it not-verifiable — the fixture is not altered (plan's Unverified Assumptions).
- Do not touch the pre-existing failing hook-distribution tests.
- Do not modify feature 01/02 deliverables (skills, 05a, orchestrator); consume their contracts as-is and report mismatches upward.

## Relationships to Sibling Plans

- **Depends on 01-review-foundation** (wave 1): conventions skill, report skill (matrix template + attribution vocabulary), `worktree-baseline`, `05a-baseline-worktree`, development fixture.
- **Depends on 02-final-review-orchestrator** (wave 2): evaluator invocation prompt shape, not-run record format, model-tier declarations; all dry-runs (AC5) route through this orchestrator.
- **Feeds 06-readiness-synthesis**: 05e's AC-regression matrix and 05f's seam report are primary synthesis inputs; 05b's narrative supplies the attribution backbone.
- **Sequential with siblings 03/04**: shares propagated output files with all sibling features (wave 5, not parallel-safe).

## Suggested Implementation Order

Within this feature: Stage 1 (05b) → Stage 2 (05e) → Stage 3 (05f) → Stage 4 (propagation), per the plan. Across the phase: after features 01 and 02 (and, per the manifest waves, after 03 and 04); before feature 06.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill assets + Python 3.12 tooling (uv-managed; `pyproject.toml` + `uv.lock`) |
| Test Runner | `uv run pytest tests/ -q` (propagation-only: `uv run pytest tests/test_propagate_master_assets.py -q`) |
| Test Baseline | 382 passed, 2 failed (pre-existing, `tests/hooks/test_hook_distribution_integration.py` latency/guide tests, unrelated) — captured 2026-07-15 |
| Lint | Not configured (no ruff/flake8/black in `pyproject.toml`) |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/review-learnings.md`:

- "When adding a new user-facing agent, update every inventory surface that carries agent counts or summarized agent lists, not just the primary catalog tables." Stale overview bullets and Mermaid diagrams can contradict the actual agent inventory. Surfaces: top-level README intros, Mermaid labels, CODEBASE_CONTEXT count summaries.
- "When a porting guide scopes an agent source directory using a filename glob (e.g., `*.agent.md`), verify whether the directory contains agent definitions that do not match that extension." Use the `.agent.md` extension for all three new agents so glob-scoped propagation and porting guides pick them up.
- "Artifact propagators must validate resolved source assets and resolved destination directories against their declared roots" — context for why AC6 relies on the existing propagation suite rather than manual copying.

From `.github/learnings/debugging-learnings.md` and `project-learnings.md`: None applicable.
