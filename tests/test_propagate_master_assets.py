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
#     as explicitly unclosable in `pr-review-conventions` (capability boundaries).
#     Per-agent command scoping is not expressible in Claude subagent frontmatter
#     (`tools: Bash(gh:*)` is an unresolved tool name, not a narrower grant), so
#     removal is the only narrowing available -- and this one cannot be removed.
#     Listing it is the honest outcome: visible and justified beats absent.
PR_REVIEW_EVALUATOR_TOOLS = {
    "05a-baseline-worktree": ["read", "search", "execute"],
    "05b-change-narrator": ["read", "search", "edit"],
    # execute granted for one purpose: read-only git fallback when the
    # orchestrator's materialized range.diff/changed-files.txt are absent.
    "05c-artifact-sweeper": ["read", "search", "edit", "execute"],
    "05d-consistency-auditor": ["read", "search", "edit", "execute"],
    "05e-dependency-auditor": ["read", "search", "edit"],
    "05f-test-health": ["read", "search", "edit"],
    # execute granted for one purpose: read-only git fallback when the
    # orchestrator's materialized range.diff/changed-files.txt are absent.
    "05h-cleanliness-auditor": ["read", "search", "edit", "execute"],
    "05g-readiness-synthesizer": ["read", "search", "edit"],
}


