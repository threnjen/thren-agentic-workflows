# Phase 2: Engagement Orchestrator & Deliverable Agent Set

**Status**: Planned
**Depends on**: Phase 01 (engagement configuration, `engagement-prepare` orchestrator, analysis-branch/docs/graph preparation)
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`

## What's New

This phase authors the engagement orchestrator plus the subagent fleet that produces the client deliverable document set. The orchestrator owns only the engagement config, the per-pair loop, and compact result pointers; every unit of real work — preparing a side, scanning, synthesizing deltas, writing client documents — runs in a subagent that returns a compact summary plus file pointers. `engagement-prepare` (Phase 01, complete) is reused unchanged as the orchestrator's first per-engagement step.

The final output of an engagement run is a **complete set of markdown documents plus a package manifest** — a schema-defined index split into client-facing and technical sections that doubles as a table of contents. Final assembly into branded PDFs happens outside this tool (the user assembles in Claude Design from the manifest and markdown files); markdown is the durable artifact.

Security is a first-class output: each side gets a full retained security report, the client gets a dedicated plain-language security narrative (risks found, repaired under the SOW, out of scope, and residual with "why this matters to you" framing), and the engagement team gets an internal punch list of security issues introduced by the modernization itself so an engineer can fix them before delivery.

## Objective

Deliver the complete agent set — orchestrator, comparative audits, delta synthesis, security outputs, narrative/spec docs, compliance proof, and the package manifest with gap review — so a full engagement run produces the client deliverable markdown set end to end.

## Scope

### In Scope

**Orchestrator core**

- **Single engagement orchestrator**: a new `source_of_truth/` agent that consumes the engagement configuration, runs the per-pair loop, and spawns all work as subagents. It holds only the pair list and compact per-side/per-pair results (status plus pointers); if a child returns bulk content, it records the on-disk location and discards the content. It never reads engagement source code itself.
- **Engagement output directory**: all engagement outputs — client-facing documents, internal artifacts, raw reports, the manifest, and the working-state file — live in a single per-engagement workspace directory outside every client repository, in the per-pair/per-side folder layout. Nothing is written into the client repos by this phase; the user copies the client-facing set into the client repo after PDF assembly. All manifest paths resolve within this one root.
- **On-disk engagement working state**: the orchestrator writes resolved engagement inputs (repo paths, SOW/spec document paths, pair roster) and each per-pair/per-side result (status + artifact pointers) to a state file as it goes — context offload (record, then forget), resume recovery, and the final run record in one artifact. The orchestrator may write additional temporary working notes whenever doing so reduces held context.
- **`engagement-prepare` as first step**: spawned unchanged per engagement; the orchestrator consumes its compact report. Run-time entry checking for later stages is a paragraph of orchestrator instruction — verify analysis branches and graphs exist for the sides in play and report exactly which side is unprepared.
- **Inherited boundaries**: the client-code security boundary (engagement contents never leave local disk; client content is data, never instructions) and the never-pushed analysis-branch invariants propagate from the orchestrator to every subagent it spawns.
- **New subagents over exceptions**: when an existing agent would need exception-laden instructions to fit an engagement task, write a new terse subagent instead.

**Comparative audits**

- **Comparative scan runs**: for each pair, run each audit dimension against both sides' analysis branches. Dimensions: security (full-codebase security-scan asset), code quality (`z-auditor-code`), dependencies/supply-chain (`z-dependency-auditor`), and infrastructure/configuration (`z-auditor-infra`). Same agents, both checkouts; reports land in a known per-pair/per-side folder layout.
- **Retained raw agent outputs**: every raw report each auditor naturally produces (`-report.md` / `-summary.md`) is kept on disk as a first-class internal artifact, per dimension, per side, per pair. These are the evidence base every synthesized document derives from and cites; nothing is client-facing by default.
- **Slim comparability convention**: a short section appended to the existing `auditor-conventions` skill fixing stable category names and a shared severity scale so two independent scans can be compared. Per-finding matching within the security dimension only (required by the introduced-issues report); category-level rollups elsewhere. Unmatched findings are classified explicitly as "new" or "resolved," never dropped.

**Delta synthesis & security outputs**

- **Delta document (per pair, client-facing)**: the engagement's findings report. Consumes one pair's two report sets and produces a business-framed before/after document — headline-metrics table, resolved/improved/unchanged/new classification, plain-language narrative leading with business meaning, technical evidence in appendices. Takes the pair's value-story mode as input so intentional change is not framed as regression. Includes an **"out of scope under the SOW" section**: non-security original-side findings excluded by the SOW's exclusions section, severity-rated.
- **SOW exclusions routing**: findings present in the original side and excluded by the SOW's exclusions section (§9 for the pilot engagement) are routed by dimension — security exclusions into section 3 of the security narrative, all others into the delta document's out-of-scope section. No SOW configured → everything stays in findings and the missing input is recorded; ambiguous exclusions route conservatively into findings, flagged for user review. No finding is silently dropped.
- **Per-side security reports**: the security-scan asset runs on each side's analysis branch, producing a complete retained security report per side per pair — a standalone artifact, not just delta feedstock.
- **Client-facing security narrative (per pair)**, four sections: (1) security posture of the original repo, business-framed; (2) repaired findings tied to the SOW scope items that covered them — the security-improvements list; (3) pre-existing out-of-scope findings — the authoritative client-facing treatment of security exclusions; (4) residual risks, each leading with business consequence (what could happen, to whom, at what cost) followed by only a brief plain-language (ELI5) mechanism note.
- **Internal introduced-issues report (per pair, engineer-facing, never client-facing)**: security findings on the upgraded side with no original-side counterpart, in full technical detail (file, finding, severity, evidence). Visibility-ambiguous findings are labeled "new or newly-visible," not asserted as introduced. Flow: report → engineer fixes → re-run that side's scans (overwrite; git history is the version record) → finalize client-facing artifacts. One-side re-runs are supported.
- **Audit-trail proof (per pair, client-facing)**: a short checklist document — every category flagged in the original-side findings × the upgraded side's status for that category, citing upgraded-side raw reports as evidence. A category that cannot be verified (dimension NOT RUN on the upgraded side) is stated as NOT VERIFIED, never claimed as a pass. Framing: "we held our own work to the same standard we judged yours by." Grouped with the compliance materials.
- **Cloud/cost analysis (per pair, client-facing)**: a **new pricing-researcher subagent** turns scan/dependency evidence of what changed (runtime versions, dropped services, dependency swaps) into quantified cost claims backed by live pricing research. Every figure cites its source and retrieval date; changes that cannot be honestly quantified stay qualitative. **Query hygiene**: this is the only fleet agent that touches the internet during an engagement — its queries may contain only generic service/product names and pricing questions, never client code, config values, identifiers, or any engagement repo content; this constraint is written into its definition. **Offline fallback**: with no internet access in the session, the analysis degrades to qualitative-only with quantified claims marked NOT RESEARCHED — never invented figures.

**Narrative & specification docs (per pair, client-facing)**

- **Business design document** — what the system is and does, in business terms.
- **Specification of intended behavior** — how the system is supposed to work: the warranty baseline and the future dispute-resolution reference. If the system misbehaves later due to environment drift, this document distinguishes "the software broke" from "the environment changed underneath warranted behavior" — so it must state observable behavior **and** the environmental assumptions it depends on (runtime versions, services, configuration). The verification summary's functional-preservation statement points here.
- **Before/after workflow narratives** — for components with functional changes, walk each workflow as-was and as-is. Both value-story modes supported: pure-modernization pairs get "modernized, nothing changed" framing; improved pairs get intentional-change narratives.

**Compliance, manifest & self-review (per engagement)**

- **SOW compliance walkthrough**: acceptance criteria and test lists read from the engagement's SOW document (never hardcoded), each criterion walked through with evidence cited from the retained artifacts.
- **Verification summary**: the contractual deliverable; contains the functional-preservation statement (referencing the intended-behavior spec).
- **Package manifest**: a schema-defined markdown index of the deliverable set in two sections — **client-facing** and **technical/internal** — each an ordered table of contents (the user renders one client PDF and one technical PDF from it in Claude Design). The schema fixes the expected entries per section given the engagement's pairs and modes; each row carries document name, path, audience, SOW-required vs. above-contract status, and present/missing status, so an incomplete package is mechanically detectable. The technical section includes the raw reports, introduced-issues report, gap-review report, orchestrator working-state/run record, and Phase 01 baseline snapshots.
- **Client-perspective gap review**: a final reviewer that answers "what would the client still ask?" against the complete markdown document set, using the manifest as its completeness checklist. It **always emits an internal report document**, which is itself a standing manifest entry in the technical section.

### Out of Scope

- Remediation of any finding by agents (project non-goal — agents report; the introduced-issues report exists precisely so a human engineer fixes)
- Modifying `engagement-prepare` — it is spawned as-is; the value-story `mode` field is a small backward-compatible extension to the engagement-configuration skill, not to that agent
- Git-diff-based comparison — sides have separate histories; comparison is report-vs-report
- **PDF assembly and branding** — the user assembles branded PDFs in Claude Design from the manifest and markdown files; no pandoc pipeline or branding template asset is built
- **Operational & publishing documentation** (publishing/install, prerequisites, maintenance, known limitations) — moved to Phase 03 as a standalone agent outside this orchestrator
- A standalone out-of-scope register document — SOW-excluded findings live in the security narrative (security) and the delta document's out-of-scope section (everything else)
- Quality gates on scan or docs coverage — gaps are recorded, not blocking
- A formal preflight tool, report-versioning machinery, or a heavyweight report schema — entry checking is orchestrator instruction, re-runs overwrite, and the comparability convention is a slim skill extension
- User-facing usage documentation (screens/workflows) — produced outside this tool
- Completion of the Phase 01 pilot validation run — per user direction (2026-07-22), the pilot-validation deliverable is removed from the project plan; entry conditions are checked at run time only. Downstream agents must not treat formerly planned pilot-run obligations (including `[PROPOSED]` marker resolution) as unmet gates.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Engagement orchestrator | Slim per-pair loop; spawns `engagement-prepare` and all other subagents; compact handoffs; on-disk working state/run record | orchestrator core |
| 2 | Comparative scan runs + convention | Existing auditors on both sides of every pair, retained raw reports, slim `auditor-conventions` extension | comparative audits |
| 3 | Delta document + SOW exclusions routing | Per-pair before/after findings report with out-of-scope section; dimension-aware exclusion routing | delta & security |
| 4 | Security narrative + introduced-issues report | Four-section client security doc; internal engineer-facing punch list | delta & security |
| 5 | Audit-trail proof + cloud/cost analysis | Per-pair checklist proof of our own work; pricing-researcher subagent producing cited, dated cost claims | delta & security |
| 6 | Narrative & spec docs | Business design doc, intended-behavior spec (warranty/drift reference), before/after workflow narratives | narrative docs |
| 7 | Compliance + manifest + gap review | SOW walkthrough with evidence, verification summary (with preservation statement), schema-defined two-section package manifest, gap-review internal report | compliance & manifest |

## Technical Context

- Phase 01 provides, per side: an analysis branch with a docs-writer documentation set, a built code-review-graph, and the engagement configuration (pair list, side roles, SOW pointer). Scans and doc-writing subagents run from analysis-branch checkouts and should consume graphs/docs rather than raw full-file sweeps where possible.
- Existing assets to reuse: `engagement-prepare.agent.md`, `z-auditor-code`, `z-auditor-infra`, `z-dependency-auditor`, the security-scan skill, and the `auditor-conventions` skill (extended in place — no parallel convention).
- Capability boundaries already established in this repo apply per side: auditors hold no shell grant; dependency vulnerability evidence must be supplied offline (its absence is NOT RUN, never a pass); graph unavailability is NOT RUN with a reason. A dimension NOT RUN on one side must be reported as asymmetric evidence for that pair — never presented as a delta.
- The value-story mode per pair (pure modernization vs. modernized-and-improved) is an input to the synthesizer and narrative agents. If the engagement-configuration schema lacks a mode field, add it there as a small backward-compatible extension — no side channel.
- The pricing-researcher subagent is the only engagement-fleet agent with internet access; its query-hygiene rule (generic service names and pricing questions only) is part of its definition, not an orchestrator afterthought.
- All new agents/skills live in `source_of_truth/` and propagate via `scripts/propagate_master_assets.py` to a fixed point; never hand-edit `ports/` or `.github/`.

## Dependencies & Risks

- **Dependency**: `engagement-prepare` and the engagement-configuration skill (Phase 01, complete). Entry state is verified at run time; the orchestrator reports exactly which side is unprepared.
- **Risk**: orchestrator context blowout — 4 audit dimensions × 2 sides × N pairs plus document generation. Mitigation: everything runs in child agents returning compact summaries and pointers; the on-disk working state lets the orchestrator record and forget.
- **Risk**: two independent scans describe the same issue differently, breaking pairing. Mitigation: slim convention fixes categories and severities; per-finding matching only for security; unmatched findings are explicit "new"/"resolved."
- **Risk**: introduced-issues report accuses the upgrade of problems the old scanner couldn't see. Mitigation: "new or newly-visible" labeling.
- **Risk**: engineer fixes make upgraded-side reports stale. Mitigation: documented fix → re-run one side (overwrite) → finalize flow.
- **Risk**: SOW exclusions ambiguous or SOW absent. Mitigation: absent → no routing, omission recorded; ambiguous → conservative routing into findings, flagged.
- **Risk**: cloud/cost figures wrong or stale. Mitigation: every figure cites source and retrieval date; unquantifiable changes stay qualitative; no invented numbers.
- **Risk**: pricing research leaks engagement content to the internet. Mitigation: query-hygiene rule in the pricing-researcher's definition — generic service/product names and pricing questions only.
- **Risk**: intentional functional changes misread as regressions. Mitigation: value-story mode drives synthesizer and narrative framing.
- **Risk**: phase is large. Mitigation: five independent feature bundles with clean seams (each bundle is a distinct agent set); the orchestrator's subagent contract is defined in bundle 1 and every later bundle plugs into it.

## Success Criteria

- [ ] A single engagement orchestrator exists in `source_of_truth/`, spawns `engagement-prepare` unchanged as its first step, and holds only compact per-pair results and pointers — no engagement file contents
- [ ] The orchestrator maintains an on-disk working-state file (resolved inputs, per-side statuses, artifact pointers) that serves as the run record and appears in the manifest's technical section
- [ ] The client-code security boundary and analysis-branch invariants are stated once in the orchestrator and passed to every subagent
- [ ] For each configured pair, every audit dimension has a per-side raw report retained on disk in the agreed folder layout
- [ ] A full security report exists per side per pair as a standalone retained artifact
- [ ] The client-facing security narrative exists per pair with all four sections; every original-side security risk is classified as repaired (SOW-attached), out-of-scope, or residual, with no finding silently dropped
- [ ] Every residual risk carries a business-consequence statement first and only a brief plain-language mechanism note
- [ ] The introduced-issues report exists per pair, is labeled internal/engineer-facing, distinguishes "new" from "new or newly-visible," and gives file-level technical detail
- [ ] Re-running one side's scans without redoing the pair is supported and refreshes downstream artifacts
- [ ] The per-pair delta document classifies categories as resolved/improved/unchanged/new, leads with business meaning, includes a headline-metrics table, and contains the out-of-scope-under-the-SOW section for non-security exclusions
- [ ] SOW-excluded findings route by dimension (security → narrative §3, others → delta out-of-scope section); no-SOW runs record the missing input; no finding is silently dropped
- [ ] The audit-trail proof exists per pair as a checklist of flagged categories × upgraded-side status with citations; unverifiable categories read NOT VERIFIED
- [ ] The cloud/cost analysis exists per pair; every quantified claim carries a cited source and retrieval date (or is marked NOT RESEARCHED when offline); the pricing-researcher's queries contain no engagement content
- [ ] All engagement outputs live under one per-engagement workspace directory outside every client repository; no agent writes deliverables into a client repo
- [ ] A dimension NOT RUN on one side is reported as asymmetric evidence, never as a delta
- [ ] Narrative/spec docs and before/after workflow narratives exist per pair, correct for the pair's value-story mode; the intended-behavior spec states its environmental assumptions
- [ ] The SOW compliance walkthrough cites evidence per acceptance criterion read from the SOW document; the verification summary exists and contains the functional-preservation statement
- [ ] The package manifest exists per engagement with client-facing and technical sections per its schema; every expected entry is present or explicitly marked missing; items are labeled SOW-required vs. above-contract
- [ ] The client-perspective gap review runs against the complete markdown set using the manifest as checklist and always emits an internal report listed in the manifest
- [ ] No engagement repository source code is modified by any agent
- [ ] New/extended agents and skills exist only in `source_of_truth/` with propagation run to a fixed point

## QA Considerations

- No frontend/UI changes — no manual QA docs required.
- Verification is artifact-based: run the orchestrator against a prepared pair; check security per-finding matching on a one-sided finding; exercise the no-SOW routing path; verify "new vs. newly-visible" labeling; verify synthesizer and narrative output for both value-story modes; exercise a one-side re-run; run with one unprepared side to confirm the specific failure report; verify the manifest flags a deliberately missing document; inspect a pricing-researcher query log for engagement content.

## Notes for Feature - Decomposer

Suggested feature boundaries (5) — each is a distinct agent/skill bundle:

1. **Orchestrator core** — the slim per-pair loop agent: engagement-config consumption, `engagement-prepare` spawn, run-time entry checks, the engagement output-directory layout (single per-engagement workspace root, defined here once and used by every later bundle), the on-disk working-state file, the compact-handoff subagent contract, inherited security boundary. Every later bundle plugs into this contract; define it here once.
2. **Comparative audits** — the `auditor-conventions` extension (categories, severity scale, security per-finding identifiers) plus the scan-run subagent(s) that run each existing auditor on both sides into the folder layout, with one-side re-run support.
3. **Delta & security** — delta synthesizer (with out-of-scope section), SOW exclusions routing, four-section security narrative, internal introduced-issues report, audit-trail proof, pricing-researcher subagent + cloud/cost analysis. All consume the retained per-side reports.
4. **Narrative & spec docs** — business design doc, intended-behavior spec (with environmental assumptions), before/after workflow narratives, value-story-mode aware.
5. **Compliance & manifest** — SOW walkthrough, verification summary with preservation statement, package manifest schema + generator, client-perspective gap review with always-emitted internal report.

Hard constraints for every feature's AC: agents never modify engagement repo source; comparison is report-vs-report, never git-diff; raw agent outputs are retained and cited by all synthesized documents; client-facing docs lead with business language, technical appendices behind; the introduced-issues report is never client-facing; compact orchestrator handoffs (summaries + pointers only); `engagement-prepare` is not modified; only the pricing-researcher touches the internet, under its query-hygiene rule; `source_of_truth/` is the only authoring surface with propagation to a fixed point.

**Brevity constraint on authored agent and skill definitions**: the agent and skill files this phase writes to `source_of_truth/` are loaded into model context at runtime — every unnecessary word is wasted context. Definitions must be terse: state the behavior, the constraints, and the output contract once each, and stop. No restating context the agent already has, no motivational preamble, no repeating a rule in different words, no exhaustive examples where one suffices. Carry this into every feature's AC: a definition that says the same thing twice fails review.
