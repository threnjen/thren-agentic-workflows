# Implementation Record: 09-hook-record-purge

## Summary

Purged the retired hook system's documentation record from the repository. Deleted
the historical hook phase-doc directories (`PHASE_01`, `PHASE_02`, `PHASE_04`) and
the `docs/hooks/` reference set; scrubbed the cross-phase decision log of pure-hook
sections and hook-only bullets while preserving every propagation/deployment contract
line verbatim; regenerated the propagator's `claude/learnings/` copy via `--once`;
scrubbed live-hook claims from the six standard docs; rewrote the README Acknowledgments
to past tense; reconciled the skills inventory count (16 → 24) across README,
ARCHITECTURE, and CODEBASE_CONTEXT to match disk; and verified the roadmap consistent
with post-removal reality. Prose/record deletions and edits only — no code or test
changes. Full suite stayed green (237 passed, 134 subtests).

## Sibling Features

Feature 09 is Wave 3 (runs last) of the Phase 05 hook-removal effort. It depends
informationally on:
- **07-propagator-hook-pipeline-removal** — static done-notify contract (hand-owned
  `.codex/hooks.json`, no `$source`, not propagated). Referenced in the README tree
  mention and the roadmap.
- **08-hook-framework-retirement** — DEFUNCT marker (`​.github/hooks/DEFUNCT.md`) whose
  wording the README Acknowledgments and roadmap "defunct scanner" note are kept
  consistent with; final file inventory used for the three-way count reconciliation.

