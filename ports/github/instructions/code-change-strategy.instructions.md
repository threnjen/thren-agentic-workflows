---
description: "Prevents small-change guidance from creating duplicate implementations. Audience is enumerated because code-writing and code-review agents have unrelated names."
applyTo: "**/04b-feature-implementer.agent.md,**/04c-feature-review-and-fix.agent.md,**/04h-unity-reviewer.agent.md,**/single-feature-agent.agent.md,**/debugger.agent.md,**/test-writer.agent.md,**/test-fixer.agent.md,**/auditor-code.agent.md"
baseline: true
---

# Code Change Strategy

## Requirements

- Load `base-code-guidelines` before you write, fix, or review code. Skipping it creates duplicate implementations.
- Scope a change by the responsibility it changes, not by lines touched. Caller updates the change forces stay in scope.
- Search for an existing implementation of the same responsibility before you add a sibling function, class, fixture, or helper.

## Traps

- An existing implementation almost fits. Weigh extending its contract against adding a sibling. Reuse it only when both callers keep one cohesive responsibility.
- Reuse touches several callers. Update and test every one. File count does not turn a required contract change into scope creep.
- Similar syntax hides different meaning. Keep implementations apart when reuse would couple responsibilities that change for different reasons.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: code-change-strategy."* Then proceed normally.
