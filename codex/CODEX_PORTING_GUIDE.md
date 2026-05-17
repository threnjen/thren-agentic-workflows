# Codex Porting Guide

This guide maps the repository's `.github/` source-of-truth surfaces into Codex-native targets. It is an authoring guide for future conversion work, not a runtime install recipe.

Use this guide with the following repository-owned references:

- `codex/CODEX_PLATFORM_REFERENCE.md` for verified Codex behavior, discovery rules, and runtime locations.
- `codex/README.md` for the repository-owned Codex source area and the distinction between `codex/` and live runtime paths.

## Core Rule

AGENTS-derived content maps to the global Codex AGENTS layer, not to either repository's checked-in `AGENTS.md`.

For this repository, that means future AGENTS source should be authored under the repository-owned `codex/` area and only later installed into the user-scoped Codex runtime surface such as `~/.codex/AGENTS.md` or `~/.codex/AGENTS.override.md` when a later feature defines the install flow. Do not treat `AGENTS.md` at the repository root as the Codex destination for ported instruction content.

## Mapping Overview

| `.github/` source surface | Primary Codex destination | Porting mode | Why it is not a file-for-file copy |
|---|---|---|---|
| `.github/instructions/` | Global Codex AGENTS guidance and selected agent `developer_instructions` | Transform | Codex does not have this repository's instruction-file system or `applyTo` matching model |
| `.github/agents/` | Codex custom-agent TOML files | Transform | Codex agents are TOML files with required fields, not Markdown manifests |
| `.github/skills/` | Codex skill directories with `SKILL.md` and optional assets | Transform | Codex skills are directory assets discovered from runtime skill roots, not standalone source manifests |

## Repository-Owned Landing Zone

Porting work for this phase starts in the repository-owned `codex/` area described in `codex/README.md`.

Use that area for:

- Mapping docs such as this guide.
- Future source material that may later produce global AGENTS content, custom-agent TOML files, or skill directories.

Do not use this guide to justify writing directly into runtime locations such as `.codex/`, `~/.codex/`, `.agents/skills`, or `$HOME/.agents/skills/`. Those are installation or discovery surfaces, not the source-of-truth authoring area for this phase.

## Instructions: `.github/instructions/` -> Global AGENTS And Agent `developer_instructions`

### Destination Model

`.github/instructions/` does not map to a single Codex file family. Instead, instruction content must be classified by scope and then moved into one or both of these Codex surfaces:

- Global Codex AGENTS guidance for rules that should apply broadly across Codex usage.
- Individual custom-agent `developer_instructions` for rules that are specific to a single agent role or workflow.

This is the main split-destination case in the Codex port.

### Transformation Rules

1. Start from the source intent, not the source filename.
2. Treat `applyTo` patterns as routing input that must be resolved manually during porting.
3. Move cross-cutting behavior into the global Codex AGENTS layer when the rule should apply regardless of which custom agent is active.
4. Move agent-specific behavior into that agent's `developer_instructions` when the rule only makes sense in the context of one custom agent.
5. Split a single instruction file across both destinations when it contains both global and agent-specific rules.
6. Drop GitHub-specific mechanics that depend on native instruction-file loading or `applyTo` matching, and replace them with explicit Codex wording.

### What Usually Ports Cleanly

- Durable behavior constraints.
- Safety or workflow rules that still make sense outside GitHub's instruction loader.
- Agent-specific implementation guidance that can be embedded directly in `developer_instructions`.

### What Requires Rewrite

- Any text that assumes instructions are auto-loaded from `.github/instructions/`.
- Any text that depends on `applyTo` patterns as a runtime routing mechanism.
- Any wording that assumes a file-for-file mirror from `.github/instructions/` into Codex.

### What Is Non-Portable Or GitHub-Only

- Instruction metadata whose only purpose is GitHub-side instruction discovery.
- Guidance that depends on GitHub Copilot-specific loading behavior rather than reusable policy.

