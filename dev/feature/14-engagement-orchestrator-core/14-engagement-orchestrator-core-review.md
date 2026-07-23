# Review Record: 14-engagement-orchestrator-core

## Summary

Reviewed the new `Engagement - Orchestrator` agent, the new `engagement-workspace` skill, the `mode` extension to `engagement-configuration`, and the count-guard/doc updates. All ACs trace to code and read correct. Re-verified executable evidence: propagation re-run reported zero changes (fixed point) and the suite matches baseline (233 passed, 113 subtests). One Medium issue found and fixed: skill/agent count claims left stale in `docs/CODEBASE_CONTEXT.md` and `docs/ARCHITECTURE.md` after this feature added the 28th skill.

## Verdict
Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Met | `source_of_truth/agents/engagement-orchestrator.agent.md` ("Context Budget", "Run Flow / 4") | No engagement-file-content handling anywhere; statuses + pointers only |
| AC2 | Met | same, "Run Flow / 2"; `agents: [Engagement - Prepare]` | Display name matches prepare frontmatter; `engagement-prepare.agent.md` unmodified in the diff |
| AC3 | Met | same, "Run Flow / 3. Entry Check" | Single paragraph, explicitly "no preflight tool", names side + missing item, other pairs continue |
| AC4 | Met | `source_of_truth/skills/engagement-workspace/SKILL.md` ("Root", "Layout") | Root outside client repos; manifest.md reserved; contract stated once |
| AC5 | Met | workspace skill ("Working-State File") + orchestrator ("Workspace and Working State") | Resume-from-state required; silent restart-from-zero forbidden |
| AC6 | Met | orchestrator, "Boundaries — Passed to Every Subagent" | Stated once, passed to every subagent; not duplicated elsewhere |
| AC7 | Met | `source_of_truth/skills/engagement-configuration/SKILL.md` schema row, example line, validation row | Backward-compat default documented; error matches existing table style |
| AC8 | Met (verified) | propagation + `tests/test_propagate_master_assets.py:765-786` | Re-executed in review: propagator reported zero changes; `uv run pytest tests/` = 233 passed, 113 subtests |
| AC9 | Met | all authored files | Boundary text only in orchestrator; layout only in workspace skill; no restated rules |

Manual QA (run against a prepared pair; unprepared-side failure report) remains **unverified** — deferred to the phase-level checklist per plan; static review cannot confirm runtime orchestration behavior.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Stale count claims after adding 28th skill: "27 skills" (CODEBASE_CONTEXT.md:16,32), "43 agent definitions / 27 skill directories" (ARCHITECTURE.md:36-37,125,128) | Medium | see left | AC8 (count-claim class) | Fixed |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `docs/CODEBASE_CONTEXT.md` | Skill count 27 → 28 (2 lines) | 1 |
| `docs/ARCHITECTURE.md` | Agent count 43 → 44, skill count 27 → 28 (4 lines) | 1 |

## Remaining Concerns
- Manual QA of the orchestrator run flow (resume, entry-check failure reporting) deferred to phase-level checklist — cannot be verified statically.
- `source_of_truth/agents/README.md` catalog entry deferred to feature 18 (documented gap; no test pins it).

## Test Coverage Assessment
- Covered: AC8 (executed: propagation fixed point + full suite); AC1–AC7, AC9 by code-review evidence per plan Section F.
- Missing: no automated guard on skill-count doc claims (agent counts are guarded by `test_retirement_reconciliation.py`; skill counts are not) — acceptable, noted only.

## Risk Summary
- `engagement-orchestrator.agent.md` is shared scope with features 15–18 (roster appends, stage insertion point) — merge coordination risk, mitigated by explicit in-file insertion markers.
- Doc count claims not test-guarded (skills) will drift again as features 15–18 add skills; the review-learnings summary-surface rule already covers this pattern.
- Ledger rows for the discovered/resolved issue appended to `eval/runs/phase-02-engagement-orchestrator/ledger-events.jsonl` and verified present.
