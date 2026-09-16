---
description: "Bounds what a test may assert on. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that writes, plans, or fixes tests."
applyTo: "**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03-phase-execute.agent.md,**/test-writer.agent.md,**/test-analyst.agent.md,**/test-orchestrator.agent.md,**/test-fixer.agent.md"
---

# Test Target Scope

A test checks executable behavior: inputs, outputs, and side effects. Do not test anything else.

## Do not use these as test targets

- Do not test files under `docs/` or any README-style prose.
- Do not test `dev/` or any other Git-ignored or scratch directory. These directories contain temporary pipeline artifacts.
- Do not test Markdown files in general.

A pipeline document, phase summary, or plan file is a work artifact, not a test unit. Verify it with a QA check or review step.

## One exception

Test file content when the repository's own deliverable **is** that content, such as a prose corpus, an agent-definition set, or a generated-output contract. This test is a real guard. Commit it to the tracked suite. Follow the `guard-integrity` skill for this case.

Apply the exception only when the repository ships the text as its product. A change to a `.md` file alone does not qualify.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-target-scope."* Then proceed normally.
