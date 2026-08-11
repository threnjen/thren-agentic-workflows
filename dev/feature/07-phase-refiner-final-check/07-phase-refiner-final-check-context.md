# Feature Context: Phase Refiner Final-Check Integration

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/agents/02-phase-refiner.agent.md` | Live Phase - Refiner definition. Its frontmatter roster and post-refinement workflow must integrate the upstream final-check reviewer without changing the two entry paths or branch/commit contract. | Modify |
| `tests/[PROPOSED - name TBD: phase final-check contract guards]` | Focused Phase 02 pytest module for topology, shared-skill, workflow-ordering, continuation, blindness, non-vacuity, and mutation evidence. The implementer must choose and record the final repository-consistent filename. | Create |

### Read-Only References and Upstream-Owned Files

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/agents/02a-phase-final-check.agent.md` | Upstream reviewer produced by `06-phase-final-check-reviewer`; supplies the exact display name, hidden/leaf metadata, tool boundary, and shared-skill reference that this feature must parse and verify. | Read-only reference |
| `source_of_truth/instructions/read-only-agent.instructions.md` | Upstream companion edit from Feature 06. Its enumerated `applyTo` must resolve to the new reviewer through the propagator. | Read-only reference |
| `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` | Upstream reusable offer, blindness, finding, and response contract produced by `05-phase-final-check-contract`; the finalized slug must be discovered from disk before integration. | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Authoritative phase requirements, including the fixed reviewer path, blindness boundary, shared offer flow, five-finding behavior, verification strategy, and non-goals. | Read-only reference |
| `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-plan.md` | Defines the upstream shared contract and its downstream public obligations. | Read-only reference |
| `dev/feature/06-phase-final-check-reviewer/06-phase-final-check-reviewer-plan.md` | Defines the upstream hidden leaf and delegates its automated topology evidence to this integration feature. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing propagator-backed structural checks for roster resolution, spawn capability, frontmatter, tool grants, instruction globs, and duplicate blocks. Run unchanged; do not add prose assertions here. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing propagation and source-rendering regression suite. Run unchanged; generated-sync failures after source edits indicate pending maintainer propagation. | Read-only reference |
| `scripts/propagate_master_assets.py` | Canonical loader/parser for source agent frontmatter, roster display names, hidden state, tools, and skill references where exposed. Reuse it from focused tests where practical. | Read-only reference |
| `docs/learnings/cross-phase-decisions.md` | Records the blindness rule, the deferred Project - Planner offer, and the limits of structural evidence. | Read-only reference |
| `docs/learnings/project-learnings.md` | Records the prohibition on prose-pinning corpus guards and the duplicate-block threshold. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `source_of_truth/agents/02-phase-refiner.agent.md` exists. Its parsed frontmatter currently declares `tools: [read, search, edit, agent]` and `agents: [Web Researcher, Docs Writer]`. | AC1 can preserve both existing entries, and no new tool grant is required to delegate to the reviewer. | Add the exact reviewer display name parsed from the upstream agent only after that file exists; retain both current entries. |
| The current Refiner has the verified phase shape assumed by the plan: Phase 5 presents, Phase 6 writes the phase document, optionally writes discovery context, and synchronizes the roadmap, then Phase 7 opens/resumes the branch and commits `eval: phase-affirmed`. | AC2 and AC8 require a deliberate split of existing Phase 6 responsibilities, while AC9 can preserve the current Phase 7 text and ordering. | Move only the discovery/roadmap synchronization portion after the shared final-check path; keep document write before the offer and branch/commit after synchronization. |
| `source_of_truth/agents/02a-phase-final-check.agent.md` does not exist at expansion time. This is expected because the feature depends on the not-yet-implemented `06-phase-final-check-reviewer`. Its exact display name and testable metadata therefore cannot yet be verified. | AC1, AC4, and AC10 cannot be implemented safely until the upstream reviewer lands. Inventing a display name would violate the concrete-name rule. | **Decomposer warning:** enforce the declared dependency. At implementation time, parse the exact display name and metadata from the new file; do not substitute an inferred name. |
| No final-check contract skill exists under `source_of_truth/skills/` at expansion time, and `05-phase-final-check-contract` intentionally leaves its slug `[PROPOSED - name TBD: phase-final-check]`. | The shared skill reference required by AC10 cannot be named or tested until Feature 05 selects its final slug. | **Decomposer warning:** enforce the declared dependency. Discover the finalized skill path/reference from the upstream files before authoring tests or Refiner text. |
| The focused test file does not exist and its filename is not fixed by the phase. No referenced or planned exact test class or test method names are present. | A new consolidated Phase 02 verification module is required, but no invented concrete test name should be treated as established. | Keep `tests/[PROPOSED - name TBD: phase final-check contract guards]` until implementation selects an idiomatic filename; express tasks as scenarios rather than invented test symbols. |
| No `Tests/Editor/Phase*/`, `tests/phase*/`, or equivalent phase-scoped directory pattern exists. Tests are flat `tests/test_*.py` modules. | The plan's single focused Phase 02 pytest module is consistent with repository layout; no omitted consolidated phase file was discovered. | Create one flat focused pytest module and do not introduce a new phase directory. |
| `tests/test_agent_corpus_invariants.py` explicitly prohibits checks keyed to agent prose and already derives structure through `scripts/propagate_master_assets.py`. | Workflow and blindness guards must be structural enough to survive rewording and must not be added as phrase-pinning checks to the generic suite. | Keep focused source-contract guards separate, normalize scoped text, assert non-vacuity, and prove obligations with deletion/semantic-negation mutations. |
| The full baseline was re-run with `uv run pytest tests/` on 2026-08-11: 242 collected, 230 passed, 12 failed. Failures match the plan: one PR Review display-name collision, one wildcard `applyTo` enumeration check, and ten missing Unity reference-asset failures. | Regression success means no failures beyond this known set; the feature is not responsible for repairing them. | Compare focused and full runs against this baseline and report any new failure as a Phase 02 regression unless it is solely generated synchronization pending maintainer propagation. |
| The repo policy forbids agents from running propagation and forbids hand-editing `ports/` or `.github/`. | Source authoring can leave generated-sync assertions red until a maintainer propagates. | Do not run `scripts/propagate_master_assets.py`; report propagation pending after source changes. |

