# Phase 03 Discovery Context

Context gathered while refining Phase 03, beyond what the code itself states.

## Reported symptoms

The maintainer reports that `03 Phase - Execute` stalls during remediation on the first
feature and does not reach the second. A phase that completes takes about twenty-four hours.
The pipeline itself reported to the maintainer that repeated review cycles produce findings
of increasing granularity rather than new defects.

## Diagnosis reached during refinement

A reviewer's exit condition is having written a report. That condition is satisfiable at any
level of detail, so nothing bounds how many findings a review produces. Four prior fixes —
the Finding Consolidator, the Finding Validator, the supported-path matrix, and immutable
per-cycle review directories — each filtered findings downstream of production and each added
an agent to the critical path. None bounded production.

Plan conformance review terminates because acceptance criteria are a finite list. Plan-blind
observation has no completion state. This is why `03c` rather than `03l` takes the single
per-feature review-and-fix slot.

## Decisions settled with the maintainer

1. The reviewer chorus moves from per-feature to phase close and runs once.
2. One per-feature review-and-fix agent, derived from `03c`, with `edit` restored. One round,
   one opportunity. Tests must always pass.
3. One phase-close repair round off the combined findings. The audits do not re-run after it.
4. The Finding Consolidator and Finding Validator survive, running once per phase. The
   Consolidator reads all nine reports so overlapping lanes cannot inflate the count. The
   Validator reads only the four repair-eligible lanes.
5. The chorus roster is nine agents in three classes — four repair-eligible, two conditional,
   three advisory only.
6. QA runs after the phase-close repair, so it measures the code Prod Code Review evaluates.

## Deferred

The density of the orchestrator's user-facing reporting language. The maintainer chose to
defer it on the expectation that a simpler pipeline carries fewer state tokens to leak.
Measure it after this phase rather than guessing now.

## Removed from the pipeline

Per-feature reviewer committee, per-feature consolidation and validation, review-cycle
directories, the two-round fix loop, the plan rewrite, the rebuild, the post-rebuild review,
and the second full audit pass.

## Sources

All context came from the repository and from the maintainer directly. No web research was
performed and no external projects were consulted. The `code-review-graph` MCP server failed
to connect during this session, so exploration used file reads and grep.
