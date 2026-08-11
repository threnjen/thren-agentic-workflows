# Feature Plan: Unity Consumer Alignment

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** yes
- **Depends on:** `01-unity-test-execution-contract`, `02-headless-asset-import`
- **Key files modified:** `source_of_truth/agents/04-phase-execute.agent.md`, `source_of_truth/agents/04g-unity-visual-verification.agent.md`, `source_of_truth/agents/04h-unity-reviewer.agent.md`, `tests/[PROPOSED - name TBD: Unity consumer contract guards]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** `source_of_truth/agents/04-phase-execute.agent.md` Step 2.5 consumes the finalized headless Test Execution ladder, writes results to the absolute main-checkout path, and no longer asks the user to run the Unity suite; the direct-supervisor-attestation escape hatch remains intact.
2. **AC2:** Phase Execute preserves `not-executed` as non-green and reaches it only through the finalized decline/unattended fallback or other genuine absence of evidence; it does not silently proceed as green.
3. **AC3:** `source_of_truth/agents/04g-unity-visual-verification.agent.md` continues using its verified editor-discovery order and saved local editor path, changes only the project execution target as required by the shared ladder, always uses `-batchmode` with graphics enabled for PlayMode capture, and never combines `-quit` with `-runTests`.
4. **AC4:** `source_of_truth/agents/04h-unity-reviewer.agent.md` aligns test execution and serialized-asset batch import with the finalized skill guidance, including the headless import path, without broadening batchmode beyond permitted test and import operations.
5. **AC5:** No consumer duplicates the full worktree or editor-discovery algorithm. Each points to the canonical skill or verified `04g` procedure so later rule changes have one source.
6. **AC6:** Structural guards derive the three required consumer paths, verify their distinct platform obligations and preserved escape hatch, and are proven red by removing or negating each consumer-specific mechanism.

### Non-Goals

- Do not rewrite the canonical skill contract owned by Features 01 and 02.
- Do not remove supervisor attestation or change the wave retry budget.
- Do not redesign visual verification, capture configuration, or editor-path persistence.
- Do not restructure, rename, or renumber agents.
- Do not run propagation or edit generated agent ports.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC2 | `source_of_truth/agents/04-phase-execute.agent.md` Step 2.5 | Must-have automated test |
| AC3 | `source_of_truth/agents/04g-unity-visual-verification.agent.md` Steps 1–2 | Must-have automated test |
| AC4 | `source_of_truth/agents/04h-unity-reviewer.agent.md` Phase 2 | Must-have automated test |
| AC5–AC6 | All three consumer definitions and `tests/[PROPOSED - name TBD: Unity consumer contract guards]` | Must-have automated test |

## B. Correctness & Edge Cases

- Phase Execute's generic `not-executed` behavior also serves non-Unity suites. Change the Unity branch without weakening the general evidence gate.
- Visual verification must not inherit EditMode's `-nographics`; its rendered frames require graphics.
- The visual verifier's editor path and project path are separate. The discovered executable remains stable while `-projectPath` points to the shadow worktree or fallback checkout.
- The reviewer may use `-quit` for serialized-asset import but not for `-runTests`; guards must distinguish these command purposes.
- Avoid copying the entire ladder into all three consumers. A concise canonical reference plus consumer-specific constraints is safer.

## C. Consistency & Architecture Fit

- Follow existing agent-authoring brevity and preserve all frontmatter, tools, rosters, and personality canaries.
- Use display names when referring to sibling agents; do not introduce unrewritten slugs.
- Reuse the public contract produced by `01-unity-test-execution-contract`: the `unity-development` skill's `## Test Execution` section. Reuse the import contract produced by `02-headless-asset-import`: the skill's Serialized Assets section.
- No new public API or helper is required. Consumers call the existing documented skill contract.
- Relationship: depends on Features 01 and 02 because it must align to their final wording and behavior. It is parallel-safe with `04-unity-test-reference-assets` because their file scopes are disjoint.

## D. Clean Design & Maintainability

