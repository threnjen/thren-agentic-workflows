# Context: Handoff Text Migration

**Phase:** 01 — Compact-Based Handoff & Docs-Writer Cleanup  
**Feature:** 01 of 2

## Key Files

### Files Being Modified

| File | Change Type | Role |
|------|-------------|------|
| `.github/agents/01-project-planner.agent.md` | Modify | Replace Pipeline Next Step handoff block with `/compact` + `@02 Phase - Refiner` pattern; preserve cycle-back text |
| `.github/agents/02-phase-refiner.agent.md` | Modify | Replace Pipeline Next Step handoff block with `/compact` + `@03 Feature - Decomposer` pattern |
| `opencode/agents/01-project-planner.md` | Modify | Replace handoff block with `/compact` + `@02-phase-refiner` pattern; preserve cycle-back text |
| `opencode/agents/02-phase-refiner.md` | Modify | Replace handoff block with `/compact` + `@03-feature-decomposer` pattern |
| `claude/agents/project-planner.md` | Modify | Replace handoff block with `/compact` + `@02-phase-refiner` pattern; preserve cycle-back text |
| `claude/agents/phase-refiner.md` | Modify | Replace handoff block with `/compact` + `@03-feature-decomposer` pattern |

### Read-Only Reference Files

None — verification is done via `git diff` against the original files.

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Handoff pattern | `/compact` + `@mention` in same chat | Reduces user friction vs. "open a new chat and attach" — keeps conversation history and context |
| `@mention` naming convention | Variant-specific (spaced vs. hyphenated) | Each file type already uses a distinct convention; the replacement preserves it to avoid breaking existing user expectations |
| Cycle-back text | Project-planner files retain it; phase-refiner files do not | Preserves the directional pipeline flow: planner → refiner → decomposer → ... → back to planner. Phase-refiner files never had cycle-back text |
| Attach recommendation | Included in all 6 files | Ensures downstream agents receive the Phase document and DISCOVERY_CONTEXT.md for full context |
| Edit boundary | Only the quoted block within `## Pipeline Next Step` | Avoids conflicts with Feature 02 (which modifies headers) and prevents unintended changes per AC10 |

## Constraints

- **Edit boundary:** Only the quoted handoff block (`> **"..."**`) within the `## Pipeline Next Step` section may be modified — no headers, no surrounding paragraphs, no other sections
- **Cycle-back preservation:** The sentence "Once you've completed executing phase 1, return here to write the next phase" must remain in project-planner files only
- **Phase-refiner headers must not change:** The `## Pipeline Next Step` heading text must remain exactly as-is (Feature 02 handles header changes)
- **Phase 7 content must not change:** The reference to `@Docs Writer` / `@docs-writer` and Phase 7 completion text in phase-refiner files must be preserved (Feature 02 handles removal)
- **No scope creep:** Do not modify `.github/instructions/` files, `03-feature-decomposer` files, or any file outside the 6 listed above
- **Replacement text integrity:** Each replacement must be exactly one paragraph, starting with `> **"`, ending with `**"`, and containing `@[AGENT_NAME]` with the correct variant-specific name

## Relationships to Sibling Plans

This feature is **01 of 2** in Phase 01. The sibling is:

- **Feature 02: Handoff Text Headers** — modifies the `## Pipeline Next Step` HEADERS in the 3 phase-refiner files and removes Phase 7 sections. Feature 01 must be applied before or concurrently with Feature 02. While their edits target different parts of the same files (Feature 01: quoted block content; Feature 02: header + Phase 7), applying Feature 01 first ensures that replacements happen against the original text content, making verification simpler.

**Suggested implementation order:** Feature 01 → Feature 02

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown documentation repo (zero runnable code — agent instruction files only) |
| Test Runner | Not applicable — no automated tests; verification via `git diff` and manual review |
| Test Baseline | N/A — docs-only repo |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable — no `.github/learnings/` directory exists in this repository.
