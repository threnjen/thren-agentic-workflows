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
7. A defect the per-feature reviewer cannot fix in its one round is recorded and carried to the
   phase-close chorus. The reviewer never blocks a feature on its own unrepaired finding.
8. `03c` changes in place rather than moving to a new identity. Seventeen files reference it,
   five of them instruction `applyTo` globs, and a silently non-matching glob is a recorded
   failure mode in this corpus. No agent is deleted by this phase.
9. The feature test gate is a baseline comparison, not absolute green. Phase 02 is recorded as
   shipping with eleven known test failures, so an absolute gate would stall every feature on
   failures it did not cause.

## Deferred

The density of the orchestrator's user-facing reporting language. The maintainer chose to
defer it on the expectation that a simpler pipeline carries fewer state tokens to leak.
Measure it after this phase rather than guessing now.

## Removed from the pipeline

Per-feature reviewer committee, per-feature consolidation and validation, review-cycle
directories, the two-round fix loop, the plan rewrite, the rebuild, the post-rebuild review,
and the second full audit pass.

## Environment finding

The checked-in virtualenv is stale. `.venv/bin/pytest` carries a shebang pointing at
`/Users/jennywadkins/github_repos/github-agents-source-of-truth/.venv/bin/python`, a path the
repository rename left behind, so the suite does not start. The eleven Phase 02 failures could
not be enumerated during refinement for that reason — eleven is the roadmap's number, not a
measurement. Rebuilding the environment is the first step of Feature 1.

## Sources

All context came from the repository and from the maintainer directly. No web research was
performed and no external projects were consulted. The `code-review-graph` MCP server failed
to connect during this session, so exploration used file reads and grep.
