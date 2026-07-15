# Hook test setup

The hook runtime remains Python-standard-library-only. Pytest and coverage are
development dependencies used by the repository test suite.

Create an isolated environment and install the developer dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Run the complete pytest suite, the hook-framework coverage gate, and the
pre-existing unittest baseline:

```bash
.venv/bin/python -m pytest tests/
.venv/bin/python -m pytest tests/hooks/ \
  --cov=.github/hooks/lib \
  --cov-report=term-missing \
  --cov-fail-under=50
python3 -m unittest discover -s tests -v
```

Stage 0 was recorded with Python 3.12.6. Before the framework implementation
exists, the hook contract suite is expected to fail with a message identifying
the missing `.github/hooks/lib/framework.py`; this is the red test baseline for
Stage 1. The two pre-existing unittest tests must remain green throughout.