### Example Classification

| Source pattern | Codex destination | Notes |
|---|---|---|
| Cross-cutting repository policy from `.github/instructions/` | Global Codex AGENTS guidance | Use when the rule should apply before any project-local or agent-local detail |
| Agent-specific workflow rule from `.github/instructions/` | Matching agent TOML `developer_instructions` | Inline as explicit prose because Codex does not resolve `applyTo` |
| Mixed file with both global and agent-local rules | Split across both destinations | Do not force one destination when the source intent is mixed |

## Agents: `.github/agents/` -> Codex Custom-Agent TOML

### Destination Model

Each agent definition in `.github/agents/` maps to a Codex custom-agent TOML file, not to another Markdown manifest.

Agent definitions are identified by YAML frontmatter containing at minimum a `name` and `description` field. Most files use the `.agent.md` extension, but some agent definitions use a plain `.md` extension (for example, `prod-code-review.md`). Use frontmatter presence, not filename extension, as the canonical signal that a file is an agent definition to port.

Documentation files in `.github/agents/` — such as `README.md`, `PORTING_GUIDE.md`, and `TOOL_MAPPING.md` — are not agent definitions. Do not create Codex custom-agent TOML files from them. If their content is useful for future Codex porting reference, carry relevant sections into `codex/` documentation rather than into agent TOML fields.

The Codex-required fields called out by the platform reference are:

- `name`
- `description`
- `developer_instructions`

Other settings such as model selection, sandbox configuration, MCP server configuration, nicknames, and skill configuration are optional Codex fields and should only be populated when the source behavior actually needs them.

Codex has no verified hide mechanism that keeps subagents out of the frontend agent picker. In this repository, any source agent with `user-invocable: false` must therefore be renamed with a `z-` prefix in the generated Codex artifact so it sorts to the bottom and clearly signals internal-only usage.

When a user selects a Codex custom agent with the `@` designator, that selected agent is already the active role. Ported `developer_instructions` for user-invocable agents must therefore tell the agent to begin work as that role immediately, not to call the same role again as a subagent on first action.

### Transformation Rules

1. Translate the Markdown agent definition into TOML fields rather than copying the file body as-is.
2. Preserve the role, purpose, and durable constraints of the source agent.
3. Inline or rewrite any instructions that were previously supplied by `.github/instructions/` so the resulting Codex agent remains self-contained where needed.
4. For every user-invocable Codex agent, add explicit `developer_instructions` that the agent should execute as the selected role immediately when invoked with `@`. Do not let a user-selected agent spend its first action spawning the same role as a subagent.
5. Reserve subagent delegation for genuinely distinct child roles. When delegation is still needed, target another generated Codex agent name, typically an internal `z-*` agent, rather than the currently selected agent's own role.
6. Convert GitHub-specific tool assumptions, orchestration metadata, or unsupported behavior into Codex-native wording or drop them when no Codex equivalent exists.
7. Rewrite source agent references in `developer_instructions` to the generated Codex agent names. Use the Codex runtime name, not the GitHub display name, so references such as internal subagents resolve to names like `z-feature-reviewer` instead of `Feature - Reviewer`.
8. Serialize `developer_instructions` as TOML-safe text. Prefer multiline literal strings for markdown-heavy content so backticks, fenced code blocks, and backslashes are preserved without escape bugs. If the body cannot be represented safely as a multiline literal string, fall back to a fully escaped TOML basic string rather than hand-escaping fragments.
9. For source agents with `user-invocable: false`, emit the generated Codex artifact with a `z-` prefix in both the installed filename and the TOML `name` field. This is a naming convention, not a true hide flag, and exists because Codex currently lacks a verified hidden-subagent surface in this repo.
10. Keep repository-owned source material in `codex/` until a later feature defines the exact generated or installed layout.

### Major Non-Portable Differences From Markdown Agent Manifests

