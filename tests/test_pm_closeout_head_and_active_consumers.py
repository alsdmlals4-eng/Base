from __future__ import annotations

import inspect
from pathlib import Path
import unittest

from tests.test_project_work_tracking import SOURCE, done_receipt
from tools.validate_work_contract_receipt import validate_execution_receipt


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CONSUMERS = (
    "docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md",
    "skills/managing-project-intake-and-work-contract/SKILL.md",
    "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md",
    "templates/planning/EXECUTION_SEQUENCE_PLAN.md",
)
CLOSEOUT_CONSUMERS = (
    "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
    "templates/project-operations/AI_WORKFLOW.md",
    "templates/project-operations/PROJECT_START_HERE.md",
    "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md",
    "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
    "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md",
    "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
)
CANONICAL_CLOSEOUT_OWNERS = (
    "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md",
    "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
)


class PMCloseoutHeadAndActiveConsumerTests(unittest.TestCase):
    def test_closeout_api_accepts_trusted_expected_head(self) -> None:
        self.assertIn("expected_head_sha", inspect.signature(validate_execution_receipt).parameters)

    def test_closeout_requires_trusted_expected_head(self) -> None:
        errors = validate_execution_receipt(
            done_receipt(),
            phase="closeout",
            expected_source_sha=SOURCE,
        )
        self.assertIn("expected_head_sha", "\n".join(errors))

    def test_closeout_rejects_receipt_verified_on_another_head(self) -> None:
        errors = validate_execution_receipt(
            done_receipt(),
            phase="closeout",
            expected_source_sha=SOURCE,
            expected_head_sha="b" * 40,
        )
        self.assertIn("verified_head_sha", "\n".join(errors))

    def test_closeout_accepts_matching_trusted_verification_target(self) -> None:
        self.assertEqual(
            [],
            validate_execution_receipt(
                done_receipt(),
                phase="closeout",
                expected_source_sha=SOURCE,
                expected_head_sha="a" * 40,
            ),
        )

    def test_all_active_execution_consumers_use_root_pm_and_trusted_start_command(self) -> None:
        for path in ACTIVE_CONSUMERS:
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("PROJECT_WORK_KANBAN_CHECKLIST", text)
                self.assertIn("project_work_kanban", text)
                commands = [
                    line
                    for line in text.splitlines()
                    if "validate_work_contract_receipt.py" in line and "--receipt" in line
                ]
                self.assertTrue(commands, f"{path} must contain an executable receipt command")
                self.assertTrue(
                    any(
                        all(
                            token in line
                            for token in (
                                "--phase start",
                                "--expected-source-sha",
                                "--render-markdown",
                            )
                        )
                        for line in commands
                    ),
                    f"{path} must use the trusted PM start command",
                )

    def test_active_router_has_no_history_only_bare_receipt_gate(self) -> None:
        path = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
        commands = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if "validate_work_contract_receipt.py" in line and "--receipt" in line
        ]
        self.assertTrue(commands)
        self.assertTrue(
            all("--phase" in line and "--expected-source-sha" in line for line in commands),
            f"all active router receipt commands must use the execution gate: {commands}",
        )

    def test_closeout_docs_require_the_trusted_verification_target(self) -> None:
        for path in CANONICAL_CLOSEOUT_OWNERS:
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("--expected-head-sha", text)
                self.assertIn("TRUSTED_VERIFICATION_TARGET_HEAD", text)

    def test_closeout_docs_do_not_require_a_receipt_to_hash_itself(self) -> None:
        for path in CANONICAL_CLOSEOUT_OWNERS:
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("VERIFIED_SUBJECT_HEAD", text)
                self.assertIn("RECEIPT_ONLY_TAIL_COMMIT", text)
                self.assertIn("FINAL_PR_HEAD_CI_REVIEW_REQUIRED", text)
                self.assertIn("제품·정본·consumer·검증 evidence", text)

    def test_every_real_closeout_consumer_routes_to_the_canonical_subject_contract(self) -> None:
        for path in (*ACTIVE_CONSUMERS, *CLOSEOUT_CONSUMERS):
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("--phase closeout", text)
                self.assertIn("--expected-head-sha", text)
                self.assertTrue(
                    "TRUSTED_VERIFICATION_TARGET_HEAD" in text
                    or "PROJECT_WORK_ITEM_CHECKLIST.md" in text
                    or "WORK_PROJECT_START_CANON_CHECKLIST.md" in text,
                    f"{path} must route closeout to the canonical trusted-subject owner",
                )

    def test_canonical_start_resume_allows_a_review_only_active_task(self) -> None:
        text = (ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("active_work_item_ref", text)
        self.assertIn("IN_PROGRESS", text)
        self.assertIn("VERIFY_REVIEW", text)
        self.assertIn("각 상태의 WIP는 최대 1개", text)
        self.assertNotIn("시작/재개에는 IN_PROGRESS 1개", text)

    def test_merge_and_postmerge_work_precedes_final_closeout(self) -> None:
        text = (ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md").read_text(
            encoding="utf-8"
        )
        section = text.split("### 실행·재개·마감", 1)[1].split(
            "`TRUSTED_VERIFICATION_TARGET_HEAD`", 1
        )[0]
        for token in (
            "PREMERGE_CANDIDATE_NOT_CLOSEOUT",
            "NORMAL_MERGE_AND_POSTMERGE_READBACK",
            "POSTMERGE_CLOSEOUT_REQUIRED_WHEN_IN_DENOMINATOR",
        ):
            self.assertIn(token, section)
        self.assertLess(
            section.index("NORMAL_MERGE_AND_POSTMERGE_READBACK"),
            section.index("POSTMERGE_CLOSEOUT_REQUIRED_WHEN_IN_DENOMINATOR"),
        )
        self.assertLess(
            section.index("POSTMERGE_CLOSEOUT_REQUIRED_WHEN_IN_DENOMINATOR"),
            section.index("--phase closeout"),
        )


if __name__ == "__main__":
    unittest.main()
