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
import json
import re
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
]

CLAUDE_AGENTS_DIR = REPO_ROOT / "claude" / "agents"
CLAUDE_COMMANDS_DIR = REPO_ROOT / "claude" / "commands"
OPENCODE_AGENTS_DIR = REPO_ROOT / "opencode" / "agents"
CODEX_AGENTS_DIR = REPO_ROOT / "codex" / "agents"
GITHUB_SKILLS_DIR = REPO_ROOT / ".github" / "skills"
CODEX_SKILLS_DIR = REPO_ROOT / "codex" / "skills"
GITHUB_HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
CLAUDE_SETTINGS_FILE = REPO_ROOT / ".claude" / "settings.json"
CODEX_HOOKS_FILE = REPO_ROOT / ".codex" / "hooks.json"
OPENCODE_PLUGINS_DIR = REPO_ROOT / ".opencode" / "plugins"


GENERATED_AGENT_HEADER = "# Generated from .github/agents source-of-truth. Do not edit manually."
GENERATED_SKILL_HEADER = "<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->\n"
GENERATED_OPENCODE_PLUGIN_HEADER = "// Generated from .github/hooks source-of-truth. Do not edit manually.\n"
HOOK_SOURCE_KEY = "$source"

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
    "documentation-architect": "docs-writer",
    "web-research-specialist": "web-researcher",
    "audit-code-or-infra": "audit-code-infra-refactor",
}

