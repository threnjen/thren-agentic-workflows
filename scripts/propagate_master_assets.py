#!/usr/bin/env python3
"""Propagate .github master assets to claude, opencode, and codex targets.

This script treats `.github/agents` as the canonical source for duplicated agent files,
and regenerates target-platform variants.

It also watches `.github/agents`, `.github/skills`, and `.github/instructions` so any
save in those folders immediately triggers a propagation run.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shlex
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple, Union


REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_AGENTS_DIR = REPO_ROOT / ".github" / "agents"
GITHUB_INSTRUCTIONS_DIR = REPO_ROOT / ".github" / "instructions"
WATCH_DIRS = [
    REPO_ROOT / ".github" / "agents",
    REPO_ROOT / ".github" / "skills",
    REPO_ROOT / ".github" / "instructions",
    REPO_ROOT / ".github" / "hooks",
    REPO_ROOT / ".github" / "learnings",
]

CLAUDE_AGENTS_DIR = REPO_ROOT / "claude" / "agents"
CLAUDE_COMMANDS_DIR = REPO_ROOT / "claude" / "commands"
OPENCODE_AGENTS_DIR = REPO_ROOT / "opencode" / "agents"
CODEX_AGENTS_DIR = REPO_ROOT / "codex" / "agents"
CODEX_PROFILES_DIR = REPO_ROOT / "codex" / "profiles"
GITHUB_SKILLS_DIR = REPO_ROOT / ".github" / "skills"
CODEX_SKILLS_DIR = REPO_ROOT / "codex" / "skills"
GITHUB_HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
CLAUDE_SETTINGS_FILE = REPO_ROOT / ".claude" / "settings.json"
CODEX_HOOKS_FILE = REPO_ROOT / ".codex" / "hooks.json"
OPENCODE_PLUGINS_DIR = REPO_ROOT / ".opencode" / "plugins"


GENERATED_AGENT_HEADER = "# Generated from .github/agents source-of-truth. Do not edit manually."
# Markdown counterpart to GENERATED_AGENT_HEADER. That constant is a TOML comment,
# correct for codex/agents/*.toml but rendered as an H1 heading by Markdown, so it
# cannot be reused for the Claude/OpenCode agent and command outputs. This mirrors
# the HTML-comment form of GENERATED_SKILL_HEADER, which is already Markdown-safe,
# while naming the source root these outputs actually come from.
GENERATED_AGENT_MARKDOWN_HEADER = "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->"
GENERATED_SKILL_HEADER = "<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->\n"
GENERATED_OPENCODE_PLUGIN_HEADER = "// Generated from .github/hooks source-of-truth. Do not edit manually.\n"
HOOK_SOURCE_KEY = "$source"
RETIRED_HOOK_ASSETS = (
    "bash-safety.json",
    "protect-files.json",
    "scripts/bash-safety.sh",
    "scripts/protect-files.sh",
    "scripts/protect-files.py",
)

# Default translation from VS Code Copilot hook events → target tool events.
# Keys are VS Code event names. Values map tool name → list of target event names.
# Overridden per-file via $meta.<VsCodeEvent>.<tool> in the hook JSON.
HOOK_EVENT_MAP: Dict[str, Dict[str, List[str]]] = {
    "Stop":             {"claude": ["Stop", "Notification"], "codex": ["Stop"],          "opencode": ["session.idle"]},
    "SessionStart":     {"claude": ["SessionStart"],          "codex": ["SessionStart"],  "opencode": ["session.created"]},
    "PreToolUse":       {"claude": ["PreToolUse"],            "codex": ["PreToolUse"],    "opencode": ["tool.execute.before"]},
    "PostToolUse":      {"claude": ["PostToolUse"],           "codex": ["PostToolUse"],   "opencode": ["tool.execute.after"]},
    "UserPromptSubmit": {"claude": ["UserPromptSubmit"],      "codex": ["UserPromptSubmit"], "opencode": []},
    "SubagentStop":     {"claude": ["SubagentStop"],          "codex": ["SubagentStop"],  "opencode": []},
    "PreCompact":       {"claude": ["PreCompact"],            "codex": ["PreCompact"],    "opencode": []},
}

# Agents that should not be propagated to any platform output directory.
# Add a source slug string here to exclude an agent during propagation.
# Currently empty — all source agents are propagated.
PROPAGATION_EXCLUDE: set[str] = set()


OPENCODE_FILE_ALIASES = {
    "docs-writer": "docs-writer",
    "web-research-specialist": "web-researcher",
    "audit-code-or-infra": "audit-code-infra-refactor",
}

CLAUDE_FILE_ALIASES = {
    "docs-writer": "docs-writer",
    "web-research-specialist": "web-researcher",
    "audit-code-or-infra": "audit-code-infra-refactor",
}


@dataclass
class SourceAgent:
    path: Path
    rel_path: str
    source_slug: str
    name: str
    description: str
    tools: List[str]
    subagents: List[str]
    user_invocable: bool
    body: str


@dataclass
class InstructionDoc:
    path: Path
    apply_to_patterns: List[str]
    body: str


FrontmatterValue = Union[str, List[str]]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_symlink():
        try:
            path.unlink()
        except OSError:
            pass
    elif path.exists() and path.is_file():
        try:
            if _read_text(path) == content:
                return False
        except OSError:
            pass
        try:
            path.unlink()
        except OSError:
            pass
    elif path.exists() and path.is_dir():
        try:
            shutil.rmtree(path)
        except OSError:
            pass

    if path.exists() and path.is_dir():
        return False

    path.write_text(content, encoding="utf-8")
    return True


def _generated_marker_line_index(text: str) -> int:
    """The one line index at which a generated marker is written, or -1 for none.

    Single source of truth shared by `_with_generated_marker` (which writes the
    marker there) and `_is_generated_output` (which looks for it only there), so
    the writer and the guard cannot drift apart.

    The position is line 0 for output with no YAML frontmatter (the TOML roots),
    and the line immediately below the closing `---` otherwise. Text whose
    frontmatter is opened but never closed has no valid position and returns -1:
    it is never marked, and therefore never pruned.
    """
    if not text.startswith("---\n"):
        return 0
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index] == "---":
            return index + 1
    return -1


def _with_generated_marker(text: str, marker: str) -> str:
    """Insert `marker` immediately below the YAML frontmatter block.

    The marker must never sit above the opening `---`: consumers parse that block
    and would stop seeing it as frontmatter. Text whose frontmatter is unterminated
    is returned unchanged rather than marked, which leaves it unprunable — an
    unmarked file is never deleted, so failing closed here is the safe direction.
    """
    marker_line = marker.strip("\n")
    index = _generated_marker_line_index(text)
    if index < 0:
        return text

    lines = text.splitlines(keepends=True)
    if index < len(lines) and lines[index].rstrip("\n") == marker_line:
        return text

    return "".join(lines[:index]) + marker_line + "\n" + "".join(lines[index:])


def _is_generated_output(path: Path, marker: str) -> bool:
    """Whether `path` carries `marker` at the exact line the emitter writes it to.

    Positional rather than a whole-file search, and deliberately not the original
    `startswith` prefix check either. Both looser rules are unsafe in opposite
    directions:

    - `startswith` is what silently disabled the codex/skills prune. Generated
      Markdown opens with YAML frontmatter, so its marker sits below that block
      rather than at byte zero; the check matched 0 of 24 files for years while
      reading as implemented.
    - A whole-file search would delete any hand-maintained file that merely
      *quotes* the marker — for example a README documenting the convention, in a
      fenced code block. `claude/agents/README.md` is exactly such a file, living
      inside a pruned root, and it is the file AC5 exists to protect.

    Checking the single position the emitter writes to matches every real
    generated file while making a quoted marker in a file body inert.

    An unreadable file is not a confirmed orphan, so read errors report False.
    """
    try:
        text = _read_text(path)
    except OSError:
        return False
    index = _generated_marker_line_index(text)
    if index < 0:
        return False
    lines = text.splitlines()
    return index < len(lines) and lines[index] == marker.strip("\n")


def _prune_orphaned_outputs(
    directory: Path,
    pattern: str,
    expected: set[Path],
    marker: str,
) -> int:
    """Delete generated files under `directory` whose source asset is gone.

    Deletion requires BOTH conditions: absent from `expected` AND positively
    identified as generated by `marker`. Absence alone is not enough —
    `claude/agents/README.md` is a real, hand-maintained file inside a generated
    root, and the marker guard is the only thing that saves it.

    A missing root has nothing to prune and is never created here.
    """
    if not directory.is_dir():
        return 0

    removed = 0
    for path in sorted(directory.glob(pattern)):
        if path in expected:
            continue
        # A symlink is never something this propagator wrote; unlinking through one
        # could reach a real file outside the generated root.
        if path.is_symlink() or not path.is_file():
            continue
        if not _is_generated_output(path, marker):
            continue
        path.unlink()
        removed += 1
    return removed


def _prune_orphaned_skill_dirs(skills_dir: Path, expected: set[Path], marker: str) -> int:
    """Delete generated skill directories under `skills_dir` whose source is gone.

    Same two-condition rule as `_prune_orphaned_outputs`, applied to a directory via
    its SKILL.md. Skills are removed as a tree because a skill is a directory of
    assets; this is the one path where recursive removal is in scope.
    """
    if not skills_dir.is_dir():
        return 0

    removed = 0
    for dest_dir in sorted(skills_dir.iterdir()):
        if dest_dir in expected or dest_dir.is_symlink() or not dest_dir.is_dir():
            continue
        skill_md = dest_dir / "SKILL.md"
        if skill_md.is_symlink() or not skill_md.is_file():
            continue
        if not _is_generated_output(skill_md, marker):
            continue
        shutil.rmtree(dest_dir)
        removed += 1
    return removed


def _parse_frontmatter(text: str) -> Tuple[Dict[str, FrontmatterValue], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    fm_text = text[4:end]
    body = text[end + 5 :]

    data: Dict[str, FrontmatterValue] = {}
    lines = fm_text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value:
            data[key] = value
            index += 1
            continue

        # Support YAML block-list values:
        # tools:
        #   - read
        #   - edit
        block_items: List[str] = []
        probe = index + 1
        while probe < len(lines):
            probe_line = lines[probe]
            if not probe_line.startswith((" ", "\t")):
                break
            item = probe_line.strip()
            if item.startswith("- "):
                block_items.append(item[2:].strip())
            probe += 1

        if block_items:
            data[key] = block_items
            index = probe
            continue

        data[key] = ""
        index += 1

    return data, body


def _parse_list_value(raw: FrontmatterValue) -> List[str]:
    if isinstance(raw, list):
        cleaned = [item.strip().strip('"').strip("'") for item in raw]
        return [item for item in cleaned if item]

    raw = str(raw).strip()
    if not raw:
        return []

    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        parts = [p.strip() for p in inner.split(",")]
    else:
        parts = [p.strip() for p in raw.split(",")]

    cleaned: List[str] = []
    for part in parts:
        item = part.strip().strip('"').strip("'")
        if item:
            cleaned.append(item)
    return cleaned


def _parse_bool(raw: FrontmatterValue, default: bool = True) -> bool:
    if raw is None:
        return default
    value = str(raw).strip().lower()
    if value in {"true", "yes", "1"}:
        return True
    if value in {"false", "no", "0"}:
        return False
    return default


def _extract_source_slug(path: Path) -> str:
    name = path.name
    if name.endswith(".agent.md"):
        return name[: -len(".agent.md")]
    if name.endswith(".md"):
        return name[: -len(".md")]
    return path.stem


def load_source_agents(repo_root: Path | None = None) -> List[SourceAgent]:
    repo_root = repo_root or REPO_ROOT
    agents_dir = repo_root / ".github" / "agents"

    agents: List[SourceAgent] = []
    for path in sorted(agents_dir.glob("*.md")):
        text = _read_text(path)
        fm, body = _parse_frontmatter(text)

        # Agent definitions always include name + description in this repo.
        if "name" not in fm or "description" not in fm:
            continue

        rel_path = path.relative_to(repo_root).as_posix()
        source_slug = _extract_source_slug(path)

        if source_slug in PROPAGATION_EXCLUDE:
            continue

        name = str(fm.get("name", "")).strip().strip('"').strip("'")
        description = str(fm.get("description", "")).strip().strip('"').strip("'")
        tools = _parse_list_value(fm.get("tools", ""))
        subagents = _parse_list_value(fm.get("agents", ""))
        user_invocable = _parse_bool(fm.get("user-invocable"), default=True)

        agents.append(
            SourceAgent(
                path=path,
                rel_path=rel_path,
                source_slug=source_slug,
                name=name,
                description=description,
                tools=tools,
                subagents=subagents,
                user_invocable=user_invocable,
                body=body.strip() + "\n",
            )
        )
    return agents


def load_instruction_docs(repo_root: Path | None = None) -> List[InstructionDoc]:
    repo_root = repo_root or REPO_ROOT
    instructions_dir = repo_root / ".github" / "instructions"

    docs: List[InstructionDoc] = []
    for path in sorted(instructions_dir.glob("*.instructions.md")):
        text = _read_text(path)
        fm, body = _parse_frontmatter(text)

        raw_apply_to = fm.get("applyTo", "")
        patterns = [p.strip() for p in str(raw_apply_to).split(",") if p.strip()]

        docs.append(
            InstructionDoc(
                path=path,
                apply_to_patterns=patterns,
                body=body.strip() + "\n",
            )
        )
    return docs


def applicable_instructions(agent: SourceAgent, instruction_docs: List[InstructionDoc]) -> List[InstructionDoc]:
    applicable: List[InstructionDoc] = []
    for doc in instruction_docs:
        if any(fnmatch.fnmatch(agent.rel_path, pattern) for pattern in doc.apply_to_patterns):
            applicable.append(doc)
    return applicable


def map_tools_for_claude(source_tools: List[str]) -> List[str]:
    mapping = {
        "read": ["Read"],
        "search": ["Grep", "Glob"],
        "edit": ["Edit", "Write"],
        "fetch": ["WebFetch"],
        "web/fetch": ["WebFetch"],
        "web/search": ["WebFetch"],
        "web/screenshot": ["WebFetch"],
        "execute": ["Bash"],
        "agent": ["Agent"],
    }

    result: List[str] = ["Skill"]
    for tool in source_tools:
        for mapped in mapping.get(tool, []):
            if mapped not in result:
                result.append(mapped)
    return result


def map_permissions_for_opencode(source_tools: List[str]) -> Dict[str, str]:
    mapping = {
        "read": ["read"],
        "search": ["grep", "glob"],
        "edit": ["edit"],
        "fetch": ["webfetch"],
        "web/fetch": ["webfetch"],
        "web/search": ["webfetch"],
        "web/screenshot": ["webfetch"],
        "execute": ["bash"],
        "agent": ["task"],
        "todo": ["todowrite"],
    }

    result: Dict[str, str] = {}
    for tool in source_tools:
        for mapped in mapping.get(tool, []):
            result[mapped] = "allow"
    return result


def _sanitize_slug(value: str) -> str:
    slug = value.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-")


def _strip_numeric_prefix(slug: str) -> str:
    return re.sub(r"^\d+[a-z]?-", "", slug)


def _discover_existing_stems(directory: Path) -> set[str]:
    if not directory.exists():
        return set()
    return {path.stem for path in directory.glob("*.md")}


def _choose_existing_stem(candidates: List[str], existing_stems: set[str]) -> str | None:
    for candidate in candidates:
        if candidate in existing_stems:
            return candidate
    return None


def _claude_filename_for(agent: SourceAgent, existing_stems: set[str]) -> str:
    stripped = _strip_numeric_prefix(agent.source_slug)
    alias = CLAUDE_FILE_ALIASES.get(agent.source_slug)
    candidates = [
        agent.source_slug,
        alias or "",
        stripped,
        f"z-{stripped}",
    ]
    existing = _choose_existing_stem([c for c in candidates if c], existing_stems)
    if existing:
        return f"{existing}.md"

    base = alias or stripped
    if not agent.user_invocable and not base.startswith("z-"):
        base = f"z-{base}"
    return f"{base}.md"


def _claude_identifier_for(agent: SourceAgent, existing_stems: set[str]) -> str:
    return Path(_claude_filename_for(agent, existing_stems)).stem


def _build_agent_reference_map(
    agents: List[SourceAgent],
    identifier_for: Callable[[SourceAgent], str],
) -> Dict[str, str]:
    return {
        agent.name: identifier_for(agent)
        for agent in agents
        if agent.name
    }


def _rewrite_agent_references(text: str, reference_map: Dict[str, str], preserve_at_sign: bool) -> str:
    rewritten = text
    for source_name, identifier in sorted(reference_map.items(), key=lambda item: len(item[0]), reverse=True):
        at_replacement = f"@{identifier}" if preserve_at_sign else identifier
        rewritten = rewritten.replace(f"@{source_name}", at_replacement)
        rewritten = rewritten.replace(source_name, identifier)
    return rewritten


def _opencode_filename_for(agent: SourceAgent, existing_stems: set[str]) -> str:
    alias = OPENCODE_FILE_ALIASES.get(agent.source_slug)
    stripped = _strip_numeric_prefix(agent.source_slug)
    candidates = [
        agent.source_slug,
        alias or "",
        stripped,
    ]
    existing = _choose_existing_stem([c for c in candidates if c], existing_stems)
    if existing:
        return f"{existing}.md"

    base = alias or agent.source_slug
    return f"{base}.md"


def _opencode_identifier_for(agent: SourceAgent, existing_stems: set[str]) -> str:
    return Path(_opencode_filename_for(agent, existing_stems)).stem


def _codex_identifier_for(agent: SourceAgent) -> str:
    identifier = _sanitize_slug(_strip_numeric_prefix(agent.source_slug))
    if not agent.user_invocable and not identifier.startswith("z-"):
        identifier = f"z-{identifier}"
    return identifier


def _codex_filename_for(agent: SourceAgent) -> str:
    if agent.user_invocable:
        return f"{agent.source_slug}.toml"

    stripped = _strip_numeric_prefix(agent.source_slug)
    return f"z-{stripped}.toml"


def _build_instruction_appendix(agent: SourceAgent, docs: List[InstructionDoc]) -> str:
    if not docs:
        return ""

    sections: List[str] = ["## Auto-Loaded Instructions", ""]
    for doc in docs:
        title = doc.path.stem.replace(".instructions", "").replace("-", " ").title()
        sections.append(f"### {title}")
        sections.append("")
        sections.append(doc.body.strip())
        sections.append("")

    return "\n".join(sections).strip() + "\n"


def _insert_clause_after_intro(body: str, clause: str) -> str:
    """Insert a clause just after the agent's intro heading/persona line."""
    if clause in body:
        return body

    paragraphs = body.split("\n\n")
    insert_after = 0

    while insert_after < len(paragraphs) and paragraphs[insert_after].lstrip().startswith("#"):
        insert_after += 1

    if insert_after < len(paragraphs):
        next_index = insert_after + 1
        next_paragraph = paragraphs[next_index].lstrip() if next_index < len(paragraphs) else ""
        if paragraphs[insert_after].lstrip().startswith("You are") and next_paragraph.startswith("Your "):
            insert_after = next_index

    paragraphs.insert(insert_after + 1, clause)
    return "\n\n".join(paragraphs)


