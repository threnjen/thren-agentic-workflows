---
name: creative-vault
description: "Obsidian vault handling for creative writing sessions - vault detection by walking up for .obsidian/, the canon and drafts read-only boundary, session-log and user-patterns.md formats, scene-summary rollups, and macro/micro zoom. Use at the start of every creative session and whenever a response depends on the writer's established canon."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Creative Vault

## Detection

Run this before the first substantive response of a session.

1. Walk up from the working directory looking for a `.obsidian/` directory. The first one
   found is the vault root.
2. On no match, **ask for the vault path**. Never guess, never treat the working directory as
   a vault, and never proceed against an unknown root.
3. On a match with no `canon/` directory, ask which directories hold canon before treating
   any file as established fact.

Report the resolved root in one line and continue.

## Layout

```text
vault/
  canon/                  # writer-authored, source of truth      READ ONLY
    world/ characters/ plot/ themes/
  drafts/                 # manuscript material                   READ ONLY
  scene-summaries/        # macro rollups                         writable on explicit request
  _editor-notes/          # agent-authored, non-canonical         writable
    session-logs/
    user-patterns.md
```

## Boundary

Read `canon/` and `drafts/` before answering, so a contradiction against established
worldbuilding gets flagged rather than repeated. Never propose an edit to either, and never
write into them.

Only `Creative - Scribe` can write at all. The boundary above is a working rule for the
scribe; the guarantee that the editor cannot write is the absent tool grant.

## Session Logs

Append-only, one file per session under `_editor-notes/session-logs/`. Log the writer's own
words close to verbatim. Never replace them with a synthesis — a summary of the writer's
material reads as a creative contribution and is not what the log is for.

```markdown
### 2026-08-06 — Worldbuilding: Soča Valley political structure
- Q: What stops the river guilds from just seizing the capital themselves?
- User: [their raw response, captured close to verbatim]
- Flagged for canon check: contradicts canon/world/politics.md re: guild treaty terms
```

## User Patterns

`_editor-notes/user-patterns.md` is visible and editable by the writer. Three categories,
each with its own bar for logging:

| Category | What is logged | Bar | Phrasing rule |
|---|---|---|---|
| **Engagement** | Topics the writer visibly lights up on | Low — one instance is enough | Plain description |
| **Avoidance** | Topics the writer redirects away from | Medium — log the behavior | Describe the pattern, never infer why |
| **Craft tendencies** | Recurring strengths and gaps | High — repetition across sessions | Observation plus evidence, never a trait label |

Announce every update as an action. Never write to this file silently. Let it steer which
questions you reach for, but do not narrate it back unless the writer asks what you have
noticed.

## Zoom

- **Micro** — scene level: dialogue, description, individual beats. Suits drafting and local
  interrogation.
- **Macro** — structural: pacing across chapters, where threads cross, where stakes stall.
  Suits Diagnose and Adversarial.

Macro work reads `scene-summaries/` rather than full draft text, which is both a better view
of shape and the only way a long manuscript fits in context.

Scene summaries are written by the writer, or by the scribe under Reflect on explicit
request. Reflect's no-additions rule applies in full.

Zoom level is set by the writer or inferred and confirmed. Never assume it silently.
