# Feature Tasks: Phase Final-Check Reviewer

## Stage 1: Hidden Leaf Definition

- [ ] Confirm `05-phase-final-check-contract` is complete, read its finalized `SKILL.md`, and record the exact selected skill slug; do not use the `[PROPOSED - name TBD: phase-final-check]` placeholder as a concrete reference. (AC4)
- [ ] Resolve the Discovery Delta by adding `**/02a-phase-final-check.agent.md` to `source_of_truth/instructions/read-only-agent.instructions.md` so the phase's direct-inheritance claim is true. Preserve the existing enumerated allowlist and do not create a new instruction file. (AC3, AC7)
- [ ] Choose a concise, collision-safe `[PROPOSED - name TBD]` display name consistent with nearby numbered hidden agents, and record it for Feature 07's exact roster and spawn references. (AC1)
- [ ] Create `source_of_truth/agents/02a-phase-final-check.agent.md` with valid `name`, `description`, `tools: [read, search]`, and `user-invocable: false` frontmatter. Omit the `agents:` key and every edit, execute, delegation, web, and task-list tool. (AC1, AC2)
- [ ] Define one two-path input contract: the supplied repository path and supplied phase-document path only. Explicitly refuse conversation content, session summaries, settled-area briefings, or the caller's assessment as review input. (AC5)
- [ ] Reference the finalized Feature 05 skill exactly once as the authoritative reading, blindness, finding-eligibility, cap, exclusion, and response contract; do not copy or paraphrase a contract-sized block into the agent. (AC4, AC5, AC6)
- [ ] Implement the cold-start workflow: read the supplied phase document, optionally read available committed newcomer context, inspect concrete repository facts as needed, and evaluate only the phase document's own content. (AC5)
- [ ] Treat absent optional `docs/phases/DISCOVERY_CONTEXT.md` or `docs/learnings/cross-phase-decisions.md` as non-fatal. If the supplied phase document is missing or unreadable, report that exact problem and stop without searching for a substitute. (AC5)
- [ ] State the reviewer's stricter response-only boundary: it never edits or creates any file, including phase documents, roadmaps, discovery contexts, learnings, or findings artifacts, even though the general read-only instruction permits assigned report documents. (AC3, AC7)
- [ ] Keep review scope off roadmap/discovery synchronization state and exclude verdicts, severity, pass/fail gates, retries, fold-in behavior, and failure recovery owned by the Refiner. (AC5, AC6, AC7)
- [ ] Keep the body stateless, dense, and brief, with no logs, external access, general refinement advice, duplicated rubric, or generated-surface instructions beyond the source-only boundary. (AC2–AC7)

## Stage 2: Return Contract Verification

- [ ] Load the new agent through `scripts/propagate_master_assets.py` and verify the exact path, parsed display name, non-empty description, `user_invocable is False`, empty child roster, and exact `tools == ["read", "search"]`. (AC1, AC2)
- [ ] Use the propagator's instruction applicability logic to verify `read-only-agent.instructions.md` now applies to the new `02a` path, while the agent's own body retains the stricter no-file-output rule. (AC3, AC7)
- [ ] Inspect the shared-skill reference against Feature 05's final directory/frontmatter slug and confirm the agent does not reproduce a 10-line contract block or define a competing review rubric. (AC4)
- [ ] Verify the workflow handles the supplied paths only, permits missing optional committed context, reports a missing supplied phase document without substitution, and excludes conversation-history inference and surrounding-file synchronization findings. (AC5, AC7)
- [ ] Verify the return contract is directly usable by Feature 07: at most five concrete findings, phase-location or repository-fact evidence, no severity or verdict, explicit cap disclosure, and a plain zero-findings response. Use scenario descriptions; do not invent test method or class names. (AC6)
- [ ] Provide Feature 07 with the exact parsed reviewer display name, exact shared-skill slug, and focused-guard scenarios for file existence, hidden/leaf topology, exact tools, instruction applicability, skill reference, no-write boundary, and bounded response states. (AC1–AC7)
- [ ] Run the existing verified regression classes in `tests/test_agent_corpus_invariants.py` (`RosterTests`, `FrontmatterShapeTests`, and `DuplicateBlockTests`) without modifying them, and record the exact result. (AC1–AC4)
- [ ] Run relevant parser and instruction-`applyTo` checks from `tests/test_propagate_master_assets.py`; distinguish the known wildcard enumeration baseline failure from any new failure caused by the `02a` allowlist entry. (AC1–AC4, AC7)
- [ ] Defer the real cold invocation, zero-finding case, more-than-five truncation case, blindness smoke test, and mutation-tested focused guards to `07-phase-refiner-final-check`, as declared by the phase and sibling plan. (AC5–AC7)
- [ ] Run `uv run pytest tests/` and compare against the captured 2026-08-11 baseline of 230 passed and 12 failed; report any additional failure as a regression. (AC1–AC7)
- [ ] Inspect the final diff to confirm it contains only the new reviewer and the required existing read-only-instruction allowlist update, with no Phase - Refiner, shared-skill, test, phase-document, learning, dependency, `ports/`, or `.github/` edits. (AC1–AC7)
- [ ] Record that maintainer propagation is pending and that no propagation command was run. (AC1–AC4)
