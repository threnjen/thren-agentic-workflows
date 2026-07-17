import os
import sys
import tempfile
import unittest
from pathlib import Path, PureWindowsPath
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as propagator
import runtime_deployment as deployment


class RuntimeDestinationTests(unittest.TestCase):
    def _repo(self, root: Path) -> Path:
        repo = root / "repo"
        for relative in (
            "claude/agents",
            "claude/commands",
            "claude/skills",
            "claude/learnings",
            "claude/instructions",
            "codex/agents",
            "codex/profiles",
            "codex/skills",
            "codex/instructions",
            "opencode/agents",
            "opencode/skills",
            "opencode/instructions",
        ):
            (repo / relative).mkdir(parents=True)
        return repo

    def _converged(self) -> propagator.PropagationConvergenceResult:
        return propagator.PropagationConvergenceResult(True, 1, 0, {}, {})

    def test_complete_roster_uses_only_documented_generated_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            records = propagator.resolve_destinations_after_convergence(
                self._converged(),
                repo_root=self._repo(root),
                active_home=home,
                environment={},
                platform_facts=deployment.PlatformFacts("linux"),
            )

        roster = {(record.harness, record.asset_class) for record in records}
        self.assertEqual(
            roster,
            {
                ("claude", "agents"),
                ("claude", "commands"),
                ("claude", "skills"),
                ("claude", "learnings"),
                ("codex", "agents"),
                ("codex", "skills"),
                ("opencode", "agents"),
                ("opencode", "skills"),
            },
        )
        self.assertNotIn(("codex", "profiles"), roster)
        self.assertFalse(any(asset == "instructions" for _, asset in roster))
        for record in records:
            self.assertTrue(record.source.is_absolute())
            self.assertEqual(record.active_home, home)
            self.assertEqual(record.status, "planned")

    def test_default_destinations_stay_in_active_posix_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            records = deployment.resolve_runtime_destinations(
                repo_root=self._repo(root),
                active_home=home,
                environment={},
                platform_facts=deployment.PlatformFacts("darwin"),
            )

        destinations = {
            (record.harness, record.asset_class): record.destination
            for record in records
        }
        self.assertEqual(destinations[("claude", "agents")], home / ".claude/agents")
        self.assertEqual(destinations[("codex", "agents")], home / ".codex/agents")
        self.assertEqual(destinations[("codex", "skills")], home / ".agents/skills")
        self.assertEqual(
            destinations[("opencode", "agents")], home / ".config/opencode/agents"
        )
        self.assertEqual(
            destinations[("opencode", "skills")], home / ".config/opencode/skills"
        )
        for destination in destinations.values():
            destination.relative_to(home)

    def test_overrides_relocate_only_documented_owner_classes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            codex_home = home / "custom-codex"
            codex_home.mkdir()
            env = {
                "CLAUDE_CONFIG_DIR": str(home / "custom-claude"),
                "CODEX_HOME": str(codex_home),
                "OPENCODE_CONFIG_DIR": str(home / "custom-opencode"),
                "XDG_CONFIG_HOME": str(home / "ignored-xdg"),
            }
            records = deployment.resolve_runtime_destinations(
                repo_root=self._repo(root),
                active_home=home,
                environment=env,
                platform_facts=deployment.PlatformFacts("linux"),
            )

        destinations = {
            (record.harness, record.asset_class): record.destination
            for record in records
        }
        self.assertEqual(
            destinations[("claude", "skills")], home / "custom-claude/skills"
        )
        self.assertEqual(destinations[("codex", "agents")], codex_home / "agents")
        self.assertEqual(destinations[("codex", "skills")], home / ".agents/skills")
        self.assertEqual(
            destinations[("opencode", "agents")], home / "custom-opencode/agents"
        )
        self.assertEqual(
            destinations[("opencode", "skills")], home / ".config/opencode/skills"
        )

    def test_custom_codex_home_must_already_be_a_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            with self.assertRaises(deployment.DestinationResolutionError) as raised:
                deployment.resolve_runtime_destinations(
                    repo_root=self._repo(root),
                    active_home=home,
                    environment={"CODEX_HOME": str(home / "missing")},
                    platform_facts=deployment.PlatformFacts("linux"),
                )
        self.assertEqual(raised.exception.category, "codex_home_not_directory")

    def test_windows_and_wsl_classification_are_mutually_exclusive(self) -> None:
        windows = deployment.classify_platform(
            deployment.PlatformFacts("windows", is_wsl=False)
        )
        wsl = deployment.classify_platform(
            deployment.PlatformFacts("linux", is_wsl=True)
        )
        self.assertEqual(windows, "windows")
        self.assertEqual(wsl, "wsl")
        with self.assertRaises(deployment.DestinationResolutionError) as raised:
            deployment.classify_platform(
                deployment.PlatformFacts("windows", is_wsl=True)
            )
        self.assertEqual(raised.exception.category, "ambiguous_platform")
        with self.assertRaises(deployment.DestinationResolutionError) as raised:
            deployment.classify_platform(deployment.PlatformFacts("plan9"))
        self.assertEqual(raised.exception.category, "unsupported_platform")

    def test_simulated_native_windows_stays_in_active_profile(self) -> None:
        home = PureWindowsPath("C:/Users/active")
        records = deployment.resolve_runtime_destinations(
            repo_root=Path("C:/repo"),
            active_home=home,
            environment={},
            platform_facts=deployment.PlatformFacts("windows"),
            require_sources=False,
        )
        self.assertTrue(records)
        for record in records:
            self.assertIsInstance(record.destination, PureWindowsPath)
            self.assertTrue(record.destination.is_relative_to(home))

    def test_wsl_never_targets_a_windows_profile_or_mount(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            records = deployment.resolve_runtime_destinations(
                repo_root=self._repo(root),
                active_home=home,
                environment={},
                platform_facts=deployment.PlatformFacts("linux", is_wsl=True),
            )
            for record in records:
                self.assertTrue(record.destination.is_relative_to(home))
                self.assertNotIn("/mnt/", record.destination.as_posix())
                self.assertNotIn("Users", record.destination.parts)

    def test_invalid_overrides_fail_with_content_safe_categories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            repo = self._repo(root)
            cases = (
                ("CLAUDE_CONFIG_DIR", "relative/path", "relative_override"),
                ("CLAUDE_CONFIG_DIR", "", "empty_override"),
                ("OPENCODE_CONFIG_DIR", str(root / "outside"), "outside_active_home"),
                ("CLAUDE_CONFIG_DIR", "bad\x00value", "invalid_override"),
                ("CLAUDE_CONFIG_DIR", "C:\\Users\\other", "cross_environment_path"),
            )
            for variable, value, category in cases:
                with self.subTest(variable=variable, category=category):
                    with self.assertRaises(deployment.DestinationResolutionError) as raised:
                        deployment.resolve_runtime_destinations(
                            repo_root=repo,
                            active_home=home,
                            environment={variable: value},
                            platform_facts=deployment.PlatformFacts("linux"),
                        )
                    self.assertEqual(raised.exception.category, category)
                    self.assertEqual(str(raised.exception), category)
                    if value:
                        self.assertNotIn(value, str(raised.exception))

    @unittest.skipIf(not hasattr(os, "symlink"), "symlinks unavailable")
    def test_leaf_link_is_preserved_but_escaping_parent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            repo = self._repo(root)
            destination_root = home / ".claude"
            destination_root.mkdir()
            (destination_root / "agents").symlink_to(repo / "claude/agents")

            records = deployment.resolve_runtime_destinations(
                repo_root=repo,
                active_home=home,
                environment={},
                platform_facts=deployment.PlatformFacts("linux"),
            )
            agents = next(
                record
                for record in records
                if record.harness == "claude" and record.asset_class == "agents"
            )
            self.assertTrue(agents.destination.is_symlink())
            self.assertEqual(agents.destination, destination_root / "agents")

            outside = root / "outside"
            outside.mkdir()
            (home / "escape").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(deployment.DestinationResolutionError) as raised:
                deployment.resolve_runtime_destinations(
                    repo_root=repo,
                    active_home=home,
                    environment={"CLAUDE_CONFIG_DIR": str(home / "escape/claude")},
                    platform_facts=deployment.PlatformFacts("linux"),
                )
            self.assertEqual(raised.exception.category, "symlinked_parent")

    def test_junction_parent_is_rejected_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            junction = home / "junction"
            junction.mkdir()
            repo = self._repo(root)

            with mock.patch.object(
                Path,
                "is_junction",
                autospec=True,
                side_effect=lambda path: path == junction,
            ):
                with self.assertRaises(
                    deployment.DestinationResolutionError
                ) as raised:
                    deployment.resolve_runtime_destinations(
                        repo_root=repo,
                        active_home=home,
                        environment={
                            "CLAUDE_CONFIG_DIR": str(junction / "claude")
                        },
                        platform_facts=deployment.PlatformFacts("linux"),
                    )

            self.assertEqual(raised.exception.category, "junction_parent")

    def test_unconverged_handoff_is_rejected_before_resolution(self) -> None:
        unconverged = propagator.PropagationConvergenceResult(False, 1, 0, {}, {})
        with self.assertRaises(propagator.PropagationConvergenceError) as raised:
            propagator.resolve_destinations_after_convergence(
                unconverged,
                repo_root=Path("/unused"),
                active_home=Path("/unused"),
                environment={},
                platform_facts=deployment.PlatformFacts("linux"),
            )
        self.assertEqual(raised.exception.category, "deployment_before_convergence")

    def test_inventory_home_relativizes_destination_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            records = deployment.resolve_runtime_destinations(
                repo_root=self._repo(root),
                active_home=home,
                environment={},
                platform_facts=deployment.PlatformFacts("linux"),
            )
            inventory = deployment.destination_inventory(records)

        self.assertEqual(len(inventory), len(records))
        self.assertTrue(all(item["destination"].startswith("~/") for item in inventory))
        self.assertTrue(all(str(home) not in item["destination"] for item in inventory))
        expected_fields = {"harness", "asset_class", "status", "destination"}
        self.assertTrue(all(set(item) == expected_fields for item in inventory))


if __name__ == "__main__":
    unittest.main()
