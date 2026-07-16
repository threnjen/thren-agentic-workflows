# Phase 1: Hook Foundation + File-Access Guard

**Status**: In Progress — implementation complete; release blocked pending Feature 04 remediation
**Depends on**: None
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01-qa-analysis.md`, `docs/hooks/installation.md`, `docs/inspiration/README.md`

## What's New

Phase 01 now provides a Python-standard-library hook framework, a config-driven file-access guard, bounded Bash-command analysis, project and generated-global distribution, and installation guidance. Automated tests verify structured decisions for protected paths, Grep, supported shell evasions, destructive-command confirmation, fail-closed guard errors, redacted logs, configuration, and legacy-rule parity. Known Bash-analysis limits remain documented rather than being presented as general shell sandboxing.

The implementation can propagate a self-contained runtime into consuming projects and can generate machine-local absolute-path wiring. That distribution is **not release-ready**: final QA reproduced an intermediate-directory symlink escape in propagation and found that the required propagated-hook latency gate is unstable. Claude Code is the only fully supported harness classification; Codex and OpenCode are partial, while Cursor and GitHub Copilot are not supported by this phase.

## Objective

Establish the Python-stdlib hook framework under `.github/hooks/` (with propagation to platform outputs) and ship its first consumer: a tiered-enforcement PreToolUse guard covering secrets, protected files, indirect access via bash, and destructive commands — closing the highest-stakes safety gap (goals 2 and 5).

## Implementation and Release Status

All four planned features have implementation and review records. The phase remains In Progress because production review is **NO-GO** until both Feature 04 blockers are fixed and re-reviewed.

| Feature | Implementation state | Release assessment |
|---|---|---|
| 01 — Hook framework | Implemented; deterministic framework tests pass | Live bypass, subagent, and recovery evidence remains pending |
| 02 — File-access guard | Implemented; path, Grep, config, and self-protection behavior is covered automatically | Live harness verification remains pending |
| 03 — Bash-command analyzer | Implemented; the 27 legacy behaviors and the documented bounded-analysis contract are covered | Published dynamic-variable, interpreter, and recursive-scan limitations require explicit risk acceptance or later hardening |
| 04 — Hook distribution integration | Implemented, including project/global emission, legacy retirement, installation docs, and temporary-consumer tests | **Blocked** by propagation containment and unstable latency evidence |

Release-blocking findings from the final QA analysis:

- **SEC-01 / F04 AC1 — destination containment**: propagation can write outside a consuming-project root through a symlinked intermediate destination directory. Every generated/copy/remove path needs canonical containment and adversarial regression coverage.
- **PERF-01 / F04 AC9 — latency stability**: the required propagated-hook median of less than 50 ms failed in the full suite and a focused rerun before later passes. The implementation needs reliable margin and repeatable evidence without weakening the threshold.

Manual QA starts only after both blockers are remediated and the feature review, security scan, QA evidence, and production review are refreshed.

### Harness Support Classification

These classifications describe implemented capability, not release approval:

| Harness | Classification | Phase 01 boundary |
|---|---|---|
| Claude Code | Fully supported | Project and generated user-scope `PreToolUse` wiring with structured allow/ask/deny decisions; final live QA is still pending |
| Codex | Partial | Project/user wiring is generated, but `ask`, runner behavior, and `apply_patch` path extraction do not provide complete equivalent enforcement |
| OpenCode | Partial | Project/global plugins launch the guard, but native decision translation and live blocking behavior are not complete |
| Cursor | Not supported | No Cursor adapter or event/decision translation is emitted |
| GitHub Copilot | Not supported | This phase does not verify the Claude-oriented adapter against Copilot's event/output contract |

## Deployment Model (decided during refinement)

Hybrid, with per-project propagation as the primary implemented contract:

- **Per-project propagation (primary, committed, shareable)**: `propagate_master_assets.py` emits hook scripts, rule config, a distribution marker, and Claude/Codex/OpenCode wiring into consuming projects using machine-agnostic relative paths. Functional detached-consumer tests pass, but the SEC-01 nested-symlink escape blocks release.
- **Generated user-global wiring (secondary, local-only)**: `scripts/setup-hook-symlinks.sh` now generates user-scope wiring with absolute paths into this repo. Generated output is machine-specific and gitignored. Claude is fully supported; Codex and OpenCode remain partial.
- **Double-fire tolerance**: automated evaluation is stateless and functionally identical when both layers run. Live dual-layer verification remains pending, and duplicate redacted audit rows can occur.

The former user-global symlink flow has been superseded by generated regular files with absolute commands. Installation, recovery, upgrade, and rollback procedures are documented in `docs/hooks/installation.md`.

## Enforcement Posture (decided during refinement)

Tiered, declared per-rule in config (never hardcoded in the engine):

- **`deny` (hard block, holds in bypass-permissions mode)**: secrets and protected-file access (read/grep/edit/write and bash-mediated equivalents); high-confidence exfiltration commands (`curl -d @<file>`, `wget --post-file`, `base64` of a protected file); tampering with the hook system's own files.
- **`ask` (pause for user confirmation)**: destructive-but-sometimes-legitimate commands (`rm -rf`, `git push --force`, `git reset --hard`, etc. — preserving current `bash-safety.sh` ergonomics); ambiguous env-var exposure (`echo $SOME_VAR`, bare `env`/`set`/`export`), which the current guard hard-denies and which false-positives on innocent commands like `echo $PATH`.

Note: the automated contract makes `deny` the bypass-resistant tier, while `ask` may not prompt in bypass-permissions mode. This split is deliberate — secrets receive the stronger decision and workflow-ergonomic rules request confirmation. Config supports a per-rule `escalate_in_bypass: deny` flag so specific rules can be hardened without a policy rewrite. Live `deny`, `ask`, bypass-mode, and subagent behavior is still awaiting the manual QA plan and must not be inferred from payload tests alone.

## Scope

### In Scope

- **Hook framework** (`.github/hooks/lib/` or equivalent): stdin JSON payload parsing, decision JSON emission (allow/ask/deny with reason), layered config loading (repo defaults → project overrides) with an mtime-checked cache to meet the latency budget (suggested implementation shape, to be verified by Feature Decomposer), structured logging with content redaction (log tool name, rule fired, and offending path — never tool_input bodies or file contents, which for a denied Write could re-expose the very secret the guard blocked), per-hook failure posture (see below), and pytest fixtures of real hook payloads for every supported event and tool.
- **Failure posture contract**: the guard fails **closed** — an unhandled error in the hook denies with a "guard error" reason rather than silently allowing (today `protect-files.py` fails open on any exception). Balanced by a documented, human-only kill switch so a buggy rule cannot brick sessions. The kill switch must be activatable only through a channel the agent cannot reach: a flag in the project override file (which is itself in the deny set) — not an environment variable, which an agent could plant via shell-profile edits. The framework makes posture per-hook: security hooks fail closed; observability hooks (audit-log) fail open.
- **File-access guard hook** (PreToolUse, matcher `Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Bash`):
  - **Path normalization before matching**: tool paths are resolved (symlinks via realpath, `~` expansion, `../` collapsing, case-insensitive comparison on case-insensitive filesystems) before rule matching — otherwise `ln -s .env notes.txt` followed by `Read notes.txt` walks straight past glob rules. Each normalization vector gets a tool-level fixture, not just a bash-level one.
  - Secrets rules: block `.env` and variants (`.env.local`, `.env.production`, …) while allowing templates (`.env.sample`, `.env.example`); credential files (`*.pem`, `*.key`, `credentials*`, tokens); SSH keys matched by exact name (`id_rsa`, `id_ed25519`, …) or by location (under `.ssh/`) — never by bare `id_*` prefix (the current rule blocks unrelated files like `id_generator.py`); cloud config locations (`.aws/`, `.kube/`, `.gnupg/`).
  - Protected-file rules: glob-based config with a per-rule `reason` and per-rule `action` (`deny`/`ask`) field (lock files, production configs, user-specified paths).
  - **Grep coverage**: Grep tool calls whose path/glob targets a protected file are denied — grep returns file contents and currently bypasses the guard entirely. Glob (filename listing only) stays unguarded.
  - **Self-protection**: in consuming projects, the propagated hook scripts, rule config, **and the hook wiring files themselves** (`.claude/settings.json`, `.claude/settings.local.json`, `.codex/hooks.json`, OpenCode plugin files) are protected paths (deny Edit/Write), and the project override file is agent-protected — overrides are a human-only escape hatch. Without wiring-file protection, an agent could disarm the guard by deregistering the hooks without ever touching a protected script. Legitimate human edits to wiring files happen outside a session or via the kill switch.
  - Bash-command analysis: parse Bash tool input to catch indirect access — `cat`/`less`/`head`/`grep`/`rg` on protected files, redirections, `cp`/`mv`, heredocs, `xargs`, subshells/command substitution, base64/`xxd` pipes, symlink traversal into protected paths, and **symlink creation pointing at protected paths** (`ln -s .env <anything>` is a deny — it is step one of a two-step read).
  - Env-var and exfiltration rules (carried forward from the existing `protect-files.py`, now explicit and tiered): `printenv` and env-dump commands, `echo $VAR` exposure, `curl`/`wget` file-posting — mapped to `deny` or `ask` per the enforcement posture above.
  - Structured messages: why it was blocked or held, which rule fired, and a suggested alternative (e.g., "read `.env.sample` instead").
- **Dangerous-command rules**: recursive-delete and similar destructive patterns, absorbing the current `bash-safety.sh` responsibilities at `ask` tier; scratchpad/temp-dir destructive operations remain allowed.
- **Consolidation**: fold existing `bash-safety.sh` and `protect-files.sh`/`protect-files.py` behavior into the new guard; retire the legacy scripts from settings wiring after regression fixtures reproduce every current block.
- **Propagation extension**: the existing hooks stage of `propagate_master_assets.py` now emits the guard entrypoint, libraries, config, distribution marker, and Claude/Codex/OpenCode wiring; the generated-global installer produces gitignored absolute-path wiring; legacy guard emission has been retired. The release blocker is destination containment for symlinked intermediate directories, not missing functional emission.
- **User-facing installation guide**: `docs/hooks/installation.md` covers Claude Code, OpenCode, Codex, Cursor, and GitHub Copilot. It classifies Claude as Fully supported, Codex/OpenCode as Partial, and Cursor/Copilot as Not supported, with limitations and verification steps. Propagation emission remains scoped to Claude/Codex/OpenCode.

### Out of Scope

- Prompt-injection scanning of tool outputs, and WebFetch-as-exfiltration-channel guarding (Phase 2 — noted in cross-phase decisions).
- Formatting, lint, and Stop-time completion gates (Phase 3).
- Skill enforcement / auto-activation (Phase 4).
- Pre-edit file backup layer (cut during refinement; deferred to Phase 03 candidate — see cross-phase decisions).
- Plugin packaging as a distribution target (deferred future capability — see cross-phase decisions).
- Guarding the Glob tool (reveals filenames only, not contents).
- Any copying of code or pattern files from `docs/inspiration/` repos (clean-room constraint — see DISCOVERY_CONTEXT.md).
- Windows support (existing setup is macOS/zsh; keep POSIX-portable but do not test Windows).
- pip-dependency-based hook logic (stdlib only).

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Hook framework | Shared Python lib: payload parsing, allow/ask/deny decision output, config layering + caching, per-hook failure posture, logging, pytest harness | framework lib; test fixtures/harness |
| 2 | File-access guard | PreToolUse hook: secrets + protected-file rules (incl. Grep coverage and self-protection) with per-rule reason/action and structured messages | rule engine; Read/Edit/Write/Grep path guard |
| 3 | Bash-command analyzer | Command parsing for indirect access, env/exfil rules, and destructive-command rules; absorbs bash-safety.sh and protect-files.py bash logic | bash parser; tiered command rules |
| 4 | Propagation + consolidation + install guide | Extend the existing hooks propagation stage for per-project script/config emission; generated-global setup step; legacy hooks retired after regression fixtures; user-facing multi-harness installation guide | propagation extension; migration/cleanup; install docs |

## Technical Context

- Current hook definitions are `.github/hooks/{file-access-guard,audit-log,done-notify}.json`, backed by `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/lib/`, and config under `.github/hooks/config/`. Legacy `bash-safety` and `protect-files` definitions/scripts have been retired after their behaviors were reproduced or deliberately re-tiered.
- `scripts/propagate_master_assets.py` emits the self-contained guard runtime, distribution marker, Claude/Codex/OpenCode wiring, and retirement cleanup. Functional tests cover detached consumers and final-file/root symlinks; intermediate-directory containment is the known release blocker.
- `scripts/setup-hook-symlinks.sh` is compatibility-named but now installs generated regular files with absolute hook commands rather than symlinking repository settings.
- Hook runtime code is Python standard library and runs via `python3` without a project virtual environment or runtime package installation. Pytest is used for development and acceptance evidence.
- The framework accepts observed hook-payload aliases, emits structured allow/ask/deny decisions, and preserves an exit-2 compatibility path. Security-hook exceptions fail closed; observability failures fail open.
- Premise-class live checks remain open for bypass-mode deny/ask behavior, subagent hook execution, dual-layer behavior, and per-harness presentation. The consolidated manual QA plan owns those checks after remediation.
- Design references (requirements only, not code): `docs/inspiration/claudekit.md` (file-guard concept, bash parsing), `docs/inspiration/claude-workflow-v2.md` (protect-files/security-check), `docs/inspiration/claude-code-hooks-mastery.md` (.env block), `docs/inspiration/buildwithclaude.md`.

## Dependencies & Risks

- **Dependency**: none upstream — this is the foundation phase. Downstream phases 2–4 depend on the framework delivered here.
- **Risk**: bash-command parsing is inherently incomplete (shell grammar is undecidable in general). *Mitigation*: layered approach — exact-match fast paths, conservative pattern rules, and a default-deny option for commands that reference protected paths in any token; document known-undetectable classes explicitly; one fixture per covered evasion vector so the covered/uncovered boundary is testable, not aspirational.
- **Risk**: false positives blocking legitimate work (e.g., editing `uv.lock` intentionally, `echo $PATH`). *Mitigation*: tiered `ask` for ambiguous rules; per-rule reasons + human-only project override file; tune rules during a soak period on this repo before propagating.
- **Risk**: fail-closed guard bricking sessions if the hook itself has a bug. *Mitigation*: documented human-only kill switch; framework-level exception tests; guard logic kept thin over the tested framework.
- **Release blocker**: propagation currently follows a symlinked intermediate destination directory and can write outside the declared consumer root. *Required mitigation*: canonical containment immediately before every write/removal, rejection of symlink ancestors, and adversarial regressions across runtime and generated-output subtrees.
- **Risk**: per-project propagation drift — projects on stale rule sets after a rule fix. *Mitigation*: propagated artifacts carry a version marker; re-propagation is one command; the generated-global layer covers your own machine regardless.
- **Release blocker**: propagated invocation latency does not yet demonstrate stable margin below the fixed 50-ms median requirement. *Required mitigation*: profile the subprocess path, reduce overhead or establish a representative repeatable benchmark, and rerun the full and focused gates repeatedly without raising the threshold.
- **Risk**: consolidation regressions when retiring `bash-safety.sh`/`protect-files.py`. *Mitigation*: port their existing rules into the new config first, with regression fixtures reproducing their current blocks (including the env-dump and exfil rules), before removing legacy wiring.
- **Risk**: propagation wiring differs per harness (Claude settings.json vs Codex hooks.json vs OpenCode plugins). *Mitigation*: preserve the implemented support classifications—Claude Full, Codex/OpenCode Partial, Cursor/Copilot Not supported—and do not infer equivalent enforcement from artifact emission.

## Success Criteria

- [x] Automated payload tests deny Read/Edit/Write/MultiEdit/NotebookEdit access to `.env` while allowing `.env.sample` and `.env.example`.
- [x] Automated tests deny Grep calls targeting protected files without affecting ordinary source searches.
- [x] Tool-path normalization fixtures cover symlinks, `~`, `../`, and case variants for protected targets.
- [x] Supported Bash-access/evasion vectors have fixtures, while unsupported dynamic expansion, interpreter-mediated access, and recursive parent scans are explicit in `docs/hooks/bash-command-limitations.md`.
- [ ] Live bypass-permissions behavior for `deny` and `ask` is verified and documented. **Manual QA pending.**
- [x] Destructive non-temp commands and ambiguous env exposure use `ask`; configured scratch/temp operations remain allowed.
- [x] `id_generator.py` is readable while exact private-key names and paths under `.ssh/` are denied.
- [ ] A live consuming-project session verifies self-protection for propagated runtime, config, wiring, and override files. **Automated coverage passes; manual QA pending.**
- [ ] Human recovery verifies that an induced guard error denies and the protected override-file kill switch restores operation. **Automated behavior passes; manual workflow pending.**
- [ ] PreToolUse guard behavior is verified for subagent tool calls. **Manual QA pending.**
- [ ] Live deny/audit output confirms no tool-input bodies or file contents leak. **Automated redaction tests pass; manual QA pending.**
- [ ] A fresh-clone installation run verifies the documented Claude Code path. The five-harness guide and support classifications are complete; **manual QA pending**.
- [x] Security and command rules are config-driven with a reason and action; Python contains engine behavior rather than duplicated policy lists.
- [x] The 16 legacy bash-safety strings and 11 protect-files regex behaviors are reproduced or deliberately re-tiered, and legacy wiring/scripts are retired.
- [ ] Project propagation and generated-global wiring are release-safe. Functional emission passes, but **SEC-01 destination containment blocks this criterion**.
- [ ] Dual project/global behavior produces a clear outcome in a live session. **Manual QA pending; duplicate redacted audit rows are an accepted documented possibility.**
- [ ] All required tests and performance gates pass reliably. Functional and coverage suites pass, but **PERF-01 unstable propagated latency blocks this criterion**.

## QA Considerations

- No frontend/UI changes; no manual QA docs required for UI.
- `docs/phases/PHASE_01/PHASE_01_QA.md` contains the live bypass, subagent, presentation, generated-global, double-fire, recovery, rollback, and limitation checks. Execute them only after the two Feature 04 blockers close.
- Integration behavior changed intentionally: legacy Bash hooks are consolidated, ambiguous env-var rules move from hard-deny to `ask`, and decisions provide structured rule/recovery guidance.
- Automated evidence includes the hook pytest suite, propagation tests, standard-library compatibility, compilation, JSON parsing, shell syntax, coverage, and patch hygiene. Final QA found 251 passing tests and one latency failure in the full suite; later focused passes did not establish stable release evidence.
- Security residuals and harness limitations must remain explicit: bounded Bash analysis is not a shell sandbox, Codex/OpenCode are Partial, Cursor/Copilot are Not supported, and live Claude premise checks remain open.

## Notes for Feature - Decomposer

The following four ordered feature boundaries were implemented:

1. **Hook framework + payload fixtures** — the shared lib: config layering + caching, allow/ask/deny decision output, per-hook failure posture (fail-closed contract + override-file kill switch), redacted logging, pytest harness with payload fixtures for every tool in the matcher (including Grep and NotebookEdit), and spike tests confirming the premise-class behaviors: deny-in-bypass-mode, ask-in-bypass-mode (documented), and hooks firing for subagent tool calls. Everything else depends on this; keep it free of any rule content.
2. **File-access guard (path-based)** — the rule engine + secrets/protected-file rules for Read/Edit/Write/MultiEdit/NotebookEdit/Grep, path normalization before matching (realpath/symlink resolution, `~`, `../`, case), per-rule `action` tiering with `escalate_in_bypass` support, structured messages, self-protection rules (scripts, config, wiring files, override file), human-only project-override mechanism. Depends on 1.
3. **Bash-command analyzer** — command parsing, indirect-access vectors (including `grep`/`rg` on protected files and `ln -s` symlink creation), env-dump/exfiltration rules (re-tiered), destructive-command rules at `ask`, absorbing `bash-safety.sh` and `protect-files.py` bash logic. Depends on 2 (reuses the rule engine); largest and riskiest feature — give it the deepest test plan (one fixture per evasion vector, plus a documented-limitations list covering the known-undetectable classes like recursive directory scans).
4. **Propagation extension + consolidation + install guide** — extend the *existing* hooks stage of `propagate_master_assets.py` for per-project script/config emission with version marker; generated-global setup step (absolute paths, gitignored); legacy regression fixtures; retire `bash-safety.sh`/`protect-files.sh`/`protect-files.py` from wiring; the user-facing multi-harness installation guide (Claude Code, OpenCode, Codex, Cursor, GitHub Copilot — verify current Cursor/Copilot hook support during implementation and state support status honestly). Depends on 1–3. Smaller than originally planned — the propagation stage already exists and is tested.

Careful separation: rule *content* (config files) vs rule *engine* (Python) — features 2 and 3 should both extend config, not fork engine logic. Integration point to watch: the guard and analyzer share the protected-path rule set and the tier semantics; define both once.

Clean-room reminder for all implementers: `docs/inspiration/` files describe *what* to cover and *what weaknesses to beat* — never open the inspiration repos' source files to copy code or patterns.
