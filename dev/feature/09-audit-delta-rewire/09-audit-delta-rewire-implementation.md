# Implementation Record: Audit Delta Rewire

## Summary

Rewired `Audit - Delta` to consume the finalized `audit-comparison` skill while
keeping its interactive type/target selection, output-root decision, matrix
confirmation, conditional delta and partial-side rerun offers, and Phase 7/8
research/remediation flow. The moved Phase 3–6b mechanics now have one compact
handoff and the existing roster/tools are unchanged.

## Sibling Features

- Feature 08 finalized `source_of_truth/skills/audit-comparison/SKILL.md`,
  which owns output-root resolution, ref materialization, matrix execution,
  gates, attribution, and post-attribution cleanup.
- Feature 10 is a concurrent, file-disjoint consumer update to
  `source_of_truth/agents/04-phase-execute.agent.md`; its source/generated
  changes were preserved and not included in this feature's source scope.
- Feature 11 owns the focused structural and mutation guards for both
  consumers; no test file was created here.
- Features 01–07 do not share the changed source file.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | Feature 11 focused guard (planned) | Finalized skill reference and explicit handoff inputs | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:95-109`; `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC2 | AC2 | Feature 11 focused guard (planned) | Retained Phase 1/2 sections and order | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:20-47` | PENDING | PENDING |
| AC3 | AC3 | Feature 11 focused guard (planned) | Retained output-root and matrix confirmation interactions | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:49-93` | PENDING | PENDING |
| AC4 | AC4 | Feature 11 focused guard (planned) | Conditional delta and partial-side rerun branches | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:117-130` | PENDING | PENDING |
| AC5 | AC5 | Feature 11 focused guard (planned) | Retained fix-research and current-side remediation flow | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:139-165` | PENDING | PENDING |
| AC6 | AC6 | Manual runtime comparison (planned) | Matrix, prompt, artifact, attribution, and returned-conclusion preservation | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:72-137`; `source_of_truth/skills/audit-comparison/SKILL.md` | PENDING | PENDING |
| AC7 | AC7 | Feature 11 focused guard (planned) | Single compact handoff with moved procedures removed | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:66-70,95-120` | PENDING | PENDING |
| AC8 | AC8 | Corpus invariants regression | Frontmatter roster and tools unchanged | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:1-6`; `dev/feature/09-audit-delta-rewire/results/final.xml` | PENDING | PENDING |
| AC9 | AC9 | Feature 11 focused guard (planned) | Newer-side output root and current-side-only remediation retained | Done | `source_of_truth/agents/delta-auditor.agent.md` | `source_of_truth/agents/delta-auditor.agent.md:62-64,99-109,159-165` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Load finalized `audit-comparison` and delegate moved mechanics | Done | `source_of_truth/agents/delta-auditor.agent.md` | Exact finalized slug loaded once. |
| AC2 | Preserve Phase 1/2 responsibility, order, and interaction | Done | `source_of_truth/agents/delta-auditor.agent.md` | Existing text retained. |
| AC3 | Preserve output-root decision and matrix confirmation | Done | `source_of_truth/agents/delta-auditor.agent.md` | Caller-only questions remain before shared spawning. |
| AC4 | Preserve delta and partial-side rerun offers | Done | `source_of_truth/agents/delta-auditor.agent.md` | No duplicate offer is added by the shared handoff. |
| AC5 | Preserve Phase 7/8 research and remediation behavior | Done | `source_of_truth/agents/delta-auditor.agent.md` | Current-side-only remediation remains explicit. |
| AC6 | Preserve observable comparison behavior, correcting cleanup lifetime | Done | `source_of_truth/agents/delta-auditor.agent.md` | Static contract is preserved; real runtime comparison remains a gap. |
| AC7 | Remove duplicated shared mechanics from consumer | Done | `source_of_truth/agents/delta-auditor.agent.md` | Phase 3–6b now references the skill and returned state. |
| AC8 | Keep roster and tool authority sufficient and unchanged | Done | `source_of_truth/agents/delta-auditor.agent.md` | Frontmatter was not edited. |
| AC9 | Keep artifacts newer-side and remediation current-side only | Done | `source_of_truth/agents/delta-auditor.agent.md` | Handoff passes `output_root`; Phase 8 remains unchanged. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/agents/delta-auditor.agent.md` | Modified | Replaced duplicated Phase 3–6b mechanics with the finalized shared-skill handoff; retained caller interactions and Phase 7/8. | Make `audit-comparison` the single mechanical owner while preserving `Audit - Delta` behavior. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|-----|
| None | None | No tests were added or edited; Feature 11 owns focused guards. | Existing corpus and regression suites only. |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/test_agent_corpus_invariants.py tests/test_unity_consumer_contract.py tests/test_propagate_master_assets.py tests/test_pr_review_orchestrator.py --junitxml=dev/feature/09-audit-delta-rewire/results/final.xml`
- **Results artifact**: `dev/feature/09-audit-delta-rewire/results/final.xml`
- **Baseline**: 121 passed, 5 failed (126 test cases/subtests), `dev/feature/09-audit-delta-rewire/results/baseline.xml`
- **Final**: 121 passed, 5 failed (126 test cases/subtests), `dev/feature/09-audit-delta-rewire/results/final.xml`
- **New tests added**: 0
- **Affected suites run**: `tests/test_agent_corpus_invariants.py`, `tests/test_unity_consumer_contract.py`, `tests/test_propagate_master_assets.py`, `tests/test_pr_review_orchestrator.py`
- **Regressions**: Unknown — tests not executed

The five failures are unchanged from baseline: three generated-agent count
subfailures, one stale `applyTo` target, and the existing `05 PR - Review` prose
collision. The source-only structural handoff checks passed separately.

## Deviations from Plan

- No focused test module was created because Feature 11 owns it.
- Full `uv run pytest tests/` and one live `Audit - Delta` comparison were not
  run in this invocation; they remain explicit gaps below.
- Propagation was not run. Concurrent Feature 08/10 generated/source changes
  were preserved and are outside this feature's Files Changed scope.

## Gaps

- Runtime behavioral comparison, prompt capture, and worktree-lifetime evidence
  remain manual/downstream verification items.
- The full repository suite was not run in this invocation; the mandated
  affected suites completed with the unchanged pre-existing failure set.
- Generated `ports/` and `.github/` outputs require maintainer propagation after
  concurrent feature work; no generated file was authored here.

## Reviewer Focus Areas

- `source_of_truth/agents/delta-auditor.agent.md:49-137` — verify all caller
  decisions remain outside the shared skill and the handoff does not recreate
  moved mechanics.
- `source_of_truth/agents/delta-auditor.agent.md:97-120` — verify the four
  finalized inputs, comparison paths, delta intent, and returned evidence are
  sufficient for interactive continuation.
- `source_of_truth/agents/delta-auditor.agent.md:139-165` — verify research
  prerequisites and current-side-only remediation remain unchanged.
