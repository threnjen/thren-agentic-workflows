---
description: "Checks for critical documentation files (README.md, CODEBASE_CONTEXT.md) during discovery and recommends running @Docs Writer if missing. Audience is DERIVED: pipeline stages 01-02, the planning agents."
applyTo: "source_of_truth/agents/0[12]-*.agent.md"
---

# Documentation Freshness Check

After discovery, check whether these critical documentation files exist:
- `README.md` (repo root)
- `docs/CODEBASE_CONTEXT.md`

If either file is missing and the repository is not genuinely brand new, spawn `@Docs Writer` as a subagent to create the missing documentation before continuing. Do not proceed until the files exist.

If the repository is genuinely brand new with nothing substantive to report yet, note that exception and continue.

Do not treat this as a user-approval gate. The missing documentation is a bootstrap dependency, not an optional follow-up.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: documentation-freshness-check."* Then proceed normally.
