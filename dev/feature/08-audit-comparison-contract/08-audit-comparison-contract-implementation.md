# Implementation Record: Audit Comparison Contract

## Summary

Created the caller-neutral `audit-comparison` skill at
`source_of_truth/skills/audit-comparison/SKILL.md`. It owns the shared audit
sequence inputs, output-root resolution, ref materialization, matrix execution,
per-type full-report delta gate, attribution batching and arithmetic, and
post-attribution cleanup ordering. It cites `auditor-conventions`,
`audit-delta-report`, `Baseline Worktree`, and `worktree-baseline` rather than
duplicating their contracts. Updated all four verified skill-count surfaces to
45. Consumer rewiring remains with Features 09 and 10.

## Sibling Features

- Features 01–04 cover Unity test execution, asset import, consumer alignment,
  and reference assets; they do not share files with this feature.
- Features 05–07 cover phase final-check contracts and integration; they do not
  share files with this feature.
- Feature 09 (`audit-delta-rewire`) and Feature 10 (`phase-execute-audit-bookend`)
  consume the finalized `audit-comparison` slug and caller-neutral vocabulary.
- Feature 11 (`audit-bookend-guards`) owns the proposed focused guard module and
  validates the skill/consumer topology, prompt parameterization, gates,
  attribution arithmetic, and cleanup ordering.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | Feature 11 proposed focused guard (planned) | Parse skill frontmatter and required sequence headings | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md`, `results/corpus.xml` | PENDING | PENDING |
| AC2 | AC2 | Feature 11 proposed focused guard (planned) | Check output root, materialization, matrix, delta, attribution, reconciliation, cleanup order | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC3 | AC3 | Feature 11 proposed focused guard (planned) | Reject interactive confirmation/question/offer content | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC4 | AC4 | Feature 11 proposed focused guard (planned) | Verify canonical skill references without copied contracts | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC5 | AC5 | Feature 11 proposed focused guard (planned) | Verify one prompt template and exactly three varying slots | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC6 | AC6 | Feature 11 proposed focused guard (planned) | Mutate/remove full-report gate and per-type isolation; guard must fail | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC7 | AC7 | Feature 11 proposed focused guard (planned) | Mutate premature regression and attribution batch sum/disjointness rules | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC8 | AC8 | Feature 11 proposed focused guard (planned) | Mutate cleanup placement and verify attribution precedes cleanup | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC9 | AC9 | Feature 11 proposed focused guard (planned) | Verify explicit caller input boundary and caller-neutral return state | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC10 | AC10 | Feature 11 proposed focused guard (planned) | Verify moved mechanism has one shared home across consumers | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC11 | AC11 | Manual count recount | Recount source skills and inspect all four documentation surfaces | Done | `CONTRIBUTING.md`; `docs/ARCHITECTURE.md`; `docs/CODEBASE_CONTEXT.md` | `source_of_truth/skills` (45 `SKILL.md` files) | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | New terse skill with valid frontmatter owns the reusable sequence | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Frontmatter name matches the finalized directory slug. |
| AC2 | Preserve output root, ref materialization, matrix, delta gate, attribution, reconciliation, and cleanup ordering | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Cleanup is explicitly after the last attribution result. |
| AC3 | Mechanism-only skill without interactive conversation | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Caller-specific selection and continuation policy remain external. |
| AC4 | Cite canonical comparability and delta-report contracts | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | References `auditor-conventions` Multi-Target Audits and `audit-delta-report`. |
| AC5 | One reusable prompt template with only root, label, and output-directory variation | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Scope and intent are required to remain byte-identical. |
| AC6 | Full-report delta gate and per-type count domains | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Missing, partial, summary-only, and unusable reports fail closed. |
| AC7 | Attribution before regression and disjoint/summed batches | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Empty and unavailable-baseline branches are explicit. |
| AC8 | Worktree retained through attribution and cleaned only afterward | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Reused worktrees are never removed. |
| AC9 | Caller-neutral support for interactive and unattended callers | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Explicit input and returned-evidence boundaries support both consumers. |
| AC10 | Single shared home for moved mechanism | Done | `source_of_truth/skills/audit-comparison/SKILL.md` | Features 09 and 10 will remove the duplicate consumer prose. |
| AC11 | All four current skill-count surfaces state 45 | Done | `CONTRIBUTING.md`; `docs/ARCHITECTURE.md`; `docs/CODEBASE_CONTEXT.md` | Source recount is 45. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/audit-comparison/SKILL.md` | Created | Added the caller-neutral audit-comparison mechanism and returned evidence contract. | Provides one reusable home for Features 09 and 10. |
| `CONTRIBUTING.md` | Modified | Changed two current skill-count annotations from 44 to 45. | Keeps contributor-facing counts aligned. |
| `docs/ARCHITECTURE.md` | Modified | Changed the diagram and directory description from 44 to 45. | Keeps architecture count surfaces aligned. |
| `docs/CODEBASE_CONTEXT.md` | Modified | Changed both skill-count statements from 44 to 45. | Keeps bootstrap context aligned. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|-------|
| None | None | No test file was created or modified; Feature 11 owns the proposed focused guard module. | Downstream guard coverage is planned in Feature 11. |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/ --junitxml=dev/feature/08-audit-comparison-contract/results/final.xml`
- **Results artifact**: `dev/feature/08-audit-comparison-contract/results/final.xml`
- **Baseline**: 256 passed, 15 failed/subfailed (268 collected), `dev/feature/08-audit-comparison-contract/results/baseline.xml`
- **Final**: 255 passed, 16 failed/subfailed (268 collected), `dev/feature/08-audit-comparison-contract/results/final.xml`
- **New tests added**: 0
- **Affected suites run**: `tests/test_agent_corpus_invariants.py`, `tests/test_unity_consumer_contract.py`, `tests/test_propagate_master_assets.py`, `tests/test_pr_review_orchestrator.py`; full `tests/` suite
- **Regressions**: The additional final failure is the expected propagation fixed-point check because generated outputs were intentionally not regenerated; no Phase 03-owned failure was identified. Existing PR Review, generated-count/applyTo, and Unity reference failures remain.

### Wave-1 Gate Remediation Check

- **Execution**: not-executed (the integrated gate artifact was inspected; no test command was run in this pass)
- **Results artifact**: `dev/feature/08-audit-comparison-contract/results/wave-1.xml`
- **Gate summary**: 89 passed, 5 failures/subfailures (32 subtests; XML suite attributes: `tests=126`, `failures=5`, `skipped=0`)
- **Finding**: No Phase 03-owned defect. The five failures match the corresponding non-Unity failures in the feature baseline: three generated-agent count assertions (`42 != 41`, `55 != 54`, `55 != 54`), one unresolved `applyTo` enumeration, and the existing `05 PR - Review` prose collision in `source_of_truth/agents/delta-auditor.agent.md`.
- **Scope check**: The feature changed only `source_of_truth/skills/audit-comparison/SKILL.md` and the three documented skill-count surfaces; none can change generated agent counts, instruction targets, or PR-review prose. No source, test, generated-output, or `.github/` changes were made for this check.

## Deviations from Plan

None. The downstream focused guard module remains intentionally uncreated, as Feature 11 owns it. No phase-document content changed because the Phase 03 summary already describes this planned contract and the implementation aligns with it.

## Gaps

- Generated `ports/` and `.github/` outputs are stale until the maintainer runs propagation; propagation was intentionally not run.
- Features 09 and 10 still need to rewire their consumers to this finalized slug.
- Runtime prompt byte-identity, worktree lifetime, and post-extraction `Audit - Delta` behavior remain manual/downstream verification items described by the plan.

## Reviewer Focus Areas

- `source_of_truth/skills/audit-comparison/SKILL.md:24-26` — verify prompt-template variation is limited to target root, snapshot label, and output directory.
- `source_of_truth/skills/audit-comparison/SKILL.md:68-100` — verify per-type delta gating, attribution arithmetic, and cleanup ordering remain load-bearing and single-owned.
- `source_of_truth/skills/audit-comparison/SKILL.md:102-116` — verify returned evidence is sufficient for both interactive and unattended callers without importing caller policy.
