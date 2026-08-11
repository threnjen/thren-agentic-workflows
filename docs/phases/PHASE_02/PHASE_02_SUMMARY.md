# Phase 2: Phase Document Final Check

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Small
**Cross-references**: None — single-repository phase

## What's New

When you finish refining a phase document, Phase - Refiner offers one last look from someone who
was not in the room. Accept, and it spawns a reviewer that starts cold — no conversation history,
no summary of what you discussed, no framing of what matters. That reviewer reads the finished
document and the repository the way a newcomer would, then reports what looks missing,
contradictory, or never examined.

The findings come back to you verbatim — at most five, each one pointing at a specific place in
the document or a concrete fact in the repository. Phase - Refiner then asks which ones you want
folded in, and edits only those. Nothing is applied without your say-so.

The check is optional and advisory. Declining it is a normal outcome, not a skipped gate, and the
phase document is finished either way.

## Objective

Give a refined phase document one context-free review pass before it goes downstream, so gaps that
became invisible to both the user and the refiner during a long convergent session get surfaced
while the document is still cheap to change.

## Scope

### In Scope

- A new hidden subagent at `source_of_truth/agents/02a-phase-final-check.agent.md`, following the
  existing parent-number-plus-letter convention used by `04a`–`04h` and `05a`–`05h`. It is a leaf:
  it spawns nothing, and it writes no files at all.
