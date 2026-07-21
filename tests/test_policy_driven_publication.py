from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.build_policy_driven_design_documents import load_registry, select_documents


ROOT = Path(__file__).resolve().parents[1]


class PolicyDrivenPublicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = {
            "schema_version": 3,
            "documents": [
                {"document_id": "source", "status": "ACTIVE", "publication_policy": "source_only"},
                {"document_id": "milestone", "status": "ACTIVE", "publication_policy": "milestone_sync"},
                {"document_id": "always", "status": "ACTIVE", "publication_policy": "always_sync"},
                {"document_id": "held", "status": "HOLD", "publication_policy": "always_sync"},
            ],
        }

    def test_default_selects_only_always_sync(self) -> None:
        chosen = select_documents(self.registry, set(), include_milestone=False)
        self.assertEqual([item["document_id"] for item in chosen], ["always"])

    def test_milestone_flag_adds_milestone_sync(self) -> None:
        chosen = select_documents(self.registry, set(), include_milestone=True)
        self.assertEqual([item["document_id"] for item in chosen], ["milestone", "always"])

    def test_only_can_build_milestone_document(self) -> None:
        chosen = select_documents(self.registry, {"milestone"}, include_milestone=False)
        self.assertEqual([item["document_id"] for item in chosen], ["milestone"])

    def test_source_only_cannot_be_requested_for_publication(self) -> None:
        with self.assertRaisesRegex(ValueError, "source_only"):
            select_documents(self.registry, {"source"}, include_milestone=False)

    def test_unknown_document_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "not found"):
            select_documents(self.registry, {"missing"}, include_milestone=False)

    def test_registry_loader_requires_schema_v3(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "registry.json"
            path.write_text(json.dumps({"schema_version": 2}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Schema v3"):
                load_registry(path)

    def test_schema_accepts_all_publication_policies(self) -> None:
        schema = json.loads((ROOT / "schemas/design-document-registry-v3.schema.json").read_text(encoding="utf-8"))
        base = {
            "schema_version": 3,
            "registry_role": "ai-design-document-router-and-publication-index",
            "project_name": "Fixture",
            "documents": [],
        }
        source_only = {
            "document_id": "source-only",
            "title": "Source Only",
            "discipline": "project-operations",
            "responsibility_coverage": ["project-operations"],
            "status": "ACTIVE",
            "source_path": "source.md",
            "source_format": "markdown",
            "source_role": "state",
            "publication_policy": "source_only",
            "output_pdf": None,
            "output_docx": None,
            "diagram_policy": "none",
            "publication_manifest": None,
            "generator": None,
        }
        milestone = dict(source_only)
        milestone.update({
            "document_id": "milestone",
            "title": "Milestone",
            "publication_policy": "milestone_sync",
            "output_pdf": "milestone.pdf",
            "publication_manifest": "milestone_PUBLICATION_MANIFEST.json",
            "generator": "tools/build_design_documents.py",
        })
        always = dict(milestone)
        always.update({"document_id": "always", "title": "Always", "publication_policy": "always_sync"})
        for document in (source_only, milestone, always):
            fixture = dict(base)
            fixture["documents"] = [document]
            errors = list(Draft202012Validator(schema).iter_errors(fixture))
            self.assertEqual(errors, [], [error.message for error in errors])


if __name__ == "__main__":
    unittest.main()
