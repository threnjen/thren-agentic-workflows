# Implementation Record: 02-final-review-orchestrator

## Summary

Implemented AC1–AC8 for the Phase Final Review orchestrator. Added the
numbered orchestrator source asset, explicit context and return-summary
contracts, ledger-first baseline preflight with a commit-message fallback,
subphase and artifact gates, model-tier assignments, partial-failure handling,
deterministic report retention, verdict write-back rules, and full re-run
policy. Updated the user-facing agent inventory and propagated the new agent
to the repository's Claude, OpenCode, and Codex outputs.

The final report-retention decision is
`dev/phase-final-review/PHASE_0N/runs/<UTC-YYYYMMDDTHHMMSSZ>-<sequence>/` for
archived prior runs, while the active run keeps the canonical report filenames
at the phase report root.

## Sibling Features

Read the first five lines of sibling plans before implementation:
`01-review-foundation` (Wave 1), `03-mechanical-evaluators` (Wave 3),
`04-delegating-evaluators` (Wave 4), `05-deep-judgment-evaluators` (Wave 5),
and `06-readiness-synthesis` (Wave 6). This feature consumes feature 01's
conventions, report templates, baseline procedure, and fixture; features 03–06
consume this orchestrator's invocation and not-run contracts. No sibling
feature files were modified. Propagated agent outputs and the shared inventory
are the only cross-feature seams.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | The numbered Phase Final Review orchestrator exists, follows the `04-phase-execute` house style, and loads `phase-final-review-conventions`. | Complete | `.github/agents/05-phase-final-review.agent.md` | Source-of-truth asset uses the required `name`, `description`, `tools`, and `agents` frontmatter. |
| AC2 | The orchestrator enforces context discipline and the ≤10-line return-summary contract. | Complete | `.github/agents/05-phase-final-review.agent.md` | It reads only report paths/metadata and structured reports; evaluators receive the ≤10-line contract. |
| AC3 | Preflight suggests a confirmed baseline from valid ledgers, with a named first-class `eval:` fallback and candidate selection when exhausted. | Complete | `.github/agents/05-phase-final-review.agent.md` | Empty/malformed ledgers fall back; `ledger-events.jsonl` is optional. |
| AC4 | Preflight discovers subphases and refuses with itemized missing-artifact results. | Complete | `.github/agents/05-phase-final-review.agent.md` | Uses `PHASE_0N*/`, rejects zero subphases with the `prod-code-review` boundary, and applies the conventions skill's readable/non-empty artifact definition. |
| AC5 | Startup warns for non-state-of-the-art models and declares deep versus mechanical tiers. | Complete | `.github/agents/05-phase-final-review.agent.md` | `05b`, `05e`, `05f`, and `05l` are top-tier; `05g`, `05j`, and `05k` are cheap-tier. |
| AC6 | Evaluator failures and hangs do not abort the run and cannot produce a false GO. | Complete | `.github/agents/05-phase-final-review.agent.md` | Bounded waits, `evaluator-status.jsonl`, failure propagation to 05l, and the required Checks Not Run ceiling are explicit. |
| AC7 | Verdict lifecycle updates only the target roadmap/summary status lines and requires a full re-run after remediation. | Complete | `.github/agents/05-phase-final-review.agent.md` | Ambiguous status lines are left unchanged; no partial re-run machinery is defined. |
| AC8 | Inventory and propagation include the new user-facing agent and existing propagation tests pass. | Complete | `.github/agents/README.md`; generated Claude/OpenCode/Codex outputs; `tests/test_propagate_master_assets.py` | Propagation produced the Claude command, OpenCode agent, Codex agent, and Codex profile without script changes. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05-phase-final-review.agent.md` | Create | Added the orchestrator role, context boundaries, baseline/subphase/artifact preflight, model tiers, evaluator prompt shape, not-run JSONL record, failure semantics, report archival, verdict write-back, and full re-run policy. | AC1–AC7. |
| `.github/agents/README.md` | Modify | Added `05 Phase - Final Review` to the user-facing inventory, detailed agent descriptions, and orchestrator summary. | AC8 and inventory-surface consistency. |
| `claude/commands/phase-final-review.md` | Generated | Propagated the user-facing orchestrator as a Claude command. | AC8. |
| `opencode/agents/05-phase-final-review.md` | Generated | Propagated the orchestrator to OpenCode. | AC8. |
| `codex/agents/05-phase-final-review.toml` | Generated | Propagated the orchestrator to Codex. | AC8. |
| `codex/profiles/phase-final-review.config.toml` | Generated | Added the Codex user-facing profile generated from the source agent. | AC8. |
| `dev/feature/02-final-review-orchestrator/02-final-review-orchestrator-tasks.md` | Modify | Checked off completed prerequisite, implementation, propagation, and manual-QA tasks. | Required pipeline handoff state. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Read-only verification | Existing propagation suite executed; no test source changed. | AC8 propagation behavior. |
| None added | Not applicable | The plan defines markdown/manual evidence for AC1–AC7 and an existing propagation suite for AC8. | Static contract checks and manual QA evidence are recorded below. |

## Test Results

- **Baseline**: 386 passed, 2 failed, 2 subtests (before implementation).
- **Final**: 386 passed, 2 failed, 2 subtests (after implementation).
- **New tests added**: 0
- **Targeted propagation**: 19 passed, 0 failed, 2 subtests.
- **Regressions**: None. The same pre-existing failures remained in `tests/hooks/test_hook_distribution_integration.py`: AC9 propagated-guard median latency and AC7 installation-guide classifications.

The ambient `python3 -m pytest tests/ -q` command could not start because
pytest is not installed in the ambient interpreter. The repository's existing
`.venv` was used for both baseline and final runs; no dependency or environment
file was changed.

Manual QA checks passed:

1. Ledger path found the first feature checkpoint
   `291fc8a0c437e3014a09a9a3709157d0e597f81e` and suggested baseline
   `48d37504bf7a59d29358a512cd4183c3f0fe0996`.
2. Ledger-absent fallback found the same phase-local `eval: implement
   01-review-foundation` checkpoint and its parent.
3. A temporary fixture copy with one QA document removed produced an itemized
   missing-artifact result.
4. The non-state-of-the-art warning appears before work and tier assignment.
5. A simulated evaluator failure is persisted, passed to 05l, and blocks GO.

## Deviations from Plan

- The repository's propagator emits user-facing agents as
  `claude/commands/phase-final-review.md`, `opencode/agents/05-phase-final-review.md`,
  and Codex agent/profile files; it does not create a
  `.claude/agents/` output. This matches the existing propagation behavior and
  feature 01's recorded destination convention. `scripts/propagate_master_assets.py`
  was not modified.
- The feature-01 fixture explicitly documents that source implementation
  records were not retained. The orchestrator inventories that category but
  honors only an explicit fixture/pipeline provenance exception, never an empty
  directory.

## Gaps

- A live 05a–05l agent spawn was unavailable in this execution harness.
  Preflight, wrong-model, and evaluator-failure behavior were validated through
  static and temporary-fixture QA checks; downstream evaluator runtime behavior
  remains for the later feature dry runs.

## Reviewer Focus Areas

- Ledger baseline selection and parent-commit derivation, including malformed or
  empty ledger fallback.
- Artifact inventory boundaries and the explicit fixture provenance exception.
- `evaluator-status.jsonl`, timeout handling, and the no-GO-with-missing-checks
  rule passed to 05l.
- Status-line-only verdict write-back and timestamped prior-run archival.
- Propagation destination mapping for this user-facing agent across Claude,
  OpenCode, and Codex.
