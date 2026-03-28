# Codebase Context

Quick-reference for AI agents working on this repository.

## What This Repo Is

- A **template repository** of `AGENTS.md` and style guide files for Claude Code
- Contains **no runnable code** — only Markdown documentation
- Two language variants: Node.js/TypeScript and Python
- Users copy files into their own projects and customize them

## Folder Structure

```
README.md                       # Repo overview, usage instructions
docs/
  ARCHITECTURE.md               # Structure diagram and design decisions
  CODEBASE_CONTEXT.md           # This file
nodejs/
  AGENTS.md                     # Claude Code instructions for Node.js/TS projects
  docs/
    STYLE_GUIDE.md              # Node.js/TS coding conventions (loaded on demand)
python/
  AGENTS.md                     # Claude Code instructions for Python projects
  docs/
    STYLE_GUIDE.md              # Python coding conventions (loaded on demand)
```

## Key Facts

- Each `AGENTS.md` contains an "Extended Guides" section pointing to `docs/STYLE_GUIDE.md`
- The two AGENTS.md files share ~70% identical content (principles, process, testing, quality, agent ops)
- Language-specific differences: dependency tooling, property-based testing library, data modeling, style preferences
- No shared base file — each AGENTS.md is fully self-contained by design
- Style guides are intentionally separate from AGENTS.md to save agent context window space

## File Relationships

- `nodejs/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- `python/AGENTS.md` references `docs/STYLE_GUIDE.md` (relative to project root after copying)
- No cross-references between `nodejs/` and `python/` — they are independent

## Conventions

- All files are Markdown (`.md`)
- AGENTS.md uses H2 (`##`) for top-level sections, H3 (`###`) for subsections
- Style guides use H2 for the language header, H3 for topics
- Checklist items use `- [ ]` syntax
- Tables use pipe-delimited Markdown format

## When Editing

- **Adding a new section to both languages**: Update both `nodejs/AGENTS.md` and `python/AGENTS.md` to keep the shared structure in sync
- **Changing language-specific content**: Only edit the relevant language folder
- **Adding a new language**: Create a new top-level folder (e.g., `go/`) with the same `AGENTS.md` + `docs/STYLE_GUIDE.md` structure
- **Updating README.md**: Keep the structure tree, usage instructions, and comparison table current

## Do Not

- Do not add runnable code, build scripts, or CI/CD configuration — this is a docs-only repo
- Do not create a shared base file and use includes/inheritance — each AGENTS.md must be independently copyable
- Do not add deployment or infrastructure documentation
- Do not reference specific project names or URLs in the templates — they must be generic
- Do not merge the style guide into AGENTS.md — the separation is intentional for context window efficiency
