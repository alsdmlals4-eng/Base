from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
INTAKE_SKILL = ROOT / "skills" / "managing-project-intake-and-work-contract" / "SKILL.md"
FIRST_PROMPT_REFERENCE = (
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "first-prompt-direction-anchoring.md"
)
INSTRUCTION_METHOD = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md"
)
LEGACY_ALIASES = ROOT / "skills" / "LEGACY_SKILL_ALIASES.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class FirstPromptIntakeContractTests(unittest.TestCase):
    def test_existing_intake_skill_owns_first_prompt_without_new_registry_skill(self) -> None:
        skill = INTAKE_SKILL.read_text(encoding="utf-8")
        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("`first-prompt`", skill)
        self.assertIn("first-prompt-direction-anchoring.md", skill)
        self.assertNotIn('"skill_id":"first-prompt"', registry.replace(" ", ""))
        self.assertNotIn('"skill_id":"good-prompt"', registry.replace(" ", ""))

    def test_reference_front_loads_direction_without_changing_authority(self) -> None:
        self.assertTrue(FIRST_PROMPT_REFERENCE.is_file())
        text = FIRST_PROMPT_REFERENCE.read_text(encoding="utf-8")
        for required in (
            "DIRECTION_ANCHOR",
            "TASK_AND_SUCCESS",
            "CONTEXT_AND_SOURCES",
            "CONSTRAINTS_AND_PROTECTED_SCOPE",
            "OUTPUT_AND_VALIDATION",
            "OPTIONAL_RESPONSE_DIVERSIFICATION",
            "프롬프트 가장 앞",
            "앞에 배치했다고 상위 권한이 되지 않는다",
            "HARD_CONSTRAINT",
            "conflict scan",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_first_prompt_absorbs_explicit_structure_and_optional_three_way_exploration(self) -> None:
        text = FIRST_PROMPT_REFERENCE.read_text(encoding="utf-8")
        for required in (
            "Task",
            "Context",
            "Source",
            "Constraints",
            "Output",
            "Validation",
            "정석안",
            "파격안",
            "통합안",
            "같은 평가 기준",
            "기계적 작업",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_every_l1_instruction_runs_intake_and_alignment_before_execution(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        skill = INTAKE_SKILL.read_text(encoding="utf-8")
        for required in (
            "모든 L1 이상 지시문 작성",
            "좋은 프롬프트 변환",
            "Grill Me alignment gate",
            "실행 전",
            "AWAITING_USER_CONFIRMATION",
        ):
            with self.subTest(required=required):
                self.assertIn(required, agents + "\n" + skill)
        self.assertLess(skill.index("`first-prompt`"), skill.index("`contract`"))

    def test_alignment_gate_reuses_approval_and_preserves_l0_exception(self) -> None:
        skill = INTAKE_SKILL.read_text(encoding="utf-8")
        for required in (
            "exact contract already approved",
            "approval reference",
            "중복 질문",
            "L0",
            "오탈자",
            "입력과 판정 기준이 동일한 검사를 재실행",
        ):
            with self.subTest(required=required):
                self.assertIn(required, skill)

    def test_method_and_legacy_names_route_to_the_same_owner(self) -> None:
        method = INSTRUCTION_METHOD.read_text(encoding="utf-8")
        aliases = LEGACY_ALIASES.read_text(encoding="utf-8")
        for required in (
            "First-prompt direction anchoring",
            "direction anchor",
            "instruction/context",
            "Grill Me alignment gate",
        ):
            with self.subTest(required=required):
                self.assertIn(required, method)
        for alias in ("[좋은 프롬프트]", "좋은 프롬프트", "퍼스트 프롬프트", "first prompt"):
            with self.subTest(alias=alias):
                self.assertIn(alias, aliases)
        self.assertIn("`first-prompt` + `contract` + `clarify`", aliases)


if __name__ == "__main__":
    unittest.main()
