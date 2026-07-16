# Phase 05 QA Coverage Map

**Date:** 2026-07-15
**Last Updated:** 2026-07-15
**Scope:** Acceptance-criterion coverage for all six Phase 05 feature folders.
**Manual QA checklist:** docs/phases/PHASE_05/PHASE_05_QA.md (24 items)

The default classification is No. Manual QA is included only where a human
must observe a real agent/delegate session, local history/worktree behavior,
cross-harness propagation, fixture persistence, or fail-closed release UX.
Static Markdown contracts and concrete propagation/parity assertions remain
automated or review evidence and are not duplicated as manual test cases.

## Consolidated AC Coverage

| Feature | AC | Automated Coverage | Manual QA Needed? | Reason |
|---|---|---|---|---|
| 01-review-foundation | AC1 | Source skill contract is present and was statically reviewed; no runtime behavior is involved. | No | The conventions text is a static, inspectable Markdown contract. |
| 01-review-foundation | AC2 | Report-template skill was statically reviewed; no runtime behavior is involved. | No | Template headings and classification vocabulary are assertable without a live session. |
| 01-review-foundation | AC3 | Review record documents a known-SHA worktree check; no automated test executes the reusable procedure end to end. | Yes | Real detached worktree creation, collision policy, clean state, and owned cleanup depend on local Git state. |
| 01-review-foundation | AC4 | Frontmatter/propagation presence is inspectable; no automated test observes a live 05a return. | Yes | The absolute returned path and observed ten-line limit require a live agent harness. |
| 01-review-foundation | AC5 | Review record reports fixture comparisons, but no automated test validates the complete copied inventory and preserved NO-GO evidence. | Yes | Human comparison is needed to verify provenance, normalized pseudo-subphase layout, and the genuine Phase 02 security case. |
| 01-review-foundation | AC6 | tests/test_propagate_master_assets.py covers generic propagation and selected Phase Final Review mirrors, but does not explicitly enumerate every 01 skill and 05a output. | Yes | The required after-each-feature source-to-harness smoke check must cover the unenumerated 05a/skill paths. |
| 02-final-review-orchestrator | AC1 | Source agent frontmatter and conventions-skill reference are statically inspectable. | No | No human judgment or deployed service is needed for this source contract. |
| 02-final-review-orchestrator | AC2 | Source text and generated output presence are inspectable; live context isolation/return behavior is not automated. | No | The declared context and return contract is a static agent instruction. |
| 02-final-review-orchestrator | AC3 | Implementation record documents ledger and fallback checks; no automated test runs both preflight history paths. | Yes | A real local ledger, commit-message fallback, and explicit user confirmation must be observed. |
| 02-final-review-orchestrator | AC4 | Source text defines the missing-artifact rule; no automated test runs a temporary incomplete fixture through preflight. | Yes | Refusal timing and itemized diagnostic output are runtime preflight behavior. |
| 02-final-review-orchestrator | AC5 | Static model-tier declarations are present; no automated test observes warning ordering in a non-top-tier session. | Yes | The visible warning-before-work behavior is session UX and model-environment dependent. |
| 02-final-review-orchestrator | AC6 | Source contract tests/retained status artifacts cover wording, but no automated test runs a real evaluator failure through synthesis. | Yes | Continuation after failure, not-run recording, and the below-GO ceiling require a live orchestration run. |
| 02-final-review-orchestrator | AC7 | Write-back rules are statically inspectable; retained fixture copies are not execution proof. | Yes | Atomic status-line-only updates and isolation from the real roadmap require observed file persistence. |
| 02-final-review-orchestrator | AC8 | tests/test_propagate_master_assets.py explicitly checks the orchestrator in Claude/OpenCode/Codex outputs and passes. | No | Generated output presence and renderer parity are covered by the existing propagation suite. |
| 03-mechanical-evaluators | AC1 | 05g source and mirrors are statically reviewed; propagation tests cover selected mirror parity but not live graph behavior. | Yes | The graph dependency, phase-diff attribution, report creation, and degraded NOT RUN path require a real run. |
| 03-mechanical-evaluators | AC2 | 05j source contract is statically reviewed; no test proves fixture drift is reported. | Yes | The known Phase 01/02 drift and canonical recommendation are judgmental report output. |
| 03-mechanical-evaluators | AC3 | 05k source contract is statically reviewed; no test proves the fixture's no-dependency result. | Yes | The offline/no-new-dependencies conclusion and bounded return must be observed in the evaluator report. |
| 03-mechanical-evaluators | AC4 | Static contract and generated-output checks cover declarations; no live dependency-failure run is automated. | Yes | Partial-failure behavior and ten-line evaluator returns require real graph/dependency runtime conditions. |
| 03-mechanical-evaluators | AC5 | No automated test runs each evaluator through the orchestrator against the fixture. | Yes | Report files, known findings, and return payloads require a delegated dry run. |
| 03-mechanical-evaluators | AC6 | Propagation suite passes, but its explicit Phase Final Review slug list does not include 05g, 05j, or 05k. | Yes | Manual propagation must cover the three mechanical agent aliases and all harness outputs. |
| 04-delegating-evaluators | AC1 | 05c source contract and current master-qa artifact are inspectable; evaluator execution is not automated. | Yes | Deduplication, supersession, conflict flagging, and report status require human inspection of a live consolidation. |
| 04-delegating-evaluators | AC2 | Static delegation rules and current fail-closed rollup are inspectable; no live final Security Scan result is available. | Yes | Cross-agent delivery and fixed/persisting/reintroduced classification require an actual delegated scan or observed fail-closed path. |
| 04-delegating-evaluators | AC3 | Static delegation/adaptation rules and current health artifact are inspectable; live Test - Analyst execution is not automated. | Yes | Delegate output shape, not-measurable coverage, redundancy, and flake sections require runtime observation. |
| 04-delegating-evaluators | AC4 | Static shared contracts and one 05d not-run record are present; 05h delegate failure is not independently observed. | Yes | Delegate-unavailable diagnostics and below-GO behavior are real cross-agent failure states. |
| 04-delegating-evaluators | AC5 | Absence of local scan/test-analysis procedures is statically inspectable and covered by review. | No | This is a source-contract boundary, not a human-only runtime outcome. |
| 04-delegating-evaluators | AC6 | Current bounded artifacts show 05c/05h outputs and 05d failure, but no complete all-three live dry run. | Yes | The 05d P2-SEC-01..03 classifications and each evaluator's report/return require live orchestration. |
| 04-delegating-evaluators | AC7 | tests/test_propagate_master_assets.py explicitly covers 05c/05d/05h renderer parity and passes. | No | Propagation output parity is covered by the existing automated suite. |
| 05-deep-judgment-evaluators | AC1 | 05b source and mirrors are statically reviewed; no test observes chunked narrative execution. | Yes | Per-subphase attribution, churn hotspots, bounded chunking, and report return require live judgment output. |
| 05-deep-judgment-evaluators | AC2 | Source contract and the current 26-row fixture-derived matrix are inspectable; no live hidden-verifier fan-out is automated. | Yes | A human must compare matrix cardinality with the 17+9 fixture criteria and inspect every status. |
| 05-deep-judgment-evaluators | AC3 | Graph operation naming is statically/live-tool checked; no test exercises both available and unavailable evaluator states. | Yes | The distinction between completed no-seams and NOT RUN graph failure needs runtime observation. |
| 05-deep-judgment-evaluators | AC4 | Source/mirror contracts are statically reviewed; live report/return behavior is not tested. | Yes | Baseline skip, partial failure, read-only behavior, and ten-line returns require a real evaluator run. |
| 05-deep-judgment-evaluators | AC5 | The current matrix and other artifacts are bounded fixture evidence, not complete evaluator execution proof. | Yes | Complete 05b/05e/05f dry runs and 05e row coverage must be observed through the orchestrator. |
| 05-deep-judgment-evaluators | AC6 | tests/test_propagate_master_assets.py explicitly covers 05b/05e/05f parity and passes. | No | Generated output parity is covered by the existing propagation suite. |
| 06-readiness-synthesis | AC1 | Six focused contract tests cover 05l report-only scope, template references, and severity vocabulary. | No | The synthesis input boundary is statically and automatically asserted. |
| 06-readiness-synthesis | AC2 | Focused tests assert missing/not-run wording and the below-GO rule; current readiness artifact preserves NO-GO. | Yes | A live missing-report/forced-failure synthesis must prove the check is named and GO is impossible. |
| 06-readiness-synthesis | AC3 | Focused tests assert history sources and draft-only boundaries; current 05i artifacts cite real history. | Yes | Real history mining and evidence-backed proposal creation depend on the local ledger/history corpus and agent runtime. |
| 06-readiness-synthesis | AC4 | Focused tests cover shared return/tier declarations and generated mirrors. | Partial — live return behavior | The declarations are automated; actual 05i/05l report creation and ten-line returns are runtime observations. |
| 06-readiness-synthesis | AC5 | Current canonical artifacts exist but the retained status file records eight evaluator checks as not-run; no complete full-flow test exists. | Yes | Only a live fan-out can prove all four canonical outputs are produced from all evaluator reports. |
| 06-readiness-synthesis | AC6 | The retained forced-failure archive names 05d and NO-GO, but the implementation record says forced execution was not independently observed. | Yes | Failure continuation, named missing check, and below-GO readiness require an observed full-flow failure run. |
| 06-readiness-synthesis | AC7 | Fixture copies and no-diff evidence are retained; no automated test exercises the write-back operation. | Yes | File mutation scope and status-line-only persistence must be observed against fixture copies. |
| 06-readiness-synthesis | AC8 | Current 05i report/drafts contain evidence citations, but no automated test runs the real-history harvest. | Yes | Human inspection must confirm the draft is evidence-backed and accepted files remain untouched. |
| 06-readiness-synthesis | AC9 | Propagation suite and readiness-agent mirror tests pass, including 05i/05l outputs. | No | Generated output parity is covered by automated tests. |

