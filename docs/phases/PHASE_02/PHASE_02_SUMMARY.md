# Phase 02: Merged Feature Scheduling and Phase Execution

**Status**: Planned
**Depends on**: Phase 01
**Estimated complexity**: Large
**Cross-references**: `source_of_truth/agents/03-feature-decomposer.agent.md`, `source_of_truth/agents/04-phase-execute.agent.md`, `source_of_truth/agents/04a-feature-plan-expander.agent.md`, `source_of_truth/agents/04b-feature-implementer.agent.md`, `source_of_truth/agents/04c-feature-review-and-fix.agent.md`, `source_of_truth/agents/05d-consistency-auditor.agent.md`, `source_of_truth/agents/05e-dependency-auditor.agent.md`, `source_of_truth/agents/05f-test-health.agent.md`, `source_of_truth/agents/05g-readiness-synthesizer.agent.md`, `source_of_truth/agents/05h-cleanliness-auditor.agent.md`, `source_of_truth/agents/auditor-refactor.agent.md`, `source_of_truth/skills/implementation-pipeline-loop/SKILL.md`, `source_of_truth/skills/feature-plan-set/SKILL.md`, `source_of_truth/skills/guard-integrity/SKILL.md`

## What's New

The feature decomposer and phase executor become one user-facing orchestrator. The orchestrator researches the phase once, writes lightweight feature plans, then executes one feature at a time. It expands each plan against the current repository state and revalidates affected future features after every dependency level.

A review committee replaces the single blind reviewer. Reviewers run concurrently against each implemented feature, and two trigger tables name the entry condition for every review agent. A consolidator merges their reports into one ranked fix list. The implementer that wrote the feature stays open and applies the fixes without rediscovering its own work.

The execution manifest becomes a living schedule. Its schema moves with it, so the skill that defines the manifest is rewritten in this phase rather than left describing the old static output.

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

- Replace the single post-implementation reviewer with a committee of concurrent reviewers, each differentiated by the evidence it may read.
- Reviewer A, plan conformance: the existing `04c-feature-review-and-fix` agent, narrowed to review only. Its fix authority moves to the held-open implementer, so it edits no source. Reads the plan and the diff. Maps every acceptance criterion to code. Blocks approval while the authoritative tests are unrun.
- Reviewer B, blast radius: reads outward from the diff and never evaluates the feature itself. Reports affected suites that did not run, callers with no coverage, non-code references such as schemas and config and name-based cross-references, and semantic breaks a caller's assertion is too loose to detect.
- Reviewer C, test falsification: reads the tests, not the code. Reports assertions that cannot fail, mocks the test configured itself, tests that pin implementation rather than behavior, and tests that would survive deleting the feature.
- Reviewer D, plan-blind: reads only the code and tests and never the plan. Reports what the code actually does, so a faithful implementation of a wrong plan is still caught.
- Run all four committee reviewers at `medium` tier, concurrently.
- Give each reviewer a lane. A reviewer files findings only inside its lane and stays silent outside it.
- Add a consolidator that merges every committee report into one deduplicated, severity-ranked fix list addressed to the implementer, and adjudicates disagreements between reviewers.
- Define two trigger tables that together name the entry condition for every review agent. The per-feature table covers agents evaluated against a feature's diff. The boundary table covers agents evaluated when a dependency level closes and when the phase closes.
- Run exactly the agents whose conditions hold.
- Derive every per-feature trigger from the changed-file list, with one stated exception. The visual verifier fires from a plan-level flag instead, because its subject is a phase's on-screen acceptance criteria rather than a file pattern.
- Derive every boundary trigger from a closure event, either a dependency level closing or the phase closing.
- Add a required visual-acceptance flag to the lightweight feature plan. The decomposition stage sets it when it writes an on-screen acceptance criterion.

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
- Apply `model_tier` to the twenty-three agents this pipeline spawns that are not user-invocable. Write no tier on user-invocable agents, where an absent key means the session model is inherited.
- Decide the tier rule by the agent's own invocability. A dual-use agent that a pipeline spawns and a user can also invoke carries no tier.
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
- Bound the mechanical rename to `source_of_truth/`, `tests/`, and repository-root files such as `CONTRIBUTING.md`. Tests and documentation that assert the old identifiers are in scope to be fixed alongside the rename, never left to fail.
- Exclude `docs/` from the mechanical pass. Documentation that names a renumbered agent is updated by Docs Writer at phase end, including this phase document's own cross-references.
- Delete generated output before regenerating, so no orphan can survive the rename. Remove `ports/` entirely and remove the four mirrored subdirectories `agents`, `hooks`, `instructions`, and `skills` from `.github/`.
- Preserve `.github/copilot-instructions.md`. It is the GitHub baseline destination written by `deploy_agents.py`, not propagation output, and the propagate script does not restore it. It is spliced section by section, so confirm the splice recreates a deleted file before treating deletion as safe.
- Update every `applyTo` glob naming a numbered agent. A glob that matches nothing fails silently and ships its instruction to no agent, so these cannot be verified by reading.
- Leave the generated stems for `prod-code-review` and `unity-reviewer` unchanged. Those stems carry no number, so the rename does not reach them.

