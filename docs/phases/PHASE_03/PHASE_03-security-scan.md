# security-scan (diff-scoped): PHASE_03 — PR Review agent family

> **Supersedes** the historical full-codebase scan previously at this path (Phase 05
> numbering, revision `4484f0f`). That report is preserved in git at blob
> `87670c68a54b91c725a18395240bda16e1d3fbc3`, retrievable with
> `git show ae9823a:docs/phases/PHASE_03/PHASE_03-security-scan.md`. Its findings are
> reconciled against final state in § "Reconciliation with the superseded scan".
> This report is **diff-scoped**, not a whole-repository scan — see § "Coverage limits".

## Scan Metadata

- **Diff range**: `ae9823a..HEAD` on branch `phase/pr-review` (17 commits).
- **Scope**: 276 changed files, +19,294 / −7,503. Composition: agent Markdown, skills,
  generated harness mirrors (`claude/`, `codex/`, `opencode/`), pipeline records under
  `dev/feature/01..08`, tests, and **one** substantive executable change —
  `scripts/propagate_master_assets.py` (+231 / −58).
- **Phase artifacts reviewed**: `PHASE_03_SUMMARY.md`, `PHASE_03_DISCOVERY_CONTEXT.md`,
  `dev/feature/phase-03-pr-review-execution-manifest.md`, all eight feature
  plan/context/tasks/implementation/review records, the `05*` source agents, the four
  PR-review skills, and `.github/learnings/cross-phase-decisions.md`.
- **Method**: static review plus **direct dynamic verification** of the propagator's
  deletion path in isolated sandbox copies (no repository file was modified). Every
  behavioural claim below marked "Reproduced" was executed, not inferred.
- **No source, test, configuration, or generated file was modified.** No secret value is
  reproduced in this report.

## Verdict

- **Pass with Conditions**
- Finding totals: **0 Critical, 1 High, 2 Medium, 1 Low, 1 Informational**.
- Phase relationship totals: **1 Worsened, 1 Introduced, 1 Accepted/Routed,
  1 Residual-by-design, 1 Verified-open.**
- **Condition**: the single High (`P3-SEC-01`) is a containment gap on the propagator's
  newly-live deletion path. It is a direct extension of pre-existing `REPO-SEC-06` from
  *writes* to *deletes*, is reproducible, and requires an attacker who can already plant a
  symlink in the repo layout. It does not block the agent family's contracts, but it
  should be closed by the same phase that owns propagator containment.

---

## Executive summary

The phase's security-relevant surface is much narrower than its file count suggests. Of 276
changed files, exactly one has runtime behaviour: `scripts/propagate_master_assets.py`. The
rest is Markdown whose safety properties are enforced only by test assertions over prose.

Three things were checked hardest, and two came back clean:

1. **The orphan-pruning guard fails closed.** Verified by execution, not reading.
2. **The one-way PR-posting boundary is now genuinely enforced.** Feature 07's reviewer
   caught it inert and repaired it; the repair holds.
3. **The prune's containment does not survive a symlinked generated root.** This is the
   High.

The most notable positive result: the phase's own docstring claims the old prune "matched
0 of 24 files for years while reading as implemented." **This was verified true** — at
baseline `ae9823a`, 0 of 24 `codex/skills/*/SKILL.md` files matched the old `startswith`
check. The phase's self-assessment is accurate and unflattering, which is the right
posture. It also means the deletion capability is **genuinely new in this phase**, not a
modification of working code — which is precisely why `P3-SEC-01` matters.

---

## Findings

