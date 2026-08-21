# Creative Toolkit

A developmental editor for fiction, built from this corpus and isolated from it. The engineering
agents and the writing agents share a repository and nothing else.

## What You Get

| Agent | Invocation | Tools |
|---|---|---|
| `Creative - Developmental Editor` | user-invocable | read, search, todo, agent |
| `Creative - Scribe` | spawned by the editor | read, edit |
| `Creative - Compliance Check` | spawned by the editor | read |
| `Creative - Vault Sync` | spawned by the editor | execute (read-only git) |

The editor interrogates, reflects, diagnoses, and pressure-tests your material. It does not
supply plot, names, or fixes outside one narrow mode you have to ask for by name.

## Guarantees

Read this table before you trust the toolkit with a manuscript. **Hard** means a capability is
absent, so no instruction can talk the agent into it. **Soft** means a rule the agent follows.

| Guarantee | Kind | Why |
|---|---|---|
| The editor cannot modify canon or drafts | **Hard** | Its tool grant has no editing tool. Asking it to edit gets a missing capability, not a refusal. |
| Nothing writes into `canon/` or `drafts/` | **Hard**, once the hook is installed | The canon guard hook denies the write before it happens, from any tool, including a shell command that would reach them. Uninstalled, this drops back to the tool grant on the row above. |
| No technical instruction reaches a creative agent | **Hard** | The propagator filters by profile at build time and inlines the surviving text into each generated file. Every harness receives a self-contained file, so the isolation does not depend on any harness feature. |
| No creative instruction reaches a technical agent | **Hard** | The same filter, in the other direction. |
| No creative instruction becomes a global Cursor rule | **Hard** | `propagate_cursor_rules_once` skips every non-technical doc unconditionally. |
| The skill allow-list | Soft | Every harness offers its whole skill catalog and matches by description. The allow-list is prose in the profile instruction; a technical skill whose description happens to match can still surface. A guard test keeps the list in sync with the skills on disk, which is a different thing from enforcing it at runtime. |
| The interpretive layer stays off until you ask | Soft | It is a rule in `creative-modes` and a violation class in `creative-compliance`, checked by the same two-layer compliance pass. Nothing at the harness level can compel it. |
| Output does not read as AI-generated prose | Soft | A named violation class with an explicit tell list, caught by the compliance pass. Judgment, not a gate. |
| Reading sections stay plainer than your prose | Soft | Same mechanism: a violation class with a worked example, checked, not enforced. |
| The compliance pass runs every turn | Soft | No agent definition can compel a subagent call. The editor self-checks inline and spawns the compliance agent for substantive responses. Two layers of discipline, not a gate. |
| The scribe writes only under `_editor-notes/` and `scene-summaries/` | Soft | Tool grants in this corpus are all-or-nothing. The scribe holds the write bit for the whole filesystem and is instructed to refuse everything else. |

Path-scoped filesystem permissions and a forced two-pass turn loop are what the standalone
harness in the master spec exists to provide. This corpus cannot provide them, and nothing here
claims to.

## Vault Setup

```text
vault/
  .obsidian/              # what detection looks for
  canon/                  # your source of truth       READ ONLY
    world/ characters/ plot/ themes/
  drafts/                 # manuscript                 READ ONLY
  scene-summaries/        # macro rollups              written on request
  _editor-notes/          # agent-authored             written freely
    context/              # one file per content type
    session-logs/
    user-patterns.md
```

Start the session from inside the vault. Detection walks up for `.obsidian/`. Outside a vault it
asks for the path rather than guessing, and a vault with no `canon/` directory prompts a question
before anything is treated as established fact.

`_editor-notes/user-patterns.md` is yours. Read it, edit it, delete it. Every write to it is
announced as an action.

## Project Context

`_editor-notes/context/` is what the editor reads first, so you can leave a project for six
months, come back, and have both of you re-oriented in one read.

It is a directory, not one document, so a change to your cast does not rewrite your plot and
you can correct one file without reading the rest.

