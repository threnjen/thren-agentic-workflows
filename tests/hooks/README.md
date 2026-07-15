# Hook test setup

The hook runtime remains Python-standard-library-only. Pytest and coverage are
development dependencies used by the repository test suite.

Create an isolated environment and install the developer dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Run the complete pytest suite, the hook-framework coverage gate, and the
stdlib compatibility baseline:

```bash
.venv/bin/python -m pytest tests/
.venv/bin/python -m pytest tests/hooks/ \
  --cov=.github/hooks/lib \
  --cov-report=term-missing \
  --cov-fail-under=50
python3 -m unittest discover -s tests -v
```

Stage 0 was recorded with Python 3.12.6. The historical pre-framework red state
and two-test unittest baseline are no longer current. Phase 02 retained a fresh
14-test stdlib compatibility baseline before Feature 07 and adds propagation
cases thereafter; use current collection/results rather than the historical
count as the release gate.
