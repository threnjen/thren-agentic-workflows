---
name: review-changes
description: Perform a structured code review using change detection and impact
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

## Review Changes

Perform a risk-aware code review with the knowledge graph.

### Steps

1. Run `detect_changes` to score change risk.
2. Run `get_affected_flows` to find execution paths that the change affects.
3. For each high-risk function, run `query_graph` with pattern="tests_for" to check test coverage.
4. Run `get_impact_radius` to identify the blast radius.
5. For any untested changes, suggest specific test cases.

### Output Format

Provide findings grouped by risk level (high/medium/low) with:
- What changed and why it matters
- Test coverage status
- Suggested improvements
- Overall merge recommendation

## Token Efficiency Rules
- ALWAYS start with `get_minimal_context(task="<your task>")` before any other graph tool.
- Use `detail_level="minimal"` on all calls. Only escalate to "standard" when minimal is insufficient.
- Complete each review, debug, or refactor task in ≤5 tool calls and ≤800 total output tokens.
