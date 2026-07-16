# Feature Context: 03-mechanical-evaluators

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/05g-artifact-sweeper.agent.md` | Cheap-tier sweep agent: debug statements, TODOs/FIXMEs, temp feature flags, dead code since baseline | Create |
| `.github/agents/05j-consistency-auditor.agent.md` | Convention-drift detector across subphases with canonical-form recommendations | Create |
| `.github/agents/05k-dependency-auditor.agent.md` | Cheap-tier dependency inventory: licenses, vulnerabilities, duplicate libraries | Create |
| Propagated outputs (`.claude/agents/`, `codex/agents/`, OpenCode equivalents) | Generated harness copies of the three agents | Generated (via propagation script) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` | Phase source: Deliverable 3, In Scope roster for 05g/05j/05k |
| `.github/agents/04a-feature-plan-expander.agent.md` (and `04b`–`04d`) | Lettered-subagent house style: frontmatter (`name`, `description`, `tools`, `user-invocable`), structure |
| `.github/skills/auditor-conventions/SKILL.md` | Severity norms referenced (never restated) by these evaluators |
| `.github/skills/refactor-safely/SKILL.md` | Documents `refactor_tool` usage (`mode="dead_code"` for unreferenced code) — the graph tool 05g invokes |
| `.github/skills/phase-final-review-conventions/SKILL.md` | Shared 05x constraints (report paths, severity, ≤10-line contract, partial-failure semantics) — **delivered by feature 01; does not exist yet** |
| `.github/skills/phase-final-review-report/SKILL.md` | Report templates the three evaluators must use — **delivered by feature 01; does not exist yet** |
| `.github/agents/05-phase-final-review.agent.md` | Orchestrator the dry-runs go through — **delivered by feature 02; does not exist yet** |
| `dev/phase-final-review/fixtures/` | Development fixture (Phase 01/02 artifact copies) for dry-runs — **delivered by feature 01; does not exist yet** |
| `scripts/propagate_master_assets.py` | Propagation pipeline (verify only — auto-discovery expected, no change) |
| `tests/test_propagate_master_assets.py` | Existing automated suite gating AC6 |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| Upstream contracts unimplemented: `phase-final-review-conventions`, `phase-final-review-report`, `worktree-baseline` skills, `05-phase-final-review.agent.md`, `05a-baseline-worktree.agent.md`, and the `dev/phase-final-review/fixtures/` fixture do not exist in the codebase yet — only plan files for features 01/02 exist | Expected for a Wave 3 feature, but the Implementer must verify features 01 and 02 have landed before starting; AC4/AC5 are unimplementable otherwise | Add a Stage-1 precondition task; orchestrator must sequence 01 → 02 → 03 |
| `refactor_tool` verified in this workspace's code-review-graph MCP server; `.github/skills/refactor-safely/SKILL.md` documents `mode="dead_code"` for unreferenced code. No diff-scoping parameter is documented — dead-code detection appears repo-wide, confirming the plan's Unverified Assumption | 05g instructions must filter dead-code results to phase-touched files (baseline→HEAD diff file list) rather than assume tool-level scoping | Author 05g with explicit result-filtering instructions; record in agent file per the plan's assumption note |
| No `model:` or tier frontmatter field exists in any current `.github/agents/*.agent.md` — house frontmatter is only `name`, `description`, `tools`, `user-invocable` | The "cheap-tier declaration in frontmatter/instructions" (AC1, AC3) has no established frontmatter key; the mechanism is `[PROPOSED - name TBD]` and should match whatever tier-declaration convention feature 02's orchestrator (its AC5) establishes | Implementer aligns the tier declaration with feature 02's landed convention; instructions-body declaration is the safe fallback |
| `.gitignore` line 5 is `dev/*` — everything under `dev/` is gitignore-matched (feature bundles are tracked only because tracked files override ignore rules) | AC5 dry-run report outputs under `dev/phase-final-review/` will be local-only unless explicitly force-added; also contradicts feature 01's plan claim that "dev/ contents are currently tracked" | Warning returned to Decomposer; for this feature, treat fixture-run reports as local QA evidence, not committed artifacts |
| Propagation baseline verified: `tests/test_propagate_master_assets.py` passes (19 passed, 2 subtests) with no changes; script auto-discovers `.github/agents/*.agent.md` — no script change expected, matching the plan | AC6 is achievable with zero script edits | None |
| Non-user-invocable agents are renamed with a `z-` prefix in Codex propagation output (per `.github/learnings/debugging-learnings.md`) | The three new agents will propagate as `z-artifact-sweeper`-style names in Codex; orchestrator references must use the source-of-truth names, and propagation verification should check the z-prefixed outputs | Include in Stage 4 verification task |
| `auditor-conventions` skill verified at `.github/skills/auditor-conventions/` | Plan's reference target for severity norms is real | None |

No other contradictions found.

## Architectural Decisions

