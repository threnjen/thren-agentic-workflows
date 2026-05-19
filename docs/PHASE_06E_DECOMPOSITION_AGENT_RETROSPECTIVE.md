# Phase 06e Decomposition Agent Retrospective

**Subject repo:** `/Users/jennywadkins/github_repos/the-movies-02`  
**Original planning branch:** `phase/06e`  
**As-built planning branch:** `phase/06e-goldenpath`  
**Compared scope:** `dev/feature/` plus `docs/phases/PHASE_06E/`  
**Written:** 2026-05-19

## Executive Summary

The major issue was not that Phase 06e lacked refinement. The phase documents on `phase/06e` already contained most of the hard edge cases: non-amenity filtering at both call sites, `ExposeComps()` load ordering, additive Purpose backfill, zero-decay optimization, fixed-attribute UI behavior, and cross-phase Ambition tier contracts.

The failure was mostly in the Feature Decomposer / Plan Expander handoff. The original `dev/feature` docs translated a good phase document into plausible but not fully grounded implementation plans. Several details drifted from the phase text or the codebase: helper names changed, XML field names were guessed, UI files were missed, and logging/testing expectations were invented. The as-built branch shows the feature decomposition docs that should have existed after a tighter fidelity and code-symbol verification pass.

There is a smaller Phase Refiner contribution: the phase doc sometimes crossed into implementation-level prescriptions, especially UI tooltip mechanics, without proving that the existing UI Toolkit test environment could support the native tooltip path. But this was secondary. The Feature Decomposer is explicitly responsible for discovery, file-scope mapping, dependency analysis, and execution-ready plans, so most preventable gaps belong there.

## Evidence From The Branch Diff

`phase/06e..phase/06e-goldenpath` changed 27 files in the planning/doc surface reviewed here:

- 25 files under `dev/feature/`
- 2 new consolidated QA docs under `docs/phases/PHASE_06E/`
- 1,254 insertions and 1,744 deletions in those planning/doc files

The phase summary and discovery context were effectively stable inputs. The meaningful delta was the feature bundle rewrite from speculative implementation plans into as-built plans, tasks, context, implementation records, and actual evidence.

## What The Original Decomposition Got Right

The Feature Decomposer selected the right six feature boundaries:

1. Ambition data and generator behavior
2. Purpose data and start values
3. Ambition/Purpose runtime behavior
4. Non-amenity need guard
5. UI integration
6. Comp save/load backfill

It also captured the important high-level execution order. Feature 06 correctly depended on Features 01-05, and the shared `CompTalentNeeds.cs` conflict between runtime behavior and amenity filtering was recognized.

That means the decomposition topology was basically right. The quality loss happened inside the feature bundles.

## Key Differences And Likely Root Causes

### 1. Phase-Doc Fidelity Drift

The clearest example is Feature 02. The phase docs called for a shared start-value helper and the goldenpath/as-built code used `NeedDef.StartValueFor()`. The original feature docs repeatedly specified `NeedDef.ComputeStartValue()`.

That is not an implementation discovery failure. It is a translation failure: the Decomposer took a requirement from the phase doc and renamed it while creating the plan. The same pattern appears in field terminology like `moodOffset` versus the actual `moodModifier` XML field.

**Root cause:** The Feature Decomposer lacks a required fidelity pass that maps each phase-level requirement to the exact plan text and flags renamed APIs, XML fields, and symbols.

### 2. Code-Symbol Verification Was Too Weak

The original docs included concrete method names, field names, file names, and test file guesses. Some were correct, but several were unverified guesses:

- `ComputeStartValue()` instead of `StartValueFor()`
- Purpose thought `moodOffset` instead of the actual authoring field
- UI tooltip implementation described as native `VisualElement.tooltip` only
- Feature 06 suggested `DefLog.Message` backfill logs that did not ship

These are the kind of facts a Decomposer or Plan Expander can verify before writing execution-ready tasks. Once a plan names a symbol, that symbol should either be found in the codebase, quoted from the phase doc, or explicitly marked as proposed.

**Root cause:** The Decomposer is allowed to write concrete implementation details without a symbol/file existence checklist.

### 3. File-Scope Mapping Missed UI Assets And Test Helpers

Feature 05 originally scoped the work mostly to controllers:

