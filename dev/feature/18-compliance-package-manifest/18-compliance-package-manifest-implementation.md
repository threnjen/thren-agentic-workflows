# Implementation Record: 18-compliance-package-manifest

## Summary

Created the `engagement-package-manifest` skill (two-section schema, row fields, derivation from the pair roster, present/missing detection stated once), two hidden agents — `Engagement - Compliance Writer` (SOW walkthrough + verification summary + manifest assembly) and `Engagement - Gap Reviewer` (client-perspective review, always-emitted internal report) — and wired the orchestrator's engagement-final stage (compliance → manifest → gap review), completing the end-to-end loop. Reconciled the agents/README.md catalog for ALL Phase 02 agents (deferred by 14–17), all count claims, and the marker guards. Propagated to a fixed point; suite at exact baseline.

Resolved names (Stage 0):
- Skill: `source_of_truth/skills/engagement-package-manifest/SKILL.md`, name `engagement-package-manifest`
- Agents: `engagement-compliance-writer.agent.md` (`Engagement - Compliance Writer`), `engagement-gap-reviewer.agent.md` (`Engagement - Gap Reviewer`) — both hidden, `tools: [read, search, edit]`
- New document paths (workspace-root relative): `deliverables/sow-compliance-walkthrough.md`, `deliverables/verification-summary.md`, `manifest.md` (root, reserved by 14), `internal/gap-review.md`
- Upstream names consumed as implemented: `engagement-state.md` (14); `pairs/<p>/<side>/audits/<dimension>/` raw reports (15); `deliverables/<p>/{delta-report,security-narrative,audit-trail-proof,cloud-cost-analysis}.md`, `internal/<p>/introduced-issues.md`, `pairs/<p>/exclusions-partition.md` (16); `deliverables/<p>/{business-design,intended-behavior-spec,workflow-narratives}.md` (17); `engagement-baseline-snapshot.md` (Phase 01)

