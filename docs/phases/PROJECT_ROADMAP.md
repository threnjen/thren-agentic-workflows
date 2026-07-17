# Project Roadmap: Security & Determinism Hooks + PR Review

## Vision

A propagated, source-of-truth hook system (Python stdlib, under `.github/hooks/`) that hardens every project against prompt injection and file/secret manipulation — even under bypass permissions — and converts agent-judgment steps in the existing pipeline (formatting, completion claims, skill activation) into deterministic, testable gates. All hooks are original implementations that improve on patterns surveyed in `docs/inspiration/`, never direct copies. The project also adds **PR Review** — a `05-` orchestrator agent family that evaluates the diff between a branch and its base when the branch is ready to open a pull request, and hands back a single advisory go/no-go readiness report.

## Phase Numbering 

| Phase | Name | Runs |
|-------|------|------|
| 01 | Hook Foundation + File-Access Guard | 1st |
| 02 | Prompt-Injection Defense | 2nd |
| 03 | PR Review agent family | 3rd |
| 04 | Hook Retirement & Cross-Platform Deployment | 4th |
| 07 | Hook Release Remediation & Verification | **5th** |
| 05 | Format-on-Save + Completion Gates | 6th |
| 06 | Skill Enforcement / Auto-Activation | 7th |

**Numbers are identity; the `Depends On` column is execution order.** Two places in this project already work that way, and both are deliberate:

- **Agent names did not renumber.** The `05-pr-review` orchestrator and its `05a`–`05g` evaluators mark pipeline position (`01-project-planner` → `02-phase-refiner` → `03-feature-decomposer` → `04-phase-execute` → `05-pr-review`), not the phase that built them. That Phase 03 ships `05-` agents is correct and intentional.
- **Phase 07 runs before Phases 05 and 06**, which both depend on it. It was filed at 07 rather than renumbering 05→06→07, because a prior renumber is recorded as having silently changed the meaning of a deferral, and re-sequencing two more phases to preserve a tidy count would risk the same failure for no benefit.

If you are deciding what to work on next, read the dependency column. The number tells you which phase, never when.

## Phases

