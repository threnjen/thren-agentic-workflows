# Phase 04 Hook Retirement & Cross-Platform Deployment — Execution Manifest

**Phase document:** `docs/phases/PHASE_04/PHASE_04_SUMMARY.md`

**Discovery context:** `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md`

**Ordering note:** None. The feature order preserves the Phase document's Key Deliverables sequence; shared-file and runtime dependencies require each later feature to execute in a later wave.

## Ordered Feature Tasks

1. `01-interceptor-retirement`
2. `02-propagation-convergence`
3. `03-cross-platform-destinations`
4. `04-managed-copy-reconciliation`
5. `05-deployment-guidance`
6. `06-runtime-verification`

## Feature Execution Metadata

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---:|---|---|---|---|
| `01-interceptor-retirement` | 1 | yes | none | `.github/hooks/file-access-guard.json`, `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/scripts/rtk-rewrite.sh`, `.github/hooks/lib/file_access.py`, `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/config/file-access-rules.json`, `.github/hooks/config/file-access-overrides.json`, `scripts/propagate_master_assets.py`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/file-access-guard.js`, guard-only and mixed hook tests/fixtures, active hook documentation | n/a |
| `02-propagation-convergence` | 2 | no | `01-interceptor-retirement` | `scripts/propagate_master_assets.py`, `.vscode/tasks.json` `(verify)`, `tests/test_propagate_master_assets.py`, `tests/test_retirement_reconciliation.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]` | shares `scripts/propagate_master_assets.py` and `tests/test_propagate_master_assets.py` with upstream `01-interceptor-retirement` |
| `03-cross-platform-destinations` | 3 | no | `02-propagation-convergence` | `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_propagate_master_assets.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]` | shares propagator and test surfaces with upstream `02-propagation-convergence` |
| `04-managed-copy-reconciliation` | 4 | no | `03-cross-platform-destinations` | `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_propagate_master_assets.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]` | shares the propagator, proposed deployment module, and phase integration test with upstream `03-cross-platform-destinations` |
| `05-deployment-guidance` | 5 | no | `04-managed-copy-reconciliation` | `.github/agents/evangelize.agent.md`, generated Evangelize variants, `claude/README.md`, `claude/SYMLINK_SETUP.md`, `claude/agents/README.md`, `codex/MACOS_SETUP_AND_SYMLINKS.md`, `codex/PILOT_SLICE_PLAN.md`, `opencode/SYMLINK_SETUP.md`, `HARNESS_SETUP.md`, `docs/TROUBLESHOOTING.md`, `README.md`, `scripts/propagate_master_assets.py` `(verify)`, shared propagation/integration tests | consumes the upstream managed-copy API and shares propagator/test surfaces with upstream features |
| `06-runtime-verification` | 6 | no | `01-interceptor-retirement`, `02-propagation-convergence`, `03-cross-platform-destinations`, `04-managed-copy-reconciliation`, `05-deployment-guidance` | `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_propagate_master_assets.py`, `tests/test_retirement_reconciliation.py` `(verify)`, `tests/hooks/test_hook_distribution_integration.py` `(verify)`, `.github/learnings/cross-phase-decisions.md`, `.github/learnings/project-learnings.md`, generated Claude learnings, Phase 04 records | integration depends on every upstream feature and shares their propagator, deployment, and verification surfaces |

## Dependency Graph

- `02-propagation-convergence` depends_on `01-interceptor-retirement` because both modify `scripts/propagate_master_assets.py` and `tests/test_propagate_master_assets.py`.
- `03-cross-platform-destinations` depends_on `02-propagation-convergence` because destination resolution runs only after bounded repository convergence and both share propagator/test surfaces.
- `04-managed-copy-reconciliation` depends_on `03-cross-platform-destinations` because it consumes the upstream destination-record API and shares the proposed deployment module and integration tests.
- `05-deployment-guidance` depends_on `04-managed-copy-reconciliation` because Evangelize and setup guidance must invoke the settled managed-copy workflow and share regression surfaces.
- `06-runtime-verification` depends_on all preceding features because it is the required integration/bootstrap tail and verifies the combined runtime result.

## Execution Schedule

### Wave 1 — parallel

- `01-interceptor-retirement`

### Wave 2 — sequential

- `02-propagation-convergence`

### Wave 3 — sequential

- `03-cross-platform-destinations`

### Wave 4 — sequential

- `04-managed-copy-reconciliation`

### Wave 5 — sequential

- `05-deployment-guidance`

### Wave 6 — sequential

- `06-runtime-verification`

## Expected Feature Bundles

| Feature Directory | Required Files |
|---|---|
| `dev/feature/01-interceptor-retirement/` | `01-interceptor-retirement-plan.md`, `01-interceptor-retirement-context.md`, `01-interceptor-retirement-tasks.md` |
| `dev/feature/02-propagation-convergence/` | `02-propagation-convergence-plan.md`, `02-propagation-convergence-context.md`, `02-propagation-convergence-tasks.md` |
| `dev/feature/03-cross-platform-destinations/` | `03-cross-platform-destinations-plan.md`, `03-cross-platform-destinations-context.md`, `03-cross-platform-destinations-tasks.md` |
| `dev/feature/04-managed-copy-reconciliation/` | `04-managed-copy-reconciliation-plan.md`, `04-managed-copy-reconciliation-context.md`, `04-managed-copy-reconciliation-tasks.md` |
| `dev/feature/05-deployment-guidance/` | `05-deployment-guidance-plan.md`, `05-deployment-guidance-context.md`, `05-deployment-guidance-tasks.md` |
| `dev/feature/06-runtime-verification/` | `06-runtime-verification-plan.md`, `06-runtime-verification-context.md`, `06-runtime-verification-tasks.md` |

## Fidelity Exceptions and Accepted Risks

- Existing user-global hook deployment is not folded into the new asset-copy stage, per Phase 04 discovery. Feature 1 retires the targeted registrations and Feature 6 verifies the final hook state.
- The repository has no generated `opencode/commands/` source. Feature 3 must not invent one without an upstream propagation change.
- The generated `codex/profiles/` to documented runtime `prompts/` mapping is unverified and must be resolved before the deployable roster is frozen.
- `codex/PILOT_SLICE_PLAN.md` contains executable runtime-link setup steps; Feature 5 must classify it as active or historical and cannot silently leave supported link-creation guidance.
- New deployment module, consolidated test file, public APIs, and CLI flag remain `[PROPOSED - name TBD]`; implementers must settle names consistently across upstream acceptance criteria and downstream calls.
- The active environment lacks the `pytest` module. Unittest baselines captured by expanders pass, while pytest-only hook evidence remains runner-constrained until dependencies are provisioned.

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]` | `02-propagation-convergence`, `03-cross-platform-destinations`, `04-managed-copy-reconciliation`, `05-deployment-guidance`, `06-runtime-verification` | Consolidated fixed-point, destination, scratch-home migration, documentation regression, partial-failure, idempotency, and end-to-end integration coverage |

