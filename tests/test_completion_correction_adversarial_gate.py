from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class CompletionCorrectionAdversarialGateTests(unittest.TestCase):
    def test_base_and_project_completion_requires_remaining_work_recalculation(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        project_os = read("skills/managing-game-project-operating-system/SKILL.md")

        for text in (operating, adversarial, project_os):
            for token in (
                "REMAINING_WORK_COMPLETION_GATE",
                "REMAINING_WORK_RECALCULATION_REQUIRED",
                "IMPLEMENTATION_CORRECTION_RESCAN",
            ):
                with self.subTest(token=token):
                    self.assertIn(token, text)

    def test_new_correction_findings_reopen_work_before_completion(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        operating = read("docs/OPERATING_MODEL.md")

        for text in (adversarial, operating):
            for token in (
                "NEW_FINDING_REOPENS_REMAINING_WORK",
                "FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK",
                "POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED",
                "CLEAN_REVIEW_EXIT",
            ):
                with self.subTest(token=token):
                    self.assertIn(token, text)

    def test_completion_review_reuses_one_final_post_change_monitor_loop(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        project_os = read("skills/managing-game-project-operating-system/SKILL.md")

        for text in (operating, adversarial, project_os):
            self.assertIn("POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED", text)
            self.assertIn("POST_CHANGE_MONITOR_LOOP", text)

        self.assertIn("두 번째 독립 review cycle", operating)
        self.assertIn("두 번째 5회 루프가 아니다", adversarial)
        self.assertIn("별도 두 번째 검토 루프", project_os)

    def test_full_completion_does_not_hide_blocked_or_deferred_work(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        project_os = read("skills/managing-game-project-operating-system/SKILL.md")
        for text in (adversarial, project_os):
            self.assertIn("BLOCKED_UNVERIFIED", text)
            self.assertIn("DEFER", text)
            self.assertIn("전체 완료", text)


if __name__ == "__main__":
    unittest.main()
