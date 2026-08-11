# Feature Context: Phase Final-Check Contract

## Key Files

### Files Changed

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` | New shared review contract consumed by the final-check reviewer and Phase - Refiner; owns the reading boundary, blindness obligations, finding eligibility, five-finding cap, exclusions, and response states. The implementer must choose a concise collision-free slug and record it for sibling features. | Create |

### Read-Only Reference Files

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Authoritative Phase 02 requirements, scope exclusions, failure modes, and success criteria. | Read-only reference |
| `docs/phases/DISCOVERY_CONTEXT.md` | Existing project-wide committed context that the new contract permits the reviewer to read; also records the advisory, one-pass final-check decision. | Read-only reference |
| `docs/learnings/cross-phase-decisions.md` | Existing committed decisions that the reading boundary permits; records the Project - Planner deferral and the blindness-rule risk. | Read-only reference |
| `source_of_truth/skills/feature-plan-set/SKILL.md` | Verified directory-based skill and frontmatter convention. | Read-only reference |
| `source_of_truth/agents/02-phase-refiner.agent.md` | Downstream spawner that will consume the selected skill and obey its blindness obligations in `07-phase-refiner-final-check`. | Read-only reference |
| `dev/feature/06-phase-final-check-reviewer/06-phase-final-check-reviewer-plan.md` | Downstream reviewer plan; depends on the finalized vocabulary and selected skill slug. | Read-only reference |
| `dev/feature/07-phase-refiner-final-check/07-phase-refiner-final-check-plan.md` | Downstream integration and focused-test plan; owns semantic guards, mutation evidence, and Refiner wiring. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing generic structural coverage for skill frontmatter and repeated 10-or-more-line blocks; not a semantic prose-contract suite. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing source parsing/rendering regression suite used downstream without planned edits. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| All existing references were verified: the Phase 02 summary, project discovery context, cross-phase decisions, Phase - Refiner, generic corpus test, propagation test, and both sibling plans exist. | The plan's inputs and dependency chain are current. | None. |
| No current skill directory supplies this contract, and Phase 02 does not fix its slug. The plan correctly marks `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` as proposed. | The implementer must make one naming decision before either downstream consumer can reference the skill. | Select a concise, collision-free slug; use it in frontmatter and directory name; record it in implementation notes for features 06 and 07. |
| `tests/test_agent_corpus_invariants.py` verifies skill frontmatter and duplicated blocks structurally, but its written policy rejects prose-keyed semantic assertions. | That suite cannot prove the six categories, blindness language, cap, or exclusions. | Keep semantic and mutation-tested contract guards in downstream `07-phase-refiner-final-check`, as planned; do not add phrase-pinning assertions to the generic suite. |
| No phase-scoped test directory convention or Phase 02 consolidated test module currently exists. The sibling `07-phase-refiner-final-check` plan already reserves one proposed focused module for all cross-feature guards. | This feature does not need a separate test bootstrap or a second test module. | Preserve the downstream consolidated-test ownership; use code review plus existing structural regressions here. |
| Both optional committed-context examples named by the phase currently exist. A phase-scoped `PHASE_02_DISCOVERY_CONTEXT.md` does not exist and is not required by the reading contract. | The contract must describe optional committed context without turning missing optional files into an error or expanding scope to sync-state checks. | State the allowed reading boundary and missing-file behavior without requiring a fixed surrounding-file inventory. |
| No test class name is referenced by this plan. The proposed downstream test file remains correctly marked `[PROPOSED - name TBD: phase final-check contract guards]`. | No invented test class or method name needs correction. | Keep tasks scenario-based and leave exact test naming to feature 07. |

## Architectural Decisions

- Put the reusable obligations in one directory-based skill because the reviewer and Phase - Refiner consume the same contract; do not copy the contract body into either agent.
- Keep the skill limited to three concerns: permitted reading, qualifying findings, and response shape. This is the smallest shared surface both consumers need.
- Make blindness a spawner obligation: the spawn input carries only the phase-document path and repository path. Conversation history, summaries, settled-area framing, and the spawner's assessment are forbidden.
- Permit repository facts and committed project context to inform findings, including `docs/phases/DISCOVERY_CONTEXT.md` and `docs/learnings/cross-phase-decisions.md` when present. Conversation content remains outside the boundary.
- Restrict findings to the six Phase 02 categories and require a phase location or concrete repository fact for each. Consolidate similar observations before applying the cap.
- Cap output at five findings, disclose omitted qualifying findings, and make a plain zero-findings response valid. Do not add severity, verdict, rubric, or blocking language.
- Keep failure recovery, user interaction, fold-in behavior, and continuation branches out of the shared skill; Phase - Refiner owns those orchestration concerns.
- Add no logs or persisted artifact. The response is the only output, including explicit zero-findings and truncation states.

## Constraints

- Author only under `source_of_truth/`; `ports/` and `.github/` are generated and must not be edited.
- Do not run `scripts/propagate_master_assets.py`; propagation is a maintainer-only step.
- Agent and skill definitions are runtime context, so the contract must be dense, brief, and non-repetitive.
- The final skill must use valid `name` and `description` frontmatter and the existing `source_of_truth/skills/<slug>/SKILL.md` layout.
- Any still-unverified concrete slug must retain `[PROPOSED - name TBD]` status until implementation selects and records it.
- Do not add tests in this feature. Feature 07 owns the focused semantic and mutation-tested guards.
- Preserve the recorded red baseline; do not absorb or remediate unrelated test failures.
- Structural tests must not pin one exact prose rendering. Semantic guards belong in the focused Phase 02 module and must be demonstrably non-vacuous.
- No authentication, secrets, external systems, metrics, tracing, or persistent findings store are introduced.

## Scope Boundaries

- Create only the shared contract skill; do not create `source_of_truth/agents/02a-phase-final-check.agent.md`.
- Do not modify `source_of_truth/agents/02-phase-refiner.agent.md`, its `agents:` roster, its workflow, or its user-interaction branches.
- Do not create `tests/[PROPOSED - name TBD: phase final-check contract guards]` or edit existing test modules.
- Do not add Project - Planner wiring; that offer is deliberately deferred.
- Do not define retry, timeout, reviewer-failure, no-answer, approval, fold-in, sync, branch, or commit behavior in the shared skill.
- Do not let roadmap or discovery-context synchronization state qualify as a finding.
- Do not add a rubric, severity scale, pass/fail judgment, blocking threshold, second pass, automatic edit, or findings artifact.
- Do not request conversation content, secrets, uncommitted session summaries, or external data.

## Relationships to Sibling Plans

- `06-phase-final-check-reviewer` depends on this feature. It must reference the selected skill slug and implement the contract without copying its body.
- `07-phase-refiner-final-check` depends on both this feature and feature 06. It uses the same selected slug, makes the reviewer discoverable in Phase - Refiner, implements the two-path spawn payload, and owns focused contract guards plus mutation evidence.
- The shared public contract required downstream is fully covered by AC1–AC7: reading boundary, spawner blindness obligations, six finding categories, evidence requirement, five-finding cap, zero/truncation states, and excluded authority.
- The cross-phase Project - Planner offer remains deferred in `docs/learnings/cross-phase-decisions.md`; no sibling in this phase may add it.

## Suggested Implementation Order

1. Execute this Wave 1 feature first and finalize the skill slug and vocabulary.
2. Pass the exact selected slug to `06-phase-final-check-reviewer`, which authors the hidden read-only leaf in Wave 2.
3. Execute `07-phase-refiner-final-check` after features 05 and 06; it wires both consumers, adds consolidated guards, and performs combined regression and smoke verification.
4. Treat this feature's `parallel safe: yes` metadata as permission to run beside unrelated Wave 1 work only; features 06 and 07 remain sequential dependents.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill corpus with Python 3.12.6 standard-library transform/deploy scripts; pytest tests configured by root `pyproject.toml` |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 230 passed, 12 failed, 63 subtests passed — captured 2026-08-11. Pre-existing failures: one PR Review name collision, one wildcard `applyTo` enumeration failure, and ten Unity reference-asset failures caused by the missing GameCI workflow asset. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- From `docs/learnings/project-learnings.md`: a block of 10 or more contiguous lines repeated across three or more agent files fails `tests/test_agent_corpus_invariants.py`; shared contract text belongs in a skill rather than copied consumer bodies.
- From `docs/learnings/project-learnings.md`: corpus tests are intentionally structural and should not assert on exact wording, because rephrasing makes prose guards inert. Phase 02 semantic coverage therefore belongs in a scoped, non-vacuous focused module.
- From `docs/learnings/cross-phase-decisions.md`: the cold-start reviewer's value is destroyed by a helpful spawn briefing. The prohibition must live in the spawn contract, and a structural guard can prove the rule exists but cannot prove runtime obedience.
- From `docs/learnings/cross-phase-decisions.md`: adding the same offer to Project - Planner is deferred until the Refiner-stage check has been exercised in a real session.