| ID | Severity | Category | Evidence | Relationship | Status |
|----|----------|----------|----------|--------------|--------|
| P3-SEC-01 | **High** | Filesystem containment / deletion | `scripts/propagate_master_assets.py:216-247`, `:250-271` | Worsened | Open |
| P3-SEC-02 | Medium | Delegation authorization | `.github/agents/05b-change-narrator.agent.md:4` | Introduced | Open |
| P3-SEC-03 | Medium | Process/runtime authorization (`execute` grants) | `.github/agents/05-pr-review.agent.md:5`; `05a-baseline-worktree.agent.md:4` | Carried, narrowed | Accepted / Routed |
| P3-SEC-04 | Low | Marker-guard residual | `scripts/propagate_master_assets.py:159-171` | Residual by design | Accepted |
| P5-SEC-02 | High (inherited) | AI trust boundary | `.github/agents/05g-readiness-synthesizer.agent.md:77-85` | Pre-existing | **Verified recorded OPEN** |

---

### P3-SEC-01 — Prune deletion escapes the repository root through a symlinked generated root — **High, Worsened**

**Evidence**: `_prune_orphaned_outputs` (`scripts/propagate_master_assets.py:216-247`) and
`_prune_orphaned_skill_dirs` (`:250-271`).

Both functions guard the **leaf**:

- `_prune_orphaned_outputs` skips `path.is_symlink() or not path.is_file()`.
- `_prune_orphaned_skill_dirs` skips `dest_dir.is_symlink()` and `skill_md.is_symlink()`.

Neither guards the **parent root**, and neither applies a canonical-realpath containment
check before `path.unlink()` / `shutil.rmtree(dest_dir)`. If a generated root itself
(`claude/skills`, `claude/agents`, `codex/agents`, …) is a symlink pointing outside the
repository, `directory.is_dir()` follows it and returns `True`, `iterdir()` yields **real**
directories outside the repo, and the leaf symlink guards never fire because those entries
are not symlinks.

**Reproduced.** In an isolated sandbox with `claude/skills` symlinked to a directory
outside the repo root, containing one marker-carrying `SKILL.md`:

```
victim exists BEFORE: True
victim exists AFTER : False   <- delete escaped the repo root
skill_orphans_removed: 1
```

`shutil.rmtree` removed a tree outside the repository root. The equivalent applies to
`_prune_orphaned_outputs` via `unlink()`.

**Why "Worsened" and not "Pre-existing"**: the superseded scan recorded `REPO-SEC-06` as
`_write_if_changed` following symlinked parent directories on non-hook destinations — a
**write** redirection. This phase adds **deletion** on those same unprotected paths. The
baseline prune that might have carried this risk was **inert**: verified at `ae9823a`,
0 of 24 `codex/skills/*/SKILL.md` matched the old `startswith(GENERATED_SKILL_HEADER)`
check, because generated Markdown opens with YAML frontmatter and the marker sits below it,
not at byte zero. So the delete surface is live for the first time in this phase, across
five file roots and three skill roots.

**Impact**: a repository layout an attacker can influence (a planted symlink at a generated
root) plus a marker-carrying target yields deletion of user-writable files outside the
repository. `shutil.rmtree` makes this recursive.

**Mitigating factors** (why High and not Critical): the attacker must already be able to
write a symlink into the repo working tree — a substantial precondition that generally
implies broader compromise. The target must also carry the generated marker at the exact
emitter position, so arbitrary trees are not deletable. The prune is a local developer
script, not a network-reachable or CI-privileged path.

