from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
EVALUATION_SKILL = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md"
)
LEARNING_LOG = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md"
)
HIGODOT_POLICY = (
    ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
)
SHARED_ROUTES = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"
COMMON_POLICY_FILES = (AGENTS, EVALUATION_SKILL, HIGODOT_POLICY)
PROJECT_NAMES = (
    "Switchy Express",
    "Blacksmith",
    "urban-legend",
    "OMENWARD",
    "GRIMOIRE",
    "Ten Paces",
)


class GodotAddonUtilizationPolicyTests(unittest.TestCase):
    def test_global_gate_prefers_approved_addon_use_without_blanket_installation(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        for marker in (
            "검증·승인된 애드온",
            "직접 중복 구현보다 활용을 우선",
            "모든 프로젝트에 일괄 설치하지 않는다",
            "INSTALLED_UNUSED",
        ):
            self.assertIn(marker, text)

    def test_evaluation_skill_requires_consumption_and_lifecycle_states(self) -> None:
        text = EVALUATION_SKILL.read_text(encoding="utf-8")
        for marker in (
            "Selective addon utilization",
            "consumption_path",
            "INSTALLED_UNUSED",
            "CANDIDATE",
            "TRIAL_APPROVED",
            "ADOPTED_ACTIVE",
            "DEFERRED",
            "REMOVAL_PENDING",
            "테스트 프레임워크",
            "대화·서사 프레임워크",
            "플랫폼 서비스 애드온",
            "개발 편의·카메라·아이콘 애드온",
        ):
            self.assertIn(marker, text)

    def test_higodot_authority_scope_allows_non_authoring_addons(self) -> None:
        text = HIGODOT_POLICY.read_text(encoding="utf-8")
        for marker in (
            "저작·편집 자동화",
            "비저작 애드온",
            "테스트",
            "대화",
            "플랫폼 서비스",
            "동일 저작 권위",
        ):
            self.assertIn(marker, text)
        self.assertIn("authority_count: 1", text)

    def test_shared_route_exposes_selective_adoption_state(self) -> None:
        payload = json.loads(SHARED_ROUTES.read_text(encoding="utf-8"))
        item = next(
            entry
            for entry in payload["shared_skills"]
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

    def test_common_policy_does_not_freeze_project_specific_addon_tables(self) -> None:
        for path in COMMON_POLICY_FILES:
            text = path.read_text(encoding="utf-8")
            for project_name in PROJECT_NAMES:
                self.assertNotIn(project_name, text, f"{project_name} leaked into {path}")

    def test_learning_log_records_the_selective_use_decision(self) -> None:
        text = LEARNING_LOG.read_text(encoding="utf-8")
        for marker in (
            "Selective addon utilization",
            "INSTALLED_UNUSED",
            "blanket installation",
            "consumption path",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
