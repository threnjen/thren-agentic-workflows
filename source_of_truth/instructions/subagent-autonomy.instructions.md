---
description: "Subagent autonomy: do not ask questions or wait for confirmation. Make sensible defaults and proceed. Audience is ENUMERATED deliberately - 'user-invocable: false' is a frontmatter property with no filename marker in source. Add every non-user-invocable subagent."
applyTo: "**/03?-*.agent.md,**/04?-*.agent.md,**/auditor-*.agent.md,**/client-deliverable-*.agent.md,**/instructions-evaluator.agent.md,**/instructions-writer.agent.md,**/qa-doc-generator.agent.md,**/qa-runner.agent.md,**/test-analyst.agent.md,**/test-fixer.agent.md,**/test-writer.agent.md"
---

You work autonomously. Do not ask questions and do not wait for confirmation. Choose sensible defaults and proceed.

You have no user to address. Your caller blocks on your return, so halting for an answer deadlocks the run. When something is ambiguous, take the reading that fits the repository best, record it as an assumption in your output, and continue. When you are genuinely blocked, return the blocker to your caller. Never prompt.

Autonomy does not relax a gate. When your contract defines a halt condition, a verdict, or a required failure string, emit it exactly.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: subagent-autonomy."* Then proceed normally.
