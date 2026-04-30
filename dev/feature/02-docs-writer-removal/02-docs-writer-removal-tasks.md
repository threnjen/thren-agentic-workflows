# Tasks: Docs-Writer Invocation Removal

**Phase:** 01 — Compact-Based Handoff & Docs-Writer Cleanup
**Feature:** 02 of 2

---

## Prerequisites

- [ ] Feature 01 (handoff-text-migration) is complete — all 3 phase-refiner files have the updated handoff text in their Pipeline Next Step sections before beginning this feature

---

## Stage 1: `.github/agents` Variant

**Goal:** Remove Phase 7 from `.github/agents/02-phase-refiner.agent.md`; update Pipeline Next Step header.
**Success Criteria:** AC1–AC2 pass.
**Status:** Not Started

- [ ] **1.1** Locate the `### Phase 7: Update Repository Documentation` heading in `.github/agents/02-phase-refiner.agent.md` (approximately lines 172–181)
- [ ] **1.2** Delete the heading and all instruction paragraphs between it and the next `##` heading — do not leave orphan blank lines or fragments
- [ ] **1.3** Collapse any excess blank lines left by the deletion so the remaining sections flow cleanly
- [ ] **1.4** Locate the `## Pipeline Next Step` header line containing `"After @Docs Writer has completed (Phase 7), tell the user:"` (approximately line 189)
- [ ] **1.5** Replace that entire header line with exactly `Tell the user:` (no trailing period, no prefix)
- [ ] **1.6** Verify AC1: `git diff` shows removal of Phase 7 section (heading + instruction paragraphs) and nothing else beyond the header change
- [ ] **1.7** Verify AC2: Pipeline Next Step section header now reads `Tell the user:`
- [ ] **1.8** Grep the modified file for `docs-writer|Docs Writer|docs writer` — confirm zero remaining references

---

## Stage 2: `opencode/agents` Variant

**Goal:** Remove Phase 7 from `opencode/agents/02-phase-refiner.md`; update Pipeline Next Step header.
**Success Criteria:** AC3–AC4 pass.
**Status:** Not Started

- [ ] **2.1** Locate the `### Phase 7: Update Repository Documentation` heading in `opencode/agents/02-phase-refiner.md` (approximately lines 189–198)
- [ ] **2.2** Delete the heading and all instruction paragraphs between it and the next `##` heading — do not leave orphan blank lines or fragments
- [ ] **2.3** Collapse any excess blank lines left by the deletion so the remaining sections flow cleanly
- [ ] **2.4** Locate the `## Pipeline Next Step` header line containing `"After @docs-writer has completed (Phase 7), tell the user:"` (approximately line 206)
- [ ] **2.5** Replace that entire header line with exactly `Tell the user:` (no trailing period, no prefix)
- [ ] **2.6** Verify AC3: `git diff` shows removal of Phase 7 section (heading + instruction paragraphs) and nothing else beyond the header change
- [ ] **2.7** Verify AC4: Pipeline Next Step section header now reads `Tell the user:`
- [ ] **2.8** Grep the modified file for `docs-writer|Docs Writer|docs writer` — confirm zero remaining references

---

## Stage 3: `claude/agents` Variant

**Goal:** Remove Phase 7 from `claude/agents/phase-refiner.md`; update Pipeline Next Step header.
**Success Criteria:** AC5–AC6 pass.
**Status:** Not Started

- [ ] **3.1** Locate the `### Phase 7: Update Repository Documentation` heading in `claude/agents/phase-refiner.md` (approximately lines 154–161)
- [ ] **3.2** Delete the heading and all instruction paragraphs between it and the next `##` heading — do not leave orphan blank lines or fragments
- [ ] **3.3** Collapse any excess blank lines left by the deletion so the remaining sections flow cleanly
- [ ] **3.4** Locate the `## Pipeline Next Step` header line containing `"After Phase 7 completes, tell the user:"` (approximately line 169)
- [ ] **3.5** Replace that entire header line with exactly `Tell the user:` (no trailing period, no prefix)
- [ ] **3.6** Verify AC5: `git diff` shows removal of Phase 7 section (heading + instruction paragraphs) and nothing else beyond the header change
- [ ] **3.7** Verify AC6: Pipeline Next Step section header now reads `Tell the user:`
- [ ] **3.8** Grep the modified file for `docs-writer|Docs Writer|docs writer` — confirm zero remaining references

---

## Stage 4: Cross-Cut Verification

**Goal:** Verify all 8 ACs pass; grep for remaining docs-writer references; confirm handoff text intact.
**Success Criteria:** AC7–AC8 verified via grep and manual review; zero unintended changes.
**Status:** Not Started

- [ ] **4.1** Verify AC7: Run `git diff` across all 3 files and confirm the only changes are Phase 7 deletions and Pipeline Next Step header replacements — no other sections modified
- [ ] **4.2** Verify AC8: In each file, read the Pipeline Next Step quoted block and confirm the `/compact` handoff text (added by Feature 01) is still intact and unchanged
- [ ] **4.3** Final grep sweep: Search all 3 modified files for `docs-writer|Docs Writer|docs writer` — confirm zero matches across all files
- [ ] **4.4** Final visual review: Spot-check each file for orphan blank lines, leftover fragments, or formatting issues where Phase 7 was removed
