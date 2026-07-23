# Tasks: 18-compliance-package-manifest

## Stage 0: Upstream Name Resolution (prerequisite)

- [x] Read the implementation records of features 14–17 and collect the final agent names, skill names, and output-document filenames (workspace layout, working-state file, raw reports, delta/security docs, introduced-issues report, audit-trail proof, narrative docs, intended-behavior spec)
- [x] Resolve every `[PROPOSED - name TBD]` name in this plan against the implemented tree; record the resolved names in the implementation record

## Stage 1: Manifest Schema Skill (AC3, AC8)

- [x] Create the `engagement-package-manifest` skill [PROPOSED - name TBD] with SKILL.md defining the two-section (client-facing / technical-internal) markdown index, each an ordered table of contents
- [x] Define row fields: document name, path, audience, SOW-required vs. above-contract, present/missing status
- [x] Define expected-entry derivation from the engagement's pairs and modes (no hand-enumeration; multi-pair expansion; single-pair not assumed)
- [x] Fix the technical section's standing entries: raw reports, introduced-issues report, gap-review report, orchestrator working-state/run record, Phase 01 baseline snapshots
- [x] Group the audit-trail proof (16) with compliance materials in the client-facing ordering
- [x] State present/missing detection once; require all paths to resolve within the single workspace root; define the "no SOW" fallback for SOW-required labels
- [x] Cross-check: every document contract from 14–17 has exactly one expected-entry rule (evidence check 1)

## Stage 2: Compliance Writer + Gap Reviewer (AC1, AC2, AC4)

- [x] Create the compliance-writer agent [PROPOSED - name TBD]: acceptance criteria and test lists read only from the engagement's SOW document; each criterion walked through with evidence cited from retained on-disk artifacts; NOT RUN dimensions stated as NOT RUN/NOT VERIFIED, never a pass; missing-SOW path recorded honestly
- [x] Include the verification summary deliverable with the functional-preservation statement referencing 17's intended-behavior spec (by its implemented name)
- [x] Create the gap-reviewer agent [PROPOSED - name TBD]: client-perspective review of the complete markdown set using the manifest as completeness checklist; internal report emitted unconditionally (honest empty-state content when nothing to report); report is a standing technical-section manifest entry
- [x] Both agents: `user-invocable: false`, read/search/edit-class grants only, engagement-prepare house style, each rule stated once (AC8)

## Stage 3: Final Orchestrator Wiring (AC5)

- [x] Add both new agents to the orchestrator roster and append the final loop steps: compliance → manifest → gap review
- [x] Verify the per-engagement loop reads end to end: prepare → comparative audits → delta/security synthesis → narrative docs → compliance → manifest → gap review, every step under the compact-handoff contract and every output in the workspace layout

## Stage 4: Reconciliation, Propagate & Verify (AC6, AC7)

- [x] Reconcile `source_of_truth/agents/README.md` catalog entries for ALL Phase 02 agents — verify earlier features' entries landed, do not assume
- [x] Reconcile `docs/CODEBASE_CONTEXT.md` count claims (agent definitions, hidden/user-invocable split, skill count) by recounting from disk
- [x] Update marker-guard counts in `tests/test_propagate_master_assets.py` (`roots` list) by recounting generated files on disk (`ls ports/<harness>/agents`), and update the accompanying comment
- [x] Run `python3 scripts/propagate_master_assets.py --once` repeatedly until a run reports zero changes (fixed point)
- [x] Run `uv run pytest tests/` — no new failures vs. baseline (233 passed, 113 subtests)
- [x] Confirm the tree is commit-clean (phase-final gate) and record AC traceability plus resolved names in the implementation record
