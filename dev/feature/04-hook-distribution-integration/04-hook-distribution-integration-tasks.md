# Feature 04: Hook Distribution Integration Tasks

## Stage 0: Test Prerequisites

- [ ] Invoke `@z-test-writer` to establish and document a pytest-capable developer test environment and coverage measurement for Feature 04 without adding any runtime dependency to propagated hooks.
- [ ] Run Features 01–03 automated suites and confirm the completed Feature 03 legacy parity matrix is green before any legacy source or generated output is removed.
- [ ] Run `python3 -m unittest discover -s tests -v` and preserve the two existing `PropagateMasterAssetsTests` cases unchanged or equivalently covered.
- [ ] Resolve the actual files and public contracts delivered by Features 01–03, replacing draft `[PROPOSED - name TBD]` assumptions only in implementation records and new Feature 04 artifacts, not by silently editing upstream plans.
- [ ] Create propagation integration scaffolding `[PROPOSED - name TBD]` with isolated source/consumer repositories, temporary HOME/user-config directories, tagged and untagged settings, stale generated plugins, complete guard assets, and representative upstream payload fixtures.
- [ ] Add baseline tests proving the current hook propagator's `$source` stripping, untagged-entry preservation, generated-header plugin ownership, and current metadata-driven event mapping before changing those behaviors.
- [ ] Reach at least 50% coverage for Feature 04 scope and keep all prerequisite tests green before Stage 1 begins.

## Stage 1: Per-Project Propagation

- [ ] Add the smallest compatible target-root/output-path seam to `propagate_hooks_once` so tests can propagate into a temporary consuming project without mutating module-global repository outputs; follow the existing `propagate_skills_once(repo_root=...)` pattern where appropriate.
- [ ] Define how the consolidated guard hook declares or resolves its deployable dependency set—entrypoint, Feature 01 framework, Feature 03 analyzer, defaults, and protected project override contract—without creating a parallel propagator.
- [ ] Extend the existing hooks stage to copy the complete guard dependency unit into a consuming project and fail verification if generated wiring references an asset that was not emitted. (AC1)
- [ ] Select and implement the narrowest version-marker format `[PROPOSED - name TBD]`, update it when source guard assets change, and verify repeat propagation is idempotent when inputs do not change. (AC1)
- [ ] Generate repository-relative Claude Code, Codex, and OpenCode commands from the consolidated source hook definition while preserving existing event translation and source metadata overrides. (AC1, AC5)
- [ ] Preserve all untagged Claude/Codex entries and user-owned OpenCode plugins; remove only stale `$source`-tagged settings entries and plugins carrying the generated ownership header. (AC5)
- [ ] Add exact generated-output assertions for the consolidated guard's source tag, matcher/event mapping, command path, timeout, and OpenCode event name selected by the final Feature 02 metadata. (AC5)
- [ ] Exercise propagation in a temporary consuming project, detach it from the source repository, and prove the guard runs after a simulated fresh clone with no pip, virtualenv, symlink, or manual installation step. (AC2)
- [ ] Re-run propagation over changed and unchanged inputs and verify coherent output updates, deterministic stale cleanup, stable versioning, and no accidental modification of unrelated settings. (AC1, AC2, AC5)

## Stage 2: Global Setup and Consolidation

- [ ] Replace the cwd-sensitive user-global symlink model in `scripts/setup-hook-symlinks.sh` with generated absolute-path wiring for each actually supported user-scope harness. (AC3)
- [ ] Preserve or safely back up/merge existing user configuration before changing generated-global wiring; never test against the developer's real HOME. (AC3)
- [ ] Select a machine-local generated-output location `[PROPOSED - name TBD]`, add it to `.gitignore`, and test that neither committed per-project outputs nor tracked documentation contain machine-specific absolute paths. (AC3)
- [ ] Add temporary-HOME tests for absolute command generation, idempotent reruns, source updates, safe handling of pre-existing user files, and useful verification failures. (AC3)
- [ ] Require green Feature 03 parity evidence and Stage 1 fresh-project/output tests as an explicit deletion gate before removing legacy hook definitions or scripts. (AC4)
- [ ] Retire `.github/hooks/bash-safety.json`, `.github/hooks/protect-files.json`, `.github/hooks/scripts/bash-safety.sh`, `.github/hooks/scripts/protect-files.sh`, and `.github/hooks/scripts/protect-files.py` only after the gate passes. (AC4)
- [ ] Regenerate Claude Code, Codex, and OpenCode outputs atomically from `.github/hooks/`, remove stale generated `bash-safety`/`protect-files` entries and plugins, and retain unrelated `audit-log`, `done-notify`, code-review-graph, and other untagged wiring. (AC4, AC5)
- [ ] Audit the resulting source and generated trees to prove no legacy wiring remains, no accepted legacy behavior was lost, and no committed absolute path was introduced. (AC3, AC4, AC5)

