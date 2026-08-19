from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"
FRONT_NAME = re.compile(r"^name:\s*([^\n]+)$", re.MULTILINE)


class BaseSharedSkillRouteTests(unittest.TestCase):
    def test_shared_skill_routes_are_registered_and_adapter_only(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

        self.assertEqual(registry["registry_role"], "base-shared-skill-extension-router")
        self.assertFalse(registry["routing_policy"]["load_all_skills"])
        self.assertTrue(registry["routing_policy"]["project_adapter_required"])
        self.assertFalse(registry["routing_policy"]["copy_shared_skill_bodies_to_projects"])

        by_id = {item["skill_id"]: item for item in registry["shared_skills"]}
        required = {
            "governing-legacy-retention-and-archives",
            "evaluating-godot-assets-and-plugins-before-creation",
        }
        self.assertEqual(set(by_id), required)

        for skill_id, item in by_id.items():
            self.assertEqual(item["status"], "ACTIVE")
            self.assertFalse(item["load_by_default"])
            self.assertTrue(item["trigger_tags"])
            self.assertTrue(item["use_when"])
            self.assertTrue(item["do_not_use_when"])
            self.assertTrue(item["project_adapter_roles"])

            skill_path = ROOT / item["path"]
            self.assertTrue(skill_path.is_file(), item["path"])
            text = skill_path.read_text(encoding="utf-8")
            match = FRONT_NAME.search(text)
            self.assertIsNotNone(match, skill_id)
            self.assertEqual(match.group(1).strip(), skill_id)

    def test_godot_asset_route_exposes_rights_and_reference_production(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        item = next(
            entry
            for entry in registry["shared_skills"]
            if entry["skill_id"]
            == "evaluating-godot-assets-and-plugins-before-creation"
        )

        for tag in (
            "asset-provenance",
            "distribution-in-game-build",
            "reference-to-original",
            "asset-rights-evidence",
        ):
            self.assertIn(tag, item["trigger_tags"])

        self.assertIn(
            "docs/knowledge/game-development/"
            "PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
            item["references"],
        )
        self.assertIn(
            "templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md",
            item["templates"],
        )
        self.assertIn(
            "templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md",
            item["templates"],
        )
        self.assertEqual(
            item["learning_log"],
            "skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md",
        )

    def test_godot_provider_route_exposes_reuse_first_and_higodot_contracts(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        item = next(
            entry
            for entry in registry["shared_skills"]
            if entry["skill_id"]
            == "evaluating-godot-assets-and-plugins-before-creation"
        )

        for tag in (
            "existing-solution-first",
            "current-environment-inventory",
            "connected-mcp",
            "higodot",
            "godot-ai",
            "reuse-absorb-refactor-archive-build-new",
        ):
            self.assertIn(tag, item["trigger_tags"])

        for mode in ("inventory-current-environment", "disposition"):
            self.assertIn(mode, item["skill_modes"])

        for role in (
            "mcp_host_inventory",
            "enabled_godot_addons",
            "dependency_manifests",
            "related_open_and_recent_prs",
            "existing_solution_disposition",
            "higodot_adoption_record",
        ):
            self.assertIn(role, item["project_adapter_roles"])

        self.assertIn(
            "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
            item["references"],
        )
        self.assertIn(
            "templates/project-operations/HIGODOT_ADOPTION_RECORD.json",
            item["templates"],
        )

    def test_godot_addon_route_exposes_selective_adoption_contract(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        item = next(
            entry
            for entry in registry["shared_skills"]
            if entry["skill_id"]
            == "evaluating-godot-assets-and-plugins-before-creation"
        )

        for tag in (
            "selective-addon-utilization",
            "installed-unused",
            "addon-consumption-path",
        ):
            self.assertIn(tag, item["trigger_tags"])

        for role in (
            "addon_adoption_state",
            "addon_consumption_path",
            "addon_removal_or_rollback",
        ):
            self.assertIn(role, item["project_adapter_roles"])

        use_when = " ".join(item["use_when"])
        self.assertIn("채택 상태", use_when)
        self.assertIn("소비 경로", use_when)
        self.assertIn("제거 절차", use_when)

    def test_godot_toolchain_route_exposes_gut_and_hera_roles(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        item = next(
            entry
            for entry in registry["shared_skills"]
            if entry["skill_id"]
            == "evaluating-godot-assets-and-plugins-before-creation"
        )

        for tag in (
            "gut",
            "gdscript-test-framework",
            "hera-agent",
            "live-runtime-qa",
            "source-delta-guard",
        ):
            self.assertIn(tag, item["trigger_tags"])

        for role in (
            "godot_test_framework",
            "gut_exact_version",
            "gut_test_consumption_path",
            "hera_cli_addon_pair",
            "hera_live_qa_consumption_path",
            "hera_source_delta_guard",
        ):
            self.assertIn(role, item["project_adapter_roles"])

        self.assertEqual(len(registry["shared_skills"]), 2)

    def test_project_specific_skills_remain_local_only(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        policy = registry["project_skill_policy"]
        self.assertEqual(policy["base_shared_skills"], "route-through-project-adapter")
        self.assertEqual(policy["project_specific_skills"], "create-and-maintain-in-project")
        self.assertEqual(policy["duplicate_base_skill_bodies"], "forbidden")

    def test_retired_qa_studio_is_replaced_by_repository_native_evidence(self) -> None:
        start_here = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        retirement = (
            ROOT / "docs" / "DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md"
        ).read_text(encoding="utf-8")
        modules = (
            ROOT
            / "docs"
            / "knowledge"
            / "game-development"
            / "reuse"
            / "PRODUCTION_TOOL_WORKFLOW_MODULES.md"
        ).read_text(encoding="utf-8")

        self.assertIn("QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW", start_here)
        self.assertIn("REPOSITORY_NATIVE_EVIDENCE_CAPTURE", retirement)
        self.assertIn("RM-TOOL-004 · REPOSITORY_NATIVE_EVIDENCE_CAPTURE", modules)
        self.assertNotIn(
            "이미지·UX 배치 후 개발자 PC 증거 검토: `tools/qa-evidence-studio/README.md`",
            start_here,
        )


if __name__ == "__main__":
    unittest.main()
