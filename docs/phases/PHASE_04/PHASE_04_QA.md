# Phase 04 Release QA Plan

## Purpose

Validate the complete Hook Retirement & Cross-Platform Deployment phase as one release boundary: retired file/Bash interceptors stay absent, repository propagation reaches a verified fixed point, destination policy is correct for each supported environment, managed-copy migration preserves foreign content, supported guidance cannot recreate runtime links, and fresh sessions discover regular managed copies.

This plan covers:

- `01-interceptor-retirement`
- `02-propagation-convergence`
- `03-cross-platform-destinations`
- `04-managed-copy-reconciliation`
- `05-deployment-guidance`
- `06-runtime-verification`

## Readiness Ceiling

The current implementation is eligible only for a **partial / GO WITH CONDITIONS** result until all four platform rows have fresh live evidence. Scratch-home and simulated-platform tests do not substitute for runtime discovery on macOS, Linux, native Windows, or WSL. Any unavailable platform is recorded as `NOT RUN` and prevents a full cross-platform GO.

The author's active runtime home must not be read or mutated without an explicitly reviewed preflight inventory and authorization for that exact active home.

## Required Automated Evidence

Run from the repository root on the phase revision:

```bash
python3 -m unittest tests.test_phase04_runtime_deployment tests.test_propagate_master_assets -v
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/propagate_master_assets.py scripts/runtime_deployment.py tests/test_phase04_runtime_deployment.py
git diff --check
```

If the declared development dependencies are available, also run:

```bash
python3 -m pytest tests/hooks/test_hook_distribution_integration.py tests/test_propagate_master_assets.py tests/test_retirement_reconciliation.py tests/test_phase04_runtime_deployment.py -q
```

Do not convert an unavailable pytest runner into a pass. Record the command as `NOT RUN`, its reason, and the narrower evidence that did execute.

The required verification assets are:

- New consolidated suite: `tests/test_phase04_runtime_deployment.py`
- Shared propagation suite: `tests/test_propagate_master_assets.py`
- Shared hook suite: `tests/hooks/test_hook_distribution_integration.py`
- Shared fixed-point/retirement suite: `tests/test_retirement_reconciliation.py`

## Automated Release Scenarios

### 1. Interceptor Retirement and Surviving Defenses

1. Assert the file-access descriptor, entrypoint, policy modules, Bash analyzer, URL-exfiltration helper, guard configuration, automatic RTK rewrite script, generated registrations, and OpenCode adapter are absent.
2. Send representative direct Read and Bash payloads through the surviving hook roster and assert no retired decision, prompt, denial, or audit row is produced.
3. Exercise the shared hook framework and prompt-injection scanner behaviorally, including injection blocking/redaction and the deterministic corpus benchmark.
4. Inspect Claude, Codex, and OpenCode generated wiring and assert only the expected scanner, audit, and notification integrations remain.
5. Execute an explicitly prefixed RTK command and assert RTK remains usable; separately assert no automatic rewrite integration remains.
6. Verify retired-asset cleanup removes only ownership-proven regular assets or repository-targeting generated links, preserves same-named foreign entries, and is idempotent.
7. Verify active security documentation states the reduced posture and does not claim injection scanning replaces file/Bash authorization.

### 2. Propagation Convergence and Mutation Gates

1. Exercise a multi-pass repository change and require an immediate zero-change verification pass before convergence succeeds.
2. Reject zero, negative, malformed, and excessive convergence bounds; fail closed on exceptions or malformed result counters.
3. Prove convergence failure or bound exhaustion occurs before destination resolution, preflight, or runtime writes.
4. Complete preflight for the full intended harness set before the first copy; reject escaping homes, symlink/junction parents, non-directory parent components, missing ownership evidence, and unresolved collisions.
5. Prove one harness failure preserves successful harness results and suppresses destructive reconciliation for the failed harness only.
6. Verify default one-pass callers remain compatible while deployment-capable CLI flow uses bounded convergence.
7. Verify watcher output requires a restart after propagator changes before migration or release verification.
8. Require structured, path-safe results for propagation passes, changes, preflight categories, per-harness outcomes, and reconciliation skips.

### 3. Cross-Platform Destination Policy

1. Verify the exact eight-class generated roster and source roots; do not invent absent commands, profiles, hooks, or settings outputs.
2. Verify Claude defaults and `CLAUDE_CONFIG_DIR` relocation for agents, commands, skills, and learnings.
3. Verify `CODEX_HOME` relocates only Codex-owned assets, requires an existing directory, and does not relocate the shared skills root.
4. Verify `OPENCODE_CONFIG_DIR` relocates only documented config-owned assets while skills remain at their documented user location.
5. Verify macOS/Linux destinations remain within the active POSIX home and native Windows destinations remain within the active profile.
6. Verify native Windows and WSL classification is mutually exclusive; WSL must not deploy into mounted Windows profiles, and native Windows must not imply a WSL deployment.
7. Reject relative, empty, NUL-bearing, cross-environment, outside-home, symlink-parent, junction-parent, and unsupported-platform inputs with category-only diagnostics.
8. Preserve the destination leaf unresolved for downstream ownership classification while validating every existing parent.

### 4. Managed-Copy Migration and Reconciliation

1. Use scratch homes containing absent destinations, managed regular copies, stale owned entries, live repository links, dangling repository links, whole-root links, foreign files/directories/links, foreign metadata, marker quotations, and unchanged assets.
2. Stage and hash-verify every record for a harness before mutation. On staging failure, assert the original destination remains and pruning is skipped.
3. Replace only positively owned repository links/junctions or managed regular entries. Never traverse a link target for deletion.
4. Convert whole-root and per-entry repository links into regular files/directories with fresh generated content.
5. Preserve foreign content, identical-but-unowned files, foreign links, foreign metadata, and files merely quoting ownership markers as collisions.
6. Prune only positively owned stale entries, including successful empty rosters, and recheck identity immediately before deletion.
7. Simulate locked/replacement failure and assert backup restoration, failure classification, and skipped pruning.
8. Run the reviewed deployment twice and require a fixed point: zero copy, replace, or remove mutations on the second run.
9. Verify all expected destinations are fresh regular copies and no managed destination is a symlink or junction into the repository.