**Manifest contract**

- Rewrite `source_of_truth/skills/feature-plan-set/SKILL.md` so the manifest it defines is the living schedule this phase describes.
- Add dependency level, dependency edges, expected read and write sets, plan revision, last validation commit, stale reason, and resolved model status to the manifest schema.
- Retire the term "wave" across the corpus in favor of "dependency level", including the skill's quality-checklist item that asserts a wave schedule. A checklist that keeps asserting the old term passes against a document that no longer means it.

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
| 6 | Review committee | Concurrent reviewers with disjoint evidence scopes and enforced lanes. | Three new reviewer agents, plus narrowing the existing review-and-fix agent into Reviewer A |
| 7 | Review trigger tables | One entry condition per review agent, split into per-feature and boundary tables. | Committee feature, gate wiring |
| 8 | Manifest schema rewrite | `feature-plan-set` defines the living schedule and drops the term "wave". | Skill rewrite, scheduling state |
| 9 | Finding consolidator | One deduplicated, severity-ranked fix list per review round, with disagreements adjudicated. | Consolidator agent |
| 10 | Held-open fix loop | The implementer applies its own fixes, with explicit fallback where a harness cannot resume it. | Loop skill, orchestrator |
| 11 | Dependency-level checks | Architecture, consistency, and test-health findings feed revalidation mid-phase. | Gate wiring |
| 12 | Failure and resumption paths | Bounded replan, blocked-feature handling, and feature-boundary resume. | Orchestrator state handling |
| 13 | Central model routing | One JSON file maps each tier to exact harness-specific model settings. | Config schema, validation, adapters |
| 14 | Session model preflight | The orchestrator displays routes, accepts tier overrides, and discloses fallback or unverifiable routing. | Session state, prompts, run record |
| 15 | Harness coverage | Claude Code, Codex, OpenCode, Cursor, and Copilot receive the correct model configuration shape. | Propagation and generated-output tests |
| 16 | Effectiveness measurement | Per-finding reviewer attribution and a committee-miss record at phase end. | Record templates |
| 17 | Renumbering | `04*` becomes `03*` and `05*` becomes `04*`, verified mechanically. | Final mechanical pass |
| 18 | Regression coverage | Tests cover scheduling, stale plans, committee lanes, routing, overrides, fallbacks, and preserved gates. | `tests/` |

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

### Review trigger tables

Every review agent has exactly one entry condition, recorded in one of two tables. The per-feature table is evaluated against a feature's diff inside the implement-review-commit loop. The boundary table is evaluated when a dependency level closes and when the phase closes.

#### Per-feature review triggers

| Review agent | Entry condition |
|---|---|
| Reviewer A, plan conformance | Always |
| Reviewer B, blast radius | The diff changes something another file imports or references |
| Reviewer C, test falsification | Always |
| Reviewer D, plan-blind | Always |
| Cleanliness auditor | Always |
| Diff security scan | The diff touches authentication, user input, network calls, or secrets |
| Dependency auditor | The diff changes a package manifest or lockfile |
| Unity reviewer | The repository satisfies the canonical Unity predicate in `tech-stack-detection` and the diff changes a `.cs` file under `Assets/` |
| Visual verifier | The feature plan carries the visual-acceptance flag |

Eight of the nine conditions are derived from the changed-file list. The visual verifier's is not, and the phase states that rather than claiming a uniformity it does not have. A screenshot answers a question about acceptance criteria, and acceptance criteria live in the plan. Any file-pattern proxy for that would both miss code-only changes that alter the screen and fire on asset edits with no visible effect.

#### Boundary triggers

| Review agent | Entry condition |
|---|---|
| Auditor - Refactor, architecture | A dependency level closed |
| Consistency auditor | A dependency level closed |
| Test health | A dependency level closed |
| Auditor - Refactor, backstop pass | The phase is closing |
| Prod code review | The phase is closing |

