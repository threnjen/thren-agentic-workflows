# Feature: Docs-Writer Invocation Removal

**Phase:** 01 — Compact-Based Handoff & Docs-Writer Cleanup
**Feature:** 02 of 2

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** 01-handoff-text-migration (shared 3 phase-refiner files — must apply after handoff text changes for clean diffs)
- **Key files modified:** `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md`
- **Sequential reason:** shares `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, `claude/agents/phase-refiner.md` with 01-handoff-text-migration — both edit same files sequentially

---

## A. Requirements & Traceability

Remove instructions that tell phase-refiner agents to automatically invoke the Docs Writer subagent at the end of their pipeline (Phase 7). Remove the Phase 7 sections and update the Pipeline Next Step section headers that reference docs-writer.

### Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC1 | `.github/agents/02-phase-refiner.agent.md` — Phase 7 section heading + all instruction paragraphs deleted | `git diff` shows removal of lines 172–181 |
| AC2 | `.github/agents/02-phase-refiner.agent.md` — Pipeline Next Step header changed from "After `@Docs Writer` has completed (Phase 7), tell the user:" to just "Tell the user:" | Manual review of line 189 |
| AC3 | `opencode/agents/02-phase-refiner.md` — Phase 7 section heading + all instruction paragraphs deleted | `git diff` shows removal of lines 189–198 |
| AC4 | `opencode/agents/02-phase-refiner.md` — Pipeline Next Step header changed from "After `@docs-writer` has completed (Phase 7), tell the user:" to just "Tell the user:" | Manual review of line 206 |
| AC5 | `claude/agents/phase-refiner.md` — Phase 7 section heading + all instruction paragraphs deleted | `git diff` shows removal of lines 154–161 |
| AC6 | `claude/agents/phase-refiner.md` — Pipeline Next Step header changed from "After Phase 7 completes, tell the user:" to just "Tell the user:" | Manual review of line 169 |
| AC7 | No other sections modified in any of the 3 files | `git diff` confirms only Phase 7 deletions and header changes |
| AC8 | Handoff text (added by Feature 01) remains intact in all 3 phase-refiner files | Manual review of Pipeline Next Step quoted block |

### Non-Goals

- NOT removing the "Recommendation: Run `@docs-writer`" from project-planner freshness checks (kept as user-facing suggestions)
- NOT modifying `.github/instructions/documentation-freshness-check.instructions.md` (kept as-is)
- NOT touching 03-feature-decomposer files (no docs-writer instructions exist)
- NOT touching `.github/agents/01-project-planner.agent.md` (no inline docs-writer text)
- NOT altering the handoff text that Feature 01 just applied

### Traceability

| Acceptance Criteria | Files |
|--------------------|-------|
| AC1–AC2 | `.github/agents/02-phase-refiner.agent.md` |
| AC3–AC4 | `opencode/agents/02-phase-refiner.md` |
| AC5–AC6 | `claude/agents/phase-refiner.md` |
| AC7 | All 3 files |
| AC8 | All 3 files |

---

## B. Correctness & Edge Cases

### Key Workflows

1. **`.github/agents/02-phase-refiner.agent.md`:**
   - Delete the entire "### Phase 7: Update Repository Documentation" section (heading + 3 instruction paragraphs + blank lines)
   - Change the Pipeline Next Step header from "After `@Docs Writer` has completed (Phase 7), tell the user:" to "Tell the user:"

2. **`opencode/agents/02-phase-refiner.md`:**
   - Delete the entire "### Phase 7: Update Repository Documentation" section (heading + 3 instruction paragraphs + blank lines)
   - Change the Pipeline Next Step header from "After `@docs-writer` has completed (Phase 7), tell the user:" to "Tell the user:"

3. **`claude/agents/phase-refiner.md`:**
   - Delete the entire "### Phase 7: Update Repository Documentation" section (heading + 2 instruction paragraphs + blank lines)
   - Change the Pipeline Next Step header from "After Phase 7 completes, tell the user:" to "Tell the user:"

### Exact Line Ranges Per File

| File | Phase 7 Lines | Pipeline Next Step Header Line | Target Header Text |
|------|---------------|-------------------------------|-------------------|
| `.github/agents/02-phase-refiner.agent.md` | 172–181 | 189 | "Tell the user:" |
| `opencode/agents/02-phase-refiner.md` | 189–198 | 206 | "Tell the user:" |
| `claude/agents/phase-refiner.md` | 154–161 | 169 | "Tell the user:" |

Note: Line numbers are current as of discovery. After Feature 01 modifies these files, line numbers may shift slightly. The implementer must locate the content by heading text, not hardcoded line numbers.

### Failure Modes & Mitigations

| Failure Mode | Mitigation |
|-------------|------------|
| Phase 7 section partially deleted (leftover text) | Delete the heading AND all paragraph content between heading and next heading/blank line |
| Pipeline Next Step header not found after Feature 01 edits | Feature 01 changes the quoted block INSIDE the section, not the header — header should still be present |
| Accidental deletion of adjacent content (e.g., Escalation section) | Locate Phase 7 by its heading `### Phase 7:` — delete only between that heading and the next `##` heading |
| Docs-writer referenced elsewhere in file | Grep for `docs-writer|Docs Writer|docs writer` in each file after edits to confirm no remaining references |

