---
name: sdlc-standards
description: "Copper Forge delivery standard: branch naming and the forbidden-branch list, PR and semver tag rules, the hotfix path, CI/CD deploy gates and OIDC role derivation, AWS account and ECR promotion model, Terraform policy (version pin, state layout, tags, prevent_destroy, plan-before-apply), S3-based secrets and config, database migration backward compatibility, coverage floors, rollback, cost guardrails, lockfile policy, repo layout, ARN naming, deploy-log hygiene, and commit standards. Use when: naming a branch or tag, writing or changing a CI/CD workflow, provisioning infrastructure, wiring config or secrets, writing a migration, setting a coverage threshold, or scaffolding a new repo."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# SDLC Standards

These rules apply across the organization. Load them by name. They are not scoped to a file type.

## Priority order

`COST ≥ SECURITY ≥ SCALABILITY = RELIABILITY > USABILITY`. Use this order to break ties between otherwise acceptable designs.

## Branches, PRs, tags

The only long-lived branch is `main`. Merging into `main` deploys to `dev`.

| Prefix | From → PR to |
|---|---|
| `feature/*` | `main` → `main` |
| `chore/*` (maintenance, refactor) | `main` → `main` |
| `docs/*` | `main` → `main` |
| `hotfix/*` | `hotfix/current-prod` → `hotfix/current-prod` |

`hotfix/current-prod` is persistent and always equals the current prod SHA. The pipeline recreates it after every prod deploy.

**Never create a branch named** `dev`, `qa`, `stg`, `preprod`, `prod`, `release`, `candidate`, or prefixed `fix/`.

Each PR needs one approval. All CI checks must pass. Squash-merge the PR. Delete the branch after merging.

Release tags use semver `vMAJOR.MINOR.PATCH`. MAJOR marks a breaking change. MINOR marks a backward-compatible feature. PATCH marks a fix. Never delete or recreate a tag. Always increment the version.

Hotfix path:

1. Branch off `hotfix/current-prod`.
2. Open a PR back into `hotfix/current-prod`.
3. Smoke-test the branch by deploying it to dev.
4. Deploy to prod with the next semver tag.
5. Merge `hotfix/current-prod` into `main`.

## CI/CD

Use three workflow roles. Filenames are an implementation detail and vary by repo.

- **PR validation** runs lint, branch-name check, tests, coverage, build, and secret scan. It blocks merge. It never deploys.
- **Dev deploy** runs on a push to `main` or a manual trigger. It builds the image, pushes it to dev ECR, and deploys it to the dev account.
- **Prod deploy** runs manually. It takes a semver tag input. It copies the image from dev ECR to prod ECR by SHA and never rebuilds it. It passes a manual approval gate.

Deploy workflows only promote SHAs that already passed PR validation. A smoke check does not substitute for PR validation.

Use OIDC authentication only. Do not use IAM access keys in GitHub. Reusable workflows must derive the role ARN from organization variables. Do not accept a raw ARN input. Use `BASELINE_ACCOUNT_MAPPINGS` (JSON, environment-slug → account ID) and `OIDC_ROLE_NAME`. Use `environment-slug` as the workflow input.

```yaml
role-to-assume: arn:aws:iam::${{ fromJSON(vars.BASELINE_ACCOUNT_MAPPINGS)[inputs.environment-slug] }}:role/${{ vars.OIDC_ROLE_NAME }}
```

**Deploy-log hygiene:** Log the environment slug, stack names, and SSM paths being resolved. Never log account IDs, role names, resolved role ARNs, or secret values.

## AWS accounts

Each project uses two accounts, `dev` and `prod`. Each service has one ECR repo in each account. Shared VPC/Route53 live in `cf-infra-*` repos. Service repos consume them through `terraform_remote_state`.

## Terraform

The [terraform-module-authoring](../terraform-module-authoring/SKILL.md) skill governs shared-module authoring and publishing. This section covers policies that skill does not cover:

- Pin `required_version = "~> 1.15"`. Treat this value as written in the source. Confirm it is current before adopting it in a new repo.
- Store state in the Shared Services S3 bucket with key `{project}/{environment}/terraform.tfstate`. Use one state file per environment. Give each environment its own root config under `iac/environments/{environment}/`. Do not use workspaces.
- Check the shared modules repo before writing resources in a service repo. Never copy-paste a resource block between repos.
- Give every resource `Project`, `Environment`, `ManagedBy = terraform`, and `Owner`.
- Set `prevent_destroy = true` on production resources that must never be deleted.
- CI must produce `terraform plan` output and post it on the PR before any prod apply. Do not apply against any account without Infrastructure Reviewer approval.
- A hand-created resource is not managed until you import it into state.

SAM is permitted for Lambda-heavy projects. Terraform remains the default. The [aws-sam](../aws-sam/SKILL.md) skill defines SAM template conventions, including cross-stack SSM wiring and current Lambda runtime identifiers.

## Secrets and configuration