Design decisions (safest-default, documented):
- **Manifest writer = Compliance Writer**: keeps the plan's "one skill + two agents" shape; it already walks the deliverable set for evidence, so it assembles `manifest.md` loading the schema skill. The gap reviewer consumes the manifest, never re-derives.
- **Phase 01 snapshot path resolution**: snapshots live on each side's analysis branch (client repo) but AC3 requires all manifest paths inside the workspace root — the schema directs the manifest-writing step to copy each snapshot (metadata only, no source content) to `pairs/<p>/<side>/engagement-baseline-snapshot.md`.
- **Orchestrator placeholder removed**: 18 is the phase's last feature; the per-pair-loop insertion comment is replaced by the engagement-level finalization stage.
- **Mode and expected entries**: `mode` affects document content upstream, not the expected-entry set — stated once in the schema (17's workflow narratives exist in both modes with honest no-delta content).

## Sibling Features

Consumes 14 (workspace root, `manifest.md` reservation, working state, boundaries), 15 (raw report retention paths), 16 (delta/security document names; audit-trail proof grouped with compliance materials in client-facing ordering; introduced-issues technical-only), 17 (intended-behavior spec referenced by the verification summary). No sibling files modified beyond the orchestrator wiring and reconciliation surfaces. This is the phase-final integration feature.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | code-review | SOW-only criteria; evidence from retained artifacts; NOT RUN never a pass; missing-SOW honest | Complete | `source_of_truth/agents/engagement-compliance-writer.agent.md` | "SOW Compliance Walkthrough" section | PENDING | PENDING |
| AC2 | AC2 | code-review | Verification summary with functional-preservation statement referencing `intended-behavior-spec.md` | Complete | same file | "Verification Summary" section | PENDING | PENDING |
| AC3 | AC3 | code-review | Two-section schema; row fields; derivation per pairs/modes; standing technical entries; workspace-root path rule | Complete | `source_of_truth/skills/engagement-package-manifest/SKILL.md` | whole file | PENDING | PENDING |
| AC4 | AC4 | code-review | Manifest-as-checklist; report emitted unconditionally; standing technical entry | Complete | `source_of_truth/agents/engagement-gap-reviewer.agent.md` | "Report — Always Emitted"; schema tech entry 3 | PENDING | PENDING |
| AC5 | AC5 | code-review + phase manual QA | End-to-end loop: prepare → audits → synthesis → narratives → compliance → manifest → gap review, compact handoff throughout | Complete | `source_of_truth/agents/engagement-orchestrator.agent.md` | roster; "5. Compliance, Manifest & Gap Review" | PENDING | PENDING |
| AC6 | AC6 | existing count/derivation guards + code-review | Catalog + counts reconciled for ALL Phase 02 agents/skills, recounted from disk | Complete | `source_of_truth/agents/README.md`, `README.md`, `docs/CODEBASE_CONTEXT.md`, `tests/test_propagate_master_assets.py` | catalog rows/blurbs for 9 engagement agents; counts 52/50/32/20/29 | PENDING | PENDING |
| AC7 | AC7 | `uv run pytest tests/` | source_of_truth only; fixed point; no new failures | Complete | tests + generated tree | second `--once` run: `converged: true, changed_passes: 0`; suite 233/113 | PENDING | PENDING |
| AC8 | AC8 | code-review | Each rule once; present/missing logic only in schema | Complete | all authored files | detection rule, no-SOW fallback, path rule each stated once, in the skill | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | SOW compliance walkthrough | Complete | engagement-compliance-writer.agent.md | Criteria only from SOW; unevidenced ≠ satisfied |
| AC2 | Verification summary | Complete | engagement-compliance-writer.agent.md | References `deliverables/<p>/intended-behavior-spec.md` |
| AC3 | Package manifest schema | Complete | skills/engagement-package-manifest/SKILL.md | Derived per pair; missing rows never suppressed; NOT RUN dimension = missing row annotated NOT RUN |
| AC4 | Gap review | Complete | engagement-gap-reviewer.agent.md | Always-emit incl. honest empty state |
| AC5 | End-to-end integration | Complete | engagement-orchestrator.agent.md | Engagement-level stage after per-pair loop; blocked pairs surface as missing rows |
| AC6 | Reconciliation | Complete | agents/README.md + README.md + CODEBASE_CONTEXT.md + test guards | 14–17 had deferred all catalog entries — all 9 engagement agents added here |
| AC7 | Propagation + clean suite | Complete | generated tree + tests | 233 passed, 113 subtests — exact baseline |
| AC8 | Brevity | Complete | all authored files | Shared rules referenced by skill name only |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/engagement-package-manifest/SKILL.md` | Create | Two-section schema, row fields, derivation, present/missing detection, no-SOW fallback, snapshot-copy rule | AC3, AC8 |
| `source_of_truth/agents/engagement-compliance-writer.agent.md` | Create | SOW walkthrough, verification summary, manifest assembly | AC1, AC2, AC3 |
| `source_of_truth/agents/engagement-gap-reviewer.agent.md` | Create | Client-perspective review, always-emitted report | AC4 |
| `source_of_truth/agents/engagement-orchestrator.agent.md` | Modify | Roster +2; "5. Compliance, Manifest & Gap Review" replacing insertion placeholder | AC5 |
| `source_of_truth/agents/README.md` | Modify | Catalog rows + blurbs for all 9 Phase 02 engagement agents (user-facing: Orchestrator; hidden: 8) | AC6 |
| `README.md` | Modify | Source-agent count 50 → 52 | AC6 |
| `docs/CODEBASE_CONTEXT.md` | Modify | 50→52 definitions, 48→50 `*.agent.md`, 30→32 hidden, 28→29 skills | AC6 |
| `ports/`, `.github/` | Generated | Regenerated to fixed point (second run zero changes) | AC7 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Marker guards recounted from disk: claude/agents 36→38, opencode 50→52, codex 50→52, claude/commands unchanged (20); comment in existing style | AC6, AC7 |

## Test Results
- **Baseline**: 233 passed, 113 subtests passed, 0 failed (re-verified at start of this pass)
- **Final**: 233 passed, 113 subtests passed, 0 failed
- **New tests added**: 0 (markdown-asset feature; existing propagation/count suite is the guard per plan §F). Red observed: guards bumped first → 3 failed / 37 passed pre-assets; Green after assets + propagation.
- **Regressions**: None

## Deviations from Plan

- Manifest assembly assigned to the Compliance Writer (plan left the manifest-writing step's owner implicit within the "compliance → manifest → gap review" sequence); documented above.
- Phase 01 baseline snapshots are copied into the workspace by the manifest-writing step so their manifest rows satisfy 14's inside-the-root path rule (snapshots natively live on client-repo analysis branches).

## Gaps

- Manual QA (full orchestrator end-to-end run; deliberately-missing-document flag; gap-review report presence) deferred to the phase-level checklist per plan §F.
- `docs/CODEBASE_CONTEXT.md` line 15 still names the plain agent file `prod-code-review.md` while on disk it is `04f-prod-code-review.md` — pre-existing wording outside this feature's scope; counts reconciled regardless.

## Reviewer Focus Areas

- `engagement-package-manifest/SKILL.md` — evidence check 1: exactly one expected-entry rule per document contract from 14–17; missing rows never suppressed (check 2); snapshot-copy rule vs. 14's path rule.
- `engagement-compliance-writer.agent.md` — criteria only from the SOW; every evidence citation is a retained on-disk artifact (check 3).
- `engagement-gap-reviewer.agent.md` — unconditional emit incl. empty state (check 4).
- `engagement-orchestrator.agent.md` — the finalization stage runs per engagement after the per-pair loop; boundaries and compact handoff pass through; 15–17 stages untouched.
- Counts 38/20/52/52 and 52/50/32/20/29 claims — recounted from disk.
