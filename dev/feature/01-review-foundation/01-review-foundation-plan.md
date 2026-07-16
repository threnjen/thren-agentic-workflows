# Feature Plan: 01-review-foundation

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** no
- **Depends on:** none
- **Key files modified:** `.github/skills/phase-final-review-conventions/SKILL.md` (new), `.github/skills/phase-final-review-report/SKILL.md` (new), `.github/skills/worktree-baseline/SKILL.md` (new), `.github/agents/05a-baseline-worktree.agent.md` (new), `.github/agents/README.md` (agent inventory update), `dev/phase-final-review/fixtures/` fixture tree `[PROPOSED - layout TBD]` (new), propagated outputs under `.claude/skills/`, `.claude/agents/` and Codex/OpenCode equivalents (generated), `scripts/propagate_master_assets.py` (verify — auto-discovery via glob at lines 260/1204 means no change expected)
- **Sequential reason:** every feature in this phase regenerates shared propagated output files; phase runs strictly sequentially

## A. Requirements & Traceability

Source: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`, Deliverable 1.

Acceptance criteria:

- **AC1**: Skill `phase-final-review-conventions` exists in `.github/skills/phase-final-review-conventions/` and declares, at minimum: report locations/naming under `dev/phase-final-review/PHASE_0N/`, severity levels, the ≤10-line return-summary contract, read-only worktree etiquette, model-tier notes, and the partial-failure semantics (run completes when an evaluator fails; readiness report must enumerate not-run checks; verdict may not be GO while any check is missing). Mirrors the structure of `.github/skills/auditor-conventions/SKILL.md`.
- **AC2**: Skill `phase-final-review-report` exists and provides output templates for: master QA doc, security rollup (fixed/persisting/reintroduced classification), AC-regression matrix, and the go/no-go readiness report (severity-ordered blocking list, not-run checks section). Mirrors `implementation-record`-style template skills.
- **AC3**: Skill `worktree-baseline` exists and defines the reusable "check out commit X in a git worktree, return the path" procedure, including cleanup expectations and read-only etiquette. Written to be reusable outside Phase Final Review (e.g., by eval-grader).
- **AC4**: Agent `05a-baseline-worktree.agent.md` exists in `.github/agents/`, follows the numbered/lettered house style of `04a-feature-plan-expander.agent.md` and siblings, loads the `worktree-baseline` skill, and returns only the worktree path plus a ≤10-line summary.
- **AC5**: A development fixture exists containing copies of the real Phase 01/02 pipeline artifacts (from `docs/phases/PHASE_01/` and `docs/phases/PHASE_02/`: summaries, QA docs, QA coverage maps, qa-analysis files, security scans) arranged in the subphase layout the orchestrator expects (two pseudo-subphase directories under one synthetic phase). Fixture root: `dev/phase-final-review/fixtures/` `[PROPOSED - exact path TBD]`. The fixture must include Phase 02's genuine NO-GO security case.
- **AC6**: Running `scripts/propagate_master_assets.py` picks up all three skills and the 05a agent into Claude, OpenCode, and Codex outputs with no diff noise in unrelated assets, and `tests/test_propagate_master_assets.py` passes.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1 | `.github/skills/phase-final-review-conventions/SKILL.md` | Code-review evidence only (markdown asset); propagation suite for wiring |
| AC2 | `.github/skills/phase-final-review-report/SKILL.md` | Code-review evidence only; propagation suite for wiring |
| AC3 | `.github/skills/worktree-baseline/SKILL.md` | Code-review evidence + manual QA (execute the documented worktree procedure once against this repo) |
| AC4 | `.github/agents/05a-baseline-worktree.agent.md` | Code-review evidence + manual QA (spawn agent, verify worktree path return) |
| AC5 | `dev/phase-final-review/fixtures/` | Manual QA check (fixture inventory vs. Phase 01/02 source artifacts) |
| AC6 | `scripts/propagate_master_assets.py` outputs | Existing automated test: `tests/test_propagate_master_assets.py` |

Non-goals:

- No orchestrator or evaluator agents beyond `05a` (features 02–06).
- No "combine sibling phases" mode — the fixture is the only mechanism for exercising Phase 01/02 material (explicit phase-level out-of-scope).
- No changes to `prod-code-review`, `auditor-conventions`, or any existing skill.
- No modification of the live `docs/phases/PHASE_01/`/`PHASE_02/` directories — fixture files are copies.

## B. Correctness & Edge Cases

- Worktree procedure must handle: baseline commit not present locally (fail with clear message), pre-existing worktree at the target path (reuse or recreate deterministically — decide in skill, document), and cleanup on completion.
- Fixture must be committable: `.gitignore` line 5 (`dev/*`) ignores all `dev/` content — prior `dev/feature/` manifests are tracked only via force-add. The implementer must either add a gitignore negation for the fixture path or force-add fixture files, and record the choice in implementation notes.
- Conventions skill must define what a "missing artifact" is precisely enough for preflight (feature 02) to fail loudly on it.
- Report templates must include an explicit "checks not run" section so partial-failure semantics have a place to land (consumed by features 02 and 06).

## C. Consistency & Architecture Fit

- Follow existing skill directory convention: one directory per skill containing `SKILL.md` (see `.github/skills/auditor-conventions/`).
- Follow agent frontmatter/house style from `04a-feature-plan-expander.agent.md` and `.github/agents/README.md`.
- Cross-feature API contracts this feature must publish (named here because downstream plans depend on them):
  - Report file locations/naming scheme in the conventions skill (consumed by all evaluator features and 06).
  - The four report templates in `phase-final-review-report` (consumed by features 03–06).
  - The worktree-checkout contract in `worktree-baseline` (consumed by features 02 and 05).
  - The fixture layout (consumed by every feature's dry-run acceptance).

## D. Clean Design & Maintainability

- Simplest design: three small skills + one thin agent + a copied-file fixture. No scripts, no code.
- Duplication risk: conventions skill overlapping `auditor-conventions` — keep phase-final-review-specific rules only; reference rather than restate shared audit norms.
- Keep-it-clean checklist: no change-tracking language in skills; templates use placeholder tokens consistent with existing template skills; fixture README explains provenance (copied from Phase 01/02, safe to regenerate).

## E. Completeness: Observability, Security, Operability

- Observability: none — markdown assets. No new logging anywhere. Correct operability decision per phase constraints.
- Security: fixture copies include the Phase 02 security scan content; it is already committed in `docs/phases/`, so no new exposure.
- Runbook: deploy = run propagation; verify = propagation test suite + fixture inventory; rollback = git revert of the feature commit.

## F. Test Plan

- Must-have automated tests: `tests/test_propagate_master_assets.py` passes after propagation (existing suite; no new automated tests — assets are markdown).
- Existing tests to update: none expected (propagation auto-discovers new assets); `(verify)` during implementation.
- Code-review evidence only: AC1, AC2 template completeness.
- Manual QA checks:
  1. Given the three skills exist, when propagation runs, then all three appear in `.claude/skills/` and Codex/OpenCode outputs with `$source` tags and no unrelated diffs.
  2. Given a known commit SHA, when the `worktree-baseline` procedure is followed, then a read-only worktree exists at the returned path and can be removed cleanly.
  3. Given the fixture tree, when compared against `docs/phases/PHASE_01/` and `PHASE_02/`, then every source artifact type (summary, QA, coverage map, qa-analysis, security scan) is present in pseudo-subphase layout, including the NO-GO verdict content.
  4. Given `05a-baseline-worktree` is spawned with a SHA, when it completes, then its return is the worktree path plus ≤10 lines.

## Stage 0: Test Prerequisites

Not required — this feature ships markdown assets and a fixture; the propagation test suite already exists and passes. Coverage-percentage gating does not apply to non-code assets.

## Stage 1: Skills

**Goal**: Author the three skills (AC1–AC3).
**Success Criteria**: All three SKILL.md files exist, complete against their ACs, and match house style.
**Status**: Not Started

## Stage 2: Baseline Agent

**Goal**: Author `05a-baseline-worktree.agent.md` (AC4).
**Success Criteria**: Agent file exists, loads `worktree-baseline`, honors the ≤10-line return contract.
**Status**: Not Started

## Stage 3: Development Fixture

**Goal**: Assemble the Phase 01/02-derived fixture in subphase layout (AC5).
**Success Criteria**: Fixture inventory manual QA check passes; fixture README documents provenance.
**Status**: Not Started

## Stage 4: Propagation

**Goal**: Propagate and verify (AC6).
**Success Criteria**: Propagation test suite passes; new assets present in all three harness outputs.
**Status**: Not Started

## Relationships to Sibling Plans

- All later features (02–06) are authored against the contracts this feature publishes; it must land first.
- The fixture is the dry-run substrate for every later feature's acceptance checks.

## Unverified Assumptions

- Propagation requires no script changes for new skills/agents (auto-discovery observed at `scripts/propagate_master_assets.py` lines 260 and 1204); if a naming edge case surfaces, the fix is scoped to discovery config, not new pipeline stages.
- `dev/phase-final-review/fixtures/` remains the fixture location despite `dev/*` being gitignored; committing requires a negation rule or force-add (see Section B). If that proves unworkable, relocate and record in implementation notes.
