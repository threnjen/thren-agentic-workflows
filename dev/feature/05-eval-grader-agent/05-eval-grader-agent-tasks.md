# 05 Eval Grader Agent Tasks

## Stage 1: Write master agent definition

- [ ] Create `.github/agents/05-eval-grader.agent.md` with the required agent name, grader description, and a tool set limited to `read`, `search`, and `edit`.
- [ ] Document the required inputs: `eval/runs/<phase-slug>/ledger-commits.jsonl`, `eval/runs/<phase-slug>/ledger-events.jsonl`, and a user-supplied rubric YAML path.
- [ ] Make the rubric schema explicit in the agent body and point future rubric authors to the seeded example file.
- [ ] Define the rubric intake and validation flow so the grader aborts clearly when the rubric path is missing.
- [ ] Describe the SHA-correlation procedure that merges commit rows and event rows into a unified scoring timeline.
- [ ] Specify how automatable rubric criteria are evaluated and how manual criteria are emitted as `[NEEDS_HUMAN_REVIEW]` entries.
- [ ] Capture missing-ledger, empty-ledger, unknown harness/model, and timestamped output-file edge cases without introducing interactive prompts.
- [ ] Define the score-report structure and output path `eval/runs/<phase-slug>/score-report-<timestamp>.md`.
- [ ] Verify the master file against MV2, MV3, MV4, and MV5 from the plan.

## Stage 3: Add the seeded rubric contract

- [ ] Create `eval/rubrics/phase-eval-infrastructure-foundation.example.yaml` with top-level `phase`, `harness`, `model`, and `criteria` fields.
- [ ] Include both automatable and `requires_human: true` criteria so the example exercises the grader's expected branches.
- [ ] Read back the example rubric and confirm it matches the schema documented in the agent and plan.

## Stage 2: Propagate to `opencode/agents/` and `claude/agents/`

- [ ] Create `opencode/agents/05-eval-grader.md` with the same grading workflow and report structure as the master agent.
- [ ] Create `claude/agents/05-eval-grader.md` with the same grading workflow and report structure as the master agent.
- [ ] Confirm the three agent files remain aligned in body content while respecting each platform's file naming and frontmatter conventions.
- [ ] Verify file existence and cross-platform parity with MV1 and MV6 from the plan.