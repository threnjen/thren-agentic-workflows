---
description: "Defines what counts as test execution evidence and forbids treating unexecuted tests as passing. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that runs or reports on tests."
applyTo: "**/04b-feature-implementer.agent.md,**/04c-feature-review-and-fix.agent.md,**/04-phase-execute.agent.md"
---

# Test Execution Evidence

Every test-status claim carries exactly one of these:

- `executed-green` — the suite ran, zero failures
- `executed-failing` — the suite ran, one or more failures
- `not-executed` — the suite did not run, or ran without producing a results artifact

`not-executed` never satisfies a gate and is never reported as, or alongside, a passing result.

## Evidence requirement

A claim of `executed-green` or `executed-failing` cites all three of:

1. The exact command run
2. The results artifact path
3. Total, passed, and failed counts read from that artifact

Without all three the status is `not-executed`. A status you inferred, expected, or were told by another agent is not evidence.

### Supervisor attestation

One exception, for a user-invocable root orchestrator only. Accept an explicit assertion from your direct supervisor that a named authoritative suite finished with zero failures, when that supervisor exported no XML artifact. This never applies to a subagent or to an indirect report.

Record the named suite, the command or Test Runner action as reported, the supervisor's stated counts when it gave any, and `supervisor-attested (no artifact exported)` as the results artifact. When the supervisor says only "all passed", record `failed=0`, `passed=all reported tests`, and `total=not supplied`. Never invent counts. Never treat silence, expectation, or a subagent's claim as attestation.

## Not test execution

- A successful compile or build
- A focused, reflection-based, or hand-rolled harness that bypasses the project's test runner
- A run that discovers zero tests. Report it as `not-executed`, not as a pass.

## Vocabulary

`Regressions: None` and "none observed" belong to `executed-green` alone. Everywhere else write `Regressions: Unknown — tests not executed`.

## Affected suites

When a change alters a shared API signature, a constructor contract, a serialized schema, a bootstrap path, a data or def file, or a policy-controlled file, run:

- Every entry in the execution manifest's `## Verification Assets` section, **and**
- Every suite that exercises the changed symbol

The feature's own new tests are not enough. A contract change that fails closed breaks callers written before it, and those callers' tests are what prove it.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-execution-evidence."* Then proceed normally.
