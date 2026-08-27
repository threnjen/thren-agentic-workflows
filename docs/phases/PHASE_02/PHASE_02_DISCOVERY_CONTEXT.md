# Phase 02 Discovery Context

Context gathered during refinement that lives outside this repository.

## User decisions

- Merge feature decomposition and phase execution into one user-facing orchestrator.
- Keep a living schedule rather than freezing the whole order during initial decomposition.
- Revalidate affected future features and their downstream prerequisite chain after each completed feature.
- Use per-harness exact model routing from one central configuration file.
- Keep source agent definitions at the abstract tiers `low`, `medium`, and `high`.
- Show intended model routes at the start of every orchestration session.
- Let the user override models by tier.
- Treat configured models as suggestions, not canon.
- Fall back with explicit disclosure when a harness cannot honor a route.
- Apply overrides to the current run only.
- Use `high` for decomposition and revalidation, `medium` for planning and review, and `low` for implementation and mechanical work.
- Replace the single blind reviewer with a four-reviewer committee, differentiated by the evidence each may read.
- Run all four committee reviewers concurrently at `medium`.
- Add a consolidator so the orchestrator never merges or ranks findings itself.
- Hold the implementer open across review so it applies its own fixes.
- Gate fix rounds on severity, allow at most two, then replan once before blocking the feature.
- Build one feature at a time. Drop concurrent feature builds and write-set conflict detection.
- Catch accretive defects per feature and emergent defects when the phase closes.
- Scope `model_tier` to the agents this pipeline spawns, not to all subagents.
- Keep the `Phase - Execute` identity for the merged agent and delete the decomposer.
- Renumber the corpus so no gaps remain: `04*` becomes `03*` and `05*` becomes `04*`. Execute it last.
- Accept a review step roughly four to six times the current cost, against the cost of dedicated cleanup phases.
- Measure which reviewer caught what, so the roster can be pruned later on evidence.
- Keep renumbering inside Phase 02 as its final feature rather than splitting it into its own phase.
- Define one trigger table with an entry condition for every review agent, in place of an always-on roster plus a separate conditional list.
- Test the review step by comparing the agent set that ran against the set the trigger table predicts, not by counting reviewers.
- Trigger the visual verifier from a plan-level visual-acceptance flag, and state in the phase that this one trigger is plan-derived while the rest are file-derived.
- Trigger the Unity reviewer from the canonical Unity predicate combined with a changed `.cs` file under `Assets/`.
- Make Phase 02 own the `feature-plan-set` skill rewrite and keep the corpus to two execution scopes, the feature and the phase.
- Decide the model-tier rule by an agent's own invocability. Docs Writer is user-invocable, so it carries no tier and leaves the pipeline tier count at twenty-three.
- Keep tests and documentation in scope for every change, including the rename. Test modules asserting old identifiers are fixed, never skipped.
- Exclude `docs/` from the mechanical rename pass. Docs Writer updates documentation at phase end, including this phase document's own cross-references.

## Current repository findings

- `source_of_truth/agents/03-phase-execute.agent.md` researches the phase, creates feature plans, validates the manifest, and runs the implementation pipeline.
- `source_of_truth/agents/03a-feature-plan-expander.agent.md` writes context and task documents before implementation.
- `source_of_truth/agents/03b-feature-implementer.agent.md` treats plan claims as hypotheses and follows the required mid-phase replan gate.
- `source_of_truth/agents/03c-feature-review-and-fix.agent.md` reviews each implemented feature while the implementer owns fixes.
- `scripts/propagate_master_assets.py` currently renders Codex agent metadata without model fields, hardcodes an OpenCode model, and emits `model: inherit` for Cursor.
- The current source agent frontmatter has no model-tier field.
- The current execution manifest is static after decomposition. This phase changes it into the living schedule.
- `tests/test_phase_execute_audit_bookend.py`, `tests/test_phase_refiner_final_check.py`, `tests/test_propagate_master_assets.py`, and `tests/test_agent_corpus_invariants.py` guard existing pipeline and generated-output contracts.
- `docs/learnings/` has no files. No repository learnings constrain this phase.

## Harness research

Research used official documentation available on 2026-08-22. Harness behavior and model catalogs can change, so implementation must verify the supported versions and run local smoke checks.

### Claude Code

Claude Code supports a `model` field in custom subagent definitions. A child can inherit the parent model or use an alias or full model identifier. Effort is a separate setting. The implementation must choose whether generated agents use aliases or full identifiers and must disclose any provider or organization fallback.