def _inject_claude_selected_agent_instruction(agent: SourceAgent, body: str, identifier: str) -> str:
    if not agent.user_invocable:
        return body

    clause = (
        f"When the user addresses you by name or role, "
        "begin work in this role immediately. "
        f"Do not spend your first action invoking `{identifier}` as a subagent. "
        "Delegate only to distinct child agents when the workflow explicitly calls for them."
    )
    return _insert_clause_after_intro(body, clause)


def _inject_claude_command_instruction(agent: SourceAgent, identifier: str, body: str) -> str:
    """Adoption clause for slash-command output: the main persona becomes this role inline."""
    clause = (
        f"You are now operating as **{agent.name}** directly in this conversation. "
        "Adopt this role and carry out the work yourself in the current session — "
        f"do not spawn `{identifier}` (or any copy of this role) as a subagent to do it. "
        "Delegate only to distinct child agents when this workflow explicitly calls for them."
    )
    return _insert_clause_after_intro(body, clause)


def render_claude_agent(
    agent: SourceAgent,
    docs: List[InstructionDoc],
    reference_map: Dict[str, str],
    identifier: str,
) -> str:
    tools = ", ".join(map_tools_for_claude(agent.tools))
    appendix = _build_instruction_appendix(agent, docs)
    body = _rewrite_agent_references(agent.body.strip(), reference_map, preserve_at_sign=True)
    body = _inject_claude_selected_agent_instruction(agent, body, identifier)

    parts = [
        "---",
        f"name: {identifier}",
        f"description: {agent.description}",
        f"tools: {tools}",
        "user-invocable: false",
        "---",
        "",
        body,
    ]

    if appendix:
        parts.extend(["", "---", "", _rewrite_agent_references(appendix.strip(), reference_map, preserve_at_sign=True)])

    return _with_generated_marker("\n".join(parts).rstrip() + "\n", GENERATED_AGENT_MARKDOWN_HEADER)


