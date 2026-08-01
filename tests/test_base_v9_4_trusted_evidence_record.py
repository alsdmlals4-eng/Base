from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "docs" / "operations" / "BASE_V9_4_RELEASE_EVIDENCE.json"
EVIDENCE_SCHEMA = ROOT / "schemas" / "base-v9-4-release-evidence-v1.schema.json"
LOCK_PATH = ROOT / "base-v9.4.lock.json"
REGISTRY_PATH = ROOT / "skills" / "SKILL_REGISTRY.json"
PAYLOAD_COMMIT = "a728712cb776ec98f4875914a580fcf7d0156593"
REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


class BaseV94TrustedEvidenceRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
        self.schema = json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
        self.lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    def test_evidence_validates_against_schema(self) -> None:
        errors = sorted(
            Draft202012Validator(self.schema).iter_errors(self.evidence),
            key=lambda item: list(item.path),
        )
        self.assertEqual([], [error.message for error in errors])

    def test_evidence_binds_payload_registry_issues_and_pr(self) -> None:
        self.assertEqual(PAYLOAD_COMMIT, self.evidence["payload_commit"])
        self.assertEqual(REGISTRY_SHA256, self.evidence["registry_sha256"])
        self.assertEqual(113, self.evidence["candidate_issue"])
        self.assertEqual(115, self.evidence["linked_issue"])
        self.assertEqual(118, self.evidence["candidate_pr"])
        self.assertEqual(
            self.lock["candidate_registry"]["sha256"],
            self.evidence["registry_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest(),
            self.evidence["registry_sha256"],
        )

    def test_payload_is_in_trusted_history(self) -> None:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PAYLOAD_COMMIT, "HEAD"],
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr.decode("utf-8", errors="replace"))

    def test_candidate_and_released_states_preserve_release_sequence(self) -> None:
        state = self.lock["release_state"]
        if state == "RELEASE_CANDIDATE":
            self.assertIsNone(self.lock["candidate_release_commit"])
            self.assertIsNone(self.lock["candidate_release_evidence_commit"])
        elif state == "BASE_RELEASED":
            self.assertEqual(PAYLOAD_COMMIT, self.lock["candidate_release_commit"])
            self.assertRegex(self.lock["candidate_release_evidence_commit"], r"^[0-9a-f]{40}$")
        else:
            self.fail(f"unsupported Base v9.4 release state: {state}")

    def test_evidence_limits_unexecuted_product_claims(self) -> None:
        limitations = self.evidence["limitations"]
        self.assertEqual("NOT_RUN", limitations["provider_billing_cache_hit_actual_savings"])
        self.assertEqual("NOT_APPLICABLE", limitations["automatic_chatgpt_model_switching"])
        self.assertEqual("NOT_RUN", limitations["godot_runtime_ui_motion_target_device_performance"])
        self.assertEqual("HUMAN_NOT_RUN", limitations["human_ui_comprehension_repetition_fatigue"])
        self.assertEqual("NOT_STARTED", limitations["project_adoption"])


if __name__ == "__main__":
    unittest.main()