---

## C. Consistency & Architecture Fit

### Existing Patterns

- All 3 phase-refiner files have a `### Phase 7: Update Repository Documentation` section that follows `### Phase 6: Write Document`
- All 3 files have a `## Pipeline Next Step` header whose first line references docs-writer
- The `.github/agents/` variant uses `@Docs Writer` (spaced, capitalised); `opencode/agents/` and `claude/agents/` use `@docs-writer` (hyphenated, lowercase)

### Deviations

None — changes bring the files in line with the desired post-removal state. The "Tell the user:" header is the simplest possible replacement.

### Interfaces/Contracts

- The Pipeline Next Step header must be exactly `Tell the user:` (no trailing period, no prefix)
- The Phase 7 section removal must not leave orphan blank lines between Phase 6 and the Escalation section

---

## D. Clean Design & Maintainability

### Simplest Design

Delete Phase 7 section content (heading + paragraphs). Replace the Pipeline Next Step header with a minimal "Tell the user:". No restructuring of remaining sections needed — the Escalation section comes next and reads naturally.

### Complexity Risks

- Line number drift after Feature 01: The quoted handoff block in Pipeline Next Step is getting longer (adding `/compact` instruction). This shifts line numbers for everything below the quoted block, but the Phase 7 section is ABOVE the Pipeline Next Step section (or in the `.github` variant, Phase 7 comes right before it), so it's unaffected by the handoff text change.
- Wait, actually let me check the file order:
  - In `.github/agents/02-phase-refiner.agent.md`: Phase 6 (line ~165), Phase 7 (172–181), Escalation (183), Pipeline Next Step (187) — Phase 7 is BEFORE Pipeline Next Step
  - In `opencode/agents/02-phase-refiner.md`: Phase 6 (178), Phase 7 (189–198), Escalation (200), Pipeline Next Step (204) — Phase 7 is BEFORE Pipeline Next Step
  - In `claude/agents/phase-refiner.md`: Phase 6 (143), Phase 7 (154–161), Escalation (163), Pipeline Next Step (167) — Phase 7 is BEFORE Pipeline Next Step

  So Phase 7 is always ABOVE Pipeline Next Step. Feature 01 changes Pipeline Next Step (below Phase 7). Feature 02 changes Phase 7 (above Pipeline Next Step). These are two different sections that don't overlap. The risk is only if the implementer modifies the wrong section, which is mitigated by targeting specific section headings.

Actually, there's no real content overlap risk because the handoff text (Feature 01) is INSIDE the Pipeline Next Step section, and Phase 7 removal is in a COMPLETELY DIFFERENT section above it. The only shared target is the Pipeline Next Step HEADER text which includes "After `@Docs Writer` has completed (Phase 7), tell the user:" — Feature 01 doesn't touch this header.