**Recommendation**: apply one no-follow, canonical containment contract —
resolve each generated root with `Path.resolve()` and assert
`repo_root.resolve()` is a parent — before any create/write/delete, and add symlinked-root
regression tests for every pruned subtree. This is the same fix `REPO-SEC-06` already calls
for; the delete path raises its priority. Route to the phase that owns propagator
containment (`REPO-SEC-06`'s owner).

---

### P3-SEC-02 — `05b-change-narrator` holds the `agent` grant with no `agents:` allowlist — **Medium, Introduced**

**Evidence**: `.github/agents/05b-change-narrator.agent.md:4` declares
`tools: [agent, read, search, edit]` and **no `agents:` key**.

`05b` is the only Phase 03 agent with a delegation grant and no delegation allowlist. Every
sibling constrains its targets explicitly:

- `05f-test-health.agent.md:5` — `agents: [Test - Analyst]`
- `05-pr-review.agent.md:6` — the full explicit evaluator roster

`05b`'s procedure (`:53-58`) calls for "hidden per-directory reader delegations" as a
context-pressure valve, but names no target agent. An unconstrained `agent` grant means the
delegation target is resolved at runtime by the model, and the roster it can reach includes
`Baseline Worktree` — which holds `execute`. This is an **indirect** path to shell for an
agent the phase's tool-grant posture describes as holding none.

**This does not falsify the phase's roster claim**, which is about *direct* grants and is
accurate: `05b`/`05c`/`05d`/`05e`/`05f`/`05g` hold no `execute`. It is a gap in the
narrower sense that the phase established the right pattern (`05f`) and did not apply it
uniformly.

**Mitigating factors**: `05b:58-59` records that reader delegations sit at depth 2 and that
Codex `agents.max_depth` defaults to 1, so the spawn is blocked by default there — and the
agent correctly documents that a blocked spawn does not raise but silently falls back
inline. There is no evidence of escalation intent; the prose scopes readers to a directory
chunk with a read-only contract. Unlike the `execute` grants in `P3-SEC-03`, **this one is
closable in Markdown today**, at the cost of one frontmatter line.

**Recommendation**: add an explicit `agents:` allowlist to `05b` naming only the reader
agent it intends to spawn (or remove the `agent` grant and rely on the documented serial
fallback, which the procedure already specifies as acceptable). One line; no hook required.

---

### P3-SEC-03 — Two `execute` grants remain, declared and unclosable at this layer — **Medium, Accepted / Routed**

**Evidence**: `.github/agents/05-pr-review.agent.md:5` (`tools: [agent, read, search, edit, execute]`);
`.github/agents/05a-baseline-worktree.agent.md:4` (`tools: [read, search, execute]`).

**Verified final roster** — enumerated directly from source frontmatter:

| Agent | `execute`? |
|---|---|
| `05-pr-review` | **yes** — `git` base derivation, `gh pr comment` |
| `05a-baseline-worktree` | **yes** — `git worktree`, no non-shell equivalent |
| `05b`, `05c`, `05d`, `05e`, `05f`, `05g` | no |

This matches the phase's stated posture exactly. The superseded scan's `P5-SEC-01` faulted
the orchestrator **plus three mechanical evaluators** (`05g`/`05j`/`05k` under the old
numbering) for holding `execute`. Those three are retired or narrowed; **the removals are
real and verified**.

**Assessment against the brief** — whether the residual is *honestly recorded*, not whether
it is closable here. It is:

- `PHASE_03_DISCOVERY_CONTEXT.md:116` records the mechanism precisely: Claude subagent
  `tools:` frontmatter accepts only bare tool names; `Bash(gh:*)` is an unresolved tool
  name and Claude Code refuses to launch the agent. No `permissions`/`allowed-tools`
  frontmatter key exists; `permissionMode` selects prompt handling, not command scope.
  Scoping exists only in non-per-agent settings rules or a per-agent PreToolUse hook.
- `PROJECT_ROADMAP.md:29` states the grants "stay open, declared with justification and
  routed to a hook-owning phase."
- Narrowing was by **removal only**, which is the only lever available at this layer.

The claim is technically correct and independently confirmed. Nothing is described as
closed that is not closed. **No new finding**; recorded to keep the residual visible.

**Recommendation**: no action in this phase. The receiving phase must implement per-agent
PreToolUse command scoping for these two agents and close `P3-SEC-03` with a runtime test.

---

### P3-SEC-04 — Positional marker guard: a hand-maintained file at the exact emitter position is indistinguishable from generated output — **Low, Residual by design**

**Evidence**: `_generated_marker_line_index` / `_is_generated_output`
(`scripts/propagate_master_assets.py:159-171`, `:190-213`).

The guard identifies generated output by the marker at **one** line index: line 0 for
frontmatter-less files, else the line immediately below the closing `---`. Any
hand-maintained file placing the marker at exactly that position would be pruned.

This residual is **inherent to marker-based identification** and the chosen design is the
best of the available options — the code documents both alternatives and why they are worse
in opposite directions (`startswith` under-matches and is what silently disabled the prune;
a whole-file search over-matches and would delete any README that merely quotes the
convention). No real file hits the residual.

**Verified fail-closed by execution.** Guard evaluated against every file in all five
pruned roots at HEAD:

```
claude/agents:   28 files, UNMARKED (safe from prune) = ['README.md']
claude/commands: 19 files, UNMARKED = []
opencode/agents: 41 files, UNMARKED = []
codex/agents:    41 files, UNMARKED = []
codex/profiles:  19 files, UNMARKED = []
```

`claude/agents/README.md` — the hand-maintained file inside a generated root that AC5 exists
to protect — is the sole unmarked file and is correctly excluded. It does not contain the
marker string anywhere.

**Adversarial sandbox test**, four cases, all correct:

| Case | Expected | Result |
|---|---|---|
| Hand-maintained doc quoting the marker in a fenced code block | survive | **survives** |
| Doc with frontmatter, marker quoted lower in the body | survive | **survives** |
| Genuine stale generated orphan | pruned | **pruned** |
| Unterminated frontmatter (index `-1`) | survive (fail closed) | **survives** |

**Idempotency / fixed point**: two consecutive `propagate_once` runs in a full sandbox copy
returned all-zero orphan counters and left `README.md` byte-identical. The prune correctly
runs only after all emission completes (AC6), so filename resolution against on-disk stems
cannot be perturbed by a deletion.

**Recommendation**: accept. Optionally note the residual in `claude/agents/README.md` so a
future editor does not place the marker at line 0.

---

### P5-SEC-02 — Readiness-report trust boundary — **Inherited High, verified recorded OPEN**

Per the scan brief this is **not** re-raised as a new finding; the check is whether it is
honestly recorded open rather than quietly closed by prose. **It is.**

Confirmed at:

- `.github/agents/05g-readiness-synthesizer.agent.md:77-85` — declared open in the agent.
- `.github/learnings/cross-phase-decisions.md:88-108` — owner and routing recorded.
- `dev/feature/phase-03-pr-review-execution-manifest.md:86` — pre-assigned to feature 07
  and *expected to remain open*, with the instruction not to close it by firming up prose.
- `dev/feature/07-…-implementation.md:52` — recorded OPEN, guarded by
  `test_p5_sec_02_is_recorded_open_in_the_synthesizer`.
- `dev/feature/08-…-review.md:222` — independently re-verified still open.
- `PHASE_04_SUMMARY.md:68` — receiving phase acknowledges it as an open High.

Feature 07's reviewer mutation-tested the **negation** (flipping the declaration from open
to closed) and confirmed the test trips — so the record cannot silently drift to "closed"
(`07-…-review.md:63-64`). This is the correct handling of an unclosable finding: the phase
records it rather than redefining it to fit scope.

