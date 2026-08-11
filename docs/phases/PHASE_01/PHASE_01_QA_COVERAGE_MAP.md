# Phase 01 QA Coverage Map

## Summary

This map covers all 30 acceptance criteria across the four features. Automated content guards cover every criterion's authored contract. Four consolidated manual/environment checks supply evidence that repository text cannot prove: main-Editor concurrency, controlled clean-project import, GitHub Actions semantic validation/current documentation, and a human runbook dry-run. There are no visual acceptance criteria.

| Verification asset | Scope | Latest evidence |
|---|---|---|
| `tests/test_unity_skill_contract.py` | Features 01–02 | Included in the combined 99-pass focused run |
| `tests/test_unity_consumer_contract.py` | Feature 03 | Included in the combined 99-pass focused run |
| `tests/test_unity_reference_assets.py` | Feature 04 | Included in the combined 99-pass focused run |
| Safe full regression suite | Repository | 239 passed, 2 known baseline failures, 1 propagation test deselected, 63 subtests |

## Feature 01 — Unity test execution contract

| AC | Automated evidence | Manual QA | Status / manual reason |
|---|---|---|---|
| AC1 | Skill guard scopes `## Test Execution` and requires `-batchmode`. | No | Covered by focused guards. |
| AC2 | Platform relationship guard requires EditMode `-nographics` and graphics-on PlayMode/visual. | No | Covered by focused guards. |
| AC3 | Command guard preserves no `-quit` with `-runTests` and `-testFilter`. | No | Covered by focused guards. |
| AC4 | Discovery guard requires the deployed Visual Verifier procedure and rejects bare `Unity`. | No | Covered by focused guards. |
| AC5 | Artifact guard requires absolute main-checkout XML and log paths. | No | Covered structurally; check 4 confirms the runtime artifacts. |
| AC6 | Lifecycle guard requires a committed SHA before shadow-worktree execution. | No | Covered by focused guards. |
| AC7 | Worktree guards cover prune/create/reuse/refresh, cleanliness, retained `Library/`, cost, and first import. | Yes — check 4 | Partial: main-Editor-open concurrency and usability remain `not-executed (main Editor-open condition unavailable)`. |
| AC8 | Persistence and manual-teardown guards reject per-run creation and automatic removal. | No | Covered by focused guards and runbook guards. |
| AC9 | Fallback guard requires an agent-run main-checkout retry after licensing/lock failure. | Partial — check 4 | The branch is structurally covered; record the observed Unity Personal outcome if reached. |
| AC10 | Status guard requires no GUI, no silent refusal, and the exact unattended status. | No | Covered by focused guards. |
| AC11 | XML semantics are guarded. | Yes — check 4 | Partial: the earlier closed-Editor result is not concurrency evidence. Required XML/log do not yet exist. |
| AC12 | Non-vacuity plus deletion and semantic-negation mutations exercise AC1–AC10. | No | Covered by the green focused suite. |

## Feature 02 — Headless asset import

| AC | Automated evidence | Manual QA | Status / manual reason |
|---|---|---|---|
| AC1 | Import-command guard binds the resolved editor, execution project, `-batchmode`, `-quit`, and log. | No | Covered by focused guards. |
| AC2 | Serializer-authority guard preserves Unity-authored serialized assets and GUIDs. | No | Covered by focused guards. |
| AC3 | Source-wide contradiction sweep rejects positive human/GUI requirements without broad-negation exemptions. | No | Covered by focused guards. |
| AC4 | Owning-section guards require `Assets/Tests/Editor` in both corrected locations and preserve PlayMode. | No | Covered by focused guards. |
| AC5 | The contract keeps regeneration explicitly conditional on empirical proof. | Yes — check 5 | `not-executed (reference project not clean)`; no Unity launch or external mutation occurred. |
| AC6 | Import, contradiction, and path guards have non-vacuity and mutation-kill coverage. | No | Covered by the green focused suite. |

## Feature 03 — Unity consumer alignment

| AC | Automated evidence | Manual QA | Status / manual reason |
|---|---|---|---|
| AC1 | Phase Execute guard requires the canonical ladder, agent ownership, absolute results, and preserved attestation. | No | Covered by focused guards. |
| AC2 | Status guard keeps `executed-green`, `executed-failing`, and `not-executed` distinct and non-green when required. | No | Covered by focused guards. |
| AC3 | Visual Verifier guard preserves discovery, nested project-version resolution, graphics-on PlayMode, and no `-quit`. | No | Covered by focused guards; no visual AC invokes capture in this phase. |
| AC4 | Unity Reviewer guard separates test execution from conditional serialized-asset import. | No | Covered by focused guards. |
| AC5 | Cross-consumer guard requires canonical pointers and rejects duplicated worktree/discovery algorithms. | No | Covered by focused guards. |
| AC6 | Derived consumer roster and semantic mutations prove all three consumer obligations. | No | Covered by the green focused suite. |

## Feature 04 — Unity test reference assets

| AC | Automated evidence | Manual QA | Status / manual reason |
|---|---|---|---|
| AC1 | Placement and inertness guards require the reference under the skill and outside installed workflow paths. | No | Covered by focused guards. |
| AC2 | Workflow guards cover checkout, separate EditMode/PlayMode runs, always-run uploads, permissions, secret absence, keys, and outputs. | Yes — check 6 | Structurally verified; current-doc reverification and GitHub Actions semantic validation remain environment checks. |
| AC3 | Runbook guards cover TL;DR length, numbering, one-action steps, exact commands, and correct results. | Yes — check 7 | Automated structure passes; the manifest also requires a human line-by-line dry-run. |
| AC4 | Runbook relationship guards cover commit, worktree lifecycle, editor discovery, platform flags, absolute artifacts, fallback, and no GUI/user-run handoff. | Yes — check 7 | Automated structure passes; dry-run checks end-to-end readability and fidelity. |
| AC5 | Runbook guards require manual-only teardown, adjacent target verification, CI scope, and licensing caveat. | No | Covered by focused guards; observed licensing behavior is recorded under Feature 01 check 4. |
| AC6 | Structural and mutation guards cover workflow and runbook obligations. | Partial — check 6 | `actionlint` is unavailable, so GitHub Actions semantic validity remains explicit review evidence rather than a pass. |

## Manual QA roll-up

| Check | Covers | Required evidence | Current state |
|---|---|---|---|
| 4. Main-Editor-open worktree run | F01 AC7, AC9, AC11 | XML/log, counts, failures, GUI absence, mouse availability, Editor usability, licensing outcome | Not executed: required Editor-open condition unavailable; worktree cleanliness must also pass. |
| 5. Controlled `.meta` import | F02 AC5 | Selected tracked fixture, import log, generated GUID, restored original, final clean status | Not executed: reference project not clean. |
| 6. GameCI validation | F04 AC2, AC6 | `actionlint` success plus current official-doc comparison | Not executed: `actionlint` unavailable; implementation-time documentation review exists. |
| 7. Runbook dry-run | F04 AC3, AC4 | Human confirmation of the 14-step command/result flow and teardown warning | Pending consolidated QA sign-off. |

Visual verification is `no visual ACs`. Propagation remains a maintainer action after review and is intentionally excluded from this QA plan.
