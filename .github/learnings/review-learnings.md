# Review Learnings

## Pattern

When a shell hook serializes git path lists into JSON, preserve git's safe path encoding instead of collapsing `-z` output into newline-delimited text before iteration.

## Impact

Filenames containing embedded newlines or other control characters can split into multiple JSON entries or produce invalid JSON, which corrupts downstream ledger consumers.

## Watch for

`git ... -z | tr '\0' '\n'`, here-doc loops over path lists, or `json_escape` helpers that only escape quotes and backslashes.

## Pattern

When agent instructions add ledger-event schemas with resolution fields, document both the initial failure write and the follow-up append-on-resolution path in the source-of-truth file and every mirrored copy.

## Impact

If `resolved_attempt` and `resolved_by` are named in the schema but the write path is undocumented, agents can log failures without ever recording their resolution, which leaves downstream grading and audit steps with incomplete state.

## Watch for

Ledger blocks that describe only the first append, schema fields that imply a later lifecycle transition without matching instructions, or parity updates that copy the schema but omit the resolution behavior.

## Pattern

When adding checkpoint-commit instructions to rerunnable authoring flows, stage every artifact mutated by that step and describe resumable scopes as created or modified, not created only.

## Impact

Overly narrow staging leaves setup files like `.gitignore` dirty after the checkpoint or drops edits from resumed runs, so later commits inherit unrelated changes and the checkpoint no longer represents a clean step boundary.

## Watch for

Checkpoint text that stages only output directories while earlier numbered steps also edit repo metadata, or authoring checkpoints that refer to files created in this session when the workflow can rerun against existing files.

## Pattern

When an orchestrator writes shared QA or final-review artifacts at phase scope, keep the checkpoint contract phase-scoped too; do not promise per-feature checkpoint commits against consolidated outputs.

## Impact

Mixed scopes create impossible staging instructions, force review records into traceability exceptions, and prevent downstream ledger consumers from mapping checkpoints back to the unit named in the commit message.

## Watch for

Per-feature `eval: qa <task>` or `eval: final-review <task>` language next to one shared QA writer invocation, one phase-wide prod review prompt, or staging notes that mention only consolidated phase documents.

## Pattern

When adding a new user-facing agent, update every inventory surface that carries agent counts or summarized agent lists, not just the primary catalog tables.

## Impact

Stale overview bullets and architecture diagrams can contradict the actual agent inventory, which weakens the source-of-truth docs and can mislead downstream agents that bootstrap from those summaries.

## Watch for

Top-level README intros, Mermaid labels, CODEBASE_CONTEXT count summaries, and any touched docs that summarize standalone agents or total agent-file counts.

## Pattern

When agent frontmatter or platform-contract rules change, update every shared documentation table that summarizes file formats or metadata fields in the same change.

## Impact

If summary tables lag behind the live files, source-of-truth docs can keep advertising removed keys like `model:` and mislead both humans and downstream agents about the actual contract.

## Watch for

Platform comparison tables, frontmatter field summaries, architecture diagrams, and codebase-context bullets that describe agent-file schemas at a glance.

## Pattern

When a porting guide scopes an agent source directory using a filename glob (e.g., `*.agent.md`), verify whether the directory contains agent definitions that do not match that extension. Some agent files use a plain `.md` extension and are only distinguishable from documentation files by their YAML frontmatter.

## Impact

A guide that gates on extension alone silently excludes valid agent definitions from the porting scope, causing missed migrations that are invisible to reviewers who only scan for the expected extension.

## Watch for

Porting guides that describe a source surface as `*.agent.md` or similar glob, source directories that contain both agent definitions and documentation files under the same parent, and any example or table that cites a single naming pattern as exhaustive.

## Pattern

In documentation guides that embed shell verification blocks for future-facing placeholder paths, bare `test -e` calls exit non-zero with no output, giving no indication whether failure means "not ready yet" or "misconfigured." This makes copy-pasted preflight blocks appear to work when run in a shell with `set -e` disabled, silently skipping the intent.

## Impact

Users following the guide copy-paste the block, see no output, and cannot distinguish between "source artifact doesn't exist yet — wait for Phase N" and "path is wrong — fix now." Silent failure obscures readiness status.

## Watch for

Preflight code blocks with bare `test -e "$PATH"` lines where those paths are documented as future-facing placeholders; fix by adding `|| echo "not yet: <path>"` or a comment block explaining expected failure.

