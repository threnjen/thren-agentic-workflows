# OpenCode Symlink Setup

This document explains how to wire the `opencode/` directory in this repo into OpenCode's global config and per-project config.

## Directory Layout

```
github-agents-source-of-truth/
├── opencode/
│   └── agents/          ← converted OpenCode agent files (source of truth)
├── .github/
│   └── skills/          ← skills directory (source of truth)
└── opencode/
    └── SYMLINK_SETUP.md ← this file
```

## Global Config Setup (`~/.config/opencode/`)

OpenCode reads agents from `~/.config/opencode/agents/` and skills from `~/.config/opencode/skills/`.

Run these commands once (adjust `REPO` to your local path):

```bash
REPO="$HOME/github_repos/github-agents-source-of-truth"

# Agents: point global opencode config at this repo's opencode/agents/
ln -sfn "$REPO/opencode/agents" "$HOME/.config/opencode/agents"

# Skills: point global opencode config at this repo's .github/skills/
ln -sfn "$REPO/.github/skills" "$HOME/.config/opencode/skills"
```

This makes all agents and skills available in every OpenCode session globally.

## Per-Project Setup (`.opencode/` in a project)

To make agents and skills available within a specific project without global config, create symlinks inside the project's `.opencode/` directory:

```bash
REPO="$HOME/github_repos/github-agents-source-of-truth"
PROJECT="/path/to/your/project"

mkdir -p "$PROJECT/.opencode"

# Agents
ln -sfn "$REPO/opencode/agents" "$PROJECT/.opencode/agents"

# Skills
ln -sfn "$REPO/.github/skills" "$PROJECT/.opencode/skills"
```

## Verifying the Setup

After symlinking, confirm OpenCode sees the agents:

```bash
# List resolved symlink targets
ls -la ~/.config/opencode/agents/
ls -la ~/.config/opencode/skills/
```

You should see the agent `.md` files from `opencode/agents/` and skill directories from `.github/skills/`.

## Keeping Agents Updated

Because the symlinks point directly into this repo, any updates to `opencode/agents/` or `.github/skills/` are immediately available to OpenCode — no re-linking needed. Just `git pull` in this repo.

## Agent Source of Truth

The `opencode/agents/` files are converted from `.github/agents/` for OpenCode compatibility. If you modify agent behavior:

1. Edit the source in `.github/agents/*.agent.md`
2. Apply the equivalent change to `opencode/agents/*.md`

The key differences between the two formats are:
- Frontmatter: OpenCode uses `permission:` object instead of `tools:` list
- Models: OpenCode uses `anthropic/claude-*` model IDs instead of Copilot display names
- Subagents: OpenCode uses `mode: subagent` + `hidden: true` instead of `user-invocable: false`
