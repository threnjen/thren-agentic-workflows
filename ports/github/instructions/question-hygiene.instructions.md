---
description: "Requires interrogating agents to make every decision question self-contained: plain-language framing, inline context, and spelled-out option trade-offs. Audience is DERIVED: pipeline stages 01-02, the agents that interrogate the user."
applyTo: "source_of_truth/agents/0[12]-*.agent.md"
baseline: true
---

# Question Hygiene

Question Triage governs **when** to ask the user a question. This file governs **how**. Every decision question must stand alone for someone who has not read the conversation or seen your files and does not remember any earlier analysis.

Include all required context in the question itself.

1. **What the thing is.** Name the subject. Describe it in plain language. Never refer to a label that you introduced earlier, such as "Option B", "the adapter approach", or "the file above". Describe the subject again in the question.
2. **Why it matters.** State what depends on the decision and what follows from each answer. If no answer changes what you would do, do not ask.
3. **What each option costs.** State each option's trade-off inline: effort, complexity, risk, or what it prevents. Write "A (simpler, but no offline support) or B (more setup, works offline)". Never offer only "A or B?".
4. **Plain language.** Do not use unexplained jargon, internal shorthand, or references to analysis the user has not seen. Define each essential technical term in a clause.

Apply these rules to every multiple-choice question. The question stem, the part before the choices, must provide enough context for the choices to make sense without earlier text. Each choice must state its own trade-off, not merely repeat its label. If you cannot include the required context, the question is premature. Analyze more before asking. Ask a narrower question if needed.

Check every question before you send it. Could the user answer it confidently if it were the only text they could see? Rewrite the question until the user can answer it confidently.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: question-hygiene."* Then proceed normally.
