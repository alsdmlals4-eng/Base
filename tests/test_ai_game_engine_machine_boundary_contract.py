from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_GUIDE = ROOT / "docs" / "BENCHMARKING_REFERENCE_GUIDE.md"
CAPABILITY_MAP = ROOT / "docs" / "CAPABILITY_COMPOSITION_MAP.md"
P06 = ROOT / "docs" / "operations" / "base-partitions" / "P06_GODOT_RUNTIME_TOOLCHAIN.md"
CASE = ROOT / "docs" / "knowledge" / "cases" / "COCOS_AI_NATIVE_ENGINE_INTERFACE_CASE.md"


class AiGameEngineMachineBoundaryContractTest(unittest.TestCase):
    def test_machine_boundary_contract_is_owned_by_existing_docs(self) -> None:
        benchmark = BENCHMARK_GUIDE.read_text(encoding="utf-8")
        capability = CAPABILITY_MAP.read_text(encoding="utf-8")
        combined = benchmark + "\n" + capability

        required_tokens = (
            "AI_GAME_ENGINE_MACHINE_BOUNDARY",
            "PROJECT_IDENTITY_BEFORE_OPERATION",
            "SHARED_CORE_FOR_CLI_AND_MCP",
            "SCHEMA_GENERATED_TOOL_SURFACE",
            "MCP_E2E_BEHAVIOR_CONTRACT",
            "NONINTERACTIVE_AUTOMATION_PATH",
            "STRUCTURED_EXECUTION_EVIDENCE",
        )
        for token in required_tokens:
            with self.subTest(token=token):
                self.assertIn(token, combined)

    def test_cocos_is_benchmark_only_and_godot_remains_engine(self) -> None:
        self.assertTrue(CASE.exists(), "Cocos benchmark case must be recorded before promotion")
        case = CASE.read_text(encoding="utf-8")
        p06 = P06.read_text(encoding="utf-8")

        self.assertIn("ENGINE_DECISION_GODOT_REMAINS", case)
        self.assertIn("COCOS_TECHNIQUES_ONLY", case)
        self.assertIn("NO_ENGINE_MIGRATION", case)
        self.assertIn("HiGodot single authority", p06)
        self.assertNotIn("COCOS_RUNTIME_AUTHORITY", p06)
        self.assertNotIn("COCOS_AUTHORING_AUTHORITY", p06)

    def test_mcp_transport_cannot_substitute_for_behavior_evidence(self) -> None:
        capability = CAPABILITY_MAP.read_text(encoding="utf-8")
        self.assertIn("MCP_CONNECTED_IS_NOT_BEHAVIOR_PASS", capability)
        self.assertIn("typed operation", capability)
        self.assertIn("behavior E2E", capability)
        self.assertIn("Implementation Reality Gate", capability)


if __name__ == "__main__":
    unittest.main()
