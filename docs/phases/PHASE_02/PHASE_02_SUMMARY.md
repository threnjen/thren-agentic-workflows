# Phase 02: Merged Feature Scheduling and Phase Execution

**Status**: Planned
**Depends on**: Phase 01
**Estimated complexity**: Large
**Cross-references**: `source_of_truth/agents/03-feature-decomposer.agent.md`, `source_of_truth/agents/04-phase-execute.agent.md`, `source_of_truth/agents/04a-feature-plan-expander.agent.md`, `source_of_truth/agents/04b-feature-implementer.agent.md`, `source_of_truth/agents/04c-feature-review-and-fix.agent.md`, `source_of_truth/agents/05d-consistency-auditor.agent.md`, `source_of_truth/agents/05e-dependency-auditor.agent.md`, `source_of_truth/agents/05f-test-health.agent.md`, `source_of_truth/agents/05g-readiness-synthesizer.agent.md`, `source_of_truth/agents/05h-cleanliness-auditor.agent.md`, `source_of_truth/agents/auditor-refactor.agent.md`, `source_of_truth/skills/implementation-pipeline-loop/SKILL.md`, `source_of_truth/skills/guard-integrity/SKILL.md`

## What's New

The feature decomposer and phase executor become one user-facing orchestrator. The orchestrator researches the phase once, writes lightweight feature plans, then executes one feature at a time. It expands each plan against the current repository state and revalidates affected future features after every dependency level.

A review committee replaces the single blind reviewer. Four reviewers run concurrently against each implemented feature. A consolidator merges their reports into one ranked fix list. The implementer that wrote the feature stays open and applies the fixes without rediscovering its own work.

Periodic checks at each dependency level catch problems that no single feature diff can show. Architecture, convention, and test-health findings feed the revalidation step, so features that are not yet expanded get planned around accumulated damage instead of adding to it.

Model selection becomes a central, harness-aware policy. Source agents name only `low`, `medium`, or `high`. A central routing file maps each tier to an exact model for each harness.

The agent numbering closes its gaps. The execution family moves from `04*` to `03*` and the PR Review family moves from `05*` to `04*`.

## Objective

Deliver one phase workflow that keeps decomposition quality high, prevents stale future plans, catches audit-class defects during the phase rather than after it, and makes child-agent model selection explicit across Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot.

## Scope

### In Scope

**Merged orchestration**

- Replace the separate user handoff between feature decomposition and phase execution with one orchestrator.
- Keep the `Phase - Execute` agent identity. Decomposition becomes an internal stage of that agent. Delete the separate decomposer agent.
- Preserve feature research and acceptance-criteria traceability from the current decomposer.
- Write lightweight feature plans before scheduling. Keep context and task documents just in time.
- Build a dependency graph, order the features from it, and recompute that order after every dependency level.
- Revalidate affected future features and every downstream dependent feature.
- Record schedule state, plan revisions, changed files, and revalidation results in the living execution manifest.
- Build one feature at a time. The dependency graph sets order and drives revalidation. It never authorizes two concurrent feature builds.

**Review committee**

- Replace the single post-implementation reviewer with four concurrent reviewers, each differentiated by the evidence it may read.
- Reviewer A, plan conformance: the existing `04c-feature-review-and-fix` agent, narrowed to review only. Its fix authority moves to the held-open implementer, so it edits no source. Reads the plan and the diff. Maps every acceptance criterion to code. Blocks approval while the authoritative tests are unrun.
- Reviewer B, blast radius: reads outward from the diff and never evaluates the feature itself. Reports affected suites that did not run, callers with no coverage, non-code references such as schemas and config and name-based cross-references, and semantic breaks a caller's assertion is too loose to detect. Runs only when the diff touches something other files import or reference.
- Reviewer C, test falsification: reads the tests, not the code. Reports assertions that cannot fail, mocks the test configured itself, tests that pin implementation rather than behavior, and tests that would survive deleting the feature.
- Reviewer D, plan-blind: reads only the code and tests and never the plan. Reports what the code actually does, so a faithful implementation of a wrong plan is still caught.
- Run all four at `medium` tier, concurrently.
- Give each reviewer a lane. A reviewer files findings only inside its lane and stays silent outside it.
- Add a consolidator that merges every committee report into one deduplicated, severity-ranked fix list addressed to the implementer, and adjudicates disagreements between reviewers.
- Keep cleanliness review always-on per feature. Run the security scan only when the diff touches authentication, user input, network calls, or secrets. Run the dependency audit only when the diff changes a package manifest or lockfile. Derive each trigger mechanically from the changed-file list.