## Architectural Decisions

- Integrate the upstream skill and hidden reviewer into one shared Refiner continuation reached by both Entry A and Entry B. This avoids divergent offer behavior and keeps the reviewer contract centralized.
- Write the phase document before offering the final check. The cold-start reviewer must inspect a concrete on-disk artifact rather than session state.
- Treat accept, decline, and silence as terminal outcomes of the offer. The final check is advisory and may never strand phase refinement.
- Pass exactly the phase-document path and repository path to the reviewer. Conversation history, summaries, settled-area briefings, and the Refiner's assessment are outside the spawn boundary because they destroy review independence.
- Attempt review once. Error, timeout, or unusable output produces a one-line report and continuation with the unchanged document; there is no retry or inline replacement review.
- Relay usable findings verbatim, ask the user which to apply, and rewrite the phase document cleanly for accepted findings only. No ranking, filtering, editorializing, automatic application, artifact, or change-log framing is introduced.
- Defer discovery-context and roadmap synchronization until the offer/fold-in path completes, then execute each synchronization responsibility once before the existing branch/commit step.
- Use focused structural pytest guards backed by the canonical propagator loader where practical. Keep prose-sensitive contract checks out of the generic corpus suite and require non-vacuity plus mutation evidence.
- Add no persistent logs or findings files. Chat output is sufficient observability for the offer, result, failure state, and fold-in choice.

## Constraints

- `source_of_truth/` is the only authoring surface. Never hand-edit generated `ports/` or `.github/` output.
- Agents must not run `scripts/propagate_master_assets.py`; propagation is a maintainer-only step.
- Preserve the Refiner's existing `Web Researcher` and `Docs Writer` roster entries and existing `agent` tool grant.
- Resolve the reviewer display name and shared skill slug from the implemented upstream files; neither may be invented from the filenames.
- Use only the two repository-local paths in the reviewer payload and transmit no external data or session material.
- The offer remains optional and advisory. No pass/fail verdict, severity threshold, gate, retry, automatic fold-in, or revise-and-recheck loop is allowed.
- A decline, silence, failure, unusable response, or selection of no findings must leave the phase document unchanged and allow synchronization plus branch continuation.
- Usable findings must be relayed verbatim; only user-accepted findings may change the phase document.
- The phase document remains a clean current source of truth. Do not add change-log narration.
- Do not add persistent logs or persist reviewer findings.
- Do not remediate the 12 known baseline failures.
- Do not add structural tests that pin one exact prose rendering or duplicate ten or more contiguous contract lines across three agent files.

