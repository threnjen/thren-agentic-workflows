import json
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / ".github" / "hooks" / "scripts" / "rtk-rewrite.sh"


@pytest.mark.parametrize(
    "command",
    ["ls -la", "grep -R foo .", "find . -maxdepth 2", "pytest -q tests"],
)
def test_rtk_rewrite_skips_common_inspection_and_test_commands(command: str) -> None:
    payload = json.dumps({"tool_input": {"command": command}})
    completed = subprocess.run(
        ["bash", str(SCRIPT_PATH)],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""
