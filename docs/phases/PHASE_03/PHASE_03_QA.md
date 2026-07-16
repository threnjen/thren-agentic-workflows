# QA Plan: Phase 05 — Phase Final Review Agent Family

> **Renumbered 2026-07-16: this phase is now Phase 03 (formerly Phase 05).** The
> body below is preserved as the historical record from the original review and
> still uses the Phase 05 numbering throughout. Development-fixture paths
> (`dev/phase-final-review/fixtures/PHASE_05/`, `PHASE_05a`/`PHASE_05b`) and the
> `05a`–`05l` agent names are unchanged and remain correct as written. See the
> mapping table in `docs/phases/PROJECT_ROADMAP.md`.

**Date:** 2026-07-15
**Last Updated:** 2026-07-15
**Mode:** Release QA Plan
**Scope:** Consolidated release QA for features 01–06: the Phase Final Review conventions, report templates, baseline-worktree agent, orchestrator, evaluator family 05a–05l, development fixture, readiness synthesis, history harvesting, and Claude/OpenCode/Codex propagation.
**Environment:** Repository root /Users/jennywadkins/github_repos/github-agents-source-of-truth; Python environment .venv; an agent harness that loads the source-of-truth files under .github/agents/ and can spawn the declared 05a–05l agents. Use the code-review-graph MCP server for 05f/05g checks and the existing Security Scan/Test - Analyst delegates where requested.
**Prerequisites:** Use the disposable fixture at dev/phase-final-review/fixtures/PHASE_05/, never the live docs/phases/PHASE_01/ or PHASE_02/ directories. Run .venv/bin/python -m pytest tests/test_propagate_master_assets.py -q and .venv/bin/python -m pytest tests/test_readiness_synthesis_agents.py -q before manual execution. The current results are 21 passed/15 subtests and 6 passed respectively. The full suite command is .venv/bin/python -m pytest tests/ -q; the current baseline is 394 passed, 2 failed, 15 subtests, with the two known failures in tests/hooks/test_hook_distribution_integration.py (propagated-guard median latency and installation-guide classification). Keep those failures recorded as baseline context.

## Features Covered

| Feature | Plan | Implementation Record | Review Record |
|---|---|---|---|
| 01-review-foundation | dev/feature/01-review-foundation/01-review-foundation-plan.md | dev/feature/01-review-foundation/01-review-foundation-implementation.md | dev/feature/01-review-foundation/01-review-foundation-review.md |
| 02-final-review-orchestrator | dev/feature/02-final-review-orchestrator/02-final-review-orchestrator-plan.md | dev/feature/02-final-review-orchestrator/02-final-review-orchestrator-implementation.md | dev/feature/02-final-review-orchestrator/02-final-review-orchestrator-review.md |
| 03-mechanical-evaluators | dev/feature/03-mechanical-evaluators/03-mechanical-evaluators-plan.md | dev/feature/03-mechanical-evaluators/03-mechanical-evaluators-implementation.md | dev/feature/03-mechanical-evaluators/03-mechanical-evaluators-review.md |
| 04-delegating-evaluators | dev/feature/04-delegating-evaluators/04-delegating-evaluators-plan.md | dev/feature/04-delegating-evaluators/04-delegating-evaluators-implementation.md | dev/feature/04-delegating-evaluators/04-delegating-evaluators-review.md |
| 05-deep-judgment-evaluators | dev/feature/05-deep-judgment-evaluators/05-deep-judgment-evaluators-plan.md | dev/feature/05-deep-judgment-evaluators/05-deep-judgment-evaluators-implementation.md | dev/feature/05-deep-judgment-evaluators/05-deep-judgment-evaluators-review.md |
| 06-readiness-synthesis | dev/feature/06-readiness-synthesis/06-readiness-synthesis-plan.md | dev/feature/06-readiness-synthesis/06-readiness-synthesis-implementation.md | dev/feature/06-readiness-synthesis/06-readiness-synthesis-review.md |

## Coverage Map

- Coverage Map: docs/phases/PHASE_05/PHASE_05_QA_COVERAGE_MAP.md

---

## Summary of Changes

Phase 05 adds three shared skills and the 05a baseline-worktree specialist,
then adds the 05-phase-final-review orchestrator and eleven evaluator agents:
05b, 05c, 05d, 05e, 05f, 05g, 05h, 05i, 05j, 05k, and 05l. The feature set
also adds a copied Phase 01/02 fixture, canonical master-QA/security/AC/readiness
report contracts, ledger and commit-message baseline selection, bounded
partial-failure handling, fixture-only verdict write-back, and propagation to
Claude, OpenCode, and Codex.

