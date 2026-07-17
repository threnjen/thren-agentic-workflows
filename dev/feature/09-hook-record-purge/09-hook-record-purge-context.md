# Feature Context: 09-hook-record-purge

Companion to `09-hook-record-purge-plan.md`. Phase document:
`docs/phases/PHASE_05/PHASE_05_SUMMARY.md` (Deliverable 3). Discovery context:
`docs/phases/PHASE_05/PHASE_05_DISCOVERY_CONTEXT.md`.

## Key Files

### Files being changed

| File | Role | Change Type |
|------|------|-------------|
| `docs/phases/PHASE_01/` | Historical hook phase record | Delete (directory) |
| `docs/phases/PHASE_02/` | Historical hook phase record | Delete (directory) |
| `docs/phases/PHASE_04/` | Historical hook phase record | Delete (directory) |
| `docs/hooks/` (7 files: bash-command-limitations, file-access-guard, hook-verification, injection-benchmark, installation, manual-qa, prompt-injection-defense) | Hook documentation | Delete (directory) |
| `.github/learnings/cross-phase-decisions.md` | Decision log; source of generated copy | Modify (section deletion + line-level scrub) |
| `claude/learnings/cross-phase-decisions.md` | Generated propagator copy | Regenerate via `--once` only — never hand-edit |
| `README.md` | Top-level doc; Acknowledgments at line 168 (§ ~168–194) | Modify (scrub + past-tense rewrite; counts) |
| `docs/ARCHITECTURE.md` | Architecture doc | Modify (scrub; counts) |
| `docs/CODEBASE_CONTEXT.md` | Inventory doc | Modify (counts) |
| `docs/TROUBLESHOOTING.md` | Ops doc; § Documentation Drift at line 110 | Modify (scrub if needed) |
| `HARNESS_SETUP.md` | Harness setup doc | Modify (scrub) |
| `docs/LOCAL_DEVELOPMENT.md` | Dev workflow doc | Modify (scrub) |
| `tests/test_phase04_runtime_deployment.py` | Contains `test_explicit_rtk_guidance_remains_available` reading `docs/hooks/*.md` (lines ~1003–1012) | Modify/delete that test if it still exists after feature 08 (see Discovery Delta) |

### Read-only reference files

| File | Role |
|------|------|
| `docs/phases/PROJECT_ROADMAP.md` | Verify-only (AC5); fix only factual mismatches |
| `docs/phases/PHASE_03/`, `PHASE_05/`, `PHASE_07/`, `docs/inspiration/` | Must remain untouched |
| `scripts/propagate_master_assets.py` | Run with `--once` to regenerate learnings copy |
| `eval/hooks/post-commit.sh` | Planning-pipeline git hook — untouchable |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `tests/test_phase04_runtime_deployment.py::test_explicit_rtk_guidance_remains_available` (line ~1003) reads three `docs/hooks/*.md` files from disk and will fail when `docs/hooks/` is deleted | Deleting the directory breaks the suite unless feature 08 has already removed this test | **Warning to Decomposer**: confirm feature 08 removes it; otherwise this feature must delete that test — but AC6 requires the record purge to be a docs-only commit, so the test removal would need its own commit or reassignment to feature 08 |
| Decision-log section anchors verified exact: "Deferred Pipeline Work" line 22, "Hook Composition" 228, "Guard Friction and Command Prompting" 233, "File-Access Guard Retirement" 248, "Propagation Contracts" 293, "Phase 04 Runtime Deployment Contract" 368 | Plan's line references are accurate | None |
| The six standard docs and PROJECT_ROADMAP already contain **zero** links to `docs/hooks/` or `docs/phases/PHASE_01|02|04/` | The dangling-link cleanup (plan § B) is likely a no-op; re-verify after deletion anyway | None — keep the verification grep task |
| Remaining "hook" mentions in the six docs: README 9, ARCHITECTURE 1, HARNESS_SETUP 2, LOCAL_DEVELOPMENT 1, TROUBLESHOOTING 0, CODEBASE_CONTEXT 0 | Scrub scope is modest; some counts may change after features 07/08 land (they also touch docs-adjacent state) | Re-grep at implementation time against the post-08 tree |
| All plan-referenced files exist, including `claude/learnings/cross-phase-decisions.md`, README Acknowledgments (line 168), and TROUBLESHOOTING § Documentation Drift (line 110) | Plan validated | No contradictions found |

