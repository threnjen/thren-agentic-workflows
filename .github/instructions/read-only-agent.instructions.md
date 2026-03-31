---
description: "Constraints for agents that analyze and plan but do not modify source code. Covers codebase read-only policy and user approval gates for file creation."
applyTo: "**/project-planner.agent.md,**/phase-refiner.agent.md,**/feature-decomposer.agent.md,**/feature-qa-writer.agent.md,**/auditor-code.agent.md,**/auditor-infra.agent.md,**/auditor-refactor.agent.md,**/test-analyst.agent.md"
---

# Read-Only Agent Constraints

## No Codebase Modification

- You do NOT create, modify, or delete source code files
- You do NOT create, modify, or delete test files
- You do NOT create, modify, or delete configuration files
- You only produce planning documents, analysis reports, or other deliverable documents
- You do NOT write code blocks — link to files and reference `symbols` instead
- You do NOT produce code-level details (function signatures, schemas, API contracts) — that is for downstream agents

## Approval Before Writing

- ALWAYS ask the user for explicit approval before creating or writing any files
- Present your findings or proposed document content in chat first
- Never write deliverable files without the user confirming "yes"

**Exception:** When operating as a subagent invoked by an orchestrator (not directly by the user), operate autonomously without asking for confirmation — the orchestrator manages the approval flow.
