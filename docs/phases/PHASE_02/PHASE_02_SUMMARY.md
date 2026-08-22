# Phase 02: Merged Feature Scheduling and Phase Execution

**Status**: Planned
**Depends on**: Phase 01
**Estimated complexity**: Large
**Cross-references**: `source_of_truth/agents/03-feature-decomposer.agent.md`, `source_of_truth/agents/04-phase-execute.agent.md`, `source_of_truth/agents/04a-feature-plan-expander.agent.md`, `source_of_truth/agents/04b-feature-implementer.agent.md`, `source_of_truth/agents/04c-feature-review-and-fix.agent.md`

## What's New

The feature decomposer and phase executor become one user-facing orchestrator. The orchestrator researches the phase once, creates lightweight feature plans, and then executes one current wave at a time.

The orchestrator expands plans against the current repository state. After each wave, it revalidates affected future features and their downstream dependency chain before recalculating order and concurrency.

Model selection becomes a central, harness-aware policy. Source agents name only `low`, `medium`, or `high`. A central routing file maps each tier to an exact model for each harness. The orchestrator shows those suggestions at session start and accepts temporary tier overrides.

## Objective

Deliver one phase workflow that keeps decomposition quality high, prevents stale future plans, and makes child-agent model selection explicit across Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot.

## Scope

### In Scope

- Replace the separate user handoff between feature decomposition and phase execution with one orchestrator.
- Preserve feature research and acceptance-criteria traceability from the current decomposer.
- Write lightweight feature plans before scheduling. Keep context and task documents just in time.
- Build a provisional dependency graph and select the first ready wave.
- Recalculate wave order and concurrency from the current repository state after every wave.
- Revalidate affected future features and every downstream dependent feature.
- Record schedule state, plan revisions, changed files, and revalidation results in the living execution manifest.
- Add a canonical `model_tier` source field with the allowed values `low`, `medium`, and `high`.
- Add `source_of_truth/config/model-routing.json` as the central harness-routing configuration.
- Render harness-specific model fields from that configuration without placing exact model IDs in source agent definitions.
- Display intended model routes at session start.
- Accept user overrides by tier for the current run only.
- Report `enforced`, `fallback`, or `unverified` status for every resolved tier route.
- Preserve implementation, review, QA, security, audit, and final-review gates.
- Update propagation logic, generated-output tests, documentation, and compatibility references.

### Out of Scope

- Changing phase acceptance criteria or the phase-refiner workflow.
- Changing the model catalog, provider availability, organization policy, or harness licensing.
- Guaranteeing exact model enforcement where a harness does not expose that guarantee.
- Redesigning phases 01, 02, or 05 beyond references required by the merged entry point.
- Implementing product features described by the phase under execution.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Merged orchestrator | One user-invocable flow that owns research, scheduling, expansion, execution, and completion. | Agent definition, migration references |
| 2 | Lightweight feature plans | Initial plans contain acceptance criteria, scope, dependency hypotheses, and expected file impact. | Decomposition stage |
| 3 | Living execution schedule | The current manifest records feature state, waves, dependencies, write sets, plan revisions, and validation points. | Scheduling state |
| 4 | Just-in-time expansion | The orchestrator expands only the selected wave against the current tree. | Plan expander integration |
| 5 | Stale-plan revalidation | Post-wave changes trigger targeted revalidation and downstream schedule recomputation. | Dependency and impact checks |
| 6 | Central model routing | One JSON file maps each tier to exact harness-specific model settings. | Config schema, validation, adapters |
| 7 | Session model preflight | The orchestrator displays routes, accepts tier overrides, and discloses fallback or unverifiable routing. | Session state, prompts, run record |
| 8 | Harness coverage | Claude Code, Codex, OpenCode, Cursor, and Copilot receive the correct model configuration shape. | Propagation and generated-output tests |
| 9 | Regression coverage | Tests cover scheduling, stale plans, routing, overrides, fallbacks, and preserved execution gates. | `tests/` |

## Technical Context

### Orchestration sequence

