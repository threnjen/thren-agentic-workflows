---
description: "Bootstraps agent context by reading docs/CODEBASE_CONTEXT.md before discovery. Reduces redundant codebase scanning for all agents."
applyTo: "source_of_truth/agents/**"
baseline: true
---

# Codebase Context Bootstrap

Read `docs/CODEBASE_CONTEXT.md` first when it exists in the repository root. Use it as your initial context. Avoid a broad rescan. Explore only details that relate to the task. If the file does not exist, continue normally. Do not fail. Do not ask the user to create the file.

Skip this step when the task needs no exploration. Examples include writing a commit message, committing pipeline records, or generating templates from a plan that already lists its files. The **handed-scope exception** applies when the input includes the agent's file list. A reviewer scoped to an implementation record's "Files Changed" table is one example. An agent body may invoke the exception by name. The agent body may not override this instruction in any other way.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: codebase-context-bootstrap."* Then proceed normally.
