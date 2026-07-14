# Feature 03: Bash-Command Analyzer — Context

## Key Files

### Files Changed by This Feature

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]` | Feature 02 guard entrypoint that remains the single PreToolUse decision boundary and delegates Bash input to the analyzer | Modify after Feature 02 finalizes the path |
| `.github/hooks/config/file-access-rules.json` `[PROPOSED - name TBD]` | Shared data-driven policy extended with environment, exfiltration, destructive-command, precedence, and approved-temp rules | Modify after Feature 02 finalizes the path |
| `.github/hooks/lib/bash_analyzer.py` `[PROPOSED - name TBD]` | Non-executing tokenizer/segment analyzer and candidate-path extraction helpers | Create |
| `tests/hooks/test_bash_command_analyzer.py` `[PROPOSED - name TBD]` | Automated contract, tier, precedence, parser-failure, and legacy-parity coverage | Create |
| `tests/hooks/fixtures/bash/` `[PROPOSED - name TBD]` | Recorded command payloads and expected outcomes for direct, evasive, destructive, and exfiltration cases | Create |
| `tests/hooks/conftest.py` `[PROPOSED - name TBD]` | Feature 01 fixture harness; extend only if Bash fixtures require a shared loader or temporary-tree helper | Modify if required |
| `docs/hooks/bash-command-limitations.md` `[PROPOSED - name TBD]` | Covered/unsupported shell-syntax boundary, risks, reproductions, and safer alternatives | Create |
| `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]` | Feature 01 live-harness checklist; append representative Bash deny and bypass-mode `ask` evidence | Modify after Feature 01 finalizes the path |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/scripts/bash-safety.sh` | Exact inventory of 16 current destructive fixed-string patterns and existing `ask` behavior | Read-only reference; retired only by Feature 04 |
| `.github/hooks/scripts/protect-files.py` | Exact inventory of 11 current Bash regexes for environment exposure, direct `.env` access, curl/wget, and base64 behavior | Read-only reference; retired only by Feature 04 |
| `.github/hooks/scripts/protect-files.sh` | Existing stdlib-Python wrapper and exit behavior | Read-only reference; retired only by Feature 04 |
| `.github/hooks/bash-safety.json` | Current Bash matcher, timeout, and platform event mapping | Read-only reference; retired only by Feature 04 |
| `.github/hooks/protect-files.json` | Current combined file/Bash matcher and published protected-pattern metadata | Read-only reference; retired only by Feature 04 |
| `dev/feature/01-hook-framework/01-hook-framework-plan.md` | Upstream payload, decision, configuration, failure, redaction, and verification contracts | Read-only reference |
| `dev/feature/02-file-access-guard/02-file-access-guard-plan.md` | Upstream normalized-path and tier-evaluation contract plus shared entrypoint/config ownership | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Authoritative enforcement posture, evasion corpus, clean-room boundary, and Phase success criteria | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing two-test `unittest` baseline; propagation expansion remains Feature 04 scope | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| The Feature 01/02 implementation directories and proposed guard/config/test/doc files do not exist on the current branch yet. Their public symbols and final paths therefore cannot be verified during expansion. | Feature 03 cannot safely import a plan-time symbol or assume the proposed filenames after its dependencies land. | **Warning:** before implementation, inspect the completed Feature 01/02 artifacts and implementation records, substitute their authoritative public APIs/paths, and keep all new names marked `[PROPOSED - name TBD]` until then. |
| The plan includes runner-constrained Bash checks but does not assign them an evidence artifact. Feature 01 already proposes a shared verification checklist. | Live evidence could otherwise be performed but not retained for Feature 04 or reviewers. | **Warning:** extend Feature 01's finalized verification checklist with representative Bash `deny` and bypass-mode `ask` observations instead of creating a competing checklist. |
| `bash-safety.sh` currently contains 16 case-insensitive fixed-string patterns: `rm -rf`, `rm -fr`, `git push --force`, `git push -f`, `git reset --hard`, `git clean -f`, `git clean -fd`, `chmod -R 777`, `dd if=`, `mkfs`, `> /dev/`, `truncate`, `shred`, `wipefs`, `DROP TABLE`, and `DROP DATABASE`. | AC7 parity must be measured against the complete current inventory, including variants omitted from the JSON metadata summary. | Build the regression matrix from the script itself and require one reproduced or explicitly re-tiered fixture per entry. |
| `protect-files.py` currently contains 11 Bash regex rules: four environment dumps, env-var echo, direct `.env` cat, three curl forms, wget post-file, and base64 `.env`. | AC7 must distinguish rule parity from preserving legacy defects. | Add each rule to the regression matrix, but apply Phase tiers and redaction rather than copying legacy deny-all and raw-command reflection behavior. |
| The legacy Python guard fails open on malformed JSON and includes full commands in denial reasons; the new shared contracts require fail-closed security behavior and redacted reasons. | Byte-for-byte legacy output parity would violate AC5/AC8 and Feature 01 security guarantees. | Record malformed-input and output-redaction behavior as intentional security corrections in the parity matrix. |
| The only existing automated suite is `tests/test_propagate_master_assets.py`, with two `unittest` tests. No `tests/hooks/`, phase-scoped consolidated test file, pytest configuration, coverage configuration, lint configuration, or format configuration exists. `pytest` is not installed in the active Python environment. | Stage 0 is a real prerequisite; Bash tests cannot assume the proposed pytest harness is already usable until Feature 01 has completed it. | Verify Feature 01's test bootstrap, retain the two-test baseline, establish feature coverage of at least 50%, and avoid introducing a redundant phase-wide test file. |
| `bash-safety.sh` uses case-insensitive substring matching while most `protect-files.py` regexes are case-sensitive. | “Uppercase variants” cannot be claimed uniformly from legacy behavior. | Include explicit case-variant fixtures and either support each intended form or document it as an unsupported boundary under AC3/AC9. |
| No existing test class or test method names are referenced by the plan; the proposed Bash test module does not exist. | Generated tasks must not invent test identifiers as existing facts. | Describe test scenarios without concrete method/class names unless the implementer selects and records them. |
| No phase-scoped test directory or consolidated Phase 01 test file exists under `tests/`. | There is no omitted established consolidation convention to follow. | Keep feature tests in the proposed `tests/hooks/` structure supplied by Feature 01; no extra phase test file is required. |

