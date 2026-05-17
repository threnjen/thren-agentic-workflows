# Eval Grader Score History

Persistent additive history for branch-comparison grading runs.

Rules:
- Scores are normalized to `1-10`, where `10` is best.
- The golden path is the reference implementation and is treated as scoring `10` on every axis.
- Append rows only. Do not delete, rewrite, reorder, or deduplicate prior entries.
- Use `NHR` for any axis that remained `[NEEDS_HUMAN_REVIEW]`.

| Timestamp | Phase | Clean Base | Golden Path | Evaluated Branch | Harness | Model | Equivalence | Maintainability | Bug Risk | Edge Cases | Turns | Initial Patch Tests | Review Quality | Footprint | Mean Time/Task | Overall Verdict | Report Path | Notes |
|-----------|-------|------------|-------------|------------------|---------|-------|-------------|-----------------|----------|------------|-------|---------------------|----------------|-----------|----------------|-----------------|-------------|-------|