**Fix loop**

- Hold the implementer open across review so it applies its own fixes without rediscovery.
- Where a harness cannot resume a subagent, fall back to a fresh implementer handed the implementation record and the consolidated fix list, and disclose the fallback.
- Gate fix rounds on severity. Blocker and High findings drive a round. Medium and Low findings are recorded and carried to phase final review.
- Allow at most two fix rounds. Re-review only the lanes that filed the findings being fixed.
- On escalation after two rounds, rewrite the feature plan once using the fix list as evidence, then rebuild the feature.
- If the rebuilt feature still fails, mark it blocked, mark its dependents blocked, and continue with independent features. Never halt the phase for one failed feature.

**Dependency-level checks**

- Run architecture, convention-consistency, and test-health checks when a dependency level closes, scoped to the phase diff so far.
- Feed their findings into the existing revalidation step so unexpanded features are planned around the findings.
- Run one final architecture pass before the phase closes as a backstop.

**Model routing**

- Add a canonical `model_tier` source field with the allowed values `low`, `medium`, and `high`.
- Apply `model_tier` to the twenty-four agents this pipeline spawns. Write no tier on user-invocable agents, where an absent key means the session model is inherited.
- Add `source_of_truth/config/model-routing.json` as the central harness-routing configuration.
- Render harness-specific model fields from that configuration without placing exact model IDs in source agent definitions.
- Display intended model routes at session start and accept user overrides by tier for the current run only.
- Report `enforced`, `fallback`, or `unverified` status for every resolved tier route.

**Resumption**

- Resume an interrupted phase at feature boundaries, using the manifest and the per-feature commits.
- Discard and rebuild any feature interrupted mid-loop rather than reasoning about partially applied fixes.
- Treat a manifest with an in-progress feature plus an uncommitted working tree as an interrupted run. Report it and offer resumption. Never build on top of it silently.
- Allow the orchestrator to drop decomposition context once the plans are written, because the manifest is its memory from that point.

**Effectiveness measurement**

- Record in each review record which reviewer produced which finding.
- Record at the phase-end audit which findings the committee did not catch.

**Renumbering**

- Move the execution family from `04*` to `03*` and the PR Review family from `05*` to `04*`.
- Rename the agents themselves, not only the filenames, because the number is part of the `name:` field and of every cross-reference.
- Execute the renumbering last, as one atomic mechanical pass.
- Bound the rename to `source_of_truth/` and `docs/`. Completed phase documents that record history are excluded, and the exclusion is listed explicitly rather than left implied.
- Delete generated output before regenerating, so no orphan can survive the rename. Remove `ports/` entirely and remove the four mirrored subdirectories `agents`, `hooks`, `instructions`, and `skills` from `.github/`.
- Preserve `.github/copilot-instructions.md`. It is the GitHub baseline destination written by `deploy_agents.py`, not propagation output, and the propagate script does not restore it. It is spliced section by section, so confirm the splice recreates a deleted file before treating deletion as safe.
- Update every `applyTo` glob naming a numbered agent. A glob that matches nothing fails silently and ships its instruction to no agent, so these cannot be verified by reading.
- Leave the generated stems for `prod-code-review` and `unity-reviewer` unchanged. Those stems carry no number, so the rename does not reach them.

**Corpus updates**

- Update propagation logic, generated-output tests, documentation, and compatibility references.

### Out of Scope

