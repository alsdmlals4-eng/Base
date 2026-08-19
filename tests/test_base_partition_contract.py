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
AGENTS = ROOT / "AGENTS.md"
ADVERSARIAL_SKILL = ROOT / "skills" / "running-adversarial-review-and-refinement" / "SKILL.md"
WORKSPACE_AUTHORITY = ROOT / "docs" / "operations" / "PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
PROJECT_OS_SKILL = ROOT / "skills" / "managing-game-project-operating-system" / "SKILL.md"


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

    def test_manifest_uses_one_base_plus_nine_responsibility_views(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual("BASE_PARTITION_OPERATING_MODEL_V1", manifest["contract_id"])
        self.assertEqual("HYBRID_CONTROL_PLANE_END_TO_END_CAPABILITY_PARTITIONS", manifest["selected_strategy"])
        self.assertEqual(9, len(manifest["parts"]))
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], [p["part_id"] for p in manifest["parts"]])
        self.assertEqual("INTEGRATION_ONLY", manifest["control_plane"]["write_authority"])
        mode = manifest["operating_mode"]
        self.assertEqual("UNIFIED_BASE", mode["daily_default"])
        self.assertTrue(mode["integration_returns_to_one_base"])

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

    def test_single_coordinator_chat_runs_p01_to_p09_sequentially(self) -> None:
        manifest = self.load_manifest()
        execution = manifest["execution_model"]
        self.assertEqual("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", execution["policy"])
        self.assertEqual("CURRENT_COORDINATOR_CHAT", execution["chat"])
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], execution["part_order"])
        self.assertEqual("SEQUENTIAL_CHECKPOINTS", execution["part_progression"])
        self.assertEqual("FOCUS_AND_ATTRIBUTION_VIEW", execution["partition_semantics"])
        self.assertEqual(0, execution["required_new_part_chats"])
        for text in (
            OPERATING_MODEL.read_text(encoding="utf-8"),
            WORKER_PROMPT.read_text(encoding="utf-8"),
            INTEGRATION_PROMPT.read_text(encoding="utf-8"),
        ):
            self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", text)
            self.assertIn("P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09", text)

    def test_part_boundary_is_focus_not_cross_part_repair_prohibition(self) -> None:
        manifest = self.load_manifest()
        execution = manifest["execution_model"]
        self.assertEqual("PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION", execution["cross_part_repair_policy"])
        self.assertEqual("ACTUAL_ACTIVE_OWNERSHIP_ONLY", execution["foreign_workstream_protection_basis"])
        self.assertTrue(execution["coordinator_can_repair_cross_part"])
        self.assertIn("semantic owner", " ".join(execution["cross_part_repair_conditions"]))
        model = OPERATING_MODEL.read_text(encoding="utf-8")
        worker = WORKER_PROMPT.read_text(encoding="utf-8")
        self.assertIn("PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION", model)
        self.assertIn("PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION", worker)
        self.assertIn("다른 Part라는 이유만으로", worker)

    def test_open_pr_is_not_automatically_active_ownership(self) -> None:
        manifest = self.load_manifest()
        execution = manifest["execution_model"]
        self.assertEqual("OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP", execution["open_pr_policy"])
        self.assertEqual("ACTUAL_ACTIVE_OWNERSHIP_ONLY", execution["foreign_workstream_protection_basis"])
        self.assertEqual("CURRENT_CHAT_ONLY_WHEN_USER_CONFIRMS", execution["single_chat_override"])
        for text in (
            AGENTS.read_text(encoding="utf-8"),
            OPERATING_MODEL.read_text(encoding="utf-8"),
            WORKER_PROMPT.read_text(encoding="utf-8"),
            INTEGRATION_PROMPT.read_text(encoding="utf-8"),
        ):
            self.assertIn("OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP", text)
            self.assertIn("실제 활성", text)

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
            self.assertIn("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", text)

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

    def test_sequential_order_and_integration_order_are_explicit(self) -> None:
        manifest = self.load_manifest()
        self.assertEqual([f"P{i:02d}" for i in range(1, 10)], manifest["execution_model"]["part_order"])
        self.assertTrue(manifest["integration"]["ordered_steps"])
        self.assertIn("P01..P09 sequential checkpoints", " ".join(manifest["integration"]["ordered_steps"]))

    def test_prompts_require_minimum_five_then_until_clean(self) -> None:
        worker = WORKER_PROMPT.read_text(encoding="utf-8")
        integration = INTEGRATION_PROMPT.read_text(encoding="utf-8")
        for text in (worker, integration):
            self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", text)
            self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", text)
            self.assertIn("CLEAN_REVIEW_EXIT", text)
            self.assertIn("FULL_LOOP_IS_NOT_A_REVIEW_LENS", text)
        self.assertIn("OPTIONAL_CODEX_EXECUTOR", worker)
        self.assertIn("사용자 학습형", worker)
        self.assertIn("CURRENT_COORDINATOR_CHAT", integration)

    def test_full_adversarial_loop_cannot_be_counted_as_one_review_lens(self) -> None:
        for adversarial in (
            AGENTS.read_text(encoding="utf-8"),
            ADVERSARIAL_SKILL.read_text(encoding="utf-8"),
        ):
            for term in (
                "FULL_LOOP_IS_NOT_A_REVIEW_LENS",
                "관점 하나만 검사한 것은 full loop로 계수하지 않는다",
                "현행·정본·범위",
                "최소 3개 실질 대안",
                "attack",
                "validate-critique",
                "refine-approved-findings",
                "regression-recheck",
                "BETTER_ALTERNATIVE_SEARCH",
                "LONG_TERM_PLAN_FIT_RECHECK",
                "RE-ATTACK resulting state",
            ):
                self.assertIn(term, adversarial)
            for invalid in (
                "Loop 1 = scope",
                "Loop 2 = UX",
                "Loop 3 = consumer",
                "Loop 4 = alternatives",
                "Loop 5 = CI",
            ):
                self.assertIn(invalid, adversarial)

    def test_project_home_is_self_contained_for_human_understanding(self) -> None:
        contract = json.loads(WORKSPACE_AUTHORITY.read_text(encoding="utf-8"))
        self.assertEqual("SELF_CONTAINED_HUMAN_HOME", contract["project_home_contract"])
        self.assertTrue(contract["child_pages_optional_for_basic_understanding"])
        required = set(contract["project_home_required_sections"])
        self.assertTrue({
            "CURRENT_DIRECTION_STATUS",
            "PLAYER_OR_USER_PROMISE",
            "CORE_LOOP",
            "MAJOR_SYSTEMS_AND_CONNECTIONS",
            "UX_UI_AND_VISUAL_DIRECTION",
            "IMPLEMENTATION_RUNTIME_EVIDENCE",
            "IMPORTANT_DECISIONS",
            "RISKS_BLOCKERS",
            "NEXT_WORK",
        }.issubset(required))
        project_os = PROJECT_OS_SKILL.read_text(encoding="utf-8")
        for term in (
            "SELF_CONTAINED_HUMAN_HOME",
            "하위 페이지를 열지 않아도",
            "CORE_LOOP",
            "MAJOR_SYSTEMS_AND_CONNECTIONS",
            "IMPLEMENTATION_RUNTIME_EVIDENCE",
            "RISKS_BLOCKERS",
            "NEXT_WORK",
        ):
            self.assertIn(term, project_os)

    def test_operating_model_compares_four_real_strategies_and_records_revisit_conditions(self) -> None:
        text = OPERATING_MODEL.read_text(encoding="utf-8")
        for term in ("A · 디렉터리 계층 분할", "B · 기능/도메인 분할", "C · Control Plane + End-to-End Capability Partition", "D · 동적 의존성 그래프 재클러스터링", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토 조건"):
            self.assertIn(term, text)
        self.assertIn("한 채팅", text)
        self.assertIn("CURRENT_COORDINATOR_CHAT", text)

    def test_scope_checker_declares_worker_and_integration_modes(self) -> None:
        text = SCOPE_CHECKER.read_text(encoding="utf-8")
        self.assertIn("--part", text)
        self.assertIn("--integration", text)
        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)
        self.assertIn("OUT_OF_PARTITION_WRITE", text)
        self.assertIn("semantic path overlap", text)
        self.assertIn("ACTIVE skills missing partition owner", text)

    def run_scope(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCOPE_CHECKER), *args], cwd=ROOT, text=True, capture_output=True, check=False)

    def test_scope_checker_still_supports_part_attribution_and_coordinator_integration(self) -> None:
        allowed = self.run_scope("--part", "P01", "--files", "skills/managing-design-documents/SKILL.md")
        self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)
        integration = self.run_scope("--integration", "--files", "AGENTS.md", "skills/designing-vertical-slices/SKILL.md")
        self.assertEqual(0, integration.returncode, integration.stdout + integration.stderr)

    def test_manifest_retirement_and_unassigned_path_policy_fail_closed_for_unowned_external_work(self) -> None:
        manifest = self.load_manifest()
        surfaces = {item["surface"] for item in manifest["retirement_targets"]}
        for surface in ("Google Sheets", "Figma references/workflows", "external HTML visual/dashboard workspace", "custom local visual Tool/Hub", "QA Evidence Studio/local QA tooling"):
            self.assertIn(surface, surfaces)
        self.assertEqual("READ_ONLY_UNLESS_COORDINATOR_AUTHORIZED_OR_ACTIVE_WORKSTREAM_TRANSFERRED", manifest["unassigned_path_policy"])

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
