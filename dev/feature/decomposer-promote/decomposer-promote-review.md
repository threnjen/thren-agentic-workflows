# Review Record: decomposer-promote

## Summary
All 7 acceptance criteria are verified. The implementation cleanly promotes the feature-decomposer agent to user-facing `03 Feature - Decomposer` and scopes output to plan-only. One undocumented but correct change (removal of `model:` field) and expected cross-reference staleness in sibling agents. High confidence.

## Verdict
Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/agents/feature-decomposer.agent.md:2` | `name: 03 Feature - Decomposer` |
| AC2 | Verified | `.github/agents/feature-decomposer.agent.md:1-6` | `user-invocable: false` line removed; confirmed absent via grep |
| AC3 | Verified | `.github/agents/feature-decomposer.agent.md` (full body) | Grep for `context\.md\|tasks\.md` returns 0 matches; deliverables scoped to `-plan.md` only |
| AC4 | Verified | `.github/agents/feature-decomposer.agent.md:74` | Standalone handoff says `@04 Phase - Execute` |
| AC5 | Verified | `.github/agents/feature-decomposer.agent.md:65-69` | Subagent return says "plan files" and "one-line plan summary" |
| AC6 | Verified | `.github/instructions/read-only-agent.instructions.md:3` | `applyTo` includes `**/feature-decomposer.agent.md`; no changes made (correct) |
| AC7 | Verified | `.github/agents/feature-decomposer.agent.md:16,20,38,61,78` | `feature-plan-set` skill referenced 5 times |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | `model: "Claude Opus 4 (Copilot)"` removed from frontmatter — not listed in any AC or task | Low | `.github/agents/feature-decomposer.agent.md:1-6` | — | Wont-Fix |
| 2 | `phase-refiner.agent.md:33` still says "three-file Feature - Decomposer deliverable" — now stale | Low | `.github/agents/phase-refiner.agent.md:33` | — | Open |
| 3 | `phase-final-review.agent.md:29-31` still lists context/tasks as decomposer outputs — now stale | Low | `.github/agents/phase-final-review.agent.md:29-31` | — | Open |
| 4 | `phase-execute.agent.md:5,27` still references `Feature - Decomposer` (old name without number) | Low | `.github/agents/phase-execute.agent.md:5` | — | Open |

**Status values**: Fixed | Open | Wont-Fix

**Issue 1 rationale**: No other agent in the repo has a `model:` frontmatter field. Removing it aligns with codebase convention and lets VS Code use its default model. This is a correct deviation even though it wasn't explicitly planned.

**Issues 2–4 rationale**: These are cross-reference updates in other agents that the plan explicitly scopes out. The `plan-expander-create` and `executor-renumber` sibling features will handle these cascading updates.

## Fixes Applied

None — no Blocker, High, or Medium severity issues found.

## Remaining Concerns

- Issue #2–4: Cross-reference staleness in `phase-refiner`, `phase-final-review`, and `phase-execute` agents. Expected and scoped to sibling features (`plan-expander-create`, `executor-renumber`). These agents will be inconsistent until those features are implemented.

## Test Coverage Assessment

- No automated tests exist in this repo (Markdown-only)
- Manual verification approach:
  - T1 (agent picker): Requires VS Code runtime check — `name: 03 Feature - Decomposer` is set correctly
  - T2 (plan-only output): Body confirmed to reference only `-plan.md` as output
  - T3 (standalone handoff): Message confirmed to say `@04 Phase - Execute`
  - T4 (subagent mode): Return value section confirmed to describe plan-only output
  - T5 (read-only constraint): `read-only-agent.instructions.md` applyTo confirmed

## Risk Summary

- **Cross-reference gap**: Until `executor-renumber` ships, the executor's `agents:` list references `Feature - Decomposer` while the agent's name is now `03 Feature - Decomposer`. This may break subagent invocation in the interim. Accepted per plan — features are designed to be deployed together.
- **Model pinning removed**: Agent previously pinned to Claude Opus 4; now uses VS Code default. Low risk, consistent with all other agents.