- Keep shared mechanics canonical in the skill; retain only role-specific decisions in each agent.
- Preserve Phase Execute's existing evidence status vocabulary and attestation branch.
- Preserve Visual Verifier's editor discovery and graphics-on requirements.
- Preserve Unity Reviewer's distinction between test execution and serialized-asset import.
- Add a dedicated consumer guard module rather than prose assertions to the generic corpus-invariant suite.

### Keep It Clean Checklist

- [ ] No copied worktree procedure across agents.
- [ ] No second editor-discovery algorithm.
- [ ] No blanket `-nographics` rule.
- [ ] No `-quit` with `-runTests`.
- [ ] No frontmatter or roster changes.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no new normal-path logs. Preserve results artifacts, Unity logs, and explicit `executed-*`/`not-executed` status reporting.
- **Security:** Preserve machine-local editor-path handling and `.gitignore` requirement. Do not place editor paths or license data in agent definitions.
- **Runbook:** Run focused consumer guards, agent corpus invariants, and propagation tests. Roll back by reverting only the three source agent files and their focused guard module. Generated-port mismatches remain propagation pending.
- **Baseline:** The full discovery baseline is 141 passes and two unrelated failures: the PR-review agent-name collision guard and the wildcard `applyTo` target guard. Identify both separately if they remain.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC2 | Scoped Phase Execute Step 2.5 contract checks | Must-have automated test |
| AC3 | Scoped Visual Verifier invocation/discovery relationship checks | Must-have automated test |
| AC4 | Scoped Unity Reviewer test/import command distinction | Must-have automated test |
| AC5–AC6 | Derived consumer enumeration plus mutation proof | Must-have automated test |

### Top Five High-Value Checks

1. Given Phase Execute Step 2.5, when Unity is selected, then it delegates invocation mechanics to the canonical skill, never asks the user to run the suite, and preserves supervisor attestation.
2. Given the Visual Verifier command, when tokens are inspected, then `-batchmode` and PlayMode are present, `-nographics` and `-quit` are absent, and the resolved editor procedure remains intact.
3. Given Unity Reviewer commands, when purpose is distinguished, then test execution excludes `-quit` and asset import permits `-quit` under the canonical Serialized Assets rule.
4. Given the three derived consumer paths, when one alignment reference is removed, then the focused guard fails and names that consumer.
5. Given a mutation that restores user-run handoff in Phase Execute, when the guard runs, then it fails even if other `not-executed` wording remains elsewhere.

### Fixtures and Test Impact

- Create `tests/[PROPOSED - name TBD: Unity consumer contract guards]` with scoped section parsing, derived path enumeration, non-vacuity assertions, and mutation proof.
- Existing agent corpus tests remain unchanged unless a structural parser helper can be reused without adding prose coupling.
- Run the focused module, `tests/test_agent_corpus_invariants.py`, and `tests/test_propagate_master_assets.py`; distinguish the known baseline failure and expected pre-propagation sync mismatch.
- No Unity runtime test is required for this feature; Features 01 and 02 own empirical command verification.

## Stage 1: Consumer Contract Guards
**Goal**: Add failing guards for each consumer's role-specific obligations and preserved behavior.
**Success Criteria**: AC1–AC6 have scoped, non-vacuous guards that fail under targeted mutations.
**Status**: Not Started

## Stage 2: Phase Execute Alignment
**Goal**: Update Step 2.5 to consume the canonical ladder while preserving evidence and attestation semantics.
**Success Criteria**: AC1–AC2 pass and the user is never asked to execute the Unity suite.
**Status**: Not Started

## Stage 3: Visual Verifier and Unity Reviewer Alignment
**Goal**: Align the two Unity specialists without duplicating shared mechanics.
**Success Criteria**: AC3–AC5 pass; graphics, editor discovery, and import/test command distinctions remain correct.
**Status**: Not Started

## Stage 4: Regression Verification
**Goal**: Run focused and corpus regression checks with source-only edits.
**Success Criteria**: New guards and structural corpus invariants pass; unrelated and propagation-pending failures are reported separately.
**Status**: Not Started
