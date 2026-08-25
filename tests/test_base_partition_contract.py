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
SKILL_REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class BasePartitionContractTests(unittest.TestCase):
    def load_manifest(self) -> dict:
        self.assertTrue(MANIFEST.exists(), "partition manifest must exist")
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def active_skill_ids(self) -> set[str]:
        payload = json.loads(SKILL_REGISTRY.read_text(encoding="utf-8"))
        return {
            row["skill_id"]
            for row in payload["skills"]
            if row.get("status") == "ACTIVE"
        }

    def test_required_partition_artifacts_exist(self) -> None:
        for path in (MANIFEST, OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT, SCOPE_CHECKER, LEARNING_SYSTEM):
            self.assertTrue(path.exists(), str(path.relative_to(ROOT)))

    def test_manifest_uses_control_plane_plus_nine_functional_parts(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual("BASE_PARTITION_OPERATING_MODEL_V1", manifest["contract_id"])
        self.assertEqual("ONE_BASE_STABLE_PARTITIONS_SEQUENTIAL_COORDINATOR", manifest["selected_strategy"])
        self.assertEqual(9, len(manifest["parts"]))
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], [p["part_id"] for p in manifest["parts"]])
        self.assertEqual("COORDINATOR_OR_INTEGRATION", manifest["control_plane"]["write_authority"])
        integration = manifest["integration"]
        self.assertEqual(0, integration["worker_chat_count"])
        self.assertEqual(0, integration["total_new_gpt_chats_after_task_1"])
        self.assertEqual(0, integration["new_integration_chat_count"])
        self.assertEqual("CURRENT_COORDINATOR_CHAT", integration["integration_chat"])
        self.assertEqual("CURRENT_COORDINATOR_CHAT", integration["final_confirmation_chat"])

    def test_all_active_skills_are_assigned_once_from_registry_authority(self) -> None:
        manifest = self.load_manifest()
        assignments = [skill for part in manifest["parts"] for skill in part["owned_skill_ids"]]
        self.assertEqual(self.active_skill_ids(), set(assignments))
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

    def test_manifest_has_no_semantic_cross_part_overlap_on_tracked_files(self) -> None:
        result = self.run_scope("--validate-manifest")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("semantic path overlap", result.stdout)

    def test_hybrid_partition_mode_keeps_one_unified_base(self) -> None:
        manifest = self.load_manifest()
        mode = manifest["operating_mode"]
        self.assertEqual("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", mode["policy"])
        self.assertEqual("UNIFIED_BASE", mode["daily_default"])
        self.assertTrue(mode["activate_only_relevant_parts"])
        self.assertFalse(mode["run_all_parts_for_every_task"])
        self.assertTrue(mode["integration_returns_to_one_base"])
        for path in (OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT):
            text = path.read_text(encoding="utf-8")
            self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", text)

    def test_single_coordinator_preserves_unique_notion_part_pages_and_semantic_attribution(self) -> None:
        manifest = self.load_manifest()
        isolation = manifest["collaboration_isolation"]
        self.assertEqual("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", isolation["worker_model"])
        self.assertTrue(isolation["github"]["one_branch_per_part"])
        self.assertTrue(isolation["github"]["one_pr_per_part"])
        self.assertEqual("COORDINATOR", isolation["notion"]["hub_write"])
        self.assertEqual("COORDINATOR", isolation["notion"]["shared_visual_write"])
        urls = []
        branches = []
        for part in manifest["parts"]:
            self.assertEqual("CURRENT_COORDINATOR_CHAT_SEQUENTIAL_CHECKPOINT", part["chat_ownership"])
            self.assertEqual("COORDINATOR_CURRENT_OR_AFFECTED_PART", part["notion_write_authority"])
            urls.append(part["notion_page_url"])
            branches.append(part["branch_template"])
        self.assertEqual(9, len(set(urls)))
        self.assertEqual(9, len(set(branches)))
        worker = WORKER_PROMPT.read_text(encoding="utf-8")
        self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", worker)
        self.assertIn("PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER", worker)
        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", INTEGRATION_PROMPT.read_text(encoding="utf-8"))

    def test_p05_visual_scope_avoids_broad_ui_ux_globs(self) -> None:
        manifest = self.load_manifest()
        p05 = next(part for part in manifest["parts"] if part["part_id"] == "P05")
        for broad in ("docs/knowledge/game-development/*UI*", "docs/knowledge/game-development/UI_*", "docs/knowledge/game-development/*UX*"):
            self.assertNotIn(broad, p05["owned_write_paths"])
        self.assertIn("docs/knowledge/game-development/UI_UX_VISUAL_DESIGN_RULEBOOK.md", p05["owned_write_paths"])
        self.assertIn("docs/knowledge/game-development/UX_LAWS_COMPLETENESS_MATRIX.md", p05["owned_write_paths"])

    def test_each_part_has_a_context_pack_and_operational_contract(self) -> None:
        manifest = self.load_manifest()
        for part in manifest["parts"]:
            self.assertTrue((ROOT / part["context_pack"]).exists(), part["part_id"])
            for field in ("purpose", "owned_write_paths", "read_only_dependencies", "important_rules", "owned_skill_ids", "modules", "validation", "acceptance_criteria", "revisit_conditions"):
                self.assertTrue(part[field], f"{part['part_id']} missing {field}")

    def test_responsibility_clusters_and_integration_order_are_explicit(self) -> None:
        manifest = self.load_manifest()
        groups = manifest["responsibility_clusters"]
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
        self.assertIn("BASE_GOVERNANCE = GPT", worker)
        self.assertIn("CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR", worker)
        self.assertIn("사용자 학습형 완료보고", worker)
        self.assertIn("CURRENT_COORDINATOR_CHAT", integration)

    def test_operating_model_compares_real_execution_strategies_and_records_revisit_conditions(self) -> None:
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        for term in ("A · 9개 별도 채팅 유지", "B · 한 coordinator 채팅", "C · Part 자체 제거", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토"):
            self.assertIn(term, text)
        self.assertIn("새 Part 채팅을 9개 만들지 않는다", text)
        self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", text)

    def test_scope_checker_declares_worker_and_integration_modes(self) -> None:
        text = SCOPE_CHECKER.read_text(encoding="utf-8")
        self.assertIn("--part", text)
        self.assertIn("--integration", text)
        self.assertIn("--coordinator", text)
        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)
        self.assertIn("CONTROL_PLANE_COORDINATOR_WRITE", text)
        self.assertIn("SEMANTIC_OWNER:", text)
        self.assertIn("OUT_OF_PARTITION_WRITE", text)
        self.assertIn("semantic path overlap", text)
        self.assertIn("ACTIVE skills missing partition owner", text)

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
        coordinator = self.run_scope("--coordinator", "--files", "AGENTS.md", "skills/designing-vertical-slices/SKILL.md")
        self.assertEqual(0, coordinator.returncode, coordinator.stdout + coordinator.stderr)
        self.assertIn("CONTROL_PLANE_COORDINATOR_WRITE", coordinator.stdout)
        self.assertIn("SEMANTIC_OWNER:P04", coordinator.stdout)
        integration = self.run_scope("--integration", "--files", "AGENTS.md", "skills/designing-vertical-slices/SKILL.md")
        self.assertEqual(0, integration.returncode, integration.stdout + integration.stderr)

    def test_manifest_retirement_and_unassigned_path_policy_fail_closed(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual("COORDINATOR_REVIEW_WITH_SEMANTIC_OWNER_ATTRIBUTION", manifest["unassigned_path_policy"])
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
