---
name: csharp-standards
description: "The complete non-Unity C# standard — hard rules plus depth: naming and member order, formatting, access control and immutability, nullability, async discipline, error handling, collections, `var`, and the test for when a service class or an abstraction is earned. Use when: writing or reviewing C# outside a Unity assembly, or needing the rationale or edge case behind a rule below. Unity C# is governed by `unity-development` instead."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# C# Standards

Self-contained: the Rules section is the standard; everything after it is the why and the deciding test.

Scope: non-Unity C#. Inside Unity assemblies, `unity-development` overrides several rules here (private-field prefix, DTO shape, nullable enablement, null checks on engine objects) — load that skill instead.

PAIRED ASSET: `instructions/csharp-style.instructions.md` carries the same rules for Cursor and Copilot, which reach them by file glob rather than by loading this skill. Change both together.

## Rules

- **Naming:** PascalCase for types, methods, properties, public members, namespaces, constants. `camelCase` for locals and parameters. **`_camelCase` for private/protected/internal fields — non-Unity C# only.** `I` prefix on interfaces. Acronyms are single words (`MyRpc`). One core class per file, filename matching it. Booleans read as a true/false statement (`CanRefund`, `IsEligibleForRefund`). No `Manager`/`Helper`/`Util`/`Data` suffix unless you can state the class's single responsibility.
- **Access and immutability:** most restrictive modifier that works — start `private`. No public setter unless external mutation is an explicit requirement; expose an intent-revealing transition method instead. `readonly` on construction-only fields. `record` for behavior-free DTOs; a class for anything owning behavior.
- **Nulls:** nullable reference types enabled (`<Nullable>enable</Nullable>`). Never return `null` for an empty collection — return `[]`. A possibly-missing single object returns `T?`. Never pass a literal `null` argument; use an overload or a named optional parameter.
- **Async:** `async` only for real I/O, never speculatively. Never `async void` outside event handlers. Every public async method calling external infrastructure takes a `CancellationToken`. Never `.Result` or `.Wait()` — `await`.
- **Error handling:** catch the specific exception you expect; bare `Exception` only at a top-level boundary. Never swallow silently. Never use exceptions for control flow.
- **Collections:** inputs take the most restrictive type (`IReadOnlyList<>`, `IEnumerable<>`); outputs return `IList<>` when transferring ownership, most restrictive otherwise. `List<>` over arrays for public members. Remove during iteration via `RemoveAll(predicate)` or a replacement container.
- **`var`:** only when the type is unambiguous from the right-hand side.
- **Member order:** nested types → static/const/readonly fields → fields and properties → constructors → methods; public before private within each group. Modifier order `public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`. `using` directives alphabetical, `System.*` first, outside any namespace.
- **Formatting:** 2-space indent, 100 columns, braces always, one statement per line, no line break before an opening brace or between `}` and `else`.
- **Misc:** `const` where possible, `readonly` as fallback, no magic numbers. Expression bodies on lambdas and single-line read-only properties only. Delegates invoked null-conditionally (`OnThing?.Invoke()`). `out` for non-input returns, placed last; `ref` only to mutate a genuine input. A named class over `Tuple<>`. Namespaces at most two levels deep. Extension methods only when the source type cannot be changed.

## Objects own behavior

A class of properties with no methods is a struct with extra steps. If domain objects are pure data and all logic sits in `*Service`/`*Handler`/`*Helper`, that is procedural code in an OO language.

Service classes are legitimate in exactly two situations: coordinating an operation that genuinely spans multiple domain objects, or calling external infrastructure. The test: could this method live on the object it operates on? If yes, it must.

## Abstraction is earned

Create an abstraction when two concrete things must be treated as one — not before. `IOrderService` with exactly one implementation is indirection with no payoff. A real test double counts as the second implementation; an imagined future one does not.

## Complexity belongs at the edges

Domain logic is synchronous, I/O-free, and knows nothing of databases, HTTP, or the file system. Only the boundary layer orchestrates async work. A domain method that is `async` by convention has leaked infrastructure into the core — which is also why speculative `async` is banned: it propagates up the whole call stack.

## Nulls in practice

```csharp
// NEVER — caller cannot know null is possible
public Order GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);
// MUST
public Order? GetById(int id) => _orders.FirstOrDefault(o => o.Id == id);
```

Expected absence is not exceptional. A repository returning `Order?` plus `if (order is null)` replaces a `try`/`catch (OrderNotFoundException)`.

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

The public setter is the default worth resisting: it declares that anything, anywhere, may change the value, which is almost never the intent.

## `var` ambiguity test

If a reader must open the method signature to learn the type, write the type out. `var order = new Order()` is fine; `var result = _repository.GetSummary(id)` is not.

## Tests

`dotnet test`; `dotnet test --filter "FullyQualifiedName~TestName"` for one test. TDD discipline and test-status reporting are governed by `test-execution-evidence.instructions.md`, not here.
