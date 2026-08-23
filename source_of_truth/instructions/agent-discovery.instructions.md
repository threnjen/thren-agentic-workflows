---
description: "Where an agent or skill definition lives when the user names one. Baseline-only: it ships in the user-global instructions file for every harness, so it carries no applyTo roster and is never inlined into an agent."
baseline: true
---

# Custom Agent and Skill Discovery

When the user asks {harness_title} to act as a named agent, resolve its definition from:

{agent_paths}

When the user explicitly names a skill that is not already available in the
session skill catalog, look for it in:

{skill_paths}

Read the selected agent or skill instructions completely before beginning work.
Do not spawn an agent merely because the user asks {harness_title} to act in that role.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: agent-discovery."* Then proceed normally.
