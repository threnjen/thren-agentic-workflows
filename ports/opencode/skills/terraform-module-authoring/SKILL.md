---
name: terraform-module-authoring
description: "Author and publish reusable Terraform modules in cf-infra-terraform-modules. Use when: adding/updating a module under terraform_modules/modules/, validating publish artifacts, reviewing module source references, or deciding whether to introduce a new shared module."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Terraform Module Authoring

Use this skill when working in `../cf-infra-terraform-modules` on reusable module design, packaging, publishing, or guidance for downstream consumption.

## Source Of Truth Files

- `../cf-infra-terraform-modules/terraform_modules/zip_files.sh`
- `../cf-infra-terraform-modules/terraform_modules/upload_modules.tf`
- `../cf-infra-terraform-modules/terraform_modules/variables.tf`
- `../cf-infra-terraform-modules/README.md`

Do not describe a publish workflow that differs from these files.

## Module Interface Requirements

Include the following files for new modules and full interface refactors:

- Include `README.md` with the module purpose, required inputs, outputs, and a usage example.
- Include `variables.tf` for the input contract.
- Include `outputs.tf` for exported values.

Current repository modules use legacy layouts. Some modules may lack one or more of the three files. Do not normalize interfaces broadly unless an approved migration or refactor includes that scope.

Interface guidance:

- Prefer to extend an existing module when its behavior is a narrow variant of the same domain.
- Propose a new module only for a distinct reusable domain. Do so only when optional inputs on an existing module cannot express the interface cleanly.
- Keep module inputs minimal and explicit. Avoid hidden behavior.

## Legacy Naming Constraint

`cf-infra-terraform-modules` currently uses legacy variable names in Terraform, such as `AWS_PROFILE`, `MODULE_BUCKET`, and `REGION`. Treat this as a bounded repo-specific exception.

- Keep existing legacy names stable in this repository unless a dedicated migration plan is in scope.
- Do not copy this style into new code in sibling repositories.

## Publish Workflow (Current Implementation)

Follow these two steps to publish modules in order:

1. Package module directories into zip artifacts with `terraform_modules/zip_files.sh`.
2. Upload zip artifacts via Terraform resources in `terraform_modules/upload_modules.tf`.

The repository currently packages and uploads these modules:

- `ecr`
- `ecs_task_definition`
- `fargate_iam_policies`
- `iam_ecs_roles`
- `iam_lambda_roles`
- `iam_lambda_run_permissions`
- `lambda_ecs_trigger_policies`
- `lambda_function_direct`

Before merging, validate the following:

- Every module zip that `zip_files.sh` generates has a matching `aws_s3_object` in `upload_modules.tf`.
- Zip names and S3 (Amazon Simple Storage Service) object keys remain identical (for example, `ecr.zip`).
- No stale upload resources reference removed artifacts.

## S3 Sourcing Pattern

Downstream repositories should consume published artifacts with the following source:

`source = "s3::https://copperforge-terraform-modules.s3.us-west-2.amazonaws.com/<module>.zip"`

Example:

`source = "s3::https://copperforge-terraform-modules.s3.us-west-2.amazonaws.com/ecr.zip"`

Use exact zip artifact names from publish outputs.

## Cross-Account Access

- The AWS Identity and Access Management (IAM) role `TerraformModuleReadAccess` grants module read access.
- Use role-based access for continuous integration and runtime consumers instead of embedding long-lived AWS credentials.

## Security Constraints

- Keep continuous integration and continuous delivery (CI/CD) authentication based on OpenID Connect (OIDC).
- Do not document static access keys for publishing or consuming modules. Do not introduce static access keys for either purpose.
- Do not broaden permissions with wildcard mutate actions, which modify resources, without explicit review and justification.

## Proposing A New Module

1. Confirm that existing modules cannot satisfy the use case through compatible interface changes.
2. Open an issue that describes the module's purpose, inputs, outputs, and consumers.
3. Implement the module in a feature branch with `README.md`, `variables.tf`, and `outputs.tf`.
4. Add zip and upload configuration so publication artifacts exist.
5. Do not merge until the module has a valid published artifact and a documented source URL.
