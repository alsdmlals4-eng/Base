"""Document/data contract tests, not Godot, image quality, or player tests."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "skills/auditing-and-refining-ui-art/references"
GUIDE = REFS / "ui-surface-production-readiness.md"
ADAPTER = REFS / "project-adapter-contract.md"


class UISurfaceProductionContractTests(unittest.TestCase):
    def text(self):
        self.assertTrue(GUIDE.is_file(), "Missing subordinate production companion")
        return GUIDE.read_text(encoding="utf-8")

    def contains(self, *phrases):
        text = self.text()
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_existing_adapter_routes_to_companion(self):
        text = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("ui-surface-production-readiness.md", text)
        self.assertIn("UI-REFERENCE-FIRST", text)
        self.assertIn("UI-MODULES", text)

    def test_external_first_does_not_bypass_current_project_authority(self):
        self.contains(
            "외부 게임 비교 기준 → 프로젝트 정본 fresh-read → 차이 분석",
            "외부 기준은 프로젝트의 승인된 의미·자산·version lock을 덮어쓰지 않는다",
            "OPEN_PR_READ_ONLY",
        )

    def test_companion_does_not_create_a_second_canon_or_schema(self):
        self.contains(
            "NOT_A_SECOND_CANON",
            "기존 Feature Spec·화면 인벤토리·Asset Catalog·Traceability에 연결",
            "새 공용 JSON schema나 모든 프로젝트의 경로 이동을 요구하지 않는다",
        )

    def test_complete_game_dimensions_are_not_just_art(self):
        self.contains(
            "핵심 재미·선택·보상", "조작·카메라", "전투·적·레벨",
            "대화·서사", "성장·경제", "오디오·VFX", "저장·복구",
            "접근성·현지화", "성능·플랫폼", "패키징·권리·출시",
        )

    def test_observation_and_public_code_evidence_stay_separate(self):
        self.contains(
            "상용 게임의 스크린샷으로 비공개 구현을 확인했다고 주장하지 않는다",
            "factorio.com/blog/post/fff-348",
            "wiki.wesnoth.org/GUIWidgetDefinitionWML",
            "Anuken/Mindustry/blob/da3b3358cd03e47ef32a87ee5b40231e656d1c76",
            "ADOPT / ADAPT / REJECT",
        )

    def test_authoring_units_and_packaging_are_separate(self):
        self.contains(
            "MODULE_ART → COMPONENT_SCENE → SCREEN_ASSEMBLY",
            "ATLAS_IS_PACKAGING_NOT_AUTHORING",
            "개별 원본과 안정된 asset_id를 보존",
            "완성 화면 한 장을 잘라 부품이 있다고 간주하지 않는다",
            "동일 이미지 스타일을 모든 프로젝트에 강제하지 않는다",
        )

    def test_compatibility_and_combinations_are_specified(self):
        self.contains(
            "style_family", "compatible_slots", "pivot_or_anchor", "alpha_mode",
            "slice_margins", "text_safe_area", "filtering", "allowed_transforms",
            "assembly_recipe", "혼합 조합",
            "조합 수를 전부 곱해 이미지 생성량으로 계산하지 않는다",
        )

    def test_borders_and_native_controls_have_separate_responsibilities(self):
        self.contains(
            "SYSTEM_PANEL", "DIALOGUE_FRAME", "TAB_FRAME",
            "9-slice 프레임 한 장을 아홉 번 따로 생성하지 않는다",
            "텍스트·수치·입력은 실제 Control",
            "IMAGE_MODEL_REQUIRED",
            "작동 가능한 UI를 한 장의 이미지로 굳히지 않는다",
        )

    def test_planned_consumer_can_receive_prepared_art_without_false_runtime(self):
        self.contains(
            "PLANNED_CONSUMER", "구현된 노드가 없어도",
            "미제작 / 생성 후보 / 승인 대기 / 원본 회수 불가 / 미연결 / 조합 불일치 / 런타임 미검증",
            "NO_NEW_IMAGE_REQUIRED", "USER_APPROVED",
        )

    def test_real_navigation_and_actions_are_required(self):
        self.contains(
            "새 게임", "이어하기", "도감", "설정", "종료",
            "PUBLIC_INPUT → 도메인 결과 → 도착 화면 → 저장·재진입",
            "버튼·signal·파일 존재만으로 실동작 완료라 하지 않는다",
            "직접 보트 진입",
        )

    def test_capture_does_not_approve_art_or_prove_human_quality(self):
        self.contains(
            "IN_GAME_CAPTURE_REQUIRED", "exact source", "fixture",
            "생성 시안은 인게임 캡처를 대체하지 않는다",
            "DOC_CONTRACT_PASS ≠ RUNTIME_PASS ≠ HUMAN_PASS",
            "최종 사용자 승인",
        )

    def test_example_is_parseable_reuses_parts_and_is_not_runtime(self):
        packets = [json.loads(block) for block in
                   re.findall(r"```json\s*\n(.*?)\n```", self.text(), re.S)]
        examples = [p for p in packets if p.get("example_kind") == "ILLUSTRATIVE_MODULE_COMPOSITION"]
        self.assertEqual(len(examples), 1)
        example = examples[0]
        self.assertEqual(example["evidence_status"], "DESIGN_EXAMPLE_NOT_RUNTIME")
        identifiers = [m["asset_id"] for m in example["modules"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        used = []
        for assembly in example["assemblies"]:
            self.assertTrue(assembly["live_text"])
            self.assertFalse(assembly["flattened_runtime_ui"])
            self.assertTrue(set(assembly["module_ids"]) <= set(identifiers))
            used.extend(assembly["module_ids"])
        self.assertEqual(set(used), set(identifiers))
        self.assertGreaterEqual(used.count("FRAME_SHARED"), 3)
        self.assertGreaterEqual(used.count("TAB_SHARED"), 2)


if __name__ == "__main__":
    unittest.main()
