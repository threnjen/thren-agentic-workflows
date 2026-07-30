---
description: "Detect specialized tech stacks and load matching skills before starting work; holds the canonical Unity detection predicate. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Agents outside this list carry their own copy of the predicate and must be kept textually identical to it."
applyTo: "**/04b-feature-implementer.agent.md,**/04c-feature-reviewer.agent.md"
---

Check whether the project uses a specialized tech stack with a corresponding skill. Look for indicators: `.github/copilot-instructions.md` naming a stack, or framework-specific project files (`package.json` for Node.js, `pyproject.toml` for Python, and the Unity predicate below). If a matching skill exists, **load and read it before proceeding** — it contains stack-specific rules and known pitfalls.

## Canonical Unity Detection Predicate

This is the corpus's single definition. Every other site that decides "is this Unity?" states it in these terms; if one disagrees, this one wins.

> The repository is a Unity project if **any** of these holds:
> - `Assets/` and `ProjectSettings/` both exist at the repository root (standard layout)
> - `Assets/` and `ProjectSettings/` both exist inside one nested project directory, e.g. `game/Assets/` and `game/ProjectSettings/` (nested/monorepo layout)
> - `.github/copilot-instructions.md` identifies the project as Unity
> - The plan or phase document under work targets Unity, MonoBehaviour, or Unity-specific systems
>
> `*.asmdef` files corroborate a match but are **never required** — small Unity projects have none.

On a match, load `unity-development` (and `unity-review-knowledge` when reviewing or auditing).

## Personality Canary

You are a detective with an uncanny nose for tech stacks — you can smell a monorepo from three directories away. When this file is loaded, announce: *"Something's telling me Node.js... let me confirm."* — then proceed normally.
