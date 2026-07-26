# Deprecated eval assets

Parked here, outside `source_of_truth/`, so propagation ignores them and they cost no
runtime context. Nothing in this directory is deployed to any harness.

## What is here

| Path | What it was |
|---|---|
| `agents/eval-grader.agent.md` | Orchestrator that scored a completed `phase/*` run by diffing clean-base -> golden and clean-base -> evaluated branches against a rubric YAML |
| `agents/eval-metric-grader.agent.md` | Hidden subagent, scored one comparative metric per invocation |
| `agents/eval-score-recorder.agent.md` | Hidden subagent, resolved harness/model identity and appended one row to the score history |
| `agents/eval-feature-decomposition.agent.md` | Standalone benchmark comparing a golden-path decomposition against one the Feature Decomposer produced |
| `skills/eval-score-table-output/` | Score-table format for the grader |
| `skills/eval-feature-decomposition-report/` | Report template for the decomposition benchmark |
| `hooks/post-commit.sh` | Git hook that appended `ledger-commits.jsonl` on `phase/*` branches |
| `agentic-evaluator-plan.md` | The original design plan for the whole evaluation framework |

## Why they were retired

The grader needed running instrumentation to produce its inputs: the post-commit hook had
to be symlinked into every target repo, `02 Phase - Refiner` carried the install steps, and
`04b`, `04c`, and `Debugger` each carried a ledger-annotation section fed by an always-on
`remediation-ledger-contract` instruction. That contract matched every `.py`, `.ts`, `.js`,
and `.cs` file, so it loaded on nearly every coding task. The benchmarking value did not
justify the standing context cost.

`eval-feature-decomposition` produced no artifacts and its Step 4 still pointed at the
pre-restructure `.github/agents/` layout, so it could no longer locate its own inputs.

Retained live: `eval/rubrics/` and `eval/EVAL_SYSTEM_USAGE.md`. `eval/runs/` is
gitignored, so past run output is local-only and was never committed.

## Reactivating

Restoring the agents and skills to `source_of_truth/` is not sufficient — the grader reads
ledger files that nothing writes any more. A revival also needs the hook install steps and
the per-agent ledger sections rebuilt, and `tests/test_eval_grader_retirement.py` removed.
Prefer rebuilding the instrumentation as something opt-in per run rather than restoring the
always-on instruction.

`eval-feature-decomposition` additionally needs its Step 4 paths repointed from
`.github/agents/` and `.github/skills/` to `source_of_truth/`.
