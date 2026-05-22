# AI Instruction File Framework

Conceptual reference for the `@Instructions Manager` agent set. Defines the
core principles and rule taxonomy that the writer and evaluator agents operate
against. For workflows, see the agents directly.

---

## Core Principles

Discovered through empirical A/B testing. Both Create and Evaluate modes depend
on these definitions.

### 1. Judgment, Not Knowledge

Instructions must encode **rules the agent cannot infer from reading source code**.

| Category | What it is | Effect on agent | Example |
|-----------|------------|-----------------|---------|
| **Judgment** | Convention, constraint, or gotcha not visible in code | Agent follows rule it would otherwise violate | "All monetary values use `Decimal`, never `float`" |
| **Knowledge** | Architectural fact discoverable by reading source | Agent regurgitates summary instead of reading code | "The BaseHandler class has a `validate()` method and a `schema` attribute" |
| **Pointer** | Directive to read a specific file before acting | Agent reads real code, gets full context | "MUST inherit from the base class in `handlers/base.py` — read that file first" |

**Target ratio:** ~60% Judgment, ~30% Pointer, ~10% Knowledge.

Knowledge-heavy instructions produce a measured, reproducible failure mode: the
agent summarizes instruction content instead of reading source, producing
shallower code that misses details the instructions don't capture. In A/B
tests, the WITHOUT-instructions version outperformed knowledge-heavy instructions
because it was forced to read actual source files.

### 2. MUST Language Over Soft Bullets

Rules stated as "should" or bare bullet points get ignored. Rules stated as
"MUST" with consequences ("will fail code review") get followed.

**Measured effect:** In blind A/B testing, converting soft bullets to MUST
language flipped two specific criteria from FAIL to PASS with no other changes.

### 3. Point, Don't Describe

Instead of describing what a class/function does, point to the file:

```
# BAD — agent summarizes this instead of reading the real class
Handler needs: METHOD attribute, validate() method, execute() method, optional cleanup()

# GOOD — agent reads real code, gets complete picture
MUST inherit from BaseHandler in handlers/base.py — read that file first
```

### 4. Test With Code Generation, Not Questions

"How do I add a new endpoint?" tests summarization ability.
"Write an endpoint that handles X" tests whether instructions prevent real bugs.

Always use code-generation tasks for evaluation.

### 5. Lint File References

Every file path mentioned in instructions must exist in the repo. Stale
references send agents to nonexistent files.

---

## Anti-Patterns

1. **Soft language** — "should" and bare bullets get ignored. "MUST (will fail
   code review)" gets followed. Measured: same rule as soft bullet = FAIL, as
   MUST = PASS.

2. **Over-scoping** — Putting domain-specific rules in the always-loaded file.
   This wastes context tokens in unrelated conversations. Use scoped files with
   `applyTo` globs.

3. **Knowledge rules** — Rules that describe what the code does rather than
   what an agent would get wrong. These cause agents to summarize instructions
   instead of reading source, producing shallower output than no instructions at all.

---

## Instruction File Template

```yaml
---
applyTo: "<glob>"
---
```

# <Domain Name>

## Hard Requirements (will fail code review)
- MUST <rule>. <consequence if violated>.

## Common Traps
- <gotcha>: <what to do instead>

## Where to Look
- `<path/to/file.py>` — <what it demonstrates>
