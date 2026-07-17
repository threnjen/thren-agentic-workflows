# Feature Tasks: 09-hook-record-purge

Derived from `09-hook-record-purge-plan.md`. All work lands as a **single dedicated
docs commit** (AC6), separate from any code-deletion commits.

## Stage 1: Directory and decision-log purge (AC1, AC2)

- [ ] Grep `tests/` for `docs/hooks`, `PHASE_01`, `PHASE_02`, `PHASE_04` before deleting; confirm feature 08 removed `test_explicit_rtk_guidance_remains_available` from `tests/test_phase04_runtime_deployment.py` — if it still exists, escalate/resolve before the deletion (see context Discovery Delta)
- [ ] Delete `docs/phases/PHASE_01/`, `docs/phases/PHASE_02/`, `docs/phases/PHASE_04/`, and `docs/hooks/`; verify `docs/phases/PHASE_03/`, `PHASE_05/`, `PHASE_07/`, and `docs/inspiration/` are untouched
- [ ] In `.github/learnings/cross-phase-decisions.md`, delete pure-hook sections wholesale: "Hook Composition" (line 228), "Guard Friction and Command Prompting" (233), "File-Access Guard Retirement" (248), plus hook-only entries within "Deferred Pipeline Work"
- [ ] Line-level scrub the mixed sections — "Deferred Pipeline Work" (line 22), "Propagation Contracts" (293), "Phase 04 Runtime Deployment Contract" (368): remove only hook lines; keep ambiguous lines; preserve every propagation/deployment contract line verbatim
- [ ] Run `scripts/propagate_master_assets.py --once` to regenerate `claude/learnings/cross-phase-decisions.md`; verify it matches the edited source and was not hand-edited
- [ ] Manual QA: read through the surviving decision-log contract sections and confirm Phase 07-relied-on content is intact

## Stage 2: Docs scrub and final consistency check (AC3–AC6)

- [ ] Grep the six standard docs (`README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, `docs/LOCAL_DEVELOPMENT.md`) for live-hook claims and remove them; ensure the bypass-permissions security claim survives nowhere
- [ ] Rewrite README Acknowledgments (§ starting line 168) to past tense, keeping attribution to the surveyed repos while removing any claim of a live hook system
- [ ] Add accurate one-line mentions of the static done-notify config and the defunct scanner where the docs describe the repo's contents (wording consistent with feature 08's DEFUNCT marker)
- [ ] Grep surviving docs for links into the deleted paths (`docs/hooks/`, `PHASE_01/`, `PHASE_02/`, `PHASE_04/`); fix any found in the six standard docs and roadmap only (`dev/feature/` manifests exempt)
- [ ] Reconcile inventory/doc counts across README, ARCHITECTURE, and CODEBASE_CONTEXT against the post-feature-08 tree per `docs/TROUBLESHOOTING.md` § Documentation Drift (three-way agreement)
- [ ] Verify `docs/phases/PROJECT_ROADMAP.md` against post-removal reality; fix only factual mismatches, do not rewrite
- [ ] Run `.venv/bin/python -m pytest tests/` as regression insurance; suite must pass
- [ ] Land everything as one dedicated, revertable commit separate from code-deletion commits; confirm no "removed in Phase 05" annotations were added to any doc
