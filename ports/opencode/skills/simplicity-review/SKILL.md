---
name: simplicity-review
description: Review the current diff — or the whole repo — for over-engineering and return a delete-list. Use when the user asks to check for over-engineering, bloat, unnecessary abstraction, or excess code, or wants a diff slimmed down before merge. Finds code that should not exist; it does not hunt for bugs (use a code-review skill for that).
license: MIT
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Simplicity Review

This review asks one question: **what here should not exist?** Ordinary code review asks, "Is this code correct?" This review asks, "Is this code necessary?" It returns a concrete delete-list.

Use the escalation ladder in [base-code-guidelines](../base-code-guidelines/SKILL.md) §2. For each code element, ask whether a lower rung would cover it: nothing, existing code, the standard library, the platform, an installed dependency, or one line.

## Scope

- **Default: the current diff.** Gather it with `git diff` (staged + unstaged). For a branch, use `git diff <base>...HEAD`. If a knowledge graph is available, use `detect_changes`.
- **Whole-repo audit** (only when explicitly asked): run a whole-repository audit. Walk the source tree module by module. State up front which directories were covered and which were skipped.

## What to look for

For each function, class, file, or dependency in scope:

1. **Speculative code:** flag features, parameters, configuration options, or "flexibility" that nothing currently uses. These are YAGNI (You Aren't Gonna Need It) violations.
2. **Reinvented code:** flag logic that duplicates an existing helper in this codebase, a standard-library function, a native platform capability, or an installed dependency.
3. **Single-consumer abstractions:** flag interfaces with one implementation, factories with one product, wrappers that only forward, or layers that only pass through.
4. **New dependencies:** flag dependencies that a few lines of code or an existing dependency would cover.
5. **Boilerplate and scaffolding:** flag empty base classes, placeholder files, commented-out "future" code, or defensive handling for impossible states.
6. **Oversized solutions:** flag 200 lines where 50 would do, a class where a function would do, or a framework where a script would do.

## What never gets flagged

Do not include anything on the **Never minimized** list in [base-code-guidelines](../base-code-guidelines/SKILL.md) §2 in the delete-list. Read that list before reporting.

## Verify before reporting

A delete recommendation claims that no caller needs the code. Before including a finding, check its callers and references with grep or the knowledge graph. If something consumes it, either drop the finding or widen it to include the consumer chain. Never recommend deleting code you have not traced.

## Output: the delete-list

Order findings by lines saved, largest first:

```
## Delete-list

| # | Location | Excess | Replace with | Lines saved |
|---|----------|--------|--------------|-------------|
| 1 | src/utils/cache.py:1-118 | Hand-rolled TTL cache class, one consumer | functools.lru_cache on the fetch function | ~115 |
| 2 | src/api/client.py:40-72 | Retry wrapper duplicating urllib3's built-in Retry | Retry(total=3) on the existing session | ~30 |

**Total: ~N lines deletable across M findings.**
```

For each finding, write one line that states the excess, names what already covers it (the exact helper, standard-library function, or feature), and states any behavior difference that the swap would introduce. If the code is genuinely minimal already, say exactly that and stop. Do not manufacture findings to look thorough.

This skill only reports. Apply deletions only when the user asks. Treat each deletion as an ordinary reviewed edit.
