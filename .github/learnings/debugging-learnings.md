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

## If a propagated agent delegates to a name that does not exist, check how the reference map is keyed

**Problem**: A propagated orchestrator's fan-out named agents that existed nowhere
in the root it shipped to. `claude/commands/pr-review.md` delegated to
`05a-baseline-worktree` and `05g-readiness-synthesizer`, but the Claude and Codex
roots file those agents as `z-baseline-worktree` and `z-readiness-synthesizer`.
Zero `z-` references survived the rewrite, against nine in a working sibling
orchestrator. The fan-out would have failed on two of three harnesses.

**Root cause**: `_build_agent_reference_map` keys on `agent.name` — the *display
name* — so only display-name references are rewritten to each root's identifier.
The source body referenced its siblings by *slug*. A slug matches no key, so
`_rewrite_agent_references` silently no-ops and the slug ships verbatim. The
convention "reference siblings by display name" was real, load-bearing, and
enforced by nothing.

**Fix**: Reference siblings by backticked display name in the source. This is the
only harness-neutral form: one source line correctly becomes `z-baseline-worktree`
in Claude and Codex and `05a-baseline-worktree` in OpenCode, because each root
builds its own map. Do **not** "fix" this by adding slug keys to the reference map
— `_rewrite_agent_references` uses naive `str.replace`, so a `05b-change-narrator`
key also rewrites the report filename `05b-change-narrator-report.md` and any
`.github/agents/...agent.md` path that contains the slug.

**Watch for**: A rewrite that cannot fail is a rewrite that cannot be trusted. Any
name-translation step that silently no-ops on a miss needs a resolution assertion
downstream, not a correctness argument upstream. Per-feature tests will not catch
this: each verifies its own agent in isolation, while the defect only exists in the
*relationship* between a body and the root it lands in. Assert that every reference
resolves in the root it ships to — `test_no_generated_body_references_an_agent_by_
unrewritten_slug` is that guard. Note it must compare against the set of agents that
root actually *renames*: most slugs equal their identifier (`prod-code-review`) and
those references are correct, and `claude/agents/README.md` is hand-maintained
inside a generated root and documents slugs on purpose.

## If code deletes files, validate the root before enumerating — not the leaf before unlinking

**Problem**: An orphan-pruning sweep guarded every leaf it was about to delete
(`path.is_symlink()`, marker check) but never checked the directory it enumerated.
With a generated root itself symlinked outside the repository, every child is an
ordinary marker-bearing file that passes all leaf checks, so the sweep unlinked
files outside the repo. The `rmtree` variant was worse: the marker guard reads one
file (`SKILL.md`) while the deletion is recursive, so every sibling of that marker
was removed without ever being inspected.

**Root cause**: Leaf-level validation answers "is this specific thing safe to
delete", never "am I standing in the right place". Those are different questions,
and only the second one is a containment property. A validator already existed in
the same module and neither prune site called it.

**Fix**: Resolve the enumeration root and assert it is inside the target root
*before* globbing, and fail loudly rather than skipping. Resolution must cover the
whole path, not the leaf: a symlinked *parent* with a real leaf directory defeats
`directory.is_symlink()` while still escaping. That is the same nested-destination
shape as the write-side escape, so a repo that fixed it for writes should assume
the delete path has it too.

**Watch for**: Reversibility asymmetry decides the severity. A bad write is undone
by re-running propagation; a bad delete is gone. Any sweep that combines "enumerate
a directory" with "delete what matches" needs its containment check at the
enumeration boundary, and the regression test must include the symlinked-parent case
— a leaf-only check passes the obvious test and still deletes outside the repo. Test
that the guard refuses AND that the legitimate in-root sweep still prunes; a
containment check that bricks the feature will be reverted by whoever hits it next.
