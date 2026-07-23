# Context: 18-compliance-package-manifest

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/skills/engagement-package-manifest/SKILL.md` [PROPOSED - name TBD] | Two-section manifest schema: row fields, expected-entry derivation, present/missing detection | Create |
| `source_of_truth/agents/engagement-compliance-writer.agent.md` [PROPOSED - name TBD] | SOW compliance walkthrough + verification summary with preservation statement | Create |
| `source_of_truth/agents/engagement-gap-reviewer.agent.md` [PROPOSED - name TBD] | Client-perspective gap review; always-emit internal report | Create |
| `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] | Roster + final loop steps (compliance → manifest → gap review); created by feature 14, extended by 15–17 | Modify |
| `source_of_truth/agents/README.md` | Catalog entries for ALL Phase 02 agents (reconciliation) | Modify |
| `docs/CODEBASE_CONTEXT.md` | Count claims (agents/skills/subagents) | Modify (verify/update) |
| `tests/test_propagate_master_assets.py` | Marker-guard counts (`roots` list, ~lines 765–770) | Modify (verify/update) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase document (Key Deliverable 7, bundle 5); lines 55–60 define compliance/manifest/gap-review contracts verbatim |
| `source_of_truth/agents/engagement-prepare.agent.md` | House style for engagement agents (frontmatter, security-boundary, fail-fast, terse prose) |
| Sibling plans 14–17 in `dev/feature/` | Document contracts the manifest schema must index |
| `ports/`, `.github/` | Generated output — never hand-edit; propagate only |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| At expansion time none of the four upstream feature bundles (14–17) are implemented; all engagement-* agent names except `engagement-prepare` and the orchestrator file itself are still `[PROPOSED]` in sibling plans | Manifest schema and orchestrator wiring must use the names/filenames actually implemented by 14–17, not the plans' proposed names | Implementer resolves every `[PROPOSED]` name against the implemented tree before finalizing the schema (plan Section C already requires this) |
| Sibling plans 15–17 explicitly defer output-document filenames to their implementers "for 18's manifest schema" | The schema's expected-entry list depends on implementation records of 15–17 | Read 14–17 implementation records (`-implementation.md`) at implement time; treat them as the name source of truth |
| `tests/test_propagate_master_assets.py:765-769` marker-guard currently pins claude/agents=28, claude/commands=19, opencode/agents=43, codex/agents=43; comments require counts recounted from disk, not incremented | AC6 reconciliation must recount after all Phase 02 agents land | Add explicit recount task |
| `docs/CODEBASE_CONTEXT.md` currently claims 43 agent definitions (24 hidden / 19 user-invocable) and 27 skills; disk agrees today, so every Phase 02 addition shifts these claims | AC6 scope confirmed real | Update all count claims after final tree settles |
| Learnings confirm the "feature-13 reconciliation" pattern (`cross-phase-decisions.md` line 28): earlier features intentionally leave counts/catalog gaps; this feature must verify all landed, not assume | Validates plan's AC6 wording | None — plan is correct |
| Test baseline captured: 233 passed, 113 subtests, 0 failed | Clean baseline for AC7 gate | None |
| No contradictions with the plan found | — | — |

## Architectural Decisions

- **Schema lives in a skill**, not in either agent, so the manifest-writing step and the gap reviewer load one definition (mirrors the workspace-layout skill from 14).
- **Expected entries are derived from the schema given pairs and modes** — never hand-enumerated per engagement (enumeration-gap lesson: close gaps by derivation).
- **Gap reviewer consumes the manifest** as its completeness checklist rather than re-deriving expectations; present/missing logic stated once, in the schema.
- **Audit-trail proof (16) groups with compliance materials** in the client-facing section ordering.
- **Agent grants**: read/search/edit-class only for both new agents.
- Simplest shape: one skill + two agents + final orchestrator loop paragraphs.

## Constraints

- `source_of_truth/` is the only authoring surface; `ports/` and `.github/` regenerate via `python3 scripts/propagate_master_assets.py --once`, run to fixed point (zero-change second run).
- Brevity constraint (AC8): each rule stated once in definitions and schema — repeated rules fail review.
- New agents are hidden subagents unless the phase says otherwise; follow `engagement-prepare.agent.md` house style.
- SOW acceptance criteria are read from the engagement's SOW document, never hardcoded.
- Dimension NOT RUN upstream → compliance evidence says NOT RUN/NOT VERIFIED, never a pass.
- No SOW configured → recorded honestly; SOW-required labels fall back to a "no SOW" state, not silently to above-contract.
- All manifest paths resolve within the single workspace root (14's AC4).
- Multi-pair engagements: schema expands per pair; do not assume single-pair.

## Scope Boundaries

- No PDF assembly or branding (user assembles in Claude Design).
- No quality gates on scan/docs coverage — gaps recorded, not blocking.
- No remediation; no operational docs (Phase 03).
- Do not modify `engagement-prepare.agent.md` or any of 14–17's deliverables beyond the orchestrator roster/loop additions and reconciliation surfaces.
- No new logging; manifest + working-state file are the run record.
- Introduced-issues report stays technical-section only.

## Relationships to Sibling Plans

Wave 5, sequential, depends on 14–17 (all share the orchestrator agent file):

- **14** — workspace root + working-state file (technical-section manifest entries; path-resolution rule).
- **15** — raw reports (technical-section entries).
- **16** — delta/security docs, audit-trail grouping, introduced-issues technical entry.
- **17** — intended-behavior spec referenced by the verification summary (AC2).

This is the phase's integration feature: AC5 is the end-to-end runnable-whole check.

## Suggested Implementation Order

Stages in plan order: schema skill → two agents → orchestrator wiring → reconciliation/propagate/verify. Must run after 14–17 are implemented and their document names are final.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Stdlib-only Python 3 scripts + markdown agent/skill definitions (no runtime app) |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 233 passed, 113 subtests passed, 0 failed — captured 2026-07-22 |
| Lint | Not configured |
| Format | Not configured |
| Propagation | `python3 scripts/propagate_master_assets.py --once` (run until zero-change) |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:
- Phase-01 feature 13 owns the deferred-reconciliation pattern this feature repeats: earlier features leave count/catalog gaps intentionally; the final feature verifies all landed (marker-guard counts, CODEBASE_CONTEXT claims, README catalog).
- Documentation count claims drift; reconcile definitions first, then guard counts by claim-shape derivation.
- Propagation is not idempotent across agent reclassification/rename — run until every change counter is zero; "I ran the propagator" is not convergence evidence (`test_committed_tree_is_at_a_propagation_fixed_point`).
- Marker-guard counts must be recounted from disk (`ls ports/<harness>/agents`), never incremented from memory.

From `.github/learnings/review-learnings.md`:
- When agent inventory or counts change, update every summary surface in the same change: README intros, Mermaid labels, CODEBASE_CONTEXT summaries, comparison tables.
- An evidence-shaped claim is not evidence — re-run cited proofs (fixed-point, suite counts) against the actual tree.
