---
description: "Requires interrogating agents to make every decision question self-contained: plain-language framing, inline context, and spelled-out option trade-offs. Audience is DERIVED: pipeline stages 01-02, the agents that interrogate the user."
applyTo: "source_of_truth/agents/0[12]-*.agent.md"
baseline: true
---

# Question Hygiene

Question Triage governs **when** to ask the user a question. This file governs **how**. Every decision question must stand alone for someone who has not read the conversation, has not seen your files, and has kept none of your earlier analysis.

Put all of this inside the question itself.

1. **What the thing is.** Name and describe the subject in plain language. Never point back to a label you introduced earlier, such as "Option B", "the adapter approach", or "the file above". Re-explain it here.
2. **Why it matters.** State what depends on the decision and what follows from each answer. If no answer changes what you would do, do not ask.
3. **What each option costs.** Give every option its trade-off inline: effort, complexity, risk, or what it forecloses. Write "A (simpler, but no offline support) or B (more setup, works offline)", never a bare "A or B?".
4. **Plain language.** No unexplained jargon, internal shorthand, or reference to analysis the user has not seen. Define an essential technical term in a clause.

Multiple choice is the easiest format to get wrong. The stem must carry enough context that the choices make sense without scrolling back, and each choice must describe its own trade-off rather than restate its label. If the context will not fit, the question is premature. Do more analysis, or ask something narrower.

Check every question before you send it: if this were the only text the user could see, could they answer it confidently? Rewrite until yes.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: question-hygiene."* Then proceed normally.
