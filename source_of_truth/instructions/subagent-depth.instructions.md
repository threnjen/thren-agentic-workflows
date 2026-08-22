---
description: "One-level delegation limit for every root agent that can spawn children. Audience is DERIVED for the numbered pipeline: `0?-*.agent.md` matches the four pipeline roots (01, 02, 04-phase-execute, 05-pr-review) and not their `0Na-` subagents, so a new pipeline root inherits it automatically. The non-numbered roots have no filename family and stay enumerated."
applyTo: "source_of_truth/agents/0?-*.agent.md,**/05-pr-review.agent.md,**/auditor.agent.md,**/delta-auditor.agent.md,**/client-deliverable.agent.md,**/debugger.agent.md,**/instructions-manager.agent.md,**/qa-bootstrap.agent.md,**/single-feature-agent.agent.md,**/test-orchestrator.agent.md"
---

# Subagent Delegation Depth

Delegation depth is one. Only the user-invocable root orchestrator may spawn
agents. Child agents never spawn agents. When work requires fan-out, the root
spawns sibling agents and coordinates them through exclusive artifact ownership
and compact returns.
