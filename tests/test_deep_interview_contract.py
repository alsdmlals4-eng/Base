from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.check_interview_contract import REQUIRED_HEADINGS, requires_deep_interview, validate_registry


ROOT = Path(__file__).resolve().parents[1]


class DeepInterviewContractTests(unittest.TestCase):
    def test_template_registry_matches_schema(self) -> None:
        payload = json.loads((ROOT / "templates/project-operations/INTERVIEW_REGISTRY.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/interview-registry-v1.schema.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(payload))
        self.assertEqual(errors, [])

    def test_record_template_has_required_sections(self) -> None:
        text = (ROOT / "templates/project-operations/INTERVIEW_RECORD.md").read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            self.assertIn(heading, text)

    def test_executable_prompt_is_blocked_before_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root / "interview.md"
            record.write_text((ROOT / "templates/project-operations/INTERVIEW_RECORD.md").read_text(encoding="utf-8"), encoding="utf-8")
            registry = root / "INTERVIEW_REGISTRY.json"
            registry.write_text(json.dumps({
                "schema_version": 1,
                "registry_role": "deep-requirement-interview-index",
                "interviews": [{
                    "interview_id": "INT-2026-001-test",
                    "title": "Test",
                    "record_path": "interview.md",
                    "status": "AWAITING_USER_CONFIRMATION",
                    "work_contract_type": "approved_direct_request",
                    "created_at": "2026-07-19",
                    "updated_at": "2026-07-19",
                    "user_confirmation_ref": None,
                    "executable_prompt_path": "prompt.md",
                    "supersedes": None,
                }],
            }), encoding="utf-8")
            errors = validate_registry(root, registry, ROOT / "schemas/interview-registry-v1.schema.json")
            self.assertTrue(any("forbidden before CONFIRMED" in error for error in errors))

    def test_confirmed_interview_requires_evidence_and_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "record.md").write_text((ROOT / "templates/project-operations/INTERVIEW_RECORD.md").read_text(encoding="utf-8"), encoding="utf-8")
            registry = root / "INTERVIEW_REGISTRY.json"
            registry.write_text(json.dumps({
                "schema_version": 1,
                "registry_role": "deep-requirement-interview-index",
                "interviews": [{
                    "interview_id": "INT-2026-002-test",
                    "title": "Test",
                    "record_path": "record.md",
                    "status": "CONFIRMED",
                    "work_contract_type": "github_issue",
                    "created_at": "2026-07-19",
                    "updated_at": "2026-07-19",
                    "user_confirmation_ref": None,
                    "executable_prompt_path": None,
                    "supersedes": None,
                }],
            }), encoding="utf-8")
            errors = validate_registry(root, registry, ROOT / "schemas/interview-registry-v1.schema.json")
            self.assertTrue(any("requires user_confirmation_ref" in error for error in errors))
            self.assertTrue(any("requires executable_prompt_path" in error for error in errors))

    def test_source_inventory_is_complete_and_classified(self) -> None:
        path = ROOT / "docs/knowledge/research/inventories/ouroboros-6202662e.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["commit"], "6202662eae2dad0531225a93e27b18f792bb139b")
        self.assertEqual(payload["tracked_file_count"], 1465)
        self.assertEqual(payload["tracked_file_count"], len(payload["files"]))
        self.assertNotIn("other", payload["role_counts"])
        self.assertTrue(all(item["sha256"] and item["role"] for item in payload["files"]))

    def test_skill_contract_has_triggers_exceptions_and_confirmation_gate(self) -> None:
        text = (ROOT / "skills/conducting-deep-requirement-interviews/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "Mandatory triggers", "Exceptions", "repository_observed", "AWAITING_USER_CONFIRMATION",
            "CONFIRMED", "transforming-requests-into-prompts", "사용자 확인",
            "sharpening-project-domain-language-and-decisions",
        ):
            self.assertIn(term, text)

    def test_mandatory_triggers_and_mechanical_exceptions(self) -> None:
        for change_type in ("feature", "game-experience", "art-direction", "architecture", "workflow", "base-change-proposal"):
            with self.subTest(change_type=change_type):
                self.assertTrue(requires_deep_interview({change_type}))
        self.assertFalse(requires_deep_interview({"typo"}, typo_only=True))
        self.assertFalse(requires_deep_interview({"mechanical"}, explicit_single_file_mechanical=True))
        self.assertFalse(requires_deep_interview({"verification-rerun"}, unchanged_validation_rerun=True))
        self.assertTrue(requires_deep_interview({"art-direction"}, explicit_single_file_mechanical=True))

    def test_detailed_request_uses_inverted_interview(self) -> None:
        text = (ROOT / "skills/conducting-deep-requirement-interviews/references/ambiguity-and-closure.md").read_text(encoding="utf-8")
        self.assertIn("상세 요청의 역인터뷰", text)
        self.assertIn("잘못되거나 빠진 부분", text)


if __name__ == "__main__":
    unittest.main()
