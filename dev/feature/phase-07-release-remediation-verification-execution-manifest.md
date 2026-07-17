# Phase 07 — Release Remediation & Verification: Execution Manifest

> **STALE — do not execute. Re-run `@feature-decomposer` against `docs/phases/PHASE_07/PHASE_07_SUMMARY.md` before this phase runs.**
>
> Two independent reasons, both mechanical:
>
> 1. **The feature numbering collides.** This manifest assigns `07-` through `15-` on the premise that `dev/feature/` held only `01-` through `06-`. Phase 03 has since executed and consumed `07-synthesis-and-pr-posting` and `08-retirement-reconciliation`. No feature bundle from this manifest was ever created — `dev/feature/` contains `01-` through `08-`, all from Phases 01–03 — so nothing is lost by re-decomposing, and re-numbering by hand would be busywork.
> 2. **The phase was renumbered 04 → 07.** The content is unchanged; the number is not. Phase 04 is now *Guard Accuracy & Propagation Reach* and owns none of this.
>
> The manifest's own B3 finding already records that the phase document's premises were partly stale at decomposition time. That is a third reason to regenerate rather than patch, and it predates both of the above.

**Phase document:** `docs/phases/PHASE_07/PHASE_07_SUMMARY.md`
**Discovery context:** `docs/phases/DISCOVERY_CONTEXT.md`
**Branch:** `earlier_phase_cleanup` (existing; decomposed in place per user instruction)
**Decomposed:** 2026-07-16

## Numbering Note

*(Superseded — see the staleness banner above. Retained as written.)*

New features start at `07-` because `dev/feature/` already contains `01-` through `06-` from Phases 01–03. Per the numbering convention, the next index is **max+1**, not gap-filling, and existing directories are never renumbered. The `0N-` prefix here encodes execution order within Phase 04 only; it is unrelated to the phase number.

## Ordering Note

Feature order follows the Phase document's own "Notes for Feature - Decomposer" sequence, with two documented changes:

1. **The smoke pass (`08`) is elevated ahead of the Phase 02 verification (`10`).** The Phase document's Key Deliverables table folds the smoke pass into Deliverable 5 (Live multi-harness QA), but its QA Considerations section explicitly directs that "a smoke pass runs early, not at the tail." This follows the Phase document's directive over its own table.
2. **The Phase document's feature 7 (Records and propagation) is split into `13` and `15`.** The Phase document itself requires this: "Documentation that describes verdicts is not part of this feature — it cannot be written before the verdicts it describes, so it belongs at the tail alongside feature 6." `13` owns records that do not depend on a verdict; `15` owns those that do, and serves as the phase's integration feature.

Net: the Phase document's 7 suggested boundaries became 9 features. Deliverable 6 (Record and doc reconciliation) maps to `09` + `13` + `15`.

## Ordered Feature List

1. `07-latency-gate-calibration`
2. `08-live-qa-smoke-pass`
3. `09-guard-rule-security-review`
4. `10-phase-02-security-verification`
5. `11-phase-03-security-remediation`
6. `12-phase-03-runtime-completion`
7. `13-propagation-enumeration-and-records`
8. `14-multi-harness-qa-execution`
9. `15-release-evidence-consolidation`

