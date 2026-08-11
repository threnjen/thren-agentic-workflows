---
name: decision-presentation
description: Activate when several decisions, open questions, or unresolved tradeoffs need to be put to the user in one sitting — planning, refinement, design review, or any point where a list of "things we need to settle" has accumulated. Presents a headline preview of everything queued, then walks the items one at a time, each with framing, costed options, and a committed recommendation. Do NOT activate for factual or context-gathering questions, which should be batched instead.
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Decision Presentation

When several decisions are open, you present them one at a time. A list of everything you want
to discuss is a list the user has to sort — you are handing back the work you were asked to do.

## Open with the queue, as headlines

Before the first decision, preview everything queued: a short ranked list, one line each, no
options and no analysis. The user gets the shape of the workload without having to face it.

Rank by consequence, not by the order you found them. If one decision changes the answer to
another, say so and take it first.

The preview carries **headlines only**. The moment it carries each item's options and costs it
has become the barrage it exists to replace.

## Then one at a time

For each item, in this order:

1. **A header naming the decision.** Not "Question 3" — what the decision is about.
2. **A TL;DR of why this decision exists.** Plain language, two or three sentences. What breaks
   or gets harder if it goes the wrong way. This is the part that gets skipped under load and
   the part that carries the most value.
3. **One to three options**, each with its cost stated inline — effort, risk, complexity, or
   what it forecloses. Never a bare label.
4. **Your recommendation, and the reason it is best.** Commit to one.
5. **An explicit ask**, on its own line.

Then stop and wait. Do not stack the next decision behind this one, and do not answer your own
question and proceed.

After each answer, restate it in one line and move on. If the answer changes a later queued
item, say which and how.

## Resolve the recommendation; never omit it

Either recommend one option and say why, or state plainly that the options are genuinely
equivalent and give the reason. Both are legitimate answers. Silence is not.

Do not manufacture a favorite to look decisive — a fabricated recommendation is
indistinguishable from a real one at the point where someone acts on it. Do not hedge across
two options and call it a recommendation.

Recommend against the user's stated leaning when the evidence says so. Being overruled is a
normal outcome and costs nothing; being agreeable costs them the decision.

## When the user asks to see everything at once

Grant it. Show the full queue with headlines and, if asked, the options — but keep the
structure. Never fall back to unstructured prose, because losing the per-option costs and
recommendations happens exactly when the user has the most to weigh.

"Show me what's open" and "let's do them all now" are different requests. The first is nearly
free. Confirm which one they mean before dumping everything.

## Scope: this is for decisions, not for questions

Run this for genuine forks — real tradeoffs where different answers lead to different work.

**Do not run it for factual or context-gathering questions.** "Which database are you using",
"do you have API keys for this", "should this go in the existing module" — batch those, ask
them plainly, move on. Ceremony on trivia trains the user to skim, and a format they skim is a
format that fails on the decision that mattered.

If you cannot state a real cost for at least two options, it is not a decision. Pick the
obvious default, say you picked it, and continue.

## Failure modes

- **The preamble becomes the checklist.** If the preview has costs and options in it, you have
  reintroduced the wall of text with extra steps.
- **Asking without deciding.** Presenting three options and no recommendation puts the whole
  analytical burden back on the user.
- **Batching under time pressure.** When the queue is long, the temptation is to collapse it.
  That is precisely when sequencing matters most.
- **Continuing past an unanswered ask.** If you asked, wait. If you did not need to wait, you
  should not have asked.
- **Re-litigating a settled decision.** Once answered, it is closed. Reopen only on new
  information, and say what the new information is.

## Related

`question-hygiene` governs how to phrase a single question so it is answerable standalone.
This skill governs how to sequence several. Follow both — a well-sequenced question that
cannot be understood without scrollback still fails.
