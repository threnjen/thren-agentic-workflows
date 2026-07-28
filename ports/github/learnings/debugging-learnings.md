# Debugging Learnings

Seed file. Agents append diagnosed root causes here — pipeline gaps, harness quirks, agent workflow failures. Check these before editing an agent definition: most "the agent is wrong" reports are environment or deployment state.

## If a subagent misbehaves in a way its own contract forbids, check the deployed copy before the source

Definitions reach a harness through more than one hop (authoring → generated port → installed config dir). A skipped hop leaves the harness running an old prompt while the source reads correctly — usually surfacing as an evaluator reporting missing permissions or missing input artifacts.

**Fix**: re-run deployment so the installed tree matches the generated one, then re-test.
**Watch for**: a restricted-tool agent (no shell/git) failing on "missing" inputs usually means its *orchestrator* is stale or skipped a materialization step, not the agent.

## If an agent can't find its subagents, check how they are loaded, not the invocation syntax

Codex spawning is native — the runtime matches the name string against the `name` field of loaded TOML files. Unloaded means the invocation silently fails or the orchestrator does the work itself. Stale symlinks from a rename are the usual cause.

**Fix**: drop dead links (`for l in ~/.codex/agents/*.toml; do [ -L "$l" ] && [ ! -f "$(readlink "$l")" ] && rm "$l"; done`), then relink idempotently with `ln -sfn`.
**Watch for**: `->` targets that don't exist in `ls -la ~/.codex/agents/`. Both the link filename and the `name` value must use the deployed identifier, not the authoring slug.

## If a child agent's spawn tool is unavailable, move the fan-out up — don't raise the depth limit

Delegation depth is one: only the user-invocable root spawns agents. A child asked to fan out either reports its spawn tool missing or silently does the nested work inline.

**Fix**: express nested work as sibling assignments from the root, each with exclusive artifact ownership and a compact return contract.
**Watch for**: raising `max_depth` to preserve a nested design — a blocked spawn can fall back to inline work and look successful, defeating the context isolation the design existed for.

## If an agent delegates to a name that does not exist, check how the reference map is keyed

Name translation between authoring and per-harness identifiers keys on the *display name*. A reference written as a slug matches no key, so the rewrite silently no-ops and ships a name that exists nowhere in the target.

**Fix**: reference siblings by backticked display name — the only harness-neutral form. Do not add slug keys: naive replacement would also rewrite report filenames and source paths containing the slug.
**Watch for**: a rewrite that cannot fail cannot be trusted. Any translation step that no-ops on a miss needs a downstream resolution assertion. Per-unit tests never catch this — the defect lives in the *relationship* between a body and the tree it lands in.
