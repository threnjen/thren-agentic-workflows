---
name: creative-vault
description: Obsidian vault handling for creative writing sessions - vault detection by walking up for .obsidian/, the canon and drafts read-only boundary, session-log and user-patterns.md formats, scene-summary rollups, and macro/micro zoom. Use at the start of every creative session and whenever a response depends on the writer's established canon.
license: MIT
profile: creative
---

# Creative Vault

## Detection

Run this before the first substantive response of a session.

1. Walk up from the working directory looking for a `.obsidian/` directory. Treat the first
   matching directory as the vault root.
2. On no match, **ask for the vault path**. Never guess. Never treat the working directory as a
   vault. Never proceed against an unknown root.
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
    context/              # one file per content type
    session-logs/
    user-patterns.md
```

## Boundary

Read `canon/` and `drafts/` before answering. Flag contradictions against established
worldbuilding instead of repeating them. Never propose an edit to either directory. Never write
into them.

Only `Creative - Scribe` can write at all. The boundary above is a working rule for the
scribe. The absent tool grant guarantees that the editor cannot write.

## Project Context

The editor reads `_editor-notes/context/` first. The writer can leave a project for six months
and return with both of you re-oriented in one read.

It is a directory, not one file. Use one file per content type. A change to the cast does not
rewrite the plot. The writer can correct one file without reading the rest.

```text
_editor-notes/context/
  index.md            # the map: what every other file holds, and the git_sha
  characters.md       # cast
  setting.md          # places, factions, how the world works
  plot.md             # threads, settled decisions, contradictions, synopsis
  scenes.md           # scenes that exist, one or two lines each
  style.md            # tone and voice as the prose reads
  open-questions.md   # questions the WRITER left open
  themes.md           # interpretive layer only, absent by default