### Existing Test Files Updated By Multiple Features

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/test_propagate_master_assets.py` | `01-interceptor-retirement`, `02-propagation-convergence`, `03-cross-platform-destinations`, `04-managed-copy-reconciliation`, `05-deployment-guidance`, `06-runtime-verification` | Shared propagation, generated-output, CLI, convergence, Evangelize, and deployment orchestration regression coverage |
| `tests/hooks/test_hook_distribution_integration.py` | `01-interceptor-retirement`, `06-runtime-verification` | Mixed-test surgery followed by final surviving-hook and absence-of-interception verification |
| `tests/test_retirement_reconciliation.py` | `02-propagation-convergence`, `06-runtime-verification` | Repository fixed-point enforcement and final evidence verification |

### Manual QA Checklist

- [ ] Run migration against scratch homes before any active runtime directory.
- [ ] Review a fresh preflight inventory of every planned replacement, removal, collision, preserved path, and failed/skipped action.
- [ ] Confirm no automated test or manual dry run targets the author's live home without explicit reviewed authorization.
- [ ] Restart any long-running propagation watcher before collecting convergence or release evidence.
- [ ] Verify macOS runtime discovery from regular fresh copies in a new session, or record `NOT RUN`/failure.
- [ ] Verify Linux runtime discovery from regular fresh copies in a new session, or record `NOT RUN`/failure.
- [ ] Verify native Windows runtime discovery, junction migration, and locked-file behavior in a new session, or record `NOT RUN`/failure.
- [ ] Verify WSL runtime discovery independently inside the active distribution's Linux home, or record `NOT RUN`/failure.
- [ ] Confirm unavailable or failed platform evidence prevents a full cross-platform GO verdict.
- [ ] Compare the fresh live inventory with generated platform rosters rather than asserting the historical count of 113 links.
- [ ] Confirm foreign files, links, package assets, plugin-cache links, debug pointers, and Git hooks remain untouched.
- [ ] Confirm all managed destinations are regular files/directories, content-fresh, and contain no repository-targeting links or junctions.
- [ ] Confirm file-access and automatic RTK-rewrite interception are absent, prompt-injection/framework checks survive, and an explicitly prefixed RTK command remains usable.
- [ ] Run deployment twice and confirm the second repository/runtime result is a fixed point with no mutations.

