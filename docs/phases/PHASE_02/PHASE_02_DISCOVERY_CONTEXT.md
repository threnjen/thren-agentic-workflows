# Phase 02 Discovery Context

Context gathered during refinement that lives outside this repository.

## User decisions

- Merge feature decomposition and phase execution into one user-facing orchestrator.
- Keep a living schedule rather than freezing every wave during initial decomposition.
- Revalidate affected future features and their downstream dependency chain after each wave.
- Use per-harness exact model routing from one central configuration file.
- Keep source agent definitions at the abstract tiers `low`, `medium`, and `high`.
- Show intended model routes at the start of every orchestration session.
- Let the user override models by tier.
- Treat configured models as suggestions, not canon.
- Fall back with explicit disclosure when a harness cannot honor a route.
- Apply overrides to the current run only.
- Use `high` for decomposition and revalidation, `medium` for planning and review, and `low` for implementation and mechanical work.

## Current repository findings

- `source_of_truth/agents/03-feature-decomposer.agent.md` researches the phase, creates feature plans, expands all feature bundles, validates them, and writes an execution manifest.
- `source_of_truth/agents/04-phase-execute.agent.md` validates the manifest, executes waves, runs implementation and review subagents, runs wave gates, and completes consolidated QA and final review.
- `source_of_truth/agents/04a-feature-plan-expander.agent.md` writes context and task documents before implementation.
- `source_of_truth/agents/04b-feature-implementer.agent.md` treats plan claims as hypotheses but has no required mid-phase replan gate.
- `source_of_truth/agents/04c-feature-review-and-fix.agent.md` reviews and fixes each implemented feature.
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

## Design implications

1. The source schema needs an abstract `model_tier` field.
2. The central routing file needs a canonical model field and optional canonical effort field.
3. Each renderer needs a harness-specific adapter instead of copying one model field blindly.
4. OpenCode likely needs one generated child definition per tier.
5. The session preflight needs a resolved-route table with requested model, override, actual route when observable, and status.
6. The schedule and run record need to preserve model status alongside feature status.
7. Tests must assert routing shape and disclosure behavior without hardcoding provider availability.

## Stale-plan scenario

Initial research may place a feature in wave five because its expected files do not conflict with the initial wave-one and wave-three plans. If those earlier waves change the same files or their APIs, the wave-five plan becomes stale.

The merged flow prevents this by withholding expansion documents for wave five, recording changed files after every earlier wave, revalidating wave five and its downstream dependents, and recomputing the schedule before wave five starts.

## Verification questions for implementation

- Which supported model identifier format is stable enough for each harness?
- Which harnesses can report the model actually used by a child at runtime?
- What exact fallback does each harness apply when a configured model is unavailable?
- Which existing external references invoke agents 03 and 04 by name?
- Can the current manifest path remain stable while its semantics change from static output to living schedule?

These questions do not reopen the phase decisions. They define implementation checks required before the phase can claim exact routing or migration completeness.
