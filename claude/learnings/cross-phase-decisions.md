# Cross-Phase Decisions

## Deferred Pipeline Work

- `04 Phase - Execute` still uses one consolidated QA-writer invocation for all features, so per-feature `eval: qa <task>` checkpoints cannot be both phase-shared and feature-local. A future phase must either move QA invocation into each feature cycle or redefine QA checkpointing as a single phase-level commit.
- **Pre-edit file backup layer** (snapshot protected-adjacent files before Edit/Write, config-gated) was cut from Hooks Phase 01 during refinement. Candidate for Hooks Phase 03, which owns edit-time hooks. (Recorded 2026-07-14.)
- **WebFetch as an exfiltration channel** is deliberately unguarded in Hooks Phase 01 (the guard blocks reading secrets in the first place). Addressed: pulled into Hooks Phase 02 scope as the WebFetch exfiltration guard deliverable (see `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`). (Recorded 2026-07-14.)
- **Plugin packaging as a distribution target**: propagation could emit a Claude Code plugin package (`${CLAUDE_PLUGIN_ROOT}`-relative hook paths) so others install the hook suite with one command, no cloning. Deferred; best revisited after Hooks Phases 01–03 stabilize the hook set. (Recorded 2026-07-14.)

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
