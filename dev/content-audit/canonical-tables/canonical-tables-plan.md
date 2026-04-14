# Plan: Canonical Documentation Tables

Eliminate the cascade documentation problem — Skills, Instructions, and Agent inventory tables are repeated in 4 docs. Establish canonical locations and replace duplicates with links.

## Acceptance Criteria

- AC1: Agent inventory canonical in `.github/agents/README.md`; README.md, ARCHITECTURE.md, CODEBASE_CONTEXT.md replaced with brief summary + link
- AC2: Skills table canonical in `docs/ARCHITECTURE.md`; README.md, CODEBASE_CONTEXT.md, agents/README.md replaced with brief summary + link
- AC3: Instructions table canonical in `docs/ARCHITECTURE.md`; README.md, CODEBASE_CONTEXT.md, agents/README.md replaced with brief summary + link
- AC4: Pipeline description canonical in `.github/agents/README.md`; README.md shortened to brief overview + link
- AC5: All cross-references use relative links that work from each file's location

## Non-Goals

- Do not change the canonical source content itself
- Do not reorganize file hierarchy