| GitHub source model | Codex model | Porting implication |
|---|---|---|
| Markdown `.agent.md` manifest | TOML custom-agent file | Requires field-based rewrite |
| User selects a Codex agent with `@agent-name` | Selected agent is already the active role | Generated `developer_instructions` must begin in-role and must not self-spawn the same role as a subagent |
| Instruction loading via `.github/instructions/` | `developer_instructions` field inside agent TOML | Relevant instructions must be embedded or rewritten |
| `user-invocable: false` hidden subagent intent | `z-`-prefixed filename and TOML `name` | Treat as a visibility hint because no Codex hide flag is verified here |
| GitHub-specific metadata and tool assumptions | Codex-specific optional fields and runtime behavior | Unsupported behavior must be classified explicitly |

### What Usually Ports Cleanly

- Agent purpose and scope.
- Stable behavioral constraints.
- User-facing description of what the agent does.
- The rule that a user-selected Codex agent begins work in-role instead of first spawning itself as a subagent.
- The `z-` prefix convention for non-user-invocable subagents.

### What Requires Rewrite

- Frontmatter structure.
- Any source wording that implies the selected Codex agent should immediately delegate to an identical role instead of acting as that role.
- Agent references inside the body that must point at generated Codex names rather than GitHub display names.
- TOML string serialization for markdown bodies that contain code fences, inline backticks, backslashes, or other escape-sensitive content.
- Any reference to GitHub-native instruction loading.
- Tool language or metadata that only makes sense in the GitHub manifest model.

### What Is Non-Portable Or GitHub-Only

- GitHub-only manifest conventions with no Codex field equivalent.
- Any behavior that assumes the GitHub agent runtime rather than Codex custom-agent execution.

### Example Classification

| Source pattern | Codex destination | Notes |
|---|---|---|
| `.github/agents/04b-feature-implementer.agent.md` role and core behavior | Custom-agent TOML fields | Convert purpose and constraints into TOML-backed content |
| Any user-invocable source agent that users will call with `@` | Matching Codex agent `developer_instructions` | Add explicit wording that the selected agent is already in role and should not self-spawn on entry |
| `.github/agents/*` with `user-invocable: false` | `z-*.toml` plus `name = "z-*"` | Use naming to de-emphasize internal subagents in the Codex frontend |
| GitHub display-name references such as `Feature - Reviewer` | Generated Codex runtime name such as `z-feature-reviewer` | Rewrite body text so orchestrators and subagent instructions reference actual Codex agent names |
| Instructions previously inherited from `.github/instructions/` | `developer_instructions` | Must be explicit in Codex; no hidden loader |
| GitHub-only metadata with no Codex field | Non-portable | Record it as dropped or rewritten instead of silently carrying it forward |

## Skills: `.github/skills/` -> Codex Skill Directories

### Destination Model

Each `.github/skills/<skill-name>/` source entry maps to a Codex skill directory rather than a single manifest file.

The verified Codex structure is:

