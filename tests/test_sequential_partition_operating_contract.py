from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
WORKER_PROMPT = ROOT / "templates" / "prompts" / "BASE_PARTITION_OPTIMIZATION_PROMPT.md"
ADVERSARIAL = ROOT / "skills" / "running-adversarial-review-and-refinement" / "SKILL.md"


class SequentialPartitionOperatingContractTests(unittest.TestCase):
    def manifest(self) -> dict:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_one_coordinator_chat_runs_p01_to_p09_sequentially(self) -> None:
        manifest = self.manifest()
        execution = manifest["sequential_execution"]
        self.assertEqual("ONE_COORDINATOR_CHAT_SEQUENTIAL_P01_TO_P09", execution["policy"])
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], execution["order"])
        self.assertEqual("CURRENT_COORDINATOR_CHAT", execution["coordinator_chat"])
        self.assertTrue(execution["repin_latest_main_between_part_merges"])
        for path in (OPERATING_MODEL, WORKER_PROMPT):
            text = path.read_text(encoding="utf-8")
            self.assertIn("ONE_COORDINATOR_CHAT_SEQUENTIAL_P01_TO_P09", text)
            self.assertNotIn("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", text)

    def test_part_boundary_is_accountability_not_fix_prohibition(self) -> None:
        manifest = self.manifest()
        repair = manifest["cross_part_repair"]
        self.assertEqual("PART_BOUNDARY_IS_ANALYSIS_AND_ACCOUNTABILITY_NOT_A_FIX_PROHIBITION", repair["policy"])
        self.assertTrue(repair["coordinator_may_fix_validated_cross_part_findings"])
        self.assertEqual("DO_NOT_MUTATE", repair["independent_active_workstream"])
        text = OPERATING_MODEL.read_text(encoding="utf-8") + WORKER_PROMPT.read_text(encoding="utf-8")
        self.assertIn("PART_BOUNDARY_IS_ANALYSIS_AND_ACCOUNTABILITY_NOT_A_FIX_PROHIBITION", text)
        self.assertIn("open/draft/ready", text)

    def test_counted_adversarial_loop_is_not_a_review_lens(self) -> None:
        text = ADVERSARIAL.read_text(encoding="utf-8")
        self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
        self.assertIn("관점", text)
        self.assertIn("5개의 관점", text)
        self.assertIn("전체 승인 범위", text)
        self.assertIn("MINIMUM_VIABLE_ALTERNATIVES: 3", text)
        self.assertIn("BETTER_ALTERNATIVE_SEARCH", text)
        self.assertIn("LONG_TERM_PLAN_FIT_RECHECK", text)
        self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", text)

    def test_human_facing_main_view_contract_is_explicit(self) -> None:
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        self.assertIn("NOTION_MAIN_VIEW_MUST_BE_HUMAN_COMPLETE", text)
        self.assertIn("PROJECT_HOME_MUST_BE_HUMAN_COMPLETE", text)
        self.assertIn("추가 이동", text)


if __name__ == "__main__":
    unittest.main()
