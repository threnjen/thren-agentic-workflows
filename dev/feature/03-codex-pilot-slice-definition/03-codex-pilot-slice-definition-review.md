# Review Record: 03 Codex Pilot Slice Definition

## Summary

`codex/PILOT_SLICE_PLAN.md` is a well-constructed planning document that satisfies all six acceptance criteria. The pilot trio is narrow, well-justified, internally consistent with `CODEX_PORTING_GUIDE.md` and `CODEX_PLATFORM_REFERENCE.md`, and gates broader Codex conversion work behind six specific exit criteria. Architecture and roadmap docs correctly reflect a four-platform model. No Blocker, High, or Medium severity issues were found.

## Verdict

Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1: Exactly one instruction slice, one custom agent, one skill named | ✅ Satisfied | `codex/PILOT_SLICE_PLAN.md` — Default Pilot Trio table | All three Codex-native surfaces covered |
| AC2: Rationale explicit and grounded in Phase 02 goals and repo structure | ✅ Satisfied | `codex/PILOT_SLICE_PLAN.md` — Selection Rationale section (three subsections each with "Why low-risk", "Why high-signal", "Phase 02 alignment") | Each rationale cites the specific CODEX_PORTING_GUIDE.md section it aligns with |
| AC3: Expected Codex outputs defined for all three surfaces | ✅ Satisfied | `codex/PILOT_SLICE_PLAN.md` — Expected Codex Outputs section (Output 1, 2, 3) | Transformation rules, expected content, portability classifications, and TOML template are all present |
| AC4: Validation workflow reuses macOS setup guide and porting guide | ✅ Satisfied | `codex/PILOT_SLICE_PLAN.md` — Manual Validation Workflow section (Steps 2, 3, 6 explicitly cite the guides) | No new installation or mapping rules invented |
| AC5: Explicit exit criteria defined | ✅ Satisfied | `codex/PILOT_SLICE_PLAN.md` — Exit Criteria section (EC1–EC6) | Each criterion has a clear, specific pass condition that blocks premature full conversion |
| AC6: Default trio recorded as output-verbosity-policy, 03-feature-decomposer, feature-plan-set | ✅ Satisfied | `codex/PILOT_SLICE_PLAN.md` — Default Pilot Trio table | Matches AC6 specification exactly; Replacement Record is empty by design |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Skill-reference resolution mechanism not documented in platform reference: the validation workflow (Step 5) and EC4 assume Codex resolves prose skill references in `developer_instructions` from the installed `$HOME/.agents/skills/` directory, but `CODEX_PLATFORM_REFERENCE.md` does not document this resolution mechanism explicitly. EC4 is correctly designed as a fail-fast gate — if the assumption is wrong, EC4 fails and the pilot doesn't pass — so the plan's design correctly handles this uncertainty. | Low | `codex/PILOT_SLICE_PLAN.md` — Step 5, EC4 | AC3, AC5 | Open — correctly handled by EC4 as a validation gate; no fix required |
| 2 | TOML multi-line string escaping not addressed: the Output 2 template shows a `developer_instructions = """..."""` block but does not note any TOML-specific escaping requirements for the agent body (e.g., embedded double-quotes, backslash sequences). This is an implementation-time concern rather than a planning gap; standard TOML triple-quoted strings handle the common cases. | Low | `codex/PILOT_SLICE_PLAN.md` — Output 2, Required TOML fields | AC3 | Open — in scope for the implementing feature; not a planning document defect |

## Fixes Applied

None

## Remaining Concerns

- Issue #1: Codex skill-reference resolution assumption — low severity; EC4 acts as the correct verification gate. If EC4 fails during pilot implementation, `CODEX_PLATFORM_REFERENCE.md` should be updated before any retry.
- Issue #2: TOML escaping — low severity; defer to the implementing feature.

## Test Coverage Assessment

- Covered: AC1, AC2, AC3, AC4, AC5, AC6 (all via manual review of document content, which is the only applicable test type for a documentation-only feature)
- Missing: No automated test coverage is applicable. The plan defines a manual validation workflow (Steps 1–6) and six exit criteria (EC1–EC6) that together constitute the full test surface for this feature. This is correct and consistent with the non-goal of not implementing Codex artifacts in this feature.

## Risk Summary

- `codex/PILOT_SLICE_PLAN.md` — Skill-reference resolution via prose in `developer_instructions` is an unverified assumption. EC4 gates on this, so failure is detectable and the plan does not let it pass silently.
- `codex/PILOT_SLICE_PLAN.md` — The Personality Canary in Output 1 depends on the canary text surviving verbatim from the source instruction file. EC2 and EC5 together cover this; EC6 prevents modification of the source. Low risk.
- Broader: No full-catalog Codex scope creep is implied. The Replacement Record is empty, the Non-Goals are explicit, and the exit criteria create a formal gate. Risk of scope drift is low.
