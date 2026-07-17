# Feature Context: Propagation Convergence

## Purpose

This feature replaces the current operator-dependent repeated propagation workflow with bounded, verified convergence before any user-global deployment can begin. It retains `propagate_once` as the verified one-pass primitive, adds one reusable orchestration contract `[PROPOSED - name TBD]`, and makes preflight and per-harness outcomes explicit data for downstream destination and reconciliation features.

## Key Files and Modules

| Path | Role in This Feature | Verified State |
|---|---|---|
| `scripts/propagate_master_assets.py` | Existing propagation implementation, CLI, watcher, structured counters, and root-containment conventions; primary implementation surface | `propagate_once`, `watch_loop`, and `main` exist and are verified |
| `tests/test_propagate_master_assets.py` | Existing focused unit and isolated-temp-repository coverage for propagation behavior | Existing tests invoke `propagate_once(repo_root=...)`; graph lookup did not resolve file-level test links, so direct inspection is authoritative |
| `tests/test_retirement_reconciliation.py` | Existing fixed-point and committed-tree regression coverage | `test_propagation_is_idempotent` and `test_committed_tree_is_at_a_propagation_fixed_point` are verified existing tests |
| `tests/test_phase04_runtime_deployment.py` | Proposed consolidated Phase 04 scratch-home and cross-feature integration coverage | `[PROPOSED - name TBD]`; file does not yet exist |
| `.vscode/tasks.json` | Existing one-shot and background watcher entry points that operators may need to restart after propagator changes | Verify whether task text or behavior must change; no modification is assumed by the plan |
| `README.md` | Existing one-shot and watch-mode operator guidance | Feature 5 owns the documentation rewrite; this feature supplies the behavior and restart requirement it must describe |

## Verified Current Behavior

- `propagate_once(verbose=True, repo_root=None)` performs a single repository pass and returns inventory totals plus mutation counters.
- `main` sends `--once` directly to `propagate_once`; `watch_loop` also invokes `propagate_once` directly at startup and after a detected source change.
- `propagate_once` currently reports inventory keys `source_agents` and `hooks_source` alongside change/removal counters. Existing fixed-point tests deliberately treat every other non-zero counter as a mutation so new counters fail closed into convergence checks.
- Existing output safety code validates generated output directories against repository roots and rejects symlinked/escaping paths. New user-global preflight should follow this fail-closed containment pattern.
- Existing regression evidence records that identifier reclassification can require three propagation passes. A valid-looking first pass is therefore not proof of convergence.

## Architectural Decisions

1. **Keep one-pass and orchestration responsibilities separate.** `propagate_once` remains the focused primitive and compatibility boundary. The new public convergence API `[PROPOSED - name TBD]` owns the bounded loop, zero-change verification, and deployment gate.
2. **Centralize mutation classification.** The implementation must define one authoritative distinction between inventory counters and mutation counters. It must not duplicate a fragile list among the CLI, watcher, and tests.
3. **Fail before user-global mutation.** Repository convergence and destination preflight are complete gates. An exception, malformed result, exhausted bound, non-zero verification pass, or failed intended-harness preflight prevents the first user-global write.
4. **Represent partial deployment structurally.** Per-harness success, failure, copy outcome, and reconciliation skip status are returned as structured results rather than inferred from console output.
5. **Preserve successful harness state.** A later harness failure does not roll back a previously verified copy. Destructive reconciliation is suppressed only for the failed harness.
6. **Use a narrow validated bound.** Reject zero, negative, and unreasonably large values. The exact default and maximum remain implementation decisions and must be documented with tests.
7. **Keep normal-path output quiet.** Extend structured results; add no per-pass or per-file normal log unless required to diagnose a failure. Failure reporting may state pass counts and categories but must not expose sensitive paths or inventory contents.

## Contracts and Boundaries

