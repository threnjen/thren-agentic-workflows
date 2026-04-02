# QA Readiness Analysis: Phase 01 — Split Feature Decomposer from Phase Execute

**Date:** 2026-04-02
**Analyst:** Prod Code Review (automated)
**Verdict:** GO WITH CONDITIONS
**Documents Analyzed:** 20
**Findings:** 14 (0 blockers, 3 high, 8 medium, 3 low)

---

## Executive Summary

All 23 acceptance criteria across 3 features are fully implemented, reviewed, and covered by the consolidated QA plan. The 8 key modified files (`feature-decomposer.agent.md`, `feature-plan-expander.agent.md`, `phase-execute.agent.md`, `project-planner.agent.md`, `phase-refiner.agent.md`, `README.md`, `feature-plan-set/SKILL.md`, `dev-task-folder.instructions.md`) are internally consistent — no stale `03 Phase - Execute` references remain in `.github/`, the pipeline flow is coherent end-to-end, and name consistency checks pass across all frontmatter `name:` fields and `agents:` lists. All 14 findings are in downstream documentation files that were explicitly out of scope for all 3 feature plans (README.md subagent tables, ARCHITECTURE.md, CODEBASE_CONTEXT.md, `phase-final-review.agent.md`, `phase-refiner.agent.md` line 33). These must be resolved — primarily through the Docs Writer pass (pipeline Step 7) and targeted agent file fixes — before the branch is merged.

---

## Document Inventory

### Per-Feature Documents

**decomposer-promote:**

| Document | File | Source | Present | Notes |
|----------|------|--------|---------|-------|
| Feature Plan | `decomposer-promote-plan.md` | Feature - Decomposer | Yes | 7 ACs, 4 stages |
| Context | `decomposer-promote-context.md` | Feature - Plan Expander | Yes | 2 key files |
| Tasks | `decomposer-promote-tasks.md` | Feature - Plan Expander | Yes | 4 stages, 13 tasks |
| Implementation Record | `decomposer-promote-implementation.md` | Feature - Implementer | Yes | All 7 ACs Done/Verified |
| Review Record | `decomposer-promote-review.md` | Feature - Reviewer | Yes | Approved; 4 issues (1 Wont-Fix, 3 Open/out-of-scope) |

**plan-expander-create:**

| Document | File | Source | Present | Notes |
|----------|------|--------|---------|-------|
| Feature Plan | `plan-expander-create-plan.md` | Feature - Decomposer | Yes | 8 ACs, 3 stages |
| Context | `plan-expander-create-context.md` | Feature - Plan Expander | Yes | 3 key files, 3 reference files |
| Tasks | `plan-expander-create-tasks.md` | Feature - Plan Expander | Yes | 3 stages, 10 tasks |
| Implementation Record | `plan-expander-create-implementation.md` | Feature - Implementer | Yes | All 8 ACs Done |
| Review Record | `plan-expander-create-review.md` | Feature - Reviewer | Yes | Approved; 3 issues (all Low/Open/out-of-scope) |

**executor-renumber:**

| Document | File | Source | Present | Notes |
|----------|------|--------|---------|-------|
| Feature Plan | `executor-renumber-plan.md` | Feature - Decomposer | Yes | 8 ACs, 5 stages |
| Context | `executor-renumber-context.md` | Feature - Plan Expander | Yes | 4 key files, 3 reference files, cross-reference audit table |
| Tasks | `executor-renumber-tasks.md` | Feature - Plan Expander | Yes | 5 stages, 17 tasks |
| Implementation Record | `executor-renumber-implementation.md` | Feature - Implementer | Yes | All 8 ACs Done |
| Review Record | `executor-renumber-review.md` | Feature - Reviewer | Yes | Approved with Reservations; 4 issues (1 High Fixed, 1 Medium Open, 2 Low Open) |

**Consolidated QA Documents:**

| Document | File | Source | Present | Notes |
|----------|------|--------|---------|-------|
| QA Plan | `docs/phases/PHASE_01/PHASE_01_QA.md` | Feature - QA Writer | Yes | 5 manual QA sections, 27 checklist items |
| Coverage Map | `docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md` | Feature - QA Writer | Yes | 23 ACs mapped; 10 flagged for cross-cutting QA |

No missing or unexpected documents.

---

## Traceability Matrix

### decomposer-promote

