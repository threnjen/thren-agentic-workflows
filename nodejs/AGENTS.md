# Agent Guidelines

## Package Management
- `package.json` is the single source of truth for all dependencies (prod and dev).
- Always commit `package-lock.json`; use `npm ci` in CI/automated environments for reproducible installs.
- Install dev-only tools (e.g. `fast-check`, `vitest`) with `npm install --save-dev`.

## Principles

- Incremental progress over big bangs — small changes that compile and pass tests
- Learn from existing code — find 3 similar features, study patterns before implementing
- Pragmatic over dogmatic — adapt to project reality
- Clear intent over clever code — be boring and obvious
- Single responsibility per function/class
- Composition over inheritance; interfaces over singletons
- Explicit data flow; fail fast with descriptive errors
- Include context for debugging; handle errors at appropriate level; never silently swallow exceptions
- If you need to explain it, it's too complex

## Process

### Implementation Flow
1. **Plan** — study existing patterns.
2. **Test** — write test first (red)
3. **Implement** — minimal code to pass (green)
4. **Refactor** — clean up with tests passing
5. **Commit** — clear message explaining "why"

### When Stuck (Max 3 Attempts)
1. Document what failed (steps, errors, hypothesis)
2. Research 2-3 alternative implementations
3. Question fundamentals — simpler approach? different abstraction?
4. Try different angle — then STOP and reassess

## Testing

### TDD Workflow
- Write tests BEFORE implementation
- Confirm tests fail first (no mock implementations)
- Commit tests separately from implementation
- Do NOT modify tests during implementation
- Run full suite to catch regressions

### Test Quality
- SHOULD NOT add test unless it can fail for real defect
- SHOULD ensure description matches expect assertion
- Parameterize inputs (no magic numbers/strings)
- Compare to independent expectations, not function output
- Strong assertions (`toEqual` over `toBeGreaterThanOrEqual`)
- Test edge cases, boundaries, realistic input
- One assertion per test; clear names describing scenario
- Group under `describe(functionName)`

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
- [ ] Check plan is up-to-date before commit

### Always
- Commit early and often with meaningful messages

### Never
- Use `--no-verify` to bypass hooks
- Disable tests instead of fixing them
- Commit code that doesn't compile
- Reference "Claude" or "AI-generated" in messages

### Decision Priority
Testability → Readability → Consistency → Simplicity → Reversibility

## Communication

- No preamble/postamble unless requested
- No code comments unless asked
- No explanations for refusals
- Use ripgrep (`rg`) not `grep`/`find`
- Use Read/LS tools not `cat`/`head`/`tail`/`ls`
- Never guess URLs

## Agent Operations

### Context Clearing
Clear at 60k tokens or 30% context:
1. Write progress to `.md` file
2. `/clear` the context
3. Start fresh session reading the `.md` file

### Subagents
- Main agent spawns Task(...) clones for parallel work
- Fresh context = better critique for self-review
- Review for: spaghetti code, API changes, missing error handling, security issues

### Self-Review Checklist
- [ ] Logic easy to follow?
- [ ] No unnecessary imports/functions/comments?
- [ ] Error handling complete?
- [ ] Security vulnerabilities addressed?

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