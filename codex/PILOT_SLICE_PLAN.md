# Codex Pilot Slice Plan

## Purpose

This document identifies the minimal pilot trio for validating the Codex porting model before any broader conversion of the `.github/` source tree.

A maintainer uses this plan to implement the first Codex artifacts without reopening platform research. A reviewer uses the exit criteria to decide whether full parity work is justified.

The plan is intentionally narrow: one instruction slice, one custom agent, one skill — enough to exercise all three Codex-native surfaces while keeping the validation surface small.

Prerequisites this plan depends on:

- `codex/CODEX_PLATFORM_REFERENCE.md` — verified Codex behavior and runtime locations
- `codex/CODEX_PORTING_GUIDE.md` — mapping rules from `.github/` surfaces to Codex-native targets
- `codex/MACOS_SETUP_AND_SYMLINKS.md` — macOS install targets and idempotent symlink commands

---

## Default Pilot Trio

| Surface | Source asset | Codex-native target |
|---------|-------------|---------------------|
| Global Codex AGENTS guidance | `.github/instructions/output-verbosity-policy.instructions.md` | `~/.codex/AGENTS.md` (via `codex/global-agents/AGENTS.md`) |
| Custom-agent TOML | `.github/agents/03-feature-decomposer.agent.md` | `~/.codex/agents/feature-decomposer.toml` (via `codex/agents/feature-decomposer.toml`) |
| Codex skill directory | `.github/skills/feature-plan-set/` | `$HOME/.agents/skills/feature-plan-set/` (via `codex/skills/feature-plan-set/`) |

### Fallback Rule

The default trio may only be replaced when a documented record in the **Replacement Record** table at the end of this document provides explicit evidence that a different trio is demonstrably lower-risk and still covers all three Codex-native surfaces. Replace one element at a time with explicit justification. Silent scope drift is not permitted.

---

## Selection Rationale

### Instruction Slice: `output-verbosity-policy.instructions.md`

**Why low-risk**

The file is short (under 25 lines), entirely prose-based, and contains no tool assumptions. It carries a cross-cutting behavioral constraint — concise output defaults with quality-preserving exceptions — that belongs exactly in the global Codex AGENTS layer as the porting guide describes for cross-cutting policy.

The only non-portable element is the YAML frontmatter block (`description`, `applyTo`). The `applyTo` pattern is GitHub-only metadata whose sole purpose is instruction discovery within the GitHub Copilot loader. Dropping it does not affect any of the body content. This makes the file an ideal first test case: it exercises the mandatory metadata-stripping step without requiring content restructuring.

The "Personality Canary" section provides a human-readable confirmation: a Codex session that begins with *"Loaded. Stop."* proves that the correct file was installed and loaded before any other session output appears.

**Why high-signal**

Global Codex AGENTS guidance is loaded first — before any project-local or agent-local configuration. Validating one real cross-cutting policy in this surface confirms that the porting model routes content to the right layer before any more complex content is attempted.

**Phase 02 alignment**

The porting guide defines cross-cutting behavior as the primary candidate for the global AGENTS layer (see the "Example Classification" table in `codex/CODEX_PORTING_GUIDE.md`). Validating this routing decision on a real policy locks in the model before it is used for any other instruction content.

---

### Custom Agent: `03-feature-decomposer.agent.md`

**Why low-risk**

The agent has a single, clearly-scoped purpose: decompose a Phase document into independent feature plan files. Its frontmatter is minimal — `name`, `description`, and `tools` — and the `tools` list is GitHub Copilot metadata that must be dropped with no content impact.

The agent body references the `feature-plan-set` skill by name. Because the same skill is the pilot skill for the third surface, porting both together validates the agent-skill reference in a realistic context rather than a synthetic one.

The agent does not embed deep dependencies on specific `.github/instructions/` files in its workflow guidance. Its operational rules are self-contained in the agent body, which reduces the number of cross-surface split decisions required during the port to zero for this pilot.

**Why high-signal**

