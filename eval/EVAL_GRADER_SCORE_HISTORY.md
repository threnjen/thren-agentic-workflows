# Eval Grader Score History

Persistent additive history for branch-comparison grading runs.

Rules:
- Scores are normalized to `1-10`, where `10` is best.
- The golden path is the reference implementation and is treated as scoring `10` on every axis.
- Append rows only. Do not delete, rewrite, reorder, or deduplicate prior entries.
- Use `NHR` for any axis that remained `[NEEDS_HUMAN_REVIEW]`.

Use this section for runs graded after the metric model split between parallel metric subagents and parent-derived execution metrics. Legacy rows above remain unchanged.

| Timestamp | Phase | Harness/Model | Evaluated Branch | Equivalence | Clarity | Coherence | Robustness | Bug Risk | Scope Discipline | Footprint | Turns | Initial Patch Tests | Review Quality | Mean Time/Task | Overall Verdict | Report Path | Notes |
|-----------|-------|-------------|------------------|-------------|---------|-----------|------------|----------|------------------|-----------|-------|---------------------|----------------|----------------|-----------------|-------------|-------|
| 2026-05-19T02:00:00Z | phase-06e | opencode/deepseekv4pro | phase/06e-modeltest1 | 5 | 7 | 5 | 6 | 3 | 3 | 4 | 3 | NHR | 4 | 5 | FAIL | the-movies/eval/runs/phase-06e/score-report-modeltest1.md |...|
| 2026-05-18T15:30:39Z | phase-06e | codex/gpt-5.4-highpath | phase/06e-modeltest2 | 5 | 7 | 6 | 5 | 3 | 6 | 4 | 7 | 8 | 5 | 7 | PARTIAL | the-movies/eval/runs/phase-06e/score-report-20260518-153039.md |...|
| 2026-05-18T22:28:18Z | phase-06e | claude/opus-4-6 | phase/06e-modeltest3 | 3 | 8 | 6 | 4 | 3 | 4 | 5 | 5 | NHR | 4 | 7 | FAIL | the-movies/eval/runs/phase-06e/score-report-modeltest3.md |...|
| 2026-05-19T01:16:50Z | phase-06e | claude/sonnet-4-6 | phase/06e-modeltest4 | 7 | 8 | 8 | 4 | 4 | 7 | 6 | 6 | 5 | 6 | NHR | PARTIAL | the-movies-03/eval/runs/phase-06e/score-report-modeltest4.md |...|
| 2026-05-18T18:17:53Z | phase-06e | codex/gpt5.5-high | phase/06e-modeltest5 | 6 | 7 | 5 | 7 | 7 | 6 | 8 | 9 | NHR | 6 | 8 | PARTIAL | the-movies/eval/runs/phase-06e/score-report-modeltest5.md |...|
| 2026-05-19T15:36:59Z | phase-06e | opencode/deepseekv4flash | phase/06e-modeltest6 | 7 | 7 | 6 | 5 | 4 | 3 | 5 | 5 | NHR | 5 | 6 | PARTIAL | the-movies/eval/runs/phase-06e/score-report-modeltest6.md |...|
| 2026-05-19T15:30:00Z | phase-06e | opencode/qwen3.6 | phase/06e-modeltest7 | 7 | 8 | 8 | 6 | 5 | 8 | 7 | 5 | NHR | 6 | 7 | FAIL | the-movies/eval/runs/phase-06e/score-report-modeltest7.md |...|
| 2026-05-21T20:12:26Z | phase-06e | codex/gpt-5.4-high | phase/06e-modeltest2-v2 | 7 | 7 | 7 | 6 | 5 | 6 | 5 | 6 | NHR | 6 | NHR | PARTIAL | the-movies-03/eval/runs/phase-06e/score-report-modeltest2-v2.md |...|
| 2026-05-22T03:05:24Z | phase-06e | claude/opus-4-6 | phase/06e-modeltest3-v2 | 6 | 6 | 7 | 6 | 5 | 8 | 7 | 5 | NHR | 6 | 5 | PARTIAL | the-movies/eval/runs/phase-06e/score-report-modeltest3-v2.md |...|
| 2026-05-21T22:00:00Z | phase-06e | claude/sonnet-4-6 | phase/06e-modeltest4-v2 | 5 | 7 | 6 | 7 | 5 | 5 | 4 | 8 | NHR | 6 | NHR | FAIL | the-movies/eval/runs/phase-06e/score-report-modeltest4-v2.md |...|
| 2026-05-21T16:15:00Z | phase-06e | opencode/deepseekv4flash | phase/06e-modeltest6-v2 | 6 | 6 | 6 | 5 | 5 | 7 | 7 | 7 | NHR | 6 | 9 | PARTIAL | the-movies/eval/runs/phase-06e/score-report-modeltest6-v2.md |...|
| 2026-05-21T18:29:53Z | phase-06e | copilot/gpt-5.4-high | phase/06e-modeltest8 | 6 | 6 | 5 | 8 | 6 | 3 | 3 | 4 | NHR | 4 | NHR | FAIL | the-movies/eval/runs/phase-06e/score-report-modeltest8-v2.md |...|
| 2026-05-22T15:15:54Z | phase-06e | copilot/sonnet-4.6-high | phase/06e-modeltest9 | 4 | 5 | 4 | 5 | 4 | 3 | 4 | 6 | NHR | 4 | NHR | FAIL | the-movies/eval/runs/phase-06e/score-report-modeltest9-v2.md |...|
| 2026-05-22T00:00:00Z | phase-06e | claude/haiku-4.6-high | phase/06e-modeltest10 | 6 | 7 | 6 | 6 | 5 | 7 | 8 | 5 | NHR | 6 | NHR | PARTIAL | eval/runs/phase-06e/score-report-modeltest10.md |...|
