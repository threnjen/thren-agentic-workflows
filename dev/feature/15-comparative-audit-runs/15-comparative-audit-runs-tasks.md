# Tasks: 15-comparative-audit-runs

Prerequisite: feature 14-engagement-orchestrator-core is implemented (orchestrator agent and workspace-layout skill exist with final names).

## Stage 1: Comparability Convention (AC3, AC8)

- [x] Read the final artifacts from feature 14 (orchestrator agent file, workspace/layout skill) and record their actual names for use below
- [x] Derive stable category names from the existing vocabularies of `security-scan`, `auditor-code`, `auditor-infra`, and `05e-dependency-auditor` — no parallel taxonomy; record final names in the implementation record
- [x] Append a comparability section to `source_of_truth/skills/auditor-conventions/SKILL.md`: stable category names, reference (not restatement) of the existing 4-level severity scale, so two independent scans are comparable
- [x] Specify per-finding matching identifiers for the security dimension only (build on security-scan's existing ID/Category/Location columns); category-level rollups for other dimensions
- [x] Specify that unmatched findings are classified explicitly as "new" or "resolved," never dropped
- [x] Brevity check: extension states each rule once and does not restate what the auditors already define

## Stage 2: Scan-Run Subagent + Orchestrator Wiring (AC1, AC2, AC4, AC5, AC6)

- [x] Decide runner shape (one parameterized runner vs. thin per-dimension wrappers) — fewest new definitions with a compact orchestrator handoff; document the decision
- [x] Create the runner agent definition(s) in `source_of_truth/agents/` (`user-invocable: false`; follow `engagement-prepare.agent.md` house style): runs all four dimensions (security-scan, auditor-code, 05e-dependency-auditor, auditor-infra) against both sides' analysis branches, agents unchanged
- [x] Runner writes every raw `-report.md` / `-summary.md` into feature 14's workspace layout, keyed per dimension, per side, per pair; nothing client-facing by default
- [x] Runner supports one-side re-run: overwrites that side's reports in place, never touches the other side; deduplicated repos get pointer reuse per (pair, side), not re-scan
- [x] Runner enforces capability boundaries: no new grants on reused auditors, dependency evidence offline or dimension NOT RUN (never a pass), graph unavailability = NOT RUN with reason; NOT RUN on one side is recorded as asymmetric evidence in the runner summary and the working-state entry, never a delta
- [x] Wire into the orchestrator agent file: add roster entries, per-pair loop step invoking the runs; children return compact summaries + report pointers only; inherited boundaries pass through verbatim

## Stage 3: Propagate & Verify (AC7)

- [x] Run `python3 scripts/propagate_master_assets.py --once` twice; second run reports zero changes
- [x] Recount generated agent files from disk (`ls ports/<harness>/agents`) and update the count guard at `tests/test_propagate_master_assets.py:766-771` if counts shifted
- [x] Run `uv run pytest tests/` — no new failures vs. baseline (233 passed, 113 subtests)
- [x] Verify code-review evidence items: category names map to auditor vocabularies without a parallel taxonomy; per-finding IDs appear only under security; asymmetric-evidence and overwrite-in-place wording present; reused auditor grant lists unchanged
