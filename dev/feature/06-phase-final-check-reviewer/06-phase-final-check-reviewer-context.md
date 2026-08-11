# Feature Context: Phase Final-Check Reviewer

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/agents/02a-phase-final-check.agent.md` | New hidden, response-only leaf reviewer. The phase fixes this exact path, but its frontmatter display name remains `[PROPOSED - name TBD]`. | Create |
| `source_of_truth/instructions/read-only-agent.instructions.md` | Existing enumerated instruction whose own description requires every agent without source-edit authority to be listed. Its `applyTo` currently omits the new `02a` reviewer, contradicting the plan's inheritance claim. | Modify |

### Read-Only References

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` | Runtime review contract produced by `05-phase-final-check-contract`; it does not exist yet, and Feature 05 deliberately leaves the final slug unresolved. | Read-only reference |
| `source_of_truth/agents/05c-artifact-sweeper.agent.md` | Verified hidden-leaf frontmatter reference with `user-invocable: false`; its broader write/execute grants must not be copied. | Read-only reference |
| `source_of_truth/agents/02-phase-refiner.agent.md` | Downstream parent that Feature 07 will rewire to declare and spawn this reviewer's final display name. This feature must not modify it. | Read-only reference |
| `scripts/propagate_master_assets.py` | Canonical frontmatter parser, `SourceAgent` loader, legal tool-key inventory, and instruction applicability implementation. It verifies that `read` and `search` are valid source tool keys. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` — `RosterTests`, `FrontmatterShapeTests`, `DuplicateBlockTests` | Verified existing regression classes for roster resolution, frontmatter/tool validity, and repeated 10-line blocks. They do not specifically prove this new agent is hidden, leaf-only, response-only, or skill-backed. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing parser/tool-key and instruction-`applyTo` regression coverage. The downstream focused test module may reuse its patterns but is owned by Feature 07. | Read-only reference |
| `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-plan.md` | Upstream contract requirements and unresolved final skill slug. | Read-only reference |
| `dev/feature/07-phase-refiner-final-check/07-phase-refiner-final-check-plan.md` | Downstream roster, spawn, focused-guard, mutation-evidence, and manual-smoke-test owner. | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase-fixed path, cold-start reading boundary, finding categories, response contract, no-write rule, and downstream integration order. | Read-only reference |
| `docs/phases/DISCOVERY_CONTEXT.md` and `docs/learnings/cross-phase-decisions.md` | Optional committed newcomer context inside the review reading boundary; absence is non-fatal. | Read-only reference |
| `docs/AUTHORING.md` | Source-only authoring, terse runtime-definition, generated-surface, and propagation-pending rules. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `source_of_truth/instructions/read-only-agent.instructions.md` uses an explicit filename allowlist and does not include `02a-phase-final-check.agent.md`. Its description says to add every agent whose tools exclude source edits. | The original plan's inheritance claim would have been false because the current `applyTo` cannot match the new reviewer. | **Resolved during decomposition:** Feature 06 now modifies the instruction atomically with the agent, and downstream guards verify applicability through the propagator. |
| Feature 05 has not run, so `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` does not exist and its final slug is intentionally unresolved. | The reviewer cannot safely author a concrete skill reference before its hard dependency is complete. | Enforce Wave 2 after Feature 05, read the finalized skill, and use its exact frontmatter/directory slug. Retain `[PROPOSED - name TBD]` in planning artifacts. |
| The phase fixes the reviewer filename but not its frontmatter display name. No existing `02a` agent exists. | Feature 07's roster and spawn call must use the exact parsed display name selected here. | Select a collision-safe `[PROPOSED - name TBD]` display name consistent with numbered agents; record it in implementation notes and the Feature 07 handoff. |
| `read` and `search` are verified legal source tool keys, and the propagator maps them to read/glob/grep capabilities. No existing source agent uses exactly `[read, search]`. | The proposed minimum grant is supported, but it is a new exact combination rather than an existing agent shape. | Use exactly `tools: [read, search]`; omit `edit`, `execute`, `agent`, `fetch`, and `todo`. Verify through the propagator loader and instruction applicability function. |
| `RosterTests`, `FrontmatterShapeTests`, and `DuplicateBlockTests` exist exactly as named. Their generic assertions do not require a specific new agent path, `user-invocable: false`, an empty roster, exact `[read, search]` tools, a shared-skill reference, or a response-only body. | Existing regression coverage is necessary but insufficient for AC1–AC7. | Preserve Feature 07 ownership of focused, non-vacuous guards and mutation evidence. Hand off scenario requirements rather than inventing test class or method names in this bundle. |
| The repository's tests are flat `tests/test_*.py` modules; no `tests/phase*/`, `Tests/Editor/Phase*/`, or consolidated Phase 02 test file exists. | The plan has not omitted a current-phase consolidated test asset. | Feature 07 may create one focused flat module with a final idiomatic name; keep it `[PROPOSED - name TBD]` until selected there. |
| The existing corpus guard rejects 10 or more significant contiguous lines duplicated across three or more agent bodies, and repository policy rejects prose-keyed corpus tests. | Copying the shared contract into this agent is both a maintainability defect and a regression risk; exact body wording is not a stable automated-test surface. | Reference the finalized skill once. Test structural topology and non-vacuous relationships; reserve qualitative finding quality and runtime blindness for manual QA. |
| The full suite still matches the plan's stated baseline on 2026-08-11: 242 collected, 230 passed, 12 failed. | Verification must not absorb or misattribute the unrelated failures. | Compare post-change results against the same 12 failures: one PR Review display-name collision, one wildcard `applyTo` enumeration failure, and ten missing Unity workflow-reference-asset failures. |

## Architectural Decisions

- Implement one stateless hidden leaf at the exact phase-specified `02a` path. It receives only a repository path and phase-document path, reads permitted committed context, and returns its analysis in the response.
- Use exactly the verified source tool keys `read` and `search`. The reviewer has no edit, execution, delegation, web, or task-list capability and declares no `agents:` roster.
- Add the new filename to the existing enumerated read-only instruction so the phase's inheritance statement is true. The agent body must still state its stricter rule: unlike ordinary report-producing read-only agents, it never writes even an assigned document.
- Consume the finalized Feature 05 skill by its selected slug. Keep only the reviewer-specific role, two-path input, workflow, error boundary, and return handoff in the agent; do not reproduce the reusable rubric.
- Treat blindness as both an input constraint and a behavioral constraint. The reviewer does not request, accept as authoritative, or infer conversation history, summaries, settled-area briefings, or the Refiner's assessment.
- Report a missing or unreadable supplied phase document to the caller and stop. Do not search for a substitute. Missing optional discovery or learning context does not fail the review.
- Keep the response advisory and bounded: no verdict, severity, score, retry, edit, or persisted artifact. Select at most five concrete findings, disclose truncation, and return a plain zero-findings state when appropriate.
- Add no logs. A transient structured response is sufficient observability for this leaf.
- Leave focused guard authoring and live Refiner invocation to Feature 07, while supplying it the exact finalized agent display name and skill slug.

## Constraints

- Feature `05-phase-final-check-contract` is a hard prerequisite. Do not guess its final skill slug or implement against its proposed placeholder.
- Author only under `source_of_truth/`; never edit `ports/` or `.github/`, and never run `scripts/propagate_master_assets.py`.
- Keep the runtime agent definition dense and brief. Shared contract text belongs in the skill and must not be duplicated.
- Preserve `user-invocable: false`, an absent `agents:` key, and exactly `tools: [read, search]`.
- The only accepted input is the supplied repository path plus supplied phase-document path. Do not request external systems, secrets, conversation transcripts, or session summaries.
- The response contains at most five findings, uses no severity or verdict, discloses when qualifying findings were omitted, and states zero findings plainly.
- Never write a phase document, roadmap, discovery context, learning, findings artifact, or any other repository file.
- Do not add prose-keyed corpus guards. Structural relationships must be non-vacuous and mutation-tested by Feature 07.
- Existing full-suite failures are baseline debt, not scope for this feature.

## Scope Boundaries

- Do not modify `source_of_truth/agents/02-phase-refiner.agent.md`, its roster, its workflow, or its error handling; Feature 07 owns integration.
- Do not author or rename the shared contract skill; Feature 05 owns it.
- Do not add focused tests in this feature; Feature 07 owns the new test module and mutation evidence.
- Do not add approval, fold-in, retry, timeout recovery, or continuation behavior to the reviewer. Those are parent-orchestrator responsibilities.
- Do not review whether the roadmap or phase-scoped discovery context has been synchronized; the check runs before those operations.
- Do not search for a replacement phase when the supplied file is missing or unreadable.
- Do not access external systems or uncommitted conversation context.
- Do not create any findings artifact or edit any repository document.
- Do not modify unrelated agent, instruction, test, documentation, dependency, or generated files.

## Relationships to Sibling Plans

- `05-phase-final-check-contract` is the hard upstream dependency. It finalizes the skill slug and reusable reading, blindness, finding, cap, exclusion, and response rules consumed here.
- `07-phase-refiner-final-check` is the downstream integration feature. It must consume this feature's exact parsed display name and Feature 05's exact skill slug, add the reviewer to Phase - Refiner's roster, issue the two-path blind spawn input, own failure continuation and accepted-finding fold-in, and create the focused guards.
- Feature 06 supplies no code API. Its public integration contract is the agent's parsed display name, its availability as a hidden leaf, the two-path input, and its skill-governed response.
- The existing read-only instruction is a companion authoring surface discovered during expansion. Assigning its allowlist update here avoids a transient reviewer that is documented as covered but is not.

## Suggested Implementation Order

1. Complete `05-phase-final-check-contract` and record its final skill slug.
2. Resolve the Discovery Delta by assigning the existing read-only instruction allowlist update to this feature.
3. Choose the reviewer's collision-safe display name and create the hidden leaf with exact `[read, search]` tools and the final skill reference.
4. Verify parsing, instruction applicability, no-write/no-roster boundaries, and absence of duplicated contract text.
5. Hand the exact display name, skill slug, and focused-guard scenarios to `07-phase-refiner-final-check`; then run regression checks without propagation.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/instruction corpus with Python 3.12.6 standard-library tooling, pytest 9.1.1, and pytest-cov 7.1.0. No application runtime or third-party runtime dependency. |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 242 collected: 230 passed, 12 failed — captured 2026-08-11. Failures are the known PR Review name collision, wildcard `applyTo` enumeration defect, and ten missing Unity workflow-reference-asset checks. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- **The blindness rule erodes through helpful spawn context.** The spawning agent must pass only the repository and phase-document paths; a session summary, settled-area briefing, or assessment of what matters destroys the cold-start value.
- **Structural presence does not prove runtime obedience.** Guards can prove that the blindness prohibition and topology exist, but a real Refiner smoke test is still required before Phase 02 completion.
- **A repeated block of 10 or more significant contiguous lines across three or more agent files fails the corpus invariant.** Keep the reusable review contract in the shared skill and reference it instead of copying it into consumers.
- **Corpus guards are structural by policy.** Do not pin arbitrary agent prose; verify parsed frontmatter, tool grants, roster topology, reference relationships, and non-vacuity, then use manual QA for finding quality.
