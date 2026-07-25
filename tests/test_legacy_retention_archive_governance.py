from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LegacyRetentionArchiveGovernanceTests(unittest.TestCase):
    def test_shared_skill_and_archive_contract_files_exist(self) -> None:
        required = [
            "skills/governing-legacy-retention-and-archives/SKILL.md",
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


if __name__ == "__main__":
    unittest.main()
