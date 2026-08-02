from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "templates" / "prompts" / "PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION_v2.md"
INDEX = ROOT / "templates" / "prompts" / "README.md"


def test_project_total_planning_and_review_prompt_contract() -> None:
    text = PROMPT.read_text(encoding="utf-8")

    required = (
        "[총기획]",
        "[검수]",
        "[핵심 내용]",
        "TOTAL_PLANNING",
        "REVIEW",
        "PROJECT_ENVIRONMENT_FIRST",
        "00 / 10 / 20 / 30 / 40 / 50 / 99",
        "using-superpowers",
        "brainstorming",
        "GRILL_ME_DECISION_GATE",
        "## 5. Grill Me",
        "NEUTRAL_RECOMMENDATION_GATE",
        "attack",
        "validate-critique",
        "regression-recheck",
        "READ_ONLY",
        "PR_CHECK_EXACT_HEAD",
        "PR_CHECK",
        "exact HEAD",
        "unresolved review thread",
        "BLOCKED_UNVERIFIED",
        "Draft PR",
        "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
    )
    missing = [marker for marker in required if marker not in text]
    assert not missing, f"missing planning/review contract markers: {missing}"


def test_prompt_index_routes_current_contracts() -> None:
    text = INDEX.read_text(encoding="utf-8")

    assert "PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION_v2.md" in text
    assert "TOTAL_PLANNING" in text
    assert "REVIEW" in text
    assert "Grill Me" in text
    assert "PR_CHECK" in text
    assert "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md" in text
    assert "SUPERSEDED_COMPATIBILITY" in text
    assert "최신 Base" in text
