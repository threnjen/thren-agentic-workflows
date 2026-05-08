# 02 Codex macOS Setup Guide Tasks

## Stage 0: Test Prerequisites

- [ ] Assess whether this documentation-only slice needs a `@z-test-writer` prerequisite or whether manual path and policy review is the intended validation gate.
- [ ] Record the baseline validation approach for the `codex/` docs slice before authoring the guide.

## Stage 1: Author the macOS Setup and Symlink Guide

- [ ] Create `codex/MACOS_SETUP_AND_SYMLINKS.md` in the repository-owned `codex/` area.
- [ ] Document the correct macOS runtime install targets for global Codex guidance, custom agents, and skills: `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md`, `~/.codex/agents/`, and `$HOME/.agents/skills/`.
- [ ] Explain how repository-owned `codex/` sources relate to runtime `.codex/` and `$HOME/.agents/skills/` destinations on macOS.
- [ ] Add reversible symlink examples that point from each runtime location back to repository-owned Codex artifacts rather than to checked-in repo `AGENTS.md` files.
- [ ] Keep the guide documentation-only by using clearly labeled repository-owned source examples or placeholders until sibling source-layout artifacts land.

## Stage 2: Add Idempotency and Safety Guidance

- [ ] Add preflight steps that tell readers how to inspect existing files or symlinks before replacing anything.
- [ ] Document parent-directory creation required for a clean macOS machine.
- [ ] Use `ln -sfn` in the examples and explain why the commands are idempotent and reversible.
- [ ] Add rollback or relink steps for safely replacing existing targets.
- [ ] Make the global AGENTS rule explicit: AGENTS-derived content installs into the global Codex AGENTS layer, not either repository's checked-in `AGENTS.md`.
- [ ] Review the finished guide against the Phase 02 summary and discovery context for path accuracy, terminology consistency, and policy wording.