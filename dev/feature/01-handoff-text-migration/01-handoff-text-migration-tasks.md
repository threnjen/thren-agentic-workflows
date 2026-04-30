# Tasks: Handoff Text Migration

**Phase:** 01 — Compact-Based Handoff & Docs-Writer Cleanup  
**Feature:** 01 of 2

---

## Stage 1: .github/agents Variant (2 files)

**Goal:** Replace handoff text in `.github/agents/01-project-planner.agent.md` and `.github/agents/02-phase-refiner.agent.md`  
**Success Criteria:** Both files show only the quoted block changed; AC1, AC2 pass

- [ ] Read `.github/agents/01-project-planner.agent.md` and locate the `## Pipeline Next Step` quoted handoff block (currently line 126)
- [ ] Replace the quoted handoff block with the target text using `@02 Phase - Refiner`, ensuring cycle-back sentence is preserved
- [ ] Read `.github/agents/02-phase-refiner.agent.md` and locate the `## Pipeline Next Step` quoted handoff block (currently line 191)
- [ ] Replace the quoted handoff block with the target text using `@03 Feature - Decomposer` (no cycle-back text)
- [ ] Verify via `git diff` that only the quoted block changed in both files — AC1, AC2 pass

## Stage 2: opencode/agents Variant (2 files)

**Goal:** Replace handoff text in `opencode/agents/01-project-planner.md` and `opencode/agents/02-phase-refiner.md`  
**Success Criteria:** Both files show only the quoted block changed; AC3, AC4 pass

- [ ] Read `opencode/agents/01-project-planner.md` and locate the `## Pipeline Next Step` quoted handoff block (currently line 141)
- [ ] Replace the quoted handoff block with the target text using `@02-phase-refiner`, ensuring cycle-back sentence is preserved
- [ ] Read `opencode/agents/02-phase-refiner.md` and locate the `## Pipeline Next Step` quoted handoff block (currently line 208)
- [ ] Replace the quoted handoff block with the target text using `@03-feature-decomposer` (no cycle-back text)
- [ ] Verify via `git diff` that only the quoted block changed in both files — AC3, AC4 pass

## Stage 3: claude/agents Variant (2 files)

**Goal:** Replace handoff text in `claude/agents/project-planner.md` and `claude/agents/phase-refiner.md`  
**Success Criteria:** Both files show only the quoted block changed; AC5, AC6 pass

- [ ] Read `claude/agents/project-planner.md` and locate the `## Pipeline Next Step` quoted handoff block (currently line 123)
- [ ] Replace the quoted handoff block with the target text using `@02-phase-refiner`, ensuring cycle-back sentence is preserved
- [ ] Read `claude/agents/phase-refiner.md` and locate the `## Pipeline Next Step` quoted handoff block (currently line 171)
- [ ] Replace the quoted handoff block with the target text using `@03-feature-decomposer` (no cycle-back text)
- [ ] Verify via `git diff` that only the quoted block changed in both files — AC5, AC6 pass

## Stage 4: Cross-Cut Verification

**Goal:** Verify all 10 ACs pass; confirm no unintended changes  
**Success Criteria:** AC7–AC10 verified via review of all 6 files and `git diff`

- [ ] Verify AC7 — All 6 handoff texts recommend attaching the Phase document and DISCOVERY_CONTEXT.md
- [ ] Verify AC8 — All 6 handoff texts end with appropriate cycle-back instructions (present in project-planner files only; absent in phase-refiner files)
- [ ] Verify AC9 — Phase-refiner `## Pipeline Next Step` section header is unchanged (no header modifications)
- [ ] Verify AC10 — `git diff` confirms zero changes outside the quoted handoff block in all 6 files
