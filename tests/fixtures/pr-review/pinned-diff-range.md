# PR Review Pinned Fixture: Base/Head Diff Range

Reproducible input for the `04 PR - Review` fixture dry run. Both commits are
reachable from `main`, so the range resolves in every clone of this repository.

- **Base SHA**: `f5ab960e5697756538f94430327e2a68eb113822`
- **Head SHA**: `e6ff28a36293697aebf62155ae0048115c4aecca`
- **Shape**: 3 commits, 26 files, 1288 insertions
- **Merge-base check**: `git merge-base <head> <base>` returns the base, so the
  head descends from the base — a genuine PR shape, not two arbitrary commits.

## Why This Pair

The pair implied by the orchestrator's base-derivation evidence
(`e3398c7..ae9823a`) is 242 files and ~27k insertions — a whole-phase diff.
Dry-running seven evaluators against that is slow, costly, and a poor proxy for
a PR. This range is the `com.threnjen.visual-verification` UPM package landing
(v0.1.0 → v0.2.1): PR-sized, additive, self-contained, and touching code,
packaging metadata, and docs — a representative spread for the evaluator roster.

## Usage

Run `04 PR - Review` with the base and head SHAs above. Reports land under
`dev/pr-review/<base-sha-short>-<UTC-timestamp>/`, which stays gitignored; this
fixture lives under `tests/fixtures/`, outside `dev/`, so it stays tracked.

Do not re-point this fixture: tests pin both SHAs and the range's shape
(`tests/test_pr_review_orchestrator.py`).