The current retained dry-run artifacts are intentionally bounded evidence, not
complete runtime proof. They show a NO-GO fixture result, preserve P2-SEC-01,
P2-SEC-02, and P2-SEC-03 as Persisting, and record missing evaluator reports as
not-run. A release decision must wait for the manual checks below, especially
the live 05d delegated scan and the complete evaluator fan-out.

## Automated Test Coverage

The existing tests/test_propagate_master_assets.py is the propagation gate
used across the feature sequence. It currently passes 21 tests and 15
subtests, including selected Phase Final Review source discovery, Claude/
OpenCode/Codex renderer parity, the 05d NOT RUN/NO-GO contract, orchestrator
output presence, and propagation safety behavior. The focused
tests/test_readiness_synthesis_agents.py adds six source/mirror contract
tests for 05l and 05i. These tests cover static declarations and generated
output parity; they do not prove live agent execution, delegate delivery,
report creation, line-limited returns, graph degradation, or fixture-safe
write-back.

No new automated test files were required by the manifest checklist, but the
current tree does contain the feature-06 focused file
tests/test_readiness_synthesis_agents.py; it is counted as automated
coverage, not manual QA. No application source or UI changes are in scope.

The full suite is not green for this phase baseline: 394 passed and 2 known
pre-existing hook-distribution tests failed. Do not use those failures as
evidence that the Phase Final Review agents passed or failed; retain them as
release context until their owning work is addressed.

---

## Manual QA Checklist

The checklist is grouped by integration surface. Every evaluator check below
must use the source-of-truth agent name and the fixture root
dev/phase-final-review/fixtures/PHASE_05/. A report path is valid only when
it is a readable, regular, non-empty file under the current
dev/phase-final-review/PHASE_05/ report root. A missing report is a failed
coverage check, never a pass.

### Fixture and Baseline Preflight

**Features:** 01-review-foundation, 02-final-review-orchestrator

**Covers ACs:** 01/AC3–AC5, 02/AC3–AC5

**Why manual:** Worktree state, local history selection, user confirmation,
fixture provenance, and visible preflight refusal/warning behavior require a
real repository and agent session.

#### Happy Path

- [ ] **Inventory the synthetic subphases and preserved security case** — From the repository root, run rg --files dev/phase-final-review/fixtures/PHASE_05 | sort; compare the five Phase 01 source files with the five PHASE_05a files and the six Phase 02 source files with the six PHASE_05b files using the filename mapping in dev/phase-final-review/fixtures/README.md and cmp. Inspect PHASE_05b_SUMMARY.md and PHASE_05b-security-scan.md. **Expected:** Exactly PHASE_05a and PHASE_05b are discoverable pseudo-subphases; all copied contents compare byte-for-byte; the optional PHASE_05b_DISCOVERY_CONTEXT.md is present; the Phase 02 summary retains its release-blocked/NO-GO content; and P2-SEC-01, P2-SEC-02, and P2-SEC-03 are present in the copied security scan.
- [ ] **Confirm a ledger-derived baseline before fan-out** — In the agent harness, invoke 05 Phase - Final Review with phase PHASE_05, explicit fixture root dev/phase-final-review/fixtures/PHASE_05/, and ledger run eval/runs/phase-phase-final-review-2/ledger-commits.jsonl; stop after preflight and do not start evaluators. **Expected:** Preflight says baseline source: ledger, shows the first feature checkpoint and its parent (the current evidence is first feature commit 291fc8a0c437e3014a09a9a3709157d0e597f81e and suggested baseline 48d37504bf7a59d29358a512cd4183c3f0fe0996), and requests explicit confirmation of that exact commit before delegating 05a.
- [ ] **Exercise the commit-message fallback in a disposable clone** — Run tmp=$(mktemp -d), git clone --local "$PWD" "$tmp/repo", and rm -rf "$tmp/repo/eval/runs"; invoke the same orchestrator from $tmp/repo against its copied fixture and stop after preflight. **Expected:** Preflight names baseline source: eval commit-message fallback, derives the parent of the first eval: implement ... checkpoint for the first subphase, and asks for explicit confirmation; it never silently guesses or treats the missing ledger as a clean result.
- [ ] **Refuse an itemized missing artifact** — Copy the fixture to a temporary directory with tmp=$(mktemp -d), cp -a dev/phase-final-review/fixtures/PHASE_05 "$tmp/PHASE_05", and rm "$tmp/PHASE_05/PHASE_05a/PHASE_05a_QA.md"; invoke the orchestrator with $tmp/PHASE_05 as the explicit fixture root and stop at preflight. **Expected:** The run refuses before evaluator fan-out and prints an item beginning MISSING — PHASE_05a — that identifies the QA document category, expected path/pattern, and concrete missing-file reason.
- [ ] **Run 05a and verify owned worktree cleanup** — Invoke Baseline Worktree with repository root /Users/jennywadkins/github_repos/github-agents-source-of-truth, baseline 48d37504bf7a59d29358a512cd4183c3f0fe0996, and a new absolute target under a temporary directory. Inspect the returned text, then tell the agent the review is complete and inspect git worktree list --porcelain. **Expected:** The agent returns an absolute path only after detached HEAD and clean-status checks, the return is no more than 10 lines and states created/reused status, and an owned worktree is removed while a reused or dirty worktree is not removed.

