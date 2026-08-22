---
description: "Prevents small-change guidance from creating duplicate implementations. Audience is enumerated because code-writing and code-review agents have unrelated names."
applyTo: "**/04b-feature-implementer.agent.md,**/04c-feature-review-and-fix.agent.md,**/04h-unity-reviewer.agent.md,**/single-feature-agent.agent.md,**/debugger.agent.md,**/test-writer.agent.md,**/test-fixer.agent.md,**/auditor-code.agent.md"
---

# Code Change Strategy

## Hard Requirements

- MUST load `base-code-guidelines` before writing, fixing, or reviewing code. Missing this step can create duplicate implementations.
- MUST define scope by the responsibility being changed, not by changed-line count. Required caller updates remain in scope.
- MUST search for an existing implementation of the same responsibility before adding a sibling function, class, fixture, or helper.

## Common Traps

- An existing implementation almost fits: compare extending its contract with adding a sibling. Reuse it only when both consumers keep one cohesive responsibility.
- Reuse changes several callers: update and test every affected caller. File count does not make a required contract change into scope creep.
- Similar syntax hides different semantics: keep implementations separate when reuse would couple responsibilities that change for different reasons.
