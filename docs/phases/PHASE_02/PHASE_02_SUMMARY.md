# Phase 2: Comparative Audit Engine

**Status**: Planned
**Depends on**: Phase 01 (analysis branches, graphs, and engagement configuration for the sides being compared)
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`

## What's New

With comparison sides prepared, the engagement can now actually be *audited*. This phase adds the comparative audit engine: the same existing audit agents run on the original side and the upgraded side of each pair, and lightweight synthesizer agents turn the paired reports into client-facing documents. Security is a first-class output, not just a scan dimension: each side gets a full retained security report, the client gets a dedicated plain-language security narrative (risks found, risks repaired under the SOW, risks out of scope, and residual risks with "why this matters to you" framing), and the engagement team gets an internal punch list of security issues introduced by the modernization itself so an engineer can fix them before delivery.

This phase is deliberately simple in construction: it is a small set of specialized agent definitions plus a short extension to the existing `auditor-conventions` skill. No new scanners, no orchestration framework, no report-versioning machinery.

## Objective

Produce retained per-side audit reports and business-framed comparison documents for every pair — including the dedicated security narrative and the internal introduced-issues report — with findings correctly routed into in-scope findings versus the out-of-scope register using the SOW's exclusions.

## Scope

### In Scope

- **Comparative scan runs**: for each pair in the engagement configuration, run each audit dimension against both sides' analysis branches. Dimensions: security (full-codebase security-scan asset), code quality (`z-auditor-code`), dependencies/supply-chain (`z-dependency-auditor`), and infrastructure/configuration (`z-auditor-infra`). Same agents, both checkouts; reports land in a known per-pair/per-side folder layout.
- **Retained raw agent outputs**: every raw report each auditor naturally produces (`-report.md` / `-summary.md`) is kept on disk as a first-class internal artifact, per dimension, per side, per pair. Client-facing documents are derived from and cite the raw reports; nothing is client-facing by default.
- **Slim comparability convention**: a short section appended to the existing `auditor-conventions` skill (in `source_of_truth/`) fixing stable category names and a shared severity scale so two independent scans can be compared. Pairing strictness: per-finding matching within the security dimension only (required by the introduced-issues report); category-level rollups for all other dimensions. Unmatched findings are classified explicitly as "new" or "resolved," never dropped.
- **Delta synthesizer**: an agent that consumes one pair's two report sets and produces a business-framed before/after document per pair — headline-metrics table, resolved/improved/unchanged/new classification, plain-language narrative leading with business meaning, technical evidence in appendices.
- **SOW exclusions routing and out-of-scope register**: findings present in the original side and excluded by the SOW's exclusions section (§9 for the pilot engagement) are routed into a severity-rated out-of-scope issues register instead of the findings report. When no SOW is configured, everything stays in the findings report and the register records the missing input; no finding is silently dropped. Ambiguous exclusions route conservatively into findings, flagged for user review.
- **Per-side security reports**: the security-scan asset runs on each side's analysis branch, producing a complete retained security report per side per pair — a standalone artifact, not just delta feedstock.
- **Client-facing security narrative (per pair)**, four sections:
  1. *Security posture of the original repo* — business-framed inventory of scan findings on the old side.
  2. *Repaired findings (SOW-attached)* — original-side risks resolved by the upgrade, each tied to the SOW scope item that covered it: the security-improvements list.
  3. *Pre-existing, out-of-scope findings* — original-side risks the SOW exclusions place outside the engagement; cross-references the out-of-scope register rather than duplicating its prose. The security narrative is the authoritative client-facing treatment of security residuals; the register's security rows point here.
  4. *Residual risks: why this matters* — every risk still live in the delivered repo, leading with business consequence (what could happen, to whom, at what cost), followed by only a brief plain-language (ELI5) sentence or two of mechanism.
- **Internal introduced-issues report (per pair, engineer-facing, not client-facing)**: security findings present on the upgraded side with no original-side counterpart — issues introduced by the modernization work — in full technical detail (file, finding, severity, evidence) so an engineer can fix them. Findings whose absence on the original side may reflect scanner visibility rather than true introduction are labeled "new or newly-visible," not asserted as introduced. Intended flow: introduced-issues report → engineer fixes → re-run upgraded-side scans (a re-run simply overwrites that side's report folder) → finalize client-facing artifacts. The engine supports re-running one side without redoing the pair.
- **Audit-trail proof output**: the upgraded-side reports reframed as evidence — "the delivered repos pass the categories we flagged on the originals" — as pipeline input for Phase 06 assembly.
- **Cloud/cost observations**: a lightweight observation pass from the same scan evidence (not a new scanner), captured for the findings report per the client deliverables spec.
- **Compact orchestrator results**: per-pair pointers and summary metrics only; full reports live on disk, mirroring Phase 01's compact-handoff pattern.

### Out of Scope

- Remediation of any finding by agents (project non-goal — agents report; the introduced-issues report exists precisely so a human engineer fixes)
- Narrative/specification documents (Phase 03) and operational docs (Phase 04)
- SOW acceptance-criteria walkthrough and verification summary (Phase 05)
- PDF assembly and branding (Phase 06) — outputs here are markdown pipeline artifacts
- Git-diff-based comparison — sides have separate histories; comparison is report-vs-report
- Quality gates on scan coverage — coverage gaps are recorded, not blocking
- A formal preflight tool, report-versioning machinery, or a heavyweight report schema — entry checking is a paragraph of orchestrator instruction, re-runs overwrite (git history is the version record), and the convention is a slim skill extension
- Completion of the Phase 01 pilot validation run — per user direction (2026-07-22), the pilot-validation deliverable is removed from the project plan; Phase 02's entry condition is only that analysis branches and graphs exist for the sides being compared, checked at run time. Downstream agents must not treat the formerly planned pilot-run obligations (including `[PROPOSED]` marker resolution) as unmet gates.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Comparative scan runs | Existing auditors run on both sides of every pair; raw reports retained in a known folder layout | scan runs |
| 2 | Comparability convention (slim) | Stable categories and severity scale appended to `auditor-conventions`; per-finding matching for security, rollups elsewhere | convention extension |
| 3 | Delta synthesizer | Per-pair before/after business-framed document with headline metrics and finding classification | delta synthesis |
| 4 | Out-of-scope register | Severity-rated register of pre-existing excluded findings, routed via the SOW exclusions | exclusions routing |
| 5 | Per-side security reports | Full retained security report for each side of each pair, from the existing security-scan asset | security scans |
| 6 | Client-facing security narrative | Four-section per-pair doc: original posture, SOW-attached repairs, out-of-scope pre-existing, residual risks with why-this-matters framing | security narrative |
| 7 | Introduced-issues report | Internal engineer-facing punch list of security issues new (or newly visible) in the upgraded side | introduced-issues classification |
| 8 | Audit-trail proof | Upgraded-side evidence framed as "our deliverable passes what we flagged" | audit-trail framing |
| 9 | Cloud/cost observations | Business-relevant cloud and cost notes drawn from scan evidence | observations capture |

## Technical Context

- Phase 01 provides, per side: an analysis branch with a docs-writer documentation set, a built code-review-graph, and the engagement configuration (pair list, side roles, SOW pointer). Scans run from those analysis-branch checkouts and should consume graphs/docs rather than raw full-file sweeps where possible. Entry checking is run-time: the orchestrator verifies the analysis branches and graphs exist for the sides being compared and reports exactly which side is unprepared.
- Existing scan assets to reuse: `source_of_truth/agents/` definitions for `z-auditor-code`, `z-auditor-infra`, `z-dependency-auditor`, and the security-scan skill. The `auditor-conventions` skill is extended in place (in `source_of_truth/`) — no parallel convention.
- Capability boundaries already established in this repo apply per side: auditors hold no shell grant; dependency vulnerability evidence must be supplied offline (its absence is NOT RUN, never a pass); graph unavailability is NOT RUN with a reason. A dimension that is NOT RUN on one side must be reported as asymmetric-evidence for that pair — the synthesizer must not present an asymmetric NOT RUN as a delta.
- The value-story mode per pair (pure modernization vs. modernized-and-improved) is an input to the synthesizer. If the Phase 01 engagement-configuration schema lacks a mode field, add it there as a small backward-compatible extension — do not invent a side channel.
- All new agents/skills live in `source_of_truth/` and propagate via `scripts/propagate_master_assets.py` to a fixed point; never hand-edit `ports/` or `.github/`.
- Two value-story modes matter downstream: pure-modernization pairs expect mostly "resolved/unchanged" deltas; modernized-and-improved pairs also show intentional "new/changed" entries — the synthesizer must not frame intentional change as regression.

## Dependencies & Risks

- **Dependency**: analysis branches and graphs exist for every side being compared (run-time check; the orchestrator reports exactly which side is unprepared). The Phase 01 pilot run is *not* a dependency (removed per user direction).
- **Risk**: two independent scans describe the same issue differently, breaking pairing. Mitigation: slim convention fixes categories and severities; per-finding matching is required only for security; unmatched findings are explicit "new"/"resolved," never dropped.
- **Risk**: introduced-issues report accuses the upgrade of pre-existing problems the old scanner simply couldn't see. Mitigation: "new or newly-visible" labeling for visibility-ambiguous findings.
- **Risk**: engineer fixes make the upgraded-side reports stale, so the audit-trail proof shows resolved issues. Mitigation: documented flow — fix, re-run that side's scans (overwrite), then finalize client-facing artifacts; one-side re-runs are supported.
- **Risk**: SOW exclusions are ambiguous or the SOW is absent. Mitigation: absent SOW → no routing, everything in findings, omission recorded; ambiguous exclusions → route conservatively into findings and flag for user review.
- **Risk**: legacy-side scans surface overwhelming finding volume. Mitigation: business-framed synthesis aggregates by category with counts; full detail stays in the retained raw reports and appendices.
- **Risk**: orchestrator context blowout across 4 dimensions × 2 sides × N pairs. Mitigation: child agents per scan, compact per-run results and file pointers only.
- **Risk**: intentional functional changes (improved-mode pairs) misread as regressions. Mitigation: synthesizer input includes the pair's value-story mode from the engagement configuration.

## Success Criteria

- [ ] For each configured pair, every audit dimension (security, code quality, dependencies, infrastructure) has a per-side raw report retained on disk from the analysis-branch checkout, in the agreed folder layout
- [ ] A full security report exists per side per pair as a standalone retained artifact
- [ ] The client-facing security narrative exists per pair with all four sections; every original-side security risk is classified as repaired (SOW-attached), out-of-scope, or residual, with no finding silently dropped
- [ ] Every residual risk in the security narrative carries a business-consequence statement first and only a brief plain-language mechanism note
- [ ] The introduced-issues report exists per pair, is labeled internal/engineer-facing, distinguishes "new" from "new or newly-visible," and gives file-level technical detail
- [ ] Re-running one side's scans without redoing the pair is supported and refreshes downstream artifacts from the new reports
- [ ] A per-pair delta document classifies finding categories as resolved/improved/unchanged/new, leads with plain-language business meaning, and includes a headline-metrics table
- [ ] Findings matching the configured SOW's exclusions land in the severity-rated out-of-scope register; the register's security rows cross-reference the security narrative; with no SOW configured, the register records the missing input and no findings are silently dropped
- [ ] An audit-trail proof artifact exists per pair, framed as upgraded-side evidence against the flagged categories
- [ ] Cloud/cost observations are captured for the findings report
- [ ] A dimension NOT RUN on one side is reported as asymmetric evidence, never presented as a delta
- [ ] The orchestrator holds only compact per-pair results and pointers; full reports live as files
- [ ] No engagement repository source code is modified by any scan
- [ ] New/extended conventions and agents exist only in `source_of_truth/` with propagation run to a fixed point

## QA Considerations

- No frontend/UI changes — no manual QA docs required.
- Verification is artifact-based: run against a prepared pair; check security per-finding matching on a finding present in one side only; exercise the no-SOW routing path; verify the introduced-issues "new vs. newly-visible" labeling; verify synthesizer output for both value-story modes; exercise a one-side re-run; run with one unprepared side to confirm the specific failure report.

## Notes for Feature - Decomposer

Suggested feature boundaries (4):

1. **Comparative scan runs + slim convention** — the `auditor-conventions` extension (categories, severity scale, security per-finding identifiers) plus the orchestration paragraphing that runs each existing auditor on both sides into the folder layout, with run-time entry checking and one-side re-run support.
2. **Delta synthesizer + out-of-scope register** — per-pair before/after document, SOW exclusions routing, register, value-story-mode awareness, asymmetric-evidence handling.
3. **Security narrative + introduced-issues report** — the four-section client-facing security doc and the internal engineer-facing punch list, both consuming the per-side security reports.
4. **Audit-trail proof + cloud/cost observations** — reframed upgraded-side evidence plus the observations capture.

Hard constraints for every feature's AC: scans never modify engagement repo source; comparison is report-vs-report, never git-diff; raw agent outputs are retained and cited by all synthesized documents; business-language-first with technical appendices for client-facing docs; the introduced-issues report is never client-facing; compact orchestrator handoffs; `source_of_truth/` is the only authoring surface.

**Brevity constraint on authored agent and skill definitions**: the agent and skill files this phase writes to `source_of_truth/` are loaded into model context at runtime — every unnecessary word is wasted context. Definitions must be terse: state the behavior, the constraints, and the output contract once each, and stop. No restating context the agent already has, no motivational preamble, no repeating a rule in different words, no exhaustive examples where one suffices. Carry this into every feature's AC: a definition that says the same thing twice fails review.
