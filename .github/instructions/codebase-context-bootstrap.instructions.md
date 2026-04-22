---
description: "Bootstraps agent context by reading docs/CODEBASE_CONTEXT.md before discovery. Reduces redundant codebase scanning for all agents."
applyTo: ".github/agents/**"
---

# Codebase Context Bootstrap

Before discovery/exploration, check whether `docs/CODEBASE_CONTEXT.md` exists in the repository root. If it exists, **read it first**.

## How to Use It

- Use it as your **starting orientation** to avoid broad rescans.
- Then continue normal discovery, focusing only on task-specific details.
- If the file does not exist, continue normally; do not fail or request file creation.
