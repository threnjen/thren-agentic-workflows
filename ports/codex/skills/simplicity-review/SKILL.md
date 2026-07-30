---
name: simplicity-review
description: "Review the current diff — or the whole repo — for over-engineering and return a delete-list. Use when the user asks to check for over-engineering, bloat, unnecessary abstraction, or excess code, or wants a diff slimmed down before merge. Finds code that should not exist; it does not hunt for bugs (use a code-review skill for that)."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Simplicity Review

A review pass with one question: **what here should not exist?** Ordinary code review asks "is this code correct?" This review asks "is this code necessary?" — and hands back a concrete delete-list.

Uses the escalation ladder from [base-code-guidelines](../base-code-guidelines/SKILL.md) §2 as the measuring stick: for each piece of code, ask whether a lower rung (nothing, existing code, stdlib, platform, installed dependency, one line) would have covered it.

## Scope

- **Default: the current diff.** Gather it with `git diff` (staged + unstaged) or `git diff <base>...HEAD` for a branch. If a knowledge graph is available, `detect_changes` works too.
- **Whole-repo audit** (only when explicitly asked): walk the source tree module by module. State up front which directories were covered and which were skipped.

## What to look for

For each function, class, file, or dependency in scope:

1. **Speculative code** — features, parameters, config options, or "flexibility" nothing currently uses. YAGNI violations.
2. **Reinvented code** — logic that duplicates an existing helper in this codebase, a stdlib function, a native platform capability, or an already-installed dependency.
3. **Single-consumer abstraction** — interfaces with one implementation, factories with one product, wrappers that only forward, layers that only pass through.
4. **New dependencies** that a few lines of code (or an existing dependency) would cover.
5. **Boilerplate and scaffolding** — empty base classes, placeholder files, commented-out "future" code, defensive handling for impossible states.
6. **Oversized solutions** — 200 lines where 50 would do; a class where a function would do; a framework where a script would do.

## What never gets flagged

Nothing on the **Never minimized** list in [base-code-guidelines](../base-code-guidelines/SKILL.md) §2 may appear in the delete-list. Read that list before reporting.

## Verify before reporting

A delete recommendation is a claim that nothing needs the code. Before including a finding, check callers/references (grep or the knowledge graph). If something does consume it, either drop the finding or widen it to include the consumer chain. Never recommend deleting code you have not traced.

## Output: the delete-list

Findings ordered by lines saved, largest first:

```
## Delete-list

| # | Location | Excess | Replace with | Lines saved |
|---|----------|--------|--------------|-------------|
| 1 | src/utils/cache.py:1-118 | Hand-rolled TTL cache class, one consumer | functools.lru_cache on the fetch function | ~115 |
| 2 | src/api/client.py:40-72 | Retry wrapper duplicating urllib3's built-in Retry | Retry(total=3) on the existing session | ~30 |

**Total: ~N lines deletable across M findings.**
```

For each finding, one line each: what the excess is, what already covers it (name the exact helper/stdlib function/feature), and any behavior difference the swap would introduce. If the code is genuinely minimal already, say exactly that and stop — do not manufacture findings to look thorough.

This skill only reports. Apply deletions only when the user asks, as ordinary reviewed edits.
