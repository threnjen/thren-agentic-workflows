#!/usr/bin/env python3
"""Transform source_of_truth/ master assets into per-harness ports/ outputs.

This script treats `source_of_truth/` as the canonical home for agents, skills,
and instructions, and regenerates target-platform variants under
`ports/{claude,codex,opencode,cursor}`. It also mirrors the source verbatim to
`ports/github` and to a real `.github/` directory at the repository root.

Run with `--watch` (the maintainer workflow) to re-propagate on every save under
`source_of_truth/`. Deployment of `ports/` to real harness config directories is
the separate `deploy_assets.py` script.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

from asset_paths import (
    GENERATED_AGENT_HEADER,
    GENERATED_AGENT_MARKDOWN_HEADER,
    GENERATED_SKILL_HEADER,
    LEGACY_GENERATED_MARKERS,
    PORTS_DIR,
    REPO_ROOT,
    SOT_DIR,
    generated_marker_line_index as _generated_marker_line_index,
    poll_watch,
)

# Source-of-truth roots.
SOT_AGENTS_DIR = SOT_DIR / "agents"
SOT_INSTRUCTIONS_DIR = SOT_DIR / "instructions"
SOT_SKILLS_DIR = SOT_DIR / "skills"
SOT_HOOKS_DIR = SOT_DIR / "hooks"

# Generated platform output roots under `ports/`.
CLAUDE_AGENTS_DIR = PORTS_DIR / "claude" / "agents"
CLAUDE_COMMANDS_DIR = PORTS_DIR / "claude" / "commands"
CLAUDE_SKILLS_DIR = PORTS_DIR / "claude" / "skills"
OPENCODE_AGENTS_DIR = PORTS_DIR / "opencode" / "agents"
OPENCODE_SKILLS_DIR = PORTS_DIR / "opencode" / "skills"
CODEX_AGENTS_DIR = PORTS_DIR / "codex" / "agents"
# Legacy generated profiles are retained as a cleanup root only. Codex CLI
# profiles are configuration layers, not custom-agent entry points.
CODEX_PROFILES_DIR = PORTS_DIR / "codex" / "profiles"
CODEX_SKILLS_DIR = PORTS_DIR / "codex" / "skills"
CURSOR_COMMANDS_DIR = PORTS_DIR / "cursor" / "commands"
CURSOR_RULES_DIR = PORTS_DIR / "cursor" / "rules"
GITHUB_PORT_DIR = PORTS_DIR / "github"
DOT_GITHUB_DIR = REPO_ROOT / ".github"

# Subdirectories mirrored verbatim to ports/github and .github. Anything else in
# .github/ (e.g. workflows/) is never touched.
GITHUB_MIRRORED_SUBDIRS = ("agents", "hooks", "instructions", "skills")

WATCH_DIRS = [
    SOT_AGENTS_DIR,
    SOT_SKILLS_DIR,
    SOT_INSTRUCTIONS_DIR,
    SOT_HOOKS_DIR,
]
# Agents that should not be propagated to any platform output directory.
# Add a source slug string here to exclude an agent during propagation.
# Currently empty — all source agents are propagated.
PROPAGATION_EXCLUDE: set[str] = set()

INVENTORY_COUNTERS = frozenset({"source_agents"})
DEFAULT_CONVERGENCE_PASSES = 5
MAX_CONVERGENCE_PASSES = 25


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
    description: str = ""


@dataclass(frozen=True)
class PropagationConvergenceResult:
    converged: bool
    pass_count: int
    changed_passes: int
    total_changes: Dict[str, int]
    final_counters: Dict[str, int]


class PropagationConvergenceError(RuntimeError):
    def __init__(self, category: str, pass_count: int) -> None:
        self.category = category
        self.pass_count = pass_count
        super().__init__(f"{category} after {pass_count} propagation pass(es)")


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
    if index >= len(lines):
        return False
    # Files written before the source_of_truth/ restructure carry the old marker
    # text; they are still generated output and still prunable.
    return lines[index] == marker.strip("\n") or lines[index] in LEGACY_GENERATED_MARKERS


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

    Containment is checked before anything is enumerated. Guarding only the leaf
    is not enough: if the generated ROOT is itself a symlink out of the repo, its
    children are ordinary files that pass every leaf check, and each carrying the
    marker gets unlinked outside the repository. This is REPO-SEC-06 in deletion
    form, and unlike a bad write it cannot be undone by re-running propagation.
    """
    _validate_output_directory(directory)

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