## Pattern

When an AC text specifies a Terraform backend `key` using variable interpolation (e.g., `baseline/${var.environment_slug}/...`), the implementation must use a partial backend config instead — the key is omitted from `backend.tf` and supplied via `-backend-config="key=..."` at `terraform init` time. Terraform does not support variable interpolation in backend blocks.

## Impact

If a reviewer compares the AC literal text against the backend file and flags the missing key as a bug, they will raise a false positive. The plan's correctness section (Section B) always resolves this ambiguity — check it before raising the issue.

## Watch for

Terraform `backend.tf` files that omit the `key` attribute combined with AC text that describes a parameterized key path. Verify the plan's correctness section for the explicit partial backend config decision before flagging as missing.

## Pattern

Scaffold placeholder comments in `outputs.tf` (e.g., "Output blocks are added in Feature N when resources are defined") are never updated when the implementing feature lands.

## Impact

Stale `outputs.tf` files carry misleading comments after resources are defined, and useful reference outputs (e.g., resource ARNs) are silently omitted, reducing post-apply verifiability.

## Watch for

`outputs.tf` files with placeholder-style comments that name a specific future feature; check whether that feature has already landed and whether any resource ARNs or IDs are worth exporting as outputs.

## Pattern

When a public value type can be constructed directly as well as through a validating factory, validate it again at every security-sensitive emission or execution boundary.

## Impact

Callers can bypass factory validation by invoking the value constructor directly, allowing invalid actions to reach an external runner and potentially turn a fail-closed path into an ambiguous or non-blocking result.

## Watch for

Exported `NamedTuple`, dataclass, or plain-object decision types paired with a validating factory, followed by emitters or guards that check only the instance type.

## Pattern

Fail-open observability requirements must cover the executable wrapper as well as exceptions handled inside the implementation language.

## Impact

An interpreter startup or shell-pipeline failure can return non-zero before application-level exception handling runs, causing an audit-only hook to block its caller.

## Watch for

Audit wrappers using `set -e` or `pipefail` without an explicit non-blocking fallback, and tests that invoke only the Python or Node entrypoint rather than the actual shell wrapper.

## Pattern

Security matchers that compare one glob pattern with another must vary wildcard replacements independently and treat the protected directory root as part of a recursive directory rule.

## Impact

Single-sample glob heuristics can miss overlapping scopes such as a broad filename pattern that includes a protected extension, while a recursive rule like `protected/**` can accidentally allow the `protected` directory itself. Either gap lets scoped search or file operations reach protected targets.

## Watch for

Glob-overlap helpers that substitute the same value for every `*`, recursive path rules tested only with descendant files, and missing controls proving ordinary source globs remain allowed.

## Pattern

When removing an exact encoded suffix from parsed shell tokens, use exact suffix removal rather than `rstrip` with the suffix characters.

## Impact

`rstrip("\\n")` removes any trailing backslash or letter `n`, corrupting ordinary filenames such as `auth.json` before security policy evaluation and creating deterministic bypasses.

## Watch for

`rstrip` or `lstrip` calls whose argument is intended as a whole delimiter, especially escaped newline markers, extensions, or protocol sentinels; cover nearby filenames ending in each delimiter character.

## Pattern

Artifact propagators must validate resolved source assets and resolved destination directories against their declared roots before reading or writing; replacing only a symlinked leaf file is not sufficient.

## Impact

A symlinked parent directory can redirect generated files outside the consumer root, while a normalized `../` command token or source symlink can reference content the deployable unit never copied. Both cases break isolation and can overwrite or disclose unrelated files.

## Watch for

Copy loops that call `target.write_*` beneath unchecked parent directories, validators that test path prefixes before normalization, source walks that follow symlinks without a resolved-root check, and tests that cover only leaf symlink replacement.

## Pattern

When selectively unignoring a nested fixture tree beneath a broad parent ignore
rule, re-ignore sibling paths between the parent exception and the fixture
exception.

## Impact

Negating only the parent directory can make unrelated future artifacts
trackable, weakening repository hygiene and the intended scope of the
exception.

## Watch for

Ignore files with a broad `parent/*` rule followed immediately by
`!parent/child/` and `!parent/child/**`, without a `parent/*` rule restoring the
boundary.

## Pattern

When a procedural document defines conditional resource lifecycle behavior,
make each create, reuse, recreate, and refusal branch executable in sequence.

