# Baseline Instructions

Instructions deployed into every harness's user-global instructions file
(`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and the rest). List one instruction
name per bullet. `deploy_agents.py` reads each named
`source_of_truth/instructions/<name>.instructions.md`, strips its frontmatter and
its Load Canary section, and splices the body under a `<!-- <name> -->` sentinel.

Every name listed here must exist as an instruction file carrying `baseline: true`.
Removing a name stops the deploy from rewriting its block. To delete a block that
past deploys already wrote, also add the name to `RETIRED_BASELINE_SECTIONS`.

- agent-discovery
- challenge-assumptions
- code-change-strategy
- code-review-graph
- codebase-context-bootstrap
- comms-protocol
- language-standards
- learnings-bootstrap
- output-verbosity-policy
- proactive-research
- prose-standards
- question-hygiene
