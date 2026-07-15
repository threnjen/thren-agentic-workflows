# Phase 01 QA Coverage Map

**Date:** 2026-07-14  
**Scope:** Hook Framework, File-Access Guard, Bash-Command Analyzer, and Hook Distribution Integration  
**Release evidence state:** Automated gates passed in the current checkout; runner-constrained checks are Not run

## Evidence Legend

- **No** means automated tests or static review can establish the criterion without a live harness.
- **Yes** means a live runner, human-controlled recovery action, or presentation judgment is required.
- **Partial** means automated behavior is established, but a live or human-observed aspect remains.
- A live item remains **Not run** until its evidence includes the runner and version, timestamp, exact command or prompt, deployment layer, and redacted outcome.

## Acceptance-Criteria Coverage

| Feature | AC | Automated Coverage | Manual QA Needed? | Reason / Remaining Evidence |
|---|---|---|---|---|
| `01-hook-framework` | AC1 | `tests/hooks/test_hook_framework.py` covers seven tools, all observed aliases, malformed input, and retained context. | No | Payload normalization and errors are deterministic and assertable. |
| `01-hook-framework` | AC2 | Decision-emitter tests cover one structured `allow`/`ask`/`deny` result and exit-code-2 output. | Partial | A live Claude Code runner must show how structured decisions and exit code 2 are presented and enforced in bypass mode. **Not run.** |
| `01-hook-framework` | AC3 | Config tests cover recursive precedence, immutable snapshots, cache hits, mtime invalidation, and repository isolation. | No | Configuration behavior is deterministic and assertable. |
| `01-hook-framework` | AC4 | Security and audit tests induce parse, config, output, directory, serialization, open, write, and wrapper failures. | No | Fail-closed and fail-open boundaries are covered by executable tests. |
| `01-hook-framework` | AC5 | Tests prove only the protected project override disables the guard and environment variables cannot. | Partial | The human-only disable, repair, restore, and re-propagate workflow must be exercised outside a guarded session. **Not run.** |
| `01-hook-framework` | AC6 | Sentinel tests cover decisions, stdout, stderr, NDJSON, nested inputs, command bodies, and file bodies. | Partial | Live runner UI and dual-layer audit presentation must be inspected for sentinel absence. **Not run.** |
| `01-hook-framework` | AC7 | Public-export, isolated-import, stdlib-only, and no-subprocess tests cover the reusable contract. | No | The contract is statically and behaviorally assertable. |
| `01-hook-framework` | AC8 | Recorded fixtures and exception-path tests pass; `docs/hooks/hook-verification.md` records the live procedure. | Yes | Live bypass-mode deny/ask/exit-2 and subagent-originated PreToolUse execution remain **Not run**. |
| `01-hook-framework` | AC9 | A 1,000-invocation direct benchmark and import audit enforce median framework overhead below 50 ms. | No | Performance and dependency constraints are automated. |
| `02-file-access-guard` | AC1 | Rule-schema tests validate IDs, actions, reasons, priorities, escalation, and absence of concrete policy in Python. | No | Rule validation is deterministic. |
| `02-file-access-guard` | AC2 | All five file tools, environment variants, exact templates, and the non-template control are covered. | No | File-policy outputs are fully assertable. |
| `02-file-access-guard` | AC3 | Credential extensions, exact key names, four protected directories, and `id_generator.py` are covered. | No | Matching behavior is fully assertable. |
| `02-file-access-guard` | AC4 | Lock, production, user override, action, and reason behavior are covered. | No | Tier and override behavior is deterministic. |
| `02-file-access-guard` | AC5 | Traversal, real/broken symlink, tilde, and controlled case-mode tests pass. | No | Normalization behavior is covered in isolated filesystems. |
| `02-file-access-guard` | AC6 | Recorded Grep `path`/`glob`, overlap regressions, malformed input, ordinary scope, and Glob exclusion are covered. | No | Scope extraction and matching are assertable. |
| `02-file-access-guard` | AC7 | Unit and propagated-consumer tests cover scripts, configs, wiring, plugins, aliases, and symlinks. | Partial | A live bypass-mode attempt against generated wiring must demonstrate actual runner enforcement. **Not run.** |
| `02-file-access-guard` | AC8 | Tests assert rule/path/reason/alternative guidance and prevent body/full-payload reflection. | Partial | Live UI message clarity and absence of duplicate/conflicting text require human observation. **Not run.** |
| `02-file-access-guard` | AC9 | Induced failures, override recovery, environment-variable ineffectiveness, and payload-level bypass escalation pass. | Yes | Real bypass-mode deny plus the human recovery/restoration workflow remain **Not run**. |
| `02-file-access-guard` | AC10 | Direct and isolated downstream imports exercise `normalize_path`, `load_rules`, and `evaluate_path`. | No | Reuse and dependency boundaries are automated/static. |
| `03-bash-command-analyzer` | AC1 | Fixture and integration tests cover direct readers, copy/move, redirection, heredoc, xargs, substitutions, base64, and xxd. | No | Covered command classification is deterministic. |
| `03-bash-command-analyzer` | AC2 | Symlink creation option forms and real traversal are covered. | No | Symlink classification is automated. |
| `03-bash-command-analyzer` | AC3 | Every named evasion class is fixture-covered or linked to `docs/hooks/bash-command-limitations.md`. | Partial | A human must confirm the unsupported boundary is understandable and not overstated. **Not run for this release QA pass.** |
| `03-bash-command-analyzer` | AC4 | Payload-level tests establish `ask` for environment exposure, including `echo $PATH`, and safe controls. | Yes | Live bypass-mode handling of `ask` must be observed; it must not be reported as equivalent to `deny`. **Not run.** |
| `03-bash-command-analyzer` | AC5 | Curl/wget/encoding exfiltration and sentinel redaction tests pass. | Partial | A representative live Bash deny and UI/log redaction inspection remain **Not run**. |
| `03-bash-command-analyzer` | AC6 | All destructive patterns, variants, approved roots, protected-target precedence, and safe controls are covered. | No | Tier selection is deterministic; live `ask` semantics are already represented by AC4. |
| `03-bash-command-analyzer` | AC7 | The exact 16 fixed strings and 11 regex behaviors replay through `legacy-parity.json`. | No | The parity inventory and re-tier rationale are automated/static. |
| `03-bash-command-analyzer` | AC8 | Tests prove one strongest decision, shared path imports, fail-closed input handling, stdlib-only execution, and no subprocess/shell evaluation. | No | Architecture and decision behavior are automated/static. |
| `03-bash-command-analyzer` | AC9 | Documentation assertions cover recursive parent scans, variable expansion, interpreters, and safer alternatives. | Partial | Human review must confirm the limitations communicate an honest operational boundary. **Not run for this release QA pass.** |
| `04-hook-distribution-integration` | AC1 | Propagation tests cover full runtime copying, stable versioning, missing assets, path escapes, and target-root isolation. | No | Artifact emission and containment are automated. |
| `04-hook-distribution-integration` | AC2 | A detached temporary consumer runs the exact relative guard command without pip, venv, or source symlink. | No | Fresh-consumer execution is covered by a real subprocess test. |
| `04-hook-distribution-integration` | AC3 | Temporary-HOME tests cover absolute commands, backups, regular files, idempotence, and Claude/Codex/OpenCode ownership. | Partial | Live user-scope loading and project-plus-global presentation require real harnesses. **Not run.** |
| `04-hook-distribution-integration` | AC4 | Legacy files are absent, the 27-entry parity inventory remains, execution order is recorded, and the suite is green. | No | Retirement gate is automated/static. |
| `04-hook-distribution-integration` | AC5 | Generated-output tests cover source tags, event mapping, untagged wiring preservation, and owned stale cleanup. | Partial | Codex and OpenCode live decision handling remains **Not run**; their outputs are intentionally classified Partial. |
| `04-hook-distribution-integration` | AC6 | Relative and absolute subprocess invocations return identical one-line allow/ask/deny results. | Yes | Live Claude Code must show one clear effective denial when project and global layers both match. **Not run.** |
| `04-hook-distribution-integration` | AC7 | Documentation tests verify five harness rows and required limitation text; primary links are recorded. | Partial | Live Codex trust/decision behavior and OpenCode native blocking remain **Not run**; Cursor/Copilot have no emitted adapter. |
| `04-hook-distribution-integration` | AC8 | The plan-permitted temporary-consumer installation path produced an observed deny; documentation separates automated and live evidence. | Yes | The Claude Code guide still needs a live runner pass with version/timestamp evidence. **Not run.** |
| `04-hook-distribution-integration` | AC9 | Real subprocess smoke tests cover allow/ask/deny, eight self-protection targets, redaction, double invocation, and median latency. | Partial | Live bypass, subagent, and dual-layer semantics remain **Not run**. |
| `04-hook-distribution-integration` | AC10 | Documentation assertions cover policy changes, upgrade, global behavior, recovery, and rollback. | Yes | Human-only recovery, restoration, re-propagation, and rollback must be walked through in a disposable clone. **Not run.** |

