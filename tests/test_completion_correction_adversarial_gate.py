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

    def test_completion_gate_reaches_active_execution_consumers(self) -> None:
        consumers = {
            "README": read("README.md"),
            "AGENTS": read("AGENTS.md"),
            "long_horizon": read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"),
            "routing": read("docs/WORK_MODE_AND_SKILL_ROUTING.md"),
            "intake": read("skills/managing-project-intake-and-work-contract/SKILL.md"),
            "continuous": read(
                "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
            ),
            "validation": read("skills/reviewing-and-validating-project-changes/SKILL.md"),
            "project_agents": read("templates/AGENTS.project.md"),
            "project_workflow": read("templates/project-operations/AI_WORKFLOW.md"),
        }

        for name, text in consumers.items():
            with self.subTest(consumer=name):
                self.assertIn("REMAINING_WORK_COMPLETION_GATE", text)
                self.assertIn("IMPLEMENTATION_CORRECTION_RESCAN", text)
                self.assertIn("POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED", text)

    def test_continuous_work_recalculates_then_rescans_before_final_review(self) -> None:
        continuous = read(
            "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
        )
        recalculation = continuous.index("REMAINING_WORK_RECALCULATION_REQUIRED")
        rescan = continuous.index("IMPLEMENTATION_CORRECTION_RESCAN")
        final_review = continuous.index("POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED")
        clean_exit = continuous.index("CLEAN_REVIEW_EXIT")
        self.assertLess(recalculation, rescan)
        self.assertLess(rescan, final_review)
        self.assertLess(final_review, clean_exit)

    def test_project_active_context_tracks_completion_candidate_evidence(self) -> None:
        active_context = read("templates/project-operations/ACTIVE_CONTEXT.md")
        for field in (
            "remaining_work_recalculation_status",
            "implementation_correction_rescan_status",
            "completion_adversarial_review_status",
            "clean_review_exit_status",
        ):
            with self.subTest(field=field):
                self.assertIn(field, active_context)

    def test_full_completion_does_not_hide_blocked_or_deferred_work(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        project_os = read("skills/managing-game-project-operating-system/SKILL.md")
        for text in (adversarial, project_os):
            self.assertIn("BLOCKED_UNVERIFIED", text)
            self.assertIn("DEFER", text)
            self.assertIn("전체 완료", text)


if __name__ == "__main__":
    unittest.main()
