---
name: decision-presentation
description: Activate when several decisions, open questions, or unresolved tradeoffs need to be put to the user in one sitting — planning, refinement, design review, or any point where a list of "things we need to settle" has accumulated. Presents a headline preview of everything queued, then walks the items one at a time, each with framing, costed options, and a committed recommendation. Do NOT activate for factual or context-gathering questions, which should be batched instead.
---

# Decision Presentation

When several decisions are open, present them one at a time. A list of everything you want to
discuss forces the user to sort it. That returns the requested work to the user.

## Gate first: drop the non-decisions

An empty decision queue (a list of open decisions) is acceptable. When the work follows a required
convention, matches a pattern the repository already uses, or has one answer that works, there is
nothing to decide. Do not invent items so the user has something to choose.

An item enters the queue only when all three conditions are true:

1. **Two or more options actually work.** An option you already know will fail is not an option.
2. **Different answers lead to different work**, and a reasonable person could pick either.
3. **Nothing already settles it** — not the repository, not a module contract, not a naming or
   language rule, and not a pattern the codebase follows everywhere.

If any check fails, follow these steps:

1. Pick the answer that works.
2. State your choice in one line.
3. Record it.
4. Continue.

Never present "follow the required convention" and "do it a way that will not work" as equal
choices.

Make technical choices yourself. Decide what to name a function and where a helper lives. Choose
the library call and module structure. Apply the repository's conventions. Continue.
The user asked you to complete the work. Do not describe every possible technical choice. Present
a technical choice only when it changes the user's result: cost, a dependency that is hard to
remove, behavior visible to the user, or future capability. Make all other technical choices
yourself.

## Open with the queue, as headlines

Before the first decision, preview the full queue as a short ranked list with one line for each
decision. Include no options or analysis. This lets the user see the workload before reviewing
each decision.

Rank decisions by consequence, not by discovery order. If one decision changes another decision's
answer, address the first decision before the second.

The preview contains **headlines only**. If it contains options and costs, it recreates the full
list that this format avoids.

## Then one at a time

For each item, in this order:

1. **Name the decision in a header.** Do not use "Question 3".
2. **Explain why this decision exists in a TL;DR (short summary).** State the reason in plain
   language in two or three sentences. Explain what breaks or becomes harder if the user chooses
   incorrectly.
   Users skip this section when they are busy, although it carries the most value.
3. **Present one to three options.** State each option's cost inline. Include effort, risk,
   complexity, or a capability the option removes. Do not use a bare label.
4. **Give one recommendation and its reason.** Explain why it is best.
5. **End with an explicit ask.** Put it on its own line.

Then stop and wait. Do not present the next decision. Do not answer your own question before the
user responds.

After each answer, restate it in one line. Then continue. If the answer changes a later decision,
identify that decision and the change.

## Resolve the recommendation; never omit it

Recommend one option and state why. If the options are genuinely equivalent, state that plainly.
Explain why. Both answers are legitimate. Do not omit either the recommendation or the
statement that the options are equivalent.

Do not invent a recommendation to appear decisive. An invented recommendation is
indistinguishable from a valid one when someone acts on it. Do not present two options as one
recommendation.

Recommend against the user's stated leaning when the evidence supports that choice. The user may
overrule you. That costs nothing. Agreeing without evidence costs the user the decision.

## When the user asks to see everything at once

Show the full decision queue with headlines. Include options only when the user asks. Keep the
structure. Unstructured prose hides the cost and recommendation for each option.

"Show me what's open" and "let's do them all now" are different requests. The first requires
little additional work. Confirm which request the user means before showing all decisions.

## Scope: this is for decisions, not for questions

Use this skill for genuine decisions with real tradeoffs. Different answers must lead to different
work.

**Do not run it for factual or context-gathering questions.** "Which database are you using",
"do you have API keys for this", "should this go in the existing module" — batch those questions
and ask them plainly. Continue. Using this format for simple questions trains users to skim it.
Skimming can hide an important decision.

If you cannot state a real cost for at least two options, treat the item as a non-decision. Then
follow these steps:

1. Use the gate above.
2. Pick the working answer.
3. State your choice.
4. Continue.

## Failure modes

- **The preamble becomes the checklist.** If the preview includes costs and options, it becomes
  the full checklist again.
- **Asking without deciding.** Presenting three options without a recommendation makes the user
  do all the analysis.
- **Batching under time pressure.** When the queue is long, the temptation is to combine items.
  Keep the sequence because long queues need one decision at a time.
- **Continuing past an unanswered ask.** If you ask a question, wait for the answer. Do not ask a
  question that does not require an answer.
- **Re-litigating a settled decision.** Once answered, close the decision. Reopen it only when new
  information appears. State the new information.

## Related

`question-hygiene` governs how to phrase one question so users can answer it without context.
This skill governs how to sequence several questions. Follow both skills. A well-sequenced
question still fails if users cannot understand it without earlier messages.