### 5. Deployment Guidance

1. Verify Evangelize requires convergence, reviewed inventory, watcher restart, managed-copy deployment, per-harness result inspection, and fresh-session discovery.
2. Verify Claude, Codex, and OpenCode Evangelize variants exactly match the corrected source renderer.
3. Scan every supported setup and troubleshooting surface for operational `ln -s`, symbolic-link, or `mklink` recipes and stale instructions to validate/repair runtime links.
4. Run negative documentation fixtures for POSIX, PowerShell, and Windows runtime-link recipes.
5. Keep historical and hostile-link security discussion allowed only when explicitly non-operational.
6. Verify explicit RTK guidance remains available and does not imply automatic rewriting.
7. Verify native Windows and WSL are documented as separate runs and unavailable environments are `NOT RUN`.

### 6. End-to-End Runtime Orchestration

1. First invoke `--runtime-deploy --active-home <scratch-home>` without a reviewed digest and require a home-relative, content-bound inventory plus a review-required exit with zero writes.
2. Bind the reviewed digest to the exact active home and generated source state. A wrong digest, cross-home replay, or inventory drift must abort before mutation.
3. Require watcher-restart confirmation, converged repository output, successful preflight, reviewed inventory, immediate re-inventory, managed-copy deployment, reconciliation, and freshness verification in that order.
4. Verify Claude, Codex, and OpenCode succeed independently in a scratch home, foreign entries survive, failures remain structured, and partial harness failure cannot report GO.
5. Compare inventory classifications and generated rosters from the current run. The historical 113-link count is context only and must never be used as the expected inventory.

## Manual QA Procedure

### A. Safe Preflight

1. Restart any long-running propagation watcher.
2. Record the exact repository revision, interpreter, RTK version, platform, active-home identity, and harness versions.
3. Run all automated checks against temporary repositories and scratch homes first.
4. Run the runtime deployment command without a reviewed digest against the intended active home. Capture its home-relative inventory and digest; confirm no runtime mutation occurred.
5. Review every inventory row and classify planned replacement, obsolete owned removal, unchanged managed copy, collision, failure, and preserved foreign entry.
6. Compare the fresh inventory to the current generated platform roster. Do not compare it to the historical total of 113 links.
7. Obtain explicit authorization for the exact reviewed active home and digest before proceeding.

### B. Authorized Current-Environment Migration

1. Re-run with the reviewed inventory digest and watcher-restart confirmation.
2. If the immediate inventory differs, stop and review the new inventory; do not reuse the old authorization.
3. Inspect per-harness outcomes. A harness failure must preserve its prior usable state and skip destructive reconciliation; successful harnesses may remain installed.
4. Confirm every expected managed destination is a regular file or directory, content matches the generated source, and no managed path links or junctions into the repository.
5. Confirm all recorded foreign files, directories, links, package/plugin links, and unrelated Git links remain unchanged.
6. Run the same reviewed deployment again and require a two-run fixed point with zero mutations.

### C. Fresh-Session Runtime Matrix

Run these independently. Evidence from one environment cannot satisfy another.

| Environment | Required run | Required evidence |
|---|---|---|
| macOS | Native macOS active user | Fresh Claude, Codex, and OpenCode processes discover expected assets from regular managed copies; no repository links; copy freshness verified. |
| Linux | Native Linux active user | Same checks against the Linux home and documented relocation variables. |
| Native Windows | Native Windows user profile, without Developer Mode/admin assumptions | Same checks plus live junction/reparse and locked-file behavior where practical. |
| WSL | Active WSL distribution and Linux home | Same checks inside WSL; no deployment into the mounted Windows profile and no inference from the native Windows run. |

For each environment record `PASS`, `FAIL`, or `NOT RUN`, the reason, OS/runtime versions, fresh-session invocation, harness discovery result, regular-copy/link inspection, collision result, and artifact locations. Any `NOT RUN` or `FAIL` blocks a full GO.

## Evidence Record

Attach or link:

- exact revision and dirty-state note;
- automated commands and pass/fail/skip counts;
- fixed-point propagation counters;
- reviewed inventory digest and redacted/home-relative inventory;
- explicit authorization record for any live-home mutation;
- first- and second-run structured deployment results;
- per-harness collision, failure, and skipped-reconciliation results;
- regular-copy freshness and repository-link absence checks;
- explicit RTK invocation result;
- scanner/framework behavioral result;
- separate macOS, Linux, native Windows, and WSL fresh-session evidence.

Do not attach secret values, absolute home contents, or unredacted sensitive paths.

## Release Decision Rules

- **GO:** all required automated suites pass, reviewed live migration succeeds, the second run is a fixed point, all foreign content is preserved, retired interceptors remain absent, scanner/framework and explicit RTK survive, and all four fresh-session platform rows pass.
- **GO WITH CONDITIONS / PARTIAL:** automated and available live checks pass, but one or more required platform rows are `NOT RUN`, pytest is runner-constrained, or another explicitly bounded evidence condition remains. List each condition.
- **NO-GO:** any unreviewed live-home mutation; convergence or inventory-gate bypass; foreign-content loss; repository link remaining in managed output; stale or linked managed copy; unresolved Critical/High safety defect; failed fixed-point check; retired interceptor restored; scanner/framework regression; or any required platform row fails.

