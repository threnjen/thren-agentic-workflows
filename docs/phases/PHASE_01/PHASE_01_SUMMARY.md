# Phase 1: Engagement Preparation & Baselines

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md` (pilot engagement context, source documents)

## What's New

Before any comparison or audit document can be produced for a client deliverable package, every comparison side must be prepared from the repository branch or ref the user has supplied. This phase adds the engagement entry point: the user declares the comparison pairs, confirms that the displayed sides and roles are intentional, and the orchestrator creates an analysis branch for each side, runs `docs-writer` there, builds a code-review graph, and records compact internal baseline results.

## Objective

Give the tool a confirmed, repeatable starting state for any engagement: user-declared comparison pairs, analysis branches prepared from those checkouts, documentation and graphs produced per side, and internal baseline results ready for downstream phases.

## Scope

### In Scope

- **Engagement configuration**: a schema/convention by which the user declares the engagement's comparison pairs. Each pair is either (original repo, upgraded repo) or (branch A, branch B) of a single repo. Any number of pairs. The configuration supplies paths to checkouts already on the branches or refs to compare, roles (original/upgraded side), and optional pointers to the SOW and deliverables-spec documents.
- **Preparation preflight and confirmation**: inspect the declared paths and current branches/refs, display each pair and side with its role, and ask the user to confirm that the planned comparison is correct before any analysis branch is created.
- **Analysis branches and documentation preparation**: create a new analysis branch from each confirmed comparison side, then always run the existing `docs-writer` agent on that analysis branch. `docs-writer` determines which applicable repository documents to create or update.
- **Graph preparation**: change into each analysis-branch checkout and run `code-review-graph build`; record the compact result and where the graph and related artifacts live.
- **Optional source-document check**: check whether the configured SOW, deliverables spec, and other recommended source documents are present. Missing documents are reported to the user for confirmation before preparation continues; they are not treated as an automatic failure, and the omission is recorded for downstream phases.
- **Internal baseline snapshot** (explicitly *not* client-facing): per side of each pair, a compact record of the confirmed source branch/ref, analysis branch, documentation result, graph result, graph stats, and language coverage. Pipeline input for Phase 2; no client document is generated from it.
- **Preparation runbook**: the whole procedure captured as a repeatable `source_of_truth/` asset for future engagements.

### Out of Scope

- Any comparison, audit, or delta document (Phase 2)
- Any client-facing document content — baseline results are internal only; client-facing figures come from later phases
- Modifying source code in any engagement repo — generated documentation on an analysis branch is the only intended repository write
- Quality gates on documentation or graph coverage — whatever `docs-writer` and the graph produce is accepted; coverage gaps are recorded as-is
- User-facing usage documentation (produced outside this tool)

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Engagement configuration schema | How the user declares pairs, paths, roles, and optional source-document pointers | config convention |
| 2 | Preparation preflight and confirmation | Display of the configured sides, branches/refs, and roles with explicit user confirmation before preparation | preflight, confirmation |
| 3 | Source-document presence check | Compact inventory of recommended source documents, with a confirmation prompt when items are missing | source-document check |
| 4 | Analysis branches and documentation preparation | New analysis branch per confirmed side and an unconditional `docs-writer` pass on that branch | branch preparation, docs-writer integration |
| 5 | Graph builds and internal baseline snapshot | Per-side graph build, graph stats/language coverage, and compact internal handoff record | graph builds, baseline capture |
| 6 | Preparation runbook | Repeatable procedure in `source_of_truth/` | runbook authoring |

## Technical Context

- Reused, not rebuilt: the existing `docs-writer` agent and the `code-review-graph` MCP/server tooling. The orchestrator establishes the analysis branch and working directory before invoking `docs-writer`; the existing agent decides which documentation is applicable.
- Graph building is parse-based (Tree-sitter), not compile-based — original/legacy repos do not need to build to be graphed. The orchestrator runs `code-review-graph build` from the intended analysis-branch directory and records the result and any reported coverage gaps.
- The user supplies the comparison checkouts and confirms the displayed pairings; Phase 01 does not infer branch intent from repository history or external workflow state.
- Any new agent or skill definitions belong in `source_of_truth/agents/` / `source_of_truth/skills/`, propagated via `scripts/propagate_master_assets.py` — never hand-edit `ports/` or `.github/`. Run propagation to a fixed point (re-run until change counters are zero).
- Pilot engagement specifics (repo identities, pairings, stack) are in `docs/phases/DISCOVERY_CONTEXT.md` — phase assets stay engagement-agnostic and read pairings from the engagement configuration.

## Dependencies & Risks

- **Dependency**: local access to every declared repo/branch and user confirmation of the displayed comparison plan. Mitigation: show all sides, roles, and branches/refs before creating analysis branches.
- **Risk**: the user confirms an incomplete or incorrect pairing. Mitigation: make the preflight inventory explicit and require confirmation before preparation starts; downstream artifacts retain the confirmed mapping.
- **Risk**: recommended source documents are missing. Mitigation: report the missing items, ask the user whether to continue, and record the omission for downstream phases rather than silently proceeding.
- **Risk**: repository state contamination. Mitigation: generated documentation is written on analysis branches created from the confirmed comparison sides; comparison branches remain the source inputs.
- **Risk**: graph command or `docs-writer` failure on one side. Mitigation: stop and report the exact side, command/agent, and failure result so the user can correct the input or environment.
- **Risk**: many pairs make the orchestrator's context too large. Mitigation: return compact per-side results and artifact pointers rather than full repository analysis.

## Success Criteria

- [ ] Engagement configuration supports N comparison pairs and records each side's path, branch/ref, role, and optional source-document pointers
- [ ] Before preparation, the orchestrator displays the configured pairings and receives explicit user confirmation that the branches/refs and original/upgraded roles are intended
- [ ] For every confirmed side, the orchestrator creates an analysis branch and always runs `docs-writer` on that branch
- [ ] For every confirmed side, the orchestrator runs `code-review-graph build` from the analysis-branch directory and records the result, graph stats, and language coverage
- [ ] When recommended source documents are missing, the orchestrator reports them and obtains confirmation before continuing; the missing items remain visible in the internal result
- [ ] Internal baseline snapshot exists per side, records the confirmed comparison source and analysis artifacts, and is labeled not-client-facing
- [ ] Comparison branches are not modified and no product source code is changed
- [ ] Preparation runbook exists in `source_of_truth/` and has been validated by an actual run on the pilot engagement

## QA Considerations

- No frontend/UI changes — no manual QA docs required.
- Verification is artifact- and interaction-based: run the orchestrator against the pilot engagement, confirm the pairing review step, exercise the missing-source-document confirmation path, verify the analysis branches contain the documentation output, verify graph-build results for every side, and run with a deliberately bad path or branch to confirm the specific failure report.

## Notes for Feature - Decomposer

Suggested feature boundaries (6):

1. **Engagement configuration** — pair declaration, side paths, branch/ref display, roles, and optional source-document pointers.
2. **Preparation preflight and user confirmation** — resolve the declared sides, present the full comparison plan, and pause until the user confirms it.
3. **Optional source-document presence check** — inventory recommended documents, prompt when any are absent, and pass the confirmed result downstream.
4. **Analysis branches and `docs-writer` integration** — create an analysis branch from each confirmed side and always run `docs-writer` on that branch.
5. **Graph builds and baseline capture** — run `code-review-graph build` in each analysis-branch directory and record compact internal results.
6. **Preparation runbook authoring** — capture the repeatable procedure as a `source_of_truth/` asset after the preparation flow has been exercised.

Hard constraints for every feature's acceptance criteria: the user confirms the comparison plan before preparation; `docs-writer` runs on the analysis branch for every side; the graph build runs from each analysis-branch directory; optional source documents may be missing only after explicit user confirmation; and client-facing documents remain out of scope.
