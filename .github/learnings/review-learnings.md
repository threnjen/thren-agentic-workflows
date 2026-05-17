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