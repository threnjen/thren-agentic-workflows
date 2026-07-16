# 02 Retired Evaluator Removal — Context

## Key Files

### Files being changed

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/05c-qa-consolidator.agent.md` | Retired evaluator (merges subphase QA docs) | Delete |
| `.github/agents/05d-security-rollup.agent.md` | Retired evaluator (union of subphase findings); declares `agents: [Security Scan]` | Delete |
| `.github/agents/05e-ac-regression.agent.md` | Retired evaluator (re-verifies subphase ACs) | Delete |
| `.github/agents/05f-seam-analyzer.agent.md` | Retired evaluator (seams between subphases) | Delete |
| `.github/agents/05i-learnings-harvester.agent.md` | Retired evaluator (mines pipeline review records) | Delete |
| `.github/agents/05-phase-final-review.agent.md` | **Orchestrator. Line 5 `agents:` frontmatter names all five retired agents; 3 further body mentions.** Not listed in the plan's Execution Metadata — see Discovery Delta D1 | Modify |
| `.github/agents/README.md` | Agent roster. Table rows 164–167 (`05c`–`05f`), 171 (`05i`); row 169 `Security Scan` declares parent `05d Security Rollup`; **prose line 243 repeats the same parent claim** | Modify |
| `tests/test_propagate_master_assets.py` | `expected_slugs` tuple at :87 (8 slugs, 5 retired); `05d-security-rollup` conditional at :119–121 | Modify |
| `tests/test_readiness_synthesis_agents.py` | 6 tests; `LEARNINGS_AGENT` const at :6; 3 tests wholly about `05i`; 1 shared-contract test to narrow | Modify |
| `claude/agents/`, `opencode/agents/`, `codex/agents/` | Generated outputs — **must self-clean via feature `01`; never hand-delete** | Regenerated (not hand-edited) |
| New reference-sweep test `[PROPOSED - name TBD]` | Repository-wide sweep for retired slugs and display names (AC6) | Create |

### Read-only reference files

| File | Why it matters |
|------|----------------|
| `.github/agents/04e-diff-security-scan.agent.md` | **Verified 2026-07-16: exists; `tools: [read, search, edit]` — holds no `execute`; `user-invocable: false`.** Stage 1's gate is satisfiable |
| `.github/agents/security-scan.agent.md` | **Verified: exists.** Survives retirement; must not be deleted as collateral |
| `.github/skills/phase-final-review-conventions/SKILL.md` | Lines 33–36, 39 name retired report filenames. Owned by feature `03` — see Discovery Delta D2 |
| `.github/learnings/cross-phase-decisions.md` | Historical record; retains retired names (AC6 exception) |
| `claude/learnings/cross-phase-decisions.md` | **Propagated copy of the above — also contains retired names.** Sweep trap; see Discovery Delta D3 |
| `docs/phases/**` | Historical records; retain retired names (AC6 exception) |
| `scripts/propagate_master_assets.py` | `_build_agent_reference_map` / `_rewrite_agent_references` rewrite by display name, sorted longest-first |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| **D1 — `.github/agents/05-phase-final-review.agent.md` is a required modification the plan never names.** Line 5 frontmatter: `agents: [Baseline Worktree, 05b Change Narrator, 05c QA Consolidator, 05d Security Rollup, 05e AC Regression, 05f Seam Analyzer, 05g Artifact Sweeper, 05h Test Health, 05i Learnings Harvester, 05j Consistency Auditor, 05k Dependency Auditor, 05l Readiness Synthesizer]` — all five retired agents present. 3 more mentions in the body. The file is absent from Execution Metadata "Key files modified", from the AC5 traceability row, and from every stage. The plan's own test case 5 ("no agent's `agents:` frontmatter list names a deleted agent") targets exactly this file but no stage does the edit. | **Warning — plan gap.** AC6's repo-wide sweep would catch it at the end, but as a late failure with no owning stage. It is also the *mirror image* of the `Security Scan` trap the plan calls "the trap": `05d` orphans its child's parent claim, and `05` orphans its own children's entries. | **Update plan** — add `05-phase-final-review.agent.md` to Execution Metadata and to AC5/AC6; task added under Stage 4 |
| **D2 — AC6 as written fails against `.github/skills/phase-final-review-conventions/SKILL.md`.** Lines 33–36 and 39 name `05c-qa-consolidator-report.md`, `05d-security-rollup-report.md`, `05e-ac-regression-report.md`, `05f-seam-analyzer-report.md`, `05i-learnings-harvester-report.md`. AC6 allows only `cross-phase-decisions.md` and `docs/phases/**` as exceptions. But the plan's non-goals defer skill renames to `03-pr-review-conventions-skills`. AC6 and the non-goals contradict each other on this file. | **Warning — AC conflict.** Either (a) this feature prunes the retired report rows from the skill's directory tree (a deletion, not a rename — arguably in scope), or (b) AC6 adds a scoped, time-boxed exception that `03` removes. Silently leaving it makes the sweep test unwritable as specified. | **Update plan** — resolve before Stage 4; recommend (a), since removing rows for deleted agents is deletion work, not the rename `03` owns |
| **D3 — The sweep must exclude propagated learnings copies, not just `.github/learnings/`.** `claude/learnings/cross-phase-decisions.md` exists and carries the retired names (propagated from the source). AC6 names `.github/learnings/cross-phase-decisions.md` as the exception; test-plan case 3 says `.github/learnings/`. Neither covers `claude/learnings/`. | Sweep fails on a file that is correct and generated. | **Add task** — exclusion list must cover source *and* propagated learnings; verify `opencode/`, `codex/` learnings roots at implementation time |
| **D4 — AC6 vs. test-plan case 3 disagree on the exception set.** AC6: `cross-phase-decisions.md` + `docs/phases/**`. Case 3: `docs/phases/**` + `.github/learnings/` (whole dir). | Minor, but the sweep's exclusion constant is the single source of truth and cannot be both. | **Update plan** — pick one; recommend directory-scoped (`.github/learnings/`, `*/learnings/`, `docs/phases/**`) |
| **D5 — README prose line 243 is a second parent claim, outside AC5's enumerated rows.** `**Security Scan** *(subagent of 05d Security Rollup)*`. AC5 names only table rows 164–167, 169, 171. Line 243 appears in the plan only under "Unverified Assumptions". | AC6 catches it, but AC5 reads as complete and is not. | **Add task** — Stage 4 covers both row 169 and prose 243 with the same re-parenting decision |
| **D6 — All enumerated plan line numbers verified exact.** README 164–167, 169, 171; `tests/test_propagate_master_assets.py:87` `expected_slugs`; the `05d` conditional at :119–121; the three `05i` test names and the shared `test_both_agents_honor_shared_return_contract_and_readiness_tier` at :94. | Plan's factual claims are accurate. | None |
| **D7 — Stage 1's gate is pre-satisfied.** `04e-diff-security-scan.agent.md` exists, is diff-shaped, `tools: [read, search, edit]` — no `execute`. | Stage 1 is a recording exercise, not an open risk. Still record it: the plan requires the check be evidenced. | None — record the finding |
| **D8 — `expected_slugs` failure mode is harder than the plan implies.** Line 116 does `agent = agents[slug]` inside `with self.subTest(slug=slug)`. A retired slug left in the tuple raises `KeyError`, not a soft assertion failure. | Good news: the plan's failure mode "`expected_slugs` updated but the `05d` conditional left in place" cannot ship silently. | None |
| **D9 — Precise AC7 count delta is predictable in advance.** `tests/test_readiness_synthesis_agents.py`: 6 tests → 3 (−3). `tests/test_propagate_master_assets.py`: test count unchanged (1), but subtests 8 → 3 slugs (−5 subtests; baseline records 15 subtests → expect 10). Net before new tests: **416 → 413 passed, 15 → 10 subtests.** New tests add back. | AC7 asks for the delta to be *explained*. It can be predicted, which is stronger. | **Add task** — state the predicted delta before running, then reconcile |
| **D10 — `05a` is named `Baseline Worktree`, not `05a Baseline Worktree`.** Visible in the orchestrator's `agents:` list. | No impact on this feature; relevant when editing that list not to "fix" the odd one out. | None — do not normalize |

## Architectural Decisions

- **Delete first, reconcile last.** The Phase sequences retirement as Deliverable 7 because it is "the integration point where dangling references surface." That rationale governs *reconciliation* (`08-retirement-reconciliation`), not *deletion*. Deleting now removes five agents from the blast radius of features `03`–`07`, each of which would otherwise rename skills across files slated for deletion.
- **Never hand-delete generated files.** If `01-propagator-orphan-pruning` fails to remove the outputs from `claude/`, `opencode/`, `codex/`, that is a bug in `01` — not a cue to `git rm`. Hand-deleting masks the defect and it returns on the next rename. AC2 states this explicitly.
- **`Security Scan` survives; its parent claim is corrected, not its existence.** `05d` declared `agents: [Security Scan]`. Deleting `05d` orphans that claim. `Security Scan` is general-purpose and separately referenced; the Phase delegates diff-scoped security to `04e-diff-security-scan`, a *different* agent. Deleting `security-scan.agent.md` by association would remove working, referenced capability.
- **Retiring `05d` is a shape change, not a security-coverage regression.** The rollup aggregated per-subphase security reports — a shape with no PR analogue. The diff-scoped check it wrapped is delegated to `04e-diff-security-scan` (verified present, no `execute`). Stage 1 exists to record that check, because if `04` did not exist this deletion *would* be a regression.
- **The reference sweep is what converts "I looked" into "the suite checks."** This feature only removes; the risk is *incomplete* removal — one table row, one prose name. The sweep must match display names (`05c QA Consolidator`) as well as slugs, because `_rewrite_agent_references` matches on display name.
- **The retired-name list is defined once**, as a module constant in the sweep test — not duplicated across tests.

## Constraints

- **Hard dependency on `01-propagator-orphan-pruning`.** AC2 is unachievable without it. `01` must land first.
- **Shares `tests/test_propagate_master_assets.py` with `01`.** Not parallel-safe; wave 2.
- Test runner is `.venv/bin/python -m pytest tests/ -q`. System `python3` has no pytest.
- A deleted source agent drops out of `_build_agent_reference_map`, so surviving prose saying "05d Security Rollup" stops being rewritten and **silently ships as literal text**. The propagator will not catch this; only the sweep will.
- `docs/phases/**` and the learnings files are historical records and **must retain** retired names.
- Learnings — *Review Contracts*: "Never restore unrestricted shell/Bash permissions to satisfy an evaluator acceptance criterion. This bound `05i`'s history mining, which is retired; the rule outlives it."

## Scope Boundaries

- **Do not rename or renumber any surviving agent.** The seven survivors renumber contiguously to `05a`–`05g` in features `03`–`07`. Not here.
- **Do not rescope any surviving agent's content.**
- **Do not delete `security-scan.agent.md` or the `Security Scan` agent.**
- **Do not hand-delete anything under `claude/`, `opencode/`, or `codex/`.**
- **Do not touch `dev/phase-final-review/`.** Verified 2026-07-16: the directory does not exist. The Phase instructs retiring `dev/phase-final-review/fixtures/PHASE_05/` and `dev/phase-final-review/PHASE_05/`; both are already absent. The `cross-phase-decisions.md` note that fixtures "keep legacy phase identifiers" describes files not on disk. Nothing to do.
- **Do not update `docs/`, root `README.md`, or `docs/CODEBASE_CONTEXT.md`** — deferred to `08-retirement-reconciliation`. (Note: `.github/agents/README.md` **is** in scope; the root `README.md` is not.)
- **Do not rename the `phase-final-review-*` skills** — that is `03-pr-review-conventions-skills`. See Discovery Delta D2 for the one place this boundary is contested.
- **Do not normalize `Baseline Worktree` to `05a Baseline Worktree`** while editing the orchestrator's `agents:` list.

## Relationships to Sibling Plans

- **Depends on `01-propagator-orphan-pruning`** — hard runtime dependency. AC2 cannot pass without it. Also shares `tests/test_propagate_master_assets.py`, so the two cannot run in parallel.
- **Shrinks the blast radius of `03`–`07`.** Every downstream feature that renames a skill or renumbers an agent touches fewer files once these five are gone.
- **`03-pr-review-conventions-skills`** renames the `phase-final-review-conventions` / `phase-final-review-report` skills. Discovery Delta D2 is the seam between that feature and this one.
- **`08-retirement-reconciliation`** owns the documentation half of the Phase's Deliverable 7 and remains last.

## Suggested Implementation Order

Wave 2, after `01-propagator-orphan-pruning` completes. Sequential — not parallel-safe with `01`.

Within the feature: Stage 1 (confirm security delegation) → Stage 2 (delete + propagate) → Stage 3 (reconcile tests) → Stage 4 (README, orchestrator, sweep).

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3 stdlib (propagator); pytest for tests; agents are Markdown with YAML frontmatter in `.github/agents/` |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` — system `python3` has no pytest |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

**PR-Review Rescope (Phase 03; resolved 2026-07-16)** — the decision this feature executes:

> The evaluator roster splits roughly in half [...] **Five are phase-shaped and are retired**: `05c-qa-consolidator` (merges *subphase* QA docs), `05d-security-rollup` (union of *subphase* findings), `05e-ac-regression` (re-verifies *every subphase's* ACs), `05f-seam-analyzer` (seams *between subphases*), `05i-learnings-harvester` (mines *pipeline review records*). A PR has no subphases and no ACs. Little working code is lost — the whole-phase flow has never successfully run against a real phase.

> **The five phase-shaped evaluators are deleted** from source and from all three generated roots; **the seven survivors renumber contiguously to `05a`–`05g`** [...] **Security is delegated to the existing `04e-diff-security-scan`**, which is already diff-shaped and already holds no `execute` — no new security agent is authored.

> Removing the multi-subphase premise deleted work rather than moving it, and that is the shape to expect from a good rescope. [...] **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.**

**Review Contracts** — scope-independent, and one names `05i` directly:

> **Never restore unrestricted shell/Bash permissions to satisfy an evaluator acceptance criterion.** This bound `05i`'s history mining, which is retired; the rule outlives it and now governs the `gh` grant. The correct move is a narrowly scoped capability — an offline audit mode, a verifiable evidence bundle from the orchestrator, a command allowlist — never a broad grant with a comment explaining why it is fine.

> Missing or incomplete required checks are a hard readiness gate [...] In this project verdicts are issued by the user by hand; no agent writes a status line.

**Propagation Contracts:**

> The current master-asset propagator's generated roots are `claude/`, `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are not generated destinations. Future feature plans must name the actual roots or explicitly add an adapter.

**Phase Numbering** — relevant to not over-correcting while editing agent lists:

> **Agent numbers are pipeline positions, not phase numbers.** `05-phase-final-review` and its `05a`–`05l` evaluators follow `04-phase-execute` in the pipeline; they did not renumber with the phase and must not be "corrected" to match it.

**Release Verification** — governs AC7's "explain the delta, not merely observe it":

> "Remediated in code" is not "verified". [...] Status lines move only on fresh final-state evidence.