## Manifest Verification Checklist

| Required manifest asset | Coverage location | Current evidence |
|---|---|---|
| No new automated test files identified | Automated Test Coverage and notes above | The current tree actually contains tests/test_readiness_synthesis_agents.py from feature 06; it passed 6 tests and is treated as automated evidence, not manual scope. |
| Existing tests/test_propagate_master_assets.py updated/verified across all features | Automated Test Coverage; propagation surface item | 21 tests and 15 subtests pass; explicit parity coverage exists for the named Phase Final Review outputs, with manual smoke coverage retained for omitted 05a/05g/05j/05k paths. |
| Fixture inventory with Phase 02 NO-GO security content | QA checklist item 1 | dev/phase-final-review/fixtures/README.md, copied Phase 05a/05b trees, and P2-SEC-01..03 evidence. |
| Preflight baseline with ledgers and commit-message fallback | QA checklist items 2–3 | Current ledger run eval/runs/phase-phase-final-review-2/; branch eval: checkpoints. |
| Itemized missing-artifact refusal | QA checklist item 4 | Temporary fixture deletion must stop fan-out with a MISSING — ... item. |
| Each evaluator dry-run writes its conventions-defined report and returns no more than 10 lines | QA checklist items 5, 7, 9–13, 15–19, and 22 | Current retained artifacts prove only bounded/partial output; the live complete run remains required. |
| 05d classifies P2-SEC-01..03 Fixed/Persisting/Reintroduced | QA checklist item 12 and full-flow item 19 | Current rollup fail-closes all three as Persisting because the final delegated scan is unavailable; no Fixed/Reintroduced claim is made. |
| 05e AC-regression row count equals fixture AC count | QA checklist item 16 | Fixture count is 17 + 9 = 26; current matrix contains 26 fixture rows. |
| Full-flow master QA/security rollup/AC matrix/readiness | QA checklist item 19 | Current bounded artifacts exist but readiness remains NO-GO with missing evaluator coverage. |
| Forced-failure missing-check/non-GO | QA checklist item 20 | Current archive records forced 05d as not-run and readiness as NO-GO; live rerun remains required. |
| Fixture-only verdict write-back | QA checklist item 21 | Current fixture copies show NO-GO and live roadmap/summary are unchanged. |
| 05i real-history learning proposal | QA checklist item 22 | Current report cites deleted records, ledger commits/events, QA failures, and produces learning/instruction drafts. |
| Propagation after each feature | QA checklist item 23 | Run the propagation script at each feature checkpoint and verify idempotence and harness naming. |

## Automated Baseline

- Focused propagation: 21 passed, 15 subtests passed.
- Focused readiness contracts: 6 passed.
- Full suite: 394 passed, 2 failed, 15 subtests passed; both failures are the
  known hook-distribution latency/installation-guide failures.
- No new Phase 05 application or UI tests are required. Runtime/manual gaps
  remain intentionally visible rather than being replaced with static checks.
