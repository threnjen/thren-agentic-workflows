# Implementation Record: 16-delta-security-synthesis

## Summary

Created four hidden engagement subagents and wired them into `Engagement - Orchestrator` as two new per-pair stages (Delta & Security Synthesis; Cloud/Cost Analysis). The delta synthesizer owns the single-point SOW-exclusions partition, the client-facing delta document, and the audit-trail proof (merge decision below). The security narrative consumes the partition and enforces classification completeness (repaired / out-of-scope / residual, exactly one each). The introduced-issues report is internal-only by header with "new or newly-visible" labeling and the documented fix-and-re-run flow. The pricing researcher is the sole web-granted engagement agent with query hygiene, citation+date, and NOT RESEARCHED rules all in its own definition. Propagated to a fixed point (second run zero changes), recounted marker guards from disk, suite restored to exact baseline.

Resolved names and decisions:
- **Merge decision**: audit-trail proof merged into the delta synthesizer (identical inputs — both report sets, same category walk); its document contract survives intact as `deliverables/<pair>/audit-trail-proof.md`. 4 agents instead of the proposed 5. Pricing researcher kept standalone as mandated.
- **Agents** (all hidden, `z-` prefixed on deploy):
  - `source_of_truth/agents/engagement-delta-synthesizer.agent.md` — `Engagement - Delta Synthesizer`
  - `source_of_truth/agents/engagement-security-narrative.agent.md` — `Engagement - Security Narrative`
  - `source_of_truth/agents/engagement-introduced-issues.agent.md` — `Engagement - Introduced Issues`
  - `source_of_truth/agents/engagement-pricing-researcher.agent.md` — `Engagement - Pricing Researcher`
