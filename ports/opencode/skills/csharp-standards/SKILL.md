---
name: csharp-standards
description: "The complete non-Unity C# standard — hard rules plus depth: naming and member order, formatting, access control and immutability, nullability, async discipline, error handling, collections, `var`, and the test for when a service class or an abstraction is earned. Use when: writing or reviewing C# outside a Unity assembly, or needing the rationale or edge case behind a rule below. Unity C# is governed by `unity-development` instead."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# C# Standards

This skill is self-contained. The Rules section defines the standard. Later sections explain the reasons and the deciding test.

This skill covers non-Unity C#. Inside Unity assemblies, `unity-development` overrides several rules here. These rules cover the private-field prefix, DTO shape, nullable enablement, and null checks on engine objects. Load that skill instead.

PAIRED ASSET: `instructions/csharp-style.instructions.md` carries the same rules for Cursor and Copilot. Those harnesses reach the rules through file globs instead of loading this skill. Change both files together.

## Rules

- **Naming:** Use PascalCase for types, methods, properties, public members, namespaces, and constants. Use `camelCase` for locals and parameters. **Use `_camelCase` for private, protected, and internal fields in non-Unity C#.** Prefix interfaces with `I`. Treat acronyms as single words, such as `MyRpc`. Put one core class in each file and match the filename to the class. Name booleans as true/false statements, such as `CanRefund` and `IsEligibleForRefund`. Do not use `Manager`, `Helper`, `Util`, or `Data` suffixes unless you can state the class's single responsibility.
- **Access and immutability:** Use the most restrictive modifier that works. Start with `private`. Do not use a public setter unless external mutation is an explicit requirement. Expose an intent-revealing transition method instead. Mark construction-only fields `readonly`. Use `record` for behavior-free DTOs. Use a class for anything that owns behavior.
- **Nulls:** Enable nullable reference types (`<Nullable>enable</Nullable>`). Never return `null` for an empty collection. Return `[]` instead. Return `T?` for a possibly missing single object. Never pass a literal `null` argument. Use an overload or a named optional parameter instead.
- **Async:** Use `async` only for real I/O. Never use it speculatively. Never use `async void` outside event handlers. Every public async method that calls external infrastructure must take a `CancellationToken`. Never use `.Result` or `.Wait()`. Use `await` instead.
- **Error handling:** Catch the specific exception you expect. Use bare `Exception` only at a top-level boundary. Never swallow an exception silently. Never use exceptions for control flow.
- **Collections:** Use the most restrictive type for inputs, such as `IReadOnlyList<>` or `IEnumerable<>`. Return `IList<>` for outputs when transferring ownership. Otherwise, return the most restrictive type. Prefer `List<>` to arrays for public members. Remove items during iteration with `RemoveAll(predicate)` or a replacement container.
- **`var`:** Use `var` only when the type is unambiguous from the right-hand side.
- **Member order:** Order members as nested types, then static/const/readonly fields, then fields and properties, then constructors, and then methods. Place public members before private members within each group. Order modifiers as `public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`. Keep `using` directives alphabetical, place `System.*` directives first, and place all directives outside any namespace.
- **Formatting:** Use 2-space indentation and a 100-column limit. Always use braces. Put one statement on each line. Do not break lines before an opening brace or between `}` and `else`.
- **Misc:** Use `const` where possible and `readonly` as fallback. Do not use magic numbers. Use expression bodies only on lambdas and single-line read-only properties. Invoke delegates null-conditionally (`OnThing?.Invoke()`). Use `out` for non-input returns and place it last. Use `ref` only to mutate a genuine input. Prefer a named class to `Tuple<>`. Keep namespaces at most two levels deep. Use extension methods only when the source type cannot be changed.

## Objects own behavior

A class with properties but no methods adds unnecessary ceremony when it could be a struct. If domain objects contain only data and all logic sits in `*Service`/`*Handler`/`*Helper`, the code is procedural despite using an object-oriented language.

Use service classes in exactly two situations. They can coordinate an operation that genuinely spans multiple domain objects or call external infrastructure. Ask whether each method could live on the object it operates on. If it could, place it there.

## Abstraction is earned

Create an abstraction when two concrete things must be treated as one. Do not create one earlier. An `IOrderService` with exactly one implementation adds indirection without payoff. A real test double counts as the second implementation. An imagined future implementation does not count.

## Complexity belongs at the edges

Domain logic is synchronous and I/O-free. It knows nothing about databases, HTTP, or the file system. Only the boundary layer orchestrates async work. A domain method that is `async` by convention has leaked infrastructure into the core. Speculative `async` is also banned because it propagates up the whole call stack.

## Nulls in practice

```csharp
// NEVER — caller cannot know null is possible
public Order GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);
// MUST
public Order? GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);
```

Expected absence is not exceptional. When a repository returns `Order?`, use `if (order is null)` instead of `try`/`catch (OrderNotFoundException)`.

## Immutability in practice

```csharp
public class Order {
    public int Id { get; }
    public string Status { get; private set; }

    public void Submit() {
        if (Status != "Draft") throw new InvalidOperationException("Only draft orders can be submitted.");
        Status = "Submitted";
    }
}
```

Resist public setters by default. A public setter allows anything, anywhere, to change the value. That is almost never the intent.

## `var` ambiguity test

If a reader must open the method signature to learn the type, write the type explicitly. `var order = new Order()` is fine. `var result = _repository.GetSummary(id)` is not.

## Tests

Run all tests with `dotnet test`. Run one test with `dotnet test --filter "FullyQualifiedName~TestName"`. The `test-execution-evidence.instructions.md` instruction governs TDD discipline and test-status reporting.
