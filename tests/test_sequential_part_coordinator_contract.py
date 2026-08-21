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
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        self.assertIn("다른 Part라는 이유만으로", text)
        self.assertIn("CROSS_PART_CHANGE", text)

    def test_open_prs_are_read_only_without_owner_inference(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual("OPEN_PR_READ_ONLY_BY_DEFAULT", manifest["open_pr_policy"])
        detection = manifest["active_workstream_detection"]
        self.assertTrue(detection["open_pr_state_is_sufficient_for_read_only"])
        self.assertTrue(detection["mutation_requires_explicit_named_authorization"])
        self.assertEqual("MERGED_MAIN_ONLY", detection["default_follow_up_target"])
        self.assertEqual(
            [
                "READ_ONLY_REFERENCE",
                "SUPERSEDED_BY_MERGED_MAIN",
                "BLOCKED_EXTERNAL",
            ],
            detection["open_pr_classifications"],
        )
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        self.assertIn("OPEN_PR_READ_ONLY_BY_DEFAULT", text)
        self.assertIn("open/draft/ready", text)
        self.assertIn("PR 번호와 허용 동작", text)

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

    def test_manifest_uses_reference_clusters_not_parallel_execution_groups(self) -> None:
        manifest = self.load_manifest()
        self.assertNotIn("parallel_execution_groups", manifest)
        clusters = manifest["responsibility_clusters"]
        self.assertEqual(3, len(clusters))
        self.assertEqual({"G1_FOUNDATION", "G2_GAME_PRODUCTION", "G3_DELIVERY_AI_CONTENT"}, {row["cluster_id"] for row in clusters})
        self.assertTrue(all(row["purpose"] == "REFERENCE_AND_LEARNING_CLUSTER_ONLY" for row in clusters))

    def test_quality_templates_have_semantic_owners_instead_of_broad_p03_glob(self) -> None:
        manifest = self.load_manifest()
        p03 = next(p for p in manifest["parts"] if p["part_id"] == "P03")
        self.assertNotIn("templates/quality/**", p03["owned_write_paths"])
        expected = {
            "templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md": "P02",
            "templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md": "P05",
            "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md": "P03",
            "templates/quality/PROJECT_CHANGE_VALIDATION.md": "P07",
            "templates/quality/REVIEW_EVIDENCE_RECORD.json": "P07",
        }
        for path, owner in expected.items():
            result = self.run_scope("--coordinator", "--files", path)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(f"SEMANTIC_OWNER:{owner}", result.stdout)

    def test_control_plane_protocol_keeps_open_prs_read_only(self) -> None:
        manifest = self.load_manifest()
        protocol = "\n".join(manifest["control_plane"]["change_protocol"])
        self.assertIn("CROSS_PART_CHANGE", protocol)
        self.assertIn("not a write barrier", protocol)
        self.assertIn("open, draft, and ready PRs remain read-only", protocol)
        self.assertIn("Follow-up changes start from latest completed main", protocol)

    def test_cross_part_request_is_only_for_real_coordination_blockers(self) -> None:
        text = WORKER_PROMPT.read_text(encoding="utf-8")
        self.assertIn("CROSS_PART_CHANGE", text)
        self.assertIn("OPEN_PR_READ_ONLY_BY_DEFAULT", text)
        self.assertIn("다른 Part라는 이유만으로 수정 보류 금지", text)


if __name__ == "__main__":
    unittest.main()
