# Feature Context: Audit Comparison Contract

## Key Files

### Files Created or Modified by This Feature

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md` | New caller-neutral home for output-root resolution, ref materialization, audit-matrix execution, delta gating, attribution batching/reconciliation, and worktree release ordering. The implementer must select a collision-safe final directory/frontmatter name and record it for sibling consumers. | Create |
| `CONTRIBUTING.md` | Current-count surface whose skill total must move from 44 to 45. | Modify |
| `docs/ARCHITECTURE.md` | Architecture diagram count surface whose skill-directory total must move from 44 to 45. | Modify |
| `docs/CODEBASE_CONTEXT.md` | Bootstrap documentation with two current skill-count statements that must both move from 44 to 45. | Modify |

### Read-Only References and Downstream Verification Files

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/agents/delta-auditor.agent.md` | Source sequence for the extraction. Phases 3 through 6b contain the output-root, worktree, audit, delta, and attribution orchestration; Phases 1, 2, 7, and 8 remain caller-owned. | Read-only reference |
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Authoritative `Multi-Target Audits` contract for independent runs, identical prompts, snapshot labels, artifact layout, and one newer-side output root. Cite it; do not copy it. | Read-only reference |
| `source_of_truth/skills/audit-delta-report/SKILL.md` | Authoritative delta, queue, provisional-attribution, probe, and reconciliation document contract. Cite it; do not copy it. | Read-only reference |
| `source_of_truth/agents/05a-baseline-worktree.agent.md` | Verifies the exact existing display name `Baseline Worktree` and its caller cleanup handshake. | Read-only reference |
| `source_of_truth/skills/worktree-baseline/SKILL.md` | Authoritative worktree ownership, reuse, failure, read-only, and cleanup mechanics behind `Baseline Worktree`. | Read-only reference |
| `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | Upstream requirement source, including the required post-attribution cleanup order and the boundary between shared mechanism and caller interaction. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing structural regression input. It requires closed skill frontmatter with non-empty `name` and `description` and rejects blank frontmatter lines. | Read-only reference; existing test |
| `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` | Consolidated Phase 03 guard module planned by `11-audit-bookend-guards`; absent at expansion time and not created by this feature. | Create in Feature 11; no change here |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `source_of_truth/agents/delta-auditor.agent.md` Phase 4 currently says to release a created worktree once audits and delta are done, but Phase 6b then requires `Auditor - Attribution` to probe the baseline and current trees. The Phase 03 summary and AC8 require release only after attribution returns. | A literal move of the existing text would preserve a stale order and remove the baseline before its final consumer. This contradicts the plan's “lift” wording while validating its explicit AC8 ordering requirement. | Treat AC8 and the phase summary as authoritative. Move the cleanup handshake into the shared sequence after attribution completes; preserve the remaining behavior. Feature 11 must guard this order. |
| The plan's traceability table omits `source_of_truth/agents/05a-baseline-worktree.agent.md` and `source_of_truth/skills/worktree-baseline/SKILL.md`, although AC2 and AC8 depend on their ownership and cleanup contracts. | Implementing lifecycle prose from memory could duplicate or contradict the existing worktree contract. | Add both as read-only implementation references; do not restate their create/reuse/remove procedure in the new skill. |
| `auditor-conventions` already owns prompt comparability, per-run independence, snapshot labels, artifact layout, and the one-output-root rule. | AC5's one-template contract must coordinate with the canonical comparability contract without becoming a second specification of it. | The new skill should require one caller-provided template and cite `auditor-conventions` `Multi-Target Audits`; only the root, label, and output-directory slots may vary between renders. |
| `audit-delta-report` sections 2A and 2D already own the attribution probe and field-update contract, including the invariant provisional-bucket total. | Re-explaining item classification or document fields in the new skill would create drift and violate AC4/AC10. | Keep only sequencing, gates, disjoint batching, arithmetic verification, and return-state mechanics in the new skill; cite the existing skill for document semantics. |
| The proposed focused Phase 03 module does not exist. Existing phase-scoped coverage uses top-level modules such as `tests/test_phase_refiner_final_check.py`; `11-audit-bookend-guards` explicitly owns the new consolidated module. | Feature 08 has no current focused guard to update, but this is an intentional wave dependency rather than a missing Stage 0 prerequisite. | Do not create or edit tests in this feature. Record the final slug and contract vocabulary for Feature 11; run existing regressions against the recorded baseline. |
| No test class name is referenced in this plan. The only new test filename is already labeled `[PROPOSED - name TBD]`, and no exact proposed test method names are asserted as existing facts. | The plan complies with concrete-name verification rules. | Use scenario descriptions in tasks and preserve the proposal marker until Feature 11 selects the filename. |
| All four stated count locations are present: one in `CONTRIBUTING.md`, one in `docs/ARCHITECTURE.md`, and two in `docs/CODEBASE_CONTEXT.md`. Disk currently contains 44 source `SKILL.md` files. | AC11 has a verified starting count and complete edit surface. | After creating the skill, recount from disk and update all four statements to 45. |

## Architectural Decisions

- Create one directory-based skill under `source_of_truth/skills/` and make its frontmatter `name` match the final collision-safe directory slug.
- Extract the existing working sequence instead of designing a second audit orchestration. The deliberate exception is the cleanup-order correction required by AC8 and the Phase 03 source of truth.
- Organize the skill around caller inputs, common sequencing, transition gates, and returned evidence state. Keep caller conversation and caller-specific failure policy outside it.
- Accept explicit caller-provided inputs for the output root, audit matrix, target roots, snapshot labels, report paths, and identical prompt content. Do not invent caller-specific defaults in the shared contract.
- Render both snapshot audit prompts from one template. The only per-snapshot substitutions are target root, snapshot label, and output directory; scope and intent clauses remain byte-identical.
- Keep each audit type in a separate matrix, report pair, delta, queue, reconciliation domain, and attribution count domain. Never produce cross-type arithmetic.
- Gate delta creation on two full findings reports that each state their own totals. A summary, partial return, or severity count elsewhere cannot satisfy the gate.
- Keep provisional findings unattributed until the separate attribution probe completes. Attribution batches must be disjoint, and assigned-item counts must sum exactly to the delta's unattributed total before results are presented.
- Retain a worktree created for a ref target through audits, delta, and attribution. Invoke cleanup only after attribution returns, and never remove a reused pre-existing worktree.
- Cite `auditor-conventions`, `audit-delta-report`, and the `Baseline Worktree` lifecycle contracts rather than duplicating their detailed rules.
- Add no normal-path logging or persistent orchestration state. Report paths, stated totals, gate outcomes, reconciliation status, attribution outcome, and cleanup status are the evidence surfaces.

## Constraints

- `source_of_truth/` is the only authoring surface. Do not edit `ports/` or `.github/` generated output.
- Do not run `scripts/propagate_master_assets.py`; propagation is a maintainer-only step and remains pending after source changes.
- Keep the new runtime-loaded skill terse. State each behavior, constraint, and output contract once.
- Do not modify `source_of_truth/agents/delta-auditor.agent.md`; Feature 09 owns that consumer rewire.
- Do not modify `source_of_truth/agents/04-phase-execute.agent.md`; Feature 10 owns that consumer wiring.
- Do not create or edit the proposed Phase 03 guard module; Feature 11 owns consolidated automated verification.
- Do not duplicate the `Multi-Target Audits`, delta/queue schema, attribution probe, attribution field ownership, or detailed worktree lifecycle contracts.
- Treat target trees as read-only. All reports belong under the newer working checkout unless the caller explicitly supplies another valid output root.
- A dirty current working checkout may be audited in place only with an explicit non-reproducibility limitation. The shared sequence must not stash, switch, reset, or otherwise mutate it.
- Return ref-materialization failures and unusable audit/delta/attribution states to the caller. The shared skill does not decide whether an interactive caller retries or an unattended caller records missing evidence and continues.
- The skill slug is not fixed upstream. Keep `[PROPOSED - name TBD: audit-comparison]` until implementation selects the final name, then use that exact slug consistently in the skill and sibling handoff notes.

## Scope Boundaries

- Only create the new shared skill and update the four verified count statements across three documentation files.
- Preserve `Audit - Delta` Phases 1, 2, 7, and 8 and all interactive confirmations, questions, and offers for Feature 09.
- Preserve Phase Execute's caller-specific scope derivation, Step 1 decision, failure continuation, remediation policy, and final-review evidence wiring for Feature 10.
- Do not add a new agent, second comparison skill, schema, config key, serializer, fixture, or test helper.
- Do not fold code, infra, refactor, or security findings into one cross-type comparison.
- Do not call a provisional item a regression before attribution or present an unreconciled count as evidence.
- Do not add normal-path logs, metrics, tracing, or persisted orchestration state.
- Do not change unrelated repository count surfaces. The verified skill-count edits are `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, and the two statements in `docs/CODEBASE_CONTEXT.md`.

