from pathlib import Path

TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md")

REQUIRED = [
    "BOUNDED_DECISION_EARLY_CANON_SYNC",
    "GOOD_PROMPT_TRANSFORMATION",
    "FIRST_SESSION_REPRESENTATIVE_EXPERIENCE",
    "MULTI_PLATFORM_SHARED_CORE_GATE",
    "FUNCTION_LEVEL_VALIDITY_CLASSIFICATION",
    "PROJECT_ADOPTED_AUTHORING_TEST_QA_AUTHORITY",
    "CI_SUPPLY_CHAIN_GATE",
    "LOCAL_RUNTIME_VALIDATION_NOT_CODEX_LAUNCHER",
    "BASE_PROMOTION_REQUIRES_REUSABLE_EVIDENCE",
]


def test_r54_capabilities_are_operational_not_only_named_in_nonregression_map():
    text = TARGET.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED if marker not in text]
    assert not missing, f"r5.4 capability regression in Work instruction: {missing}"


def test_first_session_contract_contains_observable_player_flow():
    text = TARGET.read_text(encoding="utf-8")
    for marker in ["대표 문제", "대표 행동", "의미 있는 선택", "관찰 가능한 결과", "다음 질문/동기"]:
        assert marker in text


def test_multi_platform_core_names_shared_semantic_owners():
    text = TARGET.read_text(encoding="utf-8")
    for marker in ["core rules", "game data/schema", "save/state meaning", "economy/progression meaning", "content identity", "decision/result semantics"]:
        assert marker in text
