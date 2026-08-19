from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
WORKER_PROMPT = ROOT / "templates" / "prompts" / "BASE_PARTITION_OPTIMIZATION_PROMPT.md"
SCOPE_CHECKER = ROOT / "tools" / "check_base_partition_scope.py"


class SequentialPartCoordinatorContractTests(unittest.TestCase):
    def load_manifest(self) -> dict:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def run_scope(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCOPE_CHECKER), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_one_coordinator_chat_runs_p01_through_p09_sequentially(self) -> None:
        manifest = self.load_manifest()
        coordinator = manifest["coordinator_execution"]
        self.assertEqual("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", coordinator["policy"])
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], coordinator["part_order"])
        self.assertEqual(0, coordinator["required_new_worker_chats"])
        self.assertTrue(coordinator["one_part_checkpoint_at_a_time"])
        self.assertTrue(coordinator["repin_latest_main_between_parts"])
        self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", OPERATING_MODEL.read_text(encoding="utf-8"))
        self.assertIn("P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09", WORKER_PROMPT.read_text(encoding="utf-8"))

    def test_part_ownership_is_semantic_responsibility_not_write_barrier(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual(
            "PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER",
            manifest["ownership_policy"],
        )
        self.assertEqual(
            "ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED",
            manifest["independent_workstream_policy"],
        )
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        self.assertIn("다른 Part라는 이유만으로", text)
        self.assertIn("ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED", text)
        self.assertIn("CROSS_PART_CHANGE", text)

    def test_coordinator_scope_allows_cross_part_and_cp0_with_semantic_attribution(self) -> None:
        result = self.run_scope(
            "--coordinator",
            "--files",
            "skills/managing-design-documents/SKILL.md",
            "skills/designing-vertical-slices/SKILL.md",
            "AGENTS.md",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("SEMANTIC_OWNER:P01", result.stdout)
        self.assertIn("SEMANTIC_OWNER:P04", result.stdout)
        self.assertIn("CONTROL_PLANE_COORDINATOR_WRITE", result.stdout)
        self.assertNotIn("OUT_OF_PARTITION_WRITE", result.stdout)
        self.assertNotIn("CONTROL_PLANE_WRITE_FORBIDDEN", result.stdout)

    def test_cross_part_request_is_only_for_real_coordination_blockers(self) -> None:
        text = WORKER_PROMPT.read_text(encoding="utf-8")
        self.assertIn("CROSS_PART_CHANGE", text)
        self.assertIn("독립 활성 workstream", text)
        self.assertIn("다른 Part라는 이유만으로 수정 보류 금지", text)


if __name__ == "__main__":
    unittest.main()
