# Feature Context: Phase Execute Audit Bookend

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---|---|---|
| `source_of_truth/agents/04-phase-execute.agent.md` | Live Phase Execute orchestrator. Extend its frontmatter roster, Step 1 scope/decision work, post-Step-5 bookend wiring, `all-approved` evidence, and both Step 6 prompt branches. | Modify |

### Read-Only References and Sibling-Owned Files

| File / Module | Role | Change Type |
|---|---|---|
| `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md` | Shared caller-neutral audit-comparison mechanism created by `08-audit-comparison-contract`; the implementer must discover its finalized slug from disk and load that exact skill. | Read-only reference |
| `source_of_truth/agents/delta-auditor.agent.md` | Existing interactive `Audit - Delta` consumer and current source of the Phase 3–6b sequence that Feature 08 extracts; do not spawn this orchestrator. | Read-only reference |
| `source_of_truth/agents/auditor-code.agent.md` | Existing `Auditor - Code` leaf. Defines the verified reduced test-file lens: Categories 2, 5, 8, and 9. | Read-only reference |
| `source_of_truth/agents/auditor-infra.agent.md` | Existing `Auditor - Infra` leaf. Its normal Documentation category must be explicitly overridden for this bookend. | Read-only reference |
| `source_of_truth/agents/auditor-delta.agent.md` | Existing `Auditor - Delta` leaf that may run only after both same-type full reports exist and state totals. | Read-only reference |
| `source_of_truth/agents/auditor-attribution.agent.md` | Existing `Auditor - Attribution` leaf used to settle provisional findings against both trees. | Read-only reference |
| `source_of_truth/agents/05a-baseline-worktree.agent.md` | Existing `Baseline Worktree` leaf and caller contract for materialization, created-versus-reused status, verification, and cleanup handshake. | Read-only reference |
| `source_of_truth/agents/04b-feature-implementer.agent.md` | Existing plan-driven implementer; remediation must use only the already-established bounded prose re-spawn exception from Phase Execute Steps 2.5 and 3. | Read-only reference |
| `source_of_truth/skills/auditor-conventions/SKILL.md` — `## Multi-Target Audits` | Canonical comparability, identical-prompt, snapshot-label, artifact-layout, and one-output-root rules; reference rather than duplicate. | Read-only reference |
| `source_of_truth/skills/audit-delta-report/SKILL.md` | Canonical delta, open-items queue, attribution, and reconciliation document contract; reference rather than duplicate. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing propagator-backed roster resolution, spawn-tool, frontmatter, and duplicate-block regression coverage. | Read-only reference |
| `tests/test_unity_consumer_contract.py` | Existing direct consumer of `04-phase-execute.agent.md`; asserts the Step 2.5 and Step 3 headings and multiple exact obligations that this feature must preserve. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing source-transform and generated-output regression input; run without invoking propagation. | Read-only reference |
| `tests/test_pr_review_orchestrator.py` | Existing full-suite regression input named by the plan; currently contains an unrelated known failure. | Read-only reference |
| `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` | Consolidated Phase 03 structural and mutation guards owned by downstream `11-audit-bookend-guards`; this feature must supply testable structure but must not create or edit the module. | Read-only reference |
| `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | Authoritative phase scope, runtime behavior, acceptance boundaries, and implementation order. | Read-only reference |
| `docs/phases/DISCOVERY_CONTEXT.md` | Project-level decisions for scope derivation, the one-time decision, skip semantics, and targeted post-remediation verification. | Read-only reference |
| `dev/feature/08-audit-comparison-contract/08-audit-comparison-contract-plan.md` | Upstream contract and final-skill-name dependency. | Read-only reference |
| `dev/feature/09-audit-delta-rewire/09-audit-delta-rewire-plan.md` | Parallel Wave 2 sibling consuming the same finalized skill. | Read-only reference |
| `dev/feature/11-audit-bookend-guards/11-audit-bookend-guards-plan.md` | Wave 3 verification owner for the skill, both consumers, workflow order, branches, and mutation evidence. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| Every existing source path in the plan was verified. The five exact display names exist in frontmatter and are hidden leaves: `Auditor - Code`, `Auditor - Infra`, `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree`. `04-phase-execute.agent.md` already has the `agent` tool needed to spawn them. | AC1 is grounded in the live corpus; no new agent or tool grant is required. | Append the five exact display names to the existing roster without removing current entries and never add the `Audit - Delta` orchestrator. |
| The finalized audit-comparison skill does not exist at expansion time. Feature 08 intentionally leaves its directory/frontmatter slug `[PROPOSED - name TBD: audit-comparison]`. | AC2 and the shared call/return vocabulary cannot be authored safely until the Wave 1 dependency lands. | **Decomposer warning:** enforce the dependency on Feature 08. At implementation time, resolve the exact finalized slug and contract from disk; do not guess or retain the placeholder in production text. |
| The plan's “unusable manifest” continuation clause is ambiguous against existing Step 1. The live orchestrator hard-stops when no unique manifest resolves or any feature bundle is incomplete, while AC20 says existing bundle validation remains intact. The phase dependency notes likewise say Step 1 already guarantees manifest existence but not the quality of `key files modified`. | Treating every manifest failure as a non-blocking bookend skip would regress the existing execution prerequisite and contradict AC20. | **Decomposer warning:** constrain AC4/AC18 continuation to bookend-scope unusability after the existing manifest and bundle validation succeeds, such as an unusable `key files modified` set. Preserve current hard-stops for missing/ambiguous manifests and incomplete bundles. |
| `tests/test_unity_consumer_contract.py` directly parses the same agent and asserts the existing `### Step 2.5: Wave Test Gate` and `### Step 3: Visual Verification Gate (conditional)` sections, including exact retry, evidence-status, and `all-approved: no` obligations. It is omitted from the plan's Fixtures and Test Impact list. | A broad rewrite or heading change can break an existing focused consumer contract even though Feature 11 owns new bookend guards. | **Decomposer warning:** add this unchanged module to regression verification and preserve the asserted sections. Do not edit the test in this feature. |
| The repository uses flat `tests/test_*.py` modules. No `Tests/Editor/Phase*/`, `tests/phase*/`, or equivalent phase-scoped directory exists. Feature 11 already proposes one consolidated flat Phase 03 module and correctly marks its filename `[PROPOSED - name TBD]`; no exact test class or method names are invented by this plan. | No current-phase consolidated verification artifact is omitted from the decomposition. | Keep all new automated bookend coverage in Feature 11 and use scenario descriptions here until its implementer selects the final filename and test symbols. |
| The live full suite on 2026-08-11 collected 268 tests and reported 256 passed and 15 failed/subfailed. Failures are pre-existing: one PR Review display-name collision, three generated-count subfailures, one stale `applyTo` target, and ten missing Unity workflow-reference-asset checks. | Regression success means this feature introduces no additional failures; it does not mean the repository reaches green before unrelated debt and maintainer propagation are resolved. | Record focused evidence separately, compare the full run against this exact baseline, and do not remediate baseline failures in this feature. |
| `dev/feature/PHASE_03-execution-manifest.md` was not present during expansion. This is expected while the Decomposer is still building companion files, but Phase Execute cannot run without the final manifest. | Scope-resolution behavior can be planned from the phase and live agent, but not exercised against the final Phase 03 manifest yet. | The Decomposer must generate and validate the phase manifest after all bundles are complete, including `key files modified` and `## Verification Assets`. |

