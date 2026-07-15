# QA Readiness Analysis: Phase 01 Hook Foundation + File-Access Guard

**Date:** 2026-07-14  
**Analyst:** prod-code-review (automated)  
**Verdict:** NO-GO  
**Documents Analyzed:** 24 pipeline, QA, manifest, and security documents  
**Findings:** 11 (0 blocker-severity, 5 high, 4 medium, 2 low); 2 High findings are release-blocking

## Readiness Verdict

**NO-GO.** Phase 01 must not begin manual release QA yet. A reproducible nested-destination symlink escape lets hook propagation write outside the declared consuming-project root, and the required below-50-ms propagated-hook latency gate failed two of five observed runs. Both are Phase 01 Feature 04 acceptance failures that require implementation and review re-entry.

## Executive Summary

The four feature bundles and consolidated QA documents are present, and most deterministic behavior is backed by strong automated coverage. The final validation pass produced 252 passing tests at 64.07% combined coverage, 14 passing stdlib tests, and clean compile, JSON, shell, and patch-hygiene gates; however, the ordinary full-suite run first failed the propagated latency AC, and a focused rerun failed again before three passes. More critically, an adversarial temporary-tree probe confirmed security finding SEC-01: a nested destination-directory symlink redirected copied hook modules outside the consumer root without an exception. The QA plan is detailed and actionable for the live-runner handoff, but it currently claims destination containment is fully automated when the missing nested-ancestor case is release-blocking. Confidence is high in the deterministic rule/runtime tests and only moderate in the current distribution/performance evidence.

## Review Mode and Scope

- **Mode:** Standard (`All verdicts Approved: NO`).
- **Source delta:** `c4d2eaf..12d9ff3`, 57 changed files, 6,115 insertions, and 607 deletions.
- **Graph result:** High risk (0.80), five affected flows, and 102 static test-link gaps. Dynamic imports and subprocess tests explain many graph gaps, so the graph count was cross-checked against executable tests rather than treated as a failure count.
- **Visual verification:** Skipped for Phase 01. The repository is not a Unity application (`Assets/` and `ProjectSettings/` are absent); two `*.asmdef` files belong to the reusable visual-verification package. That package remains represented by pre-existing SEC-04.
- **Mutation boundary:** No source, test, configuration, or existing pipeline document was modified during this review.

## Document Inventory

### Feature 01 — Hook Framework

| Document | File | Source | Present | Notes |
|---|---|---|---|---|
| Feature Plan | `dev/feature/01-hook-framework/01-hook-framework-plan.md` | Feature - Decomposer | Yes | Defines AC1-AC9 and the framework/failure-posture contract. |
| Context | `dev/feature/01-hook-framework/01-hook-framework-context.md` | z-feature-plan-expander | Yes | Records payload, audit, import, and test-prerequisite discovery. |
| Tasks | `dev/feature/01-hook-framework/01-hook-framework-tasks.md` | z-feature-plan-expander | Yes | Automated work is checked; runner-constrained work remains open. |
| Implementation Record | `dev/feature/01-hook-framework/01-hook-framework-implementation.md` | z-feature-implementer | Yes | AC8 is correctly Partial; commit columns remain `PENDING`. |
| Review Record | `dev/feature/01-hook-framework/01-hook-framework-review.md` | z-feature-reviewer | Yes | Approved with Reservations; one open Medium live-evidence concern. |

### Feature 02 — File-Access Guard

| Document | File | Source | Present | Notes |
|---|---|---|---|---|
| Feature Plan | `dev/feature/02-file-access-guard/02-file-access-guard-plan.md` | Feature - Decomposer | Yes | Defines AC1-AC10 and data-driven file/Grep protection. |
| Context | `dev/feature/02-file-access-guard/02-file-access-guard-context.md` | z-feature-plan-expander | Yes | Records normalization, payload, and self-protection boundaries. |
| Tasks | `dev/feature/02-file-access-guard/02-file-access-guard-tasks.md` | z-feature-plan-expander | Yes | Live bypass check remains open and delegated to integration QA. |
| Implementation Record | `dev/feature/02-file-access-guard/02-file-access-guard-implementation.md` | z-feature-implementer | Yes | All deterministic AC work is recorded; commit columns remain `PENDING`. |
| Review Record | `dev/feature/02-file-access-guard/02-file-access-guard-review.md` | z-feature-reviewer | Yes | Approved with Reservations after one High Grep fix. |

### Feature 03 — Bash-Command Analyzer