- `SKILL.md` is required.
- Supporting assets are optional and may include directories such as `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.

### Transformation Rules

1. Treat each source skill as a directory-level asset.
2. Preserve the intent and reusable workflow guidance from the source `SKILL.md`.
3. Carry forward supporting files only when they are meaningful in the Codex skill model.
4. Keep repository-owned skill source material under `codex/` until a later feature defines an exact authoring layout for generated or installed skill copies.
5. Map final installed skills to Codex runtime discovery roots such as `.agents/skills` or `$HOME/.agents/skills/` only after the authoring-to-install flow is defined.

### How This Differs From The Current Master Skill Structure

The current master skill structure already uses directory-based source entries under `.github/skills/`, so the highest-value warning is not about single-file conversion. The important differences are:

- The Codex destination is a runtime-discovered skill directory, not the existing master source directory.
- Optional Codex assets must be judged against Codex expectations, not copied automatically from GitHub-side conventions.
- Repository-owned `codex/` source material and installed runtime skill directories must stay separate.

### What Usually Ports Cleanly

- Skill purpose and usage guidance from `SKILL.md`.
- Supporting materials that are platform-agnostic and useful at runtime.

### What Requires Rewrite

- Any source wording that assumes GitHub skill discovery or GitHub-specific tooling.
- Any surrounding repository conventions that belong in global AGENTS guidance or agent `developer_instructions` instead of the skill itself.

### What Is Non-Portable Or GitHub-Only

- GitHub-specific references that do not affect Codex skill behavior.
- Supporting files whose only purpose is GitHub platform packaging or discovery.

### Example Classification

| Source pattern | Codex destination | Notes |
|---|---|---|
| `.github/skills/<skill>/SKILL.md` core workflow content | Codex skill directory `SKILL.md` | Usually portable with wording cleanup as needed |
| Platform-agnostic supporting references | Optional skill assets | Keep only if they still support Codex usage |
| GitHub-only packaging or discovery assumptions | Non-portable or transformed | Remove or rewrite rather than mirroring blindly |

## Portability Classification

Use this table before porting any source asset.

| Classification | Definition | Typical examples in this repo | Codex action |
|---|---|---|---|
| Portable | The source intent already matches a Codex-native concept with little or no structural change | Stable policy language, agent purpose text, reusable skill workflow guidance | Carry forward with minimal wording cleanup |
| Requires transformation | The content is valid in spirit but must be reshaped to fit Codex surfaces | `.github/instructions/` rules that split across global AGENTS and `developer_instructions`; Markdown agent manifests that become TOML | Rewrite into the correct Codex-native destination |
| GitHub-only or non-portable | The source depends on GitHub-specific discovery, metadata, or runtime behavior | `applyTo` matching as runtime routing, GitHub-only manifest mechanics, GitHub-only packaging assumptions | Drop, replace, or document as intentionally unsupported |

## Porting Workflow

1. Identify which `.github/` surface owns the source artifact.
2. Route the artifact using the mapping rules in this document rather than by filename similarity.
3. Confirm the repository-owned source landing zone under `codex/README.md` before creating any new authored artifacts.
4. Use `codex/CODEX_PLATFORM_REFERENCE.md` to verify the Codex runtime destination and file model.
5. Classify each piece of content as portable, transformed, or non-portable before writing any Codex copy.
6. If one source asset maps to both global AGENTS guidance and custom-agent `developer_instructions`, split it deliberately and document the split.

## Quick Decision Guide

| If you are porting... | Start here | End at | Main warning |
|---|---|---|---|
| `.github/instructions/` content | This guide's instructions section | Global AGENTS guidance and or agent `developer_instructions` | No direct instruction-file equivalent exists in Codex |
| `.github/agents/*.agent.md` | This guide's agents section | Custom-agent TOML | Codex agent files are field-based, not Markdown manifests |
| `.github/skills/<skill>/` | This guide's skills section | Codex skill directory | Installed skill directories are runtime assets, not the repository-owned source area |

## Final Guardrails

- Do not treat `codex/` as a mirror of `.github/`.
- Do not port AGENTS-derived content into either repository's checked-in `AGENTS.md`.
- Do not blur repository-owned source docs with runtime `.codex/` or `.agents/skills` locations.
- Do not let a user-selected Codex agent immediately spawn the same role as a subagent. Treat `@agent-name` selection as already being inside that agent role.
- Do not emit markdown-heavy `developer_instructions` into TOML multiline basic strings unless every backslash escape is valid TOML. Prefer multiline literal strings, with an escaped basic-string fallback for edge cases.
- Do not rely on a hidden-subagent flag for Codex in this repo. Use the `z-` prefix convention for non-user-invocable agents so the generated names communicate that they are internal pipeline roles.
- When parity is unclear, mark the behavior as requiring Codex-specific rewrite instead of implying a direct copy path.