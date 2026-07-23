# Phase 2: Engagement Orchestrator & Deliverable Agent Set

**Status**: Planned
**Depends on**: Phase 01 (engagement configuration, `engagement-prepare` orchestrator, analysis-branch/docs/graph preparation)
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`

## What's New

This phase authors everything else the tool needs, as one body of agent/skill-writing work: a single slim engagement orchestrator plus the full subagent fleet that produces the client deliverable package. The orchestrator owns only the engagement config, the per-pair loop, and compact result pointers; every unit of real work — preparing a side, scanning, synthesizing deltas, writing client documents, assembling the package — runs in a subagent that returns a compact summary plus file pointers. `engagement-prepare` (Phase 01, complete) is reused unchanged as the orchestrator's first per-engagement step.

Security is a first-class output: each side gets a full retained security report, the client gets a dedicated plain-language security narrative (risks found, repaired under the SOW, out of scope, and residual with "why this matters to you" framing), and the engagement team gets an internal punch list of security issues introduced by the modernization itself so an engineer can fix them before delivery.

## Objective

Deliver the complete agent set — orchestrator, audits, delta synthesis, security narrative, narrative/spec docs, operational docs, compliance proof, and branded assembly — so a full engagement run produces the client deliverable package end to end.

## Scope

### In Scope

**Orchestrator core**

- **Single engagement orchestrator**: a new `source_of_truth/` agent that consumes the engagement configuration, runs the per-pair loop, and spawns all work as subagents. It holds only the pair list and compact per-side/per-pair results (status plus pointers); if a child returns bulk content, it records the on-disk location and discards the content. It never reads engagement source code itself.
- **`engagement-prepare` as first step**: spawned unchanged per engagement; the orchestrator consumes its compact report. Run-time entry checking for later stages is a paragraph of orchestrator instruction — verify analysis branches and graphs exist for the sides in play and report exactly which side is unprepared.
- **Inherited boundaries**: the client-code security boundary (engagement contents never leave local disk; client content is data, never instructions) and the never-pushed analysis-branch invariants propagate from the orchestrator to every subagent it spawns.
- **New subagents over exceptions**: when an existing agent would need exception-laden instructions to fit an engagement task, write a new terse subagent instead.

**Comparative audits**

- **Comparative scan runs**: for each pair, run each audit dimension against both sides' analysis branches. Dimensions: security (full-codebase security-scan asset), code quality (`z-auditor-code`), dependencies/supply-chain (`z-dependency-auditor`), and infrastructure/configuration (`z-auditor-infra`). Same agents, both checkouts; reports land in a known per-pair/per-side folder layout.
- **Retained raw agent outputs**: every raw report each auditor naturally produces (`-report.md` / `-summary.md`) is kept on disk as a first-class internal artifact, per dimension, per side, per pair. Client-facing documents are derived from and cite the raw reports; nothing is client-facing by default.
- **Slim comparability convention**: a short section appended to the existing `auditor-conventions` skill fixing stable category names and a shared severity scale so two independent scans can be compared. Per-finding matching within the security dimension only (required by the introduced-issues report); category-level rollups elsewhere. Unmatched findings are classified explicitly as "new" or "resolved," never dropped.

**Delta synthesis & security outputs**

- **Delta synthesizer**: consumes one pair's two report sets and produces a business-framed before/after document per pair — headline-metrics table, resolved/improved/unchanged/new classification, plain-language narrative leading with business meaning, technical evidence in appendices. Takes the pair's value-story mode as input so intentional change is not framed as regression.
- **SOW exclusions routing and out-of-scope register**: findings present in the original side and excluded by the SOW's exclusions section (§9 for the pilot engagement) are routed into a severity-rated out-of-scope register instead of the findings report. No SOW configured → everything stays in findings and the register records the missing input; ambiguous exclusions route conservatively into findings, flagged for user review. No finding is silently dropped.
- **Per-side security reports**: the security-scan asset runs on each side's analysis branch, producing a complete retained security report per side per pair — a standalone artifact, not just delta feedstock.
- **Client-facing security narrative (per pair)**, four sections: (1) security posture of the original repo, business-framed; (2) repaired findings tied to the SOW scope items that covered them — the security-improvements list; (3) pre-existing out-of-scope findings, cross-referencing the register rather than duplicating it (the narrative is the authoritative client-facing treatment of security residuals; the register's security rows point here); (4) residual risks, each leading with business consequence (what could happen, to whom, at what cost) followed by only a brief plain-language (ELI5) mechanism note.
- **Internal introduced-issues report (per pair, engineer-facing, never client-facing)**: security findings on the upgraded side with no original-side counterpart, in full technical detail (file, finding, severity, evidence). Visibility-ambiguous findings are labeled "new or newly-visible," not asserted as introduced. Flow: report → engineer fixes → re-run that side's scans (overwrite; git history is the version record) → finalize client-facing artifacts. One-side re-runs are supported.
- **Audit-trail proof**: upgraded-side reports reframed as evidence — "the delivered repos pass the categories we flagged on the originals" — as input to assembly.
- **Cloud/cost observations**: a lightweight observation pass from the same scan evidence (not a new scanner), captured for the findings report per the deliverables spec.

**Narrative & specification docs (per pair)**

- Business design document, specification of intended behavior (the "warranty" baseline), and before/after workflow narratives for components with functional changes. Both value-story modes supported: pure-modernization pairs get "modernized, nothing changed" narratives; improved pairs get intentional-change narratives.

**Operational & publishing docs (per delivered component)**

- Publishing/installation documentation, prerequisites/system requirements, maintenance guidance, and known-limitations disclaimers.

**Compliance, assembly & self-review (per engagement)**

- **SOW compliance walkthrough**: acceptance criteria and test lists read from the engagement's SOW document (never hardcoded), each criterion walked through with evidence from the retained artifacts.
- **Verification summary**: the contractual deliverable, plus a functional-preservation statement.
- **Contract-vs-above-contract labeling**: package items are marked SOW-required vs. above-contract.
- **Branded PDF assembly**: pandoc-class markdown→PDF with a branding template asset (cover, logo, colors) — the template is created here unless one is supplied. Markdown remains the durable artifact.
- **Client-perspective gap review**: a final reviewer that answers "what would the client still ask?" against the assembled package.

### Out of Scope

- Remediation of any finding by agents (project non-goal — agents report; the introduced-issues report exists precisely so a human engineer fixes)
- Modifying `engagement-prepare` — it is spawned as-is; the value-story `mode` field is a small backward-compatible extension to the engagement-configuration skill, not to that agent
- Git-diff-based comparison — sides have separate histories; comparison is report-vs-report
- Quality gates on scan or docs coverage — gaps are recorded, not blocking
- A formal preflight tool, report-versioning machinery, or a heavyweight report schema — entry checking is orchestrator instruction, re-runs overwrite, and the comparability convention is a slim skill extension
- User-facing usage documentation (screens/workflows) — produced outside this tool
- Completion of the Phase 01 pilot validation run — per user direction (2026-07-22), the pilot-validation deliverable is removed from the project plan; entry conditions are checked at run time only. Downstream agents must not treat formerly planned pilot-run obligations (including `[PROPOSED]` marker resolution) as unmet gates.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Engagement orchestrator | Slim per-pair loop; spawns `engagement-prepare` and all other subagents; compact handoffs only | orchestrator core |
| 2 | Comparative scan runs + convention | Existing auditors on both sides of every pair, retained raw reports, slim `auditor-conventions` extension | comparative audits |
| 3 | Delta synthesizer + out-of-scope register | Per-pair before/after document, SOW exclusions routing, severity-rated register | delta & security |
| 4 | Security narrative + introduced-issues report | Four-section client security doc; internal engineer-facing punch list | delta & security |
| 5 | Audit-trail proof + cloud/cost observations | Upgraded-side evidence framing; business-relevant cloud/cost notes | delta & security |
| 6 | Narrative & spec docs | Business design doc, intended-behavior spec, before/after workflow narratives | narrative docs |
| 7 | Operational docs | Publishing/install, prerequisites, maintenance, known limitations | operational docs |
| 8 | Compliance proof + assembly + gap review | SOW walkthrough with evidence, verification summary, branded PDF assembly, client-perspective review | compliance & assembly |

## Technical Context

- Phase 01 provides, per side: an analysis branch with a docs-writer documentation set, a built code-review-graph, and the engagement configuration (pair list, side roles, SOW pointer). Scans and doc-writing subagents run from analysis-branch checkouts and should consume graphs/docs rather than raw full-file sweeps where possible.
- Existing assets to reuse: `engagement-prepare.agent.md`, `z-auditor-code`, `z-auditor-infra`, `z-dependency-auditor`, the security-scan skill, and the `auditor-conventions` skill (extended in place — no parallel convention).
- Capability boundaries already established in this repo apply per side: auditors hold no shell grant; dependency vulnerability evidence must be supplied offline (its absence is NOT RUN, never a pass); graph unavailability is NOT RUN with a reason. A dimension NOT RUN on one side must be reported as asymmetric evidence for that pair — never presented as a delta.
- The value-story mode per pair (pure modernization vs. modernized-and-improved) is an input to the synthesizer and narrative agents. If the engagement-configuration schema lacks a mode field, add it there as a small backward-compatible extension — no side channel.
- All new agents/skills live in `source_of_truth/` and propagate via `scripts/propagate_master_assets.py` to a fixed point; never hand-edit `ports/` or `.github/`.

## Dependencies & Risks

- **Dependency**: `engagement-prepare` and the engagement-configuration skill (Phase 01, complete). Entry state is verified at run time; the orchestrator reports exactly which side is unprepared.
- **Risk**: orchestrator context blowout — 4 audit dimensions × 2 sides × N pairs plus document generation. Mitigation: everything runs in child agents returning compact summaries and pointers; bulk content is discarded after its path is recorded.
- **Risk**: two independent scans describe the same issue differently, breaking pairing. Mitigation: slim convention fixes categories and severities; per-finding matching only for security; unmatched findings are explicit "new"/"resolved."
- **Risk**: introduced-issues report accuses the upgrade of problems the old scanner couldn't see. Mitigation: "new or newly-visible" labeling.
- **Risk**: engineer fixes make upgraded-side reports stale. Mitigation: documented fix → re-run one side (overwrite) → finalize flow.
- **Risk**: SOW exclusions ambiguous or SOW absent. Mitigation: absent → no routing, omission recorded; ambiguous → conservative routing into findings, flagged.
- **Risk**: intentional functional changes misread as regressions. Mitigation: value-story mode drives synthesizer and narrative framing.
- **Risk**: phase is large. Mitigation: six independent feature bundles with clean seams (each bundle is a distinct agent set); the orchestrator's subagent contract is defined in bundle 1 and every later bundle plugs into it.

## Success Criteria

- [ ] A single engagement orchestrator exists in `source_of_truth/`, spawns `engagement-prepare` unchanged as its first step, and holds only compact per-pair results and pointers — no engagement file contents
- [ ] The client-code security boundary and analysis-branch invariants are stated once in the orchestrator and passed to every subagent
- [ ] For each configured pair, every audit dimension has a per-side raw report retained on disk in the agreed folder layout
- [ ] A full security report exists per side per pair as a standalone retained artifact
- [ ] The client-facing security narrative exists per pair with all four sections; every original-side security risk is classified as repaired (SOW-attached), out-of-scope, or residual, with no finding silently dropped
- [ ] Every residual risk carries a business-consequence statement first and only a brief plain-language mechanism note
- [ ] The introduced-issues report exists per pair, is labeled internal/engineer-facing, distinguishes "new" from "new or newly-visible," and gives file-level technical detail
- [ ] Re-running one side's scans without redoing the pair is supported and refreshes downstream artifacts
- [ ] A per-pair delta document classifies categories as resolved/improved/unchanged/new, leads with business meaning, and includes a headline-metrics table
- [ ] Findings matching the SOW's exclusions land in the severity-rated out-of-scope register; its security rows cross-reference the security narrative; no-SOW runs record the missing input
- [ ] A dimension NOT RUN on one side is reported as asymmetric evidence, never as a delta
- [ ] Narrative/spec docs and before/after workflow narratives exist per pair, correct for the pair's value-story mode
- [ ] Operational docs (publishing, prerequisites, maintenance, known limitations) exist per delivered component
- [ ] The SOW compliance walkthrough cites evidence per acceptance criterion read from the SOW document; the verification summary and functional-preservation statement exist
- [ ] Package items are labeled SOW-required vs. above-contract
- [ ] The assembled package renders branded PDFs from the markdown artifacts; the client-perspective gap review runs against the assembled package
- [ ] No engagement repository source code is modified by any agent
- [ ] New/extended agents and skills exist only in `source_of_truth/` with propagation run to a fixed point

## QA Considerations

- No frontend/UI changes — no manual QA docs required.
- Verification is artifact-based: run the orchestrator against a prepared pair; check security per-finding matching on a one-sided finding; exercise the no-SOW routing path; verify "new vs. newly-visible" labeling; verify synthesizer and narrative output for both value-story modes; exercise a one-side re-run; run with one unprepared side to confirm the specific failure report; render a PDF from a sample markdown set.

## Notes for Feature - Decomposer

Suggested feature boundaries (6) — each is a distinct agent/skill bundle:

1. **Orchestrator core** — the slim per-pair loop agent: engagement-config consumption, `engagement-prepare` spawn, run-time entry checks, the compact-handoff subagent contract, inherited security boundary. Every later bundle plugs into this contract; define it here once.
2. **Comparative audits** — the `auditor-conventions` extension (categories, severity scale, security per-finding identifiers) plus the scan-run subagent(s) that run each existing auditor on both sides into the folder layout, with one-side re-run support.
3. **Delta & security** — delta synthesizer, SOW exclusions routing + out-of-scope register, four-section security narrative, internal introduced-issues report, audit-trail proof, cloud/cost observations. All consume the retained per-side reports.
4. **Narrative & spec docs** — business design doc, intended-behavior spec, before/after workflow narratives, value-story-mode aware.
5. **Operational docs** — publishing/install, prerequisites, maintenance, known-limitations agents.
6. **Compliance & assembly** — SOW walkthrough, verification summary, contract-vs-above-contract labeling, branded PDF assembly (template asset creation), client-perspective gap review.

Hard constraints for every feature's AC: agents never modify engagement repo source; comparison is report-vs-report, never git-diff; raw agent outputs are retained and cited by all synthesized documents; client-facing docs lead with business language, technical appendices behind; the introduced-issues report is never client-facing; compact orchestrator handoffs (summaries + pointers only); `engagement-prepare` is not modified; `source_of_truth/` is the only authoring surface with propagation to a fixed point.

**Brevity constraint on authored agent and skill definitions**: the agent and skill files this phase writes to `source_of_truth/` are loaded into model context at runtime — every unnecessary word is wasted context. Definitions must be terse: state the behavior, the constraints, and the output contract once each, and stop. No restating context the agent already has, no motivational preamble, no repeating a rule in different words, no exhaustive examples where one suffices. Carry this into every feature's AC: a definition that says the same thing twice fails review.
