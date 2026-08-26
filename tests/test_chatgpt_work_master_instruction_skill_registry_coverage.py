import json
from pathlib import Path

TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md")
REGISTRY = Path("skills/SKILL_REGISTRY.json")
GENERATED = Path("docs/generated/BASE_ACTIVE_SKILLS.md")


def test_work_instruction_delegates_skill_inventory_to_current_registry():
    text = TARGET.read_text(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["routing_policy"]["automatic_selection"] is True
    assert registry["routing_policy"]["require_trigger_match"] is True
    assert "CURRENT_REGISTRY_IS_ROUTING_AUTHORITY" in text
    assert "skills/SKILL_REGISTRY.json" in text
    assert "docs/generated/BASE_ACTIVE_SKILLS.md" in text
    assert "DO_NOT_LOAD_ALL_SKILLS" in text
    assert "TRIGGER_MATCHED_PROGRESSIVE_ROUTING" in text


def test_generated_active_skill_map_exists_for_inventory_readback():
    assert GENERATED.exists()
    generated = GENERATED.read_text(encoding="utf-8")
    assert "Base Skill Map (Current Active Skills)" in generated
    assert "SKILL_REGISTRY.json" in generated


def test_instruction_requires_missing_triggered_skill_to_fail_closed():
    text = TARGET.read_text(encoding="utf-8")
    assert "missing_triggered_skill" in text
    assert "PASS | FAIL_BLOCKED" in text
