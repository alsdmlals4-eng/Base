from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM_GATE = (
    ROOT
    / "skills"
    / "reviewing-and-validating-project-changes"
    / "references"
    / "claim-and-intent-verification.md"
)
NOTION_LAYOUT = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md"
)


class McpRealityGateContractTests(unittest.TestCase):
    def test_shared_gate_separates_discovery_execution_effect_and_device_visibility(self) -> None:
        text = CLAIM_GATE.read_text(encoding="utf-8")

        for contract in (
            "DISCOVERED_AVAILABLE != EXECUTABLE_AVAILABLE",
            "EXECUTABLE_AVAILABLE != EFFECT_VERIFIED",
            "SERVER_READBACK_PASS != HUMAN_VISIBLE_DEVICE_PASS",
            "CALLABLE_SCHEMA_PRESENT",
            "INVOCATION_PASS",
            "READBACK_PASS",
            "HUMAN_VISIBLE_PASS",
            "BLOCKED_TOOL_SURFACE",
        ):
            self.assertIn(contract, text)

        self.assertIn("callable function + usable schema exposure", text)
        self.assertIn("minimum real invocation", text)
        self.assertIn("consumer / human / device-visible observation", text)

    def test_notion_layout_consumes_shared_mcp_claim_ceiling(self) -> None:
        text = NOTION_LAYOUT.read_text(encoding="utf-8")

        for contract in (
            "MCP_DISCOVERED_AVAILABLE != CURRENT_CLIENT_EXECUTABLE",
            "CURRENT_CLIENT_EXECUTABLE != EFFECT_VERIFIED",
            "SERVER_READBACK_PASS != HUMAN_VISIBLE_DEVICE_PASS",
            "DISCOVERED_ONLY / BLOCKED_TOOL_SURFACE",
            "INVOCATION_PASS",
            "READBACK_PASS",
            "HUMAN_VISIBLE_PASS",
        ):
            self.assertIn(contract, text)

        self.assertIn("self.current_tool_access=available", text)
        self.assertIn("Android/iOS/browser", text)
        self.assertIn("successful write invocation as durable effect", text)


if __name__ == "__main__":
    unittest.main()