| Document | File | Source | Present | Notes |
|---|---|---|---|---|
| Feature Plan | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-plan.md` | Feature - Decomposer | Yes | Defines AC1-AC9, bounded parsing, and 27-case parity. |
| Context | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-context.md` | z-feature-plan-expander | Yes | Exact 16 fixed strings and 11 regex behaviors are inventoried. |
| Tasks | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-tasks.md` | z-feature-plan-expander | Yes | Live deny/ask/redaction work remains open. |
| Implementation Record | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-implementation.md` | z-feature-implementer | Yes | Limitations are explicit; commit columns remain `PENDING`. |
| Review Record | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-review.md` | z-feature-reviewer | Yes | Approved with Reservations; one open Low attribution issue. |

### Feature 04 — Hook Distribution Integration

| Document | File | Source | Present | Notes |
|---|---|---|---|---|
| Feature Plan | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-plan.md` | Feature - Decomposer | Yes | Defines AC1-AC10 for propagation, consolidation, harnesses, and latency. |
| Context | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-context.md` | z-feature-plan-expander | Yes | Identifies root-boundary and generated-output review focus. |
| Tasks | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-tasks.md` | z-feature-plan-expander | Yes | Automated tasks are checked; live harness tasks remain for QA. |
| Implementation Record | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-implementation.md` | z-feature-implementer | Yes | AC1 and AC9 are marked Complete despite final blocker evidence; commit columns remain `PENDING`. |
| Review Record | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-review.md` | z-feature-reviewer | Yes | Approved with Reservations; it incorrectly reports destination containment and stable latency as verified. |

### Consolidated and Gate Documents

| Document | File | Source | Present | Notes |
|---|---|---|---|---|
| QA Plan | `docs/phases/PHASE_01/PHASE_01_QA.md` | z-feature-qa-writer | Yes | Sixteen actionable manual items; all initially Not run. |
| Coverage Map | `docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md` | z-feature-qa-writer | Yes | Maps all 38 ACs and all nine manifest checklist concepts. |
| Execution Manifest | `dev/feature/phase-01-hook-foundation-file-access-guard-execution-manifest.md` | Feature - Decomposer | Yes | Four waves, verification assets, and nine manual QA checks. |
| Security Scan | `docs/phases/PHASE_01/PHASE_01-security-scan.md` | security-scan | Yes | BLOCKED: 0 Critical, 4 High, 3 Medium, 1 Low. |

No required per-feature or consolidated QA document is missing. No unexpected document was found inside the four feature folders.

## Traceability Matrix

`Manual pending` means the consolidated QA plan has an actionable live/human item; it is not being misreported as automated evidence.

