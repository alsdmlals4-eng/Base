#!/usr/bin/env python3
"""Remove the active v9.4 Skill from the removed-Skill alias fixture."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tests/test_game_project_operating_system_structure.py"
text = TARGET.read_text(encoding="utf-8")
needle = '            "optimizing-ai-model-and-prompt-costs",\n'
if needle not in text:
    raise RuntimeError("active v9.4 Skill alias fixture entry not found")
text = text.replace(needle, "", 1)
TARGET.write_text(text, encoding="utf-8", newline="\n")
print("Removed active v9.4 Skill from legacy alias fixture")
