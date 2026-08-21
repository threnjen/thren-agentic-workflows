# Project Roadmap: github-agents-source-of-truth

## Vision

One authored corpus of agents, skills, and instructions that propagates to every harness, partitioned by authoring profile so unrelated bodies of work cannot contaminate each other.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Creative Writing Profile and Developmental Editor Toolkit | Complete | None | Large | Creative agent roster, profile instruction with skill allow-list, four creative skills, baseline trim, guard tests, and user documentation. |

## Constraints & Non-Goals

- **`profile: technical` is never written.** An absent `profile:` key means technical. `profile: creative` is the only opt-in token, so contributors adding technical assets learn nothing new.
- **Propagation is a manual maintainer step.** Agents edit `source_of_truth/` only and never regenerate `ports/` or `.github/`.
- **Isolation is enforced at build time, not at runtime.** Instruction bodies are inlined as literal text, so every harness receives a self-contained file and no per-harness feature is relied upon.
- **Skill isolation cannot be made hard.** The skill catalog is global and description-matched, and `map_tools_for_claude` grants `Skill` to every Claude agent. Allow-lists are prose; documentation must say so.
- Not building the standalone Creative Editor Toolkit harness. That is a separate product in `cf-app-crucible-harness-extension`.

## Architecture Notes

- Authoring profiles partition instruction inlining in `applicable_instructions` (`scripts/propagate_master_assets.py`). The gate is symmetric: a technical instruction never reaches a creative agent, and a creative instruction never reaches a technical one.
- The agent glob is flat (`*.md`), so asset families are filename prefixes rather than subdirectories.
- Tool grants are all-or-nothing and never path-scoped. Write protection is achieved by withholding `edit` from an agent entirely, and by isolating the write bit in the smallest possible agent.
- The user-global baseline (`source_of_truth/baseline/baseline-instructions.md`, spliced by `deploy_agents.py`) is profile-blind by construction. Anything that must not reach a creative session cannot live there.
- A baseline section is retired in two moves: drop it from `BASELINE_SECTIONS` to stop rewriting it, and list it in `RETIRED_BASELINE_SECTIONS` to delete the block a previous deploy already wrote. Dropping alone leaves a retired rule in force on every machine that already deployed it.
