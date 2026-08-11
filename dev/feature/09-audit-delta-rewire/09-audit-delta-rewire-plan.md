# Feature Plan: Audit Delta Rewire

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** `08-audit-comparison-contract`
- **Key files modified:** `source_of_truth/agents/delta-auditor.agent.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** `Audit - Delta` loads the finalized audit-comparison skill from `08-audit-comparison-contract` and delegates the mechanical work formerly defined in Phases 3 through 6b to it.
2. **AC2:** Phase 1 type selection and Phase 2 target/scope confirmation remain unchanged in responsibility, order, and user interaction.
3. **AC3:** The current output-root override/non-current-branch decision and the matrix announcement/confirmation that precede auditor spawning remain in `Audit - Delta`; no interactive confirmation moves into the shared skill.
4. **AC4:** The conditional delta offer remains in `Audit - Delta` when the user did not request a delta up front, while a requested delta still proceeds without a second offer; the caller also retains the current offer to rerun a failed or partial audit side.
5. **AC5:** Phases 7 and 8 retain their existing fix-research offer, scope explanation, comparative remediation research, and current-side-only remediation behavior.
6. **AC6:** Observable comparison behavior is unchanged: same selected-type × target matrix, same prompt contents, same artifact paths, same per-type deltas, same attribution discipline, and same reported conclusions. The sole lifecycle correction is Phase 03's explicit requirement to release a created worktree after attribution rather than after the delta.
7. **AC7:** The agent no longer restates the shared output-root, ref-materialization, delta-gate, attribution-batching, sum-check, or worktree-release procedure.
8. **AC8:** The existing `agents:` roster and tool authority remain sufficient and unchanged unless the finalized shared-skill call requires an already-declared leaf; no new agent or delegation depth is introduced.
9. **AC9:** The rewire preserves the rule that audits and delta documents are written to the newer working checkout and that remediation writes only to the current side.

### Non-Goals

- Do not redesign or shorten `Audit - Delta`'s user conversation.
- Do not change audit types, default audit names, target confirmation, artifact naming, remediation research, or remediation scope.
- Do not copy shared mechanics back into the agent for readability.
- Do not modify `Phase - Execute`, tests, generated ports, or `.github/`.
- Do not run propagation.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC7 | `source_of_truth/agents/delta-auditor.agent.md`, finalized skill from `08-audit-comparison-contract` | Must-have automated single-home and consumer-reference guards in `11-audit-bookend-guards` |
| AC2–AC6 | Existing Phase 1, 2, 5 confirmation, 6 offer, 7, and 8 sections in `source_of_truth/agents/delta-auditor.agent.md` | Must-have automated ordering/retention guards; manual QA check through one real `Audit - Delta` run |
| AC8–AC9 | Agent frontmatter, shared skill call, current-side remediation clause | Existing test to update: no update expected in `tests/test_agent_corpus_invariants.py`; must-have focused guard for retained behavior |

## B. Correctness & Edge Cases

- A user who supplied types, targets, labels, scope, and delta intent up front is not asked to repeat them.
- Inferred matrix details still require user confirmation before spawn; the shared skill does not erase that boundary.
- More than two targets and multiple comparison pairs remain supported by the existing caller state passed into the shared contract.
- Separate audit types never share a report or delta.
- A partial side still blocks its pair's delta through the shared gate, with the interactive agent retaining the ability to offer a rerun.
- No regression count is presented before attribution even though the detailed procedure now lives outside the agent body.
- Phases 7 and 8 still run only after the delta and attribution prerequisites they require.

## C. Consistency & Architecture Fit

- Treat this as an extraction rewire. Preserve existing text where it remains and replace only the moved mechanism with a concise skill invocation and required input handoff.
- Load the exact skill slug selected by `08-audit-comparison-contract`; do not guess or introduce an alias.
- Existing public contract consumed: the shared skill accepts the confirmed audit matrix, paths, labels, roots, prompt content, and delta intent produced by Phases 1–2 and the retained confirmations.
- Relationship: this feature depends on 08 because the new reference and handoff vocabulary must target a real finalized skill. It is file-disjoint from `10-phase-execute-audit-bookend`, so both may execute in Wave 2.
- The current frontmatter already declares every leaf required by the shared sequence. Any roster edit must be justified against the existing parsed agent list, not made speculatively.

### Unverified Assumptions

- The exact call-site wording and section numbering after extraction depend on the finalized skill's input/return contract. Preserve the visible phase order even if the mechanical subheadings become a single skill-driven phase.

## D. Clean Design & Maintainability

- Keep one compact handoff from retained interactive setup to shared mechanics.
- Do not summarize rules that the loaded skill already states.
- Preserve the user's existing decision points exactly where they are.
- Avoid edits outside Phases 3–6b except where a reference must connect retained content to the shared contract.

### Keep It Clean Checklist

- [ ] One skill reference, no copied procedure.
- [ ] All interactive confirmations remain in the agent.
- [ ] Phases 1, 2, 7, and 8 preserve behavior.
- [ ] Frontmatter remains valid and collision-safe.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no logs or new reports. Preserve the current matrix announcement, report verification, reconciliation statement, and attribution presentation as the human-visible execution evidence.
- **Security:** Maintain read-only target handling and current-side-only remediation. Never stash, switch, or write into baseline targets.
- **Runbook:** Run the focused Phase 03 guards and corpus invariants. Exercise one real `Audit - Delta` run for behavioral identity. Roll back by restoring the in-agent sequence and removing the skill reference as one atomic change. Propagation remains a maintainer step.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1, AC7 | Parse the agent and shared skill; assert one shared reference and one mechanical owner | Must-have automated test |
| AC2–AC5 | Section-scoped guards verify retained selection, confirmation, offer, research, and remediation clauses | Must-have automated test |
| AC6, AC9 | Run one baseline/current comparison and compare the observed matrix, paths, prompts, and results to the pre-extraction behavior | Manual QA check |
| AC8 | Parse frontmatter and run roster-resolution invariants | Existing test to update: no update expected; run as regression evidence |

### Top Five High-Value Checks

1. Given the rewired agent, when its skill references are parsed, then it loads exactly the finalized comparison skill.
2. Given the agent body, when moved mechanism phrases are searched in consumer scope, then they exist only in the shared skill.
3. Given an inferred audit matrix, when the workflow reaches auditor spawn, then the existing user confirmation still occurs first.
4. Given no up-front delta request, when audits complete, then the existing delta offer is still made; given an up-front request, no duplicate offer is introduced.
5. Given a representative two-snapshot run, when old and new behavior are compared, then prompts, artifacts, phase order, and user decisions are unchanged.

### Fixtures and Test Impact

- `11-audit-bookend-guards` owns the new structural and mutation-tested assertions over this rewire.
- `tests/test_agent_corpus_invariants.py` remains an unchanged regression input for parsed frontmatter, roster resolution, and duplicate blocks.
- No Stage 0 is required; the focused Phase 02 guard module demonstrates the local pattern for section-scoped prose-contract tests.

## Stage 1: Inventory Retained Interaction
**Goal**: Enumerate every confirmation, offer, and interactive branch that must stay in `Audit - Delta` before removing mechanical text.
**Success Criteria**: AC2–AC5 are mapped to retained sections before the extraction edit.
**Status**: Not Started

## Stage 2: Rewire to the Shared Skill
**Goal**: Replace only the shared mechanism with the finalized skill load and explicit input handoff.
**Success Criteria**: AC1 and AC6–AC9 hold with no duplicated mechanical contract.
**Status**: Not Started
