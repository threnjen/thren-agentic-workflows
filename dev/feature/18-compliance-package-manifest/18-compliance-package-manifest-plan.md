# Plan: 18-compliance-package-manifest

## Execution Metadata

- **Wave:** 5
- **Parallel safe:** no
- **Depends on:** 14-engagement-orchestrator-core, 15-comparative-audit-runs, 16-delta-security-synthesis, 17-narrative-spec-docs
- **Key files modified:** `source_of_truth/agents/engagement-compliance-writer.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-gap-reviewer.agent.md` [PROPOSED - name TBD], `source_of_truth/skills/engagement-package-manifest/SKILL.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] (roster + final loop steps), `source_of_truth/agents/README.md`, `docs/CODEBASE_CONTEXT.md` (verify — counts), `tests/test_propagate_master_assets.py` (verify — marker-guard counts)
- **Sequential reason:** shares the orchestrator agent file with all upstream features; the manifest schema and gap review index every document the earlier features define — this is the phase's integration/bootstrap feature

Phase document: `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` (Key Deliverable 7, bundle 5).

## A. Requirements & Traceability

Acceptance criteria:

- **AC1 (SOW compliance walkthrough)**: Per engagement, acceptance criteria and test lists are read from the engagement's SOW document (never hardcoded); each criterion is walked through with evidence cited from the retained artifacts.
- **AC2 (verification summary)**: The contractual deliverable exists and contains the functional-preservation statement, referencing 17's intended-behavior spec.
- **AC3 (package manifest)**: A schema-defined markdown index of the deliverable set in two sections — **client-facing** and **technical/internal** — each an ordered table of contents. The schema fixes expected entries per section given the engagement's pairs and modes; each row carries document name, path, audience, SOW-required vs. above-contract status, and present/missing status, so an incomplete package is mechanically detectable. The technical section includes the raw reports, introduced-issues report, gap-review report, orchestrator working-state/run record, and Phase 01 baseline snapshots. All paths resolve within the single workspace root (14's AC4).
- **AC4 (gap review)**: A client-perspective gap reviewer answers "what would the client still ask?" against the complete markdown set, using the manifest as its completeness checklist. It **always emits an internal report document**, itself a standing manifest entry in the technical section.
- **AC5 (integration)**: The orchestrator's per-engagement loop now runs end to end — prepare → comparative audits → delta/security synthesis → narrative docs → compliance → manifest → gap review — with every step under the compact-handoff contract and every output in the workspace layout. This is the phase's runnable-whole check.
- **AC6 (reconciliation)**: Catalog and count surfaces are reconciled for **all** Phase 02 agents/skills: `source_of_truth/agents/README.md` catalog entries, `docs/CODEBASE_CONTEXT.md` count claims, and any remaining marker-guard counts in `tests/test_propagate_master_assets.py`. Earlier features' reviews must not be relied on to have fixed these; this feature verifies all landed (Phase 01 feature-13 pattern).
- **AC7**: `source_of_truth/` only; propagation to fixed point; full suite shows no new failures vs. baseline — this is the phase-final clean-tree gate.
- **AC8 (brevity)**: definitions and the manifest schema state each rule once.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC2 | compliance-writer agent [PROPOSED - name TBD] | Code-review evidence (SOW-read requirement; preservation statement referencing the spec) |
| AC3 | `engagement-package-manifest` skill [PROPOSED - name TBD] | Code-review evidence (schema completeness vs. every document defined in 14–17) |
| AC4 | gap-reviewer agent [PROPOSED - name TBD] | Code-review evidence (always-emit rule; manifest-as-checklist) |
| AC5 | orchestrator agent file | Code-review evidence; manual QA end-to-end run (phase-level) |
| AC6 | `source_of_truth/agents/README.md`, `docs/CODEBASE_CONTEXT.md`, `tests/test_propagate_master_assets.py:768-769` | Existing automated count/derivation guards; code-review |
| AC7 | `ports/`, `.github/` | Existing automated suite |

Non-goals: PDF assembly and branding (user assembles in Claude Design); quality gates on scan/docs coverage (gaps recorded, not blocking); remediation; operational docs (Phase 03).

## B. Correctness & Edge Cases

- No SOW configured → compliance walkthrough records the missing input honestly (consistent with 16's AC2 path); SOW-required labels in the manifest fall back to a recorded "no SOW" state, not silently to above-contract.
- Deliberately missing document → manifest row reads missing; gap review flags it (this is the phase's mechanically-detectable-incompleteness QA check).
- Gap review with nothing to report → the internal report is still emitted (empty-state honest content), per AC4's always-emit rule.
- Multi-pair engagements → schema expands expected entries per pair; single-pair is not assumed.
- Dimension NOT RUN upstream → compliance evidence citing it says NOT RUN/NOT VERIFIED, never a pass (standing review contract).

## C. Consistency & Architecture Fit

- Manifest schema lives in a skill (like the workspace layout) so the manifest-writing step and the gap reviewer both load one definition.
- Expected-entry lists must be **derived from the schema given pairs and modes**, not hand-enumerated per engagement (enumeration-gap lesson: close gaps by derivation).
- The audit-trail proof (16) is grouped with the compliance materials in the client-facing section ordering.
- Grants: read/search/edit-class only for both new agents.
- Document names from 14–17 are consumed here; any still-`[PROPOSED]` names must be resolved to the implemented names before the schema is final.

## D. Clean Design & Maintainability

Simplest design: one skill (schema) + two agents + final orchestrator loop paragraphs. Keep-it-clean: present/missing detection logic stated once in the schema; the gap reviewer consumes the manifest rather than re-deriving expectations.

## E. Observability, Security, Operability

- Observability: the manifest plus working-state file are the engagement's complete run record; the gap-review report is the standing self-review artifact. No new logging.
- Security: manifest and gap review are workspace-internal until the user copies the client-facing set out; the introduced-issues report stays technical-section only.
- Runbook: propagate to fixed point → full `uv run pytest tests/` → deploy on request; phase-final state must be commit-clean.

## F. Test Plan

- Must-have automated: existing propagation/sync/count suites all green after reconciliation (AC6, AC7).
- Existing tests to update: marker-guard counts (verify); any count-derivation guard touched by README/CODEBASE_CONTEXT claims (verify).
- Code-review evidence: AC1–AC5, AC8 — especially schema coverage of every document contract from 14–17.
- Manual QA: phase-level — full orchestrator run against a prepared pair; manifest flags a deliberately missing document; gap-review report present in the technical section (see execution manifest).

Top evidence checks:
1. Given the manifest schema and the document contracts of 14–17, when cross-checked, then every produced document has exactly one expected-entry rule and every technical-section standing entry (raw reports, introduced-issues, gap review, working state, Phase 01 snapshots) is present.
2. Given a missing document, when the manifest instructions are walked, then the row reads missing and nothing suppresses it.
3. Given the compliance-writer definition, when reviewed, then acceptance criteria come only from the SOW document and each cited evidence artifact is a retained on-disk report.
4. Given the gap-reviewer definition, when reviewed, then the internal report is emitted unconditionally.
5. Given the final tree, when propagation runs twice and the full suite runs, then zero changes and no new failures.

## Stage 1: Manifest Schema Skill
**Goal**: `engagement-package-manifest` skill [PROPOSED - name TBD] — two-section schema, row fields, expected-entry derivation, present/missing detection
**Success Criteria**: AC3, AC8
**Status**: Not Started

## Stage 2: Compliance Writer + Gap Reviewer
**Goal**: the two agents (SOW walkthrough + verification summary; client-perspective gap review with always-emitted report)
**Success Criteria**: AC1, AC2, AC4
**Status**: Not Started

## Stage 3: Final Orchestrator Wiring (Integration)
**Goal**: complete end-to-end loop; every bundle's step present in order
**Success Criteria**: AC5
**Status**: Not Started

## Stage 4: Reconciliation, Propagate & Verify
**Goal**: README catalog, CODEBASE_CONTEXT counts, test count guards; fixed point; full suite green
**Success Criteria**: AC6, AC7
**Status**: Not Started

## Relationship Notes

Consumes every upstream feature: 14 (workspace root, working state), 15 (raw reports), 16 (delta/security docs incl. audit-trail grouping and introduced-issues technical entry), 17 (spec referenced by the verification summary). This is the integration feature: its AC5 is the check that the features operate together as one engagement run.
