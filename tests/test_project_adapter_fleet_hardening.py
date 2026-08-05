from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import project_operating_contract as contract
from base_release_index import install_release_lock_paths


SCHEMA = ROOT / "schemas/project-base-adapter-v1.schema.json"
TEMPLATE = ROOT / "templates/project-operations/PROJECT_BASE_ADAPTER.json"
WORKFLOW = ROOT / "templates/project-operations/github/validate-project-base-adapter.yml"
FINALIZATION_COMMIT = "0b7c94f38d959efc0fc9442274c60b2e268a3c97"


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

    def test_release_finalization_commit_must_match_the_canonical_release_index(self) -> None:
        install_release_lock_paths(contract)
        lock = json.loads((ROOT / "base-v9.4.3.lock.json").read_text(encoding="utf-8"))
        adapter = {
            "base_release": {
                "repository": lock["repository"],
                "version": "9.4.3",
                "release_commit": lock["candidate_release_commit"],
                "release_evidence_commit": lock["candidate_release_evidence_commit"],
                "finalization_commit": "f" * 40,
            },
            "skill_registry": {"base": lock["candidate_registry"]},
        }

        errors, _, _ = contract._release_lock_contract(adapter, ROOT)
        self.assertTrue(
            any("finalization_commit" in error for error in errors),
            "A forged finalization pin must fail closed against the canonical release index.",
        )

        adapter["base_release"]["finalization_commit"] = FINALIZATION_COMMIT
        errors, _, _ = contract._release_lock_contract(adapter, ROOT)
        self.assertFalse(errors, "\n".join(errors))

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