## Scope Boundaries

- Do not wire the final-check offer into Project - Planner; that extension is explicitly deferred.
- Do not modify unrelated Refiner phases. Limit the workflow edit to splitting current Phase 6, inserting one shared offer/fold-in continuation, and preserving Phase 7 behavior.
- Do not modify the upstream reviewer agent or contract skill; Features 06 and 05 own those files.
- Do not update generic corpus or propagation tests merely to accommodate the feature; run them unchanged as regression evidence.
- Do not introduce a phase-scoped test directory, generated-port tests, or harness-specific spawn wording.
- Do not persist findings, add telemetry, or create a review artifact.
- Do not modify any phase document, roadmap, or discovery context as part of repository implementation. Those are runtime outputs governed by the Refiner workflow being authored.
- Preserve the exact `eval: phase-affirmed` commit behavior and existing branch create/resume semantics after synchronization.

## Relationships to Sibling Plans

- `05-phase-final-check-contract` is the first prerequisite. It selects the final skill slug and supplies the reusable reading boundary, blindness obligation, finding eligibility, cap, and response shape consumed by both downstream features.
- `06-phase-final-check-reviewer` depends on Feature 05 and creates `source_of_truth/agents/02a-phase-final-check.agent.md`. Its final frontmatter provides the exact display name, hidden leaf topology, minimal tools, and shared-skill reference tested here.
- `07-phase-refiner-final-check` depends on both upstream features and is the phase's integration task. It connects both Refiner entry paths to the shared contract and reviewer, owns consolidated automated guards, and owns the combined manual smoke test.
- Feature 06 deliberately delegates automated evidence for its AC1–AC4 topology to this feature. Feature 05 likewise delegates downstream shared-reference and spawn-obligation evidence here.
- Project - Planner integration is a cross-phase deferred capability, not a sibling dependency or part of this feature.

## Suggested Implementation Order

1. Complete `05-phase-final-check-contract` and record the final skill slug/reference.
2. Complete `06-phase-final-check-reviewer`; parse its exact display name and confirm its hidden leaf metadata plus skill reference.
3. Add the focused failing integration guards for topology, shared reference, Refiner workflow order, continuation branches, and blindness.
4. Update Phase - Refiner frontmatter and workflow to satisfy the guards with one shared offer path.
5. Run focused mutations, unchanged regression suites, the full baseline comparison, and manual smoke tests for Entry A and Entry B.
6. Stop with maintainer propagation explicitly pending; do not regenerate ports.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 maintenance/test tooling plus Markdown source assets; stdlib-only runtime scripts; pytest 9.1.1 |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 230 passed, 12 failed, 242 collected — captured 2026-08-11. The 12 failures are pre-existing: one PR Review name collision, one wildcard `applyTo` enumeration failure, and ten Unity reference-asset failures. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- From `docs/learnings/cross-phase-decisions.md`: the cold-start review loses its value if the spawn prompt includes a session summary, settled-area guidance, or the Refiner's assessment. Keep the blindness prohibition at the spawn contract boundary.
- From `docs/learnings/cross-phase-decisions.md`: a structural guard can prove the prohibition exists but cannot prove runtime compliance. Manual exercise of both entry paths remains required before Phase 02 can be called complete.
- From `docs/learnings/cross-phase-decisions.md`: offering the same check in Project - Planner is deliberately deferred until the Refiner-stage path has real-session evidence. Do not expand scope here.
- From `docs/learnings/project-learnings.md`: corpus invariants are structural by policy; prose-matching checks become inert after rewording and will be rejected. Put scoped semantic/order checks in the focused module with explicit non-vacuity and mutation demonstrations.
- From `docs/learnings/project-learnings.md`: ten or more contiguous lines repeated across three or more agent files fail the duplicate-block invariant. Reference the shared skill rather than copying its contract into the Refiner or reviewer.
