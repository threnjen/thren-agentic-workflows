# Feature: Handoff Text Migration

**Phase:** 01 — Compact-Based Handoff & Docs-Writer Cleanup
**Feature:** 01 of 2

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `.github/agents/01-project-planner.agent.md`, `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/01-project-planner.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/project-planner.md`, `claude/agents/phase-refiner.md`
- **Sequential reason:** n/a

---

## A. Requirements & Traceability

Replace forward-pipeline "open a new chat and attach" handoff instructions with a uniform pattern: users type `/compact` to reduce context, then invoke the next agent via `@mention` in the same chat window.

### Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC1 | `.github/agents/01-project-planner.agent.md` — Pipeline Next Step block uses `/compact` + `@02 Phase - Refiner` (spaced name) | `git diff` shows only the quoted block changed |
| AC2 | `.github/agents/02-phase-refiner.agent.md` — Pipeline Next Step block uses `/compact` + `@03 Feature - Decomposer` (spaced name) | `git diff` shows only the quoted block changed |
| AC3 | `opencode/agents/01-project-planner.md` — Pipeline Next Step block uses `/compact` + `@02-phase-refiner` (hyphenated name) | `git diff` shows only the quoted block changed |
| AC4 | `opencode/agents/02-phase-refiner.md` — Pipeline Next Step block uses `/compact` + `@03-feature-decomposer` (hyphenated name) | `git diff` shows only the quoted block changed |
| AC5 | `claude/agents/project-planner.md` — Pipeline Next Step block uses `/compact` + `@02-phase-refiner` (hyphenated name) | `git diff` shows only the quoted block changed |
| AC6 | `claude/agents/phase-refiner.md` — Pipeline Next Step block uses `/compact` + `@03-feature-decomposer` (hyphenated name) | `git diff` shows only the quoted block changed |
| AC7 | All 6 handoff texts recommend attaching Phase doc and DISCOVERY_CONTEXT.md | Manual review of each block |
| AC8 | All 6 handoff texts end with cycle-back instruction ("return here to write the next phase") where applicable | Manual review — only project-planner files retain cycle-back text |
| AC9 | Phase-refiner Pipeline Next Step section header unchanged (still reads "Pipeline Next Step") — only the quoted block changes | `git diff` confirms no header modification |
| AC10 | No changes outside the quoted handoff block in any file | `git diff` confirms zero unintended changes |

### Non-Goals

- NOT changing Pipeline Next Step HEADERS in phase-refiner files (Feature 02 does that)
- NOT removing Phase 7 sections (Feature 02 does that)
- NOT changing cycle-back instructions in project-planner files
- NOT touching 03-feature-decomposer files
- NOT modifying shared `.github/instructions/` files
- NOT touching documentation freshness check recommendations

### Traceability

| Acceptance Criteria | Files |
|--------------------|-------|
| AC1 | `.github/agents/01-project-planner.agent.md` |
| AC2 | `.github/agents/02-phase-refiner.agent.md` |
| AC3 | `opencode/agents/01-project-planner.md` |
| AC4 | `opencode/agents/02-phase-refiner.md` |
| AC5 | `claude/agents/project-planner.md` |
| AC6 | `claude/agents/phase-refiner.md` |
| AC7–AC10 | All 6 files (verification via diff/review) |

---

## B. Correctness & Edge Cases

### Key Workflows

1. **Project Planner → Phase Refiner handoff (3 files):** Each project-planner file contains a Pipeline Next Step section with a quoted handoff block. Replace the "open a new chat" wording with the `/compact` pattern. The `@mention` target differs per variant.

2. **Phase Refiner → Feature Decomposer handoff (3 files):** Each phase-refiner file contains a Pipeline Next Step section with a quoted handoff block. Replace the "open a new chat" wording with the `/compact` pattern. The `@mention` target differs per variant.

3. **Cycle-back preservation:** Project-planner files MUST retain "Once you've completed executing phase 1, return here to write the next phase." Phase-refiner files do NOT have cycle-back text.

### Failure Modes & Mitigations

| Failure Mode | Mitigation |
|-------------|------------|
| Wrong `@mention` name used for a variant | Each file read prior to edit to confirm the variant's naming convention |
| `/compact` instruction omitted from replacement text | Target text template includes `/compact` explicitly |
| Cycle-back text accidentally removed from project-planner | Target text template preserves it |
| Attach recommendation dropped | Target text template includes "We recommend attaching the Phase document" |

### Target Text — Project Planner handoffs

Replace the entire quoted handoff block with this exact text (where `[AGENT_NAME]` varies by file):

> **"Phase document written to `docs/phases/`. To refine this phase, use `/compact` to reduce context, then invoke `@[AGENT_NAME]` in this same chat. We recommend attaching the Phase document (e.g., `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`) and any `DISCOVERY_CONTEXT.md` so the refiner has full context. Once you've completed executing phase 1, return here to write the next phase."**

`[AGENT_NAME]` values:
- `.github/agents/01-project-planner.agent.md` → `02 Phase - Refiner`
- `opencode/agents/01-project-planner.md` → `02-phase-refiner`
- `claude/agents/project-planner.md` → `02-phase-refiner`

### Target Text — Phase Refiner handoffs

Replace the entire quoted handoff block with this exact text (where `[AGENT_NAME]` varies by file):

> **"Phase refinement complete. The updated document has been written to `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` and repository documentation has been refreshed. To continue, use `/compact` to reduce context, then invoke `@[AGENT_NAME]` in this same chat. We recommend attaching the Phase document and any `PHASE_0N_DISCOVERY_CONTEXT.md` so decomposition has the full context."**

