# Phase 4: Hook Retirement & Cross-Platform Deployment

**Status**: Planned
**Depends on**: Phase 01
**Estimated complexity**: Large
**Cross-references**: `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md`, `.github/learnings/cross-phase-decisions.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`, `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`, `docs/phases/PHASE_07/PHASE_07_SUMMARY.md`

## What's New

Ordinary work stops passing through two branch-added interceptors. The file-access guard and its Bash-command analysis are removed, eliminating the false denials observed during search and Git operations. Automatic RTK command rewriting is also removed. RTK itself remains installed and available for explicit use.

Propagation becomes a complete deployment workflow. After the Claude, Codex, and OpenCode repository outputs reach a stable state, the propagator copies them into the active user's runtime directories. Existing repository-managed links and junctions are replaced with real files and directories on macOS, Linux, native Windows, and WSL.

## Objective

Remove the file-access and automatic RTK-rewrite hooks without removing RTK or the shared hook framework, then make generated agents, commands, skills, profiles, and supporting assets available through safe cross-platform user-global copies.

## Scope

### In Scope

- Retire the file-access guard, including direct file-tool enforcement, Bash-command analysis, guard policy configuration, hook registration, generated wiring, tests, and active documentation claims.
- Retire automatic Bash rewriting through `rtk-rewrite.sh`, including its hook registration and rewrite-specific tests.
- Preserve the RTK executable, explicit RTK usage, and repository instructions for manually prefixed RTK commands.
- Preserve the shared hook framework and prompt-injection defense.
- Extend `scripts/propagate_master_assets.py` with a user-global deployment stage that runs only after repository propagation reaches a stable result.
- Deploy managed copies for Claude, Codex, and OpenCode on macOS, Linux, native Windows, and WSL.
- Treat WSL as an independent Linux environment with its own home directory.
- Migrate every runtime symlink, directory link, or Windows junction whose target belongs to this repository's generated outputs.
- Remove repository-owned dangling links when no generated output replaces them.
- Reconcile managed copies when generated artifacts are renamed or retired.
- Update the Evangelize source agent and its generated variants so they invoke or verify managed-copy deployment and never create or repair runtime links.
- Replace symlink-oriented runtime setup guidance with copy-deployment guidance.
- Correct guard-friction, deployment, and hook-composition records to match the resulting system.

### Out of Scope

- Removing or uninstalling RTK.
- Removing instructions that recommend explicit RTK-prefixed commands.
- Removing the shared hook framework or prompt-injection scanner.
- Deploying from native Windows into WSL, from WSL into native Windows, or across WSL distributions in one run.
- Automatically discovering and modifying other users' home directories.
- Plugin packaging or public distribution.
- Project-local runtime deployment.
- Removing unrelated application-managed links, package-manager links, plugin-cache links, debug pointers, or Git hook links.
- Moving Phase 01 or Phase 07 status lines. Their structural reconciliation belongs to `project-planner`.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Interceptor retirement | Remove file-access protection and automatic RTK rewriting while preserving RTK and the shared framework. | Hook retirement |
| 2 | Stable post-propagation deployment | Begin user deployment only after all repository-generated outputs converge successfully. | Deployment orchestration |
| 3 | Cross-platform managed copies | Copy each harness's generated assets into documented user-global locations on macOS, Linux, Windows, and WSL. | Platform deployment |
| 4 | Safe link migration | Replace repository-managed links and junctions with copies without following links or touching foreign content. | Migration and reconciliation |
| 5 | Evangelize and guidance correction | Ensure no supported workflow recreates runtime symlinks or junctions. | Agent and documentation alignment |
| 6 | Verified runtime state | Prove expected assets load from regular files and that no managed user-global path links back into the repository. | Integration QA and records |

## Technical Context

### Independent interceptor history

The file-access guard and automatic RTK rewriting are separate branch-added systems:

- Commit `8e2a498` introduced the file-access guard, Bash analyzer, path-policy implementation, and rule configuration in Phase 01.
- Commit `370fcba` introduced `rtk-rewrite.sh` and its tests during Phase Final Review work.
- Neither integration exists on `main`.
- RTK is an external tool and is not owned by either hook.

Removing both hook integrations does not remove RTK. Explicitly prefixed RTK commands remain valid.

The guard retirement unit includes its entrypoint, Bash analyzer, file-access policy implementation, URL-exfiltration logic used only by the guard, rule and override configuration, hook descriptor, generated registrations, and dedicated tests. Mixed scanner and propagation tests require surgical updates because some use guard assets as fixtures without testing guard behavior.

### Propagation and deployment ordering

Repository outputs remain the first deployment boundary:

