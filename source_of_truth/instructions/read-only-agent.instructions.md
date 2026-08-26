---
description: "Constraints for agents that analyze and plan but do not modify source code. Covers codebase read-only policy and user approval gates for file creation. Audience is ENUMERATED deliberately - 'writes no source' is a frontmatter property, not a filename family. Add any agent whose tools exclude source edits."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/02a-phase-final-check.agent.md,**/03a-feature-plan-expander.agent.md,**/03c-feature-review-and-fix.agent.md,**/03d-feature-qa-writer.agent.md,**/03e-diff-security-scan.agent.md,**/03f-prod-code-review.agent.md,**/03h-unity-reviewer.agent.md,**/03j-reviewer-blast-radius.agent.md,**/03k-reviewer-test-falsification.agent.md,**/03l-reviewer-plan-blind.agent.md,**/03m-finding-consolidator.agent.md,**/03n-finding-validator.agent.md,**/04b-change-narrator.agent.md,**/04c-artifact-sweeper.agent.md,**/04d-consistency-auditor.agent.md,**/04e-dependency-auditor.agent.md,**/04f-test-health.agent.md,**/04g-readiness-synthesizer.agent.md,**/04h-cleanliness-auditor.agent.md,**/auditor-attribution.agent.md,**/auditor-code.agent.md,**/auditor-delta.agent.md,**/auditor-infra.agent.md,**/auditor-refactor.agent.md,**/auditor-remediation-reconciler.agent.md,**/auditor-remediation-research.agent.md,**/auditor-security.agent.md,**/client-deliverable-02-delta-synthesizer.agent.md,**/client-deliverable-03-security-narrative.agent.md,**/client-deliverable-04-pricing-researcher.agent.md,**/client-deliverable-05-narrative-writer.agent.md,**/client-deliverable-06-compliance-writer.agent.md,**/client-deliverable-07-manifest-assembler.agent.md,**/client-deliverable-08-gap-reviewer.agent.md,**/qa-doc-generator.agent.md,**/test-analyst.agent.md,**/web-research-specialist.agent.md"
---

# Read-Only Agent Constraints

## Permissions

| | |
|---|---|
| ✅ **Write** | Only the deliverable documents your contract or caller assigns you, at the paths they assign — phase summaries, discovery context, audit and delta reports, review reports, research reports, test analysis plans, QA documents. Writing your own report is always allowed. Nothing else is. |
| ❌ **Never write** | Anything in the repository under analysis: source code, test files, configuration, dependency manifests, lock files. Never fix a finding you report. |
| ❌ **Never author** | New or proposed code, or code-level design that belongs downstream — function signatures, schemas, API contracts. Quoting **existing** code as evidence at a cited path and line is required, not forbidden. |

## Approval gate

One gate, and only when the user invoked you directly.

1. Present the proposed document content in chat.
2. Wait for the user to signal ready — "yes", "ready", "go ahead", "approved", "looks good", "proceed", "write it", or anything equivalent.
3. Write the files. Do not ask a second time.

**When an orchestrator spawned you**, skip the gate and write autonomously. The orchestrator owns approval.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: read-only-agent."* Then proceed normally.
