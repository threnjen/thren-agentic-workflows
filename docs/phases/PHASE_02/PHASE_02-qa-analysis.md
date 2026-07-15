# QA Readiness Analysis: Phase 02 Prompt-Injection Defense

**Date:** 2026-07-15  
**Analyst:** prod-code-review (automated)  
**Mode:** Standard (`All verdicts Approved: NO`)  
**Verdict:** NO-GO  
**Security gate:** BLOCKED — 0 Critical, 7 High, 5 Medium, 1 Low; 3 High findings introduced by Phase 02  
**Visual verification:** Not applicable; this is not a Unity project

## Readiness Verdict

**NO-GO.** Phase 02 is not ready for release or promotion to manual release sign-off. The full-codebase security scan found three Phase 02-introduced High-severity bypasses that allow high-tier indirect-injection content to remain model-visible or bypass scanning deterministically. All three are separate from the two risks the user accepted. The accepted Codex coverage limitation remains `Partial`, PERF-01 remains a failed prerequisite, and every live/manual harness check remains `NOT RUN`.

The phase has substantial positive automated evidence: the final-review checkout produced `384 passed`, and the deterministic corpus benchmark reproduced `19` true positives with `0` misses, `0` false positives, and `0` high-tier false positives. Those results do not exercise or negate the three security-gate bypasses.

## Executive Summary

All four feature bundles, their implementation and review records, the execution manifest, consolidated QA plan, coverage map, and security scan are present. Every feature review returned **Approved with Reservations**. The final security scan supersedes those feature-level approvals for release readiness because it exercised adversarial boundaries that the earlier tests and reviews did not cover.

Release is blocked by:

1. **Untrusted structured keys survive a nominal block.** Built-in structured output redaction recursively replaces values while preserving attacker-controlled mapping keys. A high-tier directive in a key can therefore remain in `updatedToolOutput` after the scanner reports `block`.
2. **Configured work limits become deterministic bypasses.** Content beyond the 262,144-byte scan cap and encoded candidates after candidate 32 are not assessed, yet the entrypoint can return the complete raw output with only a warning.
3. **Mutable directory allowlists bypass the scanner.** Entire recursive directories are trusted by path, but those directories are not protected by the same write-deny boundary as hook assets. New or modified malicious content under an allowlisted directory can be returned without scanning.

The accepted-risk record is preserved exactly:

- Codex 0.144.4 covers only Bash, `apply_patch`, and MCP PostToolUse results. User approval permits proceeding with this known residual gap but does not promote Codex beyond `Partial` or supply missing live evidence.
- PERF-01 has reproduced at approximately 117–383 ms against a fixed 50 ms threshold. User approval accepts the risk but does not convert the failed prerequisite into a pass.
- The current checkout happened to pass the full suite and three focused latency reruns. That warm-run result demonstrates variability; it does not erase the recorded failing release evidence or establish stable margin below the fixed threshold.

## Scope and Evidence Reviewed

### Feature bundles

| Feature | Implementation | Review verdict | Release assessment |
|---|---|---|---|
| `05-injection-scanner` | Present | Approved with Reservations | Blocked by P2-SEC-01, P2-SEC-02, and P2-SEC-03 |
| `05-webfetch-exfiltration-guard` | Present | Approved with Reservations | Automated deterministic URL paths are green; live WebFetch/Bash behavior is not run |
| `06-injection-pattern-corpus` | Present | Approved with Reservations | Finite corpus benchmark is green; it does not cover scanner-boundary bypasses |
| `07-multi-harness-integration` | Present | Approved with Reservations | Blocked by redaction bypass; Codex remains Partial; all live harness checks are not run |

### Consolidated artifacts

