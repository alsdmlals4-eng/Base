from __future__ import annotations

import json
import re
import subprocess
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
DECISION = ROOT / "docs/operations/decisions/DEC-BASE-20260805-001.md"
FINALIZATION_COMMIT = "0b7c94f38d959efc0fc9442274c60b2e268a3c97"
TRUSTED_IMPLEMENTATION_MERGE = "bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1"
APPROVAL_REF = "https://github.com/alsdmlals4-eng/Base/pull/175#issuecomment-5197612170"


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

    def test_project_workflow_pins_the_trusted_merged_base_validator(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        marker = "repository: alsdmlals4-eng/Base"
        self.assertIn(marker, workflow)
        base_checkout = workflow.split(marker, 1)[1].split("- name: Set up Python", 1)[0]

        match = re.search(r"(?m)^\s+ref:\s*([0-9a-f]{40})\s*$", base_checkout)
        self.assertIsNotNone(
            match,
            "The Base validator checkout must pin an immutable full commit SHA instead of floating main.",
        )
        validator_commit = match.group(1)
        self.assertEqual(TRUSTED_IMPLEMENTATION_MERGE, validator_commit)

        required_markers = {
            "schemas/project-base-adapter-v1.schema.json": '"finalization_commit"',
            "tools/base_release_index.py": "RELEASE_FINALIZATION_COMMITS",
        }
        for path, required_marker in required_markers.items():
            result = subprocess.run(
                ["git", "-C", str(ROOT), "show", f"{validator_commit}:{path}"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                check=False,
            )
            self.assertEqual(
                0,
                result.returncode,
                f"Pinned validator commit cannot provide {path}: {result.stderr}",
            )
            self.assertIn(
                required_marker,
                result.stdout,
                f"Pinned validator commit lacks required fleet hardening in {path}",
            )

    def test_project_workflow_uses_a_trusted_historical_baseline_for_normal_prs(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        for marker in (
            'ADAPTER_PATH="skills/PROJECT_BASE_ADAPTER.json"',
            'git diff --name-only "$PR_BASE_SHA"...HEAD -- "$ADAPTER_PATH"',
            'PROTECTED_BASE_SHA="$PR_BASE_SHA"',
            'git show "$PR_BASE_SHA:$ADAPTER_PATH"',
            'payload["protected_baseline"]["commit"]',
            '--protected-base "$PROTECTED_BASE_SHA"',
        ):
            self.assertIn(marker, workflow)

        executable_workflow = "\n".join(
            line for line in workflow.splitlines() if not line.lstrip().startswith("#")
        )
        self.assertNotIn(
            '--protected-base "$PR_BASE_SHA"',
            executable_workflow,
            "Every unrelated PR must not be forced to rewrite the historical adapter baseline.",
        )
        self.assertIn(
            "Adapter migration PR: trust the immutable pull-request base as the new protected baseline",
            workflow,
        )
        self.assertIn(
            "Normal PR: trust the baseline recorded by the adapter at the immutable pull-request base",
            workflow,
        )

    def test_decision_records_approval_trusted_pin_and_current_rollout_state(self) -> None:
        text = DECISION.read_text(encoding="utf-8")
        for token in (
            "status: APPROVED",
            "protected_baseline_policy: OPTION_A_EXACT_TRUSTED_BASE_EQUALITY",
            "grimoire_adapter_authority: OPTION_A_RESTORE_BASE_V1_THIN_ADAPTER",
            APPROVAL_REF,
            "base_pr_source: 175",
            "implementation_pr: 185",
            f"trusted_implementation_merge: {TRUSTED_IMPLEMENTATION_MERGE}",
            "validator_pin_status: ADVANCED_TO_TRUSTED_MERGE",
            "project_rollout: PARTIAL_COMPLETE",
            "completed_projects: 4",
            "blocked_projects: 1",
            "separately_managed_projects: 1",
        ):
            self.assertIn(token, text)
        self.assertNotIn("project_mutation: AUTHORIZED_NOT_STARTED", text)


if __name__ == "__main__":
    unittest.main()
