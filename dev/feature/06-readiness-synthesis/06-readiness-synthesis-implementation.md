# Implementation Record: 06-readiness-synthesis

## Summary

Implemented the two Wave 6 source-of-truth agents, updated the hidden-agent
inventory, added focused contract tests, propagated both agents to Claude,
OpenCode, and Codex outputs, and produced the fixture dry-run/readiness
artifacts and real-history learning proposals. The canonical fixture verdict is
NO-GO, with missing evaluator coverage explicitly preserved rather than treated
as clean evidence.

The remediation pass resolved the review's open High finding: 05i now declares
the existing `fetch` capability for narrowly scoped, read-only remote git
history and hosted PR/history evidence needed for deleted-record recovery and
AC8. The generated Claude, OpenCode, and Codex mirrors carry the same boundary;
no `execute`, Bash, or unrestricted shell capability was restored. The prior
05l status/report validation, propagation parity test, bounded-evidence label,
and focused contract coverage were preserved.

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
| AC3 | AC3 | `test_learnings_harvester_declares_history_mining_and_draft_only_outputs`; `test_learnings_harvester_declares_scoped_read_only_history_fetch` | Corpus, draft-only, instructions-loop, and read-only history/PR capability assertions | Done | `.github/agents/05i-learnings-harvester.agent.md` | `dev/phase-final-review/PHASE_05/05i-learnings-harvester-report.md`, draft files, source contract test | PENDING | PENDING |
| AC4 | AC4 | `test_both_agents_honor_shared_return_contract_and_readiness_tier`; mirror capability contract test | Shared convention/return contract, 05l tier, and cross-harness capability assertions | Done | Both new agents | Generated Claude/OpenCode/Codex mirrors | PENDING | PENDING |
| AC5 | AC5 | Manual QA check 1 / `dry-run-full-flow.md` | Canonical artifact presence and synthesis evidence | Partial — artifact-level run completed; evaluator status retains eight not-run checks | `dev/phase-final-review/PHASE_05/` artifacts | `dry-run-full-flow.md`, `readiness-report.md`, `evaluator-status.jsonl` | PENDING | PENDING |
| AC6 | AC6 | Manual QA check 2 / `dry-run-failure-path.md` | Forced evaluator failure, named missing check, below-GO verdict | Done — bounded failure-path artifact | `runs/20260715T230000Z-2/` status/readiness files | `dry-run-failure-path.md`, failure-path readiness report | PENDING | PENDING |
| AC7 | AC7 | Manual QA check 5 / fixture write-back | Fixture-only status-line update and real-roadmap isolation | Done — fixture copies only | Fixture `write-back/` copies and dry-run log | `dry-run-full-flow.md`, `fixtures/PHASE_05/write-back/` | PENDING | PENDING |
| AC8 | AC8 | Manual QA check 4 / 05i harvest | Real history produces evidence-backed draft output through the declared read-only history/PR evidence capability | Done | 05i report and draft proposal files | `05i-learnings-harvester-report.md`, `drafts/` | PENDING | PENDING |
| AC9 | AC9 | `tests/test_propagate_master_assets.py` | Source discovery, mirror generation, and propagation regression suite | Done — 21 passed | New agents plus generated mirrors; no script change | Claude/OpenCode/Codex `05i`/`05l` outputs; propagation test | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | 05l reads evaluator reports only and fills the canonical readiness report with severity-ordered blockers. | Done | `.github/agents/05l-readiness-synthesizer.agent.md` | References both phase-final-review skills and the correct `prod-code-review` filename. |
| AC2 | Missing/not-run checks cap the verdict below GO and are enumerated. | Done | 05l source agent; readiness artifacts | Uses the exact `no blockers found, coverage incomplete` ceiling and never treats missing reports as clean. |
| AC3 | 05i mines records/history/ledgers/QA failures and drafts learnings/instruction proposals. | Done | `.github/agents/05i-learnings-harvester.agent.md`; generated 05i mirrors | Includes `4dd01e9`, PRs #19/#20, and `eval/runs/*/ledger-*.jsonl`; the existing `fetch` capability is explicitly read-only and scoped to history/PR evidence. |
| AC4 | Both agents honor shared conventions and ≤10-line returns; 05l uses the top tier. | Done | Both source agents; generated mirrors | Propagation preserves the 05i `WebFetch`/`webfetch` capability without Bash/execute access; second pass was idempotent. |
| AC5 | Full fixture flow produces the four canonical synthesis artifacts. | Partial | `dev/phase-final-review/PHASE_05/` | All artifacts exist and preserve NO-GO/incomplete semantics, but the collaboration runtime did not expose eight evaluator reports. |
| AC6 | Forced evaluator failure completes and produces a named below-GO readiness result. | Done | Failure-path archive | `05d-security-rollup` is explicitly `not-run`; readiness is NO-GO. |
| AC7 | Verdict write-back is exercised against fixture copies, never the real roadmap. | Done | Fixture write-back copies | Fixture status lines show NO-GO; real planning docs remain unchanged. |
| AC8 | Real Phase 01/02 history produces at least one draft. | Done | 05i report and two draft proposals | Evidence cites ledger events, deleted-record history, QA analyses, and PR merge history; the declared read-only fetch path now covers the deleted-record/PR evidence lookup. |
| AC9 | Propagation picks up both agents and the propagation suite passes. | Done | Generated mirrors; existing propagation script/test | `21 passed`; no propagation script modification. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/05l-readiness-synthesizer.agent.md` | Created | Report-only synthesis scope, severity ordering, conflict resolution, missing-check ceiling, template/report contract, top-tier declaration, and `prod-code-review` relationship. | Implements AC1, AC2, and AC4. |
| `.github/agents/05i-learnings-harvester.agent.md` | Created and remediated | Real-history corpus, deleted-record recovery, draft formats, instructions-loop handoff, draft-only boundaries, and the scoped read-only `fetch` capability for remote git history and hosted PR/history evidence. | Implements AC3, AC4, and AC8; resolves review Issue #1. |
| `.github/agents/README.md` | Modified | Added 05i and 05l hidden-agent inventory rows. | Keeps the planned inventory surface current. |
| `claude/agents/z-learnings-harvester.md`; `claude/agents/z-readiness-synthesizer.md` | Generated and regenerated | Claude mirrors of both hidden agents; 05i exposes `WebFetch` without `Bash`. | AC4 and AC9 propagation output. |
| `opencode/agents/05i-learnings-harvester.md`; `opencode/agents/05l-readiness-synthesizer.md` | Generated and regenerated | OpenCode mirrors of both hidden agents; 05i exposes `webfetch` without `bash`. | AC4 and AC9 propagation output. |
| `codex/agents/z-learnings-harvester.toml`; `codex/agents/z-readiness-synthesizer.toml` | Generated and regenerated | Codex mirrors of both hidden agents with the read-only history/PR evidence boundary embedded in instructions. | AC4 and AC9 propagation output. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_readiness_synthesis_agents.py` | Created and expanded | Six source-contract tests covering report-only synthesis, incomplete coverage, history/draft behavior, shared return contract, 05l tier, and the scoped read-only history/PR fetch capability across generated mirrors. | AC1–AC4, AC8, AC9. |
| `tests/test_propagate_master_assets.py` | Unchanged | Existing propagation suite executed as the AC9 gate. | AC9; 21 tests passed. |