The Feature Decomposer is a central step in the GitHub agent pipeline. A successful Codex port confirms that the TOML custom-agent model can represent a real workflow agent with meaningful content — not just a trivial name and description placeholder. It exercises the full TOML conversion path: dropping GitHub-only frontmatter, populating required `developer_instructions` from the Markdown body, and confirming that Codex can load and invoke the resulting agent.

**Phase 02 alignment**

The porting guide requires that each `.github/agents/*.agent.md` become a Codex TOML file with `name`, `description`, and `developer_instructions` as required fields, and that GitHub-only frontmatter be dropped (see the Agents section of `codex/CODEX_PORTING_GUIDE.md`). The Feature Decomposer is a clean, contained candidate for validating that path end-to-end.

---

### Skill: `.github/skills/feature-plan-set/`

**Why low-risk**

The skill already uses the directory-based structure that Codex expects: a single `SKILL.md` as the primary artifact with no required supporting directories. The body content is plan-writing templates and conventions with no runtime tool dependencies that would require Codex-specific rewrites.

The only non-portable element is the YAML frontmatter block. The `name` and `description` fields are GitHub-only discovery metadata. Removing them does not affect any usable guidance content.

**Why high-signal**

Skills are the third Codex-native surface. Validating one real skill confirms the directory-asset model and verifies the symlink install path described in `codex/MACOS_SETUP_AND_SYMLINKS.md`. Because the Feature Decomposer agent references this skill, installing both together creates a minimal but realistic end-to-end scenario: the agent references the skill, the skill is installed at the correct Codex discovery root, and the reference resolves correctly.

**Phase 02 alignment**

The porting guide classifies skill directories where `SKILL.md` is the primary artifact as direct-transform candidates — portable with frontmatter removal. `feature-plan-set/` is the canonical example of this case (see the Skills section of `codex/CODEX_PORTING_GUIDE.md`).

---

## Expected Codex Outputs

### Output 1: Global AGENTS Guidance

**Source**: `.github/instructions/output-verbosity-policy.instructions.md`
**Repository-owned source path**: `codex/global-agents/AGENTS.md` *(future artifact; created by the feature that implements this pilot plan)*
**Codex runtime destination**: `~/.codex/AGENTS.md` (symlinked from repository-owned source)

**Required transformations**

1. Drop the YAML frontmatter block (`description:` and `applyTo:` fields). These are GitHub instruction-loader metadata with no Codex equivalent.
2. Retain the body text verbatim. The behavioral constraints and quality-preserving exceptions are fully portable.
3. Retain the "Personality Canary" section including the `*"Loaded. Stop."*` announcement. This serves as a human-auditable confirmation that the correct content was installed.

**Expected content after transformation**

```
Use concise defaults for high-frequency responses as soft targets, never hard limits.

Default response shape:
- Lead with delta-first content: changes made, findings, decisions, blockers, and next actions.
- Keep supporting background brief unless needed for correctness.

Soft targets (advisory):
- Simple status or direct answers: 1-3 sentences.
- Standard implementation/review updates: concise summary plus short evidence bullets.
- Complex debugging, audits, or design tradeoffs: expand only where needed to keep reasoning correct and actionable.

Quality-preserving exceptions:
- Expand detail when safety, correctness, compliance, or production-risk review would be weakened by brevity.
- Expand detail when user instructions explicitly request depth.
- Never omit required constraints, caveats, or validation outcomes to hit a length target.

Do not enforce token limits at runtime and do not truncate required analysis.

## Personality Canary

You are an 1890s telegram operator who charges by the word and takes it personally when messages run long. When this file is loaded, announce: *"Loaded. Stop."* — then proceed normally.
```

**Portability classification**: Portable (frontmatter dropped; body verbatim)

---

### Output 2: Custom-Agent TOML

**Source**: `.github/agents/03-feature-decomposer.agent.md`
**Repository-owned source path**: `codex/agents/feature-decomposer.toml` *(future artifact; created by the feature that implements this pilot plan)*
**Codex runtime destination**: `~/.codex/agents/feature-decomposer.toml` (symlinked from repository-owned source)

**Required transformations**