So the dependency is mostly about sequencing for clean diffs, not runtime correctness. However, since both features touch the same 3 files, they still can't run in parallel safely (same file modified = parallel_safe: no).

### Clean Checklist

- [ ] Phase 7 sections fully removed (heading + all instruction text)
- [ ] No orphan blank lines or leftover fragments where Phase 7 was
- [ ] Pipeline Next Step header uses exactly "Tell the user:"
- [ ] Escalation section unaffected
- [ ] Handoff text from Feature 01 unchanged
- [ ] No remaining references to docs-writer in phase-refiner files

---

## E. Completeness: Observability, Security, Operability

### Logging/Metrics/Tracing

Not applicable — purely instructional text changes. Verification is via `git diff`.

### Security

Not applicable.

### Runbook

1. For each of the 3 phase-refiner files (Feature 01 must already be complete):
   a. Locate the `### Phase 7: Update Repository Documentation` heading
   b. Delete the heading and all content between it and the next `##` heading (or end of file)
   c. Locate the `## Pipeline Next Step` section header line that contains "After `@Docs Writer` / `@docs-writer` / Phase 7"
   d. Replace that header line with just "Tell the user:"
2. Verify: `git diff` shows only Phase 7 deletion + header change per file
3. Grep each modified file for `docs-writer|Docs Writer` to confirm zero remaining references
4. Verify handoff text (from Feature 01) is still intact

---

## F. Test Plan

### Verification (no automated tests — instruction files only)

| Test | Given/When/Then | AC Covered |
|------|----------------|------------|
| T1: .github/github Phase 7 removed | GIVEN `.github/agents/02-phase-refiner.agent.md` WHEN searching for "Phase 7:" THEN no match found | AC1 |
| T2: .github/ Pipeline Next Step header simplified | GIVEN `.github/agents/02-phase-refiner.agent.md` WHEN reading Pipeline Next Step section head THEN it reads "Tell the user:" | AC2 |
| T3: opencode Phase 7 removed | GIVEN `opencode/agents/02-phase-refiner.md` WHEN searching for "Phase 7:" THEN no match found | AC3 |
| T4: opencode Pipeline Next Step header simplified | GIVEN `opencode/agents/02-phase-refiner.md` WHEN reading Pipeline Next Step section head THEN it reads "Tell the user:" | AC4 |
| T5: claude Phase 7 removed | GIVEN `claude/agents/phase-refiner.md` WHEN searching for "Phase 7:" THEN no match found | AC5 |
| T6: claude Pipeline Next Step header simplified | GIVEN `claude/agents/phase-refiner.md` WHEN reading Pipeline Next Step section head THEN it reads "Tell the user:" | AC6 |
| T7: No docs-writer references remain | GIVEN all 3 modified files WHEN grepping for `docs-writer\|Docs Writer` THEN zero matches | AC7 |
| T8: Handoff text preserved | GIVEN all 3 modified files WHEN reading Pipeline Next Step quoted block THEN it matches the `/compact` pattern from Feature 01 | AC8 |

### Test Data / Fixtures

No test data needed — the files themselves are the test artifacts.

---

## Stages

### Stage 1: .github/agents Variant
**Goal**: Remove Phase 7 from `.github/agents/02-phase-refiner.agent.md`; update Pipeline Next Step header
**Success Criteria**: AC1–AC2 pass
**Status**: Not Started

### Stage 2: opencode/agents Variant
**Goal**: Remove Phase 7 from `opencode/agents/02-phase-refiner.md`; update Pipeline Next Step header
**Success Criteria**: AC3–AC4 pass
**Status**: Not Started

### Stage 3: claude/agents Variant
**Goal**: Remove Phase 7 from `claude/agents/phase-refiner.md`; update Pipeline Next Step header
**Success Criteria**: AC5–AC6 pass
**Status**: Not Started

### Stage 4: Cross-Cut Verification
**Goal**: Verify all 8 ACs pass; grep for remaining docs-writer references; confirm handoff text intact
**Success Criteria**: AC7–AC8 verified via grep and manual review; zero unintended changes
**Status**: Not Started
