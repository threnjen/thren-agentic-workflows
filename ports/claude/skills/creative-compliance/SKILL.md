---
name: creative-compliance
description: The single source of truth for what violates each creative writing mode and how to repair the draft - per-mode violation rules, worked examples, and the strip-reformulate-regenerate repair ladder. Use when self-checking a draft response before sending it, or when scanning someone else's draft as the compliance agent.
license: MIT
profile: creative
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Creative Compliance

This skill is the **only** definition of a mode violation. `creative-modes`, the developmental
editor's inline self-check, and `Creative - Compliance Check` all cite it. None of them
restates its rules, because two copies of a rule is how rules drift.

Mode names and their permitted output live in `creative-modes`. This skill covers the
failure side only.

## The Governing Rule

In **Interrogate, Reflect, Diagnose, and Adversarial**: any declarative statement introducing
content not present in the writer's own prior input is a violation. That includes new names,
new plot mechanics, new character traits, a contradiction resolved on the writer's behalf, and
any proposed fix.

In **Generate and Copyedit**: content is expected. The violation is scope — drifting past what
was asked, into adjacent creative territory.

## Per-Mode Rules

### Interrogate

- **Violation** — anything that is not a question. A leading question carrying its own answer
  counts, as does a question offering two options.
- **Example** — *"What if the guild treaty predates the siege?"* The writer never said it did.
- **Repair** — strip the content and ask about the same gap: *"When was the guild treaty
  signed, relative to the siege?"*

### Reflect

- **Violation** — any addition, including a synthesis, a connection, or an implication the
  writer did not state. Correctness is not a defense.
- **Example** — *"So the river guilds are really about inherited debt."* The writer described
  the guilds; the theme is yours.
- **Repair** — cut the addition. Restate only what was said. If the connection seems worth
  making, convert it to an Interrogate question next turn.

### Diagnose

- **Violation** — a proposed fix, or a verdict resting on material the writer has not supplied.
- **Example** — *"Chapter four's stakes are thin — seed the threat in chapter two."* The
  first clause diagnoses, the second fixes.
- **Repair** — keep the diagnosis, delete the fix, and cite the evidence: *"Chapter four's
  stakes rest on a threat that appears once, in chapter one."*

### Adversarial

- **Violation** — everything Diagnose forbids, plus burying the weakest point. Opening with
  what works, then arriving at the problem, is a delivery failure in this mode.
- **Example** — a three-paragraph appreciation of the prose before naming the structural hole.
- **Repair** — reorder so the weakest point leads. Cut the cushioning.

### Generate

- **Violation** — answering more than was asked. A brainstorm dump, options for a question
  that was not posed, or a nudge that arrives with a plot suggestion attached.
- **Example** — asked for three surname options, returning surnames plus a note on what each
  implies about the character's lineage.
- **Repair** — cut to the scoped answer. Then exit to the prior mode.

### Copyedit

- **Violation** — a new idea, or voice drift. If the rewrite sounds like a model's prose
  rather than a cleaner version of the writer's, it fails even when it reads better.
- **Example** — replacing a deliberately blunt fragment with a balanced compound sentence.
- **Repair** — restore the writer's cadence, register, and sentence shapes. Change only what
  was actually broken.

## Repair Ladder

Apply in order. Stop at the first step that clears the draft.

1. **Strip** — delete the violating content and send the rest.
2. **Reformulate** — turn the stripped content into a question about the same gap.
3. **Regenerate** — rebuild the response with the violation named explicitly in the prompt.

Only the cleared draft reaches the writer.

## Reporting

When acting as the compliance agent, return per violation: the mode, the offending span
quoted, the rule it breaks, and the repair ladder step to apply. Return "clear" and nothing
else when the draft passes — do not editorialize about the writing itself. That is not your
job, and doing it would introduce exactly the content you exist to catch.
