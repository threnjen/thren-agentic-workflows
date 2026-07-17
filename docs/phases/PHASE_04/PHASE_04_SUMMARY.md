# Phase 4: Guard Accuracy & Propagation Reach

**Status**: Planned
**Depends on**: Phase 01 (both the file-access guard and the propagator ship there)
**Estimated complexity**: Medium
**Cross-references**: `.agent/logs/file-access-guard.ndjson` (the friction evidence), `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md`, `.github/learnings/cross-phase-decisions.md` (§ Guard Friction and Command Prompting; § File-Access Guard Retirement), `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` (the superseded user-global symlink flow), `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` (the registry-wiring gap this phase closes)

## What's New

Two tools stop being in your way.

The file-access guard hard-denies `grep -rn "test*" .` as a *Kubernetes credentials* access. Not a prompt — a denial, with no override. It did that 18 times in a single working session, every instance a false positive, and it blocked the investigation into itself twice. This phase fixes the defect behind it **without editing, weakening, or deleting a single rule.**

Propagation writes agents to `claude/agents/` — a directory nothing reads. Claude Code reads `~/.claude/agents/`. That last hop has always been a manual step nobody wrote down, which is why seven PR Review evaluators were invisible to their own live orchestrator while every one of their tests passed. This phase makes the propagator finish the job it starts.

## Objective

Fix the guard's false-positive path extraction and extend propagation to the user-global paths harnesses actually read, so the hook suite stops obstructing ordinary work and generated assets become live without a manual step.

## Scope

### In Scope

- **GUARD-01 — candidate extraction**: `grep`/`rg`/`egrep`/`fgrep` pattern operands must not be evaluated as filesystem paths. This is the entire false-positive class.
- **Friction re-measurement from evidence**: the audit log is the instrument. The fix is verified by a fresh log over real work, not by assertion.
- **Symlink propagation (macOS)**: a user-global symlink layer in `scripts/propagate_master_assets.py` covering **agents, commands, and skills**, with discovery of `~/.claude/{agents,commands,skills}`, `~/.codex`, and `~/.config/opencode`.
- **Dangling-link pruning under a containment contract**: ten dangling links exist in `~/.claude/agents/` today, and every agent rename strands another.
- **Record correction**: the recorded friction analysis is disproven by the guard's own log and is rewritten from measurement.

### Out of Scope

- **Guard retirement.** Decided at refinement: fix the defect, keep the rules. The retirement proposal recorded in `cross-phase-decisions.md` is resolved by this phase, not carried forward.
- **Windows and Linux.** macOS only. There is no OS detection in the propagator today and effectively none is added — see Technical Context.
- **Hooks in the symlink layer.** Hooks ship as generated files with absolute commands, which superseded an earlier user-global symlink flow. That reversal stands.
- **Plugin packaging.** The sanctioned distribution mechanism, already deferred under adoption readiness. Symlinks serve the author's own machine; plugins serve shipping. Different phases.
- **New guard rules, patterns, or capability.**
- **`_glob_patterns_overlap` redesign.** It is correct and load-bearing. See Technical Context.
- **Verification of Phases 01 and 02.** No status line for either phase moves in this phase.

### Owned by Phase 07 — Not Addressed Here

Each item below is real, release-blocking, and **not addressed here**. All of them live in `docs/phases/PHASE_07/PHASE_07_SUMMARY.md`, which is the only route to a release verdict for Phases 01 and 02. Phase 07 runs after this phase and before Phases 05 and 06, per the roadmap's dependency column.