- Changing phase acceptance criteria or the phase-refiner workflow.
- Changing the model catalog, provider availability, organization policy, or harness licensing.
- Guaranteeing exact model enforcement where a harness does not expose that guarantee.
- Concurrent feature builds, per-feature worktrees, and write-set conflict detection.
- Applying `model_tier` to agents outside this pipeline.
- Redesigning other phases beyond references required by the merged entry point.
- Implementing product features described by the phase under execution.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Merged orchestrator | One user-invocable flow that owns research, scheduling, expansion, execution, and completion. | Agent definition, migration references |
| 2 | Lightweight feature plans | Initial plans carry acceptance criteria, scope, dependency hypotheses, and expected file impact. | Decomposition stage |
| 3 | Living execution schedule | The manifest records feature state, dependency levels, dependencies, plan revisions, and validation points. | Scheduling state |
| 4 | Just-in-time expansion | The orchestrator expands only the selected feature against the current tree. | Plan expander integration |
| 5 | Stale-plan revalidation | Level-boundary changes trigger targeted revalidation and schedule recomputation. | Dependency and impact checks |
| 6 | Review committee | Four concurrent reviewers with disjoint evidence scopes and enforced lanes. | Three new reviewer agents, plus narrowing the existing review-and-fix agent into Reviewer A |
| 7 | Finding consolidator | One deduplicated, severity-ranked fix list per review round, with disagreements adjudicated. | Consolidator agent |
| 8 | Held-open fix loop | The implementer applies its own fixes, with explicit fallback where a harness cannot resume it. | Loop skill, orchestrator |
| 9 | Dependency-level checks | Architecture, consistency, and test-health findings feed revalidation mid-phase. | Gate wiring |
| 10 | Failure and resumption paths | Bounded replan, blocked-feature handling, and feature-boundary resume. | Orchestrator state handling |
| 11 | Central model routing | One JSON file maps each tier to exact harness-specific model settings. | Config schema, validation, adapters |
| 12 | Session model preflight | The orchestrator displays routes, accepts tier overrides, and discloses fallback or unverifiable routing. | Session state, prompts, run record |
| 13 | Harness coverage | Claude Code, Codex, OpenCode, Cursor, and Copilot receive the correct model configuration shape. | Propagation and generated-output tests |
| 14 | Effectiveness measurement | Per-finding reviewer attribution and a committee-miss record at phase end. | Record templates |
| 15 | Renumbering | `04*` becomes `03*` and `05*` becomes `04*`, verified mechanically. | Final mechanical pass |
| 16 | Regression coverage | Tests cover scheduling, stale plans, committee lanes, routing, overrides, fallbacks, and preserved gates. | `tests/` |

## Technical Context

### Orchestration sequence

1. Resolve the central model configuration and detect the active harness.
2. Display the intended `low`, `medium`, and `high` routes.
3. Apply any user overrides to the current run without changing persistent configuration.
4. Research the phase and identify candidate features.
5. Write one lightweight plan per candidate feature.
6. Build the dependency graph and choose the first ready feature.
7. Expand only that feature into context and task documents.
8. Implement the feature.
9. Run the review committee concurrently. Run conditional specialists whose triggers fire.
10. Consolidate every report into one ranked fix list.
11. Apply fixes through the held-open implementer. Re-review only the lanes that filed. Repeat at most twice on Blocker or High findings.
12. Commit the feature.
13. When the dependency level closes, run the architecture, consistency, and test-health checks against the phase diff so far.
14. Record changed files and dependency evidence. Revalidate affected future features and their downstream dependents.
15. Rewrite stale plans and recompute ordering.
16. Repeat until all features complete, then run the existing phase completion gates.

### Dependency levels

A dependency level is the set of features whose dependencies are all satisfied at the same point in the graph. It is a scheduling and checkpoint unit, never a concurrency unit. Features inside a level build one at a time, in any order the graph permits.

A level closes when its last feature is committed. That closure is the trigger for the level checks and for revalidation, and it is derivable from the graph rather than left to orchestrator judgment.

Level boundaries matter because the next level's features are still unexpanded when the current one closes. A finding raised there can still change how they are planned.

### Committee design rule

Reviewers are differentiated by the evidence each may read, not by assigned subject matter. Reviewers given the same inputs and different topic lists converge on the same findings, and the committee then costs several times one report's value. Vantage points that do not overlap cannot converge.

Reviewer A is anchored to the plan. Reviewer D is forbidden from reading it. Reviewer B reads only outward from the diff. Reviewer C reads only the tests. Lane discipline holds this apart at runtime: a reviewer files findings inside its lane and stays silent outside it.

The consolidator exists because the orchestrator must not perform analysis. Merging reports, ranking findings across lanes, and adjudicating reviewer disagreements are analysis. Its output is a fix list addressed to an implementer, which is a different artifact and a different audience from the PR Review readiness report.

### Where defect classes are caught

Code-quality and security findings are accretive. Each one enters on a specific feature's diff, so a per-feature reviewer can catch it as it lands. The committee and the conditional specialists absorb these classes.

Architecture, convention, and coverage findings are emergent. They arise from accumulation across features, and no reviewer examining one diff can see them. Five features may each add one reasonable method to the same file and leave it needing a split that no single feature caused. These classes need a check at a different altitude, run when a dependency level closes, so the findings reach features that are not yet expanded.

Level-boundary timing matters. A check that runs only at phase end reports the damage after every feature is built, which relocates a cleanup phase rather than removing it.

### Living schedule contract

The execution manifest is the authoritative schedule. Each feature entry records its status, dependency level, dependency edges, expected read and write sets, plan revision, last validation commit, stale reason when applicable, and resolved model status.