1. Source-of-truth assets propagate into `claude/`, `codex/`, and `opencode/`.
2. Propagation repeats or verifies until an immediate verification pass reports no remaining changes.
3. User-global destination preflight validates active-home paths, ownership evidence, collisions, and required parent directories.
4. Managed copies are deployed from the generated platform outputs.
5. Stale managed copies and repository-owned links are reconciled.
6. Runtime loading is verified from a fresh session where required.

No user-global mutation begins if repository propagation fails or cannot reach a bounded fixed point.

A failure in one harness is reported as a partial deployment. It must not trigger pruning in the failed harness or roll back successfully verified copies in another harness.

### Platform destination behavior

- **Claude**: honor `CLAUDE_CONFIG_DIR`; otherwise use the active user's `.claude` directory. Deploy generated agents, commands, skills, and repository-managed learning assets.
- **Codex**: honor `CODEX_HOME` for Codex-owned runtime assets. Deploy skills to the documented active-user skill location and reconcile legacy repository links only after replacement loading is verified.
- **OpenCode**: honor `OPENCODE_CONFIG_DIR` for documented asset classes. Skills use their documented user location unless the runtime explicitly supports a configured alternative.
- **Linux**: deploy within the active Linux user's home.
- **Native Windows**: deploy within the active Windows user profile without requiring Developer Mode or administrator privileges.
- **WSL**: deploy within the active distribution's Linux home. Native Windows and WSL require separate runs.

Suggested implementation shape, to be verified by Feature Decomposer against current code and tests: stage each replacement beside its destination, replace only after the complete asset is ready, and report Windows sharing violations without deleting the existing destination.

### Ownership and collision contract

The migration may replace a link or junction when its resolved target lies inside this repository's generated roots, including dangling links whose recorded target belongs there.

Regular files and directories may be overwritten or pruned only when repository ownership is proven through generated markers or equivalent deployment metadata. Foreign files, foreign links, and unmarked directories are preserved and reported as collisions.

Whole-directory links are unlinked without traversing them, replaced by real directories, and populated from the corresponding generated root. Per-file and per-skill links become regular files or directories.

The author-machine baseline contains 113 repository-targeting runtime links: 41 Claude, 70 Codex, and 2 OpenCode; 12 are dangling. The implementation must take a fresh inventory rather than assuming these counts remain unchanged.

### Evangelize and documentation

`.github/agents/evangelize.agent.md` requires runtime symlink creation, repair, and validation. It also contains platform-specific link commands and invokes setup guides that recreate links.

Evangelize must instead require successful repository propagation followed by managed-copy deployment. Its readiness checks must verify regular-file freshness, expected roster coverage, collision results, and runtime discovery. Generated Claude, Codex, and OpenCode Evangelize variants must be regenerated from the corrected source.

Symlink-oriented setup documents, runtime examples, generated learnings, and readiness instructions must be reconciled so no supported asset-deployment path recreates the retired model. Security documentation may continue discussing symlink attacks and containment where technically relevant.

### Test impact

- Guard-only tests and automatic RTK-rewrite tests are removed with their integrations.
- Mixed injection-scanner, hook-distribution, and propagation tests are updated without weakening the behavior they independently protect.
- Propagation tests must prove that user deployment cannot start from failed or non-converged generated outputs.
- Migration tests require scratch homes covering regular files, managed files, foreign files, live repository links, dangling repository links, foreign links, symlinked parents, Windows junction equivalents, and locked-file failures.
- Evangelize and documentation regression checks must fail on runtime link-creation instructions.
- Platform-path tests must cover defaults and supported relocation variables.
- Live QA is required on macOS, Linux, native Windows, and WSL. A platform that is unavailable is recorded as `NOT RUN` and prevents a full cross-platform GO verdict.
- Automated tests and manual QA must never migrate the author's live home without an explicit preflight and reviewed inventory.

## Dependencies & Risks

- **Dependency — project-level reconciliation**: retiring the guard changes Phase 01's headline capability and removes several Phase 07 remediation items. Mitigation: return those structural changes to `project-planner`.
- **Risk — protected-file enforcement disappears**: direct and Bash-mediated secret-file access will no longer be blocked by this project. Mitigation: state the reduced security posture explicitly; do not present prompt-injection defense as a replacement.
- **Risk — unprefixed commands no longer receive automatic RTK rewriting**: token optimization becomes instruction- and user-driven. Mitigation: preserve explicit RTK guidance and verify manual RTK use.
- **Risk — user content is overwritten**: global runtime directories may contain hand-authored assets. Mitigation: require ownership evidence and preserve every foreign collision.
- **Risk — migration follows a hostile or stale link**: following it could read or modify content outside the repository. Mitigation: classify the link itself, never traverse it for deletion, and replace only repository-targeting links.
- **Risk — generated outputs are copied before convergence**: a reclassification may require multiple propagation passes. Mitigation: gate deployment on a no-change verification pass.
- **Risk — Windows replacement fails on an in-use file**: sharing violations can prevent replacement. Mitigation: leave the existing entry intact, skip pruning for that destination, and report the failure.
- **Risk — documentation recreates retired links**: Evangelize is only one of several current link-creation paths. Mitigation: reconcile every supported setup path and enforce regression checks.
- **Risk — long-running watchers execute stale propagation logic**: deployment may use an older process after the script changes. Mitigation: require watcher restart before migration or release verification.

