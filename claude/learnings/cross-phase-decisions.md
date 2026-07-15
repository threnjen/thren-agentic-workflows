# Cross-Phase Decisions

## Deferred Pipeline Work

- `04 Phase - Execute` still uses one consolidated QA-writer invocation for all features, so per-feature `eval: qa <task>` checkpoints cannot be both phase-shared and feature-local. A future phase must either move QA invocation into each feature cycle or redefine QA checkpointing as a single phase-level commit.
- **Pre-edit file backup layer** (snapshot protected-adjacent files before Edit/Write, config-gated) was cut from Hooks Phase 01 during refinement. Candidate for Hooks Phase 03, which owns edit-time hooks. (Recorded 2026-07-14.)
- **WebFetch as an exfiltration channel** is deliberately unguarded in Hooks Phase 01 (the guard blocks reading secrets in the first place). Must-consider for Hooks Phase 02's tool-output/injection scanning scope. (Recorded 2026-07-14.)
- **Plugin packaging as a distribution target**: propagation could emit a Claude Code plugin package (`${CLAUDE_PLUGIN_ROOT}`-relative hook paths) so others install the hook suite with one command, no cloning. Deferred; best revisited after Hooks Phases 01–03 stabilize the hook set. (Recorded 2026-07-14.)