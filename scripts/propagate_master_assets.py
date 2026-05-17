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
]

CLAUDE_AGENTS_DIR = REPO_ROOT / "claude" / "agents"
OPENCODE_AGENTS_DIR = REPO_ROOT / "opencode" / "agents"
CODEX_AGENTS_DIR = REPO_ROOT / "codex" / "agents"


GENERATED_AGENT_HEADER = "# Generated from .github/agents source-of-truth. Do not edit manually."


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
        "fetch": ["web_fetch"],
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


def render_claude_agent(
    agent: SourceAgent,
    docs: List[InstructionDoc],
    reference_map: Dict[str, str],
    identifier: str,
) -> str:
    tools = ", ".join(map_tools_for_claude(agent.tools))
    appendix = _build_instruction_appendix(agent, docs)
    body = _rewrite_agent_references(agent.body.strip(), reference_map, preserve_at_sign=True)

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


def render_opencode_agent(agent: SourceAgent, docs: List[InstructionDoc], reference_map: Dict[str, str]) -> str:
    permissions = map_permissions_for_opencode(agent.tools)
    appendix = _build_instruction_appendix(agent, docs)
    body = _rewrite_agent_references(agent.body.strip(), reference_map, preserve_at_sign=True)

    lines: List[str] = [
        "---",
        f"description: \"{agent.description}\"",
        "deepseek/deepseek-v4-pro",
    ]

    if not agent.user_invocable:
        lines.append("mode: subagent")
        lines.append("hidden: true")

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
        f"When the user selects you with the `@` designator, you are already acting as `{identifier}`. "
        f"Begin work in this role immediately. Do not spend your first action invoking `{identifier}` again as a subagent. "
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


def render_codex_agent(agent: SourceAgent, docs: List[InstructionDoc], reference_map: Dict[str, str]) -> str:
    combined = agent.body.strip()
    appendix = _build_instruction_appendix(agent, docs)
    if appendix:
        combined = f"{combined}\n\n{appendix.strip()}"

    combined = _rewrite_agent_references(combined, reference_map, preserve_at_sign=False)
    combined = _inject_codex_selected_agent_instruction(agent, combined)

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


def propagate_once(verbose: bool = True) -> Dict[str, int]:
    agents = load_source_agents()
    instructions = load_instruction_docs()

    CLAUDE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    OPENCODE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CODEX_AGENTS_DIR.mkdir(parents=True, exist_ok=True)

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

        if _write_if_changed(
            claude_file,
            render_claude_agent(agent, docs, claude_reference_map, claude_identifier),
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

    result = {
        "source_agents": len(agents),
        "claude_changed": changed_claude,
        "opencode_changed": changed_opencode,
        "codex_changed": changed_codex,
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
    print("Starting master asset watcher for .github/{agents,skills,instructions} ...")
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
