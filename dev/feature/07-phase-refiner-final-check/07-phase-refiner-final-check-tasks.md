# Feature Tasks: Phase Refiner Final-Check Integration

## Stage 1: Failing Integration Guards

- [ ] Confirm prerequisites `05-phase-final-check-contract` and `06-phase-final-check-reviewer` are implemented before this feature starts; discover the finalized skill slug/reference and parse the reviewer's exact display name from `source_of_truth/agents/02a-phase-final-check.agent.md` rather than inferring either name. (AC1, AC4, AC10)
- [ ] Choose and record a repository-consistent filename for `tests/[PROPOSED - name TBD: phase final-check contract guards]`; keep the module flat under `tests/` and do not invent a phase-scoped directory. (AC10–AC12)
- [ ] Add a propagator-backed topology scenario proving the reviewer source exists and parses, is hidden, has no child roster, uses only its upstream-defined minimal tools, is declared by the Refiner under its exact display name, and leaves `Web Researcher` plus `Docs Writer` in the Refiner roster. (AC1, AC10)
- [ ] Add a propagator-backed applicability scenario proving `source_of_truth/instructions/read-only-agent.instructions.md` applies to `02a-phase-final-check.agent.md`; deletion of that exact enumerated target must turn the guard red. (AC10, AC11)
- [ ] Add a scenario proving the Refiner and reviewer both reference the same finalized contract skill without copying the contract body into either agent. (AC10, AC12)
- [ ] Add scoped, whitespace-normalized, non-vacuous guards proving Entry A and Entry B converge before one shared post-write offer; the phase document write precedes the offer; discovery-context/roadmap synchronization follows the completed offer/fold-in path exactly once; and branch plus `eval: phase-affirmed` commit behavior remains afterward. (AC2, AC8, AC9, AC11)
- [ ] Add continuation scenarios proving accept, decline, and silence all terminate the offer; decline/silence continue unchanged; reviewer error, timeout, or unusable output reports one line and continues unchanged; and no branch performs retry or inline review. (AC3, AC5, AC11)
- [ ] Add a blindness-boundary scenario proving a reviewer spawn receives exactly the phase-document path and repository path and excludes conversation content, session summaries, settled-area briefings, and Refiner assessments. (AC4, AC11)
- [ ] Add findings-flow scenarios proving usable findings are relayed verbatim without ranking, filtering, paraphrase, or editorial comment; the user selects findings; only accepted findings are folded into a clean in-place rewrite; and zero accepted findings leaves the document unchanged. (AC6, AC7, AC11)
- [ ] Demonstrate every new guard red for its intended obligation by deleting the protected mechanism and by semantically negating it where applicable; verify non-vacuity checks fail when the scoped source region or expected structures are absent, then restore the sources before implementation. (AC11)
- [ ] Run the new focused module in its initial red state and retain failure evidence tied to AC1–AC12 before modifying Phase - Refiner. (AC1–AC12)

## Stage 2: Refiner Workflow Integration

- [ ] Update `source_of_truth/agents/02-phase-refiner.agent.md` frontmatter to add the exact reviewer display name parsed from the upstream agent while preserving `Web Researcher`, `Docs Writer`, and the existing `agent` tool. (AC1)
- [ ] Split the current Phase 6 responsibilities so both Entry A and Entry B write the final phase document before converging on one shared final-check offer. (AC2)
- [ ] Implement the optional offer so accept, decline, and no answer are terminal outcomes; decline and silence continue without changing the phase document. (AC3)
- [ ] On acceptance, delegate once to the hidden reviewer using only the concrete phase-document path and repository path, following the finalized shared skill's blindness contract and passing no session-derived briefing. (AC4)
- [ ] Add explicit error, timeout, and unusable-output continuations that report the failed attempt in one line, do not retry, do not review inline, and proceed with the unchanged document. (AC5)
- [ ] Relay usable reviewer findings verbatim, without filtering or editorializing, and ask the user which findings to apply. (AC6)
- [ ] Rewrite the phase document in place as a clean current source of truth for accepted findings only; use no change-log framing and make no write when none are accepted. (AC7)
- [ ] Place discovery-context writing and roadmap synchronization after all offer/fold-in outcomes, preserve their existing conditional semantics, and ensure each responsibility executes exactly once. (AC8)
- [ ] Preserve the existing branch create/resume sequence, staging of session-modified `docs/phases/` files, exact `eval: phase-affirmed` commit message, and downstream pipeline handoff after synchronization. (AC9)
- [ ] Keep the Refiner body terse by referencing the upstream skill instead of duplicating its reviewer rubric, blindness rules, or response contract; add no persistent logs or findings artifact. (AC2–AC9, AC12)
- [ ] Run the focused module and confirm the previously red topology, workflow, continuation, blindness, and findings-flow scenarios now pass. (AC1–AC12)

## Stage 3: Regression and Smoke Verification

- [ ] Re-run each deletion and semantic-negation mutation against the completed integration, confirm the intended focused guard fails, restore the source exactly, and confirm the focused module returns green. (AC11)
- [ ] Run `uv run pytest tests/test_agent_corpus_invariants.py` unchanged and confirm the feature introduces no roster, frontmatter, tool, instruction-glob, or duplicate-block regression. (AC10, AC12)
- [ ] Run `uv run pytest tests/test_propagate_master_assets.py` unchanged and distinguish feature regressions from source/generated synchronization failures that require maintainer propagation. (AC12)
- [ ] Run `uv run pytest tests/` and compare with the captured baseline of 230 passed and 12 known failures out of 242 collected; investigate any additional failure without remediating the pre-existing set. (AC12)
- [ ] Smoke-test a real Entry A session from an existing phase document: accept the offer, confirm the cold-start reviewer can return useful findings or zero findings, verify the payload contains only the two allowed paths, and confirm no artifact is created. (AC13)
- [ ] Smoke-test a real Entry B session from a standalone feature description: confirm it reaches the same post-write offer and continuation, exercise decline or no answer, and verify synchronization plus branch behavior continues with the document unchanged. (AC2, AC3, AC8, AC9, AC13)
- [ ] In at least one real smoke path with usable findings, confirm findings are relayed verbatim, apply only a selected subset, and verify the phase document is rewritten cleanly before one synchronization pass. (AC6–AC8, AC13)
- [ ] Verify `ports/` and `.github/` remain untouched, do not run propagation, and report maintainer propagation pending for generated output after source authoring. (AC12)
