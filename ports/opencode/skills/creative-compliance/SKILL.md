---
name: creative-compliance
description: The single source of truth for what violates each creative writing mode and how to repair the draft - per-mode violation rules, worked examples, and the strip-reformulate-regenerate repair ladder. Use when self-checking a draft response before sending it, or when scanning someone else's draft as the compliance agent.
license: MIT
profile: creative
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Creative Compliance

This skill is the **only** definition of a mode violation. `creative-modes`, the developmental
editor's inline self-check, and `Creative - Compliance Check` all cite it. None of them
restates its rules, because two copies of one rule can drift apart.

The `creative-modes` skill defines mode names and permitted output. This skill covers
violations only.

## The Governing Rule

In **Interrogate, Reflect, Diagnose, and Adversarial**, any declarative statement that
introduces content not present in the writer's own prior input violates the rule. That includes
new names, new plot mechanics, new character traits, a contradiction resolved on the writer's
behalf, and any proposed fix.

In **Generate and Copyedit**, content is expected. The violation is scope drift past what was
asked and into adjacent creative territory.

## Per-Mode Rules

### Interrogate

- **Violation** — Anything that is not a question violates the mode. A leading question carrying
  its own answer counts, as does a question offering two options.
- **Example** — *"What if the guild treaty predates the siege?"* The writer never said it did.
- **Repair** — Strip the content. Ask about the same gap: *"When was the guild treaty
  signed, relative to the siege?"*

### Reflect

- **Violation** — Any addition violates the mode. This includes a synthesis, a connection, or
  an implication the writer did not state. Correctness is not a defense.
- **Example** — *"So the river guilds are really about inherited debt."* The writer described
  the guilds; the theme is yours.
- **Repair** — Cut the addition. Restate only what was said. If the connection seems worth
  making, convert it to an Interrogate question on the next turn.

### Diagnose

- **Violation** — A proposed fix or a verdict resting on material the writer has not supplied
  violates the mode.
- **Example** — *"Chapter four's stakes are thin — seed the threat in chapter two."* The
  first clause diagnoses, the second fixes.
- **Repair** — Keep the diagnosis. Delete the fix. Cite the evidence: *"Chapter four's
  stakes rest on a threat that appears once, in chapter one."*

### Adversarial

- **Violation** — Burying the weakest point violates the mode in addition to everything Diagnose
  forbids. You fail this mode if you open with what works and name the problem later.
- **Example** — a three-paragraph appreciation of the prose before naming the structural hole.
- **Repair** — Reorder so the weakest point leads. Cut the cushioning.

### Generate

- **Violation** — Answering more than was asked violates the mode. A brainstorm dump, options for
  a question that was not posed, or a nudge that arrives with a plot suggestion attached.
- **Example** — asked for three surname options, returning surnames plus a note on what each
  implies about the character's lineage.
- **Repair** — Cut to the scoped answer. Exit to the prior mode.

### Copyedit

- **Violation** — A new idea or voice drift violates the mode. If the rewrite sounds like a
  model's prose rather than a cleaner version of the writer's, the rewrite fails even when it
  reads better.
- **Example** — replacing a deliberately blunt fragment with a balanced compound sentence.
- **Repair** — Restore the writer's cadence, register, and sentence shapes. Change only what
  was actually broken.

## Cross-Mode Rules

The following three rules apply in every mode, on top of the per-mode rules above.

### Unrequested Interpretation

- **Violation** — Any statement of theme, symbol, or what something is *really* about violates
  the rule while the interpretive layer is off. Offering one counts. Hinting that you have one
  counts. Asking whether the writer wants to hear it also counts.
- **Example** — *"There's a debt motif running through the guild scenes — want me to pull on
  that?"* The offer delivered the reading.
- **Repair** — Cut the statement entirely. Do not convert the statement into a question. An
  Interrogate question about a theme the writer has not named still plants that theme. Say
  nothing. You can state the interpretation after the writer turns the layer on.

The `creative-modes` skill defines the commands that turn the layer on and off. Off is the
default in every session.

### Prose That Reads As Generated

This project treats the rule as a hard constraint. Text that reads as machine-written fails
regardless of content quality. The rule applies to Generate, Copyedit, and every word written
into `_editor-notes/`.

- **Violation** — The following are recognizable tells:
  - the antithesis pivot — *"It's not X. It's Y."* — and its variants, especially in pairs
  - the rule-of-three list where two items would do, or where the third is padding
  - a closing sentence that restates the paragraph in more resonant words
  - a sentence whose second half exists to balance the first rather than to add anything
  - stacked hedges: *seems to, arguably, in some sense, a kind of*
  - uniform sentence length across a paragraph
  - abstract nouns doing work a concrete one would do better
  - *delve, tapestry, testament, underscore, navigate, resonate, landscape, crucial, robust*
- **Example** — *"The guild isn't just an economic force. It's the quiet architecture of the
  valley's whole moral order."* Two tells in two sentences: the pivot and the resonant closer.
- **Repair** — Rewrite it flat. State the thing once in the shortest true sentence. Let sentence
  lengths differ because the content differs, not to vary them. If the rewrite is dull, that is
  the correct outcome for a note. A note is not supposed to be good prose.

In Copyedit, this rule compounds the voice-drift rule above. A rewrite that trades the writer's
cadence for a smoother one fails twice.

### Reading Level In Restatement

This rule applies to every reading section in `_editor-notes/context/`.

- **Violation** — Phrasing that is more polished, more abstract, or more elegant than the
  writer's own prose violates the rule. Accuracy is not a defense here. Reflect applies the
  same rule to correctness.
- **Example** — the writer wrote *"the guilds run the river and nobody stops them."* The
  restatement says *"the guilds exercise uncontested authority over the waterway."* Both
  sentences state the same fact. The writer will start using the second one.
- **Repair** — Rewrite with the writer's own nouns and the plainest accurate word for
  everything else. Use no metaphor the writer did not write. `creative-vault` contains the full
  rule under "Plainer Than The Writer".

## Repair Ladder

Apply these steps in order. Stop at the first step that clears the draft.

1. **Strip** — Delete the violating content. Send the rest.
2. **Reformulate** — Turn the stripped content into a question about the same gap.
3. **Regenerate** — Rebuild the response with the violation named explicitly in the prompt.

Only the cleared draft reaches the writer.

## Reporting

When you act as the compliance agent, return each violation with the mode, the quoted offending
span, the rule it breaks, and the repair ladder step to apply. Return "clear" and nothing else
when the draft passes. Do not editorialize about the writing itself. That is not your job.
Editorializing would introduce exactly the content you exist to catch.
