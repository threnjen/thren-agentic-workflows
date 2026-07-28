---
description: "One-level delegation limit for every root agent that can spawn children."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/03-feature-decomposer.agent.md,**/04-phase-execute.agent.md,**/05-pr-review.agent.md,**/auditor.md,**/delta-auditor.md,**/client-deliverable.agent.md,**/debugger.agent.md,**/instructions-manager.agent.md,**/qa-bootstrap.agent.md,**/single-feature-agent.agent.md,**/test-orchestrator.agent.md"
---

# Subagent Delegation Depth

Delegation depth is one. Only the user-invocable root orchestrator may spawn
agents. Child agents never spawn agents. When work requires fan-out, the root
spawns sibling agents and coordinates them through exclusive artifact ownership
and compact returns.