def render_claude_command(
    agent: SourceAgent,
    docs: List[InstructionDoc],
    reference_map: Dict[str, str],
    identifier: str,
) -> str:
    """Render a Claude slash command so the main persona adopts this role inline.

    Child-agent references still resolve to subagent identifiers, so an orchestrator
    command can `Task`-spawn its workers from within the main conversation.
    """
    appendix = _build_instruction_appendix(agent, docs)
    body = _rewrite_agent_references(agent.body.strip(), reference_map, preserve_at_sign=True)
    body = _inject_claude_command_instruction(agent, identifier, body)

    parts = [
        "---",
        f"description: {agent.description}",
        "---",
        "",
        body,
    ]

    if appendix:
        parts.extend(["", "---", "", _rewrite_agent_references(appendix.strip(), reference_map, preserve_at_sign=True)])

    return _with_generated_marker("\n".join(parts).rstrip() + "\n", GENERATED_AGENT_MARKDOWN_HEADER)


def _referenced_agent_names(agents: List[SourceAgent]) -> set[str]:
    """Source agent names that appear as a child in any agent's `agents:` list.

    Used to decide which user-invocable agents must ALSO keep a spawnable subagent
    file (dual-use), derived from the source of truth rather than a hard-coded list.
    """
    referenced: set[str] = set()
    for agent in agents:
        for child in agent.subagents:
            referenced.add(child)
    return referenced


