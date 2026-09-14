---
description: "One-level delegation limit for every root agent that can spawn children. Audience is DERIVED for the numbered pipeline: `0?-*.agent.md` matches the four pipeline roots (01, 02, 03-phase-execute, 04-pr-review) and not their `0Na-` subagents, so a new pipeline root inherits it automatically. The non-numbered roots have no filename family and stay enumerated."
applyTo: "source_of_truth/agents/0?-*.agent.md,**/04-pr-review.agent.md,**/auditor.agent.md,**/delta-auditor.agent.md,**/client-deliverable.agent.md,**/debugger.agent.md,**/instructions-manager.agent.md,**/qa-bootstrap.agent.md,**/single-feature-agent.agent.md,**/test-orchestrator.agent.md"
---

# Subagent Delegation Depth

In-process fan-out MUST remain root-only at depth one. Only the user-invocable root orchestrator may create in-process children. Child agents MUST NOT use collaboration-tool fan-out or spawn in-process descendants. When work needs in-process fan-out, the root MUST coordinate sibling agents through exclusive artifact ownership and compact returns.

Board-mediated spawning MAY recurse through Crosswire's existing durable intake and watcher path. Crosswire records parentage, applies registry-driven enforcement, and bounds each chain with `SpawnConfig.max_depth`; a request beyond that bound receives `max_depth_exceeded` and persists `max_depth_refused`. Board-mediated children MUST retain intake, claim, parent identity, chain, recovery, reconciliation, and enforcement checks.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: subagent-depth."* Then proceed normally.
