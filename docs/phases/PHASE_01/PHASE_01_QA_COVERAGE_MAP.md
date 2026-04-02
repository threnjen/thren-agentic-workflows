# AC Coverage Map: Phase 01 — Split Feature Decomposer from Phase Execute

**Date:** 2026-04-02
**Mode:** Consolidated Coverage Map
**Scope:** All acceptance criteria across 3 features: decomposer-promote, plan-expander-create, executor-renumber

## Coverage Map

Since this repository contains **no runnable code and no automated tests** (Markdown-only), the "Automated Coverage" column reflects whether the individual feature review already verified that AC through manual document inspection. "Manual QA Needed?" indicates whether additional cross-cutting verification is required beyond the per-feature review.

### decomposer-promote (7 ACs)

| Feature | AC | Reviewer Verified | Manual QA Needed? | Reason |
|---------|----|-------------------|-------------------|--------|
| decomposer-promote | AC1: Frontmatter `name` is `03 Feature - Decomposer` | Yes | No | Verified in review record; single-file check |
| decomposer-promote | AC2: `user-invocable: false` removed | Yes | No | Verified in review record; single-file check |
| decomposer-promote | AC3: Output scoped to `-plan.md` only | Yes | Yes — cross-reference | Reviewer verified the agent body itself, but downstream files (README.md, phase-final-review.agent.md) still attribute `-context.md`/`-tasks.md` to Decomposer |
| decomposer-promote | AC4: Standalone mode references `@04 Phase - Execute` | Yes | No | Verified in review record; single-file check |
| decomposer-promote | AC5: Subagent return value describes plan-only output | Yes | No | Verified in review record; single-file check |
| decomposer-promote | AC6: `read-only-agent.instructions.md` applyTo includes Decomposer | Yes | Yes — cross-reference | Verify the Decomposer is still listed in `applyTo` and that no new applyTo references are needed for the Plan Expander |
| decomposer-promote | AC7: Quality Checklist reference to `feature-plan-set` skill intact | Yes | No | Verified in review record; single-file check |

### plan-expander-create (8 ACs)

| Feature | AC | Reviewer Verified | Manual QA Needed? | Reason |
|---------|----|-------------------|-------------------|--------|
| plan-expander-create | AC1: Agent file exists | Yes | No | File creation verified |
| plan-expander-create | AC2: Frontmatter has correct fields | Yes | Yes — cross-reference | Verify `name` field matches how other files reference this agent (executor `agents:` list, skill text) |
| plan-expander-create | AC3: Agent reads plans, generates context + tasks | Yes | No | Body content verified by reviewer |
| plan-expander-create | AC4: Context file generation instructions | Yes | No | Body content verified by reviewer |
| plan-expander-create | AC5: Tasks file generation instructions | Yes | No | Body content verified by reviewer |
| plan-expander-create | AC6: Subagent mode support | Yes | No | `user-invocable: false` verified |
| plan-expander-create | AC7: Skill updated for split ownership | Yes | Yes — cross-reference | Verify skill wording aligns with both the Decomposer agent body and the Plan Expander agent body |
| plan-expander-create | AC8: Instruction producer table updated | Yes | Yes — cross-reference | Verify the instruction table is consistent with README.md Task Documentation Pattern section and phase-final-review.agent.md attribution tables |

### executor-renumber (8 ACs)

| Feature | AC | Reviewer Verified | Manual QA Needed? | Reason |
|---------|----|-------------------|-------------------|--------|
| executor-renumber | AC1: Frontmatter `name` is `04 Phase - Execute` | Yes | No | Verified in review record |
| executor-renumber | AC2: `agents:` list includes Plan Expander and Decomposer | Yes | Yes — cross-reference | Verify agent names in `agents:` field exactly match the `name:` fields in the referenced agent files |
| executor-renumber | AC3: Step 1 checks for plans, conditionally invokes Decomposer | Yes | Yes — pipeline flow | Walk through the full pipeline to verify Step 1 → Step 2 → Step 3 flow is coherent |
| executor-renumber | AC4: Plan Expander invocation step added | Yes | Yes — pipeline flow | Verify Plan Expander step references correct agent name and verifies correct output files |
| executor-renumber | AC5: `orchestrator-conventions.instructions.md` applyTo correct | Yes | No | Filename unchanged; verified |
| executor-renumber | AC6: `project-planner.agent.md` references updated to `@04` | Yes | Yes — cross-reference | Verify pipeline diagram in Planner correctly shows both `03 Feature - Decomposer` and `04 Phase - Execute` |
| executor-renumber | AC7: `phase-refiner.agent.md` references updated to `@04` | Yes | No | 3 references verified by reviewer |
| executor-renumber | AC8: Pipeline diagram updated | Yes | Yes — cross-reference | Verify the diagram aligns with actual agent names, numbering, and pipeline flow described in the executor |

## Summary

| Category | Count |
|----------|-------|
| Total ACs across all features | 23 |
| Reviewer-verified (per-feature review) | 23 |
| Requires additional cross-cutting manual QA | 10 |
| No additional QA needed | 13 |

All 23 ACs were individually verified by the Feature - Reviewer during per-feature review. The 10 ACs flagged for manual QA require **cross-cutting consistency checks** — verifying that changes made across 3 separate features align with each other and with files that were in all 3 features' "out of scope" lists (README.md, phase-final-review.agent.md, CODEBASE_CONTEXT.md).
