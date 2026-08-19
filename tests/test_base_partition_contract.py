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
INTEGRATION_PROMPT = ROOT / "templates" / "prompts" / "BASE_PARTITION_INTEGRATION_PROMPT.md"
SCOPE_CHECKER = ROOT / "tools" / "check_base_partition_scope.py"
LEARNING_SYSTEM = ROOT / "docs" / "operations" / "BASE_PARTITION_LEARNING_SYSTEM.md"

EXPECTED_SKILLS = {
    "managing-project-intake-and-work-contract", "managing-game-project-operating-system",
    "evolving-project-discipline-skills", "managing-design-documents",
    "maintaining-project-context-and-handoff", "analyzing-and-refining-game-concepts",
    "designing-vertical-slices", "producing-game-development-youtube-videos",
    "orchestrating-deepseek-worktrees", "reviewing-and-validating-project-changes",
    "auditing-canonical-reference-freshness", "designing-art-prompts-and-technique-cards",
    "auditing-and-refining-ui-art", "managing-base-change-proposals", "identifying-project-core",
    "establishing-project-core", "running-adversarial-review-and-refinement",
    "refactoring-with-contract-preservation", "simplifying-skill-bodies",
    "pruning-stale-and-nonfunctional-material", "synchronizing-local-and-github-state",
    "maintaining-long-running-task-continuity", "governing-game-user-research-coverage",
    "creating-user-learning-notes", "building-project-visual-dashboards",
    "diagnosing-game-engine-runtime-failures", "governing-legacy-retention-and-archives",
    "evaluating-godot-assets-and-plugins-before-creation", "optimizing-ai-model-and-prompt-costs",
    "developing-and-revising-serial-fiction",
}


