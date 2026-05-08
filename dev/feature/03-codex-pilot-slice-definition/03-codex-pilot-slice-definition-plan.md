# 03 Codex Pilot Slice Definition

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** yes
- **Depends on:** 02-codex-macos-setup-guide, 02-codex-porting-guide, 01-codex-source-layout
- **Key files modified:** `codex/PILOT_SLICE_PLAN.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1**: `codex/PILOT_SLICE_PLAN.md` names exactly one pilot instruction slice, one pilot custom agent, and one pilot skill to validate before any full Codex parity effort.
2. **AC2**: The pilot choices are justified against Phase 02 goals and the current repository structure, with explicit rationale for why they are low-risk and high-signal validation targets.
3. **AC3**: The pilot plan defines the expected Codex outputs for all three surfaces: global AGENTS guidance, a custom-agent TOML file, and a skill directory.
4. **AC4**: The pilot plan documents a manual validation workflow that uses the macOS setup guide and the porting guide rather than inventing new installation or mapping rules.
5. **AC5**: The pilot plan includes explicit exit criteria that must pass before any broader Codex port is attempted.
6. **AC6**: The pilot plan records the chosen default slice as: a narrow global guidance slice derived from `.github/instructions/output-verbosity-policy.instructions.md`, the `03 Feature - Decomposer` agent, and the `.github/skills/feature-plan-set/` skill, unless a later discovery uncovers a demonstrably lower-risk trio.

### Non-Goals

- Do not implement the pilot Codex artifacts in this feature.
- Do not expand the pilot into a full-catalog Codex conversion.
- Do not change the Phase 02 macOS setup or mapping rules in this feature.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---------------------|-------------------|---------------|
| AC1: one instruction slice, one agent, one skill selected | `codex/PILOT_SLICE_PLAN.md`, `.github/instructions/output-verbosity-policy.instructions.md`, `.github/agents/03-feature-decomposer.agent.md`, `.github/skills/feature-plan-set/` | Manual selection audit |
| AC2: rationale is explicit and grounded | `codex/PILOT_SLICE_PLAN.md` | Decision-review against Phase 02 goals |
| AC3: expected outputs for all three Codex surfaces defined | `codex/PILOT_SLICE_PLAN.md`, `codex/CODEX_PORTING_GUIDE.md`, `codex/README.md` | Output-contract review |
| AC4: validation workflow reuses existing guides | `codex/PILOT_SLICE_PLAN.md`, `codex/MACOS_SETUP_AND_SYMLINKS.md`, `codex/CODEX_PORTING_GUIDE.md` | Workflow consistency audit |
| AC5: exit criteria defined | `codex/PILOT_SLICE_PLAN.md` | Exit-criteria presence check |
| AC6: default pilot trio recorded | `codex/PILOT_SLICE_PLAN.md` | Literal-value review |

## B. Correctness & Edge Cases

### Key Workflows

- A maintainer uses the plan to implement the first Codex slice without reopening platform research.
- A reviewer uses the exit criteria to decide whether broader Codex parity work is justified.

### Failure Modes and Edge Cases

- Choosing a pilot that is too large or runtime-heavy will delay validation and blur whether the mapping model is correct.
- Choosing a trio that does not cover all three Codex-native surfaces will fail to validate the full model.
- Choosing a pilot without an explicit macOS install flow will make the setup guide effectively untested.
- If a lower-risk trio emerges later, the plan must allow replacement, but only with explicit evidence.

### Error-Handling Strategy

- Prefer the narrowest trio that still exercises global guidance, custom agents, and directory-based skills together.
- If the default trio proves blocked, require a documented replacement decision instead of silent drift.

## C. Consistency & Architecture Fit

### Existing Patterns To Follow

- Use Phase 02’s “pilot before full parity” rule as a hard gate.
- Reuse the repository’s current decomposition and skill surfaces rather than inventing a synthetic example disconnected from the codebase.

### Interfaces and Contracts

- Input contract: Codex source layout, Codex porting guide, macOS setup guide, and the current `.github/` source tree.
- Output contract: one pilot-slice definition that names the trio, expected deliverables, validation steps, and exit criteria.

### Sibling Feature Relationships

- Depends on `02-codex-porting-guide` for mapping rules and on `02-codex-macos-setup-guide` for install/validation flow.
- Depends on `01-codex-source-layout` so the plan can name the intended repository-owned destinations for future pilot artifacts.
- This is the final feature in the phase decomposition because it consumes the outputs of the earlier Codex docs rather than producing new base guidance.

## D. Clean Design & Maintainability

### Simplest Design

- Define one default pilot trio and one fallback rule.
- For each selected surface, specify source asset, expected Codex output, install location, and validation check.

### Complexity Risks

- A vague pilot plan will invite scope creep into full conversion.
- A pilot plan with no explicit exit criteria will not stop premature parity work.

### Keep It Clean Checklist

- [ ] The pilot includes all three Codex-native surfaces.
- [ ] The trio is grounded in existing repo assets.
- [ ] Validation reuses the previously written guides.
- [ ] Exit criteria clearly gate broader Codex work.

## E. Completeness: Observability, Security, Operability

### Logging / Metrics / Tracing

- Observability is pilot traceability: the plan should make it easy to see which source assets produced which Codex outputs and how they will be validated.

### Security

- Keep the plan free of machine-specific or user-specific absolute paths beyond generic macOS install roots.

### Runbook

- Before pilot implementation, recheck the selected source assets against the live `.github/` tree.
- Use the macOS setup guide for install mechanics and the porting guide for transformation rules.
- Do not widen scope beyond the named trio until all pilot exit criteria pass.

## F. Test Plan

### Acceptance Criteria Test Mapping

| Acceptance Criteria | Test Type | Planned Verification |
|---------------------|-----------|----------------------|
| AC1 | Selection audit | Confirm exactly one instruction slice, one agent, and one skill are named |
| AC2 | Rationale review | Confirm the plan explains why the trio is low-risk and high-signal |
| AC3 | Output-contract review | Confirm expected global AGENTS, TOML agent, and skill-directory outputs are specified |
| AC4 | Workflow consistency audit | Confirm the plan reuses the setup and porting guides rather than inventing new rules |
| AC5 | Gate review | Confirm exit criteria are specific enough to block premature full conversion |
| AC6 | Literal-value review | Confirm the default pilot trio is recorded exactly as chosen |

### Top 5 High-Value Test Cases

1. Given the plan is handed to an implementer, when they read it, then they can identify the exact instruction slice, agent, and skill to convert first without making a new selection decision.
2. Given the global AGENTS rule is critical, when the plan describes the instruction pilot, then it routes the derived guidance to the global Codex AGENTS layer rather than repo-local AGENTS files.
3. Given the selected custom agent is `03 Feature - Decomposer`, when the plan defines outputs, then it describes a Codex TOML agent plus any required `developer_instructions` split clearly.
4. Given the selected skill is `.github/skills/feature-plan-set/`, when the plan defines outputs, then it preserves the directory-based skill model and the required `SKILL.md` contract.
5. Given the pilot succeeds, when a maintainer checks the exit criteria, then they know whether broader Codex conversion may proceed or whether another documentation pass is required first.

### Test Data, Mocks, or Fixtures Needed

- `.github/instructions/output-verbosity-policy.instructions.md`
- `.github/agents/03-feature-decomposer.agent.md`
- `.github/skills/feature-plan-set/`
- `codex/CODEX_PORTING_GUIDE.md`
- `codex/MACOS_SETUP_AND_SYMLINKS.md`
- `codex/README.md`

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Test suite exists, coverage ≥ 50%, all tests pass
**Status**: Required before implementation begins

## Stage 1: Select and Justify the Pilot Trio
**Goal**: Create `codex/PILOT_SLICE_PLAN.md` that names one instruction slice, one custom agent, and one skill, with the default trio grounded in the current repo.
**Success Criteria**: AC1, AC2, and AC6 are satisfied with explicit rationale and a documented fallback rule.
**Status**: Not Started

## Stage 2: Define Outputs, Validation Flow, and Exit Criteria
**Goal**: Make the pilot executable by specifying expected Codex artifacts, reuse of the setup and porting guides, and the gate for wider conversion.
**Success Criteria**: AC3, AC4, and AC5 are satisfied, and the pilot becomes the final prerequisite before any broader Codex port.
**Status**: Not Started