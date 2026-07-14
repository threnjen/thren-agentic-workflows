# Feature 03: Bash-Command Analyzer — Tasks

## Stage 0: Test Prerequisites

- [ ] Confirm `01-hook-framework` and `02-file-access-guard` are implemented, their automated suites are green, and their implementation records identify the finalized payload, decision, configuration, normalized-path, tier-evaluation, guard-entrypoint, and verification-checklist contracts.
- [ ] Replace plan-time proposed dependency paths/symbols with those finalized upstream contracts; keep every genuinely new concrete name marked `[PROPOSED - name TBD]` until the implementation selects and records it.
- [ ] Preserve the current baseline by running `python3 -m unittest discover -s tests -v` and confirming the existing two propagation tests still pass.
- [ ] Use `@z-test-writer` to establish or verify the pytest-capable `tests/hooks/` harness, coverage measurement, Bash payload fixture loader, and temporary filesystem/symlink helpers supplied by Feature 01.
- [ ] Create `tests/hooks/fixtures/bash/` `[PROPOSED - name TBD]` with a schema that records command input, expected action, expected rule category, optional normalized offending path, and covered-versus-limited status without embedding secret values.
- [ ] Inventory all 16 fixed strings from `.github/hooks/scripts/bash-safety.sh` and all 11 Bash regex rules from `.github/hooks/scripts/protect-files.py` into a legacy parity table; classify each as reproduced, Phase-re-tiered, or intentionally corrected.
- [ ] Add prerequisite fixture scenarios for malformed/empty payloads, multiple simultaneous matches, safe commands, and full-command redaction, then demonstrate at least 50% coverage for the initial feature scope with all tests passing.

## Stage 1: Analyzer and Shared Integration

- [ ] Implement a deterministic non-executing Bash analyzer in `.github/hooks/lib/bash_analyzer.py` `[PROPOSED - name TBD]` using only Python stdlib token/segment handling; prohibit subprocesses, `shell=True`, sourcing, expansion execution, and interpreter execution. (AC1, AC8)
- [ ] Integrate Bash payload handling into Feature 02's finalized guard entrypoint so parsing uses Feature 01's payload/failure contracts, extracted paths use Feature 02's normalizer/evaluator, and Feature 01 emits exactly one structured decision. (AC1, AC8)
- [ ] Aggregate analyzer matches before decision emission and enforce `deny` over `ask` over `allow`, including mixed protected-path, destructive-command, and approved-temp cases. (AC8)
- [ ] Extract candidate protected paths from direct `cat`, `less`, `head`, `grep`, `rg`, `cp`, and `mv` forms, then evaluate every candidate through the upstream path/tier contract. (AC1)
- [ ] Handle Phase-listed structural forms—input/output redirections, heredocs, pipes, `xargs`, subshells, command substitution, and base64/xxd pipelines—without executing the command. (AC1)
- [ ] Detect symlink creation that points at a protected target, including `ln -s .env <name>`, and ensure later traversal through a real symlink is normalized and denied by the shared evaluator. (AC2)
- [ ] Add isolated temporary-tree tests for symlink creation, symlink traversal, relative targets, and protected targets nested under otherwise approved temp/scratch locations. (AC2)
- [ ] Add fixtures for quote splitting, variable indirection, glob evasion, interpreter escapes, `~`, `../`, and case variants; classify each as covered with the required tier or unsupported with a limitations entry. (AC3)
- [ ] Verify empty, malformed, and ambiguous Bash payloads use Feature 01's redacted fail-closed `guard error` behavior and never echo command bodies. (AC8)
- [ ] Add downstream contract tests proving the analyzer imports/reuses the finalized Feature 01/02 APIs and does not duplicate decision JSON, configuration loading, normalization, or tier evaluation. (AC8)

## Stage 2: Tiered Command Rules

- [ ] Extend Feature 02's finalized shared rule configuration with stable identifiers, reasons, actions, and optional `escalate_in_bypass: deny` for environment-exposure, exfiltration, destructive-command, and approved-temp rules; keep concrete policy out of Python. (AC4, AC5, AC6, AC8)
- [ ] Configure and test `printenv`, bare `env`, bare `set`, bare `export`, and `echo $VAR`-style exposure, including the required `echo $PATH` result of `ask` rather than `deny`. (AC4)
- [ ] Configure and test high-confidence protected-file exfiltration through `curl -d @<file>`, equivalent curl data options, `wget --post-file`, and base64/xxd encoding pipelines using normalized protected-path candidates. (AC5)
- [ ] Assert every exfiltration denial reports only the rule identifier, action, safe reason, and normalized offending path where available; ensure the raw command and secret-bearing values are absent from stdout, stderr, and logs. (AC5)
- [ ] Configure all current destructive patterns—including recursive delete, force push, hard reset, clean, recursive permission changes, destructive device/file operations, and database drops—to return `ask` with case-variant coverage. (AC6, AC7)
- [ ] Define narrowly scoped approved scratchpad/temp exceptions and test allow behavior for safe destructive operations inside them while retaining `deny` for any protected target and `ask` for out-of-scope destructive targets. (AC6)
- [ ] Add mixed-match tests showing exfiltration/protected-path `deny` cannot be downgraded by environment/destructive `ask`, an approved-temp exception, or evaluation order. (AC5, AC6, AC8)
- [ ] Add safe-command and false-positive fixtures, including ordinary source reads, non-dump `env` usage, non-secret variable operations, and non-destructive commands, to verify unaffected commands remain allowed. (AC4, AC6)

## Stage 3: Legacy Parity and Limits

- [ ] Complete the legacy regression matrix with an automated fixture for every `bash-safety.sh` fixed string and every `protect-files.py` Bash regex; record the Phase rationale for every re-tiered rule. (AC7)
- [ ] Record malformed-input fail-closed handling and command-body redaction as intentional corrections rather than legacy regressions, and confirm Feature 04 receives an unambiguous pass/fail parity summary. (AC7, AC8)
- [ ] Write `docs/hooks/bash-command-limitations.md` `[PROPOSED - name TBD]` with each unsupported or intentionally bounded class, reproducible example, risk, detection boundary, and safer alternative; explicitly include recursive parent-directory scans such as `grep -r`. (AC3, AC9)
- [ ] Cross-check the fixture corpus against every Phase-listed vector and ensure each is either an automated covered case or linked to a specific limitations entry—never silently omitted. (AC3, AC9)
- [ ] Extend Feature 01's finalized live verification checklist with a representative Bash protected-file `deny`, observed `ask` behavior in bypass-permissions mode, and a redaction inspection; record observed results rather than assumptions. (AC4, AC5)
- [ ] Perform code-review evidence checks that the analyzer executes no shell/user code, adds no normal-path command logging, contains no concrete policy, and reuses rather than duplicates the upstream framework/path engine. (AC8)
- [ ] Run the safe-command soak corpus and review structured reasons for usefulness without full-command disclosure; add regression fixtures for any false positive discovered. (AC4, AC6, AC9)
- [ ] Run the complete hook suite, legacy parity matrix, current `unittest` suite, and coverage measurement; require all tests green and at least 50% feature coverage before handoff. (AC1–AC9)
- [ ] Deliver the parity matrix, limitations document, automated results, and runner-constrained evidence to `04-hook-distribution-integration`; do not retire or rewire legacy hooks in this feature. (AC7, AC9)
