from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_GUIDE = ROOT / "docs" / "BENCHMARKING_REFERENCE_GUIDE.md"
CAPABILITY_MAP = ROOT / "docs" / "CAPABILITY_COMPOSITION_MAP.md"
VISUAL_POLICY = ROOT / "docs" / "VISUAL_COLLABORATION_TOOL_POLICY.md"


class ToolInterfaceSurfaceSelectionContractTest(unittest.TestCase):
    def test_surface_selection_contract_is_owned_by_existing_docs(self) -> None:
        benchmark = BENCHMARK_GUIDE.read_text(encoding="utf-8")
        capability = CAPABILITY_MAP.read_text(encoding="utf-8")
        combined = benchmark + "\n" + capability

        required_tokens = (
            "TOOL_INTERFACE_SURFACE_SELECTION",
            "CORE_LOGIC_SINGLE_OWNER",
            "CLI_OR_PROGRAMMATIC_CONTRACT_FIRST_WHEN_PRACTICAL",
            "SURFACE_DOES_NOT_OWN_CANON",
            "HUMAN_SURFACE_REQUIRES_REPAYMENT",
            "KEYBOARD_FIRST_IS_CROSS_SURFACE",
            "NO_DEPRECATED_SURFACE_REVIVAL",
            "TARGET_PLATFORM_VERIFIED",
        )
        for token in required_tokens:
            with self.subTest(token=token):
                self.assertIn(token, combined)

    def test_deprecated_management_surfaces_remain_retired(self) -> None:
        visual_policy = VISUAL_POLICY.read_text(encoding="utf-8")
        self.assertIn("Tool Hub", visual_policy)
        self.assertIn("QA Evidence Studio", visual_policy)
        self.assertIn("external HTML", visual_policy)
        self.assertIn("not active authorities or required project surfaces", visual_policy)

    def test_surface_gate_does_not_become_gui_first_or_tui_ban(self) -> None:
        capability = CAPABILITY_MAP.read_text(encoding="utf-8")
        self.assertIn("CLI", capability)
        self.assertIn("TUI", capability)
        self.assertIn("thin GUI", capability)
        self.assertNotIn("GUI_ALWAYS_FIRST", capability)
        self.assertNotIn("TUI_PROHIBITED", capability)


if __name__ == "__main__":
    unittest.main()
