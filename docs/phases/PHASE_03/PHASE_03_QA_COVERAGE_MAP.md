# QA Coverage Map: Phase 03 — PR Review Agent Family

**Date:** 2026-07-16
**Scope:** All eight features of Phase 03 (`01`–`08`), classifying every acceptance
criterion as automated-covered, manual-QA-required, or partial.
**QA Plan:** `docs/phases/PHASE_03/PHASE_03_QA.md`

> **Supersedes the pre-rescope map at this path.** The prior map classified ACs for the
> retired Phase Final Review family (`05c-qa-consolidator`, `05d-security-rollup`,
> `05e-ac-regression`, `05f-seam-analyzer`, `05i-learnings-harvester`) and its six
> superseded feature folders. Feature `02` deleted all five agents, so those rows are
> **void rather than stale** — they cannot be merged forward because their subjects do
> not exist. The historical record is retained in `docs/phases/**`, which feature `02`
> AC6 exempts from the reference sweep.

## Classification rule applied

An AC is **automated-covered** when its expected result is a value a test can compare
(`assert X == Y`) — file existence, frontmatter contents, body contract strings, prune
counts, propagation idempotency, reference sweeps. It is **manual** only when a human
must observe a runtime no assertion over Markdown can reach: an agent actually spawning,
a report actually appearing on disk, a prompt actually not appearing, a network call
actually not being made.

**This phase is unusually lopsided toward automated coverage** — it ships agent Markdown
plus one Python script, and 196 tests across eight files assert the contracts. That is
precisely why the manual residue matters: the tests prove the family is *described*
correctly. Nothing yet proves it *runs*.

## Automated coverage inventory

| Test file | Tests | Covers |
|---|---|---|
| `tests/test_pr_review_orchestrator.py` | 42 | Orchestrator contracts: deleted-machinery absence, base fallback order, self-exclusion, single-interaction declaration, report root, fixture SHA reachability |
| `tests/test_propagate_master_assets.py` | 38 | Pruning across all three roots, `expected_slugs` roster, per-agent tool lists, propagation parity |
| `tests/test_readiness_synthesis_agents.py` | 28 | `05g` contracts, no-status-line, P5-SEC-02 recorded open, posting consent, one-way output |
| `tests/test_narrative_and_test_health_agents.py` | 23 | `05b`/`05f` rescope, delegation declaration, depth requirement statement |
| `tests/test_mechanical_evaluators.py` | 21 | `05c`/`05d`/`05e` rescope, graph NOT-RUN contract, added-line attribution |
| `tests/test_retirement_reconciliation.py` | 21 | Roster of seven, dangling-reference sweep (3 forms), counts, `.gitignore`, idempotency |
| `tests/test_pr_review_skills.py` | 18 | Skill rename, report root, optional-artifact posture, ≤10-line contract |
| `tests/test_retired_evaluator_removal.py` | 5 | Five retired agents absent from source and all three roots |

