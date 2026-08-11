# Phase 02 QA

## TL;DR

This checklist verifies the Phase 02 final-check contract and Refiner wiring.
The focused structural suite is green: 26 tests passed.
The full repository suite is not green because of 12 baseline failures and pending generated propagation.
Manual Entry A and Entry B smoke checks are still required.
This repository is not a Unity project, so visual verification is skipped.

## Automated checks

Run these commands from the repository root.

1. Run the Phase 02 focused checks:

   ```bash
   uv run pytest tests/test_phase_refiner_final_check.py
   ```

   Correct result: `26 passed`.

2. Run the unchanged corpus and propagation regression checks:

   ```bash
   uv run pytest tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py
   ```

   Correct result for the current baseline: 50 passed and 1 known wildcard `applyTo` failure. A source-only tree also reports generated synchronization as pending until the maintainer propagates.

3. Run the full repository suite:

   ```bash
   uv run pytest tests/
   ```

   Correct interpretation for this execution: the Phase 02-focused tests pass. The remaining failures are the pre-existing PR Review name collision, wildcard `applyTo` enumeration, ten Unity reference-asset checks, and generated-tree synchronization. Do not edit generated outputs to address them.

## Manual acceptance checks

1. Entry A — existing phase document. Start Phase - Refiner with an existing phase document, accept the final-check offer, and confirm the reviewer receives only the repository path and phase-document path. Confirm it returns no more than five concrete findings or a plain zero-findings response and writes no artifact.

2. Entry B — standalone feature description. Start Phase - Refiner from a feature description, decline the offer or leave it unanswered, and confirm synchronization and branch progression continue with the phase document unchanged.

3. Accepted findings. Repeat either entry with usable findings. Confirm the Refiner relays them verbatim, applies only the findings the user selects, rewrites the phase document cleanly, and synchronizes the roadmap and discovery context once afterward.

4. Reviewer failure. Simulate an error, timeout, or unusable response. Confirm the Refiner reports it once, does not retry or review inline, leaves the phase document unchanged, and continues normally.

5. Guard integrity. Delete or negate each protected contract mechanism in `tests/test_phase_refiner_final_check.py`, confirm the associated test fails, restore it, and confirm the focused suite returns to 26 passed.

## Visual verification

Skipped: the repository has no Unity `Assets/` and `ProjectSettings/` project roots and Phase 02 has no visual acceptance criteria.

## Evidence

- Focused run: `dev/feature/07-phase-refiner-final-check/07-phase-refiner-final-check-focused-2.xml`
- Wave 3 full run: `dev/phase-02-wave-3-full.txt` and `dev/phase-02-wave-3-full.xml`
- Wave 3 retry: `dev/phase-02-wave-3-full-retry.txt` and `dev/phase-02-wave-3-full-retry.xml`
- Feature plans, implementation records, and reviews: `dev/feature/05-phase-final-check-contract/`, `dev/feature/06-phase-final-check-reviewer/`, and `dev/feature/07-phase-refiner-final-check/`
