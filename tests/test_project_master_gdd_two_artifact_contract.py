import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md"
INSTRUCTION = (
    ROOT
    / "templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md"
)
FEATURE_SPEC_TEMPLATE = ROOT / "templates/planning/GAME_FEATURE_DESIGN_SPEC.md"
PROJECT_OPERATIONS_README = ROOT / "templates/project-operations/README.md"
CUSTOM_INSTRUCTIONS = ROOT / "templates/custom-instructions.gpt.md"
NOTION_BLUEPRINT_CONTRACT = (
    ROOT
    / "docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md"
)
DOCUMENTATION_MAP = ROOT / "docs/DOCUMENTATION_MAP.md"


def assert_ordered(test: unittest.TestCase, text: str, terms: tuple[str, ...]) -> None:
    positions = []
    for term in terms:
        test.assertIn(term, text)
        positions.append(text.index(term))
    test.assertEqual(positions, sorted(positions), f"terms must be ordered: {terms}")


class ProjectMasterGddTwoArtifactContractTests(unittest.TestCase):
    def test_policy_defines_exactly_two_deliverables(self):
        self.assertTrue(POLICY.exists(), "two-artifact master GDD policy must exist")
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "HUMAN_MASTER_GDD_PDF",
            "AI_PRODUCTION_SPEC_MARKDOWN",
            "exports/[PROJECT]_MASTER_PRODUCTION_GDD_[YYYYMMDD].pdf",
            "docs/design/PROJECT_AI_PRODUCTION_SPEC.md",
            "NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX",
            "NO_SEPARATE_IMAGE_BUNDLE",
        ):
            self.assertIn(required, text)

    def test_layered_human_blueprint_profile_stays_inside_two_artifacts(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE",
            "NO_SEPARATE_BLUEPRINT_ARTIFACT",
            "PROJECT_PLAYER_LAYER",
            "SYSTEM_LAYER",
            "CONTENT_UX_PRESENTATION_LAYER",
            "PRODUCTION_EVIDENCE_LAYER",
            "FIRST_5_15_30",
            "REUSABLE_FLOW_AND_SYSTEM_CARDS",
            "LAYERED_TRACEABILITY_REQUIRED",
            "STATE_AND_EVIDENCE_LEGEND",
            "CONDITIONAL_MODULE_NA_WITH_REASON",
            "REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION",
            "NO_MASS_BLUEPRINT_BACKFILL",
        ):
            self.assertIn(required, text)
        assert_ordered(
            self,
            text,
            (
                "3-MINUTE PROJECT / PLAYER READ",
                "10-MINUTE SYSTEM + CONTENT / UX / PRESENTATION READ",
                "DETAIL READ",
                "IMPLEMENTATION READ",
                "VERIFICATION READ",
            ),
        )

    def test_blueprint_wireframes_are_conditional_decision_surfaces_with_evidence_boundaries(self):
        required = (
            "BLUEPRINT_WIREFRAME_DECISION_SURFACE",
            "WIREFRAME_WITHIN_EXISTING_TWO_ARTIFACTS",
            "TWO_ARTIFACT_PROFILE_CONDITIONALLY_APPLIES",
            "WIRE_FRAME_ONLY_FOR_MATERIAL_PLAYER_FACING_SURFACE",
            "SMALLEST_REPRESENTATIVE_WIREFRAME_SET",
            "SCREEN_LEVEL_COMPOSITION_REQUIRED",
            "screen_id",
            "priority",
            "entry / exit / cancel / re-entry",
            "primary / secondary action",
            "disabled / error / unavailable state",
            "planned or actual consumer",
            "WIREFRAME_NOT_RUNTIME_OR_USER_APPROVAL_EVIDENCE",
            "NOT_RUN",
        )
        for path in (POLICY, INSTRUCTION, FEATURE_SPEC_TEMPLATE):
            self.assertTrue(path.exists(), f"wireframe owner must exist: {path}")
            text = path.read_text(encoding="utf-8")
            for token in required:
                self.assertIn(token, text, f"{path} must preserve Blueprint wireframe token: {token}")

    def test_layered_profile_uses_text_native_exact_diagrams_and_image_gate(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "TEXT_NATIVE_EXACT_DIAGRAMS",
            "Mermaid / Flow / table",
            "CURRENT_IMAGE_CREATION_POLICY_REQUIRED",
            "NO_AUTOMATIC_IMAGE_GENERATION",
        ):
            self.assertIn(required, text)

    def test_policy_requires_user_final_blueprint_approval_before_implementation(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE",
            "PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH",
            "BLUEPRINT_PASS_1_STRUCTURAL_DRAFT",
            "STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT",
            "BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT",
            "REQUIRED_IMAGE_AND_MATERIAL_PREPARATION",
            "REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS",
            "BLUEPRINT_PASS_2_FINAL",
            "VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT",
            "ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD",
            "USER_FINAL_REVIEW_APPROVAL_REQUIRED",
            "NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL",
            "FRAME → RESEARCH → DESIGN → SPECIFY",
            "CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH",
            "DRAFT | INTERNAL_REVIEW | GENERATED_IMAGE | AUTOMATED_TEST | ASSISTANT_INFERENCE",
            "USER_FINAL_APPROVAL_DECISION_ID",
            "TASK_BREAKDOWN_READY_IMPLEMENTATION_EXECUTION_BLOCKED",
            "PROSPECTIVE_ONLY_EXISTING_IMPLEMENTATION_EVIDENCE_PRESERVED",
            "IMAGE_CONVERSATION_APPROVAL_GATE.md",
            "IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md",
            "STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE",
        ):
            self.assertIn(required, text)
        self.assertIn(
            "PLAN\n"
            "→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT\n"
            "→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION\n"
            "→ BLUEPRINT_REVIEW_PUBLICATION\n"
            "→ USER_FINAL_REVIEW_APPROVAL\n"
            "→ IMPLEMENTATION_AUTHORIZED",
            text,
        )

    def test_policy_preserves_only_exact_pre_adoption_approved_unstarted_package(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "PROSPECTIVE_ONLY_PREEXISTING_EXACT_USER_APPROVED_IMPLEMENTATION_AUTHORITY_PRESERVED",
            "PRE_ADOPTION_USER_APPROVED_BUT_IMPLEMENTATION_NOT_STARTED",
            "EXACT_APPROVED_SCOPE_AND_REVISION_ONLY",
            "SCOPE_EXPANSION | SUCCESSOR_PACKAGE | INFERRED_BLANKET_APPROVAL",
        ):
            self.assertIn(required, text)

    def test_human_pdf_requires_system_content_and_implementation_depth(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED",
            "플레이어 감정",
            "핵심 시스템",
            "핵심 콘텐츠",
            "Godot 씬",
            "노드",
            "스크립트 책임",
            "데이터 소유권",
            "상태 전이",
            "신호",
            "저장·로드",
            "구현 순서",
            "Acceptance Criteria",
            "실제 구현 증거 화면",
        ):
            self.assertIn(required, text)

    def test_ai_spec_preserves_machine_implementation_contract(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "CANON SNAPSHOT",
            "SOURCE REGISTRY",
            "SYSTEM REGISTRY",
            "CONTENT REGISTRY",
            "DATA CONTRACTS",
            "SCENE MAP",
            "SCRIPT RESPONSIBILITY MAP",
            "SIGNAL AND EVENT FLOW",
            "STATE MACHINES",
            "SAVE/LOAD CONTRACT",
            "IMPLEMENTATION TRACEABILITY",
            "TEST AND QA CONTRACT",
            "IMPLEMENTATION QUEUE",
        ):
            self.assertIn(required, text)

    def test_profile_makes_notion_input_only_without_global_deprecation(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "NOTION_INPUT_ONLY_NO_OUTPUT",
            "기존 Notion",
            "고유 미이관 자료",
            "신규 출력·갱신·동기화·readback 대상이 아니다",
            "GLOBAL_NOTION_DEPRECATION_FORBIDDEN",
            "DOMAIN_SPLIT_CANON",
        ):
            self.assertIn(required, text)
        self.assertNotIn("모든 프로젝트에서 Notion을 폐기한다", text)

    def test_delivery_exposes_only_pdf_download_and_reports_ai_path(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "PDF_ONLY_USER_DOWNLOAD",
            "AI_SPEC_REPOSITORY_PATH_REPORT_ONLY",
            "repository path",
            "branch",
            "commit SHA",
            "PR",
            "validation result",
        ):
            self.assertIn(required, text)

    def test_pdf_and_ai_spec_share_ids_sha_and_evidence_ceiling(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "SHARED_ID_AND_SOURCE_SHA_REQUIRED",
            "SYS-",
            "CNT-",
            "UI-",
            "UX-",
            "AST-",
            "AUD-",
            "DAT-",
            "QA-",
            "DEC-",
            "DOCUMENTED",
            "CONFIRMED",
            "IMPLEMENTED",
            "AUTOMATED_TEST_PASS",
            "RUNTIME_VERIFIED",
            "UX_VERIFIED",
            "RELEASE_READY",
            "RUNTIME_TRUTH_SEPARATE",
        ):
            self.assertIn(required, text)

    def test_profile_preserves_image_approval_boundary(self):
        text = POLICY.read_text(encoding="utf-8")
        for required in (
            "NO_AUTOMATIC_IMAGE_GENERATION",
            "기존 승인 이미지",
            "실제 build capture",
            "현재 승인 Visual 없음",
            "별도의 사용자 명시적 요청",
        ):
            self.assertIn(required, text)

    def test_work_instruction_is_paste_ready_and_executes_full_work(self):
        self.assertTrue(INSTRUCTION.exists(), "paste-ready two-artifact instruction must exist")
        text = INSTRUCTION.read_text(encoding="utf-8")
        for required in (
            "현재 이 채팅이 연결된 프로젝트",
            "정확히 2개",
            "사용자용 상세 기획서 PDF",
            "AI용 상세 기획·구현 명세 Markdown",
            "직접 경쟁작 5~8개",
            "인접 장르 참고작 2~3개",
            "ADOPT / ADAPT / REJECT",
            "핵심 시스템",
            "핵심 콘텐츠",
            "Godot",
            "PDF만 다운로드 링크",
            "Notion",
            "신규 출력",
            "NO_AUTOMATIC_IMAGE_GENERATION",
            "남은 작업 0",
        ):
            self.assertIn(required, text)
        self.assertNotIn("[프로젝트명]", text)
        self.assertNotIn("TBD", text)

    def test_work_instruction_orders_source_reconstruction_before_outputs(self):
        text = INSTRUCTION.read_text(encoding="utf-8")
        assert_ordered(
            self,
            text,
            (
                "## 1. 최신 정본 재구성",
                "## 2. 벤치마킹·현업 조사",
                "## 3. 공통 ID와 상태 모델",
                "## 4. 사용자용 PDF",
                "## 5. AI용 Markdown",
                "## 6. 생성·저장·검증",
                "## 7. 최종 제공 방식",
                "## 8. 완료 기준",
            ),
        )

    def test_work_instruction_operationalizes_same_layered_profile(self):
        text = INSTRUCTION.read_text(encoding="utf-8")
        for required in (
            "HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE",
            "NO_SEPARATE_BLUEPRINT_ARTIFACT",
            "PROJECT_PLAYER_LAYER",
            "SYSTEM_LAYER",
            "CONTENT_UX_PRESENTATION_LAYER",
            "PRODUCTION_EVIDENCE_LAYER",
            "FIRST_5_15_30",
            "REUSABLE_FLOW_AND_SYSTEM_CARDS",
            "LAYERED_TRACEABILITY_REQUIRED",
            "STATE_AND_EVIDENCE_LEGEND",
            "CONDITIONAL_MODULE_NA_WITH_REASON",
            "REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION",
            "NO_MASS_BLUEPRINT_BACKFILL",
            "TEXT_NATIVE_EXACT_DIAGRAMS",
            "CURRENT_IMAGE_CREATION_POLICY_REQUIRED",
        ):
            self.assertIn(required, text)
        assert_ordered(
            self,
            text,
            (
                "3-MINUTE PROJECT / PLAYER READ",
                "10-MINUTE SYSTEM + CONTENT / UX / PRESENTATION READ",
                "DETAIL READ",
                "IMPLEMENTATION READ",
                "VERIFICATION READ",
            ),
        )

    def test_work_instruction_stops_implementation_until_recorded_final_approval(self):
        text = INSTRUCTION.read_text(encoding="utf-8")
        for required in (
            "BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE",
            "PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH",
            "BLUEPRINT_PASS_1_STRUCTURAL_DRAFT",
            "STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT",
            "BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT",
            "REQUIRED_IMAGE_AND_MATERIAL_PREPARATION",
            "REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS",
            "BLUEPRINT_PASS_2_FINAL",
            "VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT",
            "ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD",
            "USER_FINAL_REVIEW_APPROVAL_REQUIRED",
            "NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL",
            "FRAME → RESEARCH → DESIGN → SPECIFY",
            "CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH",
            "DRAFT | INTERNAL_REVIEW | GENERATED_IMAGE | AUTOMATED_TEST | ASSISTANT_INFERENCE",
            "USER_FINAL_APPROVAL_DECISION_ID",
            "TASK_BREAKDOWN_READY_IMPLEMENTATION_EXECUTION_BLOCKED",
            "PROSPECTIVE_ONLY_EXISTING_IMPLEMENTATION_EVIDENCE_PRESERVED",
            "IMAGE_CONVERSATION_APPROVAL_GATE.md",
            "IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md",
            "STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE",
        ):
            self.assertIn(required, text)
        self.assertIn(
            "PLAN\n"
            "→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT\n"
            "→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION\n"
            "→ BLUEPRINT_REVIEW_PUBLICATION\n"
            "→ USER_FINAL_REVIEW_APPROVAL\n"
            "→ IMPLEMENTATION_AUTHORIZED",
            text,
        )

    def test_work_instruction_preserves_only_exact_pre_adoption_approved_unstarted_package(self):
        text = INSTRUCTION.read_text(encoding="utf-8")
        for required in (
            "PROSPECTIVE_ONLY_PREEXISTING_EXACT_USER_APPROVED_IMPLEMENTATION_AUTHORITY_PRESERVED",
            "PRE_ADOPTION_USER_APPROVED_BUT_IMPLEMENTATION_NOT_STARTED",
            "EXACT_APPROVED_SCOPE_AND_REVISION_ONLY",
            "SCOPE_EXPANSION | SUCCESSOR_PACKAGE | INFERRED_BLANKET_APPROVAL",
        ):
            self.assertIn(required, text)

    def test_selected_profile_skips_separate_blueprint_output_and_readback(self):
        text = NOTION_BLUEPRINT_CONTRACT.read_text(encoding="utf-8")
        for required in (
            "TWO_ARTIFACT_PROFILE_NO_NOTION_BLUEPRINT_OUTPUT_READBACK",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "NO_SEPARATE_BLUEPRINT_ARTIFACT",
            "human-projection lifecycle",
            "Notion에 write back하지 않는다",
        ):
            self.assertIn(required, text)

    def test_documentation_map_routes_the_layered_profile(self):
        text = DOCUMENTATION_MAP.read_text(encoding="utf-8")
        for required in (
            "HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE",
            "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md",
            "templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md",
            "NO_SEPARATE_BLUEPRINT_ARTIFACT",
        ):
            self.assertIn(required, text)

    def test_project_operations_readme_routes_the_optional_profile(self):
        text = PROJECT_OPERATIONS_README.read_text(encoding="utf-8")
        for required in (
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md",
            "GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md",
            "명시적으로 선택한 경우",
        ):
            self.assertIn(required, text)

    def test_custom_instructions_expose_bounded_profile_without_replacing_default_canon(self):
        text = CUSTOM_INSTRUCTIONS.read_text(encoding="utf-8")
        for required in (
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "사용자용 상세 PDF",
            "AI용 repository Markdown",
            "Notion은 입력 자료로만",
            "기존 DOMAIN_SPLIT_CANON을 전역 폐기하지 않는다",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