| Artifact | Path | Assessment |
|---|---|---|
| Phase summary | `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Defines hard-block, bounded scanning, allowlist, parity, propagation, and live-QA success criteria |
| Execution manifest | `dev/feature/phase-02-prompt-injection-defense-execution-manifest.md` | Verification assets are represented in the QA plan and coverage map |
| QA plan | `docs/phases/PHASE_02/PHASE_02_QA.md` | Actionable and honest about accepted risks and `NOT RUN` evidence |
| Coverage map | `docs/phases/PHASE_02/PHASE_02_QA_COVERAGE_MAP.md` | Maps feature ACs and manifest checks; correctly keeps accepted risks open |
| Security scan | `docs/phases/PHASE_02/PHASE_02-security-scan.md` | `BLOCKED`; three Phase 02-introduced High findings and ten pre-existing repository risks |

## Graph and Change-Risk Assessment

The repository knowledge graph analyzed the Phase 02 delta against `main`:

- 67 changed files and 161 changed functions/classes.
- Overall change risk score 0.60.
- 82 inferred structural test gaps.
- No affected execution flows were inferred, even though the phase changes shared hook entrypoints and harness adapters.
- Two-hop blast radius was rated **high**, with 29 impacted nodes across 8 additional files.
- The graph found no direct test edge for `_validate_nested_output_directory`; behavior is exercised indirectly through propagation tests, so this graph gap is not independently classified as a blocker.

The absence of inferred flows is a graph-model limitation, not proof that runtime flows are unaffected. The security scan appropriately supplemented graph evidence with direct source tracing and targeted probes.

## Validation Results

| Gate | Result | Assessment |
|---|---|---|
| Fresh full pytest suite | **Pass:** 384 passed, 2 subtests passed | Strong functional signal, but does not cover the introduced High bypasses |
| Focused PERF-01 reruns | **Pass:** 3 consecutive focused runs | Insufficient to overturn recorded 117–383 ms failures; no stable margin is established |
| Injection benchmark | **Pass:** 19 TP, 0 misses, 0 FP, 0 high-tier FP | Green for the finite production corpus and fixtures |
| Recorded coverage gate | **Pass:** 71.42% with two fixed timing assertions deselected | Above the required 50% threshold; deselection is not timing-pass evidence |
| Recorded full-suite gate | **Fail:** 383 passed, 1 failed at 135.42 ms | PERF-01 remains failed and risk accepted |
| Security scan | **BLOCKED** | Three Phase 02-introduced High findings block release |
| Live/manual QA | **NOT RUN** | Claude, Codex, OpenCode, URL, redaction, recovery, propagation, and symlink checks remain unobserved live |

## Blocking Findings

### P2-SEC-01 — Attacker-controlled structured keys survive block redaction

**Severity:** High  
**Phase relationship:** Introduced by Phase 02  
**Locations:** `.github/hooks/lib/framework.py:222-237`; `.github/hooks/scripts/injection-scanner.py:89-102`; `tests/hooks/test_injection_scanner.py:316-345`

`redact_tool_output` preserves every mapping key and recursively redacts only values. The existing structured-output test explicitly requires the redacted result to retain the original key set. The security probe demonstrated that a synthetic high-tier directive placed in a mapping key remains in the replacement object after the scanner returns `block`.

This violates the phase requirement that high-confidence output be suppressed before model context and invalidates the redaction guarantee for built-in structured results. It also leaves runner-schema rejection as a secondary risk when arbitrary source shapes are emitted as replacement output.

**Required before re-review:** Replace blocked output with a fixed, runner-valid redacted shape that retains no untrusted keys, then add emitted-payload boundary regressions for keys, nested keys, values, lists, and mixed primitive containers for built-in and MCP paths.

### P2-SEC-02 — Scan-byte and encoded-candidate limits permit deterministic bypass

**Severity:** High  
**Phase relationship:** Introduced by Phase 02  
**Locations:** `.github/hooks/lib/injection_scanner.py:58-64,191-213,256-296`; `.github/hooks/scripts/injection-scanner.py:55-70,104-116`; `.github/hooks/config/injection-allowlist.json:7-10`

The scanner assesses at most 262,144 bytes and the first 32 encoded candidates. When no match exists in the assessed subset, the entrypoint emits a warning while leaving the complete raw output intact. A high-tier instruction after the byte cap or in encoded candidate 33 can therefore reach model context without assessment.

This is a configured deterministic bypass, not an unavoidable linguistic evasion of a regex corpus. The phase's truncation notice does not provide protection while the unassessed content remains model-visible.

**Required before re-review:** Conservatively block or replace output whenever content remains unassessed, or emit only the fully assessed prefix with a fixed marker. Add exact cap+1 and candidate-limit+1 regressions at the serialized runner-output boundary.

### P2-SEC-03 — Recursive path allowlists trust mutable content

**Severity:** High  
**Phase relationship:** Introduced by Phase 02  
**Locations:** `.github/hooks/lib/injection_scanner.py:65-69,299-343`; `.github/hooks/scripts/injection-scanner.py:73-80`; `.github/hooks/config/injection-allowlist.json:2-6`; `.github/hooks/config/file-access-rules.json:267-282`

The allowlist recursively trusts `tests/hooks/fixtures/injection` and `docs/inspiration` based on their resolved path. The file-access self-protection rules protect hook assets and harness wiring but not those two content roots. Any new or modified file below an allowlisted directory bypasses scanning on subsequent Read/Grep output.

This turns repository location into an unauthenticated trust decision and conflicts with the phase's human-only allowlist escape-hatch posture.

**Required before re-review:** Remove mutable directory-wide bypasses, use reviewed file digests, or place every allowlisted source under an enforced immutable/write-deny boundary with integrity validation. Add create/modify-then-read adversarial regressions.

## Additional Release Risks

These do not replace the three Phase 02 blockers. They remain part of the release-risk decision after those blockers are closed.

| ID | Severity | Relationship | Risk |
|---|---|---|---|
| REPO-SEC-04 | High | Pre-existing | Bounded Bash analysis cannot cover interpreter-mediated, dynamic, recursive-parent, alias, function, sourced-code, and expansion paths |
| REPO-SEC-05 | High | Pre-existing | OpenCode/Codex PreToolUse enforcement is not equivalent to the verified Claude path |
| REPO-SEC-06 | High | Pre-existing | Non-hook propagation destinations still lack uniform ancestor-symlink containment |
| REPO-SEC-07 | High | Pre-existing | Unity capture paths can escape their intended output root |
| REPO-SEC-08 through REPO-SEC-12 | Medium | Pre-existing | Audit-file links, weak config cache identity, Unity resource bounds, supply-chain pinning, and PERF-01 |
| REPO-SEC-13 | Low | Pre-existing | Audit files rely on process umask rather than explicit owner-only permissions |

## Manual QA Readiness

The consolidated QA plan is detailed and appropriately distinguishes automated, live, and accepted-risk evidence. It is not complete release evidence:

- Claude live suppression, warning, no-retry, Task/MCP, truncation, allowlist, and kill-switch checks are `NOT RUN`.
- WebFetch deny/ask/allow and Bash curl/wget parity checks are `NOT RUN`.
- Cross-surface sentinel redaction and human recovery are `NOT RUN`.
- Codex supported-subset checks and OpenCode adapter loading/replacement checks are `NOT RUN`.
- Propagation preservation, self-protection, manual containment, and release-environment behavior checks are `NOT RUN`.

Risk acceptance is not a substitute for execution evidence. Manual QA should not be used to waive the three deterministic security failures; it should run after remediation, feature re-review, and a passing security scan.

## Risk Register

| # | Risk | Likelihood | Impact | Current evidence | Disposition |
|---|---|---|---|---|---|
| 1 | High-tier content survives in structured mapping keys | High | High | Targeted security probe; source and test contract confirm key preservation | Release blocker |
| 2 | Padding or candidate exhaustion places high-tier content outside assessed bounds | High | High | Targeted cap and candidate-limit probes | Release blocker |
| 3 | Mutable allowlisted directory content bypasses scanning | Medium | High | Source-path policy and protection mismatch | Release blocker |
| 4 | Codex misses Read/Grep/WebFetch/WebSearch/Task successful outputs | High | High | Contract/source evidence; no live evidence | Accepted residual risk; remain Partial |
| 5 | Security-hook latency exceeds the fixed 50 ms gate | Medium | High | Historical 117–383 ms failures; current warm passes | Accepted failed prerequisite; remain open |
| 6 | Live runner output or UI behavior differs from automated payload tests | Medium | High | All harness sessions not run | Execute after blockers close |
| 7 | Dynamic Bash paths bypass deterministic analysis | Medium | High | Published limitation and security finding | Remediate or explicitly accept separately |
| 8 | Propagation/logging/capture filesystem paths retain pre-existing write risks | Medium | High | Full-codebase security scan | Address in release-risk program |

## Required Re-entry Sequence

1. Return P2-SEC-01 through P2-SEC-03 to the responsible feature implementer without weakening the phase ACs, scan limits, or live-output expectations.
2. Run a full feature review of the remediated scanner and harness integration, including adversarial serialized-output cases.
3. Re-run the full-codebase security scan. A release candidate must contain no Phase 02-introduced or worsened Critical/High finding.
4. Refresh the consolidated QA plan and coverage map if implementation or evidence requirements changed.
5. Re-run full, coverage, benchmark, propagation, and stable PERF-01 evidence from the release checkout. Preserve PERF-01 as failed until the fixed threshold is reliably met or a future release authority records a distinct disposition.
6. Re-run prod-code-review. Only after a GO or GO WITH CONDITIONS should the disposable live/manual QA checklist be executed for release sign-off.

## Final Recommendation

Do not release Phase 02 and do not treat the user's Codex/PERF approvals as approval of the three security findings. The next production review should require a passing rerun of the full-codebase security gate, direct regressions for all three bypasses, and unchanged honest labeling for Codex, PERF-01, and live/manual evidence.

