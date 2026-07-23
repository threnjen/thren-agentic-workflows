# Phase 2: Comparative Audit Engine

**Status**: Planned
**Depends on**: Phase 01 (prepared analysis branches, graphs, baseline snapshots, engagement configuration)
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`

## What's New

With every comparison side prepared, the engagement can now actually be *audited*. This phase adds the comparative audit engine: the same audit scans run on the original side and the upgraded side of each pair, and a delta synthesizer turns the paired reports into plain-language before/after documents. Its outputs feed three client-spec deliverables — the business-framed findings report, the severity-rated out-of-scope issues register, and the "audit trail of our own work" proof that the upgraded repos pass the categories we flagged.

## Objective

Produce paired per-side audit reports and business-framed delta documents for every comparison pair, correctly routed into in-scope findings versus out-of-scope register using the SOW's exclusions.

## Scope

### In Scope

- **Comparative scan orchestration**: for each pair in the engagement configuration, run each audit dimension against both sides' analysis branches and store per-side reports with a consistent structure so they can be paired mechanically. Dimensions: security, code quality, dependencies/supply-chain, and infrastructure/configuration.
- **Reuse of existing auditors**: the existing `z-auditor-code`, `z-auditor-infra`, `z-dependency-auditor`, and full-codebase security-scan assets are the scan engines; this phase adds cross-repo comparability (stable finding categories, severities, and identifiers across two unrelated histories), not new scanners.
- **Delta synthesizer**: an agent that consumes one pair's two per-side report sets and produces a business-framed before/after document per pair — headline-metrics table, resolved/improved/unchanged/new classification per finding category, plain-language narrative leading with business meaning, technical evidence in appendices.
- **SOW exclusions routing**: findings present in the original side and excluded by the SOW's exclusions section (§9 for the pilot) are routed into a severity-rated out-of-scope issues register instead of the findings report. The routing reads the exclusions from the configured SOW document; when no SOW is configured (a recorded Phase 01 omission), everything stays in the findings report and the register notes the missing input.
- **Audit-trail proof output**: the upgraded-side reports reframed as evidence — "the delivered repos pass the categories we flagged on the originals" — as pipeline input for Phase 06 assembly.
- **Cloud/cost observations**: a lightweight observation pass (from the same scan evidence, not a new scanner) captured for inclusion in the findings report, per the client deliverables spec.
- **Compact orchestrator results**: per-pair pointers and summary metrics only; full reports live on disk, mirroring Phase 01's compact-handoff pattern.

### Out of Scope

- Remediation of any finding (project non-goal — audit agents report, never fix)
- Narrative/specification documents (Phase 03) and operational docs (Phase 04)
- SOW acceptance-criteria walkthrough and verification summary (Phase 05)
- PDF assembly and branding (Phase 06) — outputs here are markdown pipeline artifacts
- Git-diff-based comparison — sides have separate histories; comparison is report-vs-report
- Quality gates on scan coverage — coverage gaps are recorded, not blocking

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Comparative scan orchestrator | Runs each audit dimension on both sides of every pair, enforcing a pairable report structure | orchestration, per-side scan runs |
| 2 | Pairable audit report convention | Stable categories, severities, and finding identifiers so two independent scans can be compared mechanically | report schema/convention |
| 3 | Delta synthesizer | Per-pair before/after business-framed document with headline metrics and finding classification | delta synthesis |
| 4 | Out-of-scope register | Severity-rated register of pre-existing excluded findings, routed via the SOW exclusions | exclusions routing |
| 5 | Audit-trail proof | Upgraded-side evidence framed as "our deliverable passes what we flagged" | audit-trail framing |
| 6 | Cloud/cost observations | Business-relevant cloud and cost notes drawn from scan evidence | observations capture |

## Technical Context

- Phase 01 provides, per side: an analysis branch with a docs-writer documentation set, a built code-review-graph, and an internal baseline snapshot (commit SHA, graph stats, language coverage). Scans run from those analysis-branch checkouts and should consume graphs/docs rather than raw full-file sweeps where possible.
- Existing scan assets to reuse: `source_of_truth/agents/` definitions for the code/infra/dependency auditors and the security-scan skill; the `auditor-conventions` skill defines the shared report structure — extend it (in `source_of_truth/`) with the cross-repo comparability fields rather than inventing a parallel convention.
- The engagement configuration (Phase 01 schema, `engagement-configuration` skill) supplies the pair list, side roles, and the SOW pointer; the Phase 01 baseline snapshot records whether the SOW was present.
- All new agents/skills live in `source_of_truth/` and propagate via `scripts/propagate_master_assets.py` to a fixed point; never hand-edit `ports/` or `.github/`.
- Two value-story modes matter downstream: pure-modernization pairs expect mostly "resolved/unchanged" deltas; modernized-and-improved pairs will also show intentional "new/changed" entries — the synthesizer must not frame intentional change as regression.

## Dependencies & Risks

- **Dependency**: Phase 01 preparation completed for every pair (analysis branches, graphs, baseline snapshots). Mitigation: preflight verifies the baseline snapshot per side before any scan starts and reports exactly which side is unprepared.
- **Risk**: two independent scans describe the same issue differently, breaking pairing. Mitigation: the pairable report convention fixes categories/severities/identifiers up front, and the synthesizer treats unmatched findings as "new" or "resolved" explicitly rather than dropping them.
- **Risk**: SOW exclusions are ambiguous or the SOW is absent. Mitigation: absent SOW → no routing, everything in findings, omission recorded; ambiguous exclusions → route conservatively into findings and flag the ambiguity for user review.
- **Risk**: legacy-side scans surface overwhelming finding volume. Mitigation: business-framed synthesis aggregates by category with counts; full detail stays in appendices/per-side reports.
- **Risk**: orchestrator context blowout across 4+ scan dimensions × 2 sides × N pairs. Mitigation: child agents per scan, compact per-run results and file pointers only.
- **Risk**: intentional functional changes (improved-mode pairs) misread as regressions. Mitigation: synthesizer input includes the pair's value-story mode from the engagement configuration/discovery context.

## Success Criteria

- [ ] For each configured pair, every audit dimension (security, code quality, dependencies, infrastructure) has a per-side report produced from the analysis-branch checkout, in the pairable report structure
- [ ] A per-pair delta document exists that classifies finding categories as resolved/improved/unchanged/new, leads with plain-language business meaning, and includes a headline-metrics table
- [ ] Findings matching the configured SOW's exclusions land in a severity-rated out-of-scope register, not the findings report; with no SOW configured, the register records the missing input and no findings are silently dropped
- [ ] An audit-trail proof artifact exists per pair, framed as upgraded-side evidence against the flagged categories
- [ ] Cloud/cost observations are captured for the findings report
- [ ] The orchestrator holds only compact per-pair results and pointers; full reports live as files
- [ ] No engagement repository source code is modified by any scan
- [ ] New/extended conventions and agents exist only in `source_of_truth/` with propagation run to a fixed point

## QA Considerations

- No frontend/UI changes — no manual QA docs required.
- Verification is artifact-based: run against the pilot engagement's prepared pairs; check pairing correctness on a known finding present in one side only; exercise the no-SOW routing path; verify the synthesizer output for both value-story modes; run with one unprepared side to confirm the specific preflight failure report.

## Notes for Feature - Decomposer

Suggested feature boundaries (5):

1. **Pairable audit report convention** — extend `auditor-conventions` with cross-repo comparability (categories, severities, stable identifiers, per-side metadata). Foundation for everything else.
2. **Comparative scan orchestration** — preflight against Phase 01 baselines, then per-dimension, per-side scan runs producing convention-conformant reports.
3. **Delta synthesizer** — per-pair before/after document with classification, headline metrics, business-first narrative, value-story-mode awareness.
4. **SOW exclusions routing and out-of-scope register** — exclusions parsing from the configured SOW, conservative routing, severity-rated register, missing-SOW path.
5. **Audit-trail proof and cloud/cost observations** — reframed upgraded-side evidence plus the observations capture.

Hard constraints for every feature's AC: scans never modify engagement repo source; comparison is report-vs-report, never git-diff; business-language-first with technical appendices; compact orchestrator handoffs; `source_of_truth/` is the only authoring surface.
