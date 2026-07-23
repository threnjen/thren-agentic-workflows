# qa Plan: Phase 01 — Engagement Preparation & Baselines

**Date:** 2026-07-22
**Mode:** Release qa Plan
**Scope:** Pilot validation of the engagement preparation pipeline — the `engagement-configuration` skill (feature 10), the **06 Engagement - Prepare** orchestrator agent (features 11 + 12), and the `engagement-preparation-runbook` skill (feature 13). All deliverables are Markdown agent/skill assets; the only manual qa is the runtime pilot run those assets describe.
**Environment:** Local machine, from a Claude Code session in this repo's working directory with the `code-review-graph` MCP server attached (required for graph builds; if unattached, the run must record graph steps as NOT RUN with a reason — that is itself a checkable behavior, not a pass).
**Prerequisites:**

- **Pilot engagement repo local paths — currently TBD** (`docs/phases/DISCOVERY_CONTEXT.md` open item). Every checklist item below is blocked on this and is recorded **NOT RUN — deferred, owner: the user (threnjen)** per feature 13 AC6. These checks must never be reported as passed until executed.
- An engagement config file (advisory name `engagement.yaml` at the engagement root), authored per `source_of_truth/skills/engagement-configuration/SKILL.md` — declare each pair (`type: repo` with `original.path`/`upgraded.path`, or `type: branch` with `repo_path` and per-side `branch`), plus `sow_document` and `deliverables_spec` pointers.
- Follow `source_of_truth/skills/engagement-preparation-runbook/SKILL.md` Steps 1–5 as the run procedure; invoke the orchestrator as **06 Engagement - Prepare**, supplying the config path.
- Clean working trees in every engagement repo (`git status --porcelain` empty per repo) — the orchestrator fail-fasts on dirty trees by design.
- Before the first run, record baseline SHAs per engagement repo: `git -C <repo> rev-parse <main-or-original-branch>` — the runbook's verification section lists the exact commands.

## Features Covered

| Feature | Plan | Implementation Record | Review Record |
|---------|------|-----------------------|---------------|
| 10-engagement-configuration-schema | `dev/feature/10-engagement-configuration-schema/10-engagement-configuration-schema-plan.md` | `.../10-engagement-configuration-schema-implementation.md` | `.../10-engagement-configuration-schema-review.md` |
| 11-preparation-orchestrator | `dev/feature/11-preparation-orchestrator/11-preparation-orchestrator-plan.md` | `.../11-preparation-orchestrator-implementation.md` | `.../11-preparation-orchestrator-review.md` |
| 12-graph-baseline-capture | `dev/feature/12-graph-baseline-capture/12-graph-baseline-capture-plan.md` | `.../12-graph-baseline-capture-implementation.md` | `.../12-graph-baseline-capture-review.md` |
| 13-preparation-runbook | `dev/feature/13-preparation-runbook/13-preparation-runbook-plan.md` | `.../13-preparation-runbook-implementation.md` | `.../13-preparation-runbook-review.md` |

## Coverage Map

- Coverage Map: `docs/phases/PHASE_01/PHASE_01_qa_COVERAGE_MAP.md`

---

## Summary of Changes

Phase 01 built the engagement preparation toolchain as agent/skill definitions:

- **Feature 10** — `engagement-configuration` skill: config schema (unbounded comparison pairs, repo or branch type, `original`/`upgraded` roles), canonical field vocabulary, 11 validation rules with specific named error templates, fail-fast-before-work semantics, config location convention.
- **Feature 11** — `06-engagement-prepare.agent.md` orchestrator: config gathering (user-supplied path or interactive path collection)/validation, user confirmation gate, per-side prepare loop (docs → graph → record) with an unconditional docs-writer pass on every run, role-scoped docs sets, analysis-branch convention with three invariants (no source modified, byte-identical original/main history, analysis branch never pushed), delegation hard rule, fail-fast on unresolvables only, idempotent re-run.
- **Feature 12** — filled the agent's Step 2/2a integration points: unconditional incremental graph build (`build_or_update_graph_tool`, Tree-sitter, no quality gate) and the internal baseline snapshot (SHA-pinned, internal-only labeled, stored on the analysis branch, `list_graph_stats_tool` stats).
- **Feature 13** — `engagement-preparation-runbook` skill (declare → record SHAs → invoke → verify → re-run/failure table), catalog/count reconciliation (agents README, CODEBASE_CONTEXT, marker-guard test constants), and the pilot validation stage — deferred NOT RUN.

