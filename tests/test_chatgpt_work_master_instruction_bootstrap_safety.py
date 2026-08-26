from pathlib import Path

TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md")


def test_work_product_surface_and_base_work_mode_are_not_conflated():
    text = TARGET.read_text(encoding="utf-8")
    assert "CHATGPT_WORK_SURFACE != BASE_WORK_MODE" in text
    assert "PLAN / BUILD / REVIEW" in text


def test_project_name_only_bootstrap_resolves_exact_identity_before_mutation():
    text = TARGET.read_text(encoding="utf-8")
    assert "PROJECT_IDENTITY_RESOLUTION_GATE" in text
    assert "repository + Notion Home + project key" in text
    assert "AMBIGUOUS_PROJECT_IDENTITY" in text


def test_private_project_canon_cannot_be_replaced_by_web_or_memory_guessing():
    text = TARGET.read_text(encoding="utf-8")
    assert "PRIVATE_CANON_SOURCE_FAIL_CLOSED" in text
    assert "web search나 Memory로 대체하지 않는다" in text
    assert "BLOCKED_UNVERIFIED" in text