def _discover_pr_review_evaluator_slugs() -> set:
    """Every `05`-family evaluator on disk, read from the source of truth.

    Derived rather than restated: this is what makes omission from
    `PR_REVIEW_EVALUATOR_TOOLS` fail instead of silently narrowing coverage.
    `05-pr-review` is the orchestrator that dispatches the roster, not a member
    of it.
    """
    agents_dir = REPO_ROOT / "source_of_truth" / "agents"
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
            skill_dir = repo_root / "source_of_truth" / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: demo-skill\n"
                "description:\n"
                '  "Demo skill with a wrapped\n'
                '  description."\n'
                "---\n"
                "# Demo body\n",
                encoding="utf-8",
            )

            result = mod.propagate_skills_once()

            self.assertEqual(result["claude_changed"], 1)
            self.assertEqual(result["opencode_changed"], 1)
            self.assertEqual(result["codex_changed"], 1)
            self.assertTrue((repo_root / "ports" / "claude" / "skills" / "demo-skill" / "SKILL.md").exists())
            self.assertTrue((repo_root / "ports" / "opencode" / "skills" / "demo-skill" / "SKILL.md").exists())
            codex_skill = repo_root / "ports" / "codex" / "skills" / "demo-skill" / "SKILL.md"
            self.assertTrue(codex_skill.exists())
            self.assertIn(
                'description: "Demo skill with a wrapped description."',
                codex_skill.read_text(encoding="utf-8"),
            )

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

    def test_diff_security_scan_agent_matches_all_generated_harness_outputs(self) -> None:
        agents = {agent.source_slug: agent for agent in mod.load_source_agents()}
        instructions = mod.load_instruction_docs()

        agent = agents["04e-diff-security-scan"]
        self.assertFalse(agent.user_invocable)
        self.assertNotIn("execute", agent.tools)
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
            "source_of_truth/agents/05-pr-review.agent.md": "name: 05 PR - Review",
            "ports/claude/commands/pr-review.md": "PR Review Orchestrator",
            "ports/opencode/agents/05-pr-review.md": "PR Review Orchestrator",
            "ports/codex/agents/05-pr-review.toml": 'name = "pr-review"',
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
            (REPO_ROOT / "ports" / "claude" / "agents", "*.md", renamed_in_claude),
            (REPO_ROOT / "ports" / "claude" / "commands", "*.md", renamed_in_claude),
            (REPO_ROOT / "ports" / "codex" / "agents", "*.toml", renamed_in_codex),
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
        agents_dir = repo_root / "source_of_truth" / "agents"
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
        skill_dir = repo_root / "source_of_truth" / "skills" / skill_name
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

            claude_orphan = repo_root / "ports" / "claude" / "agents" / "z-doomed.md"
            opencode_orphan = repo_root / "ports" / "opencode" / "agents" / "02-doomed.md"
            self.assertTrue(claude_orphan.exists(), "fixture: expected generated output")
            self.assertTrue(opencode_orphan.exists(), "fixture: expected generated output")

            doomed.unlink()
            result = mod.propagate_once(verbose=False)

            self.assertFalse(claude_orphan.exists())
            self.assertFalse(opencode_orphan.exists())
            self.assertTrue((repo_root / "ports" / "claude" / "agents" / "z-keeper.md").exists())
            self.assertTrue((repo_root / "ports" / "opencode" / "agents" / "01-keeper.md").exists())
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
            claude_agents = repo_root / "ports" / "claude" / "agents"
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
            command_file = repo_root / "ports" / "claude" / "commands" / "flipper.md"
            self.assertTrue(command_file.exists(), "fixture: expected a command file")

            self._write_source_agent(repo_root, "01-flipper", "01 Flipper", user_invocable=False)
            result = mod.propagate_once(verbose=False)

            self.assertFalse(command_file.exists())
            # A non-invocable agent takes the `z-` prefix, so the subagent file it
            # gains on the flip is `z-flipper.md`.
            self.assertTrue((repo_root / "ports" / "claude" / "agents" / "z-flipper.md").exists())
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
            survivor = repo_root / "ports" / "claude" / "agents" / "z-artifact-sweeper.md"
            self.assertTrue(survivor.exists(), "fixture: expected the z- stem")

            doomed.unlink()
            mod.propagate_once(verbose=False)

            self.assertTrue(survivor.exists(), "survivor lost its stem to prune ordering")
            self.assertFalse((repo_root / "ports" / "claude" / "agents" / "z-doomed.md").exists())
            self.assertFalse((repo_root / "ports" / "opencode" / "agents" / "09-doomed.md").exists())

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
                repo_root / "ports" / "claude" / "skills" / "doomed-skill",
                repo_root / "ports" / "opencode" / "skills" / "doomed-skill",
                repo_root / "ports" / "codex" / "skills" / "doomed-skill",
            ]
            for orphan in orphans:
                self.assertTrue(orphan.exists(), f"fixture: expected {orphan}")

            shutil.rmtree(doomed)
            mod.propagate_once(verbose=False)

            for orphan in orphans:
                self.assertFalse(orphan.exists(), f"orphaned skill dir survived: {orphan}")
            for root in ("claude", "opencode", "codex"):
                self.assertTrue((repo_root / "ports" / root / "skills" / "keeper-skill" / "SKILL.md").exists())

    def test_unmarked_skill_directory_survives(self) -> None:
        """AC5 for the skill roots: a skill directory this propagator did not
        generate carries no marker and must never be swept."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_skill(repo_root, "keeper-skill")
            handmade = repo_root / "ports" / "claude" / "skills" / "handmade-skill"
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
            claude_agents = repo_root / "ports" / "claude" / "agents"
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

            claude_dir = repo_root / "ports" / "claude"
            claude_dir.mkdir(parents=True)
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
            (repo_root / "source_of_truth" / "skills").mkdir(parents=True)

            outside = Path(tmp_dir) / "outside"
            precious = outside / "precious-skill"
            precious.mkdir(parents=True)
            (precious / "SKILL.md").write_text(
                f"---\nname: precious\n---\n{mod.GENERATED_SKILL_HEADER}\n", encoding="utf-8"
            )
            never_inspected = precious / "irreplaceable.txt"
            never_inspected.write_text("carries no marker; rmtree does not care\n", encoding="utf-8")

            claude_dir = repo_root / "ports" / "claude"
            claude_dir.mkdir(parents=True)
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
            (repo_root / "ports").mkdir()
            (repo_root / "ports" / "claude").symlink_to(outside, target_is_directory=True)
            self.assertFalse((repo_root / "ports" / "claude" / "agents").is_symlink())

            with self.assertRaises(ValueError):
                mod.propagate_once(verbose=False)

            self.assertTrue(victim.exists(), "prune escaped through a symlinked parent")

    def test_unreadable_orphan_is_not_deleted(self) -> None:
        """An unreadable file is not a confirmed orphan — fail closed."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_source_agent(repo_root, "01-keeper", "01 Keeper")
            claude_agents = repo_root / "ports" / "claude" / "agents"
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
            (repo_root / "source_of_truth" / "agents").mkdir(parents=True)

            result = mod.propagate_once(verbose=False)

            self.assertEqual(result["claude_orphans_removed"], 0)
            self.assertEqual(result["skill_orphans_removed"], 0)
            self.assertFalse((repo_root / "ports" / "claude" / "skills").exists())

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
            claude_agents = repo_root / "ports" / "claude" / "agents"
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
        # codex/agents 46 -> 41 (the five). Command counts are unchanged:
        # Security Scan's command was renamed, not removed.
        # Evangelize retirement dropped one file from each user-invocable
        # surface (claude command, opencode agent, codex agent);
        # claude/agents is unchanged because it had no spawnable subagent file.
        # The `qa` agent added one file to each user-invocable surface (claude
        # command, opencode agent, codex agent); claude/agents is
        # unchanged because `qa` declares no subagent children.
        # The `05h Cleanliness Auditor` evaluator added one spawnable subagent
        # file to claude/agents, opencode/agents, and codex/agents; it is not
        # user-invocable, so command counts are unchanged.
        # The `06 Engagement - Prepare` orchestrator (user-invocable) added one
        # file to each user-invocable surface: claude commands 18 -> 19,
        # opencode/agents and codex/agents 42 -> 43; claude/agents is unchanged
        # (its only child, Docs Writer, already had a file). Counts recounted
        # from disk (`ls ports/<harness>/agents`), not incremented from memory.
        # The `Engagement - Orchestrator` (user-invocable) added one file to
        # each user-invocable surface: claude commands 19 -> 20, opencode/agents
        # and codex/agents 43 -> 44. It also declares `Engagement - Prepare` as
        # a child, giving Prepare its first spawnable subagent file:
        # claude/agents 28 -> 29. Counts recounted from disk.
        # The `Engagement - Audit Runner` (hidden subagent) added one file to
        # opencode/agents and codex/agents: 44 -> 45; claude commands unchanged
        # (not user-invocable). claude/agents 29 -> 31: the runner's own
        # spawnable file plus a first spawnable file for its child
        # `Security Scan`. Counts recounted from disk.
        # The four delta/security synthesis subagents (Delta Synthesizer,
        # Security Narrative, Introduced Issues, Pricing Researcher — all
        # hidden) added four files each to claude/agents (31 -> 35),
        # opencode/agents and codex/agents (45 -> 49); claude commands
        # unchanged (not user-invocable). Counts recounted from disk.
        # The `Engagement - Narrative Writer` (hidden subagent) added one file
        # to claude/agents (35 -> 36), opencode/agents and codex/agents
        # (49 -> 50); claude commands unchanged (not user-invocable). Counts
        # recounted from disk.
        # The `Engagement - Compliance Writer` and `Engagement - Gap Reviewer`
        # (both hidden subagents) added two files each to claude/agents
        # (36 -> 38), opencode/agents and codex/agents (50 -> 52); claude
        # commands unchanged (not user-invocable). Counts recounted from disk.
        # `Engagement - Audit Runner` was retired when the pair-loop skill took
        # over spawning the audit agents directly (one-deep nesting): claude
        # agents 38 -> 37, opencode and codex agents 52 -> 51. Claude commands
        # recounted from disk at 19. Counts recounted from disk.
        # `Engagement - Introduced Issues` was retired when its report folded
        # into the Security Narrative's internal security-delta document:
        # claude agents 37 -> 36, opencode and codex agents 51 -> 50. Claude
        # commands unchanged (not user-invocable). Counts recounted from disk.
        # The `Engagement - Manifest Assembler` (hidden subagent, split out of
        # the Compliance Writer) added one file to claude/agents (36 -> 37),
        # opencode/agents and codex/agents (50 -> 51); claude commands
        # unchanged (not user-invocable). Counts recounted from disk.
        # The QA bootstrap trio (`QA - Bootstrapper` plus hidden `QA - Doc
        # Generator` and `QA - Runner`) added: claude agents 37 -> 39, claude
        # commands 19 -> 20, opencode and codex agents 51 -> 54. Counts
        # recounted from disk.
        # `Auditor - Delta` (hidden subagent of the Audit orchestrator, which
        # compares two audit reports into a delta document) added one file to
        # claude agents (39 -> 40) and opencode/codex agents (54 -> 55); claude
        # commands unchanged (not user-invocable). Counts recounted from disk.
        # `Auditor - Remediation Research` (hidden subagent of the Audit
        # orchestrator, which researches fixes for a delta's open items) added
        # one file to claude agents (40 -> 41) and opencode/codex agents
        # (55 -> 56); claude commands unchanged (not user-invocable). Counts
        # recounted from disk.
        # `Auditor - Remediation Reconciler` (hidden sibling of the subsystem
        # researchers) added one file to every agent surface. After the later
        # retirements below, final counts are claude agents 40 and
        # opencode/codex agents 52.
        # `Security Scan` was folded into `Auditor - Security`, a hidden
        # sibling of the Code/Infra/Refactor auditors: the agent surfaces are
        # unchanged (its spawnable file, held because the Engagement
        # orchestrator declared it as a child, is simply renamed), but it loses
        # its user-invocable command -- claude commands 20 -> 19. Counts
        # recounted from disk.
        # The `QA` agent was merged into `Debugger`: both were authored in one
        # commit, and that same commit gave Debugger the phase-doc-sync gate
        # that was QA's only reason to exist, so QA was redundant from birth.
        # Its two unique clauses moved into Debugger and the file was deleted.
        # It was user-invocable, so it held no z-file in claude agents (41
        # unchanged) but did hold a command (19 -> 18) and an opencode/codex
        # agent file (56 -> 55). Counts recounted from disk.
        # The `Engagement - *` fleet was renamed to `Client Deliverable*`
        # (files `engagement-orchestrator`/`engagement-0N-*` ->
        # `client-deliverable`/`client-deliverable-0N-*`). Earlier entries in
        # this log keep the old names because they record what was true when
        # written. A rename is 1:1, so every count below is unchanged; the
        # propagation pass pruned the nine stale generated files as orphans.
        # The eval-grader system was archived to `eval/deprecated/` (outside
        # `source_of_truth/`, so propagation no longer sees it): `Eval - Grader`
        # and `Eval - Feature Decomposition` were user-invocable and held no
        # spawnable file, so claude commands 18 -> 16; `Eval - Metric Grader`
        # and `Eval - Score Recorder` were hidden, so claude agents 41 -> 39.
        # All four left opencode/codex agents 55 -> 51. Counts recounted from
        # disk.
        # `Visual Verifier` became hidden (`user-invocable: false`) and its
        # source moved to `04g-unity-visual-verification.agent.md`, since it
        # reads its inputs from a spawning orchestrator and cannot run cold. It
        # was dual-use, so it held both a command and a spawnable file: claude
        # commands 16 -> 15, claude agents unchanged at 39. The rename dropped
        # its stem-stickiness, so it now emits as `z-unity-visual-verification`.
        # `Unity Reviewer` became hidden the same way and moved to
        # `04h-unity-reviewer.agent.md`; it is now spawned by PR - Review as
        # well as Phase - Execute and Single Feature - Agent. It was also
        # dual-use: claude commands 15 -> 14, claude agents unchanged at 39.
        # Stripping `04h-` yields the pre-existing stem, so stickiness held and
        # it still emits as `unity-reviewer.md`, not `z-unity-reviewer.md`.
        # `Auditor - Attribution` (hidden sibling of `Auditor - Delta`, which
        # probes both trees to settle whether each provisional finding pre-dates
        # the newer work) added one file to claude agents (40 -> 41) and
        # opencode/codex agents (53 -> 54); claude commands unchanged (not
        # user-invocable). Counts recounted from disk.
        roots = [
            (mod.CLAUDE_AGENTS_DIR, "*.md", mod.GENERATED_AGENT_MARKDOWN_HEADER, 41),
            (mod.CLAUDE_COMMANDS_DIR, "*.md", mod.GENERATED_AGENT_MARKDOWN_HEADER, 15),
            (mod.OPENCODE_AGENTS_DIR, "*.md", mod.GENERATED_AGENT_MARKDOWN_HEADER, 54),
            (mod.CODEX_AGENTS_DIR, "*.toml", mod.GENERATED_AGENT_HEADER, 54),
            (mod.CODEX_PROFILES_DIR, "*.config.toml", mod.GENERATED_AGENT_HEADER, 0),
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
        trusted against a changed one.

        Asserts on the real repository's *content* without mutating it: the
        propagator's inputs (`source_of_truth/`) and outputs (`ports/`,
        `.github/`) are staged into a throwaway tree, and the run is redirected
        there by `env.use` exactly as every other test in this class does. A
        run against the live `REPO_ROOT` would rewrite and prune this
        repository as a side effect of asserting it does not.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            for name in ("source_of_truth", "ports", ".github"):
                source = REPO_ROOT / name
                if source.is_dir():
                    shutil.copytree(source, repo_root / name)
            env.use(self, repo_root)
            result = mod.propagate_once(verbose=False)

            self.assertEqual(result["claude_orphans_removed"], 0)
            self.assertEqual(result["claude_command_orphans_removed"], 0)
            self.assertEqual(result["opencode_orphans_removed"], 0)
            self.assertEqual(result["codex_orphans_removed"], 0)
            self.assertEqual(result["codex_profile_orphans_removed"], 0)
            self.assertEqual(result["skill_orphans_removed"], 0)
            self.assertEqual(result["cursor_command_orphans_removed"], 0)
            self.assertEqual(result["cursor_rule_orphans_removed"], 0)