def _prune_orphaned_skill_dirs(
    skills_dir: Path,
    expected: set[Path],
    marker: str,
) -> int:
    """Delete generated skill directories under `skills_dir` whose source is gone.

    Same two-condition rule as `_prune_orphaned_outputs`, applied to a directory via
    its SKILL.md. Skills are removed as a tree because a skill is a directory of
    assets; this is the one path where recursive removal is in scope.

    Containment is checked before anything is enumerated, for the same reason as
    `_prune_orphaned_outputs` and with a wider blast radius: the marker guard reads
    one file (`SKILL.md`) but `shutil.rmtree` removes the whole tree, so every
    sibling of that marker is deleted without ever being inspected. A symlinked
    skills root therefore trades one marker for an entire directory outside the
    repository.
    """
    _validate_output_directory(skills_dir)

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
        block_scalar_lines: List[str] = []
        probe = index + 1
        while probe < len(lines):
            probe_line = lines[probe]
            if not probe_line.startswith((" ", "\t")):
                break
            item = probe_line.strip()
            if item.startswith("- "):
                block_items.append(item[2:].strip())
            elif item:
                block_scalar_lines.append(item)
            probe += 1

        if block_items:
            data[key] = block_items
            index = probe
            continue

        if block_scalar_lines:
            data[key] = " ".join(block_scalar_lines)
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
    for path in sorted(SOT_AGENTS_DIR.glob("*.md")):
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
    for path in sorted(SOT_INSTRUCTIONS_DIR.glob("*.instructions.md")):
        text = _read_text(path)
        fm, body = _parse_frontmatter(text)

        raw_apply_to = str(fm.get("applyTo", "")).strip().strip('"').strip("'")
        patterns = [p.strip().strip('"').strip("'") for p in raw_apply_to.split(",")]
        patterns = [p for p in patterns if p]

        docs.append(
            InstructionDoc(
                path=path,
                apply_to_patterns=patterns,
                body=body.strip() + "\n",
                description=str(fm.get("description", "")).strip().strip('"').strip("'"),
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
        # Replace @agent-name references (always safe)
        rewritten = rewritten.replace(f"@{source_name}", at_replacement)

        # For bare references, use word boundaries to avoid partial matches.
        # E.g., don't replace "QA" in "QA_AUTOMATED" when looking for agent "QA".
        # Match: " QA " (space-delimited), "**QA**" (bold), "- QA" (list), etc.
        # But NOT: "QA_AUTOMATED", "qa-bootstrap", compound identifiers.
        pattern = r"(?<![A-Za-z0-9_-])(" + re.escape(source_name) + r")(?![A-Za-z0-9_-])"
        rewritten = re.sub(pattern, identifier, rewritten)
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


def _validate_output_directory(directory: Path) -> None:
    """Reject generated-output directories that resolve outside the target root."""
    resolved_root = REPO_ROOT.resolve()
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


def propagate_skills_once() -> Dict[str, int]:
    if not SOT_SKILLS_DIR.exists():
        return {
            "claude_changed": 0,
            "opencode_changed": 0,
            "codex_changed": 0,
            "skills_changed": 0,
            "skill_orphans_removed": 0,
        }

    CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    OPENCODE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    CODEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    changed_claude = 0
    changed_opencode = 0
    changed_codex = 0
    expected_claude_dirs: set[Path] = set()
    expected_opencode_dirs: set[Path] = set()
    expected_codex_dirs: set[Path] = set()

    for source_skill_dir in sorted(SOT_SKILLS_DIR.iterdir()):
        if not source_skill_dir.is_dir():
            continue

        skill_name = source_skill_dir.name
        source_skill_md = source_skill_dir / "SKILL.md"

        dest_claude_dir = CLAUDE_SKILLS_DIR / skill_name
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

        dest_opencode_dir = OPENCODE_SKILLS_DIR / skill_name
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

        dest_codex_dir = CODEX_SKILLS_DIR / skill_name
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
        _prune_orphaned_skill_dirs(
            CLAUDE_SKILLS_DIR, expected_claude_dirs, GENERATED_SKILL_HEADER
        )
        + _prune_orphaned_skill_dirs(
            OPENCODE_SKILLS_DIR, expected_opencode_dirs, GENERATED_SKILL_HEADER
        )
        + _prune_orphaned_skill_dirs(
            CODEX_SKILLS_DIR, expected_codex_dirs, GENERATED_SKILL_HEADER
        )
    )

    return {
        "claude_changed": changed_claude,
        "opencode_changed": changed_opencode,
        "codex_changed": changed_codex,
        "skills_changed": changed_claude + changed_opencode + changed_codex,
        "skill_orphans_removed": orphans_removed,
    }


def _first_sentence(text: str, limit: int = 200) -> str:
    """A one-line description: the first `#` title, else the first prose sentence."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()[:limit]
        if not stripped or stripped.startswith(("#", "---", "<!--", "**", "|", "-", ">")):
            continue
        end = stripped.find(". ")
        sentence = stripped if end == -1 else stripped[: end + 1]
        return sentence[:limit]
    return ""


def render_cursor_command(
    agent: SourceAgent,
    docs: List[InstructionDoc],
    reference_map: Dict[str, str],
    identifier: str,
) -> str:
    """Render a Cursor command (plain markdown, no frontmatter) adopting this role."""
    appendix = _build_instruction_appendix(agent, docs)
    body = _rewrite_agent_references(agent.body.strip(), reference_map, preserve_at_sign=True)
    body = _inject_claude_command_instruction(agent, identifier, body)

    parts = [body]
    if appendix:
        parts.extend(["", "---", "", _rewrite_agent_references(appendix.strip(), reference_map, preserve_at_sign=True)])

    return _with_generated_marker("\n".join(parts).rstrip() + "\n", GENERATED_AGENT_MARKDOWN_HEADER)


def render_cursor_rule(
    description: str,
    globs: List[str],
    always_apply: bool,
    body: str,
) -> str:
    """Render a Cursor rule (.mdc): MDC frontmatter, generated marker, body."""
    lines = ["---", f"description: {json.dumps(description, ensure_ascii=False)}"]
    if globs:
        lines.append(f"globs: {','.join(globs)}")
    lines.append(f"alwaysApply: {'true' if always_apply else 'false'}")
    lines.extend(["---", "", body.strip(), ""])
    return _with_generated_marker("\n".join(lines), GENERATED_AGENT_MARKDOWN_HEADER)


def propagate_cursor_rules_once(instructions: List[InstructionDoc]) -> Dict[str, int]:
    """Emit Cursor rules from instruction docs, then prune orphans.

    Instructions whose applyTo patterns target agent-definition files are internal
    plumbing for the agent renderers (their content already ships inside each
    rendered agent/command) and are skipped. Instructions with real file globs
    """
    changed = 0
    expected: set[Path] = set()

    for doc in instructions:
        globs = [
            pattern
            for pattern in doc.apply_to_patterns
            if not pattern.rstrip("*/").endswith((".agent.md", "agents"))
        ]
        if doc.apply_to_patterns and not globs:
            continue
        name = doc.path.name.replace(".instructions.md", "")
        dest = CURSOR_RULES_DIR / f"{name}.mdc"
        expected.add(dest)
        content = render_cursor_rule(
            doc.description or _first_sentence(doc.body),
            globs,
            always_apply=not globs,
            body=doc.body,
        )
        if _write_if_changed(dest, content):
            changed += 1

    orphans = _prune_orphaned_outputs(
        CURSOR_RULES_DIR, "*.mdc", expected, GENERATED_AGENT_MARKDOWN_HEADER
    )
    return {"cursor_changed": changed, "cursor_rule_orphans_removed": orphans}


def _mirror_tree(source: Path, destination: Path) -> int:
    """Mirror `source` into `destination` byte-for-byte; delete stale files.

    Deletion is scoped to `destination` itself (validated inside the repository),
    never follows symlinks, and leaves empty directories cleaned up without
    counting them as changes.
    """
    _validate_output_directory(destination)
    changed = 0
    expected: set[Path] = set()

    if source.is_dir():
        for source_file in sorted(source.rglob("*")):
            if not source_file.is_file() or source_file.is_symlink():
                continue
            dest_file = destination / source_file.relative_to(source)
            expected.add(dest_file)
            data = source_file.read_bytes()
            if dest_file.is_file() and not dest_file.is_symlink():
                try:
                    if dest_file.read_bytes() == data:
                        continue
                except OSError:
                    pass
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            dest_file.write_bytes(data)
            shutil.copymode(source_file, dest_file)  # hooks ship executable scripts
            changed += 1

    if destination.is_dir():
        for path in sorted(destination.rglob("*"), reverse=True):
            if path.is_file() and not path.is_symlink() and path not in expected:
                path.unlink()
                changed += 1
            elif path.is_dir() and not path.is_symlink() and not any(path.iterdir()):
                path.rmdir()

    return changed


def mirror_github_once() -> Dict[str, int]:
    """Mirror the source subdirs verbatim to ports/github and .github.

    Only `GITHUB_MIRRORED_SUBDIRS` are touched; anything else under the
    destinations (e.g. `.github/workflows/`) is never enumerated or deleted.
    """
    changed = 0
    for subdir in GITHUB_MIRRORED_SUBDIRS:
        source = SOT_DIR / subdir
        for destination_root in (GITHUB_PORT_DIR, DOT_GITHUB_DIR):
            changed += _mirror_tree(source, destination_root / subdir)
    return {"github_changed": changed}


def propagate_once(verbose: bool = True) -> Dict[str, int]:
    agents = load_source_agents()
    instructions = load_instruction_docs()

    CLAUDE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CLAUDE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    OPENCODE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CODEX_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    CODEX_PROFILES_DIR.mkdir(parents=True, exist_ok=True)

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
    changed_cursor = 0
    expected_claude_files: set[Path] = set()
    expected_claude_command_files: set[Path] = set()
    expected_opencode_files: set[Path] = set()
    expected_codex_files: set[Path] = set()
    expected_cursor_command_files: set[Path] = set()

    for agent in agents:
        docs = applicable_instructions(agent, instructions)

        claude_identifier = _claude_identifier_for(agent, claude_existing_stems)
        claude_file = CLAUDE_AGENTS_DIR / f"{claude_identifier}.md"
        opencode_file = OPENCODE_AGENTS_DIR / _opencode_filename_for(agent, opencode_existing_stems)
        codex_file = CODEX_AGENTS_DIR / _codex_filename_for(agent)
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
            command_file = CLAUDE_COMMANDS_DIR / f"{claude_identifier}.md"
            expected_claude_command_files.add(command_file)
            if _write_if_changed(
                command_file,
                render_claude_command(agent, docs, claude_reference_map, claude_identifier),
            ):
                changed_claude += 1

            cursor_file = CURSOR_COMMANDS_DIR / f"{claude_identifier}.md"
            expected_cursor_command_files.add(cursor_file)
            if _write_if_changed(
                cursor_file,
                render_cursor_command(agent, docs, claude_reference_map, claude_identifier),
            ):
                changed_cursor += 1

        if _write_if_changed(opencode_file, render_opencode_agent(agent, docs, opencode_reference_map)):
            changed_opencode += 1
        if _write_if_changed(codex_file, render_codex_agent(agent, docs, codex_reference_map)):
            changed_codex += 1

    # Every prune runs only after all emission above has completed. `_claude_filename_for`
    # and `_opencode_filename_for` resolve an output name against the stems already on
    # disk, so deleting first could hand a survivor a different filename (AC6).
    claude_orphans = _prune_orphaned_outputs(
        CLAUDE_AGENTS_DIR, "*.md", expected_claude_files, GENERATED_AGENT_MARKDOWN_HEADER
    )
    claude_command_orphans = _prune_orphaned_outputs(
        CLAUDE_COMMANDS_DIR,
        "*.md",
        expected_claude_command_files,
        GENERATED_AGENT_MARKDOWN_HEADER,
    )
    opencode_orphans = _prune_orphaned_outputs(
        OPENCODE_AGENTS_DIR, "*.md", expected_opencode_files, GENERATED_AGENT_MARKDOWN_HEADER
    )
    codex_orphans = _prune_orphaned_outputs(
        CODEX_AGENTS_DIR, "*.toml", expected_codex_files, GENERATED_AGENT_HEADER
    )
    # Retire the old generated config profiles. They were never deployed by the
    # current installer and incorrectly implied that --profile selected an agent.
    codex_profile_orphans = _prune_orphaned_outputs(
        CODEX_PROFILES_DIR,
        "*.config.toml",
        set(),
        GENERATED_AGENT_HEADER,
    )
    cursor_command_orphans = _prune_orphaned_outputs(
        CURSOR_COMMANDS_DIR,
        "*.md",
        expected_cursor_command_files,
        GENERATED_AGENT_MARKDOWN_HEADER,
    )

    skill_result = propagate_skills_once()
    changed_skills = skill_result["skills_changed"]

    cursor_rules_result = propagate_cursor_rules_once(instructions)
    github_result = mirror_github_once()

    result = {
        "source_agents": len(agents),
        "claude_changed": changed_claude + skill_result["claude_changed"],
        "opencode_changed": changed_opencode + skill_result["opencode_changed"],
        "codex_changed": changed_codex + skill_result["codex_changed"],
        "cursor_changed": changed_cursor + cursor_rules_result["cursor_changed"],
        "skills_changed": changed_skills,
        "github_changed": github_result["github_changed"],
        # Deletions are reported on their own keys rather than folded into the
        # `changed_*` counters, which already conflate writes with removals. This
        # follows the orphan-removal precedent: a run that
        # removes a file says so instead of removing it silently.
        "claude_orphans_removed": claude_orphans,
        "claude_command_orphans_removed": claude_command_orphans,
        "opencode_orphans_removed": opencode_orphans,
        "codex_orphans_removed": codex_orphans,
        "codex_profile_orphans_removed": codex_profile_orphans,
        "cursor_command_orphans_removed": cursor_command_orphans,
        "cursor_rule_orphans_removed": cursor_rules_result["cursor_rule_orphans_removed"],
        "skill_orphans_removed": skill_result["skill_orphans_removed"],
    }

    if verbose:
        print(json.dumps(result, indent=2))

    return result


def propagation_changes(counters: Dict[str, int]) -> Dict[str, int]:
    """Return repository mutation counters, rejecting ambiguous results."""
    if not isinstance(counters, dict):
        raise ValueError("propagation result must be a dictionary")

    changes: Dict[str, int] = {}
    for key, value in counters.items():
        if not isinstance(key, str) or isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("propagation counters must map names to integers")
        if value < 0:
            raise ValueError("propagation counters cannot be negative")
        if key not in INVENTORY_COUNTERS and value:
            changes[key] = value
    return changes


def propagate_until_converged(
    *,
    max_passes: int = DEFAULT_CONVERGENCE_PASSES,
    propagate: Callable[[], Dict[str, int]] | None = None,
) -> PropagationConvergenceResult:
    """Repeat propagation, within a total-pass bound, through a zero-change pass."""
    if (
        isinstance(max_passes, bool)
        or not isinstance(max_passes, int)
        or not 1 <= max_passes <= MAX_CONVERGENCE_PASSES
    ):
        raise ValueError(
            f"max_passes must be between 1 and {MAX_CONVERGENCE_PASSES}"
        )

    run_pass = propagate or (lambda: propagate_once(verbose=False))
    total_changes: Dict[str, int] = {}
    changed_passes = 0

    for pass_count in range(1, max_passes + 1):
        try:
            counters = run_pass()
        except Exception as exc:
            if isinstance(exc, PropagationConvergenceError):
                raise
            raise PropagationConvergenceError(
                "propagation_failed", pass_count
            ) from exc

        try:
            changes = propagation_changes(counters)
        except (TypeError, ValueError) as exc:
            raise PropagationConvergenceError("malformed_result", pass_count) from exc

        if not changes:
            return PropagationConvergenceResult(
                converged=True,
                pass_count=pass_count,
                changed_passes=changed_passes,
                total_changes=total_changes,
                final_counters=dict(counters),
            )

        changed_passes += 1
        for key, value in changes.items():
            total_changes[key] = total_changes.get(key, 0) + value

    raise PropagationConvergenceError("bound_exhausted", max_passes)



def watch_loop(interval_seconds: float = 1.0) -> None:
    print("Starting master asset watcher for source_of_truth/{agents,skills,instructions,hooks} ...")
    print(json.dumps(_convergence_payload(propagate_until_converged()), indent=2))

    def _on_change(changes: List[str]) -> None:
        sample = ", ".join(Path(c).name for c in changes[:5])
        more = "" if len(changes) <= 5 else f" (+{len(changes) - 5} more)"
        print(f"Detected change in source_of_truth: {sample}{more}")
        try:
            print(json.dumps(_convergence_payload(propagate_until_converged()), indent=2))
        except PropagationConvergenceError as exc:  # pragma: no cover - runtime guard
            print(f"Propagation failed: {exc}", file=sys.stderr)

    poll_watch(WATCH_DIRS, _on_change, interval_seconds=interval_seconds)


def _convergence_payload(result: PropagationConvergenceResult) -> Dict[str, object]:
    return {
        "converged": result.converged,
        "propagation_passes": result.pass_count,
        "changed_passes": result.changed_passes,
        "propagation_changes": result.total_changes,
        "verification_changes": propagation_changes(result.final_counters),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transform source_of_truth/ master assets into ports/ outputs."
    )
    parser.add_argument("--once", action="store_true", help="Run one propagation pass and exit.")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch source_of_truth/ folders and propagate on changes.",
    )
    args = parser.parse_args()

    if not args.watch:
        args.once = True

    if args.once:
        try:
            result = propagate_until_converged()
        except PropagationConvergenceError as exc:
            print(f"Propagation failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(_convergence_payload(result), indent=2))

    if args.watch:
        watch_loop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
