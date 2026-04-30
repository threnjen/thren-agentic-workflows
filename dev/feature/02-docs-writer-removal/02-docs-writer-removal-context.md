# Context: Docs-Writer Invocation Removal

**Phase:** 01 — Compact-Based Handoff & Docs-Writer Cleanup
**Feature:** 02 of 2

---

## Key Files

### Files Being Modified

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/02-phase-refiner.agent.md` | GitHub Copilot variant of the phase-refiner agent | **Modify** — delete Phase 7 section (lines 172–181), update Pipeline Next Step header (line 189) |
| `opencode/agents/02-phase-refiner.md` | OpenCode variant of the phase-refiner agent | **Modify** — delete Phase 7 section (lines 189–198), update Pipeline Next Step header (line 206) |
| `claude/agents/phase-refiner.md` | Claude Code variant of the phase-refiner agent | **Modify** — delete Phase 7 section (lines 154–161), update Pipeline Next Step header (line 169) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `dev/feature/01-handoff-text-migration/01-handoff-text-migration-plan.md` | Sibling plan — must be applied first (same 3 files edited with sequential dependency) |
| `docs/CODEBASE_CONTEXT.md` | Project structure reference — confirms this is a Markdown-only template repo |
| `docs/ARCHITECTURE.md` | Architecture reference — confirms agent file conventions |

---

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Replacement header text | `"Tell the user:"` (no trailing period, no prefix) | Simplest possible replacement that keeps the Pipeline Next Step section functional without referencing the removed Phase 7 |
| Section removal boundary | Delete from `### Phase 7:` heading up to the next `##` heading | Guarantees full removal without affecting adjacent sections (Escalation section, Phase 6) |
| Line number vs. heading targeting | Locate content by heading text, not hardcoded line numbers | Line numbers will shift after Feature 01 applies its handoff text changes; headings are stable identifiers |
| Post-removal cleanup | Collapse blank lines between remaining sections | Prevents orphan blank lines where Phase 7 was deleted, keeping the file clean |

---

## Constraints

- **Sequential dependency:** Feature 01 (handoff-text-migration) must be applied to all 3 files *before* this feature. Both features modify the same 3 files, so parallel execution is impossible.
- **No automated tests:** All 3 files are Markdown agent definitions — verification is via `git diff` and manual review, not unit tests.
- **Scope boundary:** Do NOT modify the Documentation Freshness Check recommendation in `.github/instructions/documentation-freshness-check.instructions.md` — this remains as a user-facing docs-writer suggestion. Do NOT touch `01-project-planner.agent.md` or `03-feature-decomposer` files.
- **Handoff text preservation:** The `/compact` handoff block added by Feature 01 in the Pipeline Next Step section must remain untouched.
- **No orphan content:** Each Phase 7 deletion must remove the heading AND all instruction paragraphs up to (but not including) the next `##` heading. Partial deletion (e.g., leaving blank lines or fragments) is a failure.
- **Verification gate:** After all edits, grep each file for `docs-writer|Docs Writer|docs writer` to confirm zero remaining references.

---

## Relationships to Sibling Plans

| Feature | Directory | Relationship |
|---------|-----------|--------------|
| 01-handoff-text-migration | `dev/feature/01-handoff-text-migration/` | **Prerequisite** — must be completed first. Both features modify `.github/agents/02-phase-refiner.agent.md`, `opencode/agents/02-phase-refiner.md`, and `claude/agents/phase-refiner.md`. The handoff text changes (Feature 01) go in the Pipeline Next Step section; this feature removes the Phase 7 section and updates the Pipeline Next Step header. These are different sections but in the same 3 files, so sequential ordering is required for clean diffs. |

**Suggested implementation order:** 01 → 02 (sequential within Phase 01).

---

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-only template repository — no runtime, no build system, no dependencies |
| Test Runner | Not applicable — no automated tests in this repo |
| Test Baseline | N/A — instruction files only; verification is via `git diff` and manual review |
| Lint | Not configured |
| Format | Not configured |

---

## Relevant Learnings

None applicable — the `.github/learnings/` directory does not exist in this repository.
