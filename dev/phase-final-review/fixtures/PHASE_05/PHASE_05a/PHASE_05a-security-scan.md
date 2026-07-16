# security-scan: Phase 01 — Hook Foundation + File-Access Guard

## Scan Metadata

- **Repository revision:** `12d9ff3` on `phase/hook-foundation-file-access-guard`
- **Scan date:** 2026-07-14
- **Scope:** 403 tracked repository artifacts, including Phase 01 source, tests, generated deployment artifacts, configuration, scripts, dependency manifests, the Unity package, and security-relevant documentation.
- **Phase artifacts reviewed:** Phase summary, execution manifest, QA plan and coverage map, and all four feature plan/context/task/implementation/review sets.
- **Method:** Graph-first change, architecture, flow, and coverage analysis; repository inventory; manual static review; redacted current-tree secret heuristics; existing automated evidence review.
- **Exclusions:** Untracked files, caches, build outputs, vendored dependencies, binary-content analysis, repository history, and live external harness execution.

## Verdict

**BLOCKED**

One High-severity filesystem-boundary defect was introduced by the Phase 01 propagation work. Under the security-scan gate, a Phase-introduced or worsened High finding blocks release until remediated and regression-tested.

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 4 |
| Medium | 3 |
| Low | 1 |
| **Total** | **8** |

| Phase relationship | Count |
|---|---:|
| Introduced | 4 |
| Worsened | 0 |
| Pre-existing | 4 |
| Unclear | 0 |

## Coverage Matrix

| Category | Artifact classes reviewed | Method/tool | Status | Limitations |
|---|---|---|---|---|
| Secrets and credentials | Tracked text, JSON, TOML, scripts, notebooks, docs | Redacted current-tree heuristics and manual configuration review | Assessed; no supported finding | No history scan or entropy-aware scanner |
| Dependencies and supply chain | `requirements-dev.txt`, `pyproject.toml`, Unity `package.json` | Manifest review and available native tooling inventory | Partial | No lockfile vulnerability scanner; no SBOM/signature verification |
| Application attack surface and injection | Python, shell, JavaScript adapters, C# package | Graph analysis and manual data-flow review | Assessed | Semgrep and Bandit unavailable |
| Authentication, authorization, sessions | Repository tooling and hook permission decisions | Manual architecture review | Limited applicability | No network application or session service is present |
| Data protection and cryptography | Secret rules, redaction, audit records, config | Manual source/config/test evidence review | Assessed | Live runner display/log inspection not executed |
| API and input boundaries | Hook payloads, Bash input, propagation roots, Unity JSON | Graph and manual boundary tracing | Assessed | External runner payload contracts not live-tested |
| Filesystem, process, runtime safety | Propagation, hook runtime, installer, Unity capture | Manual path/process review | Findings present | ShellCheck unavailable; no additional active probing in final pass |
| Infrastructure, CI/CD, deployment | Generated harness settings, MCP/VS Code config, installers | Static configuration review | Assessed | No tracked CI workflow; live harness install checks remain unrun |
| Observability and operations | Audit scripts/logging, recovery and rollback docs | Source and QA evidence review | Findings present | Live dual-layer and recovery walkthroughs remain unrun |
| Security architecture | Guard framework, adapters, self-protection, known limitations | Graph architecture/flows and cross-file review | Findings present | Codex/OpenCode/Claude live enforcement evidence remains incomplete |

## Findings

