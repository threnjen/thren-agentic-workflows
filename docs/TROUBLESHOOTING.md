# Troubleshooting

## Local Setup

### Symptom

`pyenv: cannot rehash: couldn't acquire lock ...` or `cannot overwrite existing file`

### Cause

Your shell startup is hitting a blocked or stale `pyenv` rehash before repo commands
run. This is external to the repository, but it breaks the scripts because they rely on
a working `python3`.

### Fix

- Confirm no other `pyenv` process is running.
- Clear the stale `pyenv` lock or shim only after verifying it is not in use.
- Open a fresh shell and verify `python3` resolves before rerunning repo commands.

## Transform (propagate)

### Symptom

Changes under `source_of_truth/` do not appear in `ports/` or `.github/`.

### Cause

The transform watcher is not running, or you edited source files without rerunning the
one-shot command.

### Fix

- Run `python3 scripts/propagate_master_assets.py --once`.
- In VS Code, confirm the `watch: propagate master assets` task is running.
- If you edited generated files directly, rerun the transform and recheck the diff.

### Symptom

`Propagation failed: ...` and a non-zero exit.

### Cause

A pass raised, or propagation did not reach a fixed point within the max passes. Usually
a malformed source file (bad frontmatter, an unclosed `---` block, or an `applyTo` value
that no longer matches anything).

### Fix

- Read the error; fix the offending source file under `source_of_truth/`.
- Rerun `--once`; a clean run prints a JSON convergence summary and a second run should
  report zero changes.

### Symptom

Generated filenames do not match the source agent slug.

### Cause

The transform intentionally rewrites some names for target platforms, and uses `z-`
prefixes for hidden (non-user-invocable) Claude and Codex subagents.

### Fix

- Expect these aliases: `docs-writer` → `docs-writer`, `web-research-specialist` →
  `web-researcher`, `audit-code-or-infra` → `audit-code-infra-refactor`.
- Expect non-user-invocable agents to become `z-*` files in Claude and Codex outputs, with
  two exceptions: the emitter reuses a pre-existing generated stem when one exists, so
  `04f-prod-code-review` stays `prod-code-review.md` and `04h-unity-reviewer` stays
  `unity-reviewer.md` in `ports/claude/agents`.
- Expect a user-invocable agent to *also* get a subagent file when an orchestrator declares
  it as a child (Docs Writer, Web Researcher). That is why
  `ports/claude/agents` and `ports/claude/commands` hold different counts.

### Symptom

An agent exists in `source_of_truth/agents/` but is skipped by downstream tooling.

### Cause

The source file may lack valid agent frontmatter. Agent definitions are loaded by
checking for `name` and `description`, not strictly by extension.

### Fix

- Verify the file has frontmatter with `name` and `description`.
- Do not rename `04f-prod-code-review.md`, `auditor.md`, or `docs-writer.md` just
  because they lack `.agent.md`; they are intentionally part of the source set.

## Deploy

### Symptom

`no saved harness selection; pass --harness ... or --all` (exit 2).

### Cause

`deploy_agents.py` ran in a non-interactive shell with no `.deploy-config.json` and no
`--harness`/`--all` flag, so it has nothing to deploy and will not guess.

### Fix

- Pass `--harness claude,codex,opencode,cursor,github` or `--all`, or run once
  interactively to create the saved selection.

### Symptom

A file at a destination is not being updated; it shows up under `skipped_paths` in the
deploy output.

### Cause

Deploy is fail-closed: it only overwrites or prunes files that carry a generated marker
(or live inside a marked skill directory). The destination file is hand-maintained (or a
stale copy from before markers existed), so it is left untouched.

### Fix

- If the file is a stale copy you want replaced, delete it by hand and rerun deploy.
- If it is genuinely hand-maintained, leave it — the skip is correct.

### Symptom

`FileExistsError` on a destination like `~/.config/opencode/agents`, or deploy refuses to
write into a destination directory.

### Cause

Debris from the pre-split symlink deployment: the destination root is a symlink (often
dangling) pointing into this repo.

### Fix

- Deploy self-heals this: a destination root that is a symlink pointing into the repo (or
  dangling) is unlinked and replaced with a real directory. Rerun `python3 deploy_agents.py`.
- A symlink pointing somewhere *else* is treated as foreign and skipped — remove it by
  hand if you want deploy to manage that path.

### Symptom

`[tools] WARNING: <name> could not be set up (...). Continuing without it` during deploy.

