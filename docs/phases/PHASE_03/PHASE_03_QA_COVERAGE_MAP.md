# Phase 03 QA Coverage Map

| Feature | Automated evidence | Manual evidence | Status |
|---|---|---|---|
| 08 Audit comparison contract | Focused guards validate inputs, path confinement, report gates, attribution, and cleanup ownership. | Live prompt and worktree lifecycle. | Covered statically; runtime pending |
| 09 Audit Delta rewire | Focused guards validate retained interaction and single shared-skill handoff. Grouped regression artifact covers corpus consumers. | Live Delta comparison, conditional offers, rerun, and remediation flow. | Covered statically; runtime pending |
| 10 Phase Execute audit bookend | Focused guards validate five-leaf topology, one-time scope choice, ordering, prompt contract, gates, branches, remediation, and Step 6 evidence. | Scope choice, materialization failure, prompt identity, cleanup, remediation, and final-review handoff. | Covered statically; runtime pending |
| 11 Audit bookend guards | `tests/test_phase_execute_audit_bookend.py` proves named obligations and red/green mutations. | Review the retained evidence boundary and run the manifest checklist. | 13/13 focused pass |

## Manifest verification assets

- New focused test: `tests/test_phase_execute_audit_bookend.py`
- Existing regression tests: `tests/test_agent_corpus_invariants.py`,
  `tests/test_unity_consumer_contract.py`,
  `tests/test_propagate_master_assets.py`, and
  `tests/test_pr_review_orchestrator.py`
- Full suite: `uv run pytest tests/`
- Visual verification: skipped because this repository is not a Unity project.
