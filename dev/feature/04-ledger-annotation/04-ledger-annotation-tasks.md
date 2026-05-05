# Tasks: 04 Ledger Annotation

## Stage 1: Add ledger annotation to `04c Feature - Reviewer`

- [ ] Add a ledger-write instruction block to the "Changes Requested" path in `.github/agents/04c-feature-reviewer.agent.md`.
- [ ] Set reviewer-specific fields in that block: `stage: "review"` and `detected_by: "reviewer"`.
- [ ] Include the required branch guard, phase-slug derivation, target path `eval/runs/<phase-slug>/ledger-events.jsonl`, and `mkdir -p` plus append semantics.
- [ ] Ensure the reviewer block does not write ledger rows for `Approved` or `Approved with Reservations` outcomes.

## Stage 2: Add ledger annotation to `04b Feature - Implementer`

- [ ] Add a ledger-write instruction block to the blocking-failure or unresolvable-issue path in `.github/agents/04b-feature-implementer.agent.md`.
- [ ] Set implementer-specific fields in that block: `stage: "implement"` and `detected_by: "implementer"`.
- [ ] Include the full ledger schema, branch guard, phase-slug derivation, target path, and `mkdir -p` plus append semantics.
- [ ] Keep the instruction out of routine red-green-refactor iteration paths.

## Stage 3: Add user-discovered annotation to `Debugger`

- [ ] Insert a new Step 1a, or equivalent pre-fix step, in `.github/agents/debugger.agent.md` after triage and before investigation or fixes begin.
- [ ] Set debugger-specific fields in that block: `stage: "debug"`, `detected_by: "user-discovered"`, and `human_intervention_required: true`.
- [ ] Include the branch guard, phase-slug derivation, target path, and `mkdir -p` plus append semantics.
- [ ] Make the debugger step silent on non-`phase/*` branches and ensure it runs before any first commit on a phase branch.

## Stage 4: Verify schema completeness across all three master files

- [ ] Read the three `.github/agents/` master files and confirm all required ledger fields are present in each new instruction block.
- [ ] Confirm each master file documents the target path `eval/runs/<phase-slug>/ledger-events.jsonl` and the branch-to-slug derivation rule.
- [ ] Confirm each master file documents the non-`phase/*` silent-skip rule.
- [ ] Confirm reviewer, implementer, and debugger each use the correct `stage` and `detected_by` values for their path.

## Stage 5: Propagate to all copy files

- [ ] Mirror the reviewer ledger-write block into `opencode/agents/04c-feature-reviewer.md` and `claude/agents/z-feature-reviewer.md`.
- [ ] Mirror the implementer ledger-write block into `opencode/agents/04b-feature-implementer.md` and `claude/agents/z-feature-implementer.md`.
- [ ] Mirror the debugger ledger-write block into `opencode/agents/debugger.md` and `claude/agents/debugger.md`.
- [ ] Re-read all six copy files to verify they match the master-file intent and placement.