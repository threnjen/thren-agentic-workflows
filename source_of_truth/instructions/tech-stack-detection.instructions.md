---
description: "Detect specialized tech stacks and load matching skills before starting work; holds the canonical Unity detection predicate. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family, so add each new consumer by name rather than widening the glob. This file is the only copy of the predicate; do not restate it elsewhere."
applyTo: "**/03-phase-execute.agent.md,**/03o-feature-plan-author.agent.md,**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03f-prod-code-review.agent.md,**/04-phase-final-checks.agent.md,**/auditor-code.agent.md,**/auditor-infra.agent.md,**/auditor-refactor.agent.md,**/auditor-security.agent.md,**/single-feature-agent.agent.md"
---

Check whether the project uses a specialized tech stack with a matching skill. Look for `.github/copilot-instructions.md` naming a stack or for framework-specific project files. Check `package.json` for Node.js and `pyproject.toml` for Python. Apply the Unity predicate below. When a matching skill exists, **load and read it before you proceed**. The skill holds stack-specific rules and known pitfalls.

## Canonical Unity Detection Predicate

This predicate is the corpus's single definition. Every other site that decides "is this Unity?" states this predicate in these terms. If another site disagrees, this predicate takes precedence.

> The repository is a Unity project if **any** condition below holds:
> - `Assets/` and `ProjectSettings/` both exist at the repository root (standard layout)
> - `Assets/` and `ProjectSettings/` both exist inside one nested project directory, e.g. `game/Assets/` and `game/ProjectSettings/` (nested/monorepo layout)
> - `.github/copilot-instructions.md` identifies the project as Unity
> - The plan or phase document under work targets Unity, MonoBehaviour, or Unity-specific systems
>
> `*.asmdef` files corroborate a match but are **never required** — small Unity projects have none.

When the predicate matches, load `unity-development`. When you review or audit, also load `unity-review-knowledge`.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: tech-stack-detection."* Then proceed normally.
