# DEFUNCT — Prompt-Injection Scanner

**Status:** Intentionally inert. Wired nowhere. Unrunnable by design.

This directory retains the prompt-injection scanner code as an explicitly **defunct
artifact**, per the 2026-07-17 hook cancellation decision. It is **not part of the
product** and **must not be counted in asset inventories**.

## What remains here

- `lib/injection_scanner.py` — scanner logic (self-contained; imports no framework)
- `lib/__init__.py` — package init that re-exports from the now-deleted `.framework`
- `scripts/injection-scanner.py` — scanner CLI (imports `from lib` / `from lib.injection_scanner`)
- `injection-scanner.json` — scanner manifest
- `config/injection-patterns.json`, `config/injection-allowlist.json` — scanner configs

## Why it is unrunnable

The hook framework core (`lib/framework.py`) has been **deleted**. While
`lib/injection_scanner.py` itself does not import it, the package entry point
(`lib/__init__.py`) and the CLI script (`scripts/injection-scanner.py`) do. As a result,
the package and CLI entry points are **unimportable by design**. No compatibility shim,
stub, or edit has been added to make them importable. Nothing in the product wires,
invokes, or propagates this code.

## No security claim

This marker makes **no claim of protection**. The scanner provides no active defense; it
is inert. Do not treat its presence as a security control.

## Archival record

Git history is the archival record for the retired hook framework and its scanner. This
snapshot is retained only as a coherent, unrunnable historical artifact.
