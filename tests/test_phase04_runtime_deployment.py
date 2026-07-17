import json
import os
import shutil
import subprocess
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


class ManagedCopyReconciliationTests(unittest.TestCase):
    def _record(self, root: Path, harness: str = "claude") -> deployment.DestinationRecord:
        source = root / "repo" / harness / "agents"
        source.mkdir(parents=True)
        home = root / "home"
        home.mkdir(exist_ok=True)
        return deployment.DestinationRecord(
            harness, "agents", source, home / f".{harness}" / "agents", home
        )

    def _generated(self, path: Path, body: str = "body") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->\n"
            f"{body}\n",
            encoding="utf-8",
        )

    def test_absent_destination_is_staged_as_regular_managed_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = self._record(Path(tmp))
            self._generated(record.source / "one.md")

            result = deployment.deploy_managed_copies((record,))

            destination = Path(record.destination)
            self.assertEqual(result.harnesses["claude"].status, "verified")
            self.assertEqual(result.harnesses["claude"].inventoried, 1)
            self.assertTrue((destination / "one.md").is_file())
            self.assertFalse(destination.is_symlink())
            self.assertTrue((destination / deployment.MANAGED_METADATA).is_file())

    def test_repository_link_is_unlinked_without_traversing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "one.md", "fresh")
            destination = Path(record.destination)
            destination.parent.mkdir(parents=True)
            destination.symlink_to(record.source, target_is_directory=True)

            result = deployment.deploy_managed_copies((record,))

            self.assertEqual(result.harnesses["claude"].replaced, 1)
            self.assertTrue(destination.is_dir())
            self.assertFalse(destination.is_symlink())
            self.assertEqual((record.source / "one.md").read_text(encoding="utf-8").splitlines()[1], "fresh")

    def test_foreign_content_and_foreign_links_are_preserved_as_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "owned.md")
            (record.source / "foreign.md").write_text("generated candidate", encoding="utf-8")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            (destination / "foreign.md").write_text("keep me", encoding="utf-8")
            outside = root / "outside"
            outside.write_text("outside", encoding="utf-8")
            (destination / "owned.md").symlink_to(outside)

            result = deployment.deploy_managed_copies((record,))

            harness = result.harnesses["claude"]
            self.assertEqual(harness.collisions, 2)
            self.assertEqual((destination / "foreign.md").read_text(encoding="utf-8"), "keep me")
            self.assertTrue((destination / "owned.md").is_symlink())

    def test_foreign_metadata_entry_blocks_record_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "owned.md")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            metadata = destination / deployment.MANAGED_METADATA
            metadata.write_text("user content", encoding="utf-8")

            result = deployment.deploy_managed_copies((record,))

            self.assertEqual(metadata.read_text(encoding="utf-8"), "user content")
            self.assertFalse((destination / "owned.md").exists())
            self.assertEqual(result.harnesses["claude"].collisions, 1)

    def test_owned_stale_copy_is_pruned_but_unmarked_copy_survives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "current.md")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            self._generated(destination / "stale.md", "stale")
            (destination / "foreign.md").write_text("keep", encoding="utf-8")

            result = deployment.deploy_managed_copies((record,))

            self.assertEqual(result.harnesses["claude"].removed, 1)
            self.assertFalse((destination / "stale.md").exists())
            self.assertTrue((destination / "foreign.md").exists())

    def test_empty_generated_root_prunes_only_owned_stale_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = self._record(Path(tmp))
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            self._generated(destination / "stale.md", "stale")
            foreign = destination / "foreign.txt"
            foreign.write_text("keep", encoding="utf-8")

            result = deployment.deploy_managed_copies((record,))

            self.assertFalse((destination / "stale.md").exists())
            self.assertEqual(foreign.read_text(encoding="utf-8"), "keep")
            self.assertEqual(result.harnesses["claude"].removed, 1)
            self.assertEqual(result.harnesses["claude"].collisions, 1)

    def test_quoted_generated_marker_does_not_prove_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = self._record(Path(tmp))
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            quoted = destination / "README.md"
            quoted.write_text(
                "Hand maintained\n"
                "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->\n",
                encoding="utf-8",
            )

            result = deployment.deploy_managed_copies((record,))

            self.assertTrue(quoted.exists())
            self.assertEqual(result.harnesses["claude"].removed, 0)
            self.assertEqual(result.harnesses["claude"].collisions, 1)

    def test_prune_rechecks_identity_before_removing_owned_stale_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "current.md")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            stale = destination / "stale.md"
            self._generated(stale, "stale")
            real_identity = deployment._entry_identity
            stale_checks = 0

            def replace_before_recheck(path: Path):
                nonlocal stale_checks
                if path == stale:
                    stale_checks += 1
                    if stale_checks == 2:
                        stale.unlink()
                        stale.write_text("user replacement", encoding="utf-8")
                return real_identity(path)

            with mock.patch.object(
                deployment, "_entry_identity", side_effect=replace_before_recheck
            ):
                result = deployment.deploy_managed_copies((record,))

            self.assertEqual(stale.read_text(encoding="utf-8"), "user replacement")
            self.assertEqual(result.harnesses["claude"].removed, 0)
            self.assertGreaterEqual(result.harnesses["claude"].collisions, 1)

    def test_stage_failure_preserves_old_destination_and_skips_harness_pruning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._record(root)
            self._generated(first.source / "current.md")
            destination = Path(first.destination)
            destination.mkdir(parents=True)
            self._generated(destination / "stale.md")
            second_source = root / "repo" / "claude" / "commands"
            second_source.mkdir(parents=True)
            self._generated(second_source / "command.md")
            second = deployment.DestinationRecord(
                "claude", "commands", second_source, root / "home/.claude/commands", root / "home"
            )

            def copy(source: Path, target: Path) -> None:
                if source == second_source:
                    raise OSError("injected")
                deployment._copy_source(source, target)

            result = deployment.deploy_managed_copies((first, second), copy_tree=copy)

            self.assertEqual(result.harnesses["claude"].status, "failed")
            self.assertTrue(result.harnesses["claude"].reconciliation_skipped)
            self.assertTrue((destination / "stale.md").exists())

    def test_second_run_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = self._record(Path(tmp))
            self._generated(record.source / "one.md")
            deployment.deploy_managed_copies((record,))

            result = deployment.deploy_managed_copies((record,))

            harness = result.harnesses["claude"]
            self.assertEqual(harness.copied + harness.replaced + harness.removed, 0)
            self.assertGreaterEqual(harness.unchanged, 1)

    def test_stale_metadata_does_not_authorize_overwriting_user_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = self._record(Path(tmp))
            candidate = record.source / "plain.txt"
            candidate.write_text("generated", encoding="utf-8")
            deployment.deploy_managed_copies((record,))
            installed = Path(record.destination) / "plain.txt"
            installed.write_text("user replacement", encoding="utf-8")
            candidate.write_text("new generated", encoding="utf-8")

            result = deployment.deploy_managed_copies((record,))

            self.assertEqual(installed.read_text(encoding="utf-8"), "user replacement")
            self.assertEqual(result.harnesses["claude"].collisions, 1)

            candidate.write_text("third generated", encoding="utf-8")
            repeated = deployment.deploy_managed_copies((record,))

            self.assertEqual(installed.read_text(encoding="utf-8"), "user replacement")
            self.assertEqual(repeated.harnesses["claude"].collisions, 1)

    def test_identical_unmarked_file_is_not_adopted_as_managed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = self._record(Path(tmp))
            candidate = record.source / "plain.txt"
            candidate.write_text("same", encoding="utf-8")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            installed = destination / "plain.txt"
            installed.write_text("same", encoding="utf-8")

            first = deployment.deploy_managed_copies((record,))
            candidate.write_text("generated update", encoding="utf-8")
            second = deployment.deploy_managed_copies((record,))

            self.assertEqual(first.harnesses["claude"].collisions, 1)
            self.assertEqual(second.harnesses["claude"].collisions, 1)
            self.assertEqual(installed.read_text(encoding="utf-8"), "same")

    def test_symlinked_active_home_is_rejected_before_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real_home = root / "real-home"
            real_home.mkdir()
            linked_home = root / "home"
            linked_home.symlink_to(real_home, target_is_directory=True)
            source = root / "repo/claude/agents"
            source.mkdir(parents=True)
            self._generated(source / "one.md")
            record = deployment.DestinationRecord(
                "claude", "agents", source, linked_home / ".claude/agents", linked_home
            )

            result = deployment.deploy_managed_copies((record,))

            self.assertEqual(result.harnesses["claude"].status, "failed")
            self.assertFalse((real_home / ".claude").exists())

    def test_dangling_repository_link_is_replaced_but_foreign_one_survives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "owned.md")
            self._generated(record.source / "foreign.md")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            (destination / "owned.md").symlink_to(record.source / "retired.md")
            (destination / "foreign.md").symlink_to(root / "elsewhere/missing.md")

            result = deployment.deploy_managed_copies((record,))

            self.assertTrue((destination / "owned.md").is_file())
            self.assertFalse((destination / "owned.md").is_symlink())
            self.assertTrue((destination / "foreign.md").is_symlink())
            self.assertEqual(result.harnesses["claude"].collisions, 1)

    def test_replacement_failure_restores_prior_managed_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self._record(root)
            self._generated(record.source / "one.md", "fresh")
            destination = Path(record.destination)
            destination.mkdir(parents=True)
            self._generated(destination / "one.md", "old")
            real_replace = os.replace

            def fail_install(source, target):
                if ".managed-stage-" in os.fspath(source) and Path(target).name == "one.md":
                    raise PermissionError("locked")
                return real_replace(source, target)

            with mock.patch.object(deployment.os, "replace", side_effect=fail_install):
                result = deployment.deploy_managed_copies((record,))

            self.assertEqual(result.harnesses["claude"].status, "failed")
            self.assertTrue(result.harnesses["claude"].reconciliation_skipped)
            self.assertEqual((destination / "one.md").read_text(encoding="utf-8").splitlines()[1], "old")

    def test_mixed_harness_failure_does_not_roll_back_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claude = self._record(root, "claude")
            codex = self._record(root, "codex")
            self._generated(claude.source / "one.md")
            self._generated(codex.source / "one.md")

            def copy(source: Path, target: Path) -> None:
                if "codex" in source.parts:
                    raise OSError("injected")
                deployment._copy_source(source, target)

            result = deployment.deploy_managed_copies((claude, codex), copy_tree=copy)

            self.assertEqual(result.harnesses["claude"].status, "verified")
            self.assertTrue((Path(claude.destination) / "one.md").is_file())
            self.assertEqual(result.harnesses["codex"].status, "failed")
            self.assertFalse(Path(codex.destination).exists())

    def test_propagator_gate_invokes_settled_managed_copy_api(self) -> None:
        convergence = propagator.PropagationConvergenceResult(True, 1, 0, {}, {})
        expected = deployment.ManagedCopyResult({})
        with mock.patch.object(deployment, "deploy_managed_copies", return_value=expected) as managed:
            actual = propagator.deploy_managed_copies_after_convergence(convergence, ())
        self.assertIs(actual, expected)
        managed.assert_called_once_with(())

        unconverged = propagator.PropagationConvergenceResult(False, 1, 0, {}, {})
        with self.assertRaises(propagator.PropagationConvergenceError):
            propagator.deploy_managed_copies_after_convergence(unconverged, ())


