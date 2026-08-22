
<!-- phase-doc-sync -->
## Phase Document Sync

When working in a repository that has a `docs/phases/` directory, or when the
user references a phase QA doc, a `_QA.md` checklist, QA failures, or asks for
fixes/tweaks/small updates during phase work: load the `phase-doc-sync` skill
before making code changes and follow its documentation-reconciliation
contract. Any change that alters what a phase delivers or how it behaves is
not complete until the affected `PHASE_0N_SUMMARY.md` and `PROJECT_ROADMAP.md`
(or `PHASES_OVERVIEW.md` in legacy repos) entries are updated as baseline
truth — rewritten in place with no change-log framing.
<!-- phase-doc-sync -->

<!-- agent-discovery -->
## Custom Agent and Skill Discovery

When the user asks {harness_title} to act as a named agent, resolve its definition from:

{agent_paths}

When the user explicitly names a skill that is not already available in the
session skill catalog, look for it in:

{skill_paths}

Read the selected agent or skill instructions completely before beginning work.
Do not spawn an agent merely because the user asks {harness_title} to act in that role.
<!-- agent-discovery -->

<!-- know-the-audience -->
## Know The Audience

Every piece of English you write has a reader. Pick the mode from the reader, not from
the surrounding style. Style-matching applies to **code, not prose.**

**Strict** — procedures, error messages, tool and agent descriptions, agent-to-agent
instructions, safety text. Anything parsed without a human present to resolve ambiguity.

**Flavored** — READMEs, PR descriptions, changelogs, explanatory prose, replies to a
human. Same sentence discipline, but word choice stays free.

**Neither** — client-facing deliverables, marketing copy, creative writing. Never apply
these rules there. Client deliverables follow `engagement-client-voice` instead.

Dense is still correct for machine-facing planning docs — phase summaries, discovery
context, roadmaps, feature plan/context/tasks bundles. The workflow consumes these to
decompose work, so spelling out every constraint helps. Dense is never an excuse for
ambiguous.

Sentence rules, both modes:

- Active voice. One instruction per sentence.
- 20 words for an instruction, 25 for a description.
- No semicolons. Plain verbs — start, not spin up; contact, not reach out.
- Three words maximum in a noun stack. Keep the subject, verb, and article explicit.
- Simple tenses, unless the compound tense carries information the simple one cannot.

Strict mode adds: one word per action, one name per thing, verbs over noun forms, and
every domain term unpacked inline on first use.

Human-facing documents also need:

- Answer first: the conclusion and what it changes. Evidence after, or behind a link.
- Decision-driving numbers translated into words, then given as numbers.
- One caveat, not three. Bold the decision, not the vocabulary.
- Runbooks and checklists: TL;DR of five lines or fewer, then numbered steps — one action
  each, with the exact command and what a correct result looks like. Rationale below the
  steps. Warnings where the mistake happens, not in a preamble. When a step changes,
  rewrite the step — no correction-log narration in the body.

Never weaken or strengthen a hedge to save words. "May have failed" is not "failed", and
confidence is content.

- BAD: "prose is the one thing this corpus needs to be free to reword"
- GOOD: "We need to be able to rewrite the words freely"

Write to a colleague who is sharp, busy, and has not read the rest of the phase. If the
reader asks for a simpler version, the first version was wrong. To rewrite existing text, follow
the rewrite steps in the `prose-standards` instruction for a full pass with per-violation findings.
<!-- know-the-audience -->
