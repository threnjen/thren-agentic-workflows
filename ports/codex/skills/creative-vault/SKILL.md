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
    project-context.md
    session-logs/
    user-patterns.md
```

## Boundary

Read `canon/` and `drafts/` before answering, so a contradiction against established
worldbuilding gets flagged rather than repeated. Never propose an edit to either, and never
write into them.

Only `Creative - Scribe` can write at all. The boundary above is a working rule for the
scribe; the guarantee that the editor cannot write is the absent tool grant.

## Project Context

`_editor-notes/project-context.md` is the agent's orientation file. Read it at the start of
every session, before the first substantive response. It exists so the writer can leave a
project for six months, come back, and have both of you re-oriented in one read.

It has two halves, and the difference between them is the whole design.

**The record** is fact: names, files, threads, decisions the writer declared, contradictions
with both halves cited. Everything in it is something the writer stated or something that
exists on disk.

**The reading** is the agent's own words: the synopsis, the worldbuilding restatement, the
scene list. These are paraphrase, and they are deliberate. A restatement in the agent's words
shows the writer whether the agent has actually understood the world — and a wrong one is
worth more than no summary at all, because it is diagnostic. The writer should read it as a
comprehension check and correct it.

The file ends with the commit SHA it was built from, so the next session can tell in one
command whether it is still current.

Write both halves under Reflect discipline: restate, never extend. `creative-compliance`
governs what that permits.

### Marking and Trust

Every reading section carries this line directly under its heading:

```markdown
> Agent restatement, not canon. Last written 2026-08-20. Correct anything wrong here.
```

**A reading section is never a source.** Do not cite it, do not treat a fact that appears only
there as established, and never build a later reading on an earlier one. Re-derive from canon
before relying on anything. Without this rule the agent's own paraphrase gets read back as the
writer's fact three sessions later, and a misunderstanding hardens into canon nobody wrote.

The record half is citable, because it holds the writer's own statements.

### The Record

| Section | Content | Source |
|---|---|---|
| Vault map | Canon subdirectories and what each holds | Directory listing |
| Cast | Character names, spelled as the writer spells them, with the canon file each is defined in | `canon/characters/` |
| Places and factions | Same shape as Cast | `canon/world/` |
| Threads | Plot thread labels the writer uses, and where each is established | `canon/plot/`, writer's own words |
| Stated decisions | Choices the writer declared settled, quoted or near-verbatim | Session logs |
| Open contradictions | Two canon statements that cannot both hold, both cited | Canon reads |
| Open questions | Questions the **writer** left open, quoted with a citation | The writer's own docs and session logs |
| Built from | The canon and draft files read to build it, and the date | Mechanical |

**Open questions is the writer's list, not the agent's.** Record only a question the writer
actually posed — a `TODO`, a note to self, an unanswered question in a canon file, something
they said in session. A gap the agent noticed is a diagnosis and belongs in a response, not
in this file. If the distinction is unclear for a given item, leave it out and ask.

### The Reading

| Section | Content |
|---|---|
| Synopsis | What is known of the story so far, in the agent's own words. What happens, who it happens to, where it stands. Say plainly what is unwritten or undecided rather than smoothing over the gap. |
| Worldbuilding as understood | The world restated in the agent's own words — how it works, what governs it, what is scarce, who holds power. This is the comprehension check. Getting it wrong visibly is the point. |
| Key scenes | Scenes that exist in `drafts/` or `scene-summaries/`, each with a one- or two-line synopsis and its file. Scenes only, not chapters the writer has merely planned. |
| Tone | How the book reads, in the agent's own words — register, distance, humor, how much dread it carries, what genre a reader would shelve it under. Describe the tone the prose actually produces, not the tone it seems to aim for. |

Each reading section restates. None of them proposes, extends, resolves, or evaluates. The
test for any sentence: could the writer read it and say *"no, that's not what I wrote"*? If
so it is a restatement and belongs. If instead they would say *"huh, I hadn't thought of
that"*, it is a contribution and does not.

Tone is the exception that proves the rule, and it is worth stating why it is allowed. Naming
the tone is a report on the prose the writer has already written, the way a reader would
describe it after finishing. It stays restatement as long as it describes the effect and stops
short of prescribing one. *"Wry, close third, more dread than the plot has yet earned"* is a
reading. *"This should be funnier"* is a diagnosis, and Diagnose is a live response, not a
stored verdict. Tone read wrong is as useful as worldbuilding read wrong: it tells the writer
their subtext is not landing.

### What Never Goes In

- A name, event, mechanic, character trait, or place the writer has not written down. The
  reading restates their world. It never adds to it.
- A resolution to a listed contradiction. List both halves and stop.
- An assessment of quality, readiness, or what needs work. That is Diagnose, and Diagnose is
  a live response to the writer, not a stored verdict about their book.
- A theme or meaning the writer has not stated. Describing what happens is restatement;
  declaring what it is *about* is interpretation. Quote their words if they wrote it.
- A question the agent thought of. See the record above.

### The Trailer

The last line of the file is the commit the file was built from:

```markdown
git_sha: 4f2a9c1e8b3d5a70c26f18e94b0d7a3c5e2f8b19
```

Write it whenever any part of the file is written, from the vault's current `HEAD`. When the
vault is not a git repository, write `git_sha: none` and leave it there — an unversioned vault
is normal, and the sync check simply reports nothing to compare.

The SHA is what makes the file self-dating. Without it the only way to know whether the record
still matches the vault is to re-read every canon file at every session start.

### Sync At Session Start

Before the first substantive response, and before trusting anything in this file:

1. Spawn `Creative - Vault Sync` with the vault root and the recorded `git_sha`.
2. On `up-to-date`, the record stands. Read on.
3. On `no-baseline` or `not-a-git-repo`, the file cannot be dated. Say so in one line and
   treat the record as unverified until it is checked against canon.
4. On a newer commit, read the canon and draft files the diff names — those files only, not
   the whole vault. Update the record for what changed, rewrite whole any reading section the
   changes made wrong, and write the new SHA. Say what you are updating and why, then spawn
   the scribe.

A dirty working tree means the writer has uncommitted changes. Say so and read the changed
files, but do not advance the SHA past `HEAD` — the recorded SHA names a commit, never a
working state.

### Maintaining It

Update the **record** when a turn produces something the next session would otherwise re-ask:

- the writer states a new fact, name, or settled decision
- the writer changes one that is already recorded
- a contradiction opens or the writer closes one
- the writer raises or answers an open question
- a canon file is added, renamed, or removed

Rewrite a **reading** section when the material under it moved enough that the restatement is
now wrong — a scene drafted, a rule of the world changed, a thread resolved. Rewrite it whole
rather than patching a sentence, and re-derive it from canon rather than from the version on
the page. Restamp the date.

Do not update for an ordinary exchange. Most turns change nothing.

Every update is a visible action: name what you are writing and why, then spawn the scribe.
Never write to this file silently.

Keep the record short enough to scan at session start. When a section outgrows that, replace
the detail with a pointer to the canon file — the record's job is to say where a thing lives,
not to hold a second copy of it. The reading is allowed to be longer, because re-orientation
is what it is for, but it is a page and not a treatment.

When the file is missing, offer to build it and say what it will contain. When the record
disagrees with canon, canon wins and the file gets corrected — flag the disagreement rather
than quietly overwriting. When the writer corrects a reading section, that correction is a
statement by the writer: record it.

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
