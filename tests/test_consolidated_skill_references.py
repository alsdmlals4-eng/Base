from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD_SKILL_PATHS = (
    "skills/routing-project-work-by-discipline/SKILL.md",
    "skills/conducting-deep-requirement-interviews/SKILL.md",
    "skills/transforming-requests-into-prompts/SKILL.md",
    "skills/installing-game-project-operating-system/SKILL.md",
    "skills/migrating-existing-game-project-structure/SKILL.md",
    "skills/verifying-game-project-operating-system/SKILL.md",
    "skills/writing-game-design-documents/SKILL.md",
    "skills/publishing-discipline-bibles/SKILL.md",
    "skills/promoting-project-knowledge/SKILL.md",
    "skills/reviewing-and-implementing-base-change-proposals/SKILL.md",
)
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py"}


class ConsolidatedSkillReferenceTests(unittest.TestCase):
    def test_active_entrypoints_and_templates_have_no_deleted_skill_paths(self) -> None:
        candidates = [
            ROOT / "AGENTS.md",
            ROOT / "START_HERE.md",
            ROOT / "README.md",
            ROOT / "docs/OPERATING_MODEL.md",
            ROOT / "docs/DOCUMENTATION_MAP.md",
            ROOT / "docs/AI_SHARED_WORK_RULES.md",
            ROOT / "docs/AI_WORKFLOW_RULES.md",
            ROOT / "docs/AI_SKILL_ADOPTION_GUIDE.md",
            ROOT / "docs/MVP_WORKFLOW_CHECKLIST.md",
        ]
        candidates += [
            path for path in (ROOT / "templates").rglob("*")
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
        ]
        stale: list[str] = []
        for path in sorted(set(candidates)):
            text = path.read_text(encoding="utf-8", errors="replace")
            for old_path in OLD_SKILL_PATHS:
                if old_path in text:
                    stale.append(f"{path.relative_to(ROOT)} -> {old_path}")
        self.assertEqual(stale, [], "Deleted skill paths remain in active entrypoints/templates:\n" + "\n".join(stale))

    def test_new_skill_paths_are_present_in_project_templates(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in (ROOT / "templates").rglob("*")
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
        )
        for skill_id in (
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
            "managing-base-change-proposals",
        ):
            self.assertIn(skill_id, combined)


if __name__ == "__main__":
    unittest.main()
