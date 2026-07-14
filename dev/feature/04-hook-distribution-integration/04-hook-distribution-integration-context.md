# Feature 04: Hook Distribution Integration Context

## Key Files

### Files Changed by This Feature

| File | Role | Change Type |
|------|------|-------------|
| `scripts/propagate_master_assets.py` | Existing hook propagation stage, settings regeneration, `$source` cleanup, event translation, and generated OpenCode plugin rendering | Modify |
| `tests/test_propagate_master_assets.py` | Existing `unittest` suite containing `PropagateMasterAssetsTests` and the repository's two current tests | Modify |
| `scripts/setup-hook-symlinks.sh` | Existing user-global symlink installer that must be superseded by absolute-path generated wiring | Modify or replace in place |
| `.gitignore` | Excludes machine-specific generated-global output and verification artifacts | Modify |
| `.github/hooks/bash-safety.json` | Legacy source hook definition retired only after Feature 03 parity evidence and Feature 04 integration gates pass | Delete after gate |
| `.github/hooks/protect-files.json` | Legacy source hook definition retired only after parity and integration gates pass | Delete after gate |
| `.github/hooks/scripts/bash-safety.sh` | Legacy destructive-command implementation | Delete after gate |
| `.github/hooks/scripts/protect-files.sh` | Legacy file-protection wrapper | Delete after gate |
| `.github/hooks/scripts/protect-files.py` | Legacy file and Bash protection implementation | Delete after gate |
| `.claude/settings.json` | Generated Claude wiring; preserve untagged entries and replace stale generated legacy entries | Regenerate through propagation |
| `.codex/hooks.json` | Generated Codex wiring; preserve untagged entries and replace stale generated legacy entries | Regenerate through propagation |
| `.opencode/plugins/bash-safety.js` | Stale generated legacy plugin | Delete through propagation |
| `.opencode/plugins/protect-files.js` | Stale generated legacy plugin | Delete through propagation |
| `.opencode/plugins/file-access-guard.js` `[PROPOSED - name TBD]` | Generated OpenCode adapter for the consolidated guard | Create through propagation |
| `tests/hooks/test_hook_distribution_integration.py` `[PROPOSED - name TBD]` | Fresh-project, double-invocation, smoke, redaction, and latency integration coverage | Create |
| `docs/hooks/installation.md` `[PROPOSED - name TBD]` | Five-harness installation and support-status guide | Create |
| `docs/hooks/manual-qa.md` `[PROPOSED - name TBD]` | Recorded clean-checkout, live-harness, recovery, and rollback evidence | Create |
| Generated-global output path `[PROPOSED - name TBD]` | Machine-local absolute-path wiring produced by setup and excluded from source control | Create locally; gitignored |

### Read-Only Inputs and References

