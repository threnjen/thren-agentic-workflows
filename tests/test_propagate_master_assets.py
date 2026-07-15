import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod


class PropagateMasterAssetsTests(unittest.TestCase):
    def _make_hook_source(self, root: Path) -> Path:
        hooks_dir = root / ".github" / "hooks"
        (hooks_dir / "scripts").mkdir(parents=True)
        (hooks_dir / "lib").mkdir()
        (hooks_dir / "config").mkdir()
        (hooks_dir / "file-access-guard.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "Read|Write|Bash",
                                "type": "command",
                                "command": "python3 .github/hooks/scripts/file-access-guard.py",
                                "timeout": 10,
                            }
                        ]
                    }
                }
            ),
            encoding="utf-8",
        )
        (hooks_dir / "scripts" / "file-access-guard.py").write_text(
            "from lib.framework import main\nmain()\n", encoding="utf-8"
        )
        (hooks_dir / "lib" / "framework.py").write_text(
            "def main():\n    return None\n", encoding="utf-8"
        )
        (hooks_dir / "lib" / "bash_analyzer.py").write_text(
            "def analyze(command):\n    return command\n", encoding="utf-8"
        )
        (hooks_dir / "config" / "file-access-rules.json").write_text(
            "{}\n", encoding="utf-8"
        )
        (hooks_dir / "config" / "file-access-overrides.json").write_text(
            "{}\n", encoding="utf-8"
        )
        return root

    def test_write_if_changed_replaces_self_referential_symlink(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            target = Path(tmp_dir) / "output.md"
            target.symlink_to(target)

            changed = mod._write_if_changed(target, "hello\n")

            self.assertTrue(changed)
            self.assertTrue(target.is_file())
            self.assertFalse(target.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "hello\n")

    def test_propagate_skills_mirrors_to_claude_opencode_and_codex(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            skill_dir = repo_root / ".github" / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: \"Demo skill\"\n---\n# Demo body\n",
                encoding="utf-8",
            )

            result = mod.propagate_skills_once(repo_root)

            self.assertEqual(result["claude_changed"], 1)
            self.assertEqual(result["opencode_changed"], 1)
            self.assertEqual(result["codex_changed"], 1)
            self.assertTrue((repo_root / "claude" / "skills" / "demo-skill" / "SKILL.md").exists())
            self.assertTrue((repo_root / "opencode" / "skills" / "demo-skill" / "SKILL.md").exists())
            self.assertTrue((repo_root / "codex" / "skills" / "demo-skill" / "SKILL.md").exists())

    def test_hook_propagation_copies_runtime_unit_and_writes_stable_version(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            source_root = self._make_hook_source(tmp_root / "source")
            consumer_root = tmp_root / "consumer"

            first = mod.propagate_hooks_once(
                repo_root=consumer_root, source_root=source_root
            )
            marker = consumer_root / ".github" / "hooks" / ".distribution-version"
            first_version = marker.read_text(encoding="utf-8")
            second = mod.propagate_hooks_once(
                repo_root=consumer_root, source_root=source_root
            )
            second_version = marker.read_text(encoding="utf-8")
            (source_root / ".github" / "hooks" / "config" / "file-access-rules.json").write_text(
                '{"version": 2}\n', encoding="utf-8"
            )
            third = mod.propagate_hooks_once(
                repo_root=consumer_root, source_root=source_root
            )

            self.assertEqual(first["assets_changed"], 6)
            self.assertEqual(second["assets_changed"], 0)
            self.assertEqual(second_version, first_version)
            self.assertEqual(third["assets_changed"], 1)
            self.assertNotEqual(marker.read_text(encoding="utf-8"), first_version)
            self.assertTrue(
                (consumer_root / ".github" / "hooks" / "lib" / "framework.py").is_file()
            )
            settings = json.loads(
                (consumer_root / ".claude" / "settings.json").read_text(encoding="utf-8")
            )
            generated = settings["hooks"]["PreToolUse"][0]
            self.assertEqual(generated["matcher"], "Read|Write|Bash")
            self.assertEqual(generated["$source"], "file-access-guard")
            self.assertEqual(
                generated["hooks"][0]["command"],
                "python3 .github/hooks/scripts/file-access-guard.py",
            )

    def test_hook_propagation_rejects_missing_runtime_asset(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            source_root = self._make_hook_source(tmp_root / "source")
            (source_root / ".github" / "hooks" / "scripts" / "file-access-guard.py").unlink()

            with self.assertRaisesRegex(
                FileNotFoundError, "generated hook command references missing asset"
            ):
                mod.propagate_hooks_once(
                    repo_root=tmp_root / "consumer", source_root=source_root
                )

    def test_propagated_guard_runs_from_detached_consumer_without_dependencies(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            consumer_root = Path(tmp_dir) / "consumer"
            mod.propagate_hooks_once(repo_root=consumer_root, source_root=REPO_ROOT)
            command = json.loads(
                (consumer_root / ".claude" / "settings.json").read_text(encoding="utf-8")
            )["hooks"]["PreToolUse"]
            guard_entry = next(
                entry for entry in command if entry.get("$source") == "file-access-guard"
            )

            completed = subprocess.run(
                guard_entry["hooks"][0]["command"].split(),
                input=json.dumps(
                    {
                        "tool_name": "Read",
                        "tool_input": {"file_path": ".env"},
                        "cwd": str(consumer_root),
                    }
                ),
                text=True,
                capture_output=True,
                cwd=consumer_root,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            decision = json.loads(completed.stdout)
            self.assertEqual(
                decision["hookSpecificOutput"]["permissionDecision"], "deny"
            )

    def test_generate_global_hooks_uses_absolute_source_commands(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            source_root = self._make_hook_source(tmp_root / "source with spaces")
            output_root = tmp_root / "generated"

            mod.generate_global_hooks(output_root, source_root=source_root)

            settings = json.loads(
                (output_root / ".claude" / "settings.json").read_text(
                    encoding="utf-8"
                )
            )
            command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            self.assertIn(
                str(
                    source_root
                    / ".github"
                    / "hooks"
                    / "scripts"
                    / "file-access-guard.py"
                ),
                command,
            )
            self.assertNotIn("python3 .github/hooks/", command)
            self.assertFalse((output_root / ".github" / "hooks").exists())

    def test_global_setup_backs_up_user_files_and_installs_regular_outputs(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            home = tmp_root / "home"
            output_root = tmp_root / "global-output"
            claude_dir = home / ".claude"
            claude_dir.mkdir(parents=True)
            original = '{"user_setting": true}\n'
            (claude_dir / "settings.json").write_text(original, encoding="utf-8")
            env = {
                "HOME": str(home),
                "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
                "HOOK_GLOBAL_OUTPUT_DIR": str(output_root),
            }

            first = subprocess.run(
                ["bash", str(REPO_ROOT / "scripts" / "setup-hook-symlinks.sh")],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            second = subprocess.run(
                ["bash", str(REPO_ROOT / "scripts" / "setup-hook-symlinks.sh")],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            installed = claude_dir / "settings.json"
            self.assertTrue(installed.is_file())
            self.assertFalse(installed.is_symlink())
            self.assertEqual(
                (claude_dir / "settings.json.backup").read_text(encoding="utf-8"),
                original,
            )
            self.assertIn(str(REPO_ROOT), installed.read_text(encoding="utf-8"))

    def test_hook_regeneration_preserves_user_wiring_and_cleans_owned_stale_output(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            source_root = self._make_hook_source(tmp_root / "source")
            consumer_root = tmp_root / "consumer"
            claude_settings = consumer_root / ".claude" / "settings.json"
            claude_settings.parent.mkdir(parents=True)
            claude_settings.write_text(
                json.dumps(
                    {
                        "user_setting": True,
                        "hooks": {
                            "PreToolUse": [
                                {
                                    "matcher": "UserOwned",
                                    "hooks": [{"type": "command", "command": "user-hook"}],
                                },
                                {
                                    "matcher": "",
                                    "$source": "stale-generated",
                                    "hooks": [{"type": "command", "command": "stale"}],
                                },
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            plugins = consumer_root / ".opencode" / "plugins"
            plugins.mkdir(parents=True)
            (plugins / "user-owned.js").write_text("// user owned\n", encoding="utf-8")
            (plugins / "stale-generated.js").write_text(
                mod.GENERATED_OPENCODE_PLUGIN_HEADER + "export const Stale = {}\n",
                encoding="utf-8",
            )

            mod.propagate_hooks_once(
                repo_root=consumer_root, source_root=source_root
            )

            settings = json.loads(claude_settings.read_text(encoding="utf-8"))
            entries = settings["hooks"]["PreToolUse"]
            self.assertTrue(settings["user_setting"])
            self.assertEqual(
                [entry["matcher"] for entry in entries if "$source" not in entry],
                ["UserOwned"],
            )
            generated = next(
                entry for entry in entries if entry.get("$source") == "file-access-guard"
            )
            self.assertEqual(generated["matcher"], "Read|Write|Bash")
            self.assertTrue((plugins / "user-owned.js").is_file())
            self.assertFalse((plugins / "stale-generated.js").exists())
            plugin = (plugins / "file-access-guard.js").read_text(encoding="utf-8")
            self.assertTrue(plugin.startswith(mod.GENERATED_OPENCODE_PLUGIN_HEADER))
            self.assertIn('"tool.execute.before"', plugin)

    def test_hook_regeneration_removes_only_known_retired_runtime_assets(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            source_root = self._make_hook_source(tmp_root / "source")
            consumer_root = tmp_root / "consumer"
            scripts = consumer_root / ".github" / "hooks" / "scripts"
            scripts.mkdir(parents=True)
            retired = scripts / "protect-files.py"
            user_owned = scripts / "consumer-custom.py"
            retired.write_text("# old generated guard\n", encoding="utf-8")
            user_owned.write_text("# user owned\n", encoding="utf-8")

            result = mod.propagate_hooks_once(
                repo_root=consumer_root, source_root=source_root
            )

            self.assertEqual(result["retired_assets_removed"], 1)
            self.assertFalse(retired.exists())
            self.assertTrue(user_owned.is_file())

    def test_hook_asset_copy_replaces_symlink_without_writing_through_it(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            tmp_root = Path(tmp_dir)
            source_root = self._make_hook_source(tmp_root / "source")
            consumer_root = tmp_root / "consumer"
            target = (
                consumer_root
                / ".github"
                / "hooks"
                / "scripts"
                / "file-access-guard.py"
            )
            target.parent.mkdir(parents=True)
            outside = tmp_root / "outside.py"
            outside.write_text("# must remain unchanged\n", encoding="utf-8")
            target.symlink_to(outside)

            mod.propagate_hooks_once(
                repo_root=consumer_root, source_root=source_root
            )

            self.assertFalse(target.is_symlink())
            self.assertEqual(
                outside.read_text(encoding="utf-8"), "# must remain unchanged\n"
            )


if __name__ == "__main__":
    unittest.main()
