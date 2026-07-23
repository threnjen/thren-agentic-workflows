# Tasks: 17-narrative-spec-docs

## Stage 1: Narrative Writer Agent

- [x] Verify feature 14 outputs exist on the branch: orchestrator agent file, `engagement-workspace` skill, and the `mode` field in `source_of_truth/skills/engagement-configuration/SKILL.md`; record the actual names 14 chose
- [x] Create the narrative-writer agent `source_of_truth/agents/engagement-narrative-writer.agent.md` [PROPOSED - name TBD] as a hidden subagent (`user-invocable: false`) with read/search/edit-class grants only — no shell, no web (AC1–AC3)
- [x] Define the business design document contract: per pair, client-facing, business terms, derived from analysis-branch docs-writer set and graphs; no engagement source content reproduced (AC1)
- [x] Define the intended-behavior specification contract with **mandatory** observable-behavior and environmental-assumptions sections (runtime versions, services, configuration); unverifiable assumptions stated as assumptions with what was observed (AC2)
- [x] Fix and record the intended-behavior spec's filename/location within the workspace layout — this is the contract feature 18 references; record all three document names for 18's manifest schema (AC2)
- [x] Define the before/after workflow narratives contract: as-was/as-is walkthroughs for components with functional changes; both value-story modes driven by the engagement config's `mode` — pure-modernization framing excludes intentional-change language; no-delta pairs get an honest statement, not fabricated deltas (AC3)
- [x] Name the evidence sources in the definition (docs-writer set, graphs, 15's retained reports where relevant) and exclude git-diff and engagement-source reproduction (AC1–AC3)
- [x] State the value-story-mode framing rule once in a shared place (by reference to the config skill's `mode` definition, per 16's precedent) rather than restating 16's rules; document the choice
- [x] Brevity pass: behavior, constraints, and output contract each stated once; shared rules referenced, not restated; if the single definition cannot stay terse across all three contracts, split and record the decision (AC6)

## Stage 2: Orchestrator Wiring, Propagate & Verify

- [x] Add the narrative writer to the orchestrator's `agents:` roster and per-pair loop step under the compact-handoff contract, referencing it by backticked display name; outputs go into the workspace layout with inherited boundaries passing through; client-facing docs lead with business meaning, technical evidence in appendices (AC4)
- [x] Run `python3 scripts/propagate_master_assets.py --once` until convergence; confirm a second run reports zero changes (AC5)
- [x] Update marker-guard counts in `tests/test_propagate_master_assets.py` (roots table ~lines 765–779) by recounting from disk (`ls ports/<harness>/agents`), not incrementing from memory (AC5)
- [x] Run `uv run pytest tests/` and confirm no new failures against the 233-passed baseline (AC5)
- [x] Record in the implementation record: final agent name(s), the three document filenames (especially the AC2 spec name 18 consumes), and the mode-rule placement decision
