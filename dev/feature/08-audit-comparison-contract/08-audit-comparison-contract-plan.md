# Feature Plan: Audit Comparison Contract

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** A new terse skill with valid frontmatter owns the reusable audit-comparison sequence currently implemented by `source_of_truth/agents/delta-auditor.agent.md` Phases 3 through 6b.
2. **AC2:** The extracted sequence preserves output-root resolution, ref-target materialization through `Baseline Worktree`, audit-matrix execution, the full-report delta gate, attribution batching, reconciliation checks, and worktree release ordering.
3. **AC3:** The skill contains mechanism only. It contains no user-facing confirmation, question, offer, or assumption that the caller is interactive.
4. **AC4:** The skill cites `auditor-conventions` Multi-Target Audits for comparability and `audit-delta-report` for delta and attribution document contracts without restating either contract.
5. **AC5:** The skill defines one reusable audit-prompt template contract. Across snapshots, only target root, snapshot label, and output directory may vary; caller-supplied scope and intent clauses must remain byte-identical between the two renders.
6. **AC6:** The sequence refuses to spawn `Auditor - Delta` unless both full findings reports exist and state their own totals, and it keeps each audit type in its own delta and count domain.
7. **AC7:** The sequence does not call a provisional finding a regression before `Auditor - Attribution` probes both trees; attribution batches are disjoint and their item counts must sum to the delta's unattributed total.
8. **AC8:** A worktree created for a ref target remains available through audits, delta, and attribution, and its cleanup handshake occurs only after attribution has returned.
9. **AC9:** The shared contract supports both callers: interactive `Audit - Delta` supplies its confirmed matrix and paths, while unattended `Phase - Execute` supplies its phase-derived scope, audit types, and recorded Step 1 decision.
10. **AC10:** The skill is the single home for the moved mechanical rules; neither consumer needs to copy the output-root, materialization, delta-gate, attribution-batching, sum-check, or cleanup procedure.
11. **AC11:** Repository skill-count summaries move from 44 to 45 in every current count surface: `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, and both count statements in `docs/CODEBASE_CONTEXT.md`.

### Non-Goals

- Do not change `Audit - Delta`; `09-audit-delta-rewire` owns that consumer.
- Do not change `Phase - Execute`; `10-phase-execute-audit-bookend` owns that consumer.
- Do not duplicate Multi-Target Audits or `audit-delta-report` document rules.
- Do not create an agent, a second audit-comparison skill, or any generated port output.
- Do not run propagation.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC4 | `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md`, existing `source_of_truth/agents/delta-auditor.agent.md` | Must-have automated test in downstream `11-audit-bookend-guards` |
| AC5–AC9 | New skill plus `source_of_truth/skills/auditor-conventions/SKILL.md`, `source_of_truth/skills/audit-delta-report/SKILL.md`, `source_of_truth/agents/05a-baseline-worktree.agent.md`, and `source_of_truth/skills/worktree-baseline/SKILL.md` as read-only references | Must-have automated test in downstream `11-audit-bookend-guards`; manual QA check for runtime prompt identity and cleanup lifetime |
| AC10 | New skill and both downstream consumers | Must-have automated single-home guard in downstream `11-audit-bookend-guards` |
| AC11 | `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Code-review evidence only; existing corpus tests do not validate prose counts |

## B. Correctness & Edge Cases

- A ref that cannot be materialized returns a concrete failure to the caller; the shared skill does not invent the caller's continuation policy.
- A current working checkout may contain uncommitted state. The sequence records that limitation and never tries to make it reproducible by mutating or stashing the checkout.
- A missing repository root is passed explicitly as unavailable where the delta contract permits it; fields are not silently omitted.
- A partial or summary-only auditor return cannot satisfy the delta gate even when a severity count is present elsewhere.
- An empty provisional set skips attribution cleanly. A non-empty set cannot proceed until batch cardinality is reconciled.
- Multiple audit types remain independent matrices, deltas, queues, and arithmetic domains.
- Cleanup never removes a pre-existing worktree and never runs before the last baseline-tree probe.
- Error handling is returned to the caller because `Audit - Delta` may ask or retry while `Phase - Execute` records missing evidence and continues.

## C. Consistency & Architecture Fit

