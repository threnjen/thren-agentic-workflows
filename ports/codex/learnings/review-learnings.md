<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Review Learnings

## Pattern

When adding checkpoint-commit instructions to rerunnable authoring flows, stage every artifact mutated by that step and describe resumable scopes as created *or modified*, not created only. Keep the checkpoint contract at the same scope as the artifacts it commits — do not promise per-unit checkpoint commits against consolidated outputs.

## Impact

Overly narrow staging leaves setup files dirty after the checkpoint or drops edits from resumed runs, so later commits inherit unrelated changes. Mixed scopes create impossible staging instructions and make it impossible to map a checkpoint back to the unit named in its commit message.

## Watch for

Checkpoint text that stages only output directories while earlier steps also edit repo metadata; per-unit checkpoint language next to one consolidated writer invocation; checkpoints that refer to files "created in this session" when the workflow can rerun against existing files.

## Pattern

When agent inventory, counts, frontmatter schemas, or platform-contract rules change, update every summary surface in the same change — not just the primary catalog tables.

## Impact

Stale overview bullets, comparison tables, and architecture diagrams contradict the actual inventory or keep advertising removed keys, misleading both humans and downstream agents that bootstrap from those summaries.

## Watch for

Top-level README intros, Mermaid labels, CODEBASE_CONTEXT count summaries, platform comparison tables, frontmatter field summaries, and any touched docs that summarize agent lists, counts, or file schemas at a glance.

## Pattern

When a porting guide scopes an agent source directory using a filename glob (e.g., `*.agent.md`), verify whether the directory contains agent definitions that do not match that extension — some are plain `.md`, distinguishable from documentation only by frontmatter.

## Impact

A guide that gates on extension alone silently excludes valid agent definitions from the porting scope, causing missed migrations invisible to reviewers who only scan for the expected extension.

## Watch for

Porting guides that describe a source surface as a single glob, source directories mixing agent definitions and documentation under one parent, and any example or table that cites a single naming pattern as exhaustive.

## Pattern

In documentation guides that embed shell verification blocks for future-facing placeholder paths, bare `test -e` calls exit non-zero with no output, giving no indication whether failure means "not ready yet" or "misconfigured."

## Impact

Users copy-paste the block, see no output, and cannot distinguish "source artifact doesn't exist yet" from "path is wrong — fix now."

## Watch for

Preflight blocks with bare `test -e "$PATH"` lines on documented placeholder paths; fix by adding `|| echo "not yet: <path>"` or a comment explaining expected failure.

## Pattern

When an AC specifies a Terraform backend `key` using variable interpolation, the implementation must use a partial backend config — the key is omitted from `backend.tf` and supplied via `-backend-config="key=..."` at init time. Terraform does not support variable interpolation in backend blocks.

## Impact

A reviewer comparing the AC literal text against the backend file will flag the missing key as a bug — a false positive. The plan's correctness section resolves this; check it before raising the issue.

## Watch for

`backend.tf` files that omit `key` combined with AC text describing a parameterized key path.

## Pattern

Scaffold placeholder comments (e.g., "Output blocks are added in a later feature when resources are defined") are never updated when the implementing feature lands.

## Impact

Stale files carry misleading comments after resources exist, and useful reference outputs (resource ARNs, IDs) are silently omitted.

## Watch for

Placeholder-style comments that name a specific future feature; check whether it has already landed and what is worth exporting.

## Pattern

When a public value type can be constructed directly as well as through a validating factory, validate it again at every security-sensitive emission or execution boundary.

## Impact

Callers can bypass factory validation by invoking the constructor directly, allowing invalid actions to reach an external runner and turning a fail-closed path into an ambiguous or non-blocking result.

## Watch for

Exported `NamedTuple`, dataclass, or plain-object decision types paired with a validating factory, followed by emitters or guards that check only the instance type.

## Pattern

Fail-open observability requirements must cover the executable wrapper as well as exceptions handled inside the implementation language.

## Impact

An interpreter startup or shell-pipeline failure can return non-zero before application-level exception handling runs, causing an audit-only hook to block its caller.

## Watch for

Audit wrappers using `set -e` or `pipefail` without an explicit non-blocking fallback, and tests that invoke only the language entrypoint rather than the actual shell wrapper.

## Pattern

Security matchers that compare one glob pattern with another must vary wildcard replacements independently and treat the protected directory root as part of a recursive directory rule.

## Impact

Single-sample glob heuristics miss overlapping scopes, and a recursive rule like `protected/**` can accidentally allow the `protected` directory itself.

## Watch for

Glob-overlap helpers that substitute the same value for every `*`, recursive path rules tested only with descendant files, and missing controls proving ordinary source globs remain allowed.

## Pattern

When removing an exact encoded suffix from parsed shell tokens, use exact suffix removal rather than `rstrip` with the suffix characters.

