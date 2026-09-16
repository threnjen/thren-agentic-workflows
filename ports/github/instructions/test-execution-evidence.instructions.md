---
description: "Defines what counts as test execution evidence and forbids treating unexecuted tests as passing. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that runs or reports on tests."
applyTo: "**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03-phase-execute.agent.md"
---

# Test Execution Evidence

Every claim about test status uses exactly one of these values:

- `executed-green` — the suite ran, zero failures
- `executed-failing` — the suite ran, one or more failures
- `not-executed` — the suite did not run, or ran without producing a results artifact

`not-executed` never satisfies a gate. Never report it as a passing result or with a passing result.

## Evidence requirement

A claim of `executed-green` or `executed-failing` must include all three items:

1. The exact command that ran
2. The results artifact path
3. Total, passed, and failed counts read from that artifact

If any item is missing, the status is `not-executed`. Do not treat an inferred or expected status as evidence, even when another agent reports it.

### Supervisor attestation

Only a user-invocable root orchestrator can use this exception. Accept an explicit assertion from your direct supervisor that a named authoritative suite finished with zero failures when that supervisor exported no XML artifact. This exception never applies to a subagent or to an indirect report.

Record the named suite. Record the command or Test Runner action that the supervisor reported. Record any counts the supervisor stated. Use `supervisor-attested (no artifact exported)` as the results artifact. When the supervisor says only "all passed", record `failed=0`, `passed=all reported tests`, and `total=not supplied`. Never invent counts. Never treat silence, expectation, or a subagent's claim as attestation.

## Not test execution

- A successful compile or build
- A focused, reflection-based, or hand-rolled harness that bypasses the project's test runner
- A run that discovers zero tests. Report this result as `not-executed`, not as a pass.

## Vocabulary

Use `Regressions: None` and "none observed" only with `executed-green`. For all other statuses, write `Regressions: Unknown — tests not executed`.

## Affected suites

When a change alters a shared API signature, constructor contract, serialized schema, bootstrap path, data or def file, or policy-controlled file, run the checks below:

- Every entry in the execution manifest's `## Verification Assets` section, **and**
- Every suite that exercises the changed symbol

The feature's own new tests are not enough. A contract change that fails closed breaks callers written before it. Those callers' tests prove it.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-execution-evidence."* Then proceed normally.