#### Error Handling

- [ ] **Verify the wrong-model warning ordering** — Start the orchestrator in a session using a model below the declared state-of-the-art tier and invoke it against the fixture. **Expected:** A visible model-tier warning appears before any preflight input is read or evaluator work starts; the run records the limitation as an execution condition and does not count it as a pass.

### Mechanical Evaluator Runtime

**Features:** 03-mechanical-evaluators

**Covers ACs:** 03/AC1–AC5

**Why manual:** The graph dependency, report-writing behavior, known fixture drift,
no-dependency result, and observed return length are runtime outcomes.

#### Happy Path

- [ ] **Dry-run 05g with the graph available** — After confirming the fixture baseline, run 05g-artifact-sweeper through 05 Phase - Final Review against dev/phase-final-review/fixtures/PHASE_05/; inspect dev/phase-final-review/PHASE_05/05g-artifact-sweeper-report.md and the returned summary. **Expected:** The report is a readable non-empty artifact sweep scoped to the baseline-to-final diff, the graph dead-code check is either evidenced or explicitly bounded, no unrelated repository dead code is attributed to the phase, and the return is no more than 10 lines.
- [ ] **Dry-run 05j against the two fixture subphases** — Run 05j-consistency-auditor through the orchestrator with the same fixture and inspect 05j-consistency-auditor-report.md and its return. **Expected:** The report is non-empty, names at least one concrete Phase 01-versus-Phase 02 naming, error-handling, or repeated-pattern drift with both evidence and a canonical recommendation, and the return is no more than 10 lines.
- [ ] **Dry-run 05k with no dependency-manifest changes** — Run 05k-dependency-auditor through the orchestrator against the fixture and inspect 05k-dependency-auditor-report.md. **Expected:** The report contains a completed no new dependencies check and a return of no more than 10 lines; any unavailable license or vulnerability evidence is listed as NOT RUN rather than represented as a clean scan.

#### Error Handling

- [ ] **Stop the graph dependency and rerun 05g** — In a disposable agent-harness profile, disable the code-review-graph MCP server or make refactor_tool unavailable, then invoke 05g against the unchanged fixture. **Expected:** The dead-code/graph check is recorded as NOT RUN with the concrete tool failure reason, the evaluator status is not-run or incomplete, and the eventual readiness ceiling is below GO; no clean sweep is fabricated.

### Delegating Evaluator Runtime

**Features:** 04-delegating-evaluators

**Covers ACs:** 04/AC1–AC4, 04/AC6

**Why manual:** These checks cross agent boundaries and require observing delegated
Security Scan/Test - Analyst responses and the resulting reports.

#### Happy Path

