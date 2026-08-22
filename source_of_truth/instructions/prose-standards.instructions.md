---
description: "Sentence and mode discipline for every piece of English an agent writes. Audience is an ENUMERATED agent roster - the user-invocable technical agents, whose filename shapes are unrelated, so no glob selects them without also catching subagents. Enumeration is deliberate. `client-deliverable` is absent on purpose: its output follows `engagement-client-voice`. The creative agents are withheld automatically by the profile gate, not by this roster."
applyTo: "**/01-project-planner.agent.md,**/02-phase-refiner.agent.md,**/03-phase-execute.agent.md,**/04-pr-review.agent.md,**/auditor.agent.md,**/debugger.agent.md,**/delta-auditor.agent.md,**/docs-writer.agent.md,**/instructions-manager.agent.md,**/pr-author.agent.md,**/qa-bootstrap.agent.md,**/single-feature-agent.agent.md,**/test-orchestrator.agent.md,**/web-research-specialist.agent.md"
---

# Prose Standards

Every piece of English you write has a reader. Pick the mode from the reader, not from the surrounding style. Style-matching applies to code, not prose.

**Strict** - procedures, error messages, tool and agent descriptions, agent-to-agent instructions, safety text. Anywhere a wrong reading costs something.

**Flavored** - READMEs, PR descriptions, changelogs, explanatory prose, replies to a human. Sentence rules apply in full. Word choice stays free.

**Neither** - client-facing deliverables, marketing copy, creative writing. Never apply these rules there. Client deliverables follow `engagement-client-voice`.

Dense is correct for machine-facing planning documents - phase summaries, discovery context, roadmaps, plan and context and tasks bundles. The pipeline reads these to decompose work, so spelling out every constraint helps. Dense never excuses ambiguous.

## Sentence rules - both modes

- Active voice. Use the passive only when the actor is genuinely unknown.
- One instruction per sentence.
- 20 words for an instruction, 25 for a description.
- No semicolons. An em dash is allowed but usually marks a sentence that wants splitting.
- Plain verbs - start, not spin up; contact, not reach out.
- Three words maximum in a noun stack.
- Keep the subject, verb, and article explicit. Imply nothing.
- Simple tenses, unless the compound tense carries information the simple one cannot.
- One topic per paragraph, six sentences maximum.
- Number any sequence of three or more steps.

## Human-facing documents

- Answer first. Open with the conclusion and what it changes. Evidence after, or behind a link.
- Translate a decision-driving number into words, then give the number.
- One caveat, not three. Bold the decision, not the vocabulary.
- Put a warning where the mistake happens, not in a preamble.
- Runbooks and checklists: a TL;DR of five lines or fewer, then numbered steps. One action each, with the exact command and what a correct result looks like. Rationale below the steps.
- When a step changes, rewrite the step. No correction-log narration in the body.

## Hard limits

- Never weaken or strengthen a hedge to save words. "May have failed" is not "failed". Confidence is content.
- Never add a fact the source did not state - a cause, a frequency, a mechanism.
- Never drop a safety condition, exception, or scope qualifier to shorten a sentence. Flag the trade-off instead.
- Form is not substance. Say the text has nothing to say rather than polishing it.
- Stop at unambiguous, not at shortest.

Write to a colleague who is sharp, busy, and has not read the rest of the phase. If the reader asks for a simpler version, the first version was wrong.

## Vocabulary rules - Strict only, advice in Flavored

- One word, one meaning. Pick one verb per action and reuse it. Do not rotate check, verify, and confirm for the same act.
- One name per thing. The user, the customer, and the client must not be one entity under three names.
- Verb, not noun. Write "analyze the log", not "perform an analysis of the log".
- Define each domain term once. Keep the necessary jargon. Unpack it inline on first use.

## Rewriting existing text

Follow these steps for a full rewrite pass over text that already exists.

1. Name the mode in one line before you change anything.
2. Read the text once for meaning.
3. Walk it sentence by sentence and flag each violation.
4. Rewrite to fix the violation and nothing else. If a fix costs precision, keep the longer wording and flag it.
5. Report the result as a table with three columns: rule violated, original, rewrite. End with the mode and the violation count.
6. If the text already complies, say so. Do not force changes.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: prose-standards."* Then proceed normally.
