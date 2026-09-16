---
name: python-standards
description: "The complete Python standard — hard rules plus depth: uv command cookbook, pyproject/hatchling packaging layout, when a class is justified, classmethod factories, truthiness intent, generators over nested comprehensions, import scope, global state, custom context managers, and the escape hatch for blocking calls in async. Use when: setting up or debugging a Python environment or package layout, deciding between a class and a module of functions, or needing the rationale or edge case behind a rule below."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Python Standards

The Rules section is the standard. Later sections explain why and cover edge cases. They include one example per rule when that example earns its place.

PAIRED ASSET: `instructions/python.instructions.md` carries the same rules for Cursor and Copilot, which reach them by file glob rather than by loading this skill. Change both together.

## Rules

- **Environment:** `uv` for everything — never bare `pip` or `python`. `uv run <script>`, `uv pip install -e ".[extras]"`. After any `pyproject.toml` change, re-run `uv pip install -e ".[extras]"`; `uv sync` alone does not re-evaluate editable installs.
- **Packaging:** never manipulate `sys.path` or `PYTHONPATH`. Fix imports through `pyproject.toml`. Every importable directory has an `__init__.py`.
- **Imports:** at the top of the file only — never inside a function, method, conditional, or loop. No new `import *`.
- **Data containers:** `@dataclass` for data you own (mutable defaults via `field(default_factory=...)`); Pydantic v2 `BaseModel` for anything crossing a trust boundary — user input, API responses, config; `TypedDict` for dict shapes you don't own; a full class only when there is real behavior.
- **Logging:** one module-level `logger = logging.getLogger(__name__)`, lazy `%s` args, `exc_info=True` on errors. `print` only for deliberate CLI output.
- **Observability:** log every boundary call, its outcome, every unpredictable branch, and every caught exception, with the values involved. Instrument on the way in, never after a bug appears.
- **SQL:** parameterized queries only — never f-strings.
- **Async:** never call blocking I/O inside an `async` function.
- **Tooling:** Ruff and Pyright (`strict` on greenfield) are enforced. Never disable them, never add ignore comments.

## uv

Use one virtual environment at `.venv/` in the repository root. Do not activate it. Run commands with `uv run`.

| Task | Command |
|---|---|
| First-time setup | `uv sync` (`--extra dev` for optional groups) |
| After editing `pyproject.toml` | `uv pip install -e ".[extras]"` |
| Run an entry point or script | `uv run <command>` / `uv run path/to/script.py` |
| Add / remove a dependency | `uv add <pkg>` (`--dev`, `--optional <group>`) / `uv remove <pkg>` |
| Inspect the venv | `uv pip list`, `which python` → `.venv/bin/python` |

`uv add` edits `pyproject.toml` and updates `uv.lock`. Commit `uv.lock`. It makes `uv sync` reproducible across machines and CI.

Force the editable reinstall after adding a package directory, changing `[tool.hatch.build]`, or adding an `__init__.py`.

## Packaging layout

`sys.path` hacks are invisible to static analysis and break across environments. They always indicate unregistered packages. When importable code lives in a subdirectory, declare that directory as the source root. `sources` is a list of directories:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
sources = ["src-python"]

[tool.hatch.build.targets.wheel]
packages = ["src-python/db", "src-python/core"]
```

## Classes

Use a class when it has state, inheritance, or a shared interface. Use a module of functions when a class's methods do not share state through `self` and the class has no polymorphic role. Treat the class choice as a simplicity judgment. See [simplicity-review](../simplicity-review/SKILL.md) for the general form. An abstract base with two implementations is justified even without instance state. Do not use a class as a bag of static helpers.

If `__init__` would only assign attributes, use `@dataclass`.

Do not perform I/O or heavy computation in `__init__`. A constructor that reads a file cannot be tested or reused. Use a classmethod factory:

```python
class Pipeline:
    def __init__(self, data: str):
        self.data = data

    @classmethod
    def from_file(cls, path: str) -> "Pipeline":
        with open(path) as f:
            return cls(f.read())
```

## Truthiness

Use `if not value` when `None`, `0`, `""`, `[]`, and `{}` all mean the same thing. Do not use it when `0` or `""` is a real value. For example, `if not score` hides a score of zero. When the distinction matters, use `if value is None`, `if len(items) == 0`, or `if count == 0`.

## Comprehensions

Use a generator when you do not need the full list in memory: `sum(x**2 for x in large_sequence)`.

Avoid more than one `for` clause in a comprehension. Extract a named generator function instead:

```python
def positive_values(matrix):
    for row in matrix:
        for x in row:
            if x > 0:
                yield x

result = [f(x) for x in positive_values(matrix)]
```

## Import scope

Use relative imports within a package (`from .helpers import truncate`) and absolute imports across packages (`from mypackage.config import Settings`). If a `..` chain exceeds two levels, flatten the package structure.

Function-local imports usually try to avoid a circular import. Fix the cycle. Extract the shared piece into a third module.

If a file already contains `import *`, leave it. Do not extend the pattern.

## Global mutable state

A module-level object that functions mutate as a side effect creates a hidden dependency. Tests cannot isolate that dependency. Pass the object in:

```python
def get(key: str, cache: dict) -> str:
    cache[key] = fetch(key)
    return cache[key]
```

## Context managers

When your class holds a resource, implement `__enter__`/`__exit__`. Do not make callers remember cleanup. For simple acquire and release, use `contextlib.contextmanager` instead of a full class:

```python
@contextmanager
def managed_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        resource.release()
```

## Async

Prefer an async-native library (`aiofiles`, `asyncpg`, `httpx`). When a blocking call is genuinely unavoidable, offload it. This is the only permitted exception:

```python
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(None, blocking_function, arg)
```

## Logging

`print` has no severity. A caller cannot silence or redirect it without a code change, and log aggregators do not receive it. `exc_info=True` captures the full traceback for free. Do not configure logging inside a library. Configure logging at the application entry point only.

Log every step. A module that logs only errors tells you that a run failed, but not why.

```python
logger.debug("fetching order %s from %s", order_id, url)
resp = await client.get(url)
logger.debug("order %s returned %s in %.3fs", order_id, resp.status_code, elapsed)
```

Lazy `%s` args cost nothing when the log level is off. A DEBUG line on every step is free in production. Put identifying values in the message, such as an id, a path, a count, or a duration. Log the caught exception with `logger.exception(...)` or `exc_info=True`. Log the state that produced it in the same call. Redact secrets at the call site.

## Tests

Use `uv run pytest` for the full suite. Use `uv run pytest path/to/test.py -x` for one file. The `test-execution-evidence.instructions.md` instruction governs TDD discipline and test-status reporting, not this skill.