- **Three thin agents, shared rules externalized**: each agent is mostly "scope + tool + report template" declarations; all shared constraints (report paths, severity levels, ≤10-line return contract, partial-failure semantics) live in `phase-final-review-conventions` and are referenced, never restated (plan §C, §D).
- **Severity taxonomy by reference**: severity norms come from `auditor-conventions` via the conventions skill — no per-agent severity definitions (plan §D duplication-risk mitigation).
- **No per-agent report formats**: all report structures come from `phase-final-review-report` templates (plan §D keep-it-clean rule).
- **Graceful degradation over silent skip**: when a dependency (graph server for 05g, baseline worktree for all three) is unavailable, the evaluator records not-run with a stated reason; never a silent pass (plan §B, AC4).
- **Empty findings are completed checks**: an empty phase diff or zero new dependencies is reported as a completed "nothing found" check, not a failure or a skip (plan §B).
- **House style**: lettered-subagent format per `04a`–`04d` (frontmatter with `name`, `description`, `tools`, `user-invocable: false` expected for orchestrator-spawned subagents).
- **Observability**: reports on disk are the record; no logging machinery — correct for markdown agent assets (plan §E).

## Constraints

- All three agents are **read-only against source code**; findings are report content only — no remediation (phase-level out-of-scope: auto-remediation is follow-up work through the normal pipeline).
- 05k reports vulnerabilities but must not fetch or install anything (plan §E security).
- Each agent returns a **≤10-line summary**; full detail goes to the conventions-defined report path under `dev/phase-final-review/PHASE_0N/`.
- Graph tool names must match the MCP server's actual tools — `refactor_tool` is verified; do not invent tool names.
- Cheap-tier assignment applies to 05g and 05k (mechanical sweeps); 05j is also grouped as mechanical in this feature per Deliverable 3.
- Propagation must produce no diff noise in unrelated assets (phase QA consideration).

## Scope Boundaries

- Do NOT modify `scripts/propagate_master_assets.py` (verify-only; auto-discovery expected to work).
- Do NOT modify `z-auditor-code`/`z-auditor-refactor` agents or the `auditor-conventions` skill — these evaluators are phase-diff-scoped, not whole-repo audits; reference, never duplicate or edit.
- Do NOT modify feature 01's skills (`phase-final-review-conventions`, `phase-final-review-report`, `worktree-baseline`) or feature 02's orchestrator — consume their contracts as landed.
- Do NOT set up or modify the code-review-graph server (plan non-goal).
- Do NOT touch `.github/hooks/` assets (phase-level out-of-scope).
- Do NOT implement any remediation behavior in the agents.
- Preserve the baseline-missing safety rule: if the 05a baseline worktree is unavailable, all three agents report not-run rather than evaluating against the wrong tree.

## Relationships to Sibling Plans

- **Depends on 01-review-foundation**: conventions skill, report templates, and the development fixture are this feature's contracts and dry-run substrate.
- **Depends on 02-final-review-orchestrator**: AC5 dry-runs each evaluator *through* the orchestrator; the evaluator invocation-prompt shape and not-run record format are published by feature 02.
- **Feeds 06-readiness-synthesis**: the three reports are inputs to `05l-readiness-synthesizer`; formats must stay strictly conformant to `phase-final-review-report` templates.
- **Sequential with all siblings**: every phase feature regenerates shared propagated output files — not parallel-safe.

## Suggested Implementation Order

1. Verify features 01 and 02 have landed (skills, orchestrator, fixture present) — hard precondition.
2. Stage 1: `05g-artifact-sweeper` (includes the graph-unavailable degradation path — the most involved of the three).
3. Stage 2: `05j-consistency-auditor`.
4. Stage 3: `05k-dependency-auditor`.
5. Stage 4: propagation run + verification, then fixture dry-runs of all three via the orchestrator.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12 (repo tooling) + Markdown agent/skill assets; propagation via `scripts/propagate_master_assets.py` |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` (pytest configured in `pyproject.toml [tool.pytest.ini_options]`, `testpaths = ["tests"]`) |
| Test Baseline | 382 passed, 2 failed — captured 2026-07-15. Both failures are pre-existing in `tests/hooks/test_hook_distribution_integration.py` (latency + harness-classification), unrelated to Phase 05. `tests/test_propagate_master_assets.py` passes clean (19 passed, 2 subtests) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/debugging-learnings.md`:

- **Codex z- prefix renaming**: the propagation script renames non-user-invocable agents to a `z-` prefix in `codex/agents/` (e.g., `04a-feature-plan-expander` → `z-feature-plan-expander`). The TOML `name` field and the symlink filename must match exactly, and orchestrators reference subagents by that propagated name. When verifying propagation of 05g/05j/05k, check the z-prefixed Codex outputs and confirm the orchestrator's references resolve.

From `.github/learnings/review-learnings.md`:

- **Schema fields implying a lifecycle need both write paths documented**: when a record format includes resolution/status fields (relevant to the not-run record format these evaluators emit), document the full write path, not just the initial write — otherwise downstream consumers (here, 05l synthesis) receive incomplete state.
- **Parity across mirrored copies**: when agent instructions change, every mirrored/propagated copy must carry the same behavior — propagate per feature, not once at the end.
