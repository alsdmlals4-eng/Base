from pathlib import Path


TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md")


def test_primary_instruction_makes_no_separate_goal_the_default_entry() -> None:
    text = TARGET.read_text(encoding="utf-8")
    for term in (
        "PROJECT_PLUS_INSTRUCTION_IS_DEFAULT_SUFFICIENT_INPUT",
        "SEPARATE_GOAL_NOT_REQUIRED_BY_DEFAULT",
    ):
        assert term in text

    assert "기본 입력은 **`프로젝트명 + 이 공용 작업지시문`**" in text
    assert "별도 Goal은 필수가 아니다" in text