The schedule can delay, split, merge, or rewrite a feature when later repository changes invalidate its assumptions. Every such change needs an evidence record tied to the changed files, symbols, acceptance criteria, or dependency edge.

The expected read and write sets remain recorded evidence for revalidation. They do not authorize concurrent feature builds.

### Pipeline agents receiving a tier

Twenty-four agents, counted after this phase completes. Four are created by this phase and one existing agent is narrowed rather than added, so the count is post-phase.

Already in the pipeline (15): Feature - Plan Expander, Feature - Implementer, Feature - Review and Fix (becomes Reviewer A), Unity Reviewer, Visual Verifier, Feature - QA Writer, Feature - QA Runner, Diff Security Scan, Prod Code Review, Docs Writer, Auditor - Code, Auditor - Infra, Auditor - Delta, Auditor - Attribution, Baseline Worktree.

Created by this phase (4): Reviewer B blast radius, Reviewer C test falsification, Reviewer D plan-blind, and the finding consolidator.

Existing agents newly recruited (5): Cleanliness Auditor, Dependency Auditor, Consistency Auditor, Test Health, Auditor - Refactor.

Nine of these also serve the PR Review and Auditor pipelines. Assigning them a tier makes the change visible in those pipelines, which is accepted rather than avoided.

### Model-tier contract

Source agent definitions use only the canonical `model_tier` field. The central routing file owns exact model identifiers and optional reasoning settings. Harness adapters translate canonical settings into each harness's supported fields.

- `high` handles initial decomposition and level revalidation.
- `medium` handles plan expansion, all four committee reviewers, consolidation, QA writing, and final readiness analysis.
- `low` handles implementation, test execution, and mechanical checks.

An absent `model_tier` on a user-invocable agent means the session model is inherited. This matches the corpus convention where the default token is never written.

The session preflight records the requested route, any user override, the resolved route, and the resolution status. A fallback never appears as successful enforcement. An unverified route is labeled unverified even when the generated configuration contains the requested model.

### Cost profile

The review step moves from one reviewer per feature to four always-on reviewers plus one to three conditional specialists plus a consolidator, with up to two fix rounds. That is roughly four to six times the current review cost per feature. This figure is the accepted budget, chosen deliberately against the cost of dedicated cleanup phases that currently follow several phases of work. All committee reviewers run at `medium` to hold it there.

Wall-clock cost rises less than token cost, because the committee runs concurrently. Fix rounds are the main addition to elapsed time.

### Context cost of the merge

Decomposition and execution are two agents today, and the handoff between them is a context reset that falls immediately after the heaviest research stage. Merging them removes that reset, and one agent then carries decomposition context through every level. Revalidation reads and per-feature subagent returns add to it.

This is a real cost of the merge. The resume path is the answer to it, together with the orchestrator's ability to drop decomposition context once plans are on disk.

## Dependencies & Risks

- **Subagent resumption differs by harness.** Claude Code supports live follow-up and post-completion resume. Cursor supports post-completion resume by returned ID. Codex can steer a running subagent but does not document resuming a finished one. OpenCode and GitHub Copilot do not document the capability at all. The fallback path is required, not precautionary. The discovery context records the researched constraints.
- **Claude Code's published documentation is stale on subagent resumption.** It still states that each invocation creates a new instance. Implementation must verify behavior against the installed version rather than the docs.
- **Copilot may silently compact a held-open child.** It auto-compacts at 95 percent of the token limit, and the documentation does not say whether this applies inside a subagent process.
- **Harness model contracts differ.** OpenCode binds models to agent definitions and needs tier-specific child agents. Cursor supports explicit subagent model IDs but caps nesting at grandchildren. Copilot CLI supports model dispatch while its cloud-agent surfaces do not offer the same deterministic contract.
- **Model availability can change.** Central configuration validation must detect unavailable or malformed model identifiers before execution begins.
- **Runtime enforcement may remain partly observable.** The orchestrator must distinguish generated intent from confirmed runtime use and disclose the difference.
- **Revalidation can change the feature graph.** The schedule must preserve traceability when it rewrites a plan or changes ordering.
- **Renumbering is a corpus-wide rename.** Twenty-two source files reference the current decomposer and executor by name, and the numbers live in `name:` fields rather than only in filenames. Propagation has previously damaged compound identifiers, so the rename needs a mechanical check rather than review by reading.
- **Committee findings may overlap heavily.** Without enforced lanes and consolidation, four reviewers produce one report's value at four times the cost.
- **Existing generated outputs are derived.** Maintainers must propagate source changes manually after implementation. Agents must not run propagation.