- A new skill defining the review contract — what the reviewer may read, what qualifies as a
  finding, the shape of the report, and the blindness rule below. Two consumers exist for it from
  day one (the subagent and Phase - Refiner's offer step), which is why it is a skill rather than
  prose inlined in the agent file.
- **The blindness rule, stated in the spawn contract itself.** Phase - Refiner passes the reviewer
  the phase document path and the repository path, and nothing else. It does not summarize the
  refinement session, does not say which areas it considers settled, and does not flag what it
  thinks deserves attention. The instinct to brief the subagent is strong and briefing it destroys
  the entire value of the pass, so the prohibition lives in the spawn prompt where the spawning
  agent reads it, not only in this document.
- **The reading boundary.** The reviewer reads the phase document and the repository as any
  newcomer could — including `docs/phases/DISCOVERY_CONTEXT.md` and
  `docs/learnings/cross-phase-decisions.md`. Those files record *what* was decided and are the
  reviewer's only defense against reporting settled matters as gaps. The blindness rule is absolute
  on conversation content and does not extend to committed files.
- **The findings contract.** A finding must fall into one of these categories: an internal
  contradiction, an ambiguously stated scope boundary, a success criterion that is not actually
  checkable, a term used without definition, a dependency or risk the document never addresses, or
  a deliverable with no matching success criterion. Every finding cites where in the document it
  applies or a concrete fact in the repository. No severity ratings. **At most five findings**, and
  the reviewer says so when it had to leave things out. Finding nothing is a valid result, stated
  plainly and without padding.
- **Review scope is the document's own content.** The state of surrounding files — whether the
  roadmap row has been synced, whether discovery context has been written — is explicitly not
  reviewable, because the check runs before those steps.
- **A split of Phase - Refiner's Phase 6**, in `source_of_truth/agents/02-phase-refiner.agent.md`.
  The current Phase 6 writes the phase document, writes the phase-scoped discovery context, and
  syncs the roadmap in one pass; Phase 7 opens the working branch and commits. The new order is:
  1. **Write the phase document.** Unchanged, but no longer bundled with the sync steps.
  2. **Offer the final check.** Accept, decline, and no-answer are all terminal — none of them
     blocks progression.
  3. **Report and fold in.** Present the findings verbatim, without editorializing or
     pre-filtering. Ask which the user wants applied. Rewrite the document in place for the
     accepted ones only, following the refiner's existing clean-rewrite rule — no change-log
     framing, no preserved old wording.
  4. **Sync the roadmap and write the phase discovery context.** Moved to here so both are
     generated from final content and written exactly once.
  5. **Open the working branch and commit.** Unchanged.
- **Both refiner entry paths reach the offer.** Phase - Refiner refines an existing document
  (Entry A) or drafts one from scratch for a standalone feature (Entry B). Both converge before the
  write step, so the offer is shared workflow. Entry B is the weaker document — one agent, one
  conversation, no upstream planner pass — and is where the check is worth the most.
- Structural tests covering the new wiring: the subagent file exists and parses, Phase - Refiner
  declares it in its `agents:` frontmatter list, and the skill is referenced by both consumers.

### Out of Scope

- **Any blocking behavior.** Nothing gates on the findings. There is no severity threshold, no
  rubric score, no pass/fail verdict, and no revise-and-recheck loop.
- **Any findings artifact on disk.** The reviewer returns its findings in its response; Phase -
  Refiner relays them and applies the accepted ones. Nothing is written, nothing is committed.
  Anything worth outliving the session lands in the phase document by being folded in, or is
  written deliberately to `docs/learnings/cross-phase-decisions.md`.
- **Wiring the same offer into Project - Planner.** Deferred, not rejected — recorded in
  `docs/learnings/cross-phase-decisions.md`. Adding it here would double the wiring surface for a
  stage whose output is rewritten by the refiner anyway.
- **The reviewer editing the phase document.** It reports; Phase - Refiner edits. This keeps the
  reviewer a read-only leaf and keeps every document edit under the user's approval.
- **Prose-keyed tests.** Corpus tests are structural only. A check keyed to wording goes inert the
  moment anyone rewords the file.
- **Any change to `ports/` or `.github/`.** Generated surfaces. The maintainer propagates manually.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Final-check contract skill | Reading boundary, finding categories, the five-finding cap, report shape, and the blindness rule as an obligation on the spawner. | Skill authoring |
| 2 | `02a-phase-final-check.agent.md` | Read-only leaf subagent. Cold start, reads the phase document plus the repository, returns findings in its response. Writes no files. | Agent authoring |
| 3 | Phase - Refiner Phase 6 split | Offer step, fold-in step, relocated roadmap/discovery-context sync, and the `agents:` frontmatter entry. | Consumer wiring |
| 4 | Structural tests | Guards proving the agent exists, is declared by its parent, and the skill is referenced by both consumers. Each must be provably able to fail. | Test authoring |

## Technical Context

- **Insertion point.** `source_of_truth/agents/02-phase-refiner.agent.md` currently has Phase 5
  (Present Refined Document), Phase 6 (Write Document — document, discovery context, and roadmap
  sync together), and Phase 7 (Open Working Branch, which commits `eval: phase-affirmed`). Phase 6
  splits as described in Scope. The check must run after the document exists on disk, so the
  reviewer has a real file to read, and before the sync steps, so the roadmap is written once from
  final content.
- **Frontmatter.** Phase - Refiner declares `agents: [Web Researcher, Docs Writer]`. The new
  subagent's display name joins that list. An orchestrator can only spawn what it declares.
- **Delegation depth is one.** Phase - Refiner is user-invocable, so it may spawn a leaf. The new
  subagent must declare no `agents:` of its own.
- **Naming convention.** Hidden subagents take their parent's pipeline number plus a letter, as
  with `04a-feature-plan-expander` and `05a-baseline-worktree`. These are pipeline positions, not
  phase numbers, and must not be "corrected" to match phase numbering. Hidden subagents also carry
  `user-invocable: false` — see `05c-artifact-sweeper.agent.md` for the frontmatter shape.
- **Contract text must not be inlined.** `tests/test_agent_corpus_invariants.py` fails any block of
  10 or more contiguous lines repeated across three or more agent files. The subagent references
  the contract skill; it does not copy it. This is now a test constraint, not a style preference.
- **No test asserts corpus totals.** The invariants suite compares frontmatter, paths, and tool
  grants against disk and holds no counts, so adding an agent and a skill does not break it.
- **Read-only leaf pattern.** The Read-Only Agent instruction already governs agents that produce
  reports but never touch the repository under analysis. The new subagent inherits it directly; no
  new instruction file is needed. Note this agent is stricter than most: it writes nothing at all.
- **Test conventions.** `tests/` holds structural corpus guards — see
  `test_agent_corpus_invariants.py` for the existing agent-declaration checks and
  `test_pr_review_orchestrator.py` for the pattern of verifying an orchestrator declares its
  children. The `guard-integrity` skill governs proving a new guard can fail.
- **Authoring register.** Agent and skill files are machine-facing and read at runtime by an agent
  paying for every token. Dense but brief.

## Dependencies & Risks

- **Dependency**: None. This phase touches two agent files, one new skill, and tests. It shares no
  surface with Phase 01 or Phase 03.
- **Risk — the spawner briefs the reviewer anyway.** The single highest-value property of this
  phase is the cold start, and it is also the easiest thing to erode: a helpful spawning agent
  naturally wants to summarize context. *Mitigation*: state the prohibition in the spawn contract
  itself, and have a structural test assert the contract text exists at all. A structural test can
  confirm the rule is present but cannot confirm it is obeyed at runtime.
- **Risk — findings arrive as noise and the check gets declined by habit.** A reviewer that reports
  fifteen speculative observations trains the user to say no, and a check nobody accepts is worse
  than no check because it still appears to exist. *Mitigation*: fixed finding categories, a hard
  cap of five, a requirement that each finding cite something concrete, and explicit permission to
  report nothing.
- **Risk — the reviewer reports settled matters as gaps.** Decisions recorded in
  `DISCOVERY_CONTEXT.md` and `cross-phase-decisions.md` rather than in the phase document itself
  would otherwise read as unexamined. *Mitigation*: those files are inside the reading boundary.
- **Risk — reopening a document the user just called finished.** The fold-in step is deliberately a
  second explicit approval rather than an automatic edit, so the cost of a bad finding is one "no"
  and not an unwanted rewrite.
- **Risk — sync tests fail until the maintainer propagates.** Expected, and not a defect. Agents
  never run `scripts/propagate_master_assets.py`.

## Failure Modes

The check is advisory, so every failure resolves the same way: the workflow continues to the sync
step and the working branch, with the phase document exactly as the user left it.

- **The user declines the offer.** Normal outcome. Proceed.
- **The offer goes unanswered.** Treated as a decline. Proceed.
- **The reviewer errors, times out, or returns nothing usable.** Say so in one line and proceed. Do
  not retry, and do not attempt the review inline.
- **The reviewer returns findings and the user accepts none.** Proceed with the document unchanged.

## Success Criteria

- [ ] `source_of_truth/agents/02a-phase-final-check.agent.md` exists, parses, declares no child
      agents, and carries `user-invocable: false`.
- [ ] The new subagent's display name appears in Phase - Refiner's `agents:` frontmatter list.
- [ ] The contract skill exists and is referenced by both the subagent and Phase - Refiner.
- [ ] The contract states the reading boundary, the six finding categories, the cap of five, and
      that finding nothing is a valid result.
- [ ] The spawn contract explicitly prohibits passing conversation context, session summaries, or
      the refiner's own assessment of what matters.
- [ ] Phase - Refiner's workflow writes the phase document, then offers the check, then folds in
      accepted findings, then syncs the roadmap and discovery context, then opens the branch — in
      that order.
- [ ] The roadmap and phase discovery context are written exactly once per session, after any
      fold-in.
- [ ] Declining the check, receiving no answer, and a reviewer that fails outright all allow the
      workflow to reach the branch step with the document unchanged.
- [ ] The offer is reached from both refiner entry paths — refining an existing document and
      drafting one from scratch.
- [ ] No agent or skill file added by this phase repeats a 10+ line block found in three or more
      other agent files.
- [ ] Every new test is demonstrated to fail when its target is deleted or negated, per the
      `guard-integrity` skill.
- [ ] No file under `ports/` or `.github/` is hand-edited.

## QA Considerations

- **No UI, no manual QA document required.** This is pure corpus authoring — Markdown definitions
  and structural Python tests. No frontend, no API contract, no user-visible runtime behavior.
- **Affected test suites**: `tests/test_agent_corpus_invariants.py` and
  `tests/test_propagate_master_assets.py` see a new agent and a new skill. Neither asserts on
  corpus totals, so no count updates are expected. The duplicate-block guard is the one that can
  bite if contract text is inlined.
- **The behavior this phase adds is not automatically testable.** Whether the reviewer produces
  useful findings, and whether the spawner honors the blindness rule at runtime, can only be judged
  by running a real refinement session. Worth one manual exercise against an existing phase
  document before the phase is called complete.

## Notes for Feature - Decomposer

Suggested split into three features, in this order:

1. **The contract skill.** Write it first. It defines the reading boundary, the finding categories,
   the cap, and the report shape, and both remaining features depend on that vocabulary. Includes
   the blindness rule as an obligation on the spawner, not only on the reviewer.
2. **The subagent definition.** Consumes the skill by reference, never by copying. Read-only leaf,
   no child agents, no file writes, findings returned in its response.
3. **Phase - Refiner wiring plus tests.** The Phase 6 split, the offer and fold-in steps, the
   relocated sync, the frontmatter entry, and the structural guards. Tests land with the wiring
   because that is what they assert on.

Keep separate: the reviewer's judgment about a phase document (features 1 and 2) and the refiner's
orchestration of the offer (feature 3). Mixing them tends to produce a refiner that re-implements
the review inline.

The integration point between features 2 and 3 is the spawn prompt — feature 3 writes it, feature 2
defines what it must and must not contain. Decompose so that boundary is explicit rather than
discovered during implementation.

Feature 3 carries the only edit to an existing workflow. Treat the Phase 6 split as a reordering
with one insertion, not a rewrite: the write, sync, and branch steps keep their current content and
change only in position and grouping.
