"""deploy_assets: ports/ -> real harness config dirs, marker-ownership safety."""

import contextlib
import io
import json
import re
import shlex
import subprocess
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
            "cursor": {
                home / ".cursor" / "agents",
                home / ".cursor" / "commands",
                home / ".cursor" / "rules",
                home / ".cursor" / "skills",
            },
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
        self._write_port_file("cursor/agents/z-hidden.md", self._marked())
        self._write_port_file("cursor/skills/tidy-up/SKILL.md", self._marked())

        first = mod.deploy_harness("cursor", home=self.home, environ={})
        second = mod.deploy_harness("cursor", home=self.home, environ={})

        self.assertEqual(first["copied"], 4)
        self.assertEqual(second, {"copied": 0, "pruned": 0, "skipped_unmanaged": 0})  # no skipped_paths key when clean
        self.assertTrue((self.home / ".cursor" / "commands" / "captain.md").is_file())
        self.assertTrue((self.home / ".cursor" / "agents" / "z-hidden.md").is_file())
        self.assertTrue((self.home / ".cursor" / "skills" / "tidy-up" / "SKILL.md").is_file())

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
    def test_profile_config_is_backward_compatible_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            config.write_text(json.dumps({"harnesses": ["claude"]}), encoding="utf-8")
            self.assertFalse(mod.load_comms_profile(config))
            config.write_text(
                json.dumps({"harnesses": ["claude"], "comms_profile": True}),
                encoding="utf-8",
            )
            self.assertTrue(mod.load_comms_profile(config))
            for invalid in ("true", 1, [], {"enabled": True}, None):
                config.write_text(
                    json.dumps({"harnesses": ["claude"], "comms_profile": invalid}),
                    encoding="utf-8",
                )
                with self.subTest(invalid=invalid):
                    self.assertFalse(mod.load_comms_profile(config))

    def test_save_config_persists_the_profile_without_changing_harnesses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            mod.save_config(["claude", "opencode"], config, comms_profile=True)
            self.assertEqual(mod.load_config(config), ["claude", "opencode"])
            self.assertTrue(mod.load_comms_profile(config))

    def test_load_config_state_reads_and_normalizes_one_document(self) -> None:
        with mock.patch.object(
            mod,
            "_read_config_data",
            return_value={"harnesses": ["claude"], "comms_profile": True},
        ) as read:
            state = mod.load_config_state(Path("unused.json"))
        self.assertEqual(state, mod.DeployConfig(["claude"], True))
        read.assert_called_once_with(Path("unused.json"))

    def test_save_config_normalizes_invalid_profile_values_to_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            mod.save_config(["claude"], config, comms_profile="true")
            saved = json.loads(config.read_text(encoding="utf-8"))
        self.assertIs(saved[mod.COMMS_PROFILE_KEY], False)

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

    def test_main_passes_saved_profile_to_watch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            config.write_text(
                json.dumps({"harnesses": ["claude"], "comms_profile": True}),
                encoding="utf-8",
            )
            with mock.patch.object(mod, "CONFIG_PATH", config), \
                    mock.patch.object(
                        mod.sys, "argv", ["deploy_agents.py", "--watch", "--skip-tools"]
                    ), \
                    mock.patch.object(mod, "watch") as watch:
                self.assertEqual(mod.main(), 0)
        watch.assert_called_once_with(["claude"], comms_profile=True)


