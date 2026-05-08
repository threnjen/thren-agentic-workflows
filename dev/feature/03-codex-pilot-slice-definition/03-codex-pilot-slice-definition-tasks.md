# 03 Codex Pilot Slice Definition Tasks

## Stage 0: Test Prerequisites

- [ ] Confirm whether this documentation slice has any automated test coverage; if not, record the current manual-review-only baseline and treat Stage 0 as an explicit prerequisite decision before implementation.
- [ ] If the phase requires the `@z-test-writer` prerequisite to be satisfied, define what test or validation coverage is expected for `codex/PILOT_SLICE_PLAN.md` before moving into implementation.
- [ ] Capture the current baseline for this feature as selection audit, rationale review, output-contract review, workflow consistency audit, and exit-criteria review.

## Stage 1: Select and Justify the Pilot Trio

- [ ] Verify that the sibling outputs `codex/README.md`, `codex/CODEX_PORTING_GUIDE.md`, and `codex/MACOS_SETUP_AND_SYMLINKS.md` exist or are otherwise available from their prerequisite features before drafting the pilot plan.
- [ ] Create `codex/PILOT_SLICE_PLAN.md` and name exactly one instruction slice, one custom agent, and one skill for the pilot conversion.
- [ ] Record the default trio as `.github/instructions/output-verbosity-policy.instructions.md`, `.github/agents/03-feature-decomposer.agent.md`, and `.github/skills/feature-plan-set/` unless a demonstrably lower-risk trio is documented.
- [ ] Explain why the chosen trio is low-risk and high-signal against Phase 02 goals and the current repository structure.
- [ ] Add a fallback rule that allows replacing the default trio only when explicit evidence supports the change.

## Stage 2: Define Outputs, Validation Flow, and Exit Criteria

- [ ] For the instruction slice, define the expected Codex global AGENTS guidance output, its repository-owned source, and the validation check that confirms the mapping is correct.
- [ ] For the custom agent, define the expected Codex TOML output, its source agent, and any required `developer_instructions` split or transformation.
- [ ] For the skill, define the expected Codex skill-directory output, the preserved `SKILL.md` contract, and any required directory structure details.
- [ ] Reuse `codex/CODEX_PORTING_GUIDE.md` for mapping rules and `codex/MACOS_SETUP_AND_SYMLINKS.md` for manual installation and validation steps rather than inventing new rules in the pilot plan.
- [ ] Define explicit exit criteria that must pass before any broader Codex port is attempted.
- [ ] Make the pilot the final prerequisite gate before wider Codex parity work begins.