## Architectural Decisions

- Keep one PreToolUse guard entrypoint. Bash analysis returns matches to the Feature 02 guard, which emits the single final decision through Feature 01.
- Reuse Feature 02's finalized path normalization and tier evaluator for every extracted path. Do not create a Bash-only protected-path engine.
- Use deterministic, non-executing token/segment analysis with small handlers for the Phase-listed command forms. Do not attempt a complete POSIX shell parser.
- Keep concrete command and policy content in the same shared rule configuration used by Feature 02. Python implements interpretation and precedence only.
- Aggregate every applicable match before emission and apply `deny` before `ask` before `allow`; an approved-temp exception or later match cannot weaken a protected-path denial.
- Treat unsupported syntax as an explicit, reproducible product boundary. Each unsupported class belongs in the limitations document with risk and a safer alternative.
- Preserve auditability with rule identifier, decision, and normalized offending path only. Never log or reflect full Bash command bodies.

## Constraints

- Runtime code must use Python 3 stdlib only and must not execute shell expansion, subprocesses, sourced code, or interpreters to classify a command.
- Feature 03 starts only after Features 01 and 02 are implemented and green; their finalized public symbols are authoritative over proposed names in this plan set.
- Every covered Phase vector needs an automated fixture; every intentionally unsupported vector needs documented evidence.
- Rule actions remain data-driven. High-confidence protected access/exfiltration is `deny`; destructive-but-legitimate and ambiguous environment exposure is `ask` unless configuration explicitly escalates it.
- `ask` remains `ask` in bypass-permissions mode unless a rule sets `escalate_in_bypass: deny`; observed live behavior must be recorded rather than assumed.
- Approved scratchpad/temp behavior must be narrowly scoped and can never override a protected target nested inside an approved location.
- The guard must fail closed on empty, malformed, or unexpected Bash payloads through Feature 01's security failure posture.
- Do not copy rule content or implementation from `docs/inspiration/`; current repository scripts and the Phase requirements are the clean-room inputs.
- Keep legacy hook definitions/scripts active until Feature 04 has the completed regression evidence and performs retirement.
- Do not add normal-path command logging.

## Scope Boundaries

- Do not guard WebFetch exfiltration or add prompt-injection scanning; both remain Phase 02 scope.
- Do not add generated harness wiring, delete legacy scripts, alter propagation, or write installation documentation; Feature 04 owns those changes.
- Do not alter native file-tool/Grep path behavior delivered by Feature 02 except through its documented reusable contract.
- Do not guard `Glob` or claim recursive parent-directory scans such as `grep -r` are fully detectable.
- Do not introduce a general-purpose shell interpreter or third-party parser.
- Do not edit generated `.claude/`, `.codex/`, `claude/`, `codex/`, `opencode/`, or `.opencode/` outputs in this feature.

## Relationships to Sibling Plans

- `01-hook-framework` supplies payload parsing, decisions, layered configuration, failure handling, redacted event recording, and the live verification checklist.
- `02-file-access-guard` supplies the single guard entrypoint, shared configuration, normalized-path evaluator, and tier-decision contract. Feature 03 modifies those artifacts after their interfaces are finalized.
- `04-hook-distribution-integration` consumes Feature 03's legacy parity matrix, limitations, and live verification evidence before retiring legacy hooks and performing end-to-end/double-fire checks.

## Suggested Implementation Order

1. Confirm Features 01 and 02 are complete, green, and have recorded their finalized public APIs and paths.
2. Establish the Bash fixture harness and exact legacy-rule parity inventory.
3. Implement non-executing command segmentation, candidate extraction, symlink/evasion handling, and integration through the upstream contracts.
4. Extend shared configuration with environment, exfiltration, destructive, approved-temp, and precedence rules.
5. Complete parity, limitations, live-harness evidence, safe-command soak coverage, and the Feature 04 handoff.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 stdlib hook scripts + Bash wrappers + JSON configuration; no root application/package manifest |
| Test Runner | `python3 -m unittest discover -s tests -v` for the current suite; Feature 01 must establish the planned pytest-capable hook harness |
| Test Baseline | 2 passed, 0 failed in 0.003s — captured 2026-07-14 |
| Pytest | Not installed (`python3 -m pytest --version` reports `No module named pytest`) |
| Coverage | Not configured; Stage 0 requires at least 50% coverage for feature scope |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

> WebFetch as an exfiltration channel is deliberately unguarded in Hooks Phase 01 and must be reconsidered in Hooks Phase 02's tool-output/injection work.

Applied here as a hard scope boundary: command-mediated protected-file exfiltration is in scope; WebFetch analysis is not. No other learning entry directly matches this feature's Bash classification, configuration, or test requirements.
