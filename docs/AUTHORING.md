# Authoring Agents

Diagnosed failure modes specific to *this* repository — authoring agent definitions and
getting them through the transform-and-deploy pipeline intact. None of this applies to a
consumer repo, which reads deployed agents but never writes them.

For the pipeline mechanics themselves see [ARCHITECTURE.md](ARCHITECTURE.md); for the
maintenance loop see [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md).

## Check the deployed copy before the source

Definitions reach a harness through more than one hop: authoring → generated port →
installed config dir. A skipped hop leaves the harness running an old prompt while the
source reads correctly. Most "the agent is wrong" reports are deployment state, not
prompt content.

**Fix**: re-run deployment so the installed tree matches the generated one, then re-test.

**Watch for**: a restricted-tool agent (no shell or git) failing on "missing" inputs
usually means its *orchestrator* is stale or skipped a materialization step — not the
agent being debugged.

## If an agent can't find its subagents, check how they are loaded

Codex spawning is native: the runtime matches the name string against the `name` field of
loaded TOML files. Unloaded means the invocation silently fails, or the orchestrator
quietly does the work itself. Stale symlinks left by a rename are the usual cause.

**Fix**: drop dead links, then relink idempotently with `ln -sfn`.

```bash
for l in ~/.codex/agents/*.toml; do
  [ -L "$l" ] && [ ! -f "$(readlink "$l")" ] && rm "$l"
done
```

**Watch for**: `->` targets that don't exist in `ls -la ~/.codex/agents/`. Both the link
filename and the `name` value must use the deployed identifier, not the authoring slug.

## If an agent delegates to a name that does not exist, check how the reference map is keyed

Name translation between authoring and per-harness identifiers keys on the *display
name*. A reference written as a slug matches no key, so the rewrite silently no-ops and
ships a name that exists nowhere in the target.

**Fix**: reference siblings by backticked display name — the only harness-neutral form.
Do not add slug keys: naive replacement would also rewrite report filenames and source
paths containing the slug.

**Watch for**: a rewrite that cannot fail cannot be trusted. Any translation step that
no-ops on a miss needs a downstream resolution assertion. Per-unit tests never catch
this — the defect lives in the *relationship* between a body and the tree it lands in.

## A source surface described by a single filename glob is usually incomplete

Definitions distinguishable from documentation only by frontmatter get silently excluded,
invisibly to reviewers scanning for the expected extension. `auditor.md`,
`delta-auditor.md`, `docs-writer.md`, and `04f-prod-code-review.md` are agents despite
lacking the `.agent.md` suffix, because loading keys off `name`/`description`
frontmatter.

The same trap applies to `applyTo` globs: `fnmatch` runs against the agent's
repo-relative path, so `**/x.agent.md` matches only when a `/` immediately precedes `x`,
and a pattern that matches nothing fails silently — the instruction simply ships to no
agent.

## Keep fan-out at the root, and give each child its own report path

Delegation depth is one: only the user-invocable root spawns agents. A child asked to fan
out either reports its spawn tool missing or silently does the nested work inline.

**Fix**: express nested work as sibling assignments from the root, each with exclusive
artifact ownership and a compact return contract. Report paths must be deterministic and
child-derived — a shared directory plus generic filenames means children overwrite each
other's evidence and parent cardinality checks stop working.

**Watch for**: raising a depth limit to preserve a nested design. A blocked spawn can
fall back to inline work and look successful, defeating the context isolation the design
existed for.

## Agent contracts: hold only what the role requires, and make branches executable

- **Wrapper and read-only agents should hold only what input collection, delegation, and
  report writing require.** A fetch-only contract containing shell examples invites
  violation of its own boundary.
- **Conditional resource lifecycle policy stated only in prose gets followed literally**
  as an unconditional create or cleanup. Make each create, reuse, recreate, and refusal
  branch executable in sequence.
- **MCP tools are not declared in agent frontmatter**, so `tools:` neither grants nor
  withholds graph access. Graph unavailability is `NOT RUN` with a verdict-ceiling drop,
  never a silent downgrade to grep.

## When counts or contract rules change, update every summary surface in the same change

Stale intros, comparison tables, and diagrams keep advertising removed keys and mislead
the agents that bootstrap from them. `README.md`, `docs/ARCHITECTURE.md`, and
`docs/CODEBASE_CONTEXT.md` all state counts and must move together.

Recounting cannot fix a *definition* conflict — reconcile what the counted term means
before recounting it.
