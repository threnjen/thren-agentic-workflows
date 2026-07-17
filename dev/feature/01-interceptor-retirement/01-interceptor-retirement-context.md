# Feature Context: Interceptor Retirement

## Feature Boundary

This feature removes two independent interception integrations as one retirement unit: the repository file-access guard and automatic Bash rewriting through `rtk-rewrite.sh`. It preserves the external RTK executable, explicit RTK-prefixed command guidance, the shared hook framework, the prompt-injection scanner, audit logging, and completion notifications.

The current Phase 04 document is authoritative. It supersedes the earlier refinement note in `.github/learnings/cross-phase-decisions.md` that recommended fixing rather than retiring the guard; the same learnings file remains valuable for the verified dependency cut and mixed-test inventory.

## Key Files and Modules

### Retired Source Unit

| Path | Role | Planned Disposition |
|---|---|---|
| `.github/hooks/file-access-guard.json` | Source hook descriptor and event mapping | Remove |
| `.github/hooks/scripts/file-access-guard.py` | Guard entrypoint and payload decision orchestration | Remove |
| `.github/hooks/lib/file_access.py` | Path policy, normalization, and overlap evaluation | Remove |
| `.github/hooks/lib/bash_analyzer.py` | Bash command parsing and rule evaluation | Remove |
| `.github/hooks/lib/url_exfiltration.py` | Guard-only URL-exfiltration analysis | Remove |
| `.github/hooks/config/file-access-rules.json` | File, Bash, and URL guard policy | Remove |
| `.github/hooks/config/file-access-overrides.json` | Guard kill-switch and override layer | Remove |
| `.github/hooks/scripts/rtk-rewrite.sh` | Automatic Bash rewrite integration | Remove |

### Surviving Hook Boundary

| Path | Role | Required Outcome |
|---|---|---|
| `.github/hooks/lib/framework.py` | Shared hook payload, decision, configuration, and audit support | Preserve; independent regressions remain green |
| `.github/hooks/lib/injection_scanner.py` | Prompt-injection detection engine | Preserve |
| `.github/hooks/scripts/injection-scanner.py` | Scanner entrypoint | Preserve |
| `.github/hooks/injection-scanner.json` | Scanner hook descriptor | Preserve |
| `.github/hooks/audit-log.json` | Independent audit hook descriptor | Preserve |
| `.github/hooks/done-notify.json` | Independent notification hook descriptor | Preserve |
| `.github/hooks/config/injection-allowlist.json` | Scanner allowlist | Preserve |
| `.github/hooks/config/injection-patterns.json` | Scanner policy | Preserve |

### Propagation and Generated Wiring

| Path | Role | Planned Work |
|---|---|---|
| `scripts/propagate_master_assets.py` | Discovers source hooks, emits harness wiring, removes retired assets | Extend the verified `RETIRED_HOOK_ASSETS` mechanism with the retired guard and rewrite assets; keep removal explicit and ownership-safe |
| `.claude/settings.json` | Generated Claude project hook wiring | Remove the `$source: file-access-guard` `PreToolUse` entry; preserve unrelated project hooks |
| `.codex/hooks.json` | Generated Codex project hook wiring | Remove the `$source: file-access-guard` `PreToolUse` entry; preserve unrelated project hooks |
| `.opencode/plugins/file-access-guard.js` | Generated OpenCode guard plugin | Remove through generated-plugin reconciliation |
| `~/.claude/settings.json` | User-global automatic rewrite registration outside repository control | Inventory and remove only the repository-owned `rtk-rewrite.sh` registration; Feature 6 re-verifies final runtime state |

The active machine currently has RTK 0.42.4 at `/opt/homebrew/bin/rtk`, and `~/.claude/settings.json` currently contains an absolute command path to this repository's `.github/hooks/scripts/rtk-rewrite.sh`. Do not hard-code that machine-specific path into implementation or tests.

### Tests