class WatchTests(unittest.TestCase):
    def test_watch_keeps_profile_for_initial_and_changed_deploys(self) -> None:
        callbacks = []
        deployments = []

        def capture_poll(_directories, callback):
            callbacks.append(callback)

        def capture_deploy(harnesses, **kwargs):
            deployments.append((harnesses, kwargs))

        with mock.patch.object(mod, "deploy", side_effect=capture_deploy), \
                mock.patch.object(mod, "poll_watch", side_effect=capture_poll):
            mod.watch(["claude"], comms_profile=True)
            callbacks[0](["changed.md"])

        self.assertEqual(
            deployments,
            [
                (["claude"], {"comms_profile": True}),
                (["claude"], {"comms_profile": True}),
            ],
        )


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
            result = mod.ensure_code_review_graph(["claude"])
        self.assertEqual(result["status"], "installed-and-configured")
        commands = [call.args[0] for call in run.call_args_list]
        self.assertIn(("pip", "install", "code-review-graph"), commands)
        self.assertIn(
            ["code-review-graph", "install", "-y", "--platform", "claude-code"], commands
        )

    def test_configure_runs_once_per_selected_harness_and_never_for_all(self) -> None:
        """The bare `install` (every detected platform) must never be issued."""
        which_results = iter([None, "/usr/bin/pip", "/usr/bin/code-review-graph"])
        with mock.patch.object(mod.shutil, "which", side_effect=lambda _n: next(which_results)), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
            mod.ensure_code_review_graph(["claude", "cursor", "claude"])
        configures = [
            call.args[0] for call in run.call_args_list
            if list(call.args[0])[:2] == ["code-review-graph", "install"]
        ]
        self.assertEqual(
            configures,
            [
                ["code-review-graph", "install", "-y", "--platform", "claude-code"],
                ["code-review-graph", "install", "-y", "--platform", "cursor"],
            ],
        )

    def test_no_mappable_harness_skips_configuration(self) -> None:
        which_results = iter([None, "/usr/bin/pip", "/usr/bin/code-review-graph"])
        with mock.patch.object(mod.shutil, "which", side_effect=lambda _n: next(which_results)), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
            result = mod.ensure_code_review_graph([])
        self.assertEqual(result["status"], "skipped")
        configures = [
            call.args[0] for call in run.call_args_list
            if list(call.args[0])[:2] == ["code-review-graph", "install"]
        ]
        self.assertEqual(configures, [])

    def test_configure_failure_names_the_platform(self) -> None:
        which_results = iter([None, "/usr/bin/pip", "/usr/bin/code-review-graph"])
        # pip install succeeds; the per-platform configure call fails.
        returncodes = iter([0, 1])
        with mock.patch.object(mod.shutil, "which", side_effect=lambda _n: next(which_results)), \
                mock.patch.object(
                    mod.subprocess, "run",
                    side_effect=lambda *_a, **_k: mock.Mock(returncode=next(returncodes)),
                ):
            result = mod.ensure_code_review_graph(["cursor"])
        self.assertEqual(result["status"], "configure-failed")
        self.assertIn("cursor", result["detail"])

    def test_install_failure_is_reported_not_raised(self) -> None:
        which_results = iter([None, "/usr/bin/pip", None, None])
        with mock.patch.object(mod.shutil, "which", side_effect=lambda _n: next(which_results, None)), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=1)):
            result = mod.ensure_code_review_graph(["claude"])
        self.assertEqual(result["status"], "install-failed")

    def test_main_passes_the_selection_to_the_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod, "CONFIG_PATH", Path(tmp) / "config.json"), \
                mock.patch.object(
                    mod.sys, "argv",
                    ["deploy_agents.py", "--harness", "claude,cursor", "--no-save"],
                ), \
                mock.patch.object(mod, "ensure_external_tools", return_value={}) as tools, \
                mock.patch.object(mod, "deploy", return_value={}):
            self.assertEqual(mod.main(), 0)
        tools.assert_called_once_with(["claude", "cursor"])

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
    def test_registered_mcp_server_makes_no_subprocess_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".claude.json").write_text('{"mcpServers": {"context7": {}}}', encoding="utf-8")
            with mock.patch.object(mod.subprocess, "run") as run:
                result = mod.ensure_context7(home=Path(tmp))
        self.assertEqual(result, {"status": "already-configured"})
        run.assert_not_called()

    def test_cli_mode_rule_file_does_not_count_as_configured(self) -> None:
        """CLI + Skills mode registers no server, so `resolve-library-id` and
        `query-docs` would not exist. It must not satisfy the probe."""
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / ".claude" / "rules"
            rules.mkdir(parents=True)
            (rules / "context7.md").write_text("use ctx7\n", encoding="utf-8")
            self.assertFalse(mod.context7_is_configured(home=Path(tmp)))

    def test_missing_config_runs_ctx7_setup_in_mcp_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod.shutil, "which", return_value="/usr/bin/npx"), \
                mock.patch.object(mod.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
            result = mod.ensure_context7(home=Path(tmp))
        self.assertEqual(result["status"], "installed-and-configured")
        self.assertEqual(
            run.call_args.args[0], ["npx", "ctx7", "setup", "--claude", "--mcp", "-y"]
        )

    def test_missing_npx_is_reported_not_raised(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(mod.shutil, "which", return_value=None):
            result = mod.ensure_context7(home=Path(tmp))
        self.assertEqual(result["status"], "install-failed")


class BaselineDeployTests(unittest.TestCase):
    def test_profile_off_excludes_comms_and_profile_on_includes_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            off = mod.deploy_baseline("codex", home=home, environ={}, comms_enabled=False)
            content = (home / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(off["status"], "created")
            self.assertNotIn("<!-- comms-protocol -->", content)
            on = mod.deploy_baseline("codex", home=home, environ={}, comms_enabled=True)
            content = (home / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(on["status"], "updated")
            self.assertIn("<!-- comms-protocol -->", content)
            self.assertIn("Baseline loaded: 12 sections", content)
            mod.deploy_baseline("codex", home=home, environ={}, comms_enabled=False)
            content = (home / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertNotIn("<!-- comms-protocol -->", content)
        self.assertIn("Baseline loaded: 11 sections", content)

    def test_profile_off_preserves_foreign_bytes_for_each_user_global_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            fake_repo = home / "repo"
            fake_repo.mkdir()
            with mock.patch.object(mod, "REPO_ROOT", fake_repo):
                for harness in ("claude", "codex", "opencode", "cursor", "github"):
                    destination = mod.baseline_destination(harness, home=home, environ={})
                    assert destination is not None
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    foreign = f"foreign {harness}\n\n"
                    destination.write_text(foreign, encoding="utf-8")
                    mod.deploy_baseline(harness, home=home, environ={}, comms_enabled=False)
                    before = destination.read_bytes()
                    mod.deploy_baseline(harness, home=home, environ={}, comms_enabled=True)
                    mod.deploy_baseline(harness, home=home, environ={}, comms_enabled=False)
                    after = destination.read_bytes()
                    with self.subTest(harness=harness):
                        self.assertEqual(after, before)
                        self.assertIn(foreign.encode(), after)

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

    def test_every_listed_name_resolves_to_a_baseline_instruction(self) -> None:
        """Each listed name must be a real instruction file carrying baseline: true.

        The list is the only thing naming what deploys, so a typo or a name whose
        instruction lost its baseline flag would otherwise surface as a deploy
        failure on a user's machine rather than here.
        """
        names = mod.baseline_section_names()
        self.assertTrue(names, "baseline template lists no instructions; deploys are inert")
        for name in names:
            with self.subTest(name=name):
                path = mod.BASELINE_INSTRUCTIONS_DIR / f"{name}.instructions.md"
                self.assertTrue(path.is_file(), f"{name} is listed but {path} does not exist")
                self.assertIn(
                    "baseline: true",
                    path.read_text(encoding="utf-8").split("---")[1],
                    f"{name} deploys to the global file but its frontmatter omits baseline: true",
                )

    def test_every_baseline_instruction_is_listed(self) -> None:
        """A baseline: true instruction that the template omits reaches nobody.

        Propagation refuses to inline any baseline instruction into an agent,
        so the template list is that instruction's only delivery route. An
        unlisted one is silently dropped from every harness.
        """
        listed = set(mod.baseline_section_names())
        unlisted = sorted(
            path.name.replace(".instructions.md", "")
            for path in mod.BASELINE_INSTRUCTIONS_DIR.glob("*.instructions.md")
            if "baseline: true" in path.read_text(encoding="utf-8").split("---")[1]
            and path.name.replace(".instructions.md", "") not in listed
        )
        self.assertEqual(
            [],
            unlisted,
            f"baseline instructions missing from the template list: {unlisted}",
        )

    def test_no_name_is_both_listed_and_retired(self) -> None:
        """A name cannot be listed and retired at once.

        deploy_baseline strips retired sections before splicing listed ones, so
        a name in both lists survives only by loop order. Reordering those two
        loops would silently stop deploying it.
        """
        overlap = set(mod.baseline_section_names()) & set(mod.RETIRED_BASELINE_SECTIONS)
        self.assertFalse(
            overlap,
            f"listed and retired at the same time: {sorted(overlap)}. "
            "Remove the name from RETIRED_BASELINE_SECTIONS -- splicing already "
            "replaces the block a past deploy wrote.",
        )

    def test_rendered_section_drops_frontmatter_and_canary_and_demotes_heading(self) -> None:
        """The instruction body is reshaped for a user-global file.

        A Load Canary left in place would fire in every session, which is the
        opposite of what it proves: that one agent inlined one instruction.
        """
        body = mod._instruction_body("prose-standards")
        self.assertTrue(body.startswith("## Prose Standards"), body[:40])
        self.assertNotIn("applyTo:", body)
        self.assertNotIn("baseline: true", body)
        self.assertNotIn("Load Canary", body)
        self.assertNotIn("Instruction loaded:", body)
        source = (mod.BASELINE_INSTRUCTIONS_DIR / "prose-standards.instructions.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Load Canary", source, "canary removed from the source file, not just the render")

    def test_contract_source_retains_generated_shape(self) -> None:
        """The vendored contract keeps the authority's shape before rendering."""
        path = mod.BASELINE_INSTRUCTIONS_DIR / "comms-protocol.instructions.md"
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        end = text.find("\n---\n", 3)
        self.assertGreaterEqual(end, 0, "contract frontmatter is not closed")
        frontmatter = text[:end]
        self.assertIn("description:", frontmatter)
        self.assertIn("baseline: true", frontmatter)
        body = text[end + len("\n---\n") :]
        lines = body.splitlines()
        self.assertGreaterEqual(len(lines), 4)
        self.assertEqual(lines[0], mod.GENERATED_AGENT_MARKDOWN_HEADER)
        self.assertEqual(lines[1], "# AGENT-RESULT contract")
        self.assertIn("Contract version: 1", lines)
        self.assertNotIn("Load Canary", body)

    def test_contract_is_a_registered_baseline_section(self) -> None:
        self.assertIn("comms-protocol", mod.baseline_section_names())
        self.assertEqual(len(mod.baseline_section_names()), 12)
        body = mod._instruction_body("comms-protocol")
        self.assertTrue(body.startswith("## AGENT-RESULT contract"), body[:80])
        self.assertNotIn(mod.GENERATED_AGENT_MARKDOWN_HEADER, body)
        self.assertNotIn("Load Canary", body)

    def test_quoted_generated_marker_is_not_removed_from_instruction_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "quoted.instructions.md"
            path.write_text(
                "---\nbaseline: true\n---\n\n"
                "# Quoted marker\n\n"
                f"A body example quotes {mod.GENERATED_AGENT_MARKDOWN_HEADER}.\n",
                encoding="utf-8",
            )
            with mock.patch.object(mod, "BASELINE_INSTRUCTIONS_DIR", Path(tmp)):
                body = mod._instruction_body("quoted")
        self.assertIn(mod.GENERATED_AGENT_MARKDOWN_HEADER, body)

    def test_existing_baseline_sections_keep_independent_render_bytes(self) -> None:
        expected_sha256 = {
            "agent-discovery": "639e204062080d795de3e1c85b290394c4a628ea35c87c4eda4a4987b75ccdfc",
            "challenge-assumptions": "55d2a3aaced22ea3c7508ba4dcefd3c562005b0fcb9228715d9eb55f560b8e76",
            "code-change-strategy": "4a48fe5b063d3ed234067473042b10546a0b33bc2c78311b1ca1d111670b8f88",
            "code-review-graph": "c9df3c999e7dd12ecaa3dd666c17f97e291808c22abb1adf9df2cf6bb65b5e1c",
            "codebase-context-bootstrap": "db969d68bc2563af88afdca5b206c30ca1410f8faf024edbdfdb83bb6e84ccc6",
            "language-standards": "e68e8ae7eb868235a1f90ff7fd8b6a532f3a4e297c35eb404cc66dd79c5cc599",
            "learnings-bootstrap": "81d5621047c4baa599709ddfc72cbb95c2b7fd05d3fa046ce4df5543236207fc",
            "output-verbosity-policy": "00a4a46eee283a8c15f96e321502479b5f2954f3793b4f6d95dd71e3cef70b7a",
            "proactive-research": "981a8af41e6b5aa162563e1d5676ef1682b7eaab42aa28c27420d2c773010c55",
            "prose-standards": "40440969ad9ed3b77b9296ac3a955556deac45dedb028694196f67e646f87e9b",
            "question-hygiene": "739d6b2de393d7ea836d455450c64749160e92ae56b1f4100fec756ab55281eb",
        }
        import hashlib

        self.assertEqual(set(expected_sha256), set(mod.baseline_section_names()) - {"comms-protocol"})
        for name, expected in expected_sha256.items():
            with self.subTest(name=name):
                actual = hashlib.sha256(mod._instruction_body(name).encode()).hexdigest()
                self.assertEqual(actual, expected)

    def test_listed_name_without_an_instruction_file_fails_the_deploy(self) -> None:
        """A missing instruction must fail loudly, not deploy a partial baseline."""
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            original = mod.BASELINE_TEMPLATE.read_text(encoding="utf-8")
            template = home / "baseline-instructions.md"
            template.write_text(original + "\n- no-such-instruction\n", encoding="utf-8")
            with mock.patch.object(mod, "BASELINE_TEMPLATE", template):
                result = mod.deploy_baseline("codex", home=home, environ={})
        self.assertEqual(result["status"], "failed")
        self.assertIn("no-such-instruction", result["detail"])

    def test_creates_file_with_all_sections_and_real_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = mod.deploy_baseline("codex", home=home, environ={}, comms_enabled=True)
            self.assertEqual(result["status"], "created")
            content = (home / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
        for name in mod.baseline_section_names():
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
                "# My own notes\n\n<!-- agent-discovery -->\nstale content\n<!-- agent-discovery -->\n\nTrailing custom text.\n",
                encoding="utf-8",
            )
            result = mod.deploy_baseline("codex", home=home, environ={})
            self.assertEqual(result["status"], "updated")
            content = dest.read_text(encoding="utf-8")
        self.assertIn("# My own notes", content)
        self.assertIn("Trailing custom text.", content)
        self.assertNotIn("stale content", content)
        self.assertIn("agent-discovery", content)
        self.assertIn("<!-- prose-standards -->", content)

    def test_retired_sections_are_deleted_from_an_already_deployed_file(self) -> None:
        """Dropping a name from the baseline list stops rewriting its section.

        Only RETIRED_BASELINE_SECTIONS removes the block a previous deploy
        already wrote, so a retired rule stops applying on real machines.
        """
        self.assertTrue(mod.RETIRED_BASELINE_SECTIONS, "nothing retired; this guard is inert")
        retired = mod.RETIRED_BASELINE_SECTIONS[0]
        self.assertNotIn(retired, mod.baseline_section_names())
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            dest = home / ".codex" / "AGENTS.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                f"# Keep me\n\n<!-- {retired} -->\nretired rule body\n<!-- {retired} -->\n\nKeep me too.\n",
                encoding="utf-8",
            )
            mod.deploy_baseline("codex", home=home, environ={})
            content = dest.read_text(encoding="utf-8")
        self.assertNotIn(f"<!-- {retired} -->", content)
        self.assertNotIn("retired rule body", content)
        self.assertIn("# Keep me", content)
        self.assertIn("Keep me too.", content)

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


class BaselineCanaryTests(unittest.TestCase):
    """The baseline announces itself, and says which sections it carries."""

    def _deploy(self, home):
        return mod.deploy_baseline("claude", home=home, environ={}, comms_enabled=True)

    def test_deployed_baseline_carries_a_canary_naming_every_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._deploy(home)
            text = (home / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")

        self.assertIn(f"<!-- {mod.BASELINE_CANARY_SECTION} -->", text)
        self.assertIn("Baseline loaded:", text)
        for name in mod.baseline_section_names():
            self.assertIn(name, text, f"canary omits deployed section {name}")

    def test_redeploy_leaves_exactly_one_canary_block(self) -> None:
        """A canary that accumulated a copy per deploy would be worse than none."""
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._deploy(home)
            self._deploy(home)
            text = (home / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")

        self.assertEqual(2, text.count(f"<!-- {mod.BASELINE_CANARY_SECTION} -->"))
        self.assertEqual(1, text.count("Baseline loaded:"))

    def test_canary_reports_the_section_count_it_was_given(self) -> None:
        """The count is what makes a stale deploy visible rather than silent."""
        body = mod._baseline_canary_body(("alpha", "beta"))
        self.assertIn("Baseline loaded: 2 sections", body)
        self.assertIn("alpha, beta", body)

    def test_per_instruction_canaries_are_still_stripped_from_bodies(self) -> None:
        """Only the aggregate canary fires; 11 per-section ones would say nothing."""
        for name in mod.baseline_section_names():
            with self.subTest(name=name):
                self.assertNotIn("Instruction loaded:", mod._instruction_body(name))


class RegistrationLifecycleTests(unittest.TestCase):
    def _adapter(self, root: Path) -> mod.RegistrationAdapter:
        def upsert(existing: bytes, config_path: Path) -> bytes:
            owned = f"{mod.REGISTRATION_OWNERSHIP_TAG} {config_path}\n".encode()
            prefix = existing.split(mod.REGISTRATION_OWNERSHIP_TAG.encode(), 1)[0]
            suffix = b""
            if mod.REGISTRATION_OWNERSHIP_TAG.encode() in existing:
                suffix = existing.split(b"\n", 1)[-1] if b"\n" in existing else b""
            return prefix + owned + suffix

        def remove(existing: bytes) -> tuple[bytes, str]:
            marker = mod.REGISTRATION_OWNERSHIP_TAG.encode()
            if marker not in existing:
                return existing, ""
            line, _, remainder = existing.partition(b"\n")
            return remainder, line.decode()

        return mod.RegistrationAdapter(
            target_path=lambda base: base / "settings.json",
            config_path=lambda base: base / "hook-config.json",
            upsert=upsert,
            remove=remove,
        )

    def test_probe_success_writes_and_changed_path_replaces_owned_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            adapter = self._adapter(home / ".claude")
            responses = [mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n", stderr="")]
            with mock.patch.object(mod.subprocess, "run", side_effect=responses) as run:
                result = mod.run_registration("claude", adapter, enabled=True, home=home, environ={})
            target = home / ".claude" / "settings.json"
            self.assertEqual(result["status"], "created")
            self.assertEqual(result["probe"], "CROSSWIRE_HOOK_PROBE_OK")
            self.assertEqual(run.call_args.args[0], ["crosswire-turn-hook", "--probe", "--config", str(home / ".claude" / "hook-config.json")])
            unchanged = mod.run_registration(
                "claude", adapter, enabled=True, home=home, environ={},
                probe_runner=lambda *_args, **_kwargs: mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"),
            )
            self.assertEqual(unchanged["status"], "unchanged")
            alternate = home / "alternate.json"
            changed = mod.run_registration(
                "claude", adapter, enabled=True, config_path=alternate, home=home, environ={},
                probe_runner=lambda *_args, **_kwargs: mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"),
            )
            self.assertEqual(changed["status"], "updated")
            self.assertIn(str(alternate), target.read_text())
            self.assertEqual(target.read_text().count(mod.REGISTRATION_OWNERSHIP_TAG), 1)

    def test_failed_probe_never_writes_and_failure_token_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            adapter = self._adapter(home / ".claude")
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"foreign\n")
            for response in (
                mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_FAILED\n"),
                mock.Mock(returncode=0, stdout="unexpected\n"),
            ):
                result = mod.run_registration(
                    "claude", adapter, enabled=True, home=home, environ={},
                    probe_runner=lambda *_args, response=response, **_kwargs: response,
                )
                self.assertEqual(result["status"], "failed")
                self.assertEqual(target.read_bytes(), b"foreign\n")

    def test_disabled_registration_removes_edited_content_and_reports_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            adapter = self._adapter(home / ".claude")
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            target.write_bytes((mod.REGISTRATION_OWNERSHIP_TAG + " hand-edited\nforeign\n").encode())
            result = mod.run_registration("claude", adapter, enabled=False, home=home, environ={})
            self.assertEqual(result["status"], "removed")
            self.assertIn("hand-edited", result["removed_content"])
            self.assertEqual(target.read_bytes(), b"foreign\n")

    def test_probe_timeout_and_launch_failure_are_failed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            adapter = self._adapter(home / ".claude")
            for error in (TimeoutError(), FileNotFoundError()):
                result = mod.run_registration(
                    "claude", adapter, enabled=True, home=home, environ={},
                    probe_runner=mock.Mock(side_effect=error),
                )
                self.assertEqual(result["status"], "failed")

    def test_probe_timeout_is_capped_by_the_shared_bound(self) -> None:
        runner = mock.Mock(
            return_value=mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n")
        )
        result = mod.probe_crosswire(
            Path("/tmp/explicit-config.json"),
            probe_runner=runner,
            timeout=mod.PROBE_TIMEOUT_SECONDS * 2,
        )
        self.assertEqual(result["status"], "ok")
        self.assertEqual(runner.call_args.kwargs["timeout"], mod.PROBE_TIMEOUT_SECONDS)

    def test_invalid_adapter_path_returns_bounded_failure(self) -> None:
        adapter = mod.RegistrationAdapter(
            target_path=lambda _base: object(),
            config_path=lambda base: base / "hook-config.json",
            upsert=lambda existing, _config: existing,
            remove=lambda existing: (existing, ""),
        )
        result = mod.run_registration(
            "claude", adapter, enabled=False, home=Path("/tmp"), environ={}
        )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["detail"], "invalid-registration-path")

    def test_disabled_removal_does_not_require_config_path_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            target.write_bytes((mod.REGISTRATION_OWNERSHIP_TAG + " owned\n").encode())

            def forbidden_config_path(_base):
                raise AssertionError("disabled removal should not resolve a probe config")

            adapter = mod.RegistrationAdapter(
                target_path=lambda base: base / "settings.json",
                config_path=forbidden_config_path,
                upsert=lambda existing, _config: existing,
                remove=lambda _existing: (b"", "owned"),
            )
            result = mod.run_registration(
                "claude", adapter, enabled=False, home=home, environ={}
            )

        self.assertEqual(result["status"], "removed")
        self.assertEqual(result["removed_content"], "owned")

    def test_symlinked_registration_parent_is_not_followed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside"
            outside.mkdir()
            home = root / "home"
            home.mkdir()
            (home / ".claude").symlink_to(outside, target_is_directory=True)
            adapter = self._adapter(home / ".claude")
            result = mod.run_registration(
                "claude",
                adapter,
                enabled=True,
                home=home,
                environ={},
                probe_runner=lambda *_args, **_kwargs: mock.Mock(
                    returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"
                ),
            )

        self.assertEqual(result["status"], "failed")
        self.assertFalse((outside / "settings.json").exists())

    def test_deploy_runs_registration_only_for_selected_harnesses(self) -> None:
        adapter = self._adapter(Path("/unused"))
        with mock.patch.object(mod, "deploy_harness", return_value={"copied": 0}), \
                mock.patch.object(mod, "deploy_baseline", return_value={"status": "unchanged"}), \
                mock.patch.object(mod, "run_registration", return_value={"status": "unchanged"}) as run:
            mod.deploy(
                ["claude"],
                comms_profile=True,
                registration_adapters={"claude": adapter, "codex": adapter},
                verbose=False,
            )
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0], "claude")

    def test_atomic_registration_failure_preserves_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            adapter = self._adapter(home / ".claude")
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"before\n")
            with mock.patch.object(mod.os, "replace", side_effect=OSError("disk full")):
                result = mod.run_registration(
                    "claude", adapter, enabled=True, home=home, environ={},
                    probe_runner=lambda *_args, **_kwargs: mock.Mock(
                        returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"
                    ),
                )
            self.assertEqual(result["status"], "failed")
            self.assertEqual(target.read_bytes(), b"before\n")


class ClaudeRegistrationTests(unittest.TestCase):
    def _run(self, home: Path, config_path: Path | None = None) -> dict[str, object]:
        kwargs: dict[str, object] = {
            "enabled": True,
            "home": home,
            "environ": {},
            "probe_runner": lambda *_args, **_kwargs: mock.Mock(
                returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"
            ),
        }
        if config_path is not None:
            kwargs["config_path"] = config_path
        return mod.run_registration("claude", mod.REGISTRATION_ADAPTERS["claude"], **kwargs)

    def test_missing_settings_creates_owned_stop_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            config_path = home / "host.json"
            result = self._run(home, config_path)
            target = home / ".claude" / "settings.json"
            settings = json.loads(target.read_text(encoding="utf-8"))

        self.assertEqual(result["status"], "created")
        command = settings["hooks"]["Stop"][0]["hooks"][0]
        self.assertEqual(command["type"], "command")
        self.assertEqual(command["timeout"], 10)
        self.assertIn("crosswire-turn-hook --adapter claude --config", command["command"])
        self.assertIn(mod.REGISTRATION_OWNERSHIP_TAG, command["command"])

    def test_claude_config_dir_override_and_exact_probe_argument(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            override = home / "claude config"
            config_path = home / "host config.json"
            runner = mock.Mock(
                return_value=mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n")
            )
            result = mod.run_registration(
                "claude",
                mod.REGISTRATION_ADAPTERS["claude"],
                enabled=True,
                config_path=config_path,
                home=home,
                environ={"CLAUDE_CONFIG_DIR": str(override)},
                probe_runner=runner,
            )

        self.assertEqual(result["target_path"], str(override / "settings.json"))
        self.assertEqual(
            runner.call_args.args[0],
            ["crosswire-turn-hook", "--probe", "--config", str(config_path)],
        )

    def test_existing_settings_preserve_foreign_bytes_and_replace_only_owned_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            foreign = '{\n  "custom": "\\u2603",\n  "hooks": {\n    "Stop": [\n      {"matcher":"foreign", "hooks":[{"type":"command","command":"keep me"}]},\n      {"matcher":"", "hooks":[{"type":"command","command":"old # '
            target.write_text(foreign + mod.REGISTRATION_OWNERSHIP_TAG + '"}]}]\n  }\n}\n', encoding="utf-8")
            before = target.read_bytes()
            first = self._run(home, home / "one host.json")
            after = target.read_bytes()
            second = self._run(home, home / "one host.json")
            final = target.read_bytes()
            changed = self._run(home, home / "two host.json")
            changed_final = target.read_bytes()

        self.assertEqual(first["status"], "updated")
        self.assertEqual(second["status"], "unchanged")
        self.assertEqual(changed["status"], "updated")
        self.assertEqual(final, after)
        self.assertNotEqual(before, after)
        self.assertIn(b'"custom": "\\u2603"', after)
        self.assertIn(b'"command":"keep me"', after)
        self.assertEqual(after.count(mod.REGISTRATION_OWNERSHIP_TAG.encode()), 1)
        self.assertIn(shlex.quote(str(home / "two host.json")).encode(), changed_final)
        self.assertNotIn(shlex.quote(str(home / "one host.json")).encode(), changed_final)
        self.assertEqual(changed_final.count(mod.REGISTRATION_OWNERSHIP_TAG.encode()), 1)

    def test_duplicate_owned_groups_are_collapsed_and_profile_off_reports_hand_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            duplicate = {
                "hooks": {
                    "Stop": [
                        {"matcher": "foreign", "hooks": [{"type": "command", "command": "keep"}]},
                        {"matcher": "", "hooks": [{"type": "command", "command": "edited " + mod.REGISTRATION_OWNERSHIP_TAG}]},
                        {"matcher": "", "hooks": [{"type": "command", "command": "second " + mod.REGISTRATION_OWNERSHIP_TAG}]},
                    ]
                },
                "other": 7,
            }
            target.write_text(json.dumps(duplicate, indent=2) + "\n", encoding="utf-8")
            self._run(home, home / "host.json")
            settings = json.loads(target.read_text(encoding="utf-8"))
            settings["hooks"]["Stop"][-1]["hooks"][0]["command"] = (
                "edited by operator " + mod.REGISTRATION_OWNERSHIP_TAG
            )
            target.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = mod.deploy(["claude"], home=home, environ={}, comms_profile=False)
            remaining = json.loads(target.read_text(encoding="utf-8"))

        self.assertEqual(result["claude"]["registration"]["status"], "removed")
        self.assertIn(mod.REGISTRATION_OWNERSHIP_TAG, output.getvalue())
        self.assertIn("edited by operator", output.getvalue())
        self.assertEqual(remaining["hooks"]["Stop"][0]["hooks"][0]["command"], "keep")
        self.assertEqual(remaining["other"], 7)

    def test_profile_off_without_owned_entry_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".claude" / "settings.json"
            target.parent.mkdir(parents=True)
            original = b'{"hooks":{"Stop":[{"matcher":"foreign","hooks":[]}]},"x":1}\n'
            target.write_bytes(original)
            adapter = mod.REGISTRATION_ADAPTERS["claude"]
            first = mod.run_registration(
                "claude", adapter, enabled=False, home=home, environ={}
            )
            second = mod.run_registration(
                "claude", adapter, enabled=False, home=home, environ={}
            )
            final = target.read_bytes()

        self.assertEqual(first["status"], "unchanged")
        self.assertEqual(first["removed_content"], "")
        self.assertEqual(second["status"], "unchanged")
        self.assertEqual(final, original)

    def test_invalid_settings_fail_closed_without_probe_or_write(self) -> None:
        for content in (
            b"",
            b"not json",
            b"[]",
            b'{"hooks": []}',
            b'{"hooks":{"Stop":{}}}',
            b'{"n":NaN}',
            b'{"foreign":{"duplicate":1,"duplicate":2}}',
        ):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                target = home / ".claude" / "settings.json"
                target.parent.mkdir(parents=True)
                target.write_bytes(content)
                result = self._run(home, home / "host.json")

                self.assertEqual(result["status"], "failed")
                self.assertEqual(target.read_bytes(), content)


class OpenCodeRegistrationTests(unittest.TestCase):
    def _run(
        self,
        home: Path,
        config_path: Path | None = None,
        *,
        response: object | None = None,
        environ: dict[str, str] | None = None,
        probe_runner: object | None = None,
    ) -> dict[str, object]:
        if probe_runner is None:
            probe_runner = lambda *_args, **_kwargs: response or mock.Mock(
                returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"
            )
        kwargs: dict[str, object] = {
            "enabled": True,
            "home": home,
            "environ": environ or {},
            "probe_runner": probe_runner,
        }
        if config_path is not None:
            kwargs["config_path"] = config_path
        return mod.run_registration(
            "opencode", mod.REGISTRATION_ADAPTERS["opencode"], **kwargs
        )

    def _target(self, home: Path, environ: dict[str, str] | None = None) -> Path:
        root = Path((environ or {}).get("OPENCODE_CONFIG_DIR", home / ".config" / "opencode"))
        return root / "plugins" / "crosswire-comms.ts"

    def test_missing_plugin_directory_creates_one_owned_session_idle_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            config_path = home / "hook config.json"
            result = self._run(home, config_path)
            target = self._target(home)
            content = target.read_text(encoding="utf-8")

        self.assertEqual(result["status"], "created")
        self.assertEqual(target.name, "crosswire-comms.ts")
        self.assertEqual(target.parent.name, "plugins")
        self.assertEqual(content.count(mod.REGISTRATION_OWNERSHIP_TAG), 1)
        self.assertIn('event.type !== "session.idle"', content)
        self.assertIn("event.properties.sessionID", content)
        for value in (
            "pluginInput",
            "input.directory",
            "input.worktree",
            "input.project.id",
            "input.project.worktree",
        ):
            self.assertIn(value, content)
        self.assertIn("Bun.spawn", content)
        for value in (
            '"crosswire-turn-hook"',
            '"--adapter"',
            '"opencode"',
            '"--config"',
        ):
            self.assertIn(value, content)
        self.assertIn('stdin.write', content)
        self.assertIn('process.stdin.end()', content)
        self.assertIn(str(config_path), content)
        self.assertNotIn("input.$", content)
        self.assertNotIn("sh -c", content)

    def test_plugin_failure_reaps_the_spawned_hook_process(self) -> None:
        content = mod.OPENCODE_PLUGIN_SOURCE.read_text(encoding="utf-8")

        self.assertIn("process.kill()", content)
        self.assertIn("await process.exited.catch", content)

    def test_marker_inside_foreign_code_is_not_ownership_proof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = self._target(home)
            target.parent.mkdir(parents=True)
            original = (
                b'const note = "<!-- crosswire-comms-registration -->";\n'
            )
            target.write_bytes(original)

            enabled = self._run(home, home / "host.json")
            disabled = mod.run_registration(
                "opencode",
                mod.REGISTRATION_ADAPTERS["opencode"],
                enabled=False,
                home=home,
                environ={},
            )
            final = target.read_bytes()

        self.assertEqual(enabled["status"], "failed")
        self.assertEqual(enabled["detail"], "adapter-failed")
        self.assertEqual(disabled["status"], "unchanged")
        self.assertEqual(final, original)

    def test_opencode_root_override_and_probe_use_exact_config_argv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            root = home / "open code config"
            config_path = home / "host $config\\name.json"
            runner = mock.Mock(
                return_value=mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n")
            )
            result = self._run(
                home,
                config_path,
                environ={"OPENCODE_CONFIG_DIR": str(root)},
                probe_runner=runner,
            )
            target = self._target(home, {"OPENCODE_CONFIG_DIR": str(root)})
            self.assertTrue(target.is_file())

        self.assertEqual(result["target_path"], str(target))
        self.assertEqual(
            runner.call_args.args[0],
            ["crosswire-turn-hook", "--probe", "--config", str(config_path)],
        )
        self.assertNotIn("shell", runner.call_args.kwargs)

    def test_same_path_is_idempotent_and_changed_path_replaces_owned_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first_path = home / "one host.json"
            second_path = home / "two host.json"
            self.assertEqual(self._run(home, first_path)["status"], "created")
            target = self._target(home)
            first = target.read_bytes()
            self.assertEqual(self._run(home, first_path)["status"], "unchanged")
            self.assertEqual(target.read_bytes(), first)
            self.assertEqual(self._run(home, second_path)["status"], "updated")
            changed = target.read_text(encoding="utf-8")

        self.assertIn(str(second_path), changed)
        self.assertNotIn(str(first_path), changed)
        self.assertEqual(changed.count(mod.REGISTRATION_OWNERSHIP_TAG), 1)

    def test_config_path_is_serialized_as_a_typescript_string_literal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            config_path = home / 'quote " slash \\ dollar $ tick ` ${x}.json'
            result = self._run(home, config_path)
            target = self._target(home)
            content = target.read_text(encoding="utf-8")

        self.assertEqual(result["status"], "created")
        self.assertIn(json.dumps(str(config_path), ensure_ascii=False), content)
        self.assertNotIn('__CROSSWIRE_CONFIG_PATH__', content)

    def test_unowned_target_fails_closed_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = self._target(home)
            target.parent.mkdir(parents=True)
            original = b"// operator plugin without ownership\n"
            target.write_bytes(original)
            result = self._run(home, home / "host.json")
            final = target.read_bytes()

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["detail"], "adapter-failed")
        self.assertEqual(final, original)

    def test_foreign_plugins_remain_byte_identical_and_profile_off_reports_raw_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            plugins = home / ".config" / "opencode" / "plugins"
            plugins.mkdir(parents=True)
            foreign = plugins / "foreign.ts"
            foreign_bytes = b"// foreign\\xff plugin\n"
            foreign.write_bytes(foreign_bytes)
            self._run(home, home / "host.json")
            target = self._target(home)
            edited = b"// operator edit\n" + target.read_bytes()
            target.write_bytes(edited)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = mod.deploy(["opencode"], home=home, environ={}, comms_profile=False)
            remaining_foreign = foreign.read_bytes()
            target_exists = target.exists()

        self.assertEqual(result["opencode"]["registration"]["status"], "removed")
        self.assertIn("operator edit", output.getvalue())
        self.assertFalse(target_exists)
        self.assertEqual(remaining_foreign, foreign_bytes)

    def test_probe_failures_and_empty_target_leave_plugin_unchanged(self) -> None:
        responses: tuple[object, ...] = (
            mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_FAILED\n"),
            mock.Mock(returncode=0, stdout="unexpected\n"),
            mock.Mock(returncode=1, stdout="CROSSWIRE_HOOK_PROBE_OK\n"),
            subprocess.TimeoutExpired("crosswire-turn-hook", 10),
            FileNotFoundError("crosswire-turn-hook"),
        )
        for response in responses:
            with self.subTest(response=type(response).__name__), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                target = self._target(home)
                target.parent.mkdir(parents=True)
                original = b"foreign plugin\n"
                target.write_bytes(original)
                runner = mock.Mock(side_effect=response) if isinstance(response, BaseException) else mock.Mock(return_value=response)
                result = self._run(
                    home,
                    home / "host.json",
                    response=None if isinstance(response, BaseException) else response,
                    probe_runner=runner,
                )
                self.assertEqual(result["status"], "failed")
                self.assertEqual(target.read_bytes(), original)

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = self._target(home)
            target.parent.mkdir(parents=True)
            target.write_bytes(b"")
            runner = mock.Mock(return_value=mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"))
            result = mod.run_registration(
                "opencode",
                mod.REGISTRATION_ADAPTERS["opencode"],
                enabled=True,
                home=home,
                environ={},
                probe_runner=runner,
            )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["detail"], "target-empty")

    def test_profile_off_preserves_unowned_target_and_absent_target_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = self._target(home)
            target.parent.mkdir(parents=True)
            original = b"// no ownership marker\n"
            target.write_bytes(original)
            first = mod.run_registration(
                "opencode", mod.REGISTRATION_ADAPTERS["opencode"], enabled=False, home=home, environ={}
            )
            self.assertEqual(first["status"], "unchanged")
            self.assertEqual(target.read_bytes(), original)
            target.unlink()
            second = mod.run_registration(
                "opencode", mod.REGISTRATION_ADAPTERS["opencode"], enabled=False, home=home, environ={}
            )

        self.assertEqual(second["status"], "unchanged")
        self.assertEqual(second["removed_content"], "")

    def test_symlinked_plugin_parent_is_rejected_without_writing_outside_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            outside = root / "outside"
            home.mkdir()
            outside.mkdir()
            opencode_root = home / ".config" / "opencode"
            opencode_root.mkdir(parents=True)
            (opencode_root / "plugins").symlink_to(outside, target_is_directory=True)
            result = self._run(home, home / "host.json")
            outside_files = list(outside.iterdir())

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["detail"], "target-is-symlink")
        self.assertEqual(outside_files, [])


class CodexRegistrationTests(unittest.TestCase):
    def _run(
        self,
        home: Path,
        config_path: Path | None = None,
        *,
        response: object | None = None,
    ) -> dict[str, object]:
        kwargs: dict[str, object] = {
            "enabled": True,
            "home": home,
            "environ": {},
            "probe_runner": lambda *_args, **_kwargs: response
            or mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"),
        }
        if config_path is not None:
            kwargs["config_path"] = config_path
        return mod.run_registration("codex", mod.REGISTRATION_ADAPTERS["codex"], **kwargs)

    def test_missing_config_uses_codex_home_and_writes_owned_argv_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            codex_home = home / "custom codex"
            runner = mock.Mock(
                return_value=mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n")
            )
            result = mod.run_registration(
                "codex",
                mod.REGISTRATION_ADAPTERS["codex"],
                enabled=True,
                home=home,
                environ={"CODEX_HOME": str(codex_home)},
                probe_runner=runner,
            )
            target = codex_home / "config.toml"
            content = target.read_bytes()

        self.assertEqual(result["status"], "created")
        self.assertEqual(
            runner.call_args.args[0],
            ["crosswire-turn-hook", "--probe", "--config", str(codex_home / "hook-config.json")],
        )
        self.assertNotIn("shell", runner.call_args.kwargs)
        self.assertEqual(
            content.decode(),
            'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", '
            f'"{codex_home / "hook-config.json"}"] # {mod.REGISTRATION_OWNERSHIP_TAG}\n',
        )

    def test_existing_toml_preserves_foreign_bytes_and_top_level_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            original = (
                b"# preserve this comment\r\n"
                b"title = 'foreign'\r\n"
                b"foreign_text = 'notify = [\\\"do not touch\\\"]'\r\n"
                b"\r\n"
                b"[profiles.default]\r\n"
                b"model = 'o4'\r\n"
            )
            target.write_bytes(original)
            config_path = home / "host config.json"
            result = self._run(home, config_path)
            updated = target.read_bytes()

        expected_line = (
            f'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", '
            f'"{config_path}"] # {mod.REGISTRATION_OWNERSHIP_TAG}\r\n'
        ).encode()
        self.assertEqual(result["status"], "updated")
        self.assertEqual(updated.count(expected_line), 1)
        self.assertTrue(updated.endswith(b"[profiles.default]\r\nmodel = 'o4'\r\n"))
        self.assertIn(b"foreign_text = 'notify = [\\\"do not touch\\\"]'\r\n", updated)
        self.assertEqual(updated.count(mod.REGISTRATION_OWNERSHIP_TAG.encode()), 1)

    def test_same_path_is_idempotent_and_changed_path_replaces_owned_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first_path = home / "one.json"
            second_path = home / "two.json"
            self.assertEqual(self._run(home, first_path)["status"], "created")
            target = home / ".codex" / "config.toml"
            first = target.read_bytes()
            self.assertEqual(self._run(home, first_path)["status"], "unchanged")
            self.assertEqual(target.read_bytes(), first)
            self.assertEqual(self._run(home, second_path)["status"], "updated")
            changed = target.read_text()

        self.assertIn(str(second_path), changed)
        self.assertNotIn(str(first_path), changed)
        self.assertEqual(changed.count(mod.REGISTRATION_OWNERSHIP_TAG), 1)

    def test_duplicate_owned_lines_are_collapsed_without_touching_foreign_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            target.write_text(
                "model = 'keep'\n"
                'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", "one"] '
                f"# {mod.REGISTRATION_OWNERSHIP_TAG}\n"
                "comment = 'keep between'\n"
                'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", "two"] '
                f"# {mod.REGISTRATION_OWNERSHIP_TAG}\n",
                encoding="utf-8",
            )
            result = self._run(home, home / "three")
            updated = target.read_text(encoding="utf-8")

        self.assertEqual(result["status"], "updated")
        self.assertEqual(updated.count(mod.REGISTRATION_OWNERSHIP_TAG), 1)
        self.assertIn("model = 'keep'\n", updated)
        self.assertIn("comment = 'keep between'\n", updated)
        self.assertIn(str(home / "three"), updated)

    def test_foreign_notify_and_ambiguous_owned_lines_fail_without_mutation(self) -> None:
        fixtures = (
            'notify = ["foreign-command"]\n',
            'notify = ["crosswire-turn-hook", "--adapter", "codex" # '
            + mod.REGISTRATION_OWNERSHIP_TAG
            + "\n",
            'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", '
            '"literal # ' + mod.REGISTRATION_OWNERSHIP_TAG + '"]\n',
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                target = home / ".codex" / "config.toml"
                target.parent.mkdir(parents=True)
                original = fixture.encode()
                target.write_bytes(original)
                result = self._run(home, home / "host.json")
                self.assertEqual(result["status"], "failed")
                self.assertEqual(target.read_bytes(), original)

    def test_invalid_toml_escape_in_owned_line_fails_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            original = (
                'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", "bad'
                + r"\/"
                + 'path"] # '
                + mod.REGISTRATION_OWNERSHIP_TAG
                + "\n"
            ).encode()
            target.write_bytes(original)
            result = self._run(home, home / "host.json")
            final = target.read_bytes()

        self.assertEqual(result["status"], "failed")
        self.assertEqual(final, original)

    def test_profile_off_reports_hand_edited_owned_line_and_preserves_foreign_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            original = (
                "model = 'keep'\n"
                'notify = ["operator-edited", "--config", "changed"] '
                f"# {mod.REGISTRATION_OWNERSHIP_TAG}\n"
                "[profiles.default]\nmodel = 'o4'\n"
            ).encode()
            target.write_bytes(original)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = mod.deploy(["codex"], home=home, environ={}, comms_profile=False)
            remaining = target.read_bytes()

        self.assertEqual(result["codex"]["registration"]["status"], "removed")
        self.assertIn("operator-edited", output.getvalue())
        self.assertIn(mod.REGISTRATION_OWNERSHIP_TAG, output.getvalue())
        self.assertEqual(remaining, b"model = 'keep'\n[profiles.default]\nmodel = 'o4'\n")

    def test_enabled_zero_byte_target_fails_before_probe_or_codex_logic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"")
            result = self._run(
                home,
                response=mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_OK\n"),
            )

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["detail"], "target-empty")

    def test_probe_failures_leave_existing_codex_bytes_unchanged(self) -> None:
        responses: tuple[object, ...] = (
            mock.Mock(returncode=0, stdout="CROSSWIRE_HOOK_PROBE_FAILED\n"),
            mock.Mock(returncode=0, stdout="unexpected\n"),
            mock.Mock(returncode=1, stdout="CROSSWIRE_HOOK_PROBE_OK\n"),
            subprocess.TimeoutExpired("crosswire-turn-hook", 10),
            FileNotFoundError("crosswire-turn-hook"),
        )
        for response in responses:
            with self.subTest(response=type(response).__name__), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                target = home / ".codex" / "config.toml"
                target.parent.mkdir(parents=True)
                original = b"model = 'keep'\n"
                target.write_bytes(original)
                runner = mock.Mock(side_effect=response) if isinstance(response, BaseException) else mock.Mock(return_value=response)
                result = mod.run_registration(
                    "codex",
                    mod.REGISTRATION_ADAPTERS["codex"],
                    enabled=True,
                    config_path=home / "host.json",
                    home=home,
                    environ={},
                    probe_runner=runner,
                )
                self.assertEqual(result["status"], "failed")
                self.assertEqual(target.read_bytes(), original)

    def test_nested_or_prose_tag_text_is_not_owned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            target.write_text(
                "note = 'keep <!-- crosswire-comms-registration -->'\n"
                "[profiles.default]\n"
                'notify = ["foreign", "<!-- crosswire-comms-registration -->"]\n',
                encoding="utf-8",
            )
            result = self._run(home, home / "host.json")
            updated = target.read_text(encoding="utf-8")

        self.assertEqual(result["status"], "updated")
        self.assertIn("note = 'keep <!-- crosswire-comms-registration -->'\n", updated)
        self.assertIn(
            '[profiles.default]\nnotify = ["foreign", "<!-- crosswire-comms-registration -->"]\n',
            updated,
        )
        self.assertEqual(updated.count(mod.REGISTRATION_OWNERSHIP_TAG), 3)

    def test_inline_comment_on_table_header_keeps_nested_notify_foreign(self) -> None:
        fixtures = (
            '[profiles.default] # table comment\nnotify = ["foreign"]\n',
            '["profiles#default"] # table comment\nnotify = ["foreign"]\n',
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp)
                target = home / ".codex" / "config.toml"
                target.parent.mkdir(parents=True)
                target.write_text(fixture, encoding="utf-8")
                result = self._run(home, home / "host.json")
                updated = target.read_text(encoding="utf-8")

            self.assertEqual(result["status"], "updated")
            self.assertIn(fixture, updated)
            self.assertEqual(updated.count(mod.REGISTRATION_OWNERSHIP_TAG), 1)

    def test_changed_owned_line_preserves_missing_final_newline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            original = (
                'notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", "one"] # '
                + mod.REGISTRATION_OWNERSHIP_TAG
            ).encode()
            target.write_bytes(original)
            result = self._run(home, home / "two.json")
            updated = target.read_bytes()

        self.assertEqual(result["status"], "updated")
        self.assertFalse(updated.endswith(b"\n"))
        self.assertNotIn(b'"one"]', updated)
        self.assertIn(str(home / "two.json").encode(), updated)

    def test_profile_off_without_owned_entry_preserves_complete_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".codex" / "config.toml"
            target.parent.mkdir(parents=True)
            original = b"# foreign\r\nnotify = [\"foreign\"]\r\n"
            target.write_bytes(original)
            result = mod.run_registration(
                "codex",
                mod.REGISTRATION_ADAPTERS["codex"],
                enabled=False,
                home=home,
                environ={},
            )
            final = target.read_bytes()

        self.assertEqual(result["status"], "unchanged")
        self.assertEqual(result["removed_content"], "")
        self.assertEqual(final, original)


if __name__ == "__main__":
    unittest.main()
