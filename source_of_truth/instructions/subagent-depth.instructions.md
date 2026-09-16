---
description: "One-level delegation limit for every root agent that can spawn children. The `0?-*.agent.md` pattern matches the four numbered roots and excludes their lettered children. Non-numbered roots remain enumerated."
applyTo: "source_of_truth/agents/0?-*.agent.md,**/auditor.agent.md,**/delta-auditor.agent.md,**/client-deliverable.agent.md,**/debugger.agent.md,**/instructions-manager.agent.md,**/qa-bootstrap.agent.md,**/single-feature-agent.agent.md,**/test-orchestrator.agent.md"
---

# Subagent Delegation Depth

Delegation has one level. Only the user-invocable root orchestrator may spawn agents. Child agents never spawn agents. When work needs parallel execution, the root orchestrator spawns sibling agents and coordinates them through exclusive artifact ownership and compact returns.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: subagent-depth."* Then proceed normally.
