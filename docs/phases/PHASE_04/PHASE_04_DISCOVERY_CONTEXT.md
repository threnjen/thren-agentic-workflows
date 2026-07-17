# Phase 04 Discovery Context

Context gathered during Phase 04 refinement that is not derivable from the codebase alone. Downstream agents should read this before re-deriving any of it.

## 1. Guard Friction — Measured, Not Estimated

### The instrument

`.agent/logs/file-access-guard.ndjson` — the guard's own audit log, configured via the `audit_log` key in `.github/hooks/config/file-access-rules.json`. It existed and had never been read. It is the only live behavioral instrument in this project; everything else is fixtures.

### The measurement

22 events from one working session. All 22 carry `tool: "Bash"`.

| Decision | Count |
|---|---|
| `deny` | 18 |
| `ask` | 4 |

| Rule | Fired | Tier | Assessment |
|---|---|---|---|
| `kubeconfig-file` | 10 | deny | all false positives |
| `ssh-rsa` | 5 | deny | all false positives |
| `credential-json` | 3 | deny | all false positives |
| `destructive-rm-recursive-force-variants` | 3 | ask | correct behavior |
| `environment-printenv` | 1 | ask | arguable |

Every one of the 18 denials recorded a `path` that is a grep pattern, a glob argument, or a regex — not a file path. Representative rows, verbatim from the log:

- `/users/.../^\- \*\*ac[0-9]+[a-z]?\*\*` → `ssh-rsa`
- `/users/.../z-[a-z-]*` → `kubeconfig-file`
- `/users/.../not done.*` → `kubeconfig-file`
- `/users/.../delegate[a-z']*` → `kubeconfig-file`
- `/users/.../*.agent/logs*` → `kubeconfig-file`

The last row is the command that went looking for the audit log. The guard blocked the investigation into itself twice during this refinement.

### Config shape, for contrast

Counted from `.github/hooks/config/file-access-rules.json`:

- `rules`: 37 entries — 32 `deny`, 3 `ask`, 2 `allow`
- `bash_rules`: 20 entries — **all 20 `ask`**
- `legacy_bash_parity`: 27 entries (metadata inventory, not enforcement)

Reasoning from this shape alone produces the conclusion that all friction originates in the 20 `ask` rules and that the 32 `deny` rules are silent. The log refutes it: the denials are 82% of observed traffic. **Counting rules is not measuring behavior.**

### Root cause, reproduced by execution

`_candidate_paths` in `.github/hooks/lib/bash_analyzer.py` extracts grep's **pattern** operand as a filesystem path. `evaluate_path` normalizes it against the repo root and passes it to `_glob_patterns_overlap` in `.github/hooks/lib/file_access.py`:

```python
literal_chunks = tuple(
    sorted({"", "x", *re.findall(r"[A-Za-z0-9_-]+", first + " " + second)})
)
first_samples = _glob_samples(first, literal_chunks)
second_samples = _glob_samples(second, literal_chunks)
if first_samples is None or second_samples is None:
    return True
samples = first_samples | second_samples
return any(
    fnmatch.fnmatchcase(sample, first) and fnmatch.fnmatchcase(sample, second)
    for sample in samples
)
```

The witness is constructed from literals scraped from **both** patterns. For candidate `foo*` against rule pattern `*kubeconfig`, it synthesizes `fookubeconfig`, finds both patterns match it, and reports overlap. Any candidate ending in `*` overlaps any rule.

Verified behavior table (`analyze_command`, live config, cwd = repo root):

| Command | Verdict |
|---|---|
| `cat ~/.ssh/id_rsa` | DENY `ssh-rsa` — correct |
| `cat ~/.ssh/id_*` | DENY `ssh-rsa` — correct |
| `cp ~/.ssh/id_rsa /tmp/x` | DENY `ssh-rsa` — correct |
| `head ~/.kube/kubeconfig` | DENY `kubeconfig-file` — correct |
| `grep -rn "foo*" .` | DENY `kubeconfig-file` — **false positive** |
| `grep -rn "test*" .` | DENY `kubeconfig-file` — **false positive** |
| `rg "z-[a-z-]*" .` | DENY `kubeconfig-file` — **false positive** |
| `grep -rn "hello" .` | clean — correct |
| `ls src/*` | clean |
| `find . -name "*.md"` | clean |
| `ls -la` | clean |
| `printenv` | ASK `environment-printenv` |
| `ls ~/.ssh/id_rsa` | clean — **coverage hole** |

### The trap in this finding

`_glob_patterns_overlap` looks wrong and is right. It is what makes `cat ~/.ssh/id_*` deny. Rebuilding the witness from the candidate's literals only — the natural cleanup — silently breaks real secret detection while making every test about grep pass. The defect is upstream, in which operands become path candidates at all.

## 2. Claude Code Configuration Discovery

Researched against current Claude Code documentation during refinement. Confidence noted per item.

