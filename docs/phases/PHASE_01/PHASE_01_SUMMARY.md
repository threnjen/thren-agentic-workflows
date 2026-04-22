# Phase 1: Token Efficiency Optimization

**Status**: Validation Complete - NO-GO (evidence normalization required)
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: `docs/AGENT_REGRESSION_BENCHMARK_SPEC.md` (Sections 19-25)

## Objective

Reduce total token consumption by at least 30% per full pipeline run while preserving planning and delivery quality.
This phase establishes a measurable, low-risk token reduction strategy across prompts, agent instructions, and response behavior.

## Scope

### In Scope
- Establish baseline and variant measurement for full pipeline token usage.
- Compress high-traffic prompt sources (agents, instructions, AGENTS templates, and selected docs).
- Introduce concise response defaults with soft output targets.
- Remove repeated boilerplate where equivalent shared instructions or skills already exist.
- Validate non-regression on decomposition accuracy, test/review rigor, and edge-case discovery quality.
- Deliver all changes in one large PR on the current working branch.

Phase 01 measurement execution must follow the normative protocol in `docs/AGENT_REGRESSION_BENCHMARK_SPEC.md` Sections 19-25, including:
- fixed full-pipeline scenario IDs for baseline and variant
- required run metadata (`branch`, `commit`, `scenario_id`, `timestamp_utc`)
- comparability checks before delta computation
- explicit out-of-scope exclusions
- quality-gate evidence capture

### Out of Scope
- Hook framework implementation or runtime interception changes.
- Tool permission model changes (existing GitHub agent tool scopes remain).
- Model routing or provider switching strategy changes.
- Broad architecture redesign of the orchestrator/subagent system.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|---|---|---|
| 1 | Baseline Token Benchmark Spec | Defines per-full-run measurement protocol, capture format, and comparison criteria | Baseline instrumentation |
| 2 | Prompt Compression Change Set | Consolidates repeated prose and trims high-cost instruction paths | Agent/instruction compaction |
| 3 | Concise Output Policy | Adds soft output targets and delta-first response norms | Response policy updates |
| 4 | Validation Report | Before/after benchmark plus quality gate verification | Regression benchmark pass |

## Technical Context

Primary optimization surfaces in this repository:
- `nodejs/AGENTS.md`
- `python/AGENTS.md`
- `docs/CODEBASE_CONTEXT.md`
- `README.md`
- `.github/agents/phase-refiner.agent.md`
- `.github/agents/project-planner.agent.md`
- `.github/agents/feature-decomposer.agent.md`
- `.github/agents/phase-execute.agent.md`
- `.github/instructions`
- `.github/skills`

Observed token pressure patterns to target:
- Long repeated workflow prose in multiple agent files.
- Repeated mandatory sections that can be centralized and referenced.
- Verbose orchestrator prompt blocks for subagent invocations.
- Overlapping AGENTS template guidance between language variants.

## Feature 02 Compaction Change Map

### Hotspot Inventory (Prioritized)

| Priority | Category | Surface | Rationale |
|---|---|---|---|
| P1 | Templates | `nodejs/AGENTS.md`, `python/AGENTS.md` | High-traffic copy targets with repeated workflow and quality prose |
| P2 | Docs | `README.md`, `docs/CODEBASE_CONTEXT.md` | Canonical structure references used by maintainers and downstream agents |
| P3 | Agents | `.github/agents/*.agent.md` | Large prompt surfaces identified for follow-up compaction passes |
| P4 | Instructions | `.github/instructions/*.instructions.md` | Mostly concise already; lower token-return priority |

### Grouped Change Summary

