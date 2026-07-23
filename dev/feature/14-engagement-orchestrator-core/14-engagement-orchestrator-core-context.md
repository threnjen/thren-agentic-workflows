# Context: 14-engagement-orchestrator-core

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] | New engagement orchestrator agent definition | Create |
| `source_of_truth/skills/engagement-workspace/SKILL.md` [PROPOSED - name TBD] | New skill: workspace root layout, per-pair/per-side folders, working-state file shape | Create |
| `source_of_truth/skills/engagement-configuration/SKILL.md` | Add per-pair value-story `mode` field (backward-compatible, documented default) | Modify |
| `tests/test_propagate_master_assets.py` | Marker-guard generated-file counts at lines 766–771 (`roots` list) | Modify (verify/bump) |
| `source_of_truth/agents/README.md` | Catalog entry — plan notes this may defer to feature 18 | Verify only |

### Read-Only Reference Files

| File | Why |
|------|-----|
| `source_of_truth/agents/engagement-prepare.agent.md` | House style for engagement agents: frontmatter (`name: Engagement - Prepare`, `description`, `tools`, `agents`), Security Boundary section, fail-fast style, explicit opt-out of `orchestrator-conventions` — must NOT be modified (AC2) |
| `source_of_truth/skills/engagement-preparation-runbook/SKILL.md` | Sibling engagement skill style reference |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase source (Key Deliverable 1, bundle 1) |
| `.github/learnings/cross-phase-decisions.md` | Phase-02 consolidation decisions and propagation caveats |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| No contradictions found — all referenced existing files verified on disk | — | none |
| `mode` field confirmed absent from `engagement-configuration/SKILL.md` (sections: Config Location Convention, Schema, Comparison pairs, Paths, Annotated example, Validation Rules, Not Validation Failures) | AC7 extension touches Schema, Annotated example, and Validation Rules sections; "Not Validation Failures" may need the missing-field default noted | Implementer updates those sections |
| Count-guard location confirmed: `tests/test_propagate_master_assets.py` `roots` list (claude/agents 28, claude/commands 19, opencode 43, codex 43). Prior bump `42 → 43` documented in comment at lines 760–764 — style to mirror. Plan cites lines 768-769; actual list spans ~766–771 | The new user-invocable orchestrator likely bumps claude/commands 19→20 and opencode/codex 43→44; claude/agents unchanged unless a new child subagent file is emitted. Recount from disk (`ls ports/<harness>/agents`), never increment from memory (per learnings) | Update counts after propagation |
| Repo learnings: propagation is not idempotent across renames — run until zero changes; `test_committed_tree_is_at_a_propagation_fixed_point` pins convergence | AC8 verification must run propagator twice | Already in plan; reinforced |
| Repo learnings: some tests assert exact needle strings against raw file text — Markdown line wraps can break needles; frontmatter `description` fields are pinned in PR-review tests (not engagement tests, but pattern exists) | Low risk here; no engagement-specific needle tests found | Accepted risk |
| Propagator resolves `agents:` rosters by display name — orchestrator roster must use `Engagement - Prepare` exactly | Wrong name silently breaks roster resolution | Implementer uses exact display name |
| No phase-scoped test directories exist in this repo (`tests/` is a flat regression suite over the two scripts) | No consolidated phase test file expected | none |

## Architectural Decisions

- **One slim orchestrator + subagents**: orchestrator holds only pair list and compact per-side/per-pair results; bulk child content is recorded as an on-disk pointer and discarded (context-blowout mitigation).
- **Workspace layout and working-state schema live in a skill**, not repeated in agent definitions — the contract features 15–18 plug into (defined-upstream cross-feature API rule).
- **Layout/state shapes are markdown conventions, not code schemas** — narrowest contract that lets feature 18's present/missing detection work mechanically.
- **No formal preflight tool**: entry checking is one paragraph of orchestrator instruction (AC3), per Phase-02 decision that runtime entry check replaces the dropped pilot run.
- **Working-state file is the sole observability surface** — no new logging.
- **Each boundary rule lives in exactly one place** (orchestrator or workspace skill) and is referenced from the other — no duplicated boundary text.

## Constraints

- `engagement-prepare.agent.md` must not be modified (AC2).
- Author only in `source_of_truth/`; never hand-edit `ports/` or `.github/`.
- AC9 brevity: state behavior, constraints, output contract once each — restated rules fail review.
- Client-code security boundary and never-pushed analysis-branch invariants (AC6) stated once and passed to every spawned subagent.
- No agent writes deliverables into a client repo; all manifest paths resolve inside the single workspace root (AC4).
- Never assume a pair count; repos are deduplicated across pairs (Phase-01 invariant).
- `mode` extension must be backward compatible: configs without it stay valid with a documented default; invalid value → validation error naming pair and field, in the skill's existing validation-rule style.

## Scope Boundaries

- Do not create any deliverable-producing subagent (features 15–18).
- No PDF assembly, branding, coverage quality gates, preflight tool, or report-versioning machinery.
- `source_of_truth/agents/README.md` catalog entry may defer to feature 18 — verify, do not over-deliver.
- Do not fix unrelated documentation count claims; only the marker-guard counts touched by this feature's propagation delta.

## Relationships to Sibling Plans

- **Upstream of 15–18**: all later features append subagents to this orchestrator's `agents:` roster (shared file — sequential) and write into the workspace layout defined here.
- **`mode` field (AC7)** is consumed by features 16 and 17.
- Wave 1, parallel safe, no dependencies.

## Suggested Implementation Order

Stage 1 (workspace + config contracts) before Stage 2 (orchestrator, which references the workspace skill), then Stage 3 (propagate & verify). Sequenced ahead of 15–18.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3 (stdlib-only scripts) + Markdown agent/skill assets; two-stage propagate/deploy pipeline |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 233 passed, 113 subtests passed — captured 2026-07-22 |
| Lint | Not configured |
| Format | Not configured |
| Propagation | `python3 scripts/propagate_master_assets.py --once` (run twice; second run must report zero changes) |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

- Phase 02 consolidation (2026-07-22): one slim orchestrator owning the per-pair loop; all work in subagents returning compact summaries + pointers; `engagement-prepare` spawned unchanged; `mode` field extends engagement-configuration; orchestrator keeps on-disk working-state file (inputs, statuses, pointers) as its run record.
- Entry condition is a runtime check that analysis branches and graphs exist for the sides in play — nothing more (pilot run removed).
- Propagation is not idempotent across reclassification/rename — run until every change counter is zero; convergence pinned by `test_committed_tree_is_at_a_propagation_fixed_point`.
- Marker-guard counts must be recounted from disk (`ls ports/<harness>/agents`), not incremented from memory; bump comment names the new agent (existing `42 -> 43` comment is the model).
- `agents:` roster references resolve by display name, not slug.
- Documentation count claims drift — guard by claim-shape, reconcile definitions before recounting.