## Impact

`rstrip("\\n")` removes any trailing backslash or letter `n`, corrupting ordinary filenames such as `auth.json` before security policy evaluation and creating deterministic bypasses.

## Watch for

`rstrip`/`lstrip` calls whose argument is intended as a whole delimiter; cover nearby filenames ending in each delimiter character.

## Pattern

Artifact propagators must validate resolved source assets and resolved destination directories against their declared roots before reading or writing; replacing only a symlinked leaf file is not sufficient.

## Impact

A symlinked parent directory can redirect generated files outside the consumer root, while a normalized `../` token or source symlink can reference content the deployable unit never copied.

## Watch for

Copy loops writing beneath unchecked parent directories, validators that test path prefixes before normalization, source walks that follow symlinks without a resolved-root check, and tests covering only leaf symlink replacement.

## Pattern

When selectively unignoring a nested fixture tree beneath a broad parent ignore rule, re-ignore sibling paths between the parent exception and the fixture exception.

## Impact

Negating only the parent directory can make unrelated future artifacts trackable, weakening the intended scope of the exception.

## Watch for

Ignore files with a broad `parent/*` rule followed immediately by `!parent/child/` without a rule restoring the boundary.

## Pattern

When a procedural document defines conditional resource lifecycle behavior, make each create, reuse, recreate, and refusal branch executable in sequence.

## Impact

A policy described only in prose can be followed literally as an unconditional create or cleanup, causing collisions or deleting resources that should have been retained.

## Watch for

Steps that state a collision policy and then show one unconditional command, especially when ownership determines whether cleanup is safe.

## Pattern

Orchestrators must validate both child report artifacts and the terminal synthesis result before accepting a readiness verdict.

## Impact

A child can return success with a missing or empty report, or the terminal synthesizer can fail, allowing incomplete coverage to be mistaken for a clean run.

## Watch for

Delegation contracts that record only explicit exceptions, trust returned report paths without metadata validation, or pass a synthesizer verdict onward without an independent missing-check gate.

## Pattern

Diff-scoped static analyzers must require verifiable line or range attribution before treating repo-wide results as introduced changes.

## Impact

Filtering a repo-wide result only by touched file can misclassify pre-existing findings as changes from the current branch.

## Watch for

Analyzers that fall back from added-line matching to file membership, accept missing source locations, or report findings when baseline attribution cannot be established.

## Pattern

Read-only dependency vulnerability checks must use supplied local evidence or an explicitly offline audit mode.

## Impact

A generic audit command can fetch or update vulnerability data, violating the no-network boundary and making the evidence path non-reproducible.

## Watch for

Instructions that call an audit command without stating offline behavior, commands with implicit network access, or missing-evidence paths that claim a clean result.

## Pattern

Delegating or read-only wrapper agents should receive only the capabilities needed for input collection, child delegation, and report writing; generated harness outputs should be checked against the source renderer.

## Impact

Unneeded shell or execution permissions weaken prompt-level read-only boundaries, while untested generated mirrors can silently lose delegation or safety constraints in one platform.

## Watch for

Wrapper frontmatter granting execute without a local execution requirement, platform-specific permission mappings, and propagation tests that verify only unrelated assets instead of the new agent outputs.

## Pattern

When a delegated evaluator fails after dispatch, record both the concrete NOT RUN reason and an explicit NO-GO or below-GO readiness ceiling.

## Impact

A not-run marker without a visible readiness ceiling can be mistaken for neutral coverage, allowing an incomplete review to advance as if the evaluator had passed.

## Watch for

Status rows with `status: not-run` and `report: null` but no reader-visible verdict ceiling, especially when a child report is required for release readiness.

## Pattern

Parallel verifier fan-outs must assign deterministic, child-derived report paths.

## Impact

If concurrent children are told only to write into a shared directory, generic filenames can overwrite sibling evidence and make parent row-cardinality checks unreliable.

## Watch for

Delegation prompts naming a shared output directory without a unique filename template, or a parent check that does not map each child identifier to exactly one report artifact.

## Pattern

Propagation regression tests must cover every newly added agent output — including non-delegating agents — and compare each harness render with the source renderer.

## Impact

Hard-coded evaluator subsets or orchestrator-only smoke checks can pass while a new Claude, OpenCode, or Codex mirror is stale or malformed.

## Watch for

Expected-slug tuples that omit newly added agents, tests named for one agent family that silently exclude siblings, or generated outputs checked only for existence rather than exact renderer parity.

## Pattern

Read-only history-mining agents must keep evidence-access instructions consistent with their declared capabilities and explicitly handle unavailable sources.

## Impact

A fetch-only agent that includes shell examples can violate its no-execute boundary, while a remote-only capability can be mistaken for guaranteed local history recovery.

## Watch for