## Architectural Decisions

- Keep `04-phase-execute.agent.md` thin: Step 1 owns cheap scope resolution, audit-type classification, the single user decision, and recorded branch state; the inserted end step supplies caller-specific inputs, invokes the shared comparison contract, applies the bounded remediation policy, and records returned evidence.
- Load the exact skill slug finalized by Feature 08. The shared skill owns output-root resolution, ref materialization, audit-matrix execution, full-report delta gating, attribution batching and arithmetic, and cleanup ordering; Phase Execute must not copy those mechanics.
- Reuse `<phase-baseline>` already resolved for Step 5 and the current working checkout as the newer side. Use short-SHA snapshot labels and keep every report, delta, queue, and addendum under the working checkout's `dev/[audit-name]/`; never write into the baseline worktree.
- Resolve scope from every valid manifest `key files modified` path plus exactly one uncapped reference-search hop: path-name references, module imports, and uses of names defined by a modified file. Source is all of `source_of_truth/` and `tests/`; standalone documentation is excluded.
- Use the Step 1 file count, selected audit types, and explicit scoped/full/declined choice as the cost boundary. Never infer a full audit from a large scope and never ask again after Step 1.
- Run Code for every accepted bookend and Infra if and only if manifest paths touch CI, Docker, IaC, or build configuration. Keep each type's reports, delta, queue, attribution, and counts independent.
- Render both sides from one prompt template. Only target root, snapshot label, and output directory may vary; scope, intent, “intent never excuses a finding,” documentation exclusion, Infra override, and the test-file Categories 2/5/8/9 constraint remain byte-identical.
- Follow the existing `all-approved` pattern: declined or missing bookend evidence is recorded, forces `no`, and still reaches Step 6. Preserve the pre-existing manifest/bundle hard-stop before this bookend-specific continuation policy applies.
- Auto-remediate at most once and only on the working checkout for High/Critical findings settled as phase-caused. Use the existing Steps 2.5/3 prose re-spawn shape; do not introduce another feature-plan loop.
- Verify only remediation-touched files, append results to the existing delta as explicitly non-comparable evidence, and never treat the targeted pass as a new comparable snapshot.
- Add no normal-path logs or new persistence scheme. Existing audit artifacts and Phase Execute evidence fields carry scope, decisions, reasons, paths, outcomes, and missing evidence.