## Feature Table

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---|---|---|---|---|
| `07-latency-gate-calibration` | 1 | yes | none | `tests/hooks/test_hook_distribution_integration.py`, `tests/hooks/conftest.py` (verify) | n/a |
| `08-live-qa-smoke-pass` | 1 | yes | none | `docs/phases/PHASE_07/PHASE_07-live-qa-smoke.md` [PROPOSED] (new) | n/a |
| `09-guard-rule-security-review` | 1 | yes | none | `.github/hooks/config/file-access-rules.json` (verify), `tests/hooks/fixtures/bash/legacy-parity.json` (verify), `tests/hooks/test_file_access_guard.py` (verify), `tests/hooks/test_bash_command_analyzer.py` (verify), `docs/phases/PHASE_07/PHASE_07-guard-rule-security-review.md` [PROPOSED] (new) | n/a |
| `10-phase-02-security-verification` | 2 | no | `09-guard-rule-security-review` | `docs/phases/PHASE_07/PHASE_07-phase-02-security-rescan.md` [PROPOSED] (new), `.github/hooks/config/file-access-rules.json` (verify), `.github/hooks/lib/framework.py` (verify), `.github/hooks/lib/injection_scanner.py` (verify), `.github/hooks/scripts/injection-scanner.py` (verify) | shares `.github/hooks/config/file-access-rules.json` with upstream `09-guard-rule-security-review` — P2-SEC-03's remediation lives in that file, so a scan run before 09 lands is stale |
| `11-phase-03-security-remediation` | 2 | yes | none | `.github/agents/05-phase-final-review.agent.md`, `.github/agents/05g-artifact-sweeper.agent.md`, `.github/agents/05j-consistency-auditor.agent.md`, `.github/agents/05k-dependency-auditor.agent.md`, `.github/agents/05a-baseline-worktree.agent.md` (verify), `.github/agents/05l-readiness-synthesizer.agent.md`, `scripts/propagate_master_assets.py`, `tests/test_readiness_synthesis_agents.py`, `tests/test_propagate_master_assets.py`, `claude/agents/` (verify), `opencode/agents/` (verify), `codex/` (verify) | n/a — file scope disjoint from `10` in the same wave |
| `12-phase-03-runtime-completion` | 3 | yes | `11-phase-03-security-remediation` | `dev/phase-final-review/PHASE_05/evaluator-status.jsonl`, `readiness-report.md`, `ac-regression-matrix.md`, `05g-artifact-sweeper-report.md`, `docs/phases/PHASE_07/PHASE_07-phase-03-runtime-evidence.md` [PROPOSED] (new) | n/a — runtime dependency on `11`, but no shared file |
| `13-propagation-enumeration-and-records` | 3 | no | `11-phase-03-security-remediation` | `tests/test_propagate_master_assets.py`, four `dev/feature/*/​*-implementation.md` records, `dev/feature/phase-05-phase-final-review-execution-manifest.md`, `docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md`, `docs/phases/PHASE_07/PHASE_07-anchoring-record.md` [PROPOSED] (new) | shares `tests/test_propagate_master_assets.py` with upstream `11-phase-03-security-remediation` — same test function |
| `14-multi-harness-qa-execution` | 4 | yes | `07`, `09`, `10`, `11`, `12`, `13` | `docs/phases/PHASE_07/PHASE_07_QA.md` [PROPOSED] (new), `docs/phases/PHASE_07/PHASE_07_QA_COVERAGE_MAP.md` [PROPOSED] (new) | n/a — only feature in its wave |
| `15-release-evidence-consolidation` | 5 | yes | `07`–`14` (all) | `docs/phases/PHASE_07/PHASE_07-release-evidence.md` [PROPOSED] (new), `docs/hooks/prompt-injection-defense.md`, `docs/hooks/installation.md`, `docs/hooks/hook-verification.md`, `docs/hooks/manual-qa.md`, `docs/phases/PROJECT_ROADMAP.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`, `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`, `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`, `tests/hooks/test_hook_distribution_integration.py` | n/a — only feature in its wave |

## Dependency Graph

```
07-latency-gate-calibration ──────────────────────────────┐
08-live-qa-smoke-pass ────────(informational)─────────────┤
09-guard-rule-security-review ──┬── 10-phase-02-security-verification ──┤
                                │      (shares file-access-rules.json)   │
11-phase-03-security-remediation ─┬── 12-phase-03-runtime-completion ────┤
                                  │      (runtime dep: execute removal)   │
                                  └── 13-propagation-enumeration ────────┤
                                         (shares test_propagate_master_assets.py)
                                                                          │
                                              14-multi-harness-qa-execution
                                                          │
                                              15-release-evidence-consolidation
```

**Dependency reasons:**

