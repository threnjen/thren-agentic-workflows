---
name: agent-designator-router
description: "Use whenever the user mentions an agent with @agent-name, [@agent-name](subagent://agent-name), subagent://, or asks Codex to act as a named agent. Ensures Codex adopts the selected agent role/workflow before doing work."
---
<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
# Agent Designator Router

When the user message contains an agent designator such as:

- `@feature-decomposer`
- `[@feature-decomposer](subagent://feature-decomposer)`
- `subagent://feature-decomposer`

treat that as a request to operate under that agent's instructions.

## Required Behavior

1. Resolve the selected agent name.
2. Load the matching agent instructions from the local source of truth when available.
3. Adopt those instructions as the active workflow for this turn.
4. Do not spawn the same agent as a child just because it was tagged.
5. If the selected agent workflow says to spawn child agents, spawn only those distinct child agents.
6. Complete all mandatory output gates from the selected agent before final response.
7. If the agent instructions conflict with generic local skills, the selected agent workflow wins unless system/developer instructions say otherwise.

## Failure Guard

Before final response, ask:

- Did I act as the tagged agent rather than merely acknowledging it?
- Did I run every mandatory phase in the tagged agent workflow?
- Did I spawn required child agents?
- Did I produce every required artifact?
- Did I satisfy commit/manifest/validation gates if the agent requires them?

If any answer is no, continue working.