| Category | Files | Change Type | Expected Token Effect |
|---|---|---|---|
| Templates | `nodejs/AGENTS.md`, `python/AGENTS.md` | Compacted repeated principles/testing/communication boilerplate | High |
| Docs | `README.md`, `docs/CODEBASE_CONTEXT.md` | Synced canonical section naming and compaction rationale | Medium |
| Agents | `.github/agents/feature-decomposer.agent.md`, `.github/agents/test-analyst.agent.md` | Centralized duplicated approval/autonomy wording via existing read-only instruction behavior | Low-Medium |
| Instructions | `.github/instructions/codebase-context-bootstrap.instructions.md`, `.github/instructions/documentation-freshness-check.instructions.md` | Compacted wording into shorter equivalent guidance | Low |
| Phase docs | `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Added review-ready hotspot inventory and grouped change map | Medium |

### Scope Conformance Notes

- This change set is docs-only and does not introduce hook/runtime interception.
- Tool permissions, model routing, and runtime behavior are unchanged.
- Safety, correctness, approval, and quality-gate constraints remain explicitly documented.

## Dependencies & Risks

- **Dependency**: Reliable benchmark runs against branch `token-reduction-work`.
- **Dependency**: Stable full-pipeline scenario selection for before/after comparability.
- **Risk**: Over-compression removes decision-critical constraints.
  - **Mitigation**: Preserve safety/correctness/approval constraints; compress only redundant narrative.
- **Risk**: Token reduction masks quality regression.
  - **Mitigation**: Gate phase completion on quality checks for decomposition, review rigor, and edge-case coverage.
- **Risk**: One large PR increases review complexity.
  - **Mitigation**: Include explicit change map and grouped diff summary by file category.

## Measurement Guardrails

- Baseline and variant runs are comparable only if scenario IDs and run scope match.
- Missing provenance metadata invalidates a run for comparison.
- Excluded changes (hook/runtime interception and tool-scope changes) invalidate comparability.
- Phase completion requires both >=30% total token reduction and all quality gates passing.

## Success Criteria

- [ ] Full pipeline run token usage is reduced by at least 30% versus baseline.
- [ ] Output verbosity decreases under soft targets without hard failure behavior.
- [ ] No observed regression in decomposition accuracy.
- [ ] No observed regression in test/review rigor.
- [ ] No observed regression in edge-case discovery quality.
- [ ] A single consolidated PR contains benchmark evidence and quality-gate outcomes.

Pass/fail evaluation follows the benchmark spec:
- PASS: >=30% reduction and all quality gates pass
- FAIL: <30% reduction
- REVIEW_REQUIRED: >=30% reduction with any quality-gate failure or incomplete evidence

## End-to-End Validation Outcome (Feature 03)

Validation date: 2026-04-22  
Validation report: `dev/research/phase-01-end-to-end-validation-regression-analysis/phase-01-end-to-end-validation-regression-analysis-report.md`

Benchmark outputs generated:
- `docs/benchmarks/B001/runs/local/B001-PHASE01-20260422-candidate-B-report.json`
- `docs/benchmarks/B001/runs/local/B001-PHASE01-20260422-candidate-C-report.json`

Token delta summary (baseline total = 43,700 tokens):

| Candidate | Variant total tokens | Reduction vs baseline | Outcome |
|---|---:|---:|---|
| Candidate B | 35,900 | 17.85% | Below 30% target |
| Candidate C | 43,900 | -0.46% | Token regression |

Quality and comparability summary:
- Candidate B failed review-rigor indicators (pass-rate drop in review family and hard-fail gate).
- Candidate C retained decomposition/review quality but did not improve token usage and remained below the 30% reduction target.
- Edge-case discovery quality remains inconclusive with current benchmark-family signals and requires explicit evidence in a normalized rerun.
- Current example payloads do not fully satisfy Phase 01 normative metadata/provenance requirements for comparable Phase 01 promotion evidence.

Final gate verdict for Phase 01: **NO-GO**.

Remediation routing:
- Token optimization remediation -> `dev/feature/02-prompt-instruction-compaction/`
- Output policy remediation -> `dev/feature/02-output-verbosity-policy/`
- After remediation, rerun normalized baseline/variant capture and re-evaluate this phase.

## QA Considerations

- Manual QA document should include:
- Baseline run metadata and variant run metadata.
- Token deltas per pipeline stage and total end-to-end run.
- Qualitative comparison of planning completeness and review findings quality.
- Spot-check that compressed prompts still produce traceable, actionable outputs.

## Notes for Feature - Decomposer

Decompose this phase into 4 features:
1. Baseline and Measurement Framework
2. Prompt and Instruction Compaction
3. Output Verbosity Policy (Soft Targets)
4. End-to-End Validation and Regression Analysis

Feature boundaries:
- Feature 1 must complete first to establish acceptance thresholds and comparable run protocol.
- Features 2 and 3 can proceed in parallel after Feature 1.
- Feature 4 must run last and aggregate benchmark plus quality conclusions.

Key decomposition constraints:
- Do not introduce hook/runtime interception work.
- Keep tool scope behavior unchanged; optimize prompt content and response policy only.
- Preserve planning quality behaviors while reducing verbosity and duplication.

Refinement summary for this iteration:
- Scope narrowed to prompt/output optimization, explicitly excluding hooks.
- Success metric fixed at at least 30% reduction per full pipeline run.
- Quality guardrails fixed to decomposition accuracy, test/review rigor, and edge-case discovery quality.
- Delivery strategy fixed to one large PR with regression benchmark evidence.
