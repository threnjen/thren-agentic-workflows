"""Mechanical invariants over the agent corpus in `source_of_truth/`.

These are the checks a prose review reliably misses: a roster naming an agent
that no longer exists, a malformed frontmatter block, an `applyTo` glob that
stopped matching and now inlines nothing.

Every check here is *structural* -- it compares frontmatter, file paths, and tool
grants against what is on disk. None of them match against agent prose. That is a
deliberate constraint: the corpus body text is rewritten constantly, and a check
keyed to expected wording goes silently inert the moment someone rephrases a
sentence, passing forever while verifying nothing. A check that cannot survive a
reword does not belong in this file.

Everything here is read-only. Parsing is delegated to
`scripts/propagate_master_assets.py` so the tests see exactly the frontmatter,
tool keys, and `applyTo` semantics that propagation itself sees -- a check that
parsed differently would be checking a different corpus.
"""

import hashlib
import re
import sys
import unittest
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod  # noqa: E402

SOT_DIR = REPO_ROOT / "source_of_truth"
AGENTS_DIR = SOT_DIR / "agents"
SKILLS_DIR = SOT_DIR / "skills"
VALID_AGENT_FRONTMATTER_KEYS = frozenset(
    {"name", "description", "tools", "agents", "user-invocable", "profile", "model_tier"}
)


# --------------------------------------------------------------------------
# Corpus loading
# --------------------------------------------------------------------------


def _agent_paths() -> List[Path]:
    return sorted(AGENTS_DIR.glob("*.md"))


def _load_agents() -> List[mod.SourceAgent]:
    """The propagator's own view of the agent corpus."""
    return mod.load_source_agents()


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _fail_report(header: str, problems: Iterable[str]) -> str:
    lines = [header, ""]
    lines.extend(f"  - {p}" for p in problems)
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Check 1: frontmatter rosters resolve, and are backed by the `agent` tool
# --------------------------------------------------------------------------


class RosterTests(unittest.TestCase):
    def test_every_frontmatter_roster_entry_names_a_real_agent(self) -> None:
        agents = _load_agents()
        known_names = {a.name for a in agents}

        problems: List[str] = []
        for agent in agents:
            # Frontmatter roster entries are display names.
            for entry in agent.subagents:
                if entry not in known_names:
                    problems.append(
                        f"{agent.rel_path}: frontmatter `agents:` lists "
                        f"'{entry}', which matches no agent `name:` on disk"
                    )

        self.assertFalse(problems, _fail_report("Dangling roster entries:", problems))

    def test_agents_declaring_a_roster_can_spawn_it(self) -> None:
        problems: List[str] = []
        for agent in _load_agents():
            if agent.subagents and "agent" not in set(agent.tools):
                problems.append(
                    f"{agent.rel_path}: frontmatter `agents:` declares a "
                    f"roster ({', '.join(agent.subagents)}) but `tools:` "
                    f"omits `agent` -- it cannot spawn them"
                )

        self.assertFalse(problems, _fail_report("Rosters that cannot be spawned:", problems))


# --------------------------------------------------------------------------
# Check 2: frontmatter shape
# --------------------------------------------------------------------------

_FM_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:(?: |$)")


