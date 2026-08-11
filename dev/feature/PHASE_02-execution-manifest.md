# Phase 02 Execution Manifest

- **Phase document:** `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`
- **Phase:** `PHASE_02` — Phase Document Final Check
- **Ordered features:** `05-phase-final-check-contract`, `06-phase-final-check-reviewer`, `07-phase-refiner-final-check`
- **Integration feature:** `07-phase-refiner-final-check` connects the shared contract and hidden reviewer to both live Phase - Refiner entry paths and owns combined automated and manual verification.
- **Baseline:** `uv run pytest tests/` collected 242 tests on 2026-08-11: 230 passed and 12 pre-existing failures. The failures are one PR Review display-name collision, one wildcard `applyTo` enumeration failure, and ten Phase 01 Unity reference-asset failures caused by the missing GameCI workflow asset.
- **Propagation:** Pending after source edits. Agents must not run `scripts/propagate_master_assets.py` or edit generated `ports/`/`.github/` files.

## Features

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---:|---|---|---|---|
| `05-phase-final-check-contract` | 1 | yes | none | `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` | n/a |
| `06-phase-final-check-reviewer` | 2 | yes | `05-phase-final-check-contract` | `source_of_truth/agents/02a-phase-final-check.agent.md`, `source_of_truth/instructions/read-only-agent.instructions.md` | n/a |
| `07-phase-refiner-final-check` | 3 | yes | `05-phase-final-check-contract`, `06-phase-final-check-reviewer` | `source_of_truth/agents/02-phase-refiner.agent.md`, `tests/[PROPOSED - name TBD: phase final-check contract guards]` | n/a |

## Dependency Graph

- `06-phase-final-check-reviewer` depends_on `05-phase-final-check-contract` because the reviewer must reference the finalized contract skill and cannot safely guess its slug.
- `07-phase-refiner-final-check` depends_on `05-phase-final-check-contract` because the Refiner and focused guards must reference the same finalized skill.
- `07-phase-refiner-final-check` depends_on `06-phase-final-check-reviewer` because the Refiner roster and spawn step must use the exact display name parsed from the new hidden leaf.
- The three feature file scopes are disjoint. Later waves remain dependency-gated by runtime contracts, but no upstream shared-file conflict makes them sequentially unsafe.

## Execution Schedule

### Wave 1 — parallel

- `05-phase-final-check-contract`

This single feature fixes the reusable vocabulary and chooses the final skill slug. Complete it before downstream features begin.

### Wave 2 — parallel

- `06-phase-final-check-reviewer`

Start after Wave 1. Create the hidden reviewer and update the enumerated read-only instruction in the same feature so the inheritance claim is true at every committed state.

### Wave 3 — parallel

- `07-phase-refiner-final-check`

Start after Waves 1 and 2. Parse the exact upstream skill slug and reviewer display name from disk, then integrate both Refiner entry paths and add the consolidated Phase 02 guards.

## Expected Bundle Files

| Feature | Plan | Context | Tasks |
|---|---|---|---|
| `05-phase-final-check-contract` | `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-plan.md` | `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-context.md` | `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-tasks.md` |
| `06-phase-final-check-reviewer` | `dev/feature/06-phase-final-check-reviewer/06-phase-final-check-reviewer-plan.md` | `dev/feature/06-phase-final-check-reviewer/06-phase-final-check-reviewer-context.md` | `dev/feature/06-phase-final-check-reviewer/06-phase-final-check-reviewer-tasks.md` |
| `07-phase-refiner-final-check` | `dev/feature/07-phase-refiner-final-check/07-phase-refiner-final-check-plan.md` | `dev/feature/07-phase-refiner-final-check/07-phase-refiner-final-check-context.md` | `dev/feature/07-phase-refiner-final-check/07-phase-refiner-final-check-tasks.md` |

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/[PROPOSED - name TBD: phase final-check contract guards]` | `05-phase-final-check-contract`, `06-phase-final-check-reviewer`, `07-phase-refiner-final-check` | Consolidated structural guards for the contract, hidden-leaf topology, read-only instruction applicability, shared-skill references, Refiner roster/workflow ordering, continuation branches, blindness boundary, and mutation/non-vacuity evidence. |

### Existing Test Files Updated By Multiple Features

None identified. `tests/test_agent_corpus_invariants.py` and `tests/test_propagate_master_assets.py` remain unchanged regression inputs. The existing `source_of_truth/instructions/read-only-agent.instructions.md` edit belongs only to Feature 06.

### Manual QA Checklist

- [ ] Exercise Refiner Entry A against an existing phase document. Accept the offer and confirm the reviewer starts cold with only the repository and phase-document paths, returns at most five concrete findings or a plain zero-findings result, and writes no artifact.
- [ ] Exercise Refiner Entry B from a standalone feature description. Decline or leave the offer unanswered and confirm synchronization plus branch progression continues with the document unchanged.
- [ ] With usable findings, confirm Phase - Refiner relays them verbatim, applies only the selected subset, rewrites the phase document cleanly, and performs roadmap/discovery synchronization exactly once afterward.
- [ ] Simulate reviewer error or unusable output. Confirm one-line reporting, no retry, no inline review, no document change, and normal continuation.
- [ ] Delete or semantically negate every protected source-contract mechanism, confirm the focused guard fails for the intended obligation, restore it, and confirm green.

## Phase-Level Regression Gate

1. Run the focused Phase 02 guard module after Wave 3 and retain deletion/negation evidence for every new content guard.
2. Run `uv run pytest tests/test_agent_corpus_invariants.py` and `uv run pytest tests/test_propagate_master_assets.py` unchanged.
3. Run `uv run pytest tests/` and compare against the recorded 230-pass/12-failure baseline. Any additional failure is a Phase 02 regression until explained.
4. Confirm no file under `ports/` or `.github/` changed and no propagation command ran.
5. Report generated synchronization failures as maintainer propagation pending, never as a reason to edit generated output.

