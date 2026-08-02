from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "templates" / "prompts" / "PROJECT_TOTAL_PLANNING_AUDIT_AND_IMPROVEMENT_WORK_INSTRUCTION_v3.md"
INDEX = ROOT / "templates" / "prompts" / "README.md"


def test_total_planning_is_whole_project_audit_and_improvement_contract() -> None:
    text = PROMPT.read_text(encoding="utf-8")

    required = (
        "[총기획]",
        "[검수]",
        "[핵심 내용]",
        "WHOLE_PROJECT_AUDIT_FIRST",
        "PREVIOUS_CONTRACT_PRESERVATION_GATE",
        "previous_total_planning_instruction",
        "SAFE_PLANNING_FIXES",
        "AUTO_FIX_ELIGIBLE",
        "RESEARCH_OR_TEST_REQUIRED",
        "STRENGTH_PRESERVATION_MAP",
        "RESPONSIBILITY_SOURCE_MAP",
        "PROJECT_HEALTH_MATRIX",
        "PLANNING_GAP",
        "PLANNING_CONFLICT",
        "CANON_IMPLEMENTATION_GAP",
        "UNDERDESIGN",
        "OVERDESIGN",
        "IMPROVEMENT_BACKLOG",
        "KEEP / INTEGRATE / REVISE / CREATE / HOLD / REMOVE_CANDIDATE",
        "DEFINITION_OF_READY",
        "DOCUMENTATION_GATE",
        "COMPLETION_GATE",
        "PDF_AND_DERIVATIVE_AUDIT",
        "SKILL_AND_WORKFLOW_AUDIT",
        "COLD_START_VALIDATION",
        "PROJECT_LEARNING_AND_BASE_FEEDBACK",
        "Grill Me",
        "attack",
        "validate-critique",
        "regression-recheck",
        "PR_CHECK_EXACT_HEAD",
        "unresolved review thread",
        "PLANNING_AND_REVIEW_COMPLETE_GATE",
        "CODEX_IMPLEMENTATION_HANDOFF",
        "CODEX_DEFINITION_OF_READY",
        "CODEX_EXECUTION_PACKET",
        "COMPLETE_VERTICAL_SLICE_TARGET",
        "VERTICAL_SLICE_COMPLETENESS_MATRIX",
        "ALL_APPROVED_PLANNING_IMPLEMENTED_OR_EXPLICITLY_EXCLUDED",
        "DEMO_READY_GATE",
        "NO_PAPER_ONLY_FEATURES",
        "IMMEDIATE_CANONICAL_DECISION_SYNC",
        "NO_DEFERRED_DECISION_SYNC",
        "DECISION_SYNC_LEDGER",
        "GITHUB_CANONICAL_LOCATION",
        "GOOGLE_SHEET_LOCATION",
        "SAME_DECISION_ID",
        "SYNCED",
        "PARTIAL_SYNC_BLOCKED",
        "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
    )
    missing = [marker for marker in required if marker not in text]
    assert not missing, f"missing whole-project audit/improvement markers: {missing}"


def test_total_planning_lifecycle_is_review_first_and_improvement_closed_loop() -> None:
    text = PROMPT.read_text(encoding="utf-8")
    section = text.split("## 6. 총기획 전체 생명주기", 1)[1].split("## 7.", 1)[0]

    expected_order = (
        "WHOLE_PROJECT_BASELINE_RECOVERY",
        "STRENGTH_PRESERVATION_MAP",
        "PROJECT_INVENTORY_AND_COVERAGE_AUDIT",
        "PLANNING_GAP_AND_CONFLICT_DISCOVERY",
        "ADVERSARIAL_ATTACK",
        "VALIDATE_CRITIQUE",
        "IMPROVEMENT_OPTION_DESIGN",
        "GRILL_ME_ONLY_FOR_DECISION_GAPS",
        "APPROVED_IMPROVEMENT_BUILD",
        "CANONICAL_AND_CONSUMER_UPDATE",
        "COLD_START_VALIDATION",
        "REGRESSION_RECHECK",
        "PR_CHECK_EXACT_HEAD",
        "DECISION_REPORT",
    )
    positions = [section.index(marker) for marker in expected_order]
    assert positions == sorted(positions), "total planning lifecycle must remain review-first"


def test_prompt_index_routes_v3_and_preserves_specialized_vertical_slice_prompt() -> None:
    text = INDEX.read_text(encoding="utf-8")

    assert "PROJECT_TOTAL_PLANNING_AUDIT_AND_IMPROVEMENT_WORK_INSTRUCTION_v3.md" in text
    assert "WHOLE_PROJECT_AUDIT_FIRST" in text
    assert "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md" in text
    assert "SUPERSEDED_COMPATIBILITY" in text
    assert "최신 Base" in text


def test_codex_handoff_requires_completed_planning_and_review() -> None:
    text = PROMPT.read_text(encoding="utf-8")
    section = text.split("## 6. 총기획 전체 생명주기", 1)[1].split("## 7.", 1)[0]

    expected_order = (
        "PLANNING_AND_REVIEW_COMPLETE_GATE",
        "IMMEDIATE_CANONICAL_DECISION_SYNC",
        "CODEX_IMPLEMENTATION_HANDOFF",
        "COMPLETE_VERTICAL_SLICE_TARGET",
        "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
    )
    positions = [section.index(marker) for marker in expected_order]
    assert positions == sorted(positions), "Codex handoff must follow completed planning, review, and decision sync"


def test_vertical_slice_is_complete_demo_not_partial_prototype() -> None:
    text = PROMPT.read_text(encoding="utf-8")

    required = (
        "완성형 데모",
        "승인된 전체 기획",
        "대표 콘텐츠",
        "저장·불러오기",
        "온보딩",
        "실패·복구",
        "접근성",
        "성능",
        "패키징",
        "미구현",
    )
    missing = [marker for marker in required if marker not in text]
    assert not missing, f"missing complete vertical-slice acceptance markers: {missing}"


def test_decision_sync_is_immediate_and_cross_surface() -> None:
    text = PROMPT.read_text(encoding="utf-8")

    required = (
        "동일 Decision ID",
        "GitHub 권위 문서",
        "계획 데이터",
        "연결된 Google Sheet",
        "변경 경로·섹션·행",
        "commit SHA",
        "재조회",
        "다음 주요 기획·구현 단계로 진행하지 않는다",
    )
    missing = [marker for marker in required if marker not in text]
    assert not missing, f"missing immediate decision-sync markers: {missing}"
