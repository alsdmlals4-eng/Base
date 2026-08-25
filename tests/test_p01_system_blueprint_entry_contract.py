from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class P01SystemBlueprintEntryContractTests(unittest.TestCase):
    def test_p01_context_routes_complex_project_work_through_blueprint_gate(self):
        context = (
            ROOT
            / "docs"
            / "operations"
            / "base-partitions"
            / "P01_PROJECT_PLANNING_OPERATIONS_NOTION.md"
        ).read_text(encoding="utf-8")
        contract_path = "docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md"

        self.assertIn("SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED", context)
        self.assertIn(contract_path, context)
        self.assertIn("REUSE_EXISTING_BLUEPRINT_BEFORE_CREATING_NEW", context)
        self.assertIn("NO_MASS_BLUEPRINT_BACKFILL", context)
        self.assertIn("NOT_APPLICABLE_WITH_REASON", context)

    def test_blueprint_contract_preserves_incremental_rollout_guards(self):
        contract = (
            ROOT
            / "docs"
            / "operations"
            / "project-workspace"
            / "NOTION_SYSTEM_BLUEPRINT_CONTRACT.md"
        ).read_text(encoding="utf-8")

        self.assertIn("SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED", contract)
        self.assertIn("REUSE_EXISTING_BLUEPRINT_BEFORE_CREATING_NEW", contract)
        self.assertIn("NO_MASS_BLUEPRINT_BACKFILL", contract)
        self.assertIn("NOT_APPLICABLE_WITH_REASON", contract)
        self.assertIn("SYSTEM_BLUEPRINT_REQUIRED_WHEN_COMPLEX", contract)


if __name__ == "__main__":
    unittest.main()