- `10 depends_on 09` — **file conflict**. P2-SEC-03's remediation lives in `.github/hooks/config/file-access-rules.json`, which `09` may modify. A Phase 02 scan run before `09` lands classifies a file that then changes.
- `12 depends_on 11` — **runtime requirement**. `11` removes `execute` from `05g`/`05j`/`05k`; evidence produced before that describes agents that no longer exist as configured.
- `13 depends_on 11` — **file conflict, same function**. Verified: `tests/test_propagate_master_assets.py:90` defines `expected_slugs` omitting `05g`/`05j`/`05k`, and line 118 asserts `assertNotIn("execute", agent.tools)` for every enumerated slug. Those three currently declare `execute`. **Adding them before `11` removes `execute` fails the build immediately.**
- `14 depends_on 07, 09, 10, 11, 12, 13` — validates final state.
- `15 depends_on all` — integration feature; cannot audit evidence recency until all evidence exists.

`08` is **informational only**. It feeds findings into `07`, `11`, and `12` while they are in flight but blocks nothing, and nothing blocks it.

## Execution Schedule

- **Wave 1 (parallel):** `07-latency-gate-calibration`, `08-live-qa-smoke-pass`, `09-guard-rule-security-review`
- **Wave 2 (sequential):** `09` must complete, then `10-phase-02-security-verification`. `11-phase-03-security-remediation` is file-disjoint from `10` and may run alongside it; the wave is labeled sequential because `10` is `parallel_safe: no`.
- **Wave 3 (sequential):** `11` must complete, then `12-phase-03-runtime-completion` and `13-propagation-enumeration-and-records`. `12` and `13` are file-disjoint from each other; the wave is labeled sequential because `13` is `parallel_safe: no` against upstream `11`.
- **Wave 4 (sequential):** `14-multi-harness-qa-execution`
- **Wave 5 (sequential):** `15-release-evidence-consolidation`

## Expected Bundle Files

Each feature directory contains three files:

| Directory | Files |
|---|---|
| `dev/feature/07-latency-gate-calibration/` | `07-latency-gate-calibration-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/08-live-qa-smoke-pass/` | `08-live-qa-smoke-pass-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/09-guard-rule-security-review/` | `09-guard-rule-security-review-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/10-phase-02-security-verification/` | `10-phase-02-security-verification-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/11-phase-03-security-remediation/` | `11-phase-03-security-remediation-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/12-phase-03-runtime-completion/` | `12-phase-03-runtime-completion-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/13-propagation-enumeration-and-records/` | `13-propagation-enumeration-and-records-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/14-multi-harness-qa-execution/` | `14-multi-harness-qa-execution-plan.md`, `-context.md`, `-tasks.md` |
| `dev/feature/15-release-evidence-consolidation/` | `15-release-evidence-consolidation-plan.md`, `-context.md`, `-tasks.md` |

## Blocking Scope Questions — Resolve Before Execution

Discovery surfaced findings that invalidate parts of the Phase document. **These are user decisions, not implementer decisions.**

