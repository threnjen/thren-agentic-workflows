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

## TL;DR

<ONE_PLAIN_SENTENCE>: is this change ready to open as a PR, and if not, what
should the author look at first? Write it the way you would say it to the
author out loud — no jargon, no severity codes. For example: "Looks ready to
open — just double-check the two small things below" or "Not ready yet — one
change could break sign-in for existing users."

## Verdict

**<GO / GO WITH CONDITIONS / NO-GO>**

<ONE_PARAGRAPH_RATIONALE_IN_PLAIN_LANGUAGE>

## Things to Look At Before Opening

Most important first. Each row says, in plain words, what to check or fix —
the evidence and severity are there to back it up, not to lead.

| # | What to check or fix | Why it matters | Where | How serious |
|---:|---|---|---|---|
| 1 | <PLAIN_LANGUAGE_ACTION> | <PLAIN_WHY> | <PATH:LINE> | <CRITICAL/HIGH/MEDIUM/LOW> |

## Review Metadata

For the author's local record only — this section is **not** posted to the PR.

- **Review date:** <YYYY-MM-DD>
- **Base commit:** <BASE_SHA>
- **Head commit:** <HEAD_SHA>
- **Report root:** <REPORT_ROOT>

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

The TL;DR always comes first and is written in plain language for the author.
The "Things to Look At Before Opening" list is severity-ordered under the hood,
but each row leads with the plain-language action, not the severity code. The
Checks Not Run section must name every missing evaluator or check. If coverage
is incomplete, the report must state that limitation and use an outcome below GO
even when no blocker was found; missing evidence is never an implicit clean
result.

The Review Metadata section is for the author's local record and is never
included when the report is posted to a pull request. A posted or truncated view
keeps the TL;DR, Verdict, Things to Look At Before Opening, and Checks Not Run.
