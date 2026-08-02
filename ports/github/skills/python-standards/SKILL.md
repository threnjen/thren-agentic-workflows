---
name: python-standards
description: "The complete Python standard — hard rules plus depth: uv command cookbook, pyproject/hatchling packaging layout, when a class is justified, classmethod factories, truthiness intent, generators over nested comprehensions, import scope, global state, custom context managers, and the escape hatch for blocking calls in async. Use when: setting up or debugging a Python environment or package layout, deciding between a class and a module of functions, or needing the rationale or edge case behind a rule below."
---

# Python Standards

Self-contained: the Rules section is the standard; everything after it is the why, the edge cases, and the one example per rule that earns its place.

PAIRED ASSET: `instructions/python.instructions.md` carries the same rules for Cursor and Copilot, which reach them by file glob rather than by loading this skill. Change both together.

## Rules

- **Environment:** `uv` for everything — never bare `pip` or `python`. `uv run <script>`, `uv pip install -e ".[extras]"`. After any `pyproject.toml` change, re-run `uv pip install -e ".[extras]"`; `uv sync` alone does not re-evaluate editable installs.
- **Packaging:** never manipulate `sys.path` or `PYTHONPATH`. Fix imports through `pyproject.toml`. Every importable directory has an `__init__.py`.
- **Imports:** at the top of the file only — never inside a function, method, conditional, or loop. No new `import *`.
- **Data containers:** `@dataclass` for data you own (mutable defaults via `field(default_factory=...)`); Pydantic v2 `BaseModel` for anything crossing a trust boundary — user input, API responses, config; `TypedDict` for dict shapes you don't own; a full class only when there is real behavior.
- **Logging:** one module-level `logger = logging.getLogger(__name__)`, lazy `%s` args, `exc_info=True` on errors. `print` only for deliberate CLI output.
- **SQL:** parameterized queries only — never f-strings.
- **Async:** never call blocking I/O inside an `async` function.
- **Tooling:** Ruff and Pyright (`strict` on greenfield) are enforced. Never disable them, never add ignore comments.

## uv

One venv at `.venv/` in the repo root. Never activate it — `uv run` does.

| Task | Command |
|---|---|
| First-time setup | `uv sync` (`--extra dev` for optional groups) |
| After editing `pyproject.toml` | `uv pip install -e ".[extras]"` |
| Run an entry point or script | `uv run <command>` / `uv run path/to/script.py` |
| Add / remove a dependency | `uv add <pkg>` (`--dev`, `--optional <group>`) / `uv remove <pkg>` |
| Inspect the venv | `uv pip list`, `which python` → `.venv/bin/python` |

`uv add` edits `pyproject.toml` and updates `uv.lock`. Commit `uv.lock` — it is what makes `uv sync` reproducible across machines and CI.

Force the editable reinstall after adding a package directory, changing `[tool.hatch.build]`, or adding an `__init__.py`.

## Packaging layout

`sys.path` hacks are invisible to static analysis and break across environments. They are always a symptom of unregistered packages. When importable code lives in a subdirectory, declare it as the source root — note `sources` is a list of directories:

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

Justified by state, inheritance, or a shared interface. A class whose methods don't share state through `self` and has no polymorphic role is a module of functions. Applying this is a simplicity judgement — see [simplicity-review](../simplicity-review/SKILL.md) for the general form. An abstract base with two implementations is justified even with no instance state; a bag of static helpers is not.

If you are about to write `__init__` only to assign attributes, the answer is `@dataclass`.

No I/O or heavy computation in `__init__` — a constructor that reads a file cannot be tested or reused. Use a classmethod factory:

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

`if not value` catches `None`, `0`, `""`, `[]`, `{}` at once. That is correct only when all of them mean the same thing. It is wrong wherever `0` or `""` is a real value — `if not score` hides a score of zero. When the distinction matters: `if value is None`, `if len(items) == 0`, `if count == 0`.

## Comprehensions

Use a generator when the full list isn't needed in memory: `sum(x**2 for x in large_sequence)`.

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

Relative imports within a package (`from .helpers import truncate`), absolute across packages (`from mypackage.config import Settings`). A `..` chain beyond two levels means the package structure needs flattening, not more dots.

Function-local imports are usually an attempt to dodge a circular import. Fix the cycle instead — extract the shared piece into a third module.

If `import *` already exists in a file, leave it; do not extend the pattern.

## Global mutable state

A module-level object that functions mutate as a side effect is a hidden dependency and untestable. Pass it in:

```python
def get(key: str, cache: dict) -> str:
    cache[key] = fetch(key)
    return cache[key]
```

## Context managers

When you own a class that holds a resource, implement `__enter__`/`__exit__` rather than making callers remember cleanup. For the simple acquire/release case, `contextlib.contextmanager` beats a full class:

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

Prefer an async-native library (`aiofiles`, `asyncpg`, `httpx`). When a blocking call is genuinely unavoidable, offload it — this is the only sanctioned escape hatch:

```python
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(None, blocking_function, arg)
```

## Logging

`print` has no severity, cannot be silenced or redirected without a code change, and does not reach log aggregators. `exc_info=True` captures the full traceback for free. Never configure logging inside a library — configuration belongs to the application entry point only.

## Tests

`uv run pytest`; `uv run pytest path/to/test.py -x` for a single file. TDD discipline and test-status reporting are governed by `test-execution-evidence.instructions.md`, not here.
