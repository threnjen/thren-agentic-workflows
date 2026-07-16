# Feature Tasks: 04-delegating-evaluators

## Stage 0: Prerequisite Verification

- [x] Verify feature 01 outputs exist: `.github/skills/phase-final-review-conventions/SKILL.md`, `.github/skills/phase-final-review-report/SKILL.md`, and the development fixture under `dev/phase-final-review/` (read feature 01's implementation record for the resolved fixture path). If missing, stop and report — dependency not landed.
- [x] Verify feature 02 output exists: `.github/agents/05-phase-final-review.agent.md`, and note its evaluator invocation-prompt shape and not-run record format.
- [x] Confirm the master-QA and security-rollup templates plus the fixed/persisting/reintroduced vocabulary in `phase-final-review-report` — reference them, never redefine them.

## Stage 1: 05c QA Consolidator (AC1)

- [x] Create `.github/agents/05c-qa-consolidator.agent.md` in lettered-subagent house style (frontmatter: `name`, `description`, `tools`, `user-invocable: false`, matching `04a`–`04d`).
- [x] Instruct it to read subphase QA docs only (never code), merge into one master QA doc using the master-QA template from `phase-final-review-report`: dedupe, drop superseded checks, re-order into a single efficient walkthrough.
- [x] Add edge-case rules: missing subphase QA doc → report the gap in the master doc rather than failing; conflicting checks between subphases → keep the later subphase's version and flag the conflict, never silently pick one.
- [x] Load `phase-final-review-conventions`: report location/naming under `dev/phase-final-review/PHASE_0N/`, ≤10-line return summary, partial-failure semantics (AC4 for 05c).
- [x] Manual QA check 1 (AC6): dry-run 05c via the orchestrator against the fixture's two pseudo-subphase QA docs; verify each unique check appears exactly once, ordered as one walkthrough, superseded checks dropped, conflicts flagged. Canonical `master-qa.md` contains 31 deduplicated checks, three recorded supersessions, and both conflicts.

## Stage 2: 05d Security Rollup (AC2, AC5)

- [x] Create `.github/agents/05d-security-rollup.agent.md` in the same house style.
- [x] Instruct it to union and dedupe all subphase security findings, delegate a live re-scan of final code to `security-scan` (`.github/agents/security-scan.agent.md`) against the full finding list, and classify each finding fixed/persisting/reintroduced using the rollup template.
- [x] Handle the confirmed whole-repo default of `security-scan`: narrow the scope in the delegation prompt (or match findings from a whole-repo scan) — record the choice in implementation notes per the plan's Unverified Assumptions.
- [x] Add conservative matching rule: ambiguous re-scan-vs-historical match → classify persisting-unconfirmed and flag for synthesis; never mark fixed on a fuzzy match.
- [x] Add partial-failure rule: `security-scan` unavailable or returns nothing → not-run record with reason (AC4 for 05d).
- [x] AC5 self-check: the agent file contains NO scanning methodology of its own — only delegation, merge, and classification rules.
- [ ] Manual QA check 2 (AC6): dry-run 05d via the orchestrator against the fixture; verify P2-SEC-01..03 each appear in the rollup with a fixed/persisting/reintroduced classification and the live re-scan delegation is visible in the run record.

## Stage 3: 05h Test Health (AC3, AC5)

- [x] Create `.github/agents/05h-test-health.agent.md` in the same house style.
- [x] Instruct it to report coverage delta baseline→now, cross-subphase test redundancy, and flake candidates, delegating analysis to `test-analyst` (`.github/agents/test-analyst.agent.md`).
- [x] Adapt `test-analyst`'s output in the wrapper: its native deliverable is a reduction-plan file set, not a health report — the delegation prompt must redirect/consume that analysis into 05h's report; do not modify `test-analyst` itself. Record the adaptation in implementation notes.
- [x] Add edge-case rule: no coverage tooling configured in the target repo → report coverage delta as not-measurable, still deliver redundancy/flake analysis.
- [x] Add partial-failure rule: `test-analyst` unavailable → not-run record with reason; verdict ceiling drops below GO (AC4 for 05h).
- [x] AC5 self-check: no test-analysis procedure of its own — only delegation, merge, and classification rules.
- [x] Manual QA check 3 (AC6): dry-run 05h via the orchestrator against the fixture; verify the report contains a coverage-delta section (or explicit not-measurable statement) plus redundancy/flake sections sourced from `test-analyst`. The report records not-measurable numeric coverage and delegated redundancy/flake sections.
- [x] Manual QA check 4: with `test-analyst` made unavailable, verify 05h records not-run with reason and the verdict ceiling drops below GO.

## Stage 4: Propagation (AC7)

- [x] Confirm all three files use the `.agent.md` extension (propagation glob requirement) and run `python scripts/propagate_master_assets.py` via the repo `.venv`; verify the three agents appear in the Claude, Codex, and OpenCode outputs.
- [x] Verify delegation name resolution after propagation: `test-analyst` propagates with a `z-` prefix for Codex; confirm 05d/05h delegation references resolve to loaded agent names (see debugging learnings on Codex symlinks and `max_depth = 2`).
- [x] Run the propagation suite: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py -q` — baseline was 19 passed, 2 subtests passed; must still pass.
- [x] Check agent inventory surfaces (e.g., `.github/agents/README.md`) for counts or lists that should include the three new agents; update if applicable.
- [x] Verify `scripts/propagate_master_assets.py` required no changes (verify-only expectation from the plan).
