from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCHEMA = ROOT / "schemas" / "base-v9-4-release-evidence-v1.schema.json"
INTEGRITY = ROOT / "tools" / "check_base_v9_integrity.py"


class BaseV94ReleaseEvidenceContractTests(unittest.TestCase):
    def test_release_evidence_schema_requires_both_approved_issues(self) -> None:
        schema = json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
        self.assertIn("candidate_issue", schema["required"])
        self.assertIn("linked_issue", schema["required"])
        self.assertEqual(113, schema["properties"]["candidate_issue"]["const"])
        self.assertEqual(115, schema["properties"]["linked_issue"]["const"])

    def test_integrity_checker_validates_v94_evidence_record_before_release(self) -> None:
        text = INTEGRITY.read_text(encoding="utf-8")
        for required in (
            "V94_EVIDENCE_PATH",
            "V94_EVIDENCE_SCHEMA",
            "def v94_evidence_record_errors",
            "v9.4 release evidence payload does not match the candidate lock",
            "v9.4 release evidence candidate Issue does not match the candidate lock",
            "v9.4 release evidence linked Issue does not match the candidate lock",
            "v9.4 release evidence Registry does not match the candidate lock",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
