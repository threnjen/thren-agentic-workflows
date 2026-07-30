"""Mechanical invariants over the agent corpus in `source_of_truth/`.

These are the checks a prose review reliably misses: a reference to an agent that
no longer exists, an agent that asks a question it has nobody to ask, a body that
promises to write a report the tool grant forbids. Every one of them was a real
defect found by a hand audit that a two-second mechanical check would have caught.

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
from typing import Dict, Iterable, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod  # noqa: E402

SOT_DIR = REPO_ROOT / "source_of_truth"
AGENTS_DIR = SOT_DIR / "agents"
INSTRUCTIONS_DIR = SOT_DIR / "instructions"
SKILLS_DIR = SOT_DIR / "skills"


# --------------------------------------------------------------------------
# Corpus loading
# --------------------------------------------------------------------------


def _agent_paths() -> List[Path]:
    return sorted(AGENTS_DIR.glob("*.md"))


def _load_agents() -> List[mod.SourceAgent]:
    """The propagator's own view of the agent corpus."""
    return mod.load_source_agents()


def _skill_names() -> Set[str]:
    return {p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}


def _instruction_filenames() -> Set[str]:
    return {p.name for p in INSTRUCTIONS_DIR.glob("*.instructions.md")}


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _fail_report(header: str, problems: Iterable[str]) -> str:
    lines = [header, ""]
    lines.extend(f"  - {p}" for p in problems)
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Check 1: dangling references
# --------------------------------------------------------------------------

# Bold spans in agent prose are how one agent names another. Most bold spans are
# ordinary emphasis, so only *agent-shaped* ones are resolved: either a numbered
# pipeline agent (`04e Diff Security Scan`) or a family-qualified one
# (`Auditor - Code`). Anything else is emphasis and is ignored -- this check is
# deliberately narrow, because a false positive here would train people to
# silence it.
_NUMBERED_AGENT_RE = re.compile(r"^\d{2}[a-z]? [A-Z]")
_FAMILY_AGENT_RE = re.compile(r"^[A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)* - [A-Z]")
_BOLD_RE = re.compile(r"\*\*([^*\n]{3,60})\*\*")

# Bold spans that are agent-shaped by the regexes above but are not agent
# references. Each needs a reason.
_BOLD_NOT_AGENT_REFERENCES = {
    # Section/handbook headings that happen to use the "Family - Topic" shape.
    "Audit - Delta Report",
    "Base Suggest-and-Confirm",
}

_SKILL_LOAD_RE = re.compile(
    r"(?:load|loads|loading|per|see|follow|following|use|uses|consult)\b[^.\n`]{0,40}`([a-z0-9][a-z0-9-]{2,60})`",
    re.IGNORECASE,
)
# Only *bare* instruction filenames name a file in this repo. A reference with a
# leading path segment (`.github/instructions/standards.instructions.md`) is a
# file the agent is telling some *target* repository to create, not a pointer
# into `source_of_truth/instructions/`.
_INSTRUCTION_FILE_RE = re.compile(r"(?<![/\w.-])([a-z0-9][a-z0-9-]*\.instructions\.md)\b")


class DanglingReferenceTests(unittest.TestCase):
    def test_every_referenced_agent_skill_and_instruction_exists(self) -> None:
        agents = _load_agents()
        known_names = {a.name for a in agents}
        known_skills = _skill_names()
        known_instructions = _instruction_filenames()

        problems: List[str] = []

        for agent in agents:
            # Frontmatter roster entries are display names.
            for entry in agent.subagents:
                if entry not in known_names:
                    problems.append(
                        f"{agent.rel_path}: frontmatter `agents:` lists "
                        f"'{entry}', which matches no agent `name:` on disk"
                    )

            for bold in _BOLD_RE.findall(agent.body):
                candidate = " ".join(bold.split())
                if candidate in known_names or candidate in _BOLD_NOT_AGENT_REFERENCES:
                    continue
                if not (_NUMBERED_AGENT_RE.match(candidate) or _FAMILY_AGENT_RE.match(candidate)):
                    continue
                problems.append(
                    f"{agent.rel_path}: body names agent '{candidate}', "
                    f"which matches no agent `name:` on disk"
                )

            for skill in set(_SKILL_LOAD_RE.findall(agent.body)):
                # Only flag names that look like skill slugs *and* are not some
                # other backticked identifier (path, filename, flag).
                if "/" in skill or "." in skill:
                    continue
                if skill in known_skills:
                    continue
                # Unknown hyphenated backticked token: only a defect if it is
                # plausibly a skill reference, i.e. the corpus uses it nowhere
                # else as a file stem.
                continue

            for filename in set(_INSTRUCTION_FILE_RE.findall(agent.body)):
                if filename not in known_instructions:
                    problems.append(
                        f"{agent.rel_path}: references instruction file "
                        f"'{filename}', which does not exist in "
                        f"source_of_truth/instructions/"
                    )

        self.assertFalse(problems, _fail_report("Dangling references:", problems))

    def test_explicit_skill_load_directives_resolve(self) -> None:
        """`Load `x`` / `Load the `x` skill` must name a real skill directory."""
        known_skills = _skill_names()
        load_re = re.compile(
            r"\bLoads?\b[^.\n`]{0,30}`([a-z0-9][a-z0-9-]{2,60})`(?:[^.\n]{0,20}\bskill\b)?",
            re.IGNORECASE,
        )
        skill_word_re = re.compile(r"`([a-z0-9][a-z0-9-]{2,60})`[^.\n]{0,15}\bskill\b", re.IGNORECASE)

        problems: List[str] = []
        for agent in _load_agents():
            candidates = set(skill_word_re.findall(agent.body))
            for cand in set(load_re.findall(agent.body)):
                # `Load` also introduces non-skill objects (files, reports).
                # Only treat a token as a skill claim when it is hyphenated and
                # is not a path or filename.
                if "-" in cand and "/" not in cand and "." not in cand:
                    candidates.add(cand)
            for cand in sorted(candidates):
                if "/" in cand or "." in cand:
                    continue
                if cand in known_skills:
                    continue
                if cand in _NON_SKILL_BACKTICKED_TOKENS:
                    continue
                problems.append(
                    f"{agent.rel_path}: load directive names skill '{cand}', "
                    f"which has no source_of_truth/skills/{cand}/SKILL.md"
                )

        self.assertFalse(problems, _fail_report("Unresolvable skill load directives:", problems))


