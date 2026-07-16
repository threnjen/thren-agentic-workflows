# Cross-Phase Decisions

## Phase Numbering

- **Phases were renumbered 2026-07-16** so numbers match the order work actually happened: Phase Final Review (was 05) → **03**; new Release Remediation & Verification → **04**; Format-on-Save + Completion Gates (was 03) → **05**; Skill Enforcement (was 04) → **06**. Phases 01 and 02 are unchanged. Documents written before that date use the old scheme; the mapping table is in `docs/phases/PROJECT_ROADMAP.md`.
- **Agent numbers are pipeline positions, not phase numbers.** `05-phase-final-review` and its `05a`–`05l` evaluators follow `04-phase-execute` in the pipeline; they did not renumber with the phase and must not be "corrected" to match it.
- **Development fixtures keep legacy phase identifiers.** `dev/phase-final-review/fixtures/PHASE_05/` (pseudo-subphases `PHASE_05a`/`PHASE_05b`) and the report root `dev/phase-final-review/PHASE_05/` are synthetic identifiers pinned to recorded commit SHAs. Renaming them would invalidate the fixture contract.

## Release Verification

- **"Remediated in code" is not "verified".** Phase 02's P2-SEC-01..03 fixes and Phase 01's SEC-01 fix exist in code, but a fix without a re-run gate is not a release verdict. Status lines move only on fresh final-state evidence — this is the operational form of the Final Review Contract below.
- **A fixed budget must never be relaxed to make a gate pass.** PERF-01's 50 ms propagated-guard budget was silently raised to 90 ms in PR #22 to mask a failure; that was reverted. If a budget is genuinely unachievable, the honest outcome is an explicit user-approved AC change, not a quietly edited threshold.
- **PERF-01's AC was reshaped by explicit user approval on 2026-07-16 — this is that escape hatch being used correctly, and the distinction matters.** What was unachievable was never the 50 ms number (the guard costs ~30 ms); it was asserting a *wall-clock median* on a machine whose load is not controlled, which left ~20 ms of headroom against ambient noise and failed 2 of 6 focused runs while the guard itself was unchanged. The replacement asserts a **calibrated relative budget**: a bare-interpreter baseline captured in the same run, with the guard's cost measured above it. How much latency is acceptable did not change; what is measured did. The guardrail that keeps this distinct from the PR #22 edit is a required acceptance criterion that **a deliberately slowed guard must still fail the new gate** — a reshape that cannot fail a real regression is a deletion wearing a disguise. Any future AC reshape must carry an equivalent proof.
- **Fixes made outside the pipeline still need phase records.** Hook-command project-root anchoring and file-access-guard false-positive tuning both changed shipped behavior during ad-hoc debugging sessions with no phase record. Reconciling them is Phase 04 scope. (Recorded 2026-07-16.)

## Deferred Pipeline Work

- `04 Phase - Execute` still uses one consolidated QA-writer invocation for all features, so per-feature `eval: qa <task>` checkpoints cannot be both phase-shared and feature-local. A future phase must either move QA invocation into each feature cycle or redefine QA checkpointing as a single phase-level commit.
- **Pre-edit file backup layer** (snapshot protected-adjacent files before Edit/Write, config-gated) was cut from Hooks Phase 01 during refinement. Candidate for the format-on-save/completion-gates phase, which owns edit-time hooks — that phase is **Phase 05** as of the 2026-07-16 renumber (it was Phase 03 when this note was written). (Recorded 2026-07-14; renumber noted 2026-07-16.)
- **WebFetch as an exfiltration channel** is deliberately unguarded in Hooks Phase 01 (the guard blocks reading secrets in the first place). Addressed: pulled into Hooks Phase 02 scope as the WebFetch exfiltration guard deliverable (see `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`). (Recorded 2026-07-14.)
- **Plugin packaging as a distribution target**: propagation could emit a Claude Code plugin package (`${CLAUDE_PLUGIN_ROOT}`-relative hook paths) so others install the hook suite with one command, no cloning. Deferred; best revisited after the hook phases stabilize the hook set — written 2026-07-14 as "after Hooks Phases 01–03", which under the pre-renumber scheme meant **01, 02, and what is now Phase 05**. It does not mean the current Phase 03 (Phase Final Review), and Phase 04 does not unblock it. Folded into the adoption-readiness item below. (Recorded 2026-07-14; renumber ambiguity resolved 2026-07-16.)
- **Adoption readiness is unplanned work with no roadmap entry.** Phases 01–04 are scoped for an audience of the author and friends — people who can ask a question and get an answer. That assumption is what makes three residual risks acceptable: Codex's partial tool coverage stays documented rather than redesigned, the file-access guard's friction profile stays hand-tuned to one workflow, and distribution stays "clone and run propagation". Adoption beyond that circle invalidates all three, because partial protection that reads as total protection is worse than none once the user cannot ask. A future phase would need: a packaged install path (see plugin packaging above), a friction budget tunable without editing rule files, recovery/kill-switch docs written for a stranger, an upgrade path when rules change, and install-time disclosure of Codex's coverage gap. **This needs a roadmap entry from `@project-planner`; it is explicitly out of scope for Phase 04.** (Recorded 2026-07-16.)

## Propagation Contracts

- The current master-asset propagator's generated roots are `claude/`,
  `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are
  not generated destinations. Future feature plans must name the actual roots
  or explicitly add an adapter.
- `$source` metadata is guaranteed for propagated hook JSON entries, not for
  generated skill Markdown or agent Markdown/TOML. Downstream checks must not
  require that metadata on non-hook assets without a corresponding propagator
  change.

## Final Review Contracts

- Missing or incomplete required checks are a hard readiness gate: the canonical verdict is `NO-GO`, and an unverified verdict must not update roadmap or summary status lines.
- Status write-back must resolve both target lines before editing and preserve both files unchanged if either target is ambiguous or a verification step fails.
- Diff-scoped evaluators that call repo-wide analysis must require verifiable added-line attribution; touched-file filtering alone is insufficient for phase findings.
- Read-only dependency vulnerability checks must use supplied local evidence or an explicitly offline audit mode; network-capable commands are treated as unavailable.
- Final-review evaluator fixture dry-runs remain required release evidence for agent wiring and degradation behavior when static contract review cannot observe runtime report creation.
- 05i history mining is deferred until the evaluator has a narrowly scoped read-only git/PR evidence input or receives a verifiable history bundle from its orchestrator; do not restore unrestricted shell/Bash permissions to satisfy AC3/AC8.
- A fixture readiness run with required evaluators recorded as `not-run` remains artifact-level, below-GO evidence; future orchestration must rerun the complete collaboration flow before treating AC5 as complete or promoting write-back.
- A remote/hosted read-only fetch capability may supply commit and PR evidence for history-mining agents, but unavailable endpoints or local-only history still require a verifiable bundle from the orchestrator; never substitute shell/Bash access.