- **Document filenames** (for 18's manifest schema; workspace-root relative):
  - `deliverables/<pair-name>/delta-report.md` (client-facing, AC1)
  - `deliverables/<pair-name>/security-narrative.md` (client-facing, AC3)
  - `deliverables/<pair-name>/audit-trail-proof.md` (client-facing, AC5; grouped with compliance materials by 18)
  - `deliverables/<pair-name>/cloud-cost-analysis.md` (client-facing, AC6)
  - `internal/<pair-name>/introduced-issues.md` (internal-only, AC4)
  - `pairs/<pair-name>/exclusions-partition.md` (internal working artifact, AC2)
- **Partition location**: the exclusions partition lives in the delta synthesizer only; the security narrative and delta document consume it, never re-derive it (stated in both definitions).
- **Sole-internet wording**: existing auditors carry `fetch`, so the exclusivity claim is scoped as behavior + grant class: pricing researcher is "the only engagement-fleet agent granted web-search/web-fetch access" (its own frontmatter/description) and "the only agent permitted internet access during an engagement run" (orchestrator stage prose). All other new agents: `tools: [read, search, edit]` — no web-class grants.

## Sibling Features

- Consumes 14 (`engagement-orchestrator.agent.md`, `engagement-workspace` skill, boundaries, per-pair `mode`) and 15 (retained reports at `pairs/<pair>/<side>/audits/<dimension>/`, `auditor-conventions` Comparative Scans convention, asymmetric-evidence flag, one-side re-run).
- Upstream of 17 (narrative/spec docs — untouched) and 18 (manifest — document filenames above are its inputs; agents/README.md catalog entries deferred to 18 per 14/15 precedent).
- Orchestrator edits additive: stages inserted at the retained placeholder; 14's contract and 15's stage preserved; placeholder retained for 17/18.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | code-review | Delta doc: metrics table, resolved/improved/unchanged/new, business narrative + appendices, citations, `mode` framing | Complete | engagement-delta-synthesizer.agent.md | "Delta Document" section | PENDING | PENDING |
| AC2 | AC2 | code-review | Single-point partition; security→narrative §3, others→out-of-scope; no-SOW recorded; ambiguous→conservative+flag; none dropped | Complete | engagement-delta-synthesizer.agent.md | "SOW-Exclusions Partition — Single Source" section | PENDING | PENDING |
| AC3 | AC3 | code-review | Four sections; exactly-one classification; empty states emitted | Complete | engagement-security-narrative.agent.md | numbered sections; "Classification Completeness" | PENDING | PENDING |
| AC4 | AC4 | code-review | Internal-only header; per-finding identifiers; "new or newly-visible"; fix flow; NOT RUN never "no issues" | Complete | engagement-introduced-issues.agent.md | header blockquote; "Fix Flow" section | PENDING | PENDING |
| AC5 | AC5 | code-review | Category × upgraded-status checklist; NOT VERIFIED never a pass; "same standard" framing | Complete | engagement-delta-synthesizer.agent.md | "Audit-Trail Proof" section | PENDING | PENDING |
| AC6 | AC6 | code-review | Query hygiene + citation/date + NOT RESEARCHED all in the one definition; sole web grant | Complete | engagement-pricing-researcher.agent.md | whole file; `tools:` lines of all four new agents | PENDING | PENDING |
| AC7 | AC7 | code-review | NOT RUN = asymmetric evidence, never a delta, in every document | Complete | all four agents + orchestrator | "Asymmetric Evidence" sections; stage preamble | PENDING | PENDING |
| AC8 | AC8 | code-review | Roster (display names) + loop stages; compact handoff; boundaries pass through | Complete | engagement-orchestrator.agent.md | `agents:` roster; two new stage headings | PENDING | PENDING |
| AC9 | AC9 | `uv run pytest tests/` | source_of_truth only; fixed point; count guards recounted; no new failures | Complete | tests/test_propagate_master_assets.py; README.md; docs/CODEBASE_CONTEXT.md | second propagation run zero changes; suite 233/113 | PENDING | PENDING |
| AC10 | AC10 | code-review | Each rule once; shared rules referenced (workspace, conventions, boundaries) | Complete | all authored files | skills cited by name, layouts/severities never restated | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Delta document | Complete | engagement-delta-synthesizer.agent.md | `mode` framing: intentional change ≠ regression |
| AC2 | SOW exclusions routing | Complete | engagement-delta-synthesizer.agent.md | Partition file `pairs/<pair>/exclusions-partition.md` |
| AC3 | Security narrative | Complete | engagement-security-narrative.agent.md | Unclassifiable → residual + user-review flag |
| AC4 | Introduced-issues report | Complete | engagement-introduced-issues.agent.md | Internal-only header; cites consumed reports for staleness |
| AC5 | Audit-trail proof | Complete | engagement-delta-synthesizer.agent.md | Merged into synthesizer (decision above) |
| AC6 | Pricing researcher | Complete | engagement-pricing-researcher.agent.md | `tools: [read, search, edit, web/fetch, web/search]` |
| AC7 | Asymmetric evidence | Complete | all four + orchestrator | Never a delta, never a pass |
| AC8 | Orchestrator wiring | Complete | engagement-orchestrator.agent.md | Two stages before retained placeholder |
| AC9 | Propagation + suite clean | Complete | tests + doc count claims | 233 passed, 113 subtests — exact baseline |
| AC10 | Brevity | Complete | all authored files | Shared rules by reference only |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Modify (feature 15) | "Comparative Scans" section (prior pass) | AC3/15 |
| `source_of_truth/agents/engagement-audit-runner.agent.md` | Create (feature 15) | Hidden audit runner (prior pass) | 15 |
| `source_of_truth/agents/engagement-delta-synthesizer.agent.md` | Create | Delta doc, exclusions partition, audit-trail proof, asymmetric-evidence rule | AC1, AC2, AC5, AC7 |
| `source_of_truth/agents/engagement-security-narrative.agent.md` | Create | Four-section narrative, classification completeness, empty states | AC3, AC7 |
| `source_of_truth/agents/engagement-introduced-issues.agent.md` | Create | Internal-only report, "new or newly-visible", fix flow, NOT RUN handling | AC4, AC7 |
| `source_of_truth/agents/engagement-pricing-researcher.agent.md` | Create | Cloud/cost analysis, query hygiene, offline fallback, sole web grant | AC6 |
| `source_of_truth/agents/engagement-orchestrator.agent.md` | Modify | Roster +4 display names; "Stage: Delta & Security Synthesis" and "Stage: Cloud/Cost Analysis" | AC8 |
| `README.md` | Modify | Source-agent count claim 45 → 49 | AC9 — count-claim guard (`test_retirement_reconciliation.py`) |
| `docs/CODEBASE_CONTEXT.md` | Modify | 45 → 49 definitions, 43 → 47 `*.agent.md`, 25 → 29 hidden subagents | AC9 — same guard |
| `ports/`, `.github/` | Generated | Regenerated by propagator (fixed point; second run zero changes) | AC9 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Marker-guard counts recounted from disk: claude/agents 31→35, opencode 45→49, codex 45→49, claude/commands unchanged (20); comment in existing style | AC9 |

## Test Results
- **Baseline**: 233 passed, 113 subtests passed, 0 failed (matches context record; re-verified 2026-07-22)
- **Final**: 233 passed, 113 subtests passed, 0 failed
- **New tests added**: 0 (markdown-asset feature; existing propagation suite is the guard per plan §F). Red step: guard counts bumped first, suite failed (3 failed) pre-propagation, then went green after propagation.
- **Regressions**: None

## Deviations from Plan

- Four agents, not five: audit-trail proof merged into the delta synthesizer under the plan's explicit merge permission; document contract intact.
- `README.md`/`docs/CODEBASE_CONTEXT.md` count-claim updates — required by `test_retirement_reconciliation.py`, matching 14/15 precedent.

## Gaps

- Manual QA (one-sided finding matching, no-SOW routing path, "new vs. newly-visible" labeling, pricing query-log inspection) deferred to the phase-level checklist per plan §F.
- `source_of_truth/agents/README.md` catalog entries deferred to feature 18 (matching 14/15 precedent; no test pins the catalog).

Top evidence checks (plan §F), all walked and passing:
1. Classification completeness: narrative's "exactly one of repaired / out-of-scope / residual" + unclassifiable→residual fallback makes an unclassified finding impossible by construction.
2. Pricing rules: query hygiene, citation+retrieval-date, and NOT RESEARCHED all in `engagement-pricing-researcher.agent.md` alone.
3. NOT RUN paths: audit-trail reads NOT VERIFIED; introduced-issues reads NOT RUN, never "no introduced issues."
4. `mode` changes delta framing (intentional change ≠ regression); out-of-scope section explicitly non-security-only.
5. Propagation: second `--once` run reported zero changes (`converged: true, changed_passes: 0`).

## Reviewer Focus Areas

- `engagement-delta-synthesizer.agent.md` — partition exhaustiveness (findings / security-excluded / other-excluded), NOT VERIFIED wording, and that the out-of-scope section excludes security items.
- `engagement-security-narrative.agent.md` — partition consumed, not re-derived; empty-state sections 2–4 never omitted.
- Grant review: pricing researcher is the only new agent with `web/*` grants; the other three are `[read, search, edit]` exactly.
- `engagement-orchestrator.agent.md` — roster uses display names (propagator resolves by display name); 15's stage and the insertion placeholder preserved.