## Architectural Decisions

- **Whole-section vs line-level scrub**: pure-hook decision-log sections deleted
  wholesale; mixed sections ("Deferred Pipeline Work", "Propagation Contracts",
  "Phase 04 Runtime Deployment Contract") get line-level scrub only. When a line is
  ambiguous, keep it — over-retention is safer than over-scrub (user decision,
  2026-07-17).
- **Edit source, regenerate copy**: only `.github/learnings/cross-phase-decisions.md`
  is hand-edited; `claude/learnings/` is refreshed by `--once` so source and copy
  cannot diverge.
- **Single dedicated commit** (AC6): the record purge lands separately from any code
  deletion so it is trivially revertable — this is the over-scrub safety net.
- **No change-tracking annotations**: docs state current reality plainly; git history
  is the change record ("removed in Phase 05" notes are forbidden).
- **Acknowledgments rewritten to past tense**: attribution to surveyed repos stays
  (per `docs/inspiration/` retention decision); live-hook-system claims go.

## Constraints

- Prose-only feature: no code or test changes in scope (except the Discovery Delta
  test conflict above, which must be resolved with the Decomposer).
- Three-way count rule: README / ARCHITECTURE / CODEBASE_CONTEXT inventory counts
  must agree with each other and the post-feature-08 tree (`docs/TROUBLESHOOTING.md`
  § Documentation Drift, line 110).
- The bypass-permissions security claim must not survive anywhere in the six docs.
- Roadmap's "Defunct scanner" note must match feature 08's DEFUNCT marker wording.
- Test command: `.venv/bin/python -m pytest tests/` (system python3 lacks pytest).

## Scope Boundaries

- Do not touch: `eval/hooks/`, `docs/inspiration/`, `docs/phases/PHASE_03/`,
  `docs/phases/PHASE_05/`, `docs/phases/PHASE_07/`, Phase 03 / PR Review assets.
- Do not rewrite git history.
- Do not hand-edit `claude/learnings/cross-phase-decisions.md`.
- Do not rewrite `PROJECT_ROADMAP.md` — verify only; fix only factual mismatches.
- `dev/feature/` manifests are historical records — exempt from the dangling-link scan.
- Preserve verbatim every propagation/deployment contract line Phase 07 relies on in
  the mixed decision-log sections.

## Relationships to Sibling Plans

- **Depends on**: `07-propagator-hook-pipeline-removal` (static done-notify contract:
  no `$source`, hand-owned) and `08-hook-framework-retirement` (DEFUNCT marker
  wording; final file inventory for count reconciliation).
- Wave 3, runs last. No shared files with 07/08; the dependency is informational —
  docs must describe the tree those features produce.

## Suggested Implementation Order

1. Stage 1: delete the three phase dirs + `docs/hooks/`; scrub the decision log;
   run `--once` to refresh the generated learnings copy.
2. Stage 2: scrub the six docs, rewrite Acknowledgments, reconcile counts, verify
   roadmap, run the full suite, land as one dedicated commit.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3 (stdlib scripts + unittest/pytest); markdown docs repo |
| Test Runner | `.venv/bin/python -m pytest tests/` |
| Test Baseline | 401 passed, 156 subtests passed — captured 2026-07-17 (pre-features-07/08) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- `debugging-learnings.md` — "If code deletes files, validate the root before
  enumerating — not the leaf before unlinking": when running the propagator after the
  learnings edit, deletion/prune logic must be validated at the root; relevant because
  `--once` prune behavior runs against a tree with newly deleted directories.
- No other entries in `.github/learnings/` match this docs-only feature's domain.
