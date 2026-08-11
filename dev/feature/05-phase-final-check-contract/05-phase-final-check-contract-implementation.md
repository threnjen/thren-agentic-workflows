# Implementation Record: Phase Final-Check Contract

## Summary

Created the shared `phase-final-check` skill. It defines the cold-start reading and spawn boundary,
the six eligible finding categories, evidence and five-finding cap, zero-finding response, and
read-only/no-gating limits for Features 06 and 07 to consume by reference.

## Sibling Features

Scanned sibling plans 01–04, 06, and 07 as required. Features 01–04 are unrelated Unity/corpus
work. Feature 06 adds the hidden reviewer and Feature 07 wires the Refiner and owns focused semantic
and mutation-tested guards; both depend on this skill and its selected slug `phase-final-check`.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | Feature 07 focused contract guard (planned) | Parse valid skill frontmatter and shared-reference contract | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:1-8` | PENDING | PENDING |
| AC2 | AC2 | Feature 07 focused contract guard (planned) | Check supplied phase/repository boundary, optional committed context, and missing-file behavior | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:10-17` | PENDING | PENDING |
| AC3 | AC3 | Feature 07 focused contract guard (planned) | Check two-path-only spawn payload and forbidden briefing content | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:12,19-22` | PENDING | PENDING |
| AC4 | AC4 | Feature 07 focused contract guard (planned) | Derive and verify the exact six finding categories | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:24-33` | PENDING | PENDING |
| AC5 | AC5 | Feature 07 focused contract guard (planned) | Check evidence citation, consolidation, weak-observation omission, no grading, and cap | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:35-38,42-43` | PENDING | PENDING |
| AC6 | AC6 | Feature 07 focused contract guard (planned) | Check explicit truncation disclosure and plain zero-findings state | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:42-44` | PENDING | PENDING |
| AC7 | AC7 | Feature 07 focused contract guard (planned) | Check excluded sync state, grading/gating, retries, writes, and edits | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `source_of_truth/skills/phase-final-check/SKILL.md:35-38,45-50` | PENDING | PENDING |
| AC8 | AC8 | `test_agent_corpus_invariants.py` | Validate skill frontmatter and duplicate-block safety; semantic guards remain downstream | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-corpus-final.txt` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | New terse shared skill with valid frontmatter | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Slug selected as `phase-final-check`. |
| AC2 | Newcomer reading boundary and optional context behavior | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Missing optional context is non-fatal. |
| AC3 | Spawner blindness and exactly two path inputs | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Conversation, summaries, settled-area briefing, and assessment are prohibited. |
| AC4 | Exactly six eligible finding categories | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Listed once in the qualifying-findings section. |
| AC5 | Evidence citation, consolidation, weak-observation omission, no rating, and cap | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Every finding needs a document location or concrete repository fact. |
| AC6 | Truncation disclosure and plain zero-findings response | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Response states are explicit. |
| AC7 | Excluded synchronization, judgments/gates, retries, and writes | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Consumer workflow and error handling remain out of scope. |
| AC8 | Dense reusable contract without consumer duplication | Complete | `source_of_truth/skills/phase-final-check/SKILL.md` | Existing corpus suite passed; downstream semantic guards are Feature 07 scope. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/phase-final-check/SKILL.md` | Create | Added the shared final-check contract with valid `name` and `description` frontmatter. | Provides one reusable contract for Features 06 and 07. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|-----|
| None | None | No tests added, per plan. | Feature 07 owns focused semantic and mutation-tested guards. |

## Test Results
- **Execution**: executed-failing
- **Command**: `uv run pytest tests/`
- **Results artifact**: `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-final.txt`
- **Baseline**: 230 passed, 12 failed (before implementation)
- **Final**: 229 passed, 13 failed (after implementation)
- **New tests added**: 0
- **Affected suites run**: `uv run pytest tests/test_agent_corpus_invariants.py` (7 passed; `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-corpus-final.txt`); `uv run pytest tests/test_propagate_master_assets.py` (43 passed, 1 failed; `dev/feature/05-phase-final-check-contract/05-phase-final-check-contract-propagation.txt`); full suite above
- **Regressions**: One expected generated fixed-point failure because the new source skill was not propagated; the other 12 failures match the recorded baseline (PR Review collision, wildcard `applyTo`, and ten missing Unity reference-asset failures). The corpus suite is green.

## Deviations from Plan

- A concurrent/inadvertent propagation run created untracked generated copies under
  `ports/{claude,codex,github,opencode}/skills/phase-final-check/`. This implementation did not edit
  or remove them. Propagation remains a maintainer step; the generated copies must be reviewed and
  regenerated from the final source before synchronization is considered complete.

## Gaps

- Feature 07's proposed consolidated phase-final-check contract-guard module does not exist yet and
  was not executed. Its semantic, deletion/negation mutation, and combined smoke evidence remains
  downstream scope.
- No real Phase - Refiner session was run; runtime usefulness and cold-start obedience remain Feature
  07/manual-smoke scope.

## Reviewer Focus Areas

- Verify the six category terms, optional committed-context boundary, and two-path blindness payload
  remain one authoritative contract for Features 06 and 07.
- Verify no consumer workflow, gating, retry, synchronization, or write authority is added to this
  skill, and confirm generated ports are regenerated by the maintainer from source.
