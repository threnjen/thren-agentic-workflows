# Phase 03 Execution Manifest

- **Phase document:** `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`
- **Phase:** `PHASE_03` — Phase Execute Audit Bookend
- **Ordered features:** `08-audit-comparison-contract`, `09-audit-delta-rewire`, `10-phase-execute-audit-bookend`, `11-audit-bookend-guards`
- **Integration:** No separate bootstrap feature is required. `Audit - Delta` and `Phase - Execute` are independent runtime consumers of the shared skill and do not execute together; Features 09 and 10 each integrate that contract, and Feature 11 is the final cross-consumer verification tail required by the Phase document.
- **Baseline:** `uv run pytest tests/` collected 268 tests on 2026-08-11. Pytest reported 256 passed and 15 existing failures/subfailures: a PR Review display-name collision, stale generated-output count/applyTo expectations pending source/generated reconciliation, and the missing Phase 01 GameCI reference workflow. Phase 03 must add no new failure.
- **Propagation:** Pending after source edits. Agents must not run `scripts/propagate_master_assets.py` or edit generated `ports/`/`.github/` files.

## Features

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---:|---|---|---|---|
| `08-audit-comparison-contract` | 1 | yes | none | `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | n/a |
| `09-audit-delta-rewire` | 2 | yes | `08-audit-comparison-contract` | `source_of_truth/agents/delta-auditor.agent.md` | n/a |
| `10-phase-execute-audit-bookend` | 2 | yes | `08-audit-comparison-contract` | `source_of_truth/agents/04-phase-execute.agent.md` | n/a |
| `11-audit-bookend-guards` | 3 | yes | `08-audit-comparison-contract`, `09-audit-delta-rewire`, `10-phase-execute-audit-bookend` | `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` | n/a |

## Dependency Graph

- `09-audit-delta-rewire` depends_on `08-audit-comparison-contract` because it must load the finalized skill slug and pass the confirmed interactive matrix through the skill's real input contract.
- `10-phase-execute-audit-bookend` depends_on `08-audit-comparison-contract` because its thin wiring must supply phase-specific inputs to the finalized shared sequence rather than restating it.
- `11-audit-bookend-guards` depends_on `08-audit-comparison-contract`, `09-audit-delta-rewire`, and `10-phase-execute-audit-bookend` because its topology, single-home, ordering, mutation, and continuation checks span the completed skill and both consumers.
- Features 09 and 10 have disjoint file scopes and no runtime dependency on one another, so they are safe to execute together after Feature 08.

## Execution Schedule

### Wave 1 — parallel

- `08-audit-comparison-contract`

Create the single mechanical contract first. Its finalized slug, caller inputs, prompt-template boundary, gates, and return state are prerequisites for both consumers.

### Wave 2 — parallel

- `09-audit-delta-rewire`
- `10-phase-execute-audit-bookend`

Start both after Wave 1. They consume the same finalized contract but modify separate agent definitions and do not call each other.

### Wave 3 — parallel

- `11-audit-bookend-guards`

Start after all source contracts exist. Add the consolidated, mutation-proven guards across the skill and both consumers.

## Expected Bundle Files

| Feature | Plan | Context | Tasks |
|---|---|---|---|
| `08-audit-comparison-contract` | `dev/feature/08-audit-comparison-contract/08-audit-comparison-contract-plan.md` | `dev/feature/08-audit-comparison-contract/08-audit-comparison-contract-context.md` | `dev/feature/08-audit-comparison-contract/08-audit-comparison-contract-tasks.md` |
| `09-audit-delta-rewire` | `dev/feature/09-audit-delta-rewire/09-audit-delta-rewire-plan.md` | `dev/feature/09-audit-delta-rewire/09-audit-delta-rewire-context.md` | `dev/feature/09-audit-delta-rewire/09-audit-delta-rewire-tasks.md` |
| `10-phase-execute-audit-bookend` | `dev/feature/10-phase-execute-audit-bookend/10-phase-execute-audit-bookend-plan.md` | `dev/feature/10-phase-execute-audit-bookend/10-phase-execute-audit-bookend-context.md` | `dev/feature/10-phase-execute-audit-bookend/10-phase-execute-audit-bookend-tasks.md` |
| `11-audit-bookend-guards` | `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-plan.md` | `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-context.md` | `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-tasks.md` |

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` | `08-audit-comparison-contract`, `09-audit-delta-rewire`, `10-phase-execute-audit-bookend`, `11-audit-bookend-guards` | Consolidated structural guards for skill ownership, consumer references, retained Delta interaction, Phase Execute topology/order, prompt invariants, skip branches, gates, attribution arithmetic, cleanup lifetime, remediation bounds, Step 6 evidence, and deletion/negation non-vacuity proof. |

### Existing Test Files Updated By Multiple Features

None identified. `tests/test_agent_corpus_invariants.py`, `tests/test_propagate_master_assets.py`, and `tests/test_pr_review_orchestrator.py` remain unchanged regression inputs; the new focused module is owned only by Feature 11.

### Manual QA Checklist

- [ ] Run one real Phase Execute bookend on an actual phase. Capture both rendered audit prompts and confirm they are byte-identical except target root, snapshot label, and output directory; confirm the shared scope/intent, documentation exclusion, Infra override when applicable, and reduced test-lens clauses match on both sides.
- [ ] During that run, confirm the baseline worktree exists through the last attribution probe, every artifact is written under the working checkout's `dev/[audit-name]/`, and cleanup occurs only after attribution returns.
- [ ] Exercise Step 1's three outcomes: scoped run, full-codebase run, and declined with a stated reason. Confirm the question appears once, records file count/types, and decline sets `all-approved: no` while still reaching Step 6.
- [ ] After normal manifest/bundle validation succeeds, exercise one unusable `key files modified` scope or worktree-materialization failure. Confirm the reason is recorded, no false pass is reported, and Phase Final Review receives the missing-evidence state; separately confirm missing/ambiguous manifests and incomplete bundles still hard-stop.
- [ ] Run `Audit - Delta` once after extraction and confirm its types, targets, matrix confirmation, conditional delta offer, artifact paths, attribution presentation, research offer, and remediation behavior match the pre-extraction workflow.
- [ ] If a phase-attributed High/Critical finding is available, confirm remediation runs once on the working checkout, targeted verification covers only touched files, and the delta addendum states it is not comparable with the full audits and is never used as a snapshot.
- [ ] Delete or semantically negate each protected source mechanism in turn, confirm the focused guard fails for the named obligation, restore it, and confirm green.

## Phase-Level Regression Gate

1. Run `uv run pytest tests/[final Phase 03 focused test filename]` and retain mutation/negation red-green evidence.
2. Run `uv run pytest tests/test_agent_corpus_invariants.py tests/test_unity_consumer_contract.py tests/test_propagate_master_assets.py tests/test_pr_review_orchestrator.py` unchanged.
3. Run `uv run pytest tests/` and compare against the recorded 268-collected baseline. Any new failure is a Phase 03 regression until explained.
4. Confirm `source_of_truth/skills/` contains 45 skill directories and `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, and both `docs/CODEBASE_CONTEXT.md` count statements agree.
5. Confirm no file under `ports/` or `.github/` changed and no propagation command ran.
6. Report generated synchronization failures as maintainer propagation pending, never as a reason to edit generated output.
