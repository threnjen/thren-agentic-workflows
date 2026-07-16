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