## Impact

A policy that is described only in prose can be followed literally as an
unconditional create or cleanup operation, causing collisions or deleting
resources that should have been retained.

## Watch for

Steps that say to apply a collision policy and then show one unconditional
create command, especially when ownership determines whether cleanup is safe.

## Pattern

Orchestrators must validate both child report artifacts and the terminal synthesis result before accepting a readiness verdict.

## Impact

A child can return success with a missing or empty report, or the terminal synthesizer can fail, allowing incomplete coverage to be mistaken for a clean run.

## Watch for

Delegation contracts that record only explicit exceptions, trust returned report paths without metadata validation, or pass a synthesizer verdict directly to status write-back without an independent missing-check gate.

## Pattern

Diff-scoped static analyzers must require verifiable line or range attribution before treating repo-wide results as introduced changes.

## Impact

Filtering a repo-wide result only by touched file can misclassify pre-existing dead code or other findings as changes from the current phase.

## Watch for

Analyzers that fall back from added-line matching to file membership, accept missing source locations, or report findings when baseline attribution cannot be established.

## Pattern

Read-only dependency vulnerability checks must use supplied local evidence or an explicitly offline audit mode.

## Impact

A generic audit command can fetch or update vulnerability data, violating the evaluator's no-network boundary and making the evidence path non-reproducible.

## Watch for

Instructions that call an audit command read-only without stating offline behavior, commands with implicit network access, or missing-evidence paths that claim a clean vulnerability result.

## Pattern

Delegating or read-only wrapper agents should receive only the capabilities needed for input collection, child delegation, and report writing; generated harness outputs should be checked against the source renderer.

## Impact

Unneeded shell or execution permissions weaken prompt-level read-only boundaries, while untested generated mirrors can silently lose delegation or safety constraints in one platform.

## Watch for

Wrapper frontmatter that grants execute access without a local execution requirement, platform-specific permission mappings, and propagation tests that verify only unrelated hooks or skills instead of the new agent outputs.

## Pattern

When a delegated evaluator fails after dispatch, record both the concrete NOT RUN reason and an explicit NO-GO or below-GO readiness ceiling.

## Impact

A not-run marker without a visible readiness ceiling can be mistaken for neutral coverage, allowing an incomplete review to advance as if the evaluator had passed.

## Watch for

Status rows that contain `status: not-run` and `report: null` but no machine- or reader-visible verdict ceiling, especially when a child report is required for release readiness.

## Pattern

Parallel verifier fan-outs must assign deterministic, child-derived report paths.

## Impact

If concurrent children are told only to write into a shared directory, generic filenames can overwrite sibling evidence and make parent row-cardinality checks unreliable.

## Watch for

Delegation prompts that name a shared output directory without a unique filename template or a parent check that maps each child identifier to exactly one report artifact.

## Pattern

Propagation regression tests must cover every newly added agent output, including
non-delegating harvesters and synthesis agents, and compare each harness render
with the source renderer.

## Impact

Hard-coded evaluator subsets or orchestrator-only smoke checks can pass while a
new Claude, OpenCode, or Codex mirror is stale or malformed.

## Watch for

Expected-slug tuples that omit newly added agents, tests named for one evaluator
family that silently exclude sibling agents, or generated outputs checked only
for existence rather than exact renderer parity.

## Pattern

Read-only history-mining agents must keep evidence-access instructions consistent
with their declared capabilities and explicitly handle unavailable sources.

## Impact

A fetch-only agent that includes shell examples can violate its no-execute
boundary, while a remote-only capability can be mistaken for guaranteed local
history recovery.

## Watch for

Command examples in fetch-only contracts, missing unavailable-source handling,
or mirror tests that inspect only one harness's permission boundary.

## Pattern

A marker-based guard that decides whether a generated file may be deleted must key
on the exact position the emitter writes the marker to — never on the marker
appearing anywhere in the file, and never on a prefix check that ignores
frontmatter. Extract that position into one helper shared by the writer and the
guard so the two cannot drift apart.

## Impact

Both looser rules fail, in opposite directions. A prefix check against output that
opens with YAML frontmatter matches nothing: the guard reads as implemented, passes
review, and silently disables the sweep indefinitely. A whole-file search matches any
hand-maintained document that merely quotes the marker while documenting the
convention, deleting exactly the file the guard exists to protect.

## Watch for

