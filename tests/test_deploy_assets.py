"""deploy_assets: ports/ -> real harness config dirs, marker-ownership safety."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))  # deploy_agents.py lives at the repo root

import asset_paths
import deploy_agents as mod

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
            },
            "codex": {
                home / ".codex" / "agents",
                home / ".agents" / "skills",
            },
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

    def test_github_harness_targets_the_repo_dot_github(self) -> None:
        self.assertIn("github", mod.HARNESSES)
        mappings = mod.harness_mappings("github", home=Path("/home/fixture"), environ={})
        for source, dest in mappings:
            self.assertEqual(source.parts[-3], "ports")
            self.assertEqual(source.parts[-2], "github")
            self.assertEqual(dest.parent, mod.REPO_ROOT / ".github")


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
        self.assertEqual(second, {"copied": 0, "pruned": 0, "skipped_unmanaged": 0})  # no skipped_paths key when clean
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

    def test_repo_linked_destination_root_is_replaced_with_real_dir(self) -> None:
        """Pre-split deployments symlinked dest roots into the repo; deploy heals them."""
        fake_repo = self.root / "repo"
        (fake_repo / "old" / "agents").mkdir(parents=True)
        with mock.patch.object(mod, "REPO_ROOT", fake_repo):
            self._write_port_file("opencode/agents/keeper.md", self._marked())
            agents_root = self.home / ".config" / "opencode" / "agents"
            agents_root.parent.mkdir(parents=True)
            agents_root.symlink_to(fake_repo / "old" / "agents")

            result = mod.deploy_harness("opencode", home=self.home, environ={})

        self.assertFalse(agents_root.is_symlink(), "repo link must be replaced")
        self.assertTrue((agents_root / "keeper.md").is_file())
        self.assertEqual(result["copied"], 1)

    def test_foreign_symlinked_destination_root_is_left_alone(self) -> None:
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        self._write_port_file("opencode/agents/keeper.md", self._marked())
        agents_root = self.home / ".config" / "opencode" / "agents"
        agents_root.parent.mkdir(parents=True)
        agents_root.symlink_to(elsewhere)

        result = mod.deploy_harness("opencode", home=self.home, environ={})

        self.assertTrue(agents_root.is_symlink(), "foreign symlink must survive")
        self.assertFalse((elsewhere / "keeper.md").exists())
        self.assertGreaterEqual(result["skipped_unmanaged"], 1)

    def test_github_mirror_deploys_unmarked_files_and_prunes_stale(self) -> None:
        fake_repo = self.root / "repo"
        fake_repo.mkdir()
        with mock.patch.object(mod, "REPO_ROOT", fake_repo):
            self._write_port_file("github/agents/keeper.agent.md", "no marker at all\n")
            stale = fake_repo / ".github" / "agents" / "gone.agent.md"
            stale.parent.mkdir(parents=True)
            stale.write_text("stale copy, also unmarked\n", encoding="utf-8")
            workflows = fake_repo / ".github" / "workflows"
            workflows.mkdir()
            (workflows / "ci.yml").write_text("on: push\n", encoding="utf-8")

            result = mod.deploy_harness("github", home=self.home, environ={})

            deployed = fake_repo / ".github" / "agents" / "keeper.agent.md"
            self.assertEqual(deployed.read_text(encoding="utf-8"), "no marker at all\n")
            self.assertFalse(stale.exists(), "stale mirror file must be pruned")
            self.assertTrue((workflows / "ci.yml").exists(), "non-mirrored subdir touched")
            self.assertEqual(result["copied"], 1)
            self.assertEqual(result["pruned"], 1)

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


class EnsureCodeReviewGraphTests(unittest.TestCase):
    def test_present_binary_makes_no_subprocess_calls(self) -> None:
        with mock.patch.object(mod.shutil, "which", return_value="/usr/bin/code-review-graph"), \
                mock.patch.object(mod.subprocess, "run") as run:
            result = mod.ensure_code_review_graph()
        self.assertEqual(result, {"status": "already-installed"})
        run.assert_not_called()

    def test_missing_binary_installs_and_configures(self) -> None:
        # which: absent pre-install, pip present, present post-install
        which_results = iter([None, "/usr/bin/pip", "/usr/bin/code-review-graph"])
        with mock.patch.object(mod.shutil, "which", side_effect=lambda _n: next(which_results)), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
            result = mod.ensure_code_review_graph()
        self.assertEqual(result["status"], "installed-and-configured")
        commands = [call.args[0] for call in run.call_args_list]
        self.assertIn(("pip", "install", "code-review-graph"), commands)
        self.assertIn(["code-review-graph", "install"], commands)

    def test_install_failure_is_reported_not_raised(self) -> None:
        which_results = iter([None, "/usr/bin/pip", None, None])
        with mock.patch.object(mod.shutil, "which", side_effect=lambda _n: next(which_results, None)), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=1)):
            result = mod.ensure_code_review_graph()
        self.assertEqual(result["status"], "install-failed")

    def test_deploy_proceeds_when_tool_bootstrap_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod, "CONFIG_PATH", Path(tmp) / "config.json"), \
                mock.patch.object(mod.sys, "argv", ["deploy_agents.py", "--harness", "claude", "--no-save"]), \
                mock.patch.object(
                    mod, "ensure_external_tools",
                    return_value={"code_review_graph": {"status": "install-failed"}},
                ), \
                mock.patch.object(mod, "deploy", return_value={}) as deployed:
            self.assertEqual(mod.main(), 0)
        deployed.assert_called_once()

    def test_skip_tools_flag_bypasses_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod, "CONFIG_PATH", Path(tmp) / "config.json"), \
                mock.patch.object(
                    mod.sys, "argv",
                    ["deploy_agents.py", "--harness", "claude", "--no-save", "--skip-tools"],
                ), \
                mock.patch.object(mod, "ensure_external_tools") as tools, \
                mock.patch.object(mod, "deploy", return_value={}):
            self.assertEqual(mod.main(), 0)
        tools.assert_not_called()


class ExternalToolReportingTests(unittest.TestCase):
    def test_unexpected_exception_becomes_a_status_not_a_crash(self) -> None:
        with mock.patch.object(mod, "ensure_code_review_graph", side_effect=OSError("boom")), \
                mock.patch.object(mod, "ensure_context7", return_value={"status": "already-configured"}):
            results = mod.ensure_external_tools()
        self.assertEqual(results["code-review-graph"]["status"], "install-failed")
        self.assertIn("boom", results["code-review-graph"]["detail"])
        self.assertEqual(results["context7"]["status"], "already-configured")

    def test_failure_report_names_the_tool_and_reason(self) -> None:
        import io
        err = io.StringIO()
        with mock.patch.object(mod.sys, "stderr", err):
            mod.report_external_tools(
                {"context7": {"status": "install-failed", "detail": "npx not on PATH (Node.js required)"}}
            )
        output = err.getvalue()
        self.assertIn("context7", output)
        self.assertIn("npx not on PATH (Node.js required)", output)
        self.assertIn("deployment is unaffected", output)


class EnsureContext7Tests(unittest.TestCase):
    def test_existing_config_makes_no_subprocess_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".claude.json").write_text('{"mcpServers": {"context7": {}}}', encoding="utf-8")
            with mock.patch.object(mod.subprocess, "run") as run:
                result = mod.ensure_context7(home=Path(tmp))
        self.assertEqual(result, {"status": "already-configured"})
        run.assert_not_called()

    def test_missing_config_runs_ctx7_setup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod.shutil, "which", return_value="/usr/bin/npx"), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
            result = mod.ensure_context7(home=Path(tmp))
        self.assertEqual(result["status"], "installed-and-configured")
        self.assertEqual(run.call_args.args[0], ["npx", "ctx7", "setup"])

    def test_missing_npx_is_reported_not_raised(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod.shutil, "which", return_value=None):
            result = mod.ensure_context7(home=Path(tmp))
        self.assertEqual(result["status"], "install-failed")


class BaselineDeployTests(unittest.TestCase):
    def test_destinations_per_harness(self) -> None:
        home = Path("/home/fixture")
        self.assertEqual(
            mod.baseline_destination("claude", home=home, environ={}),
            home / ".claude" / "CLAUDE.md",
        )
        self.assertEqual(
            mod.baseline_destination("codex", home=home, environ={}),
            home / ".codex" / "AGENTS.md",
        )
        self.assertEqual(
            mod.baseline_destination("opencode", home=home, environ={}),
            home / ".config" / "opencode" / "AGENTS.md",
        )
        self.assertEqual(
            mod.baseline_destination("cursor", home=home, environ={}),
            home / ".cursor" / "rules" / "baseline-instructions.mdc",
        )
        self.assertEqual(
            mod.baseline_destination("github", home=home, environ={}),
            mod.REPO_ROOT / ".github" / "copilot-instructions.md",
        )
        self.assertEqual(
            mod.baseline_destination("codex", home=home, environ={"CODEX_HOME": "/opt/codex"}),
            Path("/opt/codex/AGENTS.md"),
        )

    def test_creates_file_with_all_sections_and_real_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = mod.deploy_baseline("codex", home=home, environ={})
            self.assertEqual(result["status"], "created")
            content = (home / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
        for name in mod.BASELINE_SECTIONS:
            self.assertIn(f"<!-- {name} -->", content)
        self.assertIn("asks Codex to act as a named agent", content)
        self.assertIn(str(home / ".codex" / "agents"), content)
        self.assertIn(str(home / ".agents" / "skills"), content)
        self.assertNotIn("{harness_title}", content)
        self.assertNotIn("{agent_paths}", content)

    def test_splice_preserves_foreign_content_and_updates_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            dest = home / ".codex" / "AGENTS.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "# My own notes\n\n<!-- context7 -->\nstale content\n<!-- context7 -->\n\nTrailing custom text.\n",
                encoding="utf-8",
            )
            result = mod.deploy_baseline("codex", home=home, environ={})
            self.assertEqual(result["status"], "updated")
            content = dest.read_text(encoding="utf-8")
        self.assertIn("# My own notes", content)
        self.assertIn("Trailing custom text.", content)
        self.assertNotIn("stale content", content)
        self.assertIn("resolve-library-id", content)
        self.assertIn("<!-- code-review-graph -->", content)

    def test_second_run_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(mod.deploy_baseline("claude", home=home, environ={})["status"], "created")
            self.assertEqual(mod.deploy_baseline("claude", home=home, environ={})["status"], "unchanged")

    def test_cursor_baseline_gets_rule_frontmatter_and_survives_prune(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = mod.deploy_baseline("cursor", home=home, environ={})
            self.assertEqual(result["status"], "created")
            dest = home / ".cursor" / "rules" / "baseline-instructions.mdc"
            content = dest.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\nalwaysApply: true\n---\n"))
            # The rules dir is a pruned deploy target; the unmarked baseline
            # rule must be treated as foreign and left alone.
            mod.deploy_harness("cursor", home=home, environ={})
            self.assertTrue(dest.is_file())

    def test_github_baseline_is_repo_scoped_copilot_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod, "REPO_ROOT", Path(tmp)):
            result = mod.deploy_baseline("github", home=Path(tmp) / "unused-home", environ={})
            self.assertEqual(result["status"], "created")
            content = (Path(tmp) / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        self.assertIn("asks Copilot to act as a named agent", content)
        self.assertIn("`.github/agents/`", content)
        self.assertIn("`.github/skills/`", content)
        self.assertNotIn(tmp, content)  # repo-relative, no machine paths baked in

    def test_symlink_destination_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()
            real = home / "real.md"
            real.write_text("hands off\n", encoding="utf-8")
            (home / ".codex" / "AGENTS.md").symlink_to(real)
            result = mod.deploy_baseline("codex", home=home, environ={})
            self.assertEqual(result["status"], "skipped")
            self.assertEqual(real.read_text(encoding="utf-8"), "hands off\n")


if __name__ == "__main__":
    unittest.main()
