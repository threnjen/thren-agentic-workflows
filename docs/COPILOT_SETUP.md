# Using The Agents With GitHub Copilot

GitHub Copilot in VS Code discovers custom agents, instructions, and skills from the
`.github/` directory of folders in your **workspace** — not from a user-global config
directory like the other harnesses. That means the way to use this library with
Copilot is to open this repository in your VS Code workspace **alongside** your
project directory.

## Setup

1. **Deploy the github harness** from this repository root so `.github/` is populated:

   ```bash
   python3 deploy_agents.py --harness github
   ```

   This mirrors the agent library into this repo's `.github/` (agents, instructions,
   skills) and splices the baseline guidance into
   `.github/copilot-instructions.md`.

2. **Open your project in VS Code**, then add this repository as a second workspace
   folder: **File → Add Folder to Workspace…** and select this repo's root.

3. **Save the workspace** (File → Save Workspace As…) so the pairing persists — for
   example `my-project.code-workspace`:

   ```jsonc
   {
     "folders": [
       { "path": "/path/to/my-project" },
       { "path": "/path/to/thren-agentic-workflows" }
     ]
   }
   ```

4. **Pick an agent** in Copilot Chat. With this repo in the workspace, the agents from
   `.github/agents/` appear in the Copilot agent picker; the instructions and skills
   under `.github/` are available to it as well.

Do your actual work in the project folder — this repo just rides along in the
workspace to supply the agent definitions.

## Why alongside, not inside

Copilot scopes `.github/` discovery to workspace folders. Copying this library's
`.github/` into every project would duplicate generated content that goes stale;
adding the repo as a workspace folder gives every project the same, always-current
agent set from one place. Re-run `python3 deploy_agents.py --harness github` here
after pulling updates and every paired workspace sees the refreshed agents.

## Notes And Limits

- The `.github/` tree in this repo is generated and gitignored — it exists only after
  a deploy run on your machine. If the agent picker shows nothing, run the deploy
  command in step 1 first.
- Because `.github/` here is not committed, Copilot features that read from the
  repository on github.com (as opposed to your local VS Code workspace) will not see
  these agents or `copilot-instructions.md`.
- Your own project's `.github/copilot-instructions.md` and instructions still apply to
  its folder as usual; the two folders' configurations coexist in the workspace.

## Related References

- [../INSTALLATION.md](../INSTALLATION.md) — deploy commands and destinations
- [porting/README.md](porting/README.md) — per-harness porting guides
