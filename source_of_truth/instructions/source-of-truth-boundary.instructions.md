---
description: "Constrains agent/instruction/skill work in this repo to the .github source-of-truth surfaces and treats claude/opencode/codex outputs as downstream unless Evangelize is doing intentional porting."
applyTo: "source_of_truth/agents/**"
---

# Source-of-Truth Boundary

When you are working in **this repository** on agent definitions, instruction files, skill content, or agent behavior, treat these paths as the only source-of-truth authoring surfaces:

- `.github/agents/`
- `.github/instructions/`
- `.github/skills/`

For those tasks, treat these directories as downstream/generated or platform-specific outputs and **ignore them during normal discovery, planning, and editing**:

- `claude/`
- `opencode/`
- `codex/`

## Default Rule

- Make the change in `.github/` first.
- Do not duplicate the same logical edit manually in `claude/`, `opencode/`, or `codex/`.
- Do not broaden discovery into those downstream directories just to confirm what should be changed. The answer should come from `.github/`.

## How To Handle Downstream Outputs

- Assume downstream platform files will be regenerated or synchronized from `.github/`.
- If you need to verify propagation behavior, inspect downstream files only after the `.github/` source change is complete.
- Prefer rerunning the repo's propagation flow over hand-editing generated outputs.

## Exception

The **Evangelize** agent is the explicit exception. When the assigned role is Evangelize, it may read and update `claude/`, `opencode/`, and `codex/` on purpose as part of porting or synchronization work.

Outside Evangelize, only touch those downstream directories when the user explicitly asks for propagation debugging or output verification, and even then keep `.github/` as the change source.