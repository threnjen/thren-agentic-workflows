# Project Roadmap: github-agents-source-of-truth

## Vision

A personal agentic evaluation framework that benchmarks harness+model combinations against real workflows, providing data-driven signal for comparing Claude Code, GitHub Copilot, OpenCode, and other agents on actual project tasks.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Eval Infrastructure Foundation | Planned | None | Medium | Instrument the pipeline with failure-ledger capture, commit checkpoints, hook template, and the 05 Eval - Grader agent |

## Constraints & Non-Goals

- Rubrics, acceptance suites, task briefs, and clarification banks are per-project artifacts — they are not produced by this pipeline
- The framework is a personal benchmark, not a universal intelligence score
- No CI/CD integration or automated grader invocation in Phase 01

## Architecture Notes

- Three agent directories must stay in sync: `.github/agents/` (master), `opencode/agents/`, `claude/agents/`
- Ledger data lives in the target project repo under `eval/runs/` (gitignored)
- Hook template and grader agent live here in `github-agents-source-of-truth`
- Two-file ledger design: `ledger-commits.jsonl` (hook-written, raw timeline) + `ledger-events.jsonl` (agent-written, semantic events)
