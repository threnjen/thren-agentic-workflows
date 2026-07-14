# Feature 02: File-Access Guard — Tasks

## Stage 0: Test Prerequisites

- [ ] Confirm `01-hook-framework` is implemented and green; record the finalized payload, configuration, decision, failure, kill-switch, and redacted-recorder import contracts that Feature 02 will consume.
- [ ] Invoke `@z-test-writer` to establish the pytest-capable `tests/hooks/` harness, coverage measurement, and exact developer commands required by this plan.
- [ ] Re-run the existing `python3 -m unittest discover -s tests -v` suite and preserve the two-test baseline before adding guard tests.
- [ ] Create the proposed file-access fixture area `[PROPOSED - name TBD]` with isolated temporary trees for environment files/templates, credentials, cloud directories, project files, self-protection paths, symlinks, traversal, home-relative paths, and case behavior.
- [ ] Add or reuse recorded Feature 01 payload fixtures for `Read`, `Edit`, `Write`, `MultiEdit`, `NotebookEdit`, and every observed native `Grep` path/glob field; do not guess unsupported payload keys.
- [ ] Add failing scenario tests for AC1–AC10 before implementation, including template exceptions, `id_generator.py`, normalized aliases, Grep scope, redaction, induced errors, kill-switch behavior, and the downstream reusable contract.
- [ ] Establish at least 50% coverage for the feature scope and keep all baseline and new prerequisite tests green before Stage 1 implementation begins.

## Stage 1: Rule Model and Path Pipeline

- [ ] Finalize the proposed guard, rule-config, override-config, test, fixture, and documentation paths; record every selected name and the reusable public API in implementation notes so Feature 03 has an authoritative contract.
- [ ] Define and validate the data-driven rule schema for AC1: stable rule identifier, non-empty `reason`, `action` restricted to `deny` or `ask`, safe-alternative data where needed, and optional `escalate_in_bypass: deny`.
- [ ] Ensure invalid actions, missing reasons, malformed configuration, and internal evaluator exceptions route through Feature 01's fail-closed security wrapper as a redacted `guard error` denial (AC1, AC9).
- [ ] Implement repo-default plus project-override loading through Feature 01's layered configuration and cache contract, including deterministic precedence and mtime invalidation (AC4, AC9).
- [ ] Implement the human-only override kill switch exclusively through the protected override file and add code-review/test evidence that no environment-variable activation path exists (AC9).
- [ ] Implement one candidate-path normalization pipeline that expands `~`, anchors relative paths, collapses `..`, resolves real and broken symlink cases conservatively, supports paths outside the repository, and case-folds only on case-insensitive filesystems (AC5).
- [ ] Add portable normalization tests using temporary directories and controlled/conditional case assertions rather than assuming every macOS volume is case-insensitive (AC5).
- [ ] Implement configured matching and specificity/precedence so narrow allow exceptions can override broader environment-file denies while stronger protected-path deny rules cannot be weakened accidentally (AC1, AC2, AC4).
- [ ] Keep all concrete path policy in configuration and add code-review evidence that Python contains only schema, normalization, matching, precedence, and adapter behavior (AC1).
- [ ] Expose and test one narrow normalized path/tier evaluation contract `[PROPOSED - name TBD]` that returns enough rule, action, reason, normalized path, and safe-alternative data for Feature 03 without emitting a second decision (AC10).

## Stage 2: Tool and Secret Coverage

- [ ] Create the source-of-truth PreToolUse guard definition `[PROPOSED - name TBD]` for `Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Bash`, while keeping Bash analysis deferred to Feature 03 and `Glob` outside the matcher (AC6, AC10).
- [ ] Implement centralized payload adapters for the five supported file tools and the verified native Grep scope fields, routing every extracted candidate through the same normalization/evaluation pipeline (AC2, AC5, AC6).
- [ ] Add configured environment-file denies for `.env` and non-template variants across all five file tools, plus explicit higher-specificity allows for exactly `.env.sample` and `.env.example`; verify `.env.sample.extra` is not accidentally allowed (AC2).
- [ ] Add configured credential rules for required extensions/names and locations under `.ssh/`, `.aws/`, `.kube/`, and `.gnupg/`; verify exact SSH key names deny while unrelated `id_generator.py` remains allowed (AC3).
- [ ] Add configured lock-file, production-configuration, user-specified-path, and project-override rules with normalized glob/path matching and per-rule reason/action behavior (AC4).
- [ ] Implement Grep protection for each verified path/glob scope form and tests showing protected targets deny while ordinary source searches and Grep without a protected explicit scope remain allowed (AC6).
- [ ] Add data-driven self-protection rules for propagated hook scripts, rule config, `.claude/settings.json`, `.claude/settings.local.json`, `.codex/hooks.json`, generated `.opencode/plugins/` guard output, and the project override file (AC7).
- [ ] Cover self-protection with consuming-project fixture paths, including normalized aliases and symlinks, without editing any generated wiring in this feature (AC7).
- [ ] Build structured `deny`/`ask` guidance through Feature 01's decision contract, including fired rule, normalized offending path, configured reason, and a useful safe alternative without full input or content reflection (AC8).
- [ ] Record only rule identifier, decision, and normalized offending path through Feature 01's redacted recorder; add secret-sentinel assertions proving Write bodies and full Grep/tool payloads never appear in decisions, logs, exceptions, or test snapshots (AC8, AC9).

## Stage 3: Guard Verification

- [ ] Run the complete automated matrix for all five file tools, Grep scopes, environment templates/variants, credential exact names/locations, protected project files, configuration tiers, normalization vectors, and self-protection targets (AC1–AC8).
- [ ] Add induced evaluator/configuration exception scenarios and verify they produce one structured `guard error` denial rather than a silent allow; verify the protected override-file kill switch restores operation when changed by a human (AC9).
- [ ] Verify the reusable path/tier contract can be imported and exercised by a downstream contract test without duplicating normalization, rule loading, tier precedence, or decision JSON behavior (AC10).
- [ ] Perform code-review checks that `Glob` remains unguarded, concrete policy is absent from Python, the runtime import set is stdlib-only, no subprocess is used in the hot path, and no environment kill switch exists.
- [ ] Manually review representative deny/ask messages for clarity and safe alternatives, confirming no secret content or full tool input is reflected (AC8).
- [ ] In a disposable live harness, record runner-constrained evidence that deny-tier access to `.env` and a self-protected wiring file remains blocked in bypass mode; do not claim automated coverage for this premise check (AC7, AC9).
- [ ] Document the final policy/config contract, normalization behavior, known Grep scope boundary, human recovery procedure, verification commands, and rollback path in the proposed guard documentation `[PROPOSED - name TBD]`.
- [ ] Run the final pytest/coverage command established by Feature 01, confirm at least 50% feature coverage and all tests pass, then re-run the existing unittest suite to detect unrelated regressions.
- [ ] Hand off the finalized public evaluator contract, shared rule-config layout, and green contract evidence to `03-bash-command-analyzer`; leave generated wiring, legacy retirement, and consuming-project integration to Feature 04.
