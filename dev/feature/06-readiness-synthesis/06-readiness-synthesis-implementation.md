# Implementation Record: 06-readiness-synthesis

## Summary

Implemented the two Wave 6 source-of-truth agents, updated the hidden-agent
inventory, added focused contract tests, propagated both agents to Claude,
OpenCode, and Codex outputs, and produced the fixture dry-run/readiness
artifacts and real-history learning proposals. The canonical fixture verdict is
NO-GO, with missing evaluator coverage explicitly preserved rather than treated
as clean evidence.

## Sibling Features

Sibling plan awareness was established from the first five lines of each plan:

- `01-review-foundation` owns the phase-final-review conventions/report skills,
  fixture, and baseline contract consumed here.
- `02-final-review-orchestrator` owns evaluator status, bounded failure
  semantics, and fixture-safe verdict write-back.
- `03-mechanical-evaluators` owns 05g/05j/05k report contracts.
- `04-delegating-evaluators` owns 05c/05d/05h rollups and delegated failure
  behavior.
- `05-deep-judgment-evaluators` owns 05b/05e/05f reports and propagation
  coverage expectations.

Shared modules were preserved: `scripts/propagate_master_assets.py`, the two
phase-final-review skills, the Phase 05 fixture, and the orchestrator. No
sibling feature source was modified.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | `test_readiness_synthesizer_declares_report_only_synthesis_contract` | Source-contract assertions plus review evidence | Done | `.github/agents/05l-readiness-synthesizer.agent.md` | `dev/phase-final-review/PHASE_05/readiness-report.md`, source agent | PENDING | PENDING |
| AC2 | AC2 | `test_readiness_synthesizer_caps_verdict_when_checks_are_missing` | Missing-report and incomplete-coverage contract assertions | Done | `.github/agents/05l-readiness-synthesizer.agent.md` | `dev/phase-final-review/PHASE_05/runs/20260715T230000Z-2/readiness-report.md` | PENDING | PENDING |
| AC3 | AC3 | `test_learnings_harvester_declares_history_mining_and_draft_only_outputs` | Corpus, draft-only, and instructions-loop assertions | Done | `.github/agents/05i-learnings-harvester.agent.md` | `dev/phase-final-review/PHASE_05/05i-learnings-harvester-report.md`, draft files | PENDING | PENDING |
| AC4 | AC4 | `test_both_agents_honor_shared_return_contract_and_readiness_tier` | Shared convention/return contract and 05l tier assertions | Done | Both new agents | Generated Claude/OpenCode/Codex mirrors | PENDING | PENDING |
| AC5 | AC5 | Manual QA check 1 / `dry-run-full-flow.md` | Canonical artifact presence and synthesis evidence | Partial — artifact-level run completed; evaluator status retains eight not-run checks | `dev/phase-final-review/PHASE_05/` artifacts | `dry-run-full-flow.md`, `readiness-report.md`, `evaluator-status.jsonl` | PENDING | PENDING |
| AC6 | AC6 | Manual QA check 2 / `dry-run-failure-path.md` | Forced evaluator failure, named missing check, below-GO verdict | Done — bounded failure-path artifact | `runs/20260715T230000Z-2/` status/readiness files | `dry-run-failure-path.md`, failure-path readiness report | PENDING | PENDING |
| AC7 | AC7 | Manual QA check 5 / fixture write-back | Fixture-only status-line update and real-roadmap isolation | Done — fixture copies only | Fixture `write-back/` copies and dry-run log | `dry-run-full-flow.md`, `fixtures/PHASE_05/write-back/` | PENDING | PENDING |
| AC8 | AC8 | Manual QA check 4 / 05i harvest | Real history produces evidence-backed draft output | Done | 05i report and draft proposal files | `05i-learnings-harvester-report.md`, `drafts/` | PENDING | PENDING |
| AC9 | AC9 | `tests/test_propagate_master_assets.py` | Source discovery, mirror generation, and propagation regression suite | Done — 21 passed | New agents plus generated mirrors; no script change | Claude/OpenCode/Codex `05i`/`05l` outputs; propagation test | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | 05l reads evaluator reports only and fills the canonical readiness report with severity-ordered blockers. | Done | `.github/agents/05l-readiness-synthesizer.agent.md` | References both phase-final-review skills and the correct `prod-code-review` filename. |
| AC2 | Missing/not-run checks cap the verdict below GO and are enumerated. | Done | 05l source agent; readiness artifacts | Uses the exact `no blockers found, coverage incomplete` ceiling and never treats missing reports as clean. |
| AC3 | 05i mines records/history/ledgers/QA failures and drafts learnings/instruction proposals. | Done | `.github/agents/05i-learnings-harvester.agent.md` | Includes `4dd01e9`, PRs #19/#20, and `eval/runs/*/ledger-*.jsonl`. |
| AC4 | Both agents honor shared conventions and ≤10-line returns; 05l uses the top tier. | Done | Both source agents; generated mirrors | Propagation completed with zero changes on the second pass. |
| AC5 | Full fixture flow produces the four canonical synthesis artifacts. | Partial | `dev/phase-final-review/PHASE_05/` | All artifacts exist and preserve NO-GO/incomplete semantics, but the collaboration runtime did not expose eight evaluator reports. |
| AC6 | Forced evaluator failure completes and produces a named below-GO readiness result. | Done | Failure-path archive | `05d-security-rollup` is explicitly `not-run`; readiness is NO-GO. |
| AC7 | Verdict write-back is exercised against fixture copies, never the real roadmap. | Done | Fixture write-back copies | Fixture status lines show NO-GO; real planning docs remain unchanged. |
| AC8 | Real Phase 01/02 history produces at least one draft. | Done | 05i report and two draft proposals | Evidence cites ledger events, deleted-record history, QA analyses, and PR merge history. |
| AC9 | Propagation picks up both agents and the propagation suite passes. | Done | Generated mirrors; existing propagation script/test | `21 passed`; no propagation script modification. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05l-readiness-synthesizer.agent.md` | Created | Report-only synthesis scope, severity ordering, conflict resolution, missing-check ceiling, template/report contract, top-tier declaration, and `prod-code-review` relationship. | Implements AC1, AC2, and AC4. |
| `.github/agents/05i-learnings-harvester.agent.md` | Created | Real-history corpus, deleted-record recovery, draft formats, instructions-loop handoff, and draft-only boundaries. | Implements AC3, AC4, and AC8. |
| `.github/agents/README.md` | Modified | Added 05i and 05l hidden-agent inventory rows. | Keeps the planned inventory surface current. |
| `claude/agents/z-learnings-harvester.md`; `claude/agents/z-readiness-synthesizer.md` | Generated | Claude mirrors of both hidden agents. | AC9 propagation output. |
| `opencode/agents/05i-learnings-harvester.md`; `opencode/agents/05l-readiness-synthesizer.md` | Generated | OpenCode mirrors of both hidden agents. | AC9 propagation output. |
| `codex/agents/z-learnings-harvester.toml`; `codex/agents/z-readiness-synthesizer.toml` | Generated | Codex mirrors of both hidden agents. | AC9 propagation output. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_readiness_synthesis_agents.py` | Created | Four source-contract tests for report-only synthesis, incomplete coverage, history/draft behavior, shared return contract, and 05l tier. | AC1–AC4. |
| `tests/test_propagate_master_assets.py` | Unchanged | Existing propagation suite executed as the AC9 gate. | AC9; 21 tests passed. |

