# Phase 5: Unified Local Final Checks

**Status**: Implemented — maintainer propagation pending
**Depends on**: Phase 04
**Estimated complexity**: Large
**Cross-references**: `docs/phases/PHASE_04/PHASE_04_SUMMARY.md`

## What's New

Authors and reviewers get one local command for checking a completed change before opening a merge request. `phase-final-checks` becomes the primary command, while `pr-review` remains an alias for the same workflow.

The command reviews a confirmed commit range, writes one advisory readiness report, and then offers one bounded repair pass. It does not require an open merge request, publish comments, push changes, or rerun an open-ended review cycle.

## Problem

Local change review had overlapping responsibilities and vocabulary. The prior command assumed a pull-request-shaped workflow, while phase execution carried separate review responsibilities.

The overlap increases agent cost and gives authors more than one place to seek the same readiness answer. It also couples local review to merge-request concepts that are unnecessary for reviewing a commit range.

## Objective

Provide one advisory local-review workflow for any confirmed `base..HEAD` range. Preserve the useful range-selection and partial-failure behavior while reducing the evaluator roster and making repair explicit and bounded.

## Scope

### In Scope

- Expose the local review orchestration surface as `phase-final-checks`.
- Preserve `pr-review` as an alias that resolves to the same agent body on Claude, Codex, OpenCode, and Cursor.
- Keep the GitHub mirror on its native agent surface, which has no generated slash-command alias.
- Suggest a base, show the resulting range, and require confirmation before review begins.
- Complete an empty-diff run with a valid report instead of treating it as an orchestration failure.
- Accept optional plans, specifications, QA records, merge-request URLs, and approval summaries as enrichment.
- Allow only the readiness synthesizer to use judgment enrichment. Coverage evidence remains direct Test Health input.
- Run the baseline worktree and change narrator for every non-empty review.
- Extend the change narrator to report outward impact when the diff changes code, schema, or configuration.
- Extend test health to falsify changed tests when the diff changes test files.
- Run dependency review when the diff changes a dependency manifest or lockfile.
- Run test health when the diff changes tests or the user supplies coverage evidence.
- Run cleanliness, consistency, and diff-security checks for every non-empty review.
- Fold branch-added artifact checks into the cleanliness review and retire the separate artifact sweeper.
- Keep retired Phase 04 agents deleted. Do not recreate compatibility lanes.
- Write one readiness report before asking whether to repair eligible findings.
- Let the readiness synthesizer emit repair candidates from security, outward-impact, and test-falsification findings.
- Add one local-review fixer that works from the confirmed range and current source without Phase artifacts.
- Allow at most one repair pass against the current checkout.
- Write a separate repair report with per-finding outcomes, changed files, and regression evidence.
- Update review skills, instructions, propagation behavior, tests, and documentation for the new command.
- Recount the agent catalog from the finished source tree and synchronize every count surface.

### Out of Scope

- Running local final checks from Phase Execute.
- Replacing Prod Code Review as the phase pipeline gate.
- Posting to GitLab, GitHub, or another forge.
- Opening or updating a merge request.
- Fetching remote branches or checking out another contributor's work.
- Pushing repair commits.
- Automatically repairing consistency, cleanliness, dependency, or test-health findings.
- Repeating review after repair until the report becomes clean.
- Recreating the retired Phase validator, consolidator, or feature fixer as compatibility agents.
- Deleting agents merely to reach a catalog count from another repository fork.
- Renaming unrelated agents for a contiguous numbering scheme.
- Rewriting untouched agent families for prose style alone.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Single local-review command | One confirmed-range workflow exposed as `phase-final-checks` and `pr-review` | Invocation aliases and review lifecycle |
| 2 | Reduced review and repair contract | Conditional evaluator roster, one readiness report, and one optional validated repair pass | Roster consolidation and bounded repair |

## User Flows

### Author reviews a completed change

