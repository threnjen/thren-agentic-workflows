## Node.js Style

*When to reference*: When writing new modules, creating new classes, or unfamiliar with project conventions.

### Logging
- Use a structured logger (e.g. `pino` or `winston`) for all output
- Never use `console.log()` in production code; use `console.error()` only for fatal startup failures
- Configure log level via environment variable (e.g. `LOG_LEVEL`)
- Log with structured fields, not interpolated strings

### Configuration
- All configurable variables belong in a `config.ts` (or `config.js`)
- No magic strings or hardcoded values in business logic
- Group related constants together
- Read environment variables in the config file using `process.env`
- Provide sensible defaults where appropriate
- Validate required variables at startup (e.g. with `zod` or `envalid`)

### Style
- Prefer functional patterns (pure functions, immutability) over classes where appropriate
- Use classes for stateful services and when modeling domain entities
- Keep modules small and focused on a single responsibility
- Avoid side effects at module load time

### Variables
- Use `const` by default; use `let` only when reassignment is necessary
- Never use `var`
- Do not use global mutable state

### Async
- Always use `async/await`; avoid raw `.then()` / `.catch()` chains
- Never mix callbacks and promises in the same code path
- Propagate errors with `throw`; do not swallow them silently
- Use `Promise.all` / `Promise.allSettled` for concurrent operations

### Caching
- Use in-memory Maps or a dedicated cache library (e.g. `lru-cache`) for expensive lookups
- Set explicit TTLs and max-size limits
- Avoid caching mutable objects by reference

### Error Handling
- Extend `Error` for custom exceptions; name them with an `Error` suffix (e.g. `ValidationError`)
- Always include a descriptive message and relevant context
- Log errors with appropriate level before re-throwing or responding
- Never suppress errors with empty `catch` blocks

### Naming
- `camelCase` for variables, functions, and module-level constants that are values
- `PascalCase` for classes, types, interfaces, and enums
- `UPPER_SNAKE_CASE` for true compile-time or environment constants
- `_prefix` for private class members (or use `#` private fields in TypeScript/ES2022+)
- File names use `kebab-case`

### Imports
- Use ES module `import`/`export` syntax (not CommonJS `require`)
- One import per module per line
- Order: Node built-ins → third-party → local (enforce with ESLint `import/order`)
- Use path aliases (e.g. `@/services/...`) rather than deep relative paths

### TypeScript
- Enable `strict` mode in `tsconfig.json`
- Required type annotations for all public function signatures
- Prefer `interface` for object shapes; use `type` for unions, intersections, and aliases
- Use `unknown` instead of `any`; narrow with type guards before use
- Use `T | null` for nullable values; avoid `undefined` in return types unless intentional

### JSDoc / Comments
- Public functions and classes require JSDoc with `@param` and `@returns`
- Keep summaries ≤80 chars
- Do not add comments that merely restate what the code does

### Functions
- Small and focused (~40 lines max)
- Prefer named exports over default exports for easier refactoring
- Avoid mutating function arguments

## Communication

- No preamble/postamble unless requested
- No code comments unless asked
- No explanations for refusals
- Use ripgrep (`rg`) not `grep`/`find`
- Use Read/LS tools not `cat`/`head`/`tail`/`ls`
- Never guess URLs
