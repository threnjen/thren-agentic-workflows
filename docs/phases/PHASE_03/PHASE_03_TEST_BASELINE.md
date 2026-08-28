# Phase 03 Test Baseline

The feature test gate compares against this record. No test that passes here may fail after a
feature. A failure whose test is not named below is a real regression, never an exemption.

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

None. Every test passes at phase start.

An empty exemption list is the strongest form of this gate: any failing test during Phase 03 is
caused by the feature that introduced it. Nothing may be added to this list during the phase.
A test that starts failing is repaired, not exempted.
