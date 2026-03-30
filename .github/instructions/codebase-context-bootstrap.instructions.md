---
description: "Bootstraps agent context by reading docs/CODEBASE_CONTEXT.md before discovery. Reduces redundant codebase scanning for all agents."
applyTo: ".github/agents/**"
---

# Codebase Context Bootstrap

Before starting your discovery or exploration phase, check whether `docs/CODEBASE_CONTEXT.md` exists in the repository root. If it does, **read it first**. This file contains a dense, structured summary of the codebase — folder structure, key modules, entry points, naming conventions, patterns, and anti-patterns — written specifically for agent consumption.

## How to Use It

- Use it as your **starting orientation** — it answers most of the questions your discovery phase would otherwise spend time scanning for (tech stack, project structure, module layout, test patterns, key files)
- **Then continue your normal workflow** — proceed with your discovery/exploration phase, but focus on details specific to your task rather than re-scanning the entire codebase from scratch
- If the file does not exist, proceed with your normal discovery phase as usual — do not fail or ask the user to create it
