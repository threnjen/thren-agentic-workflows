# Project Roadmap: PR Review + Agent Distribution

## Vision

A source-of-truth repository of pipeline agents, skills, and instructions — headlined by
**PR Review**, the `05-` orchestrator agent family that evaluates a branch's diff against
its base and hands back a single advisory go/no-go readiness report — propagated to
Claude, Codex, and OpenCode outputs and deployable to user homes via the reviewed
managed-copy flow, with a final packaging phase that makes the agent suite installable
by people who are not this repo's author.

**Vision rewrite (2026-06-17):** this project was originally a security/determinism
*hook* project (prompt-injection defense, file-access guards, format-on-save, skill
enforcement, completion gates). The user cancelled the hook effort in full. Phase 05 now
removes all hook functionality and its documentation record from the repository; the
prompt-injection scanner is retained on disk as an explicitly defunct artifact, and
`docs/inspiration/` is kept as research history. No bypass-permissions security claim
survives. Phase docs for the hook phases (01, 02, 04) are deleted by Phase 05; git
history is the archival record.

## Phase Numbering

**Numbers are identity, not execution order — read the `Depends On` column.** Agent
names (`05-pr-review`, `05a`–`05g`) mark pipeline position, not the phase that built
them.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Hook Foundation + File-Access Guard | **Historical — superseded by hook cancellation** | — | — | Built the Python hook framework and (retired earlier by Phase 04) the file-access guard and Bash analyzer. All surviving hook assets are removed or marked defunct by Phase 05. Its phase docs are deleted by Phase 05; see git history. |
| 02 | Prompt-Injection Defense | **Historical — scanner retained on disk, defunct** | — | — | Built the injection scanner, corpus, and multi-harness wiring. Never reached GO. Under the hook cancellation, the scanner code stays in `.github/hooks/` unwired and marked DEFUNCT; its wiring, tests, and phase docs are removed by Phase 05. |
| 03 | PR Review agent family | Partially implemented — rescoped; diff-scoped orchestration re-planned | None | Medium | `05-pr-review` orchestrator + `05a`–`05g` evaluator subagents + 2 rescoped skills, scoped to the diff between the current branch and its base: merge-base worktree, change narrative, artifact/consistency/dependency sweeps, test health, delegated diff-scoped security scan, and go/no-go readiness synthesis. Base is suggested and user-confirmed; all questions asked in one upfront block; reports land at `dev/pr-review/<base-sha-short>-<timestamp>/`; the verdict is advisory. The first live end-to-end run was started 2026-06-17 on a real external repo; its outcome is this phase's key open evidence. |
| 04 | Hook Retirement & Cross-Platform Deployment | **Historical — deployment machinery retained** | — | — | Retired the file-access guard and Bash analyzer, and built the reviewed managed-copy `--runtime-deploy` flow (convergence gate, inventory digest, watcher-restart confirmation). The deployment machinery is live and carried forward; the hook-specific remainder and the phase docs are removed by Phase 05. |
| 05 | Hook Removal | **Planned — next to run** | None | Medium | Removes all hook functionality and its documentation record: deletes the propagator's entire hook-emission pipeline, unwires generated harness configs, deletes the hook framework and `tests/hooks/`, purges phase docs 01/02/04 and the decision log's hook sections (line-level scrub in mixed sections), and scrubs the standard docs. Keeps: the injection scanner on disk marked DEFUNCT, the `done-notify` notification converted to static hand-committed harness config (no longer propagated), and `docs/inspiration/`. See `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`. |
| 06 | Package Agents for General Use | Planned — needs re-planning | Phases 03, 05 | Medium | Makes the **agent suite** (agents, commands, skills, learnings — the asset classes `--runtime-deploy` already ships) installable and upgradable by strangers: install/upgrade/recovery docs and a reviewed one-command path. **No hooks.** The existing `docs/phases/PHASE_06/` documents describe the pre-cancellation hook-packaging scope and are stale; return to `@project-planner` after Phase 05 completes to rewrite them. |

## Constraints & Non-Goals

- **Runtime**: propagation and deployment tooling is Python 3; tests run via
  `.venv/bin/python -m pytest tests/`.
- **Distribution**: `.github/` is the source of truth; `scripts/propagate_master_assets.py`
  generates the Claude, Codex, and OpenCode outputs and prunes orphans;
  `--runtime-deploy` performs reviewed managed-copy deployment to user homes.
- **Non-goal**: generated or managed hooks of any kind — enforcement, formatting,
  security, or otherwise. The hook effort is cancelled; the propagator has no hook
  pipeline and nothing may quietly re-add one. The sole surviving hook wiring is the
  `done-notify` Stop notification, kept as static hand-committed harness config, not a
  managed asset.
- **Non-goal**: adopting any surveyed repo wholesale; `docs/inspiration/` is reference
  history only.
- **Non-goal**: notification/TTS beyond the retained `done-notify`, telemetry, and
  duplicate agents.

## Architecture Notes

- **Propagation and runtime deployment**: `propagate_master_assets.py` emits the
  generated Claude, Codex, and OpenCode outputs, prunes retired owned outputs, and can
  hand a converged result to the managed-copy runtime deployment flow. `--runtime-deploy`
  first emits a home-relative, content-bound inventory; mutation requires the reviewed
  digest and watcher-restart confirmation. Long-running `--watch` processes execute the
  propagation code they started with, so propagator edits require a watcher restart.
- **PR Review**: a branch's base is not recoverable from git, so it is suggested
  (`origin/HEAD` → `origin/main` → `origin/master` → candidates) and user-confirmed.
  The readiness verdict is advisory by design — nothing blocks a merge on NO-GO.
- **Defunct scanner**: `.github/hooks/` retains the prompt-injection scanner code,
  unwired and marked DEFUNCT, per the 2026-06-17 cancellation decision. It is not part
  of the product and must not be counted in asset inventories.

## Research Base

Ten surveyed repos are inventoried in `docs/inspiration/` (one file per repo + README
comparison), kept as research history. Attribution remains in `README.md`
(§ Acknowledgments).
