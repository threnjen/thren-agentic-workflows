"""Contract assertions for the three cheap-tier mechanical PR Review sweeps.

These agents are prompts, not code, so the only thing a test can hold is the
contract their bodies declare. The contracts pinned here are the ones whose
absence would not be visible in a passing run: a sweep that reports pre-existing
findings as branch-introduced looks exactly like a sweep that works, until a
reader notices the report is noise and stops reading it.

The roster and tool grants are asserted in `test_propagate_master_assets.py`
alongside the propagation enumeration ledger they belong to.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / ".github" / "agents"

# Agent bodies are hard-wrapped prose. A contract assertion must hold on what the
# body *says*, not on where its lines happen to break, or reflowing a paragraph
# silently drops the assertion.
_WHITESPACE = re.compile(r"\s+")

MECHANICAL_EVALUATORS = (
    "05c-artifact-sweeper",
    "05d-consistency-auditor",
    "05e-dependency-auditor",
)

# `05c` and `05d` build on code-review-graph. Availability is a dependency, not a
# fallback: an unavailable graph is a NOT RUN with a reason, never a quiet grep
# that reports as though the graph answered.
GRAPH_DEPENDENT_EVALUATORS = ("05c-artifact-sweeper", "05d-consistency-auditor")


def _body(slug: str) -> str:
    """The body as written, for assertions about literal tokens and frontmatter."""
    return (AGENTS_DIR / f"{slug}.agent.md").read_text(encoding="utf-8")


def _prose(slug: str) -> str:
    """The body with runs of whitespace collapsed, for assertions about sentences."""
    return _WHITESPACE.sub(" ", _body(slug))


class RenameTests(unittest.TestCase):
    """AC1: the renumber is complete, in both directions."""

    def test_renumbered_agents_exist_with_matching_name_frontmatter(self) -> None:
        expected_names = {
            "05c-artifact-sweeper": "05c Artifact Sweeper",
            "05d-consistency-auditor": "05d Consistency Auditor",
            "05e-dependency-auditor": "05e Dependency Auditor",
        }
        for slug, name in expected_names.items():
            with self.subTest(slug=slug):
                self.assertIn(f"name: {name}\n", _body(slug))

    def test_retired_slugs_are_gone_from_the_source_tree(self) -> None:
        for stem in ("05g-artifact-sweeper", "05j-consistency-auditor",
                     "05k-dependency-auditor"):
            with self.subTest(stem=stem):
                self.assertFalse((AGENTS_DIR / f"{stem}.agent.md").exists())

    def test_no_body_retains_an_old_self_reference(self) -> None:
        """A renamed agent that still calls itself `05g Artifact Sweeper` in prose
        is worse than one that was never renamed: the frontmatter and the body
        disagree, and the body is what the model reads.

        The retired identifiers, not the bare number. `05g` is about to be
        reissued to the readiness synthesizer in wave 6, so banning the substring
        would pass today and misfire the moment feature 07 lands -- the same trap
        that makes a `05g-*` glob the wrong assertion for the OpenCode orphans.
        """
        retired = (
            "05g-artifact-sweeper", "05g Artifact Sweeper",
            "05j-consistency-auditor", "05j Consistency Auditor",
            "05k-dependency-auditor", "05k Dependency Auditor",
        )
        for slug in MECHANICAL_EVALUATORS:
            body = _body(slug)
            for marker in retired:
                with self.subTest(slug=slug, marker=marker):
                    self.assertNotIn(marker, body)


class ScopeTests(unittest.TestCase):
    """AC2: the subject is the branch diff, not a phase."""

    def test_no_body_mentions_subphases_or_the_retired_report_root(self) -> None:
        forbidden = ("subphase", "PHASE_0N", "dev/phase-final-review")
        for slug in MECHANICAL_EVALUATORS:
            body = _body(slug).lower()
            for term in forbidden:
                with self.subTest(slug=slug, term=term):
                    self.assertNotIn(term.lower(), body)

    def test_each_body_scopes_itself_to_the_branch_diff(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertIn("<merge-base>..HEAD", _body(slug))

    def test_each_body_takes_the_base_from_the_orchestrator(self) -> None:
        """The base is confirmed once, by the orchestrator, and handed down. An
        evaluator that re-derives it can review a different range than its
        siblings and nothing would reconcile the two."""
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertRegex(
                    _prose(slug),
                    r"orchestrator supplies the confirmed base[^.]*never re-derive",
                )


class AttributionTests(unittest.TestCase):
    """AC6: added-line attribution, not touched-file filtering.

    The single most likely way these agents are quietly wrong. A branch that adds
    one line to a 900-line file did not introduce that file's 12 pre-existing
    TODOs, and a sweep that reports them trains the reader to ignore the report.
    """

    def test_each_body_requires_verifiable_added_line_attribution(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertIn("added-line attribution", _body(slug))

    def test_each_body_explicitly_rejects_touched_file_filtering(self) -> None:
        """Requiring attribution and rejecting the cheaper substitute are
        different claims. A body can demand attribution in one line and filter by
        touched file in the next without contradicting itself."""
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertRegex(
                    _prose(slug),
                    r"[Tt]ouched-file filtering (alone )?is (insufficient|not sufficient)",
                )

    def test_unattributable_findings_are_not_run_rather_than_reported(self) -> None:
        """The disposal of an unattributable candidate is the load-bearing part.
        Dropping it silently and reporting it as introduced are both wrong; it
        goes to Checks Not Run with a reason."""
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertRegex(
                    _prose(slug),
                    r"attribution cannot be verified[^.]*"
                    r"(\*\*NOT RUN\*\*|`?Checks Not Run`?)[^.]*concrete reason",
                )


class TierTests(unittest.TestCase):
    """AC7: a limitation is an execution condition, never a pass."""

    def test_each_body_treats_the_tier_assignment_as_authoritative(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertIn("authoritative", _body(slug))

    def test_no_body_converts_a_missing_check_into_a_pass(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertRegex(
                    _prose(slug),
                    r"[Nn]ever convert a missing check into a pass",
                )

    def test_graph_dependent_evaluators_label_the_fallback_when_the_graph_is_down(
        self,
    ) -> None:
        """The failure mode is a silent downgrade: grep the tree, find something
        plausible, report it as a graph result. The contract evolved from
        'graph down = NOT RUN' to 'graph preferred, not required': a text-search
        fallback is permitted but must be labeled by name so it is never
        presented as though the graph answered it."""
        for slug in GRAPH_DEPENDENT_EVALUATORS:
            prose = _prose(slug)
            with self.subTest(slug=slug):
                self.assertIn("code-review-graph", prose)
                self.assertRegex(
                    prose,
                    r"(graph server|`refactor_tool`)[^.]*"
                    r"(unavailable|not available)",
                )
                self.assertIn(
                    "text-search fallback (not graph-verified)", prose
                )
                self.assertRegex(
                    prose,
                    r"never presented as though the graph "
                    r"(answered|confirmed) it",
                )


class OfflineDependencyAuditTests(unittest.TestCase):
    """AC4: the dependency audit is offline by contract."""

    def test_the_offline_contract_survives_the_rescope(self) -> None:
        self.assertRegex(
            _prose("05e-dependency-auditor"),
            r"contacts the network, is unavailable for this audit",
        )

    def test_cve_and_license_auditing_are_declared_out_of_scope(self) -> None:
        """License/CVE checks were removed from `05e`: offline, they could never
        complete and permanently capped the verdict. The body must declare them
        out of scope by design -- not merely omit them -- so their absence reads
        as a stated non-goal instead of a coverage gap, and must not resurrect
        them as scope items or not-run checks."""
        prose = _prose("05e-dependency-auditor")
        self.assertRegex(
            prose,
            r"CVE/advisory auditing and license compliance are \*\*out of "
            r"scope\*\*",
        )
        self.assertRegex(prose, r"never recorded as a not-run check")
        self.assertNotRegex(prose, r"[Ll]icense evidence")
        self.assertNotRegex(prose, r"[Vv]ulnerability evidence")

    def test_the_audit_declares_no_shell_grant(self) -> None:
        """`05e` lost `execute`, so its body must not still promise to run an
        audit command. A body describing a capability its frontmatter withholds
        produces a confident report about a check that never ran."""
        body = _body("05e-dependency-auditor")
        self.assertNotIn("audit command", body)


class ReportContractTests(unittest.TestCase):
    """AC5: report path by reference, and a bounded return."""

    def test_each_body_writes_to_its_own_slug_report_under_the_review_root(
        self,
    ) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertIn(f"{slug}-report.md", _body(slug))

    def test_no_body_restates_the_report_root_format(self) -> None:
        """The conventions skill owns the path format. A body that restates it is
        a second copy that drifts -- and feature 03 already moved this root once.
        """
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertNotIn("<UTC-YYYYMMDDTHHMMSSZ>", _body(slug))
                self.assertNotIn("<base-sha-short>", _body(slug))

    def test_each_body_loads_the_conventions_skill(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertIn("pr-review-conventions", _body(slug))

    def test_each_body_bounds_its_return_to_ten_lines(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertRegex(_prose(slug), r"(at most|no more than) 10 lines")


class ReadOnlyTests(unittest.TestCase):
    """The house pattern: report-only, never remediate."""

    def test_each_body_forbids_remediation(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertRegex(
                    _prose(slug),
                    r"[Dd]o not remediate|[Nn]ever modify source|"
                    r"[Nn]ever remediate",
                )


class EmptyDiffTests(unittest.TestCase):
    """An empty diff is a stated result, not 'no findings'."""

    def test_each_body_handles_an_empty_diff_explicitly(self) -> None:
        for slug in MECHANICAL_EVALUATORS:
            with self.subTest(slug=slug):
                self.assertIn("nothing introduced since", _body(slug))


if __name__ == "__main__":
    unittest.main()
