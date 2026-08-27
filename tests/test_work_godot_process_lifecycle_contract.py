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
EVIDENCE_OWNER = (
    ROOT
    / "docs"
    / "knowledge"
    / "vertical-slice"
    / "SKILL_ORCHESTRATION_AND_EVIDENCE.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_ordered(test: unittest.TestCase, text: str, terms: tuple[str, ...]) -> None:
    positions = []
    for term in terms:
        test.assertIn(term, text)
        positions.append(text.index(term))
    test.assertEqual(positions, sorted(positions), f"terms must be ordered: {terms}")


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

    def test_existing_evidence_owner_controls_full_completion_sequence(self) -> None:
        evidence = read(EVIDENCE_OWNER)
        self.assertIn("EXECUTION_EVIDENCE_CANONICAL_OWNER", evidence)
        assert_ordered(
            self,
            evidence,
            (
                "EXECUTABLE_COVERAGE_OR_EXPLICIT_ENV_GATE",
                "WORK_DIRECT_GODOT_VERIFICATION_WHEN_MATERIAL",
                "FRESH_RUNTIME_ARTIFACT_GATE",
                "TASK_OWNED_PROCESS_CLEANUP",
                "RESIDUAL_PROCESS_READBACK",
                "COMPLETION_CLAIM_AFTER_VERIFICATION_AND_CLEANUP",
            ),
        )
        for term in (
            "ENV_GATED_EXPECTED_SKIP",
            "UNRUNNABLE_COVERAGE_GAP",
            "CLEANUP_PASS_IS_NOT_RUNTIME_PASS",
            "PROCESS_OWNERSHIP_UNVERIFIED",
        ):
            self.assertIn(term, evidence)

    def test_all_lifecycle_routes_link_the_existing_evidence_owner(self) -> None:
        owner_path = "docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md"
        for path in (WORKFLOW, ROUTING, GODOT_SAFETY):
            self.assertIn(owner_path, read(path), str(path))

    def test_existing_wrong_target_and_provider_boundaries_remain(self) -> None:
        workflow = read(WORKFLOW)
        for term in (
            "stale PID/session을 current truth로 쓰지 않음",
            "다른 프로젝트 editor/server/process를 임의 조작하지 않음",
            "실제 Godot/runtime을 실행하지 않았으면 runtime PASS 아님",
        ):
            self.assertIn(term, workflow)

        godot_safety = read(GODOT_SAFETY)
        for term in (
            "DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
            "persistent_source_mutation: forbidden",
            "LOOPBACK_ONLY",
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
