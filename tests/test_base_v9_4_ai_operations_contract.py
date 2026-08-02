from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
MODEL_SKILL = ROOT / "skills" / "optimizing-ai-model-and-prompt-costs" / "SKILL.md"
MODEL_ROUTING = ROOT / "skills" / "optimizing-ai-model-and-prompt-costs" / "references" / "model-stack-routing.md"
PROMPT_CACHING = ROOT / "skills" / "optimizing-ai-model-and-prompt-costs" / "references" / "prompt-caching.md"
INSTRUCTION_METHOD = ROOT / "docs" / "knowledge" / "game-development" / "AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md"
INTAKE_SKILL = ROOT / "skills" / "managing-project-intake-and-work-contract" / "SKILL.md"
FIRST_PROMPT_REFERENCE = (
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "first-prompt-direction-anchoring.md"
)
AGENTS = ROOT / "AGENTS.md"
LEGACY_ALIASES = ROOT / "skills" / "LEGACY_SKILL_ALIASES.md"
UI_SKILL = ROOT / "skills" / "auditing-and-refining-ui-art" / "SKILL.md"
UI_MOTION = ROOT / "skills" / "auditing-and-refining-ui-art" / "references" / "ui-motion-and-interaction-principles.md"
V94_LOCK = ROOT / "base-v9.4.lock.json"
V94_SCHEMA = ROOT / "schemas" / "base-v9-4-candidate-lock-v1.schema.json"
V93_LOCK = ROOT / "base-v9.3.lock.json"
PROPOSALS = ROOT / "[수정제안서]" / "PROPOSAL_REGISTRY.json"
PAYLOAD_COMMIT = "a728712cb776ec98f4875914a580fcf7d0156593"
EVIDENCE_COMMIT = "ef1fba11167e4da0b298123b0c85ebd268191a42"


