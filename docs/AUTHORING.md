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
invisibly to reviewers scanning for the expected extension. `auditor`, `delta-auditor`,
`docs-writer`, and `03f-prod-code-review` shipped for a long time without the `.agent.md`
suffix and were still agents, because loading keys off `name`/`description` frontmatter,
not the extension. They have since been renamed for consistency, but the loader remains
frontmatter-driven — the glob must stay `*.md`.

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

## Never gate a verdict on a step the agent cannot execute

Phase - Execute returned "not approved" on nearly every run. Manual QA was never one of the
inputs to `all-approved`, but the surrounding prose framed the manual checklist as outstanding
work, so the agent inferred a gate and blocked on an action only a human can perform.

**An enumeration of what counts reads as silence about what does not.** Listing the four results
that feed a verdict does not tell the agent a fifth thing is excluded — it leaves the fifth
unmentioned, and an unmentioned obligation gets read as an unmet one.

**Fix**: name the exclusion, at every site that computes or reports the verdict — the aggregation
rule, the consumer's prompt template, and the consumer's own rubric. Three sites, because one is
where the agent decides and two are where it justifies the decision.

**Watch for**: any gate whose evidence is a human action — visual inspection, a live service, UX
judgment. It belongs after the pipeline, never inside its approval. The matching obligation is to
keep the automated side honestly automatable: a check a command could decide must not be filed on
a human's checklist.

## Name every subagent at its spawn site

A trigger table mapping a condition column to an agent roster forces two lookups — read the row,
then find the prose that spawns it — and rots silently. Deleting one leaves prose pointing at
"a firing dependency row" that no longer exists, and a test that parses the table keeps passing
right up until the table is gone.

**Fix**: one sentence per spawn, carrying the agent name, its inputs, and its condition. Group
unconditional spawns under one lead and conditional ones under another, then state once that a
condition which does not hold is complete evidence, not a missing reviewer.

**Watch for**: anonymous lane labels — "Reviewer D", "Reviewers A through D". The reader cannot
tell what the agent is for, and a constraint attached to the label ("do not pass the plan to
Reviewer D") loses its reason.

## Removing a numbered step means renumbering, then sweeping

A removed step leaves a gap, and a gap invites two wrong repairs: reusing the number for
something else, or reading the sequence as broken. Close it.

**Fix**: renumber every following step, then sweep the whole repository for the old numbers —
not just the file you edited. Cross-references live in test modules that split on heading
strings, in sibling agents, and in deprecation notes.

**Watch for**: a reinstatement document. Its step numbers describe the file *after* the removed
step returns, which equals the pre-removal numbering. Applying the renumber map there makes a
correct document wrong. State which numbering a document uses, and find sites by quoted text
rather than by step number.

## Write what this step does, for the agent that will run it

An agent definition is read by one agent, once, top to bottom, and acted on. It is not read by a
reviewer weighing whether the design was right. Six kinds of sentence serve the author instead of
that reader. All six are cuts.

- **Explaining a later step.** A sentence naming an agent this step does not spawn, or a verdict
  it does not compute. The step needs to know where its output goes — never what the consumer
  will conclude from it.
- **Restating an earlier step.** A precondition already guaranteed by sequence, or a rule
  repeated where it is not applied. A step's own preconditions are fair. A summary of what
  produced them is not.
- **Describing a subagent's internals.** "Its task is to…", "It proves…", "It sweeps…" after a
  spawn whose brief already commissions the work. The subagent never reads this file, and the
  orchestrator only has to spawn it and use what comes back.
- **Defending the decision.** A clause arguing for the rule above it rather than adding a
  constraint — "because no per-feature review can see that class of defect", "so the schedule
  stays stable". The rationale belongs in this document or in a learnings note. The agent needs
  the rule.
- **Narrating the change.** "formerly", "(revised)", "this was removed because", "the slot is
  still free". An agent definition describes the current pipeline as though it were always the
  pipeline. Git history is the change log. This is the baseline-truth rule from `phase-doc-sync`,
  and it applies to agent bodies too.
- **Reasoning aloud.** Weighing an option, acknowledging a trade-off, or explaining why the
  obvious alternative was not chosen. Decide it at authoring time and write the decision.

**The one that looks like all six and stays**: a sentence forbidding a specific misreading.
"A condition that does not hold is complete evidence, not a missing reviewer" and "an absent
audit is never a clean result" are rules wearing explanatory clothing. The test is whether
deleting it permits a wrong action. If it does, keep it.

**Watch for**: a sentence you would delete if the reader had already read the whole file. Every
agent reader has. The structural form of the same waste is a lookup table — see *Name every
subagent at its spawn site* above.

## Sharp, not editorial

What survives the cuts above still has to earn its tone. An agent definition is an instruction
set, not an argument and not a piece of writing.

- **No emphasis the sentence has not earned.** "critically important", "absolutely never",
  "the single most important". If a rule needs an intensifier to read as binding, it is written
  as advice. Rewrite it as an instruction.
- **No commentary on the rule.** "Note that", "It is worth remembering that", "Importantly".
  Delete the frame and keep the sentence.
- **No stakes narration.** "This is where runs usually go wrong", "getting this wrong is
  expensive". Put the constraint where the mistake happens and let it do the work.
- **No hedging on a decision you already made.** "generally", "typically", "in most cases",
  "you may want to" — on a step the agent must run. A real conditional names its condition.
  Preserve a genuine hedge: "may have failed" is not "failed", and confidence is content.
- **One name per thing, one verb per action.** Do not rotate check, verify, and confirm for the
  same act, or call one artifact the plan, the bundle, and the plan set.

**Watch for**: an adjective in an instruction. "Run the affected suites" needs no adverb, and
"carefully validate" is weaker than naming what validation checks.


## A bound needs a stated purpose and exactly one owner

Phase - Execute and Feature - Plan Author both carried "25 rounds", one per feature and one per
level, for the same loop. The value matched, so grepping it found nothing wrong; only the
denominators disagreed. Neither said what the bound was guarding, so the number read as a tuning
knob rather than a tripwire.

**Fix**: state the bound once, in the agent that runs the loop. Every other agent says what it
does when the bound trips, never what the bound is. Give the number one sentence of purpose, so
the next reader raises the alarm instead of raising the limit.

**Watch for**: a bound whose unit was a scheduling concept you removed. Grep downstream agents for
the retired unit's *noun*, not for the value — the value survives the rename.

## Bound a repair that changes what it measures

A gate reading a whole-branch diff cannot repair from that diff and then re-measure freely: the
fix changes what the next measurement sees. Cap the rounds outright rather than testing for
convergence.

**Watch for**: blast radius, not severity, when deciding which finding class may be repaired
automatically. A high-severity defect in one file is safer to fix unattended than a low-severity
one spread across twenty.
