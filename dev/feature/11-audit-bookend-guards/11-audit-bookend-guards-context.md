# Feature Context: Audit Bookend Guards

## Key Files

### Files Changed by This Feature

| File / Module | Role | Change Type |
|---|---|---|
| `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` | Focused Phase 03 module containing structural validators, named-obligation failures, non-vacuity assertions, and deletion/semantic-negation cases across the shared skill and both consumers. Select the final concise filename only after the upstream skill and consumer headings are finalized. | Create |

No existing test class name is prescribed by the plan or Phase 03 request. Prefer scenario-style test functions. If implementation introduces a concrete test class name, treat it as `[PROPOSED - name TBD]` until selected in the code.

### Read-Only Reference Files

| File / Module | Role | Change Type |
|---|---|---|
| `source_of_truth/skills/[PROPOSED - name TBD: audit-comparison]/SKILL.md` | Feature 08 output and eventual single owner of the audit-comparison mechanism; its final slug, headings, frontmatter, input contract, and return contract are test inputs, not names to guess. | Read-only reference |
| `source_of_truth/agents/delta-auditor.agent.md` | Interactive `Audit - Delta` consumer. Before Feature 09, Phases 3–6b still contain the mechanism that will move; Phases 1, 2, 7, and 8 establish the retained interaction baseline. | Read-only reference |
| `source_of_truth/agents/04-phase-execute.agent.md` | Unattended Phase Execute consumer. Feature 10 adds the Step 1 decision and post-Step-5 bookend, the five-leaf roster, remediation, and the Step 6 evidence handoff. | Read-only reference |
| `source_of_truth/agents/auditor-code.agent.md` | Existing hidden leaf whose exact display name is `Auditor - Code`. | Read-only reference |
| `source_of_truth/agents/auditor-infra.agent.md` | Existing hidden leaf whose exact display name is `Auditor - Infra`; its Documentation category is overridden only for this bookend run. | Read-only reference |
| `source_of_truth/agents/auditor-delta.agent.md` | Existing hidden leaf whose exact display name is `Auditor - Delta`; this is distinct from the user-facing `Audit - Delta` orchestrator. | Read-only reference |
| `source_of_truth/agents/auditor-attribution.agent.md` | Existing hidden leaf whose exact display name is `Auditor - Attribution`. | Read-only reference |
| `source_of_truth/agents/05a-baseline-worktree.agent.md` | Existing hidden `Baseline Worktree` leaf and cleanup-handshake caller contract. | Read-only reference |
| `source_of_truth/agents/04b-feature-implementer.agent.md` | Existing plan-driven implementer and the read-only reference for the bounded prose re-spawn exception already used by Phase Execute. | Read-only reference |
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Canonical Multi-Target Audits contract: identical prompt text, independent targets, snapshot labels, report layout, one newer-side output root, and Coverage and Limitations reporting. | Read-only reference |
| `source_of_truth/skills/audit-delta-report/SKILL.md` | Canonical full-delta, queue, provisional-attribution, two-tree probe, and attribution write contract. | Read-only reference |
| `source_of_truth/skills/worktree-baseline/SKILL.md` | Canonical worktree lifecycle and cleanup procedure consumed by `Baseline Worktree`. | Read-only reference |
| `source_of_truth/skills/guard-integrity/SKILL.md` | Content-guard standard requiring scoped checks, mutation/semantic-negation proof, named failures, and non-vacuity assertions. | Read-only reference |
| `scripts/propagate_master_assets.py` | Repository parser. Verified existing APIs include `load_source_agents()`, `_parse_frontmatter(...)`, and `_parse_list_value(...)`; import read-only utilities only and never invoke propagation. | Read-only reference |
| `tests/test_phase_refiner_final_check.py` | Existing focused phase-contract pattern: repository-relative paths, small section/normalization helpers, validators returning named obligation sets, parameterized semantic mutations, and explicit scope non-vacuity. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Generic parsed-frontmatter, roster-resolution, skill-frontmatter, `applyTo`, and duplicate-block regression suite. It is intentionally structural rather than keyed to agent prose. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing propagation regression suite, including exact generated-output counts and enumerated instruction-target assertions; run it but do not update it or regenerate outputs in this feature. | Read-only reference |
| `tests/test_pr_review_orchestrator.py` | Existing regression input currently failing because `delta-auditor.agent.md` contains the exact `05 PR - Review` display name in prose. Preserve or improve this baseline; do not add a new failure. | Read-only reference |
| `tests/test_unity_consumer_contract.py` | Existing manifest-listed regression input for unchanged consumer contracts. | Read-only reference |
| `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | Authoritative Phase 03 scope, success criteria, static-test boundary, and required manual QA. | Read-only reference |
| `dev/feature/PHASE_03-execution-manifest.md` | Wave/dependency contract, consolidated verification-asset inventory, regression commands, and manual QA checklist. | Read-only reference |

## Discovery Delta

No contradiction to the feature plan was found. The following findings refine implementation-time discovery and evidence scope.

| Finding | Impact | Action |
|---|---|---|
| The proposed shared-skill directory does not yet exist, and neither consumer has been changed yet. Current `delta-auditor.agent.md` still owns Phases 3–6b; current `04-phase-execute.agent.md` has no audit bookend or five-leaf roster. | A focused test written against proposed paths or headings would hard-code stale assumptions or start red for dependency reasons rather than for Feature 11's own Red step. | Start only after Features 08–10 complete. Resolve the final skill path and final consumer headings from disk, then bind test constants to those verified values. |
| All five Phase Execute leaf names are verified in source frontmatter: `Auditor - Code`, `Auditor - Infra`, `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree`. Each corresponding source agent is `user-invocable: false`; `Audit - Delta` is a separate orchestrator. | AC3 can derive existence and spawnability through the repository loader rather than maintain a duplicate existence roster. | Load the corpus through `propagate_master_assets.load_source_agents()`, assert the Phase Execute roster contains the five exact names, and separately reject delegation to the `Audit - Delta` orchestrator. |
| The repository parser APIs named above exist and the Phase 02 focused test already consumes the same loader and frontmatter parser. | The plan's parsed-topology approach fits the codebase and avoids implementing a second frontmatter parser. | Reuse the verified parser APIs as read-only imports. Assert the loader result is non-empty before topology comparisons. |
| `tests/test_phase_refiner_final_check.py` is the only existing phase-scoped focused test module. It already demonstrates named-obligation validators, whitespace normalization, section extraction, parameterized semantic mutations, and non-vacuity. | No Stage 0 or separate cross-feature phase test file is missing; the proposed Phase 03 module is the consolidated current-phase test asset required by the manifest. | Follow the pattern without copying its exact test names or introducing a test class presented as existing. |
| The current shared-mechanism source contains a lifecycle defect already identified by Feature 08: Phase 4 permits worktree release after the delta even though Phase 6b still needs the baseline tree. | A guard that merely preserves current text would protect the wrong ordering. | Treat Phase 03 AC6 and Feature 08 AC8 as authoritative: require cleanup only after attribution returns, and include an early-cleanup semantic mutation. |
| The phase manifest includes `tests/test_pr_review_orchestrator.py` in the unchanged regression gate, while Feature 11's plan traceability names only corpus, propagation, and full-suite runs. The test currently fails on a display-name collision inside `delta-auditor.agent.md`. | Rewiring that agent can change this pre-existing failure. Omitting the focused regression run could hide an added or incidentally resolved baseline failure. | Add the manifest's exact grouped regression command to Stage 2 and compare failure identities, not only aggregate counts. |
| The repository-wide baseline was rerun on 2026-08-11: 268 collected, 256 passed, 15 failed/subfailed. Failures match the plan: one PR-review name collision, three generated-output count subfailures, one stale `applyTo` target, and ten missing Unity workflow/reference-asset failures. | The suite is intentionally red before Phase 03. A green-only completion rule would misclassify pre-existing failures, while aggregate-only comparison could hide replacement failures. | Require the focused Phase 03 module to be green and require the full suite to add no failure identity beyond this recorded set. Record any resolved baseline item separately. |
| No Ruff, Black, Flake8, or other lint/format configuration exists in this checkout. `pyproject.toml` contains pytest configuration only, and `uv` warns that `requires-python` is absent. | There is no repository-defined lint or format command to run for this tests-only feature. | Record lint and format as not configured; do not add tooling or change `pyproject.toml` in Feature 11. |
| Generic corpus tests are intentionally structural and documented as unsuitable for prose wording. | Adding Phase 03 prose exemptions or wording checks to the generic corpus suite would violate repository policy and couple unrelated tests. | Keep all Phase 03 content guards in the new focused module, bounded to owning sections and backed by mutation/negation proof. |

## Architectural Decisions

- Create one focused Phase 03 pytest module rather than extending the generic corpus invariants. The generic suite owns corpus-wide structure; the focused module owns the phase's semantic workflow contract.
- Reuse `scripts/propagate_master_assets.py` parsing behavior so frontmatter, display names, tools, and subagent rosters are interpreted exactly as the transform interprets them. Do not create an alternate corpus model and do not call propagation.
- Organize validation by contract domain: topology, single ownership, retained Delta interaction, Phase Execute workflow order, prompt contract, report/attribution gates, continuation branches, remediation bounds, and Step 6 handoff. Each validator returns a set of named unmet obligations.
- Bound every prose/content assertion to its owning heading or section and assert that the section exists exactly once before testing its contents. Normalize whitespace before matching load-bearing clauses.
- Test mechanisms and order, not merely choice words. A statement saying a branch exists cannot substitute for a check that its transition, gate, spawn authority, `all-approved: no`, or Step 6 continuation is present.
- Keep the moved mechanics in one shared skill. The consumers may provide inputs, preserve interaction, record caller-specific outcomes, and reference the skill; they must not restate output-root, materialization, delta-gate, attribution-batching, sum-check, or cleanup mechanics.
- Treat `auditor-conventions` as the owner of comparability and `audit-delta-report` as the owner of delta/attribution document shape. Focused guards should verify references and ownership boundaries without cloning those canonical contracts into test data.
- Demonstrate guard integrity with in-memory deletion and semantic-negation mutations. Assert the original text is green, the mutation target exists, the intended named obligation fails, and the restored/original text is green again; do not edit source contracts on disk to run the sweep.
- Preserve the static/manual evidence boundary. Static parsing can enforce a single prompt template and exactly three varying fields, but it cannot prove runtime byte identity, real worktree lifetime, or end-to-end `Audit - Delta` behavioral identity.
- Add no logging, persistent state, fixtures, test-only copies of source assets, or generated outputs. Pytest failure names and named-obligation sets are the observability surface.

## Constraints

- Feature 11 depends on all three upstream features and belongs in Wave 3. Its tests must target their finalized outputs, not proposed placeholders.
- Only the final Phase 03 focused test module is an edit surface. If a guard reveals an upstream contradiction, report it to the owning feature rather than modifying the skill or either consumer here.
- `source_of_truth/` is the source contract. The focused module must not read `ports/` or `.github/` as Phase 03 truth.
- Never run `scripts/propagate_master_assets.py`; propagation is a maintainer-only step. Generated-sync failures may remain until the maintainer propagates.
- Do not add exemptions to corpus sweeps, exact whole-document snapshots, or repository-wide unbounded substring assertions.
- Do not assert runtime byte identity, real worktree survival, or behavioral identity from static source text. Keep those claims in the Phase 03 manual QA checklist.
- The existing red repository baseline is not permission to absorb new failures. Compare named failures/subfailures before and after; the new focused module itself must pass.
- Preserve source-agent frontmatter and existing tests as read-only inputs. Do not change production contracts to make a brittle test pass.
- Use `uv` for Python commands. Do not alter Python packaging, `sys.path` policy, dependencies, or `pyproject.toml` as part of this feature.
- Any new concrete helper, class, or exact test name not copied from the phase/request and not already on disk must be selected during implementation and recorded as `[PROPOSED - name TBD]` until then. Scenario descriptions are preferred in this bundle.

## Scope Boundaries

- Do not implement or edit the audit-comparison skill; Feature 08 owns it.
- Do not rewire `Audit - Delta`; Feature 09 owns it.
- Do not add Phase Execute frontmatter, workflow, remediation, or Step 6 handoff content; Feature 10 owns it.
- Do not edit `tests/test_agent_corpus_invariants.py`, `tests/test_propagate_master_assets.py`, `tests/test_pr_review_orchestrator.py`, or `tests/test_unity_consumer_contract.py` unless a contradiction is returned to and accepted by the owning upstream feature; they are regression evidence here.
- Do not edit generated `ports/` or `.github/`, run propagation, or add tests that treat generated outputs as authoritative.
- Do not create external fixtures. Read finalized repository-relative source files directly.
- Do not test one exact prose rendering where a bounded structural/semantic obligation can be enforced.
- Do not claim static coverage for captured prompt byte equality, real cleanup timing, or live orchestrator behavior. Those remain explicit manual QA.
- Do not add security/refactor bookend types, cross-type deltas, multi-hop scope expansion, baseline remediation, lower-than-High remediation, or repeated remediation loops.
- Preserve the existing Step 1 hard-stops for missing/ambiguous manifests and incomplete bundles, plus the wave loop/gates, Step 5 diff security review, Step 6 final review, and post-review workflow except for assertions over the explicit Phase 03 integration points.

## Relationships to Sibling Plans

- `08-audit-comparison-contract` is the direct contract prerequisite. It creates the finalized skill, corrects cleanup ordering, and defines caller-neutral inputs/returns. Feature 11 verifies its frontmatter, mechanism-only boundary, canonical references, prompt template, gates, attribution arithmetic, and single ownership.
- `09-audit-delta-rewire` depends on Feature 08 and preserves the interactive consumer. Feature 11 verifies its finalized skill reference, retained type/target setup, matrix confirmation, conditional delta/rerun offer, fix-research offer, remediation flow, and absence of copied mechanics.
- `10-phase-execute-audit-bookend` depends on Feature 08 and adds the unattended consumer. Feature 11 verifies the five exact leaves, no orchestrator delegation, Step 1 decision/scope contract, post-Step-5 order, audit/prompt/gate branches, bounded remediation, `all-approved` behavior, and Step 6 evidence handoff.
- Features 09 and 10 may execute in parallel because their edit surfaces are disjoint. Feature 11 must wait for both because its consolidated guards compare the shared skill with both consumers.
- `dev/feature/PHASE_03-execution-manifest.md` is the authoritative wave and verification schedule. Its manual checks close the runtime claims that this static feature intentionally cannot prove.

## Suggested Implementation Order

1. Confirm Features 08–10 are complete and identify the finalized shared-skill slug, skill headings, retained Delta sections, and inserted Phase Execute heading from disk.
2. Capture the unmodified source texts and establish the current focused/regression baseline before authoring validators.
3. Build Stage 1 parsers and named-obligation validators, starting with non-vacuous section extraction and parsed topology before content checks.
4. Add domain validators in dependency order: ownership/interaction, Phase Execute topology/order, prompt and report gates, branches, remediation, then Step 6 continuation.
5. Build Stage 2 deletion and semantic-negation cases against every load-bearing target, with explicit target-exists assertions and named failure expectations.
6. Run the focused module, the manifest's grouped unchanged regressions, and the full repository suite; compare named failures with the captured baseline and confirm no generated source was used.
7. Hand off the runtime-only prompt, worktree, and behavioral-identity checks to the Phase 03 manual QA checklist without claiming them as automated evidence.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3.12.6 executed via `uv`; stdlib-only transform/deploy scripts; pytest 9.1.1 with pluggy 1.6.0 and pytest-cov 7.1.0 present. Repository content is primarily Markdown source contracts. `pyproject.toml` has pytest settings only and does not declare `requires-python`. |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 268 collected; 256 passed; 15 failed/subfailed in 16.60s, captured 2026-08-11. Existing failures: 1 PR-review display-name collision, 3 generated-output count subfailures, 1 stale instruction `applyTo` target, and 10 missing Unity workflow/reference-asset failures. |
| Lint | Not configured |
| Format | Not configured |

The focused Feature 11 command remains `uv run pytest tests/[final Phase 03 focused test filename]` until the proposed filename is finalized. The manifest's grouped unchanged regression command is `uv run pytest tests/test_agent_corpus_invariants.py tests/test_unity_consumer_contract.py tests/test_propagate_master_assets.py tests/test_pr_review_orchestrator.py`.

## Relevant Learnings

- From `docs/learnings/project-learnings.md`: **A block of 10 or more contiguous lines repeated across three or more agent files fails the corpus duplicate-block test.** This reinforces the Phase 03 single-home boundary: moved mechanics belong in the shared skill, not in either consumer.
- From `docs/learnings/project-learnings.md`: **Corpus tests are structural by policy; a check keyed to expected agent prose goes inert when prose is reworded.** Keep semantic Phase 03 content guards in the dedicated focused module, section-scoped and mutation-proven, rather than extending the generic corpus suite.
- From `docs/learnings/project-learnings.md`: **A contract being extracted may already be owned by a participating skill.** `auditor-conventions` already owns multi-target comparability, so tests must reject restatement in the new skill rather than reward duplicate text.
- From `docs/learnings/project-learnings.md`: **Prefer extracting an existing sequence over composing a fresh one, and separate mechanism from conversation first.** The guards must preserve the load-bearing Phase 3–6b mechanics while proving all interactive confirmations remain only in `Audit - Delta`.
- From `docs/learnings/cross-phase-decisions.md`: **A structural guard can prove a prohibition is present but cannot prove it is obeyed at runtime.** Apply the same Phase 02 blindness lesson here: static prompt-template checks are necessary, while real prompt equality and worktree lifetime remain manual QA.
