# Feature Context: Audit Delta Rewire

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/agents/delta-auditor.agent.md` | Live `Audit - Delta` orchestrator. Retain caller-specific selection, confirmation, offer, retry, research, and remediation behavior while replacing the Phase 3–6b mechanical procedure with the finalized shared-skill handoff. | Modify |

### Read-Only References and Upstream-Owned Files

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md` | Upstream caller-neutral comparison contract created by `08-audit-comparison-contract`. Its finalized path, slug, input vocabulary, return state, gates, and cleanup order must be read from disk before this rewire is authored. | Read-only reference |
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Existing authority for multi-target comparability, audit isolation, prompt identity, snapshot labels, and output layout; neither the consumer nor the new skill should restate it. | Read-only reference |
| `source_of_truth/skills/audit-delta-report/SKILL.md` | Existing delta, open-items queue, and attribution document contract used by the shared sequence. | Read-only reference |
| `source_of_truth/skills/audit-remediation-research/SKILL.md` | Existing Phase 7 comparative fix-research contract that must remain called by `Audit - Delta` after attribution and user confirmation. | Read-only reference |
| `source_of_truth/skills/audit-remediation-pipeline/SKILL.md` | Existing Phase 8 remediation contract; remediation must remain current-side only. | Read-only reference |
| `source_of_truth/agents/05a-baseline-worktree.agent.md` | Existing leaf contract for materializing and releasing ref targets. Its lifecycle is invoked through the new shared comparison contract. | Read-only reference |
| `source_of_truth/agents/auditor-delta.agent.md` | Existing leaf that writes each per-type delta and open-items queue. The `Audit - Delta` frontmatter already declares its exact display name. | Read-only reference |
| `source_of_truth/agents/auditor-attribution.agent.md` | Existing leaf that settles provisional findings. The `Audit - Delta` frontmatter already declares its exact display name. | Read-only reference |
| `dev/feature/08-audit-comparison-contract/08-audit-comparison-contract-plan.md` | Direct prerequisite defining the shared contract, caller inputs, return/failure boundary, single-home rule, and after-attribution cleanup requirement. | Read-only reference |
| `dev/feature/10-phase-execute-audit-bookend/10-phase-execute-audit-bookend-plan.md` | File-disjoint sibling consumer of the same finalized shared skill; both consumers must use one slug and compatible handoff vocabulary. | Read-only reference |
| `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-plan.md` | Downstream verification owner for the focused Phase 03 structural, interaction-retention, ownership, mutation, and regression guards. | Read-only reference |
| `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | Authoritative phase boundary: move mechanism, retain every `Audit - Delta` interaction, preserve artifacts and conclusions, and release temporary worktrees only after attribution. | Read-only reference |
| `docs/phases/DISCOVERY_CONTEXT.md` | Project-wide decision record for the shared-skill home, mechanism/conversation split, comparability ownership, and bookend timing. | Read-only reference |
| `tests/test_phase_refiner_final_check.py` | Existing focused phase-contract pattern: bounded section extraction, named obligation sets, non-vacuity checks, and deletion/semantic-negation mutations. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing unchanged regression input for parsed frontmatter, roster resolution, skill shape, instruction applicability, and duplicate blocks. | Read-only reference |
| `scripts/propagate_master_assets.py` | Canonical source-agent/frontmatter loader used by structural tests. It may be imported read-only but must never be executed for propagation by an agent. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `source_of_truth/agents/delta-auditor.agent.md` exists and has the expected Phase 1–8 workflow. Phases 3–6b currently contain the output-root, worktree, audit matrix, delta gate, attribution, count, and reporting mechanics named by the plan. | The feature is a real extraction rewire against verified source, not a speculative new flow. | Preserve existing text outside the extraction boundary and lift only mechanics owned by the finalized upstream skill. |
| The moved range is not a contiguous mechanism-only block. Current Phase 3 lines 56–57 can stop and ask the user how to handle a newer branch that is not checked out and honor an output-root override; Phase 5 line 74 announces the matrix and confirms inferred values; Phase 6 lines 98–102 make the conditional delta offer; Phase 6 line 104 offers to rerun a failed or partial side. | AC3–AC4 explicitly name only the matrix confirmation and conditional delta offer. A literal deletion of Phases 3–6b would silently remove two additional interactive branches and violate AC6's behavioral-identity requirement. | **Decomposer warning:** make the non-current-output-branch question/override and partial-report rerun offer explicit retained caller obligations, or state that AC6 covers them. Tasks below preserve all four interaction points and pass only confirmed caller state into the shared mechanism. |
| Current Phase 4 line 66 says temporary worktrees may be released once audits and delta are done, but Feature 08 AC8 and the Phase 03 success criteria require cleanup only after attribution returns. Attribution still needs the baseline tree. | The plan's broad “observable comparison behavior is unchanged” wording conflicts with the upstream lifecycle correction. Preserving the current sentence would break the finalized shared contract and can destroy evidence before attribution. | **Decomposer warning:** clarify that AC6 behavioral identity excludes this intentional cleanup-lifetime correction. Feature 09 must consume Feature 08's after-attribution cleanup order and must not preserve or restate the stale current line. |
| No audit-comparison skill exists under `source_of_truth/skills/` at expansion time, and Feature 08 intentionally marks its slug `[PROPOSED - name TBD: audit-comparison]`. | AC1 and AC7 cannot be implemented safely until the prerequisite selects a collision-safe final slug and concrete handoff vocabulary. | Enforce the Wave 1 dependency. Discover the finalized skill from Feature 08's implementation; never guess an alias or emit the placeholder as a real reference. |
| The current frontmatter already declares all verified leaves used by Phases 3–8, including `Auditor - Code`, `Auditor - Infra`, `Auditor - Refactor`, `Auditor - Security`, `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree`, plus the remediation leaves. There is no `skills:` frontmatter field; runtime skill loads are expressed in the body. | AC8 requires no speculative roster or tool edit. Loading the new skill follows the repository's existing body-reference pattern. | Keep `agents:` and tool authority byte-for-byte unchanged unless the finalized Feature 08 contract proves an already-existing declared leaf is missing; record any justified exception. |
| The current Phase 5 audit prompt and Phase 6 delta/attribution prompts provide the concrete prompt contents and artifact paths AC6 must preserve. The current Phase 1 and 2 headings and Phase 7 and 8 bodies also exist exactly as referenced. | The implementer has a verified pre-extraction behavioral baseline and can compare retained interaction and handoff data directly. | Inventory the exact caller state, prompt clauses, paths, and decision points before editing; use a move/reference strategy rather than a fresh paraphrase. |
| Test ownership is intentionally downstream. `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` does not exist and belongs to Feature 11; `tests/test_phase_refiner_final_check.py` is the verified focused-test pattern. No test class names are referenced or proposed for this feature. | This rewire needs explicit test-impact handling, but it must not create or edit tests. | Preserve scenario-level verification requirements for Feature 11, run existing regression tests unchanged, and do not invent test classes or exact methods. |
| No `Tests/Editor/Phase*/`, `tests/phase*/`, or equivalent phase-scoped directory exists. Tests are flat `tests/test_*.py` modules, and Feature 11 already plans one consolidated flat Phase 03 guard module. | The plan does not omit a current phase-scoped consolidated test file; its verification dependency is correctly assigned to Feature 11. | Do not introduce a test directory or test file in this feature. |
| `uv run pytest tests/` was rerun on 2026-08-11 with Python 3.12.6 and pytest 9.1.1: 268 collected, 256 passed, 15 failed. Failures are pre-existing and match the phase baseline, including the PR Review name collision, generated-count/applyTo drift, and missing Unity reference assets. | Full-suite green is not the current baseline. Feature success means no new failures attributable to the rewire; generated sync remains maintainer-owned. | Compare later regression runs with 256 passed / 15 failed and investigate only new failures. Do not repair unrelated failures or run propagation. |
| The repository policy makes `source_of_truth/` the only authoring surface and forbids agents from running propagation or hand-editing generated `ports/` and `.github/`. | A correct source edit may leave generated-sync checks red until the maintainer propagates. | Modify only the source agent, leave generated outputs untouched, and report propagation pending after implementation. |

## Architectural Decisions

- Treat the change as an extraction rewire. Preserve existing caller text where it remains and replace the shared mechanical rules with one concise reference to the finalized Feature 08 contract.
- Resolve the shared skill's final slug, caller-input fields, return state, failure state, and lifecycle vocabulary from the implemented prerequisite. The placeholder is not an API.
- Keep caller interaction in `Audit - Delta`: type selection, target/scope confirmation, output-root override/non-current-branch decision, matrix announcement and confirmation, conditional delta offer, partial-side rerun offer, fix-research offer and scope negotiation, and remediation offer/flow.
- Pass the confirmed audit matrix, paths, labels, roots, audit prompt content, output root, comparison pairs, and known delta intent into the shared contract. Handle caller-specific questions or retry choices in the orchestrator when the shared contract returns a pause/failure condition.
- Preserve one prompt template and the same artifact path shapes. Across snapshot renders, only target root, snapshot label, and output directory vary, as owned by the shared contract and `auditor-conventions`.
- Keep audit types and comparison pairs in separate count domains. Do not merge reports or deltas across types.
- Do not call provisional findings regressions before attribution and do not release a created baseline worktree until attribution completes. The finalized upstream lifecycle wins over the stale current cleanup sentence.
- Retain Phase 7 comparative fix research and Phase 8 current-side-only remediation outside the shared skill. The shared contract returns the delta/queue/attribution state they require.
- Keep the current frontmatter roster and tool authority unless implementation evidence from the finalized contract proves an existing leaf must be added; do not introduce an orchestrator, new leaf, or deeper delegation.
- Add no logs, telemetry, or reports. The matrix announcement, verified report/delta artifacts, reconciliation result, attribution presentation, research index, and remediation artifacts remain the execution evidence.

## Constraints

- `08-audit-comparison-contract` must be implemented first. Use its exact finalized skill slug and contract vocabulary.
- `source_of_truth/` is the only authoring surface. Never hand-edit `ports/` or `.github/`.
- Do not execute `scripts/propagate_master_assets.py`; propagation is a maintainer-only step.
- Preserve Phase 1, Phase 2, Phase 7, and Phase 8 responsibilities, order, and visible behavior.
- Preserve every caller interaction embedded in the current Phase 3–6b range, including the output-root decision and partial-report rerun offer discovered during expansion.
- Do not copy output-root, ref-materialization, prompt-comparability, delta-gate, attribution-batching, sum-check, or worktree-release procedures back into the agent.
- Preserve selected-type × target cardinality, existing prompt semantics, artifact paths, per-type deltas, reconciliation/attribution discipline, and reported conclusions.
- Treat target trees as read-only. Write audit and delta artifacts to the newer working checkout; write remediation only to the current side.
- Do not stash, switch, or mutate a baseline target. Leave pre-existing worktrees alone.
- Keep the existing `agents:` roster and tools unchanged unless the finalized prerequisite demonstrates a concrete missing existing leaf.
- Do not create or edit tests in this feature; Feature 11 owns consolidated guards.
- Do not redesign, shorten, or normalize the user's conversation as part of the extraction.
- Do not remediate the 15 known baseline failures.

## Scope Boundaries

- Modify only `source_of_truth/agents/delta-auditor.agent.md` during implementation; the companion documents in this bundle are planning artifacts, not source changes.
- Do not modify the Feature 08 shared skill; its owning feature must settle its slug and contract before this rewire starts.
- Do not modify `source_of_truth/agents/04-phase-execute.agent.md`; Feature 10 owns the other consumer.
- Do not create or edit the focused Phase 03 guard module or generic corpus tests; Feature 11 owns test implementation.
- Do not move Phase 7 research or Phase 8 remediation into the shared comparison skill.
- Do not change audit types, default audit names, scope confirmation, target labels, artifact naming, delta count domains, research scope, or remediation scope.
- Do not add an agent, delegation layer, tool, dependency, config key, schema, serializer, fixture, log, metric, or persistent state.
- Do not touch generated output or phase documentation as part of this feature implementation.

## Relationships to Sibling Plans

- `08-audit-comparison-contract` is the sole prerequisite and must land first. It creates the caller-neutral mechanical sequence, chooses the final skill slug, and defines the handoff/return vocabulary consumed here.
- `09-audit-delta-rewire` is one of two Wave 2 consumers. It keeps interactive conversation and retry policy around the shared mechanism.
- `10-phase-execute-audit-bookend` is file-disjoint and may execute in parallel after Feature 08. It consumes the same skill unattended, which is why no caller interaction may leak into the shared contract.
- `11-audit-bookend-guards` waits for Features 08–10 and owns the focused tests proving shared ownership, Delta interaction retention, Phase Execute topology/order, mutation integrity, and regression behavior.
- Both consumers must reference the same finalized slug. Any mismatch is an integration failure for Feature 11, not permission to create an alias or second skill.

## Suggested Implementation Order

1. Complete Feature 08 and inspect the implemented skill's final path, slug, caller inputs, returned state, failure boundary, and after-attribution cleanup handshake.
2. Snapshot the current `Audit - Delta` interaction inventory and prompt/artifact contracts, explicitly including the two interaction points omitted from the plan's named ACs.
3. Have Feature 11's downstream verification expectations available so section boundaries and retained interaction remain testable without duplicating mechanics.
4. Replace the Phase 3–6b mechanical prose with the concise shared-skill load/input handoff while retaining caller decisions at their existing workflow moments.
5. Verify Phase 1–2 and Phase 7–8 bodies, frontmatter, prompt contents, artifact paths, current-side write rules, and attribution-before-cleanup order.
6. Run existing corpus/full-suite regression evidence and one real `Audit - Delta` behavioral comparison after the focused guards land.
7. Stop with propagation pending for the maintainer; do not regenerate any port.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 maintenance/test tooling plus Markdown agent and skill source assets; stdlib-only runtime scripts; pytest 9.1.1 |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 268 collected, 256 passed, 15 failed — captured 2026-08-11. Failures are pre-existing: PR Review name collision, generated-count/applyTo drift, and missing Unity reference assets. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- From `docs/learnings/project-learnings.md`: check the participating agents' existing shared skills before authoring another contract. `auditor-conventions` already owns multi-target comparability, so this rewire must cite rather than restate it.
- From `docs/learnings/project-learnings.md`: when a second orchestrator needs an existing sequence, extract the working prose instead of composing a fresh version. Release ordering, “do not report this count yet,” disjoint batching, and sum checks are load-bearing even when they look like boilerplate.
- From `docs/learnings/project-learnings.md`: separate mechanism from conversation before extraction. Interactive confirmations, offers, questions, and retry policy stay in `Audit - Delta`; only the mechanical contract is shared with unattended `Phase - Execute`.
- From `docs/learnings/project-learnings.md`: corpus tests are structural by policy and must not pin one exact prose rendering. Feature 11 should use bounded sections, named obligations, non-vacuity, and mutation evidence.
- From `docs/learnings/project-learnings.md`: ten or more contiguous lines repeated across three or more agent files fail the duplicate-block invariant. The consumer must reference the finalized skill rather than paraphrase or copy its sequence.
- From `docs/learnings/cross-phase-decisions.md`: a structural guard can prove a rule is present but cannot prove runtime behavior. One real post-rewire `Audit - Delta` run remains required before Phase 03 can claim behavioral identity.
