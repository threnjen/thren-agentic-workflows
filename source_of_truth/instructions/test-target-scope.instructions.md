---
description: "Bounds what a test may assert on. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes, plans, or fixes tests."
applyTo: "**/04b-feature-implementer.agent.md,**/04c-feature-review-and-fix.agent.md,**/04-phase-execute.agent.md,**/test-writer.agent.md,**/test-analyst.agent.md,**/test-orchestrator.agent.md,**/test-fixer.agent.md"
---

# Test Target Scope

A test asserts on executable behavior — inputs, outputs, side effects. Nothing else earns a test.

## Never a test target

- `docs/` and any README-style prose
- `dev/` and every other gitignored or scratch directory, whose contents are ephemeral pipeline artifacts
- Markdown files in general

A pipeline document, a phase summary, or a plan file is an artifact of the work, not a unit under test. Verify it with a QA check or a review step.

## The one exception

Assert on file content only when the repository's own deliverable **is** that content — a prose corpus, an agent-definition set, a generated-output contract. Then the guard is a real guard: commit it to the tracked suite and follow the `guard-integrity` skill, which exists for exactly this case.

Deciding the exception applies requires the repository to ship the text as its product. "The change I made was in a `.md` file" is not that.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-target-scope."* Then proceed normally.