| Question | Finding | Confidence |
|---|---|---|
| User-level commands | `~/.claude/commands/*.md` | Documented |
| User-level skills | `~/.claude/skills/<name>/SKILL.md` | Documented |
| User-level settings | `~/.claude/settings.json` | Documented |
| **User-level agents** | **No documented path.** Project-level `.claude/agents/` is documented; there is no documented user-level equivalent. `~/.claude/agents/` demonstrably exists and is in use. | **Undocumented — verify** |
| `CLAUDE_CONFIG_DIR` | **Does not exist.** No environment variable relocates the configuration directories. Paths are hardcoded. | Documented (by absence) |
| Symlinked skill directories | Explicitly supported. Claude follows the link and reads `SKILL.md` from the target; a target reachable from multiple locations loads once. | Documented |
| Symlinked rules | Explicitly supported; circular symlinks detected and handled. | Documented |
| Symlinked agent directories | Not documented either way. | **Unknown** |
| Skills hot-reload | Yes — adding, editing, or removing a skill takes effect within the session. **Exception**: creating a top-level skills directory that did not exist at session start requires a restart. | Documented |
| Agents hot-reload | Not documented. Direct evidence from this project: additions are **not** detected mid-session; removals **are** (a dangling link fails to load). Consistent with a start-time load and cache. | Evidence, not doc |
| Precedence | Enterprise > User > Project, for skills. Not documented for agents. **User outranks project.** | Documented (skills only) |
| Plugins | The official distribution mechanism — bundles skills, agents, hooks, MCP servers; auto-updates. Symlinking into `~/.claude/` is characterized as a personal workaround for one's own setup, not a sanctioned distribution pattern. | Documented |

**Codex and OpenCode user-global paths**: no authoritative source located. `scripts/setup-hook-symlinks.sh` currently hardcodes `$HOME/.codex/hooks.json` and `$HOME/.config/opencode/plugins/` without honoring `XDG_CONFIG_HOME`. Treat both as unverified.

### Implication for scope

Because `CLAUDE_CONFIG_DIR` does not exist and the phase is macOS-only, "OS detection and directory discovery" reduces to a small set of hardcoded, documented paths plus a home lookup. The original framing anticipated meaningful platform branching; the research does not support that at this scope. Windows would reintroduce it — symlink creation there requires Developer Mode or `SeCreateSymbolicLinkPrivilege`, forcing a privilege check and a copy-mode fallback.

## 3. Prior Art — the Superseded Symlink Flow

`docs/phases/PHASE_01/PHASE_01_SUMMARY.md` records: *"The former user-global symlink flow has been superseded by generated regular files with absolute commands."*

`scripts/setup-hook-symlinks.sh` retains its name only for documentation compatibility. Its header states the filename is historical, it installs with `cp`, and it closes by printing *"no user files are symlinks."*

**This precedent does not bind the current work.** The reversal was about **hooks**, whose commands can carry absolute paths into the source repository — which is what made regular files viable. Agents, commands, and skills are content, not commands; a copy goes stale the moment the source changes, which is the property the author already relies on for `~/.claude/commands` and `~/.claude/skills`. The hook reversal should be preserved (hooks stay generated files) and not extended to the asset layer.

## 4. Existing Propagator Facts

Verified by reading `scripts/propagate_master_assets.py` in full.

- **No OS detection exists.** No `sys.platform`, no `platform` module, and `os` is not imported at all. All filesystem work goes through `pathlib` and `shutil`. The nearest platform-ish behavior is `_resolve_hook_command`, which prefers an `osx` key unconditionally, with no detection behind it.
- **No symlink is ever created.** `is_symlink` appears eight times, all defensive: unlink-before-write, skip-when-pruning, and raise-on-symlinked-output-root.
- **No home-directory discovery.** No `Path.home()`, `expanduser`, or environment reads. `generate_global_hooks` takes its destination entirely from the caller's `--global-output`.
- **No dry-run mode.** Every code path writes. `verbose` prints results after mutation.
- **The user-global layer is hooks-only**, and is a thin wrapper: `propagate_hooks_once` with `copy_assets=False` plus an absolute-command transform.
- **Output roots are recomputed locally from a `repo_root` parameter**, not read from the module constants, which are largely dead. `repo_root` is the de-facto injection point for destination.
- **Pruning requires two conditions**: absent from the run's expected set **and** carrying the generated marker at a positional line index. The marker check is positional, not a whole-file search — a README that merely quotes the marker must survive.
- **Ordering contract**: all pruning runs strictly after all emission, because filename resolution reads stems already on disk.
- `_validate_output_directory` and `_validate_nested_output_directory` raise on any symlinked component and require containment under `repo_root`. Both are called before enumeration on every prune path, per the P3-SEC-01 fix.

## 5. Decisions Taken at Refinement

- **The file-access guard is fixed, not retired.** The retirement proposal recorded in `.github/learnings/cross-phase-decisions.md` was raised on friction grounds; the measurement shows the friction is a bounded extraction defect rather than a policy outcome. The 32 deny rules, the 20 ask rules, and `_glob_patterns_overlap` all stay.
- **macOS only.** Windows and Linux are explicit non-goals at this scope. Untested cross-platform support would be the "partial protection that reads as total protection" failure already recorded under adoption readiness.
- **The phase splits.** Phase 04 becomes the unblock work — guard accuracy and propagation reach. The verification work formerly scoped here is preserved in the phase summary's deferral table and requires a new roadmap entry from `@project-planner`. Phases 01 and 02 remain release-blocked; nothing in this phase changes that, and no status line moves.