No files are shared with 07/08; this feature only documents the tree those features
produced. No files were modified for a sibling's benefit.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | none (docs feature) | Directory listing / `git status` | Done | `docs/phases/PHASE_01/`, `PHASE_02/`, `PHASE_04/`, `docs/hooks/` (deleted) | `git status --short` shows 4 dirs deleted; `docs/phases/PHASE_03,05,07` + `docs/inspiration/` present | PENDING | PENDING |
| AC2 | AC2 | `test_committed_tree_is_at_a_propagation_fixed_point` (regression) | Section/line diff review + propagator convergence | Done | `.github/learnings/cross-phase-decisions.md`, `claude/learnings/cross-phase-decisions.md` (regenerated) | Headers listed by `grep '^## '`; contract sections "Propagation Contracts"/"Phase 04 Runtime Deployment Contract" intact | PENDING | PENDING |
| AC3 | AC3 | none | Grep for live-hook/bypass claims; manual read of Acknowledgments | Done | `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, `docs/LOCAL_DEVELOPMENT.md` | `README.md:168-198` (past-tense Acks + defunct scanner mention), `README.md:47` (done-notify) | PENDING | PENDING |
| AC4 | AC4 | `test_*_count_matches_disk` (regression, agents/subagents) | Three-way count reconciliation | Done | `README.md:20`, `docs/ARCHITECTURE.md:32,81`, `docs/CODEBASE_CONTEXT.md:17,35` | skills 16→24 = 24 `SKILL.md` on disk | PENDING | PENDING |
| AC5 | AC5 | none | Verify roadmap vs post-removal reality | Done (verified, no changes) | `docs/phases/PROJECT_ROADMAP.md` | `PROJECT_ROADMAP.md:12-37` already reconciled; DEFUNCT wording matches `.github/hooks/DEFUNCT.md` | PENDING | PENDING |
| AC6 | AC6 | none | Single dedicated commit (`git log`) | Pending (orchestrator commit step) | all changed files | — | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Delete PHASE_01/02/04 + docs/hooks; leave PHASE_03/05/07 + inspiration | Done | (deletions) | 4 directories removed; untouched dirs verified present |
| AC2 | Scrub decision log; regenerate generated copy via propagator | Done | `.github/learnings/…`, `claude/learnings/…` | 3 pure-hook sections deleted wholesale; 2 hook-only bullets removed from "Deferred Pipeline Work"; mixed contract sections preserved verbatim; `--once` converged (2 passes), copies identical modulo generated marker |
| AC3 | No live-hook claims in six docs; past-tense Acks; done-notify + defunct scanner mentions | Done | six standard docs | No bypass-permissions claim survives; remaining "hook" mentions are legitimate (eval git-hook templates, git-hook rollback links, static done-notify config, past-tense survey attribution) |
| AC4 | Three-way inventory counts agree with disk | Done | README/ARCHITECTURE/CODEBASE_CONTEXT | skills 16→24 (disk = 24 SKILL.md); agents 41, instructions 15, templates 2 already correct |
| AC5 | Roadmap verified consistent | Done | `docs/phases/PROJECT_ROADMAP.md` | Verify-only; already reconciled to post-removal reality, no factual mismatches found |
| AC6 | Single dedicated docs commit | Pending | — | Commit cadence owned by orchestrator; all changes are docs/record only |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `docs/phases/PHASE_01/` (5 files) | Delete | Removed hook phase records | AC1 |
| `docs/phases/PHASE_02/` (6 files) | Delete | Removed hook phase records | AC1 |
| `docs/phases/PHASE_04/` (6 files) | Delete | Removed hook phase records | AC1 |
| `docs/hooks/` (7 files) | Delete | Removed hook documentation set | AC1 |
| `.github/learnings/cross-phase-decisions.md` | Modify | Deleted "Hook Composition", "Guard Friction and Command Prompting", "File-Access Guard Retirement" sections wholesale; removed "Pre-edit file backup layer" and "WebFetch as an exfiltration channel" bullets from "Deferred Pipeline Work" | AC2 |
| `claude/learnings/cross-phase-decisions.md` | Regenerate | Refreshed by `propagate_master_assets.py --once` (not hand-edited) | AC2 |
| `README.md` | Modify | skills 16→24; done-notify one-line tree comment; Acknowledgments rewritten to past tense with defunct-scanner mention | AC3, AC4 |
| `docs/ARCHITECTURE.md` | Modify | skills 16→24 (mermaid node + prose) | AC4 |
| `docs/CODEBASE_CONTEXT.md` | Modify | skills 16→24 (counts list + key-paths tree) | AC4 |
| `HARNESS_SETUP.md` | Modify | Removed "hook/" from "generated hook/settings outputs" | AC3 |
| `docs/LOCAL_DEVELOPMENT.md` | Modify | Removed "hook," from focused-test guidance | AC3 |
| `docs/phases/PROJECT_ROADMAP.md` | Verify only | No changes — already consistent | AC5 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| (none) | — | No test changes. Pre-delete grep of `tests/` for `docs/hooks`, `PHASE_01/02/04`, and `test_explicit_rtk_guidance_remains_available` returned zero hits (feature 08 already removed the coupled test). | — |

## Test Results
- **Baseline**: 237 passed, 134 subtests passed (before implementation; post-features-07/08 tree)
- **Final**: 237 passed, 134 subtests passed (after implementation)
- **New tests added**: 0 (prose/record-only feature)
- **Regressions**: None

## Deviations from Plan
- Plan/context cited a pre-features-07/08 baseline of 401 passed / 156 subtests. At
  implementation time (post-07/08) the suite is 237 passed / 134 subtests. This is the
  expected consequence of 07/08 removing the hook pipeline and its tests, not a
  regression — baseline was re-established before work per Test Baseline protocol.

## Gaps
- AC6 (single dedicated revertable commit) is pending the orchestrator's commit step;
  all staged changes are docs/record-only, so a single commit satisfies it.
- Defunct-scanner one-line mention was added to README (Acknowledgments) only.
  ARCHITECTURE and CODEBASE_CONTEXT do not enumerate `.github/hooks/`, and the DEFUNCT
  marker states the scanner "must not be counted in asset inventories," so no scanner
  entry was injected into those inventory surfaces.

## Reviewer Focus Areas
- **Over-scrub risk (the phase's named risk)** — `.github/learnings/cross-phase-decisions.md`:
  confirm the two mixed contract sections ("Propagation Contracts" line ~259, "Phase 04
  Runtime Deployment Contract" line ~334) are byte-preserved, and that the retained
  ambiguous bullets in "Deferred Pipeline Work" (Plugin packaging, Per-agent command
  scoping, NO-GO enforcement hook, Adoption readiness) were correctly kept, not deleted.
- **Generated-copy integrity** — verify `claude/learnings/cross-phase-decisions.md`
  differs from source only by the generated marker line (was regenerated, not hand-edited).
- **Count reconciliation** — 24 skills matches `ls .github/skills/*/SKILL.md | wc -l`;
  confirm the CODEBASE_CONTEXT orchestrator/visible/hidden breakdown (lines 95-97) was
  intentionally left untouched (flagged OPEN definitional dispute in the decision log,
  guarded by disk-derived tests, out of this feature's scope).
- **Acknowledgments** — `README.md:168-198` reads as past tense with attribution intact
  and no live/bypass-permissions security claim.
