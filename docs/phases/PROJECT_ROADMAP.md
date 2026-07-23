# Project Roadmap: Client Deliverable Package (Agent Set)

## Vision

A reusable agent set that produces a branded, PDF-assembled client deliverable package for modernization/upgrade engagements — comparative audits between original and upgraded repos, plain-language narrative documents, operational documentation, SOW compliance proof, and a self-reviewed final package that lets a non-technical client close the contract with confidence.

## Inputs (per engagement)

The tool is parameterized by:

- **Repo pairs**: one or more (original repo, upgraded repo) pairs, kept as separate repositories with separate histories
- **SOW / contract document**: authoritative scope, deliverables, exclusions, and acceptance criteria
- **Deliverables spec**: the internal list of package items promised to the client
- **Branding template asset**: cover, logo, colors for PDF rendering

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Repo Preparation & Baselines | Planned | None | Medium | Prerequisite pass over every engagement repo: docs-writer documentation set, code-review-graph builds, and baseline verification so downstream comparison agents have uniform inputs |
| 02 | Comparative Audit Engine | Planned | Phase 01 | Large | Dual-repo scan agents (security, code quality, dependencies) plus a delta synthesizer producing plain-language before/after reports; feeds findings report, out-of-scope register, and audit-trail proof |
| 03 | Narrative & Specification Docs | Planned | Phase 02 | Medium | Business design doc, specification of intended behavior ("warranty" baseline), and before/after workflow narratives for components with functional changes |
| 04 | Operational & Publishing Docs | Planned | Phase 01 | Medium | Publishing/installation docs per component, prerequisites/system requirements, maintenance guidance, known-limitations disclaimers |
| 05 | Compliance & Verification Proof | Planned | Phase 03, 04 | Medium | SOW acceptance-criteria walkthrough with evidence, verification summary (the contractual deliverable), functional-preservation statement |
| 06 | Assembly & Self-Review | Planned | Phase 02–05 | Medium | Branded markdown→PDF assembler (template asset created here unless one is supplied) and a client-perspective gap reviewer that answers "what would the client still ask?" |

## Constraints & Non-Goals

- **Audience is non-technical** — every client-facing document leads with business meaning; technical evidence goes to appendices.
- **Cross-repo comparison, not git diff**: original and upgraded repos have separate histories; the comparison engine must not assume a shared history.
- **Two value-story modes per repo pair**: "modernized, nothing changed" (pure upgrade) vs. "modernized and improved" (upgrade plus functional changes). The narrative agents must support both.
- **Contractual minimum vs. above-contract value**: the tool distinguishes SOW-required documents from the above-contract package items, and says so — exceeding the contract visibly is the point.
- **Delivery target is the client's own repo** — markdown is the durable artifact; branded PDFs render on top.
- **Non-goal**: user-facing usage documentation (screens/workflows) — produced outside this tool.
- **Non-goal**: remediation of findings. Audit agents report; fixing pre-existing defects is out of scope.
- **Agent definitions live in `source_of_truth/agents/`** per this repo's source-of-truth boundary; downstream ports are regenerated, never hand-edited.

## Architecture Notes

- **Comparative pattern**: run the same scan agent on the original repo and the upgraded repo, then a delta-synthesizer agent turns paired reports into a business-framed before/after document with a headline-metrics table. This one pattern feeds the findings report, the out-of-scope register, and the audit-trail-of-our-own-work proof.
- **Prerequisite infrastructure per repo** (Phase 01): docs-writer documentation set + built code-review-graph. Downstream agents consume graphs and docs instead of raw file scans.
- **The SOW's acceptance criteria and test lists are the skeletons** for the compliance walkthrough and verification summary — agents read them from the engagement's SOW document, not from hardcoded lists.
- **The SOW's exclusions section routes audit findings** into the severity-rated out-of-scope issues list.
- **PDF pipeline**: standardized in Phase 06 (pandoc-class markdown→PDF) plus a branding template asset (cover, logo, colors).

## Pilot Engagement

The first engagement this tool will run against is documented in `DISCOVERY_CONTEXT.md` (four repos — two pairs — plus SOW and internal deliverables spec). Phase documents stay engagement-agnostic; engagement specifics live only in the discovery context.
