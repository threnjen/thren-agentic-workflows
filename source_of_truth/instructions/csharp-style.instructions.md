---
description: "Hard C# rules a competent model violates by default — naming, member order, formatting, nullability, async, error handling, and access control. Audience is source files only: the glob fires for Cursor and Copilot whenever C# is open, and costs nothing otherwise. Harnesses that inline instructions into agents reach these rules through the csharp-standards skill instead, routed by language-standards.instructions.md. PAIRED ASSET: skills/csharp-standards/SKILL.md restates these rules — change both together. Unity carve-outs live in skills/unity-development."
applyTo: "**/*.cs"
---

# C# Style Rules (Google Style Guide)

## Naming

| Target | Convention |
|--------|-----------|
| Classes, methods, enums, public fields/properties, namespaces | PascalCase |
| Local variables, parameters | camelCase |
| Private/protected/internal fields and properties (non-Unity C#) | `_camelCase` |
| Interfaces | `I` prefix (`IMyInterface`) |
| Filenames, directories | PascalCase |

- Acronyms are single words: `MyRpc` not `MyRPC`
- `const`, `static`, `readonly` do not affect naming conventions
- Put one core class in each file.
- Match the filename to the main class.
- Name booleans as true/false statements: `CanRefund(order)`, `IsEligibleForRefund` — never `CheckRefund`.
- Do not use a `Manager` / `Helper` / `Util` / `Data` class-name suffix unless you can state the class's single responsibility.

The private-field prefix differs inside Unity assemblies. See `skills/unity-development`.

## Organization

**Modifier order:** `public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`

**`using` order:** Order using directives alphabetically. Place `System.*` directives first. Declare all directives outside any namespace.

**Class member order:**
1. Nested classes, enums, delegates, events
2. Static, const, and readonly fields
3. Fields and properties
4. Constructors and finalizers
5. Methods

Within each group, order members as Public → Internal → Protected internal → Protected → Private.

## Formatting

- Use 2-space indentation.
- Do not use tabs.
- Limit lines to 100 columns.
- Put one statement on each line.
- Put one assignment on each line.
- Always use braces, even when optional.
- Do not break a line before an opening brace.
- Do not break a line between `}` and `else`.
- Put a space after `if`, `for`, `while`, and commas.
- Do not put spaces inside parentheses.
- Indent line continuations by 4 spaces.

## C# Rules

**Constants:** Always use `const` when possible. Use `readonly` as a fallback. Do not use magic numbers.

**Collections:**
- Inputs: Use the most restrictive type (`IReadOnlyList<>`, `IReadOnlyCollection<>`, `IEnumerable<>`).
- Outputs: Return `IList<>` when transferring ownership. Otherwise, return the most restrictive option.
- Prefer `List<>` over arrays for public members. Use arrays only for fixed-size or multidimensional data.

**Properties:** Use an expression body (`=>`) for single-line read-only properties. Use `{ get; set; }` for all other properties.

**Expression body:** Use expression bodies only for lambdas and properties. Do not use them on method definitions.

**Structs vs Classes:** Almost always use a class. Use a struct only for a small value-type-like object, such as `Vector3`, `Quaternion`, or `Bounds`.

**Lambdas:** Use named methods for non-trivial (>~2 statements) or reused lambdas.

**LINQ:** Prefer single-line calls. Prefer member extension methods (`list.Where(x)`) over SQL-style keywords. Avoid `Container.ForEach(...)` when it contains more than one statement.

**`var`:** Use var when the type is obvious from context. Avoid var for basic types, compiler-resolved numerics, or when an explicit type aids readability.

**Delegates:** Always invoke delegates with null-conditional syntax: `SomeDelegate?.spawn()`.

**`ref`/`out`:** Use `out` for non-input returns. Place this parameter after all other parameters. Use `ref` only when mutating an input is necessary. Do not use it as a performance optimization for structs.

**Return types:** Prefer a named class over `Tuple<>` for complex return types.

**Extension methods:** Use extension methods only when the source is unavailable or infeasible to change. Use them only for core general features. Prefer not to add them.

**Namespaces:** Keep namespaces to at most 2 levels. Do not force the file or folder layout to match namespaces.

**Null/struct returns:** Prefer a `bool` success result with an `out` struct. Accept nullable structs when they significantly improve readability.

**Removing during iteration:** Use `list.RemoveAll(predicate)` when possible. Otherwise, build a replacement container.

**Field initializers:** Prefer field initializers.

**Object initializers:** You may use object initializers for plain data types. Avoid them for classes or structs that have constructors.

## Access and Immutability

- Use the most restrictive modifier that works.
- Start with `private`.
- Do not use a public setter unless external mutation is an explicit requirement.
- Expose an intent-revealing transition method (`Submit()`) instead.
- Keep the setter `private`.
- Mark construction-only fields `readonly`.
- Use `record` for behavior-free DTOs.
- Use a class for anything that owns behavior.

## Nulls

Enable nullable reference types (`<Nullable>enable</Nullable>`). Never return `null` for an empty collection. Return `[]` instead. Return `T?` for a single object that may be missing. Never pass a literal `null` argument.

## Async

Use `async` only for real I/O. Do not use it because it might be needed later. Never use `async void` outside event handlers. Require every public async method that calls external infrastructure to take a `CancellationToken`. Never use `.Result` or `.Wait()`. Use `await` instead.

## Error Handling

Catch the specific exception you expect. Use bare `Exception` only at a top-level boundary. Never swallow exceptions silently. Never use exceptions for control flow. Model expected absence in the return type.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: csharp-style."* Then proceed normally.