`startswith(MARKER)` applied to frontmatter-bearing output; `MARKER in text` or
`MARKER in text.splitlines()` used as a deletion predicate; a guard tested only for
what it deletes and never for what it must refuse to delete; README or convention
docs living inside a generated root.

## Pattern

A destructive helper is proven only by tests that bracket it from both directions:
one that fails if the guard is removed, and one that fails if the guard is tightened
until it matches nothing.

## Impact

A single-sided suite lets a guard pass for the wrong reason. An inert guard trivially
satisfies a "deletes zero files on a clean tree" criterion while the capability it
gates does nothing at all. Mutation-test the guard rather than asserting it.

## Watch for

Inert-run criteria ("a run on the unmodified repo deletes nothing") with no companion
test proving the pruner positively identifies real generated output; deletion counters
asserted only as zero.

## Pattern

A deliberately-failing tripwire that guards a time-boxed exemption must be addressed to
the pass that will actually trip it, not the pass nominally assigned the cleanup. Verify
which one that is by reading what the downstream work does to the exempted paths — if it
renames or moves them, the exemption stops matching and the tripwire fires there.

## Impact

A tripwire addressed to a later pass than the one that trips it converts a clean hand-off
into a red baseline for every pass in between, and each of those inherits a failing
green-baseline gate for work it does not own. The likely outcomes are a wasted escalation
or a suite left red on purpose — which trains implementers to ignore red. The tripwire
itself is usually right; only its addressee is wrong, and the fix is a message edit.

## Watch for

Inverted assertions (`assert still_offending`) whose failure message names an owner; any
exemption list keyed on a path that a downstream rename will invalidate; hand-off notes
that assign cleanup to the pass that *removes the cause* rather than the pass that *first
makes the exemption unnecessary*.

## Pattern

