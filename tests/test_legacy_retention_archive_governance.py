from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    path = ROOT / "templates/project-operations/github/check_archive_governance.py"
    spec = importlib.util.spec_from_file_location("check_archive_governance", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LegacyRetentionArchiveGovernanceTests(unittest.TestCase):
    def test_shared_skill_and_archive_contract_files_exist(self) -> None:
        required = [
            "skills/governing-legacy-retention-and-archives/SKILL.md",
            "skills/governing-legacy-retention-and-archives/references/archive-contract.md",
            "skills/governing-legacy-retention-and-archives/references/pressure-scenarios.md",
            "schemas/archive-retention-adapter-v1.schema.json",
            "schemas/archive-manifest-v1.schema.json",
            "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json",
            "templates/project-operations/ARCHIVE_MANIFEST.json",
            "templates/project-operations/ARCHIVE_README.md",
            "templates/project-operations/github/check_archive_governance.py",
        ]
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing)

    def test_registry_contains_legacy_retention_skill(self) -> None:
        registry = json.loads(
            (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        )
        ids = {item["skill_id"] for item in registry["skills"]}
        self.assertIn("governing-legacy-retention-and-archives", ids)

    def test_adapter_and_manifest_templates_match_schemas(self) -> None:
        pairs = (
            (
                "schemas/archive-retention-adapter-v1.schema.json",
                "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json",
            ),
            (
                "schemas/archive-manifest-v1.schema.json",
                "templates/project-operations/ARCHIVE_MANIFEST.json",
            ),
        )
        for schema_path, instance_path in pairs:
            with self.subTest(instance=instance_path):
                schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
                instance = json.loads((ROOT / instance_path).read_text(encoding="utf-8"))
                errors = sorted(
                    Draft202012Validator(schema).iter_errors(instance),
                    key=lambda error: list(error.path),
                )
                self.assertEqual([], [error.message for error in errors])

    def test_adapter_schema_rejects_unsafe_retention_policy(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/archive-retention-adapter-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        adapter = json.loads(
            (ROOT / "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json").read_text(
                encoding="utf-8"
            )
        )
        adapter["policies"]["blank_placeholders_allowed"] = True
        adapter["policies"]["secrets_may_be_archived"] = True
        errors = list(Draft202012Validator(schema).iter_errors(adapter))
        self.assertGreaterEqual(len(errors), 2)

    def test_manifest_schema_rejects_authoritative_archive_record(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/archive-manifest-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = {
            "schema_version": 1,
            "manifest_role": "project-archive-retention-index",
            "records": [
                {
                    "archive_id": "old-plan",
                    "classification": "ARCHIVE_HISTORY",
                    "original_path": "docs/old-plan.md",
                    "current_path": "docs/archive/old-plan.md",
                    "content_sha256": "a" * 64,
                    "archived_at": "2026-07-25",
                    "superseded_by": ["docs/current-plan.md"],
                    "reason": "superseded",
                    "active_authority": True,
                    "implementation_authority": "CURRENT",
                    "compatibility_consumers": [],
                    "rollback_ref": "a" * 40,
                    "validation_status": "PASS",
                }
            ],
        }
        errors = list(Draft202012Validator(schema).iter_errors(manifest))
        self.assertGreaterEqual(len(errors), 2)

    def test_skill_is_compact_and_contains_required_contract(self) -> None:
        skill = (
            ROOT / "skills/governing-legacy-retention-and-archives/SKILL.md"
        ).read_text(encoding="utf-8")
        required = (
            "name: governing-legacy-retention-and-archives",
            "CURRENT_AUTHORITY",
            "COMPATIBILITY_ONLY",
            "ARCHIVE_HISTORY",
            "EVIDENCE_RETENTION",
            "GENERATED_DERIVATIVE",
            "DELETE_PROHIBITED_SECRET",
            "DELETE_APPROVED",
            "KEEP_UNRESOLVED",
            "원문을 비우지 않는다",
            "active_authority: false",
            "implementation_authority: NONE",
            "Output contract",
            "Quality gate",
            "Learning Log",
        )
        for token in required:
            self.assertIn(token, skill)
        self.assertLessEqual(len(skill.splitlines()), 150)

    def test_template_validator_passes_reference_files(self) -> None:
        validator = load_validator()
        errors = validator.validate_archive_governance(
            ROOT,
            ROOT / "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json",
            ROOT / "templates/project-operations/ARCHIVE_MANIFEST.json",
        )
        self.assertEqual([], errors)

    def test_validator_rejects_empty_archived_markdown(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "docs/archive").mkdir(parents=True)
            for name in (
                "archive-retention-adapter-v1.schema.json",
                "archive-manifest-v1.schema.json",
            ):
                (root / "schemas" / name).write_text(
                    (ROOT / "schemas" / name).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            (root / "docs/current.md").write_text("current", encoding="utf-8")
            (root / "docs/archive/README.md").write_text("archive", encoding="utf-8")
            (root / "docs/archive/empty.md").write_text(
                "---\narchive_metadata: true\n---\n", encoding="utf-8"
            )
            adapter = json.loads(
                (ROOT / "templates/project-operations/ARCHIVE_RETENTION_ADAPTER.json").read_text(
                    encoding="utf-8"
                )
            )
            adapter["paths"] = {
                "active_canon_roots": ["docs/current.md"],
                "archive_root": "docs/archive",
                "archive_readme": "docs/archive/README.md",
                "archive_manifest": "docs/archive/MANIFEST.json",
                "inactive_skill_roots": [],
                "generated_derivative_roots": [],
                "protected_evidence_roots": [],
            }
            manifest = {
                "schema_version": 1,
                "manifest_role": "project-archive-retention-index",
                "records": [
                    {
                        "archive_id": "empty",
                        "classification": "ARCHIVE_HISTORY",
                        "original_path": "docs/empty.md",
                        "current_path": "docs/archive/empty.md",
                        "content_sha256": "a" * 64,
                        "archived_at": "2026-07-25",
                        "superseded_by": ["docs/current.md"],
                        "reason": "test",
                        "active_authority": False,
                        "implementation_authority": "NONE",
                        "compatibility_consumers": [],
                        "rollback_ref": "a" * 40,
                        "validation_status": "NOT_RUN",
                    }
                ],
            }
            adapter_path = root / "adapter.json"
            manifest_path = root / "docs/archive/MANIFEST.json"
            adapter_path.write_text(json.dumps(adapter), encoding="utf-8")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            errors = validator.validate_archive_governance(
                root, adapter_path, manifest_path
            )
            self.assertIn(
                "archived Markdown body is empty: docs/archive/empty.md", errors
            )


if __name__ == "__main__":
    unittest.main()
