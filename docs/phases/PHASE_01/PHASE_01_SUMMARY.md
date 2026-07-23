# Phase 1: Repo Preparation & Baselines

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md` (pilot engagement context, repo inventory, source documents)

## What's New

Before any comparison or audit document can be produced for a client deliverable package, every engagement repository (each original/upgraded pair) must be brought to a uniform, analyzable state. This phase runs the existing docs-writer agent over each repo to produce a complete documentation set, builds a code-review-graph for each repo, and verifies baselines — so every downstream agent works from graphs and docs rather than raw file scans, and comparisons are apples-to-apples.

## Objective

Establish identical analysis infrastructure (documentation set + knowledge graph + verified baseline) across all engagement repos so the Phase 2 comparative audit engine has uniform, trustworthy inputs — as a repeatable procedure, not a one-off.

## Scope

### In Scope

- Locate and record the local paths, roles, and pairing of the engagement repos in `DISCOVERY_CONTEXT.md` (pilot: two pairs, four repos)
- docs-writer pass on each repo: README, ARCHITECTURE, CODEBASE_CONTEXT, and (upgraded repos only) LOCAL_DEVELOPMENT and TROUBLESHOOTING
- code-review-graph build for each repo, with coverage verified (node/edge/file counts recorded, primary-language parsing confirmed)
- Baseline verification: confirm each repo is complete and scannable (original repos need not build; they must be readable and representative)
- A repo-preparation runbook agent or skill defining this prep as a repeatable procedure (runs again if repos change, and for future engagements)
- Record baseline metrics per repo (LOC, project count, dependency count, graph stats) — these become the "before" numbers in every downstream report

### Out of Scope

- Any comparison, audit, or delta document (Phase 2)
- Any client-facing document content
- Modifying source code in any engagement repo — this phase is strictly read-and-annotate
- User-facing usage documentation (produced outside this tool)

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Repo inventory record | Local paths, roles, and pairing of the engagement repos, recorded in `DISCOVERY_CONTEXT.md` | discovery/inventory |
| 2 | Documentation sets (per repo) | docs-writer output per repo (reduced set for original repos: README, ARCHITECTURE, CODEBASE_CONTEXT) | docs-writer orchestration |
| 3 | Knowledge graphs (per repo) | Built code-review-graph per repo with recorded stats and confirmed language coverage | graph builds, verification |
| 4 | Baseline metrics report | Per-repo metrics table (LOC, projects, dependencies, graph stats) — the canonical "before/after" input numbers | metrics collection |
| 5 | Repo-prep runbook | Repeatable procedure (agent or skill in `source_of_truth/`) for re-running prep when repos change or a new engagement starts | agent/skill authoring |

## Technical Context

- Existing agents to reuse, not rebuild: `docs-writer` (README/ARCHITECTURE/CODEBASE_CONTEXT/LOCAL_DEVELOPMENT/TROUBLESHOOTING) and the `code-review-graph` MCP server (`build_or_update_graph_tool`, `list_graph_stats_tool`, `list_repos_tool` for multi-repo support).
- Any new agent or skill definitions belong in `source_of_truth/agents/` / `source_of_truth/skills/`, propagated via `scripts/propagate_master_assets.py` — never hand-edit `ports/` or `.github/`.
- Graph building is parse-based (Tree-sitter), not compile-based — original repos on legacy frameworks do not need to build to be graphed. Verify graph language coverage for each engagement's stack and record any gaps (e.g., config files, secondary languages) as known limitations.
- The original repos represent the pre-engagement state and must not be modified; if docs-writer output cannot be committed into them, write their docs to a sibling analysis directory and record the location in `DISCOVERY_CONTEXT.md`.
- Pilot engagement specifics (repo identities, stack: C#/.NET plus JavaScript front-end assets) are in `DISCOVERY_CONTEXT.md`.

## Dependencies & Risks

- **Dependency**: local access to all engagement repos (pilot paths currently unrecorded — first task).
- **Risk**: original repos may not restore/build cleanly with modern tooling. Mitigation: prep requires readability, not buildability.
- **Risk**: docs-writer output for the original repos could be mistaken for deliverable content. Mitigation: mark original-repo docs as internal analysis artifacts; they exist to feed the audit engine, not the client package.
- **Risk**: graph coverage gaps could silently weaken later comparisons. Mitigation: deliverable 3 explicitly records coverage stats and gaps; Phase 2 agents fall back to file scans where the graph is thin.

## Success Criteria

- [ ] All engagement repo paths recorded in `DISCOVERY_CONTEXT.md` with role and pairing
- [ ] Each repo has a docs-writer documentation set (full set for upgraded repos; README/ARCHITECTURE/CODEBASE_CONTEXT minimum for original repos)
- [ ] Each repo has a built code-review-graph with recorded node/edge/file counts and confirmed primary-language coverage
- [ ] Baseline metrics table exists covering all engagement repos with consistent metric definitions
- [ ] Repo-prep runbook exists in `source_of_truth/` and has been validated by the actual prep run on the pilot engagement
- [ ] No source file in any engagement repo was modified

## QA Considerations

- No frontend/UI changes — no manual QA docs required.
- Verification is artifact-based: spot-check docs accuracy against each repo, and confirm graph stats are sane (non-zero nodes/edges, file count near repo file count).

## Notes for Feature - Decomposer

Suggested feature boundaries (4):

1. **Repo inventory & baseline verification** — locate repos, confirm readability/representativeness, record pairing and metrics definitions.
2. **Documentation pass orchestration** — run docs-writer across the engagement repos with per-repo scope (full vs. reduced set), handling the original-repo write-location decision.
3. **Graph builds & coverage verification** — build all graphs, record stats, document coverage gaps.
4. **Repo-prep runbook authoring** — capture the whole procedure as a repeatable `source_of_truth/` asset, informed by what features 1–3 actually encountered.

Features 2 and 3 are independent of each other but both depend on 1; feature 4 comes last. Keep the original-repo immutability constraint explicit in every feature's acceptance criteria.
