"""Structural and in-memory guards for the session model preflight contract."""

from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import propagate_master_assets as routing_module  # noqa: E402


PHASE_PATH = REPO_ROOT / "source_of_truth/agents/04-phase-execute.agent.md"
CONVENTIONS_PATH = (
    REPO_ROOT / "source_of_truth/instructions/orchestrator-conventions.instructions.md"
)
MANIFEST_PATH = REPO_ROOT / "source_of_truth/skills/feature-plan-set/SKILL.md"
ROUTING_PATH = REPO_ROOT / "source_of_truth/config/model-routing.json"
TIERS = ("low", "medium", "high")
STATUSES = ("enforced", "fallback", "unverified")
RECORD_FIELDS = (
    "requested_model",
    "user_override",
    "resolved_route",
    "resolution_status",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _preflight_records(
    routing: dict[str, dict[str, dict[str, str]]],
    harness: str,
    *,
    overrides: dict[str, str] | None = None,
    reported_routes: dict[str, str] | None = None,
) -> tuple[dict[str, str], ...]:
    overrides = overrides or {}
    reported_routes = reported_routes or {}
    records: list[dict[str, str]] = []
    for tier in TIERS:
        requested = routing[tier][harness]["model"]
        override = overrides.get(tier)
        effective = override or requested
        reported = reported_routes.get(tier)
        if reported is None:
            status = "unverified"
            resolved = "unreported"
        elif reported == effective:
            status = "enforced"
            resolved = reported
        else:
            status = "fallback"
            resolved = reported
        records.append(
            {
                "requested_model": requested,
                "user_override": override or "none",
                "resolved_route": resolved,
                "resolution_status": status,
            }
        )
    return tuple(records)


def _unsupported_harness_records(
    routing: dict[str, dict[str, dict[str, str]]], harness: str
) -> tuple[dict[str, str], ...]:
    assert harness not in routing_module.MODEL_HARNESSES
    return tuple(
        {
            "requested_model": "unavailable",
            "user_override": "none",
            "resolved_route": "unsupported harness",
            "resolution_status": "unverified",
        }
        for _tier in routing
    )


def _status_errors(records: tuple[dict[str, str], ...]) -> set[str]:
    errors: set[str] = set()
    for record in records:
        if tuple(record) != RECORD_FIELDS:
            errors.add("four-field record shape")
        status = record.get("resolution_status")
        if status not in STATUSES:
            errors.add(f"invalid status: {status}")
    return errors


def _override_isolation_errors(before: bytes, after: bytes) -> set[str]:
    return {"routing file changed"} if before != after else set()


def _manifest_status_errors(text: str) -> set[str]:
    errors: set[str] = set()
    field_lines = [
        line for line in text.splitlines() if "`resolved_model_status`" in line
    ]
    if not field_lines:
        errors.add("manifest field")
    if not all(status in "\n".join(field_lines) for status in STATUSES):
        errors.add("manifest status vocabulary")
    return errors


def test_preflight_runs_before_feature_selection_and_reuses_the_loader() -> None:
    phase = _read(PHASE_PATH)
    preflight_start = phase.index("### Session Model Preflight")
    execution_start = phase.index("## Execution Pipeline")
    selection = phase.index("Execute one feature at a time")

    assert preflight_start < execution_start < selection
    assert "load_model_routing()" in phase
    assert "json.loads" not in phase
    assert "model-routing.json" in phase
    assert all(f"`{tier}`" in phase for tier in TIERS)


def test_preflight_record_has_four_distinct_fields_and_three_statuses() -> None:
    routing = routing_module.load_model_routing()
    records = _preflight_records(routing, "codex")

    assert not _status_errors(records)
    assert len(RECORD_FIELDS) == len(set(RECORD_FIELDS)) == 4
    assert {record["resolution_status"] for record in records} == {"unverified"}

    fallback_records = _preflight_records(
        routing,
        "codex",
        reported_routes={tier: "reported-fallback" for tier in TIERS},
    )
    assert {record["resolution_status"] for record in fallback_records} == {"fallback"}
    assert not any(
        record["resolution_status"] == "enforced"
        for record in fallback_records
    )

    mutated = tuple(
        {**record, "resolution_status": "enforced"}
        for record in records
    )
    assert not _status_errors(mutated)
    assert {record["resolution_status"] for record in mutated} == {"enforced"}


def test_each_tier_override_changes_only_the_current_run() -> None:
    before = ROUTING_PATH.read_bytes()
    routing = routing_module.load_model_routing()

    for tier in TIERS:
        override = f"run-only-{tier}"
        run_routing = copy.deepcopy(routing)
        run_routing[tier]["codex"]["model"] = override
        records = _preflight_records(
            routing,
            "codex",
            overrides={tier: run_routing[tier]["codex"]["model"]},
        )

        record = records[TIERS.index(tier)]
        assert record["requested_model"] == routing[tier]["codex"]["model"]
        assert record["user_override"] == override
        assert _override_isolation_errors(before, ROUTING_PATH.read_bytes()) == set()

        next_run = routing_module.load_model_routing()
        assert next_run[tier]["codex"]["model"] != override

    assert ROUTING_PATH.read_bytes() == before


def test_override_isolation_guard_is_load_bearing() -> None:
    before = ROUTING_PATH.read_bytes()
    assert not _override_isolation_errors(before, before)
    assert "routing file changed" in _override_isolation_errors(before, before + b"\n")


def test_status_vocabulary_guard_is_load_bearing() -> None:
    routing = routing_module.load_model_routing()
    records = _preflight_records(routing, "codex")
    assert not _status_errors(records)

    mutated = tuple(
        {key: value for key, value in record.items() if key != "resolution_status"}
        for record in records
    )
    assert "four-field record shape" in _status_errors(mutated)


def test_unsupported_harness_discloses_fallback_without_claiming_enforcement() -> None:
    phase = _read(PHASE_PATH)
    conventions = _read(CONVENTIONS_PATH)
    records = _unsupported_harness_records(routing_module.load_model_routing(), "zed")

    assert len(records) == len(TIERS)
    assert all(record["resolution_status"] == "unverified" for record in records)
    assert not any(record["resolution_status"] == "enforced" for record in records)
    assert "fallback" in phase.lower()
    assert "unsupported harness" in phase.lower()
    assert "fallback" in conventions.lower()
    assert "unsupported harness" in conventions.lower()


def test_manifest_copies_the_preflight_status_vocabulary() -> None:
    text = _read(MANIFEST_PATH)
    assert not _manifest_status_errors(text)

    mutated = text.replace("`unverified`", "`unknown`")
    assert "manifest status vocabulary" in _manifest_status_errors(mutated)


def test_preflight_conventions_are_shared_and_do_not_expose_credentials() -> None:
    phase = _read(PHASE_PATH)
    conventions = _read(CONVENTIONS_PATH)
    combined = f"{phase}\n{conventions}"
    assert "requested_model" in combined
    assert "user_override" in combined
    assert "resolved_route" in combined
    assert "resolution_status" in combined
    assert "source_of_truth/config/model-routing.json" in phase
    assert not re.search(
        r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9]|ghp_[A-Za-z0-9]|Bearer\s+\S+|api[_-]?key\s*[:=])",
        combined,
        re.I,
    )


def test_preflight_contract_guard_fails_when_a_status_is_removed() -> None:
    text = _read(CONVENTIONS_PATH)
    assert all(status in text for status in STATUSES)
    mutated = text.replace("`unverified`", "`unknown`")
    missing = {status for status in STATUSES if status not in mutated}
    assert missing == {"unverified"}
