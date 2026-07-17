# Project Roadmap: Security & Determinism Hooks + PR Review

## Vision

A propagated, source-of-truth hook system (Python stdlib, under `.github/hooks/`) that hardens every project against prompt injection and file/secret manipulation — even under bypass permissions — and converts agent-judgment steps in the existing pipeline (formatting, completion claims, skill activation) into deterministic, testable gates. All hooks are original implementations that improve on patterns surveyed in `docs/inspiration/`, never direct copies. The project also adds **PR Review** — a `05-` orchestrator agent family that evaluates the diff between a branch and its base when the branch is ready to open a pull request, and hands back a single advisory go/no-go readiness report.

## Phase Numbering 

| Old | New | Phase |
|-----|-----|-------|
| 01 | Hook Foundation + File-Access Guard (unchanged) |
| 02 |  Prompt-Injection Defense (unchanged) |
| 03 | PR Review agent family |
| 04 | Release Remediation & Verification (new) |
| 05 | Format-on-Save + Completion Gates |
| 06 | Skill Enforcement / Auto-Activation |

Agent names deliberately did **not** renumber. The `05-pr-review` orchestrator and its `05a`–`05g` evaluators mark pipeline position (`01-project-planner` → `02-phase-refiner` → `03-feature-decomposer` → `04-phase-execute` → `05-pr-review`), not the phase that built them. That Phase 03 ships `05-` agents is correct and intentional.

## Phases

Listed in execution order.

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Hook Foundation + File-Access Guard | Implemented — release blocked (PERF-01 open) | None | Large | Python hook framework (shared helpers, config layering, fail-closed posture, tests) plus a tiered PreToolUse guard (deny secrets/protected files incl. Grep coverage and self-protection; ask for destructive commands) with bash-command parsing for indirect access and path normalization against symlink/traversal evasion. Hybrid deployment: per-project propagation is the committed contract; generated user-global wiring is a local-only extra; ships a multi-harness install guide. **SEC-01 (nested-destination symlink escape) is fixed and regression-covered.** **PERF-01 (unstable sub-50 ms propagated-guard latency) remains open** and is owned by Phase 04. |
| 02 | Prompt-Injection Defense | Implemented — release blocked (NO-GO) | Phase 01 | Large | Scanner, clean-room corpus/benchmark, URL-payload guard, and multi-harness wiring. **P2-SEC-01, P2-SEC-02, and P2-SEC-03 have been remediated in code**, but the phase stays NO-GO until the security gate is re-run against those fixes and live harness QA is executed. Codex remains Partial under accepted residual risk. Verification is owned by Phase 04. |
| 03 | PR Review agent family | Partially implemented — rescoped; diff-scoped orchestration re-planned | None (independent of the hook phases; uses existing pipeline assets) | Medium | `05-pr-review` orchestrator + `05a`–`05g` evaluator subagents + 2 rescoped skills, scoped to the diff between the current branch and its base: merge-base worktree, change narrative, artifact/consistency/dependency sweeps, test health, delegated diff-scoped security via the existing `04e-diff-security-scan`, and go/no-go readiness synthesis. A branch's base is not recoverable from git, so it is suggested (`origin/HEAD` → `origin/main` → `origin/master` → candidates) and user-confirmed. All questions — model-tier warning, base confirmation, and the opt-in PR-comment choice — are asked in one upfront block; the run then reaches a report unattended. Reports land at `dev/pr-review/<base-sha-short>-<timestamp>/`; the agent writes no status lines and the verdict is advisory. Adds orphan pruning to `propagate_master_assets.py`, without which every retirement and rename strands a live artifact in the generated roots. Retires five phase-shaped evaluators. Per-agent command scoping is out of scope — it is not expressible in Claude subagent frontmatter and needs a PreToolUse hook, so `execute` is narrowed by removal where it is not required and declared where it is. Formerly Phase 05, and formerly the Phase Final Review family. |
| 04 | Hook Release Remediation & Verification | Planned — **next** | Phases 01, 02 | Medium | **Hooks only.** Close every open hook blocker and prove it with evidence: reshape PERF-01's gate to a calibrated relative budget (user-approved 2026-06-16; the 50 ms budget's meaning is unchanged and a deliberately slowed guard must still fail), fix the bash-rewrite bypass where a PreToolUse rewrite hook can invalidate the guard's own classification (ordering guarantee + pinned binary + regression), re-run the Phase 02 security gate against final-state code, security-review all 17 loosened guard rules, resolve REPO-SEC-06 containment, execute the live Claude/Codex/OpenCode QA that is `NOT RUN` for both phases, and reconcile records. **The `05a`–`05l` agent family is explicitly out of scope** — Phase 03 rescopes it in place into the PR Review family, so its `execute` grants, propagation-enumeration gap, and P5-SEC-02 are handled there rather than fixed here on code slated for rewrite. Phase 03 closes the enumeration gap and removes `execute` from the evaluators that do not need it, but **cannot close the grants themselves**: per-agent command scoping is not expressible in Claude subagent frontmatter and requires a PreToolUse hook, so `05a`'s `git worktree` grant and the orchestrator's `git`/`gh` grant stay open, declared with justification and routed to a hook-owning phase. P5-SEC-02 is expected to stay open for the same reason — it closes in code, and Phase 03 ships agent Markdown. Phase 03 gets a NO-GO issued here from existing evidence, superseded rather than repaired. Verdicts are issued by the user by hand. Scoped for an audience of the author and friends; adoption readiness is deferred. |
| 05 | Format-on-Save + Completion Gates | Planned | Phases 01, 04 | Medium | Project-aware formatter dispatch on edit for consuming projects (this repo has no formatter toolchain of its own), plus Stop-time verification gates that block unverified "done" claims using this repo's pipeline artifacts as evidence. Owns edit-time hooks, including the pre-edit file backup layer deferred from Phase 01. Formerly Phase 03. |
| 06 | Skill Enforcement / Auto-Activation | Planned | Phase 01 (framework), Phase 04; informed by 01–05 tuning | Large | Rules file mapping globs/keywords → required skills; UserPromptSubmit suggestion injection + PreToolUse guard with block/suggest/warn enforcement levels, propagated multi-harness. Formerly Phase 04. |

## Current Release Status

No phase is releasable today. Phases 01, 02, and 03 are all implemented but release-blocked, and **live harness QA has never been run for any of them**. Phase 04 exists to close that gap in one pass rather than three.

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
- **Propagation**: `propagate_master_assets.py` emits Claude settings wiring, Codex `hooks.json`, OpenCode plugins, `$source` tags, per-project script/config emission, and an optional generated user-global layer (absolute paths, local-only, gitignored). Long-running `--watch` processes execute the propagation code they started with; edits to the propagator require a watcher restart to take effect.
- **Phase ordering rationale**: Phase 01 builds the framework everything reuses and closes the highest-stakes gap. Phase 02 is an independent consumer of that framework. Phase 03 (PR Review) has no dependency on the hook phases and was deliberately taken out of the original order after Phase 02. Phase 04 converts three release-blocked phases into releasable ones before more surface area is added. Phases 05 and 06 then build on a verified foundation, with 06 last because it is the most invasive to the working agent pipeline and benefits from pattern-tuning experience in 01–05.

## Research Base

Ten surveyed repos are inventoried in `docs/inspiration/` (one file per repo + README comparison). Key design references per phase are cross-referenced in each phase summary and in `DISCOVERY_CONTEXT.md`. Attribution is published in `README.md` (§ Acknowledgments).
