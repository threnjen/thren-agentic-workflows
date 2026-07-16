# 05 Mechanical Evaluators — Tasks

Baseline: 416 passed, 15 subtests passed (2026-07-16). Runner: `.venv/bin/python -m pytest tests/ -q`.

## Stage 0: Test Prerequisites

**Status:** Not required — baseline green across 4 consecutive full runs.

- [ ] Confirm the baseline still reproduces before starting: `.venv/bin/python -m pytest tests/ -q`
- [ ] Confirm feature `02-retired-evaluator-removal` has landed and the `05c`/`05d`/`05e` slugs are free (`ls .github/agents/05*`) — this is an undeclared hard prerequisite for Stage 1

## Stage 1: Rename and Renumber

**Goal:** `git mv` all three; update `name:` and body self-references; propagate; confirm OpenCode orphans pruned.
**Success Criteria:** AC1, AC9.

- [ ] `git mv .github/agents/05g-artifact-sweeper.agent.md .github/agents/05c-artifact-sweeper.agent.md` (AC1)
- [ ] `git mv .github/agents/05j-consistency-auditor.agent.md .github/agents/05d-consistency-auditor.agent.md` (AC1)
- [ ] `git mv .github/agents/05k-dependency-auditor.agent.md .github/agents/05e-dependency-auditor.agent.md` (AC1)
- [ ] Update `name:` frontmatter in each: `05g Artifact Sweeper` → `05c Artifact Sweeper`, `05j Consistency Auditor` → `05d Consistency Auditor`, `05k Dependency Auditor` → `05e Dependency Auditor` (AC1)
- [ ] Update every in-body self-reference to the old slug/display name — including the `You are the **05g Artifact Sweeper**` opening line and the `Write only dev/phase-final-review/PHASE_0N/05g-artifact-sweeper-report.md` line in each Shared Contracts block (AC1)
- [ ] Grep the whole repo for residual `05g-artifact-sweeper`, `05j-consistency-auditor`, `05k-dependency-auditor`, and their display-name forms; update `.github/agents/README.md` roster rows (AC1)
- [ ] Run the propagator and regenerate all three roots in the same commit as the body edits — `test_phase_review_agents_match_all_generated_harness_outputs` compares rendered output byte-for-byte and will fail otherwise (AC9)
- [ ] Verify Claude outputs survived under the existing stems `z-artifact-sweeper.md`, `z-consistency-auditor.md`, `z-dependency-auditor.md` (`_claude_filename_for` prefers an existing stem) (AC9)
- [ ] Verify `opencode/agents/05g-*.md`, `05j-*.md`, `05k-*.md` are absent and `05c-*`, `05d-*`, `05e-*` are present — OpenCode keys on slug and will orphan (AC9)
- [ ] Verify `codex/agents/z-artifact-sweeper.toml`, `z-consistency-auditor.toml`, `z-dependency-auditor.toml` regenerated (AC9)

## Stage 2: Audit the Grants

**Goal:** Determine per agent whether `execute` is genuinely required. Drop where not; justify by named command where so.
**Success Criteria:** AC3, AC4; each retained grant has a recorded justification.

- [ ] Drop `execute` from `05c-artifact-sweeper` → `tools: [read, search, edit]`. Verified during expansion: the body invokes no shell command; its only external call is the code-review-graph `refactor_tool` MCP invocation (AC3)
- [ ] Drop `execute` from `05d-consistency-auditor` → `tools: [read, search, edit]`. Verified during expansion: the body references zero commands (AC3)
- [ ] For `05e-dependency-auditor`, either drop `execute` or retain it with a justification **naming the specific offline read-only audit command** that has no non-shell equivalent. "It might be handy" is not a justification (AC3, AC4)
- [ ] If `execute` is retained on `05e`, record the named command in the implementation notes and confirm the body's existing offline contract still states that network-capable commands are unavailable (`05k` body lines 34–42 already encode this) (AC4)
- [ ] **Retain `edit` on all three** — each agent writes its own report file. Do not strip it while reading the "read-only, never remediate" body language (AC5)
- [ ] Confirm no agent gains a broader grant as a side effect; per `cross-phase-decisions.md:86`, never restore unrestricted shell to satisfy an AC
- [ ] Add per-agent tool expectations to `tests/test_propagate_master_assets.py` pinning each of the three to its exact expected `tools` list, so a future grant change becomes a deliberate test edit rather than a silent widening (AC3, AC4)