Boundary agents have no per-feature diff to trigger against, so they cannot live in the per-feature table. They are not unconditional either. "A dependency level closed" and "the phase is closing" are conditions that can fail to fire, and an agent whose condition never fires is an agent that never ran.

The tables replace counting reviewers as the correctness test. The check is that the set of agents that ran matches the set the tables predict, at both altitudes — per feature against the diff, and per boundary against the closure event. That catches an agent wrongly skipped. A count cannot.

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

Twenty-three agents, counted after this phase completes. Four are created by this phase and one existing agent is narrowed rather than added, so the count is post-phase.

Docs Writer is excluded. It is user-invocable, and a user-invocable agent never carries a tier even when a pipeline also spawns it. The rule is decided by the agent's own invocability, not by whether some pipeline uses it.

Already in the pipeline (14): Feature - Plan Expander, Feature - Implementer, Feature - Review and Fix (becomes Reviewer A), Unity Reviewer, Visual Verifier, Feature - QA Writer, Feature - QA Runner, Diff Security Scan, Prod Code Review, Auditor - Code, Auditor - Infra, Auditor - Delta, Auditor - Attribution, Baseline Worktree.

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

The review step moves from one reviewer per feature to four committee reviewers and the cleanliness auditor, plus up to four triggered specialists, plus a consolidator, with up to two fix rounds. That is roughly four to six times the current review cost per feature. This figure is the accepted budget, chosen deliberately against the cost of dedicated cleanup phases that currently follow several phases of work. All committee reviewers run at `medium` to hold it there.

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
- **Renumbering is atomic inside a phase that is not.** The workflow is built to continue when one feature fails, but the renumbering pass either completes or leaves the corpus internally inconsistent. A failed renumbering blocks the phase even though a failed feature does not.
- **Existing generated outputs are derived.** Maintainers must propagate source changes manually after implementation. Agents must not run propagation.

## Success Criteria

- [ ] One user invocation enters the merged orchestration flow without a required decomposer-to-executor handoff.
- [ ] Future features receive expanded context and task documents only shortly before execution.
- [ ] A test scenario where later features touch files changed by earlier levels causes targeted revalidation and schedule recomputation.
- [ ] The schedule records every dependency level, plan revision, revalidation result, and ordering change.
- [ ] The set of review agents that ran against a feature matches the set the per-feature trigger table predicts for that diff, and each reports only inside its own lane.
- [ ] The set of agents that ran at a dependency-level closure and at phase close matches the set the boundary trigger table predicts.
- [ ] Every review agent the phase spawns appears in exactly one of the two trigger tables.
- [ ] A feature whose diff touches nothing another file imports runs the committee without the blast-radius reviewer and is not treated as an incomplete review.
- [ ] A feature plan carrying the visual-acceptance flag runs the visual verifier, and one without it does not.
- [ ] The consolidator produces one ranked fix list, and duplicate findings across reviewers appear once.
- [ ] A reviewer disagreement about the same code reaches an adjudicated result rather than two contradictory instructions.
- [ ] Each triggered specialist runs when its condition holds and is skipped when it does not.
- [ ] The manifest schema and `feature-plan-set` describe the same living schedule, and no corpus file asserts a wave schedule.
- [ ] The implementer applies fixes without re-reading the feature from scratch, and a harness that cannot resume a subagent produces an explicit fallback record.
- [ ] Medium and Low findings do not trigger a fix round and do appear at phase final review.
- [ ] A feature that fails two fix rounds is replanned once, and a feature that fails after replanning is blocked along with its dependents while independent features continue.
- [ ] A dependency-level architecture finding changes the plan of a feature that has not yet been expanded.
- [ ] A dependency-level convention-consistency finding changes the plan of a feature that has not yet been expanded.
- [ ] A dependency-level test-health finding changes the plan of a feature that has not yet been expanded.
- [ ] The final architecture backstop pass runs before the phase closes, and its absence is recorded rather than passing silently.
- [ ] An interrupted phase resumes at the last completed feature, and an uncommitted working tree at startup is reported rather than built upon.
- [ ] Source agents contain only `low`, `medium`, or `high`, never harness-specific model IDs.
- [ ] Every one of the twenty-three pipeline subagents carries a tier, and no user-invocable agent does, including a dual-use agent such as Docs Writer.
- [ ] Generated routing covers all five harnesses with harness-correct fields.
- [ ] Session overrides change only the current run.
- [ ] Unsupported or unverifiable routes produce explicit fallback disclosure.
- [ ] Review records attribute each finding to the reviewer that produced it.
- [ ] After renumbering, no reference to a pre-renumber agent identifier remains in `source_of_truth/`, `tests/`, or repository-root files, and no agent references a name that does not exist.
- [ ] The full test suite passes after renumbering, with every test module that asserted a pre-renumber identifier updated rather than skipped.
- [ ] The Docs Writer pass at phase end leaves no pre-renumber agent identifier in `docs/`.
- [ ] After deletion and regeneration, `ports/` and the four mirrored `.github/` subdirectories contain no output file named for a pre-renumber source.
- [ ] A deletion-and-regeneration run confirms that `.github/copilot-instructions.md` is recreated with its baseline sections intact, before any renumbering step deletes generated output.
- [ ] Every `applyTo` glob naming a numbered agent still matches at least one agent after renumbering.
- [ ] The phase-end audit records which findings the committee did not catch.
- [ ] Existing implementation, review, QA, security, audit, and final-review gates remain intact.
- [ ] Source and generated-output tests pass after the maintainer propagates the changes.

