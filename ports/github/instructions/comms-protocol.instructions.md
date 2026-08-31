---
description: "The generated AGENT-RESULT contract shared by Crosswire and workflows."
baseline: true
---
<!-- Generated from source_of_truth/agents. Do not edit manually. -->
# AGENT-RESULT contract

Contract version: 1

End each turn with exactly one block using these delimiters:
- Opening: `<!-- AGENT-RESULT v{version} -->`
- Closing: `<!-- /AGENT-RESULT -->`

The block contains these required fields:

```text
<!-- AGENT-RESULT v1 -->
status: <one of: succeeded, failed, blocked>
summary: <plain text, maximum 4,000 characters>
artifacts:
- path: <text>
  description: <text>
<!-- /AGENT-RESULT -->
```

Field constraints:
- `status`: The outcome a parent can branch on. Allowed values: succeeded, failed, blocked. Maximum 32 characters.
- `summary`: A plain-text description of the turn outcome. Single-line text. Maximum 4,000 characters.
- `artifacts`: An ordered list of files or other outputs produced by the turn. Ordered list. Maximum 100 entries.

Keep `artifacts` in order. Use an empty list when the turn produced no artifacts.
Each artifact entry must contain these fields exactly once: `path`, `description`.
- `path`: A workspace-relative path or explicit external reference. Single-line text. Maximum 1,024 characters.
- `description`: A plain-text description of the artifact. Single-line text. Maximum 2,000 characters.