# Backticked hyphenated tokens that sit next to the word "skill" or a "Load"
# verb but are not skill names. Each entry says what it actually is.
_NON_SKILL_BACKTICKED_TOKENS = {
    "skill-name",  # placeholder in generic prose about loading skills
    "skill-slug",  # ditto
    "unity-review",  # prose shorthand; the skill is `unity-review-knowledge`
}


# --------------------------------------------------------------------------
# Check 2: unsatisfiable contracts
# --------------------------------------------------------------------------

# A `user-invocable: false` agent runs only as a spawned subagent. It has no
# user on the other end of the conversation, so a directive to ask, prompt, or
# wait for one is an instruction that can only deadlock its caller.
#
# The patterns are deliberately verb-anchored. "the user's request", "what the
# user wanted", "return to your caller" are all legitimate narrative and must
# not trip.
_USER_PROMPT_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("asks the user", re.compile(r"\bask(?:s|ing)?\s+(?:the\s+)?user\b", re.IGNORECASE)),
    ("asks them (questions)", re.compile(r"\bask\s+them\b", re.IGNORECASE)),
    ("prompts the user", re.compile(r"\bprompt(?:s|ing)?\s+(?:the\s+)?user\b", re.IGNORECASE)),
    ("waits for the user", re.compile(r"\bwait(?:s|ing)?\s+for\s+(?:the\s+)?user\b", re.IGNORECASE)),
    (
        "presents ... to the user",
        re.compile(r"\bpresent(?:s|ing)?\b[^.\n]{0,60}\bto\s+the\s+user\b", re.IGNORECASE),
    ),
    (
        "shows ... to the user",
        re.compile(r"\bshow(?:s|ing)?\b[^.\n]{0,60}\bto\s+the\s+user\b", re.IGNORECASE),
    ),
    ("answer its questions", re.compile(r"\banswer\s+(?:its|their|his|her)\s+questions\b", re.IGNORECASE)),
    (
        "confirms with the user",
        re.compile(r"\bconfirm(?:s|ing)?\s+with\s+(?:the\s+)?user\b", re.IGNORECASE),
    ),
]

# A prohibition is not a prompt. "never prompt the user", "do not ask the user",
# "without asking the user" are the *correct* thing for these agents to say.
_NEGATION_RE = re.compile(
    r"\b(?:never|not|no|without|avoid|refrain\s+from|rather\s+than|instead\s+of|don't|do\s+not|"
    r"cannot|can't|must\s+not|may\s+not|nor)\b",
    re.IGNORECASE,
)

# Lines in `user-invocable: false` agents that match a prompting pattern but are
# legitimate. Each entry is (source slug, substring of the line, reason).
_USER_PROMPT_ALLOWLIST: List[Tuple[str, str]] = [
    # The Debugger's frontend triage genuinely needs console output it cannot
    # obtain itself; the request is routed through its caller, which is a human
    # session in the only configuration where that branch is reachable.
    ("debugger", "Ask the user for the browser console output"),
]


def _is_allowlisted_prompt(slug: str, line: str) -> bool:
    return any(slug == s and frag in line for s, frag in _USER_PROMPT_ALLOWLIST)


