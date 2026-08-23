---
name: prose-rewrite
description: "Run a full rewrite pass over English text that already exists, reporting every violation with its original and its replacement. Covers the pass order, the report table, and the limits on what a rewrite may change. Use when asked to rewrite, tighten, clean up, or edit existing prose, and when reviewing someone else's rewrite. Not for drafting new text - the `prose-standards` instruction governs that."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Prose Rewrite

**When this applies.** Text already exists and someone asked you to improve it. Drafting new prose needs no rewrite pass. Follow the `prose-standards` instruction instead, which is loaded for you and holds the mode definitions, the sentence rules, and the hard limits this skill enforces.

A rewrite is not a redraft. You are fixing named violations in someone else's text, so every change you make has to trace back to a rule. A change you cannot name a rule for is your taste replacing theirs.

## The Pass

1. Name the mode in one line before you change anything. Strict, Flavored, or Neither, and why.
2. Read the text once for meaning. Do not edit on this pass.
3. Walk it sentence by sentence and flag each violation against the sentence, human-facing, and vocabulary rules.
4. Fix the violation and nothing else. When a fix costs precision, keep the longer wording and flag the trade-off.
5. Report a table with three columns: rule violated, original, rewrite. End with the mode and the violation count.
6. When the text already complies, say so. Do not force changes.

## What A Rewrite May Not Do

The `prose-standards` hard limits bind here, and step 4 is where they get broken. Restated in the terms of a rewrite pass:

- Never weaken or strengthen a hedge to save words. "May have failed" is not "failed".
- Never add a fact the source did not state - a cause, a frequency, a mechanism.
- Never drop a safety condition, exception, or scope qualifier to shorten a sentence.
- Never reword a paired asset alone. When a file names a counterpart that restates it, change both or neither.
- Never touch a load-bearing string: a canary, a sentinel, a required failure message, a verdict token, a path token binding.

Stop at unambiguous, not at shortest. A shorter text that lost a qualifier is a worse text.

## Reporting

The table is the deliverable, not a courtesy. It is what lets the author reject one change without rejecting the pass. Give the original and the rewrite in full for each row - a diff fragment does not show whether a qualifier survived.

State the count even when it is zero. "No violations found, Flavored mode" is a complete report.
