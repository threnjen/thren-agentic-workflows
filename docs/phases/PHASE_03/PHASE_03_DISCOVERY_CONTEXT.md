# Phase 03 Discovery Context

Context gathered during refinement of Phase 03 that is not recoverable from the
codebase alone. Downstream agents should read this before decomposition so the
user does not have to re-provide it.

## A branch's base cannot be determined from git

This was investigated empirically in this repository rather than assumed. The
conclusion drives the orchestrator's entire interaction model, so the evidence is
recorded here in full.

**A ref is only a SHA.** Git's data model stores no parentage for a branch — a
branch is a movable pointer to a commit, and nothing in the ref records which
branch it was cut from.

**`git merge-base HEAD <base>` is exact but circular.** It answers "where did
these diverge" only once you already know the base. It cannot discover one. In
this repo, `git merge-base HEAD main` returns `e3398c7`, which is correct — and
useless for discovery, because supplying `main` was the hard part.

**The reflog does not help.** It records `branch: Created from HEAD` — the SHA,
never the branch name. It is also local-only (never cloned), and gc-pruned at 90
days by default.

**`origin/HEAD` names the wrong thing, and is often absent.**
`git symbolic-ref refs/remotes/origin/HEAD` returns `refs/remotes/origin/main` in
this repo, but it names the remote's *default* branch — not *this branch's* base.
It is also unset in many fresh clones, so it cannot be relied on for a propagated
asset that ships to other projects.

**The obvious heuristic has a trap, demonstrated live.** "Pick the branch whose
merge-base with HEAD is nearest" returns the branch under review. Measured on
branch `repo_improvements_project` at HEAD `ae9823a`:

| Ref | `git merge-base HEAD <ref>` |
|---|---|
| `main` | `e3398c7` |
| `origin/main` | `e3398c7` |
| `repo_improvements_project` | `ae9823a` — HEAD itself |
| `origin/repo_improvements_project` | `ae9823a` — HEAD itself |

A branch is always its own nearest base, and so is its remote-tracking ref. Any
suggester must exclude both explicitly.

**Conclusion**: suggest-and-confirm. The suggestion order is `origin/HEAD` →
`origin/main` → `origin/master` → present candidates. The user confirms or
corrects. This matches the suggest-and-confirm preflight pattern this repo already
uses elsewhere.

**Cases where the suggestion will be wrong**, which is why correction is
first-class rather than an escape hatch:

- a branch cut from another feature branch, not the default branch;
- a rebased branch, whose merge-base no longer reflects where work began;
- a base that was squash-merged, leaving no shared commit at all.

## Existing assets that shaped the scope

- **`04e-diff-security-scan`** already exists and is diff-shaped: it accepts a
  changed-file list or a `git diff --name-only <baseline>..HEAD` range, holds no
  `execute`, is `user-invocable: false`, and declares its diff-scope limitations
  explicitly. It is the reason this phase authors no new security agent. The
  retired `05d-security-rollup` was a *rollup* of per-subphase reports — a shape
  with no PR analogue — but the security check itself still applies to a diff.
- **`prod-code-review`** cross-validates pipeline documents across a phase's
  features and produces a go/no-go. It overlaps PR Review on outcome but not on
  axis: it is document-driven and phase-scoped; PR Review is diff-driven and
  branch-scoped, and treats pipeline documents as optional enrichment. Making
  artifacts optional in PR Review is what keeps the two from being the same agent.
- **`04-phase-execute` + `04a`–`04e`** establish the numbered-orchestrator +
  lettered-subagent house style this phase follows.

## Why the rescope shrank the phase

The original scope was built around a multi-subphase phase. Removing that premise
deletes, rather than rewrites, a large fraction of the work:

- subphase discovery, and the refusal message that pointed single-phase users at
  `prod-code-review`;
- ledger parsing (`eval/runs/*/ledger-commits.jsonl`), multi-run disambiguation,
  and the `eval:` commit-message fallback — all of it replaced by `merge-base`;
- the "ledger reality" dependency and risk, which existed only because ledgers are
  gitignored and local-only;
- the artifact-inventory refusal gate, now that artifacts are optional;
- the entire verdict write-back path: two-file transactional edits of
  `PROJECT_ROADMAP.md` and `PHASE_0N_SUMMARY.md`, unique-match ambiguity detection,
  and restore-on-second-write-failure. This was the riskiest implemented code in
  the phase and the rescope leaves it with no reason to exist.
- archive-before-overwrite, since a SHA+timestamp report root gives every run its
  own directory.

## Why the interaction model is a hard requirement

The user's stated requirement is that questions arrive up front so an unattended
run is never found stuck. The design decisions above make this achievable rather
than aspirational: with ledger disambiguation, artifact refusal, and write-back
ambiguity all gone, **base confirmation is the only blocking question left in the
run**. The PR-comment choice joins it in the same block.

The *ask once the report is written* option is worth understanding precisely: a
prompt after the report exists does not block anything, because the work is
already on disk. That is what makes it possible to both run unattended and see
what gets published before it is published.

## Per-agent command scoping is not expressible — harness research

Posting to a PR needs `gh`, and `scripts/propagate_master_assets.py:332` maps
`"execute": ["Bash"]` while `:353` maps `"execute": ["bash"]`, with no allowlist
syntax anywhere. The obvious conclusion — add allowlist syntax to the propagator —
does not survive contact with the harnesses it emits to. Researched against current
documentation rather than assumed:

