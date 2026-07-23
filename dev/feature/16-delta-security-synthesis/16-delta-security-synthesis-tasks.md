# Tasks: 16-delta-security-synthesis

## Stage 1: Delta Synthesizer + Exclusions Routing

- [x] Verify prerequisites on disk: feature 14's orchestrator agent + workspace/config skills and feature 15's conventions extension + runner exist; record the actual file names 14/15 chose (all were `[PROPOSED]`)
- [x] Create the delta-synthesizer agent definition [PROPOSED - name TBD] following `engagement-prepare.agent.md` house style (frontmatter, boundary reference, fail-fast, terse prose), with read/search/edit-class grants only
- [x] Define the delta document contract (AC1): headline-metrics table; resolved/improved/unchanged/new classification; business-framed narrative first, technical evidence in appendices; citations to retained raw reports; value-story `mode` as input so intentional change is not framed as regression
- [x] Implement the single-point SOW-exclusions partition (AC2): security exclusions → security narrative section 3; all others → delta doc out-of-scope section (severity-rated); no SOW → all findings retained + missing input recorded in working state; ambiguous → conservative routing into findings with user-review flag; no finding silently dropped
- [x] Document where the partition lives so the narrative and delta docs consume it, never re-derive it (record as decision)
- [x] State asymmetric-evidence handling (AC7): a NOT RUN dimension is reported as asymmetric evidence, never a delta

## Stage 2: Security Outputs

- [x] Create the security-narrative agent [PROPOSED - name TBD] with the four sections (AC3): posture, repaired-tied-to-SOW-scope, pre-existing out-of-scope (authoritative security-exclusions treatment), residual risks leading with business consequence + brief mechanism note
- [x] Encode the classification-completeness rule: every original-side security risk lands in exactly one of repaired / out-of-scope / residual; zero-findings case emits sections 2–4 with honest empty-state statements
- [x] Create the introduced-issues agent [PROPOSED - name TBD] (AC4): internal-only header (never client-facing), full technical detail per finding (file, finding, severity, evidence) using 15's per-finding security identifiers; visibility-ambiguous findings labeled "new or newly-visible"
- [x] Document the fix flow in the introduced-issues definition: report → engineer fixes → one-side re-run (15) → finalize client-facing artifacts; upgraded-side scan NOT RUN → report reads NOT RUN, not "no introduced issues"
- [x] Create the audit-trail agent [PROPOSED - name TBD] (AC5): checklist of original-side flagged categories × upgraded-side status, citing upgraded-side raw reports; unverifiable category reads NOT VERIFIED, never a pass; "same standard" framing
- [x] If merging closely-coupled documents into fewer agents, verify each output document's contract survives intact and record the merge as a decision (pricing-researcher may never be merged)

## Stage 3: Pricing Researcher + Cloud/Cost Analysis

- [x] Create the pricing-researcher agent [PROPOSED - name TBD] (AC6) as its own agent with a web-access grant (mirror `web-research-specialist` grant shape); all other new agents remain web-free
- [x] State query hygiene in the agent's own definition: queries contain only generic service/product names and pricing questions — never client code, config values, identifiers, or engagement repo content
- [x] Define the cloud/cost analysis contract: scan/dependency evidence of change → per-pair client-facing analysis; every quantified figure cites source + retrieval date; undated/unsourced figures stay qualitative
- [x] Define the offline fallback: no internet → qualitative-only with quantified claims marked NOT RESEARCHED — never invented figures
- [x] Record the precise "sole internet-grant" wording as a decision (existing auditors carry `fetch`; scope the exclusivity claim so it is literally true — see context Discovery Delta)

## Stage 4: Orchestrator Wiring, Propagate & Verify

- [x] Add all new agents to the orchestrator roster (display names — the propagator resolves rosters by display name) and add per-pair loop steps under the compact-handoff contract, writing into the workspace layout with inherited boundaries passed through (AC8)
- [x] Fix the output document filenames within the workspace layout and record them for feature 18's manifest schema
- [x] Brevity pass (AC10): each definition states behavior, constraints, output contract once; shared rules (boundary, layout, conventions) referenced, not restated
- [x] Run `python3 scripts/propagate_master_assets.py --once` repeatedly until a run reports zero changes (fixed point)
- [x] Update the marker-guard counts in `tests/test_propagate_master_assets.py` (locate the `roots = [` block; recount from disk via `ls ports/<harness>/agents`, per the test's comment convention)
- [x] Run `uv run pytest tests/` — no new failures vs. baseline (233 passed, 113 subtests) (AC9)
- [x] Walk the plan's five top evidence checks (classification completeness; pricing rules in one file; NOT VERIFIED/NOT RUN wording; `mode` framing + out-of-scope non-security-only; propagation zero-change) and record results in the implementation record
