# Codex Platform Reference

## Purpose

This document captures the verified Codex platform model that later Phase 02 features depend on. It is a repository-owned reference under `codex/`, not a live runtime install surface.

Use this file to answer four questions before authoring any Codex-specific content:

- Where Codex loads global and project instruction guidance.
- Where custom agents live and what format they use.
- Where skills are discovered and what structure they require.
- Which paths belong to repository-owned source material versus runtime-installed content.

## Discovery Model

### Global AGENTS guidance

Codex loads home-directory guidance before it considers project-local instruction files.

Verified macOS behavior:

1. Codex checks `~/.codex/AGENTS.override.md` first.
2. If no override exists, Codex uses `~/.codex/AGENTS.md`.
3. Codex then walks project instruction files from the repository root toward the current working directory.
4. At each project level, `AGENTS.override.md` takes precedence over `AGENTS.md`.

Additional fallback project filenames may be configured through `project_doc_fallback_filenames` in `~/.codex/config.toml`.

Repository policy for this repo: if AGENTS-derived source material is later authored here, it should describe content intended for the global Codex AGENTS layer first. Do not treat either repository's checked-in `AGENTS.md` as the Codex runtime destination.

### Authoring implication

`codex/` is the source area for planning and authoring. Runtime installation targets are separate:

- `codex/` holds repository-owned reference docs and future source artifacts.
- `.codex/` holds repo-scoped runtime configuration or installed runtime assets.
- `~/.codex/` holds user-scoped Codex configuration, global AGENTS guidance, and user-scoped custom agents.

## Custom Agents

Codex custom agents are standalone TOML files rather than markdown manifests.

Verified model:

- User-scoped custom agents live under `~/.codex/agents/`.
- Repo-scoped custom agents live under `.codex/agents/`.
- Required fields are `name`, `description`, and `developer_instructions`.
- Optional fields include model selection, sandbox settings, MCP server configuration, nicknames, and skill configuration.

### Agent Invocation

Codex does **not** use the `@agent-name` designator syntax. That convention belongs to GitHub Copilot Chat and does not work in Codex CLI.

In Codex, agents are selected via natural language. Codex matches the user's prompt against the `name` and `description` fields of loaded agent files and delegates accordingly. The `/agent` slash command is for navigating between already-running agent threads, not for spawning a new one.

Implication for `developer_instructions`: do not instruct users to spawn the agent with `@`. Instead, tell the agent to begin work in its role when addressed by name or role.

Authoring rule for this repo: keep the source material for future custom agents under `codex/` until a later feature defines the exact repository-owned layout. Do not place draft source documents directly into `.codex/agents/` unless the goal is runtime installation.

## Skills

Codex skills are directory-based assets, not single files.

Verified model:

- Each skill directory requires `SKILL.md`.
- Optional contents include `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.
- Repo-scoped skills are discovered from `.agents/skills` between the repository root and the current working directory.
- User-scoped skills are discovered from `$HOME/.agents/skills/`.
- Codex supports symlinked skill folders.

### SKILL.md Format

Every `SKILL.md` must begin with YAML frontmatter delimited by `---`. Codex rejects any skill file that does not start with this block.

Required fields:

| Field | Constraints |
|-------|-------------|
| `name` | 1–64 chars, lowercase + digits + hyphens only, **must match the parent directory name** |
| `description` | 1–1024 chars. Describes what the skill does and when to trigger it. |

Minimal valid example:

```markdown
---
name: my-skill
description: "What this skill does and when to use it."
---

Skill instructions here...
```

The generated comment from the propagation script (`<!-- Generated from ... -->`) must appear **after** the closing `---`, not before it.

The macOS-relevant user install destination is `$HOME/.agents/skills/`. This feature does not define a runtime `.codex/skills` location because the discovery context did not verify one.

## Config And Runtime Locations

The following locations were explicitly verified for macOS and should be treated as the platform reference set for later setup and porting work.

| Path | Scope | Role |
|------|-------|------|
| `~/.codex/config.toml` | User | Global Codex configuration, including settings such as `project_doc_fallback_filenames` |
| `~/.codex/AGENTS.md` | User | Global AGENTS guidance when no home override file is present |
| `~/.codex/AGENTS.override.md` | User | Higher-precedence global AGENTS guidance |
| `~/.codex/agents/` | User | Installed user-scoped custom-agent TOML files |
| `$HOME/.agents/skills/` | User | Installed user-scoped skill directories |

Repository-local runtime surfaces that also matter:

- `.codex/config.toml` is a repo-scoped runtime config surface that already exists in this repository.
- `.codex/agents/` is the repo-scoped runtime location for installed custom agents.
- `.agents/skills` is the repo-scoped runtime discovery root for installed skills.

None of those runtime paths are the repository-owned source-of-truth area for this phase. Use `codex/` for authored reference material and future source artifacts.

## Source Versus Runtime Split

Keep these roles distinct:

| Surface | Category | Use It For | Do Not Use It For |
|---------|----------|------------|-------------------|
| `codex/` | Repository-owned source | Planning docs, platform references, and future source artifacts | Live installed Codex config, agents, or skills |
| `.codex/` | Repo runtime | Repo-scoped runtime config and installed runtime assets | Long-term source-of-truth authoring |
| `.agents/skills` | Repo runtime | Repo-scoped installed skills discovered by Codex | Repository-owned source material |
| `~/.codex/` | User runtime | Global Codex config, global AGENTS guidance, and user custom agents | Repository-owned documentation |
| `$HOME/.agents/skills/` | User runtime | User-scoped installed skills | Repository-owned source material |

This separation matters because later Phase 02 work needs to map `.github/` source material into Codex-native runtime targets without confusing checked-in docs with installed files.

## Implementation-Ready Precedence Summary

Future implementation work should be able to rely on the following rules without rediscovering the platform basics:

1. Global Codex AGENTS guidance is loaded from `~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md` before project-local instruction files.
2. Project-local instruction lookup walks from repository root toward the current working directory, preferring `AGENTS.override.md` over `AGENTS.md` at each level.
3. Custom agents are TOML files loaded from `~/.codex/agents/` for user scope and `.codex/agents/` for repo scope.
4. Skills are directory-based and load from `$HOME/.agents/skills/` for user scope and `.agents/skills` for repo scope.
5. Repository-owned source material belongs under `codex/`; runtime installation targets belong under `.codex/`, `.agents/skills`, `~/.codex/`, or `$HOME/.agents/skills/` depending on scope.

If future upstream Codex docs or source behavior disagree with any rule above, update this reference before implementing against it.

## Provenance And Revalidation

Last verified: 2026-05-21.

This document was authored from the repository's Phase 02 discovery record and repository context:

- `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md`
- `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`
- `.codex/config.toml`
- `codex/README.md`

Upstream source categories recorded in the discovery context:

- OpenAI Codex documentation for AGENTS discovery.
- OpenAI Codex documentation for skills authoring and discovery.
- OpenAI Codex documentation for custom agents and advanced configuration.
- Upstream `openai/codex` repository excerpts covering precedence and discovery behavior.

Recheck upstream Codex behavior immediately before any implementation feature treats this file as a stable contract. This reference is intentionally fail-fast: if a location, file format rule, or precedence rule is no longer verified, prefer updating this document first rather than silently implementing against stale assumptions.