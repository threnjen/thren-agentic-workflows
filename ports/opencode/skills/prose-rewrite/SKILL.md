---
name: prose-rewrite
description: Run a full rewrite pass over English text that already exists, reporting every violation with its original and its replacement. Covers the pass order, the report table, and the limits on what a rewrite may change. Use when asked to rewrite, tighten, clean up, or edit existing prose, and when reviewing someone else's rewrite. Not for drafting new text - the `prose-standards` instruction governs that.
license: MIT
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Prose Rewrite

**When this applies.** Text already exists and someone asked you to improve it. Drafting new prose needs no rewrite pass. Follow the loaded `prose-standards` instruction. It defines the modes, sentence rules, and hard limits this skill enforces.

A rewrite is not a redraft. You are fixing named violations in someone else's text. Every change must follow a named rule. If you cannot name the rule, you are replacing the author's choices with your own.

## The Pass

1. Write one line that names the mode as Strict, Flavored, or Neither and explains why.
2. Read the text once to understand its meaning. Do not edit during this pass.
3. Review the text sentence by sentence. Record each violation against the sentence, human-facing, or vocabulary rules.
4. Fix only the violation. If a fix would reduce precision, keep the longer wording and flag the trade-off.
5. Report a table with three columns: rule violated, original, rewrite. End the report with the mode and violation count.
6. When the text already complies, say so. Do not force changes.

## What A Rewrite May Not Do

The `prose-standards` hard limits apply here. Step 4 can introduce violations. Restate the limits in rewrite terms:

- Never weaken or strengthen a hedge to save words. "May have failed" is not "failed".
- Never add a fact that the source did not state, such as a cause, frequency, or mechanism.
- Never drop a safety condition, exception, or scope qualifier to shorten a sentence.
- Never reword a paired asset alone. When a file names a counterpart that restates it, change both or neither.
- Never touch a load-bearing string: a canary, a sentinel, a required failure message, a verdict token, a path token binding.

Stop when the text is unambiguous, not when it is shortest. A shorter text that loses a qualifier is worse.

## Reporting

The table is the deliverable. It lets the author reject one change without rejecting the pass. Give the original and rewrite in full for each row. A diff fragment does not show whether a qualifier survived.

State the count even when it is zero. "No violations found, Flavored mode" is a complete report.