```

Every file except `index.md` and `themes.md` has the same two halves, and the difference
between them is the whole design.

**The record** is fact: names, files, threads, decisions the writer declared, contradictions
with both halves cited. Everything in it is something the writer stated or something that
exists on disk.

**The reading** is the agent's own words. A restatement in the agent's words shows whether the
writer understood the material. A wrong restatement is more useful than no summary because it
diagnoses misunderstanding. The writer should read it as a comprehension check and correct it.

`index.md` is the entry point. The editor loads it when a session starts. It holds the one
`git_sha` trailer for the whole directory. `themes.md` exists only while the interpretive layer
is on. See `creative-modes`.

Write both halves under Reflect discipline: restate, never extend. `creative-compliance`
governs what that permits, and it also governs the two rules below on how the restatement is
worded.

### Marking and Trust

Every reading section carries this line directly under its heading:

```markdown
> Agent restatement, not canon. Last written 2026-08-20. Correct anything wrong here.
```

**A reading section is never a source.** Do not cite it. Do not treat a fact that appears only
there as established. Never build a later reading on an earlier one. Re-derive from canon before
relying on anything. Without this rule, the writer reads the agent's own paraphrase as the writer's
fact three sessions later. A misunderstanding then hardens into canon nobody wrote.

The record half is citable, because it holds the writer's own statements.

### Plainer Than The Writer

Write every reading section **below** the writer's natural level. This rule is counterintuitive.
A polished phrasing of the writer's own material becomes the phrasing they reach for when they
read it at the start of every session. The summary should remind them what they wrote, not offer
them a better way to write it.

- Use the writer's nouns for the writer's things. Keep their spellings, labels, and terms.
- For every other word, choose the plainest one that is still accurate.
- Use short declarative sentences. State one fact per sentence.
- Do not use a metaphor, image, or figure of speech the writer did not write first.
- Do not use a word the writer has not used unless no plainer accurate substitute exists.

The test: if a sentence in a reading section is more elegant than the writer's own prose, it is
wrong even though it is accurate. Rewrite it flatter.

`style.md` is the one place where a precise term can replace a plain one, because naming a
register needs the word for that register. It still takes the plainest word that is accurate.

### index.md

`index.md` is a table of contents, not a summary. The editor loads it at every session start. Its
job is to say what exists and where. The editor can then open the two files needed for that
session instead of all seven.

It holds three things and nothing else:

1. **The map** — one row per context file.

   ```markdown
   | File | Holds | Last written |
   |---|---|---|
   | `characters.md` | Cast, with the canon file each is defined in | 2026-08-20 |
   | `setting.md` | Places, factions, how the world works | 2026-08-18 |
   | `plot.md` | Threads, settled decisions, contradictions, synopsis | 2026-08-20 |
   | `scenes.md` | Scenes that exist, one or two lines each | 2026-08-11 |
   | `style.md` | Tone and voice as the prose reads | 2026-08-11 |
   | `open-questions.md` | Questions the writer left open | 2026-08-20 |
   ```

   List a file only if it exists. A missing row means a missing file, which is how the editor
   knows to offer to build it.

2. **The vault map** — the canon subdirectories and what each holds, plus the canon and draft
   files the directory was built from, and the date.

3. **The trailer** — the `git_sha`, on the last line.

**A row says where a thing lives. It never says what the thing says.** If `Holds` describes the
cast rather than naming its file, the index has become an eighth summary. That summary drifts
from the seven files it points to. Keep every `Holds` cell to a noun phrase.

`index.md` has no reading half. It restates nothing, so the reading-level rule and the
marking line do not apply to it.

Update a row's `Last written` in the same action that writes the file it points at. An index
that dates a file it did not just write is worse than no date, because it will be believed.

### The Files

| File | Record half | Reading half |
|---|---|---|
| `index.md` | The map above: one row per context file, the vault map, and the `git_sha` trailer | none |
| `characters.md` | Character names, spelled as the writer spells them, with the canon file each is defined in | Who each one is and what they want, in the agent's own words |
| `setting.md` | Places and factions, same shape as characters | How the world works, what governs it, what is scarce, who holds power. This is the comprehension check. Getting it wrong visibly is the point. |
| `plot.md` | Thread labels the writer uses and where each is established; decisions the writer declared settled, quoted or near-verbatim; contradictions where two canon statements cannot both hold, both cited | The synopsis: what is known of the story so far, what happens, who it happens to, where it stands. Say plainly what is unwritten or undecided rather than smoothing over the gap. |
| `scenes.md` | none | Scenes that exist in `drafts/` or `scene-summaries/`, each with a one- or two-line synopsis and its file. Scenes only, not chapters the writer has merely planned. |
| `style.md` | Any statement the writer made about their own voice or intent, quoted | Tone as the prose reads: register, distance, humor, how much dread it carries, what shelf a reader would put it on. Describe the tone the prose produces, not the tone it seems to aim for. |
| `open-questions.md` | Questions the **writer** left open, quoted with a citation | none |
| `themes.md` | none | Interpretive layer only. Absent unless the writer turned it on. |

**`open-questions.md` is the writer's list, not the agent's.** Record only a question the
writer actually posed — a `TODO`, a note to self, an unanswered question in a canon file,
something they said in session. A gap the agent noticed is a diagnosis and belongs in a
response, not in this directory. If the distinction is unclear for a given item, leave it out
and ask.

Tone in `style.md` is the exception that proves the restatement rule, and it is worth stating
why it is allowed. Naming the tone is a report on prose the writer has already written, the way
a reader would describe it after finishing. It stays restatement as long as it describes the
effect and stops short of prescribing one. *"Wry, close third, more dread than the plot has yet
earned"* is a reading. *"This should be funnier"* is a diagnosis, and Diagnose is a live
response, not a stored verdict. Tone read wrong is as useful as worldbuilding read wrong: it
tells the writer their subtext is not landing.

Each reading section restates. None of them proposes, extends, resolves, or evaluates. The
test for any sentence: could the writer read it and say *"no, that's not what I wrote"*? If so
it is a restatement and belongs. If instead they would say *"huh, I hadn't thought of that"*,
it is a contribution and does not.

### What Never Goes In

- A name, event, mechanic, character trait, or place the writer has not written down. The
  reading restates their world. It never adds to it.
- A resolution to a listed contradiction. List both halves and stop.
- An assessment of quality, readiness, or what needs work. That is Diagnose, and Diagnose is
  a live response to the writer, not a stored verdict about their book.
- A theme, symbol, or meaning the writer has not stated. Describing what happens is restatement.
  Declaring what it is *about* is interpretation. That belongs in `themes.md`,
  which exists only when the writer turned the interpretive layer on.
- A question the agent thought of. See `open-questions.md` above.

### The Trailer

The last line of `index.md` is the commit the directory was built from:

```markdown
git_sha: 4f2a9c1e8b3d5a70c26f18e94b0d7a3c5e2f8b19
```

Write it whenever you write any file in the directory, using the vault's current `HEAD`. One SHA
covers the whole directory — update and date the files together. When the vault is not a git
repository, write `git_sha: none` and leave it there. An unversioned vault is normal, and the
sync check simply reports nothing to compare.

The SHA is what makes the directory self-dating. Without it the only way to know whether the
record still matches the vault is to re-read every canon file at every session start.

### Sync At Session Start

Do this at the **start** of the conversation, before the first substantive response and before
trusting anything in the directory. Not at the end: writers stop talking, and a wrap-up step
that depends on the session ending cleanly will not run.

1. Read `index.md` first. It is the map of what exists, when each file was last written, and the
   `git_sha`. Open other files as the session needs them rather than all at once.
2. Spawn `Creative - Vault Sync` with the vault root and that `git_sha`.
3. On `up-to-date`, the record stands. Read on.
4. On `no-baseline` or `not-a-git-repo`, the directory cannot be dated. Say so in one line and
   treat the record as unverified until it is checked against canon.
5. On a newer commit, read the canon and draft files named by the diff. Read those files only,
   not the whole vault. Update the record in the files the changes touch. Rewrite each affected
   reading section in full. Write the new SHA to `index.md`. State what you are updating and why.
   Then spawn the scribe. Update each rewritten file's `Last written` row in `index.md` in the
   same pass.

Rewrite only the files the diff touches. A commit that changes one character file does not
rewrite `plot.md`, and that separation is the reason the directory is split.

A dirty working tree means the writer has uncommitted changes. Say so. Read the changed files,
but do not advance the SHA past `HEAD` — the recorded SHA names a commit, never a working state.

### Maintaining It

Update the **record** when a turn produces something the next session would otherwise re-ask:

- the writer states a new fact, name, or settled decision
- the writer changes one that is already recorded
- a contradiction opens or the writer closes one
- the writer raises or answers an open question
- a canon file is added, renamed, or removed

Rewrite a **reading** section when the material under it moved enough that the restatement is
now wrong — a scene drafted, a rule of the world changed, a thread resolved. Rewrite it whole
rather than patching a sentence. Re-derive it from canon rather than from the version on the
page.

Do not update for an ordinary exchange. Most turns change nothing. Touch only the files the
change actually reaches.

Every update is a visible action. Name which file you are writing and why. Then spawn the scribe.
Never write to this directory silently. Every write to a context file also updates that file's
row in `index.md` — a new file gets a row, and a rewritten one gets a fresh date.

Keep each record short enough to scan. When a record outgrows that limit, replace its detail with
a pointer to the canon file. The record's job is to say where a thing lives, not to hold a second
copy of it. A reading may be longer because it supports re-orientation. Keep each reading to a
page, not a treatment.

When a file is missing, offer to build it. Say what it will contain. When the record disagrees
with canon, let canon win and correct the file. Flag the disagreement instead of quietly
overwriting it. When the writer corrects a reading section, that correction is a statement by
the writer: record it.

## Session Logs

Keep session logs append-only. Use one file per session under `_editor-notes/session-logs/`. Log
the writer's own words close to verbatim. Never replace them with a synthesis — a summary of the
writer's material reads as a creative contribution and is not what the log is for.

```markdown
### 2026-08-06 — Worldbuilding: Soča Valley political structure
- Q: What stops the river guilds from just seizing the capital themselves?
- User: [their raw response, captured close to verbatim]
- Flagged for canon check: contradicts canon/world/politics.md re: guild treaty terms
```

## User Patterns

`_editor-notes/user-patterns.md` is visible and editable by the writer. It has three categories,
each with its own bar for logging:

| Category | What is logged | Bar | Phrasing rule |
|---|---|---|---|
| **Engagement** | Topics the writer visibly lights up on | Low — one instance is enough | Plain description |
| **Avoidance** | Topics the writer redirects away from | Medium — log the behavior | Describe the pattern, never infer why |
| **Craft tendencies** | Recurring strengths and gaps | High — repetition across sessions | Observation plus evidence, never a trait label |

Announce every update as an action. Never write to this file silently. Use it to choose which
questions you reach for. Do not narrate it back unless the writer asks what you have noticed.

## Zoom

- **Micro** covers scene level: dialogue, description, and individual beats. Use it for drafting
  and local interrogation.
- **Macro** covers structure: pacing across chapters, where threads cross, and where stakes
  stall. Use it for Diagnose and Adversarial.

Macro work reads `scene-summaries/` instead of full draft text. This gives a better view of shape
and is the only way a long manuscript fits in context.

The writer writes scene summaries. The scribe may write them under Reflect on explicit request.
Reflect's no-additions rule applies in full.

The writer sets the zoom level, or the agent infers and confirms it. Never assume it silently.