## QA Considerations

Add structural tests for the routing schema, tier validation, source-field restrictions, tier coverage across the twenty-three pipeline agents, and each harness renderer.

Add scenario tests for provisional scheduling, level-boundary invalidation, downstream revalidation, and schedule recomputation. Add scenario tests for committee lane discipline, consolidator deduplication, reviewer disagreement adjudication, severity-gated fix rounds, the two-round limit, the replan path, the blocked-feature path, and feature-boundary resume.

Test session overrides for all three tiers and verify that the central file remains unchanged. Test unavailable models and unsupported harness routes for explicit fallback disclosure.

Add a test asserting that every review agent the phase spawns appears in exactly one trigger table, so a new agent cannot be added without an entry condition.

Add a test that resolves the per-feature trigger table against synthetic diffs — an isolated new file, an imported symbol change, a lockfile edit, an auth-touching change, a Unity `.cs` change under `Assets/`, and a plan with and without the visual-acceptance flag — and asserts the predicted agent set each time.

Confirm the `copilot-instructions.md` splice by deleting the file and regenerating, rather than by reading the propagation logic. Run this check before the renumbering feature relies on it.

Apply `guard-integrity` to every assertion that pins document or configuration content. Mutation checks must show that schedule, routing, committee, and renumbering assertions can fail when their required content is removed. The renumbering check must fail on a single missed identifier rather than passing because it was written to match whatever it found. Add a check that every `applyTo` glob resolves to at least one agent, because a stale glob produces no error.

Test that the phase-end audit records committee misses, and that the record is absent rather than silently empty when the audit did not run.

Run harness smoke checks where each platform exposes a local or CLI contract. Mark cloud-only behavior as verified, fallback, or unverified based on observed evidence rather than generated file content alone.

## Notes for Feature - Decomposer

Treat decomposition as an internal stage of the merged orchestrator. Produce candidate features and lightweight plans, not fully expanded bundles for the entire phase.

Record acceptance criteria, dependency hypotheses, expected read and write sets, affected symbols, and research evidence. Treat every feature after the first as provisional. Do not expand a future feature until the schedule selects it against the current repository state.

Sequence the renumbering feature last. Renumbering a corpus whose agents are still changing forces the pass to be redone. Author the four new agents at their post-renumber identifiers from the start, so they never enter the rename surface. Treat a failed renumbering as blocking for the phase, unlike a failed feature.

Sequence the `feature-plan-set` rewrite as a dependency of the scheduling feature, not as cleanup after it. The schedule cannot be authoritative while the skill that defines its schema describes the old static output.

Assign the discovery context's verification questions to the features whose success criteria depend on them. The harness model-format, runtime-reporting, and fallback questions belong to the routing and preflight features. The Codex handle and Copilot compaction questions belong to the held-open fix loop feature. The manifest-path-stability question belongs to the scheduling feature. Each is an implementation check, not a reopened decision.

When defining the reviewer agents, carry the evidence-scope rule into each agent body. A reviewer whose contract does not forbid reading outside its scope will drift into general review and dissolve the committee's value.

> Suggested implementation shape, to be verified by Feature Decomposer against current code and tests: the reference lookup that decides whether the blast-radius reviewer fires may be answerable from the existing code-graph tooling rather than a fresh scan.
