<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Debugging Learnings

## If Codex Agents Can't Find Their Subagents

**Problem**: An orchestrator references a subagent by name but Codex cannot spawn it, even though the TOML file exists in `codex/agents/`.

**Root cause**: `~/.codex/agents/` symlinks were created under old filenames; the propagation script later renamed non-user-invocable agents to the `z-` prefix, breaking the symlinks with no replacements created.

**Fix**:
1. Remove broken symlinks: `for link in ~/.codex/agents/*.toml; do [ -L "$link" ] && [ ! -f "$(readlink "$link")" ] && rm "$link"; done`
2. Re-create idempotently: `for toml in "$REPO_ROOT"/codex/agents/*.toml; do ln -sfn "$toml" "$HOME/.codex/agents/$(basename "$toml")"; done`

**Watch for**: Codex loads agents by matching the TOML `name` field against what the orchestrator says. Both the symlink filename and the `name` value must use the propagated (`z-`-prefixed) identifier, not the original `.github/agents/` slug.

## If Codex Subagent Invocations Seem To Do Nothing

**Problem**: An orchestrator's instructions say to spawn a subagent but nothing happens, or the orchestrator handles the task itself.

**Root cause**: Codex multi-agent spawning is native — the runtime matches the agent name string against loaded TOML `name` fields. If the agent is not loaded (missing or broken symlink), the invocation silently fails. Check `ls -la ~/.codex/agents/` for `->` targets that don't exist.

**Watch for**: If the `[SUBAGENT-MODE]` invocation syntax looks right but spawning fails, the issue is almost always the agent not being loaded, not the invocation language.

## If a Codex Child Agent Tries To Spawn Another Agent

**Problem**: A child agent reports its own spawn tool unavailable or silently
does nested work inline.

**Root cause**: The workflow put fan-out ownership on a child. This repository
limits delegation to one level; only the user-invocable root may spawn agents.

**Fix**: Move the nested work to the root as sibling assignments. Give each
sibling exclusive artifact ownership and a compact return contract; let the
root sequence any consumer that needs their combined output.

**Watch for**: Do not raise `agents.max_depth` to preserve a nested design. A
blocked spawn may fall back to inline work and look successful, which defeats
the intended context isolation.

## If a propagated agent delegates to a name that does not exist, check how the reference map is keyed

**Problem**: A propagated orchestrator's fan-out named agents that existed nowhere in the root it shipped to — sibling references by slug survived the rewrite verbatim while the root filed those agents under different identifiers.

**Root cause**: `_build_agent_reference_map` keys on `agent.name` — the *display name* — so only display-name references are rewritten to each root's identifier. A slug matches no key, so `_rewrite_agent_references` silently no-ops. The convention "reference siblings by display name" was real, load-bearing, and enforced by nothing.

**Fix**: Reference siblings by backticked display name in the source — the only harness-neutral form, since each root builds its own map. Do **not** add slug keys to the reference map: it uses naive `str.replace`, so a slug key also rewrites report filenames and source paths containing the slug.

**Watch for**: A rewrite that cannot fail is a rewrite that cannot be trusted. Any name-translation step that silently no-ops on a miss needs a resolution assertion downstream (`test_no_generated_body_references_an_agent_by_unrewritten_slug`). Per-feature tests will not catch this — the defect exists only in the *relationship* between a body and the root it lands in. The guard must compare against the set of agents that root actually *renames*: most slugs equal their identifier and those references are correct.

## If code deletes files, validate the root before enumerating — not the leaf before unlinking

**Problem**: An orphan-pruning sweep guarded every leaf it deleted (symlink check, marker check) but never checked the directory it enumerated. With a generated root itself symlinked outside the repository, every child passed all leaf checks and the sweep unlinked files outside the repo. The `rmtree` variant was worse: the marker guard read one file while the deletion was recursive.

**Root cause**: Leaf-level validation answers "is this specific thing safe to delete", never "am I standing in the right place". Only the second is a containment property.

**Fix**: Resolve the enumeration root and assert it is inside the target root *before* globbing; fail loudly rather than skipping. Resolution must cover the whole path — a symlinked *parent* with a real leaf directory defeats `directory.is_symlink()` while still escaping.

**Watch for**: Reversibility asymmetry decides severity — a bad write is undone by re-running propagation; a bad delete is gone. The regression test must include the symlinked-parent case, and must prove both that the guard refuses *and* that the legitimate in-root sweep still prunes — a containment check that bricks the feature will be reverted by whoever hits it next.

## If agents fail with "missing permissions" or missing input artifacts, check the deployed copy's age before the agent contract

**Problem**: PR Review fan-out evaluators (artifact sweeper, consistency auditor) reported permission-style failures — they could not attribute added lines because the orchestrator never materialized `range.diff`/`changed-files.txt` for them, though the source contracts said it should.

**Root cause**: The pipeline has two hops — `source_of_truth/ -> ports/` (propagation, `scripts/propagate_master_assets.py`) and `ports/ -> live harness config dirs` (deployment, root-level `deploy_agents.py`). The second hop simply had not been run after the latest propagation, so installed copies under `~/.claude/` were executing an old orchestrator prompt. The agent definitions themselves were correct.

**Fix**: Re-ran deployment so `~/.claude/` matches `ports/claude/`. Run `python3 deploy_agents.py` after every propagation (or leave `--watch` running).

**Watch for**: When a subagent misbehaves in a way the source contract explicitly forbids, diff the installed copy against the generated port output before editing any source. A restricted-tool agent (no shell/git) failing on "missing" inputs usually means its orchestrator — not the agent — is stale or skipped a materialization step.