### Cause

Deploy tried to bootstrap an optional companion tool (code-review-graph or Context7)
and the prerequisite was missing or the installer failed — for example, no `npx` on
PATH means Node.js is not installed, so Context7 cannot be configured; no `pip`/`pipx`
means code-review-graph cannot be installed.

### Fix

- The warning is non-blocking: agent assets still deployed. Install the missing
  prerequisite (Node.js for Context7; pip or pipx for code-review-graph) and rerun
  deploy, or pass `--skip-tools` to silence the bootstrap entirely.

### Symptom

The baseline `CLAUDE.md`/`AGENTS.md` contains a duplicate section, or a stale section
deploy does not update.

### Cause

Deploy only manages content between matching sentinel comments (`<!-- context7 -->`,
`<!-- code-review-graph -->`, `<!-- agent-discovery -->`). A hand-written copy of the
same guidance outside sentinels (for example, an old unsentineled discovery section) is
foreign content and is deliberately left alone, so it coexists with the managed block.

### Fix

- Delete the unsentineled duplicate by hand and rerun deploy; the sentinel-wrapped
  version is refreshed automatically.
- If the same guidance also lives in a separate rules file (for example an old
  `~/.claude/rules/context7.md`), delete that file to avoid double-loading.

### Symptom

A harness cannot see a deployed skill or agent.

### Cause

`ports/` was not regenerated before deploy, the destination differs from the expected env
variable, or the harness session is stale.

### Fix

- Run the transform to a fixed point, then rerun deploy.
- Check `python3 deploy_agents.py --list` to see the resolved destinations (and whether
  `CLAUDE_CONFIG_DIR` / `CODEX_HOME` / `OPENCODE_CONFIG_DIR` are redirecting them).
- Restart the harness session so it rediscovers the deployed files.

## Documentation Drift

### Symptom

Counts in `README.md`, `docs/ARCHITECTURE.md`, and `docs/CODEBASE_CONTEXT.md` disagree.

### Cause

Agent, skill, instruction, or learnings inventories changed without updating the standard
docs as a set.

### Fix

- Recount the actual files under `source_of_truth/{agents,skills,instructions,learnings}`
  and update all three overview docs in the same change.

### Symptom

`test_retirement_reconciliation.py` fails with `disk holds N, but the surface still
claims M`.

### Cause

You added or removed agents, skills, or instructions, and a count claim in `README.md`,
`CONTRIBUTING.md`, or `docs/CODEBASE_CONTEXT.md` still states the old number. The guards
read the real count from disk and compare.

### Fix

- Recount from disk — do not arithmetic a new number out of the old one. Counts appear in
  more than one place per file (prose *and* a directory tree), and the guards check all of
  them.
- Per-harness port counts also live in the comment block and `roots` list of
  `test_marker_guard_matches_every_real_generated_file`; update both together.

### Symptom

`test_eval_grader_retirement.py` fails with `ledger instrumentation reappeared`.

### Cause

Something under `source_of_truth/` referenced `ledger-events.jsonl`, `eval/runs/`,
`remediation-ledger-contract`, or another archived-grader token. The eval-grader system was
retired precisely because that instrumentation loaded into context on nearly every coding
task.

### Fix

- Remove the reference. Nothing consumes those files — the grader lives in `eval/deprecated/`
  and no agent writes ledgers any more.
- If you genuinely want ledger capture back, make it opt-in per run rather than an
  always-applied instruction, and read `eval/deprecated/README.md` first.
- If the file is a historical record rather than live wiring, add its directory to
  `EXEMPT_PREFIXES` in that test — with a comment saying why.

### Symptom

Docs mention `nodejs/`, `python/`, `HARNESS_SETUP.md`, `.mcp.json`, `codex/README.md`,
`scripts/setup-hook-symlinks.sh`, `source_of_truth/hooks/`, or
`scripts/runtime_deployment.py`.

### Cause

Those surfaces were removed. Most went in the `source_of_truth/`/`ports/` restructure, which
older docs describe as a `.github/` → `claude/`/`codex/`/`opencode/` layout. The hook
installer and `source_of_truth/hooks/` went with the retired prompt-injection scanner —
the script called a `--global-output` flag `propagate_master_assets.py` no longer accepts.

### Fix

- Treat `source_of_truth/` as the authoring surface and `ports/` + `.github/` as
  generated outputs. Delete stale references to the removed paths.