| Item | Why it still matters |
|---|---|
| **PERF-01 latency gate reshape** | Phase 01's release blocker. The approved reshape is a calibrated relative budget; the budget's meaning is unchanged and a deliberately slowed guard must still fail. Untouched by GUARD-01. |
| **Bash-rewrite bypass** (`rtk-rewrite.sh`) | A PreToolUse hook that rewrites `tool_input.command` can invalidate the guard's classification of that same command. Independent of GUARD-01 and still open after it. |
| **Phase 02 security gate re-run** | P2-SEC-01, P2-SEC-02 (all three overflow paths), and P2-SEC-03 are remediated in code and unverified. |
| **Guard-rule security review (17 loosened rules)** | The `legacy_bash_parity` loosening was never scanned or reviewed. GUARD-01 does not adjudicate it. |
| **REPO-SEC-06 containment** | The in-repo propagation write path. Adjacent to this phase's containment work but distinct from it. |
| **Live multi-harness QA** | Never run, for any phase. |
| **Record reconciliation** | DOC-01's `PENDING` commit SHAs; the project-root hook-command anchoring record. |

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | A guard that does not fire on grep | GUARD-01 closed: search patterns are not path candidates. No rule edited. | Guard extraction |
| 2 | Evidence the friction is gone | A fresh audit-log measurement over real work showing zero false-positive denials. | Guard extraction |
| 3 | Propagation that reaches the harness | macOS user-global symlink layer for agents, commands, and skills. | Propagation reach |
| 4 | A prune that cannot escape | Dangling links removed under a contract that cannot delete a regular file or anything outside the repository. | Propagation containment |
| 5 | A corrected record | The friction entry rewritten from measurement rather than from config shape. | Records |

## Technical Context

### GUARD-01 — the defect is extraction, not policy

Reproduced by execution against `lib.bash_analyzer.analyze_command` with the live config:

| Command | Verdict | Assessment |
|---|---|---|
| `cat ~/.ssh/id_rsa` | DENY `ssh-rsa` | correct |
| `cat ~/.ssh/id_*` | DENY `ssh-rsa` | correct — the overlap check earning its keep |
| `cp ~/.ssh/id_rsa /tmp/x` | DENY `ssh-rsa` | correct |
| `grep -rn "foo*" .` | DENY `kubeconfig-file` | **false positive** |
| `rg "z-[a-z-]*" .` | DENY `kubeconfig-file` | **false positive** |
| `grep -rn "hello" .` | clean | correct |
| `ls ~/.ssh/id_rsa` | clean | **coverage hole** |

`_candidate_paths` in `.github/hooks/lib/bash_analyzer.py` extracts grep's **pattern** operand as a filesystem path. `evaluate_path` normalizes it to `<repo-root>/foo*` and hands it to `_glob_patterns_overlap` in `.github/hooks/lib/file_access.py`, which asks whether the candidate glob and the rule glob could both match some common string — and constructs the witness from literals scraped from **both** patterns. For `foo*` against the `kubeconfig-file` rule pattern `*kubeconfig`, it synthesizes `fookubeconfig`, observes that both match it, and denies.

The consequence is total: **any candidate ending in `*` overlaps any rule.** Every `grep` whose pattern ends in a wildcard is hard-denied.

**`_glob_patterns_overlap` is not the bug and must not be "fixed".** It is exactly what makes `cat ~/.ssh/id_*` deny correctly. Building the witness only from the candidate's own literals — the obvious cleanup — would break real secret detection. This is an inviting-looking wart that a future reader will want to tidy; the reason it looks wrong and is right belongs in a comment beside it.

The fix is command grammar: for `grep`, `rg`, `egrep`, and `fgrep`, the first non-option operand is a pattern rather than a path. Operand roles shift when `-e` or `-f` is present, and that shift is part of the deliverable.

Evidence base: `.agent/logs/file-access-guard.ndjson`, 22 events from one session — 18 `deny` and 4 `ask`. All 22 carry `tool: "Bash"`. Rule distribution: `kubeconfig-file` 10, `ssh-rsa` 5, `credential-json` 3, `destructive-rm-recursive-force-variants` 3 (`ask`, correct behavior), `environment-printenv` 1 (`ask`). Every one of the 18 denials matched a grep or glob pattern argument, not a file path.

### `ls` is not in the reader command set

`ls ~/.ssh/id_rsa` is clean while `cat ~/.ssh/id_rsa` denies. A genuine gap, surfaced while proving GUARD-01. Severity is arguable — `ls` discloses existence and metadata, not contents. Per the findings-containment rule below it is **Medium: record with routing**, not fix here.

### Propagation reach — the last hop is missing

`claude/agents/` is a *distribution* root. Claude Code reads `~/.claude/agents/`. Nothing connects the two but hand-made links, and that gap is the whole of the B1 blocker: an orchestrator went live while all seven of its evaluators were invisible, with a fully green suite.