Open `[PROPOSED - TBD]` markers (analysis-branch name `engagement-analysis`, snapshot filename `engagement-baseline-snapshot.md`) are resolved by this pilot run; record final names when executing.

## Automated Test Coverage

Do not manually re-verify any of the following — already proven:

- Propagation integrity, marker guards, count-derivation guards: `uv run pytest tests/` — **233 passed, 113 subtests passed, 0 failed** (fully green as of feature 13; both pre-existing baseline failures resolved/reconciled). Propagation is at a fixed point (`changed_passes: 0`).
- All static content ACs (schema fields, validation-rule text, loop ordering prose, tool-name usage, no pilot-fact leakage, catalog/count accuracy) were verified by per-feature code review — see the coverage map. No manual re-reading of the assets is needed.

There are **no new unit/integration tests** in this phase (deliverables are Markdown); no test files were added, and the only test-file change was count-constant reconciliation in `tests/test_propagate_master_assets.py` (feature 13, reviewed).

---

## Manual qa Checklist

All items in this section: **STATUS: NOT RUN — deferred, owner: the user (threnjen)** (pilot repo paths TBD; feature 13 AC6). Never mark passed until actually executed.

Single integration surface: the entire checklist is one end-to-end pilot engagement run plus targeted variants — Phase 01 has no UI or external service beyond the local orchestrator + code-review-graph MCP.

### Pilot Engagement Preparation Run (end-to-end)

**Features:** 10, 11, 12, 13
**Covers ACs:** 11/AC3, 11/AC5, 11/AC6, 11/AC7, 12/AC1, 12/AC6, 13/AC1, 13/AC5(a)
**Why manual:** Runtime delegation, branch manipulation, and MCP graph behavior cannot be observed in static review; this is the phase's only runtime evidence (integration-feature rule).

#### Happy Path — Check 1: unprepared engagement fully prepared

- [ ] **Record pre-run SHAs** — For each engagement repo run `git -C <repo> rev-parse <original-or-main-branch>` and save the output (runbook Step 2). **Expected:** One SHA per branch recorded before any orchestrator activity.
- [ ] **Invoke the orchestrator on the unprepared engagement** — In a Claude Code session, invoke **06 Engagement - Prepare** — supply the config path, or answer its questions and let it write the config. **Expected:** The config validates, then a confirmation gate displays every pair/side and waits for your confirmation before any analysis branch is created.
- [ ] **Confirm and let the run complete** — Approve the gate. **Expected:** The run completes with no further user intervention; the final report covers every side of every pair with status + pointers (no full analysis text inlined — compact per-side results only, per the delegation hard rule).
- [ ] **Verify role-scoped docs per side** — On each side's analysis branch (`git -C <repo> log engagement-analysis --stat` or checkout), inspect the generated docs. **Expected:** `upgraded` sides carry the full docs-writer set; `original` sides carry at minimum README/ARCHITECTURE/CODEBASE_CONTEXT, marked as internal analysis artifacts.
- [ ] **Verify a graph exists per side** — Ask the session to call `list_repos_tool` on the code-review-graph server. **Expected:** Each side's directory/revision appears as a built graph; the final report records graph stats per side (or an explicit NOT RUN with reason if the server was unavailable — never a silent fallback).
- [ ] **Verify per-side pointers resolve** — Follow each pointer in the final report (docs locations, snapshot path). **Expected:** Every pointer resolves to a real file on the side's analysis branch.
- [ ] **Resolve [PROPOSED] names** — Note the actual analysis-branch name and snapshot filename used. **Expected:** They match (or a deliberate deviation is recorded from) `engagement-analysis` and `engagement-baseline-snapshot.md`; record the final names back into the feature 13 implementation record.

#### Check 2: idempotent re-run

**Covers ACs:** 11/AC4, 11/AC9, 12/AC1, 13/AC5(b)

- [ ] **Re-run the orchestrator unchanged** — Immediately re-invoke **06 Engagement - Prepare** with the same config, no repo changes. **Expected:** Docs are regenerated on every side (docs-writer always runs — no staleness skip), the incremental graph build runs on every side, snapshots re-emit at the same SHAs, and the run reuses the pre-existing analysis branches without error.