Store all application configuration, including sensitive and non-sensitive values, in S3. Read it at runtime from `cf-<account-name>-config-{dev,prod}`. Load `standard.env` first. Then load `{project}/app.env`, which overrides collisions. Enable versioning on both buckets.

Never bake a secret into a container image or Lambda package. Never commit a secret or send one by email. Upload secrets through the AWS CLI only.

truffleHog runs as a pre-commit hook and in CI. Detected secrets block the merge.

**Scope SSM Parameter Store by purpose.** Never use it for application configuration. Use S3 for that purpose. Always use it for cross-stack infrastructure references. One stack publishes a resource ARN, and another stack consumes it. Prefer it over CloudFormation `!ImportValue`, which creates a hard dependency lock that prevents the exporting stack's deletion. The consumer must resolve the value with a dynamic reference inside the template (`{{resolve:ssm:/<org-prefix>/<environment>/<resource-slug>:1}}`). Never resolve it with a workflow-side lookup. A missing, malformed, or stale parameter must break the deploy. The deploy must not fall back silently.

## Runtime safety

These defect classes can turn a protection into a hole. Review each one by reading it correctly.

- **Validate each resolved source and destination directory against its declared root before reading or writing.** A symlinked *parent* can redirect writes outside the root even when every leaf check passes. Replacing only a symlinked leaf is insufficient.
- **When a public value type can be constructed directly and through a validating factory, re-validate it at every security-sensitive emission or execution boundary.** Otherwise callers can bypass the factory, and a fail-closed path becomes ambiguous.
- **Fail-open observability must cover the executable wrapper, not only exceptions inside the language.** An interpreter-startup or pipeline failure returns non-zero before application handling runs. An audit-only hook therefore blocks its caller. Watch for `set -e`/`pipefail` with no non-blocking fallback.
- **Glob-comparison matchers must vary wildcard replacements independently.** Treat the protected root as part of a recursive rule. `protected/**` can accidentally allow `protected` itself.
- **Use exact suffix removal, not `rstrip`, when stripping a delimiter.** `rstrip("\n")` eats any trailing backslash or `n`. It corrupts names like `auth.json` before policy evaluation.

## Database migrations

Use Alembic or the language equivalent. Migrations run as a pre-deploy step. A failed migration aborts the deploy and leaves running tasks untouched. No automated rollback exists. Resolve migration problems with a forward fix only.

Preserve backward compatibility:

- Never drop a column in the same deploy that stops using it.
- Never rename a column directly. Handle the rename across separate deploys:
  1. Add the new column.
  2. Migrate the data.
  3. Update callers.
  4. Drop the old column.
- Adding nullable or defaulted columns is always safe.

Apply the same rule to services, APIs, SDKs, and shared libraries. Announce a deprecation with a documented migration path. Give a remediation window measured in releases. Land breaking removals in a major version.

## Testing

Automated tests are mandatory. The coverage floor is 70% overall and 80%+ for new or changed code. Never lower an existing threshold. A project may set a stricter threshold.

Auth, authorization, billing, persistence, and migrations need direct coverage regardless of the aggregate. A passing percentage does not waive direct coverage. Coverage is a guardrail, not the goal. Tests written only to increase the percentage are not acceptable.

Integration tests are required wherever the project talks to a database, queue, AWS service, or external API in a non-trivial way. Manual testing supplements automated testing. Manual testing never replaces automated testing.

Each bug fix must include a regression test unless it is genuinely untestable. Document the exception in the PR.

## Rollback

Rollback requires a manual decision. Identify the last-known-good release tag in prod ECR (last 5 retained). Redeploy it with the next semver tag. If a migration was involved, stop and assess first.

## Cost guardrails

Do not use a NAT Gateway by default. Do not use AWS Secrets Manager. ECR lifecycle keeps the last 5 tagged images and deletes untagged images after one day. Set billing alarms at $10 and $50 per account.

## Dependencies

Python uses `uv`. Node.js uses `npm`. Commit lockfiles. CI installs from the lockfile, never from a floating version range. Apply this rule to pinned tool and hook versions too. Never pin them to a moving branch.

## Naming ARNs

A variable, environment variable, or config key that holds an ARN must end in `_ARN`. Reserve `_NAME` for the bare identifier. Treat `BACKEND_LAMBDA_NAME` holding an ARN as a defect. Do not keep a misleading alias for backward compatibility. Do not create two variables for one resource to paper over a legacy name.

## Repository layout

```
.github/workflows/    # PR validation, dev deploy, prod deploy
iac/backend.tf
iac/environments/{dev,prod}/main.tf + terraform.tfvars
src/
tests/
Dockerfile
.pre-commit-config.yaml
.trufflehog.yml
```

## Commits

Use Conventional Commits. Every commit must compile. Every commit must pass tests and the project's formatter/linter. Every commit must leave no TODO without an issue number. Commit early and often. Never use `--no-verify` to bypass hooks. Never disable a test instead of fixing it.

When two implementations are acceptable, choose in this order: **testability → readability → consistency → simplicity → reversibility.**