class StaticDoneNotifyNonInterferenceTests(unittest.TestCase):
    """The propagator no longer owns the done-notify wiring.

    After the hook-emission pipeline was removed, done-notify is hand-owned static
    config carrying no `$source` tag and no generated header. These tests pin that
    the propagator never touches those files: it neither rewrites the untagged
    settings entry nor prunes the header-less OpenCode plugin. Both would have
    failed against the old hook-emitting propagator.
    """

    def _write_source_agent(self, repo_root: Path) -> None:
        agents_dir = repo_root / "source_of_truth" / "agents"
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


class ToolKeyValidationTests(unittest.TestCase):
    """An unrecognized `tools:` key must fail propagation loudly.

    Silent dropping is how two auditor root agents shipped declaring `web` (the
    valid key is `fetch`) without the capability their authors believed they had.
    """

    def _write_agent(self, repo_root: Path, slug: str, tools: str) -> Path:
        agents_dir = repo_root / "source_of_truth" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        path = agents_dir / f"{slug}.agent.md"
        path.write_text(
            "---\n"
            f"name: {slug}\n"
            f'description: "Fixture agent {slug}."\n'
            f"tools: {tools}\n"
            "user-invocable: false\n"
            f"---\n\nYou are the **{slug}** fixture agent.\n",
            encoding="utf-8",
        )
        return path

    def test_invalid_tool_key_fails_propagation(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._write_agent(repo_root, "01-broken", "[read, web]")

            with self.assertRaises(ValueError) as ctx:
                mod.propagate_once(verbose=False)

            message = str(ctx.exception)
            self.assertIn("01-broken.agent.md", message)
            self.assertIn("web", message)
            self.assertIn("fetch", message)

    def test_every_valid_tool_key_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            keys = ", ".join(sorted(mod.VALID_TOOL_KEYS))
            self._write_agent(repo_root, "01-kitchen-sink", f"[{keys}]")

            mod.propagate_once(verbose=False)  # must not raise

    def test_todo_is_valid_and_a_claude_no_op(self) -> None:
        self.assertIn("todo", mod.VALID_TOOL_KEYS)
        self.assertEqual(mod.map_tools_for_claude(["todo"]), ["Skill"])
        self.assertEqual(mod.map_permissions_for_opencode(["todo"]), {"todowrite": "allow"})

    def test_source_corpus_declares_only_valid_tool_keys(self) -> None:
        offenders = []
        for path in sorted((REPO_ROOT / "source_of_truth" / "agents").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^tools:\s*(.+)$", text, re.MULTILINE)
            if not match:
                continue
            for tool in mod._parse_list_value(match.group(1)):
                if tool not in mod.VALID_TOOL_KEYS:
                    offenders.append(f"{path.name}: {tool}")
        self.assertEqual(offenders, [])


class CursorPropagationTests(unittest.TestCase):
    """Cursor harness outputs: commands from user-invocable agents, rules from
    instructions with real file globs."""

    def _seed(self, repo_root: Path) -> None:
        agents_dir = repo_root / "source_of_truth" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "01-captain.agent.md").write_text(
            "---\n"
            "name: 01 Captain\n"
            'description: "Fixture orchestrator."\n'
            "tools: [read, search]\n"
            "user-invocable: true\n"
            "---\n\nYou are the **01 Captain** fixture agent.\n",
            encoding="utf-8",
        )
        (agents_dir / "02-hidden.agent.md").write_text(
            "---\n"
            "name: 02 Hidden\n"
            'description: "Fixture subagent."\n'
            "tools: [read]\n"
            "user-invocable: false\n"
            "---\n\nYou are the **02 Hidden** fixture agent.\n",
            encoding="utf-8",
        )
        instructions_dir = repo_root / "source_of_truth" / "instructions"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        (instructions_dir / "style.instructions.md").write_text(
            "---\n"
            'description: "Style rules."\n'
            'applyTo: "**/*.cs,**/*.py"\n'
            "---\n\nUse the style guide.\n",
            encoding="utf-8",
        )
        (instructions_dir / "agent-only.instructions.md").write_text(
            "---\n"
            'description: "Agent plumbing."\n'
            'applyTo: "source_of_truth/agents/**"\n'
            "---\n\nInternal to agent rendering.\n",
            encoding="utf-8",
        )

    def test_user_invocable_agent_becomes_a_cursor_command(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)

            mod.propagate_once(verbose=False)

            command = repo_root / "ports" / "cursor" / "commands" / "captain.md"
            self.assertTrue(command.is_file())
            text = command.read_text(encoding="utf-8")
            self.assertIn(mod.GENERATED_AGENT_MARKDOWN_HEADER, text)
            self.assertTrue(text.startswith("---\nname: captain\n"))
            self.assertIn('description: "Fixture orchestrator."', text)
            self.assertIn("01 Captain", text)
            self.assertFalse(
                (repo_root / "ports" / "cursor" / "commands" / "z-hidden.md").exists(),
                "non-invocable agents must not become Cursor commands",
            )

    def test_non_invocable_agent_becomes_a_cursor_subagent(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)

            mod.propagate_once(verbose=False)

            agent = repo_root / "ports" / "cursor" / "agents" / "z-hidden.md"
            self.assertTrue(agent.is_file())
            text = agent.read_text(encoding="utf-8")
            self.assertIn("name: z-hidden", text)
            self.assertIn("model: inherit", text)
            # tools: [read] grants no edit permission, so Cursor must enforce it.
            self.assertIn("readonly: true", text)
            self.assertIn(mod.GENERATED_AGENT_MARKDOWN_HEADER, text)

    def test_cursor_subagent_names_never_collide_with_command_names(self) -> None:
        """Cursor invokes commands and subagents alike as `/name`.

        A dual-use agent - user-invocable and spawned as a child - emits both, so
        the subagent must carry the `z-` prefix or `/name` would be ambiguous.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            agents_dir = repo_root / "source_of_truth" / "agents"
            # Captain spawns Deputy; Deputy is itself user-invocable (dual-use).
            (agents_dir / "01-captain.agent.md").write_text(
                "---\n"
                "name: 01 Captain\n"
                'description: "Fixture orchestrator."\n'
                "tools: [read, search]\n"
                "agents: [03 Deputy]\n"
                "user-invocable: true\n"
                "---\n\nYou are the **01 Captain** fixture agent. Spawn **03 Deputy**.\n",
                encoding="utf-8",
            )
            (agents_dir / "03-deputy.agent.md").write_text(
                "---\n"
                "name: 03 Deputy\n"
                'description: "Fixture dual-use agent."\n'
                "tools: [read, edit]\n"
                "user-invocable: true\n"
                "---\n\nYou are the **03 Deputy** fixture agent.\n",
                encoding="utf-8",
            )

            mod.propagate_once(verbose=False)

            cursor = repo_root / "ports" / "cursor"
            command_names = {path.stem for path in (cursor / "commands").glob("*.md")}
            agent_names = {path.stem for path in (cursor / "agents").glob("*.md")}
            self.assertIn("deputy", command_names)
            self.assertIn("z-deputy", agent_names)
            self.assertEqual(
                command_names & agent_names,
                set(),
                "a Cursor command and a Cursor subagent must never share a name",
            )
            # An orchestrator's child reference resolves to the subagent, not itself.
            captain = (cursor / "commands" / "captain.md").read_text(encoding="utf-8")
            self.assertIn("z-deputy", captain)
            # tools include edit, so the subagent is not readonly.
            deputy = (cursor / "agents" / "z-deputy.md").read_text(encoding="utf-8")
            self.assertNotIn("readonly:", deputy)

    def test_skills_are_emitted_for_cursor(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            skill_dir = repo_root / "source_of_truth" / "skills" / "tidy-up"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: tidy-up\ndescription: \"Fixture skill.\"\n---\n\nTidy the tree.\n",
                encoding="utf-8",
            )
            (skill_dir / "reference.md").write_text("Reference.\n", encoding="utf-8")

            mod.propagate_once(verbose=False)

            emitted = repo_root / "ports" / "cursor" / "skills" / "tidy-up"
            self.assertTrue((emitted / "SKILL.md").is_file())
            self.assertTrue((emitted / "reference.md").is_file())
            self.assertIn(
                mod.GENERATED_SKILL_HEADER,
                (emitted / "SKILL.md").read_text(encoding="utf-8"),
            )

    def test_skills_are_hidden_from_claude_and_cursor_slash_menus(self) -> None:
        """Skills are agent capabilities, so no harness may offer them as commands.

        Claude and Cursor honour `user-invocable: false`; the flag is injected at
        emission rather than authored, so the source and the spec-clean mirrors
        must not carry it.
        """
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            skill_dir = repo_root / "source_of_truth" / "skills" / "tidy-up"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: tidy-up\ndescription: \"Fixture skill.\"\n---\n\nTidy the tree.\n",
                encoding="utf-8",
            )

            mod.propagate_once(verbose=False)

            for harness in ("claude", "cursor"):
                emitted = (
                    repo_root / "ports" / harness / "skills" / "tidy-up" / "SKILL.md"
                ).read_text(encoding="utf-8")
                fm, _ = mod._parse_frontmatter(emitted)
                self.assertEqual(
                    fm.get("user-invocable"),
                    "false",
                    f"{harness} skills must stay out of the slash menu",
                )
                self.assertIn('description: "Fixture skill."', emitted)

            for path in (
                repo_root / "ports" / "opencode" / "skills" / "tidy-up" / "SKILL.md",
                repo_root / "ports" / "codex" / "skills" / "tidy-up" / "SKILL.md",
                repo_root / "ports" / "github" / "skills" / "tidy-up" / "SKILL.md",
            ):
                self.assertNotIn(
                    "user-invocable",
                    path.read_text(encoding="utf-8"),
                    f"{path.parts[-4]} has no slash surface and takes only spec fields",
                )

            self.assertNotIn(
                "user-invocable",
                (skill_dir / "SKILL.md").read_text(encoding="utf-8"),
                "the flag is injected at emission, never written back to source",
            )

    def test_authored_skill_visibility_wins_over_the_injected_default(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            skill_dir = repo_root / "source_of_truth" / "skills" / "tidy-up"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: tidy-up\n"
                'description: "Fixture skill."\n'
                "user-invocable: true\n"
                "---\n\nTidy the tree.\n",
                encoding="utf-8",
            )

            mod.propagate_once(verbose=False)

            for harness in ("claude", "cursor"):
                emitted = (
                    repo_root / "ports" / harness / "skills" / "tidy-up" / "SKILL.md"
                ).read_text(encoding="utf-8")
                fm, _ = mod._parse_frontmatter(emitted)
                self.assertEqual(fm.get("user-invocable"), "true")
                self.assertNotIn("user-invocable: false", emitted)

    def test_glob_instruction_becomes_a_rule_agent_plumbing_does_not(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)

            mod.propagate_once(verbose=False)

            rules = repo_root / "ports" / "cursor" / "rules"
            style = (rules / "style.mdc").read_text(encoding="utf-8")
            self.assertIn('description: "Style rules."', style)
            self.assertIn("globs: **/*.cs,**/*.py", style)
            self.assertIn("alwaysApply: false", style)

            self.assertFalse(
                (rules / "agent-only.mdc").exists(),
                "agent-targeted instructions ship inside rendered agents, not as rules",
            )

    def _seed_bare_name_agents_and_internal_instructions(self, repo_root: Path) -> None:
        """The shapes the old suffix heuristic misclassified.

        Two agents whose files lack the `.agent.md` suffix, plus instructions
        matching them by bare name and by a `0*.md` glob -- all internal plumbing
        that must never reach the user-global Cursor rules directory.
        """
        agents_dir = repo_root / "source_of_truth" / "agents"
        for slug, name in (("auditor", "Auditor"), ("04f-prod-code-review", "Prod Code Review")):
            (agents_dir / f"{slug}.md").write_text(
                "---\n"
                f"name: {name}\n"
                f'description: "Fixture {name}."\n'
                "tools: [read]\n"
                "user-invocable: true\n"
                f"---\n\nYou are the **{name}** fixture agent.\n",
                encoding="utf-8",
            )
        instructions_dir = repo_root / "source_of_truth" / "instructions"
        (instructions_dir / "orchestrator-conventions.instructions.md").write_text(
            "---\n"
            'description: "Orchestrator plumbing."\n'
            'applyTo: "**/auditor.md,**/01-captain.agent.md"\n'
            "---\n\nInternal orchestration conventions.\n",
            encoding="utf-8",
        )
        (instructions_dir / "pipeline-artifacts.instructions.md").write_text(
            "---\n"
            'description: "Pipeline artifacts."\n'
            'applyTo: "source_of_truth/agents/0*.md"\n'
            "---\n\nInternal pipeline artifact rules.\n",
            encoding="utf-8",
        )

    def test_agent_targeted_instructions_never_become_cursor_rules(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            self._seed_bare_name_agents_and_internal_instructions(repo_root)

            mod.propagate_once(verbose=False)

            rules = repo_root / "ports" / "cursor" / "rules"
            for leaked in ("orchestrator-conventions.mdc", "pipeline-artifacts.mdc", "agent-only.mdc"):
                self.assertFalse(
                    (rules / leaked).exists(),
                    f"{leaked} is internal plumbing and must not ship as a user-global Cursor rule",
                )
            self.assertTrue(
                (rules / "style.mdc").is_file(),
                "instructions with real source-file globs must still ship as Cursor rules",
            )

    def test_cursor_rule_classifier_matches_inlining(self) -> None:
        """Bare-name and `0*.md` patterns resolve to agents, so they are internal."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            self._seed_bare_name_agents_and_internal_instructions(repo_root)

            agents = mod.load_source_agents()
            instructions = mod.load_instruction_docs()
            by_name = {doc.path.name: doc for doc in instructions}

            for internal in (
                "orchestrator-conventions.instructions.md",
                "pipeline-artifacts.instructions.md",
            ):
                applicable = {
                    agent.rel_path
                    for agent in agents
                    if by_name[internal] in mod.applicable_instructions(agent, instructions)
                }
                self.assertTrue(
                    applicable,
                    f"{internal} must inline into at least one agent to count as internal",
                )

            mod.propagate_cursor_rules_once(instructions, agents)
            emitted = {
                path.name for path in (repo_root / "ports" / "cursor" / "rules").glob("*.mdc")
            }
            self.assertEqual(emitted, {"style.mdc"})

    def test_orphaned_cursor_outputs_are_pruned(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)

            mod.propagate_once(verbose=False)
            command = repo_root / "ports" / "cursor" / "commands" / "captain.md"
            rule = repo_root / "ports" / "cursor" / "rules" / "style.mdc"
            subagent = repo_root / "ports" / "cursor" / "agents" / "z-hidden.md"
            self.assertTrue(command.exists())
            self.assertTrue(rule.exists())
            self.assertTrue(subagent.exists())

            (repo_root / "source_of_truth" / "agents" / "01-captain.agent.md").unlink()
            (repo_root / "source_of_truth" / "agents" / "02-hidden.agent.md").unlink()
            (repo_root / "source_of_truth" / "instructions" / "style.instructions.md").unlink()
            result = mod.propagate_once(verbose=False)

            self.assertFalse(command.exists())
            self.assertFalse(rule.exists())
            self.assertFalse(subagent.exists())
            self.assertEqual(result["cursor_command_orphans_removed"], 1)
            self.assertEqual(result["cursor_rule_orphans_removed"], 1)
            self.assertEqual(result["cursor_agent_orphans_removed"], 1)


class TestEnvironmentCoverageTests(unittest.TestCase):
    """The temp-root redirect must cover every directory global.

    A global the redirect misses stays pinned to the real repository, so an
    isolated test would read or delete files here instead of in its temp tree.
    """

    def test_every_directory_global_is_redirected(self) -> None:
        overrides = set(env.repo_dir_overrides(Path("/tmp/example")))
        globals_needing_redirect = {
            name
            for name, value in vars(mod).items()
            if isinstance(value, Path) and name.isupper()
        }
        self.assertEqual(
            globals_needing_redirect - overrides,
            set(),
            "add the missing directory global to tests/_propagate_env.repo_dir_overrides",
        )


class GithubMirrorTests(unittest.TestCase):
    def _seed(self, repo_root: Path) -> None:
        agents_dir = repo_root / "source_of_truth" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        (agents_dir / "01-keeper.agent.md").write_text(
            "---\nname: 01 Keeper\ndescription: \"Fixture.\"\n---\n\nBody.\n",
            encoding="utf-8",
        )
        hooks_dir = repo_root / "source_of_truth" / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        (hooks_dir / "hook.sh").write_text("#!/bin/sh\n", encoding="utf-8")

    def test_source_is_mirrored_to_ports_github_and_dot_github(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)

            mod.mirror_github_once()

            for base in (repo_root / "ports" / "github", repo_root / ".github"):
                self.assertTrue((base / "agents" / "01-keeper.agent.md").is_file())
                self.assertTrue((base / "hooks" / "hook.sh").is_file())

    def test_stale_mirror_files_are_deleted_but_foreign_dirs_survive(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)
            mod.mirror_github_once()

            stale = repo_root / ".github" / "agents" / "01-keeper.agent.md"
            workflows = repo_root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text("on: push\n", encoding="utf-8")

            (repo_root / "source_of_truth" / "agents" / "01-keeper.agent.md").unlink()
            mod.mirror_github_once()

            self.assertFalse(stale.exists(), "stale mirror copy survived")
            self.assertTrue(
                (workflows / "ci.yml").exists(),
                "mirror touched a non-mirrored .github subdir",
            )

    def test_mirror_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            env.use(self, repo_root)
            self._seed(repo_root)

            first = mod.mirror_github_once()
            second = mod.mirror_github_once()

            self.assertGreater(first["github_changed"], 0)
            self.assertEqual(second["github_changed"], 0)


class InstructionApplyToTests(unittest.TestCase):
    """Every enumerated `applyTo` filename must resolve to an agent on disk.

    Thirteen of the sixteen instruction files hand-enumerate their target agents
    by filename; three use a directory glob. An enumerated path that no longer
    resolves — a renamed or deleted agent — fails open: the instruction simply
    stops being injected, the agent still runs, and nothing reports it. This
    asserts the enumerations still point at real files.
    """

    INSTRUCTIONS_DIR = REPO_ROOT / "source_of_truth" / "instructions"
    AGENTS_DIR = REPO_ROOT / "source_of_truth" / "agents"

    def _apply_to_patterns(self, path: Path) -> list[str]:
        text = path.read_text(encoding="utf-8")
        match = re.search(r'^applyTo:\s*"([^"]+)"', text, re.MULTILINE)
        if not match:
            return []
        return [p.strip() for p in match.group(1).split(",") if p.strip()]

    def test_every_enumerated_applyto_target_exists(self) -> None:
        agent_names = {p.name for p in self.AGENTS_DIR.iterdir() if p.is_file()}
        self.assertTrue(agent_names, "no agent definitions found")

        unresolved = []
        for instruction in sorted(self.INSTRUCTIONS_DIR.glob("*.instructions.md")):
            for pattern in self._apply_to_patterns(instruction):
                if not pattern.startswith("**/"):
                    # Directory glob (e.g. "source_of_truth/agents/**") — matches
                    # by directory, so there is no filename to resolve.
                    continue
                target = pattern[len("**/") :]
                if not target.endswith(".md"):
                    # Source-file glob (e.g. "**/*.py", "**/pyproject.toml") —
                    # matches code being edited, not an agent definition.
                    continue
                if target not in agent_names:
                    unresolved.append(f"{instruction.name} -> {target}")

        self.assertEqual(
            [],
            unresolved,
            "applyTo entries naming agents that do not exist (the instruction "
            "silently stops being injected):\n  " + "\n  ".join(unresolved),
        )

    def test_every_instruction_declares_applyto(self) -> None:
        missing = [
            p.name
            for p in sorted(self.INSTRUCTIONS_DIR.glob("*.instructions.md"))
            if not self._apply_to_patterns(p)
        ]
        self.assertEqual([], missing, f"instructions with no applyTo: {missing}")


class AuthoringProfileGateTests(unittest.TestCase):
    """The profile gate partitions instruction inlining.

    `technical` is the implicit default and is never written in a source file.
    `creative` is opt-in, and the gate is symmetric: a technical instruction is
    never inlined into a creative agent, and a creative instruction is never
    inlined into a technical one.
    """

    @staticmethod
    def _agent(rel_path: str, profile: str = mod.DEFAULT_PROFILE):
        return mod.SourceAgent(
            path=mod.REPO_ROOT / rel_path,
            rel_path=rel_path,
            source_slug=Path(rel_path).name.replace(".agent.md", ""),
            name="Test Agent",
            description="test",
            tools=["read"],
            subagents=[],
            user_invocable=True,
            body="body\n",
            profile=profile,
        )

    @staticmethod
    def _doc(name: str, pattern: str, profile: str = mod.DEFAULT_PROFILE):
        return mod.InstructionDoc(
            path=mod.SOT_INSTRUCTIONS_DIR / f"{name}.instructions.md",
            apply_to_patterns=[pattern],
            body=f"{name} body\n",
            description=name,
            profile=profile,
        )

    def test_absent_profile_key_means_technical(self) -> None:
        self.assertEqual(mod.DEFAULT_PROFILE, mod._parse_profile("x.md", None))
        self.assertEqual(mod.DEFAULT_PROFILE, mod._parse_profile("x.md", ""))
        self.assertEqual(mod.CREATIVE_PROFILE, mod._parse_profile("x.md", '"creative"'))

    def test_unrecognized_profile_is_a_propagation_failure(self) -> None:
        with self.assertRaises(ValueError):
            mod._parse_profile("x.md", "technicl")

    def test_technical_instruction_is_withheld_from_creative_agent(self) -> None:
        blanket = self._doc("dev-task-folder", "source_of_truth/agents/**")
        creative_agent = self._agent(
            "source_of_truth/agents/creative-scene-writer.agent.md",
            mod.CREATIVE_PROFILE,
        )
        technical_agent = self._agent("source_of_truth/agents/debugger.agent.md")

        # The glob matches both agents; only the profile separates them.
        self.assertEqual([], mod.applicable_instructions(creative_agent, [blanket]))
        self.assertEqual(
            [blanket], mod.applicable_instructions(technical_agent, [blanket])
        )

    def test_creative_instruction_is_withheld_from_technical_agent(self) -> None:
        creative_doc = self._doc(
            "creative-profile", "source_of_truth/agents/**", mod.CREATIVE_PROFILE
        )
        technical_agent = self._agent("source_of_truth/agents/debugger.agent.md")
        creative_agent = self._agent(
            "source_of_truth/agents/creative-scene-writer.agent.md",
            mod.CREATIVE_PROFILE,
        )

        self.assertEqual(
            [], mod.applicable_instructions(technical_agent, [creative_doc])
        )
        self.assertEqual(
            [creative_doc], mod.applicable_instructions(creative_agent, [creative_doc])
        )

    def test_creative_instruction_never_becomes_a_global_cursor_rule(self) -> None:
        """A creative doc must be skipped even with no creative agent on disk.

        With no creative agent loaded, its applyTo patterns resolve against
        nothing, and the agent-definition check alone would render it as an
        `alwaysApply` user-global rule.
        """
        creative_doc = self._doc(
            "creative-profile",
            "source_of_truth/agents/creative-*.agent.md",
            mod.CREATIVE_PROFILE,
        )
        technical_agent = self._agent("source_of_truth/agents/debugger.agent.md")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env.use(self, root)
            rules_dir = mod.CURSOR_RULES_DIR
            rules_dir.mkdir(parents=True)
            mod.propagate_cursor_rules_once([creative_doc], [technical_agent])
            self.assertEqual([], sorted(rules_dir.glob("*.mdc")))

            # The same call with the doc left technical writes the rule, so the
            # assertion above is proving the profile skip, not an inert path.
            technical_doc = self._doc(
                "unscoped-rule", "**/*.py", mod.DEFAULT_PROFILE
            )
            mod.propagate_cursor_rules_once([technical_doc], [technical_agent])
            self.assertEqual(
                ["unscoped-rule.mdc"],
                [path.name for path in sorted(rules_dir.glob("*.mdc"))],
            )

    def test_corpus_on_disk_carries_only_valid_profiles(self) -> None:
        """No contributor step: every source file resolves to a valid profile."""
        for agent in mod.load_source_agents():
            with self.subTest(agent=agent.rel_path):
                self.assertIn(agent.profile, mod.VALID_PROFILES)
        for doc in mod.load_instruction_docs():
            with self.subTest(doc=doc.path.name):
                self.assertIn(doc.profile, mod.VALID_PROFILES)


if __name__ == "__main__":
    unittest.main()