- `PawnInspectPanelController.cs`
- `TalentHiringPoolPanelController.cs`
- `TalentMatrixSection.cs`

The as-built branch also needed:

- `InspectPanel.uxml`
- `inspect-panel.uss`
- `InspectPanelTestRootBuilder.cs`

This is exactly the kind of miss that creates downstream churn. UI Toolkit work often spans controller code, UXML hierarchy, USS classes, and test root builders. The source-of-truth repo already contains UI Toolkit guidance about keeping UXML changes synchronized with helper trees, but the decomposition process did not force that pattern into file-scope discovery.

**Root cause:** File-scope mapping is too source-code-centric. It needs framework-specific companion-file discovery.

### 4. The Plan Template Encouraged Speculative Logging

Feature 06 originally proposed `DefLog.Message` calls for Ambition and Purpose backfills. The as-built docs removed that. For this project, extra normal-path logs are risky because tests may assert exact log behavior and because load/backfill paths should not create noisy success logs unless the phase explicitly asks for them.

The `feature-plan-set` template requires an observability/operability section, which is good, but it can nudge agents into inventing logs. In a Unity single-player simulation, "no new logging" is often the correct answer.

**Root cause:** The template asks for observability, but the agent instructions do not say that "no new logging" is a valid and often preferred observability decision.

### 5. Test Plans Were Aspirational Rather Than Executable

The original plans listed many intended tests by pattern name. The as-built branch records the actual Phase 06e tests that shipped, especially the consolidated `Phase06eFeatureTests.cs` coverage. The original decomposition did not sufficiently distinguish between:

- required behavioral coverage,
- suggested test names,
- branch-diff/code-review evidence,
- tests that need real Unity infrastructure,
- tests that are too brittle for headless EditMode.

**Root cause:** The Decomposer generated test plans from requirements, but did not add enough execution realism from the current Unity test harness and existing helper structure.

## Feature Decomposer Versus Phase Refiner Fault

### Mostly Feature Decomposer / Plan Expander

The Decomposer owns execution-ready feature bundles. Its own source-of-truth definition says it must read the codebase, map source files conservatively, identify dependencies, and write plans the executor can consume as-is. On those criteria, the misses above are mostly Decomposer-side.

Specific Decomposer-owned misses:

- Renaming or inventing concrete symbols instead of preserving or verifying phase-doc terms.
- Omitting UI companion files and test root helpers from file scope.
- Turning phase requirements into over-specific task details without code verification.
- Inventing normal-path logging in a sensitive load/backfill flow.
- Treating planned test names as if they were equally reliable as existing tests or verified harness paths.

The Plan Expander shares some responsibility because it is the subagent that should verify referenced files exist and identify additional relevant files during codebase scanning. In practice, it should have caught UI asset/test-helper companions and stale symbol names in `-context.md` and `-tasks.md`.

### Smaller Phase Refiner Contribution

The Phase Refiner did strong work overall. The Phase 06e summary and discovery context contained the right edge cases, and the notes for Feature Decomposer were unusually actionable.

The weaker area was that the phase doc sometimes specified implementation mechanics that were not fully proven at the phase level. The UI tooltip note is the best example: it described native `VisualElement.tooltip`, while the shipped solution needed a custom inspect-panel overlay with UXML/USS/test-helper support. Since Phase Refiner is explicitly told not to cross into code-level planning, it should either avoid exact UI implementation mechanics or mark them as "verify against current UI Toolkit/test-helper pattern during decomposition."

So the Phase Refiner should improve its handoff language for implementation-sensitive details, but the Decomposer still had the responsibility to verify those details before producing executable feature docs.

## Recommendations

### 1. Add A Phase-To-Feature Fidelity Gate

Before writing plans, the Feature Decomposer should create an internal traceability table:

| Phase requirement | Feature | Preserved wording/API? | If changed, why? |
|---|---|---|---|

Rules:

- Do not rename APIs, fields, XML elements, or file paths from the phase doc unless codebase discovery proves a better name.
- If a requirement is intentionally moved between features, document the move.
- If a phase requirement is not implemented by any feature, mark it as deferred with rationale.

This would have caught `StartValueFor()` becoming `ComputeStartValue()`.

