---
name: base-code-guidelines
description: "Activate when writing, adding, reviewing, refactoring, or fixing any code, or when choosing libraries and dependencies. Provides behavioral guidelines to avoid common LLM coding mistakes — overcomplication, untargeted edits, hidden assumptions, and missing success criteria — and enforces an escalation ladder that exhausts cheaper sources of a solution before new code gets written. Also activate when the user asks for the simplest or most minimal solution, or complains about bloat, boilerplate, or unnecessary dependencies."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Base Code Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls, with a minimalism ladder adapted from lazy-senior-dev skill patterns.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative. Every line of code is a liability — it must be read, tested, secured, and maintained forever.**

Before writing new code, work down this escalation ladder and stop at the first level that solves the problem:

1. **Nothing.** Does this need to be built at all? If the need is speculative ("we might want to configure this later"), skip it and say so in one line.
2. **This codebase.** Search for an existing helper, utility, type, or established pattern before writing a sibling of it. Re-implementing something that lives three files away is the most common form of generated waste.
3. **The standard library.** If the language ships it, use it.
4. **The platform.** A native capability beats a hand-built one: an HTML input type over a widget library, CSS over JavaScript, a database constraint over application-side enforcement.
5. **A dependency you already have.** If an installed package solves it, use that package. Never add a *new* dependency for something a few lines of code cover.
6. **The smallest new code that works.** Often that is one line. Write it, and no more.

The ladder shortens the solution, never the investigation: read the task and the code it touches, and trace the real flow end to end *before* climbing. A tiny diff applied to a misunderstood problem is a second bug wearing a small disguise.

Rules:
- No abstraction without a second concrete consumer: no interface with one implementation, no factory producing one product, no configuration for a value that never varies.
- No features, "flexibility," or scaffolding beyond what was asked. Later can build its own scaffolding, with real requirements in hand.
- No error handling for impossible scenarios.
- Prefer deletion to addition; boring constructs over clever ones; fewest new files possible.
- When two same-size options exist, take the one that is correct on edge cases — minimalism means less code, not a flimsier algorithm.
- Bug fixes target the root cause, not the reported symptom: check every caller of the function being touched, and put one guard where all callers route through rather than a patch on the one path the report named.
- When a request looks over-specified, ship the minimal version and question the rest in the same response ("Did X; Y already covers the rest — say the word if you need full X").

**Never minimized** — cutting these is negligence, not minimalism: input validation at trust boundaries; error handling that prevents data loss or corruption; security measures; accessibility basics; anything the user explicitly asked for (if they insist on the full version after hearing the alternative, build it well — no re-litigating).

Output discipline: lead with the code, then at most a few short lines stating what was deliberately skipped and the concrete trigger for adding it ("skipped caching; add when the profiler shows this endpoint hot"). A long defense of a simplification is complexity smuggled back in as prose.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

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
