# Creative Toolkit

A developmental editor for fiction, built from this corpus and isolated from it. The engineering
agents and the writing agents share a repository and nothing else.

## What You Get

| Agent | Invocation | Tools |
|---|---|---|
| `Creative - Developmental Editor` | user-invocable | read, search, todo, agent |
| `Creative - Scribe` | spawned by the editor | read, edit |
| `Creative - Compliance Check` | spawned by the editor | read |

The editor interrogates, reflects, diagnoses, and pressure-tests your material. It does not
supply plot, names, or fixes outside one narrow mode you have to ask for by name.

## Guarantees

Read this table before you trust the toolkit with a manuscript. **Hard** means a capability is
absent, so no instruction can talk the agent into it. **Soft** means a rule the agent follows.

| Guarantee | Kind | Why |
|---|---|---|
| The editor cannot modify canon or drafts | **Hard** | Its tool grant has no editing tool. Asking it to edit gets a missing capability, not a refusal. |
| No technical instruction reaches a creative agent | **Hard** | The propagator filters by profile at build time and inlines the surviving text into each generated file. Every harness receives a self-contained file, so the isolation does not depend on any harness feature. |
| No creative instruction reaches a technical agent | **Hard** | The same filter, in the other direction. |
| No creative instruction becomes a global Cursor rule | **Hard** | `propagate_cursor_rules_once` skips every non-technical doc unconditionally. |
| The skill allow-list | Soft | Every harness offers its whole skill catalog and matches by description. The allow-list is prose in the profile instruction; a technical skill whose description happens to match can still surface. A guard test keeps the list in sync with the skills on disk, which is a different thing from enforcing it at runtime. |
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
    project-context.md
    session-logs/
    user-patterns.md
```

Start the session from inside the vault. Detection walks up for `.obsidian/`. Outside a vault it
asks for the path rather than guessing, and a vault with no `canon/` directory prompts a question
before anything is treated as established fact.

`_editor-notes/user-patterns.md` is yours. Read it, edit it, delete it. Every write to it is
announced as an action.

## Project Context

`_editor-notes/project-context.md` is what the editor reads first, so you can leave a project
for six months, come back, and have both of you re-oriented in one read.

It has two halves.

**The record** is fact — your cast and place names spelled your way, the thread labels you use,
decisions you declared settled, open contradictions with both halves cited, and the questions
*you* left open. That last one is strict: a question the editor noticed is a diagnosis and
belongs in a response, not in your file. Only questions you actually posed get recorded, with a
citation.

**The reading** is the editor's own words — a synopsis of the story so far, the worldbuilding as
it understands it, and a list of the scenes that exist with a line or two each. This is a
comprehension check you can grade. If the worldbuilding section describes a world you don't
recognize, that is the most useful thing the file will ever tell you. Correct it, and the
correction becomes a statement of yours in the record.

Every reading section is stamped and marked as restatement, and the editor is forbidden from
citing one or building a later reading on an earlier one. It re-derives from canon each time.
That rule is what stops the editor's own paraphrase from being read back as your fact three
sessions later and hardening into canon nobody wrote.

Neither half proposes, resolves, or evaluates. No name or event you didn't write. No resolution
to a contradiction it lists. No verdict on whether the book is working — that's Diagnose, and
Diagnose is a live conversation, not a stored opinion about your book.

It is offered, not imposed. The editor builds it when you ask, updates the record when a turn
settles something a future session would re-ask, rewrites a reading section when the material
under it moved, and announces every change. Like everything under `_editor-notes/`, it is plain
Markdown you can read, correct, or delete. When the record disagrees with canon, canon wins.

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
