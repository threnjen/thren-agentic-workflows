---
name: sdlc-standards
description: "Copper Forge delivery standard: branch naming and the forbidden-branch list, PR and semver tag rules, the hotfix path, CI/CD deploy gates and OIDC role derivation, AWS account and ECR promotion model, Terraform policy (version pin, state layout, tags, prevent_destroy, plan-before-apply), S3-based secrets and config, database migration backward compatibility, coverage floors, rollback, cost guardrails, lockfile policy, repo layout, ARN naming, deploy-log hygiene, and commit standards. Use when: naming a branch or tag, writing or changing a CI/CD workflow, provisioning infrastructure, wiring config or secrets, writing a migration, setting a coverage threshold, or scaffolding a new repo."
---

# SDLC Standards

Org-wide delivery rules. Loaded by name; not scoped to a file type.

## Priority order

`COST ≥ SECURITY ≥ SCALABILITY = RELIABILITY > USABILITY`. Use it to break ties between otherwise acceptable designs.

## Branches, PRs, tags

`main` is the only long-lived branch; merging to it deploys to `dev`.

| Prefix | From → PR to |
|---|---|
| `feature/*` | `main` → `main` |
| `chore/*` (maintenance, refactor) | `main` → `main` |
| `docs/*` | `main` → `main` |
| `hotfix/*` | `hotfix/current-prod` → `hotfix/current-prod` |

`hotfix/current-prod` is persistent and always equals the current prod SHA; the pipeline recreates it after every prod deploy.

**Never create a branch named** `dev`, `qa`, `stg`, `preprod`, `prod`, `release`, `candidate`, or prefixed `fix/`.

PRs: one approval, all CI checks green, squash merge, branch deleted after merge.

Release tags are semver `vMAJOR.MINOR.PATCH` — MAJOR breaking, MINOR backward-compatible feature, PATCH fix. Never delete or recreate a tag; always increment.

Hotfix path: branch off `hotfix/current-prod` → PR back into it → smoke test by deploying it to dev → prod deploy with the next semver tag → merge `hotfix/current-prod` into `main`.

## CI/CD

Three workflow roles. Filenames are an implementation detail and vary by repo.

- **PR validation** — lint, branch-name check, tests, coverage, build, secret scan. Blocks merge. Never deploys.
- **Dev deploy** — on push to `main` or manual. Builds the image, pushes to dev ECR, deploys to the dev account.
- **Prod deploy** — manual only, takes a semver tag input, copies the image dev→prod ECR by SHA (never rebuilds), passes a manual approval gate.

Deploy workflows only promote SHAs that already passed PR validation; a smoke check does not substitute for it.

Auth is OIDC only — no IAM access keys in GitHub. Reusable workflows must derive the role ARN from org variables rather than accepting a raw ARN input: `BASELINE_ACCOUNT_MAPPINGS` (JSON, environment-slug → account ID) plus `OIDC_ROLE_NAME`, with `environment-slug` as the workflow input.

```yaml
role-to-assume: arn:aws:iam::${{ fromJSON(vars.BASELINE_ACCOUNT_MAPPINGS)[inputs.environment-slug] }}:role/${{ vars.OIDC_ROLE_NAME }}
```

**Deploy-log hygiene:** log the environment slug, stack names, and SSM paths being resolved. Never log account IDs, role names, resolved role ARNs, or secret values.

## AWS accounts

Two accounts per project (`dev`, `prod`), one ECR repo per service in each. Shared VPC/Route53 live in `cf-infra-*` repos and are consumed via `terraform_remote_state`.

## Terraform

Authoring and publishing shared modules is governed by [terraform-module-authoring](../terraform-module-authoring/SKILL.md). Policy that skill does not cover:

- Pin `required_version = "~> 1.15"` (the source's value as written; confirm current before adopting in a new repo).
- State in the Shared Services S3 bucket, key `{project}/{environment}/terraform.tfstate`. One state file per environment, each with its own root config under `iac/environments/{environment}/`. No workspaces.
- Module-first: check the shared modules repo before writing resources in a service repo. Never copy-paste a resource block between repos.
- Every resource carries `Project`, `Environment`, `ManagedBy = terraform`, `Owner`.
- Production resources that must never be deleted set `prevent_destroy = true`.
- `terraform plan` output is required in CI, posted on the PR, before any prod apply. No apply against any account without Infrastructure Reviewer approval.
- A hand-created resource is not managed until it is imported into state.

SAM is permitted for Lambda-heavy projects; Terraform remains the default. SAM template conventions, including cross-stack SSM wiring and current Lambda runtime identifiers, live in [aws-sam](../aws-sam/SKILL.md).

## Secrets and configuration

All application config, sensitive and not, lives in S3 and is read at runtime from `cf-<account-name>-config-{dev,prod}`. Two files load in order — `standard.env` first, then `{project}/app.env`, which overrides on collision. Versioning is on for both buckets.

Never bake a secret into a container image or Lambda package. Never commit one or send it over email; upload via the AWS CLI only.

truffleHog runs as a pre-commit hook and in CI; detected secrets block the merge.

**Unreconciled — SSM Parameter Store.** The org standard says Parameter Store "is not used" for application configuration. The infrastructure-patterns standard mandates it for cross-stack references (one stack publishing a resource ARN for another to consume). Both are recorded as written; neither overrides the other without a maintainer decision.

## Database migrations

Alembic, or the language equivalent. Migrations run as a pre-deploy step; a failed migration aborts the deploy and leaves running tasks untouched. There is no automated rollback — migration problems are forward-fix only.

Backward compatibility is non-negotiable:

- Never drop a column in the same deploy that stops using it.
- Never rename a column directly — add, migrate, update, drop across separate deploys.
- Adding nullable or defaulted columns is always safe.

The same rule extends to services, APIs, SDKs, and shared libraries: announce a deprecation with a documented migration path, give a remediation window measured in releases, and land breaking removals in a major version.

## Testing

Automated tests are mandatory. Coverage floor is 70% overall, 80%+ for new or changed code. Never lower an existing threshold; a project may set a stricter one.

Auth, authorization, billing, persistence, and migrations need direct coverage regardless of the aggregate — a passing percentage does not waive it. Coverage is a guardrail, not the goal; tests written only to move the number are not acceptable.

Integration tests are required wherever the project talks to a database, queue, AWS service, or external API non-trivially. Manual testing supplements, never replaces.

Bug fixes carry a regression test unless genuinely untestable — document the exception in the PR.

## Rollback

A manual decision. Identify the last-known-good release tag in prod ECR (last 5 retained) and redeploy it with the next semver tag. If a migration was involved, stop and assess first.

## Cost guardrails

No NAT Gateway by default. No AWS Secrets Manager. ECR lifecycle keeps the last 5 tagged images and deletes untagged after one day. Billing alarms at $10 and $50 per account.

## Dependencies

Python uses `uv`; Node.js uses `npm`. Lockfiles are committed and CI installs from the lockfile — never from a floating version range. This applies to pinned tool and hook versions too: never pin to a moving branch.

## Naming ARNs

A variable, environment variable, or config key holding an ARN must end in `_ARN`. Reserve `_NAME` for the bare identifier. `BACKEND_LAMBDA_NAME` holding an ARN is a defect. Do not keep a misleading alias for backward compatibility, and do not create two variables for one resource to paper over a legacy name.

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

Conventional Commits. Every commit compiles, passes tests and the project's formatter/linter, and leaves no TODO without an issue number. Commit early and often. Never use `--no-verify` to bypass hooks, and never disable a test instead of fixing it.

When two acceptable implementations remain: **testability → readability → consistency → simplicity → reversibility.**