#### Check 3 (Error Handling): deliberately bad config path

**Covers ACs:** 10/AC5, 11/AC2, 11/AC8, 13/AC5(c)

- [ ] **Break one path and run** — Copy the config, change one pair's `path` (or `repo_path`) to a nonexistent directory, invoke the orchestrator with the broken config. **Expected:** A specific fail-fast error naming that pair and that field with what was expected (per the skill's Validation Rules table); the run halts before ANY preparation work — no analysis branch created or modified on any side, no docs-writer spawned, no graph build.
- [ ] **Confirm nothing was prepared** — Run `git -C <repo> branch --list` and `git -C <repo> status --porcelain` on every engagement repo after the failed run. **Expected:** No new branches, no working-tree changes attributable to the failed run.

#### Check 4: non-contamination invariants

**Covers ACs:** 11/AC6, 13/AC5(d), 13/AC5(e)

- [ ] **Compare branch tip SHAs** — After Checks 1–2, re-run `git -C <repo> rev-parse <original-or-main-branch>` per repo and diff against the pre-run record. **Expected:** Byte-identical SHAs for every original/main branch.
- [ ] **Verify no source modification** — Per repo, on the original branch: `git -C <repo> status --porcelain` and `git -C <repo> diff <recorded-SHA>`. **Expected:** Empty output — no source file modified.
- [ ] **Verify the analysis branch was never pushed** — Per repo: `git -C <repo> ls-remote --heads origin engagement-analysis` (substitute the actual branch name). **Expected:** No matching remote ref.

#### Check 5: baseline snapshot integrity

**Covers ACs:** 12/AC4, 12/AC5, 12/AC6, 13/AC5(a)

- [ ] **Open both sides' snapshots for each pair** — Read the snapshot file from each side's analysis branch. **Expected:** Identical record shape across the two sides of each pair (same field set: size/dependency snapshot, graph stats, languages, commit SHA + branch); every field group is SHA-pinned — a snapshot without a commit SHA is invalid.
- [ ] **Verify internal-only labeling** — Inspect each snapshot artifact. **Expected:** The artifact itself carries an internal-only / not-client-facing label, states client figures come from Phase 2/5 outputs, and contains no client-facing framing and no embedded source content.
- [ ] **Verify language coverage gaps are recorded, not gated** — Check the snapshot/report for graph coverage notes. **Expected:** Unparsed/unsupported languages appear as known limitations; no coverage threshold or quality-gate failure anywhere.

---

## Cross-Cutting Concerns

### Security / Confidentiality
- [ ] **Confirm no engagement content entered this repo** — After all checks, run `git -C /Users/jennywadkins/github_repos/github-agents-source-of-truth status --porcelain` and review any diff. **Expected:** No engagement repo content, SOW/deliverables-spec content, or pilot repo names committed to this repo or its generated outputs.

Performance and accessibility: not applicable — no UI, no service; the graph build is incremental by design and has no performance acceptance criterion in this phase.

---

## Notes

- **Blocking prerequisite:** all manual items are NOT RUN until the user supplies pilot repo local paths (`docs/phases/DISCOVERY_CONTEXT.md` open item). The phase success criterion "runbook validated by an actual run" remains explicitly open (feature 13 AC5/AC6); the deferral is tracked in `source_of_truth/learnings/cross-phase-decisions.md` Open Items.
- When executed, record results in `dev/feature/13-preparation-runbook/13-preparation-runbook-implementation.md` (Pilot Validation section) and resolve the `[PROPOSED]` name markers in `source_of_truth/agents/06-engagement-prepare.agent.md`.
- Any findings against features 10–12 during the pilot loop back as review items per feature 13's non-goals — do not hot-fix those assets outside the pipeline.
- Feature 12 review flagged uncommitted pre-existing modifications in `docs/phases/` at review time — orchestrator to attribute/commit; not a qa item.
- Deliberately excluded from manual qa: graph-tool-unavailable simulation (cannot be reliably staged; the NOT-RUN contract text is review-verified), docs-writer partial-failure resume (exercise opportunistically only if it occurs naturally during the pilot).