| ID | Severity | Category | Location | Phase relationship | Evidence | Impact | Recommended remediation |
|---|---|---|---|---|---|---|---|
| SEC-01 | High | Filesystem / propagation | `scripts/propagate_master_assets.py`, `_copy_hook_assets` and `_validate_output_directory` | Introduced | The destination root itself is validated, but each copied asset is written without verifying that every intermediate destination component remains inside the declared consumer root and is not a symlink. | A crafted or stale nested destination layout can redirect propagated hook writes outside the intended repository boundary, risking overwrite of user-writable files. | Resolve and contain-check every destination immediately before writing; reject symlink ancestors; use no-follow/atomic replacement semantics; add nested-directory escape regressions for every copied runtime subtree. |
| SEC-02 | High | Application attack surface | `.github/hooks/lib/bash_analyzer.py`, `analyze_command`; `docs/hooks/bash-command-limitations.md` | Pre-existing | The analyzer intentionally does not interpret dynamic variable expansion, interpreter-mediated file access, or recursive parent-directory searches. The limitations document acknowledges these classes. | Protected content can still be reached through supported Bash execution when an operation falls outside the bounded analyzer, undermining defense-in-depth for secret files. | Move high-risk command execution into a constrained execution policy, deny ambiguous interpreter/recursive forms when protected content may be reachable, and verify the residual boundary in live bypass and subagent sessions. |
| SEC-03 | High | Authorization / harness integration | `.opencode/plugins/file-access-guard.js`; `.codex/hooks.json`; `docs/hooks/installation.md` | Pre-existing | The OpenCode adapter launches the guard but does not translate structured decisions into a native blocking result. Codex limitations for confirmation decisions and command-shaped patch input are documented. | Deny and self-protection policy is not consistently enforced outside the fully supported Claude path, creating reliable control gaps for protected-file changes or reads. | Implement runner-native adapters that enforce deny results and cover each mutation primitive; retain Partial/Not supported labels until live blocking, bypass, and subagent evidence passes. |
| SEC-04 | High | Filesystem / test tooling | `packages/com.threnjen.visual-verification/Tests/CaptureGateTest.cs`, output path construction; `CaptureRunner.cs`, capture filename write | Pre-existing | Configured output directories and filename prefixes are combined and written without canonical containment checks or separator restrictions. | A consumer-controlled capture configuration can direct screenshot or manifest writes outside the project output area and overwrite accessible files during a test run. | Require relative paths, canonicalize beneath an approved project output root, reject traversal/rooted paths and separators in filename prefixes, and add containment tests. |
| SEC-05 | Medium | Observability / filesystem | `.github/hooks/lib/framework.py`, `record_event`; `.github/hooks/scripts/file-access-guard.py`, audit path use | Introduced | Audit records are appended through ordinary path opening without rejecting symlinks or confirming the final log target remains under the intended repository log directory. | A pre-positioned log link can redirect redacted event records and corrupt another user-writable file; this is primarily an integrity and availability risk. | Pin logs to a canonical approved root, reject symlink components, create files with restrictive permissions and no-follow behavior, and cover replacement/link races in tests. |
| SEC-06 | Medium | Availability | `CaptureRunner.cs`, resolution and frame iteration | Pre-existing | Capture dimensions, frame indices, and simulation duration are accepted without practical upper bounds. | Untrusted or mistaken configuration can cause excessive memory allocation or very long test execution, affecting developer machines or CI capacity. | Enforce conservative maximum resolution, frame count/index, and duration limits with clear validation errors. |
| SEC-07 | Medium | Configuration integrity | `.github/hooks/lib/framework.py`, `_file_signature` and `load_config` | Introduced | Configuration cache freshness uses modification time and file size only. A same-size replacement with preserved metadata can reuse a stale security snapshot. | The guard can retain stale rules or a stale disabled posture beyond an intended configuration change under an adversarial or unusual filesystem update. | Include stronger identity/freshness data such as change time, inode, or a small content digest, and regression-test same-size metadata-preserving replacement. |
| SEC-08 | Low | Observability accuracy | `.github/hooks/lib/bash_analyzer.py`, rule priority; `.github/hooks/scripts/file-access-guard.py`, strongest-match selection | Introduced | Bash rule priority is validated and stored, but equal-action selection is based on encounter order rather than configured priority. | Enforcement strength is unchanged, but audit attribution and guidance can name a less-specific rule, reducing incident clarity. | Carry priority into the match result and make selection deterministic by action, priority, then stable identifier. |

## No-Finding Categories

- No supported evidence of a committed private key, well-known live token form, or direct credential assignment was found in the current tracked tree. This is not a guarantee because entropy/history scanning was unavailable.
- No tracked CI workflow or network-facing application authentication/session implementation was present to assess.
- No unsupported cryptographic implementation was found; Phase 01 does not introduce custom cryptography.
- Phase runtime code remains Python-standard-library-only and does not execute analyzed Bash content during classification.

## Cross-Cutting Risks

- The security guarantee is strongest only in Claude Code. The repository correctly documents weaker harness status, but generated artifacts can still look operational while lacking equivalent enforcement.
- Hook self-protection depends on every mutation path passing through the guarded adapter. Platform-specific tools and bounded Bash parsing remain the central bypass boundary.
- Several filesystem writers correctly validate their top-level root but do not consistently apply containment and symlink checks at the final write target. A shared safe-write helper would reduce recurrence.
- Phase 01 automated evidence is strong for deterministic payload behavior, but live bypass-permissions, subagent, dual-layer presentation, Codex, and OpenCode behavior remains unverified.

## Positive Controls

- Security-hook exceptions fail closed, with a blocking fallback when structured output fails.
- Observability failures fail open and redaction uses an allowlist rather than retaining full payloads or command bodies.
- The kill switch is confined to the protected project override, with no environment-variable activation path.
- File rules cover normalized paths, existing symlinks, credential locations, Grep scopes, and hook self-protection; Bash analysis does not execute user commands.
- Propagation validates source-hook containment, top-level output roots, referenced command assets, stable versioning, and retirement ownership.
- Current automated evidence reports 252 passing tests, 14 passing standard-library compatibility tests, 63.86% combined coverage, Python compilation, JSON validation, shell syntax, and patch-hygiene success.

## Priority Remediation Order

1. Close SEC-01 and add final-target/intermediate-symlink containment regressions before release.
2. Treat SEC-02 and SEC-03 as explicit release-risk exceptions only if product scope accepts incomplete non-Claude and dynamic-Bash enforcement; otherwise implement native/restrictive enforcement before release.
3. Contain Unity output paths (SEC-04) before using the package against untrusted branch configuration or in privileged CI.
4. Harden audit log creation and configuration cache identity (SEC-05 and SEC-07).
5. Bound Unity resource inputs and correct same-tier audit attribution (SEC-06 and SEC-08).

## Residual Risk and Exceptions

- **Unavailable security tools:** gitleaks, TruffleHog, Semgrep, Bandit, pip-audit, Safety, ShellCheck, Ruff, and mypy.
- **Incomplete dependency assurance:** No dependency-vulnerability database scan, SBOM, artifact signature verification, or hash-locked Python resolution was available.
- **Incomplete secret assurance:** Current-tree heuristics were redacted and negative, but git history, entropy, binary, and external-secret-store checks were not performed.
- **Incomplete runtime assurance:** Live Claude bypass/ask/subagent/double-layer checks and live Codex/OpenCode decision enforcement were not executed. The Phase QA plan already marks these as Not run.
- **Release gate:** The report remains BLOCKED until SEC-01 is remediated and reviewed. Pre-existing High findings SEC-02 through SEC-04 still require explicit risk acceptance or remediation before claiming broad repository security.