## Relationships to Sibling Plans

- `09-audit-delta-rewire` depends on this feature's finalized skill slug and caller-neutral input/return vocabulary. It replaces the in-agent Phases 3–6b mechanism while retaining Audit - Delta's interactive conversation and later remediation flow.
- `10-phase-execute-audit-bookend` depends on the same finalized slug and contract. It supplies phase-derived scope, audit types, the recorded Step 1 decision, prompt content, roots, labels, paths, and its own continuation/remediation policy.
- Features 09 and 10 may run in parallel after this feature because they modify different agent files.
- `11-audit-bookend-guards` waits for this skill and both consumers. It creates `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` and validates single ownership, prompt parameterization, gates, attribution arithmetic, cleanup order, and consumer topology.
- This feature must record the chosen skill slug and any finalized contract vocabulary in its implementation record so all three downstream features target one real contract rather than guessing aliases.

## Suggested Implementation Order

1. Implement this Wave 1 feature first: choose the skill slug, extract and correct the shared mechanism, and synchronize count surfaces.
2. Run `09-audit-delta-rewire` and `10-phase-execute-audit-bookend` in parallel in Wave 2 after the skill contract exists.
3. Run `11-audit-bookend-guards` in Wave 3 after both consumers are complete, then execute the consolidated static and mutation-tested verification.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-authored multi-harness agent/skill corpus with Python 3.12.6 stdlib tooling; pytest 9.1.1 |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 268 collected; 256 passed, 15 failed/subfailed — captured 2026-08-11. Existing failures are the PR Review name collision, generated-count/applyTo drift, and missing Unity reference workflow assets; none is owned by Phase 03. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `docs/learnings/project-learnings.md`:

- **Check the shared skill before authoring a new one to hold a contract.** `auditor-conventions` already owns multi-target audit comparability, so this feature must cite it instead of copying its rules.
- **Prefer extracting an existing sequence over composing a fresh one.** Load-bearing ordering and reporting discipline are easy to lose when rewriting orchestration prose.
- **When extracting, separate mechanism from conversation first.** Interactive confirmations and questions remain in the caller; the unattended caller needs only the shared mechanical contract.
- **Corpus tests are structural by policy.** Do not add brittle assertions against one exact prose rendering; Feature 11 should enforce section-scoped obligations and prove its guards can fail.
- **A repeated block of 10 or more lines across three agent files fails corpus invariants.** Keeping the moved mechanism in one skill avoids both drift and duplicate-block failures when the two consumers are wired.
