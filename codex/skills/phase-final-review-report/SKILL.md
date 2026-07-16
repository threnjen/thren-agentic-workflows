---
name: phase-final-review-report
description: "Templates for the four Phase Final Review hand-off reports: master QA, security rollup, AC regression, and readiness. Use when: writing or reviewing a 05x Phase Final Review report."
---
<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
# Phase Final Review Report Templates

Use these templates for the structured reports consumed by the Phase Final
Review evaluator family. Load `phase-final-review-conventions` first for scope,
severity, report-root, and incomplete-run rules. Preserve the placeholder
tokens until the corresponding values are known.

## Output Rules

- Write reports for `<PHASE_0N>` under
  `dev/phase-final-review/PHASE_0N/`.
- Use the canonical filenames in each template below.
- Cite concrete evidence paths and line numbers when available.
- Use `Not run` only with a reason and an owner or next action.
- Keep the return message to the invoking agent within the conventions skill's
  10-line limit; the report is the complete record.

## 1. Master QA Document

Write to `dev/phase-final-review/PHASE_0N/master-qa.md`.

```markdown
# Master QA — <PHASE_0N>

## Review Metadata

- **Review date:** <YYYY-MM-DD>
- **Phase:** <PHASE_0N>
- **Source subphases:** <SUBPHASE_PATHS>
- **Evaluator:** <AGENT_NAME>

## Scope and Source Documents

| Subphase | QA source | Coverage map | QA analysis | Security source |
|---|---|---|---|---|
| <SUBPHASE> | <PATH> | <PATH> | <PATH> | <PATH> |

## Consolidated Walkthrough

| ID | Subphase | Check | Preconditions / action | Expected result | Evidence | Status |
|---|---|---|---|---|---|---|
| QA-<NN> | <SUBPHASE> | <CHECK> | <TEXT> | <TEXT> | <PATH:LINE> | PASS / FAIL / NOT RUN |

## Checks Not Run

| Check | Subphase | Reason | Required follow-up |
|---|---|---|---|
| <CHECK_ID> | <SUBPHASE> | <CONCRETE_REASON> | <ACTION_OR_NONE> |

## Findings and Follow-up

| Severity | Finding | Evidence | Required action |
|---|---|---|---|
| <CRITICAL/HIGH/MEDIUM/LOW> | <FINDING> | <PATH:LINE> | <ACTION> |

## QA Conclusion

<CONCLUSION_WITH_COVERAGE_LIMITATIONS>
```

Merge equivalent checks, preserve a source reference for each retained check,
and do not count an unexecuted check as passing.

## 2. Security Rollup

Write to `dev/phase-final-review/PHASE_0N/security-rollup.md`.

Classify each source finding as:

- **Fixed** — the final review evidence shows the finding no longer reproduces
  and the relevant control is present.
- **Persisting** — the finding remains reproducible or the control remains
  insufficient in the final state.
- **Reintroduced** — the finding was previously resolved in the reviewed
  history but is present again in the final state.

```markdown
# Security Rollup — <PHASE_0N>

## Scan Metadata

- **Review date:** <YYYY-MM-DD>
- **Phase:** <PHASE_0N>
- **Subphase scans:** <PATHS>
- **Final security review:** <PATH_OR_NOT_RUN>

## Verdict

**<GO / GO WITH CONDITIONS / NO-GO>**

<ONE_PARAGRAPH_SECURITY_CONCLUSION>

## Finding Classification

| ID | Severity | Classification | Source subphase | Final evidence | Recommendation |
|---|---|---|---|---|---|
| <FINDING_ID> | <CRITICAL/HIGH/MEDIUM/LOW> | Fixed / Persisting / Reintroduced | <SUBPHASE> | <PATH:LINE> | <ACTION> |

## Findings Not Reproduced

| ID | Source evidence | Reproduction status | Remaining uncertainty |
|---|---|---|---|
| <FINDING_ID> | <PATH:LINE> | <STATUS> | <TEXT> |

## Checks Not Run

| Check | Reason | Impact on verdict |
|---|---|---|
| <CHECK> | <CONCRETE_REASON> | <IMPACT> |

## Release Conditions

1. <CONDITION_OR_NONE>
```

Order findings by severity, then by finding ID. A source finding without final
evidence remains unresolved; do not label it Fixed solely because a scan was
not run.

## 3. Acceptance-Criteria Regression Matrix

Write to `dev/phase-final-review/PHASE_0N/ac-regression-matrix.md`.

```markdown
# AC Regression Matrix — <PHASE_0N>

## Review Metadata

- **Review date:** <YYYY-MM-DD>
- **Baseline:** <COMMIT_OR_NOT_AVAILABLE>
- **Final revision:** <COMMIT_OR_REFERENCE>
- **Subphases covered:** <SUBPHASES>

## Acceptance Criteria

| Subphase | AC | Criterion | Final verification | Evidence | Status | Severity / blocker |
|---|---|---|---|---|---|---|
| <SUBPHASE> | <AC_ID> | <CRITERION> | <VERIFICATION> | <PATH:LINE> | PASS / FAIL / NOT RUN / INCONCLUSIVE | <LEVEL_OR_NONE> |

## Checks Not Run

| Subphase | AC or check | Reason | Required follow-up |
|---|---|---|---|
| <SUBPHASE> | <AC_ID_OR_CHECK> | <CONCRETE_REASON> | <ACTION> |

## Regression Summary

- **Passed:** <COUNT>
- **Failed:** <COUNT>
- **Not run:** <COUNT>
- **Inconclusive:** <COUNT>
- **Blocking regressions:** <COUNT>

<SUMMARY_AND_LIMITATIONS>
```

Include every acceptance criterion from every discovered subphase. A criterion
cannot be marked PASS when its evidence is absent, stale, or only describes an
earlier revision.

## 4. Go/No-Go Readiness Report

Write to `dev/phase-final-review/PHASE_0N/readiness-report.md`.

```markdown
# Phase Readiness Report — <PHASE_0N>

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

| Evidence set | Path | Status |
|---|---|---|
| Master QA | <PATH> | Complete / Incomplete |
| Security rollup | <PATH> | Complete / Incomplete |
| AC regression matrix | <PATH> | Complete / Incomplete |
| Evaluator reports | <PATHS> | Complete / Incomplete |

## Required Follow-up

1. <ACTION_OR_NONE>

## Verdict Rules Applied

- GO requires every required evaluator and check to be complete.
- Any missing or incomplete required check prevents GO.
- <ADDITIONAL_PHASE_OR_SECURITY_RULE>
```

The blocking list is severity-ordered, and the Checks Not Run section must name
every missing evaluator or check. If coverage is incomplete, the report must
state that limitation and use an outcome below GO even when no blocker was
found; missing evidence is never an implicit clean result.