def render_opencode_agent(agent: SourceAgent, docs: List[InstructionDoc], reference_map: Dict[str, str]) -> str:
    permissions = map_permissions_for_opencode(agent.tools)
    appendix = _build_instruction_appendix(agent, docs)
    body = _rewrite_agent_references(agent.body.strip(), reference_map, preserve_at_sign=True)

    lines: List[str] = [
        "---",
        f"description: \"{agent.description}\"",
        "model: deepseek/deepseek-v4-pro",
    ]

    if not agent.user_invocable:
        lines.append("mode: subagent")
        lines.append("hidden: true")

    if permissions:
        lines.append("permission:")
        for key in sorted(permissions.keys()):
            lines.append(f"  {key}: allow")
    lines.extend(["---", "", body])

    if appendix:
        lines.extend(["", "---", "", _rewrite_agent_references(appendix.strip(), reference_map, preserve_at_sign=True)])

    return _with_generated_marker("\n".join(lines).rstrip() + "\n", GENERATED_AGENT_MARKDOWN_HEADER)


def _render_toml_string(value: str) -> List[str]:
    if "'''" not in value:
        return ["'''", value, "'''"]

    return [json.dumps(value, ensure_ascii=False)]


def _inject_codex_selected_agent_instruction(agent: SourceAgent, body: str) -> str:
    if not agent.user_invocable:
        return body

    identifier = _codex_identifier_for(agent)
    clause = (
        f"You are the `{identifier}` agent. When the user addresses you by name or role, "
        "begin work in this role immediately. "
        f"Do not spend your first action invoking `{identifier}` again as a subagent. "
        "Delegate only to distinct child agents when the workflow explicitly calls for them."
    )
    if clause in body:
        return body

    paragraphs = body.split("\n\n")
    insert_after = 0

    while insert_after < len(paragraphs) and paragraphs[insert_after].lstrip().startswith("#"):
        insert_after += 1

    if insert_after < len(paragraphs):
        next_index = insert_after + 1
        next_paragraph = paragraphs[next_index].lstrip() if next_index < len(paragraphs) else ""
        if paragraphs[insert_after].lstrip().startswith("You are") and next_paragraph.startswith("Your "):
            insert_after = next_index

    paragraphs.insert(insert_after + 1, clause)
    return "\n\n".join(paragraphs)


def _rewrite_codex_invocation_language(body: str) -> str:
    """Rewrite GitHub Copilot 'spawn **AgentName**' syntax to Codex natural language.

    Codex uses natural language spawning ("Spawn a X subagent") rather than
    imperative tool-call-style invocation ("spawn **X**"). The latter causes
    the model to report the named agent invocation as missing tooling.
    """
    # "spawn **X**" / "spawn the **X**" / "spawn one **X**" → "Spawn a **X** subagent"
    body = re.sub(
        r"\bspawn\b\s+(?:the\s+|one\s+)?(\*\*[^*]+\*\*)(\s+subagent)?",
        lambda m: f"Spawn a {m.group(1)} subagent",
        body,
    )
    # "spawn **X**" / "spawn the **X**" / "spawn one **X**" → "spawn a **X** subagent"
    body = re.sub(
        r"\bspawn\b\s+(?:the\s+|one\s+)?(\*\*[^*]+\*\*)(\s+subagent)?",
        lambda m: f"spawn a {m.group(1)} subagent",
        body,
    )
    return body


def _inject_codex_todo_override(agent: SourceAgent, body: str) -> str:
    """Append a Codex compatibility note when the source agent uses the todo tool.

    Codex has no native todo tool. Without this note the model will attempt to
    call a non-existent tool and report it as missing tooling.
    """
    if "todo" not in agent.tools:
        return body

    note = (
        "\n\n## Codex Compatibility Notes\n\n"
        "**No todo tool**: Codex has no native todo tool. Disregard any instructions "
        "that reference creating or updating todo list entries. Track task progress "
        "inline in your response or, for multi-step pipelines, in a state file at "
        "`dev/pipeline-state.md`."
    )
    return body + note


def render_codex_agent(agent: SourceAgent, docs: List[InstructionDoc], reference_map: Dict[str, str]) -> str:
    combined = agent.body.strip()
    appendix = _build_instruction_appendix(agent, docs)
    if appendix:
        combined = f"{combined}\n\n{appendix.strip()}"

    combined = _rewrite_agent_references(combined, reference_map, preserve_at_sign=False)
    combined = _rewrite_codex_invocation_language(combined)
    combined = _inject_codex_selected_agent_instruction(agent, combined)
    combined = _inject_codex_todo_override(agent, combined)

    name_value = _codex_identifier_for(agent)
    description = json.dumps(agent.description, ensure_ascii=False)

    lines = [
        GENERATED_AGENT_HEADER,
        f'name = "{name_value}"',
        f"description = {description}",
        "developer_instructions = ",
    ]
    lines[-1] += _render_toml_string(combined)[0]
    lines.extend(_render_toml_string(combined)[1:])
    return "\n".join(lines).rstrip() + "\n"


def _inject_codex_profile_instruction(agent: SourceAgent, body: str) -> str:
    """Adoption clause for profile output: the session adopts this role inline."""
    identifier = _codex_identifier_for(agent)
    clause = (
        f"You are now operating as **{agent.name}** directly in this session. "
        "Adopt this role and carry out the work yourself — "
        f"do not spawn `{identifier}` as a subagent to handle this. "
        "Delegate only to distinct child agents when this workflow explicitly calls for them."
    )
    return _insert_clause_after_intro(body, clause)


def render_codex_profile(agent: SourceAgent, docs: List[InstructionDoc], reference_map: Dict[str, str]) -> str:
    """Render a Codex profile TOML for direct invocation with `codex --profile <name>`.

    Profile TOMLs set developer_instructions as a config-layer key so the session
    adopts the agent role from the first turn. Use alongside the custom agent TOML
    (which handles subagent spawning) — both files are generated for user-invocable agents.
    """
    combined = agent.body.strip()
    appendix = _build_instruction_appendix(agent, docs)
    if appendix:
        combined = f"{combined}\n\n{appendix.strip()}"

    combined = _rewrite_agent_references(combined, reference_map, preserve_at_sign=False)
    combined = _rewrite_codex_invocation_language(combined)
    combined = _inject_codex_profile_instruction(agent, combined)
    combined = _inject_codex_todo_override(agent, combined)

    lines = [
        GENERATED_AGENT_HEADER,
        "developer_instructions = ",
    ]
    lines[-1] += _render_toml_string(combined)[0]
    lines.extend(_render_toml_string(combined)[1:])
    return "\n".join(lines).rstrip() + "\n"


def _to_pascal_case(name: str) -> str:
    """Convert a dash/underscore-separated name to PascalCase for JS identifiers."""
    return "".join(word.title() for word in name.replace("-", "_").split("_"))


def _resolve_hook_events(vscode_event: str, meta: Dict, tool: str) -> List[str]:
    """Return target events for a tool, using $meta overrides when present."""
    event_meta = meta.get(vscode_event, {})
    if tool in event_meta:
        return event_meta[tool]
    return HOOK_EVENT_MAP.get(vscode_event, {}).get(tool, [])


def _resolve_hook_command(entry: Dict, meta: Dict, tool: str) -> str:
    """Return the command for a tool, with $meta.commands override support."""
    commands_override = meta.get("commands", {})
    if tool in commands_override:
        return commands_override[tool]
    return entry.get("osx") or entry.get("command", "")


