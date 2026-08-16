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
            'import_run_mode: str = field(default="subscription_handoff_import", init=False)',
            'import_declared_source: str = field(default="CHATGPT_INCLUDED", init=False)',
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

    def test_handoff_import_truth_matches_both_studio_consumers(self) -> None:
        handoff = read("tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py")
        expression_imports = read("tools/expression-studio/src/expression_studio/imports.py")
        sprite_imports = read("tools/sprite-animation-studio/src/sprite_animation_studio/imports.py")
        expression_app = read("tools/expression-studio/src/expression_studio/app.py")
        sprite_app = read("tools/sprite-animation-studio/src/sprite_animation_studio/app.py")

        self.assertIn('import_declared_source: str = field(default="CHATGPT_INCLUDED", init=False)', handoff)
        self.assertIn('import_run_mode: str = field(default="subscription_handoff_import", init=False)', handoff)
        for source in (expression_imports, sprite_imports):
            self.assertIn('"CHATGPT_INCLUDED"', source)
            self.assertIn("DECLARED_SOURCES", source)
        for source in (expression_app, sprite_app):
            self.assertIn('default="subscription_handoff_import"', source)

    def test_each_registered_project_has_three_exact_reviewed_visual_routes(self) -> None:
        project_registry = json.loads(read("docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json"))
        tool_registry = json.loads(read("docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json"))
        projects = {
            entry["project_id"]: entry
            for entry in project_registry["entries"]
            if entry["delivery_status"] == "READY_FOR_DELIVERY"
        }
        routes = tool_registry["entries"]
        expected_route_names = {
            "character_expression_runs": "Expression Runs",
            "sprite_action_runs": "Sprite Action Runs",
            "effect_runs": "Effect Runs",
        }

        self.assertEqual(8, len(projects))
        self.assertEqual(24, len(routes))
        self.assertEqual(
            {(project_id, route_id) for project_id in projects for route_id in expected_route_names},
            {(entry["project_id"], entry["tool_route_id"]) for entry in routes},
        )

        by_project: dict[str, list[dict[str, object]]] = {project_id: [] for project_id in projects}
        for route in routes:
            project = projects[route["project_id"]]
            by_project[route["project_id"]].append(route)
            with self.subTest(project_id=route["project_id"], route=route["tool_route_id"]):
                self.assertEqual(project["figma_file_key"], route["figma_file_key"])
                self.assertEqual(project["generation_area_node_id"], route["parent_node_id"])
                self.assertEqual("FRAME", route["parent_node_type"])
                self.assertEqual("FRAME", route["destination_node_type"])
                self.assertEqual("FRAME", route["project_marker_node_type"])
                self.assertEqual(expected_route_names[route["tool_route_id"]], route["destination_name"])
                self.assertNotEqual(route["parent_node_id"], route["destination_node_id"])
                self.assertNotIn(
                    route["project_marker_node_id"],
                    {route["parent_node_id"], route["destination_node_id"]},
                )
                self.assertEqual(
                    f"Base Tool Hub Route · {route['project_id']}",
                    route["project_marker_name"],
                )

        for project_id, project_routes in by_project.items():
            ids = [str(route["destination_node_id"]) for route in project_routes]
            self.assertEqual(3, len(ids), project_id)
            self.assertEqual(3, len(set(ids)), project_id)
            parent_id = str(project_routes[0]["parent_node_id"])
            marker_id = str(project_routes[0]["project_marker_node_id"])
            self.assertNotIn(parent_id, ids)
            self.assertNotIn(marker_id, ids)

    def test_operator_docs_match_post_428_windows_and_figma_authority(self) -> None:
        hub = read("tools/tool-hub/README.md")
        expression = read("tools/expression-studio/README.md")
        sprite = read("tools/sprite-animation-studio/README.md")

        self.assertIn("Windows Job Object", hub)
        self.assertIn("사용자 개발자 PC", hub)
        self.assertNotIn("Studio child `BLOCKED_PLATFORM`", hub)

        self.assertIn("확정 및 전달", expression)
        self.assertIn("Figma Bridge", expression)
        self.assertNotIn("matching project GPT workspace", expression)
        self.assertNotIn("실제 Windows 런타임은 `BLOCKED_UNVERIFIED`", expression)

        self.assertIn("DELIVERY_TOOL_ROUTE_UNAVAILABLE", sprite)
        self.assertIn("dedicated", sprite)
        self.assertNotIn("`ready_for_project_gpt` 전달 패킷", sprite)
        self.assertNotIn("실제 Windows 런타임은 `BLOCKED_UNVERIFIED`", sprite)


if __name__ == "__main__":
    unittest.main()
