# Phase 1: Hook Foundation + File-Access Guard

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/inspiration/README.md`

## What's New

After this phase, every project that consumes this repo's assets gets a safety layer that cannot be bypassed: agents can no longer read, grep, or edit `.env` files and other secret-bearing files, cannot touch explicitly protected files (lock files, production configs, the hook system itself), and cannot sneak around those rules through shell commands — even when the session runs with bypass permissions. Destructive-but-sometimes-legitimate commands (recursive deletes, force pushes) pause for your confirmation instead of hard-failing. When something is blocked, the agent is told exactly why and what to do instead, so work continues smoothly rather than failing mysteriously.

Protection travels with each project: anyone who clones a consuming repo gets working hooks with no setup, and a friend who adopts this source-of-truth repo can protect their own projects with one propagation command. On your own machine, an optional setup step extends the same protection to every repo, even ones you haven't propagated to yet. This phase also builds the shared plumbing (config, testing, propagation) that every later hook phase reuses.

## Objective

Establish the Python-stdlib hook framework under `.github/hooks/` (with propagation to platform outputs) and ship its first consumer: a tiered-enforcement PreToolUse guard covering secrets, protected files, indirect access via bash, and destructive commands — closing the highest-stakes safety gap (goals 2 and 5).

## Deployment Model (decided during refinement)

Hybrid, with per-project as the tested contract:

- **Per-project propagation (primary, committed, shareable)**: `propagate_master_assets.py` emits hook scripts, rule config, and settings wiring into consuming projects using machine-agnostic relative paths. Protection is versioned with the project and travels with any clone — zero setup for someone cloning a consuming repo.
- **Generated user-global wiring (secondary, local-only)**: a setup script generates user-scope hook wiring with absolute paths into this repo, covering every project on the local machine including unpropagated ones. Generated output is machine-specific and never committed (gitignored). Documented, but not a first-class test target.
- **Double-fire tolerance**: when both layers are active the guard runs twice per tool call; it must be functionally idempotent and should suppress duplicate deny messaging where practical.

The existing `setup-hook-symlinks.sh` user-global symlink flow is superseded by the generated-global step (today its relative `bash .github/hooks/...` commands only resolve when the cwd is this repo, so it silently provides no protection elsewhere — this phase fixes that).

## Enforcement Posture (decided during refinement)

Tiered, declared per-rule in config (never hardcoded in the engine):

- **`deny` (hard block, holds in bypass-permissions mode)**: secrets and protected-file access (read/grep/edit/write and bash-mediated equivalents); high-confidence exfiltration commands (`curl -d @<file>`, `wget --post-file`, `base64` of a protected file); tampering with the hook system's own files.
- **`ask` (pause for user confirmation)**: destructive-but-sometimes-legitimate commands (`rm -rf`, `git push --force`, `git reset --hard`, etc. — preserving current `bash-safety.sh` ergonomics); ambiguous env-var exposure (`echo $SOME_VAR`, bare `env`/`set`/`export`), which the current guard hard-denies and which false-positives on innocent commands like `echo $PATH`.

Note: `ask` may not prompt in bypass-permissions mode; only `deny` is guaranteed to hold there. This split is deliberate — secrets get the guarantee, workflow-ergonomic rules get the prompt.

## Scope

### In Scope

- **Hook framework** (`.github/hooks/lib/` or equivalent): stdin JSON payload parsing, decision JSON emission (allow/ask/deny with reason), layered config loading (repo defaults → project overrides) with an mtime-checked cache to meet the latency budget (suggested implementation shape, to be verified by Feature Decomposer), structured logging, per-hook failure posture (see below), and pytest fixtures of real hook payloads for every supported event and tool.
- **Failure posture contract**: the guard fails **closed** — an unhandled error in the hook denies with a "guard error" reason rather than silently allowing (today `protect-files.py` fails open on any exception). Balanced by a documented, human-only kill switch (env var or override-file flag) so a buggy rule cannot brick sessions. The framework makes posture per-hook: security hooks fail closed; observability hooks (audit-log) fail open.
- **File-access guard hook** (PreToolUse, matcher `Read|Edit|Write|MultiEdit|Grep|Bash`):
  - Secrets rules: block `.env` and variants (`.env.local`, `.env.production`, …) while allowing templates (`.env.sample`, `.env.example`); credential files (`*.pem`, `*.key`, `credentials*`, tokens); SSH keys matched by exact name (`id_rsa`, `id_ed25519`, …) or by location (under `.ssh/`) — never by bare `id_*` prefix (the current rule blocks unrelated files like `id_generator.py`); cloud config locations (`.aws/`, `.kube/`, `.gnupg/`).
  - Protected-file rules: glob-based config with a per-rule `reason` and per-rule `action` (`deny`/`ask`) field (lock files, production configs, user-specified paths).
  - **Grep coverage**: Grep tool calls whose path/glob targets a protected file are denied — grep returns file contents and currently bypasses the guard entirely. Glob (filename listing only) stays unguarded.
  - **Self-protection**: in consuming projects, the propagated hook scripts and rule config are themselves protected paths (deny Edit/Write), and the project override file is agent-protected — overrides are a human-only escape hatch. Without this, per-project deployment would let the agent disarm its own guard.
  - Bash-command analysis: parse Bash tool input to catch indirect access — `cat`/`less`/`head` on protected files, redirections, `cp`/`mv`, heredocs, `xargs`, subshells/command substitution, base64/`xxd` pipes, and symlink traversal into protected paths.
  - Env-var and exfiltration rules (carried forward from the existing `protect-files.py`, now explicit and tiered): `printenv` and env-dump commands, `echo $VAR` exposure, `curl`/`wget` file-posting — mapped to `deny` or `ask` per the enforcement posture above.
  - Structured messages: why it was blocked or held, which rule fired, and a suggested alternative (e.g., "read `.env.sample` instead").
- **Dangerous-command rules**: recursive-delete and similar destructive patterns, absorbing the current `bash-safety.sh` responsibilities at `ask` tier; scratchpad/temp-dir destructive operations remain allowed.
- **Consolidation**: fold existing `bash-safety.sh` and `protect-files.sh`/`protect-files.py` behavior into the new guard; retire the legacy scripts from settings wiring after regression fixtures reproduce every current block.
- **Propagation extension**: the hooks stage of `propagate_master_assets.py` **already exists** (emits `.claude/settings.json` wiring, `.codex/hooks.json`, and OpenCode plugins from `.github/hooks/*.json`, with `$source` tags, event mapping, and tests). This phase extends it: emit the new guard's scripts + rule config into consuming projects (per-project model), add the generated-global setup step with gitignore handling, and remove legacy-hook emission.

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
| 4 | Propagation + consolidation | Extend the existing hooks propagation stage for per-project script/config emission; generated-global setup step; legacy hooks retired after regression fixtures | propagation extension; migration/cleanup |

## Technical Context

- Existing hook definitions: `.github/hooks/{bash-safety,protect-files,audit-log,done-notify}.json` with scripts in `.github/hooks/scripts/`; wired into `.claude/settings.json` with `$source` tags. **`protect-files.sh` is already a thin wrapper over `protect-files.py`** (stdlib Python, ~120 lines: file patterns, path substrings, 11 bash regexes including env-dump and curl/wget exfil rules). This phase upgrades and externalizes that logic to config; it is not a bash→Python port.
- **Propagation already handles hooks**: `scripts/propagate_master_assets.py` contains a working hooks stage (`HOOK_EVENT_MAP`, `$source` stripping/regeneration, Codex + OpenCode emission) with coverage in `tests/test_propagate_master_assets.py`. Deliverable 4 extends this stage; do not rebuild it.
- Current gap: `setup-hook-symlinks.sh` symlinks `~/.claude/settings.json` to this repo's settings file, but hook commands use relative paths — user-global protection currently only functions when the cwd is this repo.
- Repo conventions: Python tooling exists (`python/` template set, pytest patterns in `tests/`); hooks must be runnable via `python3` with no venv/pip step.
- Hook payload/decision contract: PreToolUse hooks receive JSON on stdin (tool name + tool_input) and can respond via exit code 2 (stderr shown to Claude) or structured JSON output with a permission decision (`allow`/`ask`/`deny`) + reason. The framework should support both, preferring structured JSON.
- Critical behavior to verify early: PreToolUse `deny` fires and blocks in bypass-permissions mode — this is the premise of the phase (spike/test this first). Also verify what `ask` does in bypass mode and document it.
- Design references (requirements only, not code): `docs/inspiration/claudekit.md` (file-guard concept, bash parsing), `docs/inspiration/claude-workflow-v2.md` (protect-files/security-check), `docs/inspiration/claude-code-hooks-mastery.md` (.env block), `docs/inspiration/buildwithclaude.md`.

## Dependencies & Risks

- **Dependency**: none upstream — this is the foundation phase. Downstream phases 2–4 depend on the framework delivered here.
- **Risk**: bash-command parsing is inherently incomplete (shell grammar is undecidable in general). *Mitigation*: layered approach — exact-match fast paths, conservative pattern rules, and a default-deny option for commands that reference protected paths in any token; document known-undetectable classes explicitly; one fixture per covered evasion vector so the covered/uncovered boundary is testable, not aspirational.
- **Risk**: false positives blocking legitimate work (e.g., editing `uv.lock` intentionally, `echo $PATH`). *Mitigation*: tiered `ask` for ambiguous rules; per-rule reasons + human-only project override file; tune rules during a soak period on this repo before propagating.
- **Risk**: fail-closed guard bricking sessions if the hook itself has a bug. *Mitigation*: documented human-only kill switch; framework-level exception tests; guard logic kept thin over the tested framework.
- **Risk**: per-project propagation drift — projects on stale rule sets after a rule fix. *Mitigation*: propagated artifacts carry a version marker; re-propagation is one command; the generated-global layer covers your own machine regardless.
- **Risk**: hook latency on every tool call. *Mitigation*: stdlib-only, no subprocess spawning in the hot path, mtime-cached config, budget <50ms per invocation, measured in tests.
- **Risk**: consolidation regressions when retiring `bash-safety.sh`/`protect-files.py`. *Mitigation*: port their existing rules into the new config first, with regression fixtures reproducing their current blocks (including the env-dump and exfil rules), before removing legacy wiring.
- **Risk**: propagation wiring differs per harness (Claude settings.json vs Codex hooks.json vs OpenCode plugins). *Mitigation*: the existing propagation stage already abstracts this; treat Claude as the primary target; Codex/OpenCode propagation is best-effort and clearly marked.

## Success Criteria

- [ ] A Read/Edit/Write/MultiEdit of `.env` in a consuming project is denied with a structured reason; `.env.sample` and `.env.example` are allowed.
- [ ] A Grep call targeting a protected file is denied; Grep over ordinary source files is unaffected.
- [ ] `cat .env`, `cp .env /tmp/x`, `base64 .env`, output redirection onto a protected file, command-substitution variants, quote-splitting (`cat '.e''nv'`), variable indirection (`F=.env; cat $F`), glob evasion (`cat .en?`), interpreter escapes (`python3 -c "open('.env')"`), `~`/`../` path forms, and uppercase variants (`cat .ENV`) are each covered by a fixture — denied where covered, listed in the documented-limitations section where not.
- [ ] Deny behavior is verified to hold in bypass-permissions mode (manual checklist documented, plus automated payload-level tests); `ask` behavior in bypass mode is verified and documented.
- [ ] A destructive command (e.g., recursive delete of a non-temp path, force push) triggers `ask`; the same command against the scratchpad/temp dirs is allowed; `echo $PATH` triggers `ask`, not `deny`.
- [ ] A file named `id_generator.py` is readable; `id_rsa` and any file under `.ssh/` are denied.
- [ ] In a consuming project, an agent Edit/Write against the propagated hook scripts, rule config, or the project override file is denied.
- [ ] An induced exception inside the guard results in a deny ("guard error"), not a silent allow; the documented kill switch restores normal operation.
- [ ] All rules live in config files with a `reason` and `action` per rule; no rule content is hardcoded in Python beyond the engine.
- [ ] Every existing block behavior of `bash-safety.sh` and `protect-files.py` (file patterns, path substrings, env-dump rules, exfil rules) is reproduced or explicitly re-tiered to `ask` (regression fixtures), and the legacy scripts are retired from settings wiring.
- [ ] `propagate_master_assets.py` emits the guard's scripts + config into a consuming project such that a fresh clone of that project has working hooks with no manual steps; the generated-global setup step produces absolute-path user-scope wiring that is gitignored.
- [ ] With both deployment layers active, a blocked call produces one clear deny outcome (no conflicting or confusing duplicate behavior).
- [ ] Hook unit tests pass via pytest with recorded payload fixtures; median hook latency <50ms in the benchmark test.

## QA Considerations

- No frontend/UI changes; no manual QA docs required for UI.
- Manual QA needed for the bypass-permissions verification (cannot be fully automated: requires a live Claude Code session in bypass mode attempting protected operations) — a short manual checklist should be produced, covering both `deny` and `ask` tiers.
- Manual QA needed for the hybrid double-fire scenario (global + per-project layers both active in one session).
- Integration behavior changes: existing bash hooks are replaced; ambiguous env-var rules move from hard-deny to `ask` (behavior change, intentional); stderr/deny messages change (better). Note in changelog.
- Test impact: new pytest suite under `tests/` for the hook framework and guard; `tests/test_propagate_master_assets.py` will need extension for the new propagation behavior; existing tests should otherwise be unaffected.

## Notes for Feature - Decomposer

Suggested feature boundaries (4 features, ordered):

1. **Hook framework + payload fixtures** — the shared lib: config layering + caching, allow/ask/deny decision output, per-hook failure posture (fail-closed contract + kill switch), logging, pytest harness with payload fixtures for every tool in the matcher (including Grep), and a spike test confirming deny-in-bypass-mode (and documenting ask-in-bypass-mode). Everything else depends on this; keep it free of any rule content.
2. **File-access guard (path-based)** — the rule engine + secrets/protected-file rules for Read/Edit/Write/MultiEdit/Grep, per-rule `action` tiering, structured messages, self-protection rules, human-only project-override mechanism. Depends on 1.
3. **Bash-command analyzer** — command parsing, indirect-access vectors, env-dump/exfiltration rules (re-tiered), destructive-command rules at `ask`, absorbing `bash-safety.sh` and `protect-files.py` bash logic. Depends on 2 (reuses the rule engine); largest and riskiest feature — give it the deepest test plan (one fixture per evasion vector, plus a documented-limitations list).
4. **Propagation extension + consolidation** — extend the *existing* hooks stage of `propagate_master_assets.py` for per-project script/config emission with version marker; generated-global setup step (absolute paths, gitignored); legacy regression fixtures; retire `bash-safety.sh`/`protect-files.sh`/`protect-files.py` from wiring; docs. Depends on 1–3. Smaller than originally planned — the propagation stage already exists and is tested.

Careful separation: rule *content* (config files) vs rule *engine* (Python) — features 2 and 3 should both extend config, not fork engine logic. Integration point to watch: the guard and analyzer share the protected-path rule set and the tier semantics; define both once.

Clean-room reminder for all implementers: `docs/inspiration/` files describe *what* to cover and *what weaknesses to beat* — never open the inspiration repos' source files to copy code or patterns.