## Success Criteria

- [ ] One user invocation enters the merged orchestration flow without a required decomposer-to-executor handoff.
- [ ] Future features receive expanded context and task documents only shortly before execution.
- [ ] A test scenario where later features touch files changed by earlier levels causes targeted revalidation and schedule recomputation.
- [ ] The schedule records every dependency level, plan revision, revalidation result, and ordering change.
- [ ] Four reviewers run concurrently against one feature and each reports only inside its own lane.
- [ ] The consolidator produces one ranked fix list, and duplicate findings across reviewers appear once.
- [ ] A reviewer disagreement about the same code reaches an adjudicated result rather than two contradictory instructions.
- [ ] The conditional specialists run when their file-based triggers fire and are skipped when they do not.
- [ ] The implementer applies fixes without re-reading the feature from scratch, and a harness that cannot resume a subagent produces an explicit fallback record.
- [ ] Medium and Low findings do not trigger a fix round and do appear at phase final review.
- [ ] A feature that fails two fix rounds is replanned once, and a feature that fails after replanning is blocked along with its dependents while independent features continue.
- [ ] A dependency-level architecture finding changes the plan of a feature that has not yet been expanded.
- [ ] An interrupted phase resumes at the last completed feature, and an uncommitted working tree at startup is reported rather than built upon.
- [ ] Source agents contain only `low`, `medium`, or `high`, never harness-specific model IDs.
- [ ] Every one of the twenty-four pipeline subagents carries a tier, and no user-invocable agent does.
- [ ] Generated routing covers all five harnesses with harness-correct fields.
- [ ] Session overrides change only the current run.
- [ ] Unsupported or unverifiable routes produce explicit fallback disclosure.
- [ ] Review records attribute each finding to the reviewer that produced it.
- [ ] After renumbering, no reference to a pre-renumber agent identifier remains in `source_of_truth/` or `docs/`, excluding completed phase documents, and no agent references a name that does not exist.
- [ ] After deletion and regeneration, `ports/` and the four mirrored `.github/` subdirectories contain no output file named for a pre-renumber source.
- [ ] `.github/copilot-instructions.md` survives the regeneration cycle with its baseline sections intact.
- [ ] Every `applyTo` glob naming a numbered agent still matches at least one agent after renumbering.
- [ ] The phase-end audit records which findings the committee did not catch.
- [ ] Existing implementation, review, QA, security, audit, and final-review gates remain intact.
- [ ] Source and generated-output tests pass after the maintainer propagates the changes.

## QA Considerations

Add structural tests for the routing schema, tier validation, source-field restrictions, tier coverage across the twenty-four pipeline agents, and each harness renderer.

Add scenario tests for provisional scheduling, level-boundary invalidation, downstream revalidation, and schedule recomputation. Add scenario tests for committee lane discipline, consolidator deduplication, reviewer disagreement adjudication, severity-gated fix rounds, the two-round limit, the replan path, the blocked-feature path, and feature-boundary resume.

Test session overrides for all three tiers and verify that the central file remains unchanged. Test unavailable models and unsupported harness routes for explicit fallback disclosure.

Apply `guard-integrity` to every assertion that pins document or configuration content. Mutation checks must show that schedule, routing, committee, and renumbering assertions can fail when their required content is removed. The renumbering check must fail on a single missed identifier rather than passing because it was written to match whatever it found. Add a check that every `applyTo` glob resolves to at least one agent, because a stale glob produces no error.

Test that the phase-end audit records committee misses, and that the record is absent rather than silently empty when the audit did not run.

Run harness smoke checks where each platform exposes a local or CLI contract. Mark cloud-only behavior as verified, fallback, or unverified based on observed evidence rather than generated file content alone.

## Notes for Feature - Decomposer

Treat decomposition as an internal stage of the merged orchestrator. Produce candidate features and lightweight plans, not fully expanded bundles for the entire phase.

Record acceptance criteria, dependency hypotheses, expected read and write sets, affected symbols, and research evidence. Treat every feature after the first as provisional. Do not expand a future feature until the schedule selects it against the current repository state.

Sequence the renumbering feature last. Renumbering a corpus whose agents are still changing forces the pass to be redone.

When defining the reviewer agents, carry the evidence-scope rule into each agent body. A reviewer whose contract does not forbid reading outside its scope will drift into general review and dissolve the committee's value.

> Suggested implementation shape, to be verified by Feature Decomposer against current code and tests: the reference lookup that decides whether the blast-radius reviewer fires may be answerable from the existing code-graph tooling rather than a fresh scan.
