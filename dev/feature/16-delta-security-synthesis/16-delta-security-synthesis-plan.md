# Plan: 16-delta-security-synthesis

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** no
- **Depends on:** 14-engagement-orchestrator-core, 15-comparative-audit-runs
- **Key files modified:** `source_of_truth/agents/engagement-delta-synthesizer.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-security-narrative.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-introduced-issues.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-audit-trail.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-pricing-researcher.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] (roster + loop steps), `tests/test_propagate_master_assets.py` (verify — marker-guard counts)
- **Sequential reason:** shares the orchestrator agent file with upstream 14 and 15; consumes 15's retained reports and comparability convention

Phase document: `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` (Key Deliverables 3–5, bundle 3).

Agent-count note: five new subagents are proposed; the implementer may merge closely-coupled documents into fewer agents (e.g., audit-trail into the delta synthesizer) if each output document's contract survives intact — record the merge as a decision. The pricing-researcher must remain its **own** agent (its internet grant and query-hygiene rule must not attach to anything else).

## A. Requirements & Traceability

Acceptance criteria:

- **AC1 (delta document)**: Per pair, a client-facing delta document — the engagement's findings report — consumes the pair's two report sets and produces a business-framed before/after document: headline-metrics table, resolved/improved/unchanged/new classification, plain-language narrative leading with business meaning, technical evidence in appendices, citing the retained raw reports. Takes the pair's value-story `mode` as input so intentional change is not framed as regression. Includes an "out of scope under the SOW" section: non-security original-side findings excluded by the SOW's exclusions section, severity-rated.
- **AC2 (SOW exclusions routing)**: Findings present on the original side and excluded by the SOW's exclusions section route by dimension — security exclusions into section 3 of the security narrative, all others into the delta document's out-of-scope section. No SOW configured → everything stays in findings and the missing input is recorded; ambiguous exclusions route conservatively into findings, flagged for user review. No finding is silently dropped.
- **AC3 (security narrative)**: Per pair, a client-facing security narrative with four sections: (1) original-repo security posture, business-framed; (2) repaired findings tied to the SOW scope items that covered them; (3) pre-existing out-of-scope findings — the authoritative client-facing treatment of security exclusions; (4) residual risks, each leading with business consequence followed by only a brief plain-language mechanism note. Every original-side security risk is classified repaired / out-of-scope / residual; none silently dropped.
- **AC4 (introduced-issues report)**: Per pair, an internal engineer-facing report (never client-facing, labeled as such): upgraded-side security findings with no original-side counterpart, in full technical detail (file, finding, severity, evidence), using 15's per-finding security identifiers. Visibility-ambiguous findings are labeled "new or newly-visible," never asserted as introduced. The fix flow is documented: report → engineer fixes → re-run that side's scans (15's one-side re-run) → finalize client-facing artifacts.
- **AC5 (audit-trail proof)**: Per pair, a short client-facing checklist: every category flagged in original-side findings × the upgraded side's status for that category, citing upgraded-side raw reports. A category unverifiable (dimension NOT RUN on the upgraded side) reads NOT VERIFIED, never a pass. Framing: "we held our own work to the same standard we judged yours by." Grouped with the compliance materials in the manifest (18).
- **AC6 (pricing-researcher + cloud/cost analysis)**: A new pricing-researcher subagent turns scan/dependency evidence of what changed (runtime versions, dropped services, dependency swaps) into a per-pair client-facing cloud/cost analysis. Every quantified figure cites source and retrieval date; unquantifiable changes stay qualitative. **Query hygiene, in the agent's own definition**: the sole internet-touching fleet agent; queries may contain only generic service/product names and pricing questions — never client code, config values, identifiers, or any engagement repo content. **Offline fallback**: no internet in session → qualitative-only with quantified claims marked NOT RESEARCHED — never invented figures.
- **AC7**: A dimension NOT RUN on one side (15's asymmetric-evidence flag) is reported as asymmetric evidence in every synthesized document — never presented as a delta.
- **AC8**: All five outputs are wired into the orchestrator loop under the compact-handoff contract, writing into the workspace layout; inherited boundaries pass through.
- **AC9**: `source_of_truth/` only; propagation to fixed point; no new test failures (count guards updated for new agents).
- **AC10 (brevity)**: each definition states behavior, constraints, output contract once; shared rules (boundary, layout, conventions) are referenced, not restated.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC2 | delta-synthesizer agent [PROPOSED]; security-narrative agent [PROPOSED] (routing target) | Code-review evidence |
| AC3 | security-narrative agent [PROPOSED] | Code-review evidence (four sections; classification completeness rule) |
| AC4 | introduced-issues agent [PROPOSED] | Code-review evidence ("new or newly-visible" labeling; internal-only header) |
| AC5 | audit-trail agent [PROPOSED] | Code-review evidence (NOT VERIFIED wording) |
| AC6 | pricing-researcher agent [PROPOSED] | Code-review evidence (query-hygiene + NOT RESEARCHED in definition) |
| AC7, AC8 | all five + orchestrator file | Code-review evidence |
| AC9 | `ports/`, `.github/`, `tests/test_propagate_master_assets.py:768-769` | Existing automated suite; count bump |

Non-goals: remediation of any finding; a standalone out-of-scope register (routing per AC2 replaces it); narrative/spec docs (17); manifest/compliance docs (18); modifying `web-research-specialist` (the pricing-researcher is new and terse, not an exception-laden extension).

## B. Correctness & Edge Cases

- No SOW → AC2's no-routing path; missing input recorded in working state and visible downstream (18's compliance docs).
- Ambiguous exclusion → conservative routing into findings + user-review flag.
- Zero original-side security findings → narrative sections 2–4 still emitted with honest empty-state statements, not omitted.
- Upgraded-side security scan NOT RUN → introduced-issues report is NOT RUN (asymmetry, AC7), not an empty "no introduced issues" claim.
- Stale reports after engineer fixes → the documented re-run flow (AC4) refreshes downstream artifacts; synthesized docs cite the reports they consumed.
- Pricing: figure found but undated/unsourced → stays qualitative; offline → NOT RESEARCHED (AC6).

## C. Consistency & Architecture Fit

- All consumers read 15's retained reports and comparability convention — report-vs-report, never git-diff.
- Value-story `mode` comes from the engagement config (14's AC7).
- Client-facing docs lead with business language, technical appendices behind (house rule from the phase).
- "Sole internet-touching" is a **behavioral engagement-time constraint, not a grant claim**: existing reused auditors already carry `fetch` in `tools:` (Discovery Delta), so the rule is expressed as (a) the pricing-researcher is the only agent *permitted* to use the internet during an engagement run, stated in the orchestrator's inherited boundaries, and (b) every **new** agent in this feature except the pricing-researcher gets read/search/edit-class grants only. Implementer records the exact wording.
- Document filenames within the workspace layout are `[PROPOSED - names TBD]` — implementer fixes them and records them for 18's manifest schema.

## D. Clean Design & Maintainability

Complexity risk is agent sprawl: five documents, up to five agents. Mitigation: merge-permission note above; shared rules by reference (AC10). Duplication risk: exclusion-routing logic must live in one place (the synthesizer that partitions findings), with the narrative and delta docs consuming the partition, not re-deriving it — implementer documents where the partition happens.

## E. Observability, Security, Operability

- Observability: every synthesized doc cites the raw reports it derives from; working-state pointers track outputs. No new logging.
- Security: introduced-issues report is internal-only by header; pricing query hygiene is the phase's highest-sensitivity control — it is an AC, in the agent definition itself, not orchestrator prose.
- Runbook: propagate → test → deploy on request; re-run flow per AC4.

## F. Test Plan

- Must-have automated: existing propagation/sync suite; count-guard bumps for the new agents.
- Existing tests to update: count guard (verify).
- Code-review evidence: AC1–AC8, AC10 — in particular grant review of the pricing-researcher (sole internet grant) and internal-only labeling of the introduced-issues report.
- Manual QA: phase-level — one-sided security finding matching, no-SOW routing path, "new vs. newly-visible" labeling, pricing query log inspection for engagement content (see execution manifest).

Top evidence checks:
1. Given the security narrative definition, when reviewed, then every original-side risk lands in exactly one of repaired/out-of-scope/residual and an unclassified finding is impossible by construction of the instructions.
2. Given the pricing-researcher definition, when reviewed, then query hygiene, citation+date, and NOT RESEARCHED rules are all present in that one file.
3. Given a NOT RUN upgraded-side dimension, when the audit-trail and introduced-issues instructions are walked, then outputs read NOT VERIFIED / NOT RUN, never a pass.
4. Given the delta synthesizer, when reviewed, then `mode` changes framing (intentional change ≠ regression) and the out-of-scope section covers non-security exclusions only.
5. Given propagation, second run reports zero changes.

## Stage 1: Delta Synthesizer + Exclusions Routing
**Goal**: delta-synthesizer agent with classification, headline metrics, out-of-scope section; single-point SOW-exclusions partition
**Success Criteria**: AC1, AC2, AC7
**Status**: Not Started

## Stage 2: Security Outputs
**Goal**: security-narrative, introduced-issues, audit-trail agents
**Success Criteria**: AC3, AC4, AC5
**Status**: Not Started

## Stage 3: Pricing Researcher + Cloud/Cost Analysis
**Goal**: pricing-researcher agent with query hygiene and offline fallback
**Success Criteria**: AC6
**Status**: Not Started

## Stage 4: Orchestrator Wiring, Propagate & Verify
**Goal**: roster/loop integration; fixed point; clean baseline
**Success Criteria**: AC8, AC9, AC10
**Status**: Not Started

## Relationship Notes

Consumes 14 (workspace, contract, `mode`) and 15 (reports, convention, asymmetry flag, one-side re-run). Upstream of 18: document filenames/locations feed the manifest schema; the audit-trail proof is grouped with compliance materials there.
