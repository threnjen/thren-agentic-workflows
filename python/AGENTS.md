# Python AGENTS.md

## Environment

- `pyproject.toml` at root is the source of truth. Build backend: `hatchling`.
- Never manipulate `sys.path`. Fix imports structurally via `pyproject.toml`.
- Every importable directory must have `__init__.py`.
- Use `uv` for all environment operations — never bare `pip` or `python`.
  - `uv pip install -e ".[extras]"` not `pip install`
  - `uv run python script.py` not `python script.py`
- After any `pyproject.toml` change, run `uv pip install -e ".[extras]"` — `uv sync` alone does not re-evaluate editable installs.

## Tooling

Ruff and Pyright strict are enforced in CI and pre-commit. Do not disable them.

```toml
# pyproject.toml
[tool.pyright]
typeCheckingMode = "strict"

[tool.ruff]
select = ["E", "F", "B", "I", "UP"]
```

On existing unannotated code, start Pyright at `standard`; move to `strict` as annotations are added. Greenfield: `strict` from day one.

## Style

Comply with PEP 8 and the Google Python Style Guide. The rules below cover what falls through.

### Data Containers

| Use case | Tool |
|---|---|
| Data-carrying object you own | `@dataclass` |
| External input / API response / config | `Pydantic v2 BaseModel` |
| Object with meaningful behavior or lifecycle | `class` |
| Dict shape you read but don't own | `TypedDict` |

- If you're writing `__init__` only to assign attributes, use `@dataclass`.
- Use `field(default_factory=...)` for mutable defaults in dataclasses — never a bare `[]` or `{}`.
- Pydantic: default to `model_config = ConfigDict(frozen=True)`. Disable only when mutability is explicitly required.
- Validate at system boundaries (user input, external APIs); trust internal models after construction.

### Classes

A class is justified when it carries state, uses inheritance, or implements a shared interface. Otherwise, use module-level functions.

- Never do I/O or heavy computation in `__init__`. Use a `@classmethod` factory (`from_file`, `from_config`, etc.).

### None and Truthiness

Use `if not value` only when all falsy values (`None`, `0`, `""`, `[]`) are equivalent in meaning. When `0` or `""` is a valid value, be explicit:

```python
if value is None: ...
if len(items) == 0: ...
```

### Comprehensions

Prefer comprehensions over append loops. Use generators when you don't need the full list in memory. Avoid nested comprehensions (more than one `for` clause) — extract a named generator function instead.

### Imports

- No `from module import *`.
- Relative imports within a package; absolute imports across packages.
- `..` chains beyond two levels signal the package structure needs flattening.

### Global State

Do not use module-level mutable objects that functions modify as a side effect. Pass state explicitly as arguments.

### Async

Never call blocking I/O inside an `async` function. Use async-native libraries (`aiofiles`, `asyncpg`, etc.) or offload to `loop.run_in_executor`.

### Context Managers

Use `with` for anything that acquires and releases a resource — files, DB connections, locks. Never rely on manual cleanup. Implement `__enter__`/`__exit__` or use `@contextlib.contextmanager` for custom resources.

### Logging

Never use `print` for anything except deliberate CLI output. Use `logging` everywhere else.

```python
import logging
logger = logging.getLogger(__name__)  # one per file, named __name__

logger.debug("Processing record %s", record_id)
logger.error("Failed to connect", exc_info=True)
```

Never configure logging inside a library — only in application entry points.

### SQL

Always use parameterized queries. Never use f-strings in SQL.

```python
# ❌
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# ✅
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

## Testing

- Add tests only when they can fail for a real defect.
- Prefer strong assertions over weak threshold checks.
- Cover realistic edge cases, boundaries, and error paths.
- When requirements change: update or delete affected tests first, then change code. Delete stale tests; do not skip them.
- Use [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing on data ranges, formats, and invariants. Include as a standard dev dependency.

## Quality

Every commit must compile, pass all tests, follow formatting/linting, and use Conventional Commits. No TODOs without issue numbers.

**Never:**
- Use `--no-verify` to bypass hooks
- Disable or skip tests instead of fixing them
- Reference AI tools in commit messages

Decision priority: **Testability → Readability → Consistency → Simplicity → Reversibility**

## Principles

- Prefer small, reversible changes. Match existing patterns before introducing new structure.
- Fail fast with descriptive errors; never silently swallow exceptions.
- Keep responsibilities narrow and data flow explicit.

## When Stuck

After 3 failed attempts: document what failed, research 2–3 alternatives, question whether a simpler abstraction exists, then stop and reassess.

## Communication

- Lead with changes/findings/actions; background after.
- Simple answers in 1–3 sentences; expand only when correctness or safety requires it.
- Prefer `rg` for text/file search. Never guess URLs.

