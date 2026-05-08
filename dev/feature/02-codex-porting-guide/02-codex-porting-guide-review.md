# Review Record: 02 Codex Porting Guide

## Summary

`codex/CODEX_PORTING_GUIDE.md` is well-structured and satisfies all six acceptance criteria. All three `.github/` source surfaces (instructions, agents, skills) have documented Codex targets, transformation rules, portability classifications, and example tables. The global AGENTS rule is prominent and repeated. The main correctable issue was that the agents section implicitly scoped agent identification to `*.agent.md` filenames only, which would cause a porter to miss `prod-code-review.md` — a valid agent definition using a plain `.md` extension. One fix was applied directly.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1: instructions → global AGENTS + `developer_instructions` | Satisfied | `CODEX_PORTING_GUIDE.md` §Instructions | Split-destination routing, `applyTo` rewrite guidance, and portability notes all present |
| AC2: agents → Codex custom-agent TOML | Satisfied (fixed) | `CODEX_PORTING_GUIDE.md` §Agents | Required fields named correctly; fix applied to cover non-`*.agent.md` agent definitions |
| AC3: skills → Codex skill directories | Satisfied | `CODEX_PORTING_GUIDE.md` §Skills | `SKILL.md` required, optional assets covered, runtime vs. source separation clear |
| AC4: portability classification | Satisfied | `CODEX_PORTING_GUIDE.md` §Portability Classification | Three-tier table (Portable / Requires transformation / GitHub-only or non-portable) with examples for each surface |
| AC5: global AGENTS rule explicit | Satisfied | `CODEX_PORTING_GUIDE.md` §Core Rule, §Final Guardrails | Stated prominently at top and repeated in guardrails |
| AC6: landing zone references `codex/README.md` | Satisfied | `CODEX_PORTING_GUIDE.md` §Repository-Owned Landing Zone, §Porting Workflow step 3 | Both prose and workflow reference `codex/README.md` explicitly |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Agents section destination model specified `*.agent.md` glob, causing `prod-code-review.md` (a valid agent definition with plain `.md` extension) to be silently excluded from porting scope | Medium | `codex/CODEX_PORTING_GUIDE.md` §Agents / Destination Model | AC2 | Fixed |
| 2 | Documentation files in `.github/agents/` (`README.md`, `PORTING_GUIDE.md`, `TOOL_MAPPING.md`) were unclassified — ambiguous whether to create TOML files from them or treat them as docs | Low | `codex/CODEX_PORTING_GUIDE.md` §Agents / Destination Model | AC2 | Fixed (included in same fix as issue 1) |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `codex/CODEX_PORTING_GUIDE.md` | Rewrote Agents Destination Model paragraph to identify agent definitions by YAML frontmatter presence rather than `*.agent.md` glob; added explicit callout that `prod-code-review.md` is an agent definition; added explicit callout that `README.md`, `PORTING_GUIDE.md`, and `TOOL_MAPPING.md` are documentation files that map to `codex/` docs, not TOML | 1, 2 |

## Remaining Concerns

- No automated documentation validation exists for this guide. Manual mapping review against the live `.github/` tree is the only verification surface. A future docs-check harness would make AC traceability auditable without manual inspection.

## Test Coverage Assessment

- Covered: AC1, AC2, AC3, AC4, AC5, AC6 — all verified by manual mapping audit against live `.github/` tree, `CODEX_PLATFORM_REFERENCE.md`, and `codex/README.md`
- Missing: No automated test harness. All verification is manual per the implementation record's documented deviation.

## Risk Summary

- `codex/CODEX_PORTING_GUIDE.md` — complex split-destination routing for instructions; manually verified against all 13 `.github/instructions/` files but no automated coverage
- No executable tests: correctness depends entirely on keeping the guide synchronized with live `.github/` tree and upstream Codex platform behavior — revalidation gates are informal