| AC | Plan | Impl | Code | Review | In QA | Verdict |
|----|------|------|------|--------|-------|---------|
| AC1: Frontmatter name `03 Feature - Decomposer` | Defined | Done | Verified (`feature-decomposer.agent.md:2`) | Verified | Section 1 + Section 5 | OK |
| AC2: `user-invocable: false` removed | Defined | Done | Verified (field absent) | Verified | Section 1 + Section 5 | OK |
| AC3: Output scoped to `-plan.md` only | Defined | Done | Verified (grep: 0 matches for `context.md`/`tasks.md`) | Verified | Section 3 | OK |
| AC4: Standalone references `@04 Phase - Execute` | Defined | Done | Verified (`feature-decomposer.agent.md:74`) | Verified | Section 2 | OK |
| AC5: Subagent return value plan-only | Defined | Done | Verified (`feature-decomposer.agent.md:65-69`) | Verified | Section 5 | OK |
| AC6: `read-only-agent.instructions.md` applyTo | Defined | Verified | Verified (applyTo includes `**/feature-decomposer.agent.md`) | Verified | Section 3 | OK |
| AC7: `feature-plan-set` skill reference intact | Defined | Verified | Verified (5 references in agent body) | Verified | Section 3 | OK |

### plan-expander-create

| AC | Plan | Impl | Code | Review | In QA | Verdict |
|----|------|------|------|--------|-------|---------|
| AC1: Agent file exists | Defined | Done | Verified (`feature-plan-expander.agent.md` exists) | Verified | Section 5 | OK |
| AC2: Frontmatter correct | Defined | Done | Verified (name, tools, user-invocable, model) | Verified | Section 1 + Section 5 | OK |
| AC3: Reads plans, generates context + tasks | Defined | Done | Verified (workflow Steps 1-4) | Verified | Section 5 | OK |
| AC4: Context generation instructions | Defined | Done | Verified (Step 3 details) | Verified | Section 5 | OK |
| AC5: Tasks generation instructions | Defined | Done | Verified (Step 4 details) | Verified | Section 5 | OK |
| AC6: Subagent mode support | Defined | Done | Verified (`user-invocable: false`, autonomous) | Verified | Section 5 | OK |
| AC7: Skill updated for split ownership | Defined | Done | Verified (`feature-plan-set/SKILL.md:8`) | Verified | Section 3 | OK |
| AC8: Instruction producer table updated | Defined | Done | Verified (`dev-task-folder.instructions.md:15-16`) | Verified | Section 3 | OK |

### executor-renumber

| AC | Plan | Impl | Code | Review | In QA | Verdict |
|----|------|------|------|--------|-------|---------|
| AC1: Frontmatter name `04 Phase - Execute` | Defined | Done | Verified (`phase-execute.agent.md:2`) | Verified | Section 1 | OK |
| AC2: `agents:` includes Plan Expander + Decomposer | Defined | Done | Verified (`phase-execute.agent.md:5`) | Verified | Section 1 + Section 5 | OK |
| AC3: Step 1 plan check + conditional Decomposer | Defined | Done | Verified (`phase-execute.agent.md:22-40`) | Verified | Section 2 | OK |
| AC4: Plan Expander invocation step | Defined | Done | Verified (`phase-execute.agent.md:42-55`) | Verified | Section 2 | OK |
| AC5: `orchestrator-conventions.instructions.md` applyTo | Defined | Verified | Verified (applyTo includes `**/phase-execute.agent.md`) | Verified | Section 3 | OK |
| AC6: `project-planner.agent.md` refs → `@04` | Defined | Done | Verified (grep: 0 `@03 Phase` in `.github/`) | Verified | Section 1 + Section 2 | OK |
| AC7: `phase-refiner.agent.md` refs → `@04` | Defined | Done | Verified (3 references updated) | Verified | Section 1 + Section 2 | OK |
| AC8: Pipeline diagram updated | Defined | Done | Verified (`project-planner.agent.md:21-28`) | Verified | Section 2 | OK |

**All 23 ACs: OK**

---

## Findings

### Cross-Document Issues

