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
| `rubrics/` | Scoring rubrics. `phase-eval-infrastructure-foundation.example.yaml` matched commits by literal prefix through `expected_commit_prefix` |
| `EVAL_SYSTEM_USAGE.md` | Operator guide for the run scoring system — run directories, rubric schema, and the grading workflow |

## Why they were retired

The grader needed running instrumentation to produce its inputs: the post-commit hook had
to be symlinked into every target repo, `02 Phase - Refiner` carried the install steps, and
`04b`, `04c`, and `Debugger` each carried a ledger-annotation section fed by an always-on
`remediation-ledger-contract` instruction. That contract matched every `.py`, `.ts`, `.js`,
and `.cs` file, so it loaded on nearly every coding task. The benchmarking value did not
justify the standing context cost.

`eval-feature-decomposition` produced no artifacts and its Step 4 still pointed at the
pre-restructure `.github/agents/` layout, so it could no longer locate its own inputs.

The rubrics and the usage guide were retained live at first, on the theory that the
scoring inputs might outlive the graders. They did not. Nothing under `source_of_truth/`
referenced either one, and their only remaining tie to a live agent was the `eval:` commit
literals that `03 Phase - Execute` emitted so `expected_commit_prefix` could match them.
Both are now archived here, so the run scoring system is retired end to end.

`eval/runs/` stays where it is. It is gitignored, so past run output is local-only and was
never committed, and `.gitignore:19` is load-bearing — see `tests/test_eval_grader_retirement.py`.

## Reactivating

Restoring the agents and skills to `source_of_truth/` is not sufficient — the grader reads
ledger files that nothing writes any more, and the rubrics here match commit prefixes that
no agent emits any more. A revival needs the commit scheme rebuilt alongside them. A revival also needs the hook install steps and
the per-agent ledger sections rebuilt, and `tests/test_eval_grader_retirement.py` removed.
Prefer rebuilding the instrumentation as something opt-in per run rather than restoring the
always-on instruction.

`eval-feature-decomposition` additionally needs its Step 4 paths repointed from
`.github/agents/` and `.github/skills/` to `source_of_truth/`.