`[AGENT_NAME]` values:
- `.github/agents/02-phase-refiner.agent.md` → `03 Feature - Decomposer`
- `opencode/agents/02-phase-refiner.md` → `03-feature-decomposer`
- `claude/agents/phase-refiner.md` → `03-feature-decomposer`

---

## C. Consistency & Architecture Fit

### Existing Patterns

- All 6 files follow the same structure: a "## Pipeline Next Step" heading, a one-line description, then a quoted block
- The `.github/agents/` variant uses spaced `@mention` names; `opencode/agents/` and `claude/agents/` use hyphenated
- The quoted block is always a single paragraph preceded by "> **"

### Deviations

None — the replacement text follows the exact same structural pattern as the existing text, just with different wording.

### Interfaces/Contracts

The replacement text must:
- Be exactly one paragraph (not multiple lines)
- Start with `> **"`
- End with `**"`
- Include `@[AGENT_NAME]` with the correct variant-specific name
- Include the phrase "use `/compact` to reduce context, then invoke"
- Preserve the "return here to write the next phase" sentence in project-planner files ONLY

---

## D. Clean Design & Maintainability

### Simplest Design

Straightforward text replacement — find the matching quoted block in each file and replace it with the new template. No structural changes, no file reorganization.

### Complexity Risks

- Overlapping edits in phase-refiner files (Feature 02 also touches these 3 files). Mitigation: Feature 01 only changes the quoted text INSIDE the Pipeline Next Step section. Feature 02 changes the section HEADER and removes the Phase 7 section. As long as Feature 01 doesn't touch the header or Phase 7 section, there is no conflict.
- The claude variant's project-planner quoted text is slightly shorter than the others (no example path). The replacement text standardizes this.

### Clean Checklist

- [ ] Only the quoted handoff block is modified — no surrounding text, no headers, no other sections
- [ ] Replacement text is identical across all files of the same type (project-planner vs. phase-refiner) modulo the `@mention` name
- [ ] Cycle-back text preserved in project-planner files only

---

## E. Completeness: Observability, Security, Operability

### Logging/Metrics/Tracing

Not applicable — purely instructional text changes. Verification is via `git diff`.

### Security

Not applicable — no secrets, no authentication, no data handling.

### Runbook

1. For each of the 6 files, locate the `## Pipeline Next Step` section
2. Find the quoted handoff block (starts with `> **"`)
3. Replace the entire quoted block with the variant-appropriate target text
4. Verify: `git diff` shows only the expected change per file
5. Verify: cycle-back sentence remains in project-planner files
6. Hand off to Feature 02 (docs-writer removal) which will modify the 3 phase-refiner files

---

## F. Test Plan

### Verification (no automated tests — instruction files only)

| Test | Given/When/Then | AC Covered |
|------|----------------|------------|
| T1: Project planner .github variant | GIVEN `.github/agents/01-project-planner.agent.md` WHEN reading Pipeline Next Step THEN quoted block contains `/compact` + `@02 Phase - Refiner` + cycle-back text | AC1, AC7–AC10 |
| T2: Phase refiner .github variant | GIVEN `.github/agents/02-phase-refiner.agent.md` WHEN reading Pipeline Next Step THEN quoted block contains `/compact` + `@03 Feature - Decomposer` (no cycle-back) | AC2, AC7–AC10 |
| T3: Project planner opencode variant | GIVEN `opencode/agents/01-project-planner.md` WHEN reading Pipeline Next Step THEN quoted block contains `/compact` + `@02-phase-refiner` + cycle-back text | AC3, AC7–AC10 |
| T4: Phase refiner opencode variant | GIVEN `opencode/agents/02-phase-refiner.md` WHEN reading Pipeline Next Step THEN quoted block contains `/compact` + `@03-feature-decomposer` (no cycle-back) | AC4, AC7–AC10 |
| T5: Project planner claude variant | GIVEN `claude/agents/project-planner.md` WHEN reading Pipeline Next Step THEN quoted block contains `/compact` + `@02-phase-refiner` + cycle-back text | AC5, AC7–AC10 |
| T6: Phase refiner claude variant | GIVEN `claude/agents/phase-refiner.md` WHEN reading Pipeline Next Step THEN quoted block contains `/compact` + `@03-feature-decomposer` (no cycle-back) | AC6, AC7–AC10 |
| T7: No unintended changes | GIVEN all 6 modified files WHEN running `git diff` THEN only the quoted handoff blocks differ from the original | AC10 |

### Test Data / Fixtures

No test data needed — the files themselves are the test artifacts.

---

## Stages

### Stage 1: .github/agents Variant (2 files)
**Goal**: Replace handoff text in `.github/agents/01-project-planner.agent.md` and `.github/agents/02-phase-refiner.agent.md`
**Success Criteria**: Both files show only the quoted block changed; AC1, AC2 pass
**Status**: Not Started

### Stage 2: opencode/agents Variant (2 files)
**Goal**: Replace handoff text in `opencode/agents/01-project-planner.md` and `opencode/agents/02-phase-refiner.md`
**Success Criteria**: Both files show only the quoted block changed; AC3, AC4 pass
**Status**: Not Started

### Stage 3: claude/agents Variant (2 files)
**Goal**: Replace handoff text in `claude/agents/project-planner.md` and `claude/agents/phase-refiner.md`
**Success Criteria**: Both files show only the quoted block changed; AC5, AC6 pass
**Status**: Not Started

### Stage 4: Cross-Cut Verification
**Goal**: Verify all 10 ACs pass; confirm no unintended changes
**Success Criteria**: AC7–AC10 verified via review of all 6 files and `git diff`
**Status**: Not Started