## Success Criteria

- [ ] No file-access guard entrypoint, Bash analyzer, guard-only policy implementation, guard configuration, hook registration, or generated wiring remains active.
- [ ] Direct file operations and Bash commands are not intercepted by the retired file-access system.
- [ ] The prompt-injection scanner and shared hook framework continue to pass their independent tests.
- [ ] `rtk-rewrite.sh` and its automatic hook registration are retired.
- [ ] RTK remains installed and an explicitly RTK-prefixed command works.
- [ ] Repository RTK guidance does not claim that RTK itself was retired.
- [ ] User-global deployment begins only after Claude, Codex, and OpenCode repository outputs reach a verified fixed point.
- [ ] Default and configured destinations resolve correctly for macOS, Linux, native Windows, and WSL.
- [ ] Native Windows and WSL are treated as separate current-environment deployments.
- [ ] Every repository-managed runtime link or junction in the fresh migration inventory is replaced by a regular managed copy or removed when obsolete.
- [ ] No managed user-global asset points into this repository through a symlink or junction after migration.
- [ ] Foreign files, directories, links, package links, plugin links, and Git hook links remain untouched.
- [ ] Stale managed copies are pruned without deleting unowned content.
- [ ] A failed harness retains its prior usable state and skips destructive reconciliation.
- [ ] Evangelize contains no behavior that creates, repairs, recommends, or validates runtime symlinks or junctions.
- [ ] Generated Evangelize variants match the corrected source behavior.
- [ ] Supported setup guidance contains no runtime link-creation path for generated agents, commands, skills, profiles, or learning assets.
- [ ] Fresh sessions resolve the deployed assets on macOS, Linux, native Windows, and WSL.
- [ ] Friction and deployment records describe the measured behavior and resulting security posture accurately.
- [ ] No Phase 01, Phase 02, or Phase 07 status line moves within this phase.

## QA Considerations

- Migration QA must run against scratch homes before touching the author's active runtime directories.
- The live migration requires a preflight inventory showing every planned replacement, removal, collision, and preserved path.
- Link and junction tests must include dangling targets and symlinked or junction-based parent directories.
- The final author-machine check must compare the fresh inventory with the generated platform rosters rather than relying on the earlier count of 113.
- Runtime verification must distinguish regular copies from links and confirm content freshness.
- Native Windows and WSL require separate evidence.
- Platform-specific failures must be reported as `NOT RUN` or failed, never inferred from another operating system.
- Retirement QA must verify absence of interception, not merely deletion of named files.
- Documentation QA must distinguish prohibited runtime-deployment instructions from legitimate discussion of symlink security threats.

## Notes for Feature - Decomposer

Suggested feature boundaries:

1. **Interceptor retirement** — remove file-access protection and automatic RTK rewriting while preserving RTK, the shared framework, and prompt-injection defense. Owns mixed-test surgery and explicit security-posture documentation.
2. **Propagation convergence and deployment orchestration** — establish the fixed-point gate, destination preflight, and per-harness failure isolation.
3. **Cross-platform destination adapters** — macOS, Linux, native Windows, and WSL path resolution using only documented defaults and relocation variables.
4. **Managed-copy migration and reconciliation** — ownership evidence, live and dangling link conversion, Windows junction handling, collision preservation, and safe stale-copy pruning. This is the phase's highest-risk feature and requires its own security review.
5. **Evangelize and setup-guidance reconciliation** — rewrite the source agent, regenerate its platform variants, and eliminate every supported runtime link-creation workflow.
6. **Cross-platform integration evidence and record correction** — scratch-home QA, live platform verification, final author-machine inventory, reduced-security disclosure, and evidence consolidation.

Features 2 through 5 are sequential where they touch the propagation pipeline. Feature 1 is parallel-safe until integration. Feature 6 is the phase tail.

Suggested implementation shape, to be verified by Feature Decomposer against current code and tests: treat generated platform outputs as the only deployment sources, represent ownership independently from destination existence, and make destructive reconciliation conditional on a successful copy for that same harness.
