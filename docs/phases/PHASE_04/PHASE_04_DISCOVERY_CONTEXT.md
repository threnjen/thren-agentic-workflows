# Phase 04 Discovery Context

Context gathered during Phase 04 refinement that is not fully derivable from the current codebase. Downstream agents should read this before planning or implementing the phase.

## 1. Branch and Interceptor History

The current branch is `repo_improvements_project`; its merge base with `main` is `e3398c7b2591378e61a62a3c4dd5444891bdb3d1`.

Git history establishes two independent branch-added integrations:

| Integration | Introduction | Main-branch status |
|---|---|---|
| File-access guard, Bash analyzer, file-access policy, and guard rules | `8e2a498` — Phase/hook foundation file access guard (#19), 2026-07-14 | Absent from `main` |
| Automatic RTK rewrite hook and its tests | `370fcba` — Phase/phase final review (#22), 2026-07-16 | Absent from `main` |

RTK is an external executable and is independent of both integrations. Retiring the guard and automatic rewrite hook does not uninstall RTK or prevent explicitly prefixed RTK commands.

## 2. File-Access Guard Friction Evidence

The guard's audit log, `.agent/logs/file-access-guard.ndjson`, contained 22 events from one working session:

| Decision | Count |
|---|---:|
| `deny` | 18 |
| `ask` | 4 |

All 18 denials were false positives caused by search patterns, glob arguments, or regular expressions being evaluated as paths. Ten fired `kubeconfig-file`, five fired `ssh-rsa`, and three fired `credential-json`. The four prompts were three destructive-command confirmations and one environment inspection.

During this refinement the same guard blocked a Git history query because exclusion pathspecs were classified as an SSH-key access. The evidence therefore extends beyond the original grep reproduction.

The root cause is `_candidate_paths` in `.github/hooks/lib/bash_analyzer.py` treating non-path Bash operands as filesystem candidates. The retirement decision removes this analyzer rather than preserving GUARD-01 as a repair feature.

## 3. Author-Machine Runtime-Link Inventory

A read-only inventory on 2026-07-16 examined repository-targeting links beneath:

- `~/.claude`
- `~/.codex`
- `~/.config/opencode`
- `~/.agents`

| Harness root | Repository-targeting links |
|---|---:|
| Claude | 41 |
| Codex | 70 |
| OpenCode | 2 |
| Shared `.agents` root | 0 |
| **Total** | **113** |

Of the 113 links, 101 resolved and 12 were dangling. The inventory includes whole-directory links and per-file or per-skill links. It excludes Codex package/executable links, Claude debug pointers, plugin-cache links, Git hooks, and other application-managed links that do not target this repository.

These counts are a baseline, not an implementation constant. Migration must take a fresh inventory and classify each entry from its current type and target.

## 4. Official Runtime Destination Research

Research was performed against current primary documentation on 2026-07-16.

### Claude Code

- User agents: `~/.claude/agents/*.md`
- Legacy commands: `~/.claude/commands/*.md`
- Skills: `~/.claude/skills/<name>/SKILL.md`
- `CLAUDE_CONFIG_DIR` relocates the `.claude` root.
- Native Windows uses the active Windows user profile. WSL uses the active Linux home.

Sources: [Claude directory](https://code.claude.com/docs/en/claude-directory), [subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills), [environment variables](https://code.claude.com/docs/en/env-vars), [installation](https://code.claude.com/docs/en/installation).

### Codex CLI

- User agents: `${CODEX_HOME:-~/.codex}/agents/*.toml`
- Custom prompts: `${CODEX_HOME:-~/.codex}/prompts/*.md`
- Skills: `~/.agents/skills/<name>/SKILL.md`
- `CODEX_HOME` relocates Codex-owned state but does not relocate the documented shared skill root.
- A custom `CODEX_HOME` must already exist.
- Native Windows and WSL are distinct runtime environments.

Sources: [environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [custom prompts](https://learn.chatgpt.com/docs/custom-prompts), [skills](https://learn.chatgpt.com/docs/build-skills), [Windows and WSL](https://learn.chatgpt.com/docs/windows/wsl).

### OpenCode

- User agents: `~/.config/opencode/agents/*.md`
- Commands: `~/.config/opencode/commands/*.md`
- Skills: `~/.config/opencode/skills/<name>/SKILL.md`; OpenCode also recognizes documented shared skill roots.
- `OPENCODE_CONFIG_DIR` covers agents and commands but is not documented as relocating skills.
- Public documentation does not promise general `XDG_CONFIG_HOME` relocation for these assets.
- Native Windows uses the active Windows profile; OpenCode recommends WSL for full compatibility. WSL state remains inside WSL.

Sources: [configuration](https://opencode.ai/docs/config/), [agents](https://opencode.ai/docs/agents/), [commands](https://opencode.ai/docs/commands/), [skills](https://opencode.ai/docs/skills/), [troubleshooting](https://opencode.ai/docs/troubleshooting/), [Windows and WSL](https://opencode.ai/docs/windows-wsl).

### Cross-platform boundary

macOS, Linux, native Windows, and WSL are supported deployment environments. Deployment targets only the environment in which the propagator runs. Native Windows and each WSL distribution require separate runs; the propagator does not cross their home-directory boundary.

No harness documents a required atomic-copy, file-lock, ACL, or rollback protocol for these user-authored asset directories. Phase 04 therefore owns its safe replacement behavior. Windows sharing violations must preserve the existing destination and be reported.

## 5. Existing Propagator Facts

Verified from `scripts/propagate_master_assets.py` and the generated roots:

- Repository-generated roots are `claude/`, `codex/`, and `opencode/`.
- Claude currently emits agents, commands, skills, instructions, and learnings.
- Codex currently emits agents, profiles, skills, and instructions.
- OpenCode currently emits agents, skills, and instructions.
- User-global hooks already use generated regular files with absolute commands; hook deployment must not be folded into the new asset-copy stage.
- `propagate_once` emits all outputs before pruning.
- Propagation may require multiple runs to converge after an emission-class change because destination naming observes existing disk state.
- Long-running watchers execute the propagator code loaded when they started and must be restarted after propagator changes.
- Existing containment helpers reject symlinked output roots and symlinked intermediate parents for in-repository generation.
- No general user-global managed-copy stage exists.

User deployment must consume completed generated outputs rather than independently transforming `.github` sources.

## 6. Evangelize and Documentation Findings

The source agent `.github/agents/evangelize.agent.md` currently requires runtime symlinks and can recreate them. Its link behavior appears in:

- Runtime discovery and preflight requirements.
- Claude, Codex, and OpenCode agent-link instructions.
- Codex per-skill link commands.
- Windows symbolic-link, junction, and hard-link fallback guidance.
- Quality gates and the runtime verification matrix.

Generated Evangelize variants repeat this behavior. Setup and explanatory documents also contain active runtime-link instructions, including `HARNESS_SETUP.md`, Claude and OpenCode symlink setup documents, Codex setup and pilot documents, generated READMEs, and generated learnings.

Phase 04 must correct the source agent first, regenerate its platform variants, and reconcile supported setup guidance. References that discuss symlinks only as a security threat, containment boundary, unrelated Git hook, or application-managed implementation detail are not retirement targets.

## 7. Authoritative Phase Boundaries

- The file-access guard and its Bash analyzer are retired as one unit.
- Automatic RTK rewriting is retired independently.
- RTK remains installed and available for explicit use.
- The hook framework and prompt-injection scanner remain.
- Repository outputs propagate and converge before user-global deployment begins.
- User-global assets are managed copies, never runtime symlinks or junctions.
- Repository-targeting legacy links and junctions are migrated; foreign content is preserved.
- Deployment supports macOS, Linux, native Windows, and WSL in the current environment only.
- Project-local deployment, plugin packaging, and cross-environment Windows/WSL mutation are excluded.
- Phase 01 and Phase 07 require project-level reconciliation by `project-planner`; Phase 04 does not alter their documents or status lines.