| File or Area | Role | Change Type |
|--------------|------|-------------|
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Authoritative Phase 01 deployment, consolidation, support, and verification contract | Read-only reference |
| `dev/feature/01-hook-framework/01-hook-framework-plan.md` | Defines framework assets, runtime contract, fixtures, redaction, and live premise evidence consumed here | Read-only reference |
| `dev/feature/02-file-access-guard/02-file-access-guard-plan.md` | Defines the consolidated guard entrypoint, rule/default and override config, and self-protection contract consumed here | Read-only reference |
| `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-plan.md` | Defines analyzer assets, limitations, and the regression matrix that gates legacy retirement | Read-only reference |
| `.github/hooks/lib/` `[PROPOSED - name TBD]` | Feature 01 framework files included in the deployable guard unit | Read-only source assets |
| `.github/hooks/file-access-guard.json` `[PROPOSED - name TBD]` | Feature 02 source hook definition used to generate platform wiring | Read-only source asset |
| `.github/hooks/config/` `[PROPOSED - name TBD]` | Feature 02/03 defaults and protected project override contract included in propagation | Read-only source assets |
| `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]` | Completed Feature 02/03 guard entrypoint copied to consumers | Read-only source asset |
| `.github/hooks/lib/bash_analyzer.py` `[PROPOSED - name TBD]` | Feature 03 analyzer helper copied to consumers | Read-only source asset |
| `docs/hooks/bash-command-limitations.md` `[PROPOSED - name TBD]` | Feature 03 limitations source for installation and migration documentation | Read-only reference |
| `.github/hooks/audit-log.json`, `.github/hooks/done-notify.json` | Unrelated hook definitions whose generated wiring must remain coherent | Read-only reference |
| `.github/hooks/scripts/audit-log.py`, `.github/hooks/scripts/audit-log.sh` | Observability implementation used to verify redacted integration behavior | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| The Phase summary says the existing hook propagation stage has coverage in `tests/test_propagate_master_assets.py`, but the file currently tests only `_write_if_changed` symlink replacement and `propagate_skills_once`; no hook propagation test exists. | Hook-distribution behavior has no existing regression safety net, so the plan must not classify hook assertions as updates to established hook coverage. | Treat all hook propagation, output preservation, cleanup, and consuming-project tests as new must-have automated coverage; keep the two existing tests green. **Discovery Delta warning for Decomposer.** |
| `propagate_hooks_once` has no `repo_root` or output-path parameter and uses module-level `REPO_ROOT`, `CLAUDE_SETTINGS_FILE`, `CODEX_HOOKS_FILE`, and `OPENCODE_PLUGINS_DIR`. `propagate_skills_once` already has a `repo_root` seam. | The proposed temporary consuming-project fixture cannot safely exercise hook propagation without monkeypatching globals or first introducing a narrow testability/target-root seam. | Add a Stage 1 task to extend the existing function with the smallest compatible target-root/dependency seam; follow the `propagate_skills_once` pattern where appropriate. **Discovery Delta warning for Decomposer.** |
| Current propagation reads only `.github/hooks/*.json` and generates wiring/plugins; it does not copy referenced scripts, library modules, or configuration into a consuming project. | AC1 and AC2 require a dependency-copy manifest or equivalent discovery mechanism in addition to the current wiring generator. | Add an explicit dependency inventory/copy task and verify every generated command references an emitted file. |
| `_update_nested_settings_file` removes every generated entry containing `$source` and preserves entries without `$source`; stale generated OpenCode plugins are removed only when they carry `GENERATED_OPENCODE_PLUGIN_HEADER`. | The repository already has deterministic preservation and cleanup seams, but tests must assert exact tag/header behavior to avoid deleting user-owned entries. | Extend these helpers instead of replacing them; add tagged-versus-untagged and generated-header cleanup assertions. |
| Current `bash-safety.json` and `protect-files.json` override OpenCode's PreToolUse event to `pre_tool_call`, while the default `HOOK_EVENT_MAP` maps it to `tool.execute.before`. | Generated output behavior is metadata-driven; changing or removing legacy metadata may change the OpenCode event shape unexpectedly. | Use the consolidated guard definition selected by Feature 02 as authoritative and add an exact generated-event assertion before retiring legacy definitions. |
| `scripts/setup-hook-symlinks.sh` backs up real user files, then replaces Claude/Codex settings and OpenCode plugins with symlinks to repository files. The relative commands inside those files remain cwd-sensitive. | The existing backup behavior is safety-relevant, but symlink replacement is the broken deployment model this feature supersedes. | Preserve safe backup/merge semantics while generating absolute commands; test against a temporary HOME and never mutate the developer's real user configuration. |
| `.gitignore` has no entry for generated-global hook wiring. | Absolute local paths could be committed accidentally. | Select the final local output path during implementation, mark it `[PROPOSED - name TBD]` until then, add it to `.gitignore`, and test that committed project outputs contain no machine path. |
| `tests/hooks/`, `docs/hooks/`, the proposed distribution integration test, and the proposed installation/manual-QA documents do not exist yet. No phase-scoped consolidated hook test pattern exists. | These are genuine new artifacts, not existing framework conventions. | Keep all names marked `[PROPOSED - name TBD]` until implementation confirms the final idiomatic structure. No omitted consolidated phase test was found. |
| Upstream Features 01–03 intentionally leave their exact filenames/public symbols proposed, and none of those planned outputs exists on the current pre-implementation branch. | Feature 04 cannot hardcode the draft names safely before its dependencies finish. | Resolve and record the actual upstream implementation artifact set before changing propagation; do not modify upstream source files in this feature unless an integration defect is first recorded and sequenced. |
| `python3 -m pytest -q` currently fails because pytest is not installed; the existing stdlib suite passes two tests. | Stage 0 cannot claim pytest or coverage readiness yet. | Have `@z-test-writer` establish/document the pytest-capable test environment and coverage gate before Feature 04 implementation. |

## Architectural Decisions

- Extend `propagate_hooks_once`, `_update_nested_settings_file`, `_render_opencode_plugin`, `$source` tagging, and the existing event mapping. Do not create a second hook propagator.
- Treat the completed upstream entrypoint, framework, analyzer, default rules, and project override contract as one deployable unit. Generated wiring is invalid unless every referenced runtime asset is emitted.
- Use repository-relative commands for committed per-project deployment and generated absolute commands for user-global deployment.
- Preserve untagged user wiring. Remove only source-tagged settings entries and generated plugins that are demonstrably owned by propagation.
- Introduce the smallest target-root/testability seam needed for temporary consuming-project tests, consistent with `propagate_skills_once(repo_root=...)` where practical.
- Gate legacy source and generated-output deletion on Feature 03's complete parity matrix plus Feature 04's propagation and smoke tests.
- Keep machine-specific global output local and gitignored. It may contain absolute paths but no secrets.
- Keep duplicate invocations stateless and functionally idempotent. Suppress duplicate denial text only where it can be done without persisting raw or secret-bearing payload data.
- Add no normal-path propagation or guard telemetry. Setup may report changed artifact counts and verification failures; guard/audit evidence remains redacted.
- Verify Cursor and GitHub Copilot capabilities from current primary documentation during implementation. Documentation classification is allowed to be fully supported, partial, or unsupported; no extension or plugin work is implied.

