# Implementation Record: 14-engagement-orchestrator-core

## Summary

Created the engagement orchestrator agent (`Engagement - Orchestrator`, file `engagement-orchestrator.agent.md`) and the `engagement-workspace` skill (workspace root layout + working-state file shape), and added the backward-compatible per-pair `mode` field to `engagement-configuration`. Propagated to a fixed point, reconciled the marker-guard counts and the two doc count-claim guards touched by the new agent file, and restored the suite to the exact baseline (233 passed, 113 subtests).

Final chosen names (resolving the plan's `[PROPOSED - name TBD]` placeholders):
- Agent: `source_of_truth/agents/engagement-orchestrator.agent.md`, display name `Engagement - Orchestrator`
- Skill: `source_of_truth/skills/engagement-workspace/SKILL.md`, name `engagement-workspace`
- Working-state file: `engagement-state.md` at the workspace root
- `mode` values: `modernization` (default when absent) | `modernized-and-improved`

## Sibling Features

- 15–18 (waves 2–5) all append subagents to this orchestrator's `agents:` roster (marked in-file: "Later engagement features append their subagents…") and write into the workspace layout defined here. The per-pair loop carries an explicit stage-insertion point.
- `mode` (AC7) is consumed by features 16 and 17.
- `manifest.md` path at the workspace root is reserved for feature 18.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | code-review | Orchestrator holds only pair list + statuses/pointers; never reads engagement source | Complete | `source_of_truth/agents/engagement-orchestrator.agent.md` | "Context Budget" section | PENDING | PENDING |
| AC2 | AC2 | code-review | Spawns `Engagement - Prepare` unchanged; prepare file untouched | Complete | `source_of_truth/agents/engagement-orchestrator.agent.md` | "Run Flow / 2. Prepare"; `git status` shows no change to `engagement-prepare.agent.md` | PENDING | PENDING |
| AC3 | AC3 | code-review | Entry check is one instruction paragraph, no tool | Complete | `source_of_truth/agents/engagement-orchestrator.agent.md` | "Run Flow / 3. Entry Check" | PENDING | PENDING |
| AC4 | AC4 | code-review | Single workspace root outside client repos; all outputs inside; contract for 15–18 | Complete | `source_of_truth/skills/engagement-workspace/SKILL.md` | "Root" and "Layout" sections | PENDING | PENDING |
| AC5 | AC5 | code-review | Working-state file shape + resume-from-state behavior | Complete | workspace skill ("Working-State File"); orchestrator ("Workspace and Working State") | both files | PENDING | PENDING |
| AC6 | AC6 | code-review | Boundaries + compact-handoff stated once, passed to every subagent | Complete | `source_of_truth/agents/engagement-orchestrator.agent.md` | "Boundaries — Passed to Every Subagent" | PENDING | PENDING |
| AC7 | AC7 | code-review + sync tests | `mode` field, documented default, validation-rule-style error | Complete | `source_of_truth/skills/engagement-configuration/SKILL.md` | Schema table, annotated example, Validation Rules row | PENDING | PENDING |
| AC8 | AC8 | `uv run pytest tests/` | Fixed-point propagation; count-guard bump; no new failures vs baseline | Complete | `tests/test_propagate_master_assets.py`, `README.md`, `docs/CODEBASE_CONTEXT.md` | second propagation run reports zero changes; suite 233/113 | PENDING | PENDING |
| AC9 | AC9 | code-review | Brevity — behavior/constraints/output contract once each | Complete | all authored files | boundary text lives only in the orchestrator; layout only in workspace skill | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Slim orchestrator, per-pair loop, subagent delegation | Complete | engagement-orchestrator.agent.md | Bulk child content → record path, discard |
| AC2 | Spawns engagement-prepare unchanged | Complete | engagement-orchestrator.agent.md | engagement-prepare.agent.md not modified |
| AC3 | Runtime entry-check paragraph | Complete | engagement-orchestrator.agent.md | Per-pair block, other pairs continue |
| AC4 | Workspace layout contract | Complete | skills/engagement-workspace/SKILL.md | Root outside client repos; manifest paths resolve inside root |
| AC5 | Working-state file + resume | Complete | both new files | Silent restart-from-zero forbidden explicitly |
| AC6 | Boundaries stated once, passed to subagents | Complete | engagement-orchestrator.agent.md | Client-code, analysis-branch, compact-handoff |
| AC7 | `mode` field, backward compatible | Complete | skills/engagement-configuration/SKILL.md | Default `modernization`; error names pair + field |
| AC8 | Propagation fixed point, suite clean | Complete | tests + docs count claims | 233 passed, 113 subtests — matches baseline |
| AC9 | Brevity | Complete | all authored files | No duplicated boundary/layout text |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/agents/engagement-orchestrator.agent.md` | Create | Orchestrator definition: config consumption, prepare spawn, entry check, per-pair loop, boundaries, working-state maintenance | AC1–AC3, AC5, AC6 |
| `source_of_truth/skills/engagement-workspace/SKILL.md` | Create | Workspace root, per-pair/per-side layout, working-state file shape | AC4, AC5 |
| `source_of_truth/skills/engagement-configuration/SKILL.md` | Modify | `mode` schema row, annotated-example line, validation-rule row | AC7 |
| `README.md` | Modify | Source-agent count claim 43 → 44 | AC8 — count-claim guard is part of this feature's propagation delta |
| `docs/CODEBASE_CONTEXT.md` | Modify | Count claims 43 → 44 (and 41 → 42 `*.agent.md`, 19 → 20 user-invocable) | AC8 — same guard |
| `ports/`, `.github/` | Generated | Regenerated by propagator (twice; second run zero changes) | AC8 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Marker-guard counts recounted from disk: claude/agents 28→29, claude/commands 19→20, opencode 43→44, codex 43→44, with comment naming the new agent in the existing style | AC8 |

## Test Results
- **Baseline**: 233 passed, 113 subtests passed, 0 failed (2026-07-22, matches context record)
- **Final**: 233 passed, 113 subtests passed, 0 failed
- **New tests added**: 0 (markdown-asset feature; existing propagation suite is the guard, per plan Section F)
- **Regressions**: None

## Deviations from Plan

- Root `README.md` and `docs/CODEBASE_CONTEXT.md` count claims were updated — the context said "do not fix unrelated documentation count claims," but these claims are guarded by `tests/test_retirement_reconciliation.py` count-shape tests that fail when the new agent lands, so they are part of this feature's propagation delta, not unrelated drift.
- claude/agents count bumped 28→29 (context predicted "unchanged unless a new child subagent file is emitted"): declaring `Engagement - Prepare` as a child emitted its first spawnable subagent file — recounted from disk per learnings.

## Gaps

- `source_of_truth/agents/README.md` catalog entry deferred to feature 18 per plan/context ("verify, do not over-deliver"); no test pins the catalog, suite is green without it.
- Manual QA (run against a prepared pair; unprepared-side failure report) deferred to the phase-level checklist per plan.

## Reviewer Focus Areas

- `engagement-orchestrator.agent.md` — verify no engagement-file-content handling anywhere (top evidence check 2) and the exact roster display name `Engagement - Prepare`.
- `engagement-configuration/SKILL.md` `mode` rows — backward compatibility wording and error-message style match the existing validation table.
- `tests/test_propagate_master_assets.py:765-777` — count bump comment and values (recounted from disk).
- `engagement-workspace/SKILL.md` — confirm feature 18's manifest paths can all resolve inside the root as stated.