| Feature | AC | Plan | Impl | Code | Review | In Consolidated QA | Verdict |
|---|---|---|---|---|---|---|---|
| 01 | AC1 | Defined | Complete | Verified | Verified | Covered | OK |
| 01 | AC2 | Defined | Complete | Verified | Verified after fix | Covered, live partial | MANUAL PENDING |
| 01 | AC3 | Defined | Complete | Verified with SEC-07 risk | Verified | Covered | AT RISK |
| 01 | AC4 | Defined | Complete | Verified | Verified after fix | Covered | OK |
| 01 | AC5 | Defined | Complete | Verified | Verified | Covered, human workflow | MANUAL PENDING |
| 01 | AC6 | Defined | Complete | Verified with SEC-05 risk | Verified | Covered, live partial | AT RISK |
| 01 | AC7 | Defined | Complete | Verified | Verified | Covered | OK |
| 01 | AC8 | Defined | Partial | Automated portion verified | Partial / Unverified | Covered by C1-C8 | MANUAL PENDING |
| 01 | AC9 | Defined | Complete | Direct benchmark verified | Verified | Covered | OK |
| 02 | AC1 | Defined | Complete | Verified | Verified | Covered | OK |
| 02 | AC2 | Defined | Complete | Verified | Verified | Covered | OK |
| 02 | AC3 | Defined | Complete | Verified | Verified | Covered | OK |
| 02 | AC4 | Defined | Complete | Verified | Verified | Covered | OK |
| 02 | AC5 | Defined | Complete | Verified | Verified | Covered | OK |
| 02 | AC6 | Defined | Complete | Verified | Verified after fix | Covered | OK |
| 02 | AC7 | Defined | Complete | Automated behavior verified | Live reservation | Covered by C4 | MANUAL PENDING |
| 02 | AC8 | Defined | Complete | Verified | Verified | Covered by C8/D2 | MANUAL PENDING |
| 02 | AC9 | Defined | Complete | Automated behavior verified | Live reservation | Covered by C2-C5/F1 | MANUAL PENDING |
| 02 | AC10 | Defined | Complete | Verified | Verified | Covered | OK |
| 03 | AC1 | Defined | Complete | Verified within published boundary | Verified after fix | Covered | OK |
| 03 | AC2 | Defined | Complete | Verified | Verified after fix | Covered | OK |
| 03 | AC3 | Defined | Complete | Covered-or-documented | Verified | Covered by G1 | MANUAL PENDING |
| 03 | AC4 | Defined | Complete | Verified | Verified | Covered by C5 | MANUAL PENDING |
| 03 | AC5 | Defined | Complete | Verified | Verified after fix | Covered by C3/C8 | MANUAL PENDING |
| 03 | AC6 | Defined | Complete | Verified | Verified after fix | Covered | OK |
| 03 | AC7 | Defined | Complete | 27/27 verified | Verified | Covered | OK |
| 03 | AC8 | Defined | Complete | Verified | Verified | Covered | OK |
| 03 | AC9 | Defined | Complete | Verified as limitation contract | Verified | Covered by G1 | MANUAL PENDING |
| 04 | AC1 | Defined | Complete | Nested destination containment missing | Incorrectly Verified | Coverage claim is inaccurate | **BLOCKED** |
| 04 | AC2 | Defined | Complete | Functional detached consumer verified | Verified automated | Covered | OK, inherits AC1 security risk |
| 04 | AC3 | Defined | Complete | Automated behavior verified | Verified automated | Covered by D1-D2 | MANUAL PENDING |
| 04 | AC4 | Defined | Complete | Verified | Verified | Covered | OK |
| 04 | AC5 | Defined | Complete | Automated ownership verified | Verified | Covered by E1-E3 | MANUAL PENDING |
| 04 | AC6 | Defined | Complete | Subprocess equivalence verified | Partial live | Covered by D2 | MANUAL PENDING |
| 04 | AC7 | Defined | Complete | Static documentation verified | Verified static | Covered by E1-E3 | MANUAL PENDING |
| 04 | AC8 | Defined | Complete | Temporary consumer verified | Verified temporary consumer | Covered by C1-C2 | MANUAL PENDING |
| 04 | AC9 | Defined | Complete | Latency gate unstable | Incorrectly Verified as stable | Covered | **BLOCKED** |
| 04 | AC10 | Defined | Complete | Documentation verified | Verified documentation | Covered by F1-F2/G1 | MANUAL PENDING |

## Validation Results

| Gate | Result | Assessment |
|---|---|---|
| Full pytest suite | **Fail:** 251 passed, 1 failed; propagated latency median 52.22 ms | Required ordinary gate was not green. |
| Focused latency reruns | **Fail:** 64.11 ms; then **Pass** three consecutive times | Demonstrates non-deterministic evidence, not a stable AC pass. |
| Combined coverage | **Pass:** 252 passed, 64.07%; threshold 50% | Functional coverage gate is green. |
| Stdlib compatibility | **Pass:** 14/14 | No regression to the stdlib suite. |
| Compile gate | **Pass** | Hook libraries, scripts, tests, and propagator compile. |
| JSON gate | **Pass** | Claude/Codex settings, hook definition, rules, and override parse. |
| Shell syntax | **Pass** | `scripts/setup-hook-symlinks.sh` passes `bash -n`. |
| Patch hygiene | **Pass** | `git diff --check` is clean. |
| Nested destination containment probe | **Fail:** no exception; `__init__.py`, `bash_analyzer.py`, `file_access.py`, and `framework.py` written through a nested `lib` symlink outside the consumer root | Reproduces SEC-01 and blocks release. |

## Findings

Finding counts are unique across the following tables. Security IDs retain the severities and phase relationships assigned by the security scan.

### Cross-Document Issues

| ID | Finding | Severity | Documents Involved | Evidence | Recommendation |
|---|---|---|---|---|---|
| QA-01 | Consolidated QA says propagation containment is automated and complete, contradicting the reproducible nested-ancestor escape. | Medium | QA plan, coverage map, Feature 04 review, security scan | `PHASE_01_QA.md:54`; coverage map `:46`; Feature 04 review `:15,30,39`; security scan `:52` | After the fix, add the missing regression and update the QA evidence text to name final-target and intermediate-ancestor containment explicitly. |
| DOC-01 | Traceability metadata was not closed: all implementation AC rows retain `PENDING` commit SHAs, and three manifest-check references in the coverage map point to stale manual IDs. | Low | Four implementation records; coverage map | Feature 04 implementation `:30-41` is representative; coverage map `:70-72` says C4/C6/C7, while the actual ask/subagent/redaction items are C5/C7/C8. | Fill implementation/review SHAs and correct the three checklist references during pipeline record refresh. |

