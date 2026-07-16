# Phase 3: Phase Final Review Agent Family

**Status**: Implemented — release blocked (NO-GO); blockers are owned by Phase 04
**Depends on**: None (independent of the hook phases; consumes existing pipeline assets only)
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md` (§ "Phase 03 Design Notes" — the user-directed design capture this summary is authored from), `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` (remediation phase that closes this phase's NO-GO findings)

> **Renumbered 2026-07-16: this phase was previously Phase 05.** It was planned
> and executed out of numeric order (immediately after Phase 02), so it was
> renumbered to 03 to match the order work actually happened. Two naming
> details deliberately did **not** change:
>
> - The `05-phase-final-review` orchestrator and its `05a`–`05l` evaluators keep
>   their numbers. Agent numbering marks pipeline position (`01-project-planner`
>   → `02-phase-refiner` → `03-feature-decomposer` → `04-phase-execute` →
>   `05-phase-final-review`), not the phase that built them.
> - The development fixture keeps its legacy identifier
>   `dev/phase-final-review/fixtures/PHASE_05/` (with pseudo-subphases
>   `PHASE_05a`/`PHASE_05b`) and its report root
>   `dev/phase-final-review/PHASE_05/`. These are synthetic phase identifiers
>   pinned to recorded commit SHAs; renaming them would invalidate the fixture
>   contract for no benefit.
>
> Older documents (including the Phase 01 and Phase 02 summaries) refer to the
> pre-renumber scheme. See the mapping table in
> `docs/phases/PROJECT_ROADMAP.md`.

## What's New

After a large phase is implemented across multiple subphases (`PHASE_0Na`–`PHASE_0NX`), there is currently no single step that looks at the whole phase end-to-end. Each subphase gets its own review, QA doc, and security scan, but nothing re-checks earlier subphases' acceptance criteria against the final code, merges the per-subphase QA docs into one walkthrough, or asks "is this whole phase actually ready to ship?" This phase adds a **Phase Final Review** flow: one orchestrator agent you invoke after finishing a large phase, which quietly fans out to a dozen specialist evaluators and hands you back a single severity-ordered go/no-go readiness report — plus a consolidated master QA doc, a security rollup, and harvested lessons for the instruction files.

## Objective

Build the `05-phase-final-review` orchestrator, its `05a`–`05l` evaluator subagents, and three supporting skills so that an entire multi-subphase phase can be evaluated end-to-end — change narrative, QA consolidation, security rollup, AC regression, seam analysis, artifact/test/consistency/dependency audits, learnings harvest, and readiness synthesis — with strict context discipline throughout.

## Scope

### In Scope

- **Orchestrator**: `.github/agents/05-phase-final-review.agent.md` — numbered-orchestrator house style (matching `04-phase-execute` + lettered subagents). Never reads code, diffs, or full subphase docs; consumes only structured reports subagents write to `dev/phase-final-review/PHASE_0N/`; each subagent returns a ≤10-line summary.
- **Preflight behavior**: auto-suggest the pre-phase baseline commit (last commit before subphase a's first feature commit) with user confirmation; derive the suggestion from ledger files when present, falling back to commit-message conventions when ledgers are absent (ledgers live in gitignored `eval/runs/` and are local-only — the fallback path is a first-class requirement, not an edge case). Discover subphases from `docs/phases/PHASE_0N*/`; inventory pipeline artifacts (implementation records, QA docs, security reports) and fail loudly on anything missing before evaluating.
- **Partial-failure semantics**: if an evaluator fails mid-run (crash, unavailable dependency, worktree error), the run completes with the remaining evaluators; the readiness report enumerates exactly which checks did not run, and the verdict can never be GO while any check is missing — the ceiling is "no blockers found, coverage incomplete." Declared in `phase-final-review-conventions` and enforced by `05l`.
- **Verdict lifecycle**: on completion, the orchestrator updates the phase's status line in `PROJECT_ROADMAP.md` and the phase summary to reflect the go/no-go verdict. After remediation, the policy is a full re-run of the entire review — no partial re-run machinery.
- **Development fixture**: a practice fixture directory built from copies of the real Phase 01/02 pipeline artifacts (QA docs, coverage maps, security scans, implementation records — including Phase 02's genuine NO-GO case), arranged in the subphase layout the orchestrator expects (`PHASE_0Xa/`, `PHASE_0Xb/`). Used to dry-run each evaluator as it is built. Fixture location: `dev/phase-final-review/fixtures/` (or equivalent gitignore-reviewed path chosen during decomposition).
- **Model-tier policy**: recommend/require a state-of-the-art model and warn at startup if not on one; deep-judgment subagents (05e, 05f, 05l) inherit the top tier, mechanical sweeps (05g, 05k) run on a cheap tier.
- **Evaluator subagents** (`05a`–`05l`, all read-only against source):
  - `05a-baseline-worktree` — check out the confirmed baseline commit in a git worktree; return the path.
  - `05b-change-narrator` — whole-phase change narrative baseline→HEAD with per-subphase attribution and multi-subphase churn hotspots; chunks diffs internally, may spawn per-directory readers.
  - `05c-qa-consolidator` — master QA doc: merge all subphase QA docs, dedupe, drop superseded checks, re-order into one efficient walkthrough. Reads QA docs only.
  - `05d-security-rollup` — union + dedupe of all subphase security findings; delegates a live re-scan of final code to the existing `security-scan` agent; classifies findings fixed / persisting / reintroduced.
  - `05e-ac-regression` — re-verify EVERY subphase's acceptance criteria against the FINAL codebase (later subphases may have broken earlier ACs); one hidden verifier per subphase.
  - `05f-seam-analyzer` — integration seams between subphases: interface mismatches, duplicated logic, orphaned scaffolding; built on code-review-graph tools (`get_impact_radius`, `get_bridge_nodes`).
  - `05g-artifact-sweeper` — debug statements, TODOs/FIXMEs, temp feature flags, commented-out/dead code introduced since baseline (`refactor_tool` dead-code detection scoped to the phase diff). Mechanical.
  - `05h-test-health` — coverage delta baseline→now, cross-subphase test redundancy, flake candidates; delegates to the existing `test-analyst` agent.
  - `05i-learnings-harvester` — mine review records, fix commits, and QA failures for recurring mistakes; draft `.github/learnings/` entries and instruction-file updates feeding the instructions-writer/evaluator loop.
  - `05j-consistency-auditor` — convention drift across subphases (naming, error handling, patterns) with recommended canonical forms.
  - `05k-dependency-auditor` — new dependencies introduced across the phase: licenses, vulnerabilities, competing/duplicate libraries. Mechanical.
  - `05l-readiness-synthesizer` — reads all reports (never code); produces the go/no-go readiness report with a severity-ordered blocking list. Extends `prod-code-review` conventions one level up rather than duplicating them.
- **Skills** (in `.github/skills/`):
  - `phase-final-review-conventions` — shared constraints for all 05x evaluators (report locations/naming, severity levels, ≤10-line return-summary contract, read-only worktree etiquette, model-tier notes). Mirrors `auditor-conventions`.
  - `phase-final-review-report` — output templates: master QA doc, security rollup, AC-regression matrix, readiness report. Mirrors `implementation-record` / `eval-feature-decomposition-report`.
  - `worktree-baseline` — reusable "check out commit X in a worktree, hand back the path" skill (candidate for reuse by `eval-grader`).
- **Propagation**: all new agents and skills join `scripts/propagate_master_assets.py` output for Claude/OpenCode/Codex, consistent with the rest of `.github/`.

### Out of Scope

- Any hook work (Phases 01–04 territory) — this phase touches no `.github/hooks/` assets.
- Changing the existing per-subphase pipeline (`04-phase-execute` and its subagents) — Phase Final Review runs *after* it, never replaces it.
- Modifying `prod-code-review` itself — `05l` extends its conventions one level up; it does not rewrite the existing gate.
- Auto-remediation of findings — the readiness report identifies blockers; fixing them is follow-up work through the normal feature pipeline.
- Evaluation of single small phases without subphases (the existing `prod-code-review` gate already covers that scale).
- A "combine sibling phases" mode (pointing the orchestrator at several separate top-level phases and treating them as one) — the development fixture covers testing needs; sibling-phase review is a possible future follow-up.
- Partial re-run machinery (re-running only failed evaluators after remediation) — the policy is always a full re-run.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Conventions + report skills + baseline infrastructure + fixture | `phase-final-review-conventions`, `phase-final-review-report`, `worktree-baseline` skills, `05a-baseline-worktree`, and the Phase 01/02-derived development fixture in subphase layout | Skill authoring, worktree tooling, fixture assembly |
| 2 | Orchestrator + preflight | `05-phase-final-review.agent.md` with baseline-commit suggestion, subphase discovery, artifact inventory, model-tier warning | Orchestration, ledger parsing |
| 3 | Mechanical evaluators | `05g-artifact-sweeper`, `05k-dependency-auditor`, `05j-consistency-auditor` | Cheap-tier sweep agents |
| 4 | Delegating evaluators | `05c-qa-consolidator`, `05d-security-rollup`, `05h-test-health` (reuse `security-scan`, `test-analyst`) | Report merging, agent delegation |
| 5 | Deep-judgment evaluators | `05b-change-narrator`, `05e-ac-regression`, `05f-seam-analyzer` | Diff chunking, graph tooling, hidden verifiers |
| 6 | Synthesis + learnings | `05l-readiness-synthesizer`, `05i-learnings-harvester` | Go/no-go report, instructions-loop integration |

## Technical Context

- **House style to follow**: numbered orchestrator + lettered subagents (`04-phase-execute` + `04a`–`04d` in `.github/agents/`); shared-convention skills (`auditor-conventions`); report-template skills (`implementation-record`, `eval-feature-decomposition-report`). The `05-` prefix is unclaimed in `.github/agents/`.
- **Pipeline artifacts consumed**: implementation records (`dev/feature/[0N-task-name]/*-implementation.md`), review records, QA docs (`docs/phases/PHASE_0N/PHASE_0N_QA.md`), security reports (`PHASE_0N-security-scan.md`), the ledger (`ledger-commits.jsonl` / `ledger-events.jsonl` conventions used by `eval-grader`).
- **Agents reused by delegation**: `security-scan` (05d), `test-analyst` (05h), instructions-writer/evaluator loop (05i output feeds it).
- **Graph tooling**: `05f` and `05g` build on the code-review-graph MCP server (`get_impact_radius`, `get_bridge_nodes`, `refactor_tool` dead-code detection).
- **Precedent for readiness gates**: `prod-code-review` agent/skill — 05l operates one level up (whole phase vs. single feature set) and extends its conventions.
- **Propagation**: `scripts/propagate_master_assets.py` regenerates Claude/OpenCode/Codex outputs from `.github/` — new agents/skills must be authored as source-of-truth assets there.
- **Fixture source material**: Phases 01 and 02 of this very project produced full artifact sets (QA docs, coverage maps, security scans, a genuine NO-GO verdict) under `docs/phases/PHASE_01/` and `PHASE_02/`. They are separate top-level phases, not subphases of one phase, so the development fixture copies them into the subphase layout the orchestrator expects rather than pointing the orchestrator at them directly.
- **Ledger reality**: ledger files (`ledger-commits.jsonl` / `ledger-events.jsonl`) live under `eval/runs/`, which is gitignored — they exist only on the machine where the phase was originally executed. Commit-message conventions (e.g., `eval:`-prefixed checkpoint commits) are the durable signal and the required fallback for baseline derivation.

## Dependencies & Risks

- **Dependency**: existing pipeline artifact formats (implementation records, QA docs, security scans, ledger conventions) — the evaluators parse these; format drift breaks them. Mitigation: preflight artifact inventory fails loudly on missing/unrecognized artifacts before any evaluation runs.
- **Dependency**: ledger files may be absent (gitignored, local-only). Mitigation: baseline derivation falls back to commit-message conventions; user confirmation is required on either path.
- **Dependency**: code-review-graph MCP server availability for 05f/05g. Mitigation: partial-failure semantics — those evaluators report as not-run with a stated reason (e.g., "graph unavailable, manual seam review required"), the run completes, and the verdict ceiling drops below GO.
- **Risk**: context blowout — 12 evaluators over a large phase can generate enormous reports. Mitigation: the ≤10-line return-summary contract and reports-on-disk pattern are hard requirements in `phase-final-review-conventions`, not suggestions; 05l reads reports only, never code.
- **Risk**: baseline-commit misidentification silently skews every diff-based evaluator (05b, 05g, 05h). Mitigation: baseline is auto-*suggested* but always user-confirmed in preflight.
- **Risk**: an evaluator failure silently reads as a clean check. Mitigation: the readiness report must enumerate not-run checks by name, and 05l is prohibited from issuing GO while any check is missing.
- **Risk**: overlap/duplication with `prod-code-review` blurs which gate is authoritative. Mitigation: explicit scope line — `prod-code-review` gates a feature set within one phase; Phase Final Review gates a multi-subphase phase; 05l extends rather than forks its conventions.
- **Risk**: subagent sprawl (12 new agents + 3 skills) makes this the largest single-phase asset addition yet; propagation or naming inconsistencies multiply. Mitigation: conventions skill is Deliverable 1 and every subsequent agent is authored against it; propagation runs and is verified per feature, not once at the end.

## Success Criteria

- [ ] `05-phase-final-review.agent.md` and all twelve `05a`–`05l` subagent files exist in `.github/agents/`, follow the numbered/lettered house style, and propagate cleanly via `scripts/propagate_master_assets.py` to Claude, OpenCode, and Codex outputs.
- [ ] The three skills (`phase-final-review-conventions`, `phase-final-review-report`, `worktree-baseline`) exist in `.github/skills/` and propagate cleanly.
- [ ] Preflight correctly auto-suggests the baseline commit for a real multi-commit phase in this repo, requires user confirmation, discovers subphase directories, and refuses to proceed (with a clear itemized message) when a required artifact is missing.
- [ ] Preflight produces a correct baseline suggestion with ledger files absent, using commit-message conventions alone (verified by running against history with `eval/runs/` removed or empty).
- [ ] With one evaluator forced to fail during a dry run, the run completes, the readiness report names the missing check, and the verdict is not GO.
- [ ] On completion, the phase's status line in `PROJECT_ROADMAP.md` and the phase summary reflects the review verdict without manual editing.
- [ ] Orchestrator warns at startup when not running on a state-of-the-art model; deep-judgment vs. mechanical model-tier assignments are declared in the agent files.
- [ ] The development fixture exists: Phase 01/02 artifact copies arranged in subphase layout, sufficient for every evaluator to run against.
- [ ] A dry run of the full flow against the development fixture produces: a master QA doc, a security rollup with fixed/persisting/reintroduced classification, an AC-regression matrix covering every subphase AC, and a severity-ordered go/no-go readiness report in `dev/phase-final-review/`.
- [ ] Every subagent's return payload in the dry run is ≤10 lines, with full detail on disk in `dev/phase-final-review/PHASE_0N/`.
- [ ] `05d` and `05h` demonstrably delegate to the existing `security-scan` and `test-analyst` agents rather than reimplementing them.
- [ ] `05i` produces at least one draft `.github/learnings/` entry or instruction-file update from real review-record history in this repo.

## QA Considerations

- No frontend/UI changes — no manual QA docs required on that basis.
- This phase ships agents and skills, not application code; QA is primarily **behavioral**: dry-run the orchestrator against real Phase 01/02 artifacts and verify report structure, return-summary discipline, and preflight failure modes. A manual QA checklist for the dry-run walkthrough is recommended.
- Propagation QA: after each feature, verify Claude/OpenCode/Codex outputs regenerate without diff noise in unrelated assets.
- Test impact: new pytest coverage is expected only where logic is scriptable (e.g., baseline-commit derivation from ledger data, if implemented as a script); agent/skill markdown is validated through the propagation script's existing test suite.

## Notes for Feature - Decomposer

- **Conventions first**: Deliverable 1 (conventions skill + report skill + `worktree-baseline` + `05a` + the development fixture) must be the first feature — every other agent is authored against those contracts and dry-run against the fixture as it lands.
- **Orchestrator second**: the preflight/orchestrator feature (Deliverable 2) should land before the evaluators so each evaluator can be dry-run through it as it's added.
- **Group evaluators by kind, not alphabetically**: mechanical sweeps (05g/05j/05k) share a cheap-tier, config-driven shape; delegating evaluators (05c/05d/05h) share a merge-and-delegate shape; deep-judgment evaluators (05b/05e/05f) each warrant careful individual design. Suggested decomposition is the six deliverable rows above (2–6 features is the target band; 6 is acceptable given phase size, or merge rows 3+4 into one feature if five is preferred).
- **Careful separation**: 05l (readiness synthesis) must depend only on report files, never on other agents' internals — keep its feature last and its inputs pinned to the `phase-final-review-report` templates.
- **Integration points**: 05d→`security-scan`, 05h→`test-analyst`, 05i→instructions-writer loop, 05f/05g→code-review-graph MCP tools, everything→`propagate_master_assets.py`. Each of these is a seam worth an explicit acceptance criterion in its feature plan.
- **Fixture strategy**: build the development fixture by copying this repo's own `docs/phases/PHASE_01/` and `PHASE_02/` artifact sets into the subphase layout the orchestrator expects — they are real, complete, and include a genuine NO-GO security rollup case. Do not point the orchestrator at the live phase directories; they are sibling top-level phases, not subphases.
- **Acceptance-criteria material**: the ledger-absent baseline fallback belongs to the orchestrator feature's ACs; partial-failure completion and the no-GO-with-missing-checks rule belong to the conventions skill and 05l features; automatic roadmap/summary status updates and the full-re-run policy belong to the orchestrator feature.
