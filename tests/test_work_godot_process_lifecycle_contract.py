from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "docs" / "GPT_CODEX_WORKFLOW_POLICY.md"
ROUTING = ROOT / "docs" / "WORK_MODE_AND_SKILL_ROUTING.md"
GODOT_SAFETY = (
    ROOT
    / "docs"
    / "knowledge"
    / "godot"
    / "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class WorkGodotProcessLifecycleContractTests(unittest.TestCase):
    maxDiff = None

    def test_workflow_requires_material_direct_verification_and_task_owned_cleanup(self) -> None:
        workflow = read(WORKFLOW)
        for term in (
            "WORK_DIRECT_GODOT_VERIFICATION_WHEN_MATERIAL",
            "TASK_LAUNCHED_GODOT_PROCESS_OWNERSHIP",
            "STOP_TASK_OWNED_GODOT_WHEN_NO_LONGER_NEEDED",
            "PRESERVE_PREEXISTING_AND_UNRELATED_GODOT_INSTANCES",
            "PROCESS_OWNERSHIP_UNVERIFIED",
            "GODOT_VERIFICATION_AND_SHUTDOWN_REPORT",
        ):
            self.assertIn(term, workflow)

    def test_routing_reports_runtime_verification_and_cleanup_separately(self) -> None:
        routing = read(ROUTING)
        for term in (
            "godot_verification:",
            "godot_process_cleanup:",
            "task_owned_processes_started:",
            "task_owned_processes_stopped:",
            "preexisting_or_unrelated_preserved:",
            "residual_check:",
            "residual_risk:",
        ):
            self.assertIn(term, routing)

    def test_godot_safety_preserves_unrelated_instances_and_avoids_broad_kill(self) -> None:
        godot_safety = read(GODOT_SAFETY)
        for term in (
            "TASK_LAUNCHED_GODOT_PROCESS_OWNERSHIP",
            "graceful stop",
            "PROCESS_OWNERSHIP_UNVERIFIED",
            "process-name 전체 종료 금지",
            "pre-existing",
            "다른 프로젝트",
            "residual check",
        ):
            self.assertIn(term, godot_safety)

    def test_direct_verification_does_not_expand_gpt_product_authoring(self) -> None:
        workflow = read(WORKFLOW)
        routing = read(ROUTING)
        self.assertIn("GPT가 Godot 제품 코드를 직접 누적 구현", workflow)
        self.assertIn(
            "GPT는 실제 게임 프로젝트의 Godot 제품 코드를 기본 구현하지 않는다.",
            routing,
        )
        self.assertIn("검수·기계검증", workflow)
        self.assertIn("persistent product authoring", workflow)


if __name__ == "__main__":
    unittest.main()
