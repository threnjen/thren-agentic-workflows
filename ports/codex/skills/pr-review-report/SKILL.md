---
name: pr-review-report
description: "Template for the PR Review go/no-go readiness report, the canonical hand-off for a review scoped to the diff between a base commit and a head commit. Use when: writing or reviewing a PR Review report."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# PR Review Report Templates

Use these templates for the structured reports consumed by the PR Review
evaluator family. Load `pr-review-conventions` first for scope, severity,
report-root, and incomplete-run rules. Preserve the placeholder tokens until the
corresponding values are known.

## Output Rules

- Write reports under `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`.
- Use the canonical filenames in each template below.
- Cite concrete evidence paths and line numbers when available.
- Use `Not run` only with a reason and an owner or next action.
- Keep the return message to the invoking agent within the conventions skill's
  10-line limit; the report is the complete record.

## 1. Go/No-Go Readiness Report

Write to `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/readiness-report.md`.

```markdown
# PR Readiness Report — <BASE_SHA_SHORT>..<HEAD_SHA_SHORT>

## Review Metadata

- **Review date:** <YYYY-MM-DD>
- **Base commit:** <BASE_SHA>
- **Head commit:** <HEAD_SHA>
- **Report root:** <REPORT_ROOT>

## Verdict

**<GO / GO WITH CONDITIONS / NO-GO>**

<ONE_PARAGRAPH_RATIONALE>

## Blocking List

List blockers in descending severity: Critical, High, Medium, Low.

| Priority | Severity | Blocker / condition | Evidence | Owner / action |
|---:|---|---|---|---|
| 1 | <CRITICAL/HIGH/MEDIUM/LOW> | <FINDING> | <PATH:LINE> | <ACTION> |

## Checks Not Run

This section is required even when the list is empty.

| Evaluator or check | Expected evidence | Reason not run | Verdict impact |
|---|---|---|---|
| <NAME> | <PATH> | <CONCRETE_REASON_OR_NONE> | <IMPACT> |

## Coverage and Evidence

Evaluator reports are required evidence. Pipeline artifacts are optional
enrichment: when one is absent, record it as `Not available` here rather than
omitting the row — the review still concludes on the diff alone, but its
coverage limitation is stated.

| Evidence set | Path | Status |
|---|---|---|
| Change narrative | <PATH> | Complete / Incomplete / Not run |
| Evaluator reports | <PATHS> | Complete / Incomplete |
| Pipeline artifacts | <PATHS_OR_NONE> | Available / Not available |

## Required Follow-up

1. <ACTION_OR_NONE>

## Verdict Rules Applied

- GO requires every required evaluator and check to be complete.
- Any missing or incomplete required check prevents GO.
- An unavailable optional artifact does not prevent GO, but must be named above.
- <ADDITIONAL_REVIEW_OR_SECURITY_RULE>
```

The blocking list is severity-ordered, and the Checks Not Run section must name
every missing evaluator or check. If coverage is incomplete, the report must
state that limitation and use an outcome below GO even when no blocker was
found; missing evidence is never an implicit clean result.
