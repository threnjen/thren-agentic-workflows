# Feature Context: 04-delegating-evaluators

## Key Files

### Files Being Created

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/05c-qa-consolidator.agent.md` | Merges all subphase QA docs into one master QA doc (dedupe, drop superseded, re-order). Reads QA docs only, never code. | Create |
| `.github/agents/05d-security-rollup.agent.md` | Unions/dedupes subphase security findings; delegates live re-scan to `security-scan`; classifies fixed/persisting/reintroduced. | Create |
| `.github/agents/05h-test-health.agent.md` | Coverage delta, cross-subphase test redundancy, flake candidates; delegates analysis to `test-analyst`. | Create |
| Propagated outputs (`claude/agents/`, `codex/agents/`, `opencode/agents/`) | Generated copies of the three agents | Generated (by `scripts/propagate_master_assets.py`) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `.github/agents/security-scan.agent.md` | Delegate for 05d live re-scan (verified present) |
| `.github/agents/test-analyst.agent.md` | Delegate for 05h analysis (verified present; `user-invocable: false`) |
| `.github/agents/04-phase-execute.agent.md` + `04a`–`04d` lettered agents | House style for numbered orchestrator + lettered subagents, frontmatter shape |
| `.github/skills/implementation-pipeline-loop/` | Delegation/invocation phrasing pattern used by orchestrators |
| `.github/skills/auditor-conventions/SKILL.md` | Structural model for shared-convention skills |
| `.github/skills/phase-final-review-conventions/` (from feature 01) | Conventions all three agents must load: report locations, ≤10-line return contract, partial-failure semantics |
| `.github/skills/phase-final-review-report/` (from feature 01) | Master-QA template (05c), security-rollup template with classification vocabulary (05d) |
| `.github/agents/05-phase-final-review.agent.md` (from feature 02) | Orchestrator that dry-runs the evaluators; publishes invocation-prompt shape and not-run record format |
| `dev/phase-final-review/fixtures/` (from feature 01) | Development fixture for AC6 dry-runs (path was `[PROPOSED]` in feature 01's plan — confirm actual path before dry-run) |
| `docs/phases/PHASE_02/PHASE_02-security-scan.md` | Source of P2-SEC-01..03 NO-GO findings (verified: lines 53–55, three High findings) |
| `scripts/propagate_master_assets.py` | Verify only — auto-discovers agents via glob over `.github/agents` (constants at lines 28–44); no change expected |
| `tests/test_propagate_master_assets.py` | Existing automated test for AC7 |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `phase-final-review-conventions` and `phase-final-review-report` skills do NOT yet exist in `.github/skills/` | Expected — produced by feature 01 (declared dependency). Implementer must verify they exist before starting; if missing, feature 01 has not landed. | Add preflight task; no plan change |
| `05-phase-final-review.agent.md` orchestrator does NOT yet exist | Expected — produced by feature 02 (declared dependency). AC6 dry-runs require it. | Add preflight task; no plan change |
| `dev/phase-final-review/` fixture tree does NOT yet exist; feature 01 marks its exact layout `[PROPOSED - layout TBD]` | AC6 depends on fixture path/layout chosen during feature 01 implementation. | Implementer reads feature 01's implementation record for the resolved fixture path |
| P2-SEC-01..03 verified in `docs/phases/PHASE_02/PHASE_02-security-scan.md` (three High findings, lines 53–55) | AC6 spot-check target confirmed real. | None |
| Plan's Unverified Assumption CONFIRMED for `security-scan`: its constraints say "Scan all tracked, non-generated, security-relevant artifacts... not only files changed by the phase" — whole-repo default | 05d's delegation prompt must explicitly scope the re-scan (or accept whole-repo scan and match findings against the list); record the choice in implementation notes per the plan. | Implementer decision, recorded in implementation record |
| Plan's Unverified Assumption CONFIRMED for `test-analyst`: its deliverable contract is "three planning files in `dev/feature/[0N-task-name]/`" (a reduction plan), not a health report | 05h's delegation prompt must redirect output or adapt the returned analysis into the health report; adaptation lives in the 05h wrapper per non-goals. | Implementer decision, recorded in implementation record |
| `test-analyst` is `user-invocable: false`; propagation renames non-user-invocable agents with `z-` prefix for Codex, and Codex spawning matches TOML `name` exactly (see debugging learnings) | Delegation references in 05d/05h must use names that survive propagation; the three new 05x agents should also carry `user-invocable: false` (subagents of the 05 orchestrator). | Follow house style; verify propagated names |
| Propagation script auto-discovers via `*.agent.md` glob under `.github/agents`; a learning warns some agent files use plain `.md` and get missed | New files must use the `.agent.md` extension exactly. | Constraint below |
| No `dev/feature/phase-05-*-execution-manifest.md` found (manifests exist only for phase-01 and phase-02) | Phase 05 execution manifest appears missing from the decomposition output. | Warning returned to Decomposer |
| `.github/agents/README.md` exists as an agent inventory surface | Learning: adding agents requires updating every inventory surface carrying agent counts/lists. | Add task to check/update README inventory |
| No contradictions found in the plan's file references otherwise | — | None |

## Architectural Decisions

- **Thin merge-and-delegate agents**: all evaluation intelligence lives in the delegates (`security-scan`, `test-analyst`) and the report templates (`phase-final-review-report`). The 05x agents contain only delegation, merge, and classification rules (AC5 — a named phase success criterion).
- **Adaptation happens in the wrapper, not upstream**: if delegate return shapes don't fit, the 05x agent adapts them; `security-scan` and `test-analyst` are consumed as-is (non-goal).
- **Classification vocabulary defined once**: fixed/persisting/reintroduced lives in `phase-final-review-report`, not redefined per agent.
- **Conservative finding-matching**: fuzzy matches between re-scan and historical findings classify as persisting-unconfirmed and are flagged for synthesis; never marked fixed on a fuzzy match.
- **No logging**: reports on disk are the observability surface; correct decision per plan Section E.
- **Lettered-subagent house style** per `04a`–`04d`: YAML frontmatter with `name`, `description`, `tools`, `user-invocable: false`.

## Constraints

- All three agents must load `phase-final-review-conventions` and honor: report locations/naming under `dev/phase-final-review/PHASE_0N/`, the ≤10-line return-summary contract, and partial-failure semantics (delegate unavailable → not-run record with reason; verdict ceiling drops below GO) (AC4).
- 05c reads QA docs only — never code.
- 05d and 05h must contain NO scanning/analysis procedure of their own — only delegation, merge, and classification rules (AC5).
- New agent files must use the `.agent.md` extension so the propagation glob picks them up.
- Markdown assets only — no application code; Stage 0 test prerequisites explicitly not required.
- 05c uses the master-QA template and 05d the rollup template from `phase-final-review-report`.

## Scope Boundaries

- Do NOT modify `.github/agents/security-scan.agent.md` or `.github/agents/test-analyst.agent.md` — consumed as-is; adaptation belongs in the 05x wrappers.
- Do NOT fix security findings or tests — classification and reporting only.
- Do NOT author net-new QA checks — 05c consolidates existing QA docs; new QA for uncovered seams belongs to features 05 (seam analyzer) and 06 (synthesis).
- Do NOT modify `scripts/propagate_master_assets.py` — verify-only; auto-discovery means no change expected.
- Do NOT modify feature 01's skills or feature 02's orchestrator — they are upstream contracts.
- Preserve edge-case behaviors from plan Section B: missing QA doc → report the gap, don't fail; QA conflicts → keep later subphase's version and flag; no coverage tooling → coverage delta not-measurable but still deliver redundancy/flake analysis.

## Relationships to Sibling Plans

- **Depends on 01-review-foundation**: conventions skill, report skill (templates + classification vocabulary), and the development fixture including the Phase 02 NO-GO case.
- **Depends on 02-final-review-orchestrator**: `05-phase-final-review.agent.md` invocation-prompt shape and not-run record format; AC6 dry-runs go through it.
- **Feeds 06-readiness-synthesis**: 05d's classification output is a primary input to the go/no-go synthesis.
- **Sequential with all siblings**: shares propagated output files; not parallel-safe (Wave 4).

## Suggested Implementation Order

Stage order per plan: 05c (Stage 1) → 05d (Stage 2) → 05h (Stage 3) → propagation (Stage 4). Within the phase: after features 01 and 02 land; sibling 03 (mechanical evaluators) is also Wave-adjacent but this feature has no contract dependency on it.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill assets + Python 3.12 propagation tooling (repo `.venv`) |
| Test Runner | `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` |
| Test Baseline | 19 passed, 2 subtests passed — captured 2026-07-15 |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/debugging-learnings.md`:
- Codex spawns subagents by matching the TOML `name` field exactly; non-user-invocable agents are renamed with a `z-` prefix by propagation, and `~/.codex/agents/` symlinks must use the propagated filename. Delegation references in 05d/05h must use names that resolve after propagation.
- Codex `agents.max_depth` defaults to 1; the orchestrator → 05d → security-scan chain is depth 2 and requires `max_depth = 2` in `~/.codex/config.toml`. AC6 dry-run failures where "delegation seems to do nothing" are usually a missing symlink or depth limit, not invocation phrasing.

From `.github/learnings/review-learnings.md`:
- When adding a new agent, update every inventory surface carrying agent counts or summarized lists (e.g., `.github/agents/README.md`), not just the primary catalog.
- Porting/propagation globs scope on `*.agent.md`; agent files with a plain `.md` extension are silently missed. Use the `.agent.md` extension.
- When an orchestrator writes shared QA or final-review artifacts at phase scope, keep the checkpoint contract phase-scoped — do not promise per-feature checkpoint commits against consolidated outputs (applies to 05c's master QA doc).
