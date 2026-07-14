# Feature 03: Bash-Command Analyzer

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** no
- **Depends on:** `01-hook-framework`, `02-file-access-guard`
- **Key files modified:** `.github/hooks/scripts/file-access-guard.py` `[PROPOSED - name TBD]`, `.github/hooks/config/file-access-rules.json` `[PROPOSED - name TBD]`, `.github/hooks/lib/bash_analyzer.py` `[PROPOSED - name TBD]`, `tests/hooks/conftest.py` `[PROPOSED - name TBD]` `(verify)`, `tests/hooks/test_bash_command_analyzer.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/bash/` `[PROPOSED - name TBD]`, `docs/hooks/bash-command-limitations.md` `[PROPOSED - name TBD]`, `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]`
- **Sequential reason:** shares `.github/hooks/scripts/file-access-guard.py` and `.github/hooks/config/file-access-rules.json` with upstream `02-file-access-guard`, and may extend `tests/hooks/conftest.py` plus `docs/hooks/hook-verification.md` from upstream `01-hook-framework`

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Indirect protected-path access:** Bash analysis detects protected paths used by `cat`, `less`, `head`, `grep`, `rg`, `cp`, `mv`, redirections, heredocs, `xargs`, subshells/command substitution, `base64`, and `xxd`, using Feature 02's normalized path and tier evaluator.
2. **AC2 — Symlink defenses:** Bash commands that traverse symlinks to protected paths or create a symlink pointing at a protected path, including `ln -s .env <name>`, are denied.
3. **AC3 — Evasion boundary:** Quote splitting, variable indirection, glob evasion, interpreter escapes, `~`/`../` paths, and uppercase variants are each represented by a fixture and are either handled with the required tier or explicitly listed as an unsupported limitation.
4. **AC4 — Environment exposure tiers:** `printenv`, bare `env`/`set`/`export`, and `echo $VAR`-style exposure use configured actions; ambiguous exposure such as `echo $PATH` results in `ask`, not `deny`.
5. **AC5 — Exfiltration tiers:** High-confidence protected-file exfiltration through `curl -d @<file>`, equivalent curl data forms, `wget --post-file`, and encoding pipelines is denied with a redacted reason.
6. **AC6 — Destructive command tiers:** Existing destructive patterns such as recursive delete, force push, hard reset, clean, destructive device/database operations, and equivalent legacy cases result in `ask`; destructive operations scoped to approved scratchpad/temp directories remain allowed.
7. **AC7 — Legacy regression parity:** All 16 current `bash-safety.sh` fixed strings and all 11 current `protect-files.py` Bash regexes are reproduced or explicitly re-tiered in configuration with regression fixtures before Feature 04 retires legacy wiring.
8. **AC8 — One shared engine:** Bash analysis reuses Feature 01's payload/decision/configuration contracts and Feature 02's path/tier evaluation contract; rule content remains in shared configuration rather than a second hardcoded engine.
9. **AC9 — Documented limitations:** Known-undetectable or intentionally unsupported classes, including recursive directory scans such as `grep -r` over a parent directory, are documented with their risk, boundary, and safer alternative.

### Non-Goals

- No claim of complete POSIX shell grammar interpretation is made.
- No WebFetch exfiltration guarding or prompt-injection scanning is added; those remain Phase 02 scope.
- No generated harness wiring, legacy file deletion, or installation documentation is performed here.
- No rule content is copied from inspiration repositories.
- No normal-path command logging is introduced.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1 | Bash analyzer `[PROPOSED - name TBD]`; guard entrypoint `[PROPOSED - name TBD]` | Must-have automated fixture per required command family |
| AC2 | Bash analyzer and Feature 02 path contract | Must-have automated symlink creation/traversal fixtures |
| AC3 | Bash fixture corpus `[PROPOSED - name TBD]`; limitations doc `[PROPOSED - name TBD]` | Must-have automated covered cases plus documented evidence for unsupported cases |
| AC4 | Shared rule config `[PROPOSED - name TBD]` | Must-have action-tier tests including `echo $PATH` |
| AC5 | Shared rule config and analyzer | Must-have deny and redaction tests for each exfiltration form |
| AC6 | Shared rule config and analyzer | Must-have destructive/non-destructive and temp exception tests |
| AC7 | Existing `.github/hooks/scripts/bash-safety.sh` and `.github/hooks/scripts/protect-files.py` as read-only references | Must-have regression matrix; code-review evidence before deletion in Feature 04 |
| AC8 | Feature 01/02 public contracts | Downstream contract tests and code-review evidence for no duplicate engine |
| AC9 | `docs/hooks/bash-command-limitations.md` `[PROPOSED - name TBD]` | Code-review evidence plus manual review for clarity |