Listed in execution order.

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Hook Foundation + File-Access Guard | Implemented — release blocked (PERF-01 open) | None | Large | Python hook framework (shared helpers, config layering, fail-closed posture, tests) plus a tiered PreToolUse guard (deny secrets/protected files incl. Grep coverage and self-protection; ask for destructive commands) with bash-command parsing for indirect access and path normalization against symlink/traversal evasion. Hybrid deployment: per-project propagation is the committed contract; generated user-global wiring is a local-only extra; ships a multi-harness install guide. **SEC-01 (nested-destination symlink escape) is fixed and regression-covered.** **PERF-01 (unstable sub-50 ms propagated-guard latency) remains open** and is owned by Phase 07. |
| 02 | Prompt-Injection Defense | Implemented — release blocked (NO-GO) | Phase 01 | Large | Scanner, clean-room corpus/benchmark, URL-payload guard, and multi-harness wiring. **P2-SEC-01, P2-SEC-02, and P2-SEC-03 have been remediated in code**, but the phase stays NO-GO until the security gate is re-run against those fixes and live harness QA is executed. Codex remains Partial under accepted residual risk. Verification is owned by Phase 07. |
| 03 | PR Review agent family | Partially implemented — rescoped; diff-scoped orchestration re-planned | None (independent of the hook phases; uses existing pipeline assets) | Medium | `05-pr-review` orchestrator + `05a`–`05g` evaluator subagents + 2 rescoped skills, scoped to the diff between the current branch and its base: merge-base worktree, change narrative, artifact/consistency/dependency sweeps, test health, delegated diff-scoped security via the existing `04e-diff-security-scan`, and go/no-go readiness synthesis. A branch's base is not recoverable from git, so it is suggested (`origin/HEAD` → `origin/main` → `origin/master` → candidates) and user-confirmed. All questions — model-tier warning, base confirmation, and the opt-in PR-comment choice — are asked in one upfront block; the run then reaches a report unattended. Reports land at `dev/pr-review/<base-sha-short>-<timestamp>/`; the agent writes no status lines and the verdict is advisory. Adds orphan pruning to `propagate_master_assets.py`, without which every retirement and rename strands a live artifact in the generated roots. Retires five phase-shaped evaluators. Per-agent command scoping is out of scope — it is not expressible in Claude subagent frontmatter and needs a PreToolUse hook, so `execute` is narrowed by removal where it is not required and declared where it is. Formerly Phase 05, and formerly the Phase Final Review family. |
| 04 | Hook Retirement & Cross-Platform Deployment | Implementation complete — **GO WITH CONDITIONS** | Phase 01 | Large | Retired the branch-added file-access guard, its Bash analyzer, and automatic `rtk-rewrite.sh` interception while preserving RTK itself, explicit RTK usage, the shared hook framework, and prompt-injection defense. `propagate_master_assets.py` now gates managed-copy deployment on repository convergence, a reviewed active-home inventory, and watcher-restart confirmation, with per-harness isolation and ownership-safe reconciliation. Supported setup guidance no longer creates runtime links. Automated scratch-home evidence is complete, but pytest hook integration and fresh-session macOS, Linux, native Windows, and WSL evidence are `NOT RUN`; full cross-platform production GO remains unavailable. Phase 01, Phase 02, and Phase 07 status ownership remains unchanged pending `project-planner` reconciliation. |
| 05 | Format-on-Save + Completion Gates | Planned | Phases 01, 07 | Medium | Project-aware formatter dispatch on edit for consuming projects (this repo has no formatter toolchain of its own), plus Stop-time verification gates that block unverified "done" claims using this repo's pipeline artifacts as evidence. Owns edit-time hooks, including the pre-edit file backup layer deferred from Phase 01. Formerly Phase 03. |
| 06 | Skill Enforcement / Auto-Activation | Planned | Phase 01 (framework), Phase 07; informed by 01–05 tuning | Large | Rules file mapping globs/keywords → required skills; UserPromptSubmit suggestion injection + PreToolUse guard with block/suggest/warn enforcement levels, propagated multi-harness. Formerly Phase 04. |
| 07 | Hook Release Remediation & Verification | Planned | Phases 01, 02 | Medium | **Hooks only; adds no features. Required by Phases 05 and 06 despite its higher number** — see the ordering rationale below. Close every open hook blocker and prove it with evidence: reshape PERF-01's gate to a calibrated relative budget (user-approved 2026-06-16; the 50 ms budget's meaning is unchanged and a deliberately slowed guard must still fail); fix the bash-rewrite bypass where a PreToolUse rewrite hook can invalidate the guard's own classification (ordering guarantee + pinned binary + regression — independent of Phase 04's GUARD-01 fix and still open after it); re-run the Phase 02 security gate against final-state code for P2-SEC-01/02/03; security-review all 17 loosened guard rules; resolve REPO-SEC-06 containment in the in-repo write path; execute the live Claude/Codex/OpenCode QA that is `NOT RUN` for both phases; and reconcile records (DOC-01's `PENDING` SHAs, the project-root anchoring record). Phase 03 gets a NO-GO issued here from existing evidence, superseded rather than repaired. **Phases 01 and 02 have no route to a release verdict until this phase runs.** Verdicts are issued by the user by hand. Scoped for an audience of the author and friends; adoption readiness is deferred. |

## Current Release Status

No phase has an unconditional production GO today. Phases 01, 02, and 03 remain
release-blocked. Phase 04 is implementation-complete with **GO WITH CONDITIONS**:
pytest hook integration and fresh-session macOS, Linux, native Windows, and WSL
evidence are all `NOT RUN`, and the authorized active-home migration gates remain
manual. Scratch-home and simulated platform coverage do not replace those results.

Phase 04 retired the file-access guard and automatic RTK rewriting, then added
cross-platform managed-copy deployment. This retirement changes the release-blocker
inventory recorded for Phases 01 and 07 but does not move either phase's status line.
`project-planner` must reconcile the affected phase documents and project-level
security claims before their release path is treated as authoritative.

Per the Final Review contract in `.github/learnings/cross-phase-decisions.md`, an unverified verdict must not update roadmap or summary status lines. The status entries above therefore record remediation work as *done in code* while leaving the release verdicts unchanged until the gates are actually re-run.

## Constraints & Non-Goals

- **Clean-room constraint**: All hooks and skills are written from scratch. `docs/inspiration/` files are requirements/design references (which events to hook, which failure modes to cover) — never code to copy. No verbatim reuse of pattern files, scripts, or prompts from the surveyed repos. Attribution for the surveyed projects lives in `README.md` (§ Acknowledgments).
- **Runtime**: Python 3 stdlib only for hook logic (no pip dependencies in the hooks themselves). Existing bash hooks are folded in or retired as phases absorb their responsibilities.
- **Enforcement posture**: Hard-block (deny) for secrets/protected-file access, high-confidence exfiltration, and hook self-tampering — the tiers that must hold in bypass-permissions mode; `ask` (user confirmation) for destructive-but-legitimate commands and ambiguous env-var exposure; warn-and-continue for prompt-injection matches except high-confidence patterns, which block. Tier is declared per-rule in config.
- **Friction budget**: Guards must prompt for genuinely destructive actions only. Rules matching ordinary text (commit messages, search patterns, benign redirects, lock-file reads) are defects, not safety.
- **Distribution**: Hooks live in `.github/hooks/` as source of truth and are propagated to platform outputs via `scripts/propagate_master_assets.py`, consistent with agents/skills/instructions.
- **Non-goal**: Adopting any surveyed repo wholesale (claudekit binary, gstack pipeline, workflow-v2 agents/skills — the latter duplicate this repo's existing pipeline).
- **Non-goal**: Notification/TTS/sound hooks, telemetry hooks, and duplicate agents (code-reviewer, security-auditor, docs-writer variants already exist here).
- **Non-goal**: UI/design skill packs (ui-ux-pro-max is orthogonal to this effort).

## Architecture Notes

- **Hook framework**: shared Python helpers for reading the hook JSON payload from stdin, emitting decision JSON (allow/deny/block with reason), loading layered config (repo defaults → project overrides), and structured logging. Every hook is a thin entrypoint over this framework, unit-testable with pytest fixtures of real hook payloads.
- **Why hooks, not permissions**: `permissions.deny` rules do not survive bypass-permissions mode; PreToolUse hooks fire regardless of permission mode and an exit-2 result blocks the tool call. This is the mechanism that satisfies "protect files even with bypass permissions."
- **Rule/pattern configs are data, not code**: protected-file rules, injection patterns, formatter mappings, and skill rules all live in readable config files (JSON/YAML) with per-rule reasons, so they can be reviewed, tested, and tuned without touching hook logic.
- **Hook commands are anchored to the project root**: Claude Code and Codex both run hook commands with the *session* working directory, so generated wiring anchors script paths (`$CLAUDE_PROJECT_DIR` for Claude, `$(git rev-parse --show-toplevel)` for Codex, plugin `directory` cwd for OpenCode). A relative path combined with fail-closed turns any subdirectory session into a total tool-call outage.
- **Propagation and runtime deployment**: `propagate_master_assets.py` emits the generated Claude, Codex, and OpenCode outputs, prunes retired owned outputs, and can hand a converged result to the managed-copy runtime deployment flow. `--runtime-deploy` first emits a home-relative, content-bound inventory; mutation requires the reviewed digest and watcher-restart confirmation. Long-running `--watch` processes execute the propagation code they started with, so edits to the propagator require a watcher restart before deployment.
- **Phase numbers record identity, not execution order. The `Depends On` column is authoritative.** This is already true elsewhere in the project — Phase 03 ships `05-` agents because those numbers mark pipeline position — and it is now true of the phase list itself: **Phase 07 is required by Phases 05 and 06.** The alternative was renumbering 05→06 and 06→07 to keep the sequence tidy, which was rejected: the 2026-07-16 renumber is recorded below as having silently changed the meaning of the plugin-packaging deferral, and a second renumber would put two more phases at that risk to satisfy a convention the project had already abandoned. **Read the dependency column, never the number.**
- **Phase ordering rationale**: Phase 01 builds the framework everything reuses. Phase 02 is an independent consumer of that framework. Phase 03 (PR Review) has no dependency on the hook phases and was deliberately taken out of the original order after Phase 02. Phase 04 removes the two branch-added command interceptors, preserves the reusable framework and prompt-injection defense, and completes cross-platform user deployment through managed copies. The Phase 01 and Phase 07 consequences require `project-planner` reconciliation before the downstream release sequence is authoritative. Until that reconciliation occurs, the recorded execution order remains **01 → 02 → 03 → 04 → 07 → 05 → 06**.

## Research Base

Ten surveyed repos are inventoried in `docs/inspiration/` (one file per repo + README comparison). Key design references per phase are cross-referenced in each phase summary and in `DISCOVERY_CONTEXT.md`. Attribution is published in `README.md` (§ Acknowledgments).