- [ ] **Dry-run 05c and inspect the consolidated walkthrough** — Run 05c-qa-consolidator through the orchestrator against the fixture and inspect master-qa.md plus 05c-qa-consolidator-report.md. **Expected:** The canonical report is readable and non-empty, every retained check appears once, superseded checks are recorded, conflicts are visible, and the current fixture baseline is consistent with 31 retained checks and three supersessions; all source manual checks remain NOT RUN unless actually executed. The evaluator return is no more than 10 lines.
- [ ] **Dry-run 05d with the Security Scan delegate available** — Run 05d-security-rollup through the orchestrator against the fixture with the existing Security Scan agent available; inspect security-rollup.md, 05d-security-rollup-report.md, and the run-status record. **Expected:** P2-SEC-01, P2-SEC-02, and P2-SEC-03 each appear exactly once with one of the template classifications Fixed, Persisting, or Reintroduced; the delegated final-scan report/path is visible; final evidence, not absence of evidence, controls a Fixed result; and the return is no more than 10 lines.
- [ ] **Dry-run 05h and inspect delegated health evidence** — Run 05h-test-health through the orchestrator against the fixture with Test - Analyst available; inspect 05h-test-health-report.md. **Expected:** The report has distinct coverage-delta, cross-subphase redundancy, and flake-candidate sections, explicitly says not-measurable when coverage tooling/evidence is unavailable, preserves delegate evidence paths, and the return is no more than 10 lines.

#### Error Handling

- [ ] **Force the Test - Analyst delegate to fail** — In a disposable harness profile, make Test - Analyst unavailable or time it out and rerun 05h against the fixture. **Expected:** 05h writes a NOT RUN/incomplete result with the concrete delegate reason, the evaluator status records the missing check, and the readiness ceiling is below GO; missing analysis is never presented as healthy coverage.

### Deep-Judgment Evaluator Runtime

**Features:** 05-deep-judgment-evaluators

**Covers ACs:** 05/AC1–AC5

**Why manual:** Chunked narrative behavior, complete matrix cardinality, graph
availability, and observed return payloads are not proven by static contracts.

#### Happy Path

- [ ] **Dry-run 05b with bounded diff chunks** — Run 05b-change-narrator through the orchestrator against the fixture with a confirmed baseline; inspect 05b-change-narrator-report.md and the return. **Expected:** The report contains per-subphase attribution, records any shared churn hotspots, identifies the chunking boundary, does not claim a single unbounded full-diff read, and the return is no more than 10 lines.
- [ ] **Dry-run 05e and verify all 26 AC rows** — Before running, count the checked success-criteria rows with rg -c '^- \[[ x]\] ' dev/phase-final-review/fixtures/PHASE_05/PHASE_05a/PHASE_05a_SUMMARY.md and the corresponding PHASE_05b_SUMMARY.md; add the two counts. Run 05e-ac-regression through the orchestrator and inspect ac-regression-matrix.md and the evaluator hand-off. **Expected:** The matrix has exactly 26 rows (17 from PHASE_05a plus 9 from PHASE_05b), every row has a status, manual-only criteria are INCONCLUSIVE (not-verifiable) or NOT RUN with reasons, and the return is no more than 10 lines.
- [ ] **Run 05f with both graph operations available** — With the code-review-graph server available, run 05f-seam-analyzer through the orchestrator and inspect 05f-seam-analyzer-report.md. **Expected:** The report evidences exact get_impact_radius and get_bridge_nodes calls and ends with either concrete seam findings or the completed conclusion no seams detected; it does not silently substitute another operation, and the return is no more than 10 lines.

#### Error Handling

- [ ] **Run 05f with the graph unavailable** — Disable the code-review-graph MCP server or make either required operation unavailable, then rerun 05f against the fixture. **Expected:** The report/status identifies the exact unavailable operation or name mismatch as NOT RUN, records the follow-up, and never calls the absence of graph evidence no seams detected; the return is no more than 10 lines.

### Full-Flow Synthesis and Verdict Lifecycle

**Features:** 02-final-review-orchestrator, 04-delegating-evaluators,
05-deep-judgment-evaluators, 06-readiness-synthesis

**Covers ACs:** 02/AC6–AC7, 04/AC6, 06/AC1–AC8

**Why manual:** This is the cross-agent release decision path: live report
fan-out, fail-closed synthesis, severity ordering, real-history evidence, and
fixture-only status write-back.

#### Happy Path