## Constraints

- Author only `source_of_truth/agents/04-phase-execute.agent.md`; never edit generated `ports/` or `.github/` outputs and never run `scripts/propagate_master_assets.py`.
- Preserve all existing roster entries, steps, checkpoint messages, wave barriers, test and visual gates, QA flow, diff security scan, final review, reporting, documentation update, and error handling except at the explicit Step 1, post-Step-5, `all-approved`, and Step 6 evidence integration points.
- Preserve the existing hard-stop for missing/ambiguous execution manifests and incomplete three-file bundles.
- Do not invent the Feature 08 skill slug, the inserted step heading/number, machine-readable evidence-field names, exact test filename, test class, or test method names. Resolve upstream names from disk and choose remaining idiomatic names during implementation.
- Keep prompt and agent text terse. Ten or more repeated significant contiguous lines across three or more agents fail the corpus duplicate-block invariant.
- Treat baseline and current trees as read-only during audits. Remediation may modify only the working checkout and only after attribution establishes eligible phase-caused High/Critical findings.
- A partial auditor return, missing stated totals, unreconciled delta, surviving provisional item, attribution count mismatch, worktree failure, scope-unusable state, or declined run is missing evidence and never a pass.
- Cleanup may remove only a worktree created by this bookend and only after every corresponding delta and attribution operation is complete.
- One remediation attempt is the cap. Remaining drift proceeds to Step 6 as explicit evidence; no audit/remediation loop is permitted.
- Do not add security or refactor bookend audits. Existing Step 5 diff security remains separate and unchanged.
- Do not edit tests in this feature. Feature 11 owns new guards; existing tests are unchanged regression inputs.

## Scope Boundaries

