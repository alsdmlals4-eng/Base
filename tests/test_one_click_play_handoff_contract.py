from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OneClickPlayHandoffContractTests(unittest.TestCase):
    def test_existing_responsibility_sources_define_one_click_play_handoff(self) -> None:
        sources = {
            "sync": ROOT / "skills/synchronizing-local-and-github-state/SKILL.md",
            "handoff": ROOT / "skills/maintaining-project-context-and-handoff/SKILL.md",
            "slice": ROOT / "skills/designing-vertical-slices/SKILL.md",
            "review": ROOT / "skills/reviewing-and-validating-project-changes/SKILL.md",
            "workflow": ROOT / "templates/project-operations/AI_WORKFLOW.md",
        }
        texts = {name: path.read_text(encoding="utf-8") for name, path in sources.items()}

        for required in (
            "Fetch origin",
            "Pull origin",
            "로컬 HEAD",
        ):
            self.assertIn(required, texts["sync"])

        for required in (
            "repository",
            "branch",
            "commit SHA",
            "Project Play",
            "기대 첫 화면",
        ):
            self.assertIn(required, texts["handoff"])

        for required in (
            "Project Play",
            "별도 Scene 선택",
            "성공·실패·복귀",
        ):
            self.assertIn(required, texts["slice"])

        for required in (
            "사용자의 기본 실행 시작점",
            "FAIL · RETEST_REQUIRED",
            "별도 Scene 선택",
        ):
            self.assertIn(required, texts["review"])

        for required in (
            "Fetch origin → Pull origin",
            "Project Play",
            "별도 Scene 선택·편집기 수동 설정 없이",
        ):
            self.assertIn(required, texts["workflow"])


if __name__ == "__main__":
    unittest.main()