### Implementation Issues

| ID | Finding | Severity | File:Line | Evidence | Recommendation |
|---|---|---|---|---|---|
| SEC-01 | Copied hook assets can traverse a nested destination-directory symlink and write outside the declared consumer root. **Release-blocking.** | High | `scripts/propagate_master_assets.py:882-896`, `:948-959` | `_validate_output_directory` validates only four top-level output directories; `_copy_hook_assets` checks a final-file symlink but not symlinked ancestors. The temporary probe wrote four modules outside the target with no error. Tests at `tests/test_propagate_master_assets.py:197-213` cover only the root directory, and `:425-449` covers only a final-file symlink. | Contain-check every resolved destination immediately before each write/removal; reject symlink ancestors; use no-follow/atomic replacement where supported; add nested regressions for `lib/`, `scripts/`, `config/`, generated settings parents, plugins, version marker, and retirement cleanup. |
| PERF-01 | The propagated guard's `<50 ms` median AC is not stable in the release checkout. **Release-blocking.** | High | `tests/hooks/test_hook_distribution_integration.py:170-183` | Full suite failed at 52.22 ms; the first focused rerun failed at 64.11 ms; three later focused runs passed. Feature 04 review `:23` and QA plan `:46-47` report an unconditional pass. | Improve runtime margin or adopt a representative, repeatable benchmark methodology that still enforces the plan's fixed `<50 ms` requirement. Do not raise the threshold to hide the failure. |
| SEC-02 | Bounded Bash analysis does not interpret dynamic variables, interpreter-mediated access, or recursive parent scans. | High | `.github/hooks/lib/bash_analyzer.py:318-373`; `docs/hooks/bash-command-limitations.md` | Known limitation; protected content can remain reachable through supported Bash outside the bounded analyzer. Phase relationship: pre-existing. | Obtain explicit risk acceptance for the published boundary or add conservative denial/constrained execution for ambiguous high-risk forms. Complete G1 and live bypass/subagent evidence. |
| SEC-03 | Codex and OpenCode generated artifacts do not provide enforcement equivalent to Claude. | High | `.opencode/plugins/file-access-guard.js:1-8`; `.codex/hooks.json`; `docs/hooks/installation.md` | OpenCode launches the process without native decision translation; Codex ask and `apply_patch` mismatches are documented. Phase relationship: pre-existing. | Retain Partial classification, gather E1-E3 evidence, and implement native adapters before any Full enforcement claim. |
| SEC-04 | The reusable Unity capture package permits output-path and filename-prefix escape. | High | `packages/com.threnjen.visual-verification/Tests/CaptureGateTest.cs`; `packages/com.threnjen.visual-verification/Runtime/CaptureRunner.cs` | Configured paths are combined without canonical containment or separator restrictions. Phase relationship: pre-existing and outside the Phase 01 hook delta. | Remediate or formally accept before using the package with untrusted config or privileged CI. |
| SEC-05 | Audit-log writes do not reject symlinks or pin the final file to an approved log root. | Medium | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/file-access-guard.py:131-143` | Ordinary append can redirect redacted records to another user-writable file. | Add canonical containment, restrictive creation, no-follow handling, and link/race tests. |
| SEC-06 | Unity capture resolution, frame indices, and duration lack practical upper bounds. | Medium | `packages/com.threnjen.visual-verification/Runtime/CaptureRunner.cs` | Malicious or mistaken config can exhaust CI/developer resources. Phase relationship: pre-existing. | Add conservative validation limits and tests. |
| SEC-07 | Config cache freshness uses only mtime and size. | Medium | `.github/hooks/lib/framework.py:150-159`, `:205-227` | Same-size replacement with preserved metadata can reuse a stale security or disabled snapshot. | Include inode/change time or a small digest and test metadata-preserving replacement. |
| SEC-08 | Equal-action Bash selection ignores validated rule priority. | Low | `.github/hooks/lib/bash_analyzer.py:46-99`; `.github/hooks/scripts/file-access-guard.py:127` | Enforcement strength is unchanged, but audit guidance can name a less-specific rule. | Carry priority into matches and select by action, priority, then stable ID. |

### QA Plan Issues

| ID | Finding | Severity | QA Item | Evidence | Recommendation |
|---|---|---|---|---|---|
| QA-01 | Destination containment is incorrectly treated as fully automated. | Medium | Automated Test Coverage / F04 AC1 | The current tests omit nested symlink ancestors and the active implementation escapes. | Add the regression to the automated gate and correct the coverage claim; this is not appropriate for manual-only detection. |
| DOC-01 | Three coverage-map references drifted after manual checklist expansion. | Low | Manifest checks at coverage map lines 70-72 | Ask, subagent, and redaction map to C5, C7, and C8, not C4, C6, and C7. | Correct labels so execution evidence lands against the right item. |

Apart from these issues, the QA plan is actionable: every live item includes prerequisites, concrete steps, observable results, evidence rules, failure semantics, and safe synthetic data. It avoids manually replaying deterministic unit matrices and appropriately reserves presentation, bypass, subagent, user-scope, recovery, rollback, and limitations judgments for human/live execution.

## Risk Register

| # | Risk | Likelihood | Impact | QA Detection | Recommendation |
|---|---|---|---|---|---|
| 1 | Nested consumer destination redirects propagation outside the target root | High | High / release-blocking | No, current automated claim is false | Fix and regression-test before manual QA. |
| 2 | Combined propagated invocation exceeds the 50-ms AC on ordinary runs | Medium | High / release-blocking | Partial; current benchmark is unstable | Create reliable margin/evidence and require repeated green gate. |
| 3 | Dynamic Bash or recursive scans reach protected content | Medium | High | Partial; G1 documents but does not enforce | Obtain explicit risk acceptance or tighten policy. |
| 4 | Codex/OpenCode appear installed without equivalent blocking | High | High | Yes, E1-E3 if executed | Keep Partial; record live outcomes; implement native enforcement before promotion. |
| 5 | Live Claude bypass, subagent, exit-2, and dual-layer semantics differ from payload tests | Medium | High | Yes, C1-C8 and D2 | Execute all live Claude items only after blockers are fixed. |
| 6 | Audit log symlink redirects writes | Low | Medium | No | Harden the log writer and add filesystem tests. |
| 7 | Same-metadata config replacement leaves stale guard posture | Low | Medium | No | Strengthen cache identity and add a regression. |
| 8 | Unity capture configuration escapes or exhausts resources | Medium | High | No Phase 01 QA coverage | Remediate/accept in the package release process. |
| 9 | Equal-tier audit attribution is inaccurate | Medium | Low | Unlikely | Make priority selection deterministic. |
| 10 | Human recovery or rollback procedure fails | Low | High | Yes, F1-F2 | Execute in disposable clones after automated blockers close. |

## Blocking Items

1. **Nested destination containment escape (SEC-01 / F04 AC1)** — Hook asset propagation writes through symlinked intermediate directories outside the declared consuming-project root. **Root cause:** Feature 04 implementation and missing adversarial test coverage; the feature review verified only top-level/final-file cases. **Return to:** `@z-feature-implementer` with instruction: “Harden every Feature 04 propagation write/removal against final-target and intermediate symlink escapes, use canonical root containment and no-follow/atomic replacement where supported, and add regressions for all runtime/generated subtrees.” **Then re-run:** `@z-feature-reviewer`, security scan, `@z-feature-qa-writer` evidence refresh, and `@prod-code-review`.

2. **Unstable propagated-hook latency gate (PERF-01 / F04 AC9)** — The mandated `<50 ms` median failed in the full suite and again in a focused run, then passed three times. **Root cause:** Feature 04 implementation/performance evidence does not provide reliable margin or a stable representative gate. **Return to:** `@z-feature-implementer` with instruction: “Profile the propagated subprocess path, reduce overhead or otherwise establish repeatable representative evidence that enforces the existing `<50 ms` AC without weakening it, and add a non-flaky regression methodology.” **Then re-run:** `@z-feature-reviewer`, the full and coverage suites repeatedly in the release environment, `@z-feature-qa-writer` evidence refresh, and `@prod-code-review`.

## Recommendations

1. **Fix both Feature 04 blockers before live QA** — Source and test changes belong to `@z-feature-implementer`; the current analysis must not be used to waive them.
2. **Require adversarial containment review** — The next reviewer should test symlinked ancestors for copied assets, generated settings, plugins, the version marker, and retired-asset deletion, not only root/final-file links.
3. **Re-establish performance evidence with margin** — Record repeated full-suite and focused results on the declared macOS/Python 3.12 environment; preserve the fixed 50-ms acceptance threshold.
4. **Refresh QA and pipeline metadata** — Correct the false containment statement, stale C-item references, and `PENDING` commit columns after remediation commits exist.
5. **Resolve or accept residual High risks explicitly** — SEC-02/SEC-03 are published support/security boundaries; SEC-04 belongs to the reusable Unity package. None should be silently promoted to verified protection.
6. **Run the 16-item manual plan only after re-review returns GO** — Then execute C1-C8, D1-D2, E1-E3, F1-F2, and G1 and attach redacted evidence as required by the QA plan.
