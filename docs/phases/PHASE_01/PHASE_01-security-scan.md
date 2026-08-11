# Diff-Scoped Security Report: PHASE_01

## Scan Metadata

- **Repository revision:** `62a77312a548b0dff04679853837399763d198f4`
- **Diff baseline:** `4a18fd16ca74a3b8362ed2a415970316b113e0c0` (`git merge-base HEAD main`)
- **Scan date:** 2026-08-10
- **Readable files scanned:** 53 of 54 paths in the caller-supplied union
- **Unavailable scoped context:** `ports/cursor/skills/decision-presentation/SKILL.md` is absent because propagation is pending. It is generated context, not an authoring surface; the canonical source skill was scanned.
- **Scope:** diff-only. Files outside the explicit list below were not assessed. Generated ports were read only as context and were not treated as independent authoring surfaces.
- **Method:** reviewed the scoped diff and current contents for embedded secrets, workflow permissions and trust boundaries, action provenance, unsafe process/filesystem commands, path handling, destructive operations, external network references, and data-bearing artifacts. Pattern sweeps reported locations only; no secret values were printed or copied into this report.

### Explicit Changed-File Union

```text
CONTRIBUTING.md
dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-context.md
dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-implementation.md
dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-plan.md
dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-review.md
dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-tasks.md
dev/feature/02-headless-asset-import/02-headless-asset-import-context.md
dev/feature/02-headless-asset-import/02-headless-asset-import-implementation.md
dev/feature/02-headless-asset-import/02-headless-asset-import-plan.md
dev/feature/02-headless-asset-import/02-headless-asset-import-review.md
dev/feature/02-headless-asset-import/02-headless-asset-import-tasks.md
dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-context.md
dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-implementation.md
dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-plan.md
dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-review.md
dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-tasks.md
dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-context.md
dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-implementation.md
dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-plan.md
dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-review.md
dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-tasks.md
docs/phases/DISCOVERY_CONTEXT.md
docs/phases/PHASE_01/PHASE_01_DISCOVERY_CONTEXT.md
docs/phases/PHASE_01/PHASE_01_QA.md
docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md
docs/phases/PHASE_01/PHASE_01_SUMMARY.md
docs/phases/PROJECT_ROADMAP.md
docs/unity/LOCAL_TESTING.md
ports/claude/commands/phase-refiner.md
ports/claude/commands/project-planner.md
ports/claude/skills/decision-presentation/SKILL.md
ports/codex/agents/01-project-planner.toml
ports/codex/agents/02-phase-refiner.toml
ports/codex/skills/decision-presentation/SKILL.md
ports/cursor/commands/phase-refiner.md
ports/cursor/commands/project-planner.md
ports/cursor/skills/decision-presentation/SKILL.md (unavailable; propagation pending)
ports/github/agents/01-project-planner.agent.md
ports/github/agents/02-phase-refiner.agent.md
ports/github/skills/decision-presentation/SKILL.md
ports/opencode/agents/01-project-planner.md
ports/opencode/agents/02-phase-refiner.md
ports/opencode/skills/decision-presentation/SKILL.md
source_of_truth/agents/01-project-planner.agent.md
source_of_truth/agents/02-phase-refiner.agent.md
source_of_truth/agents/04-phase-execute.agent.md
source_of_truth/agents/04g-unity-visual-verification.agent.md
source_of_truth/agents/04h-unity-reviewer.agent.md
source_of_truth/skills/decision-presentation/SKILL.md
source_of_truth/skills/unity-development/SKILL.md
source_of_truth/skills/unity-development/references/gameci-test-workflow.yml
tests/test_unity_consumer_contract.py
tests/test_unity_reference_assets.py
tests/test_unity_skill_contract.py
```

## Verdict

- **PASS WITH CONDITIONS**
- **Critical:** 0
- **High:** 0
- **Medium:** 1
- **Low:** 0

The scanned authoring diff contains no embedded credential values, private keys, broad write permissions, unsafe recursive deletion, or shell-evaluation construct. The condition is that the inert workflow template must be hardened before activation because its action dependencies use mutable major-version tags.

## Findings

| ID | Severity | Category | Location | Evidence | Impact | Recommended remediation |
|----|----------|----------|----------|----------|--------|-------------------------|
| PH01-SEC-001 | Medium | CI/CD supply chain | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml:18,22,34,42,54` | The copyable template references three actions by mutable major-version tags. Two Unity test steps pass caller-supplied Unity account secrets to the third-party test action. GitHub states that a full-length commit SHA is the only immutable action reference and that a compromised action can access job secrets. The template is inert in this repository, so no current workflow or secret is exposed. | If a maintainer copies and activates the template unchanged, upstream tag movement or action-repository compromise could execute changed code in a job that receives Unity credentials. Exploitation requires template activation, which is why this is Medium rather than High in the current diff. | Before installation, replace every action tag with a verified full-length commit SHA and record the corresponding release tag for update review. Apply repository or organization policy requiring SHA-pinned actions where available. Revalidate the adapted workflow after substituting the Unity project path. |

Authority: [GitHub Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) documents full-SHA pinning and the secret exposure impact of a compromised action. GitHub also documents that fork-originated `pull_request` workflows normally receive no repository secrets; any repository that deliberately enables fork-secret access must reassess this template's trust boundary before activation ([GitHub Actions repository settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)).

## Security Controls Observed

- The workflow declares `permissions: contents: read` and omits `githubToken`, write permissions, literal credentials, and serial values.
- Unity credential fields are GitHub secret-context references only; the scan found no embedded values or private-key material in the scoped files.
- The local runbook quotes variable paths, separates `-quit` asset import from `-runTests`, requires a clean detached worktree, writes deterministic evidence paths, and validates the fixed worktree target before manual removal.
- The canonical skill forbids overwriting foreign worktree content, automatic teardown, GUI fallback, uncommitted shadow execution, and ignored content outside the Unity project's `Library/`.
- The Visual Verifier contract keeps a machine-local editor path out of version control and requires it to be ignored before reuse.
- The workflow remains under `source_of_truth/skills/.../references/`; no active `.github/workflows/` path is part of the supplied scope.

## Not Assessable at Diff Scope

- **Repository and organization GitHub Actions policy:** whether SHA pinning is enforced, which contributors may approve workflows, and whether a private repository is configured to send secrets to fork pull requests require settings outside the file union.
- **Action implementation integrity:** the source, build provenance, transitive dependencies, and current compromise status of the referenced GitHub and GameCI actions are external to this diff.
- **Dependency and vulnerability posture:** no dependency manifests or lock files are in scope; a full supply-chain/SBOM audit was not performed.
- **Authentication and authorization architecture:** the diff adds no application auth surface, and files implementing repository, cloud, or Unity-account access control are outside scope.
- **Runtime Unity trust boundary:** the Unity project, its Editor scripts/tests, packages, and the external reference checkout are outside this repository diff, so behavior executed by batchmode or GameCI could not be audited.
- **Artifact confidentiality and retention:** XML and Unity logs are directed to `dev/test-results/`, but ignore rules, CI retention policy, log contents, and downstream publication controls are outside the explicit list.
- **Cross-repository data protection:** the external reference project's contents, cleanliness, licensing state, and any local Unity-generated assets were not scanned.
- **Generated-port completeness:** propagation is pending, and the listed Cursor skill mirror is absent. Generated ports were context only; no claim is made that all harness outputs currently match the canonical sources.
- **Full-codebase secret history:** the scan checked only current scoped files and their diff, not Git history, deleted content outside the baseline range, other branches, or files outside the union.
