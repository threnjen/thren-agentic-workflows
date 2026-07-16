# Feature Tasks: 02-final-review-orchestrator

## Stage 0: Prerequisites

- [x] Verify feature 01-review-foundation has landed: `.github/skills/phase-final-review-conventions/SKILL.md`, `.github/skills/phase-final-review-report/SKILL.md`, `.github/skills/worktree-baseline/SKILL.md`, `.github/agents/05a-baseline-worktree.agent.md`, and the dry-run fixture all exist; stop and report if any are missing
- [x] Establish test baseline: run `python3 -m pytest tests/ -q` and record pass/fail state before changes

## Stage 1: Orchestrator Skeleton (AC1, AC2, AC5)

- [x] Create `.github/agents/05-phase-final-review.agent.md` with YAML frontmatter (`name`, `description`, `tools`, `agents`) following the numbered-orchestrator house style of `04-phase-execute.agent.md`
- [x] Declare the role statement: coordinates evaluator subagents; never reads code, diffs, or full subphase docs — only structured reports under `dev/phase-final-review/PHASE_0N/`
- [x] Load `phase-final-review-conventions` by reference; do not restate its rules or duplicate report templates from `phase-final-review-report`
- [x] State the ≤10-line return-summary contract as an enforced requirement on every spawned subagent
- [x] Add the startup model check: warn when not running on a state-of-the-art model, before any work begins
- [x] Declare the model-tier assignment: deep-judgment evaluators (05b, 05e, 05f, 05l) on top tier; mechanical sweeps (05g, 05j, 05k) on cheap tier

## Stage 2: Preflight (AC3, AC4)

- [x] Write preflight as a linear checklist — baseline → subphase discovery → artifact inventory → model check — with one loud failure mode per step
- [x] Baseline suggestion, ledger path: derive the pre-phase baseline commit (last commit before subphase a's first feature commit) from `eval/runs/*/ledger-commits.jsonl`; treat `ledger-events.jsonl` as optional supplementary data (per Discovery Delta, only `ledger-commits.jsonl` exists in real runs)
- [x] Baseline suggestion, fallback path: when ledgers are absent, malformed, or empty, derive from `eval:`-prefixed checkpoint commits; document fallback as a first-class path and name which path was used in output
- [x] Fallback exhausted (no `eval:` commits): present candidate commits and require the user to pick — never guess silently
- [x] Require explicit user confirmation of the baseline commit on both paths, then delegate checkout to `05a-baseline-worktree`
- [x] Subphase discovery: enumerate `docs/phases/PHASE_0N*/` directory patterns; on zero subphases, refuse with a message pointing at `prod-code-review` for single un-subdivided phases
- [x] Artifact inventory: per subphase, inventory implementation records, QA docs, and security reports per the conventions skill's missing-artifact definition; refuse with a clear itemized message when any required artifact is missing

## Stage 3: Run Semantics and Verdict Lifecycle (AC6, AC7)

- [x] Partial-failure rules: an evaluator failure does not abort the run; record evaluator name + reason as a not-run entry and pass all failure records to synthesis
- [x] Bound waiting behavior for hung evaluators; record a not-run entry whether an evaluator hangs or fails
- [x] State the GO ceiling: never report GO while any check is missing — maximum is "no blockers found, coverage incomplete"
- [x] Define the evaluator invocation prompt shape and the not-run record format (contracts consumed by features 03–06), aligned with `phase-final-review-conventions`
- [x] Re-invocation handling: define deterministic behavior when prior reports exist under `dev/phase-final-review/PHASE_0N/` — timestamped run subdirectory `[PROPOSED - name TBD]`; record the final naming decision in implementation notes and keep it consistent with the conventions skill's report-location contract
- [x] Verdict write-back: on completion, update only the target phase's status line in `docs/phases/PROJECT_ROADMAP.md` and the phase summary — never restructure the roadmap
- [x] State the full-re-run policy: after remediation the entire review re-runs; no partial re-run

## Stage 4: Propagation and Inventory (AC8)

- [x] Add `05 Phase - Final Review` to the `.github/agents/README.md` user-facing agent inventory (and any surface carrying agent counts), per the review-learnings inventory-surface rule
- [x] Run `python3 scripts/propagate_master_assets.py`; verify the agent appears in `.claude/agents/` and Codex/OpenCode outputs with no unrelated diffs and no script changes
- [x] Run `python3 -m pytest tests/test_propagate_master_assets.py -q` and confirm it passes

## Stage 5: Manual QA Evidence (plan Section F)

- [x] QA 1: with `eval/runs/` ledgers present, preflight suggests the last commit before the phase's first feature commit and asks for confirmation
- [x] QA 2: with `eval/runs/` emptied, preflight still suggests a baseline from `eval:` commit conventions and names the fallback path in output
- [x] QA 3: against the 01-review-foundation fixture with one required artifact deleted, preflight refuses with an itemized missing-artifact message (fixture is the only subphase-layout substrate — no real `PHASE_0Na` dirs exist in this repo)
- [x] QA 4: in a wrong-model session, the orchestrator emits the model-tier warning before any work
- [x] QA 5: with a simulated evaluator failure record, the run completes, the not-run check is named, and the verdict is not GO
