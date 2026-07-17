"""Contract assertions for the two judgment-shaped PR Review evaluators.

`05b-change-narrator` and `05f-test-health` are the pair the Phase document says
"differ enough to warrant individual design". Everything else in the `05` family
is a mechanical sweep, a worktree, or synthesis. These two are the deep-judgment
narrator and the delegating adapter, and each has a failure mode that looks
exactly like success:

  * `05b` can quietly keep narrating a *phase* -- subphases, per-subphase
    partitions, whole-phase baselines -- after the family has been rescoped to a
    branch diff. A PR has no subphases, so the concept does not degrade
    gracefully; it produces confident prose about a structure that is not there.
  * `05f` can quietly stop delegating and "just do a quick coverage check
    itself". That produces a plausible report which diverges from the project's
    real test analysis, and nothing in the output says so.

Style follows `tests/test_pr_review_orchestrator.py`: module-level `Path`
constants and plain `assert`, pytest-style -- not the `unittest` classes of
`tests/test_propagate_master_assets.py`.

A note on what is deliberately NOT asserted here. AC5b: Codex `agents.max_depth`
defaults to 1, and a blocked spawn causes the model to do the work inline and
report success rather than fail (`.github/learnings/debugging-learnings.md:25-38`).
Both `05f` -> `Test - Analyst` and `05b` -> per-directory readers sit at depth 2.
So a static assertion that the body *says* it delegates passes while the runtime
contract is broken. `test_delegation_is_declared_not_inlined` below is a
declaration assertion and is labelled as one. It is necessary and it is not
sufficient. Delegation is verifiable only from a runtime transcript, which is why
the plan routes AC5b to manual QA.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "source_of_truth" / "agents"

NARRATOR = AGENTS_DIR / "05b-change-narrator.agent.md"
TEST_HEALTH = AGENTS_DIR / "05f-test-health.agent.md"
RETIRED_TEST_HEALTH = AGENTS_DIR / "05h-test-health.agent.md"

OPENCODE_AGENTS_DIR = REPO_ROOT / "ports" / "opencode" / "agents"

# Feature 03's canonical report contract. Read, never restated -- the same
# discipline `tests/test_pr_review_orchestrator.py` applies to the orchestrator.
CONVENTIONS_SKILL = (
    REPO_ROOT / "source_of_truth" / "skills" / "pr-review-conventions" / "SKILL.md"
)


def _prose(path: Path) -> str:
    """The whole file, lowercased, whitespace collapsed to single spaces.

    The whole file, not the body: `description:` is frontmatter, and a
    subphase-attribution check scoped to the body passes while the deleted
    concept still ships to all three generated roots in the description.

    Collapsing whitespace keeps these assertions off line-wrap position. See
    `tests/test_readiness_synthesis_agents.py:16` for the failure this avoids.
    """
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


# ---------------------------------------------------------------------------
# AC1 / AC8 -- the rename
# ---------------------------------------------------------------------------


def test_test_health_is_renamed_to_the_05f_slug() -> None:
    """AC1. `05f` is freed by feature 02 retiring the seam analyzer."""
    assert TEST_HEALTH.is_file()
    assert not RETIRED_TEST_HEALTH.exists()


def test_test_health_declares_the_cross_feature_display_name() -> None:
    """AC1. `name:` is a cross-feature contract, not a cosmetic string.

    The propagator rewrites agent references by display name, so a near-miss
    ships to all three roots as literal prose instead of a live reference.
    `.github/agents/05-pr-review.agent.md:5` already forward-references this
    exact value in its `agents:` roster (feature 04 authored it before this
    agent existed), so this feature is what resolves that reference.
    """
    assert "name: 05f Test Health" in TEST_HEALTH.read_text(encoding="utf-8")


def test_no_retired_test_health_identifier_survives_in_either_agent() -> None:
    """AC1. Self-references, the report filename, and the opener all move.

    Checked against both files: the rename is only half done if the body still
    calls itself `05h`, and `05b` must not name its retired sibling either.
    """
    for path in (TEST_HEALTH, NARRATOR):
        assert "05h" not in _prose(path), f"retired 05h identifier survives in {path.name}"


def test_retired_test_health_slug_left_no_opencode_orphan() -> None:
    """AC8. OpenCode agent files key on the source slug, so a rename orphans one.

    Claude and Codex resolve an output name against stems already on disk
    (`z-test-health`), which survives the rename untouched -- so no orphan
    appears there and none should be looked for. OpenCode has no such
    indirection: `05h-test-health.md` is left behind as a stale, still-
    dispatchable duplicate unless feature 01's pruning removes it.

    Derived from disk rather than asserted as a literal pair: the retired stem
    is retired precisely because no source agent claims it.
    """
    source_slugs = {path.name[: -len(".agent.md")] for path in AGENTS_DIR.glob("*.agent.md")}
    assert "05h-test-health" not in source_slugs, "fixture: 05h must be retired by AC1"
    assert "05f-test-health" in source_slugs

    assert not (OPENCODE_AGENTS_DIR / "05h-test-health.md").exists(), (
        "the retired OpenCode slug survived the rename as a dispatchable duplicate"
    )
    assert (OPENCODE_AGENTS_DIR / "05f-test-health.md").is_file()


# ---------------------------------------------------------------------------
# AC5 / AC5b -- delegation
# ---------------------------------------------------------------------------


def test_delegation_target_display_name_is_exact() -> None:
    """AC5. The propagator resolves agent references by display name.

    `Test - Analyst` is the verified existing value at `test-analyst.agent.md:2`.
    A near-miss (`Test Analyst`, `test-analyst`) does not fail loudly -- it
    silently ships to all three roots as literal prose, and the delegation
    quietly stops existing.
    """
    assert "agents: [Test - Analyst]" in TEST_HEALTH.read_text(encoding="utf-8")

    target = (AGENTS_DIR / "test-analyst.agent.md").read_text(encoding="utf-8")
    assert "name: Test - Analyst" in target, "the delegate's display name moved"


def test_delegation_is_declared_not_inlined() -> None:
    """AC5. A DECLARATION assertion. It cannot detect a runtime inline fallback.

    See this module's docstring: with Codex `max_depth` at its default of 1 the
    depth-2 spawn is blocked and the model does the work inline while reporting
    success. This test passes in exactly that case. It pins the declaration so a
    deliberate rewrite into a reimplementation fails; the runtime contract is
    verified only by manual QA against a transcript (AC5b).
    """
    body = _prose(TEST_HEALTH)

    # The imperative itself, with its objects and target attached. A bare
    # `"delegate" in body` cannot fail: the token occurs 13 times in this file
    # ("the delegate's analysis procedure", "delegate inputs", "as delegated
    # analysis"), so the one sentence that actually issues the instruction can
    # be reversed to "Perform coverage..." while the guard stays green.
    assert (
        "delegate coverage, redundancy, and flake-candidate analysis to `test - analyst`"
        in body
    )
    assert "analysis belongs to `test - analyst`" in body
    assert "do not reimplement the delegate's analysis procedure" in body
    assert "no local scan or test-analysis procedure is defined here" in body


def test_test_health_names_the_max_depth_fallback() -> None:
    """AC5b. The trap is that the failure is silent, so it must be named.

    `.github/learnings/debugging-learnings.md:25-38`: a blocked spawn does not
    raise. The agent must know the depth requirement and must know that
    continuing inline is the failure, not the fallback.

    Each assertion is a distinct single-occurrence claim. Asserting a bare
    `"max_depth" in body` passes while the paragraph that explains the default
    is deleted, because the required-value sentence also contains the token.
    """
    body = _prose(TEST_HEALTH)

    assert "`agents.max_depth` defaults to 1" in body
    assert "requires `[agents] max_depth = 2`" in body
    assert "silently performs the work inline and reports success" in body
    assert "never continue inline" in body


def test_test_health_preserves_the_not_run_ceiling() -> None:
    """AC5. Preserved verbatim through the rename -- not regressed.

    `.github/learnings/review-learnings.md:267-271`: a not-run marker without a
    visible readiness ceiling reads as neutral coverage.

    Pinned at the rule that requires the entry, not as a bare `"not run"`: the
    token also appears in the max_depth paragraph ("that is the NOT RUN case
    below"), so a loose check stays green while the rule that actually requires
    the entry is deleted.
    """
    body = _prose(TEST_HEALTH)

    assert "write a report with a not run entry and concrete reason" in body
    assert "verdict ceiling is below go" in body
    assert "missing analysis is never a clean result" in body


# ---------------------------------------------------------------------------
# AC6 -- the delta rescope
# ---------------------------------------------------------------------------


def test_test_health_reports_a_branch_scoped_delta() -> None:
    """AC6. `Test - Analyst` analyzes a suite; `05f` reports what the branch did
    to it. That reframing is the whole rescope.

    Asserted at the section headers, not as bare tokens: `coverage delta` also
    appears in the not-measurable rule below, so a loose membership check stays
    green while the required report section is renamed away.
    """
    body = _prose(TEST_HEALTH)

    assert "the subject is the branch diff `<merge-base>..head`" in body
    assert "the **coverage delta** from base to head" in body
    assert "**test redundancy** introduced or left behind by the branch" in body
    assert "**flake candidates**" in body


def test_test_health_names_its_evidence_source() -> None:
    """AC6 / Plan E. `.github/learnings/cross-phase-decisions.md:15`: an evidence
    artifact that does not name its revision cannot be reconciled later."""
    body = _prose(TEST_HEALTH)

    assert "name the evidence source for every one of them" in body
    assert "the tool it came from and the revision pair it covers" in body
    assert "cannot be reconciled against later work" in body


def test_test_health_consumes_the_baseline_worktree_rather_than_creating_one() -> None:
    """AC6. `05a-baseline-worktree` owns the checkout. `05f` has no `execute` and
    could not create one anyway -- but the instruction must not invite trying.

    The delegation names the agent by its *display name*, backticked, because
    that is the only form `_build_agent_reference_map` can rewrite: it keys on
    `agent.name`, so a slug reference propagates verbatim into roots where the
    agent is filed as `z-baseline-worktree` and resolves to nothing. Assert the
    backticked form -- bare "baseline worktree" also occurs in surrounding prose
    and would make this guard inert.
    """
    body = _prose(TEST_HEALTH)

    assert "`baseline worktree`" in body
    assert "do not create, switch, or remove a worktree yourself" in body


def test_test_health_degrades_honestly_without_coverage_tooling() -> None:
    """AC6. Absence of coverage tooling is a stated limitation, not a failure --
    this family ships to projects that have none. The degradation must not be a
    licence to hand-roll a check."""
    body = _prose(TEST_HEALTH)

    assert "not-measurable" in body
    assert "do not grow a coverage runner" in body


def test_test_health_drops_the_subphase_redundancy_framing() -> None:
    """AC6. The old body scoped redundancy `cross-subphase`. A PR has none."""
    assert "subphase" not in _prose(TEST_HEALTH)


# ---------------------------------------------------------------------------
# AC2 -- subphase attribution is deleted outright
# ---------------------------------------------------------------------------


def test_narrator_has_no_subphase_attribution_anywhere_in_the_file() -> None:
    """AC2 / AC1b. Whole file, because `description:` is where it hid.

    The narrator's description read "whole-phase baseline-to-HEAD change
    narrative *with subphase attribution* and churn hotspots". A body-scoped
    assertion passes while that line ships the deleted concept to all three
    generated roots. Subphase attribution is deleted outright rather than
    adapted: a PR has no subphases, so there is nothing to map paths onto, and
    the concept does not fail loudly -- it produces confident prose about a
    structure that does not exist.
    """
    assert "subphase" not in _prose(NARRATOR)


def test_narrator_frames_the_comparison_as_the_branch_diff() -> None:
    """AC2. Whole-phase baseline->final becomes `<merge-base>..HEAD`.

    Pinned in both positions that must hold -- the assigned-scope statement and
    the reconciliation step that ranges the narrative. The token occurs three
    times, so a bare membership check stays green while either individual
    framing is deleted.
    """
    body = _prose(NARRATOR)

    assert "the subject is the branch diff `<merge-base>..head`" in body
    assert (
        "reconcile the chunk summaries into one narrative over `<merge-base>..head`"
        in body
    )
    assert "whole-phase" not in body


def test_narrator_keeps_churn_hotspots() -> None:
    """AC2. Churn hotspots survive the rescope -- they were never a phase
    concept, so deleting them alongside subphases would over-apply AC2. The
    definition is re-anchored on directories, not on subphase intersection.

    Pinned at the procedure step and the report section, not as a bare phrase:
    the phrase also appears in `description:`, so a loose check stays green
    while the procedure that actually produces the hotspots is deleted.
    """
    body = _prose(NARRATOR)

    assert "list every churn hotspot" in body
    assert "no hotspots is a completed finding" in body
    assert "churn-hotspot table" in body


# ---------------------------------------------------------------------------
# AC3 -- the narrative spine
# ---------------------------------------------------------------------------


def test_narrator_accounts_for_intent_not_only_content() -> None:
    """AC3. This is why `05b` holds the top model tier.

    "What changed" is mechanical and the sweeps already cover it. The readiness
    report's narrative spine is "what is this branch trying to do", which is a
    judgment no other evaluator in the family makes.

    Pinned in both positions it must hold -- the opening charter and the
    reconciliation step that actually orders the narrative -- because a single
    membership check stays green while either one is deleted. The third
    assertion is the honesty rule: an intent account with no evidence behind it
    is worse than none, since it reads exactly like one that has evidence.
    """
    body = _prose(NARRATOR)

    assert "an account of **what the branch is trying to do**" in body
    assert "lead with **what the branch is trying to do**" in body
    assert "where the evidence does not support an intent, say that instead of inventing one" in body


def test_narrator_keeps_the_top_tier_requirement() -> None:
    """AC3. A lower tier is an execution limitation to record, never a pass."""
    body = _prose(NARRATOR)

    assert "top available, state-of-the-art model tier" in body
    assert "a lower tier is an execution limitation to record, never a passing result" in body


# ---------------------------------------------------------------------------
# AC4 -- chunking is structural, not advisory
# ---------------------------------------------------------------------------


def test_narrator_chunking_is_structural() -> None:
    """AC4. The phase's worst context-blowout risk, and the one mitigation.

    Every other evaluator is mechanical, delegating, or report-only. This one
    reads the diff and forms a judgment about it, and a long-lived branch can
    hand it a diff larger than any single context. "Be concise" is not an
    implementation: the requirement is bounded chunks read one at a time, reader
    delegations as the pressure valve, and detail on disk.

    The chunk-reading instruction is asserted with its objects attached. A bare
    `"one bounded chunk at a time"` also matches the max_depth paragraph below,
    which would keep this green while step 2 stopped saying how to read.
    """
    body = _prose(NARRATOR)

    assert "read one bounded chunk at a time from the baseline worktree and the head tree" in body
    assert "never load the full branch diff into one context" in body
    assert "per-directory reader delegations" in body


def test_narrator_chunking_degrades_when_readers_are_unavailable() -> None:
    """AC4 / AC5b. Reader spawns sit at depth 2 and Codex `max_depth` defaults
    to 1, so the pressure valve is not always there. The fallback must be a
    stated serial path -- not an inline improvisation that silently loads more
    than one chunk."""
    body = _prose(NARRATOR)

    assert "otherwise process the same chunks serially in this context" in body
    assert "`agents.max_depth` defaults to 1" in body
    assert "it is never a licence to read the whole diff at once" in body


# ---------------------------------------------------------------------------
# AC7 -- report contract, both agents
# ---------------------------------------------------------------------------


def test_both_agents_declare_the_ten_line_return() -> None:
    """AC7. The return budget is a hard requirement, not a style note: `05b` is
    the agent most exposed to a diff bigger than its context."""
    for path in (NARRATOR, TEST_HEALTH):
        body = _prose(path)
        assert "no more than 10 lines" in body, f"{path.name} dropped the return budget"
        assert "on disk" in body, f"{path.name} dropped the detail-on-disk rule"


def test_both_agents_defer_the_report_path_to_the_conventions_skill() -> None:
    """AC7. Feature 03 owns the report root; these agents must not restate it.

    Read from the skill rather than restated here, for the same reason the
    agents must not restate it: two internally-consistent roots is exactly the
    silent split `tests/test_pr_review_orchestrator.py` pins. The retired
    `dev/phase-final-review/` root must be gone from both files.
    """
    skill = CONVENTIONS_SKILL.read_text(encoding="utf-8")
    declared = re.findall(r"dev/pr-review/<[^>\n]+>-<[^>\n]+>/", skill)
    assert declared, "conventions skill declares no report root"

    for path in (NARRATOR, TEST_HEALTH):
        text = path.read_text(encoding="utf-8")
        assert "dev/phase-final-review/" not in text, (
            f"{path.name} still declares the retired report root"
        )
        # The load instruction itself, not a bare token: `05b` names
        # `pr-review-conventions` twice (the load line and the partial-failure
        # rules), so a membership check stays green there while the line that
        # actually loads the skill is deleted.
        assert "Load `pr-review-conventions` before doing any review work." in text, (
            f"{path.name} must load the skill that owns the report path"
        )


def test_neither_agent_produces_a_verdict() -> None:
    """Non-goal. Both are evidence producers; `05g` decides. An evaluator that
    reaches a verdict pre-empts synthesis and double-counts its own findings."""
    for path in (NARRATOR, TEST_HEALTH):
        assert "`05g` decides" in _prose(path), f"{path.name} lost the verdict boundary"
