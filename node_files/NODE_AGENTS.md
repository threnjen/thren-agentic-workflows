# Agent Guidelines

## Package Management
- `package.json` is the single source of truth for all dependencies (prod and dev).
- Always commit `package-lock.json`; use `npm ci` in CI/automated environments for reproducible installs.
- Install dev-only tools (e.g. `fast-check`, `vitest`) with `npm install --save-dev`.

## Core Engineering Principles

- Prefer small, reversible changes that compile and pass tests.
- Match existing code patterns before introducing new structure.
- Optimize for clarity and testability over cleverness.
- Keep responsibilities narrow and data flow explicit.
- Fail fast with descriptive errors; never silently swallow exceptions.

## Process

### When Stuck (Max 3 Attempts)
1. Document what failed (steps, errors, hypothesis)
2. Research 2-3 alternative implementations
3. Question fundamentals — simpler approach? different abstraction?
4. Try different angle — then STOP and reassess

## Testing

- Commit tests separately from implementation changes.
- Do not modify tests during implementation unless requirements changed.
- Add tests only when they can fail for a real defect.
- Use clear assertions and parameterized inputs (no magic values).
- Cover realistic edge cases, boundaries, and error paths.

### Property-Based Testing
- Use [fast-check](https://fast-check.dev/) for property-based testing; include it as a standard dev dependency.
- Prefer `fast-check` strategies over hand-crafted edge-case inputs when testing data ranges, formats, or invariants.
- Use `fc.assert(fc.property(...))` integrated with Vitest `test()` blocks.
- Combine with unit tests — fast-check finds edge cases, unit tests document known behavior.

## Quality Standards

### Every Commit Must
- [ ] Compile successfully
- [ ] Pass all tests (new functionality included)
- [ ] Follow project formatting/linting
- [ ] Have clear commit message (Conventional Commits)
- [ ] No TODOs without issue numbers

### Always
- Commit early and often with meaningful messages

### Never
- Use `--no-verify` to bypass hooks
- Disable tests instead of fixing them
- Commit code that doesn't compile
- Reference "Copilot" or "AI-generated" in messages

### Decision Priority
Testability → Readability → Consistency → Simplicity → Reversibility

## Communication

- Keep responses direct; avoid preamble/postamble unless requested.
- Use delta-first structure: lead with changes/findings/actions, then brief background.
- Treat response length guidance as soft targets, not hard limits.
- Keep simple answers to 1-3 sentences; expand detail when safety, correctness, or review quality requires it.
- Avoid unnecessary code comments and refusal explanations.
- Prefer `rg` for text/file search.
- Prefer read/list tools over shell output commands for context gathering.
- Never guess URLs.

## TypeScript Style

### Naming
- `UpperCamelCase` for types, interfaces, components
- `lowerCamelCase` for variables, functions, methods
- `CONSTANT_CASE` for global constants
- Treat acronyms as words: `loadHttpUrl` not `loadHTTPURL`

### Imports
- Named exports only; no default exports
- Use `import type` for type-only imports
- Order: stdlib → third-party → local

### Types
- Prefer `interface` over `type` for object shapes
- Prefer `unknown` over `any`; document exceptions
- Use `prop?` not `prop: Type | undefined`
- Mark immutable properties `readonly`

### Functions
- Use `const`/`let` only; never `var`
- Arrow functions for callbacks
- Function declarations for top-level named functions
- Strict equality (`===`/`!==`) always

## Extended Guides

Load when applicable:
- *Style Guide* -> `docs/STYLE_GUIDE.md` - When writing new modules or unfamiliar with project conventions