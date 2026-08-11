# Tasks: Phase Execute Audit Bookend

## Stage 1: Frontmatter and Step 1 Decision

- [x] Verify `08-audit-comparison-contract` has completed; discover the finalized audit-comparison skill slug and caller contract from disk, and do not implement against the `[PROPOSED - name TBD]` placeholder.
- [x] Add the exact existing leaves `Auditor - Code`, `Auditor - Infra`, `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree` to `source_of_truth/agents/04-phase-execute.agent.md` frontmatter while preserving every current roster entry and the existing `agent` tool.
- [x] Preserve Step 1's current hard-stops for a missing or ambiguous execution manifest and for incomplete feature bundles; apply the bookend's non-blocking unusable-scope branch only after those validations succeed.
- [x] After successful manifest/bundle validation, collect every manifest `key files modified` path, reject or record duplicate/out-of-repository/otherwise unusable scope inputs, and preserve deleted or renamed starting paths as limitations when current-tree reference search cannot resolve them.
- [x] Resolve exactly one uncapped hop of dependents for each valid modified path: files that name the path, import its module, or use names it defines; stop without transitive expansion.
- [x] Treat all files under `source_of_truth/` and `tests/` as source, exclude `docs/`, README-style files, and equivalent standalone prose, and retain the final resolved list/count for auditor Coverage and Limitations.
- [x] When reference search finds no dependents, fall back to the valid modified files alone and record the narrower-evidence limitation instead of producing empty scope.
- [x] Classify Code as always selected and Infra as selected if and only if validated manifest paths touch CI, Docker, IaC, or build configuration; record an explicit run/skip reason and expose ambiguity rather than silently skipping.
- [x] Ask exactly one Step 1 question that states the resolved file count and selected audit types and offers only the resolved scoped bookend, an explicit full-codebase alternative, or decline.
- [x] Record the selected state and any decline or bookend-scope-unusable reason without inventing fixed field names; never infer full-codebase scope from size and never ask again after Step 1.
- [x] For decline or bookend-scope unusability, perform no audit, set `all-approved: no`, retain the stated reason for Step 6, and allow the existing phase pipeline to continue.
- [x] Review the Stage 1 edit for AC1 and AC3–AC7, including one-hop/no-cap behavior, source/document boundaries, conditional Infra logic, one-time decision behavior, and preservation of existing bundle validation.

## Stage 2: End Audit and Attribution

- [x] Insert one thin bookend step after all waves, existing gates, and Step 5 Diff Security Review but before Step 6 Phase Final Review; choose an idiomatic final heading/number without renumbering or weakening existing steps.
- [x] Load the exact finalized Feature 08 skill and supply only caller-specific inputs and continuation policy; do not copy its output-root, worktree-materialization, audit-matrix, delta-gate, attribution-batching, sum-check, or cleanup mechanics into Phase Execute.
- [x] Reuse the `<phase-baseline>` resolution already obtained for Step 5, use the working checkout as the current target/output root, and ensure no baseline audit begins before the wave loop and existing gates finish.
- [x] Materialize the baseline side through the `Baseline Worktree` leaf at `<phase-baseline>` and retain whether this bookend created or reused the worktree so cleanup cannot remove a pre-existing checkout.
- [x] Derive the phase-specific audit artifact name and short-SHA baseline/current labels, then direct every snapshot report, summary, same-type delta, queue, attribution update, and later addendum under the working checkout's `dev/[audit-name]/` hierarchy.
- [x] Build one rendered auditor prompt template whose only snapshot-varying fields are target root, snapshot label, and output directory.
- [x] Keep the prompt's scope and intent byte-identical across snapshots and state that the manifest supplies scope/intent, stated intent never excuses a finding, standalone documentation is excluded, and this run overrides `Auditor - Infra`'s Documentation category.
- [x] In the shared prompt, constrain test files to `Auditor - Code` Categories 2, 5, 8, and 9 only and do not apply the remaining categories.
- [x] For an accepted bookend, run Code for baseline and current back to back; run Infra for both sides only when Stage 1 selected it, using separate reports and independent count domains.
- [x] Require both corresponding full findings reports to exist and state their own totals before spawning `Auditor - Delta`; treat partial returns, missing totals, or missing files as incomplete evidence and never cross audit types.
- [x] Keep provisional current-side findings out of regression reporting until `Auditor - Attribution` probes both trees; partition every provisional item into disjoint subsystem batches and prove batch counts sum to the delta's unattributed total.
- [x] Require reconciliation and attribution completion independently for Code and Infra, preserve separate reports/deltas/queues/counts, and record partial or arithmetic failure as missing evidence.
- [x] Release only a baseline worktree created by this bookend and only after all corresponding delta and attribution work has finished; never write an artifact into or remediate the baseline tree.
- [x] On baseline-materialization failure or any incomplete comparison transition, record the concrete reason, set `all-approved: no`, skip invalid downstream bookend operations, and continue toward Step 6.
- [x] Review the Stage 2 edit for AC2 and AC8–AC15, including prompt parameterization, working-checkout artifact ownership, per-type isolation, full-report gates, attribution arithmetic, and worktree lifetime.

## Stage 3: Bounded Remediation and Final Review Evidence

- [x] Build the remediation candidate set only after attribution: include High/Critical findings settled as caused by the phase, and exclude Medium/Low, pre-existing, provisional, unverified-origin, and otherwise non-phase findings.
- [x] Record an empty eligible remediation set as a valid result; otherwise re-spawn `Feature - Implementer` once on the working checkout using the established bounded prose shape from Steps 2.5 and 3, with the exact eligible findings and no new plan-driven loop.
- [x] Cap remediation at one attempt, capture the files it actually touched, and report remaining drift rather than re-running the full audit/remediation cycle.
- [x] Run targeted verification only over remediation-touched files and eligible findings, with no writes to the baseline worktree.
- [x] Append the targeted verification result to the existing same-type delta as explicitly non-comparable with the full end audit; never overwrite the full reports and never supply the targeted pass as a new delta snapshot.
- [x] Record the Step 1 decision, resolved scope count, audit-type run/skip reasons, report/delta/queue paths, reconciliation and attribution outcomes, remediation result, targeted verification status, cleanup state, and every missing-evidence reason in the existing phase evidence flow without adding normal-path logs or a new persistence scheme.
- [x] Feed the complete bookend evidence into both existing Step 6 Prod Code Review prompt templates and ensure any decline, failure, partial evidence, unreconciled delta, attribution mismatch, remediation failure, or unverified fix forces `all-approved: no` while still reaching Step 6.
- [x] Preserve existing Step 2.5 and Step 3 headings and obligations asserted by `tests/test_unity_consumer_contract.py`, along with all wave, checkpoint, visual, QA, Step 5 security, Step 6 review, reporting, and documentation behavior outside the explicit integration points.
- [x] Run `uv run pytest tests/test_agent_corpus_invariants.py tests/test_unity_consumer_contract.py tests/test_propagate_master_assets.py tests/test_pr_review_orchestrator.py` as unchanged regression evidence; compare failures with the recorded baseline and do not run propagation or edit tests.
- [x] Run `uv run pytest tests/` and confirm the feature introduces no failures beyond the recorded 268-collected, 256-passed, 15-failed/subfailed baseline; report generated-output synchronization as pending maintainer propagation when applicable.
- [ ] Manually exercise or retain explicit QA evidence for a scoped run, full-codebase selection, decline, bookend-scope-unusable branch, baseline-worktree failure, prompt byte identity, worktree survival through attribution, and one bounded remediation plus non-comparable addendum.
- [x] Review the completed source change for AC16–AC21, no copied shared sequence, no orchestrator spawn, no generated-output edits, no new normal-path logging, and no persistent state outside planned audit artifacts and existing evidence fields.
