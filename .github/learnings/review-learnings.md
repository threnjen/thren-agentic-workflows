# Review Learnings

## 2026-04-14: Redundant intro lines after consolidation

- **Pattern:** When consolidating a bulleted list into a single sentence, the original section's intro line often becomes redundant with the new consolidated sentence. Both the intro and the sentence start with the same directive (e.g., "Exclude these…" followed by "Exclude anything…").
- **Impact:** Adds unnecessary tokens and reads awkwardly — directly contradicts the goal of token reduction.
- **Watch for:** Any time a list is being condensed into a sentence, check whether the section's intro line is now subsumed by the consolidated text.

## 2026-04-14: ARCHITECTURE.md not updated when adding instruction/skill files

- **Pattern:** When creating new `.github/instructions/` or `.github/skills/` files, the implementation updated `docs/CODEBASE_CONTEXT.md` (file count, folder structure) but missed updating the instructions table and mermaid diagram in `docs/ARCHITECTURE.md`.
- **Impact:** Documentation falls out of sync — ARCHITECTURE.md becomes inaccurate for downstream agents and human readers relying on it for the instruction→agent mapping.
- **Watch for:** Any implementation that adds or removes instruction or skill files. Verify both `CODEBASE_CONTEXT.md` AND `ARCHITECTURE.md` are updated (mermaid diagram nodes + summary tables).
