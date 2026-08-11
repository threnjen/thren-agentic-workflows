# Feature Tasks: Phase Final-Check Contract

## Stage 1: Contract Skill

- [x] Review `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`, `docs/phases/DISCOVERY_CONTEXT.md`, and `docs/learnings/cross-phase-decisions.md` as the authoritative sources for AC1–AC8.
- [x] Select a concise, collision-free final slug for `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md`; use the same value for the directory and frontmatter `name`, and record it for features 06 and 07.
- [x] Create the selected skill directory and `SKILL.md` with valid, terse `name` and `description` frontmatter following the existing directory-based convention. (AC1, AC8)
- [x] Define the permitted reading boundary: the supplied phase document and repository-local facts available to a newcomer, including `docs/phases/DISCOVERY_CONTEXT.md` and `docs/learnings/cross-phase-decisions.md` when present. (AC2)
- [x] State that missing optional committed-context files do not fail or halt review; the reviewer proceeds with the supplied phase document and available repository state. (AC2)
- [x] Define the spawner's blindness obligation so the spawn input contains only the phase-document path and repository path and forbids conversation content, session summaries, settled-area briefings, and the spawner's assessment of what deserves attention. (AC3)
- [x] Define exactly the six eligible finding categories: contradiction, ambiguous scope boundary, uncheckable success criterion, undefined term, unaddressed dependency or risk, and deliverable without a matching success criterion. (AC4)
- [x] Require every finding to cite a phase-document location or concrete repository fact, consolidate similar observations, omit weak or speculative observations, and prohibit severity ratings. (AC5)
- [x] Limit the report to at most five findings, require disclosure when additional qualifying findings were omitted, and define a plain no-qualifying-findings response without padding. (AC5, AC6)
- [x] Exclude roadmap/discovery-context synchronization state, pass/fail judgments, blocking thresholds, retry loops, repository writes, persisted findings, and direct phase-document edits. (AC7)
- [x] Keep reviewer error handling, user approval, fold-in behavior, workflow continuation, synchronization, branch, and commit concerns out of the shared skill. (AC1, AC7, AC8)
- [x] Edit no generated surface and do not run propagation. (AC8)

## Stage 2: Contract Review

- [x] Trace every AC1–AC8 obligation from the plan to one authoritative statement in the skill, with no requirement represented only by an example or implication.
- [x] Verify the skill separates permitted reading, finding eligibility, and response shape without restating the same obligation in multiple sections.
- [x] Verify the selected slug and contract vocabulary are sufficient for `06-phase-final-check-reviewer` and `07-phase-refiner-final-check` to consume by reference.
- [x] Verify the skill contains no consumer-only failure recovery, Refiner interaction, fold-in, synchronization, or branch workflow.
- [x] Inspect consumer plans and confirm the shared body will not need to be copied into either agent definition.
- [x] Run `uv run pytest tests/test_agent_corpus_invariants.py` as existing structural regression evidence for valid skill frontmatter and duplicate-block safety; do not treat it as semantic proof of the contract.
- [x] Run `uv run pytest tests/` and compare the result with the captured baseline of 230 passed and 12 pre-existing failures; report any additional failure as a regression and do not remediate unrelated baseline failures.
- [x] Record that focused semantic guards, deletion/negation mutation evidence, and the combined smoke test remain owned by `07-phase-refiner-final-check`.
- [x] Confirm only the selected new `source_of_truth/skills/<slug>/SKILL.md` source artifact was added by implementation; `ports/`, `.github/`, agents, and tests remain untouched.
- [x] Report propagation as pending for the maintainer rather than running it.
