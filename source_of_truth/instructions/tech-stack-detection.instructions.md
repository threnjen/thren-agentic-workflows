---
description: "Detect specialized tech stacks and load matching skills before starting work; holds the canonical Unity detection predicate. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family, so add each new consumer by name rather than widening the glob. This file is the only copy of the predicate; do not restate it elsewhere."
applyTo: "**/03-phase-execute.agent.md,**/03a-feature-plan-expander.agent.md,**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/03f-prod-code-review.agent.md,**/03g-unity-visual-verification.agent.md,**/04-pr-review.agent.md,**/auditor-code.agent.md,**/auditor-infra.agent.md,**/auditor-refactor.agent.md,**/auditor-security.agent.md,**/single-feature-agent.agent.md"
---

Check whether the project uses a specialized tech stack with a matching skill. Look for `.github/copilot-instructions.md` naming a stack, or framework-specific project files: `package.json` for Node.js, `pyproject.toml` for Python, and the Unity predicate below. When a matching skill exists, **load and read it before you proceed**. It holds stack-specific rules and known pitfalls.

## Canonical Unity Detection Predicate

This is the corpus's single definition. Every other site that decides "is this Unity?" states it in these terms. If one disagrees, this one wins.

> The repository is a Unity project if **any** of these holds:
> - `Assets/` and `ProjectSettings/` both exist at the repository root (standard layout)
> - `Assets/` and `ProjectSettings/` both exist inside one nested project directory, e.g. `game/Assets/` and `game/ProjectSettings/` (nested/monorepo layout)
> - `.github/copilot-instructions.md` identifies the project as Unity
> - The plan or phase document under work targets Unity, MonoBehaviour, or Unity-specific systems
>
> `*.asmdef` files corroborate a match but are **never required** — small Unity projects have none.

On a match, load `unity-development`, and load `unity-review-knowledge` too when you are reviewing or auditing.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: tech-stack-detection."* Then proceed normally.
