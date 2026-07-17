import hashlib
import json
import re
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod
import _propagate_env as env

# The settled PR Review evaluator roster, and each agent's exact tool grant.
#
# This map is the propagation-enumeration ledger. `test_pr_review_evaluator_roster
# _is_fully_enumerated` asserts it covers every `05*` evaluator on disk, so an
# agent can no longer be dropped from enumeration to dodge an assertion about it.
# That is precisely how the previous gap arose: `05a`, `05g`, `05j` and `05k` were
# all omitted from the old `expected_slugs` tuple because they held `execute` and
# would have failed its blanket `assertNotIn("execute", ...)`. Omission was free,
# so omission happened. It is no longer free.
#
# Exact lists replace that blanket assertion. A grant change is now a deliberate
# edit here rather than a silent widening, and the two directions that assertion
# could not express are both covered:
#
#   * `edit` is REQUIRED by every evaluator that writes its own report. The bodies
#     say "read-only, never remediate", which reads as license to strip `edit` --
#     doing so would break the report contract. Pinned here so that fails.
#   * `execute` is DECLARED, not hidden. It survives only on `05a-baseline-worktree`,
#     whose `git worktree` call has no non-shell equivalent; the grant is recorded
#     as explicitly unclosable in `.github/learnings/cross-phase-decisions.md:16`.
#     Per-agent command scoping is not expressible in Claude subagent frontmatter
#     (`tools: Bash(gh:*)` is an unresolved tool name, not a narrower grant), so
#     removal is the only narrowing available -- and this one cannot be removed.
#     Listing it is the honest outcome: visible and justified beats absent.
PR_REVIEW_EVALUATOR_TOOLS = {
    "05a-baseline-worktree": ["read", "search", "execute"],
    "05b-change-narrator": ["agent", "read", "search", "edit"],
    "05c-artifact-sweeper": ["read", "search", "edit"],
    "05d-consistency-auditor": ["read", "search", "edit"],
    "05e-dependency-auditor": ["read", "search", "edit"],
    "05f-test-health": ["agent", "read", "search", "edit"],
    "05g-readiness-synthesizer": ["read", "search", "edit"],
}


def _discover_pr_review_evaluator_slugs() -> set:
    """Every `05`-family evaluator on disk, read from the source of truth.

    Derived rather than restated: this is what makes omission from
    `PR_REVIEW_EVALUATOR_TOOLS` fail instead of silently narrowing coverage.
    `05-pr-review` is the orchestrator that dispatches the roster, not a member
    of it.
    """
    agents_dir = REPO_ROOT / ".github" / "agents"
    return {
        path.name[: -len(".agent.md")]
        for path in agents_dir.glob("05*.agent.md")
        if path.name != "05-pr-review.agent.md"
    }


