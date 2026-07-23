# Review Record: 15-comparative-audit-runs

## Summary

Reviewed the Comparative Scans convention (`auditor-conventions/SKILL.md`), the new hidden runner (`engagement-audit-runner.agent.md`), and the orchestrator wiring against the plan's 8 ACs. All category-vocabulary claims were verified against the four auditors' actual definitions (Security Scan: 10 categories confirmed; Auditor - Code and Auditor - Infra: 14 `###`-numbered categories each confirmed; security report has `ID`/`Category`/`Location` columns, so the matching key is valid). Propagation re-run confirmed fixed point (second run: zero changes); suite re-run at reviewed tree: 233 passed / 113 subtests, matching baseline. One issue found and fixed: `docs/ARCHITECTURE.md` count claims (44 → 45) were missed — the same summary-surface class caught in review 14.

## Verdict
Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Met | `engagement-audit-runner.agent.md` Dimensions table; `agents:` roster | Four reused agent files confirmed unmodified (`git status` clean; not in implement commit) |
| AC2 | Met | Runner "Report Retention" | `pairs/<pair>/<side>/audits/<dimension>/` matches feature 14's `engagement-workspace` per-side layout; internal-only stated |
| AC3 | Met | `auditor-conventions/SKILL.md:112-133` | Extended in place; severity referenced ("the 4-level scale above"), not restated; security-only per-finding matching on Category + file path, line numbers excluded, `ID` never compared; new/resolved rules present |
| AC4 | Met | Runner "Re-Runs and Deduplication"; orchestrator stage paragraph | Overwrite-in-place scoped to one side; "Never touch the other side's reports" |
| AC5 | Met | Runner "NOT RUN — Never a Pass"; orchestrator asymmetric-evidence paragraph | No new grants (runner tools: agent, read, search); offline dependency evidence rule present |
| AC6 | Met | `engagement-orchestrator.agent.md:5,85-99` | Roster entry, per-pair stage, compact summaries + pointers, boundaries pass-through; insertion placeholder retained |
| AC7 | Met (verified) | propagation + suite | Re-executed: second propagation run zero changes; 233 passed / 113 subtests at reviewed tree |
| AC8 | Met | All authored files | Each rule stated once; auditor vocabularies referenced by name, not restated |

Runtime behavior of an actual engagement audit run (reports on disk, one-side re-run) is unverified by design — deferred to phase-level manual QA per plan §F.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Stale agent-count claims (44) after adding the 45th agent — same class as review-14 finding | Medium | `docs/ARCHITECTURE.md:36,125` | AC7 | Fixed |
| 2 | Dependency dimension reuses `05e Dependency Auditor`, whose definition is diff-scoped ("branch diff" vs a confirmed baseline) and pins its report path to the PR-review conventions root; runner's parent-directed path and full-side scope rely on parent instruction overriding that prose | Medium | `source_of_truth/agents/05e-dependency-auditor.agent.md:8-9,20-21` | AC1/AC2 | Wont-Fix — plan AC1 explicitly names this agent and modifying reused auditors is a plan non-goal; behavior gap belongs to phase-level manual QA / feature 16 |
| 3 | `docs/CODEBASE_CONTEXT.md:15` names the plain-`.md` exception `prod-code-review.md`; actual file is `04f-prod-code-review.md` | Low | `docs/CODEBASE_CONTEXT.md:15` | — | Open (pre-existing, not introduced by this feature) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `docs/ARCHITECTURE.md` | 44 → 45 agent definitions (Mermaid label line 36; directory description line 125) | 1 |

## Remaining Concerns

- Issue #2: whether `05e Dependency Auditor` produces a useful full-side inventory when invoked without a branch diff is unverifiable statically — confirm during phase-level manual QA and before feature 16 consumes its report.
- Issue #3: filename inaccuracy in CODEBASE_CONTEXT, low severity, defer to next docs pass.

## Test Coverage Assessment
- Covered: AC7 (propagation fixed point, marker-guard counts recounted from disk, suite baseline); AC3 partially via skill sync tests.
- Missing: no automated check that runner/orchestrator prose contracts (report paths, NOT RUN, asymmetric evidence) stay in sync with the workspace skill — acceptable per plan §F (code-review evidence class); runtime behavior deferred to phase manual QA.

## Risk Summary
- `05e Dependency Auditor` scope mismatch (diff-scoped agent reused for full-side scans) is the main behavioral risk; flagged for phase QA.
- ARCHITECTURE.md count drift has now recurred twice (features 14 and 15); the existing review-learnings rule covers it but implementers keep missing that surface.
- All other contracts verified against actual auditor vocabularies; no propagation or test drift.
