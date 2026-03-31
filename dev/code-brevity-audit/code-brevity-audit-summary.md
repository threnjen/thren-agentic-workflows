# Code Brevity Audit — Executive Summary

**Date:** 2026-03-30
**Scope:** `.github/agents/`, `.github/skills/`, `.github/instructions/` (31 files)

## Verdict

The agent/skill/instruction system is well-architected with good use of shared files, but **~1,550 words (~2,000–2,500 tokens)** of redundant content has accumulated. The main sources are: (1) agents restating constraints already injected by auto-loaded instruction files, (2) orchestrators re-implementing shared procedures instead of referencing conventions, and (3) verbose prose in the longest files.

## Findings by Severity

| Severity | Count | Est. Word Savings | Key Themes |
|----------|-------|-------------------|------------|
| **HIGH** | 4 | ~470 words | Branch logic triplicated; read-only constraints restated in 4 agents; phase-refiner verbosity |
| **MEDIUM** | 10 | ~680 words | QA path duplication; skill "When to Use" sections; orchestrator constraints; verbose prose |
| **LOW** | 12 | ~400 words | Minor prose, formatting, and partial duplication |
| **Total** | **26** | **~1,550 words** | |

## Top 5 Priority Actions

1. **Remove restated read-only constraints from 4 agents** — `project-planner`, `phase-refiner`, `feature-decomposer`, `test-analyst` all restate "You NEVER touch the codebase" despite `read-only-agent.instructions.md` auto-loading. **~160 words saved. Effort: 15 min.**

2. **Consolidate branch creation into `orchestrator-conventions.instructions.md`** — All 3 orchestrators repeat the full branch creation procedure (~10 lines each). Move the shared procedure to the instruction file; orchestrators specify only their prefix. **~150 words saved. Effort: 20 min.**

3. **Tighten `phase-refiner.agent.md`** — The longest agent file (~250 lines). Compress the ASCII pipeline diagram, condense the Question Triage section, and tighten the 7 Iteration Focus Areas. **~280 words saved. Effort: 30 min.**

4. **Add orchestrator constraints to shared instruction** — "DO NOT write code/tests/config directly" is restated in all 3 orchestrators. Move to `orchestrator-conventions.instructions.md`. **~90 words saved. Effort: 10 min.**

5. **Remove "When to Use" sections from all 5 skills** — Every skill repeats its frontmatter description in a "When to Use" section. The description is already surfaced by the skill-loading mechanism. **~75 words saved. Effort: 10 min.**

## Files Most Needing Reduction

| File | Current Size | Estimated Reducible | Primary Issues |
|------|-------------|---------------------|----------------|
| `phase-refiner.agent.md` | ~250 lines | ~60 lines | Verbose prose, large ASCII diagram, restated constraints |
| `phase-execute.agent.md` | ~120 lines | ~20 lines | Branch + QA path duplication, GO/NO-GO templates |
| `audit-code-or-infra.agent.md` | ~170 lines | ~25 lines | Branch duplication, GO/NO-GO templates, QA paths |
| `project-planner.agent.md` | ~170 lines | ~20 lines | Restated constraints, verbose explanation paragraphs |
| `test-orchestrator.agent.md` | ~130 lines | ~15 lines | Branch duplication, restated constraints |

## Risks if Unaddressed

- **Context window waste**: ~2,000–2,500 tokens of redundant content are loaded into agent context when auto-loaded instructions already provide the same constraints. This competes with user prompts and codebase context for the model's attention budget.
- **Maintenance drift**: Duplicated content must be updated in multiple places when conventions change (e.g., branch naming rules), increasing the risk of inconsistency.

## Full Report

See [code-brevity-audit-report.md](code-brevity-audit-report.md) for all 26 findings with exact file/line references, detailed explanations, and estimated savings.