### Phase Fidelity and Exceptions

- Key Deliverable 3 remains third and preserves every concrete evasion vector listed in the Phase Success Criteria.
- Recursive parent-directory scans are preserved as the explicit expected limitation named by the Phase document.
- No requirement is renamed, moved, reordered, or deferred.

### Unverified Assumptions

- A conservative tokenizer plus targeted parsing is sufficient for the required fixture corpus without introducing a third-party shell parser.
- Variable indirection and interpreter escapes may be bounded rather than fully interpreted; uncovered forms must be documented, not silently accepted as covered.
- Scratchpad/temp allow rules can be expressed narrowly enough not to weaken protected-path denials nested under those locations.

## B. Correctness & Edge Cases

### Key Workflows

- Parse Bash payload command text into conservative tokens/segments without executing it.
- Identify candidate paths and normalize them through Feature 02.
- Match configured indirect-access, env, exfiltration, and destructive rules.
- Select the strongest applicable action so a deny cannot be downgraded by an ask match.
- Emit one structured decision and document unsupported constructs.

### Failure Modes and Handling

- Parsing ambiguity involving a protected-looking path should use the conservative configured posture without echoing the command.
- Multiple matches choose `deny` over `ask` and produce one clear reason.
- Quote concatenation and command substitution cannot bypass candidate extraction for the covered fixtures.
- Temp-directory exceptions never override a protected-file deny.
- Empty or malformed Bash input follows Feature 01's fail-closed security posture.
- The analyzer must not execute shell expansion, subprocesses, or user code to determine a result.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Carry forward every pattern in current `bash-safety.sh` and the Bash portion of `protect-files.py`, but move policy to config and correct the Phase-specified tiers.
- Continue using the single PreToolUse guard definition created by Feature 02.
- Use Python 3 stdlib and structured decisions.

### Contracts and Decisions

- Feature 03 calls Feature 02's reusable normalized path/tier evaluation contract; the exact symbol selected by Feature 02 is authoritative.
- Bash-specific analysis can live in a dedicated helper `[PROPOSED - name TBD]`, while Feature 02's entrypoint remains the single decision boundary.
- Policy extensions are added to the same shared config as path rules, satisfying the Phase decision to define tier semantics once.
- Strongest-action precedence is `deny` before `ask` before `allow`.
- Duplication of upstream path normalization or decision JSON is prohibited.

### Relationships to Sibling Plans

- Depends on `01-hook-framework` and `02-file-access-guard` at runtime.
- Shares the guard entrypoint and rule configuration with Feature 02, so it must execute in Wave 3 and is not parallel safe.
- Supplies the regression evidence Feature 04 requires before deleting legacy scripts and wiring.
- Feature 04 runs end-to-end and double-fire smoke checks after this analyzer is integrated.
- Runner-constrained Bash deny/ask observations extend Feature 01's finalized shared verification checklist rather than creating a competing evidence file.

## D. Clean Design & Maintainability

### Simplest Design

- Use deterministic, non-executing token/segment analysis with small handlers for required command forms.
- Extract candidate paths, normalize once, and route all actions through the shared rule evaluator.
- Treat unsupported syntax as a documented boundary with fixtures rather than building a shell interpreter.

### Complexity and Duplication Risks

- Shell parsing can grow without bound; restrict implementation to Phase-listed vectors and clear conservative fallbacks.
- Regex-only matching can miss quote/variable composition; normalize covered constructs before rule evaluation.
- Separate destructive and secret analyzers could emit conflicting decisions; aggregate matches before emission.