class PhaseRuntimeOrchestrationTests(unittest.TestCase):
    def _generated_repo(self, root: Path) -> Path:
        repo = root / "repo"
        for policy in deployment._ASSET_POLICIES:
            source = repo / policy.source_relative
            source.mkdir(parents=True, exist_ok=True)
            (source / "asset.md").write_text(
                "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->\n"
                f"{policy.harness}:{policy.asset_class}\n",
                encoding="utf-8",
            )
        return repo

    def _run(self, root: Path, reviewed: str | None = None, **kwargs):
        kwargs.setdefault("watcher_restarted", reviewed is not None)
        return propagator.run_runtime_deployment(
            active_home=root / "home",
            reviewed_inventory=reviewed,
            repo_root=self._generated_repo(root),
            environment={},
            platform_facts=deployment.PlatformFacts("linux"),
            propagate=lambda: {"source_agents": 1},
            **kwargs,
        )

    def test_reviewed_scratch_home_path_deploys_all_harnesses_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "home").mkdir()
            inventory = self._run(root)
            self.assertEqual(inventory.status, "review_required")
            self.assertIsNone(inventory.deployment)
            self.assertEqual(inventory.stages, ("convergence", "destination_preflight", "inventory"))

            first = self._run(root, inventory.inventory_digest)
            second_inventory = self._run(root)
            second = self._run(root, second_inventory.inventory_digest)

            self.assertEqual(set(first.deployment.harnesses), {"claude", "codex", "opencode"})
            self.assertTrue(all(item.regular_fresh for item in first.verification.values()))
            self.assertTrue(all(item.repository_links == 0 for item in first.verification.values()))
            self.assertTrue(all(result.status == "verified" for result in first.deployment.harnesses.values()))
            self.assertTrue(all(result.copied + result.replaced + result.removed == 0 for result in second.deployment.harnesses.values()))
            self.assertIn("verification", first.stages)
            self.assertEqual(first.status, "partial")
            self.assertTrue(all(value.startswith("NOT RUN:") for value in first.platform_evidence.values()))

    def test_inventory_classifies_owned_removal_foreign_preservation_and_collision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            repo = self._generated_repo(root)
            destination = home / ".claude/agents"
            destination.mkdir(parents=True)
            (destination / "stale.md").write_text(
                "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->\nstale\n",
                encoding="utf-8",
            )
            (destination / "foreign.txt").write_text("keep", encoding="utf-8")
            (destination / "asset.md").write_text("user collision", encoding="utf-8")
            records = deployment.resolve_runtime_destinations(
                repo_root=repo,
                active_home=home,
                environment={},
                platform_facts=deployment.PlatformFacts("linux"),
            )

            inventory = deployment.managed_copy_inventory(records)
            statuses = {item["status"] for item in inventory}

            self.assertIn("planned_replacement", statuses)
            self.assertIn("obsolete_owned_removal", statuses)
            self.assertIn("preserved_foreign", statuses)
            self.assertIn("collision", statuses)
            self.assertTrue(all(item["destination"].startswith("~/") for item in inventory))
            self.assertNotIn(str(home), json.dumps(inventory))

    def test_material_inventory_drift_aborts_before_deploy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "home").mkdir()
            reviewed = self._run(root)
            real_inventory = deployment.managed_copy_inventory
            calls = 0

            def drifting(records):
                nonlocal calls
                calls += 1
                result = real_inventory(records)
                if calls == 2:
                    return result + ({
                        "harness": "claude",
                        "asset_class": "agents",
                        "status": "collision",
                        "destination": "~/.claude/agents/drift",
                    },)
                return result

            deployed = False

            def forbidden(_records):
                nonlocal deployed
                deployed = True
                raise AssertionError("deployment must not run")

            with mock.patch.object(deployment, "managed_copy_inventory", side_effect=drifting):
                result = self._run(root, reviewed.inventory_digest, deploy=forbidden)

            self.assertEqual(result.status, "failed")
            self.assertEqual(result.failure_categories, ("inventory_drift",))
            self.assertFalse(deployed)

    def test_review_digest_is_bound_to_the_active_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = self._generated_repo(root)
            first_home = root / "first-home"
            second_home = root / "second-home"
            first_home.mkdir()
            second_home.mkdir()
            common = {
                "repo_root": repo,
                "environment": {},
                "platform_facts": deployment.PlatformFacts("linux"),
                "propagate": lambda: {"source_agents": 1},
            }

            first = propagator.run_runtime_deployment(
                active_home=first_home, **common
            )
            second = propagator.run_runtime_deployment(
                active_home=second_home, **common
            )
            replay = propagator.run_runtime_deployment(
                active_home=second_home,
                reviewed_inventory=first.inventory_digest,
                watcher_restarted=True,
                **common,
            )

            self.assertNotEqual(first.inventory_digest, second.inventory_digest)
            self.assertEqual(replay.status, "review_required")
            self.assertEqual(replay.failure_categories, ("inventory_drift",))
            self.assertEqual(list(second_home.iterdir()), [])

    def test_unreviewed_or_wrong_inventory_digest_never_mutates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            unreviewed = self._run(root)
            wrong = self._run(root, "0" * 64)

            self.assertEqual(unreviewed.failure_categories, ("inventory_review_required",))
            self.assertEqual(wrong.failure_categories, ("inventory_drift",))
            self.assertEqual(list(home.iterdir()), [])

            valid_but_stale_watcher = self._run(
                root, unreviewed.inventory_digest, watcher_restarted=False
            )
            self.assertEqual(
                valid_but_stale_watcher.failure_categories,
                ("watcher_restart_required",),
            )
            self.assertEqual(list(home.iterdir()), [])

    def test_nonconverged_repository_causes_zero_runtime_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            home.mkdir()
            with self.assertRaises(propagator.PropagationConvergenceError) as raised:
                propagator.run_runtime_deployment(
                    active_home=home,
                    repo_root=self._generated_repo(root),
                    environment={},
                    platform_facts=deployment.PlatformFacts("linux"),
                    propagate=lambda: {"changed": 1},
                )
            self.assertEqual(raised.exception.category, "bound_exhausted")
            self.assertEqual(list(home.iterdir()), [])

    def test_partial_harness_failure_is_non_go_and_preserves_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "home").mkdir()
            reviewed = self._run(root)

            def partial(records):
                successful = [record for record in records if record.harness != "codex"]
                deployed = deployment.deploy_managed_copies(successful)
                return deployment.ManagedCopyResult({
                    **deployed.harnesses,
                    "codex": deployment.HarnessManagedCopyResult(
                        status="failed", failed=1, reconciliation_skipped=True,
                        failures=("staging_failed",),
                    ),
                })

            result = self._run(root, reviewed.inventory_digest, deploy=partial)

            self.assertEqual(result.status, "partial")
            self.assertIn("partial_deployment", result.failure_categories)
            self.assertEqual(result.deployment.harnesses["claude"].status, "verified")
            self.assertEqual(result.deployment.harnesses["codex"].status, "failed")
            self.assertTrue(result.deployment.harnesses["codex"].reconciliation_skipped)

    @unittest.skipUnless(shutil.which("rtk"), "rtk executable unavailable")
    def test_explicit_rtk_prefixed_command_remains_usable(self) -> None:
        completed = subprocess.run(
            [shutil.which("rtk"), "git", "status", "--short"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_runtime_cli_reports_review_required_without_deploying(self) -> None:
        convergence = propagator.PropagationConvergenceResult(True, 1, 0, {}, {})
        expected = propagator.RuntimeDeploymentResult(
            status="review_required",
            stages=("convergence", "destination_preflight", "inventory"),
            convergence=convergence,
            inventory=(),
            inventory_digest="a" * 64,
            deployment=None,
            verification={},
            failure_categories=("inventory_review_required",),
            platform_evidence={"macOS": "NOT RUN: test"},
        )
        with mock.patch.object(propagator, "run_runtime_deployment", return_value=expected) as run:
            with mock.patch.object(sys, "argv", ["propagate", "--runtime-deploy", "--active-home", "/tmp/scratch-home"]):
                with mock.patch("builtins.print") as printed:
                    exit_code = propagator.main()
        self.assertEqual(exit_code, 2)
        run.assert_called_once()
        payload = json.loads(printed.call_args.args[0])
        self.assertEqual(payload["status"], "review_required")
        self.assertEqual(payload["inventory_digest"], "a" * 64)


class DeploymentGuidanceTests(unittest.TestCase):
    SUPPORTED_SURFACES = (
        ".github/agents/evangelize.agent.md",
        "claude/README.md",
        "claude/agents/README.md",
        "codex/PILOT_SLICE_PLAN.md",
        "HARNESS_SETUP.md",
        "docs/TROUBLESHOOTING.md",
        "README.md",
    )
    PROHIBITED_OPERATIONAL_TOKENS = (
        "ln -s",
        "New-Item -ItemType SymbolicLink",
        "mklink /J",
        "mklink /H",
    )
    PROHIBITED_RUNTIME_LINK_VALIDATION = ("check symlinks:",)

    def _assert_no_runtime_link_recipe(self, text: str) -> None:
        for token in (
            *self.PROHIBITED_OPERATIONAL_TOKENS,
            *self.PROHIBITED_RUNTIME_LINK_VALIDATION,
        ):
            self.assertNotIn(token.casefold(), text.casefold())

    def test_supported_guidance_has_no_runtime_link_creation_recipe(self) -> None:
        for relative in self.SUPPORTED_SURFACES:
            with self.subTest(path=relative):
                text = (REPO_ROOT / relative).read_text(encoding="utf-8")
                self._assert_no_runtime_link_recipe(text)

    def test_runtime_link_guard_rejects_negative_fixture(self) -> None:
        for recipe in self.PROHIBITED_OPERATIONAL_TOKENS:
            with self.subTest(recipe=recipe):
                with self.assertRaises(AssertionError):
                    self._assert_no_runtime_link_recipe(
                        f"Install generated agents with `{recipe} source destination`."
                    )

    def test_security_and_retirement_discussion_remains_allowed(self) -> None:
        allowed = (
            "Reject a hostile symlinked parent before mutation. "
            "The former runtime-link deployment model is retired."
        )
        self._assert_no_runtime_link_recipe(allowed)

    def test_evangelize_requires_managed_copy_readiness_contract(self) -> None:
        source = (REPO_ROOT / ".github/agents/evangelize.agent.md").read_text(
            encoding="utf-8"
        )
        for obligation in (
            "propagate_until_converged",
            "--runtime-deploy",
            "--reviewed-inventory",
            "--watcher-restarted",
            "regular-copy freshness",
            "expected roster coverage",
            "collision",
            "Inspect the printed managed-copy result",
            "runtime discovery",
            "NOT RUN",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, source)

    def test_native_windows_and_wsl_are_separate_evidence(self) -> None:
        source = (REPO_ROOT / ".github/agents/evangelize.agent.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(source.split()).casefold()
        self.assertIn("native windows and wsl are separate runs", normalized)
        self.assertIn("not run prevents a full cross-platform go", normalized)


if __name__ == "__main__":
    unittest.main()
