---
name: explore-codebase
description: Navigate and understand codebase structure using the knowledge graph
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

## Explore Codebase

Use the code-review-graph MCP tools to explore and understand the codebase.

### Steps

1. Run `list_graph_stats` to see overall codebase metrics.
2. Run `get_architecture_overview` for high-level community structure.
3. Run `list_communities` to find major modules. Run `get_community` for details.
4. Run `semantic_search_nodes` to find specific functions or classes.
5. Run `query_graph` with patterns like `callers_of`, `callees_of`, `imports_of` to trace relationships.
6. Run `list_flows`. Run `get_flow` to understand execution paths.

### Tips

- Start with broad statistics and architecture. Then narrow down to specific areas.
- Run `children_of` on a file to see all its functions and classes.
- Run `find_large_functions` to identify complex code.

## Token Efficiency Rules
- ALWAYS start with `get_minimal_context(task="<your task>")` before any other graph tool.
- Use `detail_level="minimal"` on all calls. Only escalate to "standard" when minimal is insufficient.
- Target: complete any review, debug, or refactor task in ≤5 tool calls and ≤800 total output tokens.