### Keep It Clean Checklist

- [ ] No shell command is executed during analysis.
- [ ] No upstream path, decision, or configuration logic is duplicated.
- [ ] Every covered vector has a fixture and every uncovered vector is documented.
- [ ] Deny precedence cannot be weakened by ask/temp exceptions.
- [ ] Legacy parity matrix is complete before Feature 04 deletion.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Do not log normal Bash command bodies. On a match, record only rule identifier, decision, and normalized offending path where one exists. For command-only destructive rules, record the rule identifier without the raw command. Parser failures emit a redacted guard error.

### Security

- High-confidence protected access and exfiltration remain deny-tier.
- Ambiguous env exposure and legitimate-but-destructive commands remain ask-tier, with optional per-rule bypass escalation from config.
- Do not evaluate expansions through `shell=True`, subprocesses, sourcing, or interpreter execution.
- Preserve self-protection and kill-switch restrictions from Feature 02.

### Runbook

- Run the full fixture corpus and legacy regression matrix before consolidation.
- Review the limitations document after every parser change.
- Soak on representative safe commands to identify false positives.
- Roll back Feature 03 independently while Feature 02 path guarding remains available; Feature 04 must not retire legacy Bash hooks until parity passes.

## F. Test Plan

### Evidence Categories

- **Must-have automated tests:** One fixture per Phase-listed evasion vector, env/exfil tier tests, destructive/temp tests, action precedence, parser failures, and legacy parity.
- **Existing tests to update:** None; legacy scripts are references and propagation tests belong to Feature 04.
- **Runner-constrained tests:** Live `ask` behavior in bypass mode and a representative deny through Bash, recorded in Feature 01's finalized shared verification checklist.
- **Code-review evidence only:** No command execution during analysis and no duplicated upstream engine.
- **Manual QA checks:** Structured reasons are useful without including the full command; limitations are honest and reproducible.

### Top Five High-Value Checks

1. Given direct and transformed protected-file reads across every listed command family, when analyzed, then covered cases deny and uncovered cases appear in the limitations document.
2. Given `ln -s .env notes.txt` or later access through a protected symlink, when analyzed, then the creation/traversal attempt is denied.
3. Given bare env dumps and `echo $PATH`, when analyzed, then configured `ask` is returned; high-confidence file-posting/encoding exfiltration returns `deny`.
4. Given recursive delete outside and inside approved scratchpad/temp paths, when analyzed, then the former asks and the latter allows unless a protected target is involved.
5. Given every current legacy Bash rule, when replayed through the new analyzer, then behavior is reproduced or explicitly re-tiered with the Phase rationale.

### Test Data and Fixtures

- Direct access, redirection, heredoc, xargs, pipe, substitution, quote-split, variable, glob, interpreter, tilde, traversal, and case-variant commands.
- Symlink creation and traversal in temporary directories.
- Env-dump, ambiguous variable, curl/wget, base64/xxd, and mixed-action commands.
- Destructive commands inside/outside approved temp locations.
- A legacy-rule parity table derived from current scripts.

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Feature 01–02 tests are green; Bash fixture scaffolding exists; legacy behavior is inventoried; coverage for this feature is at least 50%; all tests pass
**Status**: Required before implementation begins

## Stage 1: Analyzer and Shared Integration
**Goal**: Add non-executing Bash analysis that reuses the upstream path, tier, configuration, and decision contracts
**Success Criteria**: AC1–AC3 and AC8 pass their automated contract and fixture tests
**Status**: Not Started

## Stage 2: Tiered Command Rules
**Goal**: Implement environment, exfiltration, destructive-command, and strongest-action behavior in shared configuration
**Success Criteria**: AC4–AC6 pass automated tests, including temp exceptions and deny precedence
**Status**: Not Started

## Stage 3: Legacy Parity and Limits
**Goal**: Complete legacy regression coverage and publish the covered/unsupported boundary
**Success Criteria**: AC7 and AC9 are satisfied; all Phase-listed vectors are represented; Feature 04 has evidence to retire legacy wiring
**Status**: Not Started
