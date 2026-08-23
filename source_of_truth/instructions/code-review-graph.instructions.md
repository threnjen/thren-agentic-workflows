---
description: "Requires agents to query the code-review-graph knowledge graph before scanning files with Grep, Glob, or Read. Baseline-only: it ships in the user-global instructions file for every harness, so it carries no applyTo roster and is never inlined into an agent."
baseline: true
---

# Query The Code Graph Before Scanning Files

When a repository has a code-review-graph knowledge graph, query it before you reach for Grep, Glob, or Read. The graph answers in fewer tokens and returns structural context that file scanning cannot: callers, dependents, and test coverage.

A repository has a graph when the `code-review-graph` MCP tools are available and report a non-zero node count. Fall back to Grep, Glob, and Read when the graph does not cover what you need.

## Which Tool Answers Which Question

| Question | Tool |
|---|---|
| What changed, and how risky is it? | `detect_changes` |
| What source do I need to review this? | `get_review_context` |
| What does this change break? | `get_impact_radius` |
| Which execution paths does it touch? | `get_affected_flows` |
| Who calls this, and what does it import? | `query_graph` |
| Where is the function or class named X? | `semantic_search_nodes` |
| How is this codebase laid out? | `get_architecture_overview` |
| What is dead, and what does renaming cost? | `refactor_tool` |

## Reviewing Changes

1. Call `detect_changes` for a risk-scored summary of the change.
2. Call `get_affected_flows` to see which execution paths it reaches.
3. Call `query_graph` with `pattern="tests_for"` to check coverage.

Read source files only for what these calls leave unresolved. The graph updates on file changes, so a stale result means the graph is wrong, not that your query was.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: code-review-graph."* Then proceed normally.
