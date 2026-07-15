# Debugging Learnings

## If Codex Agents Can't Find Their Subagents

**Problem**: An orchestrator agent references a subagent by name (e.g. `z-feature-plan-expander`) but Codex cannot spawn it — the subagent appears missing even though the TOML file exists in `codex/agents/`.

**Root Cause**: The `~/.codex/agents/` symlinks were created before the propagation script was written, using the original source filenames (e.g. `04a-feature-plan-expander.toml`). The propagation script later renamed non-user-invocable agents to use `z-` prefix (e.g. `z-feature-plan-expander.toml`). The old symlinks became broken; no new symlinks were created for the z-* files.

**Fix**:
1. Remove broken symlinks: `for link in ~/.codex/agents/*.toml; do [ -L "$link" ] && [ ! -f "$(readlink "$link")" ] && rm "$link"; done`
2. Re-create all symlinks idempotently: `for toml in "$REPO_ROOT"/codex/agents/*.toml; do ln -sfn "$toml" "$HOME/.codex/agents/$(basename "$toml")"; done`

**Watch For**: Codex loads agents by matching the `name` field in TOML against what the orchestrator says. Both the symlink filename and the TOML `name` value must match exactly. The propagation script uses `z-` prefix for non-user-invocable agents — the symlinks must use that same filename, not the original `.github/agents/` slug.

## If Codex Subagent Invocations Seem To Do Nothing

**Problem**: An orchestrator's instructions say to spawn a subagent but nothing happens or the orchestrator handles the task itself instead.

**Root Cause**: Codex multi-agent spawning is native (no `codex exec` shell call needed). It works by the runtime matching the agent name string in the orchestrator's instructions against loaded TOML `name` fields. If the agent is not loaded (missing or broken symlink), the invocation silently fails.

**Fix**: Verify `~/.codex/agents/` has a valid symlink for every agent TOML in `codex/agents/`. Check with `ls -la ~/.codex/agents/` and look for `->` targets that don't exist.

**Watch For**: The `[SUBAGENT-MODE]` prefix convention in `developer_instructions` is the correct invocation pattern. If syntax looks right but spawning fails, the issue is almost always the agent not being loaded (missing symlink), not the invocation language.

## If Feature Decomposer Says "z-feature-plan-expander tool is not exposed in this session"

**Problem**: The `feature-decomposer` agent outputs a message like "The z-feature-plan-expander tool is not exposed in this session, so I'm going to do that expansion directly instead." The expansion still happens inline but the subagent is never spawned.

**Root Cause**: Codex `agents.max_depth` defaults to `1`. The pipeline runs as `phase-execute` (depth 0) → `feature-decomposer` (depth 1) → `z-feature-plan-expander` (would be depth 2). Depth 2 is blocked by the default max_depth of 1, so the model detects the spawn tool is unavailable and falls back to doing the expansion inline.

**Fix**: Add `[agents] max_depth = 2` to `~/.codex/config.toml`. This allows the one additional nesting level needed for the feature pipeline. If running feature-decomposer directly (not via phase-execute), depth would only reach 1 and the default would work; the issue only manifests when running through an orchestrator.

```toml
[agents]
max_depth = 2
```

**Watch For**: Increasing max_depth beyond 2 risks runaway fan-out from broad delegation instructions. `max_depth = 2` is the minimum needed for this pipeline (orchestrator → decomposer → expander) and is the recommended setting.
