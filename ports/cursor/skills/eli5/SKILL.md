---
name: eli5
description: "Explain one named subject at three depths in a single reply — everyday words, then the working parts, then the full technical picture. Use when the user runs /eli5 or asks for a layered explanation of a branch diff, a PR, some files, a pipeline, or a concept. Explains only; never reviews, fixes, or edits."
user-invocable: true
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# ELI5

Explain one subject three times in one reply. Make each pass deeper than the last. Write every pass
in plain technical English for an adult. The heading says "explain like I'm five". The prose does
not.

## The subject

The user names the subject. Never guess it.

Resolve the named subject before writing:

| The user says | You read |
|---|---|
| current branch vs main | The diff from HEAD to the local default branch. Use local `main`. Never substitute `origin/main`. |
| current PR, MR, or PR files | The open pull request for this branch and the files it changes. |
| this folder, these files | Read those paths. |
| this pipeline, this process | The documents and agent definitions that define it. |
| a named concept | The code, documents, or conversation that defines it. |

If the user names no subject or you cannot find the subject, ask one question that states what you
need. Then stop.

Read the source before explaining it. Do not explain the subject from its label alone.

This skill explains. It does not review files. It does not fix files. It does not change files. If
you find a bug while reading, report it in one line. Do not fix it.

## The output

Open with one sentence that names the subject. Then use exactly three headings in this order. Do
not skip a heading:

### ELI5

Explain what it is and why it matters. Use everyday words. Use an analogy only if it remains
accurate. Define jargon in the sentence where it first appears. Do not use baby talk. Do not write
"imagine you have a toy".

### ELI13

Explain how it works. Name the real parts and show one layer of the mechanism. Assume the reader
knows files, functions, APIs, and git.

### ELI18

Explain the full technical picture. Use precise terms. Explain constraints, tradeoffs, and what
goes wrong. Use plain English. Explain the source instead of pasting it.

## Rules for every section
- Keep the depths distinct. If two sections could swap places, one of them is wrong.
- Never skip a section because a later section covers it.
- Answer first. Put the main point in each section's opening sentence.
- Include one caveat in each section.