- Modify only `source_of_truth/agents/04-phase-execute.agent.md`.
- Do not modify the shared audit-comparison skill, `Audit - Delta`, any auditor leaf, `Baseline Worktree`, `Feature - Implementer`, or their canonical skills; Features 08 and 09 own the shared contract and other consumer.
- Do not modify any existing test or create the proposed Phase 03 guard module; Feature 11 owns consolidated verification.
- Do not audit standalone `docs/`, README-style prose, or equivalent documentation-only files in the bookend.
- Do not expand scope beyond one reference-search hop and do not impose a numeric cap.
- Do not run Infra when the validated manifest does not touch CI, Docker, IaC, or build configuration; do not silently skip it when those paths are touched.
- Do not merge Code and Infra findings or counts and do not produce a cross-type delta.
- Do not label provisional findings as regressions before attribution settles them against both trees.
- Do not remediate Medium/Low findings, pre-existing findings, unverified-origin findings, or anything not attributed to the phase.
- Do not write reports, verification output, or fixes into the baseline worktree.
- Do not replace the full comparable end reports with the targeted post-remediation verification addendum.
- Do not add normal-path application logging or persistent state outside the planned audit artifacts and existing pipeline evidence flow.

## Relationships to Sibling Plans

- `08-audit-comparison-contract` is the hard Wave 1 prerequisite. It chooses the final skill slug and exposes the caller-neutral input/return contract this feature consumes.
- `09-audit-delta-rewire` runs beside this feature in Wave 2 after Feature 08. The two consumers have disjoint source files but must reference the same finalized skill and must not retain copied shared mechanics.
- `11-audit-bookend-guards` runs in Wave 3 after Features 08–10. It creates the consolidated focused test module and validates skill ownership, both consumer references, exact leaf topology, workflow order, branches, prompt constraints, gates, remediation, and mutation non-vacuity.
- The public cross-feature contract from Feature 08 supplies output root, selected audit matrix, roots, snapshot labels, output paths, identical caller-provided prompt content, and continuation inputs; it returns report, delta, attribution, reconciliation, and cleanup state for `all-approved` and Step 6.
- Feature 10 must make its structure testable for Feature 11 without adding a second implementation or verification mechanism.

## Suggested Implementation Order

1. Complete `08-audit-comparison-contract` in Wave 1 and record its final skill slug and caller contract.
2. In Wave 2, resolve that implemented contract from disk, then update Phase Execute frontmatter and Step 1 while preserving existing validation hard-stops.
3. Add the thin post-Step-5 consumer wiring, using the already-resolved phase baseline and one shared prompt template.
4. Add bounded remediation, targeted non-comparable verification, complete `all-approved` state handling, and evidence to both Step 6 prompt branches.
5. Run unchanged focused regressions and the full suite against the recorded baseline; retain runtime prompt/worktree/remediation scenarios for manual QA.
6. Execute `11-audit-bookend-guards` in Wave 3 to add consolidated structural and mutation evidence over the finalized skill and both consumers.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill corpus with Python 3.12.6 standard-library maintenance tooling; pytest 9.1.1 and pytest-cov 7.1.0; no Unity project under the canonical predicate |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 268 collected: 256 passed, 15 failed/subfailed — captured 2026-08-11; all failures are pre-existing and summarized in Discovery Delta |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- From `docs/learnings/project-learnings.md`: before authoring a new shared contract, check whether an existing skill already owns it. Here, `auditor-conventions` owns comparability and `audit-delta-report` owns document rules; the new comparison skill and Phase Execute consumer must cite rather than duplicate them.
- From `docs/learnings/project-learnings.md`: prefer extracting the existing sequence over composing a fresh one. Feature 08 moves the load-bearing Phase 3–6b mechanics, and this feature consumes that finalized contract without paraphrasing a parallel procedure.
- From `docs/learnings/project-learnings.md`: separate mechanism from conversation. The shared skill is caller-neutral; Phase Execute owns its one up-front scoped/full/declined question and unattended continuation policy.
- From `docs/learnings/project-learnings.md`: ten or more repeated significant contiguous lines across three or more agent files fail `tests/test_agent_corpus_invariants.py`. Keep shared rules in skills and the consumer wiring brief.
- From `docs/learnings/project-learnings.md`: corpus tests are structural by policy. New workflow-content guards belong in Feature 11's focused module with section scoping, non-vacuity, and mutation evidence, not in generic corpus invariants.
