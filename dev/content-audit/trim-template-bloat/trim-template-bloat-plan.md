# Plan: Trim Template Bloat

Reduce token usage in Markdown templates by removing HTML comments, example data rows, and self-evident descriptions.

## Acceptance Criteria

- AC1: QA Writer template HTML comments reduced to one-word hints or removed
- AC2: Implementer template example rows removed (headers + column definitions retained)
- AC3: Reviewer template example rows removed
- AC4: QA Writer template self-evident section descriptions trimmed

## Non-Goals

- Do not remove template structure (headers, table headers)
- Do not remove column definitions that clarify expected content