| # | Finding | Severity | Documents Involved | Evidence | Recommendation |
|---|---------|----------|--------------------|----------|----------------|
| 1 | README.md User-Facing table missing `03 Feature - Decomposer` | High | `README.md` (line 116-128), `feature-decomposer.agent.md` | Decomposer was promoted to user-facing but never added to the User-Facing agents table. Table jumps from `02 Phase - Refiner` to `04 Phase - Execute`. | Add `03 Feature - Decomposer` row to User-Facing table |
| 2 | README.md Hidden Subagents table: `Feature - Plan Expander` missing | High | `README.md` (line 130-150), `feature-plan-expander.agent.md` | New hidden subagent not listed in the table at all | Add `Feature - Plan Expander` row: invoked by Phase - Execute |
| 3 | README.md Task Documentation Pattern: stale producer for `-context.md` / `-tasks.md` | High | `README.md` (lines 275-276), `dev-task-folder.instructions.md` | Both lines attribute context and tasks to `Feature - Decomposer`; should be `Feature - Plan Expander` | Update annotations to `Feature - Plan Expander` |
| 4 | `phase-final-review.agent.md`: Required Inputs table attributes context + tasks to `Feature - Decomposer` | Medium | `phase-final-review.agent.md` (lines 29-31) | Context and Task rows list `Feature - Decomposer` as source agent | Change to `Feature - Plan Expander` |
| 5 | `phase-final-review.agent.md`: Document Inventory template stale | Medium | `phase-final-review.agent.md` (lines 181-183) | Same stale attribution in the output template table | Change source column to `Feature - Plan Expander` for Context and Tasks rows |
| 6 | `phase-refiner.agent.md` line 33: "three-file Feature - Decomposer deliverable" stale | Medium | `phase-refiner.agent.md`, `feature-decomposer.agent.md` | Decomposer now produces only `-plan.md`; context + tasks are from Plan Expander | Rewrite as "the Feature - Decomposer plan (`-plan.md`)" or similar |
| 7 | README.md ASCII pipeline diagram missing Plan Expander step | Medium | `README.md` (lines 42-52), `phase-execute.agent.md` | Automated subagent flow shows Decomposer → implementation loop with no Plan Expander in between. Also says "Plan sets" (implying 3-file output) | Add `Feature - Plan Expander → Context + tasks` line; change "Plan sets" to "Plan files" |
| 8 | README.md Hidden Subagents: `Feature - Decomposer` misclassified | Medium | `README.md` (line 137), `feature-decomposer.agent.md` | Listed as hidden-only with no number prefix. Now user-facing as `03 Feature - Decomposer` (dual-use like Docs Writer) | Move to User-Facing table or annotate as dual-use; use correct name `03 Feature - Decomposer` |
| 9 | README.md Skills table: `feature-plan-set` used-by column incomplete | Medium | `README.md` (line 323), `feature-plan-expander.agent.md` | Lists only `Feature - Decomposer`; Plan Expander also loads this skill | Add `Feature - Plan Expander` to "Used By" |
| 10 | ARCHITECTURE.md: Stale `03 Phase - Execute` + missing Plan Expander | Medium | `docs/ARCHITECTURE.md` (lines 91, 95, 100) | Mermaid diagram uses `03 Phase - Execute`, omits `Feature - Plan Expander`, says "20 agent definitions" | Update to `04 Phase - Execute`, add Plan Expander node, fix count to 21 |
| 11 | CODEBASE_CONTEXT.md: Stale `03 Phase - Execute` reference | Medium | `docs/CODEBASE_CONTEXT.md` (line 64) | Lists `03 Phase - Execute` as an orchestrator name | Update to `04 Phase - Execute` |
| 12 | CODEBASE_CONTEXT.md: Agent count stale | Low | `docs/CODEBASE_CONTEXT.md` (line 9) | Says "20 agent definitions (9 user-facing, 11 hidden)"; should be 21 (10 user-facing, 11 hidden) | Update counts |
| 13 | `model:` field inconsistency between Decomposer and Plan Expander | Low | `feature-plan-expander.agent.md:5`, `feature-decomposer.agent.md` | Plan Expander has `model: <model>`; Decomposer removed its model field. No other agent has `model:` in frontmatter. | Remove `model:` from Plan Expander to match convention, or document the inconsistency |
| 14 | README.md Decomposer description says "Plan sets" | Low | `README.md` (line 44) | ASCII diagram: "Feature - Decomposer → Plan sets for each feature". Should reflect plan-only output | Change "Plan sets" to "Plan files" |

### Implementation Issues

| # | Finding | Severity | File:Line | Evidence | Recommendation |
|---|---------|----------|-----------|----------|----------------|
| — | None | — | — | All 8 key modified files inspected; no issues found beyond what reviews documented | — |

### QA Plan Issues

| # | Finding | Severity | QA Item | Evidence | Recommendation |
|---|---------|----------|---------|----------|----------------|
| 1 | QA plan Section 4 does not flag ARCHITECTURE.md stale references | Medium | — | `docs/ARCHITECTURE.md:91,95,100` has `03 Phase - Execute` and missing Plan Expander node; not mentioned in QA checklist | Add ARCHITECTURE.md verification to Section 4 |
| 2 | QA plan Section 4 does not flag README.md Skills table gap | Low | — | `README.md:323` lists only `Feature - Decomposer` for `feature-plan-set` skill; not mentioned in QA checklist | Add Skills table verification to Section 4 |
| 3 | QA plan Section 4 does not flag CODEBASE_CONTEXT.md `03 Phase - Execute` reference | Low | — | `CODEBASE_CONTEXT.md:64` still says `03 Phase - Execute`; only the agent count is flagged, not the stale name | Add name reference check to CODEBASE_CONTEXT.md item |