| Harness | Per-agent command scoping | Detail |
|---|---|---|
| **Claude Code** | **No** | A subagent's `tools:` frontmatter accepts only bare tool names and MCP patterns. A command-scoped entry such as `Bash(gh:*)` is an *unresolved tool name*, and Claude Code refuses to launch the subagent. There is no `permissions` or `allowed-tools` frontmatter key; `permissionMode` selects how prompts are handled, not which commands run. Scoping exists only in project/session-wide settings rules — which are not per-agent — or in a per-agent **PreToolUse hook**. |
| **OpenCode** | **Yes** | Per-agent `permission.bash` accepts glob patterns in frontmatter or `opencode.json`. Rules are **last-match-wins**, so the `"*"` catch-all must come **first** and specific allows after. Patterns match the *parsed* command, so `"git status"` does not match `git status --short` — use `"git status *"`. Defaults are permissive; deny-all-plus-allowlist must be written explicitly. |
| **Codex** | **No** | The `ConfigProfile` backing `[profiles.*]` carries only `approval_policy`, `approvals_reviewer`, `sandbox_mode`, and `tools` — no command list. Its execpolicy *rules* system does allowlist commands, but it is global (not per-agent), governs only commands run **outside** the sandbox, is Starlark rather than TOML, and is explicitly experimental. `AGENTS.md` is model-directed prose, not a permission boundary. |

So the propagator was never the binding constraint: the *target formats* cannot
express the result. Emitting allowlist syntax would be real on one of three
harnesses and decorative on the other two — the "partial protection that reads as
total protection" failure this project already records under adoption readiness,
aimed at ourselves.

**The premise failed on its own terms as well.** The reasoning was "granting `gh`
means granting every shell command, which two recorded decisions prohibit." But the
orchestrator needs `git symbolic-ref`, `git merge-base`, and `git branch` for base
derivation, so it holds unrestricted Bash regardless of whether PR posting exists.
Adding `gh` widens nothing.

**What remains is narrowing by removal**, which *is* expressible: drop `execute`
from evaluators that need no shell command, never add it to those that lack it, and
declare it with a named command where it is genuinely required. Per-agent command
scoping is deferred to a hook-owning phase.

## The propagator prunes almost nothing, and one prune is dead code

Measured in this repository:

| Root | Prunes orphans? | Evidence |
|---|---|---|
| `codex/agents/*.toml` | yes | 46/46 carry the guard's header marker |
| `codex/profiles/*.config.toml` | yes | same guard |
| `codex/skills/*/` | **no — dead code** | **0/24** match its `startswith` guard; the marker sits on line 5, below the YAML frontmatter |
| `claude/agents/*.md` | no | 0/35 carry any marker |
| `claude/commands/*.md` | no | 0/19 carry any marker |
| `opencode/agents/*.md` | no | 0/46 carry any marker |
| `claude/skills/`, `opencode/skills/` | no | byte-identical source copies; no marker at all |

No root prunes skills. Only Codex prunes agents. The single existing Claude-side
removal fires only when an agent is *reclassified* to command-only, never when a
source agent is deleted.

Three consequences shaped the scope. The phase's own success criterion — retired
evaluators absent from all three generated roots — is unsatisfiable without new
pruning. `claude/agents/README.md` is a hand-maintained file inside a generated
root, so an expected-set sweep with no guard would delete it. And renaming is
asymmetric: Claude filenames key on the agent's *display name* and survive a
renumber, while OpenCode filenames key on the *slug* and orphan — so OpenCode
orphans are the ones a reviewer's eye will miss.

The sharpest single case: renaming the orchestrator strands
`claude/commands/phase-final-review.md`, which remains a **live, user-invocable
slash command pointing at a deleted agent**.

## Codex depth limit turns delegation into silent reimplementation

`max_depth` defaults to **1**, and a blocked spawn causes a **silent inline
fallback** — the agent performs the work itself and reports success. Recorded in
`.github/learnings/debugging-learnings.md`. Both `05f`→`test-analyst` and
`05b`→per-directory readers sit at **depth 2**.

This matters because the phase's delegation criteria are otherwise verified by
asserting that the agent body says it delegates. Under the fallback, the body is
correct and the runtime is not, so the assertion passes while the contract breaks.
Delegation must be verified from a runtime transcript.

## Decisions taken during refinement

| Decision | Choice |
|---|---|
| Pipeline artifacts | Optional enrichment; the run proceeds on the diff alone and says so |
| Verdict destination | Report file only; no roadmap or summary write-back |
| Retired evaluators | Deleted from source and from all three generated roots |
| Surviving slugs | Renumbered contiguously `05a`–`05g` |
| Report root | `dev/pr-review/<base-sha-short>-<UTC-timestamp>/` — no branch name in any path |
| Gate strength | Advisory now; an enforcement hook is deferred to a hook-owning phase |
| Base fallback | `origin/HEAD` → `origin/main` → `origin/master` → present candidates |
| Fixture | Subphase fixture retired; a pinned real base/branch SHA pair replaces it, sized to a realistic pull request |
| PR comments | Opt-in, chosen upfront: auto / ask-when-ready / never |
| `gh` grant | No allowlist. Per-agent command scoping is not expressible on Claude and is deferred to a hook-owning phase; the orchestrator already holds unrestricted Bash for base derivation, so `gh` adds no exposure |
| `execute` narrowing | By **removal** only — dropped where unneeded, declared with a named command where required (`05a`'s `git worktree`, the orchestrator's `git`/`gh`) |
| Propagation pruning | Added as the phase's first deliverable; without it every retirement and rename strands a live artifact in the generated roots |
