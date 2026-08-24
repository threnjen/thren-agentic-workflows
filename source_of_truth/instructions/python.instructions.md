---
description: "Hard Python rules that a competent model violates by default — environment, imports, data containers, logging and observability, SQL, async. Audience is source files only: the glob fires for Cursor and Copilot whenever Python code is open, and costs nothing otherwise. Harnesses that inline instructions into agents reach these rules through the python-standards skill instead, routed by language-standards.instructions.md. PAIRED ASSET: skills/python-standards/SKILL.md restates these rules — change both together."
applyTo: "**/*.py,**/pyproject.toml"
---

# Python Rules

- **Environment:** `uv` for everything — never bare `pip` or `python`. `uv run <script>`, `uv pip install -e ".[extras]"`. After any `pyproject.toml` change, re-run `uv pip install -e ".[extras]"`; `uv sync` alone does not re-evaluate editable installs.
- **Packaging:** never manipulate `sys.path` or `PYTHONPATH`. Fix imports through `pyproject.toml`. Every importable directory has an `__init__.py`.
- **Imports:** at the top of the file only — never inside a function, method, conditional, or loop. No new `import *`.
- **Data containers:** `@dataclass` for data you own (mutable defaults via `field(default_factory=...)`); Pydantic v2 `BaseModel` for anything crossing a trust boundary — user input, API responses, config; `TypedDict` for dict shapes you don't own; a full class only when there is real behavior.
- **Logging:** one module-level `logger = logging.getLogger(__name__)`, lazy `%s` args, `exc_info=True` on errors. `print` only for deliberate CLI output.
- **Observability:** log every boundary call, its outcome, every unpredictable branch, and every caught exception, with the values involved. Instrument on the way in, never after a bug appears.
- **SQL:** parameterized queries only — never f-strings.
- **Async:** never call blocking I/O inside an `async` function.
- **Tooling:** Ruff and Pyright (`strict` on greenfield) are enforced. Never disable them, never add ignore comments.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: python."* Then proceed normally.
