# Claude Symlink Setup

This guide explains how to wire the repository Claude assets into the local Claude CLI config.

## Goal

Make these paths available automatically:

- Repository agents: `claude/agents/`
- Repository skills: `claude/skills/` (symlink to `.github/skills/`)
- Repository learnings: `claude/learnings/` (symlink to `.github/learnings/`)
- Local Claude config: `~/.claude/{agents,skills,learnings}`

## 1) Create Repo-Level Symlinks

From the repository root:

```bash
cd claude
ln -sfn ../.github/skills skills
ln -sfn ../.github/learnings learnings
```

Verify:

```bash
ls -la skills learnings
```

Expected:

- `skills -> ../.github/skills`
- `learnings -> ../.github/learnings`

## 2) Create Local ~/.claude Symlinks

Use absolute paths so links are stable from any working directory.

```bash
mkdir -p ~/.claude

ln -sfn /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/agents ~/.claude/agents
ln -sfn /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/skills ~/.claude/skills
ln -sfn /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/learnings ~/.claude/learnings
```

Verify:

```bash
ls -la ~/.claude/agents ~/.claude/skills ~/.claude/learnings
```

## 3) Quick Health Check

```bash
ls /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/agents | wc -l
```

If links are correct, Claude should discover all agents/skills/learnings from this repository automatically.

## Notes

- `ln -sfn` force-updates existing symlinks in place.
- If a target path exists as a real folder (not a symlink), move or remove it before linking.
- Keep `.github/` as source-of-truth for skills and learnings; `claude/` consumes via symlink.
