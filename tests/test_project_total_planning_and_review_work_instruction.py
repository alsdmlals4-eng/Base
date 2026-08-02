from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "templates" / "prompts" / "PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION_v1.md"
INDEX = ROOT / "templates" / "prompts" / "README.md"


def test_project_total_planning_and_review_prompt_contract() -> None:
    text = PROMPT.read_text(encoding="utf-8")

    required_markers = (
        "[총기획]",
        "[검수]",
        "[핵심 내용]",
        "TOTAL_PLANNING",
        "REVIEW",
        "PROJECT_ENVIRONMENT_FIRST",
        "00 / 10 / 20 / 30 / 40 / 50 / 99",
        "using-superpowers",
        "brainstorming",
        "NEUTRAL_RECOMMENDATION_GATE",
        "attack",
        "validate-critique",
        "regression-recheck",
        "READ_ONLY",
        "BLOCKED_UNVERIFIED",
        "Draft PR",
        "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
    )

    missing = [marker for marker in required_markers if marker not in text]
    assert not missing, f"missing project planning/review prompt markers: {missing}"


def test_prompt_index_routes_planning_review_and_vertical_slice_contracts() -> None:
    text = INDEX.read_text(encoding="utf-8")

    assert "PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION_v1.md" in text
    assert "TOTAL_PLANNING" in text
    assert "REVIEW" in text
    assert "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md" in text
    assert "SUPERSEDED_COMPATIBILITY" in text
    assert "최신 Base" in text
