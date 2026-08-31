"""Routing/document regressions, not an LLM compliance or runtime evaluation."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = 'skills/auditing-and-refining-ui-art/references/benchmark-first-modular-production.md'
ADAPTER = 'skills/auditing-and-refining-ui-art/references/project-adapter-contract.md'


class ProductionContractTests(unittest.TestCase):
    def guide(self):
        self.assertTrue((ROOT / GUIDE).is_file(), 'Missing executed-skill reference')
        return (ROOT / GUIDE).read_text(encoding='utf-8')

    def test_always_on_route_points_to_guide(self):
        self.assertIn(GUIDE, (ROOT / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_project_adapter_reaches_guide_without_contract_repin(self):
        text = (ROOT / ADAPTER).read_text(encoding='utf-8')
        self.assertIn('benchmark-first-modular-production.md', text)
        self.assertIn('PRESERVE_ADOPTED_CONTRACT_PIN', text)

    def test_order_and_scope_ceilings(self):
        text = self.guide()
        for token in ['EXTERNAL_THEN_PROJECT_FIT', 'MODULAR_PARTS_FIRST',
                      'APPROVED_SCOPE_IS_DENOMINATOR', 'NO_SECOND_ASSET_CANON',
                      'PLANNED_CONSUMER_CONTRACTED', 'STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL']:
            with self.subTest(token=token): self.assertIn(token, text)

    def test_external_game_and_implementation_evidence_present(self):
        text = self.guide()
        for token in ['Mindustry', 'Wildermyth', 'Wesnoth', 'Dialogic', 'Dialogue Manager',
                      'da3b3358cd03e47ef32a87ee5b40231e656d1c76',
                      '69fb4534988c731f627246b1f0c3a98f239b69f7', 'ADOPT', 'ADAPT', 'REJECT']:
            with self.subTest(token=token): self.assertIn(token, text)

    def test_modular_source_and_runtime_artifact_are_not_confused(self):
        text = self.guide()
        for token in ['AUTHORING_PARTS_NOT_RUNTIME_ATLAS', 'MODULE_APPROVAL_IS_NOT_ASSEMBLY_APPROVAL',
                      'StyleBoxTexture', 'NinePatchRect', 'content_margin', 'texture_margin',
                      'IMAGE_MODEL_REQUIRED_FOR_AUTHORED_ART', 'NO_CARTESIAN_ASSET_EXPLOSION']:
            with self.subTest(token=token): self.assertIn(token, text)

    def test_complete_interaction_and_capture_are_required(self):
        text = self.guide()
        for token in ['새 게임', '이어하기', '도감', '설정', '종료',
                      '대화창', '탭', 'VISUAL_CHANGE_REQUIRES_INGAME_CAPTURE',
                      '실제 입력', 'SHA-256', 'HUMAN_NOT_RUN',
                      'MODULE_SHEET_IS_NOT_INGAME_CAPTURE']:
            with self.subTest(token=token): self.assertIn(token, text)

    def test_canonical_mapping_limits_are_explicit(self):
        text = self.guide()
        self.assertIn('선언된 분모 자체의 완전성은 증명하지 않는다', text)
        self.assertIn('고유 규칙', text)
        self.assertIn('이미 채택한', text)
        self.assertIn('validate_player_surface_plan.py', text)

    def test_no_hosted_service_or_new_game_engine_required(self):
        text = self.guide()
        self.assertIn('추가 유료 API', text)
        self.assertIn('엔진 자동 업그레이드', text)
        self.assertIn('기존 열린 PR', text)


if __name__ == '__main__':
    unittest.main()