CLAUDE_FILE_ALIASES = {
    "documentation-architect": "docs-writer",
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
    if path.exists() and _read_text(path) == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


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


def load_source_agents() -> List[SourceAgent]:
    agents: List[SourceAgent] = []
    for path in sorted(GITHUB_AGENTS_DIR.glob("*.md")):
        text = _read_text(path)
        fm, body = _parse_frontmatter(text)

        # Agent definitions always include name + description in this repo.
        if "name" not in fm or "description" not in fm:
            continue

        rel_path = path.relative_to(REPO_ROOT).as_posix()
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


def load_instruction_docs() -> List[InstructionDoc]:
    docs: List[InstructionDoc] = []
    for path in sorted(GITHUB_INSTRUCTIONS_DIR.glob("*.instructions.md")):
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

    return "\n".join(parts).rstrip() + "\n"


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

    return "\n".join(parts).rstrip() + "\n"


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

    return "\n".join(lines).rstrip() + "\n"


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
    fn_name = _to_pascal_case(name)
    handler_lines: List[str] = []
    for i, (event, command) in enumerate(event_commands):
        escaped = command.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        comma = "," if i < len(event_commands) - 1 else ""
        handler_lines.append(f'    "{event}": async (_input, _output) => {{')
        handler_lines.append(f"      await $`{escaped}`")
        handler_lines.append(f"    }}{comma}")
    handlers = "\n".join(handler_lines)
    return (
        GENERATED_OPENCODE_PLUGIN_HEADER
        + f"export const {fn_name} = async ({{ $ }}) => {{\n"
        + f"  return {{\n"
        + f"{handlers}\n"
        + f"  }}\n"
        + f"}}\n"
    )


def _update_nested_settings_file(
    settings_file: Path,
    source_hooks: List[Dict],
    tool: str,
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
                    timeout = entry.get("timeout")
                    inner: Dict = {"type": "command", "command": command}
                    if timeout is not None:
                        inner["timeout"] = timeout
                    settings["hooks"][target_event].append({
                        "matcher": "",
                        HOOK_SOURCE_KEY: source["name"],
                        "hooks": [inner],
                    })
    return _write_if_changed(settings_file, json.dumps(settings, indent=2) + "\n")


def propagate_hooks_once(verbose: bool = False) -> Dict[str, int]:
    """Propagate .github/hooks/*.json -> Claude settings, Codex hooks, OpenCode plugins."""
    if not GITHUB_HOOKS_DIR.exists():
        return {"hooks_source": 0, "claude_changed": 0, "codex_changed": 0, "opencode_changed": 0}

    source_hooks: List[Dict] = []
    for hook_file in sorted(GITHUB_HOOKS_DIR.glob("*.json")):
        try:
            data = json.loads(hook_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        source_hooks.append({
            "name": hook_file.stem,
            "hooks_by_event": data.get("hooks", {}),
            "meta": data.get("$meta", {}),
        })

    claude_changed = _update_nested_settings_file(CLAUDE_SETTINGS_FILE, source_hooks, "claude")
    codex_changed = _update_nested_settings_file(CODEX_HOOKS_FILE, source_hooks, "codex")

    OPENCODE_PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
    opencode_changed = 0
    expected_plugins: set[Path] = set()

    for source in source_hooks:
        event_commands: List[Tuple[str, str]] = []
        for vscode_event, entries in source["hooks_by_event"].items():
            target_events = _resolve_hook_events(vscode_event, source["meta"], "opencode")
            for target_event in target_events:
                for entry in entries:
                    command = _resolve_hook_command(entry, source["meta"], "opencode")
                    event_commands.append((target_event, command))
        if not event_commands:
            continue
        plugin_file = OPENCODE_PLUGINS_DIR / f"{source['name']}.js"
        expected_plugins.add(plugin_file)
        if _write_if_changed(plugin_file, _render_opencode_plugin(source["name"], event_commands)):
            opencode_changed += 1

    if OPENCODE_PLUGINS_DIR.exists():
        for plugin_file in OPENCODE_PLUGINS_DIR.glob("*.js"):
            if plugin_file in expected_plugins:
                continue
            content = plugin_file.read_text(encoding="utf-8")
            if content.startswith(GENERATED_OPENCODE_PLUGIN_HEADER):
                plugin_file.unlink()
                opencode_changed += 1

    if verbose:
        print(json.dumps({
            "hooks_source": len(source_hooks),
            "claude_changed": int(claude_changed),
            "codex_changed": int(codex_changed),
            "opencode_changed": opencode_changed,
        }, indent=2))

    return {
        "hooks_source": len(source_hooks),
        "claude_changed": int(claude_changed),
        "codex_changed": int(codex_changed),
        "opencode_changed": opencode_changed,
    }


def propagate_once(verbose: bool = True) -> Dict[str, int]:
    agents = load_source_agents()
    instructions = load_instruction_docs()

    CLAUDE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CLAUDE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    OPENCODE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CODEX_AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    referenced_names = _referenced_agent_names(agents)
    claude_existing_stems = _discover_existing_stems(CLAUDE_AGENTS_DIR)
    opencode_existing_stems = _discover_existing_stems(OPENCODE_AGENTS_DIR)
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
    expected_codex_files: set[Path] = set()

    for agent in agents:
        docs = applicable_instructions(agent, instructions)

        claude_identifier = _claude_identifier_for(agent, claude_existing_stems)
        claude_file = CLAUDE_AGENTS_DIR / f"{claude_identifier}.md"
        opencode_file = OPENCODE_AGENTS_DIR / _opencode_filename_for(agent, opencode_existing_stems)
        codex_file = CODEX_AGENTS_DIR / _codex_filename_for(agent)
        expected_codex_files.add(codex_file)

        # Claude emission rule (Claude target only):
        #   user-invocable: false        -> subagent file only
        #   user-invocable: true         -> slash command
        #     + subagent file IFF spawned as a child by some orchestrator (dual-use),
        #       so orchestrator commands can still `Task`-spawn it.
        is_dual_use = agent.user_invocable and agent.name in referenced_names
        emit_claude_agent = (not agent.user_invocable) or is_dual_use

        if emit_claude_agent:
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
            command_file = CLAUDE_COMMANDS_DIR / f"{claude_identifier}.md"
            if _write_if_changed(
                command_file,
                render_claude_command(agent, docs, claude_reference_map, claude_identifier),
            ):
                changed_claude += 1

        if _write_if_changed(opencode_file, render_opencode_agent(agent, docs, opencode_reference_map)):
            changed_opencode += 1
        if _write_if_changed(codex_file, render_codex_agent(agent, docs, codex_reference_map)):
            changed_codex += 1

    for codex_file in CODEX_AGENTS_DIR.glob("*.toml"):
        if codex_file in expected_codex_files:
            continue
        if not _read_text(codex_file).startswith(GENERATED_AGENT_HEADER):
            continue
        codex_file.unlink()
        changed_codex += 1

    # Propagate skills: .github/skills/<name>/SKILL.md -> codex/skills/<name>/SKILL.md
    CODEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    changed_skills = 0
    expected_skill_dirs: set[Path] = set()

    for source_skill_dir in sorted(GITHUB_SKILLS_DIR.iterdir()):
        if not source_skill_dir.is_dir():
            continue
        skill_name = source_skill_dir.name
        dest_skill_dir = CODEX_SKILLS_DIR / skill_name
        expected_skill_dirs.add(dest_skill_dir)

        # Transform SKILL.md: preserve YAML frontmatter required by Codex (name + description)
        # then append the generated-file comment after the closing ---.
        source_skill_md = source_skill_dir / "SKILL.md"
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
            if _write_if_changed(dest_skill_dir / "SKILL.md", dest_content):
                changed_skills += 1

        # Copy any additional files in the skill dir verbatim
        for source_file in sorted(source_skill_dir.rglob("*")):
            if not source_file.is_file():
                continue
            if source_file.name == "SKILL.md":
                continue
            rel = source_file.relative_to(source_skill_dir)
            dest_file = dest_skill_dir / rel
            if _write_if_changed(dest_file, _read_text(source_file)):
                changed_skills += 1

    # Clean up orphaned generated codex skill dirs
    if CODEX_SKILLS_DIR.exists():
        for dest_dir in sorted(CODEX_SKILLS_DIR.iterdir()):
            if not dest_dir.is_dir() or dest_dir in expected_skill_dirs:
                continue
            skill_md = dest_dir / "SKILL.md"
            if skill_md.exists() and _read_text(skill_md).startswith(GENERATED_SKILL_HEADER):
                for f in dest_dir.rglob("*"):
                    if f.is_file():
                        f.unlink()
                for d in sorted(dest_dir.rglob("*"), reverse=True):
                    if d.is_dir():
                        d.rmdir()
                dest_dir.rmdir()
                changed_skills += 1

    hooks_result = propagate_hooks_once(verbose=False)

    result = {
        "source_agents": len(agents),
        "hooks_source": hooks_result["hooks_source"],
        "claude_changed": changed_claude + hooks_result["claude_changed"],
        "opencode_changed": changed_opencode + hooks_result["opencode_changed"],
        "codex_changed": changed_codex + hooks_result["codex_changed"],
        "skills_changed": changed_skills,
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
    args = parser.parse_args()

    if not args.once and not args.watch:
        args.once = True

    if args.once:
        propagate_once(verbose=True)

    if args.watch:
        watch_loop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