```text
_editor-notes/context/
  index.md            # the map: what every other file holds, and the git_sha
  characters.md       # your cast
  setting.md          # places, factions, how the world works
  plot.md             # threads, settled decisions, contradictions, synopsis
  scenes.md           # the scenes that exist, a line or two each
  style.md            # tone and voice as your prose reads
  open-questions.md   # the questions YOU left open
  themes.md           # only if you turn the interpretive layer on
```

`index.md` is the entry point — the one file the editor loads when a session starts. It is a
table of contents: one row per context file saying what that file holds and when it was last
written, plus your vault map and the SHA. Nothing else. A row names the file that describes
your cast; it never describes your cast. The moment it starts doing that it has become an
eighth summary drifting from the seven it points at.

The index is what lets the editor open the two files a session needs instead of all seven, and
it is how it knows a file is missing and worth offering to build. Every write to a context file
updates that file's row in the same action, so a date you see in the index is a date the editor
just wrote.

Every file except `index.md` and `themes.md` has two halves.

**The record** is fact — your names spelled your way, the thread labels you use, decisions you
declared settled, contradictions with both halves cited. **The reading** is the editor's own
words, and it is a comprehension check you can grade. If `setting.md` describes a world you
don't recognize, that is the most useful thing the directory will ever tell you. Correct it,
and the correction becomes a statement of yours in the record.

`open-questions.md` is strict about whose questions: only ones you actually posed, with a
citation. A question the editor noticed is a diagnosis and belongs in a response, not in your
files.

`style.md` is there for subtext. It says how the book actually reads — register, distance,
humor, how much dread it carries, what shelf a reader would put it on — not how it seems to be
aiming. Tone read wrong tells you what you intended is not on the page yet.

Every reading section is stamped and marked as restatement, and the editor is forbidden from
citing one or building a later reading on an earlier one. It re-derives from canon each time.
That rule is what stops the editor's own paraphrase from being read back as your fact three
sessions later and hardening into canon nobody wrote.

### Written Plainer Than You Write

Every reading section is deliberately written **below** your natural level: your nouns for your
things, the plainest accurate word for everything else, one fact per sentence, no metaphor you
didn't write first.

This is on purpose and it is the same principle as the interpretive layer. A polished phrasing
of your own material, read back at the start of every session, becomes the phrasing you reach
for. The summary should remind you what you wrote, not offer you a better way to have written
it. If a line in a reading section reads more elegantly than your prose, that's a bug — tell the
editor and it will rewrite it flatter.

### Neither Half Interprets

No name or event you didn't write. No resolution to a contradiction it lists. No verdict on
whether the book is working — that's Diagnose, and Diagnose is a live conversation, not a stored
opinion about your book. No theme, symbol, or meaning you haven't stated: that lives in
`themes.md`, and only if you turn the layer on.

It is offered, not imposed. The editor builds the directory when you ask, updates the record
when a turn settles something a future session would re-ask, rewrites a reading when the
material under it moved, touches only the files a change actually reaches, and announces every
write. Like everything under `_editor-notes/`, these are plain Markdown you can read, correct,
or delete. When the record disagrees with canon, canon wins.

### Staying Current

The last line of `index.md` — the same file the editor loads first — is the commit the
directory was built from:

```markdown
git_sha: 4f2a9c1e8b3d5a70c26f18e94b0d7a3c5e2f8b19
```

If your vault is a git repository, the editor's first action of every session is to compare
that SHA against your current `HEAD`. When you have committed work since, it reads the files
the diff names — those files only — updates the record, rewrites any reading section the
changes made wrong, and tells you in one line what moved.

This runs at the **start** of the conversation, not the end. A wrap-up step that depends on you
saying goodbye never runs, because you'll just stop talking. It never advances the SHA past a
commit, so uncommitted work is reported as uncommitted rather than silently absorbed. An
unversioned vault records `git_sha: none` and skips the check.

## The Interpretive Layer

Off by default, in every session, including one where it was on last time.

While it's off, the editor will not tell you what your story is about — no themes, no symbols,
no reading of what a relationship is *really* doing. It also won't hint that it has one, and
won't ask whether you'd like to hear it. Offering is a way of delivering.

Turn it on with `layer: interpretive on`, "read the themes", or "what do you think this is
about". Turn it off with `layer: interpretive off`, or by starting a new session.