When an exemption list, a skip, or a non-goal is justified by a factual claim about the
tree ("this directory does not exist", "this path is only planning records, no live
wiring"), verify the claim against the tree before accepting the exemption. Do not accept
the rationale on its own authority.

## Impact

Two distinct failures follow. An over-broad exemption resting on a false premise silently
hides the very references the sweep exists to find. Worse, a non-goal justified by
"already absent" leaves work *unowned* rather than *deferred* — deferred work has an
inheritor, dismissed-as-nonexistent work has none, and it is invisible precisely because
everyone believes it was already handled.

## Watch for

Non-goals whose justification is an assertion of absence rather than a decision to defer;
exemption scopes broader than the rationale that justifies them (a whole tree exempted to
cover one subtree of records); rationales phrased as sweeping claims about a directory's
contents. Narrowing an exemption is cheap when the sweep still passes — and the passing
sweep is itself the proof the narrowing was safe.

## Pattern

Deleting an orchestrator can rename a user-facing entry point it never owned. Where a
generated artifact's name depends on whether some *other* asset references it, removing
the last referrer reclassifies it and changes its public name. Before approving a
deletion, ask what the deleted asset was the last declarer of.

## Watch for

Emission rules conditioned on a reference map (`user_invocable and name in
referenced_names`); identifier resolution that reads on-disk state rather than deriving
from source — it makes such changes converge only across multiple generator runs, so a
single run proves nothing. Run the generator until every counter reads zero before
trusting the tree, and treat "one run, looks right" as unverified.

---

## Pattern

An evidence-shaped claim is not evidence. Implementation records increasingly cite
"mutation-tested", "stable across N consecutive runs", or a named counter as proof. These
carry the *form* of verification and are read as settled, but they fail re-execution often
enough that a reviewer who accepts them is not reviewing. Re-run every cited proof against
a clean tree at the reviewed commit. A record's claim is a hypothesis about the tree, not
a description of it.

## Impact

Two defects reached a commit behind such claims in one feature: a suite reported green
that was red, and a correct action defended by a mutation test that passes identically
with and without the change it supposedly proved. The right action on false evidence still
validates the wrong reasoning, which is what the next feature inherits.

## Watch for

Claims of a passing suite where the arithmetic reconciles to *collected* rather than
*passed* (447 passed + 1 failed reported as "448"). Mutation tests where the mutation would
trip an unrelated guard anyway — verify the test fails for the stated reason, and that it
*passes* once the change under test is reverted, or it proves nothing. Dead-code deletion
described as a behaviour change: an exemption keyed to a name that a rename already
invalidated matches nothing, so removing it can neither widen nor narrow the sweep. Ask
what an exemption matched *at the moment it was deleted*, not what it matched when written.

---

## Pattern

When a sweep test goes red because a new file legitimately contains the swept token, the
one-line fix — add the file to the exemption list — is almost always wrong. It widens the
hole the sweep exists to close, often in the exact pass that was supposed to narrow it.
Remove the token instead: import the canonical definition and derive the values.

## Impact

Exemption lists grow monotonically and are never audited. Each entry is a permanent blind
spot bought to make one test green, and the next regression that lands inside one is
invisible.

## Watch for

A guard module that declares its names are defined "once, here" while another module
re-lists them as literals — the duplication is the defect, and the sweep failure is the
symptom correctly reporting it. Also: when replacing literals with a derived tuple, add a
vacuity assert (`assert derived_list`), or an empty upstream list silently neuters the
guard while it still reports green.

## Pattern

A contract test that asserts a literal is present somewhere in a whole document is inert wherever that literal occurs more than once. Deleting the occurrence the test exists to protect leaves a stray occurrence elsewhere, and the assertion stays green over a broken contract. Scope every prose assertion to the section, list item, or sentence that carries the obligation — parse the structure (numbered items, `- **bullets**`, the body below a heading) and assert against it, not against the flattened document.

## Impact

The guard reports green while the requirement it names is gone. This is worse than no test: absence tests are usually protecting the highest-risk deleted code or the least-defended contract, and a green inert guard is what licenses the next editor to remove the real thing. Reviewers cannot detect it by reading, because the test and the contract both look correct in isolation.

## Watch for

The same literal appearing in a heading and in the rule beneath it; in frontmatter `description:` and again in the body; in a rule that writes a file and again in a sentence that reads it; in a ranked list and again in a worked example. Before trusting any prose-assertion module, count occurrences of every asserted literal in the normalized target — a count of two or more marks a candidate, and only a deletion mutation settles it. Fixing the one or two instances that happen to surface is not sweeping the class: this defect arrives in cohorts, because whoever wrote one presence assertion wrote all of them.

## Pattern

A prose assertion against a hard-wrapped document can pass or fail on where the lines happen to break rather than on what the document says. A regex spanning two words that a reflow moves onto separate lines stops matching content that is still present; an assertion that only ever matched because its phrase fit on one line is inert against the requirement it names. Normalize runs of whitespace to single spaces before asserting on a sentence, and reserve raw-text assertions for literal tokens and frontmatter, where line structure is part of the contract.

## Impact

The guard's verdict tracks the formatter, not the author. Reflowing a paragraph — an edit with no semantic content — silently drops the assertion or reddens a correct document. Both directions destroy trust: the first hides a broken contract, the second trains the next editor to loosen the regex until it stops biting.

## Watch for

Any assertion module that reads an agent body, a Markdown rule file, or any hard-wrapped prose and matches multi-word phrases. This defect arrives in cohorts — whoever wrote one line-break-sensitive regex wrote all of them. Two normalized readers (one for literals, one for sentences) is the shape that works. The normalization itself is not evidence: only a mutation sweep that breaks each contract at its own anchor proves the guards bite, and anchor drift during that sweep is the harness being wrong, not the guard.

## Pattern

When adjudicating whether a capability grant is genuinely required, the decisive evidence is not the strength of the justification — it is whether a sibling with the same job already operates without the grant. An existing agent doing the harder version of the work under the narrower grant settles the question that argument cannot. Look for the architectural provision first: a capability is often already supplied as an artifact by one privileged component (a path, a prepared tree, an evidence bundle), which is the non-shell equivalent that a removal bar demands be named.

## Impact

Grant audits stall in argument about whether some command "might be needed", and the default resolution is retention with a comment — the exact anti-pattern a removal bar exists to forbid. A single sibling precedent converts an unresolvable judgment call into a verified fact, and it usually reveals the grant was vestigial rather than load-bearing.

## Watch for

A family of agents where one holds a grant recorded as unclosable and the rest are assumed to need it too. Check what the privileged one hands back: if it returns a path or artifact the others merely read, the others need no grant. Conversely, when a plan asserts an agent uses a capability, verify against the prior body before building to match — a plan's claim about existing code is a hypothesis, and implementing to satisfy a false one manufactures a dependency and a failure mode that never existed. Reporting the plan's error is the correct move, not the insubordinate one.
