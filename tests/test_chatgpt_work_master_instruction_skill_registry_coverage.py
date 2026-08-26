import json
from pathlib import Path

TARGET = Path("templates/project-operations/CHATGPT_WORK_PROJECT_MASTER_INSTRUCTION_v4.9.md")
REGISTRY = Path("skills/SKILL_REGISTRY.json")


def test_work_instruction_mentions_every_current_active_skill_without_loading_all_by_default():
    text = TARGET.read_text(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    excluded = set(registry.get("routing_policy", {}).get("exclude_statuses", []))
    active_ids = [
        skill["skill_id"]
        for skill in registry["skills"]
        if skill.get("status") not in excluded
    ]
    missing = [skill_id for skill_id in active_ids if skill_id not in text]
    assert not missing, f"current Registry skills missing from Work routing coverage: {missing}"
    assert "DO_NOT_LOAD_ALL_SKILLS" in text
    assert "TRIGGER_MATCHED_PROGRESSIVE_ROUTING" in text
    assert "current Registry" in text
