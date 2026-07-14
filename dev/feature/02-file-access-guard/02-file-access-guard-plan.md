# Feature 02: File-Access Guard

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** `01-hook-framework`
- **Key files modified:** `.github/hooks/file-access-guard.json` `[PROPOSED - name TBD]`, `.github/hooks/config/file-access-rules.json` `[PROPOSED - name TBD]`, `.github/hooks/config/file-access-overrides.json` `[PROPOSED - name TBD]`, `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]`, `tests/hooks/test_file_access_guard.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/file_access/` `[PROPOSED - name TBD]`, `docs/hooks/file-access-guard.md` `[PROPOSED - name TBD]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Tiered rule configuration:** Every file-access rule is data-driven and includes a stable rule identifier, `reason`, and `action` (`deny` or `ask`), with optional `escalate_in_bypass: deny`; Python contains engine behavior but no concrete protected-file policy.
2. **AC2 — Environment-file behavior:** `Read`, `Edit`, `Write`, `MultiEdit`, and `NotebookEdit` against `.env` and its non-template variants are denied, while `.env.sample` and `.env.example` are allowed.
3. **AC3 — Credential behavior:** Credential patterns, exact SSH key names, and paths under `.ssh/`, `.aws/`, `.kube/`, and `.gnupg/` are denied, while unrelated names such as `id_generator.py` remain allowed.
4. **AC4 — Protected project files:** Lock files, production configuration, user-specified paths, and project override configuration are matched by normalized glob/path rules with their configured action and reason.
5. **AC5 — Normalized matching:** File-tool paths are normalized before matching through `~` expansion, `..` collapse, realpath/symlink resolution, and case-insensitive comparison on case-insensitive filesystems.
6. **AC6 — Grep coverage:** After Feature 01 records and verifies native/mapped `Grep` payload scope fields, a `Grep` request whose observed path or glob target is protected is denied, ordinary source searches remain allowed, malformed guarded input fails closed, and `Glob` remains outside the matcher.
7. **AC7 — Hook self-protection:** Edit/write attempts against propagated hook scripts, rule configuration, `.claude/settings.json`, `.claude/settings.local.json`, `.codex/hooks.json`, generated OpenCode plugin files, and the project override file are denied in consuming projects.
8. **AC8 — Structured guidance:** A blocked or held action reports the fired rule, normalized offending path, reason, and a safe alternative without echoing file content or full tool input.
9. **AC9 — Failure and recovery:** The guard uses Feature 01's fail-closed security posture, produces a `guard error` denial on induced exceptions, and honors the human-only override kill switch without an environment-variable path.
10. **AC10 — Reusable guard contract:** The path evaluation and tier-decision behavior is exposed for reuse by `03-bash-command-analyzer`; exact new symbols remain `[PROPOSED - name TBD]` and are added as an explicit upstream contract rather than duplicated downstream.

### Non-Goals

- No Bash command parsing, destructive-command detection, env-dump detection, or exfiltration analysis is implemented here.
- No `Glob` tool guarding is added.
- No propagation output, global setup, legacy deletion, or installation documentation is completed here.
- No Windows support or runtime pip dependency is introduced.
- No source is copied from `docs/inspiration/` repositories.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1 | Rule config `[PROPOSED - name TBD]`; guard entrypoint `[PROPOSED - name TBD]` | Must-have schema/behavior tests plus code-review evidence for no hardcoded policy |
| AC2 | Guard entrypoint and file rules `[PROPOSED - name TBD]` | Must-have automated fixtures for all five file tools and template exceptions |
| AC3 | File rules `[PROPOSED - name TBD]` | Must-have automated exact-name/location tests including `id_generator.py` |
| AC4 | Default and project override config `[PROPOSED - name TBD]` | Must-have precedence and configured-action tests |
| AC5 | Path normalization contract `[PROPOSED - name TBD]` | Must-have automated symlink, tilde, traversal, and case fixtures |
| AC6 | `.github/hooks/file-access-guard.json` `[PROPOSED - name TBD]`; Grep extraction logic | Must-have automated protected and ordinary Grep tests; code-review evidence for Glob exclusion |
| AC7 | Self-protection rules `[PROPOSED - name TBD]` | Must-have consuming-project path fixtures; integration confirmation in Feature 04 |
| AC8 | Feature 01 decision contract; guard messages | Must-have structured-output and redaction assertions; manual readability check |
| AC9 | Feature 01 failure/override contracts | Must-have induced-exception and protected-kill-switch tests |
| AC10 | Reusable path/tier evaluation contract `[PROPOSED - name TBD]` | Downstream import/contract tests in Feature 03 |

### Phase Fidelity and Exceptions

- Key Deliverable 2 remains the second feature and preserves every named tool and concrete wiring path from the Phase document.
- Bash-mediated access is intentionally assigned to Feature 03, matching the Phase's suggested feature boundary.
- No Phase requirement is renamed, reordered, or deferred.

### Unverified Assumptions

- Native and mapped `Grep` scope fields are not yet verified; Feature 01's recorded fixtures must establish the authoritative shapes before this adapter is finalized.
- Case-insensitive-filesystem detection can be implemented without subprocesses and tested portably with isolated fixtures.
- The exact default/override config filenames will be selected during implementation and recorded in the implementation notes.

## B. Correctness & Edge Cases

### Key Workflows

- Extract paths from each supported file-tool payload and from Grep scope fields.
- Treat Feature 01's recorded Grep fixtures as the authority for scope-field extraction; do not guess an unverified field shape.
- Normalize candidate paths before applying exact-name, location, and glob rules.
- Resolve default rules plus project overrides using Feature 01's configuration contract.
- Apply configured tier semantics and emit one structured decision with a safe alternative.
- Protect the guard's own definitions, scripts, wiring, rules, and override channel.

### Failure Modes and Handling

- Broken symlinks, symlink chains, relative paths, home-relative paths, and paths outside the current repository must not bypass matching.
- Templates are narrow allow exceptions; `.env.sample.extra` must not become allowed accidentally unless explicitly configured.
- Exact SSH-key rules cannot regress to the current broad `id_*` behavior.
- Grep without an explicit path remains allowed unless its explicit glob resolves to protected targets; recursive parent-directory scans remain a documented Bash limitation in Feature 03, not silently claimed here.
- Invalid actions or missing reasons in config fail closed as configuration errors.
- Kill-switch use cannot make its own file agent-editable.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Replace the current `protect-files.json`/`protect-files.py` behavior with a new source-of-truth guard definition only after Feature 04 integration; do not edit generated `.claude`, `.codex`, or `.opencode` outputs here.
- Preserve structured PreToolUse decision output and Python stdlib runtime.
- Use the framework contracts created by `01-hook-framework` for payloads, configuration, decisions, logging, and failure posture.

### Contracts and Decisions

- Rule content remains in JSON configuration; engine code interprets normalized paths and configured actions.
- The reusable path/tier evaluator required by Feature 03 is an acceptance criterion here. Its exact public symbol is `[PROPOSED - name TBD]`.
- Normalization occurs before allow/deny matching and before logging the offending path.
- Allow-template exceptions are explicit rules with higher specificity than environment-file denies, not scattered conditionals.
- Project overrides can tune policy and activate the human kill switch, but Feature 04 must ensure the override path is propagated and self-protected.

### Relationships to Sibling Plans

- Depends on `01-hook-framework` for all shared mechanics.
- Provides normalized protected-path and tier-decision behavior to `03-bash-command-analyzer`.
- Shares the guard entrypoint and rule configuration with Feature 03; Feature 03 must therefore execute later and is not parallel safe.
- Feature 04 owns final propagation, generated wiring, and consuming-project integration.

## D. Clean Design & Maintainability

### Simplest Design

- One guard entrypoint delegates shared mechanics to Feature 01 and policy evaluation to a small data-driven evaluator.
- Treat file paths as candidates that pass through one normalization pipeline before any rule checks.
- Keep rules reviewable and include reasons/actions beside each pattern.

### Complexity and Duplication Risks

- Per-tool path logic can drift; centralize extraction adapters and normalization.
- Separate self-protection logic could become incomplete; represent it in the same rule system.
- Overbroad globs can recreate false positives such as `id_generator.py`.
- Case normalization must follow filesystem behavior rather than lowercasing every platform unconditionally.

### Keep It Clean Checklist

- [ ] All concrete policy resides in configuration.
- [ ] Each rule has identifier, reason, and action.
- [ ] All paths are normalized once before evaluation.
- [ ] Template exceptions and exact SSH names have regression coverage.
- [ ] Downstream reusable contract is explicit and tested.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Record only rule identifier, decision, and normalized offending path through Feature 01's redacted recorder. Add no normal-path log line. Structured user messages may suggest `.env.sample` or another safe alternative without revealing matched content.

### Security

- Deny-tier rules must remain effective in bypass-permissions mode, subject to live verification evidence.
- Resolve symlinks before matching and protect symlink targets.
- Keep the override file in the deny set and provide no environment kill switch.
- Protect all wiring files named by the Phase, including local Claude settings and OpenCode plugin output.

### Runbook

- Run automated path/tool/config tests before enabling the new guard in generated wiring.
- Use isolated temporary directories for symlink and traversal tests.
- Verify the human kill switch outside an agent session, then restore protection.
- Roll back by keeping legacy wiring active until Feature 04 completes consolidation.

## F. Test Plan

### Evidence Categories

- **Must-have automated tests:** Five file tools, Grep scope, templates, credential names/locations, normalization, rule tiers, self-protection, induced failure, and kill-switch configuration.
- **Existing tests to update:** None; propagation tests remain Feature 04 scope.
- **Runner-constrained tests:** Live bypass-mode deny check against a disposable `.env` and a self-protected wiring file.
- **Code-review evidence only:** Glob remains outside the matcher; rule policy is absent from Python.
- **Manual QA checks:** Message clarity and safe-alternative usefulness without secret reflection.

### Top Five High-Value Checks

1. Given each supported file tool targeting `.env` and its variants, when the guard evaluates the payload, then access is denied; template files remain allowed.
2. Given a symlink, `~` form, `../` traversal, or case variant resolving to a protected target, when evaluated, then the normalized target is denied.
3. Given `id_generator.py`, exact SSH-key names, and files under `.ssh/`, when evaluated, then only the actual key cases are denied.
4. Given Grep targeting a protected path/glob and Grep over ordinary source, when evaluated, then only the protected search is denied and Glob is untouched.
5. Given edits to guard scripts, config, wiring, or override files, when evaluated in a consuming-project fixture, then the guard denies with a redacted structured reason.

### Test Data and Fixtures

- Temporary trees containing environment templates/variants, credentials, cloud directories, lock files, and production config.
- Real and broken symlinks plus traversal and home-relative forms.
- Case-variant fixtures with platform-appropriate assertions.
- Recorded payloads for all file tools and Grep scope variants.
- Consuming-project fixture paths for every self-protected output.

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Feature 01's pytest-capable harness is available; the current baseline remains green; file-guard fixtures exist; coverage for this feature is at least 50%; all tests pass
**Status**: Required before implementation begins

## Stage 1: Rule Model and Path Pipeline
**Goal**: Define data-driven tier rules, project overrides, and normalized path evaluation on Feature 01 contracts
**Success Criteria**: AC1, AC4–AC5, AC9–AC10 pass automated tests
**Status**: Not Started

## Stage 2: Tool and Secret Coverage
**Goal**: Implement file-tool, Grep, credential, environment-template, and self-protection behavior
**Success Criteria**: AC2–AC3 and AC6–AC8 pass automated and structured-message checks
**Status**: Not Started

## Stage 3: Guard Verification
**Goal**: Complete regression, redaction, and runner-constrained verification without changing generated wiring
**Success Criteria**: All acceptance criteria pass; bypass-mode evidence is recorded; Feature 03's reusable contract is ready
**Status**: Not Started