1. Resolve the central model configuration and detect the active harness.
2. Display the intended `low`, `medium`, and `high` routes.
3. Apply any user overrides to the current run without changing persistent configuration.
4. Research the phase and identify candidate features.
5. Write one lightweight plan per candidate feature.
6. Build the provisional dependency graph and choose the first ready wave.
7. Expand only that wave into context and task documents.
8. Implement, review, test, and complete the wave.
9. Record changed files and affected dependency evidence.
10. Revalidate affected future features and their downstream dependency chain.
11. Rewrite stale plans and recompute ordering and concurrency.
12. Repeat until all features complete, then run the existing phase completion gates.

The initial graph can determine the first wave. It cannot permanently determine every later wave. Features run concurrently only when the current dependency graph permits it and their expected write sets do not conflict. The orchestrator serializes uncertain conflicts.

### Living schedule contract

The existing execution manifest becomes the authoritative schedule. Each feature entry records its status, current wave, dependency edges, expected read and write sets, plan revision, last validation commit, stale reason when applicable, and resolved model status.

The schedule can delay, split, merge, or rewrite a feature when later repository changes invalidate its assumptions. Every such change needs an evidence record tied to the changed files, symbols, acceptance criteria, or dependency edge.

### Model-tier contract

Source agent definitions use only the canonical `model_tier` field. The central routing file owns exact model identifiers and optional reasoning settings. Harness adapters translate canonical settings into each harness's supported fields.

- `high` handles initial decomposition and wave revalidation.
- `medium` handles plan expansion, review and fix, QA writing, and final readiness analysis.
- `low` handles implementation, test execution, and mechanical checks.

The session preflight records the requested route, any user override, the resolved route, and the resolution status. A fallback never appears as successful enforcement. An unverified route is labeled as unverified even when the generated configuration contains the requested model.

## Dependencies & Risks

- **Harness contracts differ.** Claude Code and Codex support model fields in child-agent definitions. OpenCode binds models to agent definitions and needs tier-specific child agents when a task call cannot carry a model. Cursor supports explicit subagent model IDs. Copilot CLI supports model dispatch, but cloud-agent surfaces do not offer the same deterministic contract. The discovery context records the researched constraints and verification plan.
- **Model availability can change.** Central configuration validation must detect unavailable or malformed model identifiers before execution begins.
- **Runtime enforcement may remain partly observable.** The orchestrator must distinguish generated intent from confirmed runtime use and disclose the difference.
- **Revalidation can change the feature graph.** The schedule must preserve traceability when it rewrites a plan or changes concurrency.
- **Existing generated outputs are derived.** Maintainers must propagate source changes manually after implementation. Agents must not run propagation.

## Success Criteria

- [ ] One user invocation enters the merged orchestration flow without a required 03-to-04 handoff.
- [ ] Future waves receive expanded context and task documents only shortly before execution.
- [ ] A test scenario where later features touch files changed by earlier waves causes targeted revalidation and schedule recomputation.
- [ ] The schedule records every wave, plan revision, revalidation result, and ordering change.
- [ ] Source agents contain only `low`, `medium`, or `high`, never harness-specific model IDs.
- [ ] Generated routing covers all five harnesses with harness-correct fields.
- [ ] Session overrides change only the current run.
- [ ] Unsupported or unverifiable routes produce explicit fallback disclosure.
- [ ] Existing implementation, review, QA, security, audit, and final-review gates remain intact.
- [ ] Source and generated-output tests pass after the maintainer propagates the changes.

## QA Considerations

Add structural tests for the routing schema, tier validation, source-field restrictions, and each harness renderer. Add scenario tests for provisional scheduling, write-set conflicts, post-wave invalidation, downstream revalidation, and schedule recomputation.

Test session overrides for all three tiers and verify that the central file remains unchanged. Test unavailable models and unsupported harness routes for explicit fallback disclosure. Add mutation checks to ensure schedule and routing assertions can fail when their required content is removed.

Run harness smoke checks where each platform exposes a local or CLI contract. Mark cloud-only behavior as verified, fallback, or unverified based on observed evidence rather than generated file content alone.

## Notes for Feature - Decomposer

Treat decomposition as an internal stage of the merged orchestrator. Produce candidate features and lightweight plans, not fully expanded bundles for the entire phase.

Record acceptance criteria, dependency hypotheses, expected read and write sets, affected symbols, and research evidence. Treat every wave after the first as provisional. Do not expand a future feature until the schedule selects it against the current repository state.

After each wave, revalidate the affected future feature set and its transitive downstream dependents. Preserve the original plan revision and record the reason for every rewrite or schedule change.
