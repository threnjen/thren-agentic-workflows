# Phase 02 QA Coverage Map

| Acceptance area | Automated evidence | Manual evidence | Status |
|---|---|---|---|
| Contract skill exists and defines the reading boundary | `tests/test_phase_refiner_final_check.py` topology and skill-reference checks | None required | PASS — focused suite 26/26 |
| Hidden reviewer is a read-only leaf | Topology checks parse the reviewer frontmatter, tools, and absent roster | Entry A cold-start check | Automated PASS; manual pending |
| Refiner declares and references the reviewer and shared skill | Roster and shared-reference checks | None required | PASS — focused suite 26/26 |
| Entry A and Entry B both reach the offer | Workflow topology and mutation checks | Exercise both entry paths | Automated PASS; manual pending |
| Blindness boundary is preserved | Spawn prompt path-only and no-briefing mutation checks | Inspect reviewer input during a live run | Automated PASS; manual pending |
| Accept, decline, no-answer, and failure continue without retry | Continuation, failure, and no-retry mutation checks | Exercise each branch | Automated PASS; manual pending |
| Findings are relayed and only accepted findings are folded in | Fold-in and verbatim-relay mutation checks | Accept a subset of findings | Automated PASS; manual pending |
| Roadmap and discovery synchronization occurs after fold-in | Ordering and exactly-once synchronization checks | Confirm both files after a live run | Automated PASS; manual pending |
| No findings artifact is written by the reviewer | Contract and response-only checks | Inspect the worktree after a live run | Automated PASS; manual pending |
| Regression corpus remains compatible | `tests/test_agent_corpus_invariants.py` | None | 7 passed in wave gates |
| Generated output is synchronized | `tests/test_propagate_master_assets.py` and fixed-point guard | Maintainer propagation | NOT VERIFIED — propagation pending; known baseline wildcard failure |
| Full repository behavior | `uv run pytest tests/` | None | NO-GO — 12 baseline failures plus propagation-pending synchronization; retry also exposed generated-tree mutations from the fixed-point guard |
| Unity visual behavior | Not applicable | Not applicable | SKIPPED — not a Unity project |

## Gate interpretation

The Phase 02-focused guards are the authoritative automated evidence for this phase and pass. The full-suite failures do not map to the Phase 02 source changes: bounded attribution found zero Phase 02-caused failures. The phase remains conditional until manual smoke checks are completed and the maintainer propagates source changes to generated harness outputs.