1. The author invokes `phase-final-checks` or `pr-review`.
2. The command suggests a base and displays the implied commit range.
3. The author confirms or corrects the base and optional enrichment list.
4. The command reviews the fixed range and writes one readiness report.
5. The author either stops with the advisory report or requests one eligible repair pass.
6. An accepted repair writes a separate outcome report without replacing the advisory verdict.

### Reviewer checks another checkout

1. The reviewer checks out the branch through their normal repository workflow.
2. The reviewer invokes either command and confirms the intended base.
3. The command reviews only the local checkout and supplied enrichment.
4. The reviewer declines repair unless they intend to modify that checkout.

### Empty range

1. The user confirms a range with no changed lines.
2. The command writes a completed no-change report.
3. The command skips evaluator and repair work that has no subject.

### Partial evaluator failure

1. One evaluator fails or cannot run after the baseline worktree succeeds.
2. The command records the missing check and continues with usable results.
3. The synthesizer lowers confidence according to the documented verdict rules.

## Technical Context

- `source_of_truth/agents/04-phase-final-checks.agent.md` owns base confirmation, conditional evaluator fan-out, and the report lifecycle.
- `source_of_truth/agents/04a-baseline-worktree.agent.md` provides the isolated baseline and remains the first mandatory child.
- `source_of_truth/agents/04b-change-narrator.agent.md` explains the branch diff without plan enrichment.
- `source_of_truth/agents/04b-change-narrator.agent.md` can own conditional outward-impact findings without another report lane.
- `source_of_truth/agents/04h-cleanliness-auditor.agent.md` owns branch-added debug markers and temporary artifacts.
- `source_of_truth/agents/04d-consistency-auditor.agent.md`, `04e-dependency-auditor.agent.md`, `03e-diff-security-scan.agent.md`, and `04f-test-health.agent.md` remain advisory lanes.
- `source_of_truth/agents/04f-test-health.agent.md` can own conditional falsification of changed tests.
- `source_of_truth/agents/04g-readiness-synthesizer.agent.md` is the sole consumer that may combine evaluator evidence with enrichment and emit repair candidates.
- Phase 04 deleted the old Phase review committee, consolidator, validator, and fixer. This phase does not restore them.
- `source_of_truth/agents/04i-local-review-fixer.agent.md` owns one plan-independent repair pass.
- `source_of_truth/skills/local-final-check-conventions/SKILL.md` and `local-final-check-report/SKILL.md` define the current report root, evidence boundary, severity model, and report template.
- `scripts/propagate_master_assets.py` validates aliases and emits harness-specific command surfaces.
- `tests/test_local_final_checks.py` and `tests/test_propagate_master_assets.py` guard the workflow.
- `source_of_truth/` remains the only authoring surface. The maintainer runs propagation after source changes.

## Dependencies & Risks

- **Dependency**: Phase 04 removed the phase-close review chorus before this command became the local-review handoff.
- **Dependency**: alias validation and emission cover Claude, Codex, OpenCode, and Cursor.
- **Dependency**: GitHub mirrors the authored agent but exposes no generated command-alias surface. Tests and documentation must state this difference.
- **Risk**: changing the primary command can strand callers or deployed files. Mitigation: add alias support first, test both invocation surfaces, then reconcile generated-file retirement rules.
- **Risk**: a report timestamp containing colons is not portable to Windows. Mitigation: use a UTC timestamp format that is safe on every supported filesystem.
- **Risk**: optional judgment enrichment may leak into evaluators. Mitigation: pass it only to the synthesizer. Pass coverage evidence only to Test Health and synthesis.
- **Risk**: removing an evaluator can strand an internal procedure or leave a report consumer dangling. Mitigation: search agent bodies, skills, instructions, tests, and documentation for both the display name and filename before retirement.
- **Risk**: repair can turn an advisory command into an unbounded implementation loop. Mitigation: let the synthesizer emit candidates once and permit one local-review fixer pass without a review rerun.
- **Risk**: repair changes the checkout after the readiness verdict. Mitigation: preserve the pre-repair report and write a separate repair report with every outcome and regression result.
- **Risk**: an evaluator that is still running may look failed because it has not written its report. Mitigation: apply output checks only after the child reports completion or failure.
- **Risk**: source and generated command sets will diverge after authoring. Mitigation: stop with propagation pending and state which sync tests are expected to fail.

