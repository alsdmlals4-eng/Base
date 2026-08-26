from pathlib import Path

TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md")
P08 = Path("docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md")


def test_bcp_037_approved_execution_contract_is_present():
    text = TARGET.read_text(encoding="utf-8")
    for marker in [
        "approval_ref: USER_CHAT_2026-08-26_WORK_NATIVE_PROJECT_INSTRUCTION",
        "PROJECT_PLUS_INSTRUCTION_IS_DEFAULT_SUFFICIENT_INPUT",
        "SEPARATE_GOAL_NOT_REQUIRED_BY_DEFAULT",
        "WORK_SELF_STARTING_FRESH_READ_BOOTSTRAP",
        "CURRENT_SKILL_REGISTRY_COVERAGE_GATE",
        "PRODUCTION_INFORMATION_TEXT_TABLE_FLOW_DB_FIRST",
        "REQUIRED_WORK_REMAINING_0_IS_COMPLETION_CANDIDATE",
    ]:
        assert marker in text


def test_p08_and_execution_contract_use_one_canonical_template_path():
    path = "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md"
    assert path in P08.read_text(encoding="utf-8")
    assert not Path("templates/project-operations/CHATGPT_WORK_PROJECT_MASTER_INSTRUCTION_v4.9.md").exists()