---

## Risk Register

| # | Risk | Likelihood | Impact | QA Detection | Recommendation |
|---|------|-----------|--------|--------------|----------------|
| 1 | Users can't find `03 Feature - Decomposer` in README docs | Certain | High | Yes (Section 4) | Update README.md User-Facing table before merge |
| 2 | Users don't know Plan Expander exists | Certain | High | Yes (Section 4) | Add to README.md Hidden Subagents table |
| 3 | Prod Code Review agent uses stale producer attributions | High | Medium | Yes (Section 4) | Update `phase-final-review.agent.md` tables |
| 4 | Phase Refiner tells users Decomposer produces 3 files | High | Medium | Partially (not in QA) | Update `phase-refiner.agent.md` line 33 |
| 5 | ARCHITECTURE.md Mermaid diagram misleads about pipeline | High | Medium | No | Update ARCHITECTURE.md |
| 6 | CODEBASE_CONTEXT.md bootstraps agents with wrong name/count | Medium | Low | Partially | Update CODEBASE_CONTEXT.md |
| 7 | Plan Expander `model:` field inconsistent with all other agents | Low | Low | No | Remove `model:` from Plan Expander or document |

---

## Conditions (GO WITH CONDITIONS)

1. **README.md must be updated before merge** — Add `03 Feature - Decomposer` to User-Facing table; add `Feature - Plan Expander` to Hidden Subagents table; update ASCII pipeline diagram with Plan Expander step; fix Task Documentation Pattern attributions (lines 275-276); update Skills table (line 323); fix "Plan sets" → "Plan files" (line 44); update Feature - Decomposer description to reflect dual-use and plan-only scope. **Expected handler:** Docs Writer (pipeline Step 7).

2. **`phase-final-review.agent.md` must be updated before merge** — Change context and tasks producer from `Feature - Decomposer` to `Feature - Plan Expander` in both the Required Inputs table (lines 29-31) and Document Inventory template (lines 181-183). **Expected handler:** Manual fix or Docs Writer. This is an agent definition file, so the Docs Writer may not catch it — verify after Step 7.

3. **`phase-refiner.agent.md` line 33 must be updated before merge** — Change "three-file Feature - Decomposer deliverable (`-plan.md`, `-context.md`, `-tasks.md`)" to reflect the Decomposer produces only `-plan.md`. **Expected handler:** Manual fix or Docs Writer.

4. **ARCHITECTURE.md must be updated before merge** — Change `03 Phase - Execute` to `04 Phase - Execute` in the Mermaid diagram; add `Feature - Plan Expander` node to the Phase - Execute subagent list; update "20 agent definitions" to 21. **Expected handler:** Docs Writer (pipeline Step 7).

5. **CODEBASE_CONTEXT.md must be updated before merge** — Change `03 Phase - Execute` to `04 Phase - Execute` (line 64); update agent count from 20 to 21 and user-facing/hidden split (line 9). **Expected handler:** Docs Writer (pipeline Step 7).

6. **`model:` field inconsistency should be resolved** — Either remove `model: <model>` from `feature-plan-expander.agent.md` (to match convention: no other agent has a `model:` field) or add it to all agents. Low priority but creates a precedent inconsistency. **Expected handler:** Manual fix.

---

## Recommendations

Ordered by priority:

1. **Run the Docs Writer** (pipeline Step 7) — This should resolve conditions 1, 4, and 5 automatically. After the Docs Writer completes, re-verify that README.md, ARCHITECTURE.md, and CODEBASE_CONTEXT.md are fully updated.

2. **Manually fix `phase-final-review.agent.md`** — Update the two producer attribution tables (lines 29-31, 181-183). The Docs Writer is unlikely to catch this because it's an agent behavior definition, not external documentation.

3. **Manually fix `phase-refiner.agent.md` line 33** — Update the stale "three-file" reference. Same rationale — this is agent behavior text.

4. **Remove `model: <model>` from `feature-plan-expander.agent.md`** — Aligns with codebase convention. Every other agent (including the just-promoted Decomposer) omits this field.

5. **After the Docs Writer pass, re-run QA checklist Section 4** — Verify all stale references are resolved. If any remain, fix manually before opening the PR.
