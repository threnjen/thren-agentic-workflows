---
name: typescript-standards
description: "The complete TypeScript standard — hard rules plus depth: naming conventions, `interface` vs `type`, optionality and `readonly`, when a class is justified, static factories, control-flow and coercion details, function form and `this` capture, modelling absence in the return type, catch narrowing, property-based testing with fast-check, and the tsconfig/eslint enforcement stack. Use when: writing or reviewing TypeScript and needing a convention the rules don't state, deciding between a class and a module of functions, shaping an options object or error type, or setting up the strict toolchain."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# TypeScript Standards

Self-contained: the Rules section is the standard; everything after it is the conventions, edge cases, and one example per rule that earns its place.

PAIRED ASSET: `instructions/typescript.instructions.md` carries the same rules for Cursor and Copilot, which reach them by file glob rather than by loading this skill. Change both together.

Baseline: the [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html), plus Prettier defaults for quotes, semicolons, line width, and indentation — formatting is the formatter's job, never hand-tuned.

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

Greenfield starts strict. On an existing loosely-typed codebase, start from `recommendedTypeChecked` and ratchet up as violations are burned down.

## Naming

| Form | Applies to |
|---|---|
| `UpperCamelCase` | classes, interfaces, type aliases, enums, type parameters |
| `lowerCamelCase` | variables, parameters, functions, methods, properties |
| `CONSTANT_CASE` | module-level constants, `static readonly` fields, enum values |

Acronyms are words: `loadHttpUrl`, not `loadHTTPURL`. No `_` prefixes or suffixes. Booleans read as true/false statements — `isEligible`, `canRefund`, not `refundCheck`. Files are `snake_case.ts`. Import order: Node stdlib → third-party → local.

## Type shapes

`interface` for object shapes; `type` for unions, tuples, and mapped types. Prefer `field?: Type` over `field: Type | undefined` — and never bake `| null` / `| undefined` into a type alias; add nullability at the usage site. `T[]` for simple element types, `Array<T>` for complex ones. Mark anything that shouldn't change `readonly` / `readonly T[]`.

Rely on inference for trivially-inferred locals (`const m = new Map<string, Order>()`); annotate public signatures and complex expressions.

## Classes

Justified by state, inheritance, or a shared interface. A class of static methods is a namespace with extra steps — use module-level functions; the module *is* the namespace. Applying this is a simplicity judgement — see [simplicity-review](../simplicity-review/SKILL.md) for the general form.

- `private` by default, using TypeScript's `private` — never `#fields`. Parameter properties avoid the assignment boilerplate.
- Properties never reassigned after construction are `readonly`.
- No I/O or heavy work in a constructor. Constructors can't be `async`; static factories can: `static async fromFile(path: string): Promise<Config>`.
- Getters are pure. No pass-through accessor pairs that add nothing over a plain property. Never manipulate prototypes.

## Control flow

- Braces on every control-flow statement. One declaration per statement.
- Iterate arrays with `for...of` or array methods — never `for...in`. On objects, `Object.keys/values/entries`.
- Every `switch` has a `default`, even if empty; no fall-through in non-empty cases.
- Coerce explicitly: `String(x)`, `Number(x)` (then check `NaN`), `Boolean(x)`/`!!x`. Never unary `+` to parse; `parseInt` only with a non-10 radix.

## Functions

Function declarations for top-level named functions; arrow functions for callbacks and anywhere `this` capture matters — never `function` expressions. Rest parameters (`...args`) over `arguments`; spread over `.apply()`. Never pass an unbound method reference (`handler = this.method`); wrap it in an arrow function.

Many optional parameters become a destructured options object with defaults:

```typescript
function fetchOrders({ limit = 50, offset = 0, includeDrafts = false }: FetchOrdersOptions = {}) { ... }
```

## Async and error modelling

Don't mark a function `async` unless it awaits something. Don't `return await` except inside `try`. Offload CPU-heavy work to a worker thread rather than blocking the event loop.

Expected, handleable absence is not exceptional — model it in the return type (`Order | undefined`) instead of throwing and catching as branching. Keep `try` blocks to the statements that can actually throw. Catch variables are `unknown` under strict config: narrow with `instanceof` before touching `.message`. Errors carry context — ids, state — not just "failed".

Deliberate fire-and-forget gets its own handler:

```typescript
void sendConfirmationEmail(order).catch((e) => logger.error({ err: e }, 'email failed'));
```

Configure the logger — level, transport, redaction — at the application entry point only, never inside a library module.

Instrument densely. Put the identifying values in the fields, not the message:

```typescript
logger.debug({ orderId, url }, 'fetching order');
const res = await fetch(url);
logger.debug({ orderId, status: res.status, ms: Date.now() - t0 }, 'order fetched');
```

Log every boundary call and its outcome, every fallback, retry, cache miss, and early return, and every caught error with `{ err }` plus the state that produced it. Configure Pino redaction for secret-bearing fields at the entry point.

## Tests

Vitest. `fast-check` is a standard dev dependency for property-based testing: use `fc.assert(fc.property(...))` inside a Vitest `test()` block, and prefer its generators over hand-crafted inputs when testing ranges, formats, or invariants. Pair with unit tests — properties find edge cases, unit tests document known behavior.

TDD discipline and test-status reporting are governed by `test-execution-evidence.instructions.md`, not here.