The reason for the default is not caution. An unrequested reading of your own story either
spoils a discovery you were walking toward, or plants an idea you didn't originate and can no
longer tell apart from your own. The second is worse and it's silent — you can't audit your own
sense of authorship after the fact. Think with you, not for you.

While the layer is on, interpretation is stored in `context/themes.md`. Turn it off and the
editor stops writing there. It leaves what's already written, because it's yours now, but won't
update it or read it back to you unprompted.

## Prose That Doesn't Read As Generated

A hard constraint, not a preference. It covers Generate, Copyedit, and every word the editor
writes into `_editor-notes/`.

`creative-compliance` names the tells the compliance pass checks for: the *"it's not X, it's
Y"* pivot, the rule-of-three where two would do, a closing sentence that restates the paragraph
more resonantly, stacked hedges, uniform sentence length, and a vocabulary list starting with
*delve* and *tapestry*. The repair is to rewrite flat — state it once, in the shortest true
sentence. Notes that come out dull are correct; a note isn't supposed to be good prose.

This is a soft guarantee in the same sense the compliance pass is: it's checked, by the editor
inline and by the compliance agent on substantive responses, but nothing enforces it at the
harness level.

## Installing the Canon Guard

The editor holds no editing tool, and the sync probe holds a shell only for read-only git.
Neither is meant to touch your prose. The hook makes that an enforcement rather than a promise,
which matters because generated text now carries provenance watermarking — one agent write into
a manuscript can mark your own prose as machine-authored, with nothing visible afterward to
tell you it happened.

Install it in your vault:

1. Copy the hook in and keep it executable.

   ```bash
   mkdir -p /path/to/vault/.claude/hooks
   cp source_of_truth/hooks/creative-canon-guard.py /path/to/vault/.claude/hooks/
   chmod +x /path/to/vault/.claude/hooks/creative-canon-guard.py
   ```

2. Register it in `/path/to/vault/.claude/settings.json`. If the file already has a `hooks`
   key, add this entry to the existing `PreToolUse` list rather than replacing it.

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash|Edit|Write|NotebookEdit",
           "hooks": [
             {
               "type": "command",
               "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/creative-canon-guard.py",
               "timeout": 10
             }
           ]
         }
       ]
     }
   }
   ```

3. Confirm it works. Ask the editor to write a line into a file under `canon/`. A correct
   result is a message beginning `BLOCKED:`. If the write succeeds, the hook is not registered.

The matcher covers write-capable tools only, which is deliberate: the hook denies an unreadable
payload rather than allowing it, and scoping the matcher keeps that strictness away from
ordinary reads. Reading your manuscript stays untouched — the editor cannot do its job without
it.

## Modes

Exactly one mode is active per response. The mode decides what the response may contain.
Default is **Diagnose**.

| Mode | You get |
|---|---|
| Interrogate | Questions only |
| Reflect | Your own material said back, compressed, with nothing added |
| Diagnose | What is not working and the evidence, with no fix attached |
| Adversarial | Diagnose, leading with the weakest point |
| Generate | One scoped answer to one explicit ask, then automatic return to the prior mode |
| Copyedit | Sentence-level phrasing in your voice, no new ideas |

Switch with `mode: interrogate` or plain English. Delivery is separate and changes only on
command: **beta reader** softens the framing, **editor** does not cushion, **adversarial** leads
with the worst thing. The agent never adjusts delivery on its own read of your mood.

Zoom is separate again. **Micro** works a scene; **macro** reads `scene-summaries/` to see shape
across chapters. It is set by you or confirmed with you, never assumed.

## Authoring

Creative assets carry `profile: creative` in frontmatter. That token is the only thing that puts
an asset in this family, and it is the only profile anyone ever writes — an absent `profile:` key
means technical, so contributors adding engineering assets learn nothing new.

Agents in the family are named `creative-*.agent.md`. The name and the profile must agree, and a
guard test fails if they do not: the profile instruction's `applyTo` glob keys off the filename,
so a mismatch isolates an agent into an empty context instead of its own.

Adding a creative skill without adding it to the allow-list in
`source_of_truth/instructions/creative-profile.instructions.md` fails a test.
