# Connecting This Repo to Your AI Harness

This repo ships agent definitions, skills, and instructions for three harnesses. Pick the section for what you use.

| Harness | Agents directory | Skills directory |
|---------|-----------------|-----------------|
| GitHub Copilot | `.github/agents/` | `.github/skills/` |
| Claude Code | `claude/agents/` | `claude/skills/` → `.github/skills/` |
| OpenCode | `opencode/agents/` | `.github/skills/` |

---

## GitHub Copilot (VS Code)

Copilot reads `.github/agents/`, `.github/skills/`, and `.github/instructions/` from every folder open in your VS Code workspace. The simplest way to make them available in any project is to open this repo as a second workspace folder alongside your project.

### Option A: Multi-root workspace file (recommended)

Create a `.code-workspace` file in your project (or anywhere convenient) and add both folders:

```json
{
  "folders": [
    { "path": "/absolute/path/to/your-project" },
    { "path": "/absolute/path/to/github-agents-source-of-truth" }
  ]
}
```

Open the `.code-workspace` file in VS Code. Copilot will pick up agents, skills, and instructions from both folders. The agents appear in the Copilot Chat `@` agent picker.

### Option B: Add folder to existing workspace

With your project already open in VS Code:

1. **File → Add Folder to Workspace…**
2. Select the root of this repo
3. Save the workspace when prompted (optional — VS Code will remember it)

### Notes

- The `.github/instructions/` files use `applyTo` globs to inject conventions into specific file types automatically — no manual invocation needed.
- To use only the `AGENTS.md` templates without the full agent system, copy `nodejs/AGENTS.md` or `python/AGENTS.md` into your project instead.

---

## Claude Code

Claude Code reads agents from `~/.claude/agents/`, skills from `~/.claude/skills/`, and learnings from `~/.claude/learnings/`. Symlinking this repo's directories there makes them available in every Claude Code session.

### Mac / Linux

```bash
REPO="/absolute/path/to/github-agents-source-of-truth"

mkdir -p ~/.claude

ln -sfn "$REPO/claude/agents"    ~/.claude/agents
ln -sfn "$REPO/claude/skills"    ~/.claude/skills
ln -sfn "$REPO/claude/learnings" ~/.claude/learnings
```

Verify:

```bash
ls -la ~/.claude/agents ~/.claude/skills ~/.claude/learnings
```

Expected output: each shows as a symlink pointing into this repo.

### Windows (PowerShell — run as Administrator or with Developer Mode enabled)

Symlinks on Windows require either Developer Mode (`Settings → System → For developers → Developer Mode`) or an elevated PowerShell session.

```powershell
$REPO = "C:\absolute\path\to\github-agents-source-of-truth"
$Claude = "$env:USERPROFILE\.claude"

New-Item -ItemType Directory -Force -Path $Claude

New-Item -ItemType SymbolicLink -Path "$Claude\agents"    -Target "$REPO\claude\agents"
New-Item -ItemType SymbolicLink -Path "$Claude\skills"    -Target "$REPO\claude\skills"
New-Item -ItemType SymbolicLink -Path "$Claude\learnings" -Target "$REPO\claude\learnings"
```

Verify:

```powershell
Get-Item "$env:USERPROFILE\.claude\agents", "$env:USERPROFILE\.claude\skills", "$env:USERPROFILE\.claude\learnings" | Select-Object Name, LinkType, Target
```

#### Windows note: in-repo symlinks

`claude/skills` and `claude/learnings` are symlinks inside the repo (pointing to `.github/skills` and `.github/learnings`). On Windows, Git may check these out as plain text files containing the target path rather than real symlinks, depending on your `core.symlinks` setting.

If the `claude/skills` or `claude/learnings` directories appear as text files, fix them:

```powershell
# Enable symlink support in git (run once per repo clone)
git config core.symlinks true
git checkout -- claude/skills claude/learnings
```

Or create them manually:

```powershell
$REPO = "C:\absolute\path\to\github-agents-source-of-truth"
Remove-Item "$REPO\claude\skills"    -ErrorAction SilentlyContinue
Remove-Item "$REPO\claude\learnings" -ErrorAction SilentlyContinue
New-Item -ItemType SymbolicLink -Path "$REPO\claude\skills"    -Target "$REPO\.github\skills"
New-Item -ItemType SymbolicLink -Path "$REPO\claude\learnings" -Target "$REPO\.github\learnings"
```

### Verify Claude Can See the Agents

Start Claude Code and run:

```
/agents
```

You should see the full list of agents from `claude/agents/`.

---

## OpenCode

OpenCode reads agents from `~/.config/opencode/agents/` and skills from `~/.config/opencode/skills/`. The `opencode/agents/` directory in this repo contains versions of the `.github/agents/` files converted to OpenCode's frontmatter format.

### Mac / Linux

```bash
REPO="/absolute/path/to/github-agents-source-of-truth"

mkdir -p ~/.config/opencode

ln -sfn "$REPO/opencode/agents"  ~/.config/opencode/agents
ln -sfn "$REPO/.github/skills"   ~/.config/opencode/skills
```

Verify:

```bash
ls -la ~/.config/opencode/agents ~/.config/opencode/skills
```

Expected output: each shows as a symlink pointing into this repo.

### Windows (PowerShell — run as Administrator or with Developer Mode enabled)

```powershell
$REPO    = "C:\absolute\path\to\github-agents-source-of-truth"
$OcDir   = "$env:USERPROFILE\.config\opencode"

New-Item -ItemType Directory -Force -Path $OcDir

New-Item -ItemType SymbolicLink -Path "$OcDir\agents" -Target "$REPO\opencode\agents"
New-Item -ItemType SymbolicLink -Path "$OcDir\skills" -Target "$REPO\.github\skills"
```

Verify:

```powershell
Get-Item "$env:USERPROFILE\.config\opencode\agents", "$env:USERPROFILE\.config\opencode\skills" | Select-Object Name, LinkType, Target
```

> **Config path note:** OpenCode follows the XDG convention and uses `~/.config/opencode/` on all platforms. If your OpenCode installation uses a different path, check `opencode --help` or the OpenCode docs for your version.

### Per-Project Setup (any OS)

To scope agents and skills to a single project without touching the global config, create a `.opencode/` directory in that project and symlink into it:

**Mac / Linux:**

```bash
REPO="/absolute/path/to/github-agents-source-of-truth"
PROJECT="/absolute/path/to/your-project"

mkdir -p "$PROJECT/.opencode"
ln -sfn "$REPO/opencode/agents" "$PROJECT/.opencode/agents"
ln -sfn "$REPO/.github/skills"  "$PROJECT/.opencode/skills"
```

**Windows:**

```powershell
$REPO    = "C:\absolute\path\to\github-agents-source-of-truth"
$Project = "C:\absolute\path\to\your-project"

New-Item -ItemType Directory -Force -Path "$Project\.opencode"
New-Item -ItemType SymbolicLink -Path "$Project\.opencode\agents" -Target "$REPO\opencode\agents"
New-Item -ItemType SymbolicLink -Path "$Project\.opencode\skills" -Target "$REPO\.github\skills"
```

---

## Keeping Everything Updated

Because the symlinks point directly into this repo, all three harnesses see changes immediately after a `git pull` — no re-linking required.

If agents in `.github/agents/` are updated, the equivalent changes should be applied to `opencode/agents/` as well, since those are maintained separately in OpenCode format.
