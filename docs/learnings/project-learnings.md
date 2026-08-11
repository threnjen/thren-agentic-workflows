# Project Learnings

Traps, framework behaviors, and diagnosed root-cause patterns that will recur. One `##` section
per entry, appended.

## Corpus test constraints that shape how agents and skills may be authored

- **A block of 10 or more contiguous lines repeated across three or more agent files fails
  `tests/test_agent_corpus_invariants.py`.** `BLOCK_LINES = 10` is the threshold. Any shared
  contract long enough to matter must live in a skill and be referenced, never pasted into each
  consumer. The signal that you are about to trip it: writing the same paragraph into a second and
  third agent because "it's only a few lines."
- **No corpus test asserts on totals.** The invariants suite compares frontmatter, paths, and tool
  grants against disk and holds no counts of agents, skills, or instructions. Adding an agent does
  not require updating a tally anywhere in `tests/`. Prose surfaces like `PROJECT_ROADMAP.md` do
  carry counts, and nothing checks them — they drift silently and must be recounted by hand.
- **Corpus tests are structural by written policy, not by accident.** The docstring of
  `test_agent_corpus_invariants.py` states that a check keyed to expected wording goes inert the
  moment someone rephrases a sentence. Proposing a prose-matching guard will be rejected on that
  basis regardless of what it catches.
