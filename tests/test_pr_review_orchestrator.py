"""Contract assertions for the PR Review orchestrator.

The PR-Review rescope (see `.github/learnings/cross-phase-decisions.md`) turned
`05 Phase - Final Review` -- an orchestrator for a multi-subphase phase, with a
ledger, an artifact-inventory gate, and a two-file transactional verdict
write-back -- into `05 PR - Review`, which reviews the diff between a base
commit and a head commit and writes no verdict anywhere.

Most of what this module asserts is *absence*. The deleted machinery was the
riskiest code in the pipeline, and every piece of it is individually plausible
to reintroduce: a ledger read looks like provenance, an artifact gate looks like
rigour, a write-back looks like a finished job. The absence tests are the only
thing standing between "we deleted it" and "someone helpfully put it back".

Style follows `tests/test_readiness_synthesis_agents.py`: module-level `Path`
constants and plain `assert`, pytest-style -- not the `unittest` classes of
`tests/test_propagate_master_assets.py`.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ORCHESTRATOR = REPO_ROOT / "source_of_truth" / "agents" / "05-pr-review.agent.md"
RETIRED_ORCHESTRATOR = (
    REPO_ROOT / "source_of_truth" / "agents" / "05-phase-final-review.agent.md"
)

FIXTURE = REPO_ROOT / "dev" / "pr-review" / "fixtures" / "pinned-diff-range.md"

# Feature 03's canonical report contract. The report root is declared there;
# this module reads it rather than restating it.
CONVENTIONS_SKILL = (
    REPO_ROOT / "source_of_truth" / "skills" / "pr-review-conventions" / "SKILL.md"
)

# The surviving evaluators that still declare the retired `dev/phase-final-review/`
# report root. Their bodies are owned by features 06 (narrative + test health) and
# 07 (synthesis), which renumber and rescope them; migrating them from feature 04
# would collide with both. Listed so the split is pinned instead of implicit --
# see `test_report_root_migration_cannot_split_silently`.
#
# Feature 05 has since migrated the three mechanical sweeps, which is why
# `05g-artifact-sweeper`, `05j-consistency-auditor` and `05k-dependency-auditor`
# are gone from this set rather than renamed into it: they now write to
# `dev/pr-review/` as `05c`, `05d` and `05e`. That is the ledger working as
# designed -- the migration tripped this assertion and was reconciled here.
#
# Feature 06 has since migrated the narrator and test health the same way, and
# for the same reason they are removed rather than renamed: `05b-change-narrator`
# and `05h-test-health` (now `05f-test-health`) both defer their report path to
# the `pr-review-conventions` skill.
#
# Feature 07 has now migrated the synthesizer (`05l` -> `05g`), which was the last
# entry. The set is empty, and the migration is COMPLETE.
#
# The original note said "when that lands, this set is empty and this test can go".
# Deleting it is the one move not taken. An empty ledger is no longer a record of
# known drift -- it is the assertion that no drift exists, which is a stronger and
# permanently useful guard than the ledger ever was. Deleting the test would leave
# the retired root free to reappear in any `05*` body with nothing to catch it.
# Kept, with the set frozen empty: the failure message below now reads as
# "an evaluator regressed to the retired root" rather than "update the ledger".
EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION: set[str] = set()

# The pinned base/head pair (AC13). Declared here once so the fixture document
# and the tests cannot drift apart: the test reads these out of the fixture
# rather than trusting that it says what it claims.
FIXTURE_BASE_SHA = "f5ab960e5697756538f94430327e2a68eb113822"
FIXTURE_HEAD_SHA = "e6ff28a36293697aebf62155ae0048115c4aecca"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _prose(path: Path = ORCHESTRATOR) -> str:
    """The body, lowercased, with every run of whitespace collapsed to one space.

    Prose assertions must not be coupled to line-wrap position. Re-wrapping a
    paragraph is not a semantic change, and a test that breaks on it teaches
    people to reformat around the test rather than to keep the contract -- see
    `tests/test_readiness_synthesis_agents.py:16`, whose `"never read\\ncode"`
    is pinned to the exact column its author happened to wrap at.
    """
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


# ---------------------------------------------------------------------------
# AC13 -- the pinned fixture
# ---------------------------------------------------------------------------


def test_fixture_pins_both_shas_of_a_real_base_head_pair() -> None:
    body = FIXTURE.read_text(encoding="utf-8")

    assert FIXTURE_BASE_SHA in body
    assert FIXTURE_HEAD_SHA in body


def test_fixture_shas_resolve_and_merge_base_is_the_pinned_base() -> None:
    """The pair is a genuine PR shape, not two arbitrary commits.

    `git merge-base head base` returning `base` is what makes this a base/head
    pair at all -- it proves the head branch descends from the base rather than
    merely differing from it.
    """
    assert _git("rev-parse", "--verify", f"{FIXTURE_BASE_SHA}^{{commit}}") == (
        FIXTURE_BASE_SHA
    )
    assert _git("rev-parse", "--verify", f"{FIXTURE_HEAD_SHA}^{{commit}}") == (
        FIXTURE_HEAD_SHA
    )
    assert _git("merge-base", FIXTURE_HEAD_SHA, FIXTURE_BASE_SHA) == FIXTURE_BASE_SHA


def test_fixture_range_is_pr_shaped_not_a_whole_phase() -> None:
    """Guards the sizing correction the plan calls out explicitly.

    The pair implied by AC4's base-derivation evidence (`e3398c7..ae9823a`) is
    242 files and ~27k insertions -- a whole-phase diff. Dry-running seven
    evaluators against that is slow, costly, and a poor proxy for a PR. The
    bound is deliberately generous: it fails the whole-phase shape, not a
    slightly-grown fixture.
    """
    files = _git(
        "diff", "--name-only", FIXTURE_BASE_SHA, FIXTURE_HEAD_SHA
    ).splitlines()
    commits = _git(
        "rev-list", "--count", f"{FIXTURE_BASE_SHA}..{FIXTURE_HEAD_SHA}"
    )

    assert 0 < len(files) <= 60, f"fixture spans {len(files)} files"
    assert 0 < int(commits) <= 10, f"fixture spans {commits} commits"


def test_fixture_records_why_the_pair_was_chosen() -> None:
    body = FIXTURE.read_text(encoding="utf-8").lower()

    assert "why this pair" in body


# ---------------------------------------------------------------------------
# AC10b -- .gitignore makes the fixture trackable and run output ignored
# ---------------------------------------------------------------------------


def test_fixture_is_actually_tracked_by_git() -> None:
    """`.gitignore:5` is `dev/*`. Without an un-ignore rule the fixture is
    silently untracked and AC13 fails invisibly -- the file is on the
    implementer's disk and in nobody else's clone."""
    tracked = _git("ls-files", "dev/pr-review/fixtures/").splitlines()

    assert "dev/pr-review/fixtures/pinned-diff-range.md" in tracked


def test_run_output_root_stays_ignored() -> None:
    """AC7's report root must NOT become trackable. Run output would pollute
    the tree and confound the propagation-idempotency checks in feature 08."""
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "dev/pr-review/abc1234-20260716T120000Z/readiness-report.md",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "run output root is not ignored"


# ---------------------------------------------------------------------------
# AC1 / AC14 -- the rename, and its propagation to all three roots
# ---------------------------------------------------------------------------


def test_orchestrator_is_renamed_and_the_old_source_is_gone() -> None:
    assert ORCHESTRATOR.is_file()
    assert not RETIRED_ORCHESTRATOR.exists()


def test_frontmatter_declares_the_pr_review_name_and_diff_scope() -> None:
    body = ORCHESTRATOR.read_text(encoding="utf-8")

    assert "name: 05 PR - Review" in body
    assert "05 Phase - Final Review" not in body

    description = next(
        line for line in body.splitlines() if line.startswith("description:")
    ).lower()
    # The description must state the branch-diff scope, not the old
    # multi-subphase / verdict-write-back framing.
    assert "base commit" in description and "head commit" in description
    assert "subphase" not in description
    assert "write-back" not in description and "write back" not in description


def test_agent_name_does_not_collide_with_prose_in_any_source_asset() -> None:
    """`_rewrite_agent_references` does an unanchored `text.replace(agent.name,
    identifier)` across every agent body, so a `name:` that also occurs as
    ordinary prose gets rewritten wherever it appears. A generic `PR Review`
    would corrupt that common phrase throughout this phase's agent and skill
    text. The ` - ` separator is what makes the name collision-safe -- load
    bearing, not stylistic.

    This reads the name out of the file rather than restating it, so renaming
    the agent to something collision-prone fails here instead of silently
    shipping mangled prose.
    """
    name = next(
        line.split("name:", 1)[1].strip()
        for line in ORCHESTRATOR.read_text(encoding="utf-8").splitlines()
        if line.startswith("name:")
    )

    assert " - " in name, f"{name!r} lacks the collision-safe separator"

    # Scope comes from the propagator's own loader, not a glob of the agents
    # directory. `_rewrite_agent_references` is applied to source-agent bodies;
    # `.github/agents/README.md` is deliberately NOT one (it carries no
    # frontmatter `name`/`description`, so `load_source_agents` skips it). The
    # README is the roster document -- naming every agent by display name is its
    # job, and a glob-based check would flag that as a collision and push an
    # implementer toward "fixing" the roster.
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import propagate_master_assets as propagator

    for agent in propagator.load_source_agents():
        if agent.name == name:
            continue
        assert name not in agent.body, (
            f"{name!r} occurs in the body of {agent.rel_path}; "
            "propagation would rewrite it into an identifier"
        )


def test_renamed_orchestrator_reaches_all_three_generated_roots() -> None:
    expected_markers = {
        "ports/claude/commands/pr-review.md": "PR Review Orchestrator",
        "ports/opencode/agents/05-pr-review.md": "PR Review Orchestrator",
        "ports/codex/agents/05-pr-review.toml": 'name = "pr-review"',
        "ports/codex/profiles/pr-review.config.toml": "PR Review Orchestrator",
    }

    for relative_path, marker in expected_markers.items():
        output = REPO_ROOT / relative_path
        assert output.is_file(), relative_path
        assert marker in output.read_text(encoding="utf-8"), relative_path


def test_stale_generated_outputs_are_absent_from_every_root() -> None:
    """AC14. `claude/commands/phase-final-review.md` is the sharpest case: it
    stays user-invocable, so a stale command file leaves a live slash command
    pointing at a deleted agent. These must disappear via feature 01's pruning,
    never by hand-deletion -- hand-deleting hides whether pruning works.
    """
    stale = (
        "claude/commands/phase-final-review.md",
        "opencode/agents/05-phase-final-review.md",
        "codex/agents/05-phase-final-review.toml",
        "codex/profiles/phase-final-review.config.toml",
    )

    for relative_path in stale:
        assert not (REPO_ROOT / relative_path).exists(), relative_path


# ---------------------------------------------------------------------------
# AC8 / AC9 -- the deleted machinery stays deleted
# ---------------------------------------------------------------------------


def test_no_ledger_machinery_survives() -> None:
    """AC8. The ledger read, its multi-run disambiguation, and the `eval:`
    commit-message fallback all existed to locate a phase's first commit. A PR
    has a base commit, so there is nothing left for them to find."""
    body = _prose()

    for token in (
        "ledger-commits.jsonl",
        "ledger-events.jsonl",
        "eval/runs/",
        "baseline source: ledger",
        "commit-message fallback",
    ):
        assert token not in body, f"ledger machinery survives: {token!r}"


def test_no_subphase_discovery_survives() -> None:
    """AC8. Subphase discovery and its refusal message are the multi-subphase
    premise itself. A PR has no subphases."""
    body = _prose()

    for token in ("subphase", "phase_0n", "prod-code-review for a single"):
        assert token not in body, f"subphase machinery survives: {token!r}"


def test_no_artifact_inventory_gate_survives() -> None:
    """AC8. The inventory refused to start a run when a pipeline artifact was
    absent. A PR declares no pipeline artifacts."""
    body = _prose()

    for token in ("artifact inventory", "inventory required artifacts", "missing —"):
        assert token not in body, f"artifact inventory survives: {token!r}"


def test_no_verdict_write_back_survives() -> None:
    """AC8/AC9 -- the highest-value deletion in the phase.

    The write-back was a two-file transactional edit with unique-match ambiguity
    detection and restore-on-second-write-failure: the riskiest implemented code
    in the pipeline. The rescope leaves it no reason to exist. It is also the
    single most plausible thing to reintroduce, because writing the verdict down
    looks like finishing the job.
    """
    body = _prose()

    for token in (
        "write-back",
        "write back",
        "phase_0n_summary.md",
        # "existing status line" was the write-back's target selector. The bare
        # phrase "status line" must stay legal -- the agent has to be able to
        # say it never writes one.
        "existing status line",
        "uniquely matching",
        "restore the first file",
    ):
        assert token not in body, f"write-back survives: {token!r}"

    # PROJECT_ROADMAP.md may only appear as a prohibition, never as a target.
    # Checked over normalized prose against the sentence the mention sits in,
    # because the prohibition wraps across lines.
    for sentence in body.split("."):
        if "project_roadmap.md" in sentence:
            assert "never" in sentence, f"roadmap named as a target: {sentence!r}"


def test_agent_declares_it_writes_no_status_line_anywhere() -> None:
    """AC9. The absence tests above prove the code is gone; this proves the
    replacement rule is stated, so a future editor knows it was deliberate."""
    body = _prose()

    assert "issue no verdict" in body or "issues no verdict" in body
    assert "never write a status line" in body

    # Asserted against the body, not the whole file: `Advisory only` also occurs
    # in the frontmatter `description:`, so deleting the advisory rule from the
    # instructions left the description behind and this assertion stayed green
    # over an agent that no longer told itself the report was advisory.
    instructions = _prose().split("---", 2)[-1]
    assert "the readiness report is advisory" in instructions


def test_no_archive_before_overwrite_survives() -> None:
    """AC8. Every run owns its own directory, so archiving has nothing to
    protect."""
    body = _prose()

    assert "archive" not in body or "nothing is ever archived" in body
    assert "never overwrite an existing archive" not in body
    assert "runs/<utc-yyyymmddthhmmssz>-<sequence>/" not in body


# ---------------------------------------------------------------------------
# AC2 -- one interaction block, and nothing after it
# ---------------------------------------------------------------------------


def test_all_three_questions_are_named_inside_the_upfront_block() -> None:
    body = ORCHESTRATOR.read_text(encoding="utf-8")
    block = body.split("## The Single Interaction Block", 1)[1].split("\n## ", 1)[0]
    lowered = block.lower()

    # (a) model-tier warning
    assert "model tier" in lowered
    assert "state of the art" in lowered or "state-of-the-art" in lowered
    # (b) suggested base + derivation source
    assert "base" in lowered and "derivation source" in lowered
    # (c) the PR-comment choice, all three options
    assert "post automatically" in lowered
    assert "ask once the report is written" in lowered
    assert "never" in lowered


def test_no_prompt_may_occur_after_the_block() -> None:
    """AC2's structural guarantee, and the requirement the plan flags as most
    likely to erode silently -- one reasonable-seeming question at a time."""
    body = _prose()

    assert "after this block, no code path may introduce a new prompt" in body
    # The four paths that would each plausibly want to ask.
    assert "not on evaluator failure" in body
    assert "not on timeout" in body
    assert "not when `gh` is absent" in body
    assert "not when no pr exists" in body
    assert "it never asks" in body


# ---------------------------------------------------------------------------
# AC3 / AC4 / AC5 / AC6 -- base derivation
# ---------------------------------------------------------------------------


def test_suggestion_chain_appears_in_order() -> None:
    """AC3. Order is the contract, not mere presence: `origin/main` ranked above
    `refs/remotes/origin/HEAD` would silently prefer a guess over a signal.

    Asserted against the *numbered list items* of the `Suggestion order`
    section, not `body.index()` over the whole document. Whole-document index
    ordering is inert here: `refs/remotes/origin/HEAD` occurs more than once
    (the ranked item, and again in the `base source:` example), so a reordering
    of the actual list still leaves an earlier stray occurrence in place and the
    ordering assertion passes over a broken contract. Verified by mutation: the
    index version survived a reorder of the list.
    """
    body = ORCHESTRATOR.read_text(encoding="utf-8")
    section = body.split("### Suggestion order", 1)[1].split("\n### ", 1)[0]

    items = re.findall(r"^\d+\.\s+(.*)$", section, flags=re.MULTILINE)
    expected = [
        "refs/remotes/origin/HEAD",
        "`origin/main`",
        "`origin/master`",
        "Present candidate branches",
    ]

    assert len(items) == len(expected), f"expected {len(expected)} ranked items, got {items}"
    for position, (item, token) in enumerate(zip(items, expected), start=1):
        assert token in item, f"rank {position} should offer {token!r}, got {item!r}"


def test_derivation_source_is_shown_with_the_suggestion() -> None:
    body = _prose()

    assert "base source:" in body
    assert "derivation source" in body


def test_self_exclusion_is_declared_for_branch_and_tracking_ref() -> None:
    """AC4 -- the load-bearing one. Any ranking over candidates that omits this
    filter returns the branch under review, with a diff of nothing, and reports
    no findings. It looks exactly like a pass."""
    body = _prose()

    assert "exclude the current branch and its own remote-tracking ref" in body
    assert "a branch is always its own nearest base" in body
    assert "and so is its remote-tracking ref" in body
    # The measured evidence, not just the claim.
    assert "git merge-base head repo_improvements_project" in body
    assert "git merge-base head origin/repo_improvements_project" in body


def test_the_three_wrong_suggestion_cases_are_named() -> None:
    """AC5. Correction must be first-class, not an escape hatch: the user can
    only correct a suggestion they have been told might be wrong.

    Scoped to the `Confirm, and make correction first-class` section rather than
    asserted over the whole document, for the same reason
    `test_suggestion_chain_appears_in_order` is: whole-document presence is inert
    wherever the phrase occurs twice. Both halves of this test were inert before
    scoping. `squash-merged base` also occurs in the `When there is no merge-base`
    section, so deleting the AC5 bullet left the stray occurrence and the
    assertion passed over a missing case; `first-class` also occurs in this
    section's own heading, so demoting the rule in the prose below it passed too.
    Verified by mutation: both deletions now fail here.
    """
    body = ORCHESTRATOR.read_text(encoding="utf-8")
    section = body.split("### Confirm, and make correction first-class", 1)[1]
    section = section.split("\n### ", 1)[0]

    cases = re.findall(r"^- \*\*(.+?)\*\*", section, flags=re.MULTILINE)
    assert len(cases) == 3, f"expected exactly three wrong-suggestion cases, got {cases}"

    joined = " ".join(cases).lower()
    for token in (
        "branch cut from another feature branch",
        "rebased branch",
        "squash-merged base",
    ):
        assert token in joined, f"AC5 case not named as a bullet: {token!r}"

    # The rule itself, not the heading it sits under.
    prose = re.sub(r"\s+", " ", section.split("\n- ", 1)[0]).lower()
    assert "correction is a first-class outcome" in prose
    assert "not an escape hatch" in prose


def test_override_replaces_the_suggestion_and_reaches_every_evaluator() -> None:
    """AC6. An override that stops at the orchestrator is worse than no
    override: the user believes they corrected the range."""
    body = _prose()

    assert "replaces" in body
    assert "every" in body and "downstream evaluator" in body
    assert "no evaluator may receive the original suggestion after an override" in body


def test_absent_merge_base_is_a_stop_not_a_fabricated_range() -> None:
    body = _prose()

    assert "do not fabricate a range" in body
    assert "stop, not a silent empty diff" in body


def test_no_remote_falls_through_to_local_candidates() -> None:
    body = _prose()

    assert "no remote" in body
    assert "local branches" in body


# ---------------------------------------------------------------------------
# AC7 -- the report root
# ---------------------------------------------------------------------------


def test_report_root_is_sha_and_timestamp_with_no_branch_component() -> None:
    body = ORCHESTRATOR.read_text(encoding="utf-8")

    assert "dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/" in body
    assert "No branch name appears in any path component" in body
    # The retired root must not survive anywhere in the body.
    assert "dev/phase-final-review/" not in body


def test_collision_policy_is_recorded() -> None:
    """The plan requires this be decided and recorded, not left implicit."""
    body = _prose()

    assert "same second" in body


def test_orchestrator_report_root_matches_the_canonical_skill_contract() -> None:
    """The root is declared in `pr-review-conventions` (feature 03). This reads
    it from there rather than restating it, so the orchestrator and the skill
    cannot drift into two roots that are each internally consistent."""
    skill = CONVENTIONS_SKILL.read_text(encoding="utf-8")
    declared = re.findall(r"dev/pr-review/<[^>\n]+>-<[^>\n]+>/", skill)

    assert declared, "conventions skill declares no report root"
    canonical = declared[0]
    assert set(declared) == {canonical}, f"skill declares multiple roots: {set(declared)}"
    assert canonical in ORCHESTRATOR.read_text(encoding="utf-8")


def test_report_root_migration_cannot_split_silently() -> None:
    """The `dev/phase-final-review/` -> `dev/pr-review/` migration is complete.

    Nothing else pins this. Written by feature 04 as a ledger of known drift --
    the orchestrator and both skills were on the new root while the surviving
    evaluators still declared the retired one, because features 05-07 owned
    those bodies. The failure mode it defended against was silent: if every
    feature in waves 4-6 assumed another one owned the migration, the roster
    would ship half-migrated with each half internally consistent, and the
    orchestrator would route evaluators to a root they do not write to.

    Features 05, 06 and 07 each tripped it and reconciled it, which is the ledger
    working as designed. Feature 07 migrated the last entry, so the set is now
    empty and the assertion has inverted meaning: it no longer records drift, it
    denies drift exists. In that form it is a permanent guard -- any `05*` body
    that declares the retired root fails here, whether by regression or by a new
    agent copying an old template. It does NOT exempt anything: the orchestrator
    and skills are separately asserted to be on the new root, so this cannot be
    satisfied by regressing them.
    """
    agents_dir = REPO_ROOT / "source_of_truth" / "agents"
    still_retired = {
        path.name
        for path in sorted(agents_dir.glob("05*.agent.md"))
        if "dev/phase-final-review/" in path.read_text(encoding="utf-8")
    }

    assert still_retired == EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION, (
        "an evaluator declares the retired `dev/phase-final-review/` report root. "
        "The migration completed in feature 07; this set is frozen empty. Migrate "
        "the agent to `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/` "
        "rather than re-adding it here.\n"
        f"  expected: {sorted(EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION)}\n"
        f"  actual:   {sorted(still_retired)}"
    )

    # The orchestrator is never in that set, on any path.
    assert ORCHESTRATOR.name not in still_retired


# ---------------------------------------------------------------------------
# AC10 -- the roster, in three distinct positions
# ---------------------------------------------------------------------------


def test_roster_declares_three_positions_not_a_flat_range() -> None:
    """AC10. A flat `05a`-`05g` reading makes AC10 contradict AC11: it implies
    an `05a` failure is survivable like any evaluator's, when nothing can run
    before the baseline exists."""
    body = _prose()

    assert "three distinct positions" in body
    assert "`05a` is not a fan-out evaluator" in body
    assert "`05g` is not one either" in body
    assert "its failure stops the run" in body


def test_fan_out_is_six_evaluators_including_the_security_seam() -> None:
    body = _prose()

    # Display name, not slug: `_build_agent_reference_map` keys on `agent.name`,
    # so only this form is rewritten to each root's identifier.
    assert "`04e diff security scan`" in body
    assert "**six**" in body
    assert "no new security agent is authored" in body


def test_frontmatter_agents_list_names_the_full_roster_by_display_name() -> None:
    """The propagator resolves `agents:` entries by display name. Note `05a`'s
    name is `Baseline Worktree` -- no numeric prefix, unlike every other 05x."""
    body = ORCHESTRATOR.read_text(encoding="utf-8")
    agents_line = next(
        line for line in body.splitlines() if line.startswith("agents:")
    )

    for name in (
        "Baseline Worktree",
        "05b Change Narrator",
        "05c Artifact Sweeper",
        "05d Consistency Auditor",
        "05e Dependency Auditor",
        "05f Test Health",
        "05g Readiness Synthesizer",
        "04e Diff Security Scan",
    ):
        assert name in agents_line, name


# ---------------------------------------------------------------------------
# AC11 -- partial-failure semantics
# ---------------------------------------------------------------------------


def test_evaluator_failure_never_aborts_and_never_passes() -> None:
    body = _prose()

    assert "never aborts the" in body
    assert "never becomes a passing result" in body
    assert "not-run" in body and "incomplete" in body

    # The append rule itself, not merely the filename. `evaluator-status.jsonl`
    # occurs twice -- once in the rule that writes a record, once in the
    # sentence that collects them for `05g` -- so bare presence stayed green
    # after the rule that produces the records was deleted, leaving an agent
    # that reads a file it never writes.
    assert "append exactly one json object to the current run's" in body
    assert "`evaluator-status.jsonl`" in body


def test_bounded_wait_is_retained() -> None:
    body = _prose()

    assert "10 minutes" in body
    assert "do not wait indefinitely" in body


def test_verdict_can_never_be_go_while_a_check_is_missing() -> None:
    body = _prose()

    assert "the verdict can never be `go` while any check is missing" in body
    assert "makes `go`\ninvalid" in body or "makes `go` invalid" in body
    assert "checks not run" in body


# ---------------------------------------------------------------------------
# AC12 -- read-only etiquette and the return contract
# ---------------------------------------------------------------------------


def test_orchestrator_never_reads_code_or_diffs() -> None:
    body = _prose()

    assert "do not read source code or diffs" in body
    assert "never open code or diffs" in body
    assert "path metadata" in body or "file metadata" in body


def test_return_contract_caps_every_subagent_at_ten_lines() -> None:
    body = _prose()

    assert "at most 10 lines" in body
    assert "no more than 10 lines" in body


def test_output_is_one_way_and_never_ingests_pr_comments() -> None:
    """Reading PR comments back in is a prompt-injection surface: the review
    would ingest attacker-authored text as instructions."""
    body = _prose()

    assert "one-way" in body
    assert "never read pr comments" in body
    assert "prompt-injection surface" in body


def test_model_and_harness_identity_stay_out_of_retained_reports() -> None:
    body = _prose()

    assert "do not place model or harness identity in retained review reports" in body


# ---------------------------------------------------------------------------
# Cleanliness -- the plan's keep-it-clean checklist
# ---------------------------------------------------------------------------


def test_report_templates_and_severity_are_not_restated() -> None:
    """They live in `pr-review-report` / `pr-review-conventions` (feature 03).
    Restating them here creates a second source of truth that drifts."""
    body = ORCHESTRATOR.read_text(encoding="utf-8")

    # The load instruction, not bare presence: both skill names also occur in the
    # evaluator invocation shape, so deleting the orchestrator's own load line
    # left those occurrences and this assertion stayed green.
    prose = _prose()
    assert "load `pr-review-conventions` before any review work" in prose
    assert "load `pr-review-report`" in prose
    for severity in ("Critical", "High", "Medium", "Low"):
        assert f"| {severity} |" not in body, f"severity table restated: {severity}"


def test_preflight_is_exactly_two_steps() -> None:
    body = ORCHESTRATOR.read_text(encoding="utf-8")
    preflight = body.split("## Preflight", 1)[1].split("\n## ", 1)[0]
    steps = [line for line in preflight.splitlines() if line.startswith("### ")]

    assert len(steps) == 2, f"preflight has {len(steps)} steps: {steps}"