## Verification Assets Checklist

This table maps every required verification asset from the Phase 01 execution manifest.

| Manifest Asset / Check | Coverage | Release Disposition |
|---|---|---|
| `tests/hooks/conftest.py` | Shared payload and fixture loaders are exercised by the full hook suite. | Passed in current 252-test run. |
| `tests/hooks/test_hook_framework.py` | Payload, decision, config/cache, failure posture, redaction, import, and latency coverage. | Passed. |
| `tests/hooks/test_file_access_guard.py` | File tools, Grep, normalization, tiers, credentials, self-protection, and recovery. | Passed. |
| `tests/hooks/test_bash_command_analyzer.py` | Evasion vectors, precedence, env/exfil/destructive tiers, and exact 27-case legacy parity. | Passed. |
| `tests/hooks/test_hook_distribution_integration.py` | Fresh consumer, double invocation, redaction, self-protection, smoke, docs, and latency. | Passed. |
| `tests/hooks/fixtures/` and subdirectories | Recorded payload, file-access, Bash command, and parity data. | Replayed by passing tests. |
| Live deny remains blocked in bypass mode | Claude live runner. | **Not run**; QA plan items C2, C3. |
| Observe ask-tier behavior in bypass mode | Claude live runner. | **Not run**; QA plan item C4. |
| Subagent-originated PreToolUse | Claude live runner. | **Not run**; QA plan item C6. |
| Secret/raw-body absence in decisions, stderr, audit, and evidence | Automated sentinels plus live UI/log inspection. | Automated passed; live **Not run**; QA plan item C7. |
| Project and generated-global consistency / clear blocked result | Automated dual command forms plus live UI. | Automated passed; live **Not run**; QA plan item D2. |
| Claude guide followed in clean consumer | Temporary consumer automated; live Claude registration and enforcement. | Automated passed; live **Not run**; QA plan items C1-C2. |
| Five-harness support classifications | Static docs/tests plus Codex/OpenCode live observations. | Static passed; partial-harness live checks **Not run**; QA plan section E. |
| Human-only override, restore, and rollback/re-propagation | Automated kill-switch behavior plus human workflow. | Automated passed; workflow **Not run**; QA plan items F1-F2. |
| Bash limitation boundary, including recursive parent scans | Documentation assertions plus human clarity review. | Static passed; human review **Not run**; QA plan item G1. |

## Current Automated Gate Evidence

| Gate | Command | Current Result |
|---|---|---|
| Full pytest suite | `uv run --with-requirements requirements-dev.txt pytest -q` | **Pass:** 252 passed in 3.56s |
| Combined coverage | `uv run --with-requirements requirements-dev.txt pytest -q --cov=.github/hooks/lib --cov=.github/hooks/scripts --cov=scripts --cov-report=term-missing --cov-fail-under=50` | **Pass:** 252 passed; 64.07% total, threshold 50% |
| Stdlib compatibility | `python3 -m unittest discover -s tests -v` | **Pass:** 14 passed |
| Python compilation | `python3 -m compileall -q .github/hooks/lib .github/hooks/scripts tests/hooks scripts/propagate_master_assets.py` | **Pass** |
| JSON syntax | `python3 -m json.tool` on Claude/Codex settings, hook metadata, and rule config | **Pass** |
| Shell syntax | `bash -n scripts/setup-hook-symlinks.sh` | **Pass** |
| Patch hygiene | `git diff --check` | **Pass** |

No automated release gate is Not run. Ruff is not a configured project gate and is therefore **Not applicable**, not a skipped failure.