---

## Prompt-injection boundary — one-way PR posting

The brief flags this as the phase's key injection boundary: nothing may read PR comments or
network-sourced text back into the agent. **Verified enforced.**

- `.github/agents/05-pr-review.agent.md:229-230` — output is one-way; never read PR
  comments, review threads, or other network-sourced text.
- `:345-347` — restates it on the posting path specifically: post and read nothing back; do
  not fetch the posted comment to confirm; do not read existing comments to check whether a
  report was already posted.
- The only network verb is `gh pr comment --body-file <path>` (`:300`) — write-only. It
  resolves the PR from the current branch, so no PR number is read in. Its sole return
  consumed is the comment URL (`:324`), which is `gh`-generated, not attacker-authored
  content.

**The guard was inert and was repaired.** Feature 07's reviewer recorded this as Issue #3,
its most serious finding (`07-…-review.md:80`): the one-way clause added at `:345-347` could
be deleted with the test suite green, because `test_output_to_the_pull_request_is_one_way`
pinned only feature 04's pre-existing sentence at `:229-230`. AC9 — a prompt-injection
boundary — was unguarded on the exact path that posts. Fixed via two `_assert_once` pins
(`07-…-review.md:102`). Related Issue #4 (High): the `gh pr comment` command itself, the
mechanism AC7's consent gate actuates, could be deleted with the consent test green — every
assertion covered the *choice*, none covered the thing the choice actuates. Also fixed.

