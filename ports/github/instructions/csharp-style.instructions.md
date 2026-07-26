---
description: "C# (Google) style rules for naming, organization, formatting, and idiomatic C#. Auto-loaded for C#-focused agents. Full reference: the-movies/docs/STYLE_GUIDE.md"
applyTo: "**/04h-unity-reviewer.agent.md,**/auditor-code.agent.md,**/04b-feature-implementer.agent.md,**/04c-feature-reviewer.agent.md"
---

# C# Style Rules (Google Style Guide)

## Naming

| Target | Convention |
|--------|-----------|
| Classes, methods, enums, public fields/properties, namespaces | PascalCase |
| Local variables, parameters | camelCase |
| Private/protected/internal fields and properties | `_camelCase` |
| Interfaces | `I` prefix (`IMyInterface`) |
| Filenames, directories | PascalCase |

- Acronyms are single words: `MyRpc` not `MyRPC`
- `const`, `static`, `readonly` do not affect naming conventions
- One core class per file; filename matches the main class

## Organization

**Modifier order:** `public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`

**`using` order:** Alphabetical; `System.*` imports first; declared outside any namespace.

**Class member order:**
1. Nested classes, enums, delegates, events
2. Static, const, and readonly fields
3. Fields and properties
4. Constructors and finalizers
5. Methods

Within each group: Public → Internal → Protected internal → Protected → Private

## Formatting

- 2-space indent; no tabs; 100-column limit
- One statement per line; one assignment per statement
- Braces always required (even when optional)
- No line break before opening brace; no line break between `}` and `else`
- Space after `if`/`for`/`while`/commas; no space inside parentheses
- Line continuations: 4-space indent

## C# Rules

**Constants:** Always `const` when possible; `readonly` as fallback; no magic numbers.

**Collections:**
- Inputs: most restrictive type (`IReadOnlyList<>`, `IReadOnlyCollection<>`, `IEnumerable<>`)
- Outputs: `IList<>` when transferring ownership; most restrictive option otherwise
- Prefer `List<>` over arrays for public members; arrays only for fixed-size or multidimensional data

**Properties:** Single-line read-only → expression body (`=>`). All others → `{ get; set; }`.

**Expression body:** Lambdas and properties only — not on method definitions.

**Structs vs Classes:** Almost always use a class. Structs only for small value-type-like objects (e.g., `Vector3`, `Quaternion`, `Bounds`).

**Lambdas:** Non-trivial (>~2 statements) or reused lambdas → named methods.

**LINQ:** Single-line calls preferred; member extension methods (`list.Where(x)`) over SQL-style keywords; avoid `Container.ForEach(...)` for more than one statement.

**`var`:** Use when type is obvious from context. Avoid for basic types, compiler-resolved numerics, or when the type aids readability.

**Delegates:** Always call via null-conditional: `SomeDelegate?.spawn()`.

**`ref`/`out`:** Use `out` for non-input returns (placed after all other params). Use `ref` only when mutating an input is necessary — not as a performance optimization for structs.

**Return types:** Prefer a named class over `Tuple<>` for complex return types.

**Extension methods:** Only when source is unavailable or unfeasible to change; only for core general features; err on the side of not adding them.

**Namespaces:** Max 2 levels deep; do not force file/folder layout to match namespaces.

**Null/struct returns:** Prefer `bool` success + `out` struct. Nullable structs acceptable when they significantly improve readability.

**Removing during iteration:** Use `list.RemoveAll(predicate)` when possible; otherwise build a replacement container.

**Field initializers:** Encouraged.

**Object initializers:** Fine for plain data types; avoid for classes or structs that have constructors.
