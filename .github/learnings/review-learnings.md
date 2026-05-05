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