- [ ] **Run the complete fixture flow through 05l** — With the orchestrator, all 05a–05l evaluators, code-review-graph, Security Scan, and Test - Analyst available, run preflight through 05l against dev/phase-final-review/fixtures/PHASE_05/; verify master-qa.md, security-rollup.md, ac-regression-matrix.md, and readiness-report.md are readable non-empty files. **Expected:** All four canonical artifacts exist; the security rollup classifies P2-SEC-01..03; the AC matrix contains all 26 fixture criteria; the readiness blocking list is severity ordered; and the fixture's known High findings keep the final verdict NO-GO until remediated. Each evaluator return is no more than 10 lines.
- [ ] **Run a forced-failure full flow** — Repeat the full flow with 05d-security-rollup forced to fail (the retained archive pattern is runs/20260715T230000Z-2/); inspect evaluator-status.jsonl and the run-specific readiness report. **Expected:** The run reaches synthesis without aborting, records 05d with status not-run and a concrete reason/report path of null, names that missing check under Checks Not Run, and returns NO-GO; even if no other blocker exists, the maximum outcome is no blockers found, coverage incomplete.
- [ ] **Exercise fixture-only verdict write-back** — Run the completion step with write-back targets set to dev/phase-final-review/fixtures/PHASE_05/write-back/PROJECT_ROADMAP.md and dev/phase-final-review/fixtures/PHASE_05/write-back/PHASE_05_SUMMARY.md; compare the real files before and after with git diff --exit-code -- docs/phases/PROJECT_ROADMAP.md docs/phases/PHASE_05/PHASE_05_SUMMARY.md. **Expected:** Only the fixture copies receive the exact NO-GO status-line replacement; no manual edit is needed; the real roadmap and phase summary remain unchanged.
- [ ] **Harvest a real-history learning proposal with 05i** — Run 05i-learnings-harvester against the repository's Phase 01/02 and Phase Final Review history, including 4dd01e9, eval/runs/phase-phase-final-review-2/ledger-commits.jsonl, and its ledger-events.jsonl; inspect 05i-learnings-harvester-report.md and both draft directories. **Expected:** At least one evidence-backed learning or instruction proposal exists under the current report root, cites real history/QA/ledger evidence, has the required draft structure, returns no more than 10 lines, and does not edit accepted .github/learnings/ or .github/instructions/ files.

### Cross-Harness Propagation and Safety

**Features:** 01-review-foundation, 02-final-review-orchestrator,
03-mechanical-evaluators, 04-delegating-evaluators,
05-deep-judgment-evaluators, 06-readiness-synthesis

**Covers ACs:** 01/AC6, 02/AC8, 03/AC6, 04/AC7, 05/AC6, 06/AC9

**Why manual:** The manifest requires propagation after every feature; the
current automated list explicitly names only a subset of the 05x agents, so
the remaining source-to-harness naming and loading paths need a real
cross-harness smoke check.

- [ ] **Propagate and smoke-check each feature checkpoint** — At each feature checkpoint, run .venv/bin/python scripts/propagate_master_assets.py --once, then inspect claude/, opencode/, and codex/ outputs and rerun the command. Check feature 01's three skills plus 05a, feature 02's orchestrator, feature 03's 05g/05j/05k, feature 04's 05c/05d/05h, feature 05's 05b/05e/05f, and feature 06's 05i/05l. **Expected:** Every source asset is present in the appropriate Claude/OpenCode/Codex representation, delegated names resolve after z- renaming where applicable, the second propagation is a no-op, and no unrelated output changes are introduced.
- [ ] **Verify read-only boundaries in a disposable run** — Capture the pre-run status/diff for .github/agents/, .github/skills/, scripts/, tests/, docs/phases/PROJECT_ROADMAP.md, and docs/phases/PHASE_05/PHASE_05_SUMMARY.md; run the complete fixture flow and fixture-only write-back; compare those paths afterward. **Expected:** Evaluators and synthesis do not modify source, tests, configuration, the live roadmap, or the live phase summary; only the declared report root and fixture write-back copies change.

---

## Notes

- Current retained artifacts are bounded and fail closed: the readiness report
  is NO-GO, the final delegated Security Scan is absent, and eight evaluator
  checks are recorded as not-run. Do not promote those artifacts to complete
  runtime evidence.
- P2-SEC-01, P2-SEC-02, and P2-SEC-03 must remain individually visible in the
  security rollup and readiness blocking list. A source finding without final
  evidence cannot be labelled Fixed.
- The fixture's Phase 01/02 documents are copied evidence, not the Phase 05
  product under review. Do not execute the 31 underlying Phase 01/02 manual
  walkthrough rows as Phase 05 evaluator tests; the Phase 05 manual scope is
  the fixture/evaluator/orchestrator integration above.
- No frontend/UI changes exist in this phase, so no visual UI or accessibility
  checklist is required.
- The repository's normal rtk wrapper reported a hook-integrity failure during
  implementation; QA commands above use the project .venv directly.