| Path | Role | Planned Work |
|---|---|---|
| `tests/hooks/test_file_access_guard.py` | Guard-only behavior suite | Remove |
| `tests/hooks/test_bash_command_analyzer.py` | Guard-only Bash analysis suite | Remove |
| `tests/hooks/test_rtk_rewrite_hook.py` | Automatic rewrite behavior suite | Remove |
| `tests/hooks/test_hook_distribution_integration.py` | Mixed guard, scanner, distribution, and operations coverage | Remove guard-only cases; retain or replace independent scanner/distribution assertions |
| `tests/hooks/test_injection_scanner.py` | Scanner coverage with one guard self-protection coupling | Remove only the guard-policy coupling; retain scanner behavior coverage |
| `tests/test_propagate_master_assets.py` | Propagation coverage whose `_seed_hooks` helper uses the guard as a fixture vehicle | Replace guard scaffolding with the smallest surviving hook fixture and preserve propagation properties |
| `tests/hooks/test_hook_framework.py` | Independent shared-framework regressions | Run unchanged unless discovery proves a stale guard-only assertion |
| `tests/hooks/test_injection_corpus.py` | Independent scanner corpus coverage | Run unchanged |
| `tests/hooks/fixtures/file_access/` | Guard-only recorded payloads `(verify)` | Remove if no surviving test consumes them |
| `tests/hooks/fixtures/bash/` | Guard-only Bash fixtures `(verify)` | Remove if no surviving test consumes them |
| `tests/hooks/fixtures/url_exfiltration/` | Guard-only URL fixtures `(verify)` | Remove if no surviving test consumes them |
| `tests/hooks/fixtures/recorded_payloads.json` | Hook distribution fixture `(verify)` | Retain only if surviving mixed tests still consume it; remove retired guard expectations |

### Documentation

| Path | Planned Work |
|---|---|
| `docs/hooks/file-access-guard.md` | Retire or replace active operational claims with an explicit reduced-posture record |
| `docs/hooks/installation.md` | Remove guard install, double-invocation, override, and recovery procedures; preserve surviving hook setup |
| `docs/hooks/bash-command-limitations.md` `(verify)` | Remove or clearly retire guard-specific Bash analysis claims |
| `docs/hooks/hook-verification.md` `(verify)` | Remove guard result rows without weakening surviving-hook evidence |
| `docs/hooks/manual-qa.md` `(verify)` | Remove guard-only live procedures and stale pass counts; retain scanner/framework QA where still valid |
| `docs/hooks/prompt-injection-defense.md` `(verify)` | Correct language that relies on the guard for self-protection, performance margin, or recovery |
| Repository RTK instruction surfaces `(verify)` | Preserve explicit RTK-prefixed command guidance and remove only automatic-rewrite claims |

Phase 01, Phase 02, and Phase 07 status lines are not edited by this feature. Structural roadmap and security-narrative reconciliation remains assigned to `project-planner`.

## Architectural Decisions

1. **Delete the full retirement unit instead of adding feature flags or compatibility shims.** The guard code has a verified narrow dependency cut, and leaving its parser or policy behind would create dead security code with ambiguous ownership.
2. **Treat `url_exfiltration.py` as guard-only.** Code and learnings confirm that the injection scanner does not consume it; retaining it would orphan a substantial module.
3. **Use source discovery for generated hook removal.** Removing the source descriptor causes normal Claude, Codex, and OpenCode regeneration to drop its registrations. `RETIRED_HOOK_ASSETS` covers runtime assets that source discovery alone cannot clean from copied hook trees.
4. **Keep retirement cleanup explicit.** Do not introduce broad filename matching. A generated artifact is removable only through a known retired path, generated marker, `$source` ownership, or equivalent verified ownership evidence.
5. **Replace test scaffolding rather than deleting unrelated coverage.** Mixed tests must continue to assert propagation, scanner, redaction, and framework behavior using surviving assets.
6. **Prove behavioral absence.** Tests and QA must show ordinary file and Bash activity no longer produces a file-access decision; a filename inventory alone does not satisfy retirement.
7. **Separate RTK availability from automatic rewriting.** The executable and explicit invocation remain supported; only the hook script and owned registrations are retired.
8. **Add no new normal-path logging.** Existing propagation result counters are sufficient. Retirement evidence comes from counters, generated-roster inspection, focused tests, and Feature 6 runtime verification.

## Correctness and Safety Constraints

- Do not remove `.github/hooks/lib/framework.py`, injection-scanner source/configuration, audit-log wiring, or notification wiring.
- Do not remove explicit `rtk` prefixes from repository instructions merely because automatic rewriting is retired.
- Do not read, print, or persist secret-file contents while proving that the interceptor is absent.
- Do not blindly rewrite user-global settings. Preserve unrelated entries and remove only the command registration proven to point at this repository's retired rewrite script.
- A same-named regular file without repository ownership evidence must not be deleted by retirement cleanup.
- Generated cleanup must be idempotent: a second pass records no repeated retirement and no unrelated wiring change.
- Restart any long-running propagation watcher before trusting regenerated evidence after modifying the propagator.
- Documentation searches must distinguish active operational guidance from legitimate historical discussion and symlink/security threat analysis.
- Repository-wide retirement sweeps must be rerun after files are staged because `git ls-files`-based checks cannot see untracked files.