class BasePartitionContractTests(unittest.TestCase):
    def load_manifest(self) -> dict:
        self.assertTrue(MANIFEST.exists(), "partition manifest must exist")
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_required_partition_artifacts_exist(self) -> None:
        for path in (MANIFEST, OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT, SCOPE_CHECKER, LEARNING_SYSTEM):
            self.assertTrue(path.exists(), str(path.relative_to(ROOT)))

    def test_manifest_uses_control_plane_plus_nine_functional_parts(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual("BASE_PARTITION_OPERATING_MODEL_V1", manifest["contract_id"])
        self.assertEqual("HYBRID_CONTROL_PLANE_END_TO_END_CAPABILITY_PARTITIONS", manifest["selected_strategy"])
        self.assertEqual(9, len(manifest["parts"]))
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], [p["part_id"] for p in manifest["parts"]])
        self.assertEqual("INTEGRATION_ONLY", manifest["control_plane"]["write_authority"])
        self.assertEqual(10, manifest["integration"]["total_new_gpt_chats_after_task_1"])

    def test_all_active_skills_are_assigned_once(self) -> None:
        manifest = self.load_manifest()
        assignments = [skill for part in manifest["parts"] for skill in part["owned_skill_ids"]]
        self.assertEqual(EXPECTED_SKILLS, set(assignments))
        self.assertEqual(len(assignments), len(set(assignments)))

    def test_part_write_paths_are_unique_and_control_plane_is_not_part_owned(self) -> None:
        manifest = self.load_manifest()
        seen: dict[str, str] = {}
        protected = set(manifest["control_plane"]["protected_write_paths"])
        for part in manifest["parts"]:
            self.assertTrue(part["owned_write_paths"], part["part_id"])
            for path in part["owned_write_paths"]:
                self.assertNotIn(path, protected, f"{part['part_id']} owns protected path {path}")
                self.assertNotIn(path, seen, f"{path} owned by both {seen.get(path)} and {part['part_id']}")
                seen[path] = part["part_id"]

    def test_each_part_has_a_context_pack_and_operational_contract(self) -> None:
        manifest = self.load_manifest()
        for part in manifest["parts"]:
            self.assertTrue((ROOT / part["context_pack"]).exists(), part["part_id"])
            for field in ("purpose", "owned_write_paths", "read_only_dependencies", "important_rules", "owned_skill_ids", "modules", "validation", "acceptance_criteria", "revisit_conditions"):
                self.assertTrue(part[field], f"{part['part_id']} missing {field}")

    def test_parallel_groups_and_integration_order_are_explicit(self) -> None:
        manifest = self.load_manifest()
        groups = manifest["parallel_execution_groups"]
        self.assertGreaterEqual(len(groups), 2)
        flattened = [part_id for group in groups for part_id in group["parts"]]
        self.assertEqual({f"P{i:02d}" for i in range(1, 10)}, set(flattened))
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertTrue(manifest["integration"]["ordered_steps"])

    def test_prompts_require_minimum_five_then_until_clean_and_cross_part_requests(self) -> None:
        worker = WORKER_PROMPT.read_text(encoding="utf-8")
        integration = INTEGRATION_PROMPT.read_text(encoding="utf-8")
        for text in (worker, integration):
            self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", text)
            self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", text)
            self.assertIn("CLEAN_REVIEW_EXIT", text)
            self.assertIn("CROSS_PART_CHANGE_REQUEST", text)
        self.assertIn("OPTIONAL_CODEX_EXECUTOR", worker)
        self.assertIn("사용자 학습형 완료보고", worker)

    def test_operating_model_compares_four_real_strategies_and_records_revisit_conditions(self) -> None:
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        for term in ("A · 디렉터리 계층 분할", "B · 기능/도메인 분할", "C · Control Plane + End-to-End Capability Partition", "D · 동적 의존성 그래프 재클러스터링", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토 조건"):
            self.assertIn(term, text)

    def test_scope_checker_declares_worker_and_integration_modes(self) -> None:
        text = SCOPE_CHECKER.read_text(encoding="utf-8")
        self.assertIn("--part", text)
        self.assertIn("--integration", text)
        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)
        self.assertIn("OUT_OF_PARTITION_WRITE", text)

    def run_scope(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCOPE_CHECKER), *args], cwd=ROOT, text=True, capture_output=True, check=False)

    def test_scope_checker_allows_owned_and_blocks_control_plane_and_other_parts(self) -> None:
        allowed = self.run_scope("--part", "P01", "--files", "skills/managing-design-documents/SKILL.md")
        self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)
        protected = self.run_scope("--part", "P01", "--files", "AGENTS.md")
        self.assertEqual(2, protected.returncode)
        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", protected.stdout)
        outside = self.run_scope("--part", "P01", "--files", "skills/designing-vertical-slices/SKILL.md")
        self.assertEqual(2, outside.returncode)
        self.assertIn("OUT_OF_PARTITION_WRITE", outside.stdout)
        integration = self.run_scope("--integration", "--files", "AGENTS.md", "skills/designing-vertical-slices/SKILL.md")
        self.assertEqual(0, integration.returncode, integration.stdout + integration.stderr)

    def test_manifest_retirement_and_unassigned_path_policy_fail_closed(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual("READ_ONLY_UNLESS_INTEGRATION_ASSIGNMENT_OR_CROSS_PART_CHANGE_REQUEST", manifest["unassigned_path_policy"])
        surfaces = {item["surface"] for item in manifest["retirement_targets"]}
        for surface in ("Google Sheets", "Figma references/workflows", "external HTML visual/dashboard workspace", "custom local visual Tool/Hub", "QA Evidence Studio/local QA tooling"):
            self.assertIn(surface, surfaces)

    def test_each_part_has_learning_log_and_source_discovery(self) -> None:
        manifest = self.load_manifest()
        self.assertTrue(manifest["learning_system"]["required_after_each_part_work"])
        for part in manifest["parts"]:
            learning_log = ROOT / part["learning_log"]
            self.assertTrue(learning_log.exists(), part["part_id"])
            self.assertIn(part["learning_log"], part["owned_write_paths"])
            capture = part["learning_capture"]
            self.assertTrue(capture["required_after_each_work"])
            self.assertIn("NO_NEW_REUSABLE_LESSON", capture["reuse_scope_values"])
            discovery = part["source_discovery"]
            self.assertTrue(discovery["source_domains"])
            self.assertGreaterEqual(len(discovery["discovery_questions"]), 3)

    def test_periodic_source_queue_renders_partition_learning_radar(self) -> None:
        from tools.periodic_source_scan_queue import render_partition_learning_radar
        text = render_partition_learning_radar(self.load_manifest())
        self.assertIn("Partition Learning Radar", text)
        for part_id in [f"P{i:02d}" for i in range(1, 10)]:
            self.assertIn(part_id, text)
        self.assertIn("신규 Source 후보", text)


if __name__ == "__main__":
    unittest.main()
