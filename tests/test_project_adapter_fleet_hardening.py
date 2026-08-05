from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/project-base-adapter-v1.schema.json"
TEMPLATE = ROOT / "templates/project-operations/PROJECT_BASE_ADAPTER.json"
WORKFLOW = ROOT / "templates/project-operations/github/validate-project-base-adapter.yml"


class ProjectAdapterFleetHardeningTests(unittest.TestCase):
    def test_release_finalization_commit_is_part_of_the_canonical_adapter_contract(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))

        base_release_schema = schema["properties"]["base_release"]
        self.assertIn("finalization_commit", base_release_schema["properties"])
        self.assertEqual(
            base_release_schema["properties"]["finalization_commit"]["pattern"],
            "^[0-9a-f]{40}$",
        )
        self.assertIn("finalization_commit", template["base_release"])
        self.assertRegex(template["base_release"]["finalization_commit"], r"^[0-9a-f]{40}$")

        errors = list(Draft202012Validator(schema).iter_errors(template))
        self.assertFalse(errors, "\n".join(error.message for error in errors))

    def test_project_workflow_pins_the_base_validator_to_an_immutable_commit(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        marker = "repository: alsdmlals4-eng/Base"
        self.assertIn(marker, workflow)
        base_checkout = workflow.split(marker, 1)[1].split("- name: Set up Python", 1)[0]

        match = re.search(r"(?m)^\s+ref:\s*([0-9a-f]{40})\s*$", base_checkout)
        self.assertIsNotNone(
            match,
            "The Base validator checkout must pin an immutable full commit SHA instead of floating main.",
        )
        self.assertNotEqual(match.group(1), "0" * 40)


if __name__ == "__main__":
    unittest.main()
