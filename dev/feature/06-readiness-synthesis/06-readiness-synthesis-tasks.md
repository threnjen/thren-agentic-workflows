# Feature Tasks: 06-readiness-synthesis

## Stage 1: 05l Readiness Synthesizer

- [x] Verify upstream deliverables exist before starting: `phase-final-review-conventions` and `phase-final-review-report` skills in `.github/skills/`, the orchestrator, and all `05a`–`05k` evaluator agents (features 01–05 shipped)
- [x] Create `.github/agents/05l-readiness-synthesizer.agent.md` in the lettered-subagent house style, loading `phase-final-review-conventions` and honoring report locations and the ≤10-line return contract (AC1, AC4)
- [x] Specify inputs as evaluator report files only (never code, never other agents' internals), pinned to `phase-final-review-report` templates; a missing report file is treated as a not-run check regardless of evaluator claims (AC1, AC2)
- [x] Specify output: go/no-go readiness report using the `phase-final-review-report` readiness template with a severity-ordered blocking list; severity vocabulary sourced from the conventions skill; conflicting severities resolved to the highest with both sources cross-referenced (AC1)
- [x] Make the no-GO-with-missing-checks rule explicit: any not-run check caps the verdict at "no blockers found, coverage incomplete" — never GO — and not-run checks are enumerated by name (AC2)
- [x] Reference `prod-code-review` conventions as the one-level-up precedent (correct filename: `.github/agents/prod-code-review.md`) without duplicating or modifying them; declare 05l top-tier per the model-tier policy (AC1, AC4)
- [x] Constrain 05l to synthesis only — rank, cross-reference, verdict; no restating report content, no re-evaluation, no writes outside `dev/phase-final-review/`

## Stage 2: 05i Learnings Harvester

- [x] Create `.github/agents/05i-learnings-harvester.agent.md` in house style, loading `phase-final-review-conventions` and honoring the ≤10-line return contract (AC3, AC4)
- [x] Specify the mining corpus: review records, fix commits, and QA failures across the phase — explicitly including git-history recovery (on-disk Phase 01/02 review records were deleted in commit `4dd01e9`; history is in git, merged PRs #19/#20, and `eval/runs/*/ledger-commits.jsonl`) (AC3, AC8)
- [x] Specify outputs: draft `.github/learnings/` entries (matching the existing entry format in `review-learnings.md` / `project-learnings.md`) and instruction-file update proposals addressed to the instructions-writer/evaluator loop (AC3)
- [x] Make the draft-only boundary explicit: 05i never edits `.github/instructions/` files and never commits learnings itself; the instructions-manager loop owns acceptance (AC3)
- [x] Define the empty-harvest behavior: "none found" plus the corpus examined is a valid result in general runs

## Stage 3: Full-Flow Integration Dry Runs

- [x] Run the full flow — orchestrator preflight through 05l synthesis — against the development fixture; archive outputs under `dev/phase-final-review/` (AC5)
- [x] Verify all four synthesis-input artifact types exist: master QA doc, security rollup with fixed/persisting/reintroduced classification, AC-regression matrix covering every fixture AC, and the severity-ordered go/no-go readiness report (AC5; Manual QA check 1)
- [x] Verify the fixture-truth check: P2-SEC-01..03 from the fixture's Phase 02 NO-GO content appear in the readiness report's blocking list (Manual QA check 3)
- [x] Run the failure-path dry run with one evaluator forced to fail; verify the run completes, the readiness report names the missing check, and the verdict is not GO (AC6; Manual QA check 2)
- [x] Exercise the verdict write-back lifecycle against fixture copies of the planning docs (never the real roadmap); verify the status line updates without manual editing, or that a missing write-back target is recorded as not-performed with reason (AC7; Manual QA check 5)
- [x] Do not remediate any dry-run findings — NO-GO from the fixture run is the expected, correct result; route any template mismatch to the owning upstream feature, not a local patch in 05l

## Stage 4: Real-History Harvest + Propagation

- [x] Run 05i against this repo's real Phase 01/02 history; verify at least one draft learnings entry or instruction-file update proposal exists and cites its evidence (AC8; Manual QA check 4)
- [x] Run `scripts/propagate_master_assets.py` and verify both new agents are picked up in Claude, OpenCode, and Codex outputs with no script changes (AC9)
- [x] Run `.venv/bin/python -m pytest tests/test_propagate_master_assets.py` and confirm it passes (baseline: 19 passed) (AC9)
- [x] Confirm the two pre-existing failures in `tests/hooks/test_hook_distribution_integration.py` remain the only full-suite failures (no new regressions)