Sources: [Subagents](https://code.claude.com/docs/en/sub-agents), [Model configuration](https://code.claude.com/docs/en/model-config)

### Codex

Codex custom agent definitions support `model` and `model_reasoning_effort`. Codex also exposes model and effort through app-server turn configuration. The generated TOML must carry the exact model route for each tier. The implementation must verify precedence between custom-agent fields, invocation settings, defaults, and parent inheritance rather than assuming one universal precedence rule.

Sources: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [App server](https://learn.chatgpt.com/docs/app-server)

### OpenCode

OpenCode binds a model to an agent definition. A child without its own model inherits the parent model. The documented task call does not provide a portable per-call model argument, so the adapter should generate separate tier-specific child agents with exact model values. The implementation must target one supported OpenCode configuration version because the documented configuration shapes differ across versions.

Sources: [Agents](https://opencode.ai/docs/agents/), [Configuration](https://opencode.ai/docs/config/), [Models](https://opencode.ai/docs/models/)

### Cursor

Cursor subagents support `inherit` or an explicit model identifier. Project agent definitions take precedence over user definitions when names conflict. The SDK and API can carry model data directly, but `auto` routing does not provide a stable exact-model guarantee. The generated route should use fixed identifiers where reproducibility matters and mark inherited or policy-replaced routes appropriately.

Sources: [Subagents](https://cursor.com/docs/subagents), [SDK](https://cursor.com/docs/sdk/typescript), [Cloud agent API](https://cursor.com/docs/cloud-agent/api/endpoints)

### GitHub Copilot

Copilot CLI supports model selection per dispatch and model fields in custom agents. Reasoning effort is separate from the model. User settings, session commands, organization policy, plan limits, and `Auto` selection can affect the resolved route. GitHub cloud-agent surfaces do not expose the same deterministic model contract as the CLI, so the adapter must distinguish CLI enforcement from cloud fallback or unverified behavior.

Sources: [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference), [Custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents), [Custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

## Subagent resumption research

Researched to settle whether the implementer can be held open across review. Full report at `dev/research/harness-subagent-resumption/`.

| Harness | Can resume a subagent with context | Mechanism | Confidence |
|---|---|---|---|
| Claude Code | Yes, live follow-up and post-completion resume | `SendMessage`, addressed by agent ID or name | Documented and supported |
| Cursor | Yes, post-completion resume only | Natural-language resume by the ID each execution returns | Documented and supported |
| Codex | Partial. Steer a running subagent. Finished threads are not documented as resumable | No named tool or ID | Documented, mechanism unnamed |
| OpenCode | Not documented | Session-level `--session`, `--continue`, and `--fork` only | High confidence it is undocumented |
| GitHub Copilot | Not documented | `--resume` and `--continue` target the caller's own session | High confidence it is undocumented |

Findings that change implementation assumptions:

- Claude Code's published documentation still states that each subagent invocation creates a new instance. That is stale as of v2.1.198. Verify against the installed version, not the docs.
- Claude Code deletes subagent transcripts after `cleanupPeriodDays`, default 30. A resume-based loop degrades to "agent not found" after that window. Feature-boundary resume must not depend on a held-open agent.
- Copilot auto-compacts at 95 percent of the token limit, and the documentation does not say whether that applies inside a subagent process. A held-open child there may be compacted silently.
- Codex waits for all fan-out results before returning a consolidated response. No partial-result streaming, so a committee cannot exit early on a Blocker finding.
- Cursor caps nesting at grandchildren. A three-tier orchestrator does not port. This independently confirms the depth-one rule.

## Measured migration surface

Twenty-two source files under `source_of_truth/` reference the current decomposer or executor by name: eight agents, six instruction files, six skills, and the two agent files themselves. Generated copies under `ports/` and `.github/` follow on the next propagation.

The agent number is part of the `name:` field, not only the filename, so renumbering is a rename of agent identity across the corpus. Propagation has previously damaged compound identifiers, which is why the renumbering needs a mechanical check rather than review by reading.

## Agent inventory for tier assignment

Sixty-one agent files exist: forty-four with `user-invocable: false` and seventeen user-invocable roots. Tier assignment is scoped to the twenty-four agents this pipeline spawns, not to all forty-four.

Several of those twenty-four also serve the PR Review and Auditor pipelines. Assigning them a tier makes the change visible in three pipelines even though only one was reasoned about.

## Design implications

1. The source schema needs an abstract `model_tier` field.
2. The central routing file needs a canonical model field and optional canonical effort field.
3. Each renderer needs a harness-specific adapter instead of copying one model field blindly.
4. OpenCode likely needs one generated child definition per tier.
5. The session preflight needs a resolved-route table with requested model, override, actual route when observable, and status.
6. The schedule and run record need to preserve model status alongside feature status.
7. Tests must assert routing shape and disclosure behavior without hardcoding provider availability.

## Stale-plan scenario

Initial research may place a feature at level five because its expected files do not conflict with the level-one and level-three plans. If those earlier features change the same files or their APIs, the level-five plan becomes stale.

The merged flow prevents this by withholding expansion documents for level five, recording changed files as each earlier feature completes, revalidating level five and its downstream dependents, and recomputing the schedule before level five starts.

## Verification questions for implementation

- Which supported model identifier format is stable enough for each harness?
- Which harnesses can report the model actually used by a child at runtime?
- What exact fallback does each harness apply when a configured model is unavailable?
- Which existing external references invoke agents 03 and 04 by name, beyond the twenty-two measured under `source_of_truth/`?
- Does Codex expose any addressable handle for a running subagent, or only conversational steering?
- Does Copilot's auto-compaction apply inside a subagent process?
- Can the current manifest path remain stable while its semantics change from static output to living schedule?

These questions do not reopen the phase decisions. They define implementation checks required before the phase can claim exact routing or migration completeness.