## Success Criteria

- [x] `phase-final-checks` and `pr-review` invoke the same user-facing agent on Claude, Codex, OpenCode, and Cursor.
- [x] GitHub receives the authored agent through its native mirror without a fabricated slash-command alias.
- [x] Alias parsing rejects invalid aliases, hidden-agent aliases, and collisions before generating output.
- [x] The command confirms one base and uses the resulting fixed range for every evaluator.
- [x] The command filters its own branch and tracking reference from automatic base suggestions.
- [x] A confirmed empty range produces a completed no-change readiness report.
- [x] Baseline-worktree failure stops the run before evaluator fan-out.
- [x] A later evaluator failure is recorded and does not discard usable reports.
- [x] The change narrator never receives plans, QA records, approval summaries, or merge-request context.
- [x] Only the readiness synthesizer receives judgment enrichment. Test Health receives coverage evidence as direct evaluator input.
- [x] Change Narrator reports outward impact exactly when code, schema, or configuration changes.
- [x] Test Health falsifies changed tests exactly when test files change.
- [x] Dependency review runs exactly when a dependency manifest or lockfile changes.
- [x] Test health runs exactly when tests change or coverage evidence is supplied.
- [x] Cleanliness checks cover branch-added debug statements, TODO or FIXME markers, temporary flags, and commented-out code.
- [x] No separate artifact-sweeper, plan-blind, blast-radius, or test-falsification lane remains.
- [x] The command writes the readiness report before it asks whether to repair findings.
- [x] Declining repair leaves the checkout unchanged and completes the workflow.
- [x] Repair considers only synthesizer-confirmed findings from security, outward-impact, and test-falsification checks.
- [x] Local validation and repair work without a phase plan, task name, review cycle, or implementation record.
- [x] An empty repair-candidate list skips the local-review fixer.
- [x] An accepted repair request invokes at most one fixer pass against current `HEAD`.
- [x] Every accepted repair writes a separate report with per-finding status, changed files, baseline tests, and post-repair results.
- [x] The repair report does not overwrite or silently upgrade the pre-repair readiness verdict.
- [x] The workflow never pushes changes, posts review comments, or requires an open merge request.
- [x] Report paths use a cross-platform-safe UTC timestamp and remain under one local-review root.
- [x] Retired source agents have no live roster entries, spawn instructions, instruction globs, tests, or documentation references.
- [x] Contract tests fail when alias identity, range consistency, evaluator conditions, or the repair bound is removed.
- [x] Catalog documentation reports counts measured from the completed source tree.
- [x] Authored changes stay within `source_of_truth/`, `scripts/`, `tests/`, and repository documentation before maintainer propagation.
- [x] No generated file under `ports/` or `.github/` is edited by an agent.

## QA Considerations

- No product UI changes.
- Automated tests must cover alias parsing, collisions, hidden-agent rejection, four command-emitting harnesses, and GitHub's native mirror behavior.
- Mutation-style guards must prove that range confirmation, evaluator conditions, enrichment isolation, and the one-pass repair bound can fail.
- A fixture review should cover a non-empty range, an empty range, a corrected base, and a partial evaluator failure.
- A manual dry read must confirm that both command names describe one local workflow and never promise forge posting.
- Port synchronization tests will remain red after source edits until the maintainer runs propagation.

## Implementation Notes

- Alias validation rejects invalid syntax, hidden-agent aliases, and invocation collisions before output emission.
- Cleanliness owns the retired artifact sweeper's checks.
- Test Health works directly from changed tests and supplied coverage evidence. It no longer needs Test Analyst.
- The readiness report remains the pre-repair judgment. One accepted repair pass writes a separate report and never reruns the roster.
- Maintainer propagation remains pending. Generated ports intentionally retain the prior command until that manual step.
