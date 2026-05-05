# Implementation Record: 04 Ledger Annotation

## Summary

Implemented ledger-event annotation instructions for the reviewer, implementer, and debugger agent definitions in the master `.github/agents/` directory and propagated the same behavior to the OpenCode and Claude copies. Each new block now documents the `phase/*` branch guard, phase-slug derivation, `eval/runs/<phase-slug>/ledger-events.jsonl` target path, `mkdir -p` plus `>>` append semantics, and the full required event schema with the agent-specific `stage` and `detected_by` values.

## Sibling Features

- `01-model-unpinning` is earlier wave foundation work and does not share files with this feature.
- `02-hook-template` provides the hook-written ledger side but does not overlap this feature's agent files.
- `03-branch-lifecycle-migration` establishes the `phase/*` branch workflow and `eval/runs/<phase-slug>/` directory this feature writes into.
- `04-commit-instrumentation` runs in the same wave but is explicitly disjoint; it modifies planner/refiner/phase-execute files while this feature modifies reviewer/implementer/debugger files.
- `05-eval-grader-agent` consumes the semantic event data produced by this feature.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `04c Feature - Reviewer` writes a ledger event for `Changes Requested` with reviewer metadata | Done | `.github/agents/04c-feature-reviewer.agent.md`, `opencode/agents/04c-feature-reviewer.md`, `claude/agents/z-feature-reviewer.md` | Added a reviewer-only ledger block that explicitly excludes `Approved` and `Approved with Reservations`. |
| AC2 | `04b Feature - Implementer` writes a ledger event for failing tests or unresolvable issues | Done | `.github/agents/04b-feature-implementer.agent.md`, `opencode/agents/04b-feature-implementer.md`, `claude/agents/z-feature-implementer.md` | Added a blocking-failure-only ledger block and kept it out of routine Red-Green-Refactor flow. |
| AC3 | `Debugger` writes a user-discovered ledger event before its first commit on `phase/*` branches | Done | `.github/agents/debugger.agent.md`, `opencode/agents/debugger.md`, `claude/agents/debugger.md` | Inserted Step 1a immediately after triage and before diagnosis/fixes. |
| AC4 | Every ledger row includes the full required schema | Done | All 9 files above | Each new block lists `task_slug`, `harness`, `model`, `stage`, `detected_by`, `severity`, `evidence`, `first_seen_attempt`, `resolved_attempt`, `resolved_by`, `human_intervention_required`, `regression`, and `propagated_from_stage`. |
| AC5 | All agents target `eval/runs/<phase-slug>/ledger-events.jsonl` | Done | All 9 files above | Verified by targeted search across all modified files. |
| AC6 | Phase slug is derived from the current branch by stripping `phase/` and replacing `/` with `-` | Done | All 9 files above | Present in each ledger instruction block. |
| AC7 | Non-`phase/*` branches skip ledger writing silently | Done | All 9 files above | Present in each ledger instruction block. |
| AC8 | Changes propagated to OpenCode and Claude copies | Done | `opencode/agents/*`, `claude/agents/*` files listed above | Verified by readback and targeted searches across the derived copies. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/04c-feature-reviewer.agent.md` | Modify | Added a `Ledger Annotation for Changes Requested` block in the reviewer return path | Satisfies AC1 and AC4-AC7 in the source-of-truth reviewer definition |
| `.github/agents/04b-feature-implementer.agent.md` | Modify | Added a `Ledger Annotation for Blocking Failures` block before deliverables | Satisfies AC2 and AC4-AC7 in the source-of-truth implementer definition |
| `.github/agents/debugger.agent.md` | Modify | Inserted Step 1a for user-discovered phase-branch annotation before diagnosis/fixes | Satisfies AC3 and AC4-AC7 in the source-of-truth debugger definition |
| `opencode/agents/04c-feature-reviewer.md` | Modify | Mirrored reviewer ledger annotation block | Satisfies AC8 for OpenCode reviewer parity |
| `opencode/agents/04b-feature-implementer.md` | Modify | Mirrored implementer ledger annotation block | Satisfies AC8 for OpenCode implementer parity |
| `opencode/agents/debugger.md` | Modify | Mirrored debugger Step 1a ledger annotation block | Satisfies AC8 for OpenCode debugger parity |
| `claude/agents/z-feature-reviewer.md` | Modify | Mirrored reviewer ledger annotation block | Satisfies AC8 for Claude reviewer parity |
| `claude/agents/z-feature-implementer.md` | Modify | Mirrored implementer ledger annotation block | Satisfies AC8 for Claude implementer parity |
| `claude/agents/debugger.md` | Modify | Mirrored debugger Step 1a ledger annotation block | Satisfies AC8 for Claude debugger parity |
| `dev/feature/04-ledger-annotation/04-ledger-annotation-implementation.md` | Add | Wrote the implementation record artifact | Required deliverable for downstream review |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated tests exist for this Markdown agent-definition slice | Validation used targeted searches, readback, and scoped diff review |

## Test Results

- **Baseline**: No tests found (before implementation)
- **Final**: No tests found (after implementation)
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

None

## Gaps

None

## Reviewer Focus Areas

- Verify the reviewer ledger block remains confined to the `Changes Requested` path and still excludes approved verdicts in `.github/agents/04c-feature-reviewer.agent.md`.
- Verify the implementer ledger block is interpreted as a blocking-return instruction, not as part of routine Red-Green-Refactor iterations, in `.github/agents/04b-feature-implementer.agent.md`.
- Verify debugger Step 1a in `.github/agents/debugger.agent.md` is clearly ordered before diagnosis, fixes, and any first commit on `phase/*` branches.
- Verify the nine modified files stay textually aligned on path, branch-guard, and schema wording across `.github/agents/`, `opencode/agents/`, and `claude/agents/`.