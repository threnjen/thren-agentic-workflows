# Feature Tasks: Audit Comparison Contract

## Stage 1: Extract the Shared Contract

- [ ] Re-read `source_of_truth/agents/delta-auditor.agent.md` Phases 3 through 6b, `auditor-conventions` `Multi-Target Audits`, `audit-delta-report` sections 2A/2D and reconciliation rules, `05a-baseline-worktree.agent.md`, and `worktree-baseline` before drafting the shared contract.
- [ ] Choose a terse, collision-safe final slug for `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/`, create its single `SKILL.md`, and make the frontmatter `name` exactly match the directory while providing a concise non-empty `description` and no blank frontmatter lines. Record the chosen slug for Features 09–11.
- [ ] Define the caller-neutral input boundary without inventing caller-specific policy: explicit output root, audit matrix, target roots and labels, report paths, caller-provided identical scope/intent prompt content, and enough lifecycle state to clean up only worktrees created by the run.
- [ ] Define the caller-neutral return boundary around report paths, stated totals, per-type gate/reconciliation/attribution outcomes, cleanup status, and concrete failure state so interactive and unattended callers can apply different continuation policies.
- [ ] Extract output-root resolution so every snapshot report, delta, queue, and attribution update lands under the newer working checkout or an explicit caller override, never in a temporary baseline worktree.
- [ ] Extract ref-target materialization through the exact existing `Baseline Worktree` agent contract: resolve and record each ref's commit, use returned absolute roots, preserve dirty-current-checkout limitations, and return materialization failures without switching, stashing, or mutating the caller's checkout.
- [ ] Require one reusable audit-prompt template and cite `auditor-conventions` `Multi-Target Audits` for comparability; ensure only target root, snapshot label, and output directory vary between snapshot renders while caller-supplied scope and intent remain byte-identical.
- [ ] Extract audit-matrix execution so every selected audit type runs independently across every target, writes a full report and summary to its own per-snapshot paths, and never reads another target or audit run.
- [ ] Preserve per-type isolation through all later stages: separate report pairs, delta spawns, queues, reconciliation arithmetic, provisional populations, and attribution batch totals; prohibit cross-type deltas or combined counts.
- [ ] Implement the delta transition gate so no `Auditor - Delta` spawn occurs until both snapshot artifacts are verified as full findings reports that state their own totals; reject summary-only, missing, partial, or internally unusable inputs.
- [ ] Cite `audit-delta-report` for delta and queue contents, require both deliverables to exist, and require reconciliation to close against both source reports before any conclusion is returned.
- [ ] Preserve the no-premature-regression discipline: provisional current-side findings remain unattributed until `Auditor - Attribution` probes both trees, and no regression count is presented before that work completes.
- [ ] Extract attribution orchestration as disjoint subsystem batches, verify no identifier appears in more than one batch, and require assigned-item cardinalities to sum exactly to the delta's unattributed total before accepting results.
- [ ] Handle the empty-provisional case without spawning attribution and handle unavailable baseline roots through the existing `UNVERIFIED-ORIGIN` contract rather than inventing a regression result.
- [ ] Correct the stale source ordering identified in Discovery Delta: retain each worktree created for a ref through audits, delta, and attribution; send the cleanup handshake only after attribution returns; and never remove a reused pre-existing worktree.
- [ ] Keep the skill mechanism-only: remove all confirmations, questions, offers, audit-type/target selection, caller-specific retries, fix-research decisions, and remediation decisions from the extracted content.
- [ ] Review the skill for single ownership and brevity: cite rather than restate comparability, delta/attribution document semantics, and worktree lifecycle mechanics; state each moved orchestration rule once.
- [ ] Run `uv run pytest tests/test_agent_corpus_invariants.py` and confirm the new source skill parses under the existing structural frontmatter guard without introducing a new failure.
- [ ] Record for `11-audit-bookend-guards` the finalized skill path plus scenario-level obligations for one-template parameterization, full-report delta gating, provisional attribution, disjoint/summed batches, and post-attribution cleanup; do not create `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` in this feature.

## Stage 2: Synchronize Skill Counts

- [ ] Recount `source_of_truth/skills/*/SKILL.md` after the new skill is created and verify the source total is exactly 45 before editing prose counts.
- [ ] Update the current skill count in `CONTRIBUTING.md` from 44 to 45 without changing unrelated agent or instruction counts.
- [ ] Update the `docs/ARCHITECTURE.md` skill-directory count from 44 to 45 without changing the pipeline diagram's structure or unrelated counts.
- [ ] Update both skill-count statements in `docs/CODEBASE_CONTEXT.md` from 44 to 45: the `Current Counts` entry and the `Key Paths` tree annotation.
- [ ] Search `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, and `docs/CODEBASE_CONTEXT.md` for stale current skill-count statements and confirm all four verified surfaces agree on 45.
- [ ] Run `uv run pytest tests/` and compare the result with the captured baseline of 268 collected, 256 passed, and 15 existing failed/subfailed cases; introduce no Phase 03 failure and do not absorb unrelated baseline failures into this feature.
- [ ] Verify the diff contains only the new source skill and the three planned count documents; confirm neither consumer agent, any test file, `ports/`, nor `.github/` was edited.
- [ ] Report propagation as pending for the maintainer. Do not run `scripts/propagate_master_assets.py` or hand-edit generated outputs.
