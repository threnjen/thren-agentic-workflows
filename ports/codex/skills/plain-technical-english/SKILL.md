---
name: plain-technical-english
description: "Rewrite existing text into plain technical English — a full pass that names the mode, flags each violation, and reports rule/original/rewrite per change. Use when asked to rewrite, tighten, clarify, or de-jargon a document, or when prose reads as dense, hedged, or easy to misread. The rules for text you are writing now are already carried by the `prose-standards` instruction; load this skill for the rewrite procedure and the full vocabulary rules. Never use on client-facing deliverables, marketing copy, or creative writing — client deliverables are governed by `engagement-client-voice` instead."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Plain Technical English

Two things make English hard to parse: words with more than one meaning, and sentences with more than one possible structure. Controlled-language standards in aerospace maintenance (ASD-STE100 is the best known) exist to remove both, because a technician who misreads a step damages an aircraft. An agent that misreads a tool description calls the wrong tool. Same failure, same fix.

This skill applies that discipline. It is not the ASD standard and does not claim compliance with it — no approved-word dictionary is used here.

The `prose-standards` instruction already carries the mode gate, the sentence rules, and the hard limits into every user-invocable agent. This skill is the deep reference: the rewrite procedure, the full vocabulary rules, and the findings format. Load it to rewrite text that already exists.

## Never apply this to

- **Client-facing deliverables.** Every document under an engagement's `deliverables/` follows
  `engagement-client-voice`. That house style is already plain and already bans buzzwords. Layering
  this on top flattens a document a client pays to read.
- **Marketing copy.**
- **Creative writing.**

Voice and persuasion are the point in all three. This skill removes both by design. If you are
unsure which category a document falls in, ask before rewriting.

## Pick a mode first

State which mode you are in, in one line, before rewriting.

**Strict** — procedures, error messages, tool and agent descriptions, agent-to-agent instructions, safety text. Anywhere a wrong reading costs something. Every rule below applies, including one-word-one-meaning.

**Flavored** — READMEs, PR descriptions, changelogs, explanatory prose, replies to a human. Sentence rules apply in full. Vocabulary rules become advice. Prose needs some range, and locking its word choice reads as a personality transplant rather than a clarification.

## Sentence rules — both modes

| Rule | Do | Instead of |
|---|---|---|
| Active voice | "The agent deletes the file." | "The file is deleted." Passive is allowed only when the actor is genuinely unknown. |
| One instruction per sentence | "Open the file. Read line 3." | "Open the file and read line 3, then check the match." |
| Length | 20 words for instructions, 25 for description | Stacked subordinate clauses |
| No semicolons | Two sentences | Any semicolon. An em dash is allowed but usually marks a sentence that wants splitting. |
| Plain verbs | start, contact, read, remove | spin up, reach out, dive into, take off |
| Noun stacks: 3 words max | "the handler that sets task-queue priority" | "the agent task queue priority handler" |
| Nothing implied | Keep the subject, verb, and article | "Files not backed up will be lost" — which files? |
| Simple tenses | "We received the report." | "We have received the report." |
| One topic per paragraph, 6 sentences max | Split, or make it a list | A paragraph carrying three ideas |
| Lists for sequences | Number 3+ steps | A sequence buried in one sentence |

The tense rule has one exception. "The job has completed" says its output is available now; "the job completed" only says it happened. Where the compound tense carries information the simple one cannot, keep it and say why.

## Vocabulary rules — Strict only, advice in Flavored

- **One word, one meaning.** Pick one verb per action and reuse it. Do not rotate check / verify / confirm for the same act.
- **One name per thing.** The user, the customer, and the client must not be the same entity under three names.
- **Verb, not noun.** "Analyze the log", not "perform an analysis of the log".
- **Define domain terms once.** Keep the necessary jargon. Unpack it inline on first use.

## Document rules — human-facing text

Sentence discipline is not enough for something a person has to act on.

- **Answer first.** Open with the conclusion and what it changes. Evidence after, or behind a link.
- **Translate decision-driving numbers into words, then give the number.**
- **One caveat, not three.** Bold the decision, not the vocabulary.
- **Runbooks and checklists:** TL;DR of five lines or fewer, then numbered steps — one action each, the exact command, and what a correct result looks like. Rationale below the steps.
- **Put warnings where the mistake happens**, not in a preamble.
- **When a step changes, rewrite the step.** No "corrected on <date>" narration in the body.

## Rewriting someone else's text

1. Name the mode.
2. Read it once for meaning before changing anything.
3. Walk it sentence by sentence and flag each violation.
4. Rewrite to fix the violation and nothing else. If a fix would cost precision, keep the longer wording and flag it.
5. Show the result as a table: rule violated, original, rewrite. End with the mode and the count.
6. If the text already complies, say so. Do not force changes.

## Hard limits

- **Never weaken or strengthen a hedge.** "May have failed" is not "failed". Confidence is content, and a length cap is exactly what tempts you to cut it.
- **Never add a fact the source did not state** — a cause, a frequency, a mechanism.
- **Never drop a safety condition, exception, or scope qualifier** to shorten a sentence. Flag the trade-off.
- **Do not apply this to client-facing deliverables, marketing copy, or creative writing.** Flatness
  is the point here, and the wrong point there. See "Never apply this to" above.
- **Form is not substance.** An empty paragraph rewritten under these rules is a short, clean, empty paragraph. Say the text has nothing to say rather than polishing it.
- **Stop at unambiguous, not at shortest.** Past a point, compression costs the reader time instead of saving it.