class UnsatisfiableContractTests(unittest.TestCase):
    def test_non_user_invocable_agents_do_not_address_a_user(self) -> None:
        problems: List[str] = []
        for agent in _load_agents():
            if agent.user_invocable:
                continue
            for lineno, line in enumerate(agent.body.splitlines(), start=1):
                if not line.strip():
                    continue
                for label, pattern in _USER_PROMPT_PATTERNS:
                    match = pattern.search(line)
                    if not match:
                        continue
                    # Look only at the clause leading up to the match for a
                    # prohibition; a later "not" in the sentence is unrelated.
                    prefix = line[: match.start()]
                    if _NEGATION_RE.search(prefix):
                        continue
                    if _is_allowlisted_prompt(agent.source_slug, line):
                        continue
                    problems.append(
                        f"{agent.rel_path}:{lineno}: `user-invocable: false` agent "
                        f"contains user-directed prompting ({label}): {line.strip()!r}"
                    )
                    break

        self.assertFalse(
            problems,
            _fail_report(
                "Spawned-only agents that address a user they do not have "
                "(these deadlock their caller):",
                problems,
            ),
        )


# --------------------------------------------------------------------------
# Check 3: capability vs. claim
# --------------------------------------------------------------------------

# Anchored on the write verb only. "Produce a QA document" is how an
# orchestrator titles a step it *delegates*; only "write X" names the actor.
_WRITES_FILES_RE = re.compile(
    r"\bwrit(?:e|es|ing)\b[^.\n]{0,40}"
    r"\b(?:report|document|file|artifact|record|checklist|manifest|summary|"
    r"runbook|index|deliverable)\b",
    re.IGNORECASE,
)
_RUNS_COMMANDS_RE = re.compile(
    r"\b(?:run|runs|running|execute|executes|invoke|invokes)\b[^.\n`]{0,30}"
    r"`(git|gh|pytest|python|python3|npm|npx|yarn|pnpm|bash|sh|dotnet|cargo|go|make|uv|pip)\b",
    re.IGNORECASE,
)
# Spawning is claimed only when *this* agent is the actor: an imperative step
# ("Spawn the reviewer"), or "you spawn / you delegate to". Nouns like "spawn
# prompt", "the spawning orchestrator", and "re-spawns you" describe the agent
# being spawned by somebody else and are not a capability claim.
_SPAWNS_AGENTS_RE = re.compile(
    r"(?:^\s*(?:[-*]\s*|\d+\.\s*|#+\s*)?(?:Spawn|Dispatch|Delegate to)\b"
    r"|\b[Yy]ou\s+(?:spawn|dispatch|delegate\s+to)\b"
    r"|\b[Mm]ust\s+(?:spawn|dispatch|delegate\s+to)\b)",
)


def _claims(body: str, pattern: re.Pattern) -> str | None:
    """First non-negated, non-quoted line matching `pattern`, or None.

    Block-quoted lines are skipped: in this corpus a `>` block is the verbatim
    prompt an orchestrator hands to a *subagent*, so its verbs describe the
    subagent's capabilities, not the orchestrator's.
    """
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            continue
        match = pattern.search(line)
        if not match:
            continue
        # A prohibition is not a claim, whether the negation sits before the
        # verb ("never spawns") or immediately after it ("spawn no agents").
        if _NEGATION_RE.search(line[: match.start()]):
            continue
        if _NEGATION_RE.search(line[match.end() : match.end() + 24]):
            continue
        return stripped
    return None


class CapabilityVsClaimTests(unittest.TestCase):
    def test_declared_tools_cover_the_capabilities_the_body_claims(self) -> None:
        problems: List[str] = []
        for agent in _load_agents():
            tools = set(agent.tools)

            if "edit" not in tools:
                claim = _claims(agent.body, _WRITES_FILES_RE)
                if claim:
                    problems.append(
                        f"{agent.rel_path}: body claims it writes files "
                        f"({claim!r}) but `tools:` omits `edit` -- it can never "
                        f"produce that output"
                    )

            if "execute" not in tools:
                claim = _claims(agent.body, _RUNS_COMMANDS_RE)
                if claim:
                    problems.append(
                        f"{agent.rel_path}: body claims it runs commands "
                        f"({claim!r}) but `tools:` omits `execute`"
                    )

            if "agent" not in tools:
                if agent.subagents:
                    problems.append(
                        f"{agent.rel_path}: frontmatter `agents:` declares a "
                        f"roster ({', '.join(agent.subagents)}) but `tools:` "
                        f"omits `agent` -- it cannot spawn them"
                    )
                else:
                    claim = _claims(agent.body, _SPAWNS_AGENTS_RE)
                    if claim:
                        problems.append(
                            f"{agent.rel_path}: body claims it spawns agents "
                            f"({claim!r}) but `tools:` omits `agent`"
                        )

        self.assertFalse(problems, _fail_report("Capability/claim mismatches:", problems))


# --------------------------------------------------------------------------
# Check 4: frontmatter shape
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
# Check 5: applyTo globs resolve
# --------------------------------------------------------------------------


class ApplyToTests(unittest.TestCase):
    def test_every_instruction_declares_a_non_empty_apply_to(self) -> None:
        problems = [
            f"{_rel(doc.path)}: `applyTo:` is missing or empty -- the file is "
            f"inlined into nothing and silently has no effect"
            for doc in mod.load_instruction_docs()
            if not doc.apply_to_patterns
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
# Check 6: no large duplicated blocks
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