**Consent gating** (`:309-315`): opt-in, chosen upfront — *post automatically* /
*ask once written* / *never*. The **never** path is specified to make no `gh` invocation and
no network call. The choice is asked upfront rather than after work is on disk (`:57`), and
the prompt must state the cost of *post automatically* plainly (`:47`), noting a posted
comment cannot be unposted by reverting (`:52`). This is sound consent design.

**Caveat**: enforcement is prose plus test assertions over prose. Feature 07's own reviewer
flags AC7/AC8 as "Met (statically); **runtime unverified**" (`07-…-review.md:46-47`) and
notes the posting path's correctness "rests entirely on prose contract assertions"
(`:151-152`). See § "Coverage limits".

---

## Systemic observation — the inert-guard defect class

Not a security finding, but it is the reason two High-severity boundary guards in this phase
were non-functional, and it bears on how much assurance the Markdown-plus-tests model
carries.

Feature 07's review records the defect class recurring in **four consecutive features**
(04: 5 inert; 06: 4 inert; 07: 5 inert), every time from the same cause, and **every time
caught by the reviewer rather than the implementer's own sweep** — including the
implementer's round-2 sweep that self-reported "0 inert at final state"
(`07-…-review.md:22-26`, `:145-150`). The `_assert_once` helper is the correct structural
fix and works; the gap is that implementers sweep the assertions they already suspect.

This matters to security specifically: an inert guard on a prompt-injection boundary is
indistinguishable from an enforced one at review time unless someone mutation-tests it. The
phase's own conclusion is right — **the sweep must enumerate every assertion mechanically,
not by intuition.** The propagator's `startswith` bug is the same class in code: a check
that read as implemented and matched 0 of 24 files.

---

## Reconciliation with the superseded scan

| Prior finding | Prior status | Final state |
|---|---|---|
| `P5-SEC-01` — `execute` on orchestrator + 3 mechanical evaluators; no allowlist; parity test omits `05g`/`05j`/`05k` | High, Introduced, **BLOCKED** | **Substantially reduced.** Evaluator grants removed and verified; retired agents deleted. Residual = `P3-SEC-03` (2 grants, declared/routed) + `P3-SEC-02` (05b delegation). |
| `P5-SEC-02` — readiness-report trust boundary | High, Introduced | **Verified recorded OPEN** with owner + routing. Not closed by prose. Per brief, not re-raised. |
| `REPO-SEC-06` — `_write_if_changed` follows symlinked parents on non-hook destinations | High, Worsened | **Still open and further worsened** → `P3-SEC-01`. Now applies to deletion, reproduced. |
| Phase 02 `P2-SEC-01..03` | High, unresolved | **Out of diff scope.** Not re-assessed; routed to Phase 04 per `PROJECT_ROADMAP.md:29`. |

The prior scan's **BLOCKED** verdict rested on `P5-SEC-01` + `P5-SEC-02` + `REPO-SEC-06` +
unresolved Phase 02 Highs. At diff scope, `P5-SEC-01` is substantially closed, `P5-SEC-02`
is correctly recorded open with routing, and the Phase 02 findings are explicitly Phase 04's.
The one High this scan raises is a containment gap on a newly-live delete path with a
significant attacker precondition. That supports **Pass with Conditions** at diff scope —
it does **not** overturn the phase-level gate, which is a whole-repository question and the
user's to issue by hand.

---