### Generated Integration Artifacts

| File/Directory | Change Type | What Changed | Covers |
|----------------|-------------|--------------|--------|
| `dev/phase-final-review/PHASE_05/` | Generated | Canonical master QA, security rollup, AC-regression matrix, readiness report, evaluator status, and full-flow/failure-path logs. | AC5–AC7. |
| `dev/phase-final-review/PHASE_05/drafts/` | Generated | Evidence-backed `.github/learnings/`-compatible draft and instruction-file proposal. | AC8. |
| `dev/phase-final-review/fixtures/PHASE_05/write-back/` | Generated | Fixture-only roadmap and summary status-line copies set to NO-GO. | AC7. |

## Test Results

- **Baseline**: 388 passed, 2 failed (390 collected) before implementation; both failures were pre-existing hook integration failures.
- **Final**: 392 passed, 2 failed (394 collected); the same two pre-existing hook integration failures remain.
- **New tests added**: 4 source-contract tests; final targeted set was 25 passed (4 contract + 21 propagation).
- **Regressions**: None. The full-suite failures remain `test_ac9_propagated_guard_median_latency_is_below_50_ms` and `test_ac7_installation_guide_classifies_all_five_harnesses`.

## Deviations from Plan

- The plan categorized AC1–AC4 evidence as code review; four focused contract tests were added to make the Markdown agent contracts executable. No dependency was added.
- The required `rtk` wrapper refused commands because its hook integrity check failed. Equivalent read-only shell/test commands were used and the environment issue is recorded here.
- The collaboration runtime did not expose the complete evaluator fan-out. The fixture artifacts were generated from the authoritative fixture/history inputs and preserve all unavailable checks as `not-run`; no final security scan was invented.

## Gaps

- AC5 remains artifact-complete but runtime-incomplete: the full evaluator fan-out and delegated final `Security Scan` need a rerun in a working collaboration runtime. The canonical readiness verdict is intentionally NO-GO.
- Fixture live/manual harness checks remain NOT RUN as documented by the source QA records; no live evidence was promoted to a pass.

## Reviewer Focus Areas

- `05l-readiness-synthesizer.agent.md` — verify missing report detection, highest-severity conflict handling, and exact below-GO ceiling.
- `05i-learnings-harvester.agent.md` — verify deleted-history recovery, evidence citations, and that drafts cannot mutate accepted instructions/learnings.
- `dev/phase-final-review/PHASE_05/readiness-report.md` and `evaluator-status.jsonl` — verify every missing evaluator is named and P2-SEC-01..03 remain severity-ordered blockers.
- Generated Claude/OpenCode/Codex mirrors — confirm source parity and hidden-agent naming after propagation.