### 2. Require Symbol And File Verification For Concrete Plans

Any plan that names a concrete file, method, class, XML field, USS class, UXML element, test helper, or log API should satisfy one of these conditions:

- Existing symbol/file verified in codebase.
- New symbol/file explicitly labeled as proposed.
- Exact name copied from phase doc and preserved.

Add a checklist item to the Feature Decomposer quality gate:

> Every concrete symbol in the plan is either verified existing, explicitly proposed, or copied exactly from the phase document.

This would have caught `moodOffset`, speculative test file names, and invented logging expectations.

### 3. Make File-Scope Mapping Framework-Aware

Extend the Decomposer and Plan Expander instructions with companion-file discovery rules:

- Unity UI Toolkit controller changes require scanning for related `.uxml`, `.uss`, `UIDocument`, and test root builders.
- Save/load changes require scanning serializer, factory, loader, fixture, and legacy compatibility tests.
- XML def changes require scanning def classes, production XML, serializers, exact-count tests, and data type tests.

This would have pushed Feature 05 to include `InspectPanel.uxml`, `inspect-panel.uss`, and `InspectPanelTestRootBuilder.cs` from the start.

### 4. Treat Observability As "Decide", Not "Add Logs"

Adjust the Feature Plan Set template guidance:

> Observability does not imply new logging. For local simulation, save/load, hot-loop, and test-sensitive paths, "no new normal-path logs" is often the correct operability decision. Add logs only when required by the phase, an existing pattern, or a diagnosable failure mode.

This would have prevented the Feature 06 `DefLog.Message` suggestion.

### 5. Split Planned Tests Into Evidence Categories

Feature plans should distinguish:

- Must-have automated tests
- Existing tests to update
- Tests that require Unity Test Runner / PlayMode / EditMode constraints
- Code-review evidence only
- Manual QA checks

The as-built docs are better because they name actual evidence. Initial decomposition docs cannot know final test names, but they can avoid presenting speculative names as if they are authoritative.

### 6. Add A "Discovery Delta" Pass For Plan Expander

The Plan Expander should not only expand the Decomposer plan. It should actively report discoveries that contradict or refine the plan:

- Missing referenced files
- Better existing API names
- Additional required companion files
- Existing tests asserting exact strings/counts
- Framework constraints that make a planned approach brittle

If it finds contradictions, it should write them into `-context.md` and return a warning to the Decomposer instead of silently generating tasks.

### 7. Improve Phase Refiner Handoff Language

When the Phase Refiner includes implementation-sensitive guidance, use language like:

> Suggested implementation shape, to be verified by Feature Decomposer against current code and tests.

For Phase 06e-style UI notes, the Refiner should say:

> Tooltip behavior must be verified against the existing UI Toolkit panel structure and test helpers; native tooltip support may not be sufficient in headless tests.

This keeps Phase Refiner at the capability/behavior level while still warning Decomposer where to look.

## Suggested Agent Definition Changes

### Feature Decomposer

Add these requirements to Phase 2b or the Quality Checklist:

- Perform a phase-to-feature fidelity pass before writing plans.
- Verify every concrete symbol/file reference or label it as proposed.
- For each feature, identify framework companion files, not just primary source files.
- Do not invent logging for normal-path behavior; justify any new log line.
- Include an "Unverified Assumptions" section when a plan depends on behavior not confirmed in code.

### Feature Plan Expander

Add these requirements to Step 2:

- Treat the plan as a draft to validate, not only an input to expand.
- Report contradictions between the plan and codebase to the invoking Decomposer.
- Add companion files discovered during scan to context and tasks.
- Distinguish planned test names from existing tests and required new tests.

### Phase Refiner

Add this handoff rule:

- If a phase doc names an implementation mechanism rather than a behavior, mark it as a suggested shape and instruct Decomposer to verify it during code-level planning.

## Bottom Line

Phase 06e is not evidence that the Phase Refiner failed. It is mostly evidence that the Feature Decomposer needs a stronger grounding loop between the refined phase document, the actual codebase, and the generated execution bundle.

The Decomposer got the feature boundaries right, but it needed one more disciplined pass: preserve the phase doc exactly where it is specific, verify every concrete symbol before tasking an implementer, and let framework companion files enter the scope before execution begins.
