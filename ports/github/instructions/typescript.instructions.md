---
description: "Hard TypeScript/Node rules that a competent model violates by default — module form, `any`, boundary validation, floating promises, throwables, logging, lockfiles. Audience is source files only: the glob fires for Cursor and Copilot whenever TypeScript code is open, and costs nothing otherwise. Harnesses that inline instructions into agents reach these rules through the typescript-standards skill instead, routed by language-standards.instructions.md. PAIRED ASSET: skills/typescript-standards/SKILL.md restates these rules — change both together."
applyTo: "**/*.ts,**/*.tsx,**/*.mts,**/*.cts"
---

# TypeScript Rules

- **Modules:** ES module syntax only — never `require()`, never `namespace`, never `export default`, never `export let`. Export only what is used outside the module. `import type` / `export type` for type-only bindings.
- **Types:** never `any` — use `unknown` and narrow. Never `@ts-ignore`, `@ts-expect-error`, or `@ts-nocheck` in production code.
- **Trust boundaries:** validate request bodies, external API responses, env vars, and file/queue contents with a Zod schema at the edge — parse, don't assert. Validate once, then trust internally.
- **Async:** every promise is awaited or explicitly handled — never disable `no-floating-promises`. Independent operations run under `Promise.all`. Never mix `.then()` and `await` in one function. No `*Sync` calls outside startup scripts.
- **Errors:** throw only `Error` subclasses, always with `new`. An empty catch block requires a comment saying why swallowing is correct.
- **Logging:** a structured logger (Pino) with context as fields. `console.*` only for deliberate CLI output.
- **Variables:** `const`/`let` only, never `var`. `===`/`!==` always — `== null` is the one exception.
- **Dependencies:** commit `package-lock.json`; CI installs with `npm ci`.
- **Tooling:** `tsc --noEmit` strict and typescript-eslint strict are enforced. Never disable them.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: typescript."* Then proceed normally.
