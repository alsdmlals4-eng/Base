from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "templates" / "prompts" / "BASE_PROJECT_INTEGRATED_WORK_INSTRUCTION_v1.md"
INDEX = ROOT / "templates" / "prompts" / "README.md"


def test_general_integrated_prompt_contract() -> None:
    text = PROMPT.read_text(encoding="utf-8")

    required_markers = (
        "[핵심 내용]",
        "ENVIRONMENT_FIRST",
        "PLAN → BUILD → REVIEW",
        "using-superpowers",
        "brainstorming",
        "NEUTRAL_RECOMMENDATION_GATE",
        "attack → validate-critique → decision-report",
        "regression-recheck",
        "BLOCKED_UNVERIFIED",
        "BENCHMARK_BEFORE_INVENTION",
        "EVIDENCE_BEFORE_COMPLETION",
        "Draft PR",
        "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
    )

    missing = [marker for marker in required_markers if marker not in text]
    assert not missing, f"missing integrated prompt contract markers: {missing}"


def test_prompt_index_routes_general_and_vertical_slice_contracts() -> None:
    text = INDEX.read_text(encoding="utf-8")

    assert "BASE_PROJECT_INTEGRATED_WORK_INSTRUCTION_v1.md" in text
    assert "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md" in text
    assert "SUPERSEDED_COMPATIBILITY" in text
    assert "최신 Base" in text
