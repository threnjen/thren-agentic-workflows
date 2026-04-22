---
description: "Checks for critical documentation files (README.md, CODEBASE_CONTEXT.md) during discovery and recommends running @Docs Writer if missing. Auto-loaded for planning agents."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md"
---

# Documentation Freshness Check

After discovery, check whether these critical documentation files exist:
- `README.md` (repo root)
- `docs/CODEBASE_CONTEXT.md`

If either file is missing, present this recommendation before continuing:

> **Documentation gap detected.** Missing: [list missing files].
>
> **Recommendation:** Run `@Docs Writer` to generate the missing docs before continuing.
>
> You may proceed without this step if the user explicitly confirms.

Wait for the user to acknowledge before continuing. If the user chooses to proceed without running Docs Writer, continue normally.