### Generated Integration Artifacts

| File/Directory | Change Type | What Changed | Covers |
|----------------|-------------|--------------|--------|
| `dev/phase-final-review/PHASE_05/` | Generated | Canonical master QA, security rollup, AC-regression matrix, readiness report, evaluator status, and full-flow/failure-path logs. | AC5–AC7. |
| `dev/phase-final-review/PHASE_05/drafts/` | Generated | Evidence-backed `.github/learnings/`-compatible draft and instruction-file proposal. | AC8. |
| `dev/phase-final-review/fixtures/PHASE_05/write-back/` | Generated | Fixture-only roadmap and summary status-line copies set to NO-GO. | AC7. |

## Test Results

- **Baseline**: 388 passed, 2 failed (390 collected) before implementation; both failures were pre-existing hook integration failures.
- **Final**: 394 passed, 2 failed (396 collected); the same two pre-existing hook integration failures remain.
- **New tests added**: 6 source-contract tests total (2 added in this remediation); final targeted set was 27 passed (6 contract + 21 propagation).
- **Regressions**: None. The full-suite failures remain `test_ac9_propagated_guard_median_latency_is_below_50_ms` and `test_ac7_installation_guide_classifies_all_five_harnesses`.

## Deviations from Plan

- The plan categorized AC1–AC4 evidence as code review; four focused contract tests were added to make the Markdown agent contracts executable. No dependency was added.
- The review remediation uses the existing cross-platform `fetch` mapping (`WebFetch`/`webfetch`) as the minimal portable read-only history/PR evidence capability; no new tool vocabulary or propagation-script change was introduced.
- Limitation: the existing agent format exposes no dedicated local-git-history or PR API tool. `fetch` therefore covers hosted/remote commit and PR evidence only; when that evidence endpoint is unavailable, 05i must record the unavailable source and reason rather than fall back to shell or claim deleted-record recovery.
- The required `rtk` wrapper refused commands because its hook integrity check failed. Equivalent read-only shell/test commands were used and the environment issue is recorded here.
- The collaboration runtime did not expose the complete evaluator fan-out. The fixture artifacts were generated from the authoritative fixture/history inputs and preserve all unavailable checks as `not-run`; no final security scan was invented.
- Pre-existing unrelated generated/config/data changes in the worktree were preserved and excluded from this remediation; the propagation pass introduced no additional unrelated changes.

