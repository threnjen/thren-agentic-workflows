# Claude Symlink Setup

This guide explains how to wire the repository Claude assets into the local Claude CLI config.

## Goal

Make these paths available automatically:

- Repository agents: `claude/agents/`
- Repository skills: `claude/skills/` (symlink to `.github/skills/`)
- Repository learnings: `claude/learnings/` (symlink to `.github/learnings/`)
- Local Claude config: a real `~/.claude/agents/` directory containing one symlink per agent file, plus `~/.claude/{skills,learnings}` symlinks

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

## 2) Create Local ~/.claude Agent Symlinks

Use absolute paths so links are stable from any working directory.

```bash
mkdir -p ~/.claude
rm -f ~/.claude/agents
mkdir -p ~/.claude/agents

for src in /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/agents/*; do
	ln -sfn "$src" "$HOME/.claude/agents/$(basename "$src")"
done

ln -sfn /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/skills ~/.claude/skills
ln -sfn /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/learnings ~/.claude/learnings
```

Verify:

```bash
ls -ld ~/.claude/agents ~/.claude/skills ~/.claude/learnings
find -H ~/.claude/agents -maxdepth 1 -mindepth 1 -exec ls -ld {} \;
```

## 3) Quick Health Check

```bash
ls /Users/jennywadkins/github_repos/github-agents-source-of-truth/claude/agents | wc -l
```

If links are correct, Claude should discover all agents/skills/learnings from this repository automatically.

## Notes

- `~/.claude/agents` should be a real directory, not a symlink.
- `ln -sfn` force-updates each individual agent symlink in place.
- The `rm -f ~/.claude/agents` step is safe only when `~/.claude/agents` is currently a symlink. If it is a real directory on your machine, inspect and back it up before replacing it.
- Keep `.github/` as source-of-truth for skills and learnings; `claude/` consumes via symlink.
