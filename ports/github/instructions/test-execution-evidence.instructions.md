---
description: "Defines what counts as test execution evidence and forbids treating unexecuted tests as passing. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that runs or reports on tests."
applyTo: "**/04b-feature-implementer.agent.md,**/04c-feature-review-and-fix.agent.md,**/04-phase-execute.agent.md"
---

# Test Execution Evidence

Every test-status claim carries exactly one of these:

- `executed-green` — the suite ran; zero failures
- `executed-failing` — the suite ran; one or more failures
- `not-executed` — the suite did not run, or ran without producing a results artifact

`not-executed` never satisfies a gate and is never reported as, or alongside, a passing result.

## Evidence requirement

Any claim of `executed-green` or `executed-failing` must cite:

1. The exact command run
2. The results artifact path
3. Total / passed / failed counts read from that artifact

Without all three, the status is `not-executed`. A status you inferred, expected, or were told by another agent is not evidence.

### Direct supervisor attestation

For a user-invocable root orchestrator, an explicit assertion from the direct supervisor that a named authoritative suite completed with zero failures is an accepted exception when the supervisor did not export an XML artifact. This exception never applies to subagents or to an indirect report. Record the named suite, the command or Test Runner action as reported, the supervisor's stated counts when available, and `supervisor-attested (no artifact exported)` as the results artifact. If the supervisor only says “all passed,” record `failed=0`, `passed=all reported tests`, and `total=not supplied` rather than inventing counts. Do not convert silence, expectation, or a subagent's claim into supervisor attestation.

## Not test execution

- A successful compile or build
- A focused, reflection-based, or hand-rolled harness that bypasses the project's test runner
- A run that discovers zero tests (report this as `not-executed`, not as a pass)

## Vocabulary

`Regressions: None` and "none observed" are reserved for `executed-green`. In every other case write `Regressions: Unknown — tests not executed`.

## Affected suites

When a change alters a shared API signature or constructor contract, a serialized schema, a bootstrap path, a data/def file, or a policy-controlled file, the suites to execute are:

- Every entry in the execution manifest's `## Verification Assets` section, **plus**
- Every suite exercising the changed symbol

The feature's own new tests are not sufficient. A contract change that fails closed breaks callers written before it — those callers' tests are the ones that prove it.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-execution-evidence."* Then proceed normally.