Command examples in fetch-only contracts, missing unavailable-source handling, or mirror tests that inspect only one harness's permission boundary.

## Pattern

A marker-based guard that decides whether a generated file may be deleted must key on the exact position the emitter writes the marker to — never on the marker appearing anywhere in the file, and never on a prefix check that ignores frontmatter. Extract that position into one helper shared by the writer and the guard.

## Impact

Both looser rules fail, in opposite directions: a prefix check against frontmatter-bearing output matches nothing and silently disables the sweep; a whole-file search matches any hand-maintained document that merely quotes the marker, deleting exactly the file the guard exists to protect.

## Watch for

`startswith(MARKER)` applied to frontmatter-bearing output; `MARKER in text` as a deletion predicate; a guard tested only for what it deletes and never for what it must refuse to delete; convention docs living inside a generated root.

## Pattern

A destructive helper is proven only by tests that bracket it from both directions: one that fails if the guard is removed, and one that fails if the guard is tightened until it matches nothing.

## Impact

A single-sided suite lets a guard pass for the wrong reason — an inert guard trivially satisfies "deletes zero files on a clean tree" while gating nothing. Mutation-test the guard rather than asserting it.

## Watch for

Inert-run criteria with no companion test proving the pruner positively identifies real generated output; deletion counters asserted only as zero.

## Pattern

A deliberately-failing tripwire guarding a time-boxed exemption must be addressed to the pass that will actually trip it, not the pass nominally assigned the cleanup. Read what the downstream work does to the exempted paths — if it renames or moves them, the exemption stops matching and the tripwire fires there.

## Impact

A tripwire addressed to a later pass than the one that trips it converts a clean hand-off into a red baseline for every pass in between, training implementers to ignore red. The tripwire is usually right; only its addressee is wrong.

## Watch for

Inverted assertions (`assert still_offending`) whose failure message names an owner; any exemption list keyed on a path a downstream rename will invalidate.

## Pattern

When an exemption list, a skip, or a non-goal is justified by a factual claim about the tree ("this directory does not exist", "this path has no live wiring"), verify the claim against the tree before accepting it. Do not accept the rationale on its own authority.

## Impact

An over-broad exemption resting on a false premise hides the very references the sweep exists to find. Worse, a non-goal justified by "already absent" leaves work *unowned* rather than *deferred* — deferred work has an inheritor; dismissed-as-nonexistent work has none.

## Watch for

Non-goals justified by an assertion of absence rather than a decision to defer; exemption scopes broader than the rationale that justifies them; rationales phrased as sweeping claims about a directory's contents. Narrowing an exemption is cheap when the sweep still passes — and the passing sweep proves the narrowing was safe.

## Pattern

Deleting an orchestrator can rename a user-facing entry point it never owned. Where a generated artifact's name depends on whether some *other* asset references it, removing the last referrer reclassifies it and changes its public name.

## Watch for

Emission rules conditioned on a reference map; identifier resolution that reads on-disk state rather than deriving from source — such changes converge only across multiple generator runs. Run the generator until every counter reads zero before trusting the tree; treat "one run, looks right" as unverified.

---

## Pattern

An evidence-shaped claim is not evidence. Implementation records cite "mutation-tested", "stable across N runs", or a named counter as proof; these carry the *form* of verification but fail re-execution often enough that a reviewer who accepts them is not reviewing. Re-run every cited proof against a clean tree at the reviewed commit. A record's claim is a hypothesis about the tree, not a description of it.

## Impact

Defects reach commits behind such claims: suites reported green that were red, and correct actions defended by mutation tests that pass identically with and without the change they supposedly prove. The right action on false evidence still validates the wrong reasoning.

## Watch for

Passing-suite claims where the arithmetic reconciles to *collected* rather than *passed*. Mutation tests where the mutation would trip an unrelated guard anyway — verify the test fails for the stated reason and *passes* once the change under test is reverted, or it proves nothing. Ask what an exemption matched *at the moment it was deleted*, not what it matched when written.

---

## Pattern

When a sweep test goes red because a new file legitimately contains the swept token, the one-line fix — add the file to the exemption list — is almost always wrong. It widens the hole the sweep exists to close. Remove the token instead: import the canonical definition and derive the values.

## Impact

Exemption lists grow monotonically and are never audited. Each entry is a permanent blind spot bought to make one test green.

## Watch for

A guard module declaring its names are defined "once, here" while another module re-lists them as literals — the duplication is the defect, and the sweep failure is the symptom correctly reporting it. When replacing literals with a derived tuple, add a vacuity assert (`assert derived_list`), or an empty upstream list silently neuters the guard.

---

## Pattern

Prose contract guards are inert by default, in several recurring ways that all share one test: **before trusting any prose assertion, establish that it can fail independently, for the right reason, and that it is owned by the change it claims to cover.**

