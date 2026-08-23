---
description: "Requires interrogating agents to make every decision question self-contained: plain-language framing, inline context, and spelled-out option trade-offs. Audience is DERIVED: pipeline stages 01-02, the agents that interrogate the user."
applyTo: "source_of_truth/agents/0[12]-*.agent.md"
baseline: true
---

# Question Hygiene

Question Triage (where present) governs **when** to ask the user a question. This file governs **how**. Every decision question you ask the user must be answerable standalone, by someone who has not read the conversation so far, has not seen the files you have seen, and has retained none of your earlier analysis.

Before asking a decision question, restate in the question itself the context needed to answer it:

1. **What the thing is** — Name and briefly describe the subject of the question in plain language. Never refer to a file, function, phase, or option purely by a label you introduced earlier ("Option B", "the adapter approach", "the file above"). Re-explain it in the question.
2. **Why it matters** — State what depends on this decision and what happens downstream of each answer. If the answer doesn't change anything you'd do, don't ask (that's Question Triage territory).
3. **What each option costs** — For every option offered, spell out its concrete trade-off inline: effort, complexity, risk, or what it forecloses. "A (simpler, but no offline support) vs B (more setup, works offline)" — never a bare "A or B?".
4. **Plain-language framing** — No unexplained jargon, internal shorthand, or references to analysis the user hasn't seen. If a technical term is essential, define it in a clause.

## Multiple-Choice Discipline

Multiple-choice questions are the highest-risk format for context-free asking. Before presenting choices:

- The question stem must contain enough context that the choices make sense without scrolling back.
- Each choice label must be self-describing; the description must carry the trade-off, not just restate the label.
- If you cannot fit the necessary context into the question, that is a signal the question is premature — do more analysis first, or ask a narrower question.

## Self-Check

Before sending any question, apply this test: *If this question were the only text the user could see, could they answer it confidently?* If no, rewrite it until yes.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: question-hygiene."* Then proceed normally.