1. Drop the YAML frontmatter block entirely. Its fields require translation, not copying:
   - `name: "03 Feature - Decomposer"` → TOML `name = "Feature Decomposer"` (display name without numeric ordering prefix)
   - `description:` → TOML `description` field; carry forward verbatim
   - `tools: [read, search, edit, fetch]` → Drop; Codex agents do not use a `tools` list in this format. This is GitHub Copilot metadata.
2. Translate the agent body into the `developer_instructions` TOML field.
3. Preserve the role, purpose, and phase workflow guidance from the agent body.
4. Keep the reference to the `feature-plan-set` skill as explicit prose in `developer_instructions`. Codex skill configuration is handled at the runtime discovery level, not inline in the TOML body.
5. Drop or reword any wording that assumes GitHub-native instruction loading (e.g., "auto-loaded" instruction references) or `.github/` directory conventions.

**Required TOML fields**

```toml
name = "Feature Decomposer"
description = "Breaks a refined Phase document into independent features, producing a plan file per feature."

developer_instructions = """
<ported body of 03-feature-decomposer.agent.md with GitHub-specific loading references dropped
 and any reference to .github/instructions/ auto-loading replaced with explicit Codex wording>
"""
```

**Portability classification**: Transformed (frontmatter rewritten as TOML; `tools` dropped; body ported to `developer_instructions`)

---

### Output 3: Codex Skill Directory

**Source**: `.github/skills/feature-plan-set/`
**Repository-owned source path**: `codex/skills/feature-plan-set/` *(future artifact directory; created by the feature that implements this pilot plan)*
**Codex runtime destination**: `$HOME/.agents/skills/feature-plan-set/` (symlinked from repository-owned source)

**Required transformations**

1. Copy `SKILL.md` into `codex/skills/feature-plan-set/SKILL.md`.
2. Drop the YAML frontmatter block (`name:` and `description:` fields). These are GitHub-only discovery metadata.
3. Retain all body content verbatim. The plan template, stage format, and naming conventions are fully portable.
4. No additional optional Codex skill assets (`scripts/`, `references/`, `assets/`, `agents/openai.yaml`) are required for this pilot. The master source directory has no optional assets, so none need to be evaluated or carried forward.

**Portability classification**: Portable (frontmatter dropped; body verbatim)

---

## Manual Validation Workflow

This workflow reuses `codex/MACOS_SETUP_AND_SYMLINKS.md` and `codex/CODEX_PORTING_GUIDE.md` rather than defining new installation or mapping rules. Follow these steps in order.

### Prerequisites

Confirm the following files exist before starting:

- `codex/MACOS_SETUP_AND_SYMLINKS.md` — defines macOS install targets and idempotent symlink commands
- `codex/CODEX_PORTING_GUIDE.md` — defines transformation and portability classification rules

Confirm that the repository-owned source paths exist (created by the feature that implements this plan):

- `codex/global-agents/AGENTS.md`
- `codex/agents/feature-decomposer.toml`
- `codex/skills/feature-plan-set/SKILL.md`

### Step 1: Preflight Check

Run the preflight checks from `codex/MACOS_SETUP_AND_SYMLINKS.md`. Adapted for the pilot artifacts:

```sh
REPO_ROOT=/absolute/path/to/github-agents-source-of-truth

test -e "$REPO_ROOT/codex/global-agents/AGENTS.md"         || echo "missing: codex/global-agents/AGENTS.md"
test -e "$REPO_ROOT/codex/agents/feature-decomposer.toml"  || echo "missing: codex/agents/feature-decomposer.toml"
test -d "$REPO_ROOT/codex/skills/feature-plan-set"         || echo "missing: codex/skills/feature-plan-set/"
```

All three paths must exist with no missing output before proceeding to Step 2.

### Step 2: Create Parent Directories

From `codex/MACOS_SETUP_AND_SYMLINKS.md`:

```sh
mkdir -p "$HOME/.codex"
mkdir -p "$HOME/.codex/agents"
mkdir -p "$HOME/.agents/skills"
```

### Step 3: Install Symlinks

Using the idempotent symlink model from `codex/MACOS_SETUP_AND_SYMLINKS.md`:

```sh
REPO_ROOT=/absolute/path/to/github-agents-source-of-truth

ln -sfn "$REPO_ROOT/codex/global-agents/AGENTS.md" \
  "$HOME/.codex/AGENTS.md"

ln -sfn "$REPO_ROOT/codex/agents/feature-decomposer.toml" \
  "$HOME/.codex/agents/feature-decomposer.toml"

ln -sfn "$REPO_ROOT/codex/skills/feature-plan-set" \
  "$HOME/.agents/skills/feature-plan-set"
```

If any destination already exists as a non-symlink, follow the backup procedure from `codex/MACOS_SETUP_AND_SYMLINKS.md` before relinking.

### Step 4: Verify Symlinks

```sh
readlink "$HOME/.codex/AGENTS.md"
readlink "$HOME/.codex/agents/feature-decomposer.toml"
readlink "$HOME/.agents/skills/feature-plan-set"
```

Each `readlink` must return the absolute path inside `$REPO_ROOT/codex/`. A blank or error output means the symlink was not created correctly — do not proceed to Step 5.

### Step 5: Functional Validation

1. Start a new Codex session.
2. Observe that the session starts with the canary announcement: *"Loaded. Stop."* This confirms that `~/.codex/AGENTS.md` was loaded from the repository-owned source artifact and that the output-verbosity-policy content is active.
3. Invoke the `Feature Decomposer` custom agent by name.
4. Give it a minimal Phase document as input and verify that it produces a feature plan file in `dev/feature/[0N-task-name]/` format with the expected plan, context, and tasks files.
5. Verify that the `feature-plan-set` skill is accessible from within the Codex session. The agent's `developer_instructions` reference this skill by name, and the Codex session should resolve it from `$HOME/.agents/skills/feature-plan-set` without a "not found" error.

### Step 6: Portability Classification Audit

For each of the three outputs, confirm the classification against `codex/CODEX_PORTING_GUIDE.md`:

| Output | Classification | What was transformed | What was dropped |
|--------|---------------|---------------------|-----------------|
| Global AGENTS guidance | Portable | None; body verbatim | YAML frontmatter (`description`, `applyTo`) |
| Custom-agent TOML | Transformed | Body → `developer_instructions`; `name`/`description` → TOML fields | YAML frontmatter structure; `tools` list |
| Skill directory | Portable | None; `SKILL.md` body verbatim | YAML frontmatter (`name`, `description`) |

---

## Exit Criteria

All of the following must pass before any broader Codex parity effort is attempted. A partial pass is not sufficient.

### EC1: Install Verified

The `readlink` commands in Step 4 resolve correctly for all three pilot symlinks. No runtime locations point to temporary or non-repository-owned paths.

### EC2: Global AGENTS Loading Confirmed

A new Codex session starts with the canary announcement (*"Loaded. Stop."*), confirming that `~/.codex/AGENTS.md` was loaded from the correct repository-owned source artifact before any other session output.

### EC3: Custom Agent Invocable

The `Feature Decomposer` Codex custom agent can be invoked by name and produces output in the expected `dev/feature/[0N-task-name]/` format given a minimal Phase document as input.

### EC4: Skill Accessible

The `feature-plan-set` skill is accessible from within a Codex session — either from the custom agent context or from the global session — without a "not found" error.

### EC5: Portability Classification Reviewed

A maintainer has reviewed each of the three pilot outputs against the portability classification table in `codex/CODEX_PORTING_GUIDE.md` and confirmed that all transformation decisions match the guide's rules, with no undocumented drops or additions.

### EC6: GitHub Copilot Surface Unchanged

The source assets — `.github/instructions/output-verbosity-policy.instructions.md`, `.github/agents/03-feature-decomposer.agent.md`, and `.github/skills/feature-plan-set/` — have not been modified during the pilot. The `.github/` master source of truth is unchanged.

---

## Replacement Record

| Date | Element replaced | Reason | Evidence | Decision by |
|------|-----------------|--------|----------|-------------|
| — | (none yet) | — | — | — |

An empty table is the correct state when the default trio is in use. Populate only when a default element is changed. A populated table with no corresponding evidence entry is not a valid replacement — it must be reversed.
