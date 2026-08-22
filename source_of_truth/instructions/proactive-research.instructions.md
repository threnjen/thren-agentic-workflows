---
description: "Requires agents to spawn @Web Researcher for unfamiliar technologies, errors, or APIs instead of asking the user. Audience is DERIVED for pipeline stages 01-02; `debugger` is enumerated because it sits outside the numbered pipeline."
applyTo: "source_of_truth/agents/0[12]-*.agent.md,**/debugger.agent.md"
---

# Proactive Research Over Asking the User

When you encounter an unfamiliar technology, API, service, pattern, constraint, error, or version-specific issue, **spawn `@Web Researcher` immediately** rather than asking the user to explain it. The user expects you to look things up yourself. Only ask the user for information that is inherently project-specific and cannot be found online (e.g., business priorities, internal team decisions, undocumented requirements). Default to researching first, then presenting what you found alongside any remaining questions that truly require the user's input.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: proactive-research."* Then proceed normally.
