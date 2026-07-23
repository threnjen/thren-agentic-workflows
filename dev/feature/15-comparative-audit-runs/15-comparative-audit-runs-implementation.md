# Implementation Record: 15-comparative-audit-runs

## Summary

Added a "Comparative Scans" section to `auditor-conventions` (stable categories = each producing agent's own vocabulary; existing 4-level severity scale referenced, not restated; security-only per-finding matching on Category + file path with line numbers excluded and scan-local IDs never compared; category × severity rollups elsewhere; unmatched findings classified new/resolved, never dropped). Created one hidden runner agent, `Engagement - Audit Runner` (`engagement-audit-runner.agent.md`), parameterized by pair/side/dimension set, spawning the four existing audit agents unchanged and retaining raw reports at `<workspace-root>/pairs/<pair>/<side>/audits/<dimension>/`. Wired a "Comparative Audit Runs" stage and roster entry into `Engagement - Orchestrator`. Propagated to a fixed point, recounted guards from disk, suite restored to exact baseline.

Resolved names:
- Runner: `source_of_truth/agents/engagement-audit-runner.agent.md`, display name `Engagement - Audit Runner`, hidden (`z-engagement-audit-runner` when deployed).
- Runner shape decision: **one parameterized runner** (fewest new definitions; compact orchestrator handoff), per plan §B.
- Stable category names: derived, not invented — security = Security Scan's 10 scope categories; code = Auditor - Code's 14; infra = Auditor - Infra's 14; dependencies = dependency inventory + duplicate-library checks.
- Report location key: `(pair, side, dimension)` directory; auditors keep natural `-report.md` / `-summary.md` filenames.

## Sibling Features

- Consumes 14's orchestrator (`engagement-orchestrator.agent.md`), `engagement-workspace` layout, and subagent boundary contract. Stage inserted at the per-pair loop's insertion point; placeholder retained for 16–18.
- Upstream of 16: retained per-side reports, Comparative Scans convention (categories, severity reference, security matching key, new/resolved rules), and the asymmetric-evidence flag in runner summary + working-state entry are 16's inputs.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | code-review | Four dimensions run per side via existing agents unchanged | Complete | `source_of_truth/agents/engagement-audit-runner.agent.md` | "Dimensions" section; `git status` clean on the four reused agent files | PENDING | PENDING |
| AC2 | AC2 | code-review | Raw `-report.md`/`-summary.md` retained per dimension/side/pair, internal-only | Complete | runner agent | "Report Retention" section | PENDING | PENDING |
| AC3 | AC3 | code-review + skill sync tests | Comparability section extends skill in place; severity referenced not restated; security-only per-finding IDs; new/resolved | Complete | `source_of_truth/skills/auditor-conventions/SKILL.md` | "Comparative Scans" section | PENDING | PENDING |
| AC4 | AC4 | code-review | One-side re-run overwrites in place, other side untouched | Complete | runner agent; orchestrator | "Re-Runs and Deduplication"; orchestrator stage paragraph | PENDING | PENDING |
| AC5 | AC5 | code-review | No new grants; dependency evidence offline or NOT RUN; graph unavailable = NOT RUN; asymmetric evidence never a delta | Complete | runner agent; orchestrator | "NOT RUN — Never a Pass"; orchestrator asymmetric-evidence paragraph; four reused agent files unmodified | PENDING | PENDING |
| AC6 | AC6 | code-review | Roster entry + per-pair loop stage; compact summaries + pointers; boundaries pass through | Complete | `source_of_truth/agents/engagement-orchestrator.agent.md` | `agents:` roster; "Stage: Comparative Audit Runs" | PENDING | PENDING |
| AC7 | AC7 | `uv run pytest tests/` | source_of_truth only; fixed point; count guards; no new failures | Complete | `tests/test_propagate_master_assets.py`, `README.md`, `docs/CODEBASE_CONTEXT.md` | second propagation run zero changes; suite 233/113 | PENDING | PENDING |
| AC8 | AC8 | code-review | Brevity — each rule once; no restating auditor definitions | Complete | all authored files | severity scale cited not restated; category lists referenced by name only | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Four dimensions, both sides, agents unchanged | Complete | engagement-audit-runner.agent.md | Roster: Security Scan, Auditor - Code, 05e Dependency Auditor, Auditor - Infra |
| AC2 | Raw reports retained per dimension/side/pair | Complete | engagement-audit-runner.agent.md | `pairs/<pair>/<side>/audits/<dimension>/`, natural filenames |
| AC3 | Comparability convention in auditor-conventions | Complete | skills/auditor-conventions/SKILL.md | Extension in place; severity scale referenced only |
| AC4 | One-side re-run, overwrite in place | Complete | runner + orchestrator | Git history is the version record; other side never touched |
| AC5 | Capability boundaries; NOT RUN never a pass; asymmetric evidence | Complete | runner + orchestrator | Reused auditor grant lists unchanged (git clean) |
| AC6 | Orchestrator wiring | Complete | engagement-orchestrator.agent.md | Stage before retained insertion placeholder |
| AC7 | Propagation fixed point, suite clean | Complete | tests + doc count claims | 233 passed, 113 subtests — matches baseline |
| AC8 | Brevity | Complete | all authored files | Each rule stated once |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Modify | Appended "Comparative Scans" section | AC3, AC8 |
| `source_of_truth/agents/engagement-audit-runner.agent.md` | Create | Hidden runner agent: dimensions table, report retention, NOT RUN semantics, re-run/dedup, compact return | AC1, AC2, AC4, AC5 |
| `source_of_truth/agents/engagement-orchestrator.agent.md` | Modify | Roster entry + "Stage: Comparative Audit Runs" in per-pair loop | AC6 |
| `README.md` | Modify | Source-agent count claim 44 → 45 | AC7 — count-claim guard (`test_retirement_reconciliation.py`) |
| `docs/CODEBASE_CONTEXT.md` | Modify | 44 → 45 definitions, 42 → 43 `*.agent.md`, 24 → 25 hidden subagents | AC7 — same guard |
| `ports/`, `.github/` | Generated | Regenerated by propagator (fixed point; second run zero changes) | AC7 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Marker-guard counts recounted from disk: claude/agents 29→31, opencode 44→45, codex 44→45, claude/commands unchanged (20); comment in existing style | AC7 |

## Test Results
- **Baseline**: 233 passed, 113 subtests passed, 0 failed (matches context record)
- **Final**: 233 passed, 113 subtests passed, 0 failed
- **New tests added**: 0 (markdown-asset feature; existing propagation suite is the guard per plan §F)
- **Regressions**: None

## Deviations from Plan

- claude/agents bumped 29→31, not +1: declaring `Security Scan` as a runner child emitted its first spawnable subagent file (`ports/claude/agents/security-scan.md`) alongside `z-engagement-audit-runner.md`. Recounted from disk per learnings.
- `README.md`/`docs/CODEBASE_CONTEXT.md` count claims updated — guarded by `tests/test_retirement_reconciliation.py`, so part of this feature's propagation delta (same rationale as feature 14).

## Gaps

- Manual QA (per-pair per-side reports on disk; one-side re-run refreshes only that side) deferred to phase-level checklist per plan §F.
- `source_of_truth/agents/README.md` catalog entry deferred to feature 18, matching 14's precedent; no test pins the catalog.

## Reviewer Focus Areas

- `auditor-conventions/SKILL.md` "Comparative Scans" — verify category names map to the four auditors' existing vocabularies (evidence check 1) and severity is referenced, not restated.
- `engagement-audit-runner.agent.md` — per-finding matching appears only via the skill's security rule (evidence check 2); NOT RUN wording never converts to a pass; overwrite-in-place scoped to one side (check 4).
- `engagement-orchestrator.agent.md` stage paragraph — asymmetric-evidence marking (check 3) and retained insertion placeholder for features 16–18.
- Four reused audit agent files — `git status` clean; grant lists unchanged (AC5).