class FrontmatterShapeTests(unittest.TestCase):
    def test_every_agent_frontmatter_is_well_formed(self) -> None:
        problems: List[str] = []
        for path in _agent_paths():
            rel = _rel(path)
            text = path.read_text(encoding="utf-8")

            if not text.startswith("---\n"):
                problems.append(f"{rel}: file does not open with a `---` frontmatter fence")
                continue
            end = text.find("\n---\n", 4)
            if end == -1:
                problems.append(f"{rel}: frontmatter block is never closed with `---`")
                continue

            block = text[4:end]
            for lineno, line in enumerate(block.splitlines(), start=2):
                if not line.strip():
                    problems.append(
                        f"{rel}:{lineno}: blank line inside the frontmatter block "
                        f"(truncates parsing in some consumers)"
                    )
                    continue
                if line.startswith((" ", "\t")) or line.lstrip().startswith(("-", "#")):
                    continue
                if not _FM_KEY_RE.match(line):
                    problems.append(f"{rel}:{lineno}: not a `key: value` frontmatter line: {line!r}")

            fm, _body = mod._parse_frontmatter(text)
            unknown_keys = sorted(set(fm) - VALID_AGENT_FRONTMATTER_KEYS)
            if unknown_keys:
                problems.append(
                    f"{rel}: unknown frontmatter key(s) {', '.join(unknown_keys)}; "
                    f"valid keys are {', '.join(sorted(VALID_AGENT_FRONTMATTER_KEYS))}"
                )
            for required in ("name", "description"):
                if not str(fm.get(required, "")).strip():
                    problems.append(f"{rel}: required frontmatter field `{required}` is missing or empty")

            tools = mod._parse_list_value(fm.get("tools", ""))
            invalid = sorted(set(tools) - set(mod.VALID_TOOL_KEYS))
            if invalid:
                problems.append(
                    f"{rel}: invalid `tools:` key(s) {', '.join(invalid)}; "
                    f"valid keys are {', '.join(sorted(mod.VALID_TOOL_KEYS))}"
                )

        self.assertFalse(problems, _fail_report("Malformed agent frontmatter:", problems))

    def test_every_skill_frontmatter_is_well_formed(self) -> None:
        problems: List[str] = []
        for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            rel = _rel(skill_md)
            text = skill_md.read_text(encoding="utf-8")
            if not text.startswith("---\n") or text.find("\n---\n", 4) == -1:
                problems.append(f"{rel}: missing or unclosed frontmatter block")
                continue
            block = text[4 : text.find("\n---\n", 4)]
            for lineno, line in enumerate(block.splitlines(), start=2):
                if not line.strip():
                    problems.append(f"{rel}:{lineno}: blank line inside the frontmatter block")
            fm, _ = mod._parse_frontmatter(text)
            for required in ("name", "description"):
                if not str(fm.get(required, "")).strip():
                    problems.append(f"{rel}: required frontmatter field `{required}` is missing or empty")

        self.assertFalse(problems, _fail_report("Malformed skill frontmatter:", problems))


# --------------------------------------------------------------------------
# Check 3: applyTo globs resolve
# --------------------------------------------------------------------------


class ApplyToTests(unittest.TestCase):
    def test_every_instruction_declares_a_non_empty_apply_to(self) -> None:
        """Only a baseline instruction may omit applyTo.

        A baseline instruction reaches agents through the user-global file
        deploy_agents.py writes, so it has an effect with no roster. Any other
        instruction with no roster is inlined into nothing.
        """
        problems = [
            f"{_rel(doc.path)}: `applyTo:` is missing or empty -- the file is "
            f"inlined into nothing and silently has no effect"
            for doc in mod.load_instruction_docs()
            if not doc.apply_to_patterns and not doc.baseline
        ]
        self.assertFalse(problems, _fail_report("Instructions with no applyTo:", problems))

    def test_every_apply_to_pattern_matches_a_real_file(self) -> None:
        """A stale glob stops applying with no error. This is that error.

        Scope note: only patterns aimed at *this* repository are checkable.
        `python.instructions.md` carries `**/*.py`, which is an editor-side glob
        for a downstream repo's sources -- it is expected to match nothing here,
        and asserting on it would be asserting on a repo we cannot see. The
        checkable set is every pattern that names `source_of_truth/` or an agent
        markdown suffix, which is the set `applicable_instructions` actually
        consults during propagation.
        """
        import fnmatch

        docs = mod.load_instruction_docs()
        agent_rel_paths = [a.rel_path for a in _load_agents()]

        problems: List[str] = []
        checked = 0
        for doc in docs:
            for pattern in doc.apply_to_patterns:
                targets_this_repo = "source_of_truth/" in pattern or pattern.endswith(
                    (".agent.md", "agents/*.md", "agents/**")
                )
                if not targets_this_repo:
                    continue
                checked += 1
                # `applicable_instructions` matches with `fnmatch` against an
                # agent's repo-relative path; use exactly that semantics.
                if any(fnmatch.fnmatch(rel, pattern) for rel in agent_rel_paths):
                    continue
                problems.append(
                    f"{_rel(doc.path)}: applyTo pattern '{pattern}' matches no "
                    f"agent under source_of_truth/agents/ -- it is stale and inlines nothing"
                )

        # Guard against the check going vacuous if the naming convention shifts.
        self.assertGreater(
            checked, 5, "no applyTo pattern targeted source_of_truth/ -- this check went vacuous"
        )
        self.assertFalse(problems, _fail_report("Stale applyTo patterns:", problems))


