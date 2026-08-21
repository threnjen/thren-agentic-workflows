"""Structural guards over the creative writing family.

Everything here derives its coverage from disk. None of it enumerates the
creative assets by name, because an enumerated list stops covering the thing it
protects the moment someone adds a file and forgets the list -- which is the
exact failure these guards exist to catch. Adding a `creative-*` skill without
allow-listing it must fail a test, not pass one that was never updated.

No check matches against agent prose beyond the one literal token the allow-list
is made of. See `tests/test_agent_corpus_invariants.py` for why.
"""

import re
import sys
import unittest
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod  # noqa: E402

SOT_DIR = REPO_ROOT / "source_of_truth"
AGENTS_DIR = SOT_DIR / "agents"
SKILLS_DIR = SOT_DIR / "skills"
PROFILE_INSTRUCTION = SOT_DIR / "instructions" / "creative-profile.instructions.md"

WRITE_TOOLS = frozenset({"edit", "write"})
# The scribe is the family's single write surface. Adding a second one is a
# design change, not a slip, so it belongs here and not in a blanket allowance.
WRITE_EXEMPT_AGENTS = frozenset({"creative-scribe"})


def _creative_agents() -> List[mod.SourceAgent]:
    return [a for a in mod.load_source_agents() if a.profile == mod.CREATIVE_PROFILE]


def _creative_skill_names() -> List[str]:
    return sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and p.name.startswith("creative-"))


class CreativeFamilyShapeTests(unittest.TestCase):
    def test_the_family_is_not_empty(self) -> None:
        """Every other guard here is vacuous over an empty corpus."""
        self.assertTrue(_creative_agents(), "no agent carries profile: creative")
        self.assertTrue(_creative_skill_names(), "no creative-* skill on disk")

    def test_creative_agents_use_the_creative_filename_prefix(self) -> None:
        """The profile instruction's applyTo glob keys off the prefix.

        An agent marked `profile: creative` under some other filename would be
        cut off from every technical instruction and receive no creative one --
        isolated into an empty context rather than into its own.
        """
        for agent in _creative_agents():
            with self.subTest(agent=agent.rel_path):
                self.assertTrue(
                    Path(agent.rel_path).name.startswith("creative-"),
                    f"{agent.rel_path} is profile: creative but lacks the creative- prefix",
                )

    def test_the_creative_prefix_implies_the_creative_profile(self) -> None:
        """The converse: a creative-named agent must not be technical.

        Without this, forgetting `profile: creative` silently inlines the whole
        engineering corpus into a writing agent.
        """
        for path in sorted(AGENTS_DIR.glob("creative-*.md")):
            agent = next(a for a in mod.load_source_agents() if Path(a.rel_path).name == path.name)
            with self.subTest(agent=path.name):
                self.assertEqual(mod.CREATIVE_PROFILE, agent.profile)

    def test_only_the_scribe_can_write(self) -> None:
        for agent in _creative_agents():
            stem = Path(agent.rel_path).name.replace(".agent.md", "")
            granted = WRITE_TOOLS & {t.lower() for t in agent.tools}
            with self.subTest(agent=stem):
                if stem in WRITE_EXEMPT_AGENTS:
                    self.assertTrue(granted, f"{stem} is the designated write surface but has no write tool")
                else:
                    self.assertFalse(granted, f"{stem} must not hold {sorted(granted)}")

    def test_the_scribe_exemption_names_a_real_agent(self) -> None:
        """An exemption for a deleted agent silently widens nothing forever."""
        stems = {Path(a.rel_path).name.replace(".agent.md", "") for a in _creative_agents()}
        self.assertLessEqual(WRITE_EXEMPT_AGENTS, stems)


class CreativeInstructionTests(unittest.TestCase):
    def _profile_doc(self) -> mod.InstructionDoc:
        return next(
            d for d in mod.load_instruction_docs() if d.path.name == PROFILE_INSTRUCTION.name
        )

    def test_the_profile_instruction_is_itself_creative(self) -> None:
        self.assertEqual(mod.CREATIVE_PROFILE, self._profile_doc().profile)

    def test_the_profile_instruction_reaches_every_creative_agent(self) -> None:
        doc = self._profile_doc()
        for agent in _creative_agents():
            with self.subTest(agent=agent.rel_path):
                self.assertIn(doc, mod.applicable_instructions(agent, [doc]))

    def test_no_technical_instruction_reaches_a_creative_agent(self) -> None:
        docs = mod.load_instruction_docs()
        technical = [d for d in docs if d.profile == mod.DEFAULT_PROFILE]
        self.assertTrue(technical, "no technical instruction on disk; this guard is inert")
        for agent in _creative_agents():
            leaked = [
                d.path.name for d in mod.applicable_instructions(agent, technical)
            ]
            with self.subTest(agent=agent.rel_path):
                self.assertEqual([], leaked)

    def test_no_creative_instruction_reaches_a_technical_agent(self) -> None:
        docs = mod.load_instruction_docs()
        creative = [d for d in docs if d.profile == mod.CREATIVE_PROFILE]
        self.assertTrue(creative, "no creative instruction on disk; this guard is inert")
        for agent in mod.load_source_agents():
            if agent.profile != mod.DEFAULT_PROFILE:
                continue
            leaked = [d.path.name for d in mod.applicable_instructions(agent, creative)]
            with self.subTest(agent=agent.rel_path):
                self.assertEqual([], leaked)

    def test_the_allow_list_covers_every_creative_skill_on_disk(self) -> None:
        """Derived, not enumerated: adding a skill without listing it fails here."""
        text = PROFILE_INSTRUCTION.read_text(encoding="utf-8")
        listed = set(re.findall(r"`(creative-[a-z0-9-]+)`", text))
        on_disk = set(_creative_skill_names())
        self.assertEqual(
            set(),
            on_disk - listed,
            msg=f"skills on disk but not allow-listed: {sorted(on_disk - listed)}",
        )
        self.assertEqual(
            set(),
            listed - on_disk,
            msg=f"allow-listed but not on disk: {sorted(listed - on_disk)}",
        )

    def test_the_allow_list_assertion_can_fail(self) -> None:
        """Mutation check for the guard above.

        The allow-list is prose. If the extraction regex stopped matching, the
        check would pass over an empty set forever.
        """
        text = PROFILE_INSTRUCTION.read_text(encoding="utf-8")
        listed = set(re.findall(r"`(creative-[a-z0-9-]+)`", text))
        self.assertTrue(listed, "extracted no skill names; the allow-list guard is inert")
        mutated = text.replace("`creative-modes`", "`creative-modez`", 1)
        self.assertNotEqual(text, mutated, "mutation target absent; guard cannot be verified")
        mutated_listed = set(re.findall(r"`(creative-[a-z0-9-]+)`", mutated))
        self.assertIn("creative-modez", mutated_listed)
        self.assertTrue(
            mutated_listed - set(_creative_skill_names()),
            "a renamed skill did not surface as an allow-list mismatch",
        )


class CreativeSkillTests(unittest.TestCase):
    def test_every_creative_skill_declares_the_creative_profile(self) -> None:
        for name in _creative_skill_names():
            frontmatter = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertRegex(frontmatter, r"(?m)^profile:\s*creative\s*$")


if __name__ == "__main__":
    unittest.main()