| # | Feature | Finding | Required decision |
|---|---|---|---|
| B1 | `11` | **AC2 is inexpressible.** `"execute": ["Bash"]` (`scripts/propagate_master_assets.py:332`) / `["bash"]` (line 353) have **no allowlist syntax**. "Sandbox `execute` with a command/path allowlist" describes a mechanism that does not exist. | Extend the propagation format (new capability — collides with this phase's "no new capability" rule), or accept `05a`'s unconstrained `execute` as documented residual risk. |
| B2 | `11` | **AC3 has no code to attach to.** No readiness-synthesis Python exists; the readiness path is agent Markdown. "Strict schema + deterministic reducer" is either more prose (does not close P5-SEC-02 — prose is what the Phase 03 scan faulted) or a new unlisted module. | Bring a validator module into scope, or record P5-SEC-02 as **not closable in this phase** with routing. |
| B3 | `12` | **The Phase document's premises are stale.** A complete run (`runs/20260716T034308Z-1/`, 2026-07-16) closed most of Deliverable 4 after the Phase doc was written. All twelve `05a`–`05l` reports exist; `05d-security-rollup-report.md` exists with a real delegated scan; `evaluator-status.jsonl` holds **one** record (`05g`, `incomplete`, valid report path), not eight `not-run` with `report: null`. | Feature `12` is rescoped here to verify-and-record. **`@phase-refiner` should reflect this into `PHASE_04_SUMMARY.md`** — rewriting the phase doc is outside a decomposer's remit. |
| B4 | `09` | **Scope is ~2× the Phase document's estimate, and `legacy_bash_parity` is metadata, not enforcement.** 17 `phase-retiered` entries, not 9. Live enforcement is in `bash_rules`/`rules`/`bash_analysis`; the mapping is not 1:1, and the four curl/wget entries have **no enforcement rule at all** — "reinstating" those means authoring enforcement that never existed. | Confirm the enlarged scope; decide whether authoring absent curl/wget enforcement is in scope or is new capability. |
| B5 | `10` / `12` | **A guaranteed contradiction.** The completed Phase 03 run's scan (`z-security-scan-final.md`) reports P2-SEC-01..03 as **persisting** at `344711d`; feature `10` proceeds from the premise they are remediated. | None needed now — both features route it to `15`'s AC3 contradiction audit by design. Flagged so it is not mistaken for a new failure. |

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| None identified | — | No new test *file* is needed. New tests extend existing suites: `07`'s slow-guard regression proof goes in `tests/hooks/test_hook_distribution_integration.py`; `11`'s capability and containment assertions go in `tests/test_propagate_master_assets.py` and `tests/test_readiness_synthesis_agents.py`. This phase adds no new surface area, so it adds no new suite. |

### Existing Test Files Updated By Multiple Features

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/test_propagate_master_assets.py` | `11-phase-03-security-remediation`, `13-propagation-enumeration-and-records` | **The phase's sharpest conflict.** Both features modify `test_phase_review_agents_match_all_generated_harness_outputs` (line 87). `11` removes `execute` from `05g`/`05j`/`05k`; `13` then adds those slugs to `expected_slugs` (line 90), which the `assertNotIn` at line 118 only tolerates afterward. **Order is load-bearing.** |
| `tests/hooks/test_hook_distribution_integration.py` | `07-latency-gate-calibration`, `15-release-evidence-consolidation` | `07` rewrites the PERF-01 latency gate. `15` must update exact-string assertions (`"50 ms"`, `"117 to 383 ms"`, `"NOT RUN"`, `"residual risk APPROVED 2026-07-15"` at line 267) when it corrects the docs those assertions pin. Different tests in the same file, different waves — no conflict, but both must be aware. |
| `.github/hooks/config/file-access-rules.json` | `09-guard-rule-security-review`, `10-phase-02-security-verification` | `09` may reinstate enforcement; `10` classifies P2-SEC-03, whose remediation lives here. Sequenced 09 → 10 so the Phase 02 evidence is not invalidated by a later rule change. |
| `tests/hooks/test_file_access_guard.py`, `tests/hooks/test_bash_command_analyzer.py`, `tests/hooks/fixtures/bash/legacy-parity.json` | `09-guard-rule-security-review` | Encode the *current, loosened* behavior. Any reinstatement breaks them — correctly. `legacy-parity.json` is hard-coupled: `test_ac7_exact_legacy_inventory` asserts exact `source_pattern` equality plus counts 27/16/11, so pattern edits need lockstep fixture updates. |

### Manual QA Checklist

Cross-feature behavior that no automated test reaches. Every item runs against a **scratch consumer repository**, never this repo.

- [ ] **Both kill switches verified before any denial is provoked.** `file-access-overrides.json` (`{}` to restore) gates only the file-access guard; the scanner reads `injection-overrides.json`, which does not exist — creating it disables the scanner, and **restoring means deleting it**. Arming one and provoking the other is the self-administration failure that bricked two prior sessions.
- [ ] **PreToolUse deny fires under bypass permissions.** This is project goal 2 — protect files *even with bypass permissions* — and it has never been verified live.
- [ ] **Subdirectory sessions work in all three harnesses.** A relative hook path plus fail-closed previously bricked a session. The mechanisms differ: `_project_root_hook_command` (`scripts/propagate_master_assets.py:792`) rewrites Claude and Codex commands but returns OpenCode's **unchanged**. Three tests, three verdicts — a pass on one says nothing about the others.
- [ ] **Friction profile — both halves.** `ls`, `grep`, `npm test > /dev/null`, lock-file reads, and a commit message containing `rm -rf` must **not** prompt, while a genuinely destructive command must. A rule matching ordinary text is a defect, not safety.
- [ ] **PostToolUse output replacement** happens on a high-tier injection match.
- [ ] **Codex coverage boundary** recorded — Read/Grep/WebFetch/WebSearch/Task have no equivalent handler coverage. Confirming the Partial tier is a successful outcome.
- [ ] **Recovery never requires a blocked tool.**
- [ ] **Adversarial checks** the Phase 03 QA plan was faulted for lacking: capability boundaries, canonical symlink containment, untrusted-report trust boundary.
- [ ] **Harness versions recorded.** Prior evidence: Claude Code 2.1.210, Codex 0.144.4, OpenCode 1.16.2, Bun 1.3.14 (2026-07-15). A tier that changed because the harness changed is a finding.
- [ ] **Every NOT RUN carries a reason.** A missing check is a NO-GO input, not an omission.
- [ ] **Scratch repo torn down; both overrides restored.**

## Test Baseline

**The baseline is unstable, and the instability is the phase's own subject matter.** Independent clean-tree runs produced both:

- `416 passed, 15 subtests, 0 failed`
- `415 passed, 1 failed` — `tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms`, at 64 ms against a 50 ms budget

Same tree, same command, different outcomes. That is PERF-01 exactly as the Phase document characterizes it: a probabilistic gate that can be passed by luck. **No feature should read a green pre-run as a stable baseline**, and no feature other than `07` should attribute that failure to itself or attempt to fix it. The budget must not be relaxed — PR #22 raised it 50→90 ms to mask this and was reverted.

Feature-scoped baselines: `tests/test_propagate_master_assets.py` → 23 passed, 15 subtests. Guard suites → 218 passed.

**Runner:** `.venv/bin/python -m pytest tests/` — system `python3` lacks pytest.

## Standing Constraints

Binding across every feature. Sourced from `.github/learnings/cross-phase-decisions.md` and the Phase document.

- **No status line moves without fresh evidence.** Verdicts are issued by the user, by hand. No feature writes one.
- **A fixed budget must never be relaxed to make a gate pass.** PERF-01's reshape is a user-approved AC change (2026-07-16) and is honest only because a deliberately slowed guard must still fail the new gate.
- **"Remediated in code" is not "verified."**
- **Missing or incomplete required checks are a hard readiness gate** — canonical verdict `NO-GO`. **NO-GO is a valid, successful outcome of this phase.**
- **Findings containment:** new findings are fixed here only if **High or Critical**. Medium and below are recorded with routing and deferred.
- **Agent numbers are pipeline positions, not phase numbers.** `05-phase-final-review` and `05a`–`05l` must **not** be renamed to match the renumber.
- **Development fixtures keep legacy identifiers.** `dev/phase-final-review/fixtures/PHASE_05/` and `dev/phase-final-review/PHASE_05/` are pinned to commit SHAs; renaming invalidates the fixture contract.
- **Never restore unrestricted shell/Bash** to satisfy an evaluator AC. Never add an env-var bypass. Never edit generated wiring directly.
- **Propagation contract:** generated roots are `claude/`, `opencode/`, `codex/`. `$source` is guaranteed for hook JSON, **not** for agent Markdown/TOML — do not assert it there.
- **Adoption readiness is out of scope** and needs a roadmap entry from `@project-planner`.
