# Project Roadmap: github-agents-source-of-truth

## Vision

A personal agentic evaluation framework that benchmarks harness+model combinations against real workflows, providing data-driven signal for comparing Claude Code, GitHub Copilot, OpenCode, and other agents on actual project tasks.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Eval Infrastructure Foundation | Planned | None | Medium | Instrument the pipeline with failure-ledger capture, commit checkpoints, hook template, and the 05 Eval - Grader agent |
| 02 | Codex Platform Bootstrap | Complete | Phase 01 | Medium | Define the repository-owned `codex/` source layout, document Codex-native instructions/custom agents/skills, cover macOS install paths, capture the porting strategy from the `.github/` source of truth, and validate a pilot trio (one instruction slice, one custom agent, one skill) against explicit exit criteria before any full Codex parity effort begins |

## Constraints & Non-Goals

- Rubrics, acceptance suites, task briefs, and clarification banks are per-project artifacts — they are not produced by this pipeline
- The framework is a personal benchmark, not a universal intelligence score
- No CI/CD integration or automated grader invocation in Phase 01

## Architecture Notes

- GitHub Copilot remains the master source of truth in `.github/`; derived platform surfaces must stay aligned with that source
- Existing derived agent directories must stay in sync: `.github/agents/` (master), `opencode/agents/`, `claude/agents/`
- Codex introduces a fourth platform surface with a different model: repository-owned source material lives under `codex/`, while runtime installation targets global AGENTS guidance, TOML custom agents, and directory-based skills rather than a direct `.github/instructions/` equivalent
- Ledger data lives in the target project repo under `eval/runs/` (gitignored)
- Hook template and grader agent live here in `github-agents-source-of-truth`
- Two-file ledger design: `ledger-commits.jsonl` (hook-written, raw timeline) + `ledger-events.jsonl` (agent-written, semantic events)
