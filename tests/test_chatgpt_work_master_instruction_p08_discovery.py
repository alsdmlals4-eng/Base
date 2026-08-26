from pathlib import Path

P08 = Path("docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md")
TARGET = "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md"


def test_p08_exposes_work_project_execution_template():
    text = P08.read_text(encoding="utf-8")
    assert TARGET in text
    assert "프로젝트명 + 공용 작업지시문" in text
    assert "Goal이 없으면" in text
    assert "skills/SKILL_REGISTRY.json" in text
