# qa Coverage Map: Phase 01 — Engagement Preparation & Baselines

**Date:** 2026-07-22
**Scope:** Features 10–13 (engagement-configuration schema, preparation orchestrator, graph/baseline capture, preparation runbook)

All deliverables in this phase are Markdown agent/skill assets. The existing propagation suite (`tests/test_propagate_master_assets.py` and siblings) is the automated guard; as of feature 13 it is fully green (233 passed, 0 failed). "Automated Coverage" below therefore means either the propagation/count-guard suite or static code-review evidence recorded in the per-feature review records — both already complete. Manual qa is reserved for runtime behavior that only an actual orchestrator run against real repos can demonstrate.

| Feature | AC | Automated Coverage | Manual qa Needed? | Reason |
|---------|----|--------------------|-------------------|--------|
| 10-engagement-configuration-schema | AC1 | Code-review evidence (review record: Met) | No | File-existence/content check, statically verified |
| 10-engagement-configuration-schema | AC2 | Code-review + grep evidence (review record: Met) | No | Static text property (unbounded pairs, no pilot facts) |
| 10-engagement-configuration-schema | AC3 | Code-review evidence (review record: Met) | No | Static schema content |
| 10-engagement-configuration-schema | AC4 | Code-review evidence (review record: Met) | No | Static schema content |
| 10-engagement-configuration-schema | AC5 | Code-review evidence (review record: Met) | Partial — runtime fail-fast only | Error templates are static, but whether the orchestrator actually emits the specific pair/field error and halts before any work requires a live bad-config run (Check 3) |
| 10-engagement-configuration-schema | AC6 | Code-review evidence (review record: Met) | No | Static doctrine statement |
| 10-engagement-configuration-schema | AC7 | Code-review evidence (review record: Met) | No | Documented convention |
| 10-engagement-configuration-schema | AC8 | Code-review evidence; features 11/12 verified vocabulary reuse in their reviews | No | Static contract, downstream reuse already reviewed |
| 10-engagement-configuration-schema | AC9 | Propagation fixed point + `uv run pytest tests/` (re-verified in review) | No | Fully automated |
| 11-preparation-orchestrator | AC1 | Code-review evidence (review record: Met) | No | Frontmatter/house-style, static |
| 11-preparation-orchestrator | AC2 | Code-review evidence (review record: Met) | Partial — runtime fail-fast only | Same live bad-config run as 10/AC5 (Check 3) |
| 11-preparation-orchestrator | AC3 | Code-review evidence (review record: Met, static) | Yes | Loop order docs→graph→record must be observed in a real run with real docs-writer delegation (Check 1) |
| 11-preparation-orchestrator | AC4 | Code-review evidence (review record: Met) | No | Staleness procedure is explicit prose; skip behavior tested via Check 2 under AC9 |
| 11-preparation-orchestrator | AC5 | Code-review evidence (review record: Met) | Partial — observed doc sets | Role-scoped doc sets per side verified during Check 1 |
| 11-preparation-orchestrator | AC6 | Review record: **Unverified (runtime)** | Yes | Analysis-branch invariants (no source modified, byte-identical original/main history, branch never pushed) observable only after a real run (Checks 1, 4) |
| 11-preparation-orchestrator | AC7 | Review record: **Unverified (runtime)** | Yes | Delegation/context-budget hard rule requires a runtime transcript (Check 1) |
| 11-preparation-orchestrator | AC8 | Review record: **Unverified (runtime)** | Yes | Fail-fast on unresolvables only, naming side + cause, requires a live bad-path run (Check 3) |
| 11-preparation-orchestrator | AC9 | Review record: **Unverified (runtime)** | Yes | Idempotent re-run (docs skipped, graph still runs, skips reported) requires a real re-run (Check 2) |
| 11-preparation-orchestrator | AC10 | Code-review + grep evidence (review record: Met) | No | Static text property |
| 11-preparation-orchestrator | AC11 | Propagation fixed point + pytest (review record: Met) | No | Fully automated |
| 12-graph-baseline-capture | AC1 | Review record: Met (static) with runtime deferral | Yes | Graph build actually running on every invocation — including docs-skip re-runs — needs live observation (Checks 1, 2) |
| 12-graph-baseline-capture | AC2 | Code-review evidence (review record: Met) | No | Parse-based/no-gate stance is static; coverage-gap recording observed incidentally in Check 5 |
| 12-graph-baseline-capture | AC3 | Code-review evidence (review record: Met) | No | Fail-fast/NOT-RUN text static; graph-tool failure cannot be reliably staged and is excluded |
| 12-graph-baseline-capture | AC4 | Review record: Met (static); cross-pair identity deferred to pilot | Yes | Snapshots measured identically across both sides of each pair, SHA-pinned, is a runtime property (Check 5) |
| 12-graph-baseline-capture | AC5 | Code-review evidence (review record: Met) | Partial — label present in emitted artifact | Verify the produced snapshot file carries the internal-only label (Check 5) |
| 12-graph-baseline-capture | AC6 | Code-review evidence (review record: Met) | Partial — pointers resolve | Verify snapshot lives on the analysis branch and per-side pointers resolve (Checks 1, 5) |
| 12-graph-baseline-capture | AC7 | Code-review + grep evidence (review record: Met) | No | Static tool-name check |
| 12-graph-baseline-capture | AC8 | Code-review + grep evidence (review record: Met) | No | Static text property |
| 12-graph-baseline-capture | AC9 | Propagation fixed point + pytest (review record: Met) | No | Fully automated |
| 13-preparation-runbook | AC1 | Code-review evidence (review record: Met) | Partial — runbook usability | The pilot run doubles as validation that the runbook's steps are followable end to end (all Checks) |
| 13-preparation-runbook | AC2 | Code-review + grep evidence (review record: Met) | No | Static text property |
| 13-preparation-runbook | AC3 | Count-derivation guards + reviewer recount from disk | No | Fully automated + reviewed |
| 13-preparation-runbook | AC4 | `uv run pytest tests/` — 233 passed, 0 failed | No | Fully automated |
| 13-preparation-runbook | AC5 | None possible (external pilot repos) | **Yes — NOT RUN, deferred** | The five pilot checks are the phase's only runtime evidence. Owner: the user (threnjen). Pilot repo paths TBD in `docs/phases/DISCOVERY_CONTEXT.md`. Must never be reported as passed until executed |
| 13-preparation-runbook | AC6 | Code-review evidence (review record: Met) | No | Deferral honestly recorded with named owner |

## Manual qa Check Index

| Check | Description | Covers |
|-------|-------------|--------|
| 1 | Unprepared pilot engagement fully prepared per side (role-scoped docs, built graph, SHA-pinned internal snapshot) | 11/AC3, 11/AC5, 11/AC6, 11/AC7, 12/AC1, 12/AC6, 13/AC1, 13/AC5a |
| 2 | Idempotent re-run — docs skipped, graph still runs, skips reported | 11/AC4, 11/AC9, 12/AC1, 13/AC5b |
| 3 | Deliberately bad config path — specific fail-fast error naming pair/field, nothing prepared | 10/AC5, 11/AC2, 11/AC8, 13/AC5c |
| 4 | Original/main branch tip SHAs byte-identical before/after, no source modified | 11/AC6, 13/AC5d, 13/AC5e |
| 5 | Baseline snapshots measured identically across both sides of each pair, labeled internal-only | 12/AC4, 12/AC5, 12/AC6, 13/AC5a |

**Status of all five checks: NOT RUN — deferred. Owner: the user (threnjen).** Prerequisite (pilot repo local paths) does not yet exist; see feature 13 AC6.
