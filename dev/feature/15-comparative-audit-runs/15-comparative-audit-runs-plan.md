# Plan: 15-comparative-audit-runs

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** no
- **Depends on:** 14-engagement-orchestrator-core
- **Key files modified:** `source_of_truth/skills/auditor-conventions/SKILL.md`, `source_of_truth/agents/engagement-audit-runner.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] (roster + loop step), `tests/test_propagate_master_assets.py` (verify — marker-guard counts)
- **Sequential reason:** shares the orchestrator agent file with upstream 14-engagement-orchestrator-core; consumes its workspace layout and subagent contract

Phase document: `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` (Key Deliverable 2, bundle 2).

## A. Requirements & Traceability

Acceptance criteria:

- **AC1**: For each pair, each audit dimension runs against **both sides' analysis branches** using existing agents unchanged: security (full-codebase `security-scan` asset), code quality (`z-auditor-code`), dependencies/supply-chain (`z-dependency-auditor`), infrastructure/configuration (`z-auditor-infra`). Same agent, both checkouts.
- **AC2**: Every raw report each auditor naturally produces (`-report.md` / `-summary.md`) is retained on disk as a first-class internal artifact in the workspace layout from feature 14 — per dimension, per side, per pair. Nothing is client-facing by default.
- **AC3**: A short section appended to the existing `auditor-conventions` skill (extended in place — no parallel convention) fixes stable category names so two independent scans are comparable, **reusing the skill's existing 4-level severity scale** (already defined there — reference it, do not restate or redefine). Per-finding matching identifiers are specified for the **security dimension only**; category-level rollups elsewhere. Unmatched findings are classified explicitly as "new" or "resolved," never dropped.
- **AC4**: One-side re-run is supported: re-running a single side's scans overwrites that side's reports in place (git history is the version record) without redoing the pair.
- **AC5**: Capability boundaries hold per side: auditors keep their existing grants (no shell grant added); dependency vulnerability evidence is supplied offline or the dimension is NOT RUN — never a pass; graph unavailability is NOT RUN with a reason. A dimension NOT RUN on one side is recorded as **asymmetric evidence** for the pair, never presented as a delta.
- **AC6**: The scan-run step is wired into the orchestrator: roster entries added, per-pair loop invokes the runs, children return compact summaries + report pointers only, inherited boundaries pass through.
- **AC7**: `source_of_truth/` only; propagation to a fixed point; no new test failures vs. baseline (count guards updated if agent counts shift).
- **AC8 (brevity)**: definitions state each rule once; the conventions extension does not restate what the auditors already define.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC2, AC4, AC6 | `engagement-audit-runner.agent.md` [PROPOSED - name TBD], orchestrator agent file | Code-review evidence; existing propagation suite |
| AC3 | `source_of_truth/skills/auditor-conventions/SKILL.md` | Code-review evidence; existing skill sync tests |
| AC5 | runner + conventions text | Code-review evidence (NOT RUN / asymmetric-evidence wording present) |
| AC7 | `ports/`, `.github/`, `tests/test_propagate_master_assets.py:768-769` | Existing automated suite; count bump if needed |

Non-goals: delta synthesis or any client-facing document (16); remediation of findings; report-versioning machinery or heavyweight report schema; modifying `z-auditor-code`, `z-auditor-infra`, `z-dependency-auditor`, or `security-scan` themselves (the comparability convention lives in the shared skill they already load).

## B. Correctness & Edge Cases

- Design decision (documented for reviewer): whether "the scan-run subagent(s)" is one runner agent parameterized by dimension+side or a thin per-dimension wrapper — choose the fewest new definitions that keep the orchestrator handoff compact; the phase permits either ("subagent(s)").
- A dimension NOT RUN on one side → per-pair record marks that dimension asymmetric; downstream (16) must see this flag, so it lives in the runner's summary and the working-state entry.
- Deduplicated repos across pairs: reports are keyed by (pair, side); a shared repo prepared once still gets its reports recorded for every referencing pair (pointer reuse, not re-scan).
- Re-run of one side must not touch the other side's reports.
- Auditors run from analysis-branch checkouts and should consume graphs/docs rather than raw full-file sweeps where possible (phase Technical Context).

## C. Consistency & Architecture Fit

- Extend `auditor-conventions` **in place**; existing auditors already load it, so comparability comes free — no auditor edits.
- Runner follows the feature-14 subagent contract: summary + pointers return shape, inherited boundaries verbatim.
- Report filenames follow the existing `-report.md` / `-summary.md` convention from the Dev Task Folder instructions; only their *location* (workspace layout) is new.
- New symbols: category-name list and severity-scale labels in the conventions extension are `[PROPOSED - names TBD]` unless copied from existing auditor output vocabulary — implementer must derive them from the auditors' current category vocabulary, not invent a parallel one.

## D. Clean Design & Maintainability

Simplest design: one skill section + one runner agent + a loop paragraph in the orchestrator. Keep-it-clean: severity scale defined once in the skill; runner cites it, never restates it.

## E. Observability, Security, Operability

- Observability: retained raw reports + working-state pointers are the record; no new logging.
- Security: inherited client-code boundary; auditors gain no new grants (AC5); reports live in the workspace root, outside client repos.
- Runbook: propagate to fixed point → `uv run pytest tests/` → deploy on user request.

## F. Test Plan

- Must-have automated: existing propagation/sync suite; count-guard bump at `tests/test_propagate_master_assets.py:768-769` if the runner agent shifts generated counts.
- Existing tests to update: count guard only (verify).
- Code-review evidence: AC1–AC6, AC8 (grant lists unchanged on the four reused assets; NOT RUN wording; new/resolved classification present).
- Manual QA: phase-level (per-pair per-side reports on disk in the agreed layout; one-side re-run refreshes only that side) — see execution manifest.

Top evidence checks:
1. Given the conventions extension, when compared against `z-auditor-code`/`z-auditor-infra`/`z-dependency-auditor`/`security-scan` vocabularies, then category names map without a parallel taxonomy.
2. Given the runner definition, when reviewed, then per-finding identifiers appear only under the security dimension.
3. Given a NOT RUN dimension on one side, when the runner reports, then the pair record says asymmetric evidence — no delta claim.
4. Given a one-side re-run instruction, when reviewed, then overwrite-in-place semantics are stated and scoped to that side.
5. Given propagation, second run reports zero changes.

## Stage 1: Comparability Convention
**Goal**: `auditor-conventions` extension — stable categories, shared severity scale, security per-finding identifiers, new/resolved classification
**Success Criteria**: AC3, AC8
**Status**: Not Started

## Stage 2: Scan-Run Subagent + Orchestrator Wiring
**Goal**: runner agent(s) writing retained reports into the workspace layout with one-side re-run support; orchestrator roster/loop step
**Success Criteria**: AC1, AC2, AC4, AC5, AC6
**Status**: Not Started

## Stage 3: Propagate & Verify
**Goal**: fixed point, count guards, clean baseline
**Success Criteria**: AC7
**Status**: Not Started

## Relationship Notes

Consumes 14's workspace layout and subagent contract. Upstream of 16: the retained per-side reports and the comparability convention (categories, severities, security finding identifiers, asymmetric-evidence flag) are 16's inputs — those contracts are ACs here per the cross-feature API rule.
