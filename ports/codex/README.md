# Codex Source Layout

This directory is the repository-owned authoring area for Codex work in this repo.

It is intentionally separate from runtime Codex installation and configuration paths:

- `codex/` holds repo-owned documentation and future source artifacts.
- `.codex/` holds repo-scoped runtime Codex configuration or installed runtime assets.
- `~/.codex/` holds user-scoped Codex configuration, global AGENTS guidance, and custom agents.
- `$HOME/.agents/skills/` holds user-scoped Codex skills.

## What Lives Here Today

Phase 02 starts this area with a single layout contract:

- `README.md` defines what belongs in the repository-owned Codex surface and what must stay in runtime locations.

As additional Phase 02 documentation is authored, Codex-facing reference documents should be added here rather than scattered across unrelated folders.

## Reserved Future Artifact Categories

This phase does not create runnable Codex artifacts, but it reserves room for three future repository-owned source categories:

- Global guidance source for Codex AGENTS content that may later be installed into `~/.codex/AGENTS.md` or `~/.codex/AGENTS.override.md`.
- Custom agent source material that may later produce TOML files installed into `~/.codex/agents/` or repo-local `.codex/agents/`.
- Skill-copy source material that may later be installed into `$HOME/.agents/skills/` or repo-local `.agents/skills/`.

If later Phase 02 work needs directories for those categories, add them here only after updating this layout contract first.

## Layout Rules

- Keep repository-owned Codex docs and source artifacts under `codex/`.
- Keep live runtime configuration out of `codex/`; do not treat `.codex/config.toml` as source material for this directory.
- Do not create user-home install content in this repo. Shared docs may describe `~/.codex/` and `$HOME/.agents/skills/`, but those paths are runtime destinations, not authoring locations.
- Do not treat `codex/` as a direct mirror of `.github/`, `opencode/`, or `claude/`. Codex uses a different installation model, so this directory defines the mapping rather than mirroring checked-in runtime copies.