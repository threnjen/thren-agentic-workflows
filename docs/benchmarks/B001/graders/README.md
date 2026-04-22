# B001 Grader Guidance

This folder defines grading expectations for B001.

## Grading Modes

- deterministic: machine-checkable criteria
- rubric: evaluator-judged criteria using anchored rubrics
- hybrid: deterministic checks plus rubric scoring

## Deterministic Checks

Use where possible:

- required section presence
- output schema compliance
- policy or constraint violations
- required references to input files or artifacts

## Rubric Anchors

For quality-sensitive tasks, score each criterion from 0 to 5:

- 0: missing or incorrect
- 1: major gaps and low utility
- 2: partial response with serious omissions
- 3: acceptable baseline with minor omissions
- 4: strong and mostly complete
- 5: complete, precise, and decision-useful

## Required Rubric Criteria

At minimum include:

- correctness and factuality
- scope discipline
- edge-case coverage
- clarity and actionability
- compliance with constraints

## Human Audit Triggers

Require manual review if:

- candidate is in gray zone near gate thresholds
- high-severity compliance regressions appear
- major behavior changes are detected from prompt-style optimization
