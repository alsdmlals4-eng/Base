from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class VisualCollaborationCapabilityContractTests(unittest.TestCase):
    def test_policy_keeps_tools_reusable_and_noncanonical(self):
        text = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        for token in ("GDD", "EXTERNAL_COLLABORATION", "BOTH", "VISUAL_CANONICAL_CONFLICT", "IMPLEMENTATION_PINNED", "NOT_RUN"):
            self.assertIn(token, text)
        self.assertIn("do not create a `figma-*`", text.lower())

    def test_registry_template_records_context_and_handoff_evidence(self):
        data = json.loads((ROOT / "templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json").read_text(encoding="utf-8"))
        item = data["artifacts"][0]
        for field in ("usage_context", "responsible_document_id", "related_decision_ids", "snapshot_path", "source_commit", "implementation_scope", "excluded_scope"):
            self.assertIn(field, item)

    def test_documentation_map_routes_existing_responsibilities_to_the_shared_policy(self):
        text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        self.assertIn("VISUAL_COLLABORATION_TOOL_POLICY.md", text)
        self.assertIn("CAPABILITY_COMPOSITION_MAP.md", text)

if __name__ == "__main__":
    unittest.main()
