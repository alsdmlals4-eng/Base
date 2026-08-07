from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = (
    ROOT
    / "templates"
    / "project-operations"
    / ".agents"
    / "skills"
    / "godot-live-editor-operations"
    / "SKILL.md"
)
REFERENCE_PATH = (
    SKILL_PATH.parent
    / "references"
    / "runnable-by-user-project-entrypoint.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class RunnableByUserGodotValidationTests(unittest.TestCase):
    def test_live_editor_skill_routes_user_runnable_entrypoint_validation(self) -> None:
        skill = read(SKILL_PATH)

        for term in (
            "RUNNABLE_BY_USER",
            "references/runnable-by-user-project-entrypoint.md",
            "F5 / Run Project",
            "USER_RUNNABLE_READY",
        ):
            self.assertIn(term, skill)

    def test_reference_requires_real_project_entrypoint_with_bounded_scope(self) -> None:
        self.assertTrue(REFERENCE_PATH.is_file(), str(REFERENCE_PATH))
        reference = read(REFERENCE_PATH)

        for term in (
            "application/run/main_scene",
            "project.godot",
            "MainMenu",
            "App Router",
            "F5 / Run Project",
            "L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE",
            "rollback",
            "Run Current Scene",
            "USER_RUNNABLE_READY",
            "HUMAN_VERIFIED",
        ):
            self.assertIn(term, reference)

    def test_reference_does_not_turn_user_runnable_validation_into_unbounded_scope(self) -> None:
        reference = read(REFERENCE_PATH)

        for term in (
            "무관한 Project Settings",
            "Prototype/Test Scene",
            "사용자가 기존 Main Scene을 유지하라고 명시",
            "필요한 최소 통합 변경",
        ):
            self.assertIn(term, reference)


if __name__ == "__main__":
    unittest.main()