# --------------------------------------------------------------------------
# Check 4: no large duplicated blocks
# --------------------------------------------------------------------------

BLOCK_LINES = 10

# ---------------------------------------------------------------------------
# ALLOWLIST -- known-acceptable repeated blocks.
#
# Each entry is a distinctive substring (whitespace-normalized) of a block that
# legitimately appears in three or more agents, plus the reason it is not a
# copy-paste defect. Anything NOT listed here is a candidate for extraction into
# a shared skill or instruction file: six divergent copies of one detection
# predicate is exactly the defect this check exists to catch.
# ---------------------------------------------------------------------------
_DUPLICATE_BLOCK_ALLOWLIST: List[Tuple[str, str]] = [
    # Placeholder for entries added when a legitimate repetition is confirmed;
    # see the failure message for the exact normalized text to paste here.
]


def _normalize(line: str) -> str:
    return " ".join(line.split())


def _significant_lines(body: str) -> List[Tuple[int, str]]:
    """Non-trivial lines: skip blanks, bare fences, and short list scaffolding."""
    out: List[Tuple[int, str]] = []
    for lineno, raw in enumerate(body.splitlines(), start=1):
        norm = _normalize(raw)
        if len(norm) < 20:
            continue
        if norm.startswith("```"):
            continue
        out.append((lineno, norm))
    return out


class DuplicateBlockTests(unittest.TestCase):
    def test_no_large_block_is_repeated_across_three_or_more_agents(self) -> None:
        agents = _load_agents()
        # window hash -> {slug: first line number}
        occurrences: Dict[str, Dict[str, int]] = defaultdict(dict)
        sample: Dict[str, str] = {}

        for agent in agents:
            lines = _significant_lines(agent.body)
            for i in range(len(lines) - BLOCK_LINES + 1):
                window = lines[i : i + BLOCK_LINES]
                joined = "\n".join(text for _, text in window)
                digest = hashlib.sha1(joined.encode("utf-8")).hexdigest()
                occurrences[digest].setdefault(agent.source_slug, window[0][0])
                sample.setdefault(digest, joined)

        # Keep only maximal reports: one entry per (set of agents) group, using
        # the longest sample, so a 30-line duplicate is not reported 21 times.
        by_group: Dict[Tuple[str, ...], Tuple[str, Dict[str, int]]] = {}
        for digest, agents_hit in occurrences.items():
            if len(agents_hit) < 3:
                continue
            key = tuple(sorted(agents_hit))
            if key not in by_group:
                by_group[key] = (sample[digest], agents_hit)

        problems: List[str] = []
        for key, (text, agents_hit) in sorted(by_group.items()):
            if any(frag in text for frag, _reason in _DUPLICATE_BLOCK_ALLOWLIST):
                continue
            where = ", ".join(f"{slug}:{line}" for slug, line in sorted(agents_hit.items()))
            first_line = text.splitlines()[0]
            problems.append(
                f"{BLOCK_LINES}+ line block repeated in {len(agents_hit)} agents "
                f"({where}); starts: {first_line!r}"
            )

        self.assertFalse(
            problems,
            _fail_report(
                "Duplicated blocks (extract into a shared skill/instruction, or "
                "allowlist in _DUPLICATE_BLOCK_ALLOWLIST with a reason):",
                problems,
            ),
        )


if __name__ == "__main__":
    unittest.main()