## Constraints

- Feature 04 executes after and depends on `01-hook-framework`, `02-file-access-guard`, and `03-bash-command-analyzer`.
- Python hook runtime code remains standard-library-only and must run through `python3` without pip or a virtual environment in a consuming clone.
- Per-project propagation is the primary tested contract. Generated user-global wiring is secondary and local-only.
- Claude Code is the primary enforcement target. Codex and OpenCode output must remain coherent but may have weaker verified semantics that documentation must state honestly.
- Propagation emission remains limited to Claude Code, Codex, and OpenCode. Cursor and GitHub Copilot are research/documentation targets only.
- Do not test Windows. Keep scripts POSIX-compatible where practical without claiming Windows support.
- Do not introduce new guard policies or parser scope except narrow integration corrections required for upstream accepted behavior to work together.
- Do not copy implementation code or patterns from `docs/inspiration/` repositories.
- Legacy files remain active until automated parity and integration evidence is green.
- The override kill switch is human-only and must be operated outside the guarded agent session; do not add an environment-variable bypass.
- The combined median hook latency remains below 50 ms.

## Scope Boundaries

- Do not modify upstream framework, path-evaluation, analyzer, or rule-engine design as part of distribution work unless a concrete integration defect is documented first.
- Do not guard the Glob tool or add WebFetch exfiltration scanning, prompt-injection scanning, edit-time backups, or plugin packaging.
- Do not hand-edit generated `.claude`, `.codex`, or `.opencode` outputs as the source of truth; regenerate them from `.github/hooks/`.
- Do not overwrite or discard untagged user settings or user-owned OpenCode plugins.
- Do not commit generated-global absolute paths, temporary HOME content, clean-checkout evidence containing machine paths, or secret-bearing payloads.
- Do not retire `audit-log` or `done-notify`; only legacy `bash-safety` and `protect-files` artifacts are consolidation targets.

## Relationships to Sibling Plans

- `01-hook-framework` supplies the payload, decision, configuration, failure-posture, redaction, and runtime assets propagated and smoke-tested here.
- `02-file-access-guard` supplies the consolidated hook definition, entrypoint, data-driven path rules, protected override contract, and self-protection behavior.
- `03-bash-command-analyzer` extends the same entrypoint/configuration and supplies the legacy parity matrix and limitations documentation that gate deletion.
- Feature 04 owns all generated platform outputs, consuming-project integration, user-global setup, legacy retirement, installation guidance, and cross-feature smoke evidence.

## Suggested Implementation Order

1. Finish and verify Features 01–03; resolve their final artifact names and public contracts.
2. Establish Feature 04's new propagation/integration tests and a safe temporary target-root/HOME harness.
3. Extend per-project asset copying and generated wiring; prove fresh-project, preservation, cleanup, and idempotence behavior.
4. Implement generated-global absolute-path setup and gitignore protection in the temporary HOME harness.
5. Run the Feature 03 parity gate, then retire legacy source definitions/scripts and regenerate all platform outputs atomically.
6. Run cross-feature, double-fire, redaction, self-protection, and latency verification.
7. Research harness support, publish the installation/operations guide, and record the clean-checkout and rollback walkthroughs.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 stdlib + Bash; JSON hook metadata/settings and generated JavaScript OpenCode adapters |
| Test Runner | `python3 -m unittest discover -s tests -v` |
| Test Baseline | 2 passed, 0 failed in 0.008s — captured 2026-07-14 |
| Pytest Readiness | `python3 -m pytest -q` fails: `No module named pytest` |
| Coverage | Not configured; below the plan's required 50% gate until Stage 0 establishes measurement |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- From `.github/learnings/cross-phase-decisions.md`: pre-edit backup hooks, WebFetch exfiltration guarding, and plugin packaging were explicitly deferred. Keep them out of this feature even if they appear adjacent to setup or security work.
- From `.github/learnings/debugging-learnings.md`: stale or mismatched user-level symlinks can fail silently. The generated-global replacement should have explicit verification output and should not retain a filename/target mismatch after regeneration.
- From `.github/learnings/review-learnings.md`: shell preflight examples for future-facing paths must not use silent bare `test -e` checks. Installation-guide verification commands should explain expected missing paths or emit a useful failure message.
