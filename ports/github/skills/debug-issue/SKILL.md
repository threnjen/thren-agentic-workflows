---
name: debug-issue
description: Systematically debug issues using graph-powered code navigation
---

## Debug Issue

Use the knowledge graph to trace and debug issues systematically.

### Steps

1. Use `semantic_search_nodes` to find code related to the issue.
2. Use `query_graph` with `callers_of` and `callees_of` to trace the sequence of calls.
3. Use `get_flow` to trace full execution paths through suspected code.
4. Use `detect_changes` to determine whether recent changes caused the issue.
5. Use `get_impact_radius` for suspected files to identify other affected code.

### Tips

- Check both callers and callees to understand the full context.
- Read affected flows to find the entry point that triggers the bug.
- Recent changes most often cause new issues.

## Token Efficiency Rules
- Always start with `get_minimal_context(task="<your task>")` before any other graph tool.
- Use `detail_level="minimal"` on all calls. Only escalate to "standard" when minimal is insufficient.
- Target: Complete each review, debug, or refactor task in ≤5 tool calls and ≤800 total output tokens.