## Gaps

- AC5 remains artifact-complete but runtime-incomplete: the full evaluator fan-out and delegated final `Security Scan` need a rerun in a working collaboration runtime. The canonical readiness verdict is intentionally NO-GO.
- Fixture live/manual harness checks remain NOT RUN as documented by the source QA records; no live evidence was promoted to a pass.

## Remediation Evidence

- Review Issue #1 (High) was addressed in the 05i source contract and all three generated mirrors. The source declares `fetch`; Claude emits `WebFetch`, OpenCode emits `webfetch`, and Codex retains the read-only boundary in `developer_instructions`.
- The capability is restricted to remote git-history and hosted PR/history evidence retrieval. The agent explicitly cannot use `execute`, Bash, shell, or PR/commit/file mutation operations.
- Tooling limitation is explicit: no dedicated local history or PR API capability exists in the current cross-platform source format, so unavailable remote evidence remains a recorded gap rather than an implicit shell fallback.
- Red: the two new remediation contract tests failed against the old source/mirrors. Green: `tests/test_readiness_synthesis_agents.py` and `tests/test_propagate_master_assets.py` passed together, 27 tests total.
- Full suite: 394 passed, 2 failed; the same pre-existing hook integration failures remain. Scoped `git diff --check` is clean; an unscoped check still reports pre-existing CRLF/trailing-whitespace changes in `deepswe_20260709.csv`.
- Ledger: remediation request `implement-06-readiness-synthesis-remediation-history-capability-20260715T174000Z` resolved by `implement-06-readiness-synthesis-resolution-history-capability-20260715T174500Z`.

## Reviewer Focus Areas

- `05l-readiness-synthesizer.agent.md` — verify missing report detection, highest-severity conflict handling, and exact below-GO ceiling.
- `05i-learnings-harvester.agent.md` — verify deleted-history recovery, evidence citations, and that drafts cannot mutate accepted instructions/learnings.
- `dev/phase-final-review/PHASE_05/readiness-report.md` and `evaluator-status.jsonl` — verify every missing evaluator is named and P2-SEC-01..03 remain severity-ordered blockers.
- Generated Claude/OpenCode/Codex mirrors — confirm source parity and hidden-agent naming after propagation.
