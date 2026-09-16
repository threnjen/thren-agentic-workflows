---
name: typescript-standards
description: "The complete TypeScript standard — hard rules plus depth: naming conventions, `interface` vs `type`, optionality and `readonly`, when a class is justified, static factories, control-flow and coercion details, function form and `this` capture, modelling absence in the return type, catch narrowing, property-based testing with fast-check, and the tsconfig/eslint enforcement stack. Use when: writing or reviewing TypeScript and needing a convention the rules don't state, deciding between a class and a module of functions, shaping an options object or error type, or setting up the strict toolchain."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# TypeScript Standards

This skill is self-contained. The Rules section is the standard. Later sections define conventions and edge cases. Each rule has one example when an example adds value.

PAIRED ASSET: `instructions/typescript.instructions.md` carries these rules for Cursor and Copilot. Cursor and Copilot load the file by glob instead of loading this skill. Change both files together.

Use the [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) as the baseline. Use Prettier defaults for quotes, semicolons, line width, and indentation. Do not tune formatting by hand.

## Rules

- **Modules:** ES module syntax only — never `require()`, never `namespace`, never `export default`, never `export let`. Export only what is used outside the module. `import type` / `export type` for type-only bindings.
- **Types:** never `any` — use `unknown` and narrow. Never `@ts-ignore`, `@ts-expect-error`, or `@ts-nocheck` in production code.
- **Trust boundaries:** validate request bodies, external API responses, env vars, and file/queue contents with a Zod schema at the edge — parse, don't assert. Validate once, then trust internally.
- **Async:** every promise is awaited or explicitly handled — never disable `no-floating-promises`. Independent operations run under `Promise.all`. Never mix `.then()` and `await` in one function. No `*Sync` calls outside startup scripts.
- **Errors:** throw only `Error` subclasses, always with `new`. An empty catch block requires a comment saying why swallowing is correct.
- **Logging:** a structured logger (Pino) with context as fields. `console.*` only for deliberate CLI output.
- **Observability:** log every boundary call, its outcome, every unpredictable branch, and every caught exception, with the values as fields. Instrument on the way in, never after a bug appears.
- **Variables:** `const`/`let` only, never `var`. `===`/`!==` always — `== null` is the one exception.
- **Dependencies:** commit `package-lock.json`; CI installs with `npm ci`.
- **Tooling:** `tsc --noEmit` strict and typescript-eslint strict are enforced. Never disable them.

## Enforcement stack

```jsonc
// tsconfig.json
{ "compilerOptions": {
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "noImplicitOverride": true,
  "exactOptionalPropertyTypes": true
} }
```

```js
// eslint.config.js
import tseslint from 'typescript-eslint';
export default tseslint.config(
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
);
```

Start new codebases with strict settings. In an existing loosely typed codebase, start with `recommendedTypeChecked`. Increase strictness as you remove violations.

## Naming

| Form | Applies to |
|---|---|
| `UpperCamelCase` | classes, interfaces, type aliases, enums, type parameters |
| `lowerCamelCase` | variables, parameters, functions, methods, properties |
| `CONSTANT_CASE` | module-level constants, `static readonly` fields, enum values |

Treat acronyms as words.
Use `loadHttpUrl`, not `loadHTTPURL`.
Do not add `_` prefixes or suffixes.
Name booleans as true-or-false statements.
Use `isEligible` or `canRefund`, not `refundCheck`.

Use `snake_case.ts` for files.
Order imports as Node stdlib, third-party, then local.

## Type shapes

Use `interface` for object shapes.
Use `type` for unions, tuples, and mapped types.
Prefer `field?: Type` over `field: Type | undefined`.
Do not put `| null` or `| undefined` in a type alias.
Add nullability where you use the type.

Use `T[]` for simple element types and `Array<T>` for complex ones.
Mark values that should not change with `readonly` or `readonly T[]`.

Use inference for locals whose types are obvious, such as `const m = new Map<string, Order>()`.
Annotate public signatures and complex expressions.

## Classes

Use a class when it owns state, supports inheritance, or implements a shared interface.
Use module-level functions for a class that contains only static methods.
The module *is* the namespace.
See [simplicity-review](../simplicity-review/SKILL.md) for the general form of this judgment.

- Use TypeScript's `private` by default.
- Never use `#fields`.
- Use parameter properties to avoid assignment boilerplate.
- Mark properties that construction never reassigns as `readonly`.
- Do not perform I/O or heavy work in a constructor.
- Constructors cannot be `async`.
- Static factories can be `async`, as in `static async fromFile(path: string): Promise<Config>`.
- Keep getters pure.
- Do not add pass-through accessor pairs when a plain property suffices.
- Never manipulate prototypes.

## Control flow

- Use braces for every control-flow statement.
- Use one declaration per statement.
- Iterate arrays with `for...of` or array methods.
- Never use `for...in` for arrays.
- Use `Object.keys/values/entries` for objects.
- Add a `default` case to every `switch`, even when it is empty.
- Do not allow fall-through in non-empty cases.
- Use explicit coercion.
- Use `String(x)`, `Boolean(x)`, or `!!x` as needed.
- Use `Number(x)` and then check `NaN`.
- Never use unary `+` to parse.
- Use `parseInt` only with a non-10 radix.

## Functions

Use function declarations for top-level named functions.
Use arrow functions for callbacks and whenever `this` capture matters.
Never use `function` expressions.
Prefer rest parameters (`...args`) to `arguments`.
Prefer spread to `.apply()`.

Never pass an unbound method reference such as `handler = this.method`.
Wrap it in an arrow function.

Use a destructured options object with defaults when a function has many optional parameters:

```typescript
function fetchOrders({ limit = 50, offset = 0, includeDrafts = false }: FetchOrdersOptions = {}) { ... }
```

## Async and error modelling

Mark a function `async` only when it awaits something.
Use `return await` only inside `try`.
Run CPU-heavy work in a worker thread so it does not block the event loop.

Model expected, handleable absence in the return type, such as `Order | undefined`.
Do not throw and catch for this branch.
Keep `try` blocks limited to statements that can throw.
Strict config gives catch variables the type `unknown`.
Narrow them with `instanceof` before accessing `.message`.
Include context such as IDs and state in errors, not only "failed".

Handle deliberate fire-and-forget operations with their own handler:

```typescript
void sendConfirmationEmail(order).catch((e) => logger.error({ err: e }, 'email failed'));
```

Configure the logger's level, transport, and redaction only at the application entry point.
Never configure the logger inside a library module.

Add detailed instrumentation.
Put identifying values in fields, not in the message:

```typescript
logger.debug({ orderId, url }, 'fetching order');
const res = await fetch(url);
logger.debug({ orderId, status: res.status, ms: Date.now() - t0 }, 'order fetched');
```

Log every boundary call and its outcome.
Log every fallback, retry, cache miss, and early return.
Log every caught error with `{ err }` and the state that produced it.
Configure Pino redaction for fields that contain secrets at the entry point.

## Tests

Use Vitest.
Treat `fast-check` as a standard dev dependency for property-based testing.
Call `fc.assert(fc.property(...))` inside a Vitest `test()` block.
Prefer its generators to hand-crafted inputs when testing ranges, formats, or invariants.

Pair property tests with unit tests. Property tests find edge cases. Unit tests document known behavior.

Use `test-execution-evidence.instructions.md` for TDD discipline and test-status reporting. This skill does not define them.
