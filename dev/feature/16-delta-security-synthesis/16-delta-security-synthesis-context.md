# Context: 16-delta-security-synthesis

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/agents/engagement-delta-synthesizer.agent.md` [PROPOSED - name TBD] | Delta document + SOW-exclusions partition (AC1, AC2, AC7) | Create |
| `source_of_truth/agents/engagement-security-narrative.agent.md` [PROPOSED - name TBD] | Four-section security narrative (AC3) | Create |
| `source_of_truth/agents/engagement-introduced-issues.agent.md` [PROPOSED - name TBD] | Internal engineer-facing introduced-issues report (AC4) | Create |
| `source_of_truth/agents/engagement-audit-trail.agent.md` [PROPOSED - name TBD] | Audit-trail proof checklist (AC5) | Create |
| `source_of_truth/agents/engagement-pricing-researcher.agent.md` [PROPOSED - name TBD] | Cloud/cost analysis; sole internet-grant agent (AC6) | Create |
| `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] | Roster + per-pair loop steps (AC8) — created by feature 14, extended by 15, extended here | Modify |
| `tests/test_propagate_master_assets.py` | Marker-guard count bump for new agents (AC9) | Modify |

### Read-Only Reference Files

| File | Role |
|------|------|
| `source_of_truth/agents/engagement-prepare.agent.md` | House style for engagement agents (frontmatter, boundary section, fail-fast, terse prose) |
| `source_of_truth/agents/web-research-specialist.agent.md` | Existing web-tool grant pattern: `tools: [read, edit, search, execute, web/fetch, web/screenshot, web/search]` — do NOT modify (plan non-goal); pricing-researcher mirrors the web grant shape only |
| `source_of_truth/agents/auditor-code.agent.md` | Read/search/edit-class grant pattern for non-internet agents: `tools: [read, search, edit, fetch]` (note: `fetch` present on auditors — pricing-researcher exclusivity claim applies to web/search-class grants; verify grant wording during implementation) |
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Comparability convention (categories, severity scale, security per-finding identifiers) extended by feature 15 — consumed, not modified |
| `source_of_truth/skills/engagement-configuration/SKILL.md` | Source of the per-pair value-story `mode` field (14's AC7) |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase document (Key Deliverables 3–5, bundle 3) |
| `source_of_truth/agents/README.md` | Agent catalog — plan defers catalog entries to 18 unless the implementer decides otherwise |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| No contradictions found in AC substance | Plan is consistent with codebase and sibling plans 14/15 | None |
| All six agent file names correctly carry `[PROPOSED - name TBD]`; none exist on disk yet | The orchestrator file is created by feature 14 (wave 1) — this feature cannot start until 14 and 15 have landed | Confirms wave-3 sequencing; no plan change |
| Traceability cites `tests/test_propagate_master_assets.py:768-769`; the actual count-guard `roots` list currently sits at lines ~766–771 (counts 28/19/43/43/0) and line numbers will shift after 14/15 land | Line references are approximate; the guard itself is verified real | Implementer: locate guard by the `roots = [` block, recount from disk per the test's own comment convention, not by line number |
| Auditor-class agents already carry `fetch` in `tools:` (e.g., `auditor-code.agent.md`) | The "sole internet-touching fleet agent" claim (AC6) should be worded as sole *web-search/web-fetch* grant among the new engagement fleet, or grants chosen to make the claim literally true for the engagement roster | Implementer records the precise grant wording as a decision |
| Sibling bundles 14 and 15 currently contain only `-plan.md` files (no context/tasks yet) | No blocking impact; 16 consumes their plans' contracts (workspace skill, working state, comparability convention, asymmetry flag, one-side re-run) | None |
| Learnings contain directly relevant propagation contracts (display-name roster resolution; run-to-fixed-point; marker-guard recount-from-disk) | Prevents known failure modes in Stage 4 | Captured under Relevant Learnings |

## Architectural Decisions (from plan)

- **Single-point exclusions partition**: SOW-exclusions routing logic lives in one place — the synthesizer that partitions findings; the security narrative and delta doc consume the partition, never re-derive it. Implementer documents where the partition happens.
- **Merge permission**: five subagents proposed; closely-coupled documents may merge into fewer agents (e.g., audit-trail into delta synthesizer) if each output document's contract survives — record the merge as a decision. **Exception**: pricing-researcher must remain its own agent (internet grant + query-hygiene rule must not attach to anything else).
- **Report-vs-report, never git-diff**: all consumers read 15's retained reports under the comparability convention.
- **Client-facing docs lead with business language**; technical evidence in appendices (phase house rule).
- **Query hygiene is an AC in the pricing-researcher's own definition**, not orchestrator prose — the phase's highest-sensitivity control.
- **Grants**: pricing-researcher is the only new agent with web access; all other new agents get read/search/edit-class grants mirroring existing auditor patterns.

## Constraints

- `source_of_truth/` is the only authoring surface; never hand-edit `ports/` or `.github/` (AC9).
- Brevity (AC10): each definition states behavior, constraints, output contract once; shared rules (client-code boundary, workspace layout, comparability conventions) are referenced, not restated. A definition that says the same thing twice fails review.
- No finding is silently dropped: every original-side security risk classifies as exactly one of repaired / out-of-scope / residual (AC3); ambiguous SOW exclusions route conservatively into findings with a user-review flag (AC2).
- NOT RUN dimensions surface as asymmetric evidence in every synthesized document — never a delta, never a pass (AC7); audit-trail reads NOT VERIFIED (AC5).
- Introduced-issues report is internal-only by header, never client-facing (AC4); ambiguous visibility labeled "new or newly-visible," never asserted introduced.
- Pricing: every quantified figure cites source + retrieval date; offline → qualitative-only with NOT RESEARCHED markers — never invented figures (AC6).
- Document filenames within the workspace layout are `[PROPOSED - names TBD]`; implementer fixes and records them for 18's manifest schema.

## Scope Boundaries

- No remediation of any finding.
- No standalone out-of-scope register (AC2 routing replaces it).
- Do not touch narrative/spec docs (feature 17) or manifest/compliance docs (feature 18).
- Do not modify `web-research-specialist.agent.md` — the pricing-researcher is new and terse, not an extension of it.
- Do not modify feature 15's auditors, the security-scan asset, or `engagement-prepare.agent.md`.
- Orchestrator edits are additive (roster entries + loop steps); preserve 14's contract and 15's wiring.

## Relationships to Sibling Plans

- **Depends on 14** (`dev/feature/14-engagement-orchestrator-core/`): workspace layout skill, working-state file, compact-handoff contract, inherited boundaries, value-story `mode` field.
- **Depends on 15** (`dev/feature/15-comparative-audit-runs/`): retained per-side reports, comparability convention (categories, severity scale, security per-finding identifiers), asymmetric-evidence flag, one-side re-run flow.
- **Upstream of 18**: fixed document filenames/locations feed the manifest schema; audit-trail proof is grouped with compliance materials in 18's manifest.
- Sequential (wave 3, not parallel-safe): shares the orchestrator agent file with 14 and 15.

## Suggested Implementation Order

Stages 1 → 2 → 3 build the agent definitions (3 can be authored in parallel with 1–2 conceptually, but the exclusions partition from Stage 1 is consumed by Stage 2's narrative); Stage 4 wires the orchestrator, propagates to fixed point, and updates count guards last.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill definitions + Python 3 (stdlib-only) propagation/deploy scripts |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 233 passed, 113 subtests passed — captured 2026-07-22 |
| Lint | Not configured |
| Format | Not configured |
| Propagation | `python3 scripts/propagate_master_assets.py --once` — run repeatedly until a run reports zero changes |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:
- The propagator resolves `agents:` roster references by **display name**, not slug — new roster entries in the orchestrator must use display names.
- Propagation is **not idempotent** across agent additions/renames: run until every change counter is zero; "I ran the propagator" is not evidence of convergence (pinned by `test_committed_tree_is_at_a_propagation_fixed_point`).
- Marker-guard counts must be **recounted from disk** (`ls ports/<harness>/agents`), not incremented from memory (convention stated in the test's own comments).
- A `--watch` propagator holding stale code is a silent-failure hazard — prefer `--once` runs during this feature.

From `.github/learnings/project-learnings.md`:
- **Never give an offline agent a required check whose evidence cannot exist locally** — supports AC6's offline fallback design (NOT RESEARCHED, never a hard failure or invented figures).
- **Security caps must fail closed, not downgrade to warnings** — supports conservative routing (AC2) and NOT VERIFIED semantics (AC5).
- **Prose-guard tests match exact strings across line wraps** — if any test asserts on agent prose, keep required phrases (e.g., NOT VERIFIED, NOT RESEARCHED) exact and unwrapped-sensitive.
