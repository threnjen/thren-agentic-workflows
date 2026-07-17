"""deploy_assets: ports/ -> real harness config dirs, marker-ownership safety."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import asset_paths
import deploy_assets as mod

MARKER = asset_paths.GENERATED_AGENT_MARKDOWN_HEADER
SKILL_MARKER = asset_paths.GENERATED_SKILL_HEADER.strip("\n")


class HarnessMappingTests(unittest.TestCase):
    def test_default_destinations_per_harness(self) -> None:
        home = Path("/home/fixture")
        expected = {
            "claude": {
                home / ".claude" / "agents",
                home / ".claude" / "commands",
                home / ".claude" / "skills",
                home / ".claude" / "learnings",
            },
            "codex": {home / ".codex" / "agents", home / ".agents" / "skills"},
            "opencode": {
                home / ".config" / "opencode" / "agents",
                home / ".config" / "opencode" / "skills",
            },
            "cursor": {home / ".cursor" / "commands", home / ".cursor" / "rules"},
        }
        for harness, destinations in expected.items():
            with self.subTest(harness=harness):
                mappings = mod.harness_mappings(harness, home=home, environ={})
                self.assertEqual({dest for _, dest in mappings}, destinations)
                for source, _ in mappings:
                    self.assertEqual(source.parts[-3], "ports")
                    self.assertEqual(source.parts[-2], harness)

    def test_env_overrides_relocate_roots(self) -> None:
        home = Path("/home/fixture")
        environ = {
            "CLAUDE_CONFIG_DIR": "/opt/claude",
            "CODEX_HOME": "/opt/codex",
            "OPENCODE_CONFIG_DIR": "/opt/opencode",
        }
        claude = {dest for _, dest in mod.harness_mappings("claude", home=home, environ=environ)}
        self.assertIn(Path("/opt/claude/agents"), claude)
        codex = {dest for _, dest in mod.harness_mappings("codex", home=home, environ=environ)}
        self.assertIn(Path("/opt/codex/agents"), codex)
        # codex skills stay home-rooted regardless of CODEX_HOME
        self.assertIn(home / ".agents" / "skills", codex)
        opencode = {dest for _, dest in mod.harness_mappings("opencode", home=home, environ=environ)}
        self.assertIn(Path("/opt/opencode/agents"), opencode)

    def test_unknown_harness_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            mod.harness_mappings("emacs", home=Path("/home/fixture"), environ={})

    def test_github_port_is_not_a_deployable_harness(self) -> None:
        self.assertNotIn("github", mod.HARNESSES)


class DeployTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.ports = self.root / "ports"
        patcher = mock.patch.object(mod, "PORTS_DIR", self.ports)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _write_port_file(self, rel: str, text: str) -> Path:
        path = self.ports / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _marked(self, body: str = "body\n") -> str:
        return f"{MARKER}\n{body}"

    def test_deploy_copies_and_is_idempotent(self) -> None:
        self._write_port_file("cursor/commands/captain.md", self._marked())
        self._write_port_file("cursor/rules/style.mdc", self._marked())

        first = mod.deploy_harness("cursor", home=self.home, environ={})
        second = mod.deploy_harness("cursor", home=self.home, environ={})

        self.assertEqual(first["copied"], 2)
        self.assertEqual(second, {"copied": 0, "pruned": 0, "skipped_unmanaged": 0})
        self.assertTrue((self.home / ".cursor" / "commands" / "captain.md").is_file())

    def test_owned_stale_copy_is_pruned_but_unmarked_file_survives(self) -> None:
        self._write_port_file("claude/agents/keeper.md", self._marked())
        agents = self.home / ".claude" / "agents"
        agents.mkdir(parents=True)
        stale = agents / "z-stale.md"
        stale.write_text(self._marked("old generated file\n"), encoding="utf-8")
        foreign = agents / "my-notes.md"
        foreign.write_text("hand-written notes\n", encoding="utf-8")

        result = mod.deploy_harness("claude", home=self.home, environ={})

        self.assertFalse(stale.exists(), "owned stale copy must be pruned")
        self.assertTrue(foreign.exists(), "unmarked file must never be pruned")
        self.assertEqual(result["pruned"], 1)

    def test_unmarked_destination_is_never_overwritten(self) -> None:
        self._write_port_file("claude/agents/keeper.md", self._marked("new content\n"))
        agents = self.home / ".claude" / "agents"
        agents.mkdir(parents=True)
        target = agents / "keeper.md"
        target.write_text("user-customized, no marker\n", encoding="utf-8")

        result = mod.deploy_harness("claude", home=self.home, environ={})

        self.assertEqual(target.read_text(encoding="utf-8"), "user-customized, no marker\n")
        self.assertEqual(result["skipped_unmanaged"], 1)

    def test_quoted_marker_in_body_does_not_prove_ownership(self) -> None:
        self._write_port_file("claude/agents/keeper.md", self._marked())
        agents = self.home / ".claude" / "agents"
        agents.mkdir(parents=True)
        readme = agents / "README.md"
        readme.write_text(
            f"# Docs\n\nGenerated files carry:\n\n```\n{MARKER}\n```\n",
            encoding="utf-8",
        )

        mod.deploy_harness("claude", home=self.home, environ={})

        self.assertTrue(readme.exists(), "a doc quoting the marker was deleted")

    def test_skill_aux_files_are_owned_via_marked_skill_md(self) -> None:
        self._write_port_file(
            "claude/skills/demo/SKILL.md", f"---\nname: demo\n---\n{SKILL_MARKER}\n# Demo\n"
        )
        self._write_port_file("claude/skills/demo/helper.py", "print('v1')\n")
        mod.deploy_harness("claude", home=self.home, environ={})

        helper = self.home / ".claude" / "skills" / "demo" / "helper.py"
        self.assertEqual(helper.read_text(encoding="utf-8"), "print('v1')\n")

        # Update the aux file upstream: unmarked, but inside a marked skill dir.
        self._write_port_file("claude/skills/demo/helper.py", "print('v2')\n")
        result = mod.deploy_harness("claude", home=self.home, environ={})
        self.assertEqual(helper.read_text(encoding="utf-8"), "print('v2')\n")
        self.assertEqual(result["skipped_unmanaged"], 0)

        # Remove the skill upstream: the whole deployed dir is pruned.
        import shutil

        shutil.rmtree(self.ports / "claude" / "skills" / "demo")
        mod.deploy_harness("claude", home=self.home, environ={})
        self.assertFalse((self.home / ".claude" / "skills" / "demo").exists())

    def test_symlinked_destination_is_skipped(self) -> None:
        self._write_port_file("claude/agents/keeper.md", self._marked("new\n"))
        agents = self.home / ".claude" / "agents"
        agents.mkdir(parents=True)
        outside = self.root / "outside.md"
        outside.write_text("real file\n", encoding="utf-8")
        (agents / "keeper.md").symlink_to(outside)

        result = mod.deploy_harness("claude", home=self.home, environ={})

        self.assertEqual(outside.read_text(encoding="utf-8"), "real file\n")
        self.assertEqual(result["skipped_unmanaged"], 1)


class ConfigAndCliTests(unittest.TestCase):
    def test_config_round_trip_filters_unknown_harnesses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            mod.save_config(["claude", "cursor"], path=config)
            self.assertEqual(mod.load_config(config), ["claude", "cursor"])

            config.write_text(json.dumps({"harnesses": ["claude", "emacs"]}), encoding="utf-8")
            self.assertEqual(mod.load_config(config), ["claude"])

    def test_missing_or_malformed_config_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(mod.load_config(Path(tmp) / "absent.json"), [])
            bad = Path(tmp) / "bad.json"
            bad.write_text("not json", encoding="utf-8")
            self.assertEqual(mod.load_config(bad), [])

    def test_parse_harness_arg(self) -> None:
        self.assertEqual(mod.parse_harness_arg("claude,cursor"), ["claude", "cursor"])
        with self.assertRaises(ValueError):
            mod.parse_harness_arg("claude,emacs")

    def test_non_tty_without_config_or_flag_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod, "CONFIG_PATH", Path(tmp) / "config.json"), \
                mock.patch.object(mod.sys, "argv", ["deploy_assets.py"]), \
                mock.patch.object(mod.sys.stdin, "isatty", return_value=False):
            with self.assertRaises(SystemExit) as raised:
                mod.main()
            self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
