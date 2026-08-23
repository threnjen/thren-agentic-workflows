---
description: "Where an agent or skill definition lives when the user names one. Baseline-only: it ships in the user-global instructions file for every harness, so it carries no applyTo roster and is never inlined into an agent."
baseline: true
---

# Agent and Skill Discovery

When the user asks {harness_title} to act as a named agent, look for its definition in:

{agent_paths}

When the user names a skill that is not already in the session catalog, look for it in:

{skill_paths}

Read the whole definition before you start work. Do not spawn a subagent merely because the user asked {harness_title} to act in that role.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: agent-discovery."* Then proceed normally.
