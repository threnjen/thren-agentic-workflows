# Agent Guidelines

## Virtual environments
- Use `uv` for environment and dependency management; `pyproject.toml` is the single source of truth for dependencies.
- Create the virtual environment with `uv venv` and install dependencies with `uv sync`.
- Do not use `requirements.txt`; define all dependencies (including dev dependencies) in `pyproject.toml`.

## Base Classes & Data Models
- Use **Pydantic v2** for data models; prefer `model_config = ConfigDict(frozen=True)` by default to enforce immutability.
- Only disable `frozen` when mutability is explicitly required and justified.
- Validate at system boundaries (user input, external APIs); trust internal Pydantic models after construction.

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
- Prefer strong assertions over weak threshold checks.
- Cover realistic edge cases, boundaries, and error paths.

### Property-Based Testing
- Use [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing; include it as a standard dev dependency.
- Prefer Hypothesis strategies over hand-crafted edge-case inputs when testing data ranges, formats, or invariants.
- Combine with unit tests — Hypothesis finds edge cases, unit tests document known behavior.

### When Requirements Change
- Update/delete affected tests FIRST, then change code
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

## Extended Guides

Load when applicable:
- *Style Guide* -> `docs/STYLE_GUIDE.md` - When writing new modules or unfamiliar with project conventions
