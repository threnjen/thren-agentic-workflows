# Review Record: 04 Commit Instrumentation

## Summary

Reviewed the current rework against the task plan, the prior review findings, and the mirrored OpenCode and Claude copies. The refiner and decomposer checkpoint-scope problems from the prior review are resolved in the current files. One high-severity requirement mismatch remains in the execute orchestrator: QA and final-review checkpoints are still modeled as consolidated phase-level commits instead of per-feature checkpoints inside each feature cycle.

## Verdict

Changes Requested

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Implemented | `.github/agents/01-project-planner.agent.md:105`; `opencode/agents/01-project-planner.md:121`; `claude/agents/project-planner.md:106` | All three variants document `eval: affirm plan` inline after plan affirmation. |
| AC2 | Implemented | `.github/agents/02-phase-refiner.agent.md:193`; `opencode/agents/02-phase-refiner.md:211`; `claude/agents/phase-refiner.md:176` | All three variants stage the phase docs plus the target repo `.gitignore` when Step 6 appends `eval/runs/`. |
| AC3 | Implemented | `.github/agents/03-feature-decomposer.agent.md:94`; `opencode/agents/03-feature-decomposer.md:97`; `claude/agents/feature-decomposer.md:99` | All three variants derive the phase slug and stage created or modified feature-plan files. |
| AC4 | Partial | `.github/agents/04-phase-execute.agent.md:92`; `.github/agents/04-phase-execute.agent.md:96`; `.github/agents/04-phase-execute.agent.md:98`; `.github/agents/04-phase-execute.agent.md:150`; `.github/agents/04-phase-execute.agent.md:180` | Implement and review checkpoints are per-feature, but QA and final-review checkpoints are deferred to consolidated phase-level steps. |
| AC5 | Divergent | `.github/agents/04-phase-execute.agent.md:98`; `.github/agents/04-phase-execute.agent.md:127`; `.github/agents/04-phase-execute.agent.md:150`; mirrored in `opencode/agents/04-phase-execute.md` and `claude/agents/phase-execute.md` | The documented QA and final-review staging scope is phase-level, not feature-local as required. |
| AC6 | Implemented | `.github/agents/01-project-planner.agent.md:105`; `.github/agents/02-phase-refiner.agent.md:193`; `.github/agents/03-feature-decomposer.agent.md:94`; `.github/agents/04-phase-execute.agent.md:92` | Exact `eval:` message formats are defined inline in each agent. |
| AC7 | Implemented | `opencode/agents/01-project-planner.md:121`; `opencode/agents/02-phase-refiner.md:211`; `opencode/agents/03-feature-decomposer.md:97`; `opencode/agents/04-phase-execute.md:95`; `claude/agents/project-planner.md:106`; `claude/agents/phase-refiner.md:176`; `claude/agents/feature-decomposer.md:99`; `claude/agents/phase-execute.md:91` | The current wording is propagated across all eight live copies. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | The execute orchestrator still defers QA and final-review checkpoints to phase-level steps, using shared QA outputs and phase-wide staging. That design cannot satisfy the plan's requirement for per-feature `eval: qa <task>` and per-feature-scoped checkpointing inside each feature cycle. | High | `.github/agents/04-phase-execute.agent.md:98`; `.github/agents/04-phase-execute.agent.md:127`; `.github/agents/04-phase-execute.agent.md:150`; `.github/agents/04-phase-execute.agent.md:180` | AC4, AC5 | Open |

## Fixes Applied

None

## Remaining Concerns

- Issue #1: closing this gap requires changing the execute orchestrator's QA/final-review checkpoint model, not just wording. The current rework still routes those commits through shared phase-level artifacts.

## Test Coverage Assessment

- Covered: AC1, AC2, AC3, AC6, AC7 via targeted searches and targeted git diffs across the master and mirrored agent files.
- Missing: No executable validation exists for AC4 and AC5 beyond document inspection because the mismatch is in the orchestration design itself.

## Risk Summary

- `.github/agents/04-phase-execute.agent.md:98` explicitly removes QA and final-review commits from the per-feature loop, so the implementation no longer matches the accepted plan contract.
- `.github/agents/04-phase-execute.agent.md:150` commits shared QA artifacts at phase scope, which prevents feature-local staging for any phase with more than one feature.
- `.github/agents/04-phase-execute.agent.md:180` emits a single phase-level `eval: final-review` commit, so downstream ledger consumers cannot correlate final-review checkpoints to individual feature cycles.