## Verified clean

- **Secrets**: no hardcoded credential material in the diff. Scanned all added lines across
  the full `ae9823a..HEAD` range for AWS keys, GitHub PATs, Slack tokens, OpenAI-style keys,
  PEM private-key headers, and quoted credential assignments. **Zero hits in every
  category.** No secret value is reproduced here.
- **Retirement completeness**: `05h`–`05l` are deleted from `.github/agents/` and **zero**
  survivors exist anywhere in the tree (filesystem-wide search). No orphaned generated
  mirror in `claude/`, `codex/`, or `opencode/`.
- **`.gitignore` change**: correct and consistent. The removed `dev/phase-final-review/`
  un-ignore entries follow the family's retirement — those fixtures are deleted at HEAD
  (0 tracked files), so no tracked path is silently untracked. The replacement correctly
  tracks `dev/pr-review/fixtures/` while leaving run output ignored. Verified with
  `git check-ignore`.
- **Tests**: 150 passed + 106 subtests across the five Phase 03 test files. No new failure.
- **Propagator repo_root parameterization**: the added `repo_root` parameters thread a caller
  path into `load_source_agents` / `load_instruction_docs` / `propagate_once`. All call sites
  default to the module-level `REPO_ROOT`; the parameter is test-injection scaffolding and
  introduces no untrusted-input path (no CLI flag or env var feeds it).
- **PERF-01**: out of scope per brief. Confirmed not a Phase 03 regression.

---

## Coverage limits — what this scan could NOT assess

1. **Diff scope only.** This is not a whole-repository scan. Unchanged code, dependencies,
   CI/CD, and infrastructure were not re-assessed. Phase 02's `P2-SEC-01..03` remain
   unresolved and unexamined here.
2. **The agent family has never been run.** The fixture dry run is an open gap, so every
   agent-behaviour property below is **statically verified only** — asserted against
   Markdown prose by tests over that prose, never observed at runtime:
   - that *never* consent truly issues no syscall (no process-level evidence);
   - that `gh pr comment` resolves the PR from the branch as documented;
   - that the one-way boundary holds under an actual injection attempt in a real PR;
   - that `05b`'s delegation is in fact bounded to readers at runtime (`P3-SEC-02`);
   - that depth-2 spawn blocking behaves as `05b:58-59` documents.
   A test asserting a sentence exists in a Markdown file is evidence about the file, not
   about the agent's behaviour. Feature 07's reviewer reaches the same conclusion
   independently (`07-…-review.md:46-47`, `:151-152`).
3. **Prose-enforced contracts are unenforceable at this layer.** Read-only and no-write-back
   constraints are model instructions, not sandbox boundaries. `edit` is granted broadly
   across the evaluator roster and constrained only by prose — the mechanism `P5-SEC-02`
   and the superseded scan's `P5-SEC-03` both name.
4. **`P3-SEC-01` exploitability** was demonstrated in a constructed sandbox. Whether a
   real attacker can plant the prerequisite symlink depends on repo-layout trust not
   assessable from the diff.
5. **Generated mirrors** (`claude/`, `codex/`, `opencode/`) were checked for parity and
   orphan hygiene, not treated as independent finding sources.

## Recommended actions

| Priority | Action | Owner |
|---|---|---|
| 1 | Close `P3-SEC-01`: canonical no-follow containment on every generated root before create/write/delete; symlinked-root regression tests per subtree. Closes `REPO-SEC-06` on the same pass. | Propagator/containment phase (Phase 04 candidate) |
| 2 | Close `P3-SEC-02`: add an explicit `agents:` allowlist to `05b`, matching the `05f` pattern. Closable now, one line. | This phase or Phase 04 |
| 3 | Execute the fixture dry run. It is the only thing that converts limits 2 and 3 into evidence. | Phase 04 QA |
| 4 | `P3-SEC-03` + `P5-SEC-02` close in the hook-owning phase, per existing routing. No action here. | Phase 04+ |