- Follow the directory-based skill pattern under `source_of_truth/skills/`, with a single marked `SKILL.md` and concise `name`/`description` frontmatter.
- Use `[PROPOSED - name TBD: audit-comparison]` until implementation chooses the final collision-safe skill slug. Both consumers must load that exact finalized slug.
- Lift the existing Phase 3–6b sequence rather than rewriting it from the phase summary. Preserve load-bearing ordering and reporting discipline.
- Discovery found one stale ordering clause: the current Phase 4 cleanup text can release a created worktree after the delta even though Phase 6b still needs the baseline tree. AC8 and the Phase 03 document are authoritative; move cleanup after attribution and preserve all other behavior.
- Existing public contracts remain authoritative: `auditor-conventions` owns comparable runs, `audit-delta-report` owns delta/queue/attribution documents, and `Baseline Worktree` owns worktree lifecycle mechanics.
- Cross-feature API contract: this feature must expose a caller-neutral sequence with explicit input slots for output root, audit matrix, roots/labels/paths, and caller-provided identical prompt content. Features 09 and 10 consume that contract by skill reference.
- Relationship: `09-audit-delta-rewire` and `10-phase-execute-audit-bookend` both depend on the finalized skill path and contract vocabulary. `11-audit-bookend-guards` validates single ownership across all three.

### Unverified Assumptions

- The phase fixes the skill's responsibility but not its directory/frontmatter name. The implementer must select the final slug, record it, and update both consumers consistently.

## D. Clean Design & Maintainability

- Move the existing mechanism once; do not paraphrase it into a parallel specification.
- Separate caller inputs, shared sequencing, gates, and return state.
- Keep interactive decisions and caller-specific failure policy outside the skill.
- Prefer references to canonical contracts over embedded summaries.

### Keep It Clean Checklist

- [ ] No confirmation or question in the skill.
- [ ] No copied comparability or delta-report contract.
- [ ] No second prompt template per snapshot.
- [ ] No generated-output edits.
- [ ] Count surfaces agree on 45 skills.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no normal-path logs or persistent state. The caller's report paths, stated totals, reconciliation result, attribution result, and cleanup status are the evidence surfaces.
- **Security:** Treat every target tree as read-only. Write all reports under the newer working checkout and never expose secrets or copy repository content into orchestration state beyond the paths and finding identifiers required by the existing contracts.
- **Runbook:** Run the focused Phase 03 guard module, corpus invariants, and full suite. Roll back the skill and both consumer references together. After source changes, report propagation pending for the maintainer.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC4 | Parse the new skill; verify frontmatter, consumer-neutral scope, canonical references, and absence of interactive clauses | Must-have automated test |
| AC5–AC8 | Delete or negate prompt invariants, delta gate, attribution sum, and cleanup ordering and confirm named guards fail | Must-have automated test |
| AC9–AC10 | Verify both consumers load one finalized skill and do not retain moved mechanism | Must-have automated test |
| AC11 | Review all current count surfaces and recount `source_of_truth/skills/*/SKILL.md` from disk | Code-review evidence only |

### Top Five High-Value Checks

1. Given the new skill, when its frontmatter and headings are parsed, then the complete Phase 3–6b mechanism is present without interactive conversation.
2. Given the prompt-template contract, when any field other than root, label, or output directory is made snapshot-specific, then the focused guard fails for prompt comparability.
3. Given a missing or partial snapshot report, when the delta stage is reached, then the sequence refuses to spawn a delta.
4. Given overlapping or incomplete attribution batches, when cardinality is checked, then the sequence stops before presenting a regression count.
5. Given an active attribution probe, when cleanup is moved earlier, then a mutation guard fails for worktree lifetime.

### Fixtures and Test Impact

- `11-audit-bookend-guards` creates `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` and owns all content-guard mutation evidence.
- `tests/test_agent_corpus_invariants.py` remains an unchanged regression input for frontmatter, roster, skill shape, and duplicate blocks.
- The repository has broad test coverage over its Python tooling and corpus contracts. No Stage 0 is required despite the red baseline: `uv run pytest tests/` collected 268 tests on 2026-08-11 and reported 256 passed with 15 existing failures/subfailures unrelated to Phase 03.

## Stage 1: Extract the Shared Contract
**Goal**: Move the caller-neutral mechanics from `Audit - Delta` Phases 3–6b into one terse reusable skill.
**Success Criteria**: AC1–AC10 are represented once, with canonical contracts cited and interactive behavior excluded.
**Status**: Not Started

## Stage 2: Synchronize Skill Counts
**Goal**: Keep every repository skill-count summary aligned with the new source skill.
**Success Criteria**: AC11 is satisfied and all current count surfaces state 45 skills.
**Status**: Not Started