What exists today: `generate_global_hooks` in `scripts/propagate_master_assets.py` wraps `propagate_hooks_once` with `copy_assets=False` and an absolute-command transform, driven by the `--global-output` flag. It performs **no** home-directory discovery — the destination is supplied entirely by the caller. Discovery lives instead in `scripts/setup-hook-symlinks.sh`, which despite its name uses `cp`, prints *"no user files are symlinks"*, hardcodes `$HOME/.config/opencode`, and covers **hooks only**.

Verified against current Claude Code documentation (see `PHASE_04_DISCOVERY_CONTEXT.md`):

- **`CLAUDE_CONFIG_DIR` does not exist.** Configuration paths are hardcoded. There is no environment variable to honor, which is most of why "OS detection" collapses to nearly nothing at macOS-only scope.
- **Symlinked skill directories are explicitly supported and documented.** Symlinked rules likewise. Claude follows the link and de-duplicates a target reachable from more than one location.
- **`~/.claude/agents/` is undocumented.** It demonstrably exists and is in use, but no documentation sanctions it.
- **Skills hot-reload; agents do not.** A newly added agent requires a session restart. Removals are detected — a dangling link fails to load — while additions are not.
- **Precedence is Enterprise > User > Project.** User-level *outranks* project-level.
- **Plugins are the sanctioned distribution mechanism.** Symlinking is documented as a personal workaround for one's own setup, which is precisely this phase's use case.

### Containment — the sharpest edge in this phase

`_validate_output_directory` and `_validate_nested_output_directory` in `scripts/propagate_master_assets.py` raise on any symlinked path component and require the target to resolve inside the repository. `generate_global_hooks` sidesteps both by passing the caller's output root as `repo_root`.

A user-global prune deletes **outside the repository**. That is the blast radius P3-SEC-01 hardened, and the reason its fix validates the root *before enumeration* rather than the leaf before unlinking. The in-repo marker guard does not transfer: a symlink carries no content of its own, so there is no marker to read without following the link.

Suggested containment shape, to be verified by Feature Decomposer against current code and tests:

> Remove a path from a user-global root only when it is a **symlink** whose resolved target lies inside this repository's generated roots and is absent from the current run's expected set. Never unlink a regular file. Never remove a directory tree. Never follow a link in order to decide whether to delete it.

### Test impact

- `tests/hooks/test_bash_command_analyzer.py` and `tests/hooks/test_file_access_guard.py` encode current extraction behavior and will need updates. The regression pair is the deliverable: the attack still blocks, the benign input passes.
- `tests/test_propagate_master_assets.py` gains the containment cases. Mirror the P3-SEC-01 sandbox scenarios: symlinked root, symlinked intermediate parent, and a legitimate prune that must still work.
- No fixture or rule config is edited to make any of the above pass.

## Dependencies & Risks

- **Risk — the guard fix weakens real detection.** Mitigation: `cat ~/.ssh/id_rsa` and `cat ~/.ssh/id_*` must both still deny, as explicit acceptance criteria. The temptation is to simplify `_glob_patterns_overlap`; that breaks the second one silently.
- **Risk — the prune deletes outside the repository.** The most dangerous code in the phase. Mitigation: the containment contract above, plus adversarial tests mirroring the P3-SEC-01 sandbox cases.
- **Risk — `~/.claude/agents/` is undocumented and the headline case rests on it.** Mitigation: the B1 dry run is this feature's feasibility test and runs first. If agent symlinks do not load, the feature is commands-and-skills-only and the roster problem needs a different answer.
- **Risk — user-level shadows project-level.** A global symlink outranks a project agent of the same name. Benign in this repository, which has no `.claude/agents/`; hostile in a consumer repository.
- **Risk — clobbering the user's own files.** `~/.claude/agents/` is hand-curated and holds both real user content and ten dangling links. Mitigation: the `backup_once` pattern already established in `scripts/setup-hook-symlinks.sh`.
- **Risk — whole-directory versus per-file symlinking is an open fork.** Commands and skills are whole-directory symlinks today; agents are per-file links inside a real directory. Whole-directory is simpler and self-pruning but claims the directory. Per-file preserves foreign entries but requires the prune. The two asset classes may not want the same answer, and the decision belongs to the feature that owns it.
- **Risk — a long-running `--watch` executes the propagation code it started with.** Propagator edits require a watcher restart. This phase edits the propagator.
- **Dependency — verification requires a fresh session.** The agent registry loads at session start and does not rescan.
- **Dependency — Codex and OpenCode user-global paths are lower-confidence.** No authoritative source was found for either. Verify before writing; record NOT RUN honestly where a harness cannot be checked.