HOOK_PROJECT_ROOT_TOKENS = {
    "claude": "$CLAUDE_PROJECT_DIR",
    "codex": "$(git rev-parse --show-toplevel)",
}


def _project_root_hook_command(command: str, tool: str) -> str:
    """Anchor a project-relative hook command to the repository root.

    Claude Code and Codex both run hook commands with the *session* working
    directory, so a bare relative script path stops resolving as soon as the
    agent works from a subdirectory — and a guard that fails to launch fails
    closed, blocking every subsequent tool call. Both accept shell-form
    commands, so the root token expands at invocation time. OpenCode has no
    equivalent token; its plugins pin cwd at the call site instead.
    """
    root_token = HOOK_PROJECT_ROOT_TOKENS.get(tool)
    if root_token is None:
        return command
    rendered = [
        f'"{root_token}/{part}"' if part.startswith(".github/hooks/") else part
        for part in shlex.split(command)
    ]
    return " ".join(rendered)


def _strip_propagated_hooks(settings: Dict) -> None:
    """Remove all hook entries tagged with HOOK_SOURCE_KEY from settings in-place."""
    for event_key in list(settings.get("hooks", {}).keys()):
        settings["hooks"][event_key] = [
            e for e in settings["hooks"][event_key]
            if HOOK_SOURCE_KEY not in e
        ]
        if not settings["hooks"][event_key]:
            del settings["hooks"][event_key]


def _render_opencode_plugin(name: str, event_commands: List[Tuple[str, str]]) -> str:
    """Render an OpenCode JS plugin file from (event, command) pairs."""
    if name == "injection-scanner" and len(event_commands) == 1:
        event, command = event_commands[0]
        if event == "tool.execute.after":
            command_parts = json.dumps(shlex.split(command))
            return (
                GENERATED_OPENCODE_PLUGIN_HEADER
                + "export const InjectionScanner = async ({ directory }) => {\n"
                + "  return {\n"
                + '    "tool.execute.after": async (input, output) => {\n'
                + "      const toolAliases = {\n"
                + '        shell: "Bash", bash: "Bash", read: "Read", grep: "Grep",\n'
                + '        fetch: "WebFetch", webfetch: "WebFetch",\n'
                + '        search: "WebSearch", websearch: "WebSearch", task: "Task",\n'
                + '        patch: "apply_patch"\n'
                + "      }\n"
                + "      const toolName = toolAliases[input.tool] ?? input.tool\n"
                + "      const toolInput = input.args && typeof input.args === \"object\" && !Array.isArray(input.args)\n"
                + "        ? { ...input.args } : {}\n"
                + "      if (toolName === \"Read\" && typeof toolInput.filePath === \"string\" && toolInput.file_path === undefined) {\n"
                + "        toolInput.file_path = toolInput.filePath\n"
                + "      }\n"
                + "      const payload = {\n"
                + '        hook_event_name: "PostToolUse",\n'
                + "        tool_name: toolName,\n"
                + "        tool_input: toolInput,\n"
                + "        tool_output: output.output,\n"
                + "        tool_output_truncated: false,\n"
                + "        session_id: input.sessionID\n"
                + "      }\n"
                + f"      const proc = Bun.spawnSync({command_parts}, {{\n"
                + "        cwd: directory,\n"
                + "        stdin: new TextEncoder().encode(JSON.stringify(payload)),\n"
                + "        stdout: \"pipe\", stderr: \"pipe\"\n"
                + "      })\n"
                + "      const stdout = new TextDecoder().decode(proc.stdout)\n"
                + "      let result\n"
                + "      try { result = JSON.parse(stdout) } catch { result = null }\n"
                + "      const context = result?.hookSpecificOutput?.additionalContext\n"
                + "      const isBlock = result?.decision === \"block\" && typeof result.reason === \"string\"\n"
                + "      const isWarn = result?.decision === undefined && typeof context === \"string\" && context.length > 0\n"
                + "      const isAllow = result && Object.keys(result).length === 0\n"
                + "      if (proc.exitCode !== 0 || (!isBlock && !isWarn && !isAllow)) {\n"
                + '        output.output = "Injection scanner blocked tool output. guard error"\n'
                + "      } else if (isBlock) {\n"
                + "        output.output = result.reason\n"
                + "      } else if (isWarn) {\n"
                + "        output.output += `\\n\\n${context}`\n"
                + "      }\n"
                + "    }\n"
                + "  }\n"
                + "}\n"
            )
    fn_name = _to_pascal_case(name)
    handler_lines: List[str] = []
    for i, (event, command) in enumerate(event_commands):
        escaped = command.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        comma = "," if i < len(event_commands) - 1 else ""
        handler_lines.append(f'    "{event}": async (_input, _output) => {{')
        handler_lines.append(f"      await $`{escaped}`.cwd(directory)")
        handler_lines.append(f"    }}{comma}")
    handlers = "\n".join(handler_lines)
    return (
        GENERATED_OPENCODE_PLUGIN_HEADER
        + f"export const {fn_name} = async ({{ $, directory }}) => {{\n"
        + f"  return {{\n"
        + f"{handlers}\n"
        + f"  }}\n"
        + f"}}\n"
    )


def _update_nested_settings_file(
    settings_file: Path,
    source_hooks: List[Dict],
    tool: str,
    command_transform: Callable[[str], str] | None = None,
) -> bool:
    """Rebuild Claude/Codex-style nested settings, preserving untagged entries."""
    if settings_file.exists():
        settings: Dict = json.loads(settings_file.read_text(encoding="utf-8"))
    else:
        settings = {}
    settings.setdefault("hooks", {})
    _strip_propagated_hooks(settings)
    for source in source_hooks:
        for vscode_event, entries in source["hooks_by_event"].items():
            target_events = _resolve_hook_events(vscode_event, source["meta"], tool)
            for target_event in target_events:
                settings["hooks"].setdefault(target_event, [])
                for entry in entries:
                    command = _resolve_hook_command(entry, source["meta"], tool)
                    if command_transform is not None:
                        command = command_transform(command)
                    else:
                        command = _project_root_hook_command(command, tool)
                    timeout = entry.get("timeout")
                    inner: Dict = {"type": "command", "command": command}
                    if timeout is not None:
                        inner["timeout"] = timeout
                    settings["hooks"][target_event].append({
                        "matcher": entry.get("matcher", ""),
                        HOOK_SOURCE_KEY: source["name"],
                        "hooks": [inner],
                    })
    return _write_if_changed(settings_file, json.dumps(settings, indent=2) + "\n")