## Relationships to Sibling Features

- **`02-propagation-convergence`:** follows this feature because both modify `scripts/propagate_master_assets.py` and `tests/test_propagate_master_assets.py`. Feature 2 must begin from the surviving hook roster produced here.
- **`05-deployment-guidance`:** owns the broad managed-copy and Evangelize documentation rewrite. This feature owns only interceptor-retirement and reduced-security claims; avoid duplicating deployment guidance work.
- **`06-runtime-verification`:** rechecks the final surviving hook roster, explicit RTK behavior, user-global automatic-rewrite absence, and cross-feature runtime state.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6, Bash, JSON hook manifests, generated JavaScript OpenCode plugins |
| Test Runner | `python3 -m pytest -q tests/hooks tests/test_propagate_master_assets.py` after installing `requirements-dev.txt` |
| Focused Verification | `python3 -m pytest -q tests/hooks/test_hook_framework.py tests/hooks/test_injection_scanner.py tests/hooks/test_injection_corpus.py tests/hooks/test_hook_distribution_integration.py tests/test_propagate_master_assets.py` |
| Test Baseline | Runner constrained on 2026-07-16: `/Users/jennywadkins/.pyenv/versions/3.12.6/bin/python3` has no `pytest` module; no passing count claimed |
| Development Requirements | `pytest>=9.0,<10`, `pytest-cov>=7.0,<8` from `requirements-dev.txt` |
| Pytest Configuration | `testpaths = ["tests"]`, `addopts = "-ra"` in `pyproject.toml` |
| Lint | Not configured in repository metadata inspected for this feature |
| Format | Not configured in repository metadata inspected for this feature |
| RTK Runtime | RTK 0.42.4 is installed at `/opt/homebrew/bin/rtk`; its integrity wrapper currently refuses commands because the user-global rewrite hook hash differs from RTK's expected hash |

The implementer must either provision the declared development requirements or explicitly record runner-constrained evidence. Static review, compile checks, and manual QA are not substitutes for a test pass.

## Relevant Learnings

- `.github/learnings/cross-phase-decisions.md`, **Hook Composition**: a command-mutating PreToolUse hook can invalidate another hook's authorization analysis; the global rewrite registration is an absolute repository path and depends on an unpinned RTK binary from `PATH`. Retirement removes this composition hazard rather than attempting to order it.
- `.github/learnings/cross-phase-decisions.md`, **File-Access Guard Retirement**: the verified dependency cut includes `url_exfiltration.py`; `tests/hooks/test_injection_scanner.py`, `tests/hooks/test_hook_distribution_integration.py`, and `tests/test_propagate_master_assets.py` require surgery rather than blanket deletion.
- `.github/learnings/cross-phase-decisions.md`, **Propagation Contracts**: generated roots are marker-governed, stale watchers can suppress pruning, and one propagation run is not evidence of convergence. Run until counters are zero and let Feature 2 formalize the bounded fixed-point gate.
- `.github/learnings/project-learnings.md`, **Hook commands with relative script paths**: generated hook commands must not assume repository-root working directory. Retirement must preserve the anchored commands used by surviving hooks.
- `.github/learnings/review-learnings.md`, **Artifact propagator containment**: validate resolved source assets and destination parents before reading or writing; a symlinked parent can redirect cleanup outside the intended root.
- `.github/learnings/review-learnings.md`, **Tracked-file sweep visibility**: rerun retirement regression searches after staging so newly added files cannot evade a `git ls-files`-based sweep.

## Unverified Assumptions

- Other developer machines may register automatic RTK rewriting in a different user-global file or command shape. Repository implementation must use narrow ownership evidence; Feature 6 inventories the active machine instead of generalizing this machine's exact path.
- The three guard fixture directories appear guard-only but must be checked against the post-surgery test import graph before deletion.
- The additional hook documents marked `(verify)` contain active guard claims today; the implementer must decide whether each is removed, rewritten, or retained as explicitly historical content.
