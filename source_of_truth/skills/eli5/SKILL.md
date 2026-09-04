---
name: eli5
description: "Explain one named subject at three depths in a single reply — everyday words, then the working parts, then the full technical picture. Use when the user runs /eli5 or asks for a layered explanation of a branch diff, a PR, some files, a pipeline, or a concept. Explains only; never reviews, fixes, or edits."
user-invocable: true
---

# ELI5

Explain one subject three times in one reply, each pass deeper than the last. Write every pass
in plain technical English for an adult. The heading says "explain like I'm five". The prose
does not.

## The subject

The user names the subject. Never guess it.

Resolve what they named before you write a word:

| The user says | You read |
|---|---|
| current branch vs main | The diff from HEAD to the local default branch. Use local `main`. Never substitute `origin/main`. |
| current PR, MR, or PR files | The open pull request for this branch, plus the files it changes. |
| this folder, these files | Those paths. |
| this pipeline, this process | The docs and agent definitions that define it. |
| a named concept | The code, docs, or conversation where it is defined. |

If no subject was given, or the one given cannot be found, ask one question naming what you
need, then stop.

Read the source before explaining it. A label is not enough to explain from.

This skill explains. It does not review, fix, or change files. If the reading turns up a bug,
say so in one line and leave it there.

## The output

Open with one sentence that names the subject. Then exactly three headings, in this order,
none skipped:

### ELI5

What it is and why anyone cares. Everyday words. An analogy is fine if it holds. Unpack any
jargon in the same sentence it appears. No baby talk, no "imagine you have a toy".

### ELI13

How it works. Name the real parts and show one layer of mechanism. Assume the reader knows
files, functions, APIs, and git.

### ELI18

The full technical picture. Precise terms, constraints, tradeoffs, and what goes wrong. Still
plain English, and still an explanation rather than a paste of the source.

## Rules for every section
- Keep the depths distinct. If two sections could swap places, one of them is wrong.
- Never skip a section on the grounds that a later one covers it.
- Answer first. The opening sentence of each section carries the point.
- One caveat per section.

