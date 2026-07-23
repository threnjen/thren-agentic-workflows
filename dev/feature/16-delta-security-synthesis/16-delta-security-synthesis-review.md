# Review Record: 16-delta-security-synthesis

## Summary

Reviewed four new hidden engagement subagents (delta synthesizer, security narrative, introduced issues, pricing researcher) and the orchestrator wiring against the plan's ten ACs. The audit-trail merge into the delta synthesizer (plan's explicit merge permission) preserves the AC5 document contract intact: `deliverables/<pair>/audit-trail-proof.md`, category × upgraded-status checklist, NOT VERIFIED wording, "same standard" framing. Two issues found and fixed: `docs/ARCHITECTURE.md` count claims stale at 45 (actual 49) — third recurrence of the summary-surface count pattern from reviews 14 and 15 — and the pricing researcher lacked the AC7 asymmetric-evidence rule despite the implementation record claiming it was present in all four agents. Propagated to a fixed point (second run zero changes); suite at exact baseline.

## Verdict
Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Met | `engagement-delta-synthesizer.agent.md` "Delta Document" | Metrics table, 4-way classification, business narrative, appendices with report citations, `mode` framing (intentional change ≠ regression) |
| AC2 | Met | `engagement-delta-synthesizer.agent.md` "SOW-Exclusions Partition" | Single source; security→narrative §3, others→out-of-scope; no-SOW recorded; ambiguous→conservative+flag; exhaustive three-way partition |
| AC3 | Met | `engagement-security-narrative.agent.md` | Four numbered sections; exactly-one classification with unclassifiable→residual+flag; empty-state sections 2–4 never omitted |
| AC4 | Met | `engagement-introduced-issues.agent.md` | Internal-only header blockquote; per-finding identifiers; "new or newly-visible"; fix-and-re-run flow; NOT RUN never "no issues" |
| AC5 | Met | `engagement-delta-synthesizer.agent.md` "Audit-Trail Proof" | Merged per plan permission; contract intact (checklist, citations, NOT VERIFIED, "same standard" framing) |
| AC6 | Met | `engagement-pricing-researcher.agent.md` | Query hygiene, citation+date, NOT RESEARCHED all in the one file; sole `web/*` grant among the four (others `[read, search, edit]` exactly, verified) |
| AC7 | Met (after fix) | All four agents + orchestrator stage prose | Pricing researcher was missing the rule (Issue #2, fixed) |
| AC8 | Met | `engagement-orchestrator.agent.md:5,99-124` | Roster uses display names; two stages inserted before retained placeholder; 15's stage and boundaries pass-through preserved |
| AC9 | Met (verified) | Propagation + `tests/` | Re-ran: second `--once` run zero changes; `uv run pytest tests/` = 233 passed, 113 subtests — exact baseline |
| AC10 | Met | All authored files | Shared rules cited by skill name; no restated layouts/severities; each rule stated once |

Runtime behavior of the agents (partition routing, empty states, query hygiene in practice) is unverifiable statically; deferred to the phase-level manual QA checklist per plan §F — consistent with the implementation record's Gaps section.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Agent-count claims stale (45, actual 49) — same summary-surface class as reviews 14 and 15 | Medium | `docs/ARCHITECTURE.md:36,125` | AC9 | Fixed |
| 2 | AC7 asymmetric-evidence rule absent from pricing researcher; implementation record overclaimed "Asymmetric Evidence sections" in all four agents | Medium | `engagement-pricing-researcher.agent.md` | AC7 | Fixed |
| 3 | `docs/CODEBASE_CONTEXT.md:15` names `prod-code-review.md`; actual file is `04f-prod-code-review.md` (pre-existing, not introduced by this feature) | Low | `docs/CODEBASE_CONTEXT.md:15` | — | Open |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `docs/ARCHITECTURE.md` | 45 → 49 agent definitions (Mermaid label line 36, prose line 125) | 1 |
| `source_of_truth/agents/engagement-pricing-researcher.agent.md` | Added one line: NOT RUN dependency/infra dimension reported as asymmetric evidence, never a cost delta | 2 |
| `ports/`, `.github/` | Regenerated via propagator (fixed point; second run zero changes) | 2 |

## Remaining Concerns

- Issue #3: stale filename reference in CODEBASE_CONTEXT — low severity, defer to next docs pass.
- No automated guard pins `docs/ARCHITECTURE.md` counts; this is the third consecutive review catching it manually. Pattern already captured in `review-learnings.md` ("update every summary surface"); consider extending `test_retirement_reconciliation.py` coverage to ARCHITECTURE.md.

## Test Coverage Assessment
- Covered: AC9 (propagation/sync suite + count guards, re-executed); AC1–AC8, AC10 by code-review evidence per plan §F.
- Missing: phase-level manual QA (one-sided finding matching, no-SOW routing, "new vs. newly-visible" labeling, pricing query-log inspection) — deferred by plan, not this feature's scope.

## Risk Summary
- Agent behavior is prose-enforced; classification completeness and query hygiene depend on runtime adherence — manual QA at phase level is the real gate.
- `engagement-orchestrator.agent.md` is shared with features 14/15/17/18; placeholder retained, but merge conflicts remain a coordination risk for 17/18.
- ARCHITECTURE.md counts have no test guard and drift every feature.
