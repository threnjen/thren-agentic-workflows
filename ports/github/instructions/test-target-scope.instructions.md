---
description: "Bounds what a test may assert on. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes, plans, or fixes tests."
applyTo: "**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03-phase-execute.agent.md,**/test-writer.agent.md,**/test-analyst.agent.md,**/test-orchestrator.agent.md,**/test-fixer.agent.md"
---

# Test Target Scope

A test asserts on executable behavior — inputs, outputs, side effects. Nothing else earns a test.

## Never a test target

- `docs/` and any README-style prose
- `dev/` and every other gitignored or scratch directory, whose contents are ephemeral pipeline artifacts
- Markdown files in general

A pipeline document, a phase summary, or a plan file is an artifact of the work, not a unit under test. Verify it with a QA check or a review step.

## The one exception

Assert on file content when the repository's own deliverable **is** that content — a prose corpus, an agent-definition set, a generated-output contract. The guard is then a real guard. Commit it to the tracked suite and follow the `guard-integrity` skill, which exists for this case.

The exception applies only when the repository ships the text as its product. "The change I made was in a `.md` file" is not that.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-target-scope."* Then proceed normally.