### Findings containment rule

New findings surfaced during this phase are fixed here **only if High or Critical**. Medium and below are recorded with routing and deferred. The rule is not a lever: a finding is not promoted because fixing it is desirable, nor demoted because fixing it is inconvenient.

## Success Criteria

- [ ] `grep -rn "test*" .` and `rg "z-[a-z-]*" .` complete with no guard decision.
- [ ] `cat ~/.ssh/id_rsa` still denies.
- [ ] `cat ~/.ssh/id_*` still denies — the overlap check is preserved, not removed.
- [ ] **No rule pattern is edited and no rule is deleted to achieve the above.** The fix lives in extraction. A rule change that makes the friction disappear is a threshold edit wearing a different hat.
- [ ] A fresh `.agent/logs/file-access-guard.ndjson`, captured over a real working session after the fix, records zero false-positive denials.
- [ ] The `ls` coverage hole is recorded with routing.
- [ ] Propagation creates the user-global links on macOS, and a **fresh session** resolves every propagated agent, command, and skill.
- [ ] The prune removes a dangling generated link, and **refuses** to remove a regular file, a foreign symlink, and any path resolving outside the repository — each proven by its own test.
- [ ] The ten existing dangling links in `~/.claude/agents/` are resolved.
- [ ] Hooks still ship as generated files with absolute commands; the symlink layer does not touch them.
- [ ] The friction entry in `.github/learnings/cross-phase-decisions.md` states what was measured, and the retirement proposal is recorded as resolved.
- [ ] No status line for Phases 01 or 02 moves.

## QA Considerations

- **The B1 dry run runs first, not at the tail.** It is the propagation feature's feasibility test, and the phase's highest-uncertainty item.
- **Symlink QA requires a scratch consumer repository and a throwaway `HOME`.** A prune bug here deletes the author's real agent wiring. Live QA must never be self-administered against the working setup.
- The guard fix is verifiable from the audit log — the first item in this project with a live instrument rather than a fixture. Use it, and prefer it to reasoning about config.
- The guard's friction profile should be QA'd deliberately against ordinary work: `grep` with wildcard patterns, `rg` with character classes, lock-file reads, and commit messages mentioning `rm -rf` must not prompt or deny, while genuinely destructive commands must.
- Codex and OpenCode user-global discovery is unverified. Record NOT RUN honestly where a harness is unavailable; a missing check is a below-GO input, not an omission.

## Notes for Feature - Decomposer

Suggested feature boundaries, ordered so that feasibility is proven before the work that depends on it:

1. **GUARD-01 extraction fix** — self-contained, small, and the highest relief per line changed. Owns `.github/hooks/lib/bash_analyzer.py` and its tests. The regression pair (`id_rsa` denies, `id_*` denies, `grep "foo*"` clean) is the deliverable, not a nice-to-have — it is what distinguishes a fix from a loosening. Disjoint from everything else in the phase and parallel-safe.
2. **B1 dry run and symlink feasibility spike** — small and early. Confirms that `~/.claude/agents/` symlinks resolve at all, which is undocumented. Gates feature 3; if it fails, feature 3's scope changes rather than its schedule.
3. **Symlink propagation core** — macOS discovery plus link creation for agents, commands, and skills. Owns the whole-directory-versus-per-file decision and must record the rationale, since the two asset classes may diverge.
4. **Prune containment** — deliberately separated from feature 3 so it receives its own review. This is the code that deletes things outside the repository, and it should not be reviewed as a footnote to the feature that creates them.
5. **Record correction** — the tail. Rewrites the friction entry from measurement and records the retirement proposal as resolved.

Integration points to watch: features 3 and 4 both own `scripts/propagate_master_assets.py` and must be **sequential, not parallel**. Feature 1 touches no file the others touch. Feature 2 produces evidence rather than code, and its finding is an input to feature 3's acceptance criteria.

The phase's defining rule: **the friction fix is verified by measurement, not by assertion.** The audit log already exists and already disproved one confident analysis in this project; decomposition should make a fresh measurement an explicit deliverable rather than a side effect.