1. **Multi-occurrence literals.** An assertion that a literal is present somewhere in a whole document is inert wherever the literal occurs more than once — deleting the occurrence the test protects leaves a stray occurrence elsewhere. A token appearing many times (a delegating agent's word for delegation) makes the assertion unconditionally true. Anchor on the full sentence with its objects attached, or on a claim verified to occur exactly once, and scope assertions to the section or list item that carries the obligation rather than the flattened document.
2. **Line-wrap sensitivity.** A regex spanning words that a reflow moves onto separate lines stops matching content that is still present. Normalize whitespace runs to single spaces before asserting on sentences; reserve raw-text assertions for literal tokens and frontmatter, where line structure is part of the contract.
3. **Wrong ownership.** When a feature adds a new path to a file that already states the contract in general terms, a guard on the new path can be satisfied entirely by the pre-existing general statement — the assertion pins exactly one occurrence, but the wrong one. For each guard, check which feature introduced the pinned line; if it predates the diff under review, the new path needs its own pin. Relatedly, guards that all assert the *choice* a contract captures while none assert the *mechanism* leave the command, call, or write that does the work deletable with the whole suite green. Per acceptance criterion, delete the single line that performs the work and confirm something fails.
4. **Count claims.** A guard keyed to the corrected string ("41 widgets") cannot match a stale restatement ("43 widgets") elsewhere on the surface. Match the claim's *shape* with a regex, read the value out of every restatement, and add the inverse assertion that at least one claim matches — or rewording the sentence out of existence silently disarms the guard.

## Impact

The guard reports green while the requirement it names is gone — worse than no test, because a green inert guard licenses the next editor to remove the real thing, and the blast radius is the newest, least-reviewed path protected by the oldest, most-trusted assertion. These defects arrive in cohorts: whoever wrote one such assertion wrote all of them, so fixing the instances that surface is not sweeping the class.

## Watch for

Any assertion matching a short phrase against agent prose or rule files — count occurrences of every asserted literal in the normalized target first. Guards that loop over several files sharing one assertion (live for one file, inert for another). Only a deletion/negation mutation settles whether a guard bites.

---

## Pattern

A mutation sweep that only breaks the phrase each guard *intends* to pin will systematically miss inert guards. The sweep must independently attempt to **negate each load-bearing sentence** — inverting an imperative to its opposite instruction models the real regression, and a deletion-only sweep never tries it.

## Impact

The verification claim inverts: "N/N killed, zero inert" is produced by a sweep that could not have detected the defect it is cited to rule out. Headline contracts are the likeliest casualties, because they get restated in prose most often, so their key tokens are exactly the ones that recur. The count is honestly arrived at and worthless.

## Watch for

Sweeps that damage only the named phrase; treat any "zero inert" claim as unverified until a negation sweep reproduces it. Anchor drift during the sweep is the harness being wrong, not the guard.

---

## Pattern

A repository-wide sweep that enumerates candidates through `git ls-files` cannot see an untracked file. A new test module that itself violates the sweep (e.g., a retired identifier in a docstring) is green for its entire authoring life and turns red at `git add` — every local pre-commit run is honest, reproducible, and wrong. Similarly, git tracks files not directories, so empty-directory residue is invisible to `git status`.

## Impact

The recorded test baseline is false in the direction that hides work: "green" when the tree is red. An arithmetic-checked count reconciliation that matches its own prediction reads as confirmation while certifying the wrong number, and downstream stages inherit an unreproducible baseline.

## Watch for

Never accept a reported test count measured before the feature's own files were committed — re-run the suite on a clean tree at the implement commit and state which commit it was measured at. When a sweep fires on a test module's own text, fix the text, not the sweep: the identifier belongs in exactly one module. Check empty-directory residue with `find . -type d -empty`, never `git status`.

---

## Pattern

When adjudicating whether a capability grant is genuinely required, the decisive evidence is not the strength of the justification — it is whether a sibling with the same job already operates without the grant. Look for the architectural provision first: the capability is often already supplied as an artifact by one privileged component (a path, a prepared tree, an evidence bundle), which is the non-shell equivalent a removal bar demands be named.

## Impact

Grant audits stall in argument about whether some command "might be needed", and the default resolution is retention with a comment — the exact anti-pattern a removal bar forbids. A single sibling precedent converts an unresolvable judgment call into a verified fact, and it usually reveals the grant was vestigial.

## Watch for

A family of agents where one holds a grant recorded as unclosable and the rest are assumed to need it too — check what the privileged one hands back. Conversely, when a plan asserts an agent uses a capability, verify against the prior body before building to match: a plan's claim about existing code is a hypothesis, and implementing to satisfy a false one manufactures a dependency that never existed. Reporting the plan's error is the correct move, not the insubordinate one.
