# Review Record: Audit Delta Rewire

## Summary

Retry review found no new source defect. The two prior medium-severity fixes remain
intact: Phase 6 is the single shared-skill handoff after matrix confirmation, and
Phase 3 explicitly handles separate newer checkouts while forbidding temporary
worktrees. Runtime behavior and the Feature 11 focused guards remain unavailable.
The affected regression command still has the unchanged baseline failure set.

## Verdict

Changes Requested

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:99-117` | The exact `audit-comparison` reference and handoff are present statically. Feature 11's focused reference/ownership guard was not executed, and runtime skill loading was not observed. |
| AC2 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:20-47` | Phase 1/2 responsibility, order, and interaction remain in source; no live interaction was run. |
| AC3 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:49-81` | Output-root, non-current-branch, separate-directory, override, and matrix-confirmation decisions remain statically; runtime confirmation was not run. |
| AC4 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:121-134` | The up-front/no-up-front delta branches and partial-side rerun offer remain in source; both continuation paths need a live run. |
| AC5 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:143-169` | Fix-research and current-side-only remediation remain statically; execution was not performed. |
| AC6 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:95-141` | Prompt, matrix, artifact, attribution, conclusion, and after-attribution cleanup identity require the planned baseline/current comparison; none was executed. |
| AC7 | Verified (static) | `source_of_truth/agents/delta-auditor.agent.md:69-74,99-124` | The moved ref-materialization, matrix execution, delta gate, attribution batching, reconciliation, sum-check, and cleanup procedures are not restated; one Phase 6 handoff remains. Feature 11 mutation evidence is still missing. |
| AC8 | Verified (static) | `source_of_truth/agents/delta-auditor.agent.md:1-6` | Frontmatter roster and tools are unchanged. The corpus portion of the affected command passed, but the overall command remains failing on unrelated baseline failures. |
| AC9 | Unverified | `source_of_truth/agents/delta-auditor.agent.md:49-67,101-113,163-169` | Newer-side output and current-side remediation are explicit; runtime artifact placement and write isolation were not observed. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | The earlier version implied duplicate/premature skill loading and conflicting output-root ownership. Phase 6 is now the single handoff after matrix confirmation, with caller-only output-root resolution. | Medium | `source_of_truth/agents/delta-auditor.agent.md:49-74,99-117` | AC1, AC3, AC7 | Fixed (applied during the first review) |
| 2 | The earlier replacement dropped separate newer-checkout handling and the temporary-worktree prohibition. Both are now explicit. | Medium | `source_of_truth/agents/delta-auditor.agent.md:54-67` | AC3, AC9 | Fixed (applied during the first review) |
| 3 | The planned live comparison and Feature 11 focused structural/mutation guards remain unavailable, so runtime skill loading, prompts, artifacts, attribution, cleanup lifetime, and continuation branches are unverified. | High | `source_of_truth/agents/delta-auditor.agent.md:99-141`; `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-plan.md:8,89-94` | AC1, AC4, AC6, AC9 | Open (requires the focused guard module and manual comparison) |
| 4 | The affected regression command remains failing: three generated-output count subfailures, one stale `applyTo` target, and one pre-existing `05 PR - Review` prose collision. These match baseline; propagation was intentionally not run. | Medium | `dev/feature/09-audit-delta-rewire/results/retry-final.xml` | AC8 | Open (out of this source-only review scope) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| None during retry | Prior source fixes for Issues 1 and 2 were re-verified and retained; only this review record was updated. | 1, 2 |

## Remaining Concerns

- Issue #3: AC1–AC6 and AC9 need the planned live `Audit - Delta` comparison and Feature 11 focused guard suite before approval.
- Issue #4: The authoritative affected command is `executed-failing` (126 total, 121 passed, 5 failed, 0 errors); propagation and generated-output reconciliation remain maintainer/concurrent-feature work.

## Test Coverage Assessment

- Covered: static AC7; frontmatter/roster portions of AC8; affected regression command rerun after the prior fixes.
- Missing: Feature 11 focused structural and mutation-tested guards (module absent); live comparison for AC6/AC9; runtime interaction checks for AC2–AC5; full `uv run pytest tests/`.
- Test command: `uv run pytest tests/test_agent_corpus_invariants.py tests/test_unity_consumer_contract.py tests/test_propagate_master_assets.py tests/test_pr_review_orchestrator.py --junitxml=dev/feature/09-audit-delta-rewire/results/retry-final.xml`
- Results artifact: `dev/feature/09-audit-delta-rewire/results/retry-final.xml` — 126 total, 121 passed, 5 failed, 0 errors (`executed-failing`). The failure identities match `baseline.xml`.
- Regressions: Unknown — the command is not green; failures match baseline but runtime behavior was not exercised.

## Risk Summary

- `source_of_truth/agents/delta-auditor.agent.md:99-141` — the central shared comparison contract is structurally wired, but runtime behavior and worktree release timing remain unobserved.
- `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-plan.md:15-24` — the required focused ownership, interaction, gate, and mutation checks have no implementation to execute.
- `dev/feature/09-audit-delta-rewire/results/retry-final.xml` — affected suites are not green; all five failure subresults match baseline.
