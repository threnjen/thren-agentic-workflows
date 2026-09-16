---
name: base-code-guidelines
description: Activate when writing, adding, reviewing, refactoring, or fixing any code, or when choosing libraries and dependencies. Provides behavioral guidelines to avoid common LLM coding mistakes — overcomplication, untargeted edits, hidden assumptions, missing success criteria, and thin instrumentation — enforces an escalation ladder that exhausts cheaper sources of a solution before new code gets written, and mandates dense observability in every code path. Also activate when the user asks for the simplest or most minimal solution, or complains about bloat, boilerplate, or unnecessary dependencies.
license: MIT
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Base Code Guidelines

These guidelines reduce common LLM coding mistakes. They draw on [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) about LLM coding pitfalls and use a minimalism ladder adapted from lazy-senior-dev skill patterns.

**Tradeoff:** These guidelines favor caution over speed. Use judgment for trivial tasks.

## 1. Think Before Coding

**Do not assume. Do not hide confusion. State tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them. Do not choose one silently.
- If a simpler approach exists, state it. Push back when warranted.
- If something is unclear, stop. Name the confusion. Ask for clarification.

## 2. Simplicity First

**Write the minimum code that solves the problem. Avoid speculative code. Treat every line of code as a liability. Read, test, secure, and maintain every line forever.**

Before writing new code, follow this escalation ladder. Stop at the first level that solves the problem:

1. **Nothing.** Does this need to be built at all? If the need is speculative ("we might want to configure this later"), skip it. State that decision in one line.
2. **This codebase.** Search for an existing helper, utility, type, or established pattern before writing a duplicate. Re-implementing something that lives three files away is the most common form of generated waste.
3. **The standard library.** If the language ships it, use it.
4. **The platform.** Prefer a native capability over a hand-built one. For example, use an HTML input type instead of a widget library. Use CSS instead of JavaScript. Use a database constraint instead of application-side enforcement.
5. **A dependency you already have.** If an installed package solves the problem, use that package. Never add a *new* dependency for a problem that a few lines of code solve.
6. **The smallest new code that works.** It often requires one line. Write only that line.

The ladder shortens the solution, not the investigation. Before climbing, read the task and the touched code. Trace the real flow end to end. A tiny diff on a misunderstood problem creates a second bug.

Rules:
- Add an abstraction only when a second concrete consumer exists. Do not add an interface with one implementation or a factory with one product. Do not add configuration for a value that never varies.
- Do not add features, "flexibility," or scaffolding beyond what was asked. Add scaffolding later when real requirements exist.
- Do not add error handling for impossible scenarios.
- Prefer deletion over addition. Prefer boring constructs over clever ones. Use as few new files as possible.
- When two options have the same size, choose the one that handles edge cases correctly. Minimalism means less code, not a weaker algorithm.
- Target the root cause, not the reported symptom. Check every caller of the changed function. Add one guard where all callers route through it instead of patching one reported path.
- Measure scope by responsibility, not by diff size. Extending an existing implementation and updating its affected callers are in scope when they prevent a sibling implementation.
- Treat an almost-fitting implementation as a design decision. Do not reuse it automatically. Extend it only when both consumers share one responsibility and its contract stays cohesive. Otherwise, keep the implementations separate.
- When a request looks over-specified, ship the minimal version. Question the remaining requirements in the same response ("Did X; Y already covers the rest — say the word if you need full X").

**Never minimized:** Do not cut these items. Cutting them is negligence, not minimalism.

- Observability (Section 5)
- Input validation at trust boundaries
- Error handling that prevents data loss or corruption
- Security measures
- Accessibility basics
- Tests for non-trivial logic
- Anything the user explicitly asked for

If a listed item *looks* over-built, raise it as a question. Do not cut it. If the user insists on the full version after hearing the alternative, build it well. Do not re-litigate the decision.

Output discipline: Lead with the code. Then write at most a few short lines. State what you deliberately skipped and the concrete trigger for adding it ("skipped caching; add when the profiler shows this endpoint hot"). A long defense of a simplification adds complexity as prose.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own changes.**

When editing existing code:
- Do not "improve" adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style, even if you would do it differently.
- If you notice unrelated dead code, mention it. Do not delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Do not remove pre-existing dead code unless the user asks.

Use this test: every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until you verify them.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Observability

**Instrument the code while you write it. Adding logs later requires you to reproduce the bug first.**

Write enough logging that a reader reconstructs a failed run from the log alone, with no debugger and no second attempt.

Log every one of these:
- Log entry to every operation that crosses a boundary, including network, disk, database, subprocess, and queue operations. Include key inputs.
- Log the outcome of each operation. Include status, result size, row count, and duration.
- Log every branch that a reader would not predict, including fallback, retry, cache miss, early return, and skipped work.
- Log every caught exception. Include the exception and the state that produced it.
- Log every state transition and every configuration value resolved at startup.

Rules:
- Log identifiers that distinguish one run from millions of runs. Include request id, job id, user id, and file path.
- Log values, not labels. "validation failed" wastes the reader's time. "validation failed for order 4412: total -3" ends the investigation.
- Select the log level for the audience. DEBUG traces steps. INFO marks lifecycle events. WARNING marks degraded but handled states. ERROR carries the stack.
- Never log secrets, tokens, credentials, or personal data. Redact at the call site.
- Section 2 does not apply here. Observability is exempt from the minimalism ladder.
- Excess logging requires a later cleanup pass. Missing logging requires a later debugging session. Choose the cleanup pass.

The language standard defines language-specific form. It covers logger construction, structured fields, and exception capture.
