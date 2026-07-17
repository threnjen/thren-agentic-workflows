# Phase 7: Package for General Use

**Status**: Planned
**Depends on**: Phases 01, 02, 04 (deployment machinery), 05, 06 (the complete hook set — package once, not three times). Runs last; execution order is 01 → 02 → 03 → 04 → 05 → 06 → 07.
**Required by**: Nothing — terminal phase.
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/PHASE_07/PHASE_07_DISCOVERY_CONTEXT.md`, `dev/research/codex-hooks-mechanism/`, `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` (deployment machinery this phase extends), `docs/phases/PHASE_02/PHASE_02-security-scan.md` (P2-SEC-01..03), `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` (PR Review rescope; verdict evidence), `docs/hooks/prompt-injection-defense.md`, `.github/learnings/cross-phase-decisions.md`

## What's New

Distribution. Today the hook suite protects exactly one repository: this one. Hook wiring is generated only into this repo's own config surfaces (`.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/`), anchored to paths that resolve nowhere else, while `--runtime-deploy` ships agents, commands, skills, and learnings to the user's home — but not hooks. The hooks this project authors mean nothing without a path out.

This phase makes the hooks **global**: hook scripts deployed to stable home locations through the same reviewed managed-copy machinery Phase 04 built, and hook wiring registered in user-level harness config so hooks fire in every repo the user works in. All three harnesses support user-global hook registration (verified from primary sources — see Technical Context). The phase then verifies the packaged install live — the first live agent-session testing this project has ever run — and issues the release verdicts (Phase 02, Phase 03) that have been waiting on that evidence.

## Objective

A stranger can install the hook suite into their environment with one reviewed command, have it protect every repo they work in, opt out per-project, recover when it blocks them, and upgrade when rules change — with per-harness coverage disclosed honestly at install time. Then: live verification of that install, and evidence-backed verdicts for the phases that have been waiting on live QA.

## Audience and Bar

This phase *changes* the audience assumption. Phases 01–06 are scoped for the author and friends; this phase is what makes the suite fit for anyone else. That is why recovery docs written for a stranger, per-repo opt-out, and install-time disclosure are deliverables here rather than niceties.

Platform bar: the author has macOS only. **macOS is the sole live-evidence platform; Linux, native Windows, and WSL are recorded `NOT RUN` by hardware constraint** — permanently for this phase, not as a gap to close. Phase 04's cross-platform conditions stay open; this phase does not claim to close them.

## Scope

### In Scope

- **Per-harness global-hook verification** — confirm live, and pin version gates for, each harness's user-global hook mechanism: Claude Code (`~/.claude/settings.json`), OpenCode (global config/plugin directory), and Codex (`~/.codex/hooks.json` / `[hooks]` in `~/.codex/config.toml`). The mechanisms are documented as existing; the deliverable is a verified support matrix with version prerequisites that the deployment design and install docs consume.
- **Global hook deployment** — a `hooks` asset class in the `--runtime-deploy` managed-copy flow (scripts + config to stable home paths), plus wiring registration in user-level harness config, with the same review/digest/collision-preservation contract as the existing asset classes. User-level config files (e.g. `~/.claude/settings.json`) are user-owned and merged, never overwritten.
- **Per-repo opt-out** — a global install fires everywhere, so a per-project "not here" mechanism is required, built on the framework's existing config layering. Includes fixing the kill-switch asymmetry: the scanner's disable mechanism must not remain "create a file to disable, delete it to restore" once a stranger depends on it.
- **Install, upgrade, and recovery path** — one documented install command; a defined upgrade story when upstream rules change (including Codex's per-hook hash-based re-trust, which makes upgrades non-silent there); recovery/kill-switch docs written for someone who cannot ask the author.
- **Install-time disclosure** — per-harness support tiers and prerequisites surfaced where the installer runs: Codex partial tool-hook coverage and minimum version, Codex `max_depth` operator prerequisite, OpenCode plugin caveats.
- **REPO-SEC-06** — propagation containment via the single canonical no-follow contract; this phase owns the propagation write path anyway.
- **Live packaged-install QA (macOS)** — a fresh repo with no connection to this project, installed via the packaged path, with the scanner proven to fire; opt-out and recovery proven; the runtime-only enforcement tiers covered (PostToolUse output replacement, Stop behavior, subagent contexts), per harness.
- **Verdicts and record reconciliation** — Phase 02 security gate re-run against final-state code (P2-SEC-01/02/03, all three overflow paths); DOC-01 `PENDING` SHAs closed; project-root anchoring record written; Phase 03 verdict issued from evidence (including live PR Review run evidence); documentation matched to verified reality with test assertions updated in lockstep.

### Out of Scope

- New hook capabilities beyond what packaging itself requires. Phases 05 and 06 own new hooks.
- Non-macOS live evidence (hardware constraint; recorded `NOT RUN`).
- The `05a`–`05g` PR Review agent family's internals — Phase 03's rescope owns them; this phase only consumes run evidence for the verdict.
- Public registry publication (npm, marketplace, Homebrew). Install is "from a clone or release artifact of this repo"; a hosted channel is future work if adoption warrants it.
- Closing Phase 04's Linux/Windows/WSL evidence conditions.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Harness hook-support matrix | Live confirmation and version-gate pinning of user-global hooks on Claude Code, Codex, and OpenCode, from primary sources plus local verification. Consumed by deliverable 2's design and deliverable 3's docs. | Harness verification |
| 2 | Global hook deployment | `hooks` asset class in `--runtime-deploy` + user-level wiring registration + per-repo opt-out. Same review/digest contract as existing classes; user-owned config merged, never clobbered, with a restore path. | Deployment build |
| 3 | Stranger-grade docs | Install command, upgrade story (incl. Codex re-trust), recovery/kill-switch docs, install-time per-harness disclosure. | Docs |
| 4 | REPO-SEC-06 containment | Canonical no-follow contract routed through the existing helper (`_validate_nested_output_directory`) — not a second helper. | Propagation security |
| 5 | Live packaged-install QA | First live multi-harness QA, on macOS, against a fresh repo via the packaged install path. Early smoke pass + full tail walkthrough. | QA execution |
| 6 | Verdicts & reconciliation | Phase 02 gate re-run; Phase 02/03 user-issued verdicts from fresh evidence; DOC-01 SHAs; anchoring record; docs/tests in lockstep. | Records/verdicts |

## Technical Context

### Harness global-hook support (researched 2026-07-17; report in `dev/research/codex-hooks-mechanism/`)

- **Claude Code**: hooks in `~/.claude/settings.json` apply to all sessions in every repo. First-class.
- **Codex**: user-global hooks exist and are official — `~/.codex/hooks.json` (highest precedence) or `[hooks]` in `~/.codex/config.toml`, merged **additively** with repo-level hooks (all matching hooks run). The event set and decision protocol are Claude-Code-shaped: `PreToolUse` can deny via exit code 2 or JSON `permissionDecision`, and can rewrite tool inputs. Caveats that shape this phase: **per-hook hash-based trust** (regenerating a hook command changes its hash and requires re-trust via `/hooks` — upgrades are non-silent); not all shell calls are intercepted (only "simple" ones under `unified_exec`); an open bug where `codex exec` non-interactive mode does not dispatch repo-level `hooks.json` hooks (verify whether the user-global layer is affected during live QA); minimum version ~v0.123 (late Apr 2026) for the full feature set; enterprise `requirements.toml` can suppress user/project hooks entirely.
- **OpenCode**: global plugin/config directory (`~/.config/opencode/`) is already a deployment destination for skills; hooks ride the plugin mechanism. The plugin working-directory caveat from prior QA notes still applies.

### Deployment machinery

- **The managed-copy flow is built and reviewed** — `scripts/runtime_deployment.py`'s `_ASSET_POLICIES` is where a `hooks` asset class lands; the review/digest/collision flow extends rather than being redesigned. The genuinely new part is **wiring registration**: existing asset classes copy directories, while hook wiring must *merge into user-owned config files* — a new write mode needing its own collision rules and restore path.
- **Config layering already supports global-with-override** — the framework loads repo defaults → project overrides; per-repo opt-out builds on this, not on new mechanism.
- **Kill-switch asymmetry**: `.github/hooks/config/injection-overrides.json` absent = enabled, present = disabled; restoring means deleting, not writing `{}`. Any live QA that provokes the scanner arms the switch first. The packaged design should remove the asymmetry.
- **Watcher staleness**: a long-running `--watch` propagator executes pre-change code; propagator changes here require watcher restart before any deployment, as Phase 04's flow already enforces.

### Phase 02 gate specifics (unchanged from the prior scope)

- P2-SEC-02 covers **three** overflow paths — the scan-byte cap, the encoded-candidate budget, and `max_decoded_bytes`. The fail-closed block/replace behavior lives in `.github/hooks/scripts/injection-scanner.py`, not the lib module (which only truncates and raises a notice); a classification drawn from the lib alone is a false negative.
- Every finding classification names the revision it examined; every evidence artifact must post-date the code it covers. The stale-scan history behind this rule is recorded in `.github/learnings/cross-phase-decisions.md`.
- **Test entry points**: `.venv/bin/python -m pytest tests/` (system `python3` lacks pytest).

### Test impact

- `docs/hooks/prompt-injection-defense.md` is pinned by exact-string test assertions (`"NOT RUN"`, dated residual-risk approval); deliverable 6's documentation corrections require lockstep assertion updates. These documents are test-asserted by design.
- Deliverable 2 changes propagation/deployment code covered by `tests/test_phase04_runtime_deployment.py` and `tests/test_propagate_master_assets.py`; expect additions for the new asset class and the config-merge write mode, including collision and restore cases.

## Dependencies & Risks

- **Dependency**: Phases 05 and 06 must land first — their hooks are part of what gets packaged, and packaging before they exist means packaging twice.
- **Risk — merging into user-owned config files.** `~/.claude/settings.json` and `~/.codex/hooks.json` may contain the user's own hooks and settings; a bad merge breaks their environment in every repo at once. This is the highest-blast-radius write the project has attempted; it inherits the review-before-mutate contract and needs its own restore path.
- **Risk — Codex re-trust friction.** Hash-based per-hook trust means every upgrade prompts re-approval on Codex. Not fixable from this side; must be disclosed, and the upgrade docs must walk through it.
- **Risk — consequence of running last**: Phase 02 carries its NO-GO (unverified) status through Phases 05 and 06. Accepted deliberately: the scanner protects only this repo until this phase runs, and its verdict waits for the live QA this phase owns.
- **Risk — live QA reveals more work.** It has never run; it is the most likely source of surprises. Mitigated by the findings containment rule below and by an early smoke pass.

### Findings containment rule

New findings surfaced during this phase are fixed here **only if High or Critical**. Medium and below are recorded with routing and deferred. The rule cuts both ways and is not a lever: a finding is not promoted to High because fixing it is desirable, and not demoted because fixing it is inconvenient.

## Success Criteria

- [ ] A harness hook-support matrix exists with primary-source citations and live local verification, and the deployment design records which mechanism each harness uses, with minimum-version prerequisites documented at install time.
- [ ] `--runtime-deploy` ships hook assets and registers user-level wiring under the same reviewed-inventory contract; user-owned config is merged, never clobbered, with a verified restore path.
- [ ] A repo with no connection to this project is protected by the scanner after a documented install, verified live on macOS per harness; opt-out and recovery verified live; runtime-only enforcement tiers covered.
- [ ] Per-repo opt-out exists and the kill-switch restore is no longer delete-to-enable.
- [ ] Install docs, upgrade story (including Codex re-trust), recovery docs, and per-harness disclosure exist and are written for a stranger.
- [ ] REPO-SEC-06 is resolved through the existing canonical helper rather than a second one.
- [ ] The Phase 02 security gate has been re-run against final-state code and records a verdict derived from fresh evidence for P2-SEC-01, P2-SEC-02 (all three overflow paths), and P2-SEC-03.
- [ ] Phase 02 and Phase 03 have user-issued, evidence-backed verdicts — GO or NO-GO, either is a valid outcome.
- [ ] No implementation record retains a `PENDING` commit SHA; the project-root anchoring has a phase record.
- [ ] Every piece of evidence post-dates the last change to the code it covers; Linux, native Windows, and WSL rows are recorded `NOT RUN` (hardware constraint).

## QA Considerations

This phase carries the project's **first live agent-session testing**. Manual QA docs are mandatory.

- **A smoke pass runs early, not at the tail** — as soon as deliverable 2 can deploy anything, prove one hook fires in one fresh repo on one harness. This project's hooks have contradicted a passing test suite live before; a green suite is not live evidence.
- Live QA must cover the enforcement tiers that only exist at runtime: PostToolUse output replacement, Stop behavior, and subagent contexts — per harness, not once.
- Codex QA must additionally verify: global-layer hooks fire in interactive sessions, whether the `codex exec` dispatch bug affects the user-global layer, and the re-trust flow after a regeneration.
- Recovery needs live verification: kill switch, per-repo opt-out, uninstall/restore of merged user config, and the property that a hook failure never requires a blocked tool to recover from.
- QA records `NOT RUN` honestly where a platform or harness is unavailable. A missing check is a below-GO input, not an omission.

## Notes for Feature - Decomposer

Suggested feature boundaries, ordered:

1. **Harness hook-support verification** — first, small, blocks deliverable 2's design decisions. Codex needs the most attention (version gate, trust flow, `codex exec` behavior); Claude/OpenCode are confirmations.
2. **Hooks asset class + wiring registration** — the core build. The merge-into-user-owned-config write mode is the risky half; suggest splitting it into its own reviewable increment with collision and restore tests. Suggested implementation shape, to be verified by Feature Decomposer against current code and tests: extend `_ASSET_POLICIES` and the inventory/review flow in `scripts/runtime_deployment.py`.
3. **Opt-out + kill-switch rework** — depends on 2's config layout; removes the delete-to-enable asymmetry.
4. **REPO-SEC-06 containment** — independent of 1–3; parallel-safe.
5. **Docs + disclosure** — after 2 and 3 stabilize the install surface.
6. **Live packaged-install QA** — early smoke pass as soon as 2 can deploy; full walkthrough at the tail against the final state. Scratch repo, kill switch armed first. Must not double-record findings already surfaced by the smoke pass.
7. **Verdicts & reconciliation** — strictly last; consumes QA evidence plus live PR Review run evidence for Phase 03. The phase's defining rule: **no status line moves without fresh evidence**, and verdicts are issued by the user, by hand — no feature writes one.
