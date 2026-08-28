# Phase 03 Test Baseline

This records the green suite Phase - Execute requires before it starts. The orchestrator now
runs the suite itself at its Step 1 preflight and stops the run on any failing or unrunnable
test, so this file documents the measured result rather than acting as a list a gate consults.

## Environment

The suite runs from `.venv`, built with `uv venv .venv --python 3.12` and populated from
`requirements-dev.txt`. `.venv` is gitignored, so rebuilding it produces no diff. Rebuild it
from scratch rather than repairing it — the previous virtualenv carried a shebang pointing at
the repository's pre-rename path and could not start.

## Command

```
.venv/bin/pytest -q
```

## Result at phase start

```
376 passed, 307 subtests passed
```

## Exempt tests

None, and the concept is retired. Because the phase cannot begin red, no test can be excused
during it. Any failing test is caused by the feature that introduced it and is repaired by the
agent that touched the code — the Implementer, then 03c. A feature whose gate still fails is a
production blocker, never a completed feature.
