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

## Check the shared skill before authoring a new one to hold a contract

- **A contract you are about to write into a new skill may already be owned by a skill the
  participating agents load for themselves.** `auditor-conventions` already carries multi-target
  audit comparability — identical prompt text, per-run independence, snapshot labels, the
  `dev/[audit-name]/<snapshot-label>/` layout, the one-output-root rule. A plan to put those rules
  in a new orchestration skill would have created the second copy that the plan itself existed to
  prevent. The signal: the rule is about how a *subagent* behaves, not about how the orchestrator
  sequences it — subagent behavior almost always already has a home.
- **Prefer extracting an existing sequence over composing a fresh one.** When a second orchestrator
  needs what an existing orchestrator already does, the working prose is the asset. Rewriting it
  loses the rules that read as boilerplate and are load-bearing — release-ordering handshakes,
  "do not report this count yet" discipline, disjoint-set and sum checks.
- **When extracting, separate mechanism from conversation first.** An interactive orchestrator's
  confirmations, offers, and questions must stay in the agent; only the mechanical contract moves.
  An extraction that carries the confirmations along is unusable by the unattended caller that
  motivated it.
