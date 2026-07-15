# Project Learnings

## Keep Runtime Identity Out Of Retained Eval Artifacts

**Problem**
Retained eval artifacts can leak `harness` and `model` into ledgers or score history, which biases the grader and makes blind comparisons harder.

**Root cause**
The evaluation contract treated runtime identity as part of the grading evidence instead of keeping it separate from the retained artifacts.

**Fix**
Do not write runtime identity into `ledger-events.jsonl`, score history, rubric templates, or other retained grading artifacts. If comparison bookkeeping still needs harness/model, keep it outside those artifacts.

**Watch for**
Any ledger schema, run template, or report contract that reintroduces `harness`, `model`, or similar runtime identity fields into retained evaluation evidence.