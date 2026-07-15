from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK_PATH = REPO_ROOT / ".github" / "hooks" / "lib" / "framework.py"
FIXTURES_DIR = Path(__file__).with_name("fixtures")


@pytest.fixture(scope="session")
def framework() -> ModuleType:
    if not FRAMEWORK_PATH.is_file():
        pytest.fail(
            "hook framework is not implemented: expected "
            f"{FRAMEWORK_PATH.relative_to(REPO_ROOT)}"
        )

    spec = importlib.util.spec_from_file_location("phase01_hook_framework", FRAMEWORK_PATH)
    if spec is None or spec.loader is None:
        pytest.fail(f"cannot load hook framework from {FRAMEWORK_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def recorded_payloads() -> list[dict[str, object]]:
    fixture_path = FIXTURES_DIR / "recorded_payloads.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))
