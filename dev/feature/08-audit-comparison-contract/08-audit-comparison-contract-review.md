# Review Record: Audit Comparison Contract

## Verdict

**Approved with Reservations**

## Scope Reviewed

- `source_of_truth/skills/audit-comparison/SKILL.md`
- `CONTRIBUTING.md`
- `docs/ARCHITECTURE.md`
- `docs/CODEBASE_CONTEXT.md`
- `08-audit-comparison-contract-implementation.md`

## Findings

- The shared skill has valid frontmatter and keeps caller-specific selection,
  retry, continuation, remediation, and presentation outside the contract.
- It cites `auditor-conventions`, `audit-delta-report`, `Baseline Worktree`, and
  `worktree-baseline` rather than duplicating their detailed contracts.
- It states the three permitted prompt substitutions, full-report delta gate,
  per-type isolation, attribution arithmetic, and post-attribution cleanup.
- All four documented skill-count surfaces state 45.

## Reservation

Both spawned review attempts stalled without producing a child review record;
the root performed this bounded fallback review after the retry budget was
exhausted. The implementation record reports one additional full-suite failure
from stale generated-output synchronization. The new focused corpus checks pass.

Generated `ports/*/skills/audit-comparison/SKILL.md` files appeared during the
implementation despite the implementation record stating propagation was not
run. They are outside this feature's authored scope and are not staged here;
the maintainer must reconcile generated output through the normal propagation
step.

## Test Evidence

- Focused: `uv run pytest tests/test_agent_corpus_invariants.py` — passed.
- Full suite: `executed-failing`; results at
  `dev/feature/08-audit-comparison-contract/results/final.xml`.
- Known baseline failures remain; the additional failure is the expected
  generated-output fixed-point mismatch while propagation is pending.

## Required Follow-Up

- Feature 09 and Feature 10 must load the finalized `audit-comparison` slug.
- Feature 11 must add the focused structural and mutation guards.
- The maintainer must review the generated-output discrepancy before deployment.

