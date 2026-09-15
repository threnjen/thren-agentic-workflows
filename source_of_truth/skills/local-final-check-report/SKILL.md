---
name: local-final-check-report
description: "Templates for local final-check evaluator, readiness, and repair reports."
---

# Local Final Check Report Templates

Load `local-final-check-conventions` first. Preserve unknown placeholders until
their values exist.

## Evaluator Report

```markdown
# <CHECK> — <BASE_SHORT>..<HEAD_SHORT>

## Result
<COMPLETE / INCOMPLETE / NOT RUN>

## Evidence
| Evidence | Path or revision | Status |
|---|---|---|

## Findings
| ID | Severity | Location | Evidence | Required action | Repair eligible |
|---|---|---|---|---|---|

## Checks Not Run
| Check | Reason | Follow-up |
|---|---|---|

## Conclusion
<CONCISE_CONCLUSION>
```

## Readiness Report

Write `readiness-report.md`.

```markdown
# Local Readiness Report — <BASE_SHORT>..<HEAD_SHORT>

## TL;DR
<PLAIN_LANGUAGE_RESULT>

## Verdict
**<GO / GO WITH CONDITIONS / NO-GO>**

<PLAIN_LANGUAGE_RATIONALE>

## Things to Address
| # | Action | Why | Location | Severity |
|---:|---|---|---|---|

## Checks Not Run
| Evaluator or check | Reason | Verdict impact |
|---|---|---|

## Evidence
| Evidence set | Path | Status |
|---|---|---|

## Repair Candidates
| ID | Class | Source finding | Location | Reason eligible |
|---|---|---|---|---|

## Required Follow-up
1. <ACTION_OR_NONE>
```

The repair-candidate class must be `security`, `outward-impact`, or
`changed-test-falsification`. Omit every other finding from that table. Preserve
the readiness report after writing it.

## Repair Report

Write `repair-report.md` without changing the readiness report.

```markdown
# Local Repair Report — <BASE_SHORT>..<PRE_REPAIR_HEAD_SHORT>

## Revisions and Tree State
- Base: <SHA>
- Pre-repair HEAD: <SHA>
- Post-repair HEAD: <SHA>
- Dirty before: <STATE>
- Dirty after: <STATE>

## Candidate Outcomes
| ID | Status | Evidence | Files changed | Remaining risk |
|---|---|---|---|---|

## Baseline Tests
| Command | Result | Evidence |
|---|---|---|

## Post-Repair Tests
| Command | Result | Evidence |
|---|---|---|

## Unresolved Risks
<RISKS_OR_NONE>
```
