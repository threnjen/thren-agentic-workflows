# Phase 04 Diff-Scoped Security Scan

## Executive Summary

**Phase:** PHASE_04 Hook Retirement & Cross-Platform Deployment  
**Diff range:** `fd0f1a0c1a30f78c8217e32e953606932b9dd5f2..HEAD`  
**Verdict:** **Pass with Conditions**  
**Files audited:** 66 changed paths  
**Severity totals:** Critical 0, High 0, Medium 2, Low 0

The phase adds no network listener, privileged operation, dependency, credential, or shell-command execution surface. Destination overrides are restricted to absolute paths beneath the active home; generated source trees reject links and special files; replacement is staged and content-verified; foreign entries fail closed; link deletion acts on the link entry rather than its target; inventory approval is bound to the selected home and rechecked before writes; and errors expose categories rather than sensitive paths.

The release conditions are the intentional retirement of project-level file/Bash access enforcement, a residual concurrent-filesystem race around path and identity checks, and the absence of live native-platform evidence. These do not demonstrate a Critical or High vulnerability in the diff, but they prevent an unconditional security pass.

## Scope and Method

- Reviewed only files changed in the requested baseline-to-HEAD diff.
- Used the code-review graph first. It reported medium aggregate change risk; the two deployment modules have a high two-hop blast radius (348 impacted nodes across 26 additional files), while no stored execution flow was mapped to the new CLI path.
- Examined the complete new `scripts/runtime_deployment.py`, all Phase 04 additions to `scripts/propagate_master_assets.py`, hook-registration removals, relevant phase/review records, and security-sensitive tests.
- Checked added diff content for common embedded credential/private-key forms without printing candidate values; no match was found.
- Ran `python3 -m unittest tests.test_phase04_runtime_deployment tests.test_propagate_master_assets`: 101 tests passed.

## Findings by Category

### Filesystem Safety and TOCTOU

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `scripts/runtime_deployment.py` | L224-L246, L652-L673, L742-L769, L772-L850 | Medium | Containment and ownership decisions are not atomic with mutation | Parent-link checks, destination identity checks, backup-name availability checks, and prune identity checks occur before later `mkdir`, `os.replace`, or removal operations. A process able to mutate the same home tree concurrently can exchange a checked parent or entry during that window, potentially redirecting a write outside the declared home or causing replacement/removal of content that was not the object previously classified. The implementation substantially narrows the windows and fails closed for stable-state collisions, but path-based rechecks do not establish an atomic filesystem boundary. |

### Access Control and Defense in Depth

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 2 | `.claude/settings.json`, `.codex/hooks.json`, `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/lib/file_access.py`, `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/lib/url_exfiltration.py`, `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` | Structural deletions; summary L109-L110 | Medium | Project-level file and Bash access enforcement is intentionally retired | Direct and Bash-mediated reads of sensitive paths are no longer denied by this repository's hook layer, and the guard-specific URL-exfiltration checks are removed with it. The surviving injection scanner is correctly documented as not being an authorization replacement. This is an explicit phase objective and disclosed risk, but deployments now depend on harness-native controls, OS permissions, operator review, and secret-management hygiene for that boundary. |

### Secrets, Injection, and Information Exposure

No finding. No credential material was identified in added diff content. The deployment CLI emits home-relative destinations and a digest rather than the active-home path. It does not interpolate destination data into a shell, evaluate generated content, or invoke subprocesses.

### Ownership, Links, and Destructive Reconciliation

No additional finding. Regular entries require current metadata fingerprints or exact generated markers; repository links require targets inside generated roots; foreign metadata and entries become collisions; stages are manifest-verified; and harness failures suppress pruning. Predictable backup/stage names are collision-checked, subject to the concurrent race recorded above.

### Cryptography and Approval Binding

No finding. SHA-256 is used for content identity and inventory approval binding rather than password storage. The reviewed inventory digest includes the absolute active-home identity without disclosing it, and an immediate re-inventory detects stable-state drift before mutation.

### Dependency and Supply-Chain Changes

No finding. The diff adds no dependency manifest or fetched runtime package. Deployment sources remain repository-generated trees, and nested links or special source entries are rejected during manifest construction.

### Error Handling and Fail-Closed Behavior

No finding. Public failures are reduced to content-safe categories; malformed overrides, non-native destinations, linked homes/parents, source links, foreign collisions, staging mismatches, and replacement failures stop or isolate mutation. Partial harness results are non-GO.

## Cross-Cutting Observations

- The security model deliberately shifts from preventive hook authorization toward explicit operator review plus ownership-safe managed copies. Documentation reflects this reduced posture and does not claim that prompt-injection scanning restores the retired boundary.
- The most security-sensitive behavior is local filesystem reconciliation, not remote input handling. Stable-state cases are well covered; remaining risk is concentrated in concurrent mutation and native platform semantics.
- The graph cannot infer test edges for much of the new code, but direct scratch-home tests exercise path containment, foreign collisions, metadata tampering, link migration, replacement recovery, inventory replay prevention, and fail-closed convergence.

## Conditions and Priority Order

1. **Release condition:** Treat live deployment as an explicitly reviewed local operation, and do not describe the surviving scanner as file/Bash authorization.
2. **Important hardening:** Resolve the concurrent filesystem race finding before relying on active-home containment against an adversary who can mutate the destination tree during deployment.
3. **Platform evidence:** Keep readiness below full cross-platform GO until native Windows junction/sharing behavior and fresh-session macOS, Linux, Windows, and WSL results are recorded.

## Categories Not Assessable at Diff Scope

- Native Windows reparse-point, junction, ACL, sharing-violation, and atomic replacement behavior on a real Windows filesystem.
- Live WSL separation and runtime discovery inside an actual distribution.
- Live macOS/Linux runtime loading, user-home permissions, and interaction with concurrently running harness processes.
- Effectiveness of external harness-native authorization, sandboxing, endpoint protection, and organizational secret controls after guard retirement.
- Network, API authentication/authorization, session management, database security, and transport security: the changed diff introduces no such runtime surface.
- Third-party vulnerability posture beyond the diff: no dependency manifests changed, so repository-wide transitive dependency analysis was outside scope.

## Final Verdict

**Pass with Conditions.** No Critical or High finding was identified. The two Medium conditions and unavailable live platform evidence must remain visible to the final production-readiness decision.
