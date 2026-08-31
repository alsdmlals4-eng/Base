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

    def test_first_prompt_routes_l1_game_system_work_through_same_contract(self):
        first_prompt = (
            ROOT
            / "skills"
            / "managing-project-intake-and-work-contract"
            / "references"
            / "first-prompt-direction-anchoring.md"
        ).read_text(encoding="utf-8")
        contract_path = "docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md"

        self.assertIn("SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED", first_prompt)
        self.assertIn("REUSE_EXISTING_BLUEPRINT_BEFORE_CREATING_NEW", first_prompt)
        self.assertIn("NO_MASS_BLUEPRINT_BACKFILL", first_prompt)
        self.assertIn(contract_path, first_prompt)
        self.assertIn("NOT_APPLICABLE_WITH_REASON", first_prompt)
        self.assertIn("system_blueprint_entry_resolved_if_applicable", first_prompt)
        self.assertIn("세부 Blueprint 규칙을 이 reference에 복제하지 않는다", first_prompt)

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

    def test_blueprint_contract_reuses_a_compact_player_to_validation_decision_chain(self):
        contract = (
            ROOT
            / "docs"
            / "operations"
            / "project-workspace"
            / "NOTION_SYSTEM_BLUEPRINT_CONTRACT.md"
        ).read_text(encoding="utf-8")

        for token in (
            "BLUEPRINT_COMPACT_DECISION_CHAIN_REQUIRED",
            "BLUEPRINT_BENCHMARK_CONTEXT_BOUND",
            "NO_DUPLICATED_CANON_OR_DECORATIVE_NODES",
            "Player Meaning / Intent",
            "Validation",
        ):
            self.assertIn(token, contract)


if __name__ == "__main__":
    unittest.main()
