from pathlib import Path

TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_MASTER_INSTRUCTION_v4.9.md")

REQUIRED_LITERALS = [
    "WORK_EXECUTION_SURFACE_NOT_CANON",
    "DEFAULT_MEMORY_DISCOVERY_HINT_ONLY",
    "FRESH_READ_PROJECT_BOOTSTRAP",
    "DERIVE_CURRENT_GOAL_FROM_CANON_WHEN_OMITTED",
    "BASE_OWNER_PROGRESSIVE_LOAD",
    "SKILL_COVERAGE_AUDIT",
    "CURRENT_REGISTRY_IS_ROUTING_AUTHORITY",
    "REUSE_FIRST_PREFLIGHT_REQUIRED",
    "CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY",
    "MINIMUM_VIABLE_ALTERNATIVES: 3",
    "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
    "FULL_LOOP_COUNT_MINIMUM: 5",
    "IMPLEMENTATION_REALITY_GATE",
    "ACTUAL_CONSUMER_REQUIRED",
    "TEXT_TABLE_FLOW_DB_FIRST",
    "VISUAL_ASSET_COVERAGE",
    "ART_STYLE_LOCK",
    "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER",
    "ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE",
    "ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON",
    "GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER",
    "STABLE_ENGINE_BASELINE",
    "NO_AUTOMATIC_LATEST_FOLLOW",
    "OPEN_PR_READ_ONLY_BY_DEFAULT",
    "CURRENT_REQUIRED_CHECK_DISCOVERY",
    "INCIDENT_SOLUTION_LESSON_LOOP",
    "REQUIRED_WORK_REMAINING",
    "COMPLETION_CANDIDATE",
    "PROJECT_NAME + SHARED_INSTRUCTION",
]


def read_target() -> str:
    assert TARGET.exists(), f"missing Work master instruction: {TARGET}"
    return TARGET.read_text(encoding="utf-8")


def test_work_master_instruction_preserves_required_operating_contracts():
    text = read_target()
    missing = [item for item in REQUIRED_LITERALS if item not in text]
    assert not missing, f"missing required Work contract literals: {missing}"


def test_work_master_instruction_uses_dynamic_skill_routing_without_forcing_all_skills():
    text = read_target()
    assert "DO_NOT_LOAD_ALL_SKILLS" in text
    assert "TRIGGER_MATCHED_PROGRESSIVE_ROUTING" in text
    assert "skills/SKILL_REGISTRY.json" in text
    assert "docs/generated/BASE_ACTIVE_SKILLS.md" in text


def test_memory_and_authority_order_prevent_cross_project_contamination():
    text = read_target()
    authority_markers = [
        "1. 사용자 최신 지시",
        "2. 현재 프로젝트 AGENTS.md",
        "3. Active Context / 승인 결정 / 작업 계약",
        "4. 해당 분야 Notion·GitHub 정본",
        "5. 실제 code/data/test/runtime evidence",
        "6. 프로젝트가 채택한 Base 규칙",
        "7. Base 공용 원본",
        "8. 외부 benchmark",
        "9. 다른 프로젝트 사례",
        "10. Memory / 과거 채팅",
    ]
    missing = [item for item in authority_markers if item not in text]
    assert not missing, f"authority order drifted: {missing}"
    assert "Memory → candidate discovery → actual source readback → ADOPT / ADAPT / REFERENCE_ONLY / REJECT" in text


def test_work_stays_noncanonical_and_codex_stays_product_implementation_owner():
    text = read_target()
    assert "Work 대화/중간 산출물은 정본이 아니다" in text
    assert "Work가 실제 게임 product code를 누적 구현하지 않는다" in text
    assert "Codex는 이미지를 생성하거나 생성형 편집하지 않는다" in text


def test_goal_is_optional_and_frontier_is_derived_from_current_canon():
    text = read_target()
    assert "별도 Goal은 필수가 아니다" in text
    assert "unfinished frontier" in text
    assert "next highest-value playable slice" in text
    assert "사용자에게 Goal을 다시 묻지 않는다" in text
