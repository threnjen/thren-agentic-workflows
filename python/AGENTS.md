# Agent Guidelines

## Virtual environments
- Use `uv` for environment and dependency management; `pyproject.toml` is the single source of truth for dependencies.
- Create the virtual environment with `uv venv` and install dependencies with `uv sync`.
- Do not use `requirements.txt`; define all dependencies (including dev dependencies) in `pyproject.toml`.

## Base Classes & Data Models
- Use **Pydantic v2** for data models; prefer `model_config = ConfigDict(frozen=True)` by default to enforce immutability.
- Only disable `frozen` when mutability is explicitly required and justified.
- Validate at system boundaries (user input, external APIs); trust internal Pydantic models after construction.

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

### When Stuck (Max 3 Attempts)
1. Document what failed (steps, errors, hypothesis)
2. Research 2-3 alternative implementations
3. Question fundamentals — simpler approach? different abstraction?
4. Try different angle — then STOP and reassess

## Testing

- SHOULD NOT add test unless it can fail for a real defect.
- Strong assertions (`toEqual` over `toBeGreaterThanOrEqual`)

### Property-Based Testing
- Use [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing; include it as a standard dev dependency.
- Prefer Hypothesis strategies over hand-crafted edge-case inputs when testing data ranges, formats, or invariants.
- Combine with unit tests — Hypothesis finds edge cases, unit tests document known behavior.

### When Requirements Change
- Udpate/delete affected tests FIRST, then change code
- Stale tests (for removed behavior) should be deleted, not skipped
- Deprecated functions: remove tests entirely or update to test new stub behavior
- If unsure whether a test is stale: check if the requirement still exists

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

## Extended Guides

Load when applicable:
- *Style Guide* -> `docs/STYLE_GUIDE.md` - When writing new modules or unfamiliar with project conventions