class BaseV94AiOperationsContractTests(unittest.TestCase):
    def test_required_skill_method_and_reference_files_exist(self) -> None:
        required = [
            MODEL_SKILL,
            MODEL_ROUTING,
            PROMPT_CACHING,
            INSTRUCTION_METHOD,
            FIRST_PROMPT_REFERENCE,
            UI_MOTION,
            V94_LOCK,
            V94_SCHEMA,
            ROOT / "docs" / "operations" / "BASE_V9_4_RELEASE_CONTRACT.md",
            ROOT / "docs" / "operations" / "BASE_V9_4_RELEASE_EVIDENCE.json",
        ]
        missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_model_cost_skill_has_five_modes_and_recommendation_contract(self) -> None:
        text = MODEL_SKILL.read_text(encoding="utf-8")
        for mode in (
            "route-model-and-effort",
            "design-cacheable-prefix",
            "estimate-cost",
            "measure-actual-usage",
            "recalibrate",
        ):
            with self.subTest(mode=mode):
                self.assertIn(f"`{mode}`", text)
        for field in (
            "recommended_model",
            "recommended_reasoning",
            "next_checkpoint",
            "provider_profile_status",
            "continue_without_change_risk",
        ):
            with self.subTest(field=field):
                self.assertIn(field, text)
        self.assertIn("[모델 추천]", text)
        self.assertIn("실제 모델 설정을 변경", text)

    def test_model_routing_and_caching_keep_quality_and_provider_boundaries(self) -> None:
        routing = MODEL_ROUTING.read_text(encoding="utf-8")
        caching = PROMPT_CACHING.read_text(encoding="utf-8")
        for required in (
            "SIMPLE_BULK",
            "ROUTINE_BALANCED",
            "HIGH_RISK_REASONING",
            "Luna",
            "Terra",
            "Sol",
            "재작업",
            "checkpoint",
        ):
            with self.subTest(required=required):
                self.assertIn(required, routing)
        for required in (
            "stable_prefix",
            "dynamic_suffix",
            "verified_at",
            "official_source",
            "STALE_RECHECK_REQUIRED",
            "민감",
            "재시도",
        ):
            with self.subTest(required=required):
                self.assertIn(required, caching)

    def test_instruction_method_preserves_authority_examples_and_context_curation(self) -> None:
        text = INSTRUCTION_METHOD.read_text(encoding="utf-8")
        for required in (
            "HARD_CONSTRAINT",
            "RECOMMENDED_DEFAULT",
            "JUDGMENT_SPACE",
            "Interface-first",
            "Fixture",
            "Golden Set",
            "decision_question",
            "exclude_criteria",
            "known_conflicts",
            "progressive_load_trigger",
            "refresh_trigger",
            "반대 근거",
            "주장 상한",
            "NOT_RUN",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_first_prompt_intake_and_alignment_contract(self) -> None:
        reference = FIRST_PROMPT_REFERENCE.read_text(encoding="utf-8")
        skill = INTAKE_SKILL.read_text(encoding="utf-8")
        method = INSTRUCTION_METHOD.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")
        aliases = LEGACY_ALIASES.read_text(encoding="utf-8")
        for required in (
            "DIRECTION_ANCHOR",
            "TASK_AND_SUCCESS",
            "CONTEXT_AND_SOURCES",
            "CONSTRAINTS_AND_PROTECTED_SCOPE",
            "OUTPUT_AND_VALIDATION",
            "OPTIONAL_RESPONSE_DIVERSIFICATION",
            "프롬프트 가장 앞",
            "앞에 배치했다고 상위 권한이 되지 않는다",
            "정석안",
            "파격안",
            "통합안",
            "conflict scan",
        ):
            with self.subTest(reference=required):
                self.assertIn(required, reference)
        for required in (
            "`first-prompt`",
            "first-prompt-direction-anchoring.md",
            "Grill Me alignment gate",
            "AWAITING_USER_CONFIRMATION",
            "exact contract already approved",
            "approval reference",
        ):
            with self.subTest(skill=required):
                self.assertIn(required, skill)
        for required in (
            "First-prompt direction anchoring",
            "direction anchor",
            "instruction/context",
            "Grill Me alignment gate",
        ):
            with self.subTest(method=required):
                self.assertIn(required, method)
        for required in (
            "모든 L1 이상 지시문 작성",
            "좋은 프롬프트 변환",
            "Grill Me alignment gate",
            "실행 전",
        ):
            with self.subTest(agents=required):
                self.assertIn(required, agents)
        for alias in ("[좋은 프롬프트]", "좋은 프롬프트", "퍼스트 프롬프트", "first prompt"):
            with self.subTest(alias=alias):
                self.assertIn(alias, aliases)
        self.assertIn("`first-prompt` + `contract` + `clarify`", aliases)

    def test_ui_motion_contract_covers_authority_interruption_and_fallbacks(self) -> None:
        text = UI_MOTION.read_text(encoding="utf-8")
        for required in (
            "staging",
            "anticipation",
            "timing",
            "easing",
            "공간적 연속성",
            "follow-through",
            "입력 접수",
            "처리 중",
            "결과",
            "중단",
            "즉시 완료",
            "빠른 반복",
            "재진입",
            "Reduced Motion",
            "mute",
            "haptic-off",
            "AnimationPlayer",
            "Tween",
            "도메인",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("ui-motion-and-interaction-principles.md", UI_SKILL.read_text(encoding="utf-8"))

    def test_registry_routes_new_skill_and_extended_existing_responsibilities(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        self.assertIn("optimizing-ai-model-and-prompt-costs", by_id)
        model = by_id["optimizing-ai-model-and-prompt-costs"]
        self.assertEqual("ACTIVE", model["status"])
        self.assertTrue(
            {
                "model-recommendation",
                "model-effort-routing",
                "prompt-caching",
                "ai-cost-estimation",
                "provider-profile",
            }.issubset(set(model["trigger_tags"]))
        )
        intake = by_id["managing-project-intake-and-work-contract"]
        simplifying = by_id["simplifying-skill-bodies"]
        ui = by_id["auditing-and-refining-ui-art"]
        self.assertIn("instruction-authority", intake["trigger_tags"])
        self.assertIn("example-as-fixture", simplifying["trigger_tags"])
        self.assertIn("ui-motion-design", ui["trigger_tags"])

    def test_required_consumers_link_to_new_contracts(self) -> None:
        consumers = {
            ROOT / "docs" / "DOCUMENTATION_MAP.md": (
                "AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md",
                "optimizing-ai-model-and-prompt-costs",
                "ui-motion-and-interaction-principles.md",
            ),
            ROOT / "docs" / "knowledge" / "game-development" / "AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md": (
                "AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md",
                "optimizing-ai-model-and-prompt-costs",
            ),
            ROOT / "templates" / "project-operations" / "AI_WORKFLOW.md": (
                "[모델 추천]",
                "HARD_CONSTRAINT",
                "Context 큐레이션",
            ),
            ROOT / "templates" / "planning" / "GAME_UX_UI_SYSTEM.md": (
                "모션 목적",
                "중단",
                "Reduced Motion",
            ),
            ROOT / "templates" / "quality" / "GAME_UX_UI_REVIEW_CHECKLIST.md": (
                "도메인 상태 권위",
                "즉시 완료",
                "haptic-off",
            ),
        }
        for path, required_values in consumers.items():
            text = path.read_text(encoding="utf-8")
            for required in required_values:
                with self.subTest(path=path.relative_to(ROOT).as_posix(), required=required):
                    self.assertIn(required, text)

    def test_bcp_003_and_004_are_implemented_and_linked(self) -> None:
        registry = json.loads(PROPOSALS.read_text(encoding="utf-8"))
        by_id = {item["proposal_id"]: item for item in registry["proposals"]}
        expected = {
            "BCP-2026-003-ai-model-prompt-cost-optimization": "https://github.com/alsdmlals4-eng/Base/issues/113",
            "BCP-2026-004-ai-instruction-context-ui-motion": "https://github.com/alsdmlals4-eng/Base/issues/115",
        }
        for proposal_id, approval_ref in expected.items():
            with self.subTest(proposal_id=proposal_id):
                proposal = by_id[proposal_id]
                self.assertEqual("IMPLEMENTED", proposal["status"])
                self.assertEqual(approval_ref, proposal["approval_ref"])
                self.assertEqual("https://github.com/alsdmlals4-eng/Base/pull/118", proposal["implementation_pr"])

    def test_v94_released_pins_and_current_registry_hash(self) -> None:
        lock = json.loads(V94_LOCK.read_text(encoding="utf-8"))
        schema = json.loads(V94_SCHEMA.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(lock))
        self.assertEqual([], [error.message for error in errors])
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(PAYLOAD_COMMIT, lock["candidate_release_commit"])
        self.assertEqual(EVIDENCE_COMMIT, lock["candidate_release_evidence_commit"])
        self.assertEqual(113, lock["github_issue"])
        self.assertEqual(115, lock["linked_issue"])
        self.assertEqual(
            hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
            lock["candidate_registry"]["sha256"],
        )

    def test_v94_does_not_rewrite_v93_released_identity(self) -> None:
        lock = json.loads(V93_LOCK.read_text(encoding="utf-8"))
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual("30ca6c7b5f93521f0eb0eed42d01437cd43c50ae", lock["candidate_release_commit"])
        self.assertEqual("462a86db192d23d0f386281a1eb54b0a8cbad62e", lock["candidate_release_evidence_commit"])


if __name__ == "__main__":
    unittest.main()