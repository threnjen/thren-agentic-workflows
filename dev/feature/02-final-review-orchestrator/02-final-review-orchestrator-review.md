# Review Record: 02-final-review-orchestrator

## Summary

The source agent and all propagated representations were reviewed against the
implementation record and plan. Six issues were found and fixed: 2 High and 4
Medium. The source now validates evaluator reports before synthesis, handles a
failed or timed-out 05l synthesizer, prevents incomplete coverage from becoming
GO, makes verdict write-back atomic, disambiguates ledger selection, and uses
valid evaluator-status values. A propagation smoke assertion was added.

## Verdict

Approved with Reservations

Static implementation review and propagation checks are clean. AC3–AC7 still
need live/manual execution evidence; the harness could not spawn 05a–05l. The
full suite has two documented pre-existing hook failures and no new failures.

## Top Risks

1. **False readiness from missing evaluator reports** — Fixed with metadata-only report validation before synthesis (`.github/agents/05-phase-final-review.agent.md:190-194`).
2. **Terminal synthesizer failure** — Fixed with bounded 05l failure handling and an explicit no-report `NO-GO` outcome (`.github/agents/05-phase-final-review.agent.md:196-209`).
3. **Unobserved runtime behavior** — Manual preflight, evaluator-failure, wrong-model, and status-write-back checks remain unverified.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified (static) | `.github/agents/05-phase-final-review.agent.md:1-23` | Numbered source agent, frontmatter, evaluator roster, and required skills are present. |
| AC2 | Verified (static; runtime obedience unverified) | `.github/agents/05-phase-final-review.agent.md:16-23,44-65` | Context boundary and ≤10-line return contract are explicit. |
| AC3 | Implemented; manual execution unverified | `.github/agents/05-phase-final-review.agent.md:90-130` | Ledger path, named fallback, candidate selection, and confirmation are documented. |
| AC4 | Implemented; fixture execution unverified | `.github/agents/05-phase-final-review.agent.md:132-170` | Subphase discovery and itemized artifact refusal are documented. |
| AC5 | Implemented; wrong-model execution unverified | `.github/agents/05-phase-final-review.agent.md:25-42,172-176` | Startup warning and deep/mechanical tier assignments are explicit. |
| AC6 | Implemented; evaluator-failure execution unverified | `.github/agents/05-phase-final-review.agent.md:67-81,178-209` | Status schema, report validation, bounded waits, 05l handling, and no-GO gate are explicit. |
| AC7 | Implemented; write-back execution unverified | `.github/agents/05-phase-final-review.agent.md:227-249` | Full rerun policy and both-file atomic status write-back are explicit. |
| AC8 | Verified by execution | `.github/agents/README.md:128-143,183-188`; generated outputs; `tests/test_propagate_master_assets.py:86-99` | Propagation pass completed; targeted suite passed with 20 tests and 7 subtests. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Claimed-success evaluator reports were not explicitly validated before synthesis. | High | `.github/agents/05-phase-final-review.agent.md:190-194` | AC6 | Fixed (applied during this review) |
| 2 | 05l timeout/failure/invalid-report behavior had no defined terminal outcome. | High | `.github/agents/05-phase-final-review.agent.md:196-209` | AC6 | Fixed (applied during this review) |
| 3 | Multiple valid ledger runs could be selected by filesystem order. | Medium | `.github/agents/05-phase-final-review.agent.md:96-111` | AC3 | Fixed (applied during this review) |
| 4 | `not-run|incomplete` was shown as a literal JSON status value rather than an enum choice. | Medium | `.github/agents/05-phase-final-review.agent.md:67-78` | AC6 | Fixed (applied during this review) |
| 5 | Verdict write-back could leave roadmap and summary statuses inconsistent after a partial failure. | Medium | `.github/agents/05-phase-final-review.agent.md:227-245` | AC7 | Fixed (applied during this review) |
| 6 | The reviewed propagation test had no assertion for the new final-review outputs. | Medium | `tests/test_propagate_master_assets.py:86-99` | AC8 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/agents/05-phase-final-review.agent.md` | Added deterministic ledger candidate selection, valid status values, evaluator report validation, 05l failure handling, canonical incomplete-coverage `NO-GO`, and atomic verdict write-back rules. | 1–5 |
| `claude/commands/phase-final-review.md` | Propagated the source contract fixes. | 1–5 |
| `opencode/agents/05-phase-final-review.md` | Propagated the source contract fixes. | 1–5 |
| `codex/agents/05-phase-final-review.toml` | Propagated the source contract fixes. | 1–5 |
| `codex/profiles/phase-final-review.config.toml` | Propagated the source contract fixes. | 1–5 |
| `tests/test_propagate_master_assets.py` | Added checked-in source and Claude/OpenCode/Codex output presence assertions. | 6 |
| `eval/runs/phase-phase-final-review-2/ledger-events.jsonl` | Recorded the remediation request, discovered review issues, and resolutions per the phase ledger contract. | Review traceability |

## Remaining Concerns

- AC3–AC7 require live/manual checks for baseline selection, artifact refusal, model warning, evaluator failure/hang propagation, and status-line write-back.
- The full suite still has two pre-existing failures in `tests/hooks/test_hook_distribution_integration.py` (latency threshold and installation-guide classifications); they were unchanged by this review.

## Test Coverage Assessment

- Covered: AC8 propagation smoke test; 20 targeted tests and 7 subtests passed; both Codex TOML files parsed successfully; diff whitespace check passed.
- Missing: Live 05a–05l orchestration evidence for AC3–AC7. The implementation record reports manual QA, but this review did not independently observe those executions.
- Full suite after fixes: 387 passed, 2 failed, 7 subtests passed; failures match the pre-existing failures recorded in the implementation record.

## Risk Summary

- `.github/agents/05-phase-final-review.agent.md:190-209` now has explicit gates against missing evaluator coverage and failed readiness synthesis.
- Runtime/manual acceptance evidence remains outstanding for AC3–AC7.
- Existing hook-suite failures remain outside this feature's changed files.

## Quick Wins

1. Keep the new generated-output presence test alongside future agent propagation changes (`tests/test_propagate_master_assets.py:86-99`).
2. Preserve the explicit `not-run`/`incomplete` status enum whenever downstream evaluator contracts evolve (`.github/agents/05-phase-final-review.agent.md:67-78`).

## Uncertainty

Confidence is high for the static traceability and contract findings. Runtime
obedience, live subagent failure handling, and actual roadmap write-back remain
unverified and require the manual checks listed above.
