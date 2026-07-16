# Review Record: 06-readiness-synthesis

## Summary

The remediation retry resolves the prior High finding: 05i now declares the
existing `fetch` capability for narrowly scoped, read-only remote git-history
and hosted PR/history evidence, and the Claude, OpenCode, and Codex mirrors carry
the same boundary without Bash or execute access. The prior 05l status/report
validation, propagation parity, bounded-evidence label, and NO-GO artifacts
remain intact. Two additional Medium review findings were fixed: a prohibited
`git show` example was removed from the no-shell contract, and the mirror test
now checks the boundary in every generated output.

## Verdict

<!-- Approved | Approved with Reservations | Changes Requested -->
Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified (static; runtime unverified) | `.github/agents/05l-readiness-synthesizer.agent.md:12-18,27-38,65-85`; generated 05l mirrors | Report-only inputs, canonical template/report path, severity ordering, and `prod-code-review` relationship are explicit. Runtime synthesis was not observed. |
| AC2 | Verified (static + 6 direct contract checks; runtime unverified) | `.github/agents/05l-readiness-synthesizer.agent.md:40-63`; `tests/test_readiness_synthesis_agents.py:24-34` | `not-run`/`failed`/`incomplete`, invalid report evidence, canonical hand-off substitution, named missing checks, and the exact below-GO ceiling are explicit. |
| AC3 | Verified (static; runtime unverified) | `.github/agents/05i-learnings-harvester.agent.md:4,21-29,31-50`; generated 05i mirrors | `fetch` is explicitly restricted to read-only remote git-history and hosted PR/history evidence; mutation and Bash/execute fallbacks are denied. If no hosted endpoint exists, the agent records the evidence gap. |
| AC4 | Verified (static + parity test) | Both source agents and generated mirrors; `tests/test_propagate_master_assets.py:86-144` | Shared conventions, return limits, top-tier 05l instruction, and mirror rendering are aligned. |
| AC5 | Partial / bounded evidence only | `dev/phase-final-review/PHASE_05/dry-run-full-flow.md:1-8,18-43`; `evaluator-status.jsonl:1-8`; `readiness-report.md:7-12` | Required artifacts exist and the run is correctly labelled bounded; eight required evaluator checks remain `not-run`, so no complete full-flow proof exists. |
| AC6 | Unverified (static failure-path artifact) | `dev/phase-final-review/PHASE_05/dry-run-failure-path.md:1-19`; `runs/20260715T230000Z-2/readiness-report.md:1-34` | The archive names forced `05d-security-rollup`, records `not-run`, and returns NO-GO; forced runtime execution was not observed. |
| AC7 | Unverified (static fixture copies) | `dry-run-full-flow.md:35-43`; `fixtures/PHASE_05/write-back/PROJECT_ROADMAP.md:3-5`; `PHASE_05_SUMMARY.md:1-6` | Fixture copies show NO-GO and real roadmap paths have no diff; static files do not prove write-back executed without manual editing. |
| AC8 | Unverified (static harvest artifacts) | `05i-learnings-harvester-report.md:10-46`; `drafts/learnings/phase-final-review-report-validation.md:1-29`; `drafts/instructions/orchestrator-report-validation.md:1-28` | Evidence-backed drafts cite real history/ledger/QA sources; an actual 05i fetch/history-mining runtime was not observed. |
| AC9 | Verified (21 unittest parity tests) | `tests/test_propagate_master_assets.py:86-144`; generated Claude/OpenCode/Codex 05i/05l files | The comparison includes both new agents and exact renderer output; 21 tests passed. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|--------|----------|-----------|-----|--------|
| 1 | Prior 05i capability gap: history/PR evidence access was absent from the source and generated tool declarations. | High | `.github/agents/05i-learnings-harvester.agent.md:4,21-29`; Claude/OpenCode/Codex 05i frontmatter/instructions | AC3, AC8 | Fixed |
| 2 | The no-shell 05i contract included a `git show` command example that could contradict its explicit no-execute boundary. | Medium | `.github/agents/05i-learnings-harvester.agent.md:37-41`; generated 05i mirrors | AC3, AC8 | Fixed (applied during this review) |
| 3 | The new mirror safety test asserted detailed history-fetch restrictions only for the source and only a subset of mirror metadata. | Medium | `tests/test_readiness_synthesis_agents.py:67-91` | AC4, AC9 | Fixed (applied during this review) |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

## Fixes Applied
<!-- "None" if none -->

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/agents/05i-learnings-harvester.agent.md`; `claude/agents/z-learnings-harvester.md`; `opencode/agents/05i-learnings-harvester.md`; `codex/agents/z-learnings-harvester.toml` | Replaced the prohibited command example with fetch-only parent/deleted-path recovery and an explicit unavailable-endpoint evidence gap. | 2 |
| `tests/test_readiness_synthesis_agents.py` | Asserted read-only history scope and explicit execute/Bash denial across all three generated mirrors. | 3 |

## Remaining Concerns
<!-- "None" if all clear -->
- AC5–AC8 still require the specified collaboration/manual runtime checks. The retained artifacts are bounded, consistent evidence, not execution proof; the canonical readiness verdict correctly remains NO-GO.
- The declared capability is remote/hosted fetch, not a local-git-history adapter. If the hosted endpoint is unavailable, the orchestrator must supply a verifiable history bundle or preserve the evidence gap; shell/Bash must not be restored.
- `pytest` is unavailable in this environment. The 394-passed/2-failed implementation-record total was not independently reproduced; unittest discovery ran 21 tests successfully.

## Test Coverage Assessment
- Covered: AC1–AC4 source-contract assertions (6 direct passes), AC9 generated-mirror parity (21 unittest passes), TOML parsing, artifact/status/NO-GO consistency assertions, real-roadmap no-diff check, and scoped `git diff --check`.
- Missing: runtime 05i history/PR fetch, 05l synthesis against actual invalid/missing status/report inputs, complete fixture flow, forced evaluator failure, and fixture write-back execution.

## Risk Summary
<!-- 2-5 bullets -->
- `dev/phase-final-review/PHASE_05/evaluator-status.jsonl:1-8` records eight required checks as `not-run`; readiness correctly remains NO-GO.
- `05i` can mine remote/hosted history only when the declared fetch endpoint is available; local-history recovery remains an explicit integration condition.
- Generated 05i/05l mirrors are now checked by exact renderer parity plus the focused read-only capability assertions.
- Full pytest validation remains unavailable because pytest is not installed.
