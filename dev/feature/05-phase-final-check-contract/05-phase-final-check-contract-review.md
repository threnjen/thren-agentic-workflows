# Review Record: Phase Final-Check Contract

## Summary

The retry fixes are present in the source skill: missing optional context explicitly continues with
the supplied phase document and available committed repository facts, and grades, gates, and
blocking thresholds are explicitly excluded. Static traceability is complete for AC1–AC8, and the
existing corpus invariant is executed-green. The Feature 07 focused semantic/mutation/smoke guard
is intentionally downstream and absent, so AC1–AC7 remain unverified by authoritative execution.
Generated outputs remain intentionally unpropagated pending maintainer propagation.

## Verdict
<!-- Approved | Approved with Reservations | Changes Requested -->
<!-- Neither Approved nor Approved with Reservations is permitted while the authoritative tests for the changed behavior are not-executed. -->
Changes Requested

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:1-8` | Valid shared skill is present; the authoritative downstream focused guard is not-executed. |
| AC2 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:12-18` | Reading boundary and explicit missing-context continuation are present; focused boundary guard is not-executed. |
| AC3 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:12,20-23` | Exactly two path inputs and forbidden briefing content are explicit; focused guard is not-executed. |
| AC4 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:25-34` | Exact six categories are listed once; category guard is not-executed. |
| AC5 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:36-39,43-47` | Evidence, consolidation, omission, no rating, and cap rules are explicit; semantic guard is not-executed. |
| AC6 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:43-45` | Truncation and zero-finding states are explicit; response guard is not-executed. |
| AC7 | Unverified | `source_of_truth/skills/phase-final-check/SKILL.md:36-39,46-50` | Synchronization, judgments/grades/gates/thresholds, retries, writes, and edits are excluded; exclusion guard is not-executed. |
| AC8 | Verified (executed-green corpus) | `source_of_truth/skills/phase-final-check/SKILL.md:1-50` | `test_agent_corpus_invariants.py` passed 7/7; generated fixed-point validation remains pending propagation. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Missing optional context was only described as non-fatal, without explicitly requiring continuation with the supplied phase document and available repository facts. | Medium | `source_of_truth/skills/phase-final-check/SKILL.md:16-18` | AC2 | Fixed (prior retry; verified present) |
| 2 | The exclusion list did not explicitly prohibit grades, gates, or blocking thresholds. | Medium | `source_of_truth/skills/phase-final-check/SKILL.md:36-39` | AC7 | Fixed (prior retry; verified present) |
| 3 | The authoritative Feature 07 focused semantic, deletion/negation mutation, and combined smoke guard is intentionally downstream and remains absent/not-executed. | High | `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-plan.md:78,85-87` | AC1-AC7 | Open (downstream verification) |
| 4 | The committed tree is not at a generated fixed point because the new source skill has not been propagated; propagation is intentionally maintainer-owned. | High | `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-review-full.txt:146,668` | AC8 | Open (maintainer propagation) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| None | No source fixes were needed; prior retry fixes for Issues 1–2 are present. | — |

## Remaining Concerns

- Issue #3: the Feature 07 focused semantic, mutation, and combined smoke guard remains downstream work required before AC1–AC7 can be execution-verified; no source fix is indicated.
- Issue #4: generated outputs must be propagated and the fixed-point suite rerun by the maintainer; propagation was not run in this review.
- No source files were edited during this re-review. The prior retry fixes remain present at `source_of_truth/skills/phase-final-check/SKILL.md:16-18,36-39`.

## Test Coverage Assessment

- Covered: AC8 structural frontmatter and duplicate-block checks.
- Missing: Feature 07 focused semantic/deletion-negation/mutation/smoke guard for AC1-AC7; no real Phase - Refiner cold-start session.
- Executed-green: `uv run pytest tests/test_agent_corpus_invariants.py` — `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-rereview-corpus.txt` — total 7, passed 7, failed 0.
- Executed-green: `uv run pytest tests/test_agent_corpus_invariants.py` — `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-review-corpus.txt` — total 7, passed 7, failed 0.
- Executed-failing: `uv run pytest tests/test_propagate_master_assets.py` — `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-review-propagation.txt` — total 44, passed 43, failed 1 (pre-existing wildcard `applyTo` failure).
- Executed-failing: `uv run pytest tests/` — `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-review-full.txt` — total 242, passed 229, failed 13 (12 recorded baseline failures plus the expected source-only propagation fixed-point failure).

## Risk Summary

- `source_of_truth/skills/phase-final-check/SKILL.md:12-50` is statically complete, but runtime cold-start obedience and semantic guard behavior are unverified until Feature 07 executes its focused guard.
- `05-phase-final-check-contract-review-full.txt:146` shows generated fixed-point failure until maintainer propagation occurs.
- Feature 07's focused semantic/mutation/smoke guard is the authoritative evidence and is not-executed.
