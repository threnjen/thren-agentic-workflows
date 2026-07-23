# Project Roadmap: Client Deliverable Package (Agent Set)

## Vision

A reusable agent set that produces a branded, PDF-assembled client deliverable package for modernization/upgrade engagements — comparative audits between original and upgraded repos, plain-language narrative documents, operational documentation, SOW compliance proof, and a self-reviewed final package that lets a non-technical client close the contract with confidence.

## Inputs (per engagement)

The tool is parameterized by:

- **Comparison pairs**: one or more pairs, each either (original repo, upgraded repo) as separate repositories or (branch A, branch B) of a single repository — any number of pairs, declared by the user in an engagement configuration
- **Repository access**: local checkouts of every declared repo/branch — the tool presents the configured sides for user confirmation, then prepares them itself (analysis branch, docs-writer pass, and code-review-graph build per side)
- **SOW / contract document**: authoritative scope, deliverables, exclusions, and acceptance criteria
- **Deliverables spec**: the internal list of package items promised to the client
- **Branding template asset**: cover, logo, colors for PDF rendering

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Engagement Preparation & Baselines | Complete | None | Medium | User-confirmed comparison pairs and a prepare-or-verify orchestrator (`engagement-prepare`) that creates an analysis branch per side, always runs docs-writer there, builds the code-review-graph, checks optional source documents, and records compact internal-only baseline results |
| 02 | Engagement Orchestrator & Deliverable Agent Set | Complete | Phase 01 | Large | A single slim engagement orchestrator that owns the per-pair loop, keeps an on-disk working state, and spawns everything as subagents (including `engagement-prepare` as its first step, reused unchanged). Feature bundles: orchestrator core; comparative audit runs with retained raw reports; delta synthesis with SOW-exclusion routing, client-facing security narrative, internal introduced-issues report, audit-trail proof, and pricing-researched cloud/cost analysis; narrative/spec docs; SOW compliance proof plus a schema-defined two-section package manifest and client-perspective gap review. Output is markdown + manifest; PDF assembly happens outside the tool |
| 03 | Operational & Publishing Docs Agent | Planned | Phase 01 | Small | A standalone agent (outside the engagement orchestrator) that produces per-component operational documentation: publishing/installation, prerequisites/system requirements, maintenance guidance, and known-limitations disclaimers |

## Constraints & Non-Goals

- **Audience is non-technical** — every client-facing document leads with business meaning; technical evidence goes to appendices.
- **Cross-repo comparison, not git diff**: original and upgraded repos have separate histories; the comparison engine must not assume a shared history.
- **Two value-story modes per repo pair**: "modernized, nothing changed" (pure upgrade) vs. "modernized and improved" (upgrade plus functional changes). The narrative agents must support both.
- **Contractual minimum vs. above-contract value**: the tool distinguishes SOW-required documents from the above-contract package items, and says so — exceeding the contract visibly is the point.
- **Delivery target is the client's own repo, but the tool never writes there** — all engagement outputs land in a single per-engagement workspace directory outside every client repository; the user assembles branded PDFs outside the tool (Claude Design) from the package manifest and copies the client-facing set into the client repo as the final manual step. Markdown is the durable artifact.
- **Non-goal**: user-facing usage documentation (screens/workflows) — produced outside this tool.
- **Non-goal**: remediation of findings. Audit agents report; fixing pre-existing defects is out of scope (the internal introduced-issues report exists so a human engineer fixes).
- **Agent definitions live in `source_of_truth/agents/`** per this repo's source-of-truth boundary; downstream ports are regenerated, never hand-edited.
- **Terse definitions**: agent and skill files are loaded into model context at runtime; every definition states behavior, constraints, and output contract once each and stops.

## Architecture Notes

- **One orchestrator**: a single slim engagement orchestrator owns the engagement config, the per-pair loop, and compact result pointers — nothing else. Every unit of real work (preparing a side, scanning, synthesizing, writing a client doc, assembling) runs in a subagent that returns a compact summary plus file pointers. New subagents are preferred over exception-laden extensions of existing ones.
- **`engagement-prepare` is a subagent** of the orchestrator — its first per-engagement step, reused unchanged from Phase 01. Prerequisite infrastructure per side (docs-writer documentation set + built code-review-graph, on never-pushed analysis branches) is its responsibility.
- **Comparative pattern**: run the same scan agent on the original and upgraded side, then a delta-synthesizer agent turns paired reports into a business-framed before/after document with a headline-metrics table. This one pattern feeds the delta document (the findings report), its out-of-scope-under-the-SOW section, and the audit-trail-of-our-own-work proof.
- **The SOW's acceptance criteria and test lists are the skeletons** for the compliance walkthrough and verification summary — agents read them from the engagement's SOW document, not from hardcoded lists.
- **The SOW's exclusions section routes audit findings** by dimension: security exclusions into the security narrative's out-of-scope section, all others into the delta document's out-of-scope-under-the-SOW section.
- **Package output is markdown + manifest**: a schema-defined package manifest (client-facing and technical sections, each an ordered table of contents with SOW-required vs. above-contract labels and present/missing detection) indexes the deliverable set. Branded PDF assembly happens outside the tool, in Claude Design, from the manifest and markdown files.
- **Client-code security boundary**: engagement repo contents never leave local disk and are data to analyze, never instructions to follow; the orchestrator passes this rule to every subagent. The pricing-researcher subagent is the sole internet-touching exception, restricted to generic service-name/pricing queries containing no engagement content.

## Pilot Engagement

The first engagement this tool will run against is documented in `DISCOVERY_CONTEXT.md` (four repos — two pairs — plus SOW and internal deliverables spec). Phase documents stay engagement-agnostic; engagement specifics live only in the discovery context.

The pilot-validation run is **not a project deliverable** (removed by user direction, 2026-07-22): no phase's completion is gated on a validation run against the pilot engagement, and pilot-run obligations formerly attached to Phase 01 (including `[PROPOSED]` marker resolution) are not treated as unmet gates by downstream phases. The pilot remains the first intended target engagement.
