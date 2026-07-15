# Feature 02: File-Access Guard — Context

## Key Files

### Files to Create or Modify

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/file-access-guard.json` `[PROPOSED - name TBD]` | Source-of-truth PreToolUse hook definition for file tools, Grep, and the later Bash analyzer | Create |
| `.github/hooks/config/file-access-rules.json` `[PROPOSED - name TBD]` | Data-driven default path rules, actions, reasons, safe alternatives, and optional bypass escalation | Create |
| `.github/hooks/config/file-access-overrides.json` `[PROPOSED - name TBD]` | Human-managed project override and kill-switch channel; the final path must be self-protected | Create |
| `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]` | Single guard entrypoint and small path/tool adapter layer built on Feature 01 contracts | Create |
| `tests/hooks/test_file_access_guard.py` `[PROPOSED - name TBD]` | Automated path, tool, tier, failure, redaction, and reusable-contract coverage | Create |
| `tests/hooks/fixtures/file_access/` `[PROPOSED - name TBD]` | Recorded tool payloads and temporary-tree scenario data | Create |
| `docs/hooks/file-access-guard.md` `[PROPOSED - name TBD]` | Policy model, safe alternatives, manual verification, recovery, and rollback guidance | Create |

### Read-Only References and Upstream Contracts

| File | Role | Change Type |
|------|------|-------------|
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Authoritative Phase 01 requirements, scope, enforcement posture, and success criteria | Read-only reference |
| `dev/feature/01-hook-framework/01-hook-framework-plan.md` | Upstream payload, configuration, decision, failure, kill-switch, logging, and fixture contracts | Read-only reference |
| `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-plan.md` | Downstream consumer of this feature's normalized path and tier evaluator | Read-only reference |
| `.github/hooks/protect-files.json` | Existing hook matcher and protected-pattern metadata to inventory; currently omits `NotebookEdit` and `Grep` | Read-only reference |
| `.github/hooks/scripts/protect-files.py` | Existing hardcoded path/Bash behavior and known regressions to reproduce or correct | Read-only reference |
| `.github/hooks/scripts/protect-files.sh` | Existing stdlib Python wrapper; remains wired until Feature 04 consolidation | Read-only reference |
| `.claude/settings.json` | Existing generated Claude wiring and a required self-protection target | Read-only reference |
| `.claude/settings.local.json` | Existing local Claude wiring and a required self-protection target | Read-only reference |
| `.codex/hooks.json` | Existing generated Codex wiring and a required self-protection target | Read-only reference |
| `.opencode/plugins/protect-files.js` | Current generated OpenCode guard plugin; future guard plugin name remains `[PROPOSED - name TBD]` | Read-only reference |
| `scripts/propagate_master_assets.py` | Existing `propagate_hooks_once` integration owned by Feature 04 | Read-only reference |
| `tests/test_propagate_master_assets.py` | Current two-test baseline; propagation assertions remain Feature 04 scope | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| The existing `.github/hooks/scripts/protect-files.py` hardcodes policy, uses broad `.env.*` and `id_*` patterns, has no `NotebookEdit`/`Grep` handling, reflects full paths/commands in deny messages, and exits successfully on JSON parse errors. | Confirms the planned behavior change and the need for template, false-positive, redaction, coverage, and fail-closed regressions. | Add explicit automated scenarios in Stages 1–3; keep the legacy files read-only until Feature 04. |
| Every new path in the plan is currently absent and is correctly marked `[PROPOSED - name TBD]`. No concrete test class or method names were presented as existing facts. | The implementer cannot assume the proposed layout or public symbol names are final. Feature 03 will depend on the selected public contract. | Finalize idiomatic paths/symbols after Feature 01 lands, record them in implementation notes, and make Feature 03 import the finalized contract. |
| Feature 01's framework files, public symbols, pytest fixtures, and protected override contract do not exist yet. | Feature 02 cannot safely implement its own substitute without duplicating or conflicting with the upstream framework. | Treat Feature 01 completion as a hard Stage 0 prerequisite and consume its final contracts. |
| No `tests/hooks/` tree, pytest configuration, or installed pytest module exists. The current suite is two `unittest` tests. | The plan's pytest/coverage success criteria are not executable in the current checkout. | Use `@z-test-writer` in Stage 0 after Feature 01 establishes the harness; document the exact resulting pytest/coverage command. |
| No recorded native `Grep` payload fixture exists, so the assumed path/glob field shapes cannot be verified from this repository. | A guessed adapter could miss a harness payload and silently allow protected searches. | **Warning:** use Feature 01's recorded Grep fixture to finalize extraction; add a fixture for every observed scope field and fail closed on malformed guard input. |
| Existing self-protection targets are concretely present at `.claude/settings.json`, `.claude/settings.local.json`, `.codex/hooks.json`, and `.opencode/plugins/*.js`; the future generated OpenCode guard filename is not yet known. | Self-protection must cover both current concrete paths and the final Feature 04 output without inventing a filename now. | Configure normalized path/glob rules for the named wiring files and the generated plugin location; coordinate the final plugin name with Feature 04. |
| No phase-scoped test directory or consolidated Phase 01 test file exists. The sole current test module covers propagation helpers, not guard behavior. | There is no omitted consolidated phase test to update, and existing guard assertions will not break. | Create the feature-local hook suite; leave propagation tests for Feature 04. |
| The checkout is macOS, but filesystem case sensitivity is not guaranteed by platform name alone. | Globally lowercasing paths would be incorrect on case-sensitive volumes and hard to verify portably. | Detect comparison behavior from the filesystem or isolate it behind a tested abstraction; make case-variant assertions conditional or controlled. |

## Architectural Decisions

- Keep all concrete protected-file policy in JSON configuration. Python owns payload adaptation, normalization, matching mechanics, precedence, and decision construction only.
- Route every candidate through one normalization pipeline before rule matching or redacted recording: expand `~`, resolve relative traversal, resolve symlink targets, and apply case folding only when the underlying filesystem is case-insensitive.
- Represent environment template exceptions as explicit, higher-specificity allow rules. Do not scatter `.env.sample` or `.env.example` exceptions through tool adapters.
- Use Feature 01's finalized payload, layered-configuration, decision, fail-closed, kill-switch, and redacted-recording contracts. Do not recreate any of them in this feature.
- Expose one narrow reusable normalized path/tier evaluation contract for Feature 03. The exact public symbol and file remain `[PROPOSED - name TBD]` until implementation.
- Centralize file-tool and Grep extraction adapters so supported payload fields cannot drift across tools.
- Select the strongest applicable configured action consistently. Invalid actions, missing reasons, malformed security payloads, and internal exceptions produce Feature 01's redacted `guard error` denial.
- Add no normal-path log output. On a match, record only rule identifier, decision, and normalized offending path through Feature 01's recorder.
- Keep the legacy guard wired until Feature 04 completes propagation and consolidation; Feature 02 creates source-of-truth behavior but does not modify generated outputs.

## Constraints

- Runtime code must use Python 3 stdlib only; no pip runtime dependency or subprocess-based hot path is allowed.
- Rules require a stable identifier, `reason`, and `action` of `deny` or `ask`; `escalate_in_bypass: deny` is optional and data-driven.
- Supported path-bearing tools are `Read`, `Edit`, `Write`, `MultiEdit`, and `NotebookEdit`; protected-scope `Grep` is guarded; `Glob` remains unguarded.
- Bash parsing, env-dump/exfiltration analysis, and destructive-command detection belong exclusively to Feature 03.
- Secret/protected-path rules fail closed and retain deny posture in bypass mode, subject to live premise verification.
- The human kill switch is available only through the protected project override file. No environment-variable activation path may exist.
- Denials and logs must never echo file contents, full tool input, or command bodies.
- Self-protection includes propagated scripts, rule configuration, Claude settings (including local settings), Codex hooks, generated OpenCode plugin files, and the override file itself.
- Windows support and code copied from `docs/inspiration/` repositories are out of scope.
- The feature must be idempotent under duplicate invocation; duplicate-message suppression is finalized by Feature 04.

## Scope Boundaries

- Do not modify `.claude/settings.json`, `.claude/settings.local.json`, `.codex/hooks.json`, or `.opencode/plugins/` in this feature.
- Do not change `scripts/propagate_master_assets.py` or `tests/test_propagate_master_assets.py`; propagation and consuming-project integration belong to Feature 04.
- Do not remove or rewire `.github/hooks/protect-files.json`, `.github/hooks/scripts/protect-files.sh`, `.github/hooks/scripts/protect-files.py`, or Bash-safety assets; Feature 04 owns retirement after Feature 03 parity evidence.
- Do not implement shell parsing, recursive parent-directory Grep analysis through Bash, destructive-command tiers, WebFetch guarding, prompt-injection scanning, pre-edit backup, or plugin packaging.
- Do not introduce normal-path logs, raw payload snapshots, a second framework, or a second tier engine.
- Do not broaden template exceptions beyond explicitly configured names or broaden SSH matching back to `id_*`.

## Relationships to Sibling Plans

- `01-hook-framework` is a hard prerequisite and supplies every shared mechanic. Feature 02 must wait for and import its finalized public contract.
- `03-bash-command-analyzer` consumes Feature 02's normalized path and tier evaluator and later extends the same guard entrypoint and rule configuration. This makes Feature 03 sequential and prevents it from forking the engine.
- `04-hook-distribution-integration` propagates the completed guard, updates generated Claude/Codex/OpenCode wiring, protects the final generated plugin path, retires legacy wiring, and verifies consuming-project/double-fire behavior.

## Suggested Implementation Order

1. Complete `01-hook-framework` and capture its final public names, fixture shapes, test command, and override contract.
2. Establish Feature 02's fixture corpus and confirm all supported file-tool and Grep payload fields.
3. Implement and test the data-driven rule schema, override precedence, normalization pipeline, and reusable tier evaluator.
4. Add tool adapters and configured environment, credential, project-file, Grep, and self-protection rules.
5. Complete failure, redaction, coverage, manual-message, and live bypass verification without enabling generated wiring.
6. Hand the finalized reusable contract and shared config layout to Feature 03, then leave propagation and legacy retirement to Feature 04.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 stdlib hook scripts, Bash wrappers, and JSON hook/rule configuration on macOS |
| Current Test Runner | `python3 -m unittest discover -s tests -v` |
| Planned Hook Test Runner | Pytest/coverage command to be established by Feature 01; `python3 -m pytest --version` currently fails with `No module named pytest` |
| Test Baseline | 2 passed, 0 failed in 0.003s — captured 2026-07-14 |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

- WebFetch as an exfiltration channel is deliberately outside Phase 01 and must remain for Phase 02 consideration.
- The pre-edit file backup layer was removed from Phase 01 and is a Phase 03 candidate; do not fold it into self-protection work.
- Plugin packaging is a deferred distribution target; this feature prepares propagated project assets only and does not create a plugin package.

No entries in the debugging, project, or review learnings files apply directly to the path-rule engine or its planned test corpus.