## Stage 3: Rescope to the Branch Diff

**Goal:** Replace phase/subphase inputs with `<merge-base>..HEAD`; require added-line attribution; retarget report paths.
**Success Criteria:** AC2, AC5, AC6, AC7.

- [ ] Rescope `05c-artifact-sweeper` from "the current phase diff" to the branch diff `<merge-base>..HEAD`, receiving the confirmed base from the orchestrator (AC2)
- [ ] Rescope `05d-consistency-auditor` from "across the assigned phase subphases" to the branch diff; remove the supplied-subphase-artifacts comparison input (AC2)
- [ ] Rescope `05e-dependency-auditor` from "the current phase diff" to the branch diff, comparing manifests/lock files against the confirmed base (AC2)
- [ ] Remove all subphase language and every `PHASE_0N` report-root reference from all three bodies (AC2)
- [ ] Retarget each report to `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/<slug>-report.md`; reference feature `03`'s conventions skill rather than restating the path format (AC5)
- [ ] Confirm each agent returns ≤10 lines (AC5)
- [ ] Add an explicit added-line attribution requirement to each body: findings must be attributable to lines the branch **added**; touched-file filtering alone is insufficient (AC6)
- [ ] Confirm each body preserves the cheap-tier-is-authoritative language and records a tier limitation as an execution condition, never as evidence a check passed (AC7)
- [ ] Confirm `05c`/`05d` graph-unavailable handling still reports not-run with a stated reason and drops the verdict ceiling — never a silent grep fallback (AC7)
- [ ] Confirm empty-diff handling says so explicitly rather than reporting "no findings" (AC7)
- [ ] Add contract assertions for the three bodies `[PROPOSED - name TBD]`: added-line attribution declared and touched-file filtering rejected (AC6); no subphase or `PHASE_0N` mentions (AC2); report path present (AC5)
- [ ] Regenerate all three roots after the body edits

## Stage 4: Close the Enumeration Gap

**Goal:** Re-derive `expected_slugs` over the settled roster so no agent can be omitted; dry-run all three.
**Success Criteria:** AC8; suite green; three reports produced.

- [ ] Re-derive `expected_slugs` in `PropagateMasterAssetsTests.test_phase_review_agents_match_all_generated_harness_outputs` (line ~89) over the settled seven: `05a-baseline-worktree`, `05b-change-narrator`, `05c-artifact-sweeper`, `05d-consistency-auditor`, `05e-dependency-auditor`, `05f-test-health`, `05g-readiness-synthesizer` (AC8)
- [ ] **Resolve the `05a` question before writing the tuple** — `05a-baseline-worktree` holds `execute` and is currently omitted from the tuple alongside the three. Its grant is recorded as unclosable (`cross-phase-decisions.md:16`). Either admit it with a per-agent expectation and a recorded justification, or escalate to the Decomposer. **Do not omit it to keep the tuple clean — that is the exact gap AC8 exists to close** (AC8)
- [ ] Replace the blanket `self.assertNotIn("execute", agent.tools)` (line ~116) with per-agent expected tool lists. Do **not** delete the assertion and do **not** drop an agent from the tuple to dodge it (AC8)
- [ ] Remove the `if slug == "05d-security-rollup":` conditional if feature `02` has not already; do not re-add it under the new `05d-consistency-auditor` slug (AC8)
- [ ] Write the tuple so that omitting an agent **fails** rather than silently narrowing coverage — the enumeration gap arose from omission being free (AC8)
- [ ] Coordinate with feature `06-narrative-and-test-health` on `expected_slugs`; whichever lands second rebases onto the other's tuple rather than re-deriving independently
- [ ] Assert `opencode/agents/05g-*`, `05j-*`, `05k-*` are absent after propagation `[PROPOSED - name TBD]` (AC9)
- [ ] Run the full suite: `.venv/bin/python -m pytest tests/ -q` — expect ≥416 passed, no regressions
- [ ] **Manual QA:** dry-run all three against the pinned fixture; confirm three findings reports with added-line attribution
- [ ] **Manual QA:** confirm graph-unavailable degradation reports not-run rather than a clean result
- [ ] Record in implementation notes: each retained `execute` grant with its named command, and the `05a` resolution