**Suite state:** `1 failed, 582 passed, 106 subtests`. The single failure is **PERF-01**
(`test_ac9_propagated_guard_median_latency_is_below_50_ms`) and is **not a Phase 03
regression**: at phase baseline `ae9823a` it fails at median 54.54 ms; at HEAD 54.35 ms
— statistically identical. It is Phase 04's already-open release blocker and is **out of
scope for this QA plan**. Do not re-litigate it here, and never relax the budget to make
it pass (done once in PR #22, 50→90 ms, and reverted).

---

## Coverage Map

| Feature | AC | Automated Coverage | Manual QA Needed? | Reason |
|---|---|---|---|---|
| 01-propagator-orphan-pruning | AC1 — prune `claude/agents/` orphans | `test_propagate_master_assets.py` | No | Prune count is an assertable value |
| 01 | AC2 — prune `claude/commands/` orphans | Same | No | Assertable |
| 01 | AC3 — prune `opencode/agents/` orphans | Same | No | Assertable |
| 01 | AC4a — repair dead Codex skills guard | Same | No | Guard match is assertable |
| 01 | AC4b — prune `claude`/`opencode` skill dirs by directory-name expectation | Same | No | Assertable |
| 01 | AC5 — never delete a non-generated file; `claude/agents/README.md` survives | `test_claude_agents_root_holds_only_the_catalogue_and_generated_output` | No | File-survival assertion, expressed as a derived invariant rather than a hardcoded list |
| 01 | AC6 — pruning never changes a surviving identifier | Same | No | Emission-before-prune ordering is assertable |
| 01 | AC7 — zero deletions on the unmodified repo | Same | No | Count equality |
| 01 | AC8 — deletion counts surface in result dict + CLI | Same | No | Return-value shape |
| 01 | AC9 — prune testable without touching the real tree | Temp-repo isolation in the test file | No | Test-infrastructure concern, proven by the tests running at all |
| 02-retired-evaluator-removal | AC1 — five source agents deleted | `test_retired_evaluator_removal.py` | No | File absence |
| 02 | AC2 — generated outputs absent from all three roots | Same | No | File absence |
| 02 | AC3 — `expected_slugs` + `05d` conditional cleaned | `test_propagate_master_assets.py` | No | Assertable |
| 02 | AC4 — `05i` tests deleted, fourth narrowed | `test_readiness_synthesis_agents.py` | No | Assertable |
| 02 | AC5 / AC5b — README rows re-parented; orchestrator roster trimmed | `test_retirement_reconciliation.py` | No | Reference sweep |
| 02 | AC6 — no retired reference outside exempt paths | `test_retirement_reconciliation.py` (3 pattern forms) | No | Sweep is assertable |
| 02 | AC7 — suite passes with an explained count delta | Suite run | No | Count arithmetic |
| 03-pr-review-conventions-skills | AC1–AC2 — skills renamed, frontmatter updated | `test_pr_review_skills.py` | No | Frontmatter equality |
| 03 | AC3 — report root + seven report filenames declared | Same | No | String contract |
| 03 | AC4 — no subphase concepts remain | Same | No | Negative sweep |
| 03 | AC5 — artifacts are optional enrichment | Same | No | Contract string |
| 03 | AC6 — ≤10-line + reports-on-disk retained | Same | No | The *presence* of the contract is assertable. Whether returns are actually ≤10 lines at runtime is 08/AC4 — manual |
| 03 | AC7 — no surviving agent references the old skill names | Same | No | Negative sweep |
| 03 | AC8 — skills propagate; old dirs absent | `test_propagate_master_assets.py` | No | File presence/absence |
| 03 | AC9 — `worktree-baseline` unchanged | Diff / code review | No | Diff equality |
| 04-pr-review-orchestrator | AC1 — orchestrator renamed + rescoped | `test_pr_review_orchestrator.py` | No | Frontmatter |
| 04 | **AC2 — single upfront interaction; no later prompt** | Body contract asserted | **Yes** | A prompt is a runtime event. The body can promise one block and the run still ask a second question. Verified end to end as 08/AC2 |
| 04 | AC3 — base suggestion fallback order | Body assertion | **Partial — live only** | The order is asserted statically; that it *resolves* with `origin/HEAD` unset needs a real repo where it is unset |
| 04 | AC4 — suggester excludes the current branch and its remote-tracking ref | Body assertion | Partial — folded into AC3's live check | The trap is demonstrable in git; the agent's obedience to it is runtime |
| 04 | AC5 — prompt names the three wrong-suggestion cases | Body assertion | No | String contract |
| 04 | **AC6 — base correction reaches every downstream evaluator** | Body assertion only | **Yes** | Propagation of a corrected value across an agent fan-out is observable only in a run |
| 04 | AC7 — report root shape; no branch name in any path component | Body assertion + regex | No (shape) / **Yes (actual creation)** | The declared shape is assertable; that a directory is *created* at it is 08/AC1 |
| 04 | AC8 — deleted machinery absent (ledger, subphase discovery, write-back, archive) | Negative sweep | No | Absence is assertable |
| 04 | AC9 — writes no status line on any path | `test_orchestrator_writes_no_status_line_anywhere` | No | Negative assertion; mutation-verified |
| 04 | AC10 — three roster positions (preflight / six concurrent / synthesis) | Body assertion | No (declaration) / **Yes (behavior)** | That an `05a` failure *stops* the run while an evaluator failure *does not* is runtime — 08/AC3 |
| 04 | AC10b — `.gitignore` tracks the fixture, ignores run output | `test_retirement_reconciliation.py` (real traversal, both directions) | No | Assertable |
| 04 | AC11 — partial-failure semantics; `evaluator-status.jsonl` records | Body assertion | **Yes** | Covered by the forced-failure run, 08/AC3 |
| 04 | AC12 — orchestrator never reads code; returns ≤10 lines | Body assertion | **Yes (return length)** | 08/AC4 |
| 04 | AC13 — pinned fixture exists and is reachable | `rev-parse --verify` assertion | No | SHA reachability is assertable. **The dry run this fixture exists for was deferred to feature `08` — see 08/AC1** |
| 04 | AC14 — propagates; stale slash command absent | `test_propagate_master_assets.py` | No | File absence |
| 05-mechanical-evaluators | AC1–AC2 — renamed; rescoped to the branch diff | `test_mechanical_evaluators.py` | No | Frontmatter + negative sweep |
| 05 | AC3 — `execute` dropped or justified by a named command | Per-agent tool lists in `test_propagate_master_assets.py` | No | Frontmatter equality |
| 05 | AC4 — `05e` retains an explicitly offline read-only audit mode | Body assertion | No | Contract string |
| 05 | **AC5 — each writes its report; returns ≤10 lines** | Body assertion | **Yes** | Report creation is a runtime artifact — 08/AC1, 08/AC4 |
| 05 | AC6 — verifiable added-line attribution, not touched-file filtering | `test_each_body_explicitly_rejects_touched_file_filtering` | **Partial** | The prohibition is asserted and mutation-verified; whether the sweep *obeys* it needs a run against the fixture, where pre-existing findings could be misattributed to the branch |
| 05 | AC7 — cheap tier is an execution condition, never a pass | Body assertion | No | Contract string |
| 05 | AC8 / AC8b / AC8c — roster re-derived; `05a` declared with `execute`; `edit` pinned | `test_propagate_master_assets.py` | No | Tool-list equality |
| 05 | AC9 — propagates; old OpenCode slugs absent | Same | No | File absence |
| 05 | **Graph MCP unavailable → NOT RUN with a reason** | `GRAPH_DEPENDENT_EVALUATORS` contract assertion | **Yes** | Both `05c` and `05d` carry graph dependencies. That an unavailable graph yields NOT RUN rather than a silent degradation to grep is a runtime path |
| 06-narrative-and-test-health | AC1 / AC1b — `05h`→`05f` rename; both descriptions rescoped | `test_narrative_and_test_health_agents.py` | No | Frontmatter |
| 06 | AC2 — `05b` subphase attribution deleted | Same | No | Negative sweep |
| 06 | **AC3 — the narrative says what the branch is *trying to do*** | Body assertion only | **Yes** | Narrative quality is human judgment. A body can demand insight; only a reader can tell whether the output has any |
| 06 | AC4 — `05b` chunks internally; may spawn per-directory readers | Body assertion | **Partial** | Chunking is runtime; the ≤10-line return is 08/AC4 |
| 06 | **AC5 — `05f` demonstrably delegates to `test-analyst`** | Declaration asserted | **Yes** | A declaration is not a delegation |
| 06 | **AC5b — Codex `max_depth` silent inline fallback** | Depth requirement stated in the body; the record marks this **"Verification deferred to manual QA"** rather than Done | **Yes — NOT statically verifiable** | `max_depth` defaults to **1**; `05f`→`test-analyst` and `05b`→per-directory readers both sit at **depth 2**. A blocked spawn falls back to inline work **silently and reports success**. The body will correctly say "delegate" while the runtime does not. Verify from the transcript, never the prompt text. A green suite means nothing here, and the record says so |
| 06 | AC6 — coverage delta base→HEAD, redundancy, flake candidates | Body assertion | Partial | Report content is runtime; folded into 08/AC1 |
| 06 | AC7 — reports written; ≤10-line returns | Body assertion | **Yes** | 08/AC1, 08/AC4 |
| 06 | AC8 — roster + propagation | `test_propagate_master_assets.py` | No | Assertable |
| 06 | AC9 — neither agent acquires `execute` | Per-agent tool list | No | Frontmatter equality |
| 07-synthesis-and-pr-posting | AC1 — `05l`→`05g` rename | `test_readiness_synthesis_agents.py` | No | Frontmatter |
| 07 | AC2 — `05g` reads only reports; inputs pinned to the templates | Same (guard repaired during review — Issue #2) | No | Contract string |
| 07 | AC3 — severity-ordered readiness report at the report root | Body assertion | **Yes (actual output)** | 08/AC1 |
| 07 | **AC4 — `Checks Not Run` names every missing check; never GO while one is missing** | Body assertion, mutation-verified | **Yes** | The fail-closed path exists only at runtime — 08/AC3 |
| 07 | AC5 — writes no status line anywhere | `test_readiness_synthesizer_writes_no_status_line_anywhere` | No | Negative assertion; mutation-verified |
| 07 | AC6 — P5-SEC-02 closed or recorded open | `test_p5_sec_02_is_recorded_open_in_the_synthesizer` | No | **Recorded OPEN by design**, with owner and routing. Mutation-verified: flipping the declaration to "closed" trips the test. This is a tracked deferral, not a QA item |
| 07 | **AC7 — posting honors the upfront choice; *never* makes no network call** | Contract assertions. The `gh pr comment` command guard was **inert** and was repaired during review (Issue #4) | **Yes** | "No syscall was made" is not assertable over Markdown |
| 07 | **AC8 — no PR open / `gh` absent or unauthenticated is not an error** | Body assertion, mutation-verified | **Yes** | Needs a real repo with no PR open and an unauthenticated `gh` |
| 07 | AC9 — output to the PR is one-way | Body assertion. **The posting path's own one-way clause was unguarded** (Issue #3, the review's most serious finding) — repaired | No | Negative assertion, now guarded |
| 07 | AC10 — posting adds no new prompt beyond the designed *ask when ready* | Body assertion | **Yes** | Part of the single-interaction runtime check, 08/AC2 |
| 07 | AC11 / AC11b / AC11c — test rewrite; `05d` conditional deleted not re-keyed; counterexample removed | The test file itself | No | Assertable |
| 07 | AC12 — `05g` propagates; `05l` absent | `test_propagate_master_assets.py` | No | File absence |
| 08-retirement-reconciliation | **AC1 — end-to-end dry run: all seven reports + the `04e` security report under one run dir** | **NONE — recorded NOT DONE** | **Yes — the headline item** | Feature `04` deferred its AC13 dry run to `08`; `08` could not execute it (no agent-spawning tool in that context). **The assembled family has never been run.** |
| 08 | **AC2 — the single-interaction contract holds end to end** | **NONE — recorded NOT DONE** | **Yes** | Verified on the assembled system, never per feature |
| 08 | **AC3 — forced-failure run completes and is not GO** | **NONE — recorded NOT DONE** | **Yes** | Fail-closed behavior under a real failure |
| 08 | **AC4 — every subagent return is ≤10 lines** | **NONE — recorded NOT DONE** | **Yes** | Observed on the run |
| 08 | AC5 — roster is exactly seven plus the delegated `04e` | `test_retirement_reconciliation.py` | No | File presence/absence |
| 08 | AC6 / AC6b / AC6c — no dangling refs (3 forms); counts corrected; `.gitignore` reconciled | Same | No | Sweeps, plus counts recounted from disk rather than by arithmetic |
| 08 | AC7 — stale command absent; replacement present | Same | No | File absence; the replacement name is derived from the propagator, not assumed |
| 08 | AC8 — propagation clean and idempotent | `test_propagation_is_idempotent`, `test_committed_tree_is_at_a_propagation_fixed_point` | No | Second-run diff equality |
| 08 | AC9 — baseline reconciled and explained | Suite run | No | Count arithmetic (561→581, exactly +20) |
| 08 | AC10 / AC11 — decision record reconciled; deferrals recorded with routing | Code review | No | Document review |
| Cross-cutting | **All three harnesses load the propagated family without error** | Propagation parity asserted | **Yes** | Parity of *files* is asserted. That Claude, OpenCode, and Codex each *load* the family is a runtime check against three different runtimes |

## Summary

| Disposition | Count |
|---|---|
| Automated-covered (no manual QA) | 54 |
| Manual QA required | 17 |
| Partial — logic tested; runtime or judgment aspect manual | 6 |

**17 manual QA items** are carried into `PHASE_03_QA.md`, consolidated by integration
surface into **9 checklist sections**. Every item in the manifest's `## Verification
Assets` § Manual QA Checklist is covered; none was dropped.

The distribution is itself the finding. Fifty-four ACs are provably done and four are
not — and those four are **08/AC1–AC4, the dry run**, the criterion the other eight
features were building toward. The recorded contract governs: *a fixture dry-run is
required release evidence; a run whose required evaluators are recorded `not-run` is
below-GO evidence, not a passing run.* Eight green features are not evidence the family
runs.