class PropagateMasterAssetsTests(unittest.TestCase):
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
            env.use(self, repo_root)
            skill_dir = repo_root / ".github" / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: \"Demo skill\"\n---\n# Demo body\n",
                encoding="utf-8",
            )

            result = mod.propagate_skills_once()

            self.assertEqual(result["claude_changed"], 1)
            self.assertEqual(result["opencode_changed"], 1)
            self.assertEqual(result["codex_changed"], 1)
            self.assertTrue((repo_root / "claude" / "skills" / "demo-skill" / "SKILL.md").exists())
            self.assertTrue((repo_root / "opencode" / "skills" / "demo-skill" / "SKILL.md").exists())
            self.assertTrue((repo_root / "codex" / "skills" / "demo-skill" / "SKILL.md").exists())

    def test_pr_review_evaluator_roster_is_fully_enumerated(self) -> None:
        """AC8: no evaluator may be omitted from propagation enumeration.

        The enumeration gap this closes was not a typo -- it was structural. The
        old tuple asserted `assertNotIn("execute", agent.tools)` over a
        hand-listed roster, so the four agents holding `execute` were simply left
        out of the list, and nothing failed. Coverage narrowed silently and the
        grants went unexamined.

        Deriving the roster from disk inverts that: adding a `05*` evaluator
        without a tool expectation fails here, and so does deleting one without
        removing its entry.
        """
        self.assertEqual(
            set(PR_REVIEW_EVALUATOR_TOOLS), _discover_pr_review_evaluator_slugs()
        )

    def test_pr_review_evaluator_tool_grants_match_expected_lists(self) -> None:
        """AC3/AC4/AC8b/AC8c: exact per-agent grants, not a blanket prohibition.

        Replaces the old `assertNotIn("execute", agent.tools)`. Exact equality
        catches a widening (`execute` reappearing on a sweeper) and a narrowing
        (`edit` stripped from an agent that must write its own report) in the
        same assertion.
        """
        agents = {agent.source_slug: agent for agent in mod.load_source_agents()}

        for slug, expected_tools in PR_REVIEW_EVALUATOR_TOOLS.items():
            with self.subTest(slug=slug):
                self.assertEqual(agents[slug].tools, expected_tools)

    def test_phase_review_agents_match_all_generated_harness_outputs(self) -> None:
        agents = {agent.source_slug: agent for agent in mod.load_source_agents()}
        instructions = mod.load_instruction_docs()
        expected_slugs = tuple(sorted(PR_REVIEW_EVALUATOR_TOOLS))

        claude_stems = mod._discover_existing_stems(mod.CLAUDE_AGENTS_DIR)
        opencode_stems = mod._discover_existing_stems(mod.OPENCODE_AGENTS_DIR)
        claude_references = mod._build_agent_reference_map(
            list(agents.values()),
            lambda agent: mod._claude_identifier_for(agent, claude_stems),
        )
        opencode_references = mod._build_agent_reference_map(
            list(agents.values()),
            lambda agent: mod._opencode_identifier_for(agent, opencode_stems),
        )
        codex_references = mod._build_agent_reference_map(
            list(agents.values()), mod._codex_identifier_for
        )

        for slug in expected_slugs:
            with self.subTest(slug=slug):
                agent = agents[slug]
                # Tool grants are asserted per-agent in
                # `test_pr_review_evaluator_tool_grants_match_expected_lists`.
                docs = mod.applicable_instructions(agent, instructions)

                claude_identifier = mod._claude_identifier_for(agent, claude_stems)
                claude_path = mod.CLAUDE_AGENTS_DIR / f"{claude_identifier}.md"
                self.assertEqual(
                    mod.render_claude_agent(
                        agent, docs, claude_references, claude_identifier
                    ),
                    claude_path.read_text(encoding="utf-8"),
                )

                opencode_path = mod.OPENCODE_AGENTS_DIR / mod._opencode_filename_for(
                    agent, opencode_stems
                )
                self.assertEqual(
                    mod.render_opencode_agent(agent, docs, opencode_references),
                    opencode_path.read_text(encoding="utf-8"),
                )

                codex_path = mod.CODEX_AGENTS_DIR / mod._codex_filename_for(agent)
                self.assertEqual(
                    mod.render_codex_agent(agent, docs, codex_references),
                    codex_path.read_text(encoding="utf-8"),
                )

    def test_evangelize_matches_every_generated_harness_variant(self) -> None:
        agents = {agent.source_slug: agent for agent in mod.load_source_agents()}
        instructions = mod.load_instruction_docs()
        agent = agents["evangelize"]
        docs = mod.applicable_instructions(agent, instructions)
        claude_stems = mod._discover_existing_stems(mod.CLAUDE_AGENTS_DIR)
        opencode_stems = mod._discover_existing_stems(mod.OPENCODE_AGENTS_DIR)
        claude_references = mod._build_agent_reference_map(
            list(agents.values()),
            lambda item: mod._claude_identifier_for(item, claude_stems),
        )
        opencode_references = mod._build_agent_reference_map(
            list(agents.values()),
            lambda item: mod._opencode_identifier_for(item, opencode_stems),
        )
        codex_references = mod._build_agent_reference_map(
            list(agents.values()), mod._codex_identifier_for
        )

        claude_identifier = mod._claude_identifier_for(agent, claude_stems)
        self.assertEqual(
            mod.render_claude_command(
                agent, docs, claude_references, claude_identifier
            ),
            (mod.CLAUDE_COMMANDS_DIR / "evangelize.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            mod.render_opencode_agent(agent, docs, opencode_references),
            (mod.OPENCODE_AGENTS_DIR / "evangelize.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            mod.render_codex_agent(agent, docs, codex_references),
            (mod.CODEX_AGENTS_DIR / "evangelize.toml").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            mod.render_codex_profile(agent, docs, codex_references),
            (mod.CODEX_PROFILES_DIR / "evangelize.config.toml").read_text(
                encoding="utf-8"
            ),
        )

    def test_diff_security_scan_agent_matches_all_generated_harness_outputs(self) -> None:
        agents = {agent.source_slug: agent for agent in mod.load_source_agents()}
        instructions = mod.load_instruction_docs()

        agent = agents["04e-diff-security-scan"]
        self.assertFalse(agent.user_invocable)
        self.assertNotIn("execute", agent.tools)
        self.assertIn("BLOCKED", agent.body)
        self.assertIn("OUT OF SCOPE", agent.body)
        docs = mod.applicable_instructions(agent, instructions)

        claude_stems = mod._discover_existing_stems(mod.CLAUDE_AGENTS_DIR)
        opencode_stems = mod._discover_existing_stems(mod.OPENCODE_AGENTS_DIR)
        claude_references = mod._build_agent_reference_map(
            list(agents.values()),
            lambda a: mod._claude_identifier_for(a, claude_stems),
        )
        opencode_references = mod._build_agent_reference_map(
            list(agents.values()),
            lambda a: mod._opencode_identifier_for(a, opencode_stems),
        )
        codex_references = mod._build_agent_reference_map(
            list(agents.values()), mod._codex_identifier_for
        )

        claude_identifier = mod._claude_identifier_for(agent, claude_stems)
        self.assertEqual(claude_identifier, "z-diff-security-scan")
        claude_path = mod.CLAUDE_AGENTS_DIR / f"{claude_identifier}.md"
        self.assertEqual(
            mod.render_claude_agent(agent, docs, claude_references, claude_identifier),
            claude_path.read_text(encoding="utf-8"),
        )

        opencode_path = mod.OPENCODE_AGENTS_DIR / mod._opencode_filename_for(
            agent, opencode_stems
        )
        self.assertEqual(opencode_path.name, "04e-diff-security-scan.md")
        self.assertEqual(
            mod.render_opencode_agent(agent, docs, opencode_references),
            opencode_path.read_text(encoding="utf-8"),
        )

        codex_path = mod.CODEX_AGENTS_DIR / mod._codex_filename_for(agent)
        self.assertEqual(codex_path.name, "z-diff-security-scan.toml")
        self.assertEqual(
            mod.render_codex_agent(agent, docs, codex_references),
            codex_path.read_text(encoding="utf-8"),
        )

    def test_pr_review_agent_is_present_in_all_harness_outputs(self) -> None:
        # Renamed from `05 Phase - Final Review` by the PR-Review rescope. The
        # Claude output is a *command*, not an agent: this orchestrator is
        # user-invocable.
        expected_markers = {
            ".github/agents/05-pr-review.agent.md": "name: 05 PR - Review",
            "claude/commands/pr-review.md": "PR Review Orchestrator",
            "opencode/agents/05-pr-review.md": "PR Review Orchestrator",
            "codex/agents/05-pr-review.toml": 'name = "pr-review"',
            "codex/profiles/pr-review.config.toml": "PR Review Orchestrator",
        }

        for relative_path, marker in expected_markers.items():
            with self.subTest(path=relative_path):
                output = REPO_ROOT / relative_path
                self.assertTrue(output.is_file(), relative_path)
                self.assertIn(marker, output.read_text(encoding="utf-8"))

    def test_no_generated_body_references_an_agent_by_unrewritten_slug(self) -> None:
        # `_build_agent_reference_map` keys on `agent.name` -- the display name --
        # so a source body that names a sibling by *slug* matches nothing and the
        # rewrite silently no-ops. The slug then ships verbatim into Claude and
        # Codex, where that agent is filed as `z-<stem>`, and the fan-out points at
        # a file that does not exist. Nothing failed when this happened: every
        # per-feature test verified its own agent in isolation, and no test asserted
        # that a reference resolves in the root it lands in.
        #
        # A bare backticked token equal to a source slug is the signature -- but
        # only where that root *renames* the agent. Most slugs survive unchanged
        # (`prod-code-review` is both the slug and the Claude filename), so those
        # references resolve and are not defects. The defect is a slug whose
        # identifier in that root differs, which is exactly the set the rewrite was
        # supposed to translate and didn't.
        #
        # Exact equality is what keeps this honest: `05b-change-narrator-report.md`
        # (a report filename) and `.github/agents/04-phase-execute.agent.md` (a
        # path) both contain a slug as a substring and must not trip it.
        #
        # `claude/agents/README.md` is hand-maintained inside a generated root -- it
        # documents the slug-to-filename mapping on purpose and is never rewritten.
        agents = mod.load_source_agents()

        claude_stems = mod._discover_existing_stems(mod.CLAUDE_AGENTS_DIR)
        renamed_in_claude = {
            agent.source_slug
            for agent in agents
            if mod._claude_identifier_for(agent, claude_stems) != agent.source_slug
        }
        renamed_in_codex = {
            agent.source_slug
            for agent in agents
            if mod._codex_identifier_for(agent) != agent.source_slug
        }

        renaming_roots = (
            (REPO_ROOT / "claude" / "agents", "*.md", renamed_in_claude),
            (REPO_ROOT / "claude" / "commands", "*.md", renamed_in_claude),
            (REPO_ROOT / "codex" / "agents", "*.toml", renamed_in_codex),
        )

        offenders = []
        for directory, pattern, renamed in renaming_roots:
            for output in sorted(directory.glob(pattern)):
                if output.name == "README.md":
                    continue
                text = output.read_text(encoding="utf-8")
                for token in set(re.findall(r"`([^`\n]+)`", text)):
                    if token in renamed:
                        offenders.append(f"{output.relative_to(REPO_ROOT)} -> `{token}`")

        self.assertEqual(
            [],
            sorted(offenders),
            "generated bodies reference agents by slug; these do not resolve in a "
            "root that files agents as `z-<stem>`. Name the sibling by its display "
            "name in the source so the reference map can rewrite it.",
        )


class PropagationConvergenceTests(unittest.TestCase):
    def test_convergence_requires_an_immediate_zero_change_pass(self) -> None:
        passes = [
            {"source_agents": 2, "claude_changed": 2},
            {"source_agents": 2, "codex_changed": 1},
            {"source_agents": 2, "claude_changed": 0},
        ]

        result = mod.propagate_until_converged(
            max_passes=4, propagate=lambda: passes.pop(0)
        )

        self.assertTrue(result.converged)
        self.assertEqual(result.pass_count, 3)
        self.assertEqual(result.changed_passes, 2)
        self.assertEqual(result.total_changes["claude_changed"], 2)
        self.assertEqual(result.total_changes["codex_changed"], 1)

    def test_convergence_rejects_invalid_bounds(self) -> None:
        for bound in (0, -1, mod.MAX_CONVERGENCE_PASSES + 1, True):
            with self.subTest(bound=bound), self.assertRaises(ValueError):
                mod.propagate_until_converged(max_passes=bound, propagate=lambda: {})

    def test_convergence_fails_closed_for_exception_and_malformed_result(self) -> None:
        with self.assertRaises(mod.PropagationConvergenceError) as raised:
            mod.propagate_until_converged(
                max_passes=2,
                propagate=mock.Mock(side_effect=RuntimeError("private/path")),
            )
        self.assertEqual(raised.exception.category, "propagation_failed")
        self.assertNotIn("private/path", str(raised.exception))

        with self.assertRaises(mod.PropagationConvergenceError) as raised:
            mod.propagate_until_converged(
                max_passes=2, propagate=lambda: {"claude_changed": "one"}
            )
        self.assertEqual(raised.exception.category, "malformed_result")

    def test_convergence_exhaustion_includes_pass_count(self) -> None:
        with self.assertRaises(mod.PropagationConvergenceError) as raised:
            mod.propagate_until_converged(
                max_passes=2, propagate=lambda: {"claude_changed": 1}
            )
        self.assertEqual(raised.exception.category, "bound_exhausted")
        self.assertEqual(raised.exception.pass_count, 2)

    def test_preflight_rejects_unsafe_destinations_before_any_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            home.mkdir()
            outside = Path(tmp) / "outside"
            outside.mkdir()
            (home / "linked").symlink_to(outside, target_is_directory=True)
            targets = (
                mod.HarnessDestination("claude", home / "claude"),
                mod.HarnessDestination("codex", home / "linked" / "codex"),
            )
            copy = mock.Mock()

            result = mod.deploy_after_convergence(
                targets,
                copy_operation=copy,
                reconcile_operation=mock.Mock(),
                home=home,
                propagate=lambda: {"source_agents": 1, "claude_changed": 0},
            )

        self.assertFalse(result.preflight_succeeded)
        self.assertEqual(result.preflight_failures["codex"], "outside_active_home")
        copy.assert_not_called()

    def test_preflight_reports_missing_parent_evidence_and_collision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            targets = (
                mod.HarnessDestination(
                    "claude", home / "missing" / "claude", create_parents=False
                ),
                mod.HarnessDestination(
                    "codex", home / "codex", ownership_evidence_available=False
                ),
                mod.HarnessDestination(
                    "opencode", home / "opencode", collision_ready=False
                ),
            )

            failures = mod.preflight_destinations(targets, home=home)

        self.assertEqual(failures["claude"], "missing_parent_not_allowed")
        self.assertEqual(failures["codex"], "ownership_evidence_unavailable")
        self.assertEqual(failures["opencode"], "collision_not_ready")

    def test_preflight_rejects_non_directory_parent_before_any_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            blocked_parent = home / "blocked"
            blocked_parent.write_text("not a directory", encoding="utf-8")
            targets = (
                mod.HarnessDestination("claude", home / "claude"),
                mod.HarnessDestination("codex", blocked_parent / "codex"),
            )
            copy = mock.Mock()

            result = mod.deploy_after_convergence(
                targets,
                copy_operation=copy,
                reconcile_operation=mock.Mock(),
                home=home,
                propagate=lambda: {"source_agents": 1, "claude_changed": 0},
            )

        self.assertFalse(result.preflight_succeeded)
        self.assertEqual(result.preflight_failures["codex"], "parent_not_directory")
        copy.assert_not_called()

    def test_failed_harness_skips_only_its_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            targets = (
                mod.HarnessDestination("claude", home / "claude"),
                mod.HarnessDestination("codex", home / "codex"),
            )
            reconciled = []

            def copy(target: mod.HarnessDestination) -> int:
                if target.harness == "codex":
                    raise OSError("sensitive destination")
                target.destination.mkdir()
                return 2

            result = mod.deploy_after_convergence(
                targets,
                copy_operation=copy,
                reconcile_operation=lambda target: reconciled.append(target.harness) or 1,
                home=home,
                propagate=lambda: {"source_agents": 1, "claude_changed": 0},
            )

        self.assertEqual(result.harnesses["claude"].status, "verified")
        self.assertEqual(result.harnesses["claude"].copied, 2)
        self.assertFalse(result.harnesses["claude"].reconciliation_skipped)
        self.assertEqual(result.harnesses["codex"].status, "failed")
        self.assertTrue(result.harnesses["codex"].reconciliation_skipped)
        self.assertEqual(reconciled, ["claude"])
        self.assertNotIn("sensitive destination", result.harnesses["codex"].failure)

    def test_watcher_announces_restart_requirement(self) -> None:
        convergence = mod.PropagationConvergenceResult(True, 1, 0, {}, {})
        with mock.patch.object(mod, "propagate_until_converged", return_value=convergence), \
             mock.patch.object(mod, "_collect_file_state", return_value={}), \
             mock.patch.object(mod.time, "sleep", side_effect=KeyboardInterrupt), \
             mock.patch("builtins.print") as printed:
            with self.assertRaises(KeyboardInterrupt):
                mod.watch_loop()
        output = " ".join(str(call.args[0]) for call in printed.call_args_list)
        self.assertIn("restart", output.lower())
        self.assertIn("release verification", output.lower())


class OrphanPruningTests(unittest.TestCase):
    """Pruning of generated outputs whose source asset no longer exists.

    Every test here runs `propagate_once(repo_root=...)` against an isolated
    temp repo. `propagate_once` gained that parameter for exactly this reason:
    it previously resolved every output directory from module constants bound
    to the real `REPO_ROOT` at import time, so a prune test written the obvious
    way would have deleted files from this repository.
    """

    def _write_source_agent(
        self,
        repo_root: Path,
        slug: str,
        name: str,
        user_invocable: bool = False,
    ) -> Path:
        agents_dir = repo_root / ".github" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        path = agents_dir / f"{slug}.agent.md"
        path.write_text(
            "---\n"
            f"name: {name}\n"
            f'description: "Fixture agent {slug}."\n'
            "tools: [read, search]\n"
            f"user-invocable: {'true' if user_invocable else 'false'}\n"
            "---\n"
            "\n"
            f"You are the **{name}** fixture agent.\n",
            encoding="utf-8",
        )
        return path

    def _write_source_skill(self, repo_root: Path, skill_name: str) -> Path:
        skill_dir = repo_root / ".github" / "skills" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {skill_name}\ndescription: \"Fixture skill.\"\n---\n"
            f"# {skill_name} body\n",
            encoding="utf-8",
        )
        return skill_dir

    def test_orphaned_claude_and_opencode_agents_are_pruned(self) -> None:
        """AC1 + AC3: outputs survive their source agent's deletion today."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")
            doomed = self._write_source_agent(repo_root, "02-doomed", "02 Doomed")

            mod.propagate_once(verbose=False)

            claude_orphan = repo_root / "claude" / "agents" / "z-doomed.md"
            opencode_orphan = repo_root / "opencode" / "agents" / "02-doomed.md"
            self.assertTrue(claude_orphan.exists(), "fixture: expected generated output")
            self.assertTrue(opencode_orphan.exists(), "fixture: expected generated output")

            doomed.unlink()
            result = mod.propagate_once(verbose=False)

            self.assertFalse(claude_orphan.exists())
            self.assertFalse(opencode_orphan.exists())
            self.assertTrue((repo_root / "claude" / "agents" / "z-keeper.md").exists())
            self.assertTrue((repo_root / "opencode" / "agents" / "01-keeper.md").exists())
            self.assertEqual(result["claude_orphans_removed"], 1)
            self.assertEqual(result["opencode_orphans_removed"], 1)

    def test_hand_maintained_file_in_generated_root_survives(self) -> None:
        """AC5: the critical guard. `claude/agents/README.md` is a real, hand-
        maintained file living inside a pruned root. It carries no generated
        marker and is in no expected set, so only the marker guard saves it.
        This test must fail if that guard is removed."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")
            claude_agents = repo_root / "claude" / "agents"
            claude_agents.mkdir(parents=True, exist_ok=True)
            readme = claude_agents / "README.md"
            readme.write_text("# Agent index\n\nHand-maintained.\n", encoding="utf-8")

            result = mod.propagate_once(verbose=False)

            self.assertTrue(readme.exists(), "hand-maintained README.md was deleted")
            self.assertEqual(readme.read_text(encoding="utf-8"), "# Agent index\n\nHand-maintained.\n")
            self.assertEqual(result["claude_orphans_removed"], 0)

    def test_orphaned_command_is_pruned_and_subagent_file_retained(self) -> None:
        """AC2: an agent flipped to `user-invocable: false` loses its command
        file but keeps its subagent file."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-flipper", "01 Flipper", user_invocable=True)

            mod.propagate_once(verbose=False)
            command_file = repo_root / "claude" / "commands" / "flipper.md"
            self.assertTrue(command_file.exists(), "fixture: expected a command file")

            self._write_source_agent(repo_root, "01-flipper", "01 Flipper", user_invocable=False)
            result = mod.propagate_once(verbose=False)

            self.assertFalse(command_file.exists())
            # A non-invocable agent takes the `z-` prefix, so the subagent file it
            # gains on the flip is `z-flipper.md`.
            self.assertTrue((repo_root / "claude" / "agents" / "z-flipper.md").exists())
            self.assertEqual(result["claude_command_orphans_removed"], 1)

    def test_emission_completes_before_pruning(self) -> None:
        """AC6: `_claude_filename_for` resolves an output name against stems
        already on disk, so pruning before emission could rename a survivor."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "05c-artifact-sweeper", "05c Artifact Sweeper")
            doomed = self._write_source_agent(repo_root, "09-doomed", "09 Doomed")

            mod.propagate_once(verbose=False)
            survivor = repo_root / "claude" / "agents" / "z-artifact-sweeper.md"
            self.assertTrue(survivor.exists(), "fixture: expected the z- stem")

            doomed.unlink()
            mod.propagate_once(verbose=False)

            self.assertTrue(survivor.exists(), "survivor lost its stem to prune ordering")
            self.assertFalse((repo_root / "claude" / "agents" / "z-doomed.md").exists())
            self.assertFalse((repo_root / "opencode" / "agents" / "09-doomed.md").exists())

    def test_orphaned_skill_directories_are_pruned_in_all_three_roots(self) -> None:
        """AC4: no root pruned skills before this feature. The `codex/skills/`
        guard existed but never matched (marker sits below frontmatter, and it
        used a prefix check); Claude and OpenCode had no prune at all."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_skill(repo_root, "keeper-skill")
            doomed = self._write_source_skill(repo_root, "doomed-skill")

            mod.propagate_once(verbose=False)
            orphans = [
                repo_root / "claude" / "skills" / "doomed-skill",
                repo_root / "opencode" / "skills" / "doomed-skill",
                repo_root / "codex" / "skills" / "doomed-skill",
            ]
            for orphan in orphans:
                self.assertTrue(orphan.exists(), f"fixture: expected {orphan}")

            shutil.rmtree(doomed)
            mod.propagate_once(verbose=False)

            for orphan in orphans:
                self.assertFalse(orphan.exists(), f"orphaned skill dir survived: {orphan}")
            for root in ("claude", "opencode", "codex"):
                self.assertTrue((repo_root / root / "skills" / "keeper-skill" / "SKILL.md").exists())

    def test_unmarked_skill_directory_survives(self) -> None:
        """AC5 for the skill roots: a skill directory this propagator did not
        generate carries no marker and must never be swept."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_skill(repo_root, "keeper-skill")
            handmade = repo_root / "claude" / "skills" / "handmade-skill"
            handmade.mkdir(parents=True, exist_ok=True)
            (handmade / "SKILL.md").write_text(
                "---\nname: handmade-skill\n---\n# Hand written\n", encoding="utf-8"
            )

            mod.propagate_once(verbose=False)

            self.assertTrue((handmade / "SKILL.md").exists())

    def test_symlinked_orphan_is_not_unlinked(self) -> None:
        """A symlink is never something this propagator wrote. Following one
        would reach a real tree outside the generated root."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")
            outside = repo_root / "outside.md"
            outside.write_text(
                f"---\nname: outside\n---\n{mod.GENERATED_AGENT_MARKDOWN_HEADER}\nreal file\n",
                encoding="utf-8",
            )
            claude_agents = repo_root / "claude" / "agents"
            claude_agents.mkdir(parents=True, exist_ok=True)
            link = claude_agents / "z-linked.md"
            link.symlink_to(outside)

            mod.propagate_once(verbose=False)

            self.assertTrue(outside.exists(), "prune followed a symlink into a real file")
            self.assertTrue(link.is_symlink())

    def test_prune_refuses_a_generated_root_symlinked_outside_the_repo(self) -> None:
        """P3-SEC-01. Guarding the leaf is not enough; the ROOT must be contained.

        `test_symlinked_orphan_is_not_unlinked` covers a symlinked *file* inside a
        real root. This is the inverse and the dangerous one: the root itself is the
        symlink, so every child is an ordinary marker-bearing file that passes every
        leaf check, and the prune unlinks it outside the repository. A bad write can
        be undone by re-running propagation; a bad delete cannot.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            env.use(self, repo_root)
            repo_root.mkdir()
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")

            outside = Path(tmp_dir) / "outside"
            outside.mkdir()
            victim = outside / "z-victim.md"
            victim.write_text(
                f"---\nname: victim\n---\n{mod.GENERATED_AGENT_MARKDOWN_HEADER}\nreal file\n",
                encoding="utf-8",
            )

            claude_dir = repo_root / "claude"
            claude_dir.mkdir()
            (claude_dir / "agents").symlink_to(outside, target_is_directory=True)

            with self.assertRaises(ValueError):
                mod.propagate_once(verbose=False)

            self.assertTrue(victim.exists(), "prune deleted a file outside the repo root")

    def test_prune_refuses_a_skills_root_symlinked_outside_the_repo(self) -> None:
        """P3-SEC-01, recursive form -- the wider blast radius of the two.

        The marker guard reads one file (`SKILL.md`), but `shutil.rmtree` removes the
        whole tree: every sibling of that marker is deleted without ever being
        inspected. A symlinked skills root trades a single marker for an entire
        directory outside the repository.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            env.use(self, repo_root)
            (repo_root / ".github" / "skills").mkdir(parents=True)

            outside = Path(tmp_dir) / "outside"
            precious = outside / "precious-skill"
            precious.mkdir(parents=True)
            (precious / "SKILL.md").write_text(
                f"---\nname: precious\n---\n{mod.GENERATED_SKILL_HEADER}\n", encoding="utf-8"
            )
            never_inspected = precious / "irreplaceable.txt"
            never_inspected.write_text("carries no marker; rmtree does not care\n", encoding="utf-8")

            claude_dir = repo_root / "claude"
            claude_dir.mkdir()
            (claude_dir / "skills").symlink_to(outside, target_is_directory=True)

            with self.assertRaises(ValueError):
                mod.propagate_skills_once()

            self.assertTrue(precious.exists(), "rmtree removed a tree outside the repo root")
            self.assertTrue(never_inspected.exists())

    def test_prune_refuses_a_root_escaping_through_a_symlinked_parent(self) -> None:
        """The nested-destination form: the leaf directory is real, its PARENT is not.

        This is SEC-01's shape (already fixed once for writes) applied to deletes. A
        check that only asks `directory.is_symlink()` passes here and deletes outside
        the repo anyway; only resolving the whole path catches it.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            env.use(self, repo_root)
            repo_root.mkdir()
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")

            outside = Path(tmp_dir) / "outside"
            (outside / "agents").mkdir(parents=True)
            victim = outside / "agents" / "z-victim.md"
            victim.write_text(
                f"---\nname: victim\n---\n{mod.GENERATED_AGENT_MARKDOWN_HEADER}\nreal file\n",
                encoding="utf-8",
            )

            # `claude` is the symlink; `claude/agents` is a real directory beyond it.
            (repo_root / "claude").symlink_to(outside, target_is_directory=True)
            self.assertFalse((repo_root / "claude" / "agents").is_symlink())

            with self.assertRaises(ValueError):
                mod.propagate_once(verbose=False)

            self.assertTrue(victim.exists(), "prune escaped through a symlinked parent")

    def test_unreadable_orphan_is_not_deleted(self) -> None:
        """An unreadable file is not a confirmed orphan — fail closed."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")
            claude_agents = repo_root / "claude" / "agents"
            claude_agents.mkdir(parents=True, exist_ok=True)
            unreadable = claude_agents / "z-unreadable.md"
            unreadable.write_text("whatever\n", encoding="utf-8")
            unreadable.chmod(0o000)
            try:
                mod.propagate_once(verbose=False)
                self.assertTrue(unreadable.exists())
            finally:
                # Restore before the temp root is torn down.
                unreadable.chmod(0o644)

    def test_missing_generated_root_is_not_created_to_prune_it(self) -> None:
        """A missing root has nothing to prune; never create one to sweep it."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            (repo_root / ".github" / "agents").mkdir(parents=True)

            result = mod.propagate_once(verbose=False)

            self.assertEqual(result["claude_orphans_removed"], 0)
            self.assertEqual(result["skill_orphans_removed"], 0)
            self.assertFalse((repo_root / "claude" / "skills").exists())

    def test_hand_maintained_file_quoting_the_marker_survives(self) -> None:
        """AC5: the marker guard keys on the one position the emitter writes to,
        not on the marker appearing anywhere in the file. A hand-maintained doc
        that *quotes* the marker — e.g. `claude/agents/README.md` explaining the
        convention in a fenced code block — is not a generated file and must not
        be swept. A whole-file search would delete exactly the file AC5 protects.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")
            claude_agents = repo_root / "claude" / "agents"
            claude_agents.mkdir(parents=True, exist_ok=True)
            readme = claude_agents / "README.md"
            body = (
                "# Claude Agents\n\n"
                "Generated files in this directory carry a marker:\n\n"
                "```markdown\n"
                f"{mod.GENERATED_AGENT_MARKDOWN_HEADER}\n"
                "```\n\n"
                "This README is hand-maintained and carries no such marker.\n"
            )
            readme.write_text(body, encoding="utf-8")

            result = mod.propagate_once(verbose=False)

            self.assertTrue(readme.exists(), "a doc quoting the marker was deleted")
            self.assertEqual(readme.read_text(encoding="utf-8"), body)
            self.assertEqual(result["claude_orphans_removed"], 0)

    def test_marker_guard_matches_every_real_generated_file(self) -> None:
        """The guard must still positively identify all real generated output.
        A guard tightened until it matches nothing would make the pruner inert
        and pass AC7 for entirely the wrong reason."""
        # Counts dropped when the five phase-shaped evaluators were retired:
        # claude/agents 33 -> 27 (the five, plus `z-security-scan.md` -- Security
        # Scan lost its spawnable subagent file once `05d` stopped declaring it as
        # a child, and is now a user-invocable command only); opencode/agents and
        # codex/agents 46 -> 41 (the five). Command and profile counts are
        # unchanged: Security Scan's command was renamed, not removed.
        roots = [
            (mod.CLAUDE_AGENTS_DIR, "*.md", mod.GENERATED_AGENT_MARKDOWN_HEADER, 27),
            (mod.CLAUDE_COMMANDS_DIR, "*.md", mod.GENERATED_AGENT_MARKDOWN_HEADER, 19),
            (mod.OPENCODE_AGENTS_DIR, "*.md", mod.GENERATED_AGENT_MARKDOWN_HEADER, 41),
            (mod.CODEX_AGENTS_DIR, "*.toml", mod.GENERATED_AGENT_HEADER, 41),
            (mod.CODEX_PROFILES_DIR, "*.config.toml", mod.GENERATED_AGENT_HEADER, 19),
        ]
        for directory, pattern, marker, expected_count in roots:
            with self.subTest(root=directory.name):
                matched = [
                    p
                    for p in sorted(directory.glob(pattern))
                    if mod._is_generated_output(p, marker)
                ]
                self.assertEqual(len(matched), expected_count)

        # The one remaining unmarked file in claude/agents must stay unmatched.
        # `single-feature.md` was the other, and was deleted by
        # `08-retirement-reconciliation`: it was a stale, unsourced duplicate of
        # `Single Feature - Agent` that Claude Code still loaded. The marker
        # guard could not tell it apart from this README -- both predate the
        # marker -- so the pruner correctly failed closed on both and the call
        # was made by hand. `tests/test_retirement_reconciliation.py::
        # test_claude_agents_root_holds_only_the_catalogue_and_generated_output`
        # now asserts the invariant that leaves README.md as the only exception.
        path = mod.CLAUDE_AGENTS_DIR / "README.md"
        if path.exists():
            self.assertFalse(
                mod._is_generated_output(path, mod.GENERATED_AGENT_MARKDOWN_HEADER)
            )

    def test_renumbered_mechanical_evaluators_left_no_opencode_orphans(self) -> None:
        """AC9: OpenCode agent files key on slug, so a renumber orphans them.

        Claude and Codex key on an existing stem (`z-artifact-sweeper`), which
        survives the renumber untouched; OpenCode does not, so `05g-*.md` would
        linger as a stale duplicate of `05c-*.md` and stay dispatchable.

        Exact stems, deliberately not a `05g-*` glob: feature 07 renumbers the
        readiness synthesizer to `05g-readiness-synthesizer`, so a glob would
        pass today and break the moment that lands -- asserting the opposite of
        what it means.
        """
        retired_stems = (
            "05g-artifact-sweeper",
            "05j-consistency-auditor",
            "05k-dependency-auditor",
        )
        for stem in retired_stems:
            with self.subTest(stem=stem):
                self.assertFalse(
                    (mod.OPENCODE_AGENTS_DIR / f"{stem}.md").exists(),
                    f"retired OpenCode slug survived the renumber: {stem}.md",
                )

        for stem in ("05c-artifact-sweeper", "05d-consistency-auditor",
                     "05e-dependency-auditor"):
            with self.subTest(stem=stem):
                self.assertTrue((mod.OPENCODE_AGENTS_DIR / f"{stem}.md").is_file())

    def test_real_repository_propagation_removes_nothing(self) -> None:
        """AC7: the pruner is proven inert against the current tree before it is
        trusted against a changed one. This asserts on the real repository."""
        result = mod.propagate_once(verbose=False)

        self.assertEqual(result["claude_orphans_removed"], 0)
        self.assertEqual(result["claude_command_orphans_removed"], 0)
        self.assertEqual(result["opencode_orphans_removed"], 0)
        self.assertEqual(result["codex_orphans_removed"], 0)
        self.assertEqual(result["codex_profile_orphans_removed"], 0)
        self.assertEqual(result["skill_orphans_removed"], 0)
        self.assertTrue((mod.CLAUDE_AGENTS_DIR / "README.md").exists())


class StaticDoneNotifyNonInterferenceTests(unittest.TestCase):
    """The propagator no longer owns the done-notify wiring.

    After the hook-emission pipeline was removed, done-notify is hand-owned static
    config carrying no `$source` tag and no generated header. These tests pin that
    the propagator never touches those files: it neither rewrites the untagged
    settings entry nor prunes the header-less OpenCode plugin. Both would have
    failed against the old hook-emitting propagator.
    """

    def _write_source_agent(self, repo_root: Path) -> None:
        agents_dir = repo_root / ".github" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "01-keeper.agent.md").write_text(
            "---\n"
            "name: 01 Keeper\n"
            'description: "Fixture agent."\n'
            "tools: [read, search]\n"
            "user-invocable: false\n"
            "---\n"
            "\n"
            "You are the **01 Keeper** fixture agent.\n",
            encoding="utf-8",
        )

    def test_propagation_leaves_untagged_done_notify_entry_untouched(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root)
            settings_file = repo_root / ".claude" / "settings.json"
            settings_file.parent.mkdir(parents=True, exist_ok=True)
            original = json.dumps(
                {
                    "hooks": {
                        "SessionStart": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "code-review-graph status",
                                        "timeout": 10,
                                    }
                                ],
                            }
                        ],
                        "Stop": [
                            {
                                "matcher": "",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": (
                                            "osascript -e display notification "
                                            '"Claude is done" with title "Claude Code"'
                                        ),
                                    }
                                ],
                            }
                        ],
                    }
                },
                indent=2,
            ) + "\n"
            settings_file.write_text(original, encoding="utf-8")

            mod.propagate_once(verbose=False)

            self.assertEqual(
                settings_file.read_text(encoding="utf-8"),
                original,
                "propagation must never rewrite the hand-owned done-notify wiring",
            )

    def test_propagation_does_not_prune_static_done_notify_plugin(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root)
            plugins_dir = repo_root / ".opencode" / "plugins"
            plugins_dir.mkdir(parents=True, exist_ok=True)
            plugin_file = plugins_dir / "done-notify.js"
            original = (
                "export const DoneNotify = async ({ $, directory }) => {\n"
                "  return {\n"
                '    "session.idle": async (_input, _output) => {\n'
                "      await $`osascript -e 'display notification "
                '"OpenCode is done" with title "OpenCode"\'`.cwd(directory)\n'
                "    }\n"
                "  }\n"
                "}\n"
            )
            plugin_file.write_text(original, encoding="utf-8")

            mod.propagate_once(verbose=False)

            self.assertTrue(
                plugin_file.is_file(),
                "the header-less static done-notify plugin must survive propagation",
            )
            self.assertEqual(plugin_file.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