- **Input from Feature 1:** the propagator after interceptor retirement, including its updated result counters and tests.
- **Output for Feature 3:** a convergence-gated orchestration boundary that accepts destination records from the cross-platform destination policy.
- **Output for Feature 4:** a per-harness operation boundary and status model that reconciliation can use to distinguish verified copies from failed harnesses.
- **Output for Features 5 and 6:** one CLI/orchestration entry point that documentation and end-to-end verification can invoke without rebuilding convergence logic.
- **Compatibility contract:** existing direct callers may continue to use `propagate_once` for exactly one repository pass.
- **Non-owned policy:** this feature does not decide platform paths, implement copy/reconciliation, or broaden deployment across users or distributions.

## Constraints and Failure Handling

- Count all repository mutation keys, including removals; inventory totals are not changes.
- Require an immediate zero-change verification pass after the last mutating pass.
- Treat unknown or malformed result entries conservatively and block deployment until they are classified.
- Complete preflight for the entire intended harness set before starting user-global mutation.
- Validate destinations against the active user's home boundary and reject escaping or symlink-diverted paths.
- Do not create missing parents until preflight has established that parent handling is safe.
- A failed harness must retain a diagnostic status and must not enter destructive reconciliation.
- Repeated runs against a converged repository and unchanged scratch home must report no mutations.
- Operators must restart a watcher that predates the propagator change before migration or release verification.

## Relationships to Sibling Plans

| Feature | Relationship |
|---|---|
| `01-interceptor-retirement` | Upstream dependency and shared-file predecessor; this feature must use the post-retirement propagator counters and avoid restoring retired behavior |
| `03-cross-platform-destinations` | Supplies destination records to this feature's orchestration/preflight boundary |
| `04-managed-copy-reconciliation` | Consumes verified per-harness status and must reuse this feature's orchestration gate rather than duplicate convergence |
| `05-deployment-guidance` | Documents the CLI behavior and stale-watcher restart requirement established here |
| `06-runtime-verification` | Exercises the complete convergence, preflight, deployment, and idempotency flow through the same entry point |

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3.12.6; standard-library propagation CLI and pytest test suite |
| Test Runner | `python3 -m pytest tests/test_propagate_master_assets.py tests/test_retirement_reconciliation.py -q` |
| Test Baseline | Runner constrained on 2026-07-16: `python3` reports `No module named pytest`; no pass/fail baseline captured |
| Test Dependencies | `requirements-dev.txt` declares `pytest>=9.0,<10` and `pytest-cov>=7.0,<8` |
| Lint | Not configured in `pyproject.toml` |
| Format | Not configured in `pyproject.toml` |

## Relevant Learnings

- **Validate propagator roots before reads, writes, or enumeration.** `.github/learnings/review-learnings.md` records that a symlinked parent can divert generated files outside the declared root. Preflight must validate resolved destination directories, not only leaf files.
- **Validate deletion roots before enumerating.** `.github/learnings/debugging-learnings.md` records that leaf checks cannot make an orphan sweep safe when the enumeration root escapes. Although Feature 4 owns pruning, this feature's per-harness failure model must ensure failed copy/preflight paths never authorize destructive reconciliation.
- **Generated agent references can require multiple passes.** `.github/learnings/debugging-learnings.md` records that reference-map behavior depends on identifiers present in each generated root. This supports preserving bounded fixed-point verification rather than assuming one pass is sufficient.
- **Interpreter shims can distort subprocess timing.** `.github/learnings/project-learnings.md` recommends using the resolved interpreter for subprocess measurements. This feature has no latency gate, but tests or operator checks should use `sys.executable` when spawning the propagation CLI.

## Unverified Assumptions and Discovery Notes

- The existing result dictionary contains every mutation counter needed for convergence. Implementation must verify and centralize the inventory-versus-mutation classification before relying on it.
- Exact names and shapes for the convergence API, destination record, orchestration result, and per-harness status remain `[PROPOSED - name TBD]`.
- The proposed consolidated `tests/test_phase04_runtime_deployment.py` does not exist yet and may be created by a later integration feature; this feature should add its scenarios there only if that shared test asset has been established.
- The current environment cannot execute pytest until development dependencies are available. This is runner-constrained evidence, not evidence that tests pass or fail.