## Stage 3: Cross-Feature Integration

- [ ] Build an end-to-end smoke test that launches the propagated consolidated guard from the temporary consuming project using the same relative command emitted into platform wiring. (AC9)
- [ ] Replay representative file-tool and Bash payloads for `allow`, `ask`, and `deny`, including protected-path self-protection and an ordinary allowed operation, and assert one valid structured outcome per invocation. (AC9)
- [ ] Verify generated self-protection denies edits/writes to the propagated scripts, framework/analyzer modules, rule/default and override configuration, Claude/Codex wiring, and generated OpenCode plugin. (AC9)
- [ ] Seed payloads with unique secret sentinels and assert that decisions, stderr, audit output, setup output, and test artifacts never contain tool bodies, command bodies, file contents, or the sentinel. (AC9)
- [ ] Invoke the guard twice with both per-project and generated-global layers represented and prove allow/ask/deny decisions are functionally idempotent and never conflict. (AC6)
- [ ] Select the narrowest stateless duplicate-message suppression mechanism `[PROPOSED - name TBD]` only if needed, and prove it does not persist or compare raw secret-bearing payload content. (AC6)
- [ ] Assert a blocked double invocation presents one clear effective denial and does not create confusing duplicate denial or audit messages where practical. (AC6)
- [ ] Measure the completed propagated invocation path over representative payloads and assert median combined hook latency remains below 50 ms. (AC9)
- [ ] Run the full upstream framework, path-guard, analyzer/parity, propagation, and integration suites after consolidation and record the commands/results. (AC4, AC9)

## Stage 4: Installation and Operations Guide

- [ ] Research current official Claude Code, OpenCode, Codex, Cursor, and GitHub Copilot hook/extension capabilities during implementation; record direct evidence for each support classification rather than inferring a PreToolUse equivalent. (AC7)
- [ ] Create the installation guide `[PROPOSED - name TBD]` with an explicit fully supported/partial/not-supported table and reasons, limiting propagation instructions to Claude Code, Codex, and OpenCode mechanisms actually implemented. (AC7)
- [ ] Document per-project propagation as the primary shareable path and generated-global absolute wiring as optional local coverage, including how to verify each layer and recognize double firing. (AC7, AC10)
- [ ] Ensure every shell preflight or verification block reports useful failures for missing future/generated paths instead of relying on silent bare `test -e` commands. (AC7)
- [ ] Follow the Claude Code instructions verbatim in a clean checkout or temporary consuming project, verify a representative protected access is denied, and record the observed commands/results in the manual-QA artifact `[PROPOSED - name TBD]`. (AC8)
- [ ] Record live checks for bypass-mode deny/ask behavior, subagent tool calls, global-plus-project double firing, message clarity, and redacted logs without storing sensitive payloads. (AC8, AC9)
- [ ] Document the intentional env-rule re-tiering, improved denial messages, known Bash limitations, generated-global behavior, version marker, and upgrade/re-propagation steps. (AC10)
- [ ] Document human-only kill-switch recovery outside a guarded session, restoration of protection, and a safe rollback that restores prior source definitions and reruns propagation. (AC8, AC10)
- [ ] Perform a documentation/code-review audit confirming that support claims match current evidence, machine-local paths and secrets are absent, deferred WebFetch/backups/plugin packaging remain out of scope, and every AC has automated, code-review, or manual evidence. (AC7, AC8, AC10)