def _hook_asset_files(hooks_dir: Path) -> List[Path]:
    hooks_root = hooks_dir.resolve()
    assets: List[Path] = []
    for path in sorted(hooks_dir.rglob("*")):
        if (
            not path.is_file()
            or path.name == ".distribution-version"
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        try:
            path.resolve().relative_to(hooks_root)
        except ValueError as exc:
            raise ValueError(
                f"hook source asset resolves outside .github/hooks: {path}"
            ) from exc
        assets.append(path)
    return assets


def _hook_distribution_version(hooks_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in _hook_asset_files(hooks_dir):
        digest.update(path.relative_to(hooks_dir).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"phase-01-sha256:{digest.hexdigest()}\n"


def _copy_hook_assets(source_dir: Path, target_dir: Path) -> int:
    changed = 0
    same_tree = source_dir.resolve() == target_dir.resolve()
    for source_path in _hook_asset_files(source_dir):
        target_path = target_dir / source_path.relative_to(source_dir)
        if same_tree:
            continue
        content = source_path.read_bytes()
        _validate_nested_output_directory(target_dir, target_path.parent)
        if target_path.is_symlink():
            target_path.unlink()
        if target_path.exists() and target_path.read_bytes() == content:
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(content)
        changed += 1
    return changed


def _remove_retired_hook_assets(source_dir: Path, target_dir: Path) -> int:
    removed = 0
    for relative_path in RETIRED_HOOK_ASSETS:
        if (source_dir / relative_path).exists():
            continue
        target_path = target_dir / relative_path
        _validate_nested_output_directory(target_dir, target_path.parent)
        if target_path.is_file() or target_path.is_symlink():
            target_path.unlink()
            removed += 1
    return removed


def _validate_hook_commands(source_hooks: List[Dict], source_root: Path) -> None:
    hooks_root = (source_root / ".github" / "hooks").resolve()
    for source in source_hooks:
        for entries in source["hooks_by_event"].values():
            for entry in entries:
                for tool in ("claude", "codex", "opencode"):
                    command = _resolve_hook_command(entry, source["meta"], tool)
                    try:
                        command_parts = shlex.split(command)
                    except ValueError as exc:
                        raise ValueError(
                            f"invalid generated hook command for {source['name']}: {exc}"
                        ) from exc
                    candidate_parts = list(command_parts)
                    for part in command_parts:
                        if any(character.isspace() for character in part):
                            candidate_parts.extend(shlex.split(part))
                    for part in candidate_parts:
                        normalized = part.removeprefix("./")
                        if not normalized.startswith(".github/hooks/"):
                            continue
                        candidate = (source_root / normalized).resolve()
                        try:
                            candidate.relative_to(hooks_root)
                        except ValueError as exc:
                            raise ValueError(
                                "generated hook command escapes .github/hooks: "
                                f"{part}"
                            ) from exc
                        if not candidate.is_file():
                            raise FileNotFoundError(
                                "generated hook command references missing asset: "
                                f"{part}"
                            )


def _validate_output_directory(repo_root: Path, directory: Path) -> None:
    """Reject generated-output directories that resolve outside the target root."""
    resolved_root = repo_root.resolve()
    resolved_directory = directory.resolve()
    try:
        resolved_directory.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(
            f"generated output directory resolves outside target root: {directory}"
        ) from exc
    if directory.is_symlink():
        raise ValueError(f"generated output directory must not be a symlink: {directory}")


def _validate_nested_output_directory(root: Path, directory: Path) -> None:
    """Reject symlinked or escaping intermediate directories under an output root."""

    relative = directory.relative_to(root)
    resolved_root = root.resolve()
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(
                f"generated output directory must not be a symlink: {current}"
            )
        if current.exists():
            try:
                current.resolve().relative_to(resolved_root)
            except ValueError as exc:
                raise ValueError(
                    f"generated output directory resolves outside target root: {current}"
                ) from exc


def propagate_hooks_once(
    verbose: bool = False,
    repo_root: Path | None = None,
    source_root: Path | None = None,
    *,
    copy_assets: bool = True,
    command_transform: Callable[[str], str] | None = None,
) -> Dict[str, int]:
    """Propagate source hooks and their runtime assets into one repository root."""
    repo_root = repo_root or REPO_ROOT
    source_root = source_root or REPO_ROOT
    github_hooks_dir = source_root / ".github" / "hooks"
    target_hooks_dir = repo_root / ".github" / "hooks"
    claude_settings_file = repo_root / ".claude" / "settings.json"
    codex_hooks_file = repo_root / ".codex" / "hooks.json"
    opencode_plugins_dir = repo_root / ".opencode" / "plugins"
    for output_directory in (
        target_hooks_dir,
        claude_settings_file.parent,
        codex_hooks_file.parent,
        opencode_plugins_dir,
    ):
        _validate_output_directory(repo_root, output_directory)
        _validate_nested_output_directory(repo_root, output_directory)
    if not github_hooks_dir.exists():
        return {
            "hooks_source": 0,
            "assets_changed": 0,
            "retired_assets_removed": 0,
            "version_changed": 0,
            "claude_changed": 0,
            "codex_changed": 0,
            "opencode_changed": 0,
        }

    assets_changed = (
        _copy_hook_assets(github_hooks_dir, target_hooks_dir) if copy_assets else 0
    )
    retired_assets_removed = (
        _remove_retired_hook_assets(github_hooks_dir, target_hooks_dir)
        if copy_assets
        else 0
    )
    version_path = (
        target_hooks_dir / ".distribution-version"
        if copy_assets
        else repo_root / ".hook-distribution-version"
    )
    version_changed = _write_if_changed(
        version_path, _hook_distribution_version(github_hooks_dir)
    )

    source_hooks: List[Dict] = []
    for hook_file in sorted(github_hooks_dir.glob("*.json")):
        try:
            data = json.loads(hook_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        source_hooks.append({
            "name": hook_file.stem,
            "hooks_by_event": data.get("hooks", {}),
            "meta": data.get("$meta", {}),
        })
    _validate_hook_commands(source_hooks, source_root)

    claude_changed = _update_nested_settings_file(
        claude_settings_file, source_hooks, "claude", command_transform
    )
    codex_changed = _update_nested_settings_file(
        codex_hooks_file, source_hooks, "codex", command_transform
    )

    opencode_plugins_dir.mkdir(parents=True, exist_ok=True)
    opencode_changed = 0
    expected_plugins: set[Path] = set()

    for source in source_hooks:
        event_commands: List[Tuple[str, str]] = []
        for vscode_event, entries in source["hooks_by_event"].items():
            target_events = _resolve_hook_events(vscode_event, source["meta"], "opencode")
            for target_event in target_events:
                for entry in entries:
                    command = _resolve_hook_command(entry, source["meta"], "opencode")
                    if command_transform is not None:
                        command = command_transform(command)
                    event_commands.append((target_event, command))
        if not event_commands:
            continue
        plugin_file = opencode_plugins_dir / f"{source['name']}.js"
        expected_plugins.add(plugin_file)
        if _write_if_changed(plugin_file, _render_opencode_plugin(source["name"], event_commands)):
            opencode_changed += 1

    if opencode_plugins_dir.exists():
        for plugin_file in opencode_plugins_dir.glob("*.js"):
            if plugin_file in expected_plugins:
                continue
            content = plugin_file.read_text(encoding="utf-8")
            if content.startswith(GENERATED_OPENCODE_PLUGIN_HEADER):
                plugin_file.unlink()
                opencode_changed += 1

    if verbose:
        print(json.dumps({
            "hooks_source": len(source_hooks),
            "assets_changed": assets_changed,
            "retired_assets_removed": retired_assets_removed,
            "version_changed": int(version_changed),
            "claude_changed": int(claude_changed),
            "codex_changed": int(codex_changed),
            "opencode_changed": opencode_changed,
        }, indent=2))

    return {
        "hooks_source": len(source_hooks),
        "assets_changed": assets_changed,
        "retired_assets_removed": retired_assets_removed,
        "version_changed": int(version_changed),
        "claude_changed": int(claude_changed),
        "codex_changed": int(codex_changed),
        "opencode_changed": opencode_changed,
    }


def _absolute_hook_command(command: str, source_root: Path) -> str:
    parts = shlex.split(command)
    replaced = [
        str(source_root / part) if part.startswith(".github/hooks/") else part
        for part in parts
    ]
    return shlex.join(replaced)


def generate_global_hooks(
    output_root: Path, source_root: Path | None = None, verbose: bool = False
) -> Dict[str, int]:
    """Generate local-only user-scope hook wiring with absolute source paths."""
    source_root = (source_root or REPO_ROOT).resolve()
    return propagate_hooks_once(
        verbose=verbose,
        repo_root=output_root,
        source_root=source_root,
        copy_assets=False,
        command_transform=lambda command: _absolute_hook_command(command, source_root),
    )


def propagate_skills_once(repo_root: Path | None = None) -> Dict[str, int]:
    repo_root = repo_root or REPO_ROOT
    github_skills_dir = repo_root / ".github" / "skills"
    claude_skills_dir = repo_root / "claude" / "skills"
    opencode_skills_dir = repo_root / "opencode" / "skills"
    codex_skills_dir = repo_root / "codex" / "skills"

    if not github_skills_dir.exists():
        return {
            "claude_changed": 0,
            "opencode_changed": 0,
            "codex_changed": 0,
            "skills_changed": 0,
            "skill_orphans_removed": 0,
        }

    claude_skills_dir.mkdir(parents=True, exist_ok=True)
    opencode_skills_dir.mkdir(parents=True, exist_ok=True)
    codex_skills_dir.mkdir(parents=True, exist_ok=True)

    changed_claude = 0
    changed_opencode = 0
    changed_codex = 0
    expected_claude_dirs: set[Path] = set()
    expected_opencode_dirs: set[Path] = set()
    expected_codex_dirs: set[Path] = set()

    for source_skill_dir in sorted(github_skills_dir.iterdir()):
        if not source_skill_dir.is_dir():
            continue

        skill_name = source_skill_dir.name
        source_skill_md = source_skill_dir / "SKILL.md"

        dest_claude_dir = claude_skills_dir / skill_name
        expected_claude_dirs.add(dest_claude_dir)
        dest_claude_dir.mkdir(parents=True, exist_ok=True)
        if source_skill_md.exists():
            dest_content = _with_generated_marker(_read_text(source_skill_md), GENERATED_SKILL_HEADER)
            if _write_if_changed(dest_claude_dir / "SKILL.md", dest_content):
                changed_claude += 1
        for source_file in sorted(source_skill_dir.rglob("*")):
            if not source_file.is_file() or source_file.name == "SKILL.md":
                continue
            rel = source_file.relative_to(source_skill_dir)
            dest_file = dest_claude_dir / rel
            if _write_if_changed(dest_file, _read_text(source_file)):
                changed_claude += 1

        dest_opencode_dir = opencode_skills_dir / skill_name
        expected_opencode_dirs.add(dest_opencode_dir)
        dest_opencode_dir.mkdir(parents=True, exist_ok=True)
        if source_skill_md.exists():
            dest_content = _with_generated_marker(_read_text(source_skill_md), GENERATED_SKILL_HEADER)
            if _write_if_changed(dest_opencode_dir / "SKILL.md", dest_content):
                changed_opencode += 1
        for source_file in sorted(source_skill_dir.rglob("*")):
            if not source_file.is_file() or source_file.name == "SKILL.md":
                continue
            rel = source_file.relative_to(source_skill_dir)
            dest_file = dest_opencode_dir / rel
            if _write_if_changed(dest_file, _read_text(source_file)):
                changed_opencode += 1

        dest_codex_dir = codex_skills_dir / skill_name
        expected_codex_dirs.add(dest_codex_dir)
        dest_codex_dir.mkdir(parents=True, exist_ok=True)
        if source_skill_md.exists():
            fm, body = _parse_frontmatter(_read_text(source_skill_md))
            name = str(fm.get("name", skill_name)).strip().strip('"').strip("'")
            description = str(fm.get("description", "")).strip().strip('"').strip("'")
            desc_yaml = json.dumps(description, ensure_ascii=False)
            dest_content = (
                f"---\nname: {name}\ndescription: {desc_yaml}\n---\n"
                + GENERATED_SKILL_HEADER
                + body.lstrip("\n")
            )
            if _write_if_changed(dest_codex_dir / "SKILL.md", dest_content):
                changed_codex += 1
        for source_file in sorted(source_skill_dir.rglob("*")):
            if not source_file.is_file() or source_file.name == "SKILL.md":
                continue
            rel = source_file.relative_to(source_skill_dir)
            dest_file = dest_codex_dir / rel
            if _write_if_changed(dest_file, _read_text(source_file)):
                changed_codex += 1

    # Pruning runs only after every skill has been emitted.
    orphans_removed = (
        _prune_orphaned_skill_dirs(claude_skills_dir, expected_claude_dirs, GENERATED_SKILL_HEADER)
        + _prune_orphaned_skill_dirs(opencode_skills_dir, expected_opencode_dirs, GENERATED_SKILL_HEADER)
        + _prune_orphaned_skill_dirs(codex_skills_dir, expected_codex_dirs, GENERATED_SKILL_HEADER)
    )

    return {
        "claude_changed": changed_claude,
        "opencode_changed": changed_opencode,
        "codex_changed": changed_codex,
        "skills_changed": changed_claude + changed_opencode + changed_codex,
        "skill_orphans_removed": orphans_removed,
    }


def propagate_learnings_once(repo_root: Path | None = None) -> Dict[str, int]:
    repo_root = repo_root or REPO_ROOT
    github_learnings_dir = repo_root / ".github" / "learnings"
    claude_learnings_dir = repo_root / "claude" / "learnings"

    if not github_learnings_dir.exists():
        return {"claude_changed": 0, "learnings_changed": 0}

    claude_learnings_dir.mkdir(parents=True, exist_ok=True)

    changed_claude = 0
    for source_file in sorted(github_learnings_dir.glob("*.md")):
        if _write_if_changed(claude_learnings_dir / source_file.name, _read_text(source_file)):
            changed_claude += 1

    return {"claude_changed": changed_claude, "learnings_changed": changed_claude}


def propagate_once(verbose: bool = True, repo_root: Path | None = None) -> Dict[str, int]:
    repo_root = repo_root or REPO_ROOT
    claude_agents_dir = repo_root / "claude" / "agents"
    claude_commands_dir = repo_root / "claude" / "commands"
    opencode_agents_dir = repo_root / "opencode" / "agents"
    codex_agents_dir = repo_root / "codex" / "agents"
    codex_profiles_dir = repo_root / "codex" / "profiles"

    agents = load_source_agents(repo_root)
    instructions = load_instruction_docs(repo_root)

    claude_agents_dir.mkdir(parents=True, exist_ok=True)
    claude_commands_dir.mkdir(parents=True, exist_ok=True)
    opencode_agents_dir.mkdir(parents=True, exist_ok=True)
    codex_agents_dir.mkdir(parents=True, exist_ok=True)
    codex_profiles_dir.mkdir(parents=True, exist_ok=True)

    referenced_names = _referenced_agent_names(agents)
    claude_existing_stems = _discover_existing_stems(claude_agents_dir)
    opencode_existing_stems = _discover_existing_stems(opencode_agents_dir)
    claude_reference_map = _build_agent_reference_map(
        agents,
        lambda agent: _claude_identifier_for(agent, claude_existing_stems),
    )
    opencode_reference_map = _build_agent_reference_map(
        agents,
        lambda agent: _opencode_identifier_for(agent, opencode_existing_stems),
    )
    codex_reference_map = _build_agent_reference_map(agents, _codex_identifier_for)

    changed_claude = 0
    changed_opencode = 0
    changed_codex = 0
    changed_codex_profiles = 0
    expected_claude_files: set[Path] = set()
    expected_claude_command_files: set[Path] = set()
    expected_opencode_files: set[Path] = set()
    expected_codex_files: set[Path] = set()
    expected_codex_profile_files: set[Path] = set()

    for agent in agents:
        docs = applicable_instructions(agent, instructions)

        claude_identifier = _claude_identifier_for(agent, claude_existing_stems)
        claude_file = claude_agents_dir / f"{claude_identifier}.md"
        opencode_file = opencode_agents_dir / _opencode_filename_for(agent, opencode_existing_stems)
        codex_file = codex_agents_dir / _codex_filename_for(agent)
        expected_opencode_files.add(opencode_file)
        expected_codex_files.add(codex_file)

        # Claude emission rule (Claude target only):
        #   user-invocable: false        -> subagent file only
        #   user-invocable: true         -> slash command
        #     + subagent file IFF spawned as a child by some orchestrator (dual-use),
        #       so orchestrator commands can still `Task`-spawn it.
        is_dual_use = agent.user_invocable and agent.name in referenced_names
        emit_claude_agent = (not agent.user_invocable) or is_dual_use

        if emit_claude_agent:
            expected_claude_files.add(claude_file)
            if _write_if_changed(
                claude_file,
                render_claude_agent(agent, docs, claude_reference_map, claude_identifier),
            ):
                changed_claude += 1
        elif claude_file.exists():
            # Reclassified to command-only: remove the now-stale generated subagent file.
            claude_file.unlink()
            changed_claude += 1

        if agent.user_invocable:
            command_file = claude_commands_dir / f"{claude_identifier}.md"
            expected_claude_command_files.add(command_file)
            if _write_if_changed(
                command_file,
                render_claude_command(agent, docs, claude_reference_map, claude_identifier),
            ):
                changed_claude += 1

        if _write_if_changed(opencode_file, render_opencode_agent(agent, docs, opencode_reference_map)):
            changed_opencode += 1
        if _write_if_changed(codex_file, render_codex_agent(agent, docs, codex_reference_map)):
            changed_codex += 1

        if agent.user_invocable:
            codex_profile_file = codex_profiles_dir / f"{_codex_identifier_for(agent)}.config.toml"
            expected_codex_profile_files.add(codex_profile_file)
            if _write_if_changed(codex_profile_file, render_codex_profile(agent, docs, codex_reference_map)):
                changed_codex_profiles += 1

    # Every prune runs only after all emission above has completed. `_claude_filename_for`
    # and `_opencode_filename_for` resolve an output name against the stems already on
    # disk, so deleting first could hand a survivor a different filename (AC6).
    claude_orphans = _prune_orphaned_outputs(
        claude_agents_dir, "*.md", expected_claude_files, GENERATED_AGENT_MARKDOWN_HEADER
    )
    claude_command_orphans = _prune_orphaned_outputs(
        claude_commands_dir, "*.md", expected_claude_command_files, GENERATED_AGENT_MARKDOWN_HEADER
    )
    opencode_orphans = _prune_orphaned_outputs(
        opencode_agents_dir, "*.md", expected_opencode_files, GENERATED_AGENT_MARKDOWN_HEADER
    )
    codex_orphans = _prune_orphaned_outputs(
        codex_agents_dir, "*.toml", expected_codex_files, GENERATED_AGENT_HEADER
    )
    codex_profile_orphans = _prune_orphaned_outputs(
        codex_profiles_dir, "*.config.toml", expected_codex_profile_files, GENERATED_AGENT_HEADER
    )

    skill_result = propagate_skills_once(repo_root)
    changed_skills = skill_result["skills_changed"]

    learnings_result = propagate_learnings_once(repo_root)

    hooks_result = propagate_hooks_once(verbose=False, repo_root=repo_root, source_root=repo_root)

    result = {
        "source_agents": len(agents),
        "hooks_source": hooks_result["hooks_source"],
        "hook_assets_changed": hooks_result["assets_changed"],
        "retired_hook_assets_removed": hooks_result["retired_assets_removed"],
        "hook_version_changed": hooks_result["version_changed"],
        "claude_changed": changed_claude + hooks_result["claude_changed"] + skill_result["claude_changed"] + learnings_result["claude_changed"],
        "opencode_changed": changed_opencode + hooks_result["opencode_changed"] + skill_result["opencode_changed"],
        "codex_changed": changed_codex + hooks_result["codex_changed"] + skill_result["codex_changed"],
        "codex_profiles_changed": changed_codex_profiles,
        "skills_changed": changed_skills,
        "learnings_changed": learnings_result["learnings_changed"],
        # Deletions are reported on their own keys rather than folded into the
        # `changed_*` counters, which already conflate writes with removals. This
        # follows the `retired_hook_assets_removed` precedent above: a run that
        # removes a file says so instead of removing it silently.
        "claude_orphans_removed": claude_orphans,
        "claude_command_orphans_removed": claude_command_orphans,
        "opencode_orphans_removed": opencode_orphans,
        "codex_orphans_removed": codex_orphans,
        "codex_profile_orphans_removed": codex_profile_orphans,
        "skill_orphans_removed": skill_result["skill_orphans_removed"],
    }

    if verbose:
        print(json.dumps(result, indent=2))

    return result


def _collect_file_state(paths: Iterable[Path]) -> Dict[str, Tuple[float, int]]:
    state: Dict[str, Tuple[float, int]] = {}
    for root in paths:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            state[str(path)] = (stat.st_mtime, stat.st_size)
    return state


def _compute_changes(
    old: Dict[str, Tuple[float, int]],
    new: Dict[str, Tuple[float, int]],
) -> List[str]:
    changed: List[str] = []
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    for path in sorted(old_keys | new_keys):
        if path not in old:
            changed.append(path)
            continue
        if path not in new:
            changed.append(path)
            continue
        if old[path] != new[path]:
            changed.append(path)
    return changed


def watch_loop(interval_seconds: float = 1.0) -> None:
    print("Starting master asset watcher for .github/{agents,skills,instructions,hooks} ...")
    propagate_once(verbose=True)

    last_state = _collect_file_state(WATCH_DIRS)
    pending_since: float | None = None
    pending_changes: List[str] = []

    while True:
        time.sleep(interval_seconds)
        current_state = _collect_file_state(WATCH_DIRS)
        changes = _compute_changes(last_state, current_state)

        if changes:
            pending_changes = changes
            pending_since = time.time()
            last_state = current_state

        if pending_since is None:
            continue

        if time.time() - pending_since < 0.8:
            continue

        sample = ", ".join(Path(c).name for c in pending_changes[:5])
        more = "" if len(pending_changes) <= 5 else f" (+{len(pending_changes) - 5} more)"
        print(f"Detected change in .github source: {sample}{more}")

        try:
            propagate_once(verbose=True)
        except Exception as exc:  # pragma: no cover - runtime guard
            print(f"Propagation failed: {exc}", file=sys.stderr)

        pending_since = None
        pending_changes = []


def main() -> int:
    parser = argparse.ArgumentParser(description="Propagate .github master assets to target platforms.")
    parser.add_argument("--once", action="store_true", help="Run one propagation pass and exit.")
    parser.add_argument("--watch", action="store_true", help="Watch .github source folders and propagate on changes.")
    parser.add_argument(
        "--global-output",
        type=Path,
        help="Generate local user-scope hook wiring with absolute source paths.",
    )
    args = parser.parse_args()

    if args.global_output is not None:
        generate_global_hooks(args.global_output, verbose=True)

    if not args.once and not args.watch and args.global_output is None:
        args.once = True

    if args.once:
        propagate_once(verbose=True)

    if args.watch:
        watch_loop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
