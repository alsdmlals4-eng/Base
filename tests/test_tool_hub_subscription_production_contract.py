from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ToolHubSubscriptionProductionContractTests(unittest.TestCase):
    def test_tool_hub_launch_adapter_pins_subscription_import_for_visual_studios(self) -> None:
        adapter = read("tools/tool-hub/src/tool_hub/adapters.py")
        self.assertIn('"--run-mode",\n                "subscription_handoff_import"', adapter)
        self.assertNotIn("OPENAI_API_KEY", adapter)

        studios = {
            "expression": read("tools/expression-studio/src/expression_studio/app.py"),
            "sprite": read("tools/sprite-animation-studio/src/sprite_animation_studio/app.py"),
        }
        for name, source in studios.items():
            with self.subTest(source=name):
                self.assertIn('default="subscription_handoff_import"', source)

    def test_subscription_handoff_contract_is_truthful_and_network_free(self) -> None:
        source = read("tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py")
        for token in (
            'schema_version: int = field(default=1, init=False)',
            'state: str = field(default="GPT_PRO_HANDOFF_READY", init=False)',
            'generation_surface: str = field(default="CHATGPT_PRO_SUBSCRIPTION", init=False)',
            'output_media_type: str = field(default="image/png", init=False)',
            'provider_call_made: bool = field(default=False, init=False)',
            'requires_additional_payment: bool = field(default=False, init=False)',
            "This function deliberately performs no provider call",
        ):
            self.assertIn(token, source)
        for forbidden_import in (
            "import requests",
            "import httpx",
            "import webbrowser",
            "import selenium",
            "import playwright",
            "from openai",
            "import openai",
        ):
            self.assertNotIn(forbidden_import, source)

    def test_each_registered_project_has_one_reviewed_character_expression_route(self) -> None:
        project_registry = json.loads(
            read("docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json")
        )
        tool_registry = json.loads(
            read("docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json")
        )
        projects = {
            entry["project_id"]: entry
            for entry in project_registry["entries"]
            if entry["delivery_status"] == "READY_FOR_DELIVERY"
        }
        routes = tool_registry["entries"]

        self.assertEqual(8, len(projects))
        self.assertEqual(8, len(routes))
        self.assertEqual(set(projects), {entry["project_id"] for entry in routes})
        self.assertEqual(
            {"character_expression_runs"},
            {entry["tool_route_id"] for entry in routes},
        )

        for route in routes:
            project = projects[route["project_id"]]
            with self.subTest(project_id=route["project_id"]):
                self.assertEqual(project["figma_file_key"], route["figma_file_key"])
                self.assertEqual(project["generation_area_node_id"], route["parent_node_id"])
                self.assertEqual("FRAME", route["parent_node_type"])
                self.assertEqual("FRAME", route["destination_node_type"])
                self.assertEqual("FRAME", route["project_marker_node_type"])
                self.assertEqual("Expression Runs", route["destination_name"])
                self.assertNotEqual(route["parent_node_id"], route["destination_node_id"])
                self.assertNotIn(
                    route["project_marker_node_id"],
                    {route["parent_node_id"], route["destination_node_id"]},
                )
                self.assertEqual(
                    f"Base Tool Hub Route · {route['project_id']}",
                    route["project_marker_name"],
                )

    def test_unreviewed_sprite_and_effect_destination_nodes_are_not_invented(self) -> None:
        tool_registry = json.loads(
            read("docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json")
        )
        route_ids = {entry["tool_route_id"] for entry in tool_registry["entries"]}
        self.assertNotIn("sprite_action_runs", route_ids)
        self.assertNotIn("effect_runs", route_ids)


if __name__ == "__main__":
    unittest.main()
