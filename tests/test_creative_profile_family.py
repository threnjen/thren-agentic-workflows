"""Structural guards over the creative writing family.

Everything here derives its coverage from disk. None of it enumerates the
creative assets by name, because an enumerated list stops covering the thing it
protects the moment someone adds a file and forgets the list -- which is the
exact failure these guards exist to catch. Adding a `creative-*` skill without
allow-listing it must fail a test, not pass one that was never updated.

No check matches against agent prose beyond the one literal token the allow-list
is made of. See `tests/test_agent_corpus_invariants.py` for why.
"""

import json
import os
import re
import subprocess
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

# A shell is a write surface the tool mapping does not label as one. Only the
# vault-sync probe holds it, and only for read-only git. The canon guard hook is
# what keeps that from being a hole; this list keeps it from quietly growing.
SHELL_EXEMPT_AGENTS = frozenset({"creative-vault-sync"})

CANON_GUARD = REPO_ROOT / "source_of_truth" / "hooks" / "creative-canon-guard.py"


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


class CanonGuardHookTests(unittest.TestCase):
    """The hook that makes the canon boundary an enforcement, not a promise.

    These run the hook as the harness runs it: JSON on stdin, exit code out.
    Asserting on its source text would pass against a hook that denies nothing.
    """

    @staticmethod
    def _run(payload: dict) -> int:
        result = subprocess.run(
            [sys.executable, str(CANON_GUARD)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
        )
        return result.returncode

    def test_the_hook_exists_and_is_executable(self) -> None:
        self.assertTrue(CANON_GUARD.is_file(), f"{CANON_GUARD} is missing")
        self.assertTrue(os.access(CANON_GUARD, os.X_OK), "canon guard is not executable")

    def test_a_write_into_canon_is_denied(self) -> None:
        for tool, key in (("Write", "file_path"), ("Edit", "file_path")):
            for target in (
                "/vault/canon/world/politics.md",
                "/vault/drafts/ch01.md",
                "canon/characters/mira.md",
                "../vault/canon/notes.md",
            ):
                with self.subTest(tool=tool, target=target):
                    self.assertEqual(
                        2, self._run({"tool_name": tool, "tool_input": {key: target}})
                    )

    def test_a_write_outside_the_prose_is_allowed(self) -> None:
        for target in (
            "/vault/_editor-notes/context/index.md",
            "/vault/scene-summaries/ch01.md",
            "/vault/_editor-notes/session-logs/2026-08-20.md",
        ):
            with self.subTest(target=target):
                self.assertEqual(
                    0, self._run({"tool_name": "Write", "tool_input": {"file_path": target}})
                )

    def test_a_shell_command_that_can_modify_prose_is_denied(self) -> None:
        for command in (
            "echo hi > /vault/canon/world.md",
            "rm -rf /vault/drafts/",
            "sed -i '' 's/a/b/' /vault/canon/world.md",
            "cp /tmp/x.md /vault/canon/x.md",
            "git -C /vault checkout -- canon/world.md",
            "tee /vault/canon/world.md < /tmp/x",
        ):
            with self.subTest(command=command):
                self.assertEqual(
                    2, self._run({"tool_name": "Bash", "tool_input": {"command": command}})
                )

    def test_reading_the_prose_stays_allowed(self) -> None:
        """The editor cannot do its job without reading the manuscript."""
        for command in (
            "cat /vault/canon/world/politics.md",
            "grep -rn 'Mira' /vault/canon/",
            "ls /vault/drafts/",
            "git -C /vault diff --name-status abc123..HEAD",
            "git -C /vault rev-parse HEAD",
            "rm -rf /tmp/scratch",
        ):
            with self.subTest(command=command):
                self.assertEqual(
                    0, self._run({"tool_name": "Bash", "tool_input": {"command": command}})
                )

    def test_the_hook_fails_closed_on_an_unreadable_payload(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CANON_GUARD)],
            input="not json",
            capture_output=True,
            text=True,
        )
        self.assertEqual(2, result.returncode)


class VaultSyncShellTests(unittest.TestCase):
    def test_only_the_sync_probe_holds_a_shell(self) -> None:
        for agent in _creative_agents():
            stem = Path(agent.rel_path).name.replace(".agent.md", "")
            with self.subTest(agent=stem):
                if stem in SHELL_EXEMPT_AGENTS:
                    continue
                self.assertNotIn(
                    "execute",
                    agent.tools,
                    f"{stem} holds a shell; only {sorted(SHELL_EXEMPT_AGENTS)} may",
                )

    def test_the_shell_exemption_names_a_real_agent(self) -> None:
        stems = {Path(a.rel_path).name.replace(".agent.md", "") for a in _creative_agents()}
        self.assertLessEqual(SHELL_EXEMPT_AGENTS, stems)

    def test_the_sync_probe_cannot_edit(self) -> None:
        """A shell plus an edit grant would be the write surface twice over."""
        for agent in _creative_agents():
            stem = Path(agent.rel_path).name.replace(".agent.md", "")
            if stem not in SHELL_EXEMPT_AGENTS:
                continue
            with self.subTest(agent=stem):
                self.assertFalse(WRITE_TOOLS & set(agent.tools))


if __name__ == "__main__":
    unittest.main()
