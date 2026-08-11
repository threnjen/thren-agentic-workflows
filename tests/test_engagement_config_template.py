"""The engagement config template must stay in step with its schema.

`engagement-template.yaml` is what the Client Deliverable orchestrator hands a
user to fill out, so a required field the schema gained but the template never
grew is a field nobody is asked for -- the run fails validation later, at the
user's expense.

These checks are structural: required fields are read out of the schema's own
tables rather than restated here, so adding a required field to the skill and
forgetting the template fails this file. Each extraction asserts it found
something first; a table rewrite that breaks the parse fails loudly instead of
silently verifying nothing.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "source_of_truth" / "skills" / "engagement-configuration"
SCHEMA = SKILL_DIR / "SKILL.md"
TEMPLATE = SKILL_DIR / "engagement-template.yaml"

# A schema row: | `field` | yes | meaning |  -- required is the second cell.
ROW = re.compile(r"^\|\s*`([a-z_]+)`\s*\|\s*(yes|no|[^|]+?)\s*\|", re.MULTILINE)


def _schema_fields() -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in ROW.finditer(SCHEMA.read_text())}


# A live (uncommented) YAML key, at any indent, optionally the first key of a
# list item: `  - name:` and `    path:` both count.
LIVE_KEY = re.compile(r"^\s*(?:-\s+)?([a-z_]+):", re.MULTILINE)


def _live_keys(text: str) -> set[str]:
    body = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    return {m.group(1) for m in LIVE_KEY.finditer(body)}


class TemplateSchemaParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fields = _schema_fields()
        # Guard the guard: an unparseable schema must fail, not pass vacuously.
        self.assertGreater(
            len(self.fields), 5, "parsed too few schema rows -- the table shape changed"
        )
        self.text = TEMPLATE.read_text()
        self.live = _live_keys(self.text)
        self.assertIn("pairs", self.live, "template lost its pairs block")

    def test_every_required_field_is_present_and_uncommented(self) -> None:
        required = {f for f, req in self.fields.items() if req == "yes"}
        self.assertTrue(required, "no required fields parsed out of the schema")

        for field in required:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.live,
                    f"required schema field '{field}' is missing (or commented out) "
                    "in the template",
                )

    def test_every_optional_field_appears_at_least_as_a_comment(self) -> None:
        optional = {f for f, req in self.fields.items() if req == "no"}
        self.assertTrue(optional, "no optional fields parsed out of the schema")

        for field in optional:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.text,
                    f"optional schema field '{field}' is never mentioned in the template",
                )

    def test_required_values_are_blanks_the_user_must_replace(self) -> None:
        """The orchestrator treats a lingering FILL ME as 'not authored yet'."""
        # Only scalars can carry a blank; `pairs` and the role keys are mappings.
        scalars = {"sow_document", "deliverables_spec", "name", "path"}
        required = {f for f, req in self.fields.items() if req == "yes"} & scalars
        self.assertIn("sow_document", required, "schema no longer requires sow_document")

        for field in required:
            with self.subTest(field=field):
                # Either `field: FILL ME`, or a list whose first live entry is
                # `- FILL ME` (sow_document ships as a priority-ordered list).
                self.assertRegex(
                    self.text,
                    rf"(?m)^\s*(?:-\s+)?{field}:(?:\s*FILL ME|\s*(?:\n\s*#[^\n]*)*\n\s*-\s*FILL ME)",
                    f"required field '{field}' must ship blank as FILL ME",
                )


if __name__ == "__main__":
    unittest.main()
