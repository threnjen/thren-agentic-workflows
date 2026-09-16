---
name: ai-instruction-framework
description: "Rule taxonomy (Judgment / Knowledge / Pointer), rule-quality standard, anti-patterns, and file template for AI coding instruction files. The single shared definition the Instructions Writer authors against and the Instructions Evaluator scores against. Use when: writing, evaluating, or reasoning about instruction files (.instructions.md, copilot-instructions.md, CLAUDE.md, .cursorrules)."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# AI Instruction File Framework

This file provides authoritative definitions for the Instructions agent set. Workflows live in the
agents. This file defines what a rule is and what makes a rule well-formed. Do not paraphrase it
from memory.

## Rule Taxonomy

Instructions must encode **rules the agent cannot infer from reading source code**.

| Category | What it is | Effect on agent | Example |
|-----------|------------|-----------------|---------|
| **Judgment** | Convention, constraint, or gotcha not visible in code | Agent follows a rule it would otherwise violate | "All monetary values use `Decimal`, never `float`" |
| **Knowledge** | Architectural fact discoverable by reading source | Agent regurgitates a summary instead of reading code | "The BaseHandler class has a `validate()` method and a `schema` attribute" |
| **Pointer** | Directive to read a specific file before acting | Agent reads real code, gets full context | "MUST inherit from the base class in `handlers/base.py` — read that file first" |

**Target ratio:** ~60% Judgment, ~30% Pointer, ~10% Knowledge.

Knowledge-heavy instructions produce a measured and reproducible failure mode. The agent summarizes
instruction content instead of reading the source. The agent then produces shallower code than it
would without instructions.

## Rule Quality Standard

The writer applies one standard when drafting. The evaluator applies it during the static scan. The
evaluator **flags** a rule that violates any item. It does not fail the rule automatically.

1. **Two-line ceiling** — no rule exceeds 2 lines. Verbose rules fail on weaker models and in longer
   contexts. This ceiling applies to every section.
2. **No conditionals in Hard Requirements** — a hard requirement must not contain `if`, `when`,
   `unless`, or `depending on`. A requirement that only sometimes applies belongs in **Common
   Traps**, which is exempt from this rule. A trap is situational by definition. Its
   `<gotcha>: <what to do instead>` form is the intended shape. Flag conditionals only in Hard
   Requirements, Standards, and Orientation content.
3. **No soft language** — `should`, `consider`, `try to`, and `where possible` are ignored. Use
   MUST with a consequence ("will fail code review"). Apply this rule to every section. The measured
   result is FAIL for the same rule as a soft bullet and PASS for the same rule as MUST.

## Additional Principles

- **Point, don't describe.** Point to the file instead of listing what a class provides:
  `MUST inherit from BaseHandler in handlers/base.py — read that file first`.
- **Test with code generation, not questions.** "Write an endpoint that handles X" tests whether
  instructions prevent real bugs. "How do I add an endpoint?" only tests summarization.
- **Lint file references.** Every path mentioned in an instruction file must exist in the repo.

## Anti-Patterns

1. **Soft language** — see rule-quality standard 3.
2. **Over-scoping** — domain-specific rules in an always-loaded file waste context in unrelated
   conversations. Use scoped files with `applyTo` globs.
3. **Knowledge rules** — rules describe what the code does rather than what an agent would get
   wrong.

## Instruction File Template

```yaml
---
applyTo: "<glob>"
---
```

```markdown
# <Domain Name>

## Hard Requirements (will fail code review)
- MUST <rule>. <consequence if violated>.

## Common Traps
- <gotcha>: <what to do instead>

## Where to Look
- `<path/to/file.py>` — <what it demonstrates